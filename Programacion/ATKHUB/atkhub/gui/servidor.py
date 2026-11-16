"""Servidor local de la interfaz: sirve la página y la API.

Solo escucha en 127.0.0.1. La página recibe un token aleatorio al cargarse y cada
llamada a la API lo debe mandar en la cabecera X-ATKHUB-Token: así ninguna otra
página web abierta en el PC puede mandarle comandos a tus periféricos.
"""

from __future__ import annotations

import json
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .api import API, METODOS_PUBLICOS

WEB = Path(__file__).parent / "web"
MAX_CUERPO = 64 * 1024
# Tipos fijos: en Windows el registro a veces dice que .js es "text/plain" y los módulos no cargan.
TIPOS = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
         ".js": "text/javascript; charset=utf-8", ".svg": "image/svg+xml", ".png": "image/png"}


def crear_servidor(api: API, puerto: int = 0) -> ThreadingHTTPServer:
    token = secrets.token_urlsafe(24)

    class Manejador(BaseHTTPRequestHandler):
        server_version = "ATKHUB"

        def log_message(self, *args):  # silencio en la consola
            pass

        def _enviar(self, codigo: int, cuerpo: bytes, tipo: str, cache: bool = False):
            self.send_response(codigo)
            self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", str(len(cuerpo)))
            self.send_header("Cache-Control", "max-age=3600" if cache else "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(cuerpo)

        def do_GET(self):
            ruta = self.path.split("?", 1)[0]
            if ruta == "/":
                ruta = "/index.html"
            archivo = (WEB / ruta.lstrip("/")).resolve()
            if WEB.resolve() not in archivo.parents or not archivo.is_file():
                return self._enviar(404, b"no encontrado", "text/plain")
            datos = archivo.read_bytes()
            if archivo.name == "index.html":
                datos = datos.replace(b"__TOKEN__", token.encode())
            tipo = TIPOS.get(archivo.suffix.lower(), "application/octet-stream")
            self._enviar(200, datos, tipo, cache=archivo.name != "index.html")

        def do_POST(self):
            if self.headers.get("X-ATKHUB-Token") != token:
                return self._enviar(403, b"token invalido", "text/plain")
            if not self.path.startswith("/api/"):
                return self._enviar(404, b"no encontrado", "text/plain")
            metodo = self.path[5:]
            if metodo not in METODOS_PUBLICOS:
                return self._enviar(404, b"metodo desconocido", "text/plain")
            largo = int(self.headers.get("Content-Length") or 0)
            if largo > MAX_CUERPO:
                return self._enviar(413, b"muy grande", "text/plain")
            try:
                args = json.loads(self.rfile.read(largo) or b"[]")
                if not isinstance(args, list):
                    raise ValueError
            except ValueError:
                return self._enviar(400, b"json invalido", "text/plain")
            try:
                res = getattr(api, metodo)(*args)
            except TypeError as e:
                res = {"ok": False, "error": f"Argumentos inválidos: {e}"}
            self._enviar(200, json.dumps(res, ensure_ascii=False).encode("utf-8"),
                         "application/json; charset=utf-8")

    srv = ThreadingHTTPServer(("127.0.0.1", puerto), Manejador)
    srv.daemon_threads = True
    srv.token = token  # para las pruebas
    return srv
