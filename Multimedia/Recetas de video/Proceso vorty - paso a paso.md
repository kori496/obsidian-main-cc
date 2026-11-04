---
tags: [beats, proceso, vorty, lecciones]
actualizado: 2026-10-21
---

# 🧭 Proceso vorty: de la idea al prompt final

Volver a [[Estilo de videos de vorty]] · Prompt final: [[Prompt vorty - breakdown rosa 3D (Remotion)]]

Resumen de todo lo que se hizo en el chat "estilo de videos de vorty" (≈19 oct 2026), en orden, con mis mensajes literales, lo que pasó y lo que aprendimos. Sirve para repetirlo con otro beat sin empezar de cero.

## Línea de tiempo

| # | Lo que pedí (literal) | Qué pasó |
| --- | --- | --- |
| 1 | "podemos hacer el estilo de videos de vorty?" (con 3 videos de referencia adjuntos) | Primero no encontró "vorty" ni en memoria ni en la web y pidió una referencia. Con los 3 videos analizó fotograma a fotograma y guardó el estilo en el documento del proyecto. Aclaró que la marca de agua era @iambenjam1n. |
| 2 | "lagrimankv, me gustaria que muestres los stems por partes, tipo lead (solo el pattern de las leads) piano (solo el pattern de los pianos) drums (solo las drums) pero con las partes que mas destaquen en el beat y luego el beat final" | Definió la estructura: gancho → lead → piano → drums → beat final → tarjeta "lagrimankv". Pidió beat, stems, MIDI y las partes que más destacan. El nombre del productor se confirmó como **lagrimankv** (no "lakrimankv"). |
| 3 | "134bpm B iwato, te paso los videos de todos los stems y escoge los que mas te gusten recortalos donde sea necesario y haz que el video sea fluido y siempre siga el ritmo del beat (134bpm) tambien haz que las transcisiones o efectos en pantalla tengan animaciones al tempo del beat" | 11 archivos (grabaciones de pantalla de FL). Empezó a revisarlos por compás a 134 BPM. |
| 4 | "olvide subirte el video del beat completo, ahi esta, quiero hagas 3 videos de ese estilo con este mismo beat en variaciones distintas" | Cambió a 3 videos con el mismo beat, cada uno con otra selección y orden. |
| 5 | "el video debe ser en vertical, para tiktok y youtube shorts" | 1080x1920. |
| — | (Claude entregó los 3 primeros videos) | `v1_how_i_cooked` 21,5 s, `v2_b_iwato` 25 s, `v3_layer_by_layer` 19,7 s. Usaban capturas de FL pasadas a rosa. |
| 6 | "casi nada armoniza bien, te paso los stems de los instrumentos?" | **Causa:** cada grabación de pantalla empezaba en un punto distinto de la canción; al pegar pedazos de lugares diferentes los acordes chocaban. Solución: stems exportados desde el compás 1, todos con la misma duración. |
| 7 | "y tambien dime como te paso los midis del proyecto" | FL: `File → Export → MIDI file` (todo el proyecto, alineado) o, por pattern, `File → Export as MIDI file` desde el piano roll. Pasar por carpeta conectada o .zip. |
| 8 | "con 4 midis te sirve? me gustaria que las drums las hagas con ondas de audio, tipo el combo completo" | Sí. Drums = una onda grande del stem combo, rosa, con línea de reproducción fija. |
| 9 | "esta separado por carpetas, aun no hagas el video me falta renderizar las drums" | Revisó la carpeta: los 4 MIDI eran el mismo archivo vacío (79 bytes, canal Denstrings sin notas). |
| 10 | "y ahora? la cancion esta arrangeada asi: [captura] y quiero que la parte de un video sea de la intro (1) hasta el compas 12 y el resto de videos busca la parte mas movida de la cancion videos sea empezando en el compas, todavia no lo hagas y dame el prompt para hacerlo con claude code" | MIDI ya con notas (sakura 34, 808 14, bass 6, lead 4). Faltaban drums completas, beat completo desde el compás 1 e instrumentos de la intro. Escribió el prompt para Claude Code. |
| 11 | "ya actualice la carpeta con las drums y el beat completo" | `drums.wav` dura 4 compases (7,5 s) y arranca en el primer tiempo. `kill4meeee.mp3` es el beat completo con el compás 1 en 0 s. Partes más movidas medidas: **17–24** (primer drop), 45–52 y 61–68. 41–44 es un break. |
| 12 | "ponle que haga los videos en remotion para una mejor calidad" | Prompt reescrito para Remotion: 60 fps, CRF ≤ 16, AAC 320 kbps, fuente pixelada real, piano roll desde MIDI, 3D con CSS, audio mezclado antes y un solo `<Audio>`. |
| 13 | "le paso los videos de referencia?" | Sí: ponerlos en `...\referencias\` y añadir la sección "Videos de referencia" al prompt (está en [[Prompt vorty - breakdown rosa 3D (Remotion)#Sección opcional: videos de referencia]]). |
| 15 | (21 oct) "actualiza para que no siempre tenga color rosa, que sea variado conforme a la estetica que yo te diga del beat" | Se agregó el bloque "Estética del beat" al prompt: paleta, fondo y motivo variables, colores en `config.ts`, contraste mínimo. El rosa queda como paleta de referencia. |
| 14 | "/skill-creator" | Se creó la skill `prompt-video-beats` (revisa archivos, detecta errores conocidos, escribe el prompt con esta estructura y tiene una biblioteca de estilos). Pendiente probarla con 3 casos. |

## Archivos del beat (kill4meeee)
Carpeta: `C:\Users\sharo\OneDrive\Documentos\Image-Line\FL Studio\Projects\el rap de charlie kirk\midis\`
- `kill4meeee.mp3`: beat completo (compás 1 en 0 s).
- `drums.wav` (combo, 4 compases). Ignorar `drums\drums 8 compases.wav` (solo 2 compases).
- Piano: `piano sakura\Sakura_2.wav` + `sakura.mid` (ignorar `piano sakura.mid`, vacío).
- Lead: `lead lead biohazard\Toxic Biohazard #3_2.wav` + `lead biohazard.mid`.
- Bass: `bass\3x Osc_2.wav` + `bass.mid`.
- 808: `808\MM3 808 @bangtozzy_2.wav` + `el rap de charlie kirk.mid`.
- Los WAV son loops que empiezan en el compás 1 de su pattern; los MIDI son patterns de 4 compases (PPQ 96). Las notas encajan en B iwato (B, C, E, F, A).

