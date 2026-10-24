---
tags: [beats, estilo, make-beat, glitch, scripts]
actualizado: 2026-10-21
---

# 🧁 Estilo make beat (menta, lila y glitch)

Volver a [[Videos beats]] · Formatos en [[Estilos y formatos]]
Scripts: carpeta `Scripts make beat/` (`analyze.py`, `fit_beatgrid.py`, `render.py`, `glitch.py`). Obsidian no muestra `.py`: abrirlos desde VS Code o Claude Code.

Fuente: chat "Video editing style for beats" (17 oct 2026). Es **otro** estilo distinto de [[Estilo de videos de vorty]]: aquí se edita una **grabación de pantalla de FL Studio** con look pastel, TV retro/ventana, stickers y textos al ritmo. Para repetirlo con otro beat se usan estos scripts y estos parámetros, sin reinventar.

## Referencia
- Un TikTok de "make beat" (descargado como `valtoory_TikTokDownloader...`; en el chat se anotó el nombre del creador como "lunexea"). Clip vertical de 11.7 s, 576x1024, 30 fps, audio ~ -6.4 LUFS.
- Lo que tenía: fondo blanco y azul cian, tipografía geométrica en minúsculas, stickers (flor, estrella) en los bordes, pantallas tipo TV retro o rejillas de secuenciador, etiquetas cortas por capa ("beat", "chords", "arpeggio", "drum", "base") que entran justo en el golpe, elementos que cambian casi a cada golpe (onsets cada ~0.2–0.5 s) y capas que entran y salen cada 0.5–1.5 s.
- No se copia logo, nombre ni contenido del creador.

## Mis mensajes (literales)
1. "https://vt.tiktok.com/ZSg2pA7vy/ puedes editar un video para que quede en ese estilo? la idea sería videos de beats, y me gusta ese estilo de edición"
2. "quiero el look completo pero que adaptes el color y estilo en formas diferentes, haz que el que te mande dure aproximadamente 15segundos en una parte catchy"
3. "como debería grabar los clips para que se vea mejor"
4. "puedes agregarle un estilo de edición parecido al que te pasé a este video? puedes hacerlo un poco más glitchy para que vaya con la canción"

## Proceso (versión 15.9 s: menta y lila)
Entrada: grabación de pantalla horizontal de FL (1280x720, 114 s).
1. **Analizar la referencia** con ffmpeg: cortes de escena (`select='gt(scene,0.08)'`), hoja de contacto (`fps=2,scale=144:256,tile=12x2`), onsets del audio y volumen (LUFS).
2. **Analizar el audio del video base** con `analyze.py` (numpy/scipy, `librosa` no se instaló): BPM por autocorrelación del flujo espectral, energía por tramos, mejor ventana de 15 s.
3. **Elegir el tramo catchy:** drop en **89.025 s**, BPM **150.9** (ajustado con `fit_beatgrid.py` sobre 88.8–104 s, BPM 148–156). El video arranca 1 compás antes del drop (`START = 89.025 - 4·P`) y dura **40 tiempos = 10 compases = 15.9 s**.
4. **Renderizar con `render.py`** (Python + PIL + numpy + ffmpeg, cuadro a cuadro): `python render.py menta|lila <src.mp4> <out.mp4> [--preview]`. `--preview` guarda 10 cuadros de prueba. Se renderizan las dos variantes en paralelo.
5. **Revisar** hoja de contacto de los cuadros (y subir contraste de las pantallas del DAW si no se leen). Salida: 1080x1920, 30 fps, H.264 CRF 18, AAC 192k con audio original, fade-in de 30 ms y fade-out de 0.4 s.

### Estructura por secciones (en tiempos/beats)
| Beats | Sección | Qué pasa |
| --- | --- | --- |
| 0–3 | Intro | "make" / "beat" / subtítulo en coreano (como la referencia) / ♪ |
| 4–11 | Drop | Flash de color, pantalla grande, "new beat" y "drop!" saltando en cada golpe |
| 12–19 | Loop | Pantalla + "all sounds / by me" + miniatura |
| 20–27 | Melody/808 | Dos pantallas que se turnan cada 2 beats |
| 28–35 | Drums | Zoom stutter en cada golpe, "bum" |
| 36–39 | Cierre | "link in bio", "full beat" |

