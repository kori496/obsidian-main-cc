---
tags: [beats, metricool, publicacion, herramienta]
actualizado: 2026-10-23
---

Volver a [[Videos beats]] · Analítica propia: [[Panel web lagrim-stats]] · Alternativas: [[Alternativas a Metricool]]

# Publicar y conectar con Metricool

## Conectar lagrim-stats con Metricool
- Metricool ya tiene datos de Instagram (alcance diario desde el 18 oct; el 20 oct llegó a 48 y el 19 oct a 23).
- Opción 1 (recomendada, sin credenciales): exportar el CSV desde Metricool y subirlo en la pestaña Instagram del panel. Formato sin probar.
- Opción 2: script `importar_metricool.py` que consulte la API. Necesita el token de API de la cuenta de Metricool, que genera el usuario. Claude no lo genera ni lo guarda.

## Subir videos desde Metricool (programar)
- Metricool sí permite programar Reels, Shorts, videos de YouTube y publicaciones de TikTok, con título, texto, tags y miniatura opcional.
- El video tiene que estar en una dirección pública (Google Drive o Dropbox vinculados a Metricool).
- YouTube pide título y si el video es para niños. Instagram y TikTok necesitan el video.
- `autoPublish` true publica solo a la hora programada; false manda aviso a la app para publicar a mano.
- Publicar es una acción pública: Claude pide confirmación de enlace, redes, texto, fecha y modo antes de programar.

## Descartado por ahora
- Subir directo desde lagrim-stats a YouTube, TikTok o Instagram. Requiere permisos de subida en cada API y, en Instagram y TikTok, revisión de la app.
