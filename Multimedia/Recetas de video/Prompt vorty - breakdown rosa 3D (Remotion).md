---
tags: [beats, prompt, vorty, remotion, claude-code]
actualizado: 2026-10-21
---

# 🎬 Prompt vorty: breakdown 3D por stems (Claude Code + Remotion)

Volver a [[Estilo de videos de vorty]] · Proceso en [[Proceso vorty - paso a paso]] · Pipeline general en [[Pipeline visualizer Remotion]]

Versión **final** (la que se pega en Claude Code, dentro de una carpeta vacía). Es la versión Remotion del chat (cambio pedido: "ponle que haga los videos en remotion para una mejor calidad"). Vale para el beat **kill4meeee** (134 BPM, B iwato). Para otro beat, cambiar solo lo de la sección "Qué cambiar para un beat nuevo" que está abajo.

> 🎨 **El color ya no es siempre rosa.** La paleta, el fondo y el motivo de las tarjetas salen de la "Estética del beat" que yo indique en cada pedido. El rosa fucsia es solo la paleta de referencia (la del beat kill4meeee). La estructura, el 3D y las reglas de sincronía no cambian.

Copia también guardada en el proyecto de Claude: `claude/prompt-videos-claude-code.md`.

## Qué cambiar para un beat nuevo
- **Estética y paleta** (lo primero): ver el bloque "Estética del beat" dentro del prompt. Si no la dije, preguntarme antes de empezar.
- Nombre del beat, BPM, escala, y `1 tiempo = 60/BPM`, `1 compás = 4 × tiempo`, fotogramas por tiempo a 60 fps.
- Carpeta y archivos: beat completo (mp3 o wav, con el compás 1 en 0 s), stems WAV y MIDI de cada instrumento, drums combo.
- **Arreglo por compases** (qué entra en cada bloque de 4 compases) y **qué compases son los más movidos** (si no se sabe, pedir que los mida por energía).
- Qué 3 videos se quieren, ganchos (títulos en inglés) y movimiento de cada uno.
- Rutas de entrega.
- Antes de ejecutarlo, revisar los archivos con la lista de [[Proceso vorty - paso a paso#Checklist antes de empezar un video nuevo]].

## Prompt

```txt
Eres mi editor de video. Crea 3 videos verticales para TikTok y YouTube Shorts que muestran por partes cómo está hecho mi beat. Hazlos en Remotion (React) para tener la mejor calidad. No me preguntes nada salvo que falte un archivo o que la estética del beat esté sin definir (en ese caso pregúntamela una sola vez, antes de programar): toma decisiones razonables y anótalas al final.

## Proyecto y herramientas
- Crea un proyecto de Remotion nuevo con TypeScript en C:\Users\sharo\OneDrive\Documentos\Image-Line\FL Studio\Projects\el rap de charlie kirk\remotion\. Necesitas Node.js 18 o más nuevo; si falta, dime cómo instalarlo y para.
- Tres composiciones: V1Intro, V2BIwato y V3Layers. Cada una de 1080x1920, a 60 fps, con la duración exacta en fotogramas calculada desde los compases.
- Copia los WAV, los MIDI y el mp3 a public/ y cárgalos con staticFile().
- Lee los MIDI con @tonejs/midi. Saca las formas de onda con @remotion/media-utils (getAudioData y visualizeAudio o getWaveformPortion).
- Tipografía: carga con @remotion/google-fonts una fuente pixelada de bloques (Silkscreen, Jersey 10 o Pixelify Sans). Usa una versión condensada y alta para las etiquetas grandes.
- Perspectiva 3D con transformaciones CSS (perspective, rotateX, rotateY, rotateZ) y sombras con box-shadow o filter: drop-shadow.
- Audio: arma primero la mezcla final de cada video como un solo WAV de 48 kHz con Python (numpy, soundfile) o ffmpeg, con cortes exactos al sample, normalización y fundidos. Después ponla en Remotion con un único <Audio>. No cortes el audio dentro de Remotion.
- Render final: npx remotion render con codec h264, CRF 16 o menos, pixel format yuv420p, audio AAC de 320 kbps. Revisa en Remotion Studio mientras trabajas.

## Datos del beat
- Productor: lagrimankv
- 134 BPM, 4/4, escala B iwato. 1 tiempo = 0,447761 s; 1 compás = 1,791045 s. A 60 fps, 1 tiempo = 26,866 fotogramas.
- Carpeta: C:\Users\sharo\OneDrive\Documentos\Image-Line\FL Studio\Projects\el rap de charlie kirk\midis\
  - kill4meeee.mp3: beat completo. El compás 1 empieza en 0,000 s (confírmalo con la rejilla).
  - drums.wav: combo completo de drums, loop de 4 compases. Ignora drums\drums 8 compases.wav (solo dura 2 compases).
  - piano sakura\Sakura_2.wav + sakura.mid: piano. Ignora "piano sakura.mid", está vacío.
  - lead lead biohazard\Toxic Biohazard #3_2.wav + lead biohazard.mid: lead.
  - bass\3x Osc_2.wav + bass.mid: bass.
  - 808\MM3 808 @bangtozzy_2.wav + el rap de charlie kirk.mid: 808.
  Los WAV son loops que empiezan en el compás 1 de su pattern. Los MIDI son patterns de 4 compases (PPQ 96).
- Arreglo en la playlist de FL. Los patterns van en bloques de 4 compases que empiezan en los compases 1, 5, 9, 13, 17, 21...
  - 1-8: 3x Osc (bass), M1 crab nebula, Sawer, Toxic Biohazard #2, Toxic Biohazard #4, SFX de drop en el compás 1.
  - 9-12: entran Sakura (piano), Morphine, Denstrings y el vox ULTRAVIOLET. Siguen bass, crab nebula, Sawer y TB#2.
  - 13-16: entran las drums (snares y open hat). El 808 entra en el compás 15.
  - 17-24: la parte más llena: todo lo anterior + Toxic Biohazard #3 (lead), 808 completo, hats FLORIDA FLOW y tags de voz.
  - 25-32: bass, piano, Toxic Biohazard, Morphine, Denstrings, crab nebula, Sawer, 808 #2, drums y vox.
  - Por energía medida: 41-44 es un break, y 45-52 y 61-68 son las otras partes más fuertes.

## Reglas de sincronía (lo más importante)
- Todo corte, entrada y salida cae exactamente en el primer tiempo de un compás. Calcula los tiempos con la fórmula, no a ojo.
- Antes de cortar, detecta el primer transiente de cada WAV y confírmalo ajustando una rejilla de 134 BPM. Reporta el desfase de cada archivo y corrígelo.
- Los loops solo se combinan entre sí o con el beat completo en la misma posición dentro del bloque de 4 compases. El compás 1 del loop va con el compás 1, 5, 9, 13, 17... de la canción. Nunca pongas el compás 3 de un loop sobre el compás 1 de otro.
- Cada parte por instrumento dura 2 compases y alterna los compases 1-2 y 3-4 del loop, para que la progresión avance como en la canción. El número de partes antes del beat completo es par, para que el beat completo entre en el compás 1 de un bloque.
- Si un loop es más corto que lo que necesitas, repítelo en compases enteros. Corta la cola que sobra después del compás 4 del loop.
- En Remotion, calcula todo desde el tiempo: t = frame / fps; beat = t / 0,447761; fase = beat % 1. Pulsos, entradas, salidas, letras y destellos salen de ahí con interpolate() y spring(). No redondees los límites de compás a fotogramas enteros cuando calcules las animaciones.
- Haz una función central (por ejemplo beatClock(frame)) con compás, tiempo, fase y un "kick" que decae, y úsala en todos los componentes.

## Estética del beat (la cambio en cada beat)
- Estética: [describir con palabras, ej.: "lo-fi cálido, tonos tierra", "oscuro y neón", "pastel menta", "frío, azul hielo", "rosa fucsia"]. Si dice [por definir], pregúntamela.
- Paleta: fondo [#hex o degradado], acento principal [#hex], acento 2 [#hex], acento 3 para subtítulos [#hex], texto [#hex]. Si solo te doy la estética en palabras, elige tú los hex, anótalos en DECISIONS.md y muéstrame una paleta de muestra (un npx remotion still) antes de seguir.
- Fondo: claro con degradado suave del acento, u oscuro, según la estética. Si es oscuro, invierte sombras y brillos para que los paneles sigan flotando.
- Motivo de las tarjetas decorativas: [ej.: nubes, estrellas, cuadrícula, ondas, humo, pétalos], generado por código.
- Contraste: el texto sobre cualquier fondo cumple 4.5:1 como mínimo. Si un color de la paleta no lo cumple, ajústalo y anótalo.
- Paleta de referencia, solo si no te doy otra (la del beat kill4meeee, rosa): fondo blanco con degradado rosa suave, acento #ff2d8a, magenta #d0105c y lavanda #9b6bff.
- Todos los colores salen de un objeto `palette` en config.ts. Ningún color va escrito dentro de los componentes, para poder cambiar la estética tocando un solo archivo.

## Estilo visual: breakdown 3D por stems
- Usa los colores de la paleta de arriba en todo lo que se describe a continuación (donde diga "color de acento", "fondo" o "color de las letras").
- Paneles flotantes inclinados en 3D con perspectiva y sombra suave. Laten en cada tiempo, entran y salen en medio tiempo con spring, y en cada cambio de parte hay un destello corto.
- Piano roll dibujado desde el MIDI como componente (SVG o divs), sin capturas de pantalla: rejilla clara, teclas a la izquierda, notas en el color de acento con su nombre (B4, F5...) y una línea de reproducción sincronizada. Cada nota se ilumina y crece un poco cuando suena.
- Drums: panel con la forma de onda del combo completo (drums.wav), en el color de acento sobre el fondo, que avanza bajo una línea de reproducción fija. Cada kick o snare hace saltar el panel y enciende un destello.
- 808 y bass: piano roll desde su MIDI, con una forma de onda pequeña debajo.
- Beat completo: panel con la forma de onda del mp3 y marcas de compás numeradas con el número real de compás de la canción.
- Etiquetas en la tipografía de bloques (LEAD, PIANO, 808, BASS, DRUMS, FULL BEAT). Las letras aparecen una por semicorchea con un pop.
- Tarjetas decorativas generadas por código, sin fotos ni material de terceros: nubes procedurales en SVG o canvas, partículas que estallan en cada tiempo y el espectro del audio con visualizeAudio.
- Abajo a la izquierda, fijo: "PROD. LAGRIMANKV" y "134 BPM · B IWATO".
- Textos en pantalla en inglés, tono slang, sin emojis.
- Zonas seguras de TikTok: nada importante en x > 900 entre y 900 y 1700, ni en los 300 px de abajo.

## Estructura general
1. Gancho durante el primer compás: título grande en letras de bloques con los colores de la paleta, encima del primer panel. Sale al empezar el compás 2.
2. Partes por instrumento (2 compases cada una, solo el audio de ese stem, o las capas indicadas).
3. Beat completo durante 4 compases desde el inicio de su sección, con miniaturas de los paneles anteriores alrededor y un destello en cada compás.
4. Tarjeta final de 1 compás: "LAGRIMANKV", "FREE FOR NON PROFIT", "134 BPM · B IWATO · TYPE BEAT". El audio del beat completo sigue y se desvanece.

## Los 3 videos
- V1Intro (compases 1 a 12 de la canción): el audio es kill4meeee.mp3 desde el compás 1 hasta el final del compás 12, tal como suena, más 1 compás de tarjeta final (compás 13, con fundido). En pantalla:
  - Compases 1-8: panel BASS (piano roll de bass.mid, en bucle) y un panel FULL MIX con la forma de onda del mp3.
  - Compases 9-12: entra el panel PIANO (piano roll de sakura.mid) con destello. El bass se encoge y se queda arriba.
  - Gancho: "HOW I COOKED THIS??". Movimiento: los paneles giran hacia los lados al entrar y salir.
- V2BIwato, primera parte más movida (compases 17-24): DRUMS, 808, LEAD y BASS, 2 compases cada uno y solo el audio de ese stem. Usan las posiciones 1-2, 3-4, 1-2 y 3-4 de sus loops. Después, el beat completo de los compases 17-20 del mp3. Gancho: "B IWATO GOES CRAZY". Movimiento: zoom de golpe al entrar y temblor en los tiempos 2 y 4.
- V3Layers, capas: PIANO, luego + LEAD, + 808 y + DRUMS. Cada parte suma su stem a los anteriores, 2 compases cada una, en las mismas posiciones de loop. Después, el beat completo de los compases 45-48 del mp3. Antes, compara el espectro de los compases 45-48 con los loops: si no usan los mismos patterns, usa los compases 21-24. Gancho: "LAYER BY LAYER". Movimiento: los paneles anteriores se encogen y se apilan arriba.

## Audio
- Normaliza cada parte para que se oigan parejas (alrededor de -16 LUFS). El beat completo va un poco más fuerte (alrededor de -12 LUFS). Pico final de -1 dBTP o menos.
- Fundidos de 5 ms en cada corte para evitar clics.

## Entrega y verificación
- Renderiza en C:\Users\sharo\OneDrive\Documentos\Image-Line\FL Studio\Projects\el rap de charlie kirk\videos\ como lagrimankv_v1_intro.mp4, lagrimankv_v2_b_iwato.mp4 y lagrimankv_v3_layer_by_layer.mp4.
- Antes de entregar, verifica:
  1. Que los transientes del audio final caigan en la rejilla de 134 BPM (desfase menor a 15 ms).
  2. Que cada cambio de parte esté en un primer tiempo.
  3. Con npx remotion still, saca 10 fotogramas por video y revisa texto cortado, zonas seguras y paneles legibles.
  4. Loudness y pico del MP4 final con ffmpeg.
- Al final, escribe una tabla por video con los compases de la canción usados, las partes, la duración y las decisiones que tomaste. Dime también cómo abrir Remotion Studio para hacer cambios.
```

## Sección opcional: videos de referencia
Se agrega justo después de "Estilo visual". Poner los 3 videos de referencia (los de @iambenjam1n) en `...\el rap de charlie kirk\referencias\`.

```txt
## Videos de referencia
- En C:\Users\sharo\OneDrive\Documentos\Image-Line\FL Studio\Projects\el rap de charlie kirk\referencias\ hay 3 videos de otro productor con el estilo que busco.
- Antes de programar, saca con ffmpeg una hoja de contacto de cada uno (un fotograma cada 0,5 s) y unos 12 fotogramas seguidos de 2 a 3 segundos, para ver cómo se mueven los paneles. Anota:
  - el tamaño de los paneles respecto a la pantalla,
  - cuánto se inclinan y cuánto duran las entradas y salidas,
  - el tamaño y la posición de las etiquetas,
  - cuántas tarjetas hay en pantalla a la vez,
  - el ritmo de los cortes.
- Son solo referencia de **estructura y movimiento**. El **color no se toma de ellas**: la paleta sale de la sección "Estética del beat".
- Son solo referencia de estilo, no se copian. No uses nada de esos videos: ni capturas, ni fotos, ni marcas de agua, ni el @ del creador, ni su pantalla final de TikTok. Todo el contenido sale de mis archivos y de gráficos generados por código.
- Cuando termines, compara una hoja de contacto de cada video mío con la de la referencia y dime en qué se parecen y en qué no.
```
