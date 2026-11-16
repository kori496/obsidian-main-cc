"""API de la interfaz gráfica.

La usan dos "puentes" con los mismos métodos:
  * pywebview (ventana nativa): window.pywebview.api.<metodo>(...)
  * servidor HTTP local (modo navegador y pruebas): POST /api/<metodo> con una lista JSON de argumentos.

Cada método devuelve un dict JSON: {"ok": True, ...} o {"ok": False, "error": "..."}.
Las operaciones con cada dispositivo se serializan con un candado, así la ventana
nunca se bloquea y nunca hay dos comandos a la vez al mismo periférico.
"""

from __future__ import annotations

import copy
import functools
import json
import os
import threading
import time
import traceback
from pathlib import Path

from .. import __version__
from .. import mouse_attackshark as ms
from .. import mouse_botones as mb
from .. import teclado_ajazz as tk
from ..hidutil import ErrorATKHUB

METODOS_PUBLICOS = (
    "info", "catalogo", "dispositivos", "teclado_leer", "teclado_aplicar",
    "mouse_leer", "mouse_aplicar", "mouse_macro", "mouse_restaurar_botones", "guardar_preferencias",
)


def _carpeta_datos() -> Path:
    base = os.environ.get("APPDATA") or os.path.join(Path.home(), ".config")
    p = Path(base) / "ATKHUB"
    p.mkdir(parents=True, exist_ok=True)
    return p


TECLADO_DEFECTO = {"efecto": 8, "brillo": 5, "velocidad": 4, "color": 7, "direccion": 0, "suspension": "15"}


def _api(fn):
    @functools.wraps(fn)
    def envoltura(self, *args):
        try:
            res = fn(self, *args)
            return {"ok": True, **(res or {})}
        except ErrorATKHUB as e:
            return {"ok": False, "error": str(e)}
        except OSError as e:
            return {"ok": False, "error": f"Error de comunicación con el dispositivo: {e}. "
                                          "Si es el mouse, muévelo para despertarlo y reintenta."}
        except Exception as e:  # noqa: BLE001 - la ventana debe recibir siempre una respuesta
            traceback.print_exc()
            return {"ok": False, "error": f"Error inesperado: {e}"}
    return envoltura


