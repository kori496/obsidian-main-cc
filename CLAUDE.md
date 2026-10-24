# Instrucciones para Claude (vault "main cc")

Este vault de Obsidian es mi memoria de trabajo. Úsalo siempre.

## Regla principal
- **Antes de empezar** cualquier tarea, lee las notas relacionadas del vault (empieza por `Videos beats/Videos beats.md` o `Edicion de imagenes/Edición de imágenes.md`, según el tema).
- **Al terminar** cualquier cosa nueva (cambios, decisiones, novedades, resultados, errores resueltos, rutas, parámetros que funcionaron) que pueda servir a futuro, **escríbela como nota en el vault**. No esperes a que te lo pida.
- Anota también lo que NO funcionó y por qué.

## Cómo escribir las notas
- Markdown de Obsidian, en español, con frontmatter (`tags`, `actualizado: AAAA-MM-DD`).
- Enlaza con `[[wikilinks]]` a las notas relacionadas y deja un "Volver a [[...]]" arriba, como las demás.
- Actualiza la nota existente en vez de crear duplicados. Si es un tema nuevo, crea una nota en la carpeta que corresponda y enlázala desde la nota índice de esa carpeta.
- Después de cada sesión con cambios, añade una entrada corta en `Bitácora.md` (fecha, qué se hizo, qué notas se tocaron).
- Nunca borres ni sobrescribas notas mías sin avisar. Si cambias algo existente, di qué cambiaste.

## Videos de beats: usar las recetas, no inventar
Cuando pida un video de un estilo ya hecho, **lee primero la receta y úsala tal cual** (cambiando solo lo que cambia por beat):
- "estilo vorty" / breakdown 3D por stems (**la paleta NO es fija ni siempre rosa: sale de la estética del beat que yo diga; si no la digo, pregúntamela**) → `Videos beats/Estilo de videos de vorty.md`, `Prompt vorty - breakdown rosa 3D (Remotion).md` y `Proceso vorty - paso a paso.md` (incluye checklist de archivos).
- "make beat" (menta/lila) o glitch sobre una grabación de FL → `Videos beats/Estilo make beat (menta, lila y glitch).md` y los scripts de `Videos beats/Scripts make beat/`.
- Visualizer distorsionado "core" → `Videos beats/Pipeline visualizer Remotion.md`.
- Si el pedido no encaja con ninguna receta, dilo, y después de hacerlo guarda la nueva receta (estilo, prompt, proceso, errores) en una nota de `Videos beats/` y enlázala desde `Videos beats.md`.

## Carpetas
- `Videos beats/`: canal de beats y videos (estilos, pipeline Remotion, métricas, pendientes).
- `Edicion de imagenes/`: V.YA, la tienda de ropa femenina elegante (fotos, referencias, base de datos de prendas).
- `Skills.md`: skills e instalaciones de Claude Code.

## Marca y reglas fijas (beats)
- Productor: **lagrimankv**. Tag en los videos: **prod. lagrimankv**. (Ya no se usa "p4m".)
- Títulos y descripciones 100 % en inglés, tono slang/urbano, sin emojis.
- Género principal: boom bap; también trap y experimental.
- Los visualizers se hacen con Remotion (React + TypeScript), sin Python. Ver `Videos beats/Pipeline visualizer Remotion.md`.

## Reglas fijas (V.YA)
- Estética fancy y elegante, colores neutros.
- Piezas limpias, solo con el logo; el texto se agrega después en la story.
- Nada de estilo glitchy, humo, estilo antiguo ni paletas dentro de las piezas. Ver `Edicion de imagenes/Preferencias de estilo.md`.

## Preferencias de trabajo
- Respuestas directas y cortas. Dime qué hiciste y dónde quedó el archivo.
- Si algo es ambiguo y barato de rehacer, decide y anótalo; si es caro de rehacer, pregunta.
