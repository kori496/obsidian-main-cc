---
tags: [programacion, indice]
actualizado: 2026-10-25
---

# Programación

Índice de notas de código. Reglas en `CLAUDE.md`.

## Proyectos y aprendizaje
- [[Descargador de YouTube con Node y yt-dlp]]: app local con Express y yt-dlp, explicada paso a paso (npm, Express, formularios, GET/POST, spawn).
- [[Descargador de redes - motores, diseño y panel]]: continuación (23 oct). Arreglos del código, 6 motores con redes por motor, botón «Ver descarga», diseño y animaciones, e integración como pestaña de [[Panel web lagrim-stats]].

- [[Alta de productos - herramienta portable para Siigo]]: herramienta HTML con base SQLite para dar de alta productos (reemplazo de CRS), con IVA/DIAN, códigos de barras propios y etiquetas BarTender, para importar a Siigo (23 oct). Pendiente: plantilla de Siigo.
- [[Prompt - seguir Alta de productos con Claude Code]]: prompt para continuar el proyecto en VS Code.
- [[Mapa Alta de productos.canvas|Mapa Alta de productos]]: canvas con cómo funciona la versión 2 (arranque, interfaz, servidor, disco, flujos y reglas) (24 oct).

- [[Navegador propio - fork de Zen Browser]]: fork de Zen (MPL-2.0) con marca propia; bloqueado porque el PC no tiene disco ni RAM para compilar Firefox (24 oct).
- [[Análisis de apps con REA]]: índice de apps analizadas con REA y Ghidra (inventario de opciones y efectos en el sistema). Primera: [[FabFilter Pro-Q 4]] (25 oct).

## Conceptos rápidos
- npm: `package.json` es la lista; `node_modules` no se sube a Git y se regenera con `npm install`.
- GET pide info sin cambiar nada; POST envía datos para que el servidor actúe. Los datos de POST van en el cuerpo.
- `express.urlencoded` es necesario para leer `req.body` en formularios.
- No fiarse de la ruta que imprime yt-dlp (`--print after_move:filepath`): con caracteres especiales en el título falla en Windows. Mejor buscar el archivo nuevo en la carpeta de descargas por fecha.
- Para abrir el Explorador con un archivo seleccionado: `explorer /select,"ruta"` (con `windowsVerbatimArguments: true` en Node).

Volver a [[Bitácora]]
