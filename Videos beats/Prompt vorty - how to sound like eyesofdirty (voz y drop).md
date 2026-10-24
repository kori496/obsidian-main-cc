---
tags: [beats, prompt, vorty, voz, remotion, claude-code]
actualizado: 2026-10-23
---

Volver a [[Videos beats]] · Estilo base: [[Estilo de videos de vorty]] · Voz: [[Referencias de voz en shorts]] · Recetas relacionadas: [[Prompt vorty - breakdown rosa 3D (Remotion)]]

# 🎬 Prompt: "how to sound like eyesofdirty" (voz + drop en el compás 9)

Un solo video con gancho de voz sintética, recuadros de piano roll que se suman y drop en el compás 9. Mezcla el estilo vorty con la voz de [[Referencias de voz en shorts]].

## Estado (22 oct 2026)
- **Verificado:** la voz (`analitica/eyes of dirty vox robotic.mp3` y su `.json`, alineados con correlación 0,91) y los archivos del beat en `Image-Line\FL Studio\Presets\Scores\` (revisados el 22 oct).
- **Datos medidos del beat:** 151 BPM; 1 tiempo = 0,397351 s, 1 compás = 1,589404 s. El mp3 `eyes of dirty type beat 151 Am.mp3` dura 119,64 s y su compás 1 está en **0,030 s** (los stems empiezan en 0 ms). El **drop sí cae en el compás 9**: los graves bajo 100 Hz pasan de 0-5 % a ~36 %. En los compases 1-8 suenan piano y lead, sin drums ni bass; las drums entran en el 9.
- **Tonalidad:** medida **A# menor** (el MIDI usa A# C C# D# F F# G#); el nombre del archivo dice "Am", que no coincide. El prompt usa "A# MINOR" en los textos.
- **MIDI:** `midi piano 1/untitled.mid` (pista "Chorus ep 1 1", 66 notas) y `midi lead/untitled.mid` (pista "Platinium saw 1", 57 notas) tienen notas, 4 compases, PPQ 96, no están repetidos. Los WAV de piano 1 y lead duran 4 compases y tienen el mismo nombre de archivo en carpetas distintas (se copian con nombres únicos).
- **Dudas encontradas:** (1) el WAV de piano 1 coincide poco con su MIDI en notas (0,3-0,7, el del lead 0,95): hay que revisar de oído que el WAV es el pattern correcto; (2) el archivo con cortes ("piano (mismas notas del midi solo que suena dos cuartos de compas).wav", 7,51 compases, está en la carpeta `midi lead`) tiene las notas del **lead**, no las del piano 1 (similitud 0,97 vs 0,2-0,47): suena 2 tiempos y calla 2 en cada compás. El prompt lo usa como "PIANO 1 · CUTS" y dibuja las notas de lead.mid recortadas; (3) `pluck/Pattern 2` no tiene MIDI y casi no se detecta en el beat: no se usa; (4) no hay stems de bass/808 (no hacen falta, el drop usa el mp3).
- **Decisiones que tomé (cambiables):** paleta rosa de referencia; compases 1-8 con stems y beat completo desde el 9; kick, 808 y bass solo desde el drop; último tiempo del compás 8 en silencio; proyecto Remotion fuera de OneDrive (`C:\Users\sharo\remotion\eyesofdirty`) para no sincronizar node_modules; el video se guarda en `Documentos\marketing`.
- **Aviso:** la voz dice "how to **sound** like eyesofdirty", no "how to **make a beat** like". El texto en pantalla sigue lo que dice la voz. Para cambiar la frase hay que regenerar la voz con `voz_gancho.py` y volver a editarla en FL.

## Qué completar antes de pegarlo
Nada obligatorio: el prompt ya no lleva marcadores. Confirmar solo las dudas (1) y (2) de arriba.

## Prompt

```txt
Eres mi editor de video. Crea 1 video vertical (TikTok, YouTube Shorts y Reels) en Remotion. Empieza con una voz sintética de IA que dice la frase gancho y después muestra cómo está hecho mi beat con recuadros de piano roll (MIDI) que se van sumando hasta que cae el drop en el compás 9 de la canción. Trabaja de forma autónoma: pregunta solo si falta un archivo o si algo de la Fase 0 no coincide con lo que digo aquí (pregúntalo una sola vez, antes de programar). Anota tus decisiones al final.

