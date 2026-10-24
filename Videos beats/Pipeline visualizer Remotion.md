---
tags: [beats, remotion, claude-code, visualizer]
---

# 🛠️ Pipeline visualizer Remotion

Volver a [[Videos beats]] · Prompt completo: [Notion](https://app.notion.com/p/3ffd722a78338117b977fe50e66c71fe)

Los visualizers los hace **Claude Code con Remotion** (React + TypeScript) en el PC, no Claude en el chat, porque me gusta más cómo quedan. El prompt de Cuerda sirve de plantilla para los demás beats: se cambian el nombre del beat, el audio y las carpetas.

## Antes de ejecutar
- [x] Carpeta `marketing` de OneDrive disponible en el PC ("Mantener siempre en este dispositivo")
- [x] Ruta de `Cuerda.mp3` confirmada (si no, el prompt la busca)
- [x] Node instalado
- Abrir Claude Code en una carpeta vacía y pegar el prompt

## Las 8 etapas del prompt
0. **Reglas generales**: trabaja solo y anota sus decisiones en `DECISIONS.md`; nunca toca mis originales; todo en Node/TS, **sin Python**; ffmpeg solo para inspeccionar; rutas de Windows entrecomilladas.
1. **Entradas**: material en crudo (`OneDrive\Documentos\marketing`), 5 referencias (`Downloads\visualizers referencias...`) y el audio.
2. **Analizar referencias** → `STYLE_BRIEF.md`: paleta en hex, tipos de distorsión, ritmo de cortes, visualización de audio, texto y estructura (gancho, build-up, drop, cierre). Inspirarse sin copiar.
3. **Inventario del material** → `public/assets.json` con etiquetas; descarta clips cortos, borrosos o con marca de agua.
4. **Analizar el audio** (Node) → `public/cuerda-analysis.json`: BPM, cuadrícula de pulsos, onsets por graves, medios y agudos, energía y secciones, **todo en frames**. Incluye un modo debug con la cuadrícula dibujada encima.
5. **Construcción**: 1080×1920 a 30 fps; **determinismo** (nada de `Math.random`); clips que cambian en los pulsos; distorsión reactiva (RGB, franjas, scanlines, ruido, pixelado, stutter, zoom y shake, flashes, CRT, grano); arco de intensidad; título "CUERDA" + "prod. lagrimankv"; zonas seguras de TikTok; máximo 3 flashes por segundo; componentes separados + `config.ts`.
6. **Revisión de calidad**: fotogramas en momentos clave, sincronía con el modo debug, render de prueba, corregir y repetir.
7. **Render final**: H.264, CRF 16–18, bt709, AAC 320k → `out/cuerda_visualizer.mp4` + `out/cuerda_clip.mp4` (20–30 s). Verifica con ffprobe, copia a `vidal` si está sincronizada y deja un `README.md` para volver a renderizar.

## Para reutilizarlo con otro beat
- Cambiar "Cuerda" y el nombre del mp3.
- Si cambia el estilo (p. ej. lowpoly), reescribir la sección de distorsión y la de referencias.
- Ajustar sin rehacer nada desde `config.ts`: paleta, intensidades, sensibilidad al audio, duración de cortes y `FLASH_INTENSITY`.
