---
tags: [beats, prompt, remotion, formatos]
actualizado: 2026-10-23
---

Volver a [[Videos beats]] · Estilo base: [[Estilo de videos de vorty]] · Prompt base: [[Prompt vorty - breakdown rosa 3D (Remotion)]] · Estilos: [[Estilos y formatos]]

# Prompt: tres estilos por beat (layer by layer, loop a mezcla, fragmento)

Se usa para cualquier beat nuevo. Los datos del beat (nombre, BPM, escala, estética, rutas de stems y mp3, compás del drop) se cambian en el encabezado del prompt. El video de layer by layer ya existe para otros beats, así que el prompt pide solo los otros dos formatos.

## Video A: loop crudo a mezcla final (unos 13 s, 8 compases)
- Compases 1-2: loop seco, texto "THIS SOUNDS UNFINISHED".
- Compases 3-4: mismo loop con efectos (filtro, distorsión, reverb, compresión; lista exacta en DECISIONS.md), texto "NOW LISTEN".
- Compases 5-8: mezcla completa, visualizer y forma de onda del mp3, texto "FULL BEAT".
- Tarjeta final de 1 compás. El loop seco y la mezcla salen del mismo compás de la canción.

## Video B: fragmento corto con enlace al completo (10 a 13 s, 6 a 8 compases)
- Tramo con drop o parte más pesada, empieza en un primer tiempo.
- Gancho en los primeros 2 compases, visualizer desde el inicio.
- Texto final "FULL BEAT ON YOUTUBE" y tarjeta final. Corte limpio para bucle.

## Reglas comunes
- Remotion, 1080x1920, 60 fps, H.264 CRF 16 o menos. Audio de 48 kHz armado antes en Python o ffmpeg, niveles de -16 LUFS (partes), -12 LUFS (completo), pico -1 dBTP.
- Tiempos calculados con 60/BPM. Cortes en primer tiempo de compás.
- Textos en inglés, sin emojis, zonas seguras de TikTok.
- Verificación: transientes en rejilla (menos de 15 ms), 10 fotogramas con `remotion still`, loudness con ffmpeg.

## Cómo se usa
- Se da el prompt a Claude Code con los datos del beat. Pide que busque los stems en el proyecto y confirme el compás 1 antes de renderizar.
- Primer uso: Clean Eyes, ver [[Clean Eyes - beat y publicación]].