## Reglas generales
- No modifiques ni muevas mis archivos originales: trabaja con copias en public/.
- Windows: rutas entre comillas y path.join. Necesitas Node.js 18 o más nuevo y ffmpeg; si faltan, instálalos con winget o dime cómo.
- Textos en pantalla en inglés, tono slang/urbano, sin emojis.
- Los videos de referencia son solo guía de estilo: no copies fotogramas, marcas de agua, @ de otros creadores ni pantallas finales. Todo sale de mis archivos y de gráficos hechos con código.

## Proyecto Remotion
- Carpeta nueva: C:\Users\sharo\remotion\eyesofdirty\, con TypeScript (fuera de OneDrive, para que no sincronice node_modules).
- Una composición "EyesOfDirty": 1080x1920, 60 fps, 13 compases en total (compases 1-12 de la canción + 1 compás de tarjeta final). Calcula la duración en fotogramas desde los compases.
- Dependencias: @remotion/google-fonts, @remotion/media-utils, @remotion/noise, @tonejs/midi.
- Todos los colores salen de un objeto `palette` en config.ts. Ningún color va escrito dentro de los componentes.
- Modo debug (config.DEBUG): dibuja la rejilla de tiempos y compases y el inicio de cada palabra de la voz sobre el video.

## Archivos de entrada
VOZ (ya hecha, no la regeneres):
- "C:\Users\sharo\OneDrive\Documentos\obsidian\main cc\Videos beats\analitica\eyes of dirty vox robotic.mp3": voz sintética ya procesada. 3,47 s, estéreo, 44,1 kHz.
- "C:\Users\sharo\OneDrive\Documentos\obsidian\main cc\Videos beats\analitica\eyes of dirty vox robotic.json": tiempos por palabra en segundos. Frase: "how to sound like eyesofdirty". how 0,14-0,34 · to 0,35-0,45 · sound 0,47-0,82 · like 0,83-1,05 · eyesofdirty 1,07-1,87.
- El audio tiene 0,14 s de silencio al inicio. Recórtale 0,10 s para que "how" empiece en 0,04 s y réstale 0,10 s a todos los tiempos del json. La voz termina en ~1,77 s; el resto del archivo es cola: córtala con un fundido de 150 ms.

