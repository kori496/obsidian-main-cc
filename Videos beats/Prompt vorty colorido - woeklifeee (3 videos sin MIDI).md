---
tags: [beats, prompt, vorty, remotion, claude-code, visualizer, woeklifeee]
actualizado: 2026-10-21
---

# 🌈 Prompt vorty colorido: woeklifeee, 3 videos sin MIDI (Claude Code + Remotion)

Volver a [[Videos beats]] · Estilo base: [[Estilo de videos de vorty]] · Variante oscura (descartada para este beat): [[Prompt vorty oscuro - visualizer sin MIDI (Remotion)]]

Beat **woeklifeee** (140 BPM, E mayor). Solo hay mp3 (`Downloads\gruñido.mp3`): sin MIDI, stems ni proyecto de FL. Los 3 videos (27,4 s = 16 compases) salen de tramos del beat completo.

## Lo verificado del audio
- 157,6 s, estéreo 44,1 kHz. 140 BPM confirmado.
- Compás 1 en 0,000 s: el drop entra en 13,7 s = compás 9 exacto. (El detector de pulsos dio un desfase falso de 0,39 s por subdivisiones.)
- ~85 % de la energía está bajo 100 Hz (808 muy presente): los paneles MID/HIGH hay que normalizarlos para que se vean.
- Energía por bloques de 4 compases: 1-8 intro suave (0,06), 9-24 primer drop (0,42), 25-40 parte más fuerte sin agudos (0,455), 41-56 vuelve a 0,41, 57-72 la más llena (0,459), 73-88 cierre.
- Los tramos se eligieron por energía, no por oído: confirmar con audífonos cuál es la parte más pegadiza.

## Decisiones
- Paleta: se pidió oscuro y luego se retiró; el beat es feliz, así que colorida (coral, turquesa, violeta, amarillo sol sobre crema/rosa claro).
- Carpeta `marketing` usada como base: proyecto en `marketing\woeklifeee-remotion` y salida en `marketing\woeklifeee-videos`.
- Audio sin filtrar por banda (opción `FILTER_PARTS` apagada), porque el beat es casi todo graves.
- ✅ Ejecutado el 21/10/2026 con Claude Code: ver "Resultado de la ejecución".

