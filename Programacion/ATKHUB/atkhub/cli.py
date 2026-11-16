"""Línea de comandos de ATKHUB."""

from __future__ import annotations

import argparse
import sys
import time

from . import __version__, mouse_attackshark as ms, mouse_botones as mb, teclado_ajazz as tk
from .hidutil import ErrorATKHUB, enumerar

CONOCIDOS = {
    (tk.VID, pid): f"Teclado Ajazz AK820 Max ({c})" for pid, c in tk.PIDS.items()
} | {
    (ms.VID, pid): f"Mouse Attack Shark X11 ({c})" for pid, c in ms.PIDS.items()
}


# -- detectar ------------------------------------------------------------------

def cmd_detectar(a):
    if a.simular:
        print("(simulado) Teclado Ajazz AK820 Max (cable USB)  1A2C:A036")
        print("(simulado) Mouse Attack Shark X11 (dongle 2.4G)  1D57:FA60")
        return
    grupos: dict[tuple[int, int], list[dict]] = {}
    for d in enumerar():
        grupos.setdefault((d["vendor_id"], d["product_id"]), []).append(d)
    encontrados = [k for k in grupos if k in CONOCIDOS]
    if not encontrados:
        print("No encontré ningún periférico soportado.")
    for k in encontrados:
        print(f"[OK] {CONOCIDOS[k]}  {k[0]:04X}:{k[1]:04X}")
    if a.todo:
        print("\nTodos los dispositivos HID:")
        for (vid, pid), ds in sorted(grupos.items()):
            nombre = ds[0].get("product_string") or "?"
            print(f"  {vid:04X}:{pid:04X}  {nombre}")
            for d in ds:
                print(f"      interfaz {d.get('interface_number')}  "
                      f"usage_page 0x{d.get('usage_page', 0):04X}  usage 0x{d.get('usage', 0):02X}")


# -- teclado -------------------------------------------------------------------

def cmd_teclado_efectos(a):
    print("Efectos (nombre o número):")
    for modo, (slug, nombre, dirc, col) in tk.EFECTOS.items():
        extra = ", ".join(x for x, ok in (("dirección", dirc), ("color", col)) if ok)
        print(f"  {modo:>2}  {slug:<18} {nombre}" + (f"  [{extra}]" if extra else ""))
    print("\nColores:", ", ".join(tk.COLORES))


def cmd_teclado_estado(a):
    with tk.TecladoAjazz(simular=a.simular, log=a.log) as kb:
        e = kb.estado()
        print(f"Teclado Ajazz AK820 Max ({kb.conexion})")
        print(e.texto() if e else "El teclado no respondió al pedido de estado.")


def cmd_teclado_luz(a):
    modo = tk.buscar_efecto(a.efecto)
    color = tk.buscar_color(a.color)
    direccion = 1 if a.direccion == "der-izq" else 0
    with tk.TecladoAjazz(simular=a.simular, log=a.log) as kb:
        kb.luz(modo, a.brillo, a.velocidad, direccion, color)
    print(f"Luz: {tk.EFECTOS[modo][1]} · brillo {a.brillo} · velocidad {a.velocidad} · {a.color}")


def cmd_teclado_suspension(a):
    with tk.TecladoAjazz(simular=a.simular, log=a.log) as kb:
        kb.suspension(tk.SUSPENSION[a.minutos])
    print(f"Suspensión: {a.minutos}" + ("" if a.minutos == "nunca" else " min"))


# -- mouse ---------------------------------------------------------------------

def _confirmacion(ok):
    return {True: "el mouse lo confirmó", False: "el mouse lo RECHAZÓ",
            None: "enviado (no llegó confirmación)"}[ok]


