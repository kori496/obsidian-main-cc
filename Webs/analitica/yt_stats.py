"""Analitica propia de YouTube (lagrim-stats).

Uso:  python yt_stats.py [dias] [--auto]      (por defecto 90 dias)

--auto: para la tarea programada. Si hace falta volver a autorizar (el permiso
caduca cada 7 dias en modo prueba) NO abre el navegador: crea el archivo
NECESITA_AUTORIZAR.txt y termina. Entonces ejecuta "python yt_stats.py" a mano.

Primera vez: abre el navegador para autorizar tu canal y guarda token.json.
Cada ejecucion: guarda los numeros en datos/youtube.db (SQLite, historial que
se va acumulando) y escribe reporte_youtube.md (para leer en Obsidian).
"""
import sqlite3
import sys
from datetime import date, timedelta
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

HERE = Path(__file__).resolve().parent
CLIENT_FILE = HERE / "client_secret.json"
TOKEN_FILE = HERE / "token.json"
FLAG_FILE = HERE / "NECESITA_AUTORIZAR.txt"
DATA_DIR = HERE / "datos"
DB_FILE = DATA_DIR / "youtube.db"
REPORT_FILE = HERE / "reporte_youtube.md"
SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]


def get_credentials(auto=False):
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
            return creds
        except Exception:
            print("El permiso caduco (modo prueba: dura 7 dias). Hay que autorizar de nuevo.")
    if auto:
        FLAG_FILE.write_text(
            "El permiso de YouTube caduco. Abre una terminal en esta carpeta y ejecuta:\n"
            "    python yt_stats.py\nAutoriza en el navegador y este archivo se borra solo.\n",
            encoding="utf-8",
        )
        sys.exit(2)
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_FILE), SCOPES)
    creds = flow.run_local_server(port=0)
    TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    FLAG_FILE.unlink(missing_ok=True)
    return creds


def init_db(con):
    con.executescript(
        """
        CREATE TABLE IF NOT EXISTS channel (
            fecha TEXT PRIMARY KEY, suscriptores INTEGER, vistas_totales INTEGER, videos INTEGER);
        CREATE TABLE IF NOT EXISTS video_publico (
            fecha TEXT, video_id TEXT, titulo TEXT, publicado TEXT,
            vistas INTEGER, likes INTEGER, comentarios INTEGER,
            PRIMARY KEY (fecha, video_id));
        CREATE TABLE IF NOT EXISTS diario (
            dia TEXT PRIMARY KEY, vistas INTEGER, minutos REAL, dur_media REAL,
            subs_ganados INTEGER, subs_perdidos INTEGER);
        CREATE TABLE IF NOT EXISTS video_analitica (
            fecha TEXT, video_id TEXT, vistas INTEGER, minutos REAL,
            dur_media REAL, pct_visto REAL, likes INTEGER, subs_ganados INTEGER,
            PRIMARY KEY (fecha, video_id));
        CREATE TABLE IF NOT EXISTS trafico (
            fecha TEXT, fuente TEXT, vistas INTEGER, minutos REAL,
            PRIMARY KEY (fecha, fuente));
        """
    )


def analytics_query(yta, **kw):
    kw.setdefault("ids", "channel==MINE")
    return yta.reports().query(**kw).execute()


