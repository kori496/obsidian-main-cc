"""Pruebas sin hardware: los bytes deben coincidir con los drivers de referencia.

Correr desde la carpeta ATKHUB:  python -m unittest
"""

import unittest

from atkhub import mouse_attackshark as ms
from atkhub import teclado_ajazz as tk
from atkhub.cli import main


class Teclado(unittest.TestCase):
    def test_paquete_estado(self):
        p = tk.paquete(tk.CMD_ESTADO)
        self.assertEqual(len(p), 64)
        self.assertEqual(p[:5], bytes([0xAA, 0x55, 0xCC, 0x33, 0x0E]))
        self.assertEqual(set(p[5:]), {0})

    def test_luz_resta_uno(self):
        enviados = []
        kb = tk.TecladoAjazz(simular=True, log=enviados.append)
        kb.luz(tk.buscar_efecto("respiracion"), brillo=5, velocidad=4, color=tk.buscar_color("azul"))
        self.assertIn("AA 55 CC 33 07 07 04 03 00 02", enviados[0])

    def test_estado_simulado(self):
        e = tk.TecladoAjazz(simular=True).estado()
        self.assertEqual((e.bateria, e.energia), (87, 2))

    def test_errores(self):
        with self.assertRaises(tk.ErrorATKHUB):
            tk.buscar_efecto("nada")
        with self.assertRaises(tk.ErrorATKHUB):
            tk.TecladoAjazz(simular=True).luz(7, brillo=9)


class Mouse(unittest.TestCase):
    def test_polling(self):
        self.assertEqual(ms.paquete_polling(1000), bytes([6, 9, 1, 1, 0xFE, 0, 0, 0, 0]))
        self.assertEqual(ms.paquete_polling(125)[3:5], bytes([0x08, 0xF7]))

    def test_checksum_por_defecto(self):
        p = ms.DPI_POR_DEFECTO
        self.assertEqual(len(p), 56)
        self.assertEqual(ms.checksum_dpi(p), (p[50] << 8) | p[51])

    def test_leer_dpi_por_defecto(self):
        etapas, actual = ms.leer_paquete_dpi(ms.DPI_POR_DEFECTO)
        self.assertEqual([e.dpi for e in etapas[:6]], [800, 1600, 2400, 3200, 5000, 22000])
        self.assertEqual(actual, 2)

    def test_ida_y_vuelta(self):
        for dpi in (50, 400, 800, 1600, 3200, 10000, 10100, 12000, 16000, 22000):
            bajo, alto = ms.dpi_a_bytes(dpi)
            doble = 12_000 < dpi < 24_000
            self.assertEqual(ms.bytes_a_dpi(bajo, alto, doble), dpi, dpi)

    def test_cambiar_etapa(self):
        p = bytearray(ms.DPI_POR_DEFECTO)
        ms.poner_dpi_en_paquete(p, 1, 1200)
        etapas, _ = ms.leer_paquete_dpi(bytes(p))  # checksum válido
        self.assertEqual(etapas[0].dpi, 1200)
        self.assertEqual(etapas[1].dpi, 1600)

    def test_reporte_peligroso_bloqueado(self):
        m = ms.MouseAttackShark(simular=True)
        with self.assertRaises(ms.ErrorATKHUB):
            m._escribir(bytes([0x10, 0x00]))  # 0x10 = bootloader


class CLI(unittest.TestCase):
    def test_comandos_simulados(self):
        for args in (["detectar", "--simular"], ["teclado", "estado", "--simular"],
                     ["teclado", "luz", "fijo", "--color", "blanco", "--simular"],
                     ["mouse", "info", "--simular"], ["mouse", "polling", "500", "--simular"],
                     ["mouse", "dpi", "2", "1800", "--simular"]):
            self.assertEqual(main(args), 0, args)


if __name__ == "__main__":
    unittest.main()


class FalsoHID:
    """Imita un dispositivo hidapi: leer con espera 0 bloquearía para siempre."""

    def __init__(self, respuestas=(), listo=None):
        self.pendientes = [list(r) for r in respuestas]
        self.escrito = []
        self.listo = listo or (lambda: bool(self.escrito))  # responde solo después de un envío

    def read(self, n, espera=0):
        if espera <= 0:
            raise AssertionError("read(n, 0) bloquea en hidapi")
        return self.pendientes.pop(0) if self.pendientes and self.listo() else []

    def write(self, datos):
        self.escrito.append(bytes(datos))
        return len(datos)

    def send_feature_report(self, datos):
        self.escrito.append(bytes(datos))
        return len(datos)

    def close(self):
        pass