def cmd_mouse_info(a):
    with ms.MouseAttackShark(simular=a.simular, log=a.log) as m:
        print(f"Mouse Attack Shark X11 ({m.conexion})")
        print(f"Polling rate: {m.polling()} Hz")
        etapas, actual = m.dpi()
        print("DPI:")
        for e in etapas:
            if e.dpi == 0:
                continue
            marca = "<- actual" if e.numero == actual else ""
            estado = "" if e.activa else "(desactivada)"
            r, g, b = e.color
            print(f"  etapa {e.numero}: {e.dpi:>6}  color #{r:02X}{g:02X}{b:02X} {estado}{marca}")
        luz = m.luz()
        print(f"Luz: {luz.texto()}")
        print(f"Suspensión: {luz.sueno_min:g} min · profunda: {luz.sueno_profundo_min} min"
              f" · respuesta de botones: {luz.respuesta_ms} ms")
        bat = m.bateria()
        print(f"Batería: {bat[0]} % ({bat[1]})" if bat else
              "Batería: no llegó el aviso (el mouse lo manda cada cierto tiempo).")


def cmd_mouse_modos(a):
    print("Modos de luz del mouse (nombre o número):")
    for modo, (slug, nombre) in ms.MODOS_LUZ.items():
        print(f"  {modo}  {slug:<18} {nombre}")
    print("\nColores: hex sin # (ej. C8B49A) o", ", ".join(ms.COLORES_NOMBRE))


def cmd_mouse_luz(a):
    cambios = {"modo": ms.buscar_modo_luz(a.modo)}
    if a.color:
        cambios["color"] = ms.leer_color(a.color)
    if a.brillo is not None:
        cambios["brillo"] = a.brillo
    if a.velocidad is not None:
        cambios["velocidad"] = a.velocidad
    with ms.MouseAttackShark(simular=a.simular, log=a.log) as m:
        ok = m.set_luz(**cambios)
    print(f"Luz del mouse: {ms.MODOS_LUZ[cambios['modo']][1]}: {_confirmacion(ok)}")


def cmd_mouse_suspension(a):
    if a.normal is None and a.profunda is None:
        raise ErrorATKHUB("Indica --normal MIN y/o --profunda MIN")
    with ms.MouseAttackShark(simular=a.simular, log=a.log) as m:
        ok = m.set_luz(sueno=a.normal, sueno_profundo=a.profunda)
    partes = [f"normal {a.normal:g} min" if a.normal is not None else "",
              f"profunda {a.profunda} min" if a.profunda is not None else ""]
    print(f"Suspensión del mouse ({', '.join(x for x in partes if x)}): {_confirmacion(ok)}")


def cmd_mouse_acciones(a):
    print("Botones:", ", ".join(mb.BOTONES))
    print("\nAcciones:")
    for nombre, (_, desc) in mb.ACCIONES.items():
        print(f"  {nombre:<20} {desc}")
    print("  tecla:ATAJO          un atajo de teclado, ej. tecla:ctrl+c, tecla:alt+f4, tecla:f5")
    print("  macro:N              ejecuta la macro N (1-16), ver: atkhub mouse macro")


def cmd_mouse_botones(a):
    with ms.MouseAttackShark(simular=a.simular, log=a.log) as m:
        if a.restaurar:
            print(f"Botones de fábrica: {_confirmacion(m.restaurar_botones())}")
            return
        for nombre, accion in m.botones().items():
            print(f"  {mb.BOTONES[nombre][1]:<20} ({nombre:<12}) -> {mb.describir(*accion)}")


def cmd_mouse_boton(a):
    accion = mb.leer_accion(a.accion)
    if a.boton == "izquierdo" and accion[0] != mb.ACCIONES["clic-izq"][0] and not a.forzar:
        raise ErrorATKHUB("Cambiar el clic izquierdo puede dejarte sin clic. Si estás seguro, "
                          "agrega --forzar (se arregla con: atkhub mouse botones --restaurar)")
    with ms.MouseAttackShark(simular=a.simular, log=a.log) as m:
        ok = m.set_boton(a.boton, accion)
    print(f"{mb.BOTONES[a.boton][1]} -> {mb.describir(*accion)}: {_confirmacion(ok)}")


