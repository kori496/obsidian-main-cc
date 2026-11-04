---
tags: [programacion, alta, crs]
actualizado: 2026-10-28
---

Volver a [[ALTA - Inicio]] · mapa: [[ALTA - mapa completo.canvas|Mapa de ALTA]] · registro en [[Bitácora]]

# Subir productos a CRS

## Tres formas
1. **Subir productos (N)** (panel morado): N = productos de Alta que **no están en CRS** (columna CRS vacía). Abre la **lista** (referencia, nombre, costo, detal, mayorista) con casillas, todas marcadas → **Subir a CRS** sube las marcadas de 200 en 200. **Cancelar** cierra sin subir.
2. **Enviar a CRS** en la barra azul, para los productos seleccionados.
3. Casilla **«Crear en CRS cada producto que guarde»**: se crea al guardar.

El contador N solo es fiable después de comparar con CRS (al abrir Alta): «Actualizar desde CRS» marca como subidos todos los que ya existen en CRS. Si sale en miles, no subir y revisar.

## Qué escribe en `BDSCRS.mde` (igual que CRS)
Antes revisa que el código no exista en `Productos` ni en `ProductosReferencia`; si existe → «ya existe», no se toca. Si no, en **una transacción por producto**:
- **Productos**: CODIGO, IdCategoria, IdProveedor 1, DESCRIPCION, CodIva, Costo, PVDetal, PVMayor (o costo), PVEspecial1/2 = detal, CantidadMayor/E1/E2 = 1, Embalaje 1, IdEstado 1, Fecha_Sistema = ahora, Existencias 0, PDetal/PEspecial1/PEspecial2 = margen sobre la venta, PMayor, IdMarca 1, ObligarSeriales No.
- **ProductosReferencia**: CODIGO = REFERENCIA, HABILITADO Sí.
- **ProductosParametros**: IdProveedor 1, CODIGO, Costo.
- **ProductosBodegas**: una fila por bodega (solo BP), CANTIDAD 0.
- No toca el consecutivo de CRS ni carga existencias (eso se hace en CRS con Entrada de Mercancía).

## Después
- Mensaje: «Creado en CRS: …», «Ya existía en CRS (no se tocó): …» o el error. La columna CRS queda con la fecha. `registro.log` anota cada envío.
- En esta sede el producto ya se puede escanear (la caja usa la misma base del servidor).
- Para las otras sedes: [[ALTA - Sincronizar cajas y Revisar Dropbox]].
