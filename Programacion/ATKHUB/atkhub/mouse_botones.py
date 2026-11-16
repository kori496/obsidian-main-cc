"""Botones y macros del Attack Shark X11 (reportes 0x08 y 0x09).

Tomado de attack-shark-x11-driver (licencia MIT): docs/protocols/button-mapping.md y
custom-macro-protocol.md.

Botones (reporte 0x08, 59 bytes): 18 "slots" de 3 bytes desde el byte 3
(acción del firmware, modificadores, tecla) y checksum big endian en 57-58
(suma de los bytes 3 a 56).

OJO, el firmware reordena los slots: lo que se escribe en un slot se lee en otro.
Según la prueba del autor (tabla de button-mapping.md):
    escribir 7 -> leer 5 · escribir 8 -> leer 6 · escribir 6 -> leer 8
    escribir 17 <-> leer 18 · escribir 5 no tiene efecto · leer 7 = 0x3C (protegido)
El 0x3C es la tecla de modo (cambia la conexión). ATKHUB nunca lo escribe.
(El driver de referencia, al releer y reescribir, mete el 0x3C en el slot 7, que es
el botón "adelante". Aquí se usa la tabla para evitarlo.)
"""

from __future__ import annotations

from .hidutil import ErrorATKHUB

R_BOTONES, LARGO_BOTONES = 0x08, 0x3B
R_MACRO, LARGO_MACRO_PAQUETE = 0x09, 0x40
ACCION_PROTEGIDA = 0x3C

# botón físico -> (slot de escritura, nombre)
BOTONES = {
    "izquierdo": (1, "Clic izquierdo"),
    "derecho": (2, "Clic derecho"),
    "medio": (3, "Clic de la rueda"),
    "dpi": (6, "Botón DPI"),
    "adelante": (7, "Lateral adelante"),
    "atras": (8, "Lateral atrás"),
    "rueda-arriba": (17, "Rueda hacia arriba"),
    "rueda-abajo": (18, "Rueda hacia abajo"),
}

# slot de escritura -> slot de lectura
ESCRIBIR_A_LEER = {**{i: i for i in range(1, 19)}, 5: None, 6: 8, 7: 5, 8: 6, 17: 18, 18: 17}

# nombre -> (código de acción, descripción)
ACCIONES = {
    "desactivar": (0x01, "No hace nada"),
    "clic-izq": (0x02, "Clic izquierdo"),
    "clic-der": (0x03, "Clic derecho"),
    "clic-medio": (0x04, "Clic de la rueda"),
    "atras": (0x05, "Atrás"),
    "adelante": (0x06, "Adelante"),
    "doble-clic": (0x07, "Doble clic"),
    "disparo": (0x08, "Clic izquierdo repetido mientras se mantiene"),
    "rueda-arriba": (0x09, "Rueda arriba"),
    "rueda-abajo": (0x0A, "Rueda abajo"),
    "dpi-ciclo": (0x0D, "Cambia de etapa DPI"),
    "dpi-mas": (0x0E, "Sube el DPI"),
    "dpi-menos": (0x0F, "Baja el DPI"),
    "francotirador": (0x10, "Baja mucho el DPI mientras se mantiene"),
    "polling-ciclo": (0x28, "Cambia el polling rate"),
    "luz-ciclo": (0x29, "Cambia el efecto de luz"),
    "luz-on-off": (0x30, "Prende/apaga la luz"),
    "perfil-ciclo": (0x34, "Cambia de perfil"),
    "inicio": (0x14, "Abre el menú Inicio"),
    "reproductor": (0x15, "Abre el reproductor"),
    "anterior": (0x16, "Canción anterior"),
    "siguiente": (0x17, "Canción siguiente"),
    "play-pausa": (0x18, "Play / pausa"),
    "detener": (0x19, "Detener"),
    "silenciar": (0x1A, "Silenciar"),
    "volumen-mas": (0x1B, "Subir volumen"),
    "volumen-menos": (0x1C, "Bajar volumen"),
    "calculadora": (0x1D, "Calculadora"),
    "correo": (0x1E, "Correo"),
    "navegador-atras": (0x21, "Navegador: atrás"),
    "navegador-adelante": (0x20, "Navegador: adelante"),
    "navegador-recargar": (0x24, "Navegador: recargar"),
    "mi-pc": (0x23, "Este equipo"),
}
ACCION_TECLA = 0x11
ACCION_MACRO = 0x12
NOMBRE_POR_CODIGO = {c: n for n, (c, _) in ACCIONES.items()}

