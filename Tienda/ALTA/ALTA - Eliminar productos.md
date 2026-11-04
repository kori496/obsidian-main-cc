---
tags: [programacion, alta, eliminar]
actualizado: 2026-10-28
---

Volver a [[ALTA - Inicio]] · mapa: [[ALTA - mapa completo.canvas|Mapa de ALTA]] · registro en [[Bitácora]]

# Eliminar productos

- **Eliminar** (por fila o varios con la barra azul) borra el producto **solo de Alta**. Su código de barras queda reservado para no repetirlo.
- **No borra nada en CRS.** Alta nunca borra en CRS.
- Si el producto **ya estaba en CRS**, la próxima vez que se abra Alta, [[ALTA - Actualizar desde CRS]] lo **vuelve a traer** (manda CRS).
- Si **no se había subido**, desaparece del todo.

## Quitar un producto de verdad (de CRS y las cajas)
1. En CRS: Inventario → Productos → poner el producto como **Inhabilitado** (mejor que borrarlo, puede tener ventas o inventario).
2. En Alta: **Sincronizar cajas** para que las otras sedes reciban el cambio.

Pendiente propuesto: que Alta avise al eliminar un producto que ya está en CRS, o que pueda inhabilitarlo en CRS.
