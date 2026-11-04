---
tags: [programacion, crs, wwwsyncro, access, inventario, alta-de-productos]
actualizado: 2026-10-28
---

# CRS: wwwSyncro y escribir productos desde Alta

Volver a [[Programacion]] · registro en [[Bitácora]] · relacionado: [[CRS - cómo funciona el código]], [[Alta de productos - herramienta portable para Siigo]]

**Objetivo:** que los productos creados en Alta lleguen a todas las cajas de CRS con wwwSyncro, como si se hubieran creado en CRS.
**Resultado (27 oct 2026):** se puede. Probado en copias con un producto de prueba. Falta conectarlo dentro de Alta.

## Qué es wwwSyncro
Programa de Access de Smart Data (`wwwSyncro.mdb`) que copia el **catálogo de productos** de la caja principal a las demás cajas o sedes. No vende ni factura nada, y no pasa existencias ni ventas: cada caja lleva su propio inventario.

Usa dos bases:
- `BDSCRS.mde`: la base real de CRS, donde están los productos.
- `wwwProductos.mdb`: una "foto" del catálogo que se manda a las otras cajas.

### Modo subida (en la caja principal)
1. Compara cuántas filas tiene cada tabla de productos en `BDSCRS` con su copia en `wwwProductos.mdb` para ver qué hay de nuevo.
2. Borra lo que había en `wwwProductos.mdb` y copia otra vez todo desde `BDSCRS`: productos y referencias (códigos de barras).
3. Anota la fecha y hora de la última actualización.
4. Corre `wwwComprimir.bat`: `uharc.exe` comprime `wwwProductos.mdb` en `VYAwwwProductos.uha` y deja una copia en `D:\Dropbox\CRS-BK-2019\VYA`.
5. Sube el `.uha` por FTP al servidor de Smart Data (carpeta `httpdocs`), usando el archivo `ftp.txt`.

### Modo descarga (en las otras cajas)
1. Baja el `.uha` del FTP y lo descomprime (`wwwDescomprimir.bat`).
2. Los productos que esa caja no tiene los crea con existencias en 0, con el proveedor por defecto y en todas las bodegas.
3. **Borra toda su lista de códigos de barras** y la reemplaza por la del archivo.
4. A los productos que ya tenía les actualiza nombre, costo, precios, IVA, categoría, marca, línea y observaciones.

> Por el paso 3, el archivo que se sube tiene que traer **el catálogo completo**. Si se subiera un archivo solo con los productos nuevos, las cajas se quedarían sin los códigos de barras de todo lo demás y el escáner dejaría de encontrarlos.

## Cómo crea CRS un producto (lo que Alta tiene que copiar)
Cada producto va en **4 tablas** de `BDSCRS.mde`:

| Tabla | Qué guarda | Valores que usa V.YA |
|---|---|---|
| `Productos` | Datos y precios | `CODIGO` texto de 6 dígitos (ej. `007783`), `IdProveedor` 1, `IdMarca` 1 (V.YA), `CodIva` 19, `PVMayor` = costo, `PVEspecial1` y `PVEspecial2` = precio detal, `CantidadMayor/E1/E2` = 1, `Embalaje` 1, `IdEstado` 1, `Existencias` 0, `Fecha_Sistema` = ahora |
| `ProductosReferencia` | Código de barras que lee la caja | `CODIGO` = `REFERENCIA` = el mismo número, `HABILITADO` = Sí |
| `ProductosParametros` | Proveedor y costo | `IdProveedor` 1, `CODIGO`, `Costo` |
| `ProductosBodegas` | Una fila por bodega | Solo existe la bodega `BP` (BODEGA PRINCIPAL), `CANTIDAD` 0 |

Detalles importantes:
- **Margen:** CRS guarda en `PDetal`, `PEspecial1` y `PEspecial2` el **% de ganancia sobre el precio de venta**: (venta − costo) ÷ venta × 100. Ejemplo: costo 76.000 y venta 117.900 → 35,54 % (no el 30 % sobre el costo que usa Alta). `PMayor` queda en 0.
- **Numeración:** CRS saca el siguiente código de la tabla `Consecutivos`, fila `ID = 10` ("Productos"), que iba en **7783**. No mira el código más alto, así que la serie **27xxxx** de Alta no le cambia nada y no choca.
- Categorías que existen: -1 General, 1 Jean Bota Recta, 2 Jeans Modelo, 3 Jeans Campana, 4 Blusas, 5 Short, 6 Chaleco, 7 set, 8 Body, 9 Crop Top, 10 Polo, 11 Braga, 12 Jeans.
- Marcas: -1 General, 1 V.YA, 2 Dyaboo, 3 Beso Menta. IVAs: 0, 5, 10, 16, 19, 25.
- Al 27 oct: `BDSCRS` tenía 7.784 productos y `wwwProductos.mdb` 7.747. Había 37 productos sin sincronizar desde la última subida (24 oct, 9:58 a. m.).