class SinBloqueo(unittest.TestCase):
    def test_teclado_estado_real(self):
        kb = tk.TecladoAjazz(simular=True)
        kb.simular, kb.dev = False, FalsoHID([tk.paquete(tk.CMD_ESTADO, bytes([64, 3]))])
        e = kb.estado()
        self.assertEqual((e.bateria, e.energia), (64, 3))
        self.assertEqual(kb.dev.escrito[0][:6], bytes([0x00, 0xAA, 0x55, 0xCC, 0x33, 0x0E]))

    def test_teclado_luz_real(self):
        kb = tk.TecladoAjazz(simular=True)
        kb.simular, kb.dev = False, FalsoHID()
        kb.luz(8, color=2)
        self.assertEqual(len(kb.dev.escrito), 1)

    def test_mouse_polling_real(self):
        m = ms.MouseAttackShark(simular=True)
        m.simular, m.cmd = False, FalsoHID()
        m.ev = FalsoHID([[0x00, 0x00, 0x50, 0x00, 0x06]], listo=lambda: bool(m.cmd.escrito))
        self.assertTrue(m.set_polling(1000))


class Permiso(unittest.TestCase):
    def _mouse(self, respuestas_feature):
        m = ms.MouseAttackShark(simular=True)
        m.simular, m.ev = False, FalsoHID()
        m.cmd = FalsoHID()
        cola = list(respuestas_feature)
        m.cmd.get_feature_report = lambda rid, n: cola.pop(0)
        return m

    def test_permiso_al_segundo_intento(self):
        m = self._mouse([[0xA0, 0x00], [0xA0, 0x01], list(ms.paquete_polling(500))])
        self.assertEqual(m.polling(), 500)

    def test_sin_permiso_muestra_bytes(self):
        m = self._mouse([[0xA0, 0x00, 0x00]] * 3)
        with self.assertRaises(ms.ErrorATKHUB) as e:
            m.polling()
        self.assertIn("A0 00 00", str(e.exception))


class LuzMouse(unittest.TestCase):
    def test_checksum_ejemplo_documentado(self):
        # ejemplo de docs/protocols/user-preferences-protocol.md: checksum 01 AF
        p = bytes([0x05, 0x0F, 0x01, 0x00, 0x03, 0xA8, 0x00, 0xFF, 0x00, 0x01, 0x04, 0x01, 0xAF, 0, 0])
        luz = ms.leer_paquete_luz(p)
        self.assertEqual((luz.modo, luz.velocidad, luz.brillo), (0, 3, 8))
        self.assertEqual((luz.sueno_min, luz.sueno_profundo_min, luz.respuesta_ms), (0.5, 10, 8))

    def test_cambiar_solo_color(self):
        p = bytearray(ms.LUZ_POR_DEFECTO)
        ms.modificar_paquete_luz(p, modo=2, color=ms.leer_color("#FF3C96"))
        luz = ms.leer_paquete_luz(bytes(p))
        self.assertEqual((luz.modo, luz.color, luz.brillo), (2, (0xFF, 0x3C, 0x96), 8))

    def test_suspension(self):
        p = bytearray(ms.LUZ_POR_DEFECTO)
        ms.modificar_paquete_luz(p, sueno=5, sueno_profundo=45)
        luz = ms.leer_paquete_luz(bytes(p))
        self.assertEqual((luz.sueno_min, luz.sueno_profundo_min, luz.brillo, luz.velocidad), (5, 45, 8, 3))

    def test_rangos(self):
        for k, v in (("brillo", 9), ("velocidad", 0), ("sueno", 0.3), ("sueno_profundo", 61)):
            with self.assertRaises(ms.ErrorATKHUB, msg=k):
                ms.modificar_paquete_luz(bytearray(ms.LUZ_POR_DEFECTO), **{k: v})

    def test_cli_luz(self):
        for args in (["mouse", "modos"], ["mouse", "luz", "respiracion", "--color", "rosa", "--simular"],
                     ["mouse", "suspension", "--normal", "5", "--profunda", "30", "--simular"]):
            self.assertEqual(main(args), 0, args)


from atkhub import mouse_botones as mb


class BotonesMouse(unittest.TestCase):
    def test_lectura_de_fabrica_vuelve_a_fabrica(self):
        # la fila "Read" de la doc, pasada a orden de escritura, debe dar la fila "Write"
        w = mb.paquete_escritura_desde_lectura(mb.LECTURA_POR_DEFECTO)
        self.assertEqual(bytes(w), bytes(mb.paquete_por_defecto()))

    def test_nunca_escribe_3c(self):
        w = mb.paquete_escritura_desde_lectura(mb.LECTURA_POR_DEFECTO)
        mb.verificar_seguro(w)
        self.assertNotIn(0x3C, w[3:57:3])
        with self.assertRaises(mb.ErrorATKHUB):
            mb.poner_boton(w, "adelante", (0x3C, 0, 0))

    def test_botones_leidos(self):
        b = mb.botones_desde_lectura(mb.LECTURA_POR_DEFECTO)
        self.assertEqual(mb.describir(*b["adelante"]), "adelante")
        self.assertEqual(mb.describir(*b["dpi"]), "dpi-ciclo")
        self.assertEqual(mb.describir(*b["rueda-arriba"]), "rueda-arriba")

    def test_acciones(self):
        self.assertEqual(mb.leer_accion("tecla:ctrl+shift+s"), (0x11, 0x03, 0x16))
        self.assertEqual(mb.leer_accion("macro:3"), (0x12, 0, 3))
        self.assertEqual(mb.leer_accion("volumen-mas"), (0x1B, 0, 0))
        with self.assertRaises(mb.ErrorATKHUB):
            mb.leer_accion("tecla:ctrl")

    def test_cambiar_un_boton(self):
        w = mb.paquete_por_defecto()
        mb.poner_boton(w, "atras", mb.leer_accion("play-pausa"))
        self.assertEqual(w[24:27], bytes([0x18, 0, 0]))
        self.assertEqual(mb.checksum_botones(w), (w[57] << 8) | w[58])

    def test_izquierdo_pide_forzar(self):
        self.assertEqual(main(["mouse", "boton", "izquierdo", "desactivar", "--simular"]), 1)


