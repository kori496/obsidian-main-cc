---
tags: [beats, estilo, vorty, breakdown, remotion]
actualizado: 2026-10-21
---

# 🎀 Estilo de videos de vorty (breakdown 3D por stems, paleta variable)

Volver a [[Videos beats]] · Formatos en [[Estilos y formatos]]
Prompt final: [[Prompt vorty - breakdown rosa 3D (Remotion)]] · Cómo se llegó: [[Proceso vorty - paso a paso]]

Fuente: chat "estilo de videos de vorty" (≈19 oct 2026, con el proyecto de beats). Este es **el** estilo que llamo "vorty". Cuando pida "otro video como el de vorty", se hace con esta receta y ese prompt, sin inventar nada.

> Aclaración que quedó anotada: en los 3 videos de referencia la marca de agua dice **@iambenjam1n**, no "vorty". Es solo una referencia de estilo: no se copia nada (ni capturas, ni fotos, ni marcas de agua, ni el @, ni la pantalla final de TikTok).

## 🎨 La paleta cambia según la estética del beat
El **rosa no es fijo**. Rosa fucsia fue la paleta de las referencias y del beat kill4meeee. En cada video nuevo yo digo la **estética del beat** (ej.: lo-fi cálido, oscuro y neón, pastel menta, frío azul hielo) y de ahí salen:
- fondo (claro con degradado suave, u oscuro),
- acento principal, acento 2 y acento 3 para subtítulos, y color de texto,
- el motivo de las tarjetas decorativas (nubes, estrellas, cuadrícula, ondas, humo...).

Reglas: si no digo la estética, Claude me la pregunta una vez antes de empezar. Si solo la digo con palabras, elige los hex, los anota en `DECISIONS.md` y enseña una muestra de paleta. Contraste mínimo 4.5:1 en los textos. Todos los colores viven en un objeto `palette` en `config.ts`, nunca dentro de los componentes. **Lo que no cambia:** estructura, paneles 3D, piano roll desde MIDI, onda de drums, tipografía pixelada, textos en inglés y las reglas de sincronía.

## Qué es
Un video corto vertical que muestra **cómo está hecho el beat por partes (stems)**: cada instrumento solo, con lo que más destaca, y al final el beat completo como recompensa (el drop).

## El look (de las 3 referencias)
- En las referencias: fondo blanco con degradado rosa suave y **un solo color de acento**, rosa fucsia. **Paleta de referencia** (kill4meeee): `#ff2d8a`, magenta `#d0105c` y lavanda `#9b6bff` para subtítulos. Para otros beats se cambia (ver arriba).
- **Paneles** flotando e inclinados en 3D con perspectiva y sombra suave: piano roll, playlist, forma de onda.
- **Tarjetas** de color de acento entre los paneles (rosas en las referencias): en las referencias llevan partículas y fotos de naturaleza (nubes, girasoles, flores). En mis videos se hacen **por código** (nubes procedurales, partículas que estallan en cada tiempo, espectro del audio), sin fotos de terceros.
- **Texto:** etiquetas en letra pixelada y condensada (SYNTH, LEAD, PLUCK, DRUMS, CHOPPED LOOP). El título del gancho tiene letras de colores que se arman. En Remotion: fuente Silkscreen, Jersey 10 o Pixelify Sans.
- Movimiento: cámara continua, casi sin cortes. Los paneles **laten en cada tiempo**, entran y salen en medio tiempo, y hay un **destello** en cada cambio de parte.

## Estructura de la referencia (18–22 s)
- 0–3 s: gancho tipo "how??" o "secret of crazy sound!!".
- 3–6 s: la playlist completa con "kit link in bio".
- 6–16 s: un panel por instrumento.
- Cierre: barra de búsqueda de TikTok con el @ (la pone TikTok). En los míos va la **tarjeta final con "lagrimankv"**.

## Estructura de mis videos
1. **Gancho** (1 compás): título grande en letras de bloques de colores sobre el primer panel.
2. **Partes por instrumento:** 2 compases cada una, solo el audio de ese stem (o capas que se suman). Número de partes **par**, para que el beat completo entre en el compás 1 de un bloque.
3. **Beat completo:** 4 compases, con miniaturas de los paneles anteriores alrededor y un destello en cada compás.
4. **Tarjeta final** (1 compás): "LAGRIMANKV", "FREE FOR NON PROFIT", "134 BPM · B IWATO · TYPE BEAT"; el audio se desvanece.
- Fijo abajo a la izquierda: "PROD. LAGRIMANKV" y "134 BPM · B IWATO".

