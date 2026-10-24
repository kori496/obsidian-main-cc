---
tags: [beats, videos, voz, referencias]
actualizado: 2026-10-21
---

Volver a [[Videos beats]] · Relacionado: [[Estilo de videos de vorty]] · [[Métricas y revisiones]]

# Referencias de voz al inicio de los shorts

Idea (21 oct 2026): meter una voz al comienzo de los shorts para ver si sube la retención (hoy los Shorts retienen ~31-35 % y duran ~10 s de media). Se pasaron 3 referencias en `.mp4` (vertical 576x1024, 18-22 s), todas en estilo vorty rosa.

## Qué tienen en común (medido del audio y los fotogramas)
- **Estructura:** 0 a ~3,2 s = voz recortada sobre fondo suave y casi sin graves; en ~3,2 s **corte seco y entra el beat con todo el low end** (la voz desaparece); el primer bloque de graves dura unos 3 s (hasta ~6,5 s) y luego el beat baja de intensidad. La parte de la voz suena a ~0,1-0,2 de nivel y el drop a ~0,4-0,6 (unas 3-4 veces más fuerte).
- **Texto en pantalla sincronizado palabra por palabra**, grande y animado, que aparece mientras suena la voz. Frases vistas: "how?? prettifun make beats like!!", "secret of crazy nettspen...", "how misogi make beats like this". Fórmula: **pregunta o secreto + nombre de un productor + "make beats like this"**.
- **Después del gancho**, el video sigue como breakdown rosa: ventana de FL con pistas, piano rolls con nombres (SYNTH, LEAD, PLUCK), fotos de fondo, "link in bio" al final.
- **Voz:** en el espectrograma se ven armónicos de habla entre ~200 Hz y 3 kHz, con cortes entre palabras (recortada), sin cola de reverb y sin graves. No pude escucharla, así que **el timbre (sintético, distorsionado) lo describo por lo que se ve, no por lo que suena**.

## Cómo se podría reproducir (propuesta, sin hacer todavía)
1. Frase corta con la fórmula de arriba, 2-4 s.
2. Voz generada (TTS) o grabada, y procesada: subir el tono, recortar entre palabras, saturación/bitcrusher, filtro de graves (corte bajo ~200 Hz) y sin reverb.
3. Texto animado palabra por palabra con el mismo tiempo que la voz (Remotion).
4. Silencio breve y **drop del beat en el compás 1** con los graves completos.
5. Probar con 5 Shorts con voz y 5 sin voz, comparando % visto y duración media en el panel de [[Herramienta analitica YouTube]].

## Decisión (22 oct 2026)
- Primer video: **"how to sound like eyesofdirty"**, voz **generada con IA y procesada** (no grabada).
- Script: `Videos beats/Scripts voz/voz_gancho.py` (voz con `edge-tts`, gratis y sin clave; efectos con ffmpeg; no necesita Pedalboard).

## Cómo usarlo
1. Una vez: `pip install edge-tts` (y tener ffmpeg en el PATH).
2. `python voz_gancho.py "how to sound like eyesofdirty"` genera 2 voces (Guy y Aria) x 3 presets en `voz/salida/`: **robot** (metálica), **glitch** (recortada palabra por palabra) y **radio** (teléfono sucio).
3. Con `--beat mi_beat.wav --beat-inicio 12.5` (segundo del drop) crea también `prev_*.mp3`: voz + pausa corta + drop del beat, para escuchar el efecto completo.
4. Cada voz trae un `.json` con inicio y duración de cada palabra, para animar el texto en Remotion sin cronometrar a mano.
5. Otras voces: `--voces en-US-ChristopherNeural en-GB-RyanNeural`. Tu propia voz: `--entrada grabacion.wav` (saca los tiempos por los silencios).

## Primer resultado (22 oct 2026)
- El script **sí funcionó en el PC** (descargó la voz IA con edge-tts y creó los 6 audios con sus JSON), así que la parte que no se había podido probar está probada.
- Se eligió la voz **Aria**, preset **robot** (editada además en FL Studio). Archivo final: `analitica/eyes of dirty vox robotic.mp3` (3,47 s, estéreo 44,1 kHz). Tiempos por palabra en `analitica/eyes of dirty vox robotic.json`.
- Tiempos (s): how 0,14-0,34 · to 0,35-0,45 · sound 0,47-0,82 · like 0,83-1,05 · eyesofdirty 1,07-1,87. La voz termina en ~1,87 s; el resto del archivo (hasta 3,47 s) es cola/eco.
- Los tiempos se alinearon midiendo el audio editado contra la pista original de Aria (correlación 0,91, desfase +0,04 s): el timing de FL coincide con el del script.

## Estado y límites
- Probado aquí con una voz de prueba (flite) como entrada y un beat sintético: genera los 3 presets, los JSON y las vistas previas sin errores; los graves de la voz bajan de ~24 % a 1-8 % como en las referencias.
- No se pudo escuchar el resultado: elegir preset por oído y ajustar los parámetros en `PRESETS` del script (tono, bitcrusher, filtros).
- edge-tts es una librería no oficial de las voces de Microsoft Edge; si algún día deja de funcionar, alternativas: ElevenLabs (plan gratis limitado) o la voz de Windows.

## Pendiente
- Elegir beat y estética de colores para el video (el estilo vorty pregunta la paleta).
- Escribir la receta en Remotion: texto animado con el `.json`, voz, silencio y drop (añadir como paso al estilo vorty).
- Medir 5 shorts con voz vs 5 sin voz (% visto y duración media) en el panel.
