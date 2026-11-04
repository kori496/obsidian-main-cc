---
tags: [programacion, alta, crs]
actualizado: 2026-10-28
---

Volver a [[ALTA - Inicio]] · mapa: [[ALTA - mapa completo.canvas|Mapa de ALTA]] · registro en [[Bitácora]]

# Conexión con CRS

Configuración → **«CRS: crear los productos también en CRS»**.

## Rutas (reales, 28 oct)
- **BDSCRS.mde**: `\\vyasas\CRS\BDSCRS.mde` (servidor; en `D:\CRS` de este PC solo hay bases locales).
- **wwwProductos.mdb**: `\\vyasas\CRS\wwwProductos.mdb` · **uharc.exe**: `\\vyasas\CRS\uharc.exe`.
- **Carpeta de Dropbox**: `D:\Dropbox\CRS-BK-2019\VYA`.
- Proveedor (Id) 1 · Marca (Id) 1 = V.YA · Categoría (Id) -1 = General. Marcas: 1 V.YA, 2 Dyaboo, 3 Beso Menta. Categorías: -1 General, 1 Jean Bota Recta, 2 Jeans Modelo, 3 Jeans Campana, 4 Blusas, 5 Short, 6 Chaleco, 7 set, 8 Body, 9 Crop Top, 10 Polo, 11 Braga, 12 Jeans.
- Casilla **«Crear en CRS cada producto que guarde»** (apagada por defecto).
- Botones: **Elegir archivo…**, **Guardar**, **Probar conexión** (muestra motor, productos en CRS, consecutivo, bodegas y si encuentra las rutas de sincronizar). 28 oct: 7.813 productos, consecutivo 7812.

## Qué modifica cada botón
| Botón | ¿Modifica BDSCRS? | ¿Otra cosa? |
|---|---|---|
| Probar conexión | No (solo lectura) | No |
| Actualizar desde CRS | No (solo lectura) | Solo la base de Alta |
| Revisar Dropbox | No (solo lectura) | No (descomprime en una carpeta temporal) |
| Sincronizar cajas | No (solo lectura) | Sí: wwwProductos.mdb y el .uha (con copia previa) |
| Subir productos / Enviar a CRS / crear al guardar | **Sí: agrega productos nuevos** | No |

`BDSCRS.mde` se abre con **Mode=Read** en todo menos al crear productos. Antes de la primera subida: **copia de BDSCRS.mde**.

## Cómo funciona por dentro
`app\crs.ps1`, PowerShell 64 bits + **Microsoft.ACE.OLEDB.16.0** (ya instalado en el PC). El SQL entre dos bases de Access no funciona («Operación no válida para este tipo de objeto»): las filas se copian una por una desde el script.

Cómo es CRS por dentro: [[CRS - cómo funciona el código]] · wwwSyncro: [[CRS - wwwSyncro y escribir productos desde Alta]].
