---
tags: [vya, video, receta]
actualizado: 2026-11-03
---

# 🎬 Video de stories (receta)

Volver a [[Edición de imágenes]] · Grabación: [[Guía de grabación]] · Estilo: [[Referencias de stories de otras tiendas]] · [[Preferencias de estilo]]

Receta para editar un video vertical de V.YA a partir de los clips crudos de una sesión. Primera vez: 29 oct 2026 (`Documents\IA SOURCE IMAGES\editados_29oct\VYA_video_29oct.mp4`).

## Estilo
- 9:16, 1080×1920, 30 fps, 25–30 s.
- Planos reales de **2,5 s** (último de 3 s), **cortes secos**, sin transiciones con efectos. Solo fundido de 0,25 s al inicio y 0,6 s al final.
- **El plano más llamativo primero** (29 oct: la modelo de cuerpo entero con el conjunto rojo).
- Alternar modelo en el probador (cuerpo entero / detalle) con planos de tienda (arcos, maniquíes, vitrina) para dar aire. Cerrar con la vitrina.
- Clips de tienda grabados a 60 fps → a **0,75×** (cámara lenta suave).
- Color: cálido-neutro suave, igual para todos los clips (`eq=contrast=1.04:saturation=1.03:brightness=0.01` + `colorbalance=rs=0.015:bs=-0.015:rm=0.01:bm=-0.01`).
- **Logo chico abajo al centro** (`logo_mask.png` a 190 px, blanco al 80 %, y=1735). Sin texto: el texto y la música se agregan en Instagram/TikTok.
- Audio: pista muda. Los cortes cada 2,5 s caen al compás con música de **96 BPM** (1 compás = 2,5 s).
- No usar clips con texto quemado (p. ej. `IMG_1591.MOV`, "jeans clásicos…").

## Orden del 29 oct
IMG_1597 (rojo) → 173432 arcos → IMG_1569 detalle bustier → IMG_1577 corset denim → 171434 maniquí rayas → IMG_1598 blanco botones → IMG_1600 chaleco negro → IMG_1601 volantes (espalda) → IMG_1603 vinotinto → IMG_1602 vestido blanco → 174011 vitrina.

## Proceso (ffmpeg)
1. `ffprobe` de cada clip (los `.mp4` del Samsung vienen 1920×1080 con rotación −90: ffmpeg los gira solo).
2. Cortar cada plano con `-ss inicio -t duración`, `scale+crop` a 1080×1920, `fps=30`, el filtro de color y `-an`.
3. `concat` de los planos → `overlay` del logo + fundidos + pista muda (`anullsrc`).
4. Exportar con `-crf 22 -maxrate 7M`: queda en ~21 MB (el límite para copiar al PC desde la sesión es 30 MB por archivo).

## Errores y notas
- En un bucle `while read` de bash, ffmpeg se come la entrada: usar siempre `-nostdin`.
- Exportado a `-crf 18` pesó 37 MB y no se pudo copiar al PC (límite 30 MB).

## Variantes (31 oct)
Hechas con `Scripts/videos_31oct.py`, todas 1080×1920, 30 fps, pista muda, logo chico, 8–20 MB:
- **Lookbook a ritmo** (20 s): 16 planos de cuerpo entero de **1,25 s** (medio compás a 96 BPM), dos pasadas por los 9 looks.
- **Recorrido de tienda** (25 s): solo planos de tienda a 0,75×, empieza en los arcos y cierra en la vitrina.
- **Detalles** (20 s): primeros planos (botones, hombro, cinturón, cierre, broche, espalda, volantes, escote), algunos con zoom 1,1×.
- **Díptico frente/espalda** (18 s): dos tomas del mismo look a la vez (524×932 c/u) sobre fondo crema `#EFE9E1`, logo oscuro debajo; 6 looks × 3 s.
- **Jeans** (25 s): modelo con jean alternado con jeans en gancho y maniquí (va con el enfoque de venta).

## Errores y notas (31 oct)
- Ojo con la duración del clip: un plano que pasa del final sale **negro** (pasó con IMG_1598 a 13 s + 3 s; el clip dura 14,6 s).
- `20261029_171329` al final tiene una persona entrando a cuadro: usar solo los primeros 8 s.

## Variantes (3 nov)
Hechas con `Scripts/videos_03nov.py` (`python3 videos_03nov.py 2` rehace solo uno), en `Documents\vya contenido\ia`:
- **Nueva colección** (25 s): solo los clips de tienda del 3 nov a 0,75×, cada plano con **acercamiento lento** de 7 % (`scale` con `eval=frame` + `crop` fijo; ojo: el `w/h` de `crop` no se evalúa por fotograma).
- **Ventana en arco** (20 s): los looks dentro de un arco 820×1340 (`alphamerge` con máscara PNG) sobre crema, línea fina color arena alrededor, logo oscuro debajo. Repite la forma de los arcos de la tienda.
- **Tríptico en movimiento** (14 s): tres looks a la vez en columnas 316×1420 a distinta altura; cambia de trío cada 3,5 s.
- ❌ **Fotos en movimiento** (18 s) — **NO le gustó, no repetir este formato**: 14 fotos del 19 oct a sangre, 1,25 s cada una con acercamiento de 6 %. Logo **arriba** (abajo tapaba los pies).
- **Denim 4:5** (23 s): ventana 1080×1350 con bandas crema arriba y abajo, logo oscuro en la banda inferior; modelo con jean + jeans en maniquí/gancho.

## Errores y notas (3 nov)
- Nombres temporales: no usar `v3_{i}{j}` y `v3_{i:02d}` a la vez (chocan en `v3_00` y ffmpeg falla con "same as Input").
- Clips `20261103_*` del Samsung: 1920×1080 rotados −90, 59,94/60 fps, 10–17 s.
