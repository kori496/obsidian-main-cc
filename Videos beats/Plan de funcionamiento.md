---
tags: [beats, plan, flujo]
---

# ⚙️ Plan de funcionamiento

Volver a [[Videos beats]]

Es un ciclo que se repite. Cada vuelta deja un aprendizaje anotado en [[Métricas y revisiones]].

```
Producir beat ─► Grabar / exportar ─► Editar video ─► Publicar ─► Medir ─► Decidir
      ▲                                                                   │
      └──────────────── repetir lo que funciona / cambiar estilo ◄────────┘
```

## 1. Producir y grabar
- Hacer el beat en FL Studio.
- **Exportar el audio limpio por separado** (mp3/wav).
- Si tengo el proyecto, grabar la pantalla siguiendo estas reglas:
  - 1080p o más.
  - **Un clip por capa**: melodía, acordes, 808, drums y playlist completa, en lugar de una sola toma larga del playlist.
  - Hacer zoom en las notas y clips dentro de FL.
  - Esconder el cursor o usarlo con intención.
  - No hace falta grabar en vertical: el reencuadre se hace al editar.
- Si **no** tengo el proyecto de FL (como con Cuerda), el video sale solo del audio + material en crudo → ruta visualizer.

## 2. Elegir formato
Según el beat y lo aprendido en las métricas (ver [[Estilos y formatos]]):
- **Make beat**: grabación de FL con marcos retro, stickers y textos al ritmo.
- **Glitch**: lo mismo, pero distorsionado, para beats más oscuros.
- **Visualizer "core"**: sin FL, con audio + clips distorsionados, hecho en Remotion.
- **Lowpoly**: el estilo de la próxima tanda de prueba.
- **Short con gancho de título**: "boombap but make it ...".

## 3. Editar
- **Rápido / prueba:** en el chat de Claude (ffmpeg + Python), le subo el video y me devuelve variantes.
- **Calidad / visualizer:** con Claude Code + Remotion en el PC, usando el prompt de Notion → [[Pipeline visualizer Remotion]].
- Reglas que siempre se cumplen:
  - **Cortes y efectos sincronizados al beat** (es mi estilo favorito).
  - Vertical 1080×1920 y respetar las zonas seguras de la interfaz de TikTok.
  - Gancho en el primer segundo y final limpio para que haga bucle.
  - Tag **prod. lagrimankv** / nombre de productor.
  - Inspirarse en referencias sin copiar logos, marcas de agua ni textos.

## 4. Publicar
- Redes: **YouTube Shorts, TikTok e Instagram Reels**; el video largo va a YouTube.
- Títulos y descripciones **en inglés, tono slang, sin emojis** → [[Marca y textos]].
- Enlazar cada Short con el video largo o con una lista de reproducción de beats.

## 5. Medir
- Fuentes: YouTube Studio + Metricool.
- Qué mirar: vistas, tiempo de reproducción y retención media, suscriptores ganados, interacciones, y qué video se lleva el tráfico.
- Cuándo: revisión fija, la primera el 21 oct. Anotar cada resultado en [[Métricas y revisiones]].

## 6. Decidir
- Se publica **una tanda de al menos 5 videos por red** con un mismo estilo.
- Si funciona → convertirlo en serie y producirlo por lotes.
- Si no funciona → **cambiar de estilo** y empezar otra tanda.
- Si un video no me convence → pasarlo a privado (como los 3 Shorts del 18/10).
- Claude analiza los números que le paso y recomienda qué descartar, repetir o variar.

## Reparto de tareas
| Yo | Claude (chat) | Claude Code |
| --- | --- | --- |
| Producir beats, grabar, conseguir material, publicar, pasar métricas | Ideas, prompts, títulos y descripciones, ediciones de prueba, análisis de métricas, planning en Notion | Visualizers en Remotion y renders finales en el PC |