## Resultado de la ejecución (21/10/2026)
- Videos en `marketing\woeklifeee-videos\`: `lagrimankv_woeklifeee_v1_drop.mp4`, `_v2_hits.mp4`, `_v3_layers.mp4`. 1080x1920, 60 fps, 27,435 s, H.264 CRF 16, AAC 320k, sin negros.
- Proyecto en `marketing\woeklifeee-remotion` (README y `DECISIONS.md` dentro). Studio: `npm run dev`, puerto **3418**.
- Composiciones `V1Drop`, `V2Hits`, `V3Layers` + versiones `...Debug` con la rejilla y los kicks reales encima.

**Lo que funcionó**
- Desfase 0 confirmado: el drop cae a 4,7 ms del compás 9. No se usó detector de pulsos, así que no salió el falso 0,39 s.
- Decodificar con **ffmpeg** tanto para el análisis como para el corte, para que los dos usen el mismo instante 0.
- WAV por video cortado al sample (1.316.571 muestras a 48 kHz) + loudnorm de 2 pasadas: -11,7 a -11,9 LUFS.
- MID con su propio rango en dB y HIGH normalizado con el máximo de **cada video**: se ven aunque el 808 domine.
- Contorno azul noche en las letras de colores del gancho: solas no pasan 4.5:1 sobre el crema (1,5-4,5:1).
- Adelantar el gancho 5 semicorcheas para que el fotograma 0 nunca esté vacío.
- La onda FULL con amplitud media por columna (con el pico, el drop comprimido salía como un bloque).

**Lo que no funcionó / ojo**
- Pico a -1,0 dBTP en el WAV → -0,8 en el mp4 (el AAC lo sube). Se usa **-1,5 dBTP** como objetivo.
- Los kicks del tiempo 1 caen a +5 ms, pero en algunos compases (13, 17, 29, 33…) se miden a +28/30 ms: el golpe cae encima de un 808 que todavía suena y su ataque queda tapado. Es igual en cada vuelta de 4 compases, así que no es un desfase, pero sin stems no se puede medir mejor. En los mp4 sale el mismo patrón: el render no añade desfase.
- Compases 25-40 (V2) casi sin agudos (0,2 %): la parte HIGH de V2 se ve más floja. Alternativa: 41-56, que sí tiene hats.
- `FILTER_PARTS = true` está programado pero sin probar.
- Render: ~20 min V1 y ~7 min V2 y V3 cada uno (concurrency 4, GL angle).
- Falta escucharlos con audífonos y elegir cuál subir.

## Título y descripción de YouTube (video completo, subido con Tunes to Tube)
- Título elegido para probar: `trap but make it happy (woeklifeee) *free for non profit*` (sigue la fórmula "boombap but make it ..." que ya funcionó; cambiar "trap" si el género real es otro).
- Alternativas: `woeklifeee | happy 808 type beat *free for non profit*` y `[artist] type beat - "woeklifeee" | 140 BPM`.
- Descripción en inglés, slang, sin emojis: BPM y escala (140 BPM, E major), "free for non profit", crédito "prod. lagrimankv", contacto/compra pendiente, hashtags de type beat.
- Pendiente: confirmar género y artista de referencia, y poner enlaces de contacto/compra.

## Títulos y descripción del Short V3 Layers (21/10/2026)
- Opciones de título (inglés, slang, sin emojis):
  1. `trap but make it happy: woeklifeee layer by layer *free for non profit*` (sigue la fórmula que funciona)
  2. `watch this 140 BPM beat stack up layer by layer (woeklifeee)`
  3. `woeklifeee | happy 808 type beat *free for non profit*`
- Descripción: 140 BPM, E major, "free for non profit", "prod. lagrimankv", hashtags de type beat. Contacto/compra sigue pendiente.
- Pendiente: confirmar el género real antes de publicar (si no es trap, cambiar la palabra del título 1).

## Títulos y descripciones de los Shorts V1 Drop y V2 Hits (21/10/2026)
- V1 Drop (gancho "HOW I COOKED THIS??", el drop cae en el compás 9):
  1. `trap but make it happy: woeklifeee *free for non profit*`
  2. `wait for the 808 to drop (woeklifeee)` (ojo: "wait for the drop" está en descartados de [[Marca y textos]]; solo para probar)
  3. `how i cooked this happy 808 beat (woeklifeee)`
  - Descripción: "tension, then the 808 drops and everything lights up. woeklifeee | 140 BPM | E major | free for non profit | prod. lagrimankv" + hashtags #typebeat #trapbeat #happybeat #808 #flstudio #lagrimankv
- V2 Hits (gancho "THIS ONE HITS DIFFERENT"):
  1. `this 808 hits different (woeklifeee) *free for non profit*`
  2. `woeklifeee | hard happy trap type beat *free for non profit*`
  3. `trap but make it hit: woeklifeee 140 BPM`
  - Descripción: "low, mid, high, then all of it at once. this one hits different. woeklifeee | 140 BPM | E major | free for non profit | prod. lagrimankv" + hashtags #808 #typebeat #hardbeat #freebeat #flstudio #lagrimankv
- Pendiente: género real (si no es trap, cambiar la palabra) y contacto/compra.

## Prompt

```txt
Eres mi editor de video. Crea 3 videos verticales de 27,4 s cada uno (16 compases) para TikTok, YouTube Shorts y Reels de mi beat "woeklifeee", en estilo "vorty colorido": paneles flotantes 3D con letra pixelada, paleta alegre y un visualizer que reacciona al audio. No tengo MIDI, stems ni proyecto de FL: solo el beat completo. NO dibujes piano rolls ni uses capturas de FL Studio. Hazlo en Remotion (React + TypeScript), sin Python. Trabaja de forma autónoma: pregúntame solo si falta un archivo. Anota tus decisiones en DECISIONS.md.

## Reglas generales
- Antes de empezar, agrega el vault con /add-dir "C:\Users\sharo\OneDrive\Documentos\obsidian\main cc" y lee su CLAUDE.md, Videos beats\Estilo de videos de vorty.md y Videos beats\Marca y textos.md. Al terminar, deja una nota en el vault con lo que funcionó y lo que no, y una entrada en Bitácora.md.
- No modifiques ni muevas mis archivos originales: copia el mp3 a public\woeklifeee.mp3 (sin la ñ en el nombre).
- Windows: rutas entre comillas y path.join. Necesitas Node 18 o más nuevo y ffmpeg; si faltan, instálalos con winget. ffmpeg solo para inspeccionar y preparar el audio.
- Proyecto en: "C:\Users\sharo\OneDrive\Documentos\marketing\woeklifeee-remotion". TypeScript. Tres composiciones: V1Drop, V2Hits y V3Layers, cada una de 1080x1920 a 60 fps. Añade versiones Debug (rejilla de tiempos y compases dibujada encima).