MODIFICADORES = {"ctrl": 0x01, "shift": 0x02, "alt": 0x04, "win": 0x08}

# Teclas (HID, página teclado 0x07)
TECLAS = {
    **{chr(ord("a") + i): 0x04 + i for i in range(26)},
    **{str((i + 1) % 10): 0x1E + i for i in range(10)},
    "enter": 0x28, "esc": 0x29, "borrar": 0x2A, "tab": 0x2B, "espacio": 0x2C,
    "-": 0x2D, "=": 0x2E, "[": 0x2F, "]": 0x30, "\\": 0x31, ";": 0x33, "'": 0x34,
    "`": 0x35, ",": 0x36, ".": 0x37, "/": 0x38, "bloqmayus": 0x39,
    **{f"f{i}": 0x3A + i - 1 for i in range(1, 13)},
    "imprpant": 0x46, "pausa": 0x48, "insert": 0x49, "inicio": 0x4A, "repag": 0x4B,
    "supr": 0x4C, "fin": 0x4D, "avpag": 0x4E, "derecha": 0x4F, "izquierda": 0x50,
    "abajo": 0x51, "arriba": 0x52,
}
SINONIMOS = {"backspace": "borrar", "space": "espacio", "del": "supr", "delete": "supr",
             "escape": "esc", "home": "inicio", "end": "fin", "pageup": "repag",
             "pagedown": "avpag", "right": "derecha", "left": "izquierda", "up": "arriba",
             "down": "abajo", "control": "ctrl", "mayus": "shift", "windows": "win",
             "printscreen": "imprpant"}
TECLA_MOD = {"ctrl": 0xE0, "shift": 0xE1, "alt": 0xE2, "win": 0xE3}
CLICS_MACRO = {"clic-izq": 0xF1, "clic-der": 0xF2, "clic-medio": 0xF3,
               "clic-atras": 0xF4, "clic-adelante": 0xF5}
NOMBRE_TECLA = {**{v: k for k, v in TECLAS.items()}, **{v: k for k, v in TECLA_MOD.items()},
                **{v: k for k, v in CLICS_MACRO.items()}}


def _norm(t: str) -> str:
    t = t.strip().lower()
    return SINONIMOS.get(t, t)


def leer_atajo(texto: str) -> tuple[int, int]:
    """'ctrl+shift+s' -> (modificadores, tecla)."""
    mods, tecla = 0, None
    for parte in texto.split("+"):
        p = _norm(parte)
        if p in MODIFICADORES:
            mods |= MODIFICADORES[p]
        elif p in TECLAS and tecla is None:
            tecla = TECLAS[p]
        else:
            raise ErrorATKHUB(f"No entiendo '{parte}' en el atajo '{texto}'")
    if tecla is None:
        raise ErrorATKHUB(f"El atajo '{texto}' necesita una tecla (ej. ctrl+c)")
    return mods, tecla


def leer_accion(texto: str) -> tuple[int, int, int]:
    """'volumen-mas' / 'tecla:ctrl+c' / 'macro:2' -> (acción, modificadores, tecla)."""
    t = texto.strip().lower()
    if t.startswith("tecla:"):
        return (ACCION_TECLA, *leer_atajo(t[6:]))
    if t.startswith("macro:"):
        n = t[6:]
        if not n.isdigit() or not 1 <= int(n) <= 16:
            raise ErrorATKHUB("El número de macro va de 1 a 16")
        return ACCION_MACRO, 0, int(n)
    if t in ACCIONES:
        return ACCIONES[t][0], 0, 0
    raise ErrorATKHUB(f"Acción desconocida: '{texto}'. Mira la lista con:  atkhub mouse acciones")


def describir(accion: int, mods: int, tecla: int) -> str:
    if accion == ACCION_TECLA:
        partes = [m for m, b in MODIFICADORES.items() if mods & b]
        partes.append(NOMBRE_TECLA.get(tecla, f"0x{tecla:02X}"))
        return "tecla " + "+".join(partes)
    if accion == ACCION_MACRO:
        return f"macro {tecla}"
    if accion == ACCION_PROTEGIDA:
        return "tecla de modo (protegida)"
    return NOMBRE_POR_CODIGO.get(accion, f"acción 0x{accion:02X}")