class API:
    def __init__(self, simular: bool = False, carpeta: Path | None = None):
        self.simular = simular
        self._candado_teclado = threading.Lock()
        self._candado_mouse = threading.Lock()
        self._archivo = (carpeta or _carpeta_datos()) / ("estado_simulado.json" if simular else "estado.json")
        self._local = self._cargar()
        self._mouse_sim: dict | None = None

    # -- estado local (lo que el teclado no deja leer + preferencias de la ventana) --

    def _cargar(self) -> dict:
        try:
            datos = json.loads(self._archivo.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            datos = {}
        datos.setdefault("teclado", dict(TECLADO_DEFECTO))
        datos.setdefault("preferencias", {"vista_previa": True, "historial_colores": []})
        return datos

    def _guardar(self) -> None:
        try:
            self._archivo.write_text(json.dumps(self._local, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError:
            pass

    # -- general ----------------------------------------------------------------

    @_api
    def info(self):
        return {"version": __version__, "simular": self.simular,
                "preferencias": self._local["preferencias"]}

    @_api
    def guardar_preferencias(self, prefs: dict):
        permitidas = {"vista_previa", "historial_colores"}
        self._local["preferencias"].update({k: v for k, v in prefs.items() if k in permitidas})
        self._guardar()

    @_api
    def catalogo(self):
        return {
            "teclado": {
                "efectos": [{"id": m, "slug": slug, "nombre": n, "direccion": d, "color": c}
                            for m, (slug, n, d, c) in tk.EFECTOS.items()],
                "colores": tk.COLORES,
                "suspension": list(tk.SUSPENSION),
            },
            "mouse": {
                "modos_luz": [{"id": m, "slug": slug, "nombre": n} for m, (slug, n) in ms.MODOS_LUZ.items()],
                "colores": {k: "#%02X%02X%02X" % v for k, v in ms.COLORES_NOMBRE.items()},
                "polling": sorted(ms.TASA_A_BYTE),
                "botones": [{"id": b, "slot": s, "nombre": n} for b, (s, n) in mb.BOTONES.items()],
                "acciones": [{"id": a, "nombre": d} for a, (_, d) in mb.ACCIONES.items()],
                "modos_macro": list(mb.MODOS_MACRO),
            },
        }

    @_api
    def dispositivos(self):
        if self.simular:
            return {"teclado": {"conectado": True, "conexion": "simulado"},
                    "mouse": {"conectado": True, "conexion": "simulado"}}
        kb = tk.encontrar()
        par = ms.encontrar()
        return {
            "teclado": {"conectado": kb is not None, "conexion": tk.PIDS.get(kb["product_id"]) if kb else None},
            "mouse": {"conectado": par is not None,
                      "conexion": ms.PIDS.get(par[0]["product_id"]) if par else None},
        }

    # -- teclado ----------------------------------------------------------------

    @_api
    def teclado_leer(self):
        with self._candado_teclado, tk.TecladoAjazz(simular=self.simular) as kb:
            e = kb.estado()
            return {
                "conexion": kb.conexion,
                "bateria": e.bateria if e else None,
                "energia": tk.ESTADOS_ENERGIA.get(e.energia) if e else None,
                "config": self._local["teclado"],
            }

    @_api
    def teclado_aplicar(self, cfg: dict):
        actual = self._local["teclado"]
        nuevo = {**actual, **{k: cfg[k] for k in TECLADO_DEFECTO if k in cfg}}
        nuevo["efecto"] = int(nuevo["efecto"])
        if nuevo["efecto"] not in tk.EFECTOS:
            raise ErrorATKHUB("Efecto inválido")
        if str(nuevo["suspension"]) not in tk.SUSPENSION:
            raise ErrorATKHUB("Suspensión inválida")
        luz = ("efecto", "brillo", "velocidad", "color", "direccion")
        with self._candado_teclado, tk.TecladoAjazz(simular=self.simular) as kb:
            if any(nuevo[k] != actual.get(k) for k in luz) or cfg.get("forzar"):
                kb.luz(nuevo["efecto"], int(nuevo["brillo"]), int(nuevo["velocidad"]),
                       int(nuevo["direccion"]), int(nuevo["color"]))
            if str(nuevo["suspension"]) != str(actual.get("suspension")) or cfg.get("forzar"):
                kb.suspension(tk.SUSPENSION[str(nuevo["suspension"])])
        self._local["teclado"] = nuevo
        self._guardar()
        return {"config": nuevo}

    # -- mouse ------------------------------------------------------------------

    @staticmethod
    def _estado_mouse(m: ms.MouseAttackShark, bateria: bool) -> dict:
        polling = m.polling()
        time.sleep(ms.PAUSA_ENTRE_COMANDOS)
        etapas, actual = m.dpi()
        time.sleep(ms.PAUSA_ENTRE_COMANDOS)
        luz = m.luz()
        time.sleep(ms.PAUSA_ENTRE_COMANDOS)
        botones = m.botones()
        bat = m.bateria(espera=0.8) if bateria else None
        return {
            "conexion": m.conexion,
            "polling": polling,
            "dpi": {"etapas": [{"numero": e.numero, "dpi": e.dpi, "activa": e.activa,
                                "color": "#%02X%02X%02X" % e.color} for e in etapas],
                    "actual": actual},
            "luz": {"modo": luz.modo, "color": "#%02X%02X%02X" % luz.color, "brillo": luz.brillo,
                    "velocidad": luz.velocidad},
            "suspension": {"normal": luz.sueno_min, "profunda": luz.sueno_profundo_min},
            "respuesta_ms": luz.respuesta_ms,
            "botones": {b: _accion_a_dict(*a) for b, a in botones.items()},
            "bateria": {"porcentaje": bat[0], "estado": bat[1]} if bat else None,
        }

    @_api
    def mouse_leer(self):
        with self._candado_mouse:
            if self.simular and self._mouse_sim is not None:
                return copy.deepcopy(self._mouse_sim)
            with ms.MouseAttackShark(simular=self.simular) as m:
                estado = self._estado_mouse(m, bateria=True)
            if self.simular:
                self._mouse_sim = estado
            return copy.deepcopy(estado)

    @_api
    def mouse_aplicar(self, cambios: dict):
        """cambios: polling, dpi {etapa: valor}, luz {modo, color, brillo, velocidad},
        suspension {normal, profunda}, botones {boton: accion}."""
        hechos, sin_confirmar = [], []

        def anotar(nombre, ok):
            if ok is False:
                raise ErrorATKHUB(f"El mouse rechazó el cambio de {nombre}.")
            (hechos if ok else sin_confirmar).append(nombre)

        with self._candado_mouse, ms.MouseAttackShark(simular=self.simular) as m:
            if "polling" in cambios:
                anotar("polling", m.set_polling(int(cambios["polling"])))
            if cambios.get("dpi"):
                anotar("DPI", m.set_dpis({int(k): int(v) for k, v in cambios["dpi"].items()}))
            luz = dict(cambios.get("luz") or {})
            if luz or cambios.get("suspension"):
                args = {}
                if "modo" in luz:
                    args["modo"] = int(luz["modo"])
                if "color" in luz:
                    args["color"] = ms.leer_color(luz["color"])
                if "brillo" in luz:
                    args["brillo"] = int(luz["brillo"])
                if "velocidad" in luz:
                    args["velocidad"] = int(luz["velocidad"])
                sus = cambios.get("suspension") or {}
                if "normal" in sus:
                    args["sueno"] = float(sus["normal"])
                if "profunda" in sus:
                    args["sueno_profundo"] = int(sus["profunda"])
                anotar("luz y suspensión", m.set_luz(**args))
            if cambios.get("botones"):
                acciones = {}
                for boton, texto in cambios["botones"].items():
                    accion = mb.leer_accion(texto)
                    if boton == "izquierdo" and accion[0] != mb.ACCIONES["clic-izq"][0] \
                            and not cambios.get("forzar_izquierdo"):
                        raise ErrorATKHUB("Cambiar el clic izquierdo puede dejarte sin clic. "
                                          "Confírmalo en la ventana para continuar.")
                    acciones[boton] = accion
                anotar("botones", m.set_botones(acciones))
        if self.simular:
            if self._mouse_sim is None:
                with ms.MouseAttackShark(simular=True) as m:
                    self._mouse_sim = self._estado_mouse(m, bateria=True)
            self._actualizar_sim(cambios)
        return {"hechos": hechos, "sin_confirmar": sin_confirmar}

    def _actualizar_sim(self, c: dict) -> None:
        s = self._mouse_sim
        if "polling" in c:
            s["polling"] = int(c["polling"])
        for etapa, valor in (c.get("dpi") or {}).items():
            s["dpi"]["etapas"][int(etapa) - 1]["dpi"] = int(valor)
        s["luz"].update(c.get("luz") or {})
        s["suspension"].update(c.get("suspension") or {})
        for boton, texto in (c.get("botones") or {}).items():
            s["botones"][boton] = _accion_a_dict(*mb.leer_accion(texto))

    @_api
    def mouse_macro(self, numero: int, secuencia: str, modo: str = "veces", veces: int = 1,
                    boton: str | None = None):
        pasos = mb.leer_secuencia(secuencia)
        paquetes = mb.paquetes_macro(int(numero), pasos, modo, int(veces), f"ATKHUB {numero}")
        with self._candado_mouse, ms.MouseAttackShark(simular=self.simular) as m:
            ok = m.set_macro(paquetes)
            if ok is False:
                raise ErrorATKHUB("El mouse rechazó la macro.")
            if boton:
                time.sleep(ms.PAUSA_ENTRE_COMANDOS)
                if m.set_boton(boton, (mb.ACCION_MACRO, 0, int(numero))) is False:
                    raise ErrorATKHUB("La macro se guardó, pero el mouse rechazó asignarla al botón.")
        if self.simular and self._mouse_sim is not None and boton:
            self._mouse_sim["botones"][boton] = _accion_a_dict(mb.ACCION_MACRO, 0, int(numero))
        return {"pasos": mb.describir_secuencia(pasos)}

    @_api
    def mouse_restaurar_botones(self):
        with self._candado_mouse, ms.MouseAttackShark(simular=self.simular) as m:
            if m.restaurar_botones() is False:
                raise ErrorATKHUB("El mouse rechazó restaurar los botones.")
        if self.simular and self._mouse_sim is not None:
            for b, a in mb.botones_desde_lectura(mb.LECTURA_POR_DEFECTO).items():
                self._mouse_sim["botones"][b] = _accion_a_dict(*a)


def _accion_a_dict(accion: int, mods: int, tecla: int) -> dict:
    """Acción del firmware -> texto que entiende leer_accion() + descripción."""
    if accion == mb.ACCION_TECLA:
        texto = "tecla:" + mb.describir(accion, mods, tecla)[len("tecla "):]
    elif accion == mb.ACCION_MACRO:
        texto = f"macro:{tecla}"
    else:
        texto = mb.NOMBRE_POR_CODIGO.get(accion, f"0x{accion:02X}")
    return {"id": texto, "texto": mb.describir(accion, mods, tecla)}
