---
tags: [beats, remotion, plantilla]
actualizado: 2026-10-21
---

# 🧩 Plantilla: CLAUDE.md para el proyecto de Remotion

Volver a [[Videos beats]] · Pipeline en [[Pipeline visualizer Remotion]]

Copia el bloque de abajo como `CLAUDE.md` en la raíz de cada proyecto de Remotion (uno por beat). Así Claude Code en VS Code usa el vault aunque el proyecto esté en otra carpeta.

```md
# Proyecto Remotion: visualizer de beats

## Vault de Obsidian (úsalo siempre)
Ruta: C:\Users\sharo\OneDrive\Documentos\obsidian\main cc
- Al iniciar, agrega el vault con /add-dir y lee: Videos beats\Marca y textos.md, Videos beats\Estilos y formatos.md y Videos beats\Pipeline visualizer Remotion.md.
- Lee también C:\Users\sharo\OneDrive\Documentos\obsidian\main cc\CLAUDE.md y sigue sus reglas.
- Al terminar cualquier cambio o novedad útil a futuro (decisiones, parámetros de config.ts que funcionaron, errores resueltos, rutas), escríbelo como nota en el vault y añade una entrada en Bitácora.md. No esperes a que te lo pida.

## Marca
- Productor: lagrimankv. Tag en el video: "prod. lagrimankv".
- Textos en inglés, slang, sin emojis.

## Técnico
- Remotion + TypeScript, sin Python. 1080x1920, 30 fps.
- Determinismo: sin Math.random ni Date.now; todo en función del frame.
- No modificar mis archivos originales; trabajar con copias en /public/assets.
- Rutas de Windows entrecomilladas.
```
