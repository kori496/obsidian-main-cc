---
tags: [bitacora]
actualizado: 2026-10-24
---

# 📓 Bitácora

Registro corto de lo que Claude hace en este vault. Lo más reciente arriba. Reglas en `CLAUDE.md`.

## 2026-10-24 (alta de productos: canvas)
- Nuevo canvas `Programacion/Mapa Alta de productos.canvas`: arranque, interfaz, servidor, disco, flujos (guardar, Siigo, BarTender, base vieja y conflictos), reglas de negocio y estado de las pruebas. Enlazado desde [[Programacion]] y [[Alta de productos - herramienta portable para Siigo]].

## 2026-10-24 (alta de productos: versión 2, carpeta instalable)
- Opción A elegida: Node.js incluido + interfaz en el navegador. Carpeta en `Documentos\alta de productos\` y paquete `paquete\AltaDeProductos_v2_2026-10-24.zip` (34 MB). Sin internet, guardado automático con copias, BarTender directo, Excel de Siigo escrito sobre la plantilla sin tocar su formato (lotes de 500, validación de obligatorias y listas).
- Probado con una plantilla de prueba hecha en Excel, con Playwright + Edge (22 pruebas) e instalando en limpio. Corregido un error con espacios en la ruta de bartend.exe. Falta la plantilla real de Siigo y probar BarTender en la tienda. `productos.html` sin cambios.
- Nota tocada: [[Alta de productos - herramienta portable para Siigo]] (secciones Archivo, Versión 2, Pendiente, Decisiones y Riesgos).

## 2026-10-23 (alta de productos para Siigo)
- Herramienta portable para dar de alta productos, reemplazo de la creación de productos de CRS: `Programacion\Alta de productos\productos.html`. Un solo archivo, sin instalación, guarda una base `.sqlite` y exporta CSV. Nota: [[Alta de productos - herramienta portable para Siigo]].
- Revisada la guía de Siigo «Subir desde Excel Productos»: plantilla desde Configuración → Productos y servicios → Importación, máximo 500 registros, no modificar columnas. Falta la plantilla real para generar el Excel.

## 2026-10-24 (alta de productos: vincular BarTender)
- Revisada la ayuda de BarTender sobre la línea de comandos y anotados los pasos para imprimir etiquetas desde la herramienta, qué está confirmado (`/F`, `/P`, `/C`, `/D`) y qué no (`/PRN`, `/X`, ediciones con Commander). Ver [[Alta de productos - herramienta portable para Siigo]].

## 2026-10-24 (alta de productos: formato carpeta instalable)
- Decisión: el proyecto ya no tiene que ser un solo HTML; puede ser una carpeta instalable para pocas computadoras. Prompt actualizado en [[Prompt - seguir Alta de productos con Claude Code]] (propone estructura antes de reescribir) y decisión anotada en [[Alta de productos - herramienta portable para Siigo]].

## 2026-10-24 (alta de productos: prompt para Claude Code)
- Nueva nota [[Prompt - seguir Alta de productos con Claude Code]] con el prompt para continuar el proyecto en VS Code. Se volvieron a añadir el enlace en el índice [[Programacion]] y la sección de códigos que no se repiten en la nota del proyecto: el PC había vuelto a una versión vieja tras guardar.

## 2026-10-23 (alta de productos: códigos que no se repiten)
- `productos.html`: índice único en la base, contador que nunca baja, códigos de productos eliminados reservados y carga de códigos existentes de CRS o Siigo. Detalles y límites en [[Alta de productos - herramienta portable para Siigo]].

## 2026-10-23 (alta de productos: precio con ganancia)
- `productos.html`: campo «Ganancia sobre el costo (%)» (30% por defecto) y redondeo (terminar en 900), con el precio calculado y botón «Usar este precio». Ejemplo: 76.000 → 117.572 → 117.900. Ver [[Alta de productos - herramienta portable para Siigo]].

## 2026-10-23 (alta de productos: código de barras propio)
- `productos.html`: botón Generar y generación automática de EAN-13 con prefijo 20 a 29 (uso interno GS1), sin repetir códigos. Notas y límites en [[Alta de productos - herramienta portable para Siigo]].

## 2026-10-23 (alta de productos: reglas DIAN)
- `productos.html`: precio con IVA incluido y desglose (base, IVA), tipos IVA 19%, 5%, exento, excluido y no gravado, unidad de medida, validación GS1 del código de barras y avisos de INC. Detalles y límites en [[Alta de productos - herramienta portable para Siigo]].

## 2026-10-23 (alta de productos: plantillas y BarTender)
- `Programacion\Alta de productos\productos.html`: botón Plantilla por producto, referencia en vez de código interno, grupo Confecciones con opción Otro, y etiqueta/impresión con BarTender vía CSV + .bat. Sin probar en el PC. Detalles en [[Alta de productos - herramienta portable para Siigo]].

## 2026-10-23 (descargador de redes)
- Descargador Node (`Documentos\lagrima dlp`): código arreglado, carpeta `descargas/`, botón «Ver descarga», 6 motores con barra y redes por motor, diseño tipo Apple con paleta de tres azules y animaciones. Resuelto: decía «falló» aunque descargaba (la ruta que imprime yt-dlp no sirve con caracteres especiales; ahora se busca el archivo nuevo en `descargas/`).
- Integrado en lagrim-stats como pestaña **Descargas** (`web/descargas.php`, `web/descargas_api.php`, `motores_descargas.py`) y enlace en el menú de las demás páginas. Sin probar en el PC. Notas: [[Descargador de redes - motores, diseño y panel]], [[Panel web lagrim-stats]], [[Descargador de YouTube con Node y yt-dlp]] (se agregó una actualización arriba y se marcó el Pendiente como resuelto).
- Se vio otra vez que el PC vuelve a una versión vieja de `server.js` e `index.html` tras guardar; verificar después de guardar.

## 2026-10-23 (programación)
- Aprendizaje guiado de un descargador de YouTube con Node.js, Express y yt-dlp (sin que Claude escribiera el código). Nueva nota [[Descargador de YouTube con Node y yt-dlp]], dentro de la nueva carpeta `Programacion/` con índice [[Programacion]]. Cubre npm/package.json/node_modules, `.gitignore`, Express y `app.listen`, formulario HTML, GET vs POST, `express.urlencoded` y `req.body`, el error "Cannot read properties of undefined", y el plan de `spawn` para yt-dlp (pendiente de escribir).
- Mismo contenido copiado a Notion como página privada (borrador).

## 2026-10-23
- CLEAN EYES (= cancer type beat): 2 videos oscuros rojo sangre en `Documentos\marketing\clean_eyes\` (A: loop seco → efectos → mezcla de los compases 9-12; B: fragmento en bucle de los compases 57-64). Nueva nota [[CLEAN EYES - loop a mezcla y fragmento (oscuro rojo)]], enlazada desde [[Videos beats]]. El disco C: se llenó durante el trabajo (proyecto en OneDrive).
- eyesofdirty: tras bajar las capas de GIF del drop, la verificación pasa entera (máximo 3 destellos por segundo).
- Video eyesofdirty (2): más destellos (uno por compás, hasta 3/s en el drop), pulso en cada tiempo, sacudida en cada compás y los 6 GIFs de `marketing` teñidos de azul (ciudad de fondo, tarjetas, explosión en el drop). Anotado en [[Prompt vorty - how to sound like eyesofdirty (voz y drop)]].
- Video eyesofdirty corregido: sin silencio antes de las drums (y sin congelado/oscurecido) y paleta azul intenso + letras blancas + fondo negro. Mismo archivo en `Documentos\marketing`. Anotado en [[Prompt vorty - how to sound like eyesofdirty (voz y drop)]].

## 2026-10-23
- Panel lagrim-stats: vista **Global** (`web/global.php`) con YouTube, TikTok e Instagram juntos y progreso hacia las metas de agosto 2027. Pestaña **Instagram** (`web/instagram.php`) con gráficos por publicación para el CSV de Meta. Se quitó `mb_strtolower` porque el PHP de Windows no tiene `mbstring`. Notas en [[Panel web lagrim-stats]] y [[API de Instagram (Meta) - configuración y errores]].
- Corregida la lectura de kill4meeee: sí funciona (338 vistas en YouTube y 127 y 162 en TikTok). Ver [[Métricas y revisiones]] y [[Estilo de videos de vorty]].
- Nuevo beat **Clean Eyes** (type beat de Eyes of Dirty, 151 BPM, A minor, oscuro y agresivo, en `marketing\`). Título, descripción, 20 tags y textos de TikTok. Ver [[Clean Eyes - beat y publicación]].
- Nuevo prompt para Claude Code: tres estilos por beat (layer by layer ya hecho, loop a mezcla final y fragmento con enlace). Ver [[Prompt tres estilos por beat (layer, loop a mezcla, fragmento)]].
- Revisado si se puede conectar lagrim-stats con Metricool. Metricool ya tiene datos de Instagram. Opción recomendada: exportar CSV y subirlo al panel. Y se puede programar videos desde Metricool con enlace público. Ver [[Publicar y conectar con Metricool]].
- Decisión: textos en inglés en títulos, descripciones y textos de video. Español solo como línea extra al final de la descripción.
- Aprendido: el primer guardado de un archivo existente en el PC no siempre se aplica. Verificar después de guardar (tamaño o contenido).

## 2026-10-22
- Hecho el video "how to sound like eyesofdirty" (voz IA + piano roll por capas + drop en el compás 9): `Documentos\marketing\lagrimankv_how_to_sound_like_eyesofdirty.mp4`, proyecto en `C:\Users\sharo\remotion\eyesofdirty`. Fase 0 confirmó BPM, desfases y drop. Resultados, verificación y errores (contraste, yuvj420p, oscurecido pegado en el drop) en [[Prompt vorty - how to sound like eyesofdirty (voz y drop)]].
- Pestaña Instagram del panel: gráficos por publicación (alcance, vistas, interacciones) para el CSV de Meta, que trae un dato por post. Respuesta "qué contenido funcionó más" anotada en [[Métricas y revisiones]]; corregida la lectura de kill4meeee en [[Estilo de videos de vorty]] (338 vistas, sí funciona). Nota: el primer guardado de un archivo existente en el PC a veces no se aplica; verificar después de guardar.
- Panel lagrim-stats: nueva pestaña **Instagram** (`web/instagram.php`, API de Meta o CSV) y nueva vista **Global** (`web/global.php`) con YouTube, TikTok e Instagram juntos: resumen por red, vistas por día, tabla comparativa y progreso hacia las metas de agosto 2027. Nuevo `importar_instagram.py`, añadido a `ejecutar_diario.bat`. Probado con datos de ejemplo, no con tu token real. Detalles en [[Panel web lagrim-stats]] y [[API de Instagram (Meta) - configuración y errores]].
- Panel TikTok (`analitica/web/tiktok.php`): botón "Subir CSV de TikTok" arriba a la derecha. Guarda el CSV en `tiktok/entrada/` y ejecuta `importar_tiktok.py` (ruta de Python configurable con `LAGRIM_PYTHON`, por defecto `python`). Estilos en `estilo.css`. Sin probar en el PC todavía; `php -l` sin errores.
- Anotados en [[Métricas y revisiones]] los datos de 22 oct (YouTube 1.338 vistas, TikTok 541) y recomendaciones.
- Anotados en [[Estilo de videos de vorty]] los resultados de kill4meeee: flojos en YouTube (53 vistas), mejores en TikTok (289). woeklifeee no aparece en el reporte.

## 2026-10-21
- Revisados los archivos del beat "eyes of dirty" (`Presets\Scores`) y actualizado [[Prompt vorty - how to sound like eyesofdirty (voz y drop)]] sin marcadores: 151 BPM, compás 1 del mp3 en 0,030 s, drop confirmado en el compás 9, tonalidad medida A# menor (el archivo dice Am), MIDI con notas. Dudas: el WAV de piano 1 coincide poco con su MIDI, y el archivo con cortes trae las notas del lead.
- Nuevo prompt [[Prompt vorty - how to sound like eyesofdirty (voz y drop)]]: voz IA al inicio, recuadros MIDI que se suman, piano 1 normal y con cortes, drop en el compás 9. Lleva Fase 0 de verificación porque los archivos del beat no se pudieron revisar; faltan datos del beat (BPM, escala, rutas). La voz dice "sound like", no "make a beat like".
- Voz del primer video lista: `analitica/eyes of dirty vox robotic.mp3` (Aria + preset robot, editada en FL) y sus tiempos por palabra en `eyes of dirty vox robotic.json` (alineados con correlación 0,91). `voz_gancho.py` confirmado funcionando en el PC. Anotado en [[Referencias de voz en shorts]]. Falta elegir beat y paleta.
- Decidido el primer video con gancho de voz: "how to sound like eyesofdirty", voz IA procesada. Nuevo script `Videos beats/Scripts voz/voz_gancho.py` (edge-tts + ffmpeg, 3 presets, JSON de tiempos por palabra, vista previa con beat). Documentado en [[Referencias de voz en shorts]]. La parte edge-tts sin probar.
- Nueva nota [[Referencias de voz en shorts]]: análisis de 3 referencias con voz al inicio (voz recortada ~3 s, drop con graves a ~3,2 s, texto sincronizado) y plan de prueba con/sin voz. Enlazada desde [[Videos beats]]. No se pudo escuchar el audio, solo ver el espectrograma.
- Módulo TikTok: `importar_tiktok.py` (CSV de TikTok Studio a la base de datos, genérico, probado con el Overview real) y página `web/tiktok.php` con pestañas YouTube/TikTok. Primer dato de TikTok anotado en [[Métricas y revisiones]]: 541 vistas el 19-20 oct (Metricool decía 0). Detalles en [[Herramienta analitica YouTube]].
- Panel web PHP (`analitica/web/index.php`) y ejecución diaria automática (`programar_tarea.bat`, `ejecutar_diario.bat`, `abrir_dashboard.bat`); `yt_stats.py` ahora acepta `--auto` (no abre el navegador si el permiso caducó). Documentado en [[Herramienta analitica YouTube]]. Panel probado solo con datos de ejemplo.
- `yt_stats.py` probado con el canal real: OK. Primer reporte anotado en [[Métricas y revisiones]]; corrige la lectura de Metricool (el Short top es "cooking boom bap at the skatepark", 315 vistas; Shorts retienen ~32 % vs ~14 % de los type beats). Actualizada [[Herramienta analitica YouTube]].
- Creado el script `Videos beats/analitica/yt_stats.py` y la nota [[Herramienta analitica YouTube]] (proyecto Google Cloud lagrim-stats, OAuth en modo prueba, `client_secret.json` armado a mano). Sin probar todavía con el canal real.
- Ejecutado [[Prompt vorty colorido - woeklifeee (3 videos sin MIDI)]]: 3 videos (v1_drop, v2_hits, v3_layers) en `marketing\woeklifeee-videos`, proyecto en `marketing\woeklifeee-remotion`. Desfase 0 confirmado (4,7 ms), -12 LUFS, pico objetivo bajado a -1,5 dBTP porque el AAC lo subía a -0,8. Anotado en la nota qué funcionó y qué no; propuesta de usar 41-56 para V2 (25-40 casi sin agudos).
- Decidido hacer primero una herramienta propia de analítica (YouTube primero) y dejar la web `lagrim.art` para después. Detalles en [[Alternativas a Metricool]].
- Nueva nota [[Alternativas a Metricool]] (Iconosquare, Buffer, Publer y nativas), enlazada desde [[Videos beats]].
- Proyecto **y-una-angelica-visualizer**: el vault pasa a ser su base de datos. Nueva nota [[Y una angelica - visualizer]] (BPM, secciones, montaje, estado), enlazada desde [[Videos beats]], y `CLAUDE.md` en la raíz del proyecto (desde [[Plantilla CLAUDE.md proyecto Remotion]]) con esa regla.
- Miniaturas de YouTube de woeklifeee (1280x720, 4 versiones A sunburst, B bold, C panels, D sun) en `Videos beats/Miniaturas woeklifeee/`, con el script `gen.py` para regenerarlas. La foto del atardecer se descartó: sin texto, oscura y de baja resolución para un beat alegre. Falta elegir y subir una.
- Anotado el rendimiento de Metricool (22 sep a 21 oct) en [[Métricas y revisiones]]: 227 vistas en YouTube, pico de 164 el 18/10, 2 suscriptores, TikTok sin datos. Metricool no devolvió lista de videos ni fuentes de tráfico.
- Beat **woeklifeee** (140 BPM, E mayor): medido el mp3 (compás 1 en 0 s, drop en el compás 9, 85 % graves) y escrito [[Prompt vorty colorido - woeklifeee (3 videos sin MIDI)]]: 3 videos de 16 compases (5-20, 25-40, 57-72), paleta colorida porque el beat es feliz. La versión oscura se retiró (queda como variante reutilizable). Sin ejecutar todavía.
- Nuevo prompt [[Prompt vorty oscuro - visualizer sin MIDI (Remotion)]]: estilo vorty en oscuro (casi negro + magenta/violeta) para beats sin MIDI ni stems; paneles LOW/MID/HIGH reactivos al audio, `FILTER_PARTS` opcional, 13 compases. Sin probar todavía con un beat real. Enlazado desde [[Videos beats]].
- Estilo vorty: la paleta ya no es siempre rosa. Se agregó el bloque "Estética del beat" (fondo, 3 acentos, texto, motivo de tarjetas, colores en `config.ts`, contraste 4.5:1) a [[Prompt vorty - breakdown rosa 3D (Remotion)]], [[Estilo de videos de vorty]] y la checklist de [[Proceso vorty - paso a paso]]. El rosa queda como paleta de referencia de kill4meeee. Los nombres de archivo conservan "rosa" para no romper enlaces.
- Guardado el chat **"estilo de videos de vorty"** (breakdown rosa 3D por stems): [[Estilo de videos de vorty]], [[Prompt vorty - breakdown rosa 3D (Remotion)]] (prompt final completo) y [[Proceso vorty - paso a paso]] (mis mensajes literales, errores y checklist). Antes había confundido "vorty" con el estilo make beat; corregido.
- Guardado el chat "Video editing style for beats" como [[Estilo make beat (menta, lila y glitch)]], con scripts en `Videos beats/Scripts make beat/` (`analyze.py`, `fit_beatgrid.py`, `render.py`, `glitch.py`), probados con video sintético. Tag cambiado a `lagrimankv`.
- Regla nueva en `CLAUDE.md`: para videos de estos estilos, usar las recetas del vault, no inventar.
- Cambio de marca: "prod. p4m" pasó a **prod. lagrimankv** en [[Marca y textos]], [[Pipeline visualizer Remotion]], [[Plan de funcionamiento]] y [[Videos beats]] (alias). También en el prompt de Cuerda en Notion.
- Pendiente: el archivo `beat_glitch_p4m.mp4` conserva el nombre antiguo (es el nombre real del archivo).
- Se creó `CLAUDE.md` en la raíz con la regla de usar siempre el vault y anotar novedades aquí y en notas.