## Errores que nos pasaron (y cómo evitarlos)
1. **Armonía rota** por mezclar grabaciones que empiezan en puntos distintos → usar stems exportados desde el compás 1, misma duración.
2. **MIDI vacíos** porque en FL estaba seleccionado otro canal (Denstrings) → antes de exportar, abrir el pattern del instrumento y comprobar que el piano roll dice ese instrumento y se ven las notas.
3. **Loops más cortos de lo que dice el nombre** (`drums 8 compases.wav` duraba 2 compases) → medir la duración de cada WAV.
4. **Archivos repetidos o vacíos** (`piano sakura.mid`) → ignorarlos explícitamente en el prompt.
5. **Instrumentos de la intro sin exportar** (M1 crab nebula, Sawer, Toxic Biohazard #2 y #4, Denstrings, vox ULTRAVIOLET) → si se quiere mostrarlos en V1 hay que exportar su MIDI y WAV.
6. **Sincronía "a ojo"** → fórmula exacta, rejilla de BPM y desfase < 15 ms.
7. Los textos pequeños de la playlist (barras de compás, nombres de samples como "@bangtozzy") se ven mal en vertical → ocultarlos/tapar o dibujar el panel por código.

## Checklist antes de empezar un video nuevo
- [ ] BPM, compases y escala del beat.
- [ ] Beat completo exportado desde el compás 1 (confirmar que el compás 1 cae en 0 s).
- [ ] Stems WAV con `Split mixer tracks`, todos desde el compás 1, misma duración.
- [ ] MIDI de cada instrumento con notas (abrir uno y verificar) y nombre claro.
- [ ] Drums como combo en un solo WAV, con la duración correcta.
- [ ] Arreglo por bloques de 4 compases (qué entra y cuándo).
- [ ] Compases más movidos (o dejar que Claude los mida por energía).
- [ ] Cuántos videos, ganchos en inglés y movimiento de cada uno.
- [ ] **Estética del beat y paleta** (palabras y, si la tengo, hex): fondo, acento principal, acento 2, acento 3, motivo de las tarjetas.
- [ ] Referencias de estilo en una carpeta (solo estructura y movimiento, no el color).
- [ ] Tag: **lagrimankv** / "PROD. LAGRIMANKV".

## Pendientes
- [ ] Ejecutar el prompt en Claude Code (carpeta `remotion` nueva).
- [ ] Escuchar los 3 videos con audífonos y confirmar que el ritmo cae bien.
- [ ] Probar la skill `prompt-video-beats` con los 3 casos de prueba.
- [ ] Exportar MIDI/WAV de los instrumentos de la intro si quiero mostrarlos en V1.