### Variantes
- **menta** (`beat_menta.mp4`): menta `(24,196,138)` y rosa `(255,122,198)`; pantalla dentro de un televisor retro; stickers daisy, sparkle, heart; letras minúsculas con borde blanco.
- **lila** (`beat_lila.mp4`): lila `(150,104,255)` y amarillo `(255,196,46)`; pantalla en ventana de escritorio con sombra fuerte; stickers star, ring, bubble; letras en mayúscula gruesas con sombra.
- Pantallas del DAW en **duotono** según brillo (con las líneas más brillantes como acento oscuro) y scanlines suaves.

## Versión glitch (video completo, 50.9 s)
Pedido: "un poco más glitchy para que vaya con la canción". Fuente: video vertical `.mov` 1080x1920 (contenido real en filas **292–1626**), BPM **150.98**, primer tiempo fuerte **0.344 s**, drop en el **compás 8** (~13 s).
- Se usa `analyze.py` (envolvente de flujo) y `glitch.py`. El **glitch sube y baja con la energía real del audio**: suave antes del drop, fuerte después.
- Efectos: desplazamiento por franjas, bloques copiados (macrobloques), separación RGB, líneas de ruido, **stutter** (congelado repetido en corcheas) cada 2 compases, texto que entra revuelto 3 cuadros, cuadro invertido + flash en el drop, tiempos 2 y 4 con golpe extra (clap), crecimiento del glitch en el último tiempo antes del drop, ráfagas aleatorias, sección "glitch" que alterna colores originales y filtro menta.
- Render en **2 mitades en paralelo** y unión con ffmpeg:
```
python glitch.py <src> <env.npy> out/p1.mp4 0 764
python glitch.py <src> <env.npy> out/p2.mp4 764 1527
ffmpeg -f concat -safe 0 -i out/list.txt -i <src> -map 0:v -map 1:a -c:v copy -af "afade=t=out:st=50.5:d=0.4" -c:a aac -b:a 192k -shortest -movflags +faststart out/beat_glitch.mp4
```
- Peso: ~63 MB. Se puede ofrecer una versión más liviana.

## Cómo repetirlo con otro beat
1. Preparar el wav: `ffmpeg -i video -vn -ac 1 -ar 22050 base.wav -y`; correr `analyze.py base.wav env.npy`.
2. Ajustar el BPM y el primer golpe con `fit_beatgrid.py env.npy 148 156`; localizar el drop.
3. Editar las constantes de arriba del script (BPM, START/PH, DUR, DROP_BAR, CY0/CY1, `TAG`).
4. `--preview` / `preview` primero, mirar los cuadros, y luego renderizar.
- Cambios respecto al script original del chat: la marca ahora es `TAG = 'lagrimankv'` (antes "p4m") y los textos largos se reducen solos para no salirse del cuadro. Pruebas de los scripts hechas con un video sintético (corren sin errores).
- Si se quiere llevar este estilo a Remotion (mejor calidad, 60 fps), ver [[Pipeline visualizer Remotion]]; la lógica de tiempos es la misma.

## Cómo grabar el material para que quede mejor
- Grabar en **1920x1080 o más** (el recorte y el zoom pierden nitidez en 720p); 30 o 60 fps.
- Un clip por capa: **melody, chords, 808** (piano roll), **drums** (Channel Rack), **full** (Playlist), 10–20 s en loop. Nombrarlos así.
- Zoom dentro de FL: notas y clips grandes, ventana maximizada, cerrar el Browser y ventanas que sobran. Pocas cosas grandes funcionan mejor que muchas pequeñas.
- Cursor quieto, o usado a propósito (dibujando notas). Mostrar el **proceso** (poner notas, activar pasos) engancha más que una pantalla estática.
- Colores claros en clips y notas sobre el fondo oscuro de FL (mejor contraste en duotono).
- Exportar el audio de la parte catchy como WAV aparte. Sin notificaciones ni ventanas emergentes.

## Lecciones
- Las etiquetas (melody, 808, drums) son genéricas si en la grabación no se leen los nombres de pista; para nombres reales, pasarlos en el pedido.
- No pude ver el video en movimiento, solo cuadros sueltos: confirmar el ritmo con audífonos.
- Los cortes duros no definen este estilo: son **capas que entran y salen** con texto y stickers en el golpe.
