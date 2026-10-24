---
tags: [beats, remotion, visualizer, proyecto]
actualizado: 2026-10-21
---

# 👼 Y una angelica · visualizer

Volver a [[Videos beats]] · Receta: [[Pipeline visualizer Remotion]]

Este vault es la **base de datos** del proyecto: aquí se anota todo lo que haya que recordar (decisiones, parámetros, errores, estado).

## Proyecto
- Carpeta: `C:\Users\sharo\OneDrive\Documentos\marketing\y-una-angelica-visualizer`
- Remotion 4.0.537 + TypeScript. Studio en el puerto **3417** (el 3000 lo usa otro proyecto).
- Detalle completo de decisiones en `DECISIONS.md` y estilo en `STYLE_BRIEF.md` del proyecto.

## Datos del beat
- **126 BPM**, half-time (caja en el tiempo 3). Primer pulso en 0,454 s (frame 14).
- Secciones: INTRO 0-7,6 s · BUILD 1 7,6-15,2 · **DROP 1** 15,2-45,7 · CALMA 45,7-68,5 · BUILD 2 68,5-76,2 · **DROP 2** 76,2-121,9 (el más fuerte) · OUTRO 121,9-129,2.
- Clip corto: 24 compases (45,7 s) desde el DROP 2, frames 2285-3656.

## Montaje
- Toda la línea de tiempo se calcula en `src/data.ts` desde `analysis.json` + `SEED`. `npm run check` valida cortes en beat, sin repetidos y dentro de tramos buenos.
- 5 clips de fondo (silueta_lago, estudio_rojo, ciudad_noche, fiesta_flash, gif_autopista) + 6 GIFs. Abre con estudio_rojo.

## Estado
- En curso (2026-10-21). Sin cambios sin commitear revisados todavía.