## Archivo de entrada (ya revisado)
- Beat completo: "C:\Users\sharo\Downloads\gruñido.mp3". 157,57 s, estéreo, 44,1 kHz.
- 140 BPM, 4/4, escala E mayor. 1 tiempo = 0,428571 s; 1 compás = 1,714286 s; a 60 fps, 1 compás = 102,857 fotogramas (no redondees los límites a fotogramas enteros al animar; calcula desde t = frame / fps).
- El compás 1 empieza en 0,000 s. Lo verifiqué: la sección fuerte entra en 13,7 s, que es exactamente el inicio del compás 9 (8 × 1,714286 = 13,714 s). Confírmalo tú también con tu análisis (tolerancia 30 ms) y, si difiere, corrige el desfase. Ojo: un detector de pulsos puede dar un desfase falso de 0,39 s por contar subdivisiones; ignóralo.
- Mapa de energía por bloques de 4 compases (medido):
  - 1-8: intro suave (RMS 0,06), con más agudos; ahí suena la melodía.
  - 9-24: primer drop (RMS 0,42), 85 % de la energía bajo 100 Hz.
  - 25-40: parte más fuerte (RMS 0,455), casi sin agudos (hats fuera).
  - 41-56: vuelve a RMS 0,41 con agudos.
  - 57-72: la más fuerte y llena (RMS 0,459).
  - 73-88: baja a 0,38-0,42 (cierre del beat).
  Como el beat es muy grave (808), la banda LOW domina; los visuales de MID y HIGH deben escalarse con su propia normalización, para que se vean aunque suenen bajito.
- Análisis (script Node/TS, npm run analyze → public/analysis.json, todo en frames): onsets por banda (graves <150 Hz, medios 150 Hz-4 kHz, agudos >4 kHz) y energía por compás. Úsalo para ubicar los kicks reales y confirmar el mapa de arriba.

## Los 3 videos (16 compases cada uno = 27,43 s)
Cada video usa compases enteros del beat y el compás final es la tarjeta final con el audio en fundido.
- V1Drop: compases 5 a 20 del beat. Compases 5-8 (intro): paneles MID/HIGH y la onda del beat, ambiente suave, con el gancho "HOW I COOKED THIS??" en el primer compás. Compás 9 (el drop): explosión: destello, sacudida de cámara y entran los paneles LOW y FULL BEAT con confeti. Compases 9-19: drop completo con los paneles latiendo. Compás 20: tarjeta final. Movimiento: los paneles giran hacia los lados al entrar y salir. Este video es el de "tensión y caída".
- V2Hits: compases 25 a 40. Gancho "THIS ONE HITS DIFFERENT". Compases 25-32: cuatro partes de 2 compases (LOW, MID, HIGH, y las tres juntas). Compases 33-39: FULL BEAT con miniaturas de los paneles alrededor. Compás 40: tarjeta final. Movimiento: zoom de golpe al entrar y temblor en los tiempos 2 y 4.
- V3Layers: compases 57 a 72. Gancho "LAYER BY LAYER". Compases 57-64: capas que se suman cada 2 compases (LOW; + MID; + HIGH; + onda FULL), y los paneles anteriores se encogen y se apilan arriba. Compases 65-71: FULL BEAT. Compás 72: tarjeta final.
- Si al escuchar un tramo no te parece pegadizo (por ejemplo, se queda vacío), dímelo en el resumen final con una alternativa de compases; no cambies los tramos sin avisar.

## Estética: colorida y alegre (todo sale de config.ts, objeto `palette`, nada de colores dentro de los componentes)
- Fondo: degradado cálido y luminoso, #fff6dc arriba a #ffd9ec abajo, con rayos de sol suaves (sunburst) que giran despacio y laten con el kick.
- Acentos: coral #ff4f6d (LOW), turquesa #12c2b3 (MID), violeta #7c4dff (HIGH), amarillo sol #ffc233 (FULL BEAT), lima #6bd36b para detalles. Texto: azul noche #1d1440. Contraste mínimo 4.5:1; si falla, ajústalo y anótalo.
- Paneles: tarjetas blancas semitransparentes con borde de 3 px del color de su banda, esquinas redondeadas, inclinadas en 3D (perspective, rotateX/Y/Z) con sombra suave de color. Laten en cada tiempo, entran y salen en medio tiempo con spring, y hay un destello corto en cada cambio de parte.
- Tarjetas decorativas generadas por código, sin fotos: confeti que estalla en cada tiempo, estrellas, arcos de arcoíris, burbujas y rayos de sol. Fondo siempre vivo pero sin ensuciar los paneles.
- Etiquetas en fuente pixelada de bloques (Silkscreen, Jersey 10 o Pixelify Sans, con @remotion/google-fonts). Las letras del gancho aparecen una por semicorchea con un pop, cada letra de un color de la paleta.
- Textos en pantalla en inglés, tono slang, sin emojis.

