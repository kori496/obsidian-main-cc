---
tags: [programacion, alta, crs, wwwsyncro, dropbox]
actualizado: 2026-10-28
---

Volver a [[ALTA - Inicio]] · mapa: [[ALTA - mapa completo.canvas|Mapa de ALTA]] · registro en [[Bitácora]]

# Sincronizar cajas y Revisar Dropbox

## Qué es wwwSyncro (de Smart Data)
- **Subida** (principal): copia el catálogo de `BDSCRS` a `wwwProductos.mdb`, lo comprime con uharc en `VYAwwwProductos.uha`, lo copia a Dropbox y lo **sube por FTP** a Smart Data.
- **Descarga** (cajas de otras sedes): baja el .uha (por FTP), crea los productos nuevos (existencias 0), **reemplaza todos los códigos de barras** y actualiza nombre, costo, precios e IVA.
- Solo pasa el **catálogo**: no existencias, ventas ni clientes.

## Botón morado «Sincronizar cajas» (hace la subida, SIN FTP)
1. Pide confirmación (rutas). Cerrar wwwSyncro antes (también en el servidor).
2. Copia el `wwwProductos.mdb` actual a `datos\copias_wwwProductos` (últimas 10).
3. Lee BDSCRS (solo lectura) y reescribe en `wwwProductos.mdb` las tablas Categorias, CategoriasAlternas, Grupos, Ivas, Lineas, Marcas, Productos, ProductosReferencia, Secciones (todas las `www…` menos wwwData), en una transacción.
4. Pone la fecha en `wwwData` (Id 1).
5. **Compacta** el .mdb (si no, se duplica: 4,4 → 9,7 MB). Suelta la conexión y reintenta hasta 5 veces si está «en uso».
6. `uharc a -o+` → `VYAwwwProductos.uha`, siempre con el archivo adentro llamado **wwwProductos.mdb** (las cajas esperan ese nombre).
7. Copia el .uha a Dropbox (reemplaza).
8. **Comprueba**: abre el .uha de Dropbox como una caja y cuenta productos y códigos; actualiza el panel.
- Manda el **catálogo completo de CRS**, no la lista de Alta. Lo que solo está en Alta no llega hasta [[ALTA - Subir productos a CRS|subirlo]].
- Prueba con copias: 9 s, 7.785 productos, .uha de 372 KB.

## Revisar Dropbox
Descomprime el .uha de Dropbox en una carpeta temporal (sin tocarlo), lee `wwwProductos.mdb` y compara con BDSCRS: productos en el archivo, fecha de sincronización, productos en CRS, **cuántos faltan** y cuáles (lista desplegable, hasta 500). También alimenta «en cajas / falta sincronizar» en la lista. Corre solo al abrir Alta.

## Volver atrás
Copiar el `wwwProductos.mdb` guardado en `datos\copias_wwwProductos` y volver a comprimir; Dropbox también guarda versiones anteriores.

## Ojo
Las cajas bajan el archivo del **FTP de Smart Data**, no de Dropbox (según el código). Falta confirmar con una prueba real en otra sede que el producto llega. Ver [[ALTA - Pruebas, errores y pendientes]].
