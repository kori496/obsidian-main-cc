"""Mouse Attack Shark X11.

Protocolo tomado de attack-shark-x11-driver (HarukaYamamoto0, licencia MIT).
La configuración va por reportes "feature" en la interfaz 2 (colección con
usage page 0x0B). Las confirmaciones y la batería llegan como mensajes de 5
bytes por la colección de eventos (usage page 0x0A) de la misma interfaz.

SEGURIDAD: escribir el reporte 0x10, con cualquier contenido, reinicia el X11
en su bootloader y lo deja trabado. Por eso solo se permiten los reportes de
REPORTES_PERMITIDOS y cualquier otro se rechaza antes de enviarse.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from . import mouse_botones as mb
from .dpi_tabla import DPI_3311
from .hidutil import ErrorATKHUB, abrir, enumerar, hexa, vaciar

VID = 0x1D57
PIDS = {0xFA60: "dongle 2.4G", 0xFA55: "cable USB"}
PID_CABLE = 0xFA55
INTERFAZ = 2
USAGE_PAGE_COMANDOS = 0x0B
USAGE_PAGE_EVENTOS = 0x0A

R_DPI, LARGO_DPI = 0x04, 0x38
R_LUZ, LARGO_LUZ = 0x05, 0x0F
R_POLLING, LARGO_POLLING = 0x06, 0x09
R_PERMISO = 0xA0

# Los únicos reportes que ATKHUB escribe (los mismos que el driver de referencia).
REPORTES_PERMITIDOS = frozenset({0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0xA0})

TASA_A_BYTE = {125: 0x08, 250: 0x04, 500: 0x02, 1000: 0x01}
BYTE_A_TASA = {v: k for k, v in TASA_A_BYTE.items()}

MSG_BATERIA = (0x40, 0x41)
MSG_CONFIRMACION = 0x50
ESTADO_BATERIA = {0x01: "normal", 0x02: "carga completa", 0x03: "cargando"}

PAUSA_ENTRE_COMANDOS = 0.3  # el driver de referencia recomienda 250-300 ms
INTENTOS_PERMISO = 3

# Paquete DPI por defecto del driver de referencia (para el modo simular).
# El checksum de los bytes 50-51 se recalcula abajo.
_DPI_BASE = bytearray([
    0x04, 0x38, 0x01, 0x00, 0x01, 0x3F, 0x20, 0x20,
    0x12, 0x25, 0x38, 0x4B, 0x75, 0x81, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00,
    0x02,
    0xFF, 0x00, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0x00,
    0x00, 0xFF, 0xFF, 0xFF, 0x00, 0xFF, 0xFF, 0x40, 0x00, 0xFF, 0xFF, 0xFF,
    0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
])
_suma = sum(_DPI_BASE[3:50])
_DPI_BASE[50], _DPI_BASE[51] = _suma >> 8, _suma & 0xFF
DPI_POR_DEFECTO = bytes(_DPI_BASE)


# -- DPI ---------------------------------------------------------------------

def dpi_a_bytes(valor: int) -> tuple[int, int]:
    """DPI -> (byte bajo, byte alto), igual que convertDpiToBytes del driver."""
    if valor < 0:
        raise ErrorATKHUB(f"DPI inválido: {valor}")
    v = max(valor, 50)
    dpi = v
    if 24_100 <= v <= 25_000:
        dpi = max(8_000, min(8_500, round(v / 3)))
    elif v > 24_000:
        dpi = 8_500
    elif v > 12_000:
        dpi = round(v / 2)
    if dpi <= 10_000:
        dpi = min(10_000, max(50, round(dpi / 50) * 50))
        indice, alto = (dpi - 50) // 50, 0
    else:
        dpi = max(10_100, round(dpi / 100) * 100)
        indice, alto = 200 + (dpi - 10_100) // 100, 1
    if not 0 <= indice < len(DPI_3311):
        raise ErrorATKHUB(f"DPI no soportado: {valor}")
    return DPI_3311[indice], alto


def bytes_a_dpi(bajo: int, alto: int, doble: bool) -> int:
    """(byte bajo, byte alto, bandera doble) -> DPI, igual que convertBytesToDpi."""
    if bajo == 0 and alto == 0:
        return 0
    i = DPI_3311.index(bajo) if bajo in DPI_3311 else -1
    if alto == 0:
        dpi = i * 50 + 50 if i != -1 else 50
    elif alto == 1:
        dpi = i * 100 + 100 if i != -1 else 100
    else:
        dpi = 10_100 + (((alto << 8) | bajo) - 199) * 100
    if doble:
        if bajo == 0xEB:
            return 20_100
        dpi *= 2
    return min(dpi, 26_000)


def checksum_dpi(p: bytes | bytearray) -> int:
    return sum(p[3:50]) & 0xFFFF


def poner_dpi_en_paquete(p: bytearray, etapa: int, valor: int) -> None:
    """Cambia una etapa (1-8) de un paquete DPI de 56 bytes y recalcula el checksum."""
    if not 1 <= etapa <= 8:
        raise ErrorATKHUB("La etapa va de 1 a 8")
    i = etapa - 1
    bajo, alto = dpi_a_bytes(valor)
    p[8 + i], p[16 + i] = bajo, alto
    doble, triple = p[6], p[7]
    if 12_000 < valor < 24_000:
        doble |= 1 << i
    else:
        doble &= ~(1 << i) & 0xFF
    if 24_100 <= valor <= 25_000:
        triple |= 1 << i
    else:
        triple &= ~(1 << i) & 0xFF
    p[6], p[7] = doble, triple
    suma = checksum_dpi(p)
    p[50], p[51] = suma >> 8, suma & 0xFF


@dataclass
class EtapaDPI:
    numero: int
    dpi: int
    color: tuple[int, int, int]
    activa: bool


def leer_paquete_dpi(p: bytes) -> tuple[list[EtapaDPI], int]:
    """Devuelve (etapas, etapa actual). Verifica el checksum."""
    if len(p) < 52:
        raise ErrorATKHUB(f"Respuesta DPI muy corta ({len(p)} bytes)")
    esperado = (p[50] << 8) | p[51]
    if checksum_dpi(p) != esperado:
        raise ErrorATKHUB("La respuesta DPI llegó con checksum incorrecto; no la uso.")
    etapas = []
    for i in range(8):
        etapas.append(EtapaDPI(
            numero=i + 1,
            dpi=bytes_a_dpi(p[8 + i], p[16 + i], bool(p[6] & (1 << i))),
            color=(p[25 + 3 * i], p[26 + 3 * i], p[27 + 3 * i]),
            activa=bool(p[5] & (1 << i)),
        ))
    return etapas, p[24]


def paquete_polling(hz: int, perfil: int = 1) -> bytes:
    if hz not in TASA_A_BYTE:
        raise ErrorATKHUB("Polling rate válido: 125, 250, 500 o 1000")
    b = TASA_A_BYTE[hz]
    return bytes([R_POLLING, LARGO_POLLING, perfil, b, b ^ 0xFF, 0, 0, 0, 0])


# -- luz y preferencias (reporte 0x05) -------------------------------------
# Byte 3: modo (nibble alto) · 4: sueño profundo alto | velocidad · 5: sueño profundo bajo | brillo
# 6-8: R G B · 9: sueño normal (min * 2) · 10: respuesta de botones (ms / 2) · 11-12: checksum

MODOS_LUZ = {
    0: ("apagado", "Apagado"),
    1: ("fijo", "Color fijo"),
    2: ("respiracion", "Respiración"),
    3: ("neon", "Neón (arcoíris)"),
    4: ("respiracion-color", "Respiración cambiando de color"),
    5: ("fijo-dpi", "Fijo con el color de la etapa DPI"),
    6: ("respiracion-dpi", "Respiración con el color de la etapa DPI"),
}
COLORES_NOMBRE = {
    "rojo": (255, 0, 0), "verde": (0, 255, 0), "azul": (0, 0, 255),
    "amarillo": (255, 255, 0), "magenta": (255, 0, 255), "cian": (0, 255, 255),
    "blanco": (255, 255, 255), "naranja": (255, 64, 0), "morado": (128, 0, 255),
    "rosa": (255, 60, 150),
}


def buscar_modo_luz(nombre: str) -> int:
    n = nombre.strip().lower()
    if n.isdigit() and int(n) in MODOS_LUZ:
        return int(n)
    for modo, (slug, _) in MODOS_LUZ.items():
        if slug == n:
            return modo
    raise ErrorATKHUB(f"Modo de luz desconocido: '{nombre}'. Mira la lista con:  atkhub mouse modos")


def leer_color(texto: str) -> tuple[int, int, int]:
    t = texto.strip().lower()
    if t in COLORES_NOMBRE:
        return COLORES_NOMBRE[t]
    h = t.lstrip("#")
    if len(h) == 6:
        try:
            return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        except ValueError:
            pass
    raise ErrorATKHUB(f"Color inválido: '{texto}'. Usa hex sin # (ej. C8B49A) o: {', '.join(COLORES_NOMBRE)}")


def checksum_luz(p: bytes | bytearray) -> int:
    return sum(p[3:11]) & 0xFFFF


@dataclass
class Luz:
    modo: int
    color: tuple[int, int, int]
    brillo: int
    velocidad: int
    sueno_min: float
    sueno_profundo_min: int
    respuesta_ms: int

    def texto(self) -> str:
        r, g, b = self.color
        return (f"{MODOS_LUZ.get(self.modo, (None, f'modo {self.modo}'))[1]} · color #{r:02X}{g:02X}{b:02X}"
                f" · brillo {self.brillo}/8 · velocidad {self.velocidad}/5")


def leer_paquete_luz(p: bytes) -> Luz:
    if len(p) < 13:
        raise ErrorATKHUB(f"Respuesta de luz muy corta ({len(p)} bytes)")
    if checksum_luz(p) != (p[11] << 8) | p[12]:
        raise ErrorATKHUB("La respuesta de luz llegó con checksum incorrecto; no la uso.")
    return Luz(
        modo=p[3] >> 4,
        color=(p[6], p[7], p[8]),
        brillo=p[5] & 0x0F,
        velocidad=p[4] & 0x0F,
        sueno_min=p[9] / 2,
        sueno_profundo_min=(p[4] & 0xF0) | (p[5] >> 4),
        respuesta_ms=p[10] * 2,
    )


def modificar_paquete_luz(p: bytearray, modo=None, color=None, brillo=None, velocidad=None,
                          sueno=None, sueno_profundo=None) -> None:
    """Cambia solo los campos dados de un paquete 0x05 y recalcula el checksum."""
    if modo is not None:
        if modo not in MODOS_LUZ:
            raise ErrorATKHUB("Modo de luz fuera de rango")
        p[3] = (modo & 0x0F) << 4
    if color is not None:
        p[6], p[7], p[8] = (c & 0xFF for c in color)
    if brillo is not None:
        if not 1 <= brillo <= 8:
            raise ErrorATKHUB("El brillo del mouse va de 1 a 8")
        p[5] = (p[5] & 0xF0) | brillo
    if velocidad is not None:
        if not 1 <= velocidad <= 5:
            raise ErrorATKHUB("La velocidad va de 1 a 5")
        p[4] = (p[4] & 0xF0) | velocidad
    if sueno is not None:
        if not 0.5 <= sueno <= 30 or (sueno * 2) % 1:
            raise ErrorATKHUB("La suspensión normal va de 0.5 a 30 min, de media en media")
        p[9] = int(sueno * 2)
    if sueno_profundo is not None:
        if not 1 <= sueno_profundo <= 60:
            raise ErrorATKHUB("La suspensión profunda va de 1 a 60 min")
        p[4] = (sueno_profundo & 0xF0) | (p[4] & 0x0F)
        p[5] = ((sueno_profundo & 0x0F) << 4) | (p[5] & 0x0F)
    suma = checksum_luz(p)
    p[11], p[12] = suma >> 8, suma & 0xFF


# Paquete de luz por defecto del driver de referencia (para el modo simular).
_LUZ_BASE = bytearray([0x05, 0x0F, 0x01, 0x10, 0x03, 0xA8, 0x00, 0xFF, 0x00, 0x01, 0x04, 0, 0, 0, 0])
modificar_paquete_luz(_LUZ_BASE)
LUZ_POR_DEFECTO = bytes(_LUZ_BASE)


# -- dispositivo ---------------------------------------------------------------

def encontrar() -> tuple[dict, dict] | None:
    """Devuelve (colección de comandos, colección de eventos) del mouse."""
    devs = [d for d in enumerar() if d["vendor_id"] == VID and d["product_id"] in PIDS
            and d.get("interface_number") == INTERFAZ]
    devs.sort(key=lambda d: d["product_id"] != PID_CABLE)  # prefiere el cable
    for pid in dict.fromkeys(d["product_id"] for d in devs):
        cmd = next((d for d in devs if d["product_id"] == pid
                    and d.get("usage_page") == USAGE_PAGE_COMANDOS), None)
        ev = next((d for d in devs if d["product_id"] == pid
                   and d.get("usage_page") == USAGE_PAGE_EVENTOS), None)
        if cmd and ev:
            return cmd, ev
    return None


class MouseAttackShark:
    def __init__(self, simular: bool = False, log=None):
        self.simular = simular
        self.log = log
        self.cmd = self.ev = None
        self.pid = 0xFA60
        self.conexion = "simulado"
        if simular:
            return
        par = encontrar()
        if par is None:
            raise ErrorATKHUB(
                "No encontré el mouse Attack Shark X11 (1D57:FA60 por dongle o 1D57:FA55 por cable). "
                "¿Está conectado y encendido?"
            )
        info_cmd, info_ev = par
        self.pid = info_cmd["product_id"]
        self.conexion = PIDS[self.pid]
        self.cmd = abrir(info_cmd["path"])
        self.ev = abrir(info_ev["path"])

    def cerrar(self):
        for d in (self.cmd, self.ev):
            if d is not None:
                d.close()
        self.cmd = self.ev = None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.cerrar()

    # -- transporte --------------------------------------------------------

    def _escribir(self, buf: bytes):
        if not buf or buf[0] not in REPORTES_PERMITIDOS:
            raise ErrorATKHUB(f"Bloqueado: el reporte 0x{buf[0]:02X} no está en la lista segura.")
        if self.log:
            self.log(f"-> mouse: {hexa(buf)}")
        if self.simular:
            return
        vaciar(self.ev)  # descartar eventos viejos
        self.cmd.send_feature_report(list(buf))

    def _leer(self, reporte: int, largo: int, parametro: int = 0x01) -> bytes:
        """Pide permiso de lectura (0xA0) y lee un reporte. No cambia la configuración."""
        if self.simular:
            return {R_DPI: DPI_POR_DEFECTO, R_LUZ: LUZ_POR_DEFECTO,
                    mb.R_BOTONES: mb.LECTURA_POR_DEFECTO}.get(reporte, paquete_polling(1000))
        perm = b""
        for intento in range(1, INTENTOS_PERMISO + 1):
            self._escribir(bytes([R_PERMISO, reporte, largo, 0x00, parametro, 0, 0, 0]))
            time.sleep(0.25 * intento)  # por el dongle, cada intento espera más
            perm = bytes(self.cmd.get_feature_report(R_PERMISO, 8))
            if self.log:
                self.log(f"<- mouse (permiso, intento {intento}): {hexa(perm)}")
            if len(perm) >= 2 and perm[1] == 0x01:
                break
        else:
            raise ErrorATKHUB(
                f"El mouse no dio permiso para leer el reporte 0x{reporte:02X} "
                f"(respuesta: {hexa(perm) or 'vacía'}).\n"
                "Si está por el dongle, mueve el mouse justo antes del comando (se duerme a los "
                "30 s) y vuelve a intentar. Si sigue, córrelo con --debug y pásame la salida."
            )
        datos = bytes(self.cmd.get_feature_report(reporte, largo))
        if self.log:
            self.log(f"<- mouse: {hexa(datos)}")
        return datos

    def _esperar_confirmacion(self, reporte: int, espera: float = 1.0) -> bool | None:
        """True = aceptado, False = rechazado, None = no llegó confirmación."""
        if self.simular:
            return True
        limite = time.monotonic() + espera
        while (resta := limite - time.monotonic()) > 0:
            r = self.ev.read(64, max(1, int(resta * 1000)))
            if not r:
                continue
            if len(r) >= 5 and r[2] == MSG_CONFIRMACION and r[4] == reporte:
                return r[3] == 0x00
        return None

    def _enviar_comando(self, buf: bytes) -> bool | None:
        self._escribir(buf)
        ok = self._esperar_confirmacion(buf[0])
        time.sleep(PAUSA_ENTRE_COMANDOS)
        return ok

    # -- lectura -------------------------------------------------------------

    def polling(self) -> int:
        r = self._leer(R_POLLING, LARGO_POLLING)
        if len(r) < 4 or r[3] not in BYTE_A_TASA:
            raise ErrorATKHUB(f"Respuesta de polling rara: {hexa(r)}")
        return BYTE_A_TASA[r[3]]

    def paquete_dpi(self) -> bytearray:
        r = bytearray(self._leer(R_DPI, LARGO_DPI)[:LARGO_DPI])
        return r.ljust(LARGO_DPI, b"\x00")

    def dpi(self) -> tuple[list[EtapaDPI], int]:
        return leer_paquete_dpi(bytes(self.paquete_dpi()))

    def paquete_luz(self) -> bytearray:
        r = bytearray(self._leer(R_LUZ, LARGO_LUZ)[:LARGO_LUZ])
        return r.ljust(LARGO_LUZ, b"\x00")

    def luz(self) -> Luz:
        return leer_paquete_luz(bytes(self.paquete_luz()))

    def bateria(self, espera: float = 2.0) -> tuple[int, str] | None:
        """Escucha un mensaje de batería. El mouse lo manda solo, así que puede no llegar."""
        if self.simular:
            return 80, "normal"
        limite = time.monotonic() + espera
        while (resta := limite - time.monotonic()) > 0:
            r = self.ev.read(64, max(1, int(resta * 1000)))
            if r and len(r) >= 5 and r[2] in MSG_BATERIA:
                return r[4], ESTADO_BATERIA.get(r[3], f"estado {r[3]}")
        return None

    # -- escritura -----------------------------------------------------------

    def set_polling(self, hz: int) -> bool | None:
        return self._enviar_comando(paquete_polling(hz))

    def set_dpis(self, valores: dict[int, int]) -> bool | None:
        """Cambia varias etapas en una sola escritura: {etapa: dpi}."""
        p = self.paquete_dpi()
        leer_paquete_dpi(bytes(p))
        time.sleep(PAUSA_ENTRE_COMANDOS)
        p[0], p[1] = R_DPI, LARGO_DPI
        for etapa, valor in valores.items():
            poner_dpi_en_paquete(p, int(etapa), int(valor))
        buf = bytes(p[:51]) if self.pid == PID_CABLE else bytes(p)
        return self._enviar_comando(buf)

    def set_dpi(self, etapa: int, valor: int) -> bool | None:
        """Lee la configuración actual, cambia solo esa etapa y la vuelve a escribir."""
        p = self.paquete_dpi()
        leer_paquete_dpi(bytes(p))  # valida checksum antes de tocar nada
        time.sleep(PAUSA_ENTRE_COMANDOS)
        p[0], p[1] = R_DPI, LARGO_DPI
        poner_dpi_en_paquete(p, etapa, valor)
        buf = bytes(p[:51]) if self.pid == PID_CABLE else bytes(p)  # igual que el driver
        return self._enviar_comando(buf)

    def set_luz(self, **cambios) -> bool | None:
        """Lee la luz/suspensión actual, cambia solo lo pedido y la vuelve a escribir.

        cambios: modo, color, brillo, velocidad, sueno, sueno_profundo.
        """
        p = self.paquete_luz()
        leer_paquete_luz(bytes(p))  # valida checksum antes de tocar nada
        time.sleep(PAUSA_ENTRE_COMANDOS)
        p[0], p[1] = R_LUZ, LARGO_LUZ
        modificar_paquete_luz(p, **cambios)
        buf = bytes(p[:13]) if self.pid == PID_CABLE else bytes(p)  # igual que el driver
        return self._enviar_comando(buf)

    # -- botones y macros ------------------------------------------------------

    def paquete_botones(self) -> bytes:
        r = bytes(self._leer(mb.R_BOTONES, mb.LARGO_BOTONES, parametro=0x01)[:mb.LARGO_BOTONES])
        return r.ljust(mb.LARGO_BOTONES, b"\x00")

    def botones(self) -> dict[str, tuple[int, int, int]]:
        return mb.botones_desde_lectura(self.paquete_botones())

    def _escribir_botones(self, w: bytearray) -> bool | None:
        mb.verificar_seguro(w)
        return self._enviar_comando(bytes(w))

    def set_boton(self, boton: str, accion: tuple[int, int, int]) -> bool | None:
        """Lee los botones actuales, cambia solo ese y los vuelve a escribir."""
        w = mb.paquete_escritura_desde_lectura(self.paquete_botones())
        time.sleep(PAUSA_ENTRE_COMANDOS)
        mb.poner_boton(w, boton, accion)
        return self._escribir_botones(w)

    def set_botones(self, acciones: dict[str, tuple[int, int, int]]) -> bool | None:
        """Cambia varios botones en una sola escritura: {boton: (accion, mods, tecla)}."""
        w = mb.paquete_escritura_desde_lectura(self.paquete_botones())
        time.sleep(PAUSA_ENTRE_COMANDOS)
        for boton, accion in acciones.items():
            mb.poner_boton(w, boton, accion)
        return self._escribir_botones(w)

    def restaurar_botones(self) -> bool | None:
        return self._escribir_botones(mb.paquete_por_defecto())

    def set_macro(self, paquetes: list[bytes]) -> bool | None:
        resultado: bool | None = True
        for pkt in paquetes:
            ok = self._enviar_comando(pkt)
            if ok is False:
                return False
            if ok is None:
                resultado = None
        return resultado
