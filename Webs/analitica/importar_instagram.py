"""Importa datos de Instagram a datos/youtube.db (tablas instagram_*).

Uso:
  python importar_instagram.py             # CSV de instagram/entrada/ + API de Meta
  python importar_instagram.py --solo-csv  # solo los CSV
  python importar_instagram.py --solo-api  # solo la API

Fuente 1, API de Instagram (inicio de sesion de Instagram, graph.instagram.com):
  lee meta_config.json (access_token y user_id; ver meta_config.ejemplo.json) y guarda
  seguidores, alcance diario, metricas diarias de los ultimos 7 dias y las ultimas
  publicaciones con sus metricas.
Fuente 2, CSV exportados de Meta Business Suite o del panel profesional de Instagram:
  sueltalos en instagram/entrada/. Mismas reglas que importar_tiktok.py (fecha + numeros =
  serie diaria que se une con importaciones anteriores; columna de texto = tabla).

Si el token falla (caduco o se revoco) crea NECESITA_TOKEN_META.txt y el panel lo avisa.
"""
import argparse
import json
import os
import shutil
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from importar_tiktok import clasificar, leer_csv, tipo_de, a_fecha, a_numero  # noqa: E402

ENTRADA = HERE / "instagram" / "entrada"
IMPORTADOS = HERE / "instagram" / "importados"
DB_FILE = HERE / "datos" / "youtube.db"
CONFIG_FILE = HERE / "meta_config.json"
FLAG_FILE = HERE / "NECESITA_TOKEN_META.txt"

API = "https://graph.instagram.com"
VERSION = "v26.0"
ERRORES_TOKEN = {190, 452, 463, 467}

# Etiquetas con las que se guardan las metricas de la API (las usa el panel)
ETIQUETAS = {
    "reach": "Alcance (cuentas únicas)",
    "views": "Vistas",
    "profile_views": "Visitas al perfil",
    "accounts_engaged": "Cuentas que interactuaron",
    "total_interactions": "Interacciones",
    "new_followers": "Seguidores nuevos",
    "followers_count": "Seguidores",
    "follows_count": "Siguiendo",
    "media_count": "Publicaciones",
}


def init_db(con):
    con.executescript(
        """
        CREATE TABLE IF NOT EXISTS instagram_archivo (
            id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, tipo TEXT, importado TEXT,
            filas INTEGER, columnas TEXT, es_serie INTEGER);
        CREATE TABLE IF NOT EXISTS instagram_fila (
            archivo_id INTEGER, n INTEGER, datos TEXT, PRIMARY KEY (archivo_id, n));
        CREATE TABLE IF NOT EXISTS instagram_serie (
            tipo TEXT, metrica TEXT, fecha TEXT, valor REAL, PRIMARY KEY (tipo, metrica, fecha));
        """
    )


def guardar_serie(con, tipo, metrica, fecha, valor):
    con.execute("INSERT OR REPLACE INTO instagram_serie VALUES (?,?,?,?)", (tipo, metrica, fecha, float(valor)))


def guardar_tabla(con, nombre, tipo, cols, filas):
    ahora = datetime.now().isoformat(timespec="seconds")
    cur = con.execute(
        "INSERT INTO instagram_archivo (nombre, tipo, importado, filas, columnas, es_serie) VALUES (?,?,?,?,?,0)",
        (nombre, tipo, ahora, len(filas), json.dumps(cols, ensure_ascii=False)),
    )
    for i, r in enumerate(filas):
        con.execute("INSERT INTO instagram_fila VALUES (?,?,?)", (cur.lastrowid, i, json.dumps(r, ensure_ascii=False)))


# ---------------------------------------------------------------- CSV

def importar_csv(path: Path, con) -> str:
    cols, datos = leer_csv(path)
    if not datos:
        return f"{path.name}: vacio o sin filas, se omite"
    tipo = tipo_de(path.name)
    col_f, nums = clasificar(cols, datos)
    ahora = datetime.now().isoformat(timespec="seconds")
    cur = con.execute(
        "INSERT INTO instagram_archivo (nombre, tipo, importado, filas, columnas, es_serie) VALUES (?,?,?,?,?,?)",
        (path.name, tipo, ahora, len(datos), json.dumps(cols, ensure_ascii=False), 1 if col_f else 0),
    )
    aid = cur.lastrowid
    for i, r in enumerate(datos):
        con.execute("INSERT INTO instagram_fila VALUES (?,?,?)", (aid, i, json.dumps(r, ensure_ascii=False)))
    if col_f:
        for r in datos:
            f = a_fecha(r[col_f])
            if not f:
                continue
            for m in nums:
                v = a_numero(r.get(m, ""))
                if v is not None:
                    guardar_serie(con, tipo, m, f.isoformat(), v)
        return f"{path.name}: serie diaria '{tipo}' ({len(datos)} dias, metricas: {', '.join(nums)})"
    return f"{path.name}: tabla '{tipo}' ({len(datos)} filas, columnas: {', '.join(cols)})"


