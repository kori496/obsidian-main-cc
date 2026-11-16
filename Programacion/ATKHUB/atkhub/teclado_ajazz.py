"""Teclado Ajazz AK820 Max (versión mecánica / Max Plus).

Protocolo tomado de ak820ctl / openajazz (shrey715, licencia MIT), que lo sacó del
DeviceDriver.exe oficial. Cada comando es un reporte de salida HID de 64 bytes
(report ID 0) en la colección del fabricante (usage page 0xFF02, usage 0x02):

    AA 55 CC 33 <comando> <argumentos...> 00...
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from .hidutil import ErrorATKHUB, abrir, enumerar, hexa, vaciar

VID = 0x1A2C
PIDS = {0xA036: "cable USB", 0x8FFF: "dongle 2.4G"}
USAGE_PAGE_CONTROL = 0xFF02

MAGIA = bytes([0xAA, 0x55, 0xCC, 0x33])
LARGO = 64

CMD_LUZ = 0x07
CMD_SUSPENSION = 0x0C
CMD_RESPUESTA = 0x0D
CMD_ESTADO = 0x0E

# modo: (nombre, admite dirección, admite color)
EFECTOS = {
    1: ("ondas-lados", "Ondas a los lados", True, True),
    2: ("estrellas", "Puntos de estrellas", False, True),
    3: ("ondas-vertical", "Ondas arriba y abajo", True, True),
    4: ("expulsion", "Expulsión doble", True, True),
    5: ("espectro", "Ciclo de espectro", False, False),
    6: ("caleidoscopio", "Caleidoscopio", True, True),
    7: ("fijo", "Luz fija", False, True),
    8: ("respiracion", "Respiración general", False, True),
    9: ("cruz", "Cruz", True, True),
    11: ("respiracion-tecla", "Respiración por tecla", False, True),
    12: ("pergamino", "Pergamino", False, True),
    15: ("arriba-abajo", "Tres arriba, tres abajo", False, True),
    16: ("lluvia", "Lluvia", False, True),
    17: ("molino", "Molino", False, True),
    18: ("seno", "Onda seno", False, True),
    19: ("galope", "Galope", True, True),
}
COLORES = ["rojo", "verde", "azul", "amarillo", "magenta", "cian", "blanco", "arcoiris"]
SUSPENSION = {"5": 1, "15": 2, "30": 3, "nunca": 4}
ESTADOS_ENERGIA = {0: "sin datos", 1: "cargando", 2: "con batería", 3: "carga completa"}


def paquete(cmd: int, args: bytes = b"") -> bytes:
    return (MAGIA + bytes([cmd]) + bytes(args)).ljust(LARGO, b"\x00")


def buscar_efecto(nombre: str) -> int:
    n = nombre.strip().lower()
    if n.isdigit() and int(n) in EFECTOS:
        return int(n)
    for modo, (slug, *_r) in EFECTOS.items():
        if slug == n:
            return modo
    raise ErrorATKHUB(f"Efecto desconocido: '{nombre}'. Mira la lista con:  atkhub teclado efectos")


def buscar_color(nombre: str) -> int:
    n = nombre.strip().lower().replace("í", "i")
    if n in COLORES:
        return COLORES.index(n)
    raise ErrorATKHUB(f"Color desconocido: '{nombre}'. Opciones: {', '.join(COLORES)}")


@dataclass
class Estado:
    bateria: int | None
    energia: int

    def texto(self) -> str:
        bat = f"{self.bateria} %" if self.bateria is not None else "desconocida"
        return f"Batería: {bat} · {ESTADOS_ENERGIA.get(self.energia, f'estado {self.energia}')}"


def encontrar() -> dict | None:
    """Devuelve la interfaz de control del teclado (prefiere el cable)."""
    candidatos = [
        d for d in enumerar()
        if d["vendor_id"] == VID and d["product_id"] in PIDS
        and d.get("usage_page") == USAGE_PAGE_CONTROL
    ]
    candidatos.sort(key=lambda d: d["product_id"] != 0xA036)
    return candidatos[0] if candidatos else None


class TecladoAjazz:
    def __init__(self, simular: bool = False, log=None):
        self.simular = simular
        self.log = log
        self.dev = None
        self.conexion = "simulado"
        if simular:
            return
        info = encontrar()
        if info is None:
            raise ErrorATKHUB(
                "No encontré el teclado Ajazz (1A2C:A036 por cable o 1A2C:8FFF por dongle). "
                "¿Está conectado?"
            )
        self.conexion = PIDS[info["product_id"]]
        self.dev = abrir(info["path"])

    def cerrar(self):
        if self.dev is not None:
            self.dev.close()
            self.dev = None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.cerrar()

    # -- transporte --------------------------------------------------------

    def enviar(self, cmd: int, args: bytes = b"", respuesta: bool = False,
               espera: float = 0.5) -> bytes | None:
        pkt = paquete(cmd, args)
        if self.log:
            self.log(f"-> teclado: {hexa(pkt[:12])} ...")
        if self.simular:
            return paquete(CMD_ESTADO, bytes([87, 2])) if respuesta else None
        vaciar(self.dev, LARGO)  # descartar respuestas viejas
        self.dev.write([0x00] + list(pkt))  # 0x00 = report ID
        if not respuesta:
            return None
        time.sleep(0.1)
        limite = time.monotonic() + espera
        while (resta := limite - time.monotonic()) > 0:
            r = self.dev.read(LARGO, max(1, int(resta * 1000)))
            if not r:
                break
            r = bytes(r)
            if r[:4] != MAGIA and r[1:5] == MAGIA:  # algunas versiones dejan el report ID
                r = r[1:]
            if self.log:
                self.log(f"<- teclado: {hexa(r[:12])} ...")
            if r[:4] == MAGIA and r[4] == cmd:
                return r
        return None

    # -- comandos ----------------------------------------------------------

    def estado(self) -> Estado | None:
        """Solo lectura: batería y estado de carga."""
        r = self.enviar(CMD_ESTADO, respuesta=True)
        if r is None:
            return None
        return Estado(bateria=r[5] if r[5] <= 100 else None, energia=r[6])

    def luz(self, modo: int, brillo: int = 5, velocidad: int = 4,
            direccion: int = 0, color: int = 7):
        for nombre, v in (("brillo", brillo), ("velocidad", velocidad)):
            if not 1 <= v <= 5:
                raise ErrorATKHUB(f"El {nombre} va de 1 a 5")
        if direccion not in (0, 1):
            raise ErrorATKHUB("La dirección es 0 (izq. a der.) o 1 (der. a izq.)")
        if not 0 <= color < len(COLORES):
            raise ErrorATKHUB("Color fuera de rango")
        self.enviar(CMD_LUZ, bytes([modo - 1, brillo - 1, velocidad - 1, direccion, color]))
        time.sleep(0.01)

    def suspension(self, opcion: int):
        """1 = 5 min, 2 = 15 min, 3 = 30 min, 4 = nunca."""
        self.enviar(CMD_SUSPENSION, bytes([opcion]))
