---
tags: [programacion, alta, pruebas, pendientes]
actualizado: 2026-10-28
---

Volver a [[ALTA - Inicio]] · mapa: [[ALTA - mapa completo.canvas|Mapa de ALTA]] · registro en [[Bitácora]]

# Pruebas, errores y pendientes

## Probado
- Playwright (en la nube, con CRS simulado): guardar, crear en CRS al guardar, Enviar a CRS, Subir productos con lista, Actualizar desde CRS (nuevo, cambio de precio, reserva, «00 Producto»), Revisar Dropbox, Sincronizar, sin Siigo.
- En el PC con copias (`Documents\crs\prueba-sync`): escribir en las 4 tablas, simular subida y descarga (el 279999 aparece al escanear en «otra caja»), `crs.ps1` real con crear, sincronizar, compactar y revisar (`prueba_sincronizar4.bat`: OK).
- Probar conexión con la base real: 7.813 productos, consecutivo 7812.

## Errores resueltos (y por qué)
- Script de lectura se caía: PowerShell desarmaba la tabla al devolverla → `return ,$t`.
- Archivos reenviados con el mismo nombre quedaban viejos en el PC → nombres nuevos.
- SQL entre dos bases de Access («Operación no válida») → copiar fila por fila.
- uharc mete el archivo con su nombre → siempre se comprime como `wwwProductos.mdb`.
- El .mdb se duplicaba → compactar con DAO.
- Compactar fallaba «archivo en uso» → `OLE DB Services=-4`, soltar el pool, reintentos.
- En `D:\CRS` no estaba BDSCRS → está en `\\vyasas\CRS`.
- Fechas raras («p.┬ám.») en la consola: solo la consola; en Alta se ven bien.

## Pendiente
- [ ] Copia de `\\vyasas\CRS\BDSCRS.mde` antes de la primera subida real.
- [ ] Revisar Dropbox con los datos reales: debe mostrar la última subida (24/10/2026 9:58 a. m.).
- [ ] Primera **Sincronizar cajas** real y **prueba en otra sede**: descarga de wwwSyncro y escanear un producto nuevo. Si no llega: el archivo no está llegando al FTP.
- [ ] Dejar de usar el FTP de Smart Data: que las cajas bajen del **servidor propio** (modificar la descarga de wwwSyncro; carpeta compartida o HTTPS con curl).
- [ ] Idea grande: que las **3 sedes** usen las mismas bases (Escritorio remoto/RemoteApp con CRS en el servidor, o el CRS nuevo en JavaScript / ERP Laravel).
- [ ] Avisar en Alta al eliminar un producto que ya está en CRS (o inhabilitarlo en CRS).
- [ ] Borrar `app\siigo.js` y `node_modules\jszip`; borrar las copias de prueba de `Documents\crs\prueba-sync`.
- [ ] Avisar a Smart Data si se sube desde Alta.
- [ ] Seguridad: `ftp.txt` y `wwwSyncro.mdb` tienen la clave del FTP de Smart Data en texto plano.
