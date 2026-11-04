---
tags: [programacion, alta, indice]
actualizado: 2026-10-28
---

# ALTA (Alta de productos): inicio

Mapa visual: [[ALTA - mapa completo.canvas|Mapa de ALTA]] · registro en [[Bitácora]] · índice: [[Programacion]]

**Qué es:** programa propio de V.YA para crear los productos de la tienda, imprimir sus etiquetas con BarTender y mantenerlos al día con **CRS** (el sistema de Smart Data) y con las **cajas** de las sedes (vía wwwSyncro y Dropbox).

**Dónde está:** `C:\Users\VYASotano\Downloads\AltaDeProductos_v2_2026-10-24\AltaDeProductos\` (PC `vyasotano-pc`). Se abre en el navegador en `http://127.0.0.1:3789`. Código en el repo privado `kori496/ALTA`.

**Qué ya no hace:** Siigo se quitó el 28 oct 2026 (no se compró).

## Notas, una por parte
1. Arranque: [[ALTA - Instalación y arranque]]
2. Disco: [[ALTA - Archivos y carpetas]] · [[ALTA - Base de datos y guardado]]
3. Servidor: [[ALTA - Servidor local y seguridad]]
4. Pantalla: [[ALTA - Formulario nuevo producto]] · [[ALTA - Precio e impuestos]] · [[ALTA - Códigos de barras]] · [[ALTA - Lista de productos y selección]] · [[ALTA - Eliminar productos]]
5. Etiquetas: [[ALTA - Etiquetas con BarTender]]
6. CRS y cajas: [[ALTA - Conexión con CRS]] · [[ALTA - Subir productos a CRS]] · [[ALTA - Actualizar desde CRS]] · [[ALTA - Sincronizar cajas y Revisar Dropbox]]
7. Historia: [[ALTA - Decisiones e historial]] · [[ALTA - Pruebas, errores y pendientes]]

## El recorrido de un producto nuevo
1. Se crea en el **formulario** (código 27xxxx automático, precio desde el costo).
2. Se guarda solo en la base de Alta (`datos\productos.sqlite`).
3. Se imprime la **etiqueta** con BarTender (pestaña Imprimir o botón Etiqueta).
4. Se **sube a CRS** (`\\vyasas\CRS\BDSCRS.mde`): botón «Subir productos» o automático al guardar.
5. **Sincronizar cajas** deja el catálogo en Dropbox (`VYAwwwProductos.uha`).
6. Cada caja hace la **descarga de wwwSyncro** y el producto aparece al escanearlo. (Ojo: falta confirmar que las cajas lo reciban sin el FTP de Smart Data; ver [[ALTA - Pruebas, errores y pendientes]].)

Relacionado: [[CRS - cómo funciona el código]] · [[CRS - wwwSyncro y escribir productos desde Alta]] · nota vieja: [[Alta de productos - herramienta portable para Siigo]] · mapa viejo (24 oct, desactualizado): [[Mapa Alta de productos.canvas|Mapa Alta de productos]].
