"""Importa los CSV de TikTok Studio a datos/youtube.db (tablas tiktok_*).

Uso:  python importar_tiktok.py

1. En TikTok Studio > Analytics > "Descargar datos" exporta el CSV.
2. Sueltalo en la carpeta tiktok/entrada/
3. Ejecuta este script. Cada archivo importado se mueve a tiktok/importados/.

Funciona con cualquier CSV de TikTok Studio (Overview, Content, Followers...):
- Si trae una columna de fecha y solo numeros -> serie diaria (se une con importaciones
  anteriores, asi el historial crece aunque TikTok solo deje exportar 7-60 dias).
- Si trae una columna de texto (titulo de video, pais...) -> tabla; el panel muestra la ultima.
"""
import csv
import io
import json
import re
import shutil
import sqlite3
import sys
from datetime import date, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENTRADA = HERE / "tiktok" / "entrada"
IMPORTADOS = HERE / "tiktok" / "importados"
DB_FILE = HERE / "datos" / "youtube.db"

MESES = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7,
    "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "sept": 9,
    "oct": 10, "nov": 11, "dec": 12,
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7,
    "agosto": 8, "septiembre": 9, "setiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
    "ene": 1, "abr": 4, "ago": 8, "dic": 12,
}


def leer_texto(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-16", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except (UnicodeDecodeError, UnicodeError):
            continue
    return raw.decode("utf-8", errors="replace")


def leer_csv(path: Path):
    texto = leer_texto(path)
    try:
        dialect = csv.Sniffer().sniff(texto[:4096], delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    filas = [f for f in csv.reader(io.StringIO(texto), dialect) if any(c.strip() for c in f)]
    if len(filas) < 2:
        return [], []
    cols = [c.strip() for c in filas[0]]
    datos = [dict(zip(cols, [c.strip() for c in f])) for f in filas[1:]]
    return cols, datos


def a_numero(s):
    """'1,234' '1.234' '12,5%' '3' -> float, o None si no es numero."""
    s = (s or "").strip().replace(" ", "").replace(" ", "")
    if s in ("", "-", "--"):
        return None
    pct = s.endswith("%")
    s = s.rstrip("%")
    if re.fullmatch(r"-?\d+", s):
        v = float(s)
    elif re.fullmatch(r"-?\d{1,3}(,\d{3})+(\.\d+)?", s):
        v = float(s.replace(",", ""))
    elif re.fullmatch(r"-?\d{1,3}(\.\d{3})+(,\d+)?", s):
        v = float(s.replace(".", "").replace(",", "."))
    elif re.fullmatch(r"-?\d+[.,]\d+", s):
        v = float(s.replace(",", "."))
    else:
        return None
    return v


def a_fecha(s, hoy=None, dia_primero=True):
    """Devuelve date o None. Soporta '2026-10-14', 'October 14', '14 de octubre', '14/10/2026', '14/10'."""
    hoy = hoy or date.today()
    s = (s or "").strip().lower()
    if not s:
        return None
    m = re.fullmatch(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})(?:[ t].*)?", s)
    if m:
        return _fecha(int(m[1]), int(m[2]), int(m[3]))
    m = re.fullmatch(r"(\d{1,2})[/.-](\d{1,2})(?:[/.-](\d{2,4}))?(?: .*)?", s)
    if m:
        a, b = int(m[1]), int(m[2])
        d, mo = (a, b) if dia_primero else (b, a)
        if mo > 12:
            d, mo = mo, d
        y = int(m[3]) if m[3] else None
        if y is not None and y < 100:
            y += 2000
        return _fecha(y, mo, d, hoy)
    s2 = re.sub(r"[,.]", " ", s).replace(" de ", " ")
    m = re.fullmatch(r"([a-záéíóú]+) +(\d{1,2})(?:(?:st|nd|rd|th))?(?: +(\d{4}))?", s2.strip())
    if m and m[1] in MESES:
        return _fecha(int(m[3]) if m[3] else None, MESES[m[1]], int(m[2]), hoy)
    m = re.fullmatch(r"(\d{1,2})(?:(?:st|nd|rd|th))? +([a-záéíóú]+)(?: +(\d{4}))?", s2.strip())
    if m and m[2] in MESES:
        return _fecha(int(m[3]) if m[3] else None, MESES[m[2]], int(m[1]), hoy)
    return None


def _fecha(y, mo, d, hoy=None):
    try:
        if y is None:
            hoy = hoy or date.today()
            f = date(hoy.year, mo, d)
            if f > hoy:  # fecha sin ano que cae en el futuro = ano pasado
                f = date(hoy.year - 1, mo, d)
            return f
        return date(y, mo, d)
    except ValueError:
        return None


def tipo_de(nombre: str) -> str:
    stem = Path(nombre).stem.lower()
    stem = re.sub(r"^[0-9a-f]{8}-", "", stem)          # prefijo de subida
    stem = re.sub(r"[\d_\-\s().]+", " ", stem).strip()  # fechas, (2), etc.
    return stem or "datos"


def clasificar(cols, datos):
    """Devuelve (col_fecha, cols_numericas) si es serie diaria, o (None, None) si es tabla."""
    if not datos:
        return None, None
    n = len(datos)
    # dia primero o mes primero: mirar si algun valor tiene un numero > 12 en alguna posicion
    for c in cols:
        vals = [r.get(c, "") for r in datos]
        fechas = [a_fecha(v) for v in vals]
        if sum(f is not None for f in fechas) >= 0.8 * n and len({f for f in fechas if f}) >= 0.8 * n:
            otras = [x for x in cols if x != c]
            # columna de texto (ni numero ni fecha) => es una lista, no una serie
            hay_texto = False
            for o in otras:
                ov = [r.get(o, "") for r in datos if r.get(o, "").strip()]
                if ov and sum(a_numero(v) is not None for v in ov) < 0.8 * len(ov) and sum(a_fecha(v) is not None for v in ov) < 0.8 * len(ov):
                    hay_texto = True
            if hay_texto:
                return None, None
            nums = [o for o in otras if any(a_numero(r.get(o, "")) is not None for r in datos)]
            return (c, nums) if nums else (None, None)
    return None, None


def init_db(con):
    con.executescript(
        """
        CREATE TABLE IF NOT EXISTS tiktok_archivo (
            id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, tipo TEXT, importado TEXT,
            filas INTEGER, columnas TEXT, es_serie INTEGER);
        CREATE TABLE IF NOT EXISTS tiktok_fila (
            archivo_id INTEGER, n INTEGER, datos TEXT, PRIMARY KEY (archivo_id, n));
        CREATE TABLE IF NOT EXISTS tiktok_serie (
            tipo TEXT, metrica TEXT, fecha TEXT, valor REAL, PRIMARY KEY (tipo, metrica, fecha));
        """
    )


def importar(path: Path, con) -> str:
    cols, datos = leer_csv(path)
    if not datos:
        return f"{path.name}: vacio o sin filas, se omite"
    tipo = tipo_de(path.name)
    col_f, nums = clasificar(cols, datos)
    ahora = datetime.now().isoformat(timespec="seconds")
    cur = con.execute(
        "INSERT INTO tiktok_archivo (nombre, tipo, importado, filas, columnas, es_serie) VALUES (?,?,?,?,?,?)",
        (path.name, tipo, ahora, len(datos), json.dumps(cols, ensure_ascii=False), 1 if col_f else 0),
    )
    aid = cur.lastrowid
    for i, r in enumerate(datos):
        con.execute("INSERT INTO tiktok_fila VALUES (?,?,?)", (aid, i, json.dumps(r, ensure_ascii=False)))
    if col_f:
        # dia primero salvo que los datos indiquen lo contrario
        for r in datos:
            f = a_fecha(r[col_f])
            if not f:
                continue
            for m in nums:
                v = a_numero(r.get(m, ""))
                if v is not None:
                    con.execute("INSERT OR REPLACE INTO tiktok_serie VALUES (?,?,?,?)", (tipo, m, f.isoformat(), v))
        return f"{path.name}: serie diaria '{tipo}' ({len(datos)} dias, metricas: {', '.join(nums)})"
    return f"{path.name}: tabla '{tipo}' ({len(datos)} filas, columnas: {', '.join(cols)})"


def main():
    ENTRADA.mkdir(parents=True, exist_ok=True)
    IMPORTADOS.mkdir(parents=True, exist_ok=True)
    archivos = sorted(p for p in ENTRADA.iterdir() if p.suffix.lower() == ".csv")
    if not archivos:
        print(f"No hay CSV nuevos en {ENTRADA}. Exporta desde TikTok Studio y sueltalos ahi.")
        return
    (HERE / "datos").mkdir(exist_ok=True)
    con = sqlite3.connect(DB_FILE)
    init_db(con)
    for p in archivos:
        try:
            print(importar(p, con))
            con.commit()
            destino = IMPORTADOS / f"{datetime.now():%Y-%m-%d_%H%M%S}_{p.name}"
            shutil.move(str(p), str(destino))
        except Exception as e:  # un archivo raro no debe frenar a los demas
            con.rollback()
            print(f"{p.name}: ERROR {e}")
    con.close()


if __name__ == "__main__":
    sys.exit(main())