# -- paquete de botones ------------------------------------------------------

def checksum_botones(p) -> int:
    return sum(p[3:57]) & 0xFFFF


def _poner_checksum(p: bytearray) -> None:
    s = checksum_botones(p)
    p[57], p[58] = s >> 8, s & 0xFF


def slot_leido(p: bytes, slot_lectura: int) -> tuple[int, int, int]:
    o = 3 + (slot_lectura - 1) * 3
    return p[o], p[o + 1], p[o + 2]


def validar_lectura(p: bytes) -> None:
    if len(p) < 59:
        raise ErrorATKHUB(f"Respuesta de botones muy corta ({len(p)} bytes)")
    if checksum_botones(p) != (p[57] << 8) | p[58]:
        raise ErrorATKHUB("La respuesta de botones llegó con checksum incorrecto; no la uso.")


def botones_desde_lectura(p: bytes) -> dict[str, tuple[int, int, int]]:
    validar_lectura(p)
    return {nombre: slot_leido(p, ESCRIBIR_A_LEER[slot]) for nombre, (slot, _) in BOTONES.items()}


def paquete_escritura_desde_lectura(p: bytes, perfil: int | None = None) -> bytearray:
    """Convierte lo leído al orden de escritura (para cambiar un botón sin tocar los demás)."""
    validar_lectura(p)
    w = bytearray(LARGO_BOTONES)
    w[0], w[1], w[2] = R_BOTONES, LARGO_BOTONES, perfil if perfil is not None else p[2]
    for slot in range(1, 19):
        lectura = ESCRIBIR_A_LEER[slot]
        a, m, k = (0x01, 0, 0) if lectura is None else slot_leido(p, lectura)
        if a == ACCION_PROTEGIDA:
            a, m, k = 0x01, 0, 0
        o = 3 + (slot - 1) * 3
        w[o:o + 3] = bytes([a, m, k])
    _poner_checksum(w)
    return w


def paquete_por_defecto(perfil: int = 1) -> bytearray:
    w = bytearray(LARGO_BOTONES)
    w[0], w[1], w[2] = R_BOTONES, LARGO_BOTONES, perfil
    defecto = [0x02, 0x03, 0x04, 0x01, 0x01, 0x0D, 0x06, 0x05] + [0x01] * 8 + [0x09, 0x0A]
    for i, a in enumerate(defecto):
        w[3 + i * 3] = a
    _poner_checksum(w)
    return w


def poner_boton(w: bytearray, boton: str, accion: tuple[int, int, int]) -> None:
    if boton not in BOTONES:
        raise ErrorATKHUB(f"Botón desconocido: '{boton}'. Opciones: {', '.join(BOTONES)}")
    if accion[0] == ACCION_PROTEGIDA:
        raise ErrorATKHUB("La tecla de modo (0x3C) no se asigna desde ATKHUB.")
    o = 3 + (BOTONES[boton][0] - 1) * 3
    w[o:o + 3] = bytes(accion)
    _poner_checksum(w)


def verificar_seguro(w: bytes) -> None:
    for slot in range(18):
        if w[3 + slot * 3] == ACCION_PROTEGIDA:
            raise ErrorATKHUB("Bloqueado: el paquete de botones lleva la tecla de modo (0x3C).")


# lectura de ejemplo para el modo simular (fila "Read" de button-mapping.md)
_LECTURA = bytearray(LARGO_BOTONES)
_LECTURA[0], _LECTURA[1], _LECTURA[2] = R_BOTONES, LARGO_BOTONES, 1
for _i, _a in enumerate([0x02, 0x03, 0x04, 0x01, 0x06, 0x05, 0x3C, 0x0D] + [0x01] * 8 + [0x0A, 0x09]):
    _LECTURA[3 + _i * 3] = _a
_poner_checksum(_LECTURA)
LECTURA_POR_DEFECTO = bytes(_LECTURA)


# -- macros --------------------------------------------------------------------

MODOS_MACRO = {"veces": 0x00, "hasta-tecla": 0x01, "mientras": 0x02}
ESPERA_DEFECTO = 30  # ms entre pasos si no se indica
CAPACIDAD_ACCIONES = 100