class MacrosMouse(unittest.TestCase):
    def test_secuencia(self):
        pasos = mb.leer_secuencia("ctrl+c 100ms a")
        self.assertEqual(pasos[:4], [(False, 0xE0, 30), (False, 0x06, 30), (True, 0x06, 30), (True, 0xE0, 100)])
        self.assertEqual(pasos[4:], [(False, 0x04, 30), (True, 0x04, 30)])

    def test_espera_larga(self):
        self.assertEqual(mb.codificar_paso(False, 0x04, 50), bytes([0x05, 0x04]))
        self.assertEqual(mb.codificar_paso(True, 0x04, 2050), bytes([0x80 | 5, 0x04, 10, 0x03]))

    def test_paquetes(self):
        p1, p2, p3 = mb.paquetes_macro(2, mb.leer_secuencia("a"), "mientras", 1, "prueba")
        self.assertEqual(p1[:5], bytes([0x09, 0x40, 2, 0, 0x02]))
        self.assertEqual(p1[29], 2)  # dos pasos estándar
        self.assertEqual(p1[30:34], bytes([0x03, 0x04, 0x83, 0x04]))
        suma = (sum(p1[4:]) + sum(p2[4:]) + sum(p3[4:9])) & 0xFFFF
        self.assertEqual((p3[10] << 8) | p3[11], suma)

    def test_macro_muy_larga(self):
        with self.assertRaises(mb.ErrorATKHUB):
            mb.paquetes_macro(1, mb.leer_secuencia(" ".join("abcdefghijklmnopqrstuvwxyz")))


class GUI(unittest.TestCase):
    def setUp(self):
        import tempfile, pathlib, threading
        from atkhub.gui.api import API
        from atkhub.gui.servidor import crear_servidor
        self.api = API(simular=True, carpeta=pathlib.Path(tempfile.mkdtemp()))
        self.srv = crear_servidor(self.api, 0)
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.srv.server_address[1]}"

    def tearDown(self):
        self.srv.shutdown()
        self.srv.server_close()

    def _post(self, metodo, args, token=True):
        import json, urllib.request
        req = urllib.request.Request(self.url + "/api/" + metodo, data=json.dumps(args).encode(), method="POST",
                                     headers={"X-ATKHUB-Token": self.srv.token if token else "malo"})
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())

    def test_pagina_y_tipos(self):
        import urllib.request
        with urllib.request.urlopen(self.url + "/") as r:
            html = r.read().decode()
        self.assertIn(self.srv.token, html)
        with urllib.request.urlopen(self.url + "/js/app.js") as r:
            self.assertTrue(r.headers["Content-Type"].startswith("text/javascript"))

    def test_sin_token_rechaza(self):
        import urllib.error
        with self.assertRaises(urllib.error.HTTPError) as e:
            self._post("mouse_aplicar", [{"polling": 125}], token=False)
        self.assertEqual(e.exception.code, 403)

    def test_no_sale_de_la_carpeta_web(self):
        import urllib.error, urllib.request
        with self.assertRaises(urllib.error.HTTPError):
            urllib.request.urlopen(self.url + "/../api.py")

    def test_flujo_mouse(self):
        self.assertTrue(self._post("mouse_leer", [])["ok"])
        r = self._post("mouse_aplicar", [{"dpi": {"1": 1200}, "botones": {"atras": "play-pausa"}}])
        self.assertTrue(r["ok"], r)
        leido = self._post("mouse_leer", [])
        self.assertEqual(leido["dpi"]["etapas"][0]["dpi"], 1200)
        self.assertEqual(leido["botones"]["atras"]["id"], "play-pausa")
        self.assertFalse(self._post("mouse_aplicar", [{"botones": {"izquierdo": "desactivar"}}])["ok"])

    def test_teclado_guarda_estado(self):
        r = self._post("teclado_aplicar", [{"efecto": 7, "color": 2}])
        self.assertEqual((r["config"]["efecto"], r["config"]["color"]), (7, 2))
        self.assertEqual(self._post("teclado_leer", [])["config"]["efecto"], 7)