def importar_todos_csv(con):
    ENTRADA.mkdir(parents=True, exist_ok=True)
    IMPORTADOS.mkdir(parents=True, exist_ok=True)
    archivos = sorted(p for p in ENTRADA.iterdir() if p.suffix.lower() == ".csv")
    if not archivos:
        print(f"CSV de Instagram: no hay archivos nuevos en {ENTRADA}.")
        return 0
    n = 0
    for p in archivos:
        try:
            print(importar_csv(p, con))
            con.commit()
            destino = IMPORTADOS / f"{datetime.now():%Y-%m-%d_%H%M%S}_{p.name}"
            shutil.move(str(p), str(destino))
            n += 1
        except Exception as e:  # un archivo raro no debe frenar a los demas
            con.rollback()
            print(f"{p.name}: ERROR {e}")
    return n


# ---------------------------------------------------------------- API

class ApiError(Exception):
    def __init__(self, code, msg, sub=None):
        super().__init__(msg)
        self.code, self.sub = code, sub


def _pedir(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "lagrim-stats"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            err = json.load(e).get("error", {})
        except Exception:
            err = {}
        raise ApiError(err.get("code", e.code), err.get("message", f"HTTP {e.code}"), err.get("error_subcode"))
    except urllib.error.URLError as e:
        raise ApiError(0, f"sin conexion: {e.reason}")


def api_get(ruta: str, token: str, **params):
    """Nunca imprimir la URL: lleva el token."""
    params["access_token"] = token
    return _pedir(f"{API}/{VERSION}/{ruta}?" + urllib.parse.urlencode(params))


def cargar_config():
    token = os.environ.get("META_ACCESS_TOKEN")
    uid = os.environ.get("META_USER_ID")
    cfg = {}
    if CONFIG_FILE.is_file():
        try:
            cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8-sig"))
        except Exception as e:
            print(f"meta_config.json no se pudo leer: {e}")
            return None
    if token:
        cfg["access_token"] = token
    if uid:
        cfg["user_id"] = uid
    tok = str(cfg.get("access_token", ""))
    if not tok or tok.startswith("PEGA_AQUI") or not cfg.get("user_id"):
        return None
    return cfg


def renovar_token(cfg):
    """Si el token es de larga duracion, lo renueva cada 7 dias (ig_refresh_token)."""
    if not cfg.get("token_largo") or not CONFIG_FILE.is_file():
        return
    try:
        ult = date.fromisoformat(str(cfg.get("token_actualizado", "")))
    except ValueError:
        ult = None
    if ult and (date.today() - ult).days < 7:
        return
    try:
        r = _pedir(f"{API}/refresh_access_token?" + urllib.parse.urlencode(
            {"grant_type": "ig_refresh_token", "access_token": cfg["access_token"]}))
        cfg["access_token"] = r["access_token"]
        cfg["token_actualizado"] = date.today().isoformat()
        CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
        print("Token de Instagram renovado.")
    except (ApiError, KeyError) as e:
        print(f"No se pudo renovar el token: {e}")


def fecha_de_end_time(s: str) -> str:
    """El valor diario de Meta trae el FIN del dia (07:00 UTC = medianoche del Pacifico): el dia es el anterior."""
    dt = datetime.strptime(s, "%Y-%m-%dT%H:%M:%S%z")
    return (dt - timedelta(days=1)).date().isoformat()


def metricas_publicacion(token, media_id):
    for lista in ("reach,views,saved,shares,total_interactions", "reach,saved,shares,total_interactions", "reach"):
        try:
            j = api_get(f"{media_id}/insights", token, metric=lista)
        except ApiError:
            continue
        out = {}
        for m in j.get("data", []):
            try:
                out[m["name"]] = m["values"][0]["value"]
            except (KeyError, IndexError):
                pass
        return out
    return {}


def importar_api(con) -> bool:
    cfg = cargar_config()
    if not cfg:
        print("API de Instagram: falta meta_config.json con el token (ver meta_config.ejemplo.json); se omite.")
        return False
    renovar_token(cfg)
    token, uid = cfg["access_token"], str(cfg["user_id"])
    hoy = date.today().isoformat()
    try:
        cuenta = api_get("me", token, fields="user_id,username,followers_count,follows_count,media_count")
    except ApiError as e:
        if e.code in ERRORES_TOKEN:
            FLAG_FILE.write_text(
                "El token de Instagram caduco o fue revocado.\n"
                "Genera uno nuevo en developers.facebook.com > lagrim-stats > Casos de uso > "
                "Instagram > Configuracion de la API con el inicio de sesion de Instagram > Generar identificador,\n"
                "y pegalo en analitica/meta_config.json (campo access_token).\n", encoding="utf-8")
            print(f"API de Instagram: token invalido ({e}). Se creo NECESITA_TOKEN_META.txt")
        else:
            print(f"API de Instagram: error ({e.code}) {e}")
        return False
    if FLAG_FILE.is_file():
        FLAG_FILE.unlink()
    for campo in ("followers_count", "follows_count", "media_count"):
        if campo in cuenta:
            guardar_serie(con, "api", ETIQUETAS[campo], hoy, cuenta[campo])
    print(f"API de Instagram: @{cuenta.get('username', '?')} · {cuenta.get('followers_count', '?')} seguidores")

    ahora = int(time.time())
    # series diarias (ultimos 30 dias)
    for met in ("reach", "follower_count"):
        try:
            j = api_get(f"{uid}/insights", token, metric=met, period="day", since=ahora - 29 * 86400, until=ahora)
        except ApiError as e:
            print(f"  {met}: no disponible ({e})")
            continue
        for m in j.get("data", []):
            nombre = ETIQUETAS["new_followers" if m["name"] == "follower_count" else m["name"]]
            for v in m.get("values", []):
                guardar_serie(con, "api", nombre, fecha_de_end_time(v["end_time"]), v["value"])
    # totales por dia (ultimos 7 dias completos)
    fallidas = set()
    for i in range(7, 0, -1):
        d = date.today() - timedelta(days=i)
        ini = int(datetime(d.year, d.month, d.day, tzinfo=timezone.utc).timestamp())
        for met in ("views", "profile_views", "accounts_engaged", "total_interactions"):
            if met in fallidas:
                continue
            try:
                j = api_get(f"{uid}/insights", token, metric=met, metric_type="total_value",
                            period="day", since=ini, until=ini + 86400)
                guardar_serie(con, "api", ETIQUETAS[met], d.isoformat(), j["data"][0]["total_value"]["value"])
            except ApiError as e:
                if e.code in ERRORES_TOKEN or e.code == 0:
                    raise
                fallidas.add(met)
                print(f"  {met}: no disponible ({e})")
            except (KeyError, IndexError):
                pass
    # publicaciones
    try:
        j = api_get("me/media", token, limit=25,
                    fields="id,caption,media_type,media_product_type,timestamp,permalink,like_count,comments_count")
    except ApiError as e:
        print(f"  publicaciones: no disponibles ({e})")
        con.commit()
        return True
    cols = ["Fecha", "Tipo", "Descripción", "Alcance", "Vistas", "Likes", "Comentarios",
            "Guardados", "Compartidos", "Interacciones", "Enlace"]
    filas = []
    for m in j.get("data", []):
        ins = metricas_publicacion(token, m["id"])
        txt = " ".join((m.get("caption") or "").split())[:80]

        def g(x):
            return "" if x is None else str(x)
        filas.append({
            "Fecha": (m.get("timestamp") or "")[:10], "Tipo": m.get("media_product_type") or m.get("media_type", ""),
            "Descripción": txt, "Alcance": g(ins.get("reach")), "Vistas": g(ins.get("views")),
            "Likes": g(m.get("like_count")), "Comentarios": g(m.get("comments_count")),
            "Guardados": g(ins.get("saved")), "Compartidos": g(ins.get("shares")),
            "Interacciones": g(ins.get("total_interactions")), "Enlace": m.get("permalink", ""),
        })
    if filas:
        guardar_tabla(con, "API de Instagram", "publicaciones", cols, filas)
        print(f"  publicaciones: {len(filas)}")
    con.commit()
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo-csv", action="store_true")
    ap.add_argument("--solo-api", action="store_true")
    a = ap.parse_args()
    (HERE / "datos").mkdir(exist_ok=True)
    con = sqlite3.connect(DB_FILE)
    init_db(con)
    try:
        if not a.solo_api:
            importar_todos_csv(con)
        if not a.solo_csv:
            try:
                importar_api(con)
            except ApiError as e:  # token invalido a mitad de camino o sin conexion
                print(f"API de Instagram: se interrumpio ({e.code}) {e}")
                con.rollback()
    finally:
        con.close()


if __name__ == "__main__":
    sys.exit(main())