def leer_secuencia(texto: str, espera: int = ESPERA_DEFECTO) -> list[tuple[bool, int, int]]:
    """Convierte texto en pasos (soltar?, código, espera_ms).

    Palabras separadas por espacios:
      a            pulsa y suelta la tecla a
      ctrl+c       mantiene ctrl, pulsa c, suelta c, suelta ctrl
      +shift -shift   solo pulsar / solo soltar
      clic-izq     un clic (también clic-der, clic-medio, clic-atras, clic-adelante)
      200ms        cambia la espera del paso anterior a 200 ms
    """
    pasos: list[list] = []

    def codigo(nombre: str) -> int:
        n = _norm(nombre)
        for tabla in (TECLAS, TECLA_MOD, CLICS_MACRO):
            if n in tabla:
                return tabla[n]
        raise ErrorATKHUB(f"No entiendo '{nombre}' en la macro")

    for palabra in texto.split():
        p = palabra.lower()
        if p.endswith("ms") and p[:-2].isdigit():
            if not pasos:
                raise ErrorATKHUB("La macro no puede empezar con una espera")
            pasos[-1][2] = int(p[:-2])
        elif p.startswith("+") and len(p) > 1:
            pasos.append([False, codigo(p[1:]), espera])
        elif p.startswith("-") and len(p) > 1:
            pasos.append([True, codigo(p[1:]), espera])
        elif "+" in p:
            codigos = [codigo(x) for x in p.split("+")]
            pasos += [[False, c, espera] for c in codigos]
            pasos += [[True, c, espera] for c in reversed(codigos)]
        else:
            c = codigo(p)
            pasos += [[False, c, espera], [True, c, espera]]
    if not pasos:
        raise ErrorATKHUB("La macro está vacía")
    return [tuple(x) for x in pasos]


def codificar_paso(soltar: bool, codigo: int, espera_ms: int) -> bytes:
    if not 10 <= espera_ms <= 50_000:
        raise ErrorATKHUB("Cada espera de la macro va de 10 ms a 50000 ms")
    ms = espera_ms // 10 * 10
    direccion = 0x80 if soltar else 0x00
    unidades = ms // 10
    if unidades <= 0x7F:
        return bytes([direccion | unidades, codigo])
    return bytes([direccion | ((ms % 200) // 10), codigo, ms // 200, 0x03])


def paquetes_macro(macro_id: int, pasos, modo: str = "veces", veces: int = 1,
                   nombre: str = "ATKHUB", color=(255, 255, 255)) -> list[bytes]:
    if not 1 <= macro_id <= 16:
        raise ErrorATKHUB("El número de macro va de 1 a 16")
    if modo not in MODOS_MACRO:
        raise ErrorATKHUB(f"Modo de macro: {', '.join(MODOS_MACRO)}")
    if not 1 <= veces <= 255:
        raise ErrorATKHUB("Las repeticiones van de 1 a 255")
    acciones, cuenta = bytearray(), 0
    for paso in pasos:
        b = codificar_paso(*paso)
        acciones += b
        cuenta += 1 if len(b) == 2 else 2
    if len(acciones) > CAPACIDAD_ACCIONES:
        raise ErrorATKHUB(f"La macro es muy larga ({len(acciones)} de {CAPACIDAD_ACCIONES} bytes)")
    acciones = bytes(acciones.ljust(CAPACIDAD_ACCIONES, b"\x00"))

    p1, p2, p3 = (bytearray(LARGO_MACRO_PAQUETE) for _ in range(3))
    for pagina, p in enumerate((p1, p2, p3)):
        p[0], p[1], p[2], p[3] = R_MACRO, LARGO_MACRO_PAQUETE, macro_id, pagina
    p1[4] = MODOS_MACRO[modo]
    p1[5:8] = bytes(color)
    p1[8] = veces
    p1[9:29] = nombre.encode("utf-8")[:20].ljust(20, b"\x00")
    p1[29] = cuenta
    p1[30:64] = acciones[0:34]
    p2[4:64] = acciones[34:94]
    p3[4:10] = acciones[94:100]
    suma = (sum(p1[4:64]) + sum(p2[4:64]) + sum(p3[4:9])) & 0xFFFF  # igual que el driver
    p3[10], p3[11] = suma >> 8, suma & 0xFF
    return [bytes(p1), bytes(p2), bytes(p3)]


def describir_secuencia(pasos) -> str:
    return " ".join(("-" if s else "+") + NOMBRE_TECLA.get(c, f"0x{c:02X}") + f"({e}ms)"
                    for s, c, e in pasos)
