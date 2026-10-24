---
tags: [skills, claude, herramientas, reglas]
actualizado: 2026-10-21
---

# 🧩 Skills

Manual de los skills de Claude: **cómo funciona** cada uno, **qué debe hacer** y **cómo debe comportarse** en situaciones que ya pasaron.

**Proyectos:** [[Edición de imágenes]] · [[Videos beats]]

Leyenda: 🖼️ Edición de imágenes · 🎧 Videos beats · 🌐 general · ⚠️ situación que ya pasó

---

## 0. Reglas generales (aplican a todos los skills)

| Situación ya vivida | Cómo comportarse |
| --- | --- |
| ⚠️ Pido instalar algo con `pip`, `curl` o un repo de GitHub y el espacio de Claude lo bloquea (rembg, Real-ESRGAN, Composio dieron 403) | No reintentar por otra vía. Decir que está bloqueado y dar dos caminos: instalarlo yo en el PC con los comandos exactos, o usar un conector alternativo (p. ej. Adobe) |
| ⚠️ Un plugin o repo es de **Claude Code** (CPR, Ponytail, comandos `/plugin`) | Aclarar que no se instala en el chat y darme los comandos para Claude Code en el PC |
| ⚠️ Pido algo de mi PC y no hay terminal en él (sin `device_bash`) | Escribir los archivos en la nube y copiarlos al PC con commit. No decir que no se puede |
| ⚠️ Algo está en una ruta de OneDrive | Avisar que puede estar "solo en la nube" y que lo deje disponible en el dispositivo |
| ⚠️ Un servicio corre en `localhost` (Obsidian Local REST API, OmniRoute) | Claude no lo alcanza desde la nube. Ofrecer conectar la carpeta o un MCP local |
| ⚠️ Comandos en PowerShell | Usar `curl.exe` y no `curl`. Si `npx` falla por la política de ejecución → `npx.cmd` o `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| ⚠️ Trabajo en otro computador | Los archivos del otro PC no se ven desde aquí: usar Drive o pedirme que los copie |
| ⚠️ Pido el contenido de un proyecto de Claude desde otro chat | Los chats de un proyecto no se leen desde fuera. Usar la memoria y Notion, y avisar qué faltó |
| Tareas largas o de varios pasos | Empezar directo, preguntar solo si una mala suposición cuesta mucho, y terminar con un resumen corto |
| Idioma | Hablarme en español. Los textos para beats van en inglés ([[Marca y textos]]) |

---

## 1. Skills de la cuenta (Claude en la app)

### 📄 Documentos y archivos

#### docs
- **Cómo funciona:** crea documentos vivos en Claude Docs que se pueden comentar y exportar a Word, PDF o Google Docs.
- **Qué debe hacer:** usarlo por defecto cuando pido "un documento" sin decir el formato. Primero crea el esqueleto y después llena cada sección.
- **Comportamiento:** si el documento es para Notion u Obsidian, usar esa herramienta en su lugar.

#### docx · pptx · xlsx · pdf
- **Cómo funcionan:** generan o editan archivos de Office o PDF con scripts.
- **Qué deben hacer:** usarse solo cuando pido el formato por nombre o adjunto un archivo de ese tipo. Un archivo que me pasan se edita en su mismo formato.
- **Comportamiento:** 🎧 para el seguimiento de métricas basta una tabla en [[Métricas y revisiones]] o en Sheets; xlsx solo si pido Excel.

#### pdf-reading · file-reading
- **Cómo funcionan:** leen el archivo de la forma correcta según su tipo (texto, escaneado, tablas, imágenes).
- **Qué deben hacer:** intentarlo siempre antes de decir que no se puede leer un archivo.
- **Comportamiento:** ⚠️ el conector de Drive **no lee .mp4 ni GIF**. Para ver un video hay que descargarlo (con mi permiso) o que yo lo adjunte.

#### google-workspace
- **Cómo funciona:** crea o edita Google Docs, Sheets y Slides en mi Drive.
- **Qué debe hacer:** usarse solo si digo "Google Doc", "Sheet" o "Drive".
- **Comportamiento:**
  - ⚠️ Al buscar carpetas en Drive, filtrar por `mimeType = 'application/vnd.google-apps.folder'` y listar con `parentId`.
  - ⚠️ La carpeta `edición ` tiene un **espacio al final**.
  - ⚠️ "videos beats" no tiene subcarpetas.
  - Si no encuentra algo, decir qué sí hay y ofrecer abrirlo en Chrome.

### 🎨 Diseño y visual

#### taste
- **Cómo funciona:** aplica criterio del oficio para hacer o criticar trabajo (código, documentos, UI, gráficos, planes) y detecta lo que se ve "generado".
- **Qué debe hacer:** usarse cuando pido "que quede bien", con entregas importantes o con instrucciones escasas.
- **Comportamiento:**
  - 🖼️ Juzgar contra [[Preferencias de estilo]]: elegante, coherente, solo el logo, **sin glitch, humo ni paletas de colores**.
  - 🎧 En los visualizers, lo contrario: mientras más distorsionado y "core", mejor.

#### frontend-design · editorial-design-system
- **Cómo funcionan:** dan una dirección estética intencional. Editorial = fondo marfil y casi negro, estilo revista.
- **Qué deben hacer:** usarse para piezas, páginas o plantillas visuales.
- **Comportamiento:** 🖼️ en V.YA, colores neutros y elegantes, nada extravagante. Variar el formato entre lotes.

#### design:design-critique · design-system · design-handoff · accessibility-review · ux-copy · user-research · research-synthesis
- **Cómo funcionan:** son flujos de diseño: crítica estructurada, auditar un sistema de diseño, especificaciones para desarrollo, accesibilidad WCAG, textos de interfaz, planear investigación y sintetizar resultados.
- **Qué deben hacer:** usarse cuando los pido por nombre o comparto un diseño para revisar.
- **Comportamiento:** 🖼️ la crítica de un lote revisa coherencia entre piezas, legibilidad del logo y respeto a las preferencias. No proponer agregar texto, porque el texto lo pongo en Instagram.

#### web-design-guidelines
- **Cómo funciona:** revisa código de UI contra buenas prácticas de interfaz.
- **Qué debe hacer:** usarse cuando pido "revisa mi UI" o "audita el diseño".

#### dataviz
- **Cómo funciona:** método para hacer gráficos coherentes y accesibles, en modo claro y oscuro.
- **Qué debe hacer:** leerse antes de hacer cualquier gráfico.
- **Comportamiento:** 🎧 graficar vistas, retención y suscriptores por tanda o estilo, para ver qué formato gana.

#### artifact-design · artifact-diagramming · artifact-capabilities
- **Cómo funcionan:** reglas para páginas publicadas (artifacts): diseño, diagramas y funciones como datos en vivo o estado compartido.
- **Qué deben hacer:** usarse cuando el resultado es una página que voy a volver a abrir o compartir.

### ✍️ Escritura e investigación

#### de-ai-writing
- **Cómo funciona:** reescribe un texto para quitar las marcas de IA (exceso de rayas, "no solo X, sino Y", palabras infladas).
- **Qué debe hacer:** limpiar un texto antes de publicarlo.
- **Comportamiento:** 🎧 los títulos y descripciones de beats van en **inglés, slang y sin emojis**. Mantener el tono urbano y no "corregirlo" a formal.

#### deep-research
- **Cómo funciona:** coordina varias búsquedas y escribe un informe con fuentes.
- **Qué debe hacer:** usarse para comparar opciones, mercados o tendencias.
- **Comportamiento:** ⚠️ **Reddit está bloqueado** tanto en Chrome como en el navegador de la app. Pedirme que copie la información o buscar otra fuente. Para precios en Colombia funcionó Facebook Marketplace con URLs por ciudad.

### 🌐 Navegador y computador

#### claude-in-chrome / chrome-browser
- **Cómo funciona:** controla mi Chrome real, con mis sesiones iniciadas.
- **Qué debe hacer:** usarse para subir videos, revisar redes, Marketplace o Drive tal como yo lo veo.
- **Comportamiento:**
  - ⚠️ Solo funciona en **Chrome**, no en Edge ni en Zen.
  - Nunca hacer clic en "publicar" sin mi confirmación, no escribir contraseñas y no resolver captchas.
  - Instagram y TikTok fallan más que YouTube desde la web.
  - ⚠️ En Facebook, un grupo solo se puede leer si soy miembro.

#### built-in-browser
- **Cómo funciona:** es el panel de navegador dentro de la app de escritorio, con sus propias sesiones.
- **Qué debe hacer:** usarse si pido "tu navegador" o si Chrome no está disponible.

#### computer-use
- **Cómo funciona:** toma capturas y controla el mouse y el teclado de mi PC.
- **Qué debe hacer:** usarse con apps de escritorio (FL Studio, Explorador). No sirve para sitios web.
- **Comportamiento:** es lento y puede equivocarse, así que confirmar antes de cualquier acción que no se pueda deshacer.

### 💻 Programación y plugins

#### tdd
- **Cómo funciona:** ciclo de prueba que falla → código → refactor.
- **Qué debe hacer:** usarse si pido "test-first" o "red-green-refactor".

#### plugin-authoring
- **Cómo funciona:** crea mods de la interfaz de Claude (paneles, comandos, hooks).

#### skill-creator
- **Cómo funciona:** crea, mejora y evalúa skills.
- **Comportamiento:**
  - ⚠️ Los nombres no pueden contener "claude": por eso "claude" pasó a llamarse **editorial-design-system**.
  - ⚠️ Los skills que traen scripts, carpetas de referencias o agentes (graphify, humanizer, impeccable, shadcn, taste-image-to-code) no se pueden subir a la cuenta tal cual. Ofrecer una versión condensada o instalarlos en Claude Code.
  - Los archivos de referencia se integran dentro del SKILL.md.

#### cowork-plugin · cowork-plugin-management
- **Cómo funcionan:** crean o personalizan plugins para una organización.

### 🎧 Videos beats

#### prompt-video-beats
- **Cómo funciona:** revisa los archivos de un beat (audio, stems, MIDI, clips, referencias) y escribe un prompt listo para Claude Code + Remotion que haga videos verticales del beat (breakdown, visualizer u otro estilo).
- **Qué debe hacer:** usarse siempre que pida un prompt para un video, visualizer o short de un beat.
- **Comportamiento:** en el chat solo se escribe el prompt; el video lo hace Claude Code + Remotion. Seguir las reglas de [[Videos beats]] (sección 3) (sin Python, Node/TS, detalle profesional, textos en inglés).

#### beat-visualizer
- **Cómo funciona:** pipeline probado en Remotion para hacer un visualizer vertical 1080x1920 (glitch / VHS / CCTV) con cortes al ritmo del beat.
- **Qué debe hacer:** usarse cuando pida un visualizer o video de un beat con mis clips.

```yaml
name: beat-visualizer
description: Build a vertical 1080x1920 music visualizer in Remotion (React/TS) for TikTok/Reels/Shorts from an audio file plus the user's own video clips and GIFs, in a distorted glitchcore / VHS / CCTV / analog-horror style, with cuts and effects locked to the beat. Use when the user asks for a beat or song visualizer, a "video como el de Y una angelica", or a music video for social media from an mp3 and clips.
```

##### Beat visualizer (Remotion, vertical, glitch/VHS/CCTV)

A proven pipeline from the "Y una angelica" project (`C:\Users\sharo\OneDrive\Documentos\marketing\y-una-angelica-visualizer`).

`template/` holds a full copy of that project's code; start from it rather than rewriting.

##### Workflow

1. **Environment.** Need Node ≥ 18 and ffmpeg/ffprobe. If ffmpeg is missing: `winget install Gyan.FFmpeg`. It lands in `%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_*\ffmpeg-*\bin`, so add that to PATH in each Bash call. On Windows, never run `python -` (the Store alias hangs waiting on stdin). Use `node -e` instead.

2. **Scaffold.** Run `npx create-video@latest --blank --no-tailwind --yes <dir>`. Its `npm i` fails ("--allow-scripts"), so run `npm i` yourself afterwards. Then copy `template/*` over it (`src/`, `scripts/`, `remotion.config.ts`, the `package.json` scripts and deps) and install:

   `npm i @remotion/media-utils @remotion/google-fonts @remotion/gif @remotion/noise mpg123-decoder` and `npm i -D tsx @remotion/bundler @remotion/renderer`. Pin every `@remotion/*` package to the same version as `remotion`.

3. **Assets.** Copy media into `public/assets` with short ASCII names. Never touch the originals. Run ffprobe on each file (size, fps, duration, audio), `cropdetect` to find black bars, and a 1 fps contact sheet (`fps=1,scale=200:-2,tile=6x5`). Note that `drawtext` segfaults on this ffmpeg build because fontconfig is missing. Write `public/assets.json`: id, file, type clip/overlay, media video/gif, w/h, fps, duration, `crop`, `good` ranges (skip weak shots and legible text), tags, `background`, and for flashy GIFs `brightWindowsSec` measured with `signalstats` YAVG.

4. **References** (if given). Contact sheets, scene cuts (`select='gt(scene,0.3)',showinfo`), and palettes (`palettegen` to 8 colors). Write `STYLE_BRIEF.md` with concrete numbers. Check for duplicate files with md5.

5. **Audio.** Set `AUDIO_FILE`, `TITLE`, `TAG` and `PALETTE` in `src/config.ts`, then run `npm run analyze`. Read its log: BPM, half-time flag, downbeat slot and sections. Sanity-check the downbeat against the strongest onset (the drop entrance should land on a downbeat). Then run `npm run check`.

6. **Adapt the clip lists.** In `src/data.ts` edit `POOL` (which clips each section may use), the first-shot hook clip (`k === 0 ? "..."`), and the GIF events (explosion, glitch sticker, VHS stripes, textures). In `src/Overlays.tsx` edit the `Hud` cam list.

7. **Stills.** `npm run stills -- Full 0 <firstBeat> <midBuild> <dropStart> <calm> <lastFrames>`. Montage them with ffmpeg `hstack` and look. To check sync, set `DEBUG = true` and render stills at a cut frame and the frame before it.

8. **Test render** at `--scale=0.5 --x264-preset=veryfast`, then `npm run qa -- out/x.mp4 <offset>`. Pass criteria: max 3 flashes/s, 0 unexplained 1-frame spikes, no blackdetect, correct frame count. Fix, then re-render only the failing range (`--frames=a-b`, qa offset = a).

9. **Final.** `npm run render:clip`, then `npm run render:full` (h264 yuv420p, CRF 17, slow, bt709, AAC 320k, `--enforce-audio-track`, `--gl=angle`, concurrency 2). Check the results with `npm run qa` and ffprobe.

##### Lessons that cost time (do not repeat)

- **Use `--gl=angle`.** The default software GL took ~6.5 s/frame on the Intel laptop; angle takes ~1 s/frame with an identical image. Expect a full 2-minute video to take ~70 min and a 45 s clip ~25 min. Tell the user the estimate up front. Concurrency 3 was not faster (GPU-bound). Set it in `remotion.config.ts` (`Config.setChromiumOpenGlRenderer("angle")`).

- **Port 3000** may be taken by another Remotion Studio ("not a valid Remotion project / foreign page"). Use `Config.setPort(3417)` and pass `port` in renderer API calls.

- **Batch stills.** `npx remotion still` re-bundles every time (~36 s). `scripts/stills.ts` bundles once (~15-20 s per still).

- **Media time math.** `OffthreadVideo` shows source time `(trimBefore + frame*playbackRate)/fps`. For GIFs, emulate trimBefore with `<Sequence from={-trimBefore/rate}>`.

- **Displacement maps from `feFlood` bands** (synchronous). Avoid `feImage` with data URIs: async loading risks flicker in renders.

- **Overscan.** Put the filtered layer 64 px larger on each side so displacement, RGB offsets and shake never reveal an edge.

- **Flashes.** Cuts between clips of different brightness count as flashes too. Schedule at most `MAX-1` per second, put any bright GIF (VHS stripes, explosion) in the limiter, and keep white flashes at 0.55 or less opacity with a 4-frame decay.

- **Title glitch.** Slice the letters themselves into strips that shift sideways. Stacking duplicate text copies made it unreadable. Keep frame 0 unsliced (it is the thumbnail). Hook = an RGB/slice burst at frame 0, not a white flash (that washed the thumbnail out).

- **Grade.** A gradient map over luminance (feColorMatrix → feComponentTransfer table) mixed with the source, with contrast folded into a single `feComposite arithmetic` (k2 = d·c, k3 = (1−d)·c, k4 = (1−c)/2).

- **Half-time beats.** Autocorrelation prefers the half tempo by coherence. Keep the tempo inside 70-160 and get the downbeat from the dominant snare slot − 2.

- **Endings.** Fade to ~85 % of the palette black, not pure black, so blackdetect stays clean and the loop back to frame 0 is soft.

- **Determinism.** Everything comes from `random(SEED|key)` and the frame number. No `Math.random`, `Date` or mutable state.

##### Deliverables checklist

`STYLE_BRIEF.md`, `DECISIONS.md`, `README.md` (analyze / studio / render commands plus config knobs), `public/assets.json`, `public/analysis.json`, `out/<name>_visualizer.mp4`, `out/<name>_clip.mp4`. Write the docs in the user's language (Spanish for this user).

### ⚙️ Cuenta y utilidades

| Skill | Cómo funciona / qué debe hacer |
| --- | --- |
| setup-claude | Configuración guiada por rol |
| import-memory | Importar memoria de otro asistente, tratándola como datos |
| morning | Resumen de la mañana; solo si lo pido |
| explain-usage | Explicar en qué se gastaron los tokens, con un gráfico |
| product-self-knowledge | Consultar antes de dar datos de productos de Anthropic. ⚠️ El plan Pro **no** sirve para extensiones de terceros, porque necesitan una API key aparte |

### 🔎 prompts.chat

| Skill | Cómo funciona / qué debe hacer |
| --- | --- |
| prompts / prompt-lookup | Busca plantillas de prompts. 🎧 Útil para mejorar el prompt de [[Pipeline visualizer Remotion]] |
| skills / skill-lookup | Busca e instala skills del registro |

---

## 2. Skills locales de Claude Code

Están en `C:\Users\sharo\.claude\skills` (carpeta oculta).

**Comportamiento ante situaciones ya vividas:**
- ⚠️ "Agregar carpeta" falla con `.claude` por permisos. Comprimirla con `Compress-Archive -Path $HOME\.claude\skills\* -DestinationPath $HOME\Desktop\skills.zip`.
- ⚠️ `Compress-Archive` no muestra nada cuando funciona: verificar con `dir`.
- ⚠️ Si el Escritorio está en OneDrive, el zip queda en `OneDrive\Desktop`.
- Para instalar en otro PC → `instalar-skills.bat`. Revisa Claude Code, Node y Python, pero no los instala.

| Skill | Cómo funciona / qué debe hacer | Proyecto |
| --- | --- | --- |
| graphify | Genera grafos y mapas de conocimiento. Puede necesitar Python. Sirve para mapear esta bóveda | 🌐 |
| taste | Igual que el de la cuenta | 🖼️ 🎧 |
| taste-image-to-code | Convierte una imagen de referencia en código o diseño | 🖼️ |
| impeccable | Pule detalles de UI | 🌐 |
| shadcn | Componentes shadcn/ui. Mejor instalarlo con su CLI | 🌐 |
| humanizer | Hace que el texto suene humano. 🎧 Respetar el slang en inglés | 🎧 |
| de-ai-writing | Versión local, con un script de escaneo | 🎧 |
| tdd · web-design-guidelines | Igual que en la cuenta | 🌐 |
| claude / synced | Sin confirmar: revisar si tienen SKILL.md. "synced" son copias de skills de la cuenta | — |

---

## 3. Comportamiento por proyecto

### 🖼️ [[Edición de imágenes]]
- Todo el trabajo de fotos de V.YA va en el **chat del proyecto de ediciones de stories**.
- Salida **1080×1920**, con varias fotos en crudo por pieza ([[Material y carpetas]]).
- Piezas limpias, solo con el logo. Sin glitch, humo, manchas de pincel, paletas ni estilo antiguo ([[Preferencias de estilo]]).
- Si pido algo "experimental", hacer lo más normal posible, p. ej. collage de tiras de fotos.
- Para quitar fondos o subir resolución, ver [[Herramientas]]. ⚠️ rembg y Real-ESRGAN no se instalan en la nube.

### 🎧 [[Videos beats]]
- Los cortes y efectos **siempre caen al ritmo del beat**.
- Los visualizers de calidad los hace **Claude Code + Remotion**, no el chat. En el chat solo se escribe el prompt.
- ⚠️ En el prompt de Remotion: **sin Python**, todo en Node/TS, y nivel de detalle profesional (determinismo, CRF, bt709, modo debug).
- Al editar en el chat: ⚠️ librosa no se instala, así que el BPM sale con numpy/scipy (flujo + autocorrelación). Hay fuentes disponibles (Poppins, Noto CJK).
- Material de video en **video, no GIFs**; buscar con los términos de [[Material beats]].
- Textos en inglés, slang y sin emojis ([[Marca y textos]]).
- Estilo de los visualizers: distorsionado y "core". Inspirarse en las referencias **sin copiarlas**.
- Medir y decidir según el [[Plan de funcionamiento]].
