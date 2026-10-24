---
tags: [beats, prompt, vorty, remotion, claude-code, visualizer]
actualizado: 2026-10-21
---

# 🌑 Prompt vorty oscuro: visualizer sin MIDI (Claude Code + Remotion)

Volver a [[Videos beats]] · Estilo base: [[Estilo de videos de vorty]] · Versión con MIDI: [[Prompt vorty - breakdown rosa 3D (Remotion)]] · Pipeline: [[Pipeline visualizer Remotion]]

Para cuando **no hay MIDI ni stems**: solo el beat completo (mp3/wav). Mismo look vorty (paneles 3D inclinados, letra pixelada, tarjetas por código) pero **oscuro** y con paneles que reaccionan al audio (ondas, espectro, bandas graves/medios/agudos) en lugar de piano roll.

> ⚠️ Retirado para woeklifeee (21 oct 2026): el beat es feliz y pedí algo colorido. Ver [[Prompt vorty colorido - woeklifeee (3 videos sin MIDI)]]. Esta versión oscura queda como variante para un beat oscuro.

**Antes de pegarlo, completar los [marcadores]:** nombre del beat, BPM, escala, ruta del mp3, ruta del proyecto y de salida. Si no sabes el BPM, déjalo así y el prompt lo mide.

## Prompt

