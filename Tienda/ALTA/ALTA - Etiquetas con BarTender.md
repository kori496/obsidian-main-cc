---
tags: [programacion, alta, bartender, etiquetas]
actualizado: 2026-10-28
---

Volver a [[ALTA - Inicio]] · mapa: [[ALTA - mapa completo.canvas|Mapa de ALTA]] · registro en [[Bitácora]]

# Etiquetas con BarTender

## Configuración (panel «Configuración de BarTender» o en la pestaña Imprimir)
- `bartend.exe`: `C:\Program Files\Seagull\BarTender Suite\bartend.exe`.
- Plantilla: `plantillas\CBZebra.btw` (copia; la original no se toca).
- Impresora: se **elige siempre en el programa** (lista de instaladas + usadas). Real: **4BARCODE 4B-2054TF** (USB). Si no hay impresora elegida no imprime y avisa.
- Argumentos: `/F="{plantilla}" /D="{datos}" {impresora} /C={copias} /P /X` (`/D` y `/PRN` confirmados con esta licencia).

## Cómo imprime
1. Todas las impresiones pasan por `/api/imprimir` (pestaña Imprimir, botón Etiqueta, Etiquetas…, reimpresión, Imprimir con BarTender).
2. Escribe un CSV **por trabajo** en `datos\etiquetas\trabajos\etiquetas_<fecha>_<id>.csv` (últimos 30) y actualiza `etiquetas.csv` si puede.
3. CSV con **punto y coma**, UTF-8 con BOM, **una fila por etiqueta** (cantidad 3 = 3 filas) y BarTender con `/C=1`. Máximo 1000 etiquetas por impresión.
4. Ejecuta bartend.exe y anota comando y resultado en `registro.log` (una impresión real tarda 5–13 s).

## Columnas del CSV
`referencia, nombre, codigo_barras, precio_detal, grupo, impuesto` (viejas) + `referencia_descripcion` (texto de arriba), `codigo_interno` (= código de barras, texto de abajo), `precio_detal_txt` (precio grande sin puntos: 140900), `precio_mayor`, `precio_mayor_sin_ceros` (107900 → 1079), `precio_mayor_codigo` (**2*1079VY**).

Etiqueta V.YA: `Jean VFk11017` / código de barras / `007754` / `2*1079VY` / `$140900`. Rollo de 3 etiquetas a lo ancho, 3 mm de separación.

## Pestaña IMPRIMIR (`imprimir.html`)
- Botón verde **Imprimir** arriba → abre la pestaña.
- **Productos de esta sesión** (guardados desde que se abrió el programa): marcar, cantidad y precio en etiqueta (cambiarlo solo cambia la etiqueta, la fila se pone amarilla). Los no impresos vienen marcados. Confirma con resumen.
- **Historial de la sesión**: hora, referencia, nombre, precio, cantidad, desde dónde, resultado; **Reimprimir**. Se borra al cerrar el programa.
- **Ctrl+F7**: reinicia la sesión (lista e historial).
- **Log permanente** `datos\impresiones.log`: `fecha | IMPRESO/ERROR | ref | nombre | barras | $precio | N etiquetas | impresora | desde`. Botón «Ver log de impresiones».

## Problemas conocidos
- Dice «IMPRESO» pero no sale nada → BarTender abierto o `bartend.exe` ocultos: cerrarlos (Administrador de tareas → Detalles).
- `EPERM ... etiquetas.csv` → resuelto con un CSV por trabajo.
- El código de barras no sale → el objeto debe estar enlazado a `codigo_barras` (Code 128) en la conexión de texto (no la vieja de Access CB-Zebra).