def main():
    args = sys.argv[1:]
    auto = "--auto" in args
    nums = [a for a in args if a.isdigit()]
    days = int(nums[0]) if nums else 90
    if not CLIENT_FILE.exists():
        sys.exit(f"Falta {CLIENT_FILE.name} en esta carpeta.")
    DATA_DIR.mkdir(exist_ok=True)
    creds = get_credentials(auto)
    FLAG_FILE.unlink(missing_ok=True)
    yt = build("youtube", "v3", credentials=creds)
    yta = build("youtubeAnalytics", "v2", credentials=creds)
    today = date.today()
    today_s = today.isoformat()
    start = (today - timedelta(days=days)).isoformat()
    end = (today - timedelta(days=1)).isoformat()

    con = sqlite3.connect(DB_FILE)
    init_db(con)

    # 1) Canal
    ch = yt.channels().list(part="snippet,statistics,contentDetails", mine=True).execute()["items"][0]
    st = ch["statistics"]
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    con.execute(
        "INSERT OR REPLACE INTO channel VALUES (?,?,?,?)",
        (today_s, int(st.get("subscriberCount", 0)), int(st.get("viewCount", 0)), int(st.get("videoCount", 0))),
    )
    print(f"Canal: {ch['snippet']['title']} | {st.get('subscriberCount', 0)} suscriptores | {st.get('viewCount', 0)} vistas")

    # 2) Videos (datos publicos)
    ids, page = [], None
    while True:
        r = yt.playlistItems().list(part="contentDetails", playlistId=uploads, maxResults=50, pageToken=page).execute()
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        page = r.get("nextPageToken")
        if not page:
            break
    titles = {}
    for i in range(0, len(ids), 50):
        r = yt.videos().list(part="snippet,statistics", id=",".join(ids[i:i + 50])).execute()
        for v in r["items"]:
            s = v["statistics"]
            titles[v["id"]] = v["snippet"]["title"]
            con.execute(
                "INSERT OR REPLACE INTO video_publico VALUES (?,?,?,?,?,?,?)",
                (today_s, v["id"], v["snippet"]["title"], v["snippet"]["publishedAt"][:10],
                 int(s.get("viewCount", 0)), int(s.get("likeCount", 0)), int(s.get("commentCount", 0))),
            )
    print(f"Videos leidos: {len(titles)}")

    # 3) Analitica: por dia
    try:
        r = analytics_query(
            yta, startDate=start, endDate=end, dimensions="day", sort="day",
            metrics="views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost",
        )
        for row in r.get("rows", []):
            con.execute("INSERT OR REPLACE INTO diario VALUES (?,?,?,?,?,?)", tuple(row))

        # 4) Analitica: por video
        r = analytics_query(
            yta, startDate=start, endDate=end, dimensions="video", sort="-views", maxResults=200,
            metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,likes,subscribersGained",
        )
        vrows = r.get("rows", [])
        for row in vrows:
            con.execute("INSERT OR REPLACE INTO video_analitica VALUES (?,?,?,?,?,?,?,?)", (today_s, *row))

        # 5) Analitica: fuentes de trafico
        r = analytics_query(
            yta, startDate=start, endDate=end, dimensions="insightTrafficSourceType", sort="-views",
            metrics="views,estimatedMinutesWatched",
        )
        trows = r.get("rows", [])
        for row in trows:
            con.execute("INSERT OR REPLACE INTO trafico VALUES (?,?,?,?)", (today_s, *row))
        daily = con.execute(
            "SELECT SUM(vistas), SUM(minutos), SUM(subs_ganados), SUM(subs_perdidos) FROM diario WHERE dia BETWEEN ? AND ?",
            (start, end),
        ).fetchone()
    except HttpError as e:
        con.commit()
        sys.exit(f"Error en YouTube Analytics API: {e}\n(Comprueba que 'YouTube Analytics API' este activada en Google Cloud.)")
    con.commit()

    # Reporte en markdown
    L = [
        "---", "tags: [beats, metricas, youtube]", f"actualizado: {today_s}", "---", "",
        "Volver a [[Videos beats]] · [[Métricas y revisiones]]", "",
        f"# Reporte YouTube ({start} a {end})", "",
        f"- Suscriptores: **{st.get('subscriberCount', 0)}** · Vistas totales del canal: **{st.get('viewCount', 0)}** · Videos: **{st.get('videoCount', 0)}**",
        f"- En el periodo: **{int(daily[0] or 0)}** vistas · **{round(daily[1] or 0)}** minutos vistos · "
        f"+{int(daily[2] or 0)} / -{int(daily[3] or 0)} suscriptores", "",
        "## Videos por vistas", "",
        "| Video | Vistas | Min. vistos | Duracion media (s) | % visto | Likes | Subs |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for vid, views, mins, dur, pct, likes, subs in vrows:
        t = titles.get(vid, vid).replace("|", "/")
        L.append(f"| {t} | {int(views)} | {round(mins)} | {round(dur)} | {round(pct, 1)} | {int(likes)} | {int(subs)} |")
    L += ["", "## De donde llegan las vistas", "", "| Fuente | Vistas | Min. vistos |", "| --- | --- | --- |"]
    for src, views, mins in trows:
        L.append(f"| {src} | {int(views)} | {round(mins)} |")
    REPORT_FILE.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"Listo. Reporte: {REPORT_FILE.name} | Base de datos: datos/{DB_FILE.name}")


if __name__ == "__main__":
    main()