BEAT: "eyes of dirty type beat", 151 BPM, 4/4, escala A# menor (medida en el audio y en las notas del MIDI: A# C C# D# F F# G#. El nombre del archivo dice "Am", pero no coincide: usa A# menor en los textos).
Carpeta: "C:\Users\sharo\OneDrive\Documentos\Image-Line\FL Studio\Presets\Scores\"
Copia todo a public/ con estos nombres únicos (varios WAV se llaman igual en carpetas distintas):
- beat.mp3 = "eyes of dirty type beat 151 Am.mp3". Beat completo, 119,64 s. Ya verificado: el compás 1 empieza en 0,030 s (no en 0) y el DROP cae en el compás 9 (los graves bajo 100 Hz pasan de 0-5 % de la energía en los compases 1-8 a ~36 % desde el 9). En los compases 1-8 solo suenan piano y lead, sin drums ni bass. Recorta 30 ms del inicio al preparar la copia, para que el compás 1 quede en 0 s.
- piano1.wav = "midi piano 1\Pattern 1 (consolidated) #3 (consolidated)_4.wav" (6,395 s = 4,02 compases) y piano1.mid = "midi piano 1\untitled.mid" (pista "Chorus ep 1 1", 66 notas, 4 compases, F3-C#6).
- lead.wav = "midi lead\Pattern 1 (consolidated) #3 (consolidated)_4.wav" (6,374 s = 4,01 compases) y lead.mid = "midi lead\untitled.mid" (pista "Platinium saw 1", 57 notas, 4 compases, D#2-C#6).
- piano1_cuts.wav = "midi lead\piano (mismas notas del midi solo que suena dos cuartos de compas).wav" (11,937 s = 7,51 compases). Es la versión con cortes que hice yo: en cada compás suenan los 2 primeros tiempos y callan los otros 2. Por su contenido de notas coincide con el MIDI y el WAV del lead (similitud 0,97), no con el del piano 1.
- drums.wav = "drums\drums.wav" (12,719 s = 8,00 compases exactos, combo completo, sin MIDI). En el beat completo las drums entran en el compás 9.
- NO uses "pluck\Pattern 2 (consolidated).wav": no tiene MIDI y casi no se detecta en el beat completo.
- Los stems empiezan en el compás 1 con desfase 0 ms; es el mp3 el que lleva 30 ms. Los MIDI vienen a 151 BPM, PPQ 96.

## Fase 0: comprobación rápida de lo que ya medí (antes de programar nada)
1. Confirma 151 BPM, que el compás 1 de beat.mp3 está en 0,030 s y que los stems arrancan en 0 ms (rejilla de 151 BPM, desfase menor a 15 ms tras corregirlo).
2. Confirma que los graves del mp3 saltan en el compás 9 y que antes solo suenan piano y lead.
3. Lee piano1.mid y lead.mid y comprueba que tienen las notas indicadas. Compara por compás las notas del MIDI de piano 1 con el audio de piano1.wav: su coincidencia de notas con el MIDI era baja (0,3 a 0,7; la del lead es 0,95). Si de verdad no coinciden, dibuja igual el MIDI pero escríbelo en DECISIONS.md.
4. Si algo no coincide con lo que digo aquí, pregúntamelo una sola vez.

## Datos musicales
- 151 BPM: 1 tiempo = 0,397351 s; 1 compás = 1,589404 s. A 60 fps, 1 tiempo = 23,8411 fotogramas y 1 compás = 95,364 fotogramas. 13 compases = 20,662 s = 1240 fotogramas.
- El compás 9 del beat completo empieza en 12,745 s del mp3 original (0,030 + 8 x 1,589404).
- Escribe estos valores calculados en config.ts.

## Reglas de sincronía (lo más importante)
- Todo corte, entrada y salida de paneles cae exactamente en el primer tiempo de un compás, calculado con la fórmula y no a ojo. La excepción es el texto de la voz, que sigue los tiempos del json.
- Los loops solo se combinan entre sí o con el beat completo en la misma posición dentro del bloque de 4 compases: el compás 1 del loop va con los compases 1, 5, 9 de la canción; el 2 con los 2, 6, 10; el 3 con los 3, 7, 11, y así. Nunca mezcles posiciones.
- Todas las animaciones se calculan desde el tiempo: t = frame / fps; tiempo musical = t x 151 / 60; fase = tiempo % 1. Crea una función central beatClock(frame) que devuelva compás, tiempo, fase y un "kick" que decae, y úsala en todos los componentes. Usa interpolate() y spring().
- Todo es determinista: función pura del frame, con random("semilla") o @remotion/noise. Nunca Math.random() ni estado.
- Los destellos no superan 3 por segundo y tienen un parámetro de intensidad en config.ts.

## Estructura del video (cada línea es compases de la canción)
- Gancho (0 a 1,9 s, durante el compás 1 y el inicio del 2): suena la voz. En pantalla, el texto de la frase aparece palabra por palabra en los tiempos exactos del json: HOW · TO · SOUND · LIKE · y EYESOFDIRTY escrito como "EYES OF DIRTY" en tres palabras que entran repartidas dentro de los 0,8 s de esa palabra. Debajo, ya visible desde el fotograma 0, el panel PIANO 1.
- Compases 1-2: PIANO 1 versión normal (piano1.wav, posiciones 1-2 del loop). Panel con el piano roll de piano1.mid y etiqueta "PIANO 1". Durante la voz, el piano suena -10 dB; cuando la voz termina sube en un tiempo.
- Compases 3-4: PIANO 1 versión con cortes: audio de piano1_cuts.wav, sus compases 3-4. Etiqueta "PIANO 1 · CUTS". Mira la regla de cortes abajo.
- Compases 5-6: piano1.wav (posiciones 1-2) + lead.wav (posiciones 1-2). Entra el recuadro LEAD con piano roll de lead.mid, con destello corto; PIANO 1 se encoge y se apila arriba.
- Compases 7-8: piano1.wav + lead.wav, ahora las posiciones 3-4 de los loops. Ambos paneles visibles; el piano roll de cada uno sigue sus notas.
- Último tiempo del compás 8: silencio total en el audio (aire antes del drop). La imagen se congela medio tiempo y se oscurece un poco.
- Compás 9 (DROP): entra el beat completo desde su compás 9 hasta el compás 12, con todos los graves. En pantalla: destello, zoom de golpe con temblor en los tiempos 2 y 4, partículas que estallan en cada tiempo, los recuadros PIANO 1 y LEAD como miniaturas alrededor, un panel DRUMS con la forma de onda de drums.wav (compases 1-4 del loop alineados con los compases 9-12 del video, saltando con cada kick y snare) y un panel FULL BEAT con la forma de onda del mp3 y los números reales de compás.
- Compás 13: tarjeta final con "LAGRIMANKV", "FREE FOR NON PROFIT" y "151 BPM · A# MINOR · EYESOFDIRTY TYPE BEAT". El beat completo sigue sonando y se desvanece.

## Versión con cortes de PIANO 1 (compases 3-4)
- El audio es mi archivo piano1_cuts.wav, no lo regeneres. Usa sus compases 3 y 4 (de 2 x 1,589404 s a 4 x 1,589404 s del archivo). En esa parte suenan los tiempos 1-2 de cada compás y callan el 3 y el 4. Ponle fundidos de 5 ms en cada corte si hace clic.
- Piano roll: dibuja las notas de lead.mid (son las que contiene ese audio) recortadas a los 2 primeros tiempos de cada compás, para que lo que se ve coincida con lo que suena. Etiqueta "PIANO 1 · CUTS". Cada nota se ilumina cuando suena y el panel tiembla un poco en cada ataque.
- Comprueba los ataques del WAV contra las notas dibujadas (desfase menor a 60 ms) y anótalo en DECISIONS.md.
- Solo si piano1_cuts.wav no se pudiera usar, genera los cortes por código con una máscara de semicorcheas (pasos activos 0, 2, 3, 6, 8, 9, 11, 14) sobre piano1.wav, y dilo.

## Estilo visual (basado en 3 referencias vorty que analicé)
- Fondo casi blanco con degradado rosa suave, en pantalla desde el fotograma 0 (nunca negro). Paleta de referencia, que puedes cambiar en config.ts: fondo #fff5fa a #ffd6e8, acento #ff2d8a, magenta #d0105c, lavanda #9b6bff, azul #3aa0ff y verde menta #7be0a0 para los textos del gancho. Texto con contraste 4,5:1 como mínimo sobre su fondo.
- Texto del gancho: letras de bloques grandes (Silkscreen, Jersey 10 o Pixelify Sans, con @remotion/google-fonts), cada palabra en un color distinto de la paleta, apiladas en 2 o 3 líneas, centradas arriba. Cada palabra entra con un pop en el tiempo exacto de la voz, con un pequeño temblor.
- Paneles de piano roll dibujados desde el MIDI (SVG o divs), sin capturas de pantalla: rejilla clara, teclas a la izquierda, notas rosas con su nombre, línea de reproducción sincronizada. Flotan inclinados en 3D (perspective, rotateX, rotateY) con sombra suave. Laten en cada tiempo y entran y salen en medio tiempo con spring.
- Etiquetas en la tipografía de bloques (PIANO 1, PIANO 1 · CUTS, LEAD, DRUMS, FULL BEAT...). Las letras aparecen una por semicorchea.
- Tarjetas decorativas hechas con código, sin fotos: nubes procedurales y partículas.
- Abajo a la izquierda, fijo: "PROD. LAGRIMANKV" y "151 BPM · A# MINOR".
- Zonas seguras de 1080x1920: nada importante en los 150 px de arriba, ni en los 300 a 480 px de abajo, ni en x > 900 entre y 900 y 1700 (interfaz de TikTok).

## Audio (un solo WAV de 48 kHz armado antes de renderizar, con Python o ffmpeg)
- Cortes exactos al sample, fundidos de 5 ms y un único <Audio> en Remotion. No cortes el audio dentro de Remotion.
- Compases 1-8: voz + stems. Compases 9-12: beat.mp3 desde su compás 9 (12,745 s). Compás 13: el mp3 sigue y se desvanece.
- Voz alrededor de -14 LUFS y por encima del piano durante el gancho. Stems alrededor de -16 LUFS. Beat completo alrededor de -12 LUFS. Pico máximo de -1 dBTP.
- Entre la voz y el compás 3 no debe haber clics ni saltos de volumen.

## Verificación
1. Los transientes del audio final caen en la rejilla de 151 BPM (desfase menor a 15 ms).
2. Cada palabra del texto aparece como máximo 1 fotograma (16 ms) después de que suena en la voz.
3. El drop del compás 9 cae en un primer tiempo y el audio tiene silencio total en el último tiempo del compás 8.
4. Con npx remotion still, saca 12 fotogramas (incluye el 0, el de cada palabra, el último del compás 8 y el primero del compás 9) y revisa texto cortado, zonas seguras y legibilidad.
5. ffprobe del MP4 (1080x1920, 60 fps, pista de audio), blackdetect (no debe haber negro) y loudness con ffmpeg.

## Entrega
- Render H.264, yuv420p, CRF 16 o menos, audio AAC 320 kbps, en C:\Users\sharo\OneDrive\Documentos\marketing\lagrimankv_how_to_sound_like_eyesofdirty.mp4.
- Al final, escribe DECISIONS.md y un resumen con: compases usados, capas usadas, duración, desfases encontrados y cómo abrir Remotion Studio.
```

## Después de ejecutarlo
- Escuchar el video con audífonos: ¿la voz se entiende?, ¿el silencio antes del drop funciona?, ¿las capas suenan bien juntas?
- Anotar aquí qué funcionó y qué no, y pasar los ajustes (máscara de cortes, niveles de voz, orden de capas) a esta nota.
- Medir en el panel de [[Herramienta analitica YouTube]] el % visto y la duración media frente a los Shorts sin voz.

## Resultado (22 oct 2026, ejecutado en Claude Code)
- **Video:** `Documentos\marketing\lagrimankv_how_to_sound_like_eyesofdirty.mp4` (1080x1920, 60 fps, 1240 fotogramas = 20,67 s, H.264 CRF 16 yuv420p, AAC 320k).
- **Proyecto:** `C:\Users\sharo\remotion\eyesofdirty\` (composición `EyesOfDirty`). Studio: `npx remotion studio --port=3417`. Decisiones en `DECISIONS.md`, comandos en `README.md`.
- **Se reutilizó el código de kill4meeee** (piano roll, ondas, tarjetas 3D, `beatClock`) cambiando BPM, escala y paleta. Para el próximo video de este estilo, copiar esta carpeta y no empezar de cero.
- **Fase 0 confirmó todo:** 151 BPM (residuo 1,1 ms), mp3 en 30,0 ms, stems en 0 ms, graves de 0-5 % a 36 % en el compás 9. Las dudas (1) y (2) de arriba no se pueden resolver midiendo: piano y lead comparten armonía y ritmo, así que cualquier comparación da parecido. Se dibujó piano1.mid igual. Los ataques de piano1_cuts.wav coinciden con lead.mid recortado (mediana 1 ms).
- **Mezcla:** ganancia por fuente (cada stem a -16 LUFS) para que un sonido no salte de volumen entre partes; las capas sumadas de los compases 5-8 quedan en -13 LUFS (crecen hacia el drop de -12). Pico -1,77 dBTP.
- **Verificación (`audio/verify.py`):** transientes a 0,9 ms de la rejilla (mediana); palabras de 2 a 15 ms después del sonido (menos de 1 fotograma); drop a +1 ms del compás 9; sin negro; -13,4 LUFS.

### Errores de esta vez (y cómo evitarlos)
1. **Colores claros (menta, rosa, azul) sobre fondo casi blanco no llegan a 4,5:1 de contraste** (la menta da 1,5). Solución: contorno oscuro (`ink` #3b0a24) en todo el texto grande; texto chico en magenta o ink.
2. **Con fotogramas JPEG, Remotion sacó el mp4 como yuvj420p** (rango completo) aunque se pidiera yuv420p. Usar `Config.setVideoImageFormat("png")`.
3. **El oscurecido antes del drop se quedó puesto en todo el drop** (un `interpolate` con clamp a la derecha). Se vio solo al revisar fotogramas del mp4 final: revisar siempre fotogramas del drop en el video final, no solo los stills de antes.
4. El "silencio total" del último tiempo del compás 8 es exacto en `mix.wav`, pero el AAC deja un resto de unos -67 dBFS (inaudible). Es normal del códec.
5. El puerto 3000 estaba ocupado por otro Remotion Studio: usar `--port=3417`.
6. La tarjeta que abre el video debe verse entera en el fotograma 0 (miniatura); el resorte de entrada la dejaba invisible.

### Cambios del 23 oct (después de verlo)
- **No me gustó el silencio antes de las drums:** ahora el último tiempo del compás 8 suena (piano + lead hasta el drop), sin congelado ni oscurecido. Para próximos videos: **no meter el silencio de "aire antes del drop"** salvo que lo pida.
- **Paleta cambiada a azul intenso (#1f4bff / #0026d9), letras blancas y fondo negro.** Todos los colores siguen en `palette` de `config.ts`, así que cambiar de estética es editar un solo objeto. Con fondo negro el destello blanco pega más fuerte: bajado a 0,55.

### Cambios del 23 oct (2): GIFs de marketing, más destellos y animación
- **GIFs de `Documentos\marketing`** (los 6 sueltos) teñidos de azul con `TintedGif` (grises + mezcla "color" con el azul): ciudad de noche de fondo, árboles y atardecer como tarjetas, explosión del transformador como golpe del drop, rayas de luz en el drop, figura glitch detrás de la tarjeta final. Teñirlos hace que cualquier GIF encaje en la paleta.
- **La explosión sobre el drop tiene que ser corta** (40 fotogramas): la primera versión de 1,5 s lavó toda la pantalla y tapaba los paneles. Para sincronizar un GIF con un golpe, medir el brillo por fotograma (`signalstats`) y arrancarlo en el fotograma de la explosión.
- **Destellos:** uno por compás + tiempo 3 en la subida + tiempos 2 y 4 en el drop = 3 en 1 s como máximo (límite de fotosensibilidad). `verify.py` los cuenta sobre el mp4.
- Con fondo negro, `blackdetect` da falsos positivos en las tarjetas oscuras; las capas de GIF de fondo lo evitan.

### Pendiente
- Escucharlo con audífonos (voz, silencio antes del drop, capas) y subirlo; medir % visto contra los Shorts sin voz.