def cmd_mouse_macro(a):
    pasos = mb.leer_secuencia(a.secuencia, a.espera)
    paquetes = mb.paquetes_macro(a.numero, pasos, a.modo, a.veces, a.nombre)
    print(f"Macro {a.numero}: {mb.describir_secuencia(pasos)}")
    with ms.MouseAttackShark(simular=a.simular, log=a.log) as m:
        ok = m.set_macro(paquetes)
        print(f"Guardar macro {a.numero}: {_confirmacion(ok)}")
        if a.boton and ok is not False:
            time.sleep(ms.PAUSA_ENTRE_COMANDOS)
            ok2 = m.set_boton(a.boton, (mb.ACCION_MACRO, 0, a.numero))
            print(f"{mb.BOTONES[a.boton][1]} -> macro {a.numero}: {_confirmacion(ok2)}")


def cmd_mouse_polling(a):
    with ms.MouseAttackShark(simular=a.simular, log=a.log) as m:
        ok = m.set_polling(a.hz)
    print(f"Polling rate {a.hz} Hz: {_confirmacion(ok)}")


def cmd_mouse_dpi(a):
    with ms.MouseAttackShark(simular=a.simular, log=a.log) as m:
        ok = m.set_dpi(a.etapa, a.valor)
    print(f"Etapa {a.etapa} = {a.valor} DPI: {_confirmacion(ok)}")


# -- argumentos ----------------------------------------------------------------

def cmd_gui(a):
    from .gui.app import lanzar
    lanzar(simular=a.simular, navegador=a.navegador, puerto=a.puerto)