## Paneles del visualizer (sin MIDI)
Todo se calcula desde el audio y el tiempo, como función pura del frame.
- LOW (coral): onda de los graves y un círculo central que late con cada kick/808.
- MID (turquesa): barras de espectro suavizadas (visualizeAudio de @remotion/media-utils).
- HIGH (violeta): chispas y partículas que saltan en los agudos.
- FULL BEAT (amarillo): onda completa del mp3 (getAudioData, getWaveformPortion), línea de reproducción fija y marcas de compás con el número real de compás de la canción.
- Un espectro circular en una tarjeta decorativa.

## Audio
- Arma primero el audio de cada video como un solo WAV de 48 kHz con ffmpeg: corte exacto al sample en compases enteros (inicio = (compás_inicial - 1) × 1,714286 s, 16 compases de largo), fundidos de 5 ms al inicio y un fundido de salida de 1 compás en la tarjeta final. Normaliza a ~ -12 LUFS con pico ≤ -1 dBTP. En Remotion entra con un único <Audio>; no cortes dentro de Remotion.
- Usa el beat sin filtrar en las tres partes: las partes LOW/MID/HIGH son solo visuales. Deja en config.ts la opción FILTER_PARTS (false por defecto) por si quiero probar el filtrado por banda.

## Marca y textos
- Fijo abajo a la izquierda: "PROD. LAGRIMANKV" y "WOEKLIFEEE · 140 BPM · E MAJOR".
- Tarjeta final (1 compás): "LAGRIMANKV", "FREE FOR NON PROFIT", "WOEKLIFEEE · 140 BPM · E MAJOR · TYPE BEAT".

## Reglas de sincronía (no negociables)
- Todo corte, entrada y salida cae en el primer tiempo de un compás, calculado con la fórmula y no a ojo.
- Función central beatClock(frame) que devuelve compás, tiempo, fase y un "kick" que decae, usada por todos los componentes, con interpolate() y spring().
- Determinista: ningún Math.random ni Date.now; usa random("semilla") o @remotion/noise.
- Modo debug: dibuja la rejilla y úsalo para comprobar que los golpes caen en las líneas.

## Seguridad visual y zonas seguras
- Nada importante en los 150 px de arriba, en los 300 a 480 px de abajo, ni en el borde derecho entre y = 900 y 1700.
- Gancho fuerte desde el fotograma 0 (nunca negro). Cierre limpio que pueda repetirse en bucle.
- Máximo 3 flashes por segundo, con un parámetro FLASH_INTENSITY en config.ts. El fondo es claro, así que los destellos blancos deben ser suaves.

## Verificación
1. Con npx remotion still, saca 10 fotogramas por video (gancho, cada parte, el drop y la tarjeta final) y revisa texto cortado, zonas seguras y legibilidad.
2. Con el modo debug, confirma que los kicks caen en la rejilla (desfase menor a 15 ms) y que cada cambio está en un primer tiempo.
3. Mide loudness y pico de cada mp4 con ffmpeg.
4. ffprobe: 1080x1920, 60 fps, duración 27,43 s ± 0,05 s, pista de audio. blackdetect sin negros.

## Entrega
- Render: H.264, yuv420p, CRF 16, AAC 320 kbps → "C:\Users\sharo\OneDrive\Documentos\marketing\woeklifeee-videos\" como lagrimankv_woeklifeee_v1_drop.mp4, lagrimankv_woeklifeee_v2_hits.mp4 y lagrimankv_woeklifeee_v3_layers.mp4.
- Deja README.md para volver a renderizar y config.ts con todos los parámetros (paleta, compases de inicio de cada video, FLASH_INTENSITY, FILTER_PARTS, ganchos).
- Resumen final: tabla por video con compases usados, partes, duración y decisiones, y cómo abrir Remotion Studio.
```