```txt
Eres mi editor de video. Crea 1 video vertical para TikTok, YouTube Shorts y Reels de mi beat "[NOMBRE_BEAT]", en estilo "vorty oscuro": paneles flotantes 3D con letra pixelada, pero con estética oscura, y un visualizer que reacciona al audio. No tengo archivos MIDI ni stems, solo el beat completo, así que NO dibujes piano rolls ni uses capturas de FL Studio. Hazlo en Remotion (React + TypeScript), sin Python. Trabaja de forma autónoma: pregúntame solo si falta un archivo. Anota tus decisiones en DECISIONS.md.

## Reglas generales
- Antes de empezar, agrega el vault con /add-dir "C:\Users\sharo\OneDrive\Documentos\obsidian\main cc" y lee su CLAUDE.md, Videos beats\Estilo de videos de vorty.md y Videos beats\Marca y textos.md. Al terminar, deja una nota en el vault con lo que funcionó y lo que no, y una entrada en Bitácora.md.
- No modifiques ni muevas mis archivos originales: copia lo que necesites a public/.
- Windows: rutas entre comillas y path.join. Necesitas Node 18 o más nuevo y ffmpeg; si faltan, instálalos con winget. ffmpeg solo para inspeccionar y para preparar el audio.
- Proyecto en: [RUTA_PROYECTO]. TypeScript. Composición principal "VortyDark": 1080x1920, 60 fps, duración exacta en fotogramas calculada desde los compases. Añade también "VortyDarkDebug" (la misma con la rejilla de tiempos y compases dibujada encima).

## Archivos de entrada
- Beat completo: "[RUTA_MP3]". Confirma con ffprobe la duración y que no tenga silencio al inicio.
- Datos del beat: BPM [BPM o "medirlo"], 4/4, escala [ESCALA]. 1 tiempo = 60/BPM s; 1 compás = 240/BPM s (calcula con 6 decimales y también en fotogramas a 60 fps).
- Análisis del audio (script de Node/TS, npm run analyze → public/analysis.json), todo convertido a frames:
  - BPM y rejilla: detecta el desfase del primer golpe (flujo espectral) y confirma dónde cae el compás 1. Cuidado con medir la mitad o el doble del tempo; elige el que cuadre con los kicks.
  - Onsets por banda: graves (<150 Hz), medios (150 Hz a 4 kHz) y agudos (>4 kHz).
  - Energía (RMS) por bloques de 4 compases, para ubicar las partes más movidas y los breaks.
- Elige la sección a mostrar: [COMPÁS_INICIO, ej. 17] o, si lo dejo vacío, la ventana de 13 compases más movida que empiece en un compás 1, 5, 9, 13... Anótalo en DECISIONS.md.

## Estética: oscuro (todo sale de config.ts, objeto `palette`, nada de colores dentro de los componentes)
- Fondo: degradado casi negro, #07060b arriba a #1a0f26 abajo, con viñeta suave y grano muy ligero.
- Acento principal: magenta profundo #e0145f (con glow suave). Acento 2: violeta #7a2cff. Acento 3 para subtítulos: lavanda apagada #b79cff. Texto: #f4eaf6.
- Si algún color no llega a contraste 4.5:1 sobre su fondo, ajústalo y anótalo.
- Paneles: vidrio oscuro (fondo #0d0a14 al 85 %, borde de 2 px en el acento con poca opacidad), flotando e inclinados en 3D (perspective, rotateX/Y/Z) con sombra y un glow del color de acento en lugar de sombra clara.
- Motivo de las tarjetas decorativas, generado por código: humo/niebla procedural lenta, partículas que estallan en cada tiempo, cuadrícula en perspectiva y estrellas. Nada de nubes pastel.
- Etiquetas en fuente pixelada de bloques (Silkscreen, Jersey 10 o Pixelify Sans, con @remotion/google-fonts). Las letras aparecen una por semicorchea con un pop.
- Textos en pantalla en inglés, tono slang, sin emojis.

## Paneles del visualizer (sin MIDI)
Todo se calcula desde el audio y el tiempo, como función pura del frame.
- LOW: panel con la onda de los graves y un círculo central que late con cada kick/808 (usa los onsets de graves).
- MID: panel con barras de espectro (visualizeAudio de @remotion/media-utils, con suavizado) para la zona media.
- HIGH: panel con partículas/chispas que saltan en los hats y en los agudos.
- FULL BEAT: panel grande con la forma de onda del mp3 completo (getAudioData, getWaveformPortion), línea de reproducción fija y marcas de compás con el número real de compás de la canción.
- Un espectro circular o de barras en una tarjeta decorativa de fondo.
- Los paneles laten en cada tiempo, entran y salen en medio tiempo con spring y hay un destello corto en cada cambio de parte.

## Estructura (13 compases, empieza en un compás 1, 5, 9... de la canción)
1. Compases 1-2: parte LOW. En el compás 1 aparece el gancho: título grande "[GANCHO, por defecto: HOW I COOKED THIS??]" en letras de bloques de los colores de la paleta, sobre el panel. Sale al empezar el compás 2.
2. Compases 3-4: parte MID.
3. Compases 5-6: parte HIGH.
4. Compases 7-8: capas que se suman (LOW + MID + HIGH juntos) con los paneles anteriores encogidos y apilados arriba.
5. Compases 9-12: FULL BEAT (el drop) con los paneles anteriores como miniaturas alrededor y un destello en cada compás.
6. Compás 13: tarjeta final "LAGRIMANKV", "FREE FOR NON PROFIT", "[BPM] BPM · [ESCALA] · TYPE BEAT". El audio se desvanece.
Fijo abajo a la izquierda: "PROD. LAGRIMANKV" y "[BPM] BPM · [ESCALA]". Es un número par de partes (4) antes del drop, así el drop entra en el primer tiempo de un bloque.

## Audio
- Arma primero el audio del video como un solo WAV de 48 kHz con ffmpeg: cortes exactos al sample en compases enteros, fundidos de 5 ms y normalización (partes ~ -16 LUFS, drop ~ -12 LUFS, pico ≤ -1 dBTP). En Remotion entra con un único <Audio>; no cortes dentro de Remotion.
- Opción FILTER_PARTS (true por defecto en config.ts): en las partes 1 a 3 aplica al mismo tramo del beat un filtro (LOW: pasabajos a ~200 Hz; MID: pasabanda 200 Hz a 3 kHz; HIGH: pasaaltos ~3 kHz) con cruces de 5 ms, y la parte 4 va sin filtrar. Es el mismo tramo de la canción, así todo armoniza. Si suena raro o sin cuerpo, ponlo en false y usa el beat sin filtrar, con el mismo visual.

## Reglas de sincronía (no negociables)
- Todo corte, entrada y salida cae en el primer tiempo de un compás, calculado con la fórmula y no a ojo.
- Función central beatClock(frame) que devuelve compás, tiempo, fase y un "kick" que decae. Todas las animaciones salen de t = frame / fps con interpolate() y spring().
- Determinista: ningún Math.random ni Date.now; usa random("semilla") o @remotion/noise.
- Modo debug: con VortyDarkDebug dibuja la rejilla; úsalo para comprobar que los golpes caen en las líneas.

## Seguridad visual y zonas seguras
- Nada importante en los 150 px de arriba, en los 300 a 480 px de abajo, ni en el borde derecho entre y = 900 y 1700.
- Gancho fuerte desde el fotograma 0 (nunca negro). Cierre limpio que pueda repetirse en bucle.
- Máximo 3 flashes por segundo, con un parámetro FLASH_INTENSITY en config.ts.

## Referencias (opcional)
Si hay videos en [RUTA_REFERENCIAS], sácales hojas de contacto con ffmpeg (1 fotograma cada 0,5 s) y anota en STYLE_BRIEF.md tamaño de paneles, inclinación, duración de entradas y salidas, y cuántas tarjetas hay a la vez. Son solo guía de estructura y movimiento: no copies fotogramas, marcas de agua, @ de otros creadores ni su pantalla final, y el color no se toma de ellas.

## Verificación
1. Con npx remotion still, saca 10 fotogramas (gancho, cada parte, el drop y la tarjeta final) y revisa texto cortado, zonas seguras y legibilidad sobre el fondo oscuro.
2. Con el modo debug, confirma que los kicks caen en la rejilla (desfase menor a 15 ms) y que cada cambio de parte está en un primer tiempo.
3. Mide loudness y pico del mp4 final con ffmpeg.
4. ffprobe: 1080x1920, 60 fps, duración esperada, pista de audio. blackdetect sin negros.

## Entrega
- Render: H.264, yuv420p, CRF 16, AAC 320 kbps → [RUTA_SALIDA]\lagrimankv_[nombre-beat]_vorty_oscuro.mp4.
- Deja README.md para volver a renderizar y config.ts con todos los parámetros (paleta, FILTER_PARTS, FLASH_INTENSITY, compás de inicio, gancho).
- Resumen final: tabla con compases de la canción usados, partes, duración y decisiones, y cómo abrir Remotion Studio.
```

## Qué cambia respecto a la versión con MIDI
- Piano roll → paneles reactivos por banda (LOW / MID / HIGH) y onda del beat completo.
- Paleta clara/rosa → oscura (magenta profundo + violeta sobre casi negro).
- Sin stems: las "partes" son el mismo tramo del beat, opcionalmente filtrado por banda (`FILTER_PARTS`).
- Pendiente: ejecutarlo con un beat real y anotar aquí qué funcionó.
