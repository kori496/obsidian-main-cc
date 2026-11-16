---
tags: [beats, metricool, publicacion, herramienta]
actualizado: 2026-11-14
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

## Revisión del enlace con lagrim-stats (14 nov 2026)
Antes de programar el enlace se consultó Metricool por el conector de Claude (marca `lakrimankv`, id 7509492, zona America/Bogota) del 15 oct al 13 nov y se comparó con `datos/youtube.db`.
- **TikTok:** Metricool solo tiene datos del 19 al 22 oct (vistas 140 y 401, iguales al CSV). Después, nada. Seguidores en `0.0` (dato falso).
- **Instagram:** datos solo hasta el 24 oct, y **corridos un día** respecto a la API (Metricool pone el 48 de alcance el 20 oct; la API lo pone el 19). Después, todo `0.0` o vacío.
- **YouTube:** al día (hasta ~11 nov) y casi igual a la API propia (438 vs 433 el 20 oct), pero el panel ya tiene más detalle por su cuenta.
- Conclusión: hoy Metricool no aporta nada que el panel no tenga. TikTok e Instagram parecen desconectados en Metricool desde el 22-24 oct.
- Cómo sería el enlace: `ejecutar_diario.bat` no puede hablar con el conector de Claude; solo una sesión de Claude puede. Sería "Claude trae los datos cuando se lo pides" (o una tarea programada de Claude), no un enlace en vivo. Uno automático de verdad necesita el token de la API de Metricool, que va en planes de pago.
- Reglas si se hace: `0.0` de Metricool no es un cero real (no importar seguidores en 0 ni días todo en cero); Metricool solo rellena huecos (p. ej. seguidores de TikTok, que el CSV no trae) y el CSV/API gana cuando hay los dos; guardarlo con `tipo='metricool'` para poder borrarlo con un DELETE.
- Decisión (14 nov): reconectar TikTok e Instagram en Metricool y construir el enlace igual.

## Enlace hecho (14 nov 2026)
- **Cómo se usa:** pedirle a Claude «actualiza Metricool» (o `/actualiza-metricool`, archivo `lagrim-stats/.claude/commands/actualiza-metricool.md`). Claude consulta Metricool con el conector, deja el JSON en `analitica/metricool/entrada/` y corre `importar_metricool.py`.
- `importar_metricool.py` guarda en `tiktok_serie` / `instagram_serie` con `tipo='metricool'`. Solo rellena: si el CSV o la API ya tienen esa métrica ese día, la salta. Ignora seguidores en 0, días todo en 0 y el día de hoy. A Instagram le resta 1 día. YouTube no se importa.
- Métricas: TikTok TKEV12 vistas, 03 likes, 04 comentarios, 05 compartidos, 09 visitas al perfil, 07 seguidores, 08 seguidores nuevos. Instagram IGEV01 seguidores, 05 vistas, 06 alcance, 38 interacciones (posts + reels), 42 cuentas que interactuaron, 43 seguidores nuevos.
- Panel: tarjeta **Metricool** en Conexiones (último dato y estado); bloque «Metricool (rellena huecos)» en las pestañas TikTok e Instagram; «Actualizar todo» y `ejecutar_diario.bat` corren también el importador (solo importa JSON pendientes). TikTok sale «Al día (Metricool)» si Metricool trae datos de hace 3 días o menos.
- Resumen (Global): las sumas de TikTok ahora toman el mayor por día y métrica, no la suma, para no contar doble CSV + Metricool.
- **Comprobado:** importado en una copia de la base y luego en la real; los totales del Resumen salen idénticos antes y después. Solo entraron 3 datos (seguidores de TikTok = 1 el 17 oct, seguidores nuevos −1 y 0 el 20-21 oct). El Resumen ahora muestra 1 seguidor en TikTok (dato viejo de Metricool) en vez de «—».
- Copia de la base antes de importar: `datos/youtube.antes-metricool.db`. Deshacer: `DELETE FROM tiktok_serie WHERE tipo='metricool'` (y lo mismo en `instagram_serie`, `*_archivo`).
- **Tarea diaria (14 nov):** tarea programada de Claude `actualiza-metricool-diario` (título «Actualiza Metricool (diario)»), todos los días ~12:30, guardada en modo Auto. Hace lo mismo que «actualiza Metricool». Solo corre con la app de Claude abierta; si está cerrada, corre al abrirla. Archivo: `C:\Users\sharo\.claude\scheduled-tasks\actualiza-metricool-diario\SKILL.md`. No se pudo probar con «Run now» desde la sesión (permiso denegado): falta comprobar que la tarea llega al conector de Metricool.
- **Sin probar:** la tarjeta en el navegador (el navegador integrado no abrió localhost; se revisó el HTML con `php`). Tras reconectar, Metricool seguía sin datos después del 22-24 oct: volver a pedir «actualiza Metricool» en uno o dos días. Metricool no suele recuperar días viejos.
