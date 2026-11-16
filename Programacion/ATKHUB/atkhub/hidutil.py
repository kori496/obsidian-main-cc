"""Acceso a hidapi y utilidades comunes."""

from __future__ import annotations


class ErrorATKHUB(RuntimeError):
    pass


def cargar_hid():
    """Importa hidapi solo cuando hace falta (así el modo simular funciona sin instalarlo)."""
    try:
        import hid  # paquete de pip: hidapi
    except ImportError as e:
        raise ErrorATKHUB(
            "Falta la librería hidapi. Instálala con:  pip install hidapi"
        ) from e
    if not hasattr(hid, "device"):
        raise ErrorATKHUB(
            "Está instalado el paquete 'hid' en vez de 'hidapi'. Arréglalo con:\n"
            "  pip uninstall hid\n  pip install hidapi"
        )
    return hid


def enumerar() -> list[dict]:
    return cargar_hid().enumerate()


def abrir(ruta: bytes):
    hid = cargar_hid()
    dev = hid.device()
    try:
        dev.open_path(ruta)
    except OSError as e:
        raise ErrorATKHUB(
            "No se pudo abrir el dispositivo. Cierra el software oficial (Ajazz / Attack Shark) "
            "y vuelve a intentar."
        ) from e
    return dev


def vaciar(dev, largo: int = 64, maximo: int = 64) -> None:
    """Descarta lo que haya pendiente sin bloquear.

    OJO: en hidapi, read(n, 0) NO es "sin espera": con 0 llama a hid_read, que se queda
    esperando para siempre. Por eso se lee con 1 ms y con un tope de lecturas.
    """
    for _ in range(maximo):
        if not dev.read(largo, 1):
            break


def hexa(datos) -> str:
    return " ".join(f"{b:02X}" for b in bytes(datos))
