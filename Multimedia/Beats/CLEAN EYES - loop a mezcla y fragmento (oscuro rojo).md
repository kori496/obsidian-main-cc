---
tags: [beats, videos, remotion, oscuro, clean-eyes]
actualizado: 2026-10-23
---

Volver a [[Videos beats]] · Base: [[Estilo de videos de vorty]] · Mismo beat: [[Prompt vorty - how to sound like eyesofdirty (voz y drop)]]

# 🩸 CLEAN EYES: "loop a mezcla" y "fragmento" (oscuro, rojo sangre)

Dos videos verticales del beat **CLEAN EYES**, que es el proyecto de FL `cancer type beat 151 Am` (el mismo beat que eyesofdirty). 151 BPM, **A# menor**.

## Archivos
- Videos: `Documentos\marketing\clean_eyes\clean_eyes_v_a_loop_a_mezcla.mp4` y `clean_eyes_v_b_fragmento.mp4`.
- Proyecto: `Documentos\marketing\clean_eyes_remotion\` (composiciones `CleanEyesA`, `CleanEyesB`). Studio: `npx remotion studio --port=3418`. Detalle en `DECISIONS.md` y `README.md`.
- mp3: el del proyecto de FL (`eyesofdirty type beat 151 Am.mp3`). **Es una mezcla más nueva que el de `Presets\Scores`** (correlación 0,93). Compás 1 en 29,8 ms.
- Stems y MIDI: los de `Presets\Scores` (piano1, lead).

## Los dos formatos (nuevos, reutilizables)
- **A, "de loop crudo a mezcla final"** (9 compases, 14,3 s): loop seco (piano + lead) → el mismo loop con efectos hechos en Python (filtro que se abre de 300 Hz a 18 kHz, tanh, reverb de 0,5 s, compresor 4:1) → mezcla completa de **los mismos compases de la canción (9-12)** → tarjeta. En pantalla hay un FX RACK con medidores; el del filtro muestra la frecuencia real.
- **B, "fragmento en bucle"** (8 compases, 12,7 s): compases **57-64**, la parte más pesada del tema (graves del 85 %). Gancho "THIS ONE HITS DIFFERENT" visible entero desde el fotograma 0, "BAR 59…62" golpeando en cada compás, onda con números reales, tarjeta final. Corte limpio al final para el bucle.
- Para encontrar la parte más pesada: `audio/check_beat.py` mide graves y RMS por compás y elige el bloque de 8 que empieza en un compás 4n+1.

## Paleta oscura (la de este beat)
Fondo #0a0a0c, rojo sangre #c1121f, gris humo #6b6b75, texto #ededed. **El rojo (3:1) y el gris (3,8:1) no sirven para texto chico sobre el fondo**: letras grandes rojas con contorno #ededed, texto chico siempre en #ededed. Grano, scanlines y grietas hechos con código.

## Errores y lecciones
1. **El disco C: se llenó (0 bytes) a mitad del trabajo.** Proyecto en OneDrive = `node_modules` sincronizando; `npm i` tardó más de 10 min. Mantener los proyectos de Remotion fuera de OneDrive (como `C:\Users\sharo\remotion\...`) o excluir `node_modules`.
2. El visualizer con bandas lineales dibujaba una rampa quieta (casi todo graves): usar bandas logarítmicas.
3. Los destellos y las grietas no van en el compás 1 de un video en bucle: es la miniatura y el punto de repetición.

## Pendiente
- Verlos y escucharlos; subirlos y comparar A contra B (¿el antes/después retiene más que el fragmento?).