## La prueba, paso a paso (27 oct)
Todo se hizo en `Documents\crs\prueba-sync\`, con **copias**. No se tocó `D:\CRS`, ni la copia `Documents\crs`, ni el FTP.

1. **Copias de trabajo.** El script copia `BDSCRS.mde` como `P_BDSCRS_principal.mde` (la caja principal) y como `P_BDSCRS_otra_caja.mde` (otra caja), y `wwwProductos.mdb` como `P_wwwProductos.mdb`. Se rehacen cada vez que se corre.
2. **Leer la estructura** (`leer_v2.bat` → `estructura.txt`). Abre las copias solo para leer con el motor de Access que ya está en el PC (**Microsoft.ACE.OLEDB.16.0**, PowerShell de 64 bits). Lista columnas, índices y los últimos 5 productos creados en CRS para ver cómo los llena.
3. **Alta escribe el producto** (`prueba_alta3.bat`, paso 1). Crea el `279999` "PRUEBA ALTA - BORRAR" en las 4 tablas de la copia principal, dentro de una **transacción**: si algo falla no queda nada a medias.
4. **Simular la subida de wwwSyncro** (paso 2). Vacía `wwwProductos` y `wwwProductosReferencia` en la copia de `wwwProductos.mdb` y copia ahí todas las filas de la principal. Resultado: 7.747 → **7.785** productos, incluido el 279999.
5. **Simular la descarga en otra caja** (paso 3). Compara la copia de "otra caja" con el archivo: recibió **1 producto nuevo**. Lo inserta con existencias 0, el proveedor y la bodega BP, y reemplaza los códigos de barras (7.791).
6. **Verificar** (paso 4). En la otra caja, al buscar la referencia `279999` aparece el producto con precio 117.900, IVA 19, existencias 0 y bodega BP. Quedaron **0 productos sin código de barras**.

Resultado: `RESULTADO: PRUEBA COMPLETA OK` en `prueba-sync\resultado_prueba.txt`.

## Lo que NO funcionó (y por qué)
- **Primer script de lectura:** se caía justo después de listar las tablas. Era un error del script: PowerShell "desarma" la tabla de resultados al devolverla de una función. Se arregla devolviéndola con `return ,$t`.
- **Archivos que no se actualizaron:** al reenviar el script corregido con el mismo nombre, en el PC quedó la versión vieja. Se resolvió con nombres nuevos (`leer_v2`, `prueba_alta2`, `prueba_alta3`).
- **SQL entre dos bases:** `INSERT ... SELECT * FROM Productos IN 'archivo.mde'` y también `FROM [;DATABASE=archivo.mde].Productos` dan *"Operación no válida para este tipo de objeto"*. Solución: leer las filas con el script y escribirlas una por una en la otra base. Alta tendrá que hacerlo igual.
- **Herramientas en la nube:** no se pudo instalar mdbtools ni lectores de Access (red bloqueada), por eso todo se corrió en el PC con PowerShell.
- **Control del PC:** el Explorador de Windows solo deja hacer clics, sin teclado. Los `.bat` los ejecutó el usuario con doble clic.

## Lo que se agregó a Alta (27 oct, noche)
Archivos: `app\crs.ps1` (nuevo), `app\server.js`, `app\public\index.html` en `Downloads\AltaDeProductos_v2_2026-10-24\AltaDeProductos\`. Lo de antes quedó en `respaldo_antes_de_CRS\`.
Alta trabaja con Access llamando a `crs.ps1` (PowerShell de 64 bits + motor ACE OLEDB 16.0 del PC). Configuración en `configuracion\opciones.json` → `crs`.

**Configuración → «CRS: crear los productos también en CRS»**
- Archivo `BDSCRS.mde` (real: `\\vyasas\CRS\BDSCRS.mde`), proveedor 1, marca 1 (V.YA), categoría -1 (General).
- Casilla «Crear en CRS cada producto que guarde» (apagada por defecto).
- Rutas para sincronizar: `D:\CRS\wwwProductos.mdb`, `D:\CRS\uharc.exe`, `D:\Dropbox\CRS-BK-2019\VYA`. «Probar conexión» dice si falta alguna.

**Crear en CRS / Enviar a CRS** (Alta → CRS)
- Escribe el producto en las 4 tablas, en una transacción. Si el código ya existe en CRS no lo toca («ya existe»).
- Columna **CRS** en la lista: fecha de envío y, si se revisó Dropbox, «en cajas» (verde) o «falta sincronizar» (naranja).
- Botón «Enviar a CRS» en la barra de selección.

**Botón morado «Sincronizar cajas»** (Alta → Dropbox, como la subida de wwwSyncro, SIN FTP)
1. Copia de seguridad de `wwwProductos.mdb` en `datos\copias_wwwProductos` (últimas 10).
2. Copia de BDSCRS a wwwProductos.mdb las tablas: Categorias, CategoriasAlternas, Grupos, Ivas, Lineas, Marcas, Productos, ProductosReferencia, Secciones (todas las `www…` menos wwwData).
3. `wwwData` Id 1 = fecha y hora.
4. Compacta `wwwProductos.mdb` (DAO.DBEngine.120): sin esto el archivo se duplica en cada sincronización (4,4 MB → 9,7 MB en la prueba).
5. `uharc a -o+` → `VYAwwwProductos.uha`, siempre con el archivo adentro llamado `wwwProductos.mdb`, y copia a Dropbox.
6. Comprueba abriendo el .uha de Dropbox como una caja.

**Panel «Estado de las cajas»** (arriba de la lista)
- «Revisar Dropbox»: descomprime el .uha en una carpeta temporal y compara con BDSCRS: productos en Dropbox, fecha, cuántos faltan por sincronizar y cuáles.

**«Actualizar desde CRS»** (CRS → Alta, manda CRS)
- Al abrir Alta y con el botón (el botón muestra antes un resumen y pide confirmar).
- Agrega a Alta los productos de CRS que no tiene (grupo Confecciones, unidad, marcados como exportados a Siigo «importado de CRS», como el 24 oct).
- Actualiza nombre, costo, detal, mayorista e IVA cuando son distintos. No toca grupo, unidad ni INC. Los productos que solo están en Alta no se tocan.
- Los códigos de barras extra de CRS (una referencia distinta al código) quedan reservados en Alta para no repetirlos.
- Se salta el genérico «00 Producto». Si un código de CRS ya es el código de barras de otro producto de Alta, no se trae y se avisa.

**Botón «Subir productos (N)»** (28 oct, en el panel morado)
- Cuenta los productos de Alta que no están en CRS (columna `en_crs` vacía). Al abrir Alta, «Actualizar desde CRS» marca como subidos todos los que ya existen en CRS, así que solo quedan los creados en Alta.
- Al pulsarlo sale la **lista** (referencia, nombre, costo, detal, mayor) con casillas, todas marcadas; «Subir a CRS» sube las marcadas de 200 en 200. Los que ya existan en CRS no se tocan.
- Después hay que pulsar «Sincronizar cajas» para que lleguen a las otras sedes.
- Ojo: **Sincronizar cajas no elige productos**: manda el catálogo completo de CRS (las cajas reemplazan toda su lista de códigos de barras). Lo que solo está en Alta no llega hasta subirlo.

## Pruebas en el PC (27 oct, noche)
- `prueba_sincronizar.bat`: crear 279998 OK, 007783 «ya existe» OK, 9 tablas en 7 s. Falló el paso de revisar: **uharc guarda el archivo con su nombre** (`S_wwwProductos.mdb`) y las cajas esperan `wwwProductos.mdb` → ahora siempre se comprime con ese nombre.
- `prueba_sincronizar2.bat`: **OK**. Dropbox de prueba con 7.785 productos y 7.791 referencias, 0 pendientes, 279998 incluido. Se vio que el .uha pasó de 371 KB a 764 KB → se agregó el compactado.
- `prueba_sincronizar3.bat`: OK pero **no compactó**: «el archivo ya está en uso». Windows deja abierto el .mdb un momento tras cerrar la conexión (pool de OLE DB). Arreglo: `OLE DB Services=-4`, `ReleaseObjectPool()`, GC y hasta 5 reintentos.
- `prueba_sincronizar4.bat`: **OK y compactado**: wwwProductos.mdb 4.435.968 → 4.456.448 bytes, .uha 371.839 bytes, 7.785 productos, 0 pendientes, 9 s.
- En la consola la fecha sale como «p.┬ám.»: es solo la consola; en Alta se ve bien.

## Decisiones (27 oct)
- Base real: **`\\vyasas\CRS\BDSCRS.mde`** (servidor). En `D:\CRS` de este PC solo están las bases locales (BDBCRS, BDLCRS, BDMCRS) y CRS. Probar conexión el 27 oct: 7.813 productos, consecutivo 7812.
- wwwProductos.mdb y uharc.exe: `\\vyasas\CRS\`. Dropbox: `D:\Dropbox\CRS-BK-2019\VYA` en este PC (falta confirmar con «Revisar Dropbox» que es la misma carpeta que usan las cajas: debe mostrar la última subida, 24/10/2026 9:58 a. m.).
- **BDSCRS se abre en modo solo lectura** (`Mode=Read`) en todo menos «Crear en CRS». «Crear en CRS» queda apagado hasta hacer copia de BDSCRS.
- Sincronizar solo hasta Dropbox, sin FTP (Smart Data lo toma de ahí).
- Si un dato es distinto entre Alta y CRS, **manda CRS**. Alta se actualiza desde CRS al abrir y con el botón.
- Se acepta escribir en `D:\CRS` para esto (antes era solo lectura).

## Archivos de la prueba
`Documents\crs\prueba-sync\`: `leer_v2.bat/.ps1`, `estructura.txt`, `prueba_alta3.bat/.ps1`, `resultado_prueba.txt` y las copias `P_*.mde`, `P_wwwProductos.mdb`. Las versiones `1_leer_estructura`, `prueba_alta` y `prueba_alta2` son las que fallaron.
