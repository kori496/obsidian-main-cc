---
tags: [beats, metricas, herramienta, web, descargas]
actualizado: 2026-10-24
---

Volver a [[Herramienta analitica YouTube]] · Skills en [[Skills]] · Instagram: [[API de Instagram (Meta) - configuración y errores]] · Descargas: [[Descargador de redes - motores, diseño y panel]]

# Panel web lagrim-stats (PHP)

Panel de lectura de la base de datos `datos/youtube.db`, en `Webs/analitica/web/`.

## Cómo se abre
- `abrir_dashboard.bat` levanta `http://localhost:8080` con `php -S localhost:8080 -t web`. Requiere PHP con la extensión `pdo_sqlite` activada.
- **Importante:** servir siempre con `web/` como raíz, así `client_secret.json` y `token.json` no quedan accesibles por web.
- Si algún día se sube a un hosting: subir solo `web/`, apuntar la base de datos con la variable de entorno `LAGRIM_DB` y protegerlo con contraseña (son tus números).

## Páginas
- `web/global.php` (Global), `web/index.php` (YouTube), `web/tiktok.php` (TikTok), `web/instagram.php` (Instagram) y `web/descargas.php` (Descargas). Estilo común en `web/estilo.css`.
- **YouTube:** lee `datos/youtube.db` (solo lectura). Muestra KPIs, vistas/minutos/suscriptores por día, historial del canal, tabla ordenable de todos los videos (analítica del periodo + datos públicos), historial de un video a lo largo del tiempo y fuentes de tráfico. Avisa si el permiso caducó o los datos tienen 2 días o más.
- **TikTok:** tarjetas y gráfico por métrica de cada serie (el Overview primero), tablas ordenables de los archivos con texto e historial de importaciones.
- **Subir CSV (22 oct 2026):** botón "Subir CSV de TikTok" arriba a la derecha en la pestaña TikTok. Guarda el archivo en `tiktok/entrada/` y ejecuta `importar_tiktok.py`. Usa `python` por defecto; si tu comando es otro (p. ej. `py`), define la variable `LAGRIM_PYTHON`. Sin probar todavía en el PC.
- **Instagram (22 oct 2026):** igual que TikTok (tarjetas, gráficos, tablas, botón de subir CSV), pero los datos vienen sobre todo de la API de Meta con `importar_instagram.py` (cuenta, alcance y seguidores nuevos por día, métricas de 7 días, últimas 25 publicaciones). Lee el token de `meta_config.json` (modelo en `meta_config.ejemplo.json`). Si el token falla, crea `NECESITA_TOKEN_META.txt` y el panel muestra un aviso. También corre en `ejecutar_diario.bat`.
- **Global · Todas las plataformas (24 oct 2026):** panel arriba con la suma de las tres redes (seguidores + suscriptores, vistas, interacciones, interacciones por 100 vistas), indicando qué redes entran en cada suma. La tasa solo usa redes con vistas e interacciones.
- **Global (22 oct 2026):** resumen por red (seguidores o suscriptores, vistas y interacciones de los últimos 28 días, con los días que tienen dato), gráfico de vistas por día de las tres redes, tabla comparativa y barras de progreso hacia las metas de agosto 2027 (10.000 suscriptores en YouTube; 30.000 seguidores sumando TikTok e Instagram) con el ritmo diario necesario. Instagram usa el alcance mientras la API no dé vistas por día. Un «—» significa que no hay dato, no cero.
- **Descargas (23 oct 2026):** pestaña `web/descargas.php` con el descargador: barra de motores (Automático, yt-dlp, gallery-dl, Instaloader, you-get, Streamlink), redes compatibles por motor y botón «Ver descarga» que abre el Explorador con el archivo seleccionado. Usa `web/descargas_api.php` y `motores_descargas.py` (en `analitica/`), igual que el botón de subir CSV usa Python con `LAGRIM_PYTHON`. Guarda en `analitica/descargas/` y deja `ultimo_log.txt`. Instalar una vez: `pip install yt-dlp gallery-dl instaloader you-get streamlink`. Contenido con sesión: `cookies.txt` junto a `motores_descargas.py` (no compartirlo). Instaloader: `LAGRIM_IG_USUARIO` + `instaloader --login`. **Sin probar en el PC** (solo `php -l` y `py_compile`). Se agregó el enlace «Descargas» al menú de las otras cuatro páginas. Historia completa en [[Descargador de redes - motores, diseño y panel]].

## Notas técnicas
- **Código común (24 oct 2026):** todo lo compartido vive en `web/comun.php` (`h`, `n`, `num`, `aNum`, `abrirDb`, `cabecera` con el menú, `manejarSubida`, `cargarRed`, `pintarBloques`, `pintarTablas`) y `web/comun.js` (tablas `table.ord`, `col()`, `graficosSerie`). Para añadir una pestaña al menú se cambia solo `cabecera()`. Si se crea otra red con CSV, basta con tablas `<red>_serie/_archivo/_fila` y un `importar_<red>.py`.
- Los gráficos usan Chart.js desde cdnjs (necesita internet); las tablas funcionan sin él.
- Los gráficos del historial (canal y video) solo muestran línea cuando hay 2 o más días guardados.
- Global e Instagram probados con datos de ejemplo (PHP 8.3, sin avisos), pero no con el token real de Instagram ni en el navegador. Lo anterior: probado con datos de ejemplo y un Chart.js simulado (sin errores de JavaScript, orden de tabla y selector de video OK). No probado todavía con tu PHP ni con el navegador real.
- `descargas_api.php` ejecuta comandos (`exec`, `popen`): el panel debe correr solo en `localhost`, nunca expuesto a internet.

## Pendientes
- ~~Quitar de TikTok la tabla «Sep oct»~~ (archivo id 3 en `tiktok_archivo`, CSV de Instagram importado por error): **decidido dejarla** (24 oct 2026). No afecta a las sumas.

## Skills relacionadas
- `web-design-guidelines`: revisar accesibilidad y buenas prácticas del panel. Ver [[Skills]].
