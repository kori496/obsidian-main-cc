---
tags: [programacion, nodejs, yt-dlp, descargas, lagrim-stats]
actualizado: 2026-10-23
---

Volver a [[Programacion]] · Antes: [[Descargador de YouTube con Node y yt-dlp]] · Panel: [[Panel web lagrim-stats]]

# Descargador de redes: motores, diseño y panel (23 oct 2026)

Continuación de [[Descargador de YouTube con Node y yt-dlp]]. Esta vez el código lo escribió Claude a petición mía (arreglar, ampliar y decorar). Uso personal.

## Dónde está cada cosa
- **Versión Node:** `Documentos\lagrima dlp\` → `server.js`, `public/index.html`, `yt-dlp.exe`, carpeta `descargas/`. Se abre con `node server.js` en `http://localhost:3000`.
- **Versión integrada en el panel:** `Videos beats\analitica\` → `motores_descargas.py`, `web/descargas.php`, `web/descargas_api.php`, carpeta `descargas/`. Es la que se va a usar; el servidor Node ya no hace falta (no se borró).

## Errores del código original y arreglos
- `spawn` sin importar; la descarga se lanzaba dos veces (`yt-dlp` y `./yt-dlp.exe`); `res.send` llamado dos veces ("headers already sent"); `app.use(...)` dentro de la ruta; `"-o --no-playlist"` como un solo argumento; `express.urlencoded` después de las rutas.
- Argumentos de yt-dlp separados uno por uno, con `--` antes de la URL, y `-P` para elegir la carpeta de destino.
- Se valida que la URL empiece por `http://` o `https://`.

## Lo que NO funcionó y por qué
- **«Descarga completada» pero no se veía nada:** el archivo se guardaba en la carpeta desde la que se ejecutaba `node`. Solución: carpeta fija `descargas/` dentro del proyecto.
- **«La descarga falló» aunque sí descargaba:** el servidor confiaba en la ruta que imprime yt-dlp (`--print after_move:filepath`). Con títulos con caracteres especiales (“ ” ｜) la ruta llega distinta en Windows y `existsSync` da falso. **Solución que funcionó:** buscar el archivo **nuevo** dentro de `descargas/` (por fecha de modificación) y registrar el código de salida en consola.
- **Aviso «No supported JavaScript runtime could be found»:** es solo una advertencia (puede faltar alguna calidad de YouTube). Se quita con `--js-runtimes node` o instalando Deno (`winget install DenoLand.Deno`).
- **El archivo del PC volvió a una versión vieja (2 veces):** `server.js` e `index.html` aparecieron con el contenido anterior tras un guardado. Síntoma: la consola no mostraba «código de salida» o la página no tenía la barra de motores. Mismo aprendizaje que en [[Bitácora]] del 23 oct: verificar tamaño o contenido después de guardar, y recargar con Ctrl+F5.

## Funciones
- Botón **Ver descarga**: abre el Explorador con el archivo seleccionado (`explorer /select,"ruta"`; en Node con `windowsVerbatimArguments: true`, en PHP con `popen('start "" explorer.exe /select,"..."')`). Solo deja abrir archivos dentro de `descargas/`.
- **Motores** (barra arriba) y **redes compatibles** por motor:
  - Automático: yt-dlp y, si falla, gallery-dl.
  - yt-dlp: videos de YouTube, TikTok, X, Facebook, Vimeo y cientos más (la lista sale de `--list-extractors`).
  - gallery-dl: fotos, galerías y stories (Instagram, Reddit, Pinterest, Flickr, DeviantArt, Tumblr, Imgur…).
  - Instaloader: posts, reels y stories de Instagram.
  - you-get: videos de muchos sitios que yt-dlp no cubre.
  - Streamlink: grabar directos (corta a la hora).
- **No se agregó spotDL** (música de Spotify, derechos de autor).
- Instalar una vez: `pip install yt-dlp gallery-dl instaloader you-get streamlink`.
- Contenido con sesión (stories, cuentas privadas): `cookies.txt` junto al script (no compartirlo ni subirlo a git). Instaloader: `instaloader --login TU_USUARIO` una vez y variable `LAGRIM_IG_USUARIO`.

## Lo que hablamos sobre redes
- **Stories de Instagram:** piden sesión incluso de cuentas públicas, solo las que puedes ver, duran 24 h, sin marca de agua de Instagram. gallery-dl o Instaloader funcionan mejor que yt-dlp.
- **Marcas de agua:** se baja el archivo tal como lo sirve la plataforma. TikTok a veces entrega versión sin logo, no es garantizado. No se agregó nada para quitar marcas de agua de contenido ajeno.
- **Páginas web que bajan stories:** consultan contenido público, o piden tu usuario/contraseña/cookies (riesgo de robo de cuenta), o traen anuncios y malware. Mejor herramientas locales; nunca dar contraseña ni cookies de sesión a un sitio de terceros.
- Otros repos útiles: gallery-dl (mikf), Instaloader, you-get, Streamlink.

## Diseño (versión Node, ya heredado al panel)
- Estilo tipo Apple, modo oscuro automático, barra de motores arriba.
- Animaciones: fondo con círculos que siguen el cursor, brillo de la tarjeta, botón con efecto imán, destello y onda al hacer clic, chips que se elevan, título con brillo. Respeta `prefers-reduced-motion`.
- Paleta única, **sin RGB**: `#0a84ff`, `#5e5ce6`, `#64d2ff` (más neutros).
- Tipografías: Sora (títulos) y Manrope (texto), desde Google Fonts. Encabezado a la izquierda con etiqueta «Descargador personal».
- En el panel se usa el estilo del propio panel (`estilo.css`, morado), no este.

## Estado y pendientes
- **Sin probar en el PC:** la integración en el panel y los motores nuevos (solo `php -l` y `py_compile`, más probar `listar` en un entorno sin las herramientas). Si algo falla, abrir `analitica/descargas/ultimo_log.txt`. Las banderas de Instaloader, you-get y Streamlink son las menos seguras.
- El panel debe correr solo en tu PC (`localhost`): `descargas_api.php` ejecuta comandos. Nunca exponerlo a internet.
- Idea sin hacer: ventana tipo app (Chrome/Edge con `--app=http://localhost:8080/descargas.php` y un `.bat` que levante todo) o app de escritorio con Electron.
- Si `lagrim-stats` se sube a GitHub: dejar en `.gitignore` `client_secret.json`, `token.json`, `meta_config.json` y `cookies.txt`.
