# Instrucciones para Claude (vault "main cc")

Este vault de Obsidian es mi memoria de trabajo. Úsalo siempre.

## Regla principal
- **Antes de empezar** cualquier tarea, lee `Inicio.md` y luego el índice de la carpeta del tema (tabla de abajo).
- **Al terminar** cualquier cosa nueva (cambios, decisiones, novedades, resultados, errores resueltos, rutas, parámetros que funcionaron) que pueda servir a futuro, **escríbela como nota en el vault**. No esperes a que te lo pida.
- Anota también lo que NO funcionó y por qué.

## Carpetas (una por tema) y su nota índice
| Carpeta | Qué hay | Empezar por |
| --- | --- | --- |
| `Multimedia/` | Beats y videos: plan, metas, marca. `Recetas de video/` (vorty, make beat, core, voz), `Beats/` (videos de beats concretos), `Archivos/` (scripts y miniaturas) | `Multimedia/Multimedia.md` y `Multimedia/Videos beats.md` |
| `Redes/` | Métricas, Metricool, API de Instagram/TikTok/YouTube | `Redes/Redes.md` |
| `Webs/` | Panel lagrim-stats, lagrim.art. `Webs/analitica/` es el código del panel (en `.gitignore`: tiene tokens) | `Webs/Webs.md` |
| `Edicion de imagenes/` | V.YA, la tienda de ropa femenina elegante: fotos, referencias, base de datos de prendas, scripts de stories, `Adjuntos/` | `Edicion de imagenes/Edición de imágenes.md` |
| `Tienda/` | Negocio de V.YA: `ALTA/` (alta de productos, BarTender) y `CRS/` (sistema viejo, DIAN) | `Tienda/Tienda y negocio.md` y `Tienda/ALTA/ALTA - Inicio.md` |
| `Programacion/` | Descargadores, LKV EQ, juego ADOFAI, navegador propio, aprendizaje | `Programacion/Programacion.md` |
| `Herramientas y IA/` | Skills de Claude, REA / Ghidra, análisis de apps | `Herramientas y IA/Herramientas y IA.md` |
| `Sistema/` | `Bitácora.md` (registro de cambios) y resúmenes | `Sistema/Bitácora.md` |

- `Inicio.md` es el mapa general. Toda nota nueva va en la carpeta de su tema y se enlaza desde la nota índice de esa carpeta.
- Colores: grafo en `.obsidian/graph.json` y explorador en `.obsidian/snippets/colores-vault.css`, por carpeta. Si se crea una carpeta nueva, añadirle color en los dos.

## Cómo escribir las notas
- Markdown de Obsidian, en español, con frontmatter (`tags`, `actualizado: AAAA-MM-DD`).
- Enlaza con `[[wikilinks]]` a las notas relacionadas y deja un "Volver a [[...]]" arriba, como las demás. No repitas nombres de nota (los enlaces van por nombre, no por carpeta).
- Actualiza la nota existente en vez de crear duplicados.
- Después de cada sesión con cambios, añade una entrada corta en `Sistema/Bitácora.md` (fecha, qué se hizo, qué notas se tocaron).
- Nunca borres ni sobrescribas notas mías sin avisar. Si cambias algo existente, di qué cambiaste.
- Mover notas: hacerlo dentro de Obsidian (arrastrando) para que actualice los enlaces; si se mueve desde fuera, revisar rutas escritas en notas y canvas.

## Videos de beats: usar las recetas, no inventar
Cuando pida un video de un estilo ya hecho, **lee primero la receta y úsala tal cual** (cambiando solo lo que cambia por beat). Todas están en `Multimedia/Recetas de video/`:
- "estilo vorty" / breakdown 3D por stems (**la paleta NO es fija ni siempre rosa: sale de la estética del beat que yo diga; si no la digo, pregúntamela**) → `Estilo de videos de vorty.md`, `Prompt vorty - breakdown rosa 3D (Remotion).md` y `Proceso vorty - paso a paso.md` (incluye checklist de archivos).
- "make beat" (menta/lila) o glitch sobre una grabación de FL → `Estilo make beat (menta, lila y glitch).md` y los scripts de `Multimedia/Archivos/Scripts make beat/`.
- Visualizer distorsionado "core" → `Pipeline visualizer Remotion.md`.
- Si el pedido no encaja con ninguna receta, dilo, y después de hacerlo guarda la nueva receta (estilo, prompt, proceso, errores) en `Multimedia/Recetas de video/` y enlázala desde `Multimedia/Multimedia.md`.

## Marca y reglas fijas (beats)
- Productor: **lagrimankv**. Tag en los videos: **prod. lagrimankv**. (Ya no se usa "p4m".)
- Títulos y descripciones 100 % en inglés, tono slang/urbano, sin emojis.
- Género principal: boom bap; también trap y experimental.
- Los visualizers se hacen con Remotion (React + TypeScript), sin Python. Ver `Multimedia/Recetas de video/Pipeline visualizer Remotion.md`.

## Reglas fijas (V.YA)
- Estética fancy y elegante, colores neutros.
- Piezas limpias, solo con el logo; el texto se agrega después en la story.
- Nada de estilo glitchy, humo, estilo antiguo ni paletas dentro de las piezas. Ver `Edicion de imagenes/Preferencias de estilo.md`.

## Preferencias de trabajo
- Respuestas directas y cortas. Dime qué hiciste y dónde quedó el archivo.
- Si algo es ambiguo y barato de rehacer, decide y anótalo; si es caro de rehacer, pregunta.
