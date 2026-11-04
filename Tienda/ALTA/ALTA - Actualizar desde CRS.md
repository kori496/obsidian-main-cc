---
tags: [programacion, alta, crs]
actualizado: 2026-10-28
---

Volver a [[ALTA - Inicio]] · mapa: [[ALTA - mapa completo.canvas|Mapa de ALTA]] · registro en [[Bitácora]]

# Actualizar desde CRS (CRS → Alta)

**Manda CRS.** Corre **solo al abrir Alta** y con el botón **Actualizar desde CRS** (el botón muestra antes un resumen y pide confirmar).

## Qué hace
1. Lee de `BDSCRS.mde` (solo lectura) todos los productos y sus referencias.
2. **Productos nuevos** (en CRS y no en Alta) → los agrega: código = referencia = código de barras, nombre limpio de espacios, costo, detal, mayorista, IVA (19 → IVA 19 %, 5 → IVA 5 %, 0 → Excluido), grupo Confecciones, unidad Unidad, columna CRS con fecha.
3. **Productos que ya están** → si cambió nombre, costo, detal, mayorista o IVA en CRS, lo actualiza. No toca grupo, unidad ni INC. Si estaban como «IVA 19 % incluido» se respeta.
4. **Marca como subidos** los que ya existen en CRS (para que no cuenten en «Subir productos»).
5. **Reserva** los códigos de barras extra de CRS (referencias distintas del código).
6. Se salta el genérico «00 Producto». Si un código de CRS ya es el código de barras de otro producto en Alta, no lo trae y avisa.
7. Los productos que **solo están en Alta no se tocan**.

## Resumen en el panel
«Actualizado desde CRS: N productos nuevos, M con cambios…», con los primeros nuevos y cambios (ej. «007788 detal 133.900 → 139.900»). «Alta está igual a CRS» si no hay nada.

Para volver atrás: las copias de la base (`datos\copias`, la «al-abrir» se hace antes).