def construir_parser() -> argparse.ArgumentParser:
    comun = argparse.ArgumentParser(add_help=False)
    comun.add_argument("--simular", action="store_true",
                       help="no toca ningún dispositivo; muestra lo que se enviaría")
    comun.add_argument("--debug", action="store_true", help="muestra los bytes enviados y recibidos")

    p = argparse.ArgumentParser(prog="atkhub",
                                description=f"ATKHUB {__version__}: hub para tus periféricos")
    sub = p.add_subparsers(dest="grupo", required=True)

    g = sub.add_parser("gui", parents=[comun], help="abre la interfaz gráfica")
    g.add_argument("--navegador", action="store_true", help="abrir en el navegador en vez de ventana")
    g.add_argument("--puerto", type=int, default=0, help="puerto local (0 = cualquiera)")
    g.set_defaults(func=cmd_gui)

    d = sub.add_parser("detectar", parents=[comun], help="lista los periféricos conectados")
    d.add_argument("--todo", action="store_true", help="muestra también todos los HID")
    d.set_defaults(func=cmd_detectar)

    t = sub.add_parser("teclado", help="teclado Ajazz AK820 Max").add_subparsers(dest="accion", required=True)
    t.add_parser("estado", parents=[comun], help="batería (solo lectura)").set_defaults(func=cmd_teclado_estado)
    t.add_parser("efectos", parents=[comun], help="lista efectos y colores").set_defaults(func=cmd_teclado_efectos)
    luz = t.add_parser("luz", parents=[comun], help="cambia el efecto de luz")
    luz.add_argument("efecto", help="nombre o número (ver: atkhub teclado efectos)")
    luz.add_argument("--brillo", type=int, default=5, help="1-5 (5)")
    luz.add_argument("--velocidad", type=int, default=4, help="1-5 (4)")
    luz.add_argument("--color", default="arcoiris", help="rojo, verde, ..., arcoiris")
    luz.add_argument("--direccion", choices=["izq-der", "der-izq"], default="izq-der")
    luz.set_defaults(func=cmd_teclado_luz)
    su = t.add_parser("suspension", parents=[comun], help="tiempo para dormirse")
    su.add_argument("minutos", choices=list(tk.SUSPENSION))
    su.set_defaults(func=cmd_teclado_suspension)

    m = sub.add_parser("mouse", help="mouse Attack Shark X11").add_subparsers(dest="accion", required=True)
    m.add_parser("info", parents=[comun], help="polling, DPI, luz, suspensión y batería (solo lectura)").set_defaults(func=cmd_mouse_info)
    m.add_parser("modos", parents=[comun], help="lista los modos de luz y colores").set_defaults(func=cmd_mouse_modos)
    lu = m.add_parser("luz", parents=[comun], help="cambia la luz del mouse")
    lu.add_argument("modo", help="nombre o número (ver: atkhub mouse modos)")
    lu.add_argument("--color", help="hex sin # (ej. C8B49A) o nombre (rojo, azul, rosa...)")
    lu.add_argument("--brillo", type=int, help="1-8")
    lu.add_argument("--velocidad", type=int, help="1-5")
    lu.set_defaults(func=cmd_mouse_luz)
    m.add_parser("acciones", parents=[comun], help="lista botones y acciones").set_defaults(func=cmd_mouse_acciones)
    bt = m.add_parser("botones", parents=[comun], help="muestra qué hace cada botón")
    bt.add_argument("--restaurar", action="store_true", help="vuelve los botones a fábrica")
    bt.set_defaults(func=cmd_mouse_botones)
    b1 = m.add_parser("boton", parents=[comun], help="cambia lo que hace un botón")
    b1.add_argument("boton", choices=list(mb.BOTONES))
    b1.add_argument("accion", help="ver: atkhub mouse acciones")
    b1.add_argument("--forzar", action="store_true", help="permite cambiar el clic izquierdo")
    b1.set_defaults(func=cmd_mouse_boton)
    mc = m.add_parser("macro", parents=[comun], help="guarda una macro (y la asigna a un botón)")
    mc.add_argument("numero", type=int, help="1-16")
    mc.add_argument("secuencia", help='entre comillas, ej. "ctrl+c 100ms ctrl+v"')
    mc.add_argument("--boton", choices=list(mb.BOTONES), help="botón que la ejecuta")
    mc.add_argument("--modo", choices=list(mb.MODOS_MACRO), default="veces")
    mc.add_argument("--veces", type=int, default=1, help="repeticiones en modo veces (1)")
    mc.add_argument("--espera", type=int, default=mb.ESPERA_DEFECTO, help="ms entre pasos (30)")
    mc.add_argument("--nombre", default="ATKHUB")
    mc.set_defaults(func=cmd_mouse_macro)
    su2 = m.add_parser("suspension", parents=[comun], help="tiempos para dormirse")
    su2.add_argument("--normal", type=float, help="minutos, de 0.5 a 30 (de media en media)")
    su2.add_argument("--profunda", type=int, help="minutos, de 1 a 60")
    su2.set_defaults(func=cmd_mouse_suspension)
    po = m.add_parser("polling", parents=[comun], help="cambia el polling rate")
    po.add_argument("hz", type=int, choices=sorted(ms.TASA_A_BYTE))
    po.set_defaults(func=cmd_mouse_polling)
    dp = m.add_parser("dpi", parents=[comun], help="cambia el DPI de una etapa")
    dp.add_argument("etapa", type=int, choices=range(1, 9), metavar="ETAPA (1-8)")
    dp.add_argument("valor", type=int, help="50 a 22000")
    dp.set_defaults(func=cmd_mouse_dpi)
    return p


def main(argv=None) -> int:
    a = construir_parser().parse_args(argv)
    a.log = print if (a.debug or (a.simular and a.func is not cmd_gui)) else None
    if a.simular and a.func is not cmd_gui:
        print("[modo simulado: no se toca ningún dispositivo]")
    try:
        a.func(a)
    except ErrorATKHUB as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0
