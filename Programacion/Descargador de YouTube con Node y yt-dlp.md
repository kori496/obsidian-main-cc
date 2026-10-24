---
tags: [programacion, nodejs, yt-dlp, aprendizaje]
actualizado: 2026-10-23
---

Volver a [[Programacion]]

# Descargador de YouTube con Node y yt-dlp (aprendizaje paso a paso)

Proyecto personal de uso propio. Carpeta: `descargador/` (en el PC, `lagrim dlp` dentro de OneDrive, según la ruta del error). Se hizo a mano, guiado paso a paso, sin que Claude escribiera el código.

> **Actualización (23 oct, más tarde):** el proyecto siguió, esta vez con el código escrito por Claude a mi petición. La carpeta real en el PC es `Documentos\lagrima dlp`. Todo lo nuevo está en [[Descargador de redes - motores, diseño y panel]].

## Decisiones
- Se descartó copiar sitios como y2mate. Se hace una app propia.
- Motor de descarga: **yt-dlp** (Python), llamado desde Node. Razón: es la herramienta más mantenida; las librerías JS para YouTube se rompen seguido.
- Stack elegido: **Node.js + Express** (JavaScript). Se evaluó Flask (Python) y se descartó para este proyecto por preferencia de lenguaje.
- Aviso: los términos de YouTube no permiten descargar fuera de sus herramientas. Uso previsto: contenido propio, licencia libre o con permiso.

## Conceptos aprendidos

### package.json y npm
- `npm init -y` crea `package.json`: nombre del proyecto, punto de entrada (`main`) y lista de dependencias.
- `npm install express` descarga Express a `node_modules/` y lo registra en `dependencies`.
- `node_modules` **no se sube a Git**: es código de terceros, pesa mucho y se regenera con `npm install`. Se ignora con un archivo `.gitignore` que contiene `node_modules/`.
- Para llevar el proyecto a otra computadora: copiar sin `node_modules`, luego `npm install`, y luego `node server.js`.
- Error "Cannot find module 'express'": casi siempre significa que se ejecuta desde una carpeta donde no está `node_modules` o que no se instaló. Solución: estar en la carpeta del proyecto y ejecutar `npm install express`.

### Express y el servidor
- Express simplifica el módulo `http` de Node: rutas con `app.get(...)` y `app.post(...)`.
- `require("express")` carga el módulo (CommonJS).
- `app.listen(3000)` abre un puerto. El proceso **no termina** mientras escucha; por eso la terminal se queda esperando. Se detiene con `Ctrl + C`.
- Una URL sin ruta registrada responde `Cannot GET /otra` (404). Express enruta cada URL a su manejador.
- `req` = lo que llega (dirección, cabeceras, cuerpo). `res` = lo que se devuelve.

### HTML básico del formulario
- `<form action="/descargar" method="post">`: a dónde se envía y cómo.
- `<input type="text" name="url">`: el `name` es la clave con la que el servidor lee el dato.
- `<button type="submit">`: envía el formulario.
- `app.use(express.static("public"))`: sirve la carpeta `public/` tal cual. Por eso se abre `http://localhost:3000/index.html`.

### GET y POST
- **GET**: pide información sin cambiar nada en el servidor. Los datos (si los hay) van en la URL (`?url=...`). Visible en historial y registros.
- **POST**: envía datos para que el servidor haga algo con ellos. Los datos viajan en el **cuerpo** de la petición, no en la dirección.
- No es "crear un archivo" ni "devolver los datos enviados": lo que define a POST es que el servidor procesa los datos. La respuesta depende de lo que el servidor decida devolver.
- Por eso la descarga usa POST: dispara una acción (crear un archivo).

### Leer el cuerpo en Express
- `app.use(express.urlencoded({ extended: true }));` convierte el cuerpo del formulario en `req.body`. Debe ir **antes** de las rutas.
- Con `req.body.url` se lee el campo cuyo `name` es `url`.
- Error `TypeError: Cannot read properties of undefined (reading 'url')`: `req.body` está vacío. Causas vistas en el chat:
  1. Falta `express.urlencoded` o está después de la ruta.
  2. Se abrió `/descargar` escribiéndolo en la barra (eso es GET, sin cuerpo). El POST solo se activa desde el formulario en `/index.html`.
  3. El formulario no tiene `method="post"` (por defecto usa GET).
- Ruta de prueba que funcionó: `res.send('url recibida: ' + url)`.

## Paso 5 (en curso): ejecutar yt-dlp desde Node
- Comando de referencia en terminal: `yt-dlp -o "%(title)s.%(ext)s" "URL"`.
  - `-o`: plantilla del nombre de salida. `%(title)s` = título del video, `%(ext)s` = extensión.
- En Node se usa `child_process.spawn`, con programa y argumentos separados en un arreglo:
  `spawn("yt-dlp", ["-o", "%(title)s.%(ext)s", url])`.
  - Por qué separado: la URL entra como un elemento más; espacios o caracteres especiales no rompen el comando.
- `spawn` no espera por sí solo: el proceso tarda, y la ruta debe esperar al evento `close` y revisar el código de salida (0 = bien).
- Si Node no encuentra `yt-dlp`, comprobar `yt-dlp --version` en la misma terminal donde corre `node server.js`.
- Instalar antes: `winget install yt-dlp` y `winget install ffmpeg` (FFmpeg hace falta para convertir a MP3). Cerrar y abrir la terminal después para que actualice el PATH.

## Pendiente (resuelto el 23 oct, ver [[Descargador de redes - motores, diseño y panel]])
- Escribir la ruta `POST /descargar` con `spawn` y el evento `close`.
- Decidir la carpeta de destino de las descargas.
- Opcional: validar que la URL sea de YouTube, selector MP4/MP3, mensaje de "descargando...".

## Versión inicial de referencia (Python, no usada)
Se generó una versión en Flask con yt-dlp como librería (`yt_dlp.YoutubeDL`). Se descartó en favor de Node. Ver las opciones `format`, `outtmpl`, `noplaylist` y `FFmpegExtractAudio` si se quiere portar la lógica.
