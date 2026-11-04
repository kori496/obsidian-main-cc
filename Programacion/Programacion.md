---
tags: [programacion, indice]
actualizado: 2026-11-03
---

Volver a [[Inicio]]

# 🟢 Programación

Índice de proyectos de código y aprendizaje. Reglas en `CLAUDE.md`.

## Proyectos y aprendizaje
- [[Descargador de YouTube con Node y yt-dlp]]: app local con Express y yt-dlp, explicada paso a paso (npm, Express, formularios, GET/POST, spawn).
- [[Descargador de redes - motores, diseño y panel]]: continuación (23 oct). Arreglos del código, 6 motores con redes por motor, botón «Ver descarga», diseño y animaciones, e integración como pestaña de [[Panel web lagrim-stats]].
- [[LKV EQ - plugin VST3 propio (JUCE)]]: ecualizador VST3 propio en C++/JUCE, base para añadir herramientas; compila y pasa los tests (25 oct).
- [[Idea juego de ritmo tipo ADOFAI]]: idea de juego de ritmo para celular estilo ADOFAI + modelo Geometry Dash (sets con mis beats, niveles generados desde el MIDI, mapas de la comunidad). Solo idea, plan por fases (27 oct).
- [[Navegador propio - fork de Zen Browser]]: fork de Zen (MPL-2.0) con marca propia; bloqueado porque el PC no tiene disco ni RAM para compilar Firefox (24 oct).

## En otras carpetas
- **Tienda** ([[Tienda y negocio]]): ALTA, la herramienta de alta de productos ([[ALTA - Inicio]]), y el análisis de CRS ([[CRS - cómo funciona el código]]).
- **Herramientas y IA** ([[Herramientas y IA]]): [[Análisis de apps con REA]] · [[FabFilter Pro-Q 4]].
- **Webs** ([[Webs]]): código del panel lagrim-stats en `Webs/analitica/`.

## Conceptos rápidos
- npm: `package.json` es la lista; `node_modules` no se sube a Git y se regenera con `npm install`.
- GET pide info sin cambiar nada; POST envía datos para que el servidor actúe. Los datos de POST van en el cuerpo.
- `express.urlencoded` es necesario para leer `req.body` en formularios.
- No fiarse de la ruta que imprime yt-dlp (`--print after_move:filepath`): con caracteres especiales en el título falla en Windows. Mejor buscar el archivo nuevo en la carpeta de descargas por fecha.
- Para abrir el Explorador con un archivo seleccionado: `explorer /select,"ruta"` (con `windowsVerbatimArguments: true` en Node).

Volver a [[Bitácora]]
