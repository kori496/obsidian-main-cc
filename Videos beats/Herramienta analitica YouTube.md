---
tags: [beats, metricas, youtube, herramienta]
actualizado: 2026-10-21
---

Volver a [[Videos beats]] · Contexto en [[Alternativas a Metricool]] · Resultados en [[Métricas y revisiones]]

# Herramienta de analítica de YouTube (lagrim-stats)

Script propio que lee las APIs oficiales de YouTube (Data + Analytics) y guarda el historial. Carpeta: `Videos beats/analitica/`.

## Archivos
- `yt_stats.py`: el script. `requirements.txt`: dependencias.
- `client_secret.json`: credenciales OAuth del proyecto de Google Cloud `lagrim-stats`. **Secreto: no compartir ni subir a GitHub.**
- `token.json`: se crea solo tras autorizar. También secreto.
- `datos/youtube.db`: SQLite con el historial (tablas `channel`, `video_publico`, `diario`, `video_analitica`, `trafico`).
- `reporte_youtube.md`: reporte legible que se reescribe en cada ejecución.

## Cómo correrlo (Windows)
1. Abrir `cmd` en la carpeta `analitica` (barra de direcciones del Explorador, escribir `cmd`).
2. Una sola vez: `pip install -r requirements.txt`
3. `python yt_stats.py` (o `python yt_stats.py 30` para los últimos 30 días; por defecto 90).
4. La primera vez abre el navegador: elegir la cuenta del canal y pulsar Permitir (aviso de "app no verificada" = normal, es tuya).

## Ejecución diaria automática
- `programar_tarea.bat` (doble clic, una sola vez) crea la tarea de Windows **"lagrim-stats YouTube"**: todos los días a las 12:00; si el PC estaba apagado, corre al encenderlo. Usa `ejecutar_diario.bat` y escribe el registro en `datos/log.txt`.
- Corre con `--auto`: si el permiso caducó (cada 7 días en modo prueba) **no abre el navegador**: crea `NECESITA_AUTORIZAR.txt` y termina. Entonces ejecutar `python yt_stats.py` a mano y autorizar; el archivo se borra solo.
- Probar ya: `schtasks /Run /TN "lagrim-stats YouTube"`. Quitarla: `schtasks /Delete /TN "lagrim-stats YouTube" /F`.

## TikTok (CSV de TikTok Studio)
- TikTok no tiene API de analítica accesible, así que se importan los CSV: TikTok Studio > Analytics > Descargar datos.
- Soltar el CSV en `analitica/tiktok/entrada/` y ejecutar `python importar_tiktok.py` (también corre solo dentro de `ejecutar_diario.bat`). Los archivos importados pasan a `tiktok/importados/`.
- Formato real visto (21 oct 2026): `Overview.csv`, UTF-8 con BOM, columnas `Date, Video Views, Profile Views, Likes, Comments, Shares`, fechas tipo `October 14` **sin año** (se asume el año actual; si cae en el futuro, el año pasado).
- El importador es genérico: archivo con fecha + solo números = serie diaria (se une con importaciones anteriores, así crece el historial aunque TikTok solo exporte 7/28/60 días); archivo con una columna de texto (título de video, país) = tabla, el panel muestra la última importada. Entiende fechas en inglés y español y números con coma o punto.
- Tablas en `datos/youtube.db`: `tiktok_archivo`, `tiktok_fila`, `tiktok_serie`.
- Probado con el Overview real y con archivos de ejemplo (Content, FollowerHistory en español, Territories con `;`). Los de ejemplo se inventaron: falta ver un Content.csv real de TikTok y ajustar si sus columnas se comportan distinto.

## Panel web (PHP)
- Movido a [[Panel web lagrim-stats]].

## Estado de Google Cloud
- Proyecto `lagrim-stats`, APIs YouTube Data v3 y YouTube Analytics activadas, cliente OAuth tipo escritorio.
- La app está en modo **Prueba** (usuario de prueba: koripasteles@gmail.com). El permiso caduca cada **7 días**: el script vuelve a abrir el navegador solo. Para evitarlo hay que publicar la app, y Google exige URL de página principal y de política de privacidad (se podrá con el dominio lagrim.art).
- Lo que NO funcionó: el botón "Publicar app" está desactivado sin esas dos URLs; el JSON del cliente solo se descarga al crearlo (se armó a mano con ID y secreto).

## Pendiente
- ✅ Primera ejecución real el 21 oct 2026: funcionó sin errores y devolvió datos por video y fuentes de tráfico (ver [[Métricas y revisiones]]).
- Sumar Instagram (Graph API). TikTok ya entra por CSV (ver arriba): exportar uno cada semana.
