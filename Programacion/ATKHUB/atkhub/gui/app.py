"""Abre la interfaz gráfica de ATKHUB.

Por defecto usa una ventana nativa (pywebview + WebView2 de Windows). Si pywebview no
está instalado, o con --navegador, la abre en el navegador.
"""

from __future__ import annotations

import threading
import time
import webbrowser

from .api import API
from .servidor import crear_servidor


def lanzar(simular: bool = False, navegador: bool = False, puerto: int = 0) -> int:
    api = API(simular=simular)
    srv = crear_servidor(api, puerto)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{srv.server_address[1]}/"

    if not navegador:
        try:
            import webview  # pywebview
        except ImportError:
            print("pywebview no está instalado (pip install pywebview). Abro ATKHUB en el navegador.")
            navegador = True

    if not navegador:
        try:
            webview.create_window("ATKHUB", url, width=1280, height=800, min_size=(1100, 700),
                                  background_color="#151515")
            webview.start()
        except Exception as e:  # noqa: BLE001 - sin ventana nativa, seguir en el navegador
            print(f"No se pudo abrir la ventana nativa ({e}). Abro ATKHUB en el navegador.")
            navegador = True

    if navegador:
        print(f"ATKHUB abierto en {url}  (Ctrl+C para cerrar)")
        webbrowser.open(url)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    srv.shutdown()
    return 0