## Los 3 videos (variaciones del mismo beat, "kill4meeee")
| Video | Gancho | Orden | Movimiento |
| --- | --- | --- | --- |
| V1 `lagrimankv_v1_intro` | HOW I COOKED THIS?? | Compases 1–12 tal como suenan (bass, luego entra el piano en el 9) + tarjeta final | Paneles giran hacia los lados |
| V2 `lagrimankv_v2_b_iwato` | B IWATO GOES CRAZY | Compases 17–24: DRUMS → 808 → LEAD → BASS → beat completo | Zoom de golpe y temblor en los tiempos 2 y 4 |
| V3 `lagrimankv_v3_layer_by_layer` | LAYER BY LAYER | PIANO → + LEAD → + 808 → + DRUMS → beat completo (compases 45–48, o 21–24 si no coinciden los patterns) | Los paneles anteriores se encogen y se apilan arriba |

## Reglas que NO se negocian (nacieron de errores)
- **Todo corte, entrada y salida cae en el primer tiempo de un compás**, calculado con la fórmula (1 tiempo = 60/BPM s; a 134 BPM = 0,447761 s; 1 compás = 1,791045 s), no a ojo.
- Los **loops solo se combinan en la misma posición** dentro del bloque de 4 compases. Nunca el compás 3 de un loop sobre el compás 1 de otro (así "casi nada armonizaba").
- Cada parte alterna compases 1–2 y 3–4 del loop, para que la progresión avance como en la canción.
- Animaciones calculadas con el **tiempo** (t = frame / fps), no con el número de fotograma. Función central `beatClock(frame)`.
- Piano roll **dibujado desde el MIDI**, nunca de capturas de pantalla (las capturas empiezan en puntos distintos de la canción).
- Drums como **onda de audio** del combo completo (`drums.wav`), en el color de acento sobre el fondo, con línea de reproducción fija; cada kick/snare hace saltar el panel y enciende un destello.
- Textos en **inglés**, slang, **sin emojis**. Zonas seguras de TikTok: nada importante en x > 900 entre y 900 y 1700, ni en los 300 px de abajo.
- Audio: cada parte ~ -16 LUFS, beat completo ~ -12 LUFS, pico ≤ -1 dBTP, fundidos de 5 ms en cada corte. La mezcla de cada video se arma **antes** como un solo WAV de 48 kHz y se mete en Remotion con un único `<Audio>`.

## Calidad (versión Remotion)
- 1080x1920 a **60 fps**, H.264, CRF ≤ 16, yuv420p, AAC 320 kbps.
- 3 composiciones: `V1Intro`, `V2BIwato`, `V3Layers`. Se puede abrir en Remotion Studio para cambiar textos y tiempos.

## Resultados publicados (22 oct 2026)
Videos con "kill4meeee" según el reporte de YouTube (24 jul a 21 oct) y las publicaciones de TikTok de Metricool. Los títulos no dicen qué variante es (V1, V2 o V3), así que no se puede separar por variante.

| Canal | Video | Vistas | % visto | Duración |
| --- | --- | --- | --- | --- |
| YouTube | "kill4meeee outnowww" | 12 | 69,5 | 16 s |
| YouTube | "sickkk beat out NOWWWW" | 7 | 86,2 | 17 s |
| YouTube | "free for non profit dark trap type beat - kill4meeee" | 34 | 14,5 | 19 s |
| YouTube | "check the whole beat kill4meeee" | 0 | - | - |
| TikTok | "kill4meeee YT>lagrimankv" (20 oct) | 127 | - | 9 likes |
| TikTok | "kill4meeee on youtubeeee" (21 oct) | 162 | - | 3 likes |

- En YouTube, el estilo queda muy por debajo de los Shorts de boom bap (skatepark 700, ps2 162).
- En TikTok, el mismo beat da 289 vistas entre dos posts. Es lo mejor que tiene ese beat.
- Muestra muy chica. No concluir que el estilo no funciona: cambiar una variable a la vez.
- "woeklifeee" no aparece en los títulos del reporte de YouTube. No se puede medir todavía.

## Estado (21 oct 2026)
- ✅ Estilo analizado y guardado; prompt final para Claude Code + Remotion escrito.
- ✅ Skill `prompt-video-beats` creada para generar este tipo de prompts (revisa los archivos, detecta errores y escribe el prompt).
- ⏳ Falta **ejecutar el prompt en Claude Code** (con la estética del beat indicada) y revisar los 3 videos (confirmar el ritmo escuchándolos con audífonos).
- Primer intento en el chat (30 fps, con capturas de FL en rosa) salió con problemas de armonía: no usar ese enfoque.

## Corrección (22 oct 2026)
- Los kill4meeee **funcionan bien**: "check the whole beat kill4meeee" tiene unas 338 vistas en YouTube (la analítica de YouTube aún lo mostraba en 0 por retraso) y en TikTok 127 y 162 vistas. La tabla de arriba lo subestimaba. Dato de YouTube confirmado por el usuario. Detalle en [[Métricas y revisiones]].
