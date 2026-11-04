---
tags: [programacion, siigo, inventario, crs, herramienta]
actualizado: 2026-10-27
---

# Alta de productos: herramienta portable para Siigo

Volver a [[Programacion]] · registro en [[Bitácora]]

## Objetivo
Reemplazar la pantalla de creación de productos de CRS (software de inventario, cartera y facturación de Smart Data, Colombia). Cada producto nuevo se digita en una herramienta propia, queda guardado en una base de datos portable (.sqlite) y, más adelante, se exporta a un Excel listo para importar en Siigo Nube / Siigo Facturación.

## Archivo
- **Versión 2 (actual, 24 oct): carpeta instalable** en `C:\Users\sharo\OneDrive\Documentos\alta de productos\`. Paquete para otras computadoras: `paquete\AltaDeProductos_v2_2026-10-24.zip`. Ver «Versión 2» abajo.
- Versión 1 (se deja igual como referencia): `Tienda/ALTA/Alta de productos/productos.html`, un solo archivo HTML. Se abre con doble clic en cualquier navegador, sin instalar nada ni Python.
- Usa sql.js (SQLite en el navegador) desde cdnjs. La primera vez necesita internet.

## Qué hace hoy
- Formulario de alta: código interno (único), código de barras, nombre, línea/grupo, costo sin IVA, precio detal, precio mayorista, impuesto (IVA 19%, IVA 5%, exento, excluido) e INC %.
- Validaciones: obligatorios, código de barras de 6 a 14 dígitos, código interno sin repetir, aviso si el precio detal queda por debajo del costo.
- Lista con búsqueda por código, código de barras o nombre, y botón para eliminar.
- **Guardar base (.sqlite)**: descarga la base. Cada descarga crea un archivo con la fecha (`productos_AAAA-MM-DD.sqlite`).
- **Abrir base**: carga un .sqlite anterior para seguir agregando.
- **Exportar CSV** (separado por `;`, con BOM para que Excel lea bien los acentos).

## Datos de Siigo (guía oficial "Subir desde Excel Productos")
- La plantilla se descarga desde Siigo: Configuración → Productos y servicios → Importación → Productos y Servicios → **Crear plantilla**.
- Encabezados azul oscuro = obligatorios; azul claro = opcionales (importantes igual).
- No modificar, borrar ni agregar columnas, ni meter fórmulas en la plantilla.
- Máximo **500 registros por archivo**; si hay más, partir el archivo.
- Los productos existentes (mismo código) se **actualizan**, no se duplican.
- Productos tipo combo no se importan por Excel.
- Si sale "plantilla desactualizada": descargar la plantilla de nuevo y pegar los datos ahí.
- Si sale "Grupo de inventario no tiene un valor de lista válido": el grupo debe existir antes en Siigo (clasificación de inventario y servicios).
- Si un producto no entra, Siigo muestra el detalle; se corrige en la plantilla y se sube de nuevo.

## Notas de la nota de Notion original
- Campos que pide CRS: código interno, código de barras, nombre (sin abreviaturas, sale en la factura electrónica), línea/grupo/familia, costo de compra sin IVA, listas de precios (detal, mayorista), tipo de impuesto e INC.
- Para etiquetas de productos nuevos se mencionó BarTender.
- Requisito: "se tiene que poder vincular con siigo.com".

## Cambios del 23 oct (noche)
- Columna «Código interno» renombrada a **Referencia** (la base sigue guardando la columna `codigo_interno` para que los .sqlite viejos funcionen).
- Grupo por defecto **Confecciones**; opción «Otro…» para escribir otro grupo.
- Botón **Plantilla** en cada producto de la lista: copia nombre, grupo, costo, precios, impuesto e INC a un producto nuevo; quita referencia y código de barras para que los pongas tú.
- Botón **Etiqueta** por producto y **Imprimir con BarTender** en el formulario. La herramienta no habla con BarTender directamente: descarga un CSV (`referencia, nombre, codigo_barras, precio_detal, grupo, impuesto`) y un `.bat` que llama a `bartend.exe` con la plantilla .btw. Ruta, plantilla, impresora y copias se configuran en «Configuración de BarTender» y se recuerdan en el navegador.
- Sin probar: los parámetros del `.bat` (`/F`, `/D`, `/PRN`, `/C`, `/P`) hay que verificarlos con `bartend /?` en la versión instalada, y la plantilla .btw debe estar enlazada al CSV.

## Cambios DIAN (23 oct, noche)
- **Precio con IVA incluido**: base = precio / (1 + IVA + INC); IVA = base x tarifa. Se muestra el desglose en vivo en el formulario y las columnas Base detal e IVA detal en la lista y en el CSV.
- **Tipos de impuesto**: IVA 19% (por defecto), IVA 5%, Exento (0%), Excluido y No gravado.
- **Unidad de medida** obligatoria (por defecto Unidad). Las bases viejas se migran solas (columna `unidad`).
- **Validaciones**: precio detal obligatorio; código de barras de 8, 12, 13 o 14 dígitos con dígito verificador GS1 (si no cuadra solo avisa); INC solo avisa (las prendas normalmente no lo llevan); aviso si la base sin IVA es menor que el costo; aviso al elegir exento, excluido o no gravado.
- Panel «Reglas DIAN que aplica esta herramienta» con referencias a verificar: Estatuto Tributario arts. 468, 468-1, 477 y 424, y Resolución DIAN 000042 de 2020 con su anexo técnico vigente.
- No sustituye al contador: confirmar el tipo de impuesto de cada referencia. No se verificaron los códigos UBL de la DIAN; el XML lo arma Siigo.
- Probado: sintaxis del script y cálculo (119.000 con IVA 19% = base 100.000 + IVA 19.000). Sin probar en el navegador.

## Código de barras propio (23 oct, noche)
> **Reemplazado el 24 oct (tarde):** ya no se generan EAN-13 con prefijo 20. Ahora son códigos de **6 dígitos** como los de CRS. Ver «Sesión 24 oct (tarde)».

- Botón **Generar** junto al campo, y opción (activada por defecto) de generarlo solo al guardar si se deja vacío.
- Formato EAN-13: **prefijo (2 dígitos, 20 a 29) + consecutivo (10) + dígito verificador**. Por defecto `20`, por ejemplo `2000000000015`. Los prefijos 20 a 29 son de circulación restringida de GS1 (uso interno de una empresa), así que no chocan con códigos de fabricantes.
- El consecutivo sigue al mayor que ya exista en la base con ese prefijo y salta cualquier código ya usado. No se permite guardar dos productos con el mismo código de barras.
- Sirve para la tienda (lector, Siigo, etiquetas BarTender). No sirve para vender en plataformas que exigen un GTIN real de GS1.
- Para que Siigo lo reconozca, el código tiene que ir en la columna de código de barras de la plantilla de importación (pendiente: confirmar el nombre exacto de esa columna con la plantilla).
- Probado: el dígito verificador coincide con el algoritmo GS1. Sin probar en el navegador ni con el lector.

## Precio a partir del costo (23 oct, noche)
- Fórmula de la tienda: **costo sin IVA x (1 + ganancia) x (1 + IVA)**, luego redondeo. Los porcentajes no se suman: el IVA va sobre el precio que ya incluye la ganancia.
- Ejemplo del usuario: costo 76.000, ganancia 30% = 98.800, con IVA 19% = 117.572, redondeado a **117.900** (terminación 900, hacia arriba).
- La ganancia es sobre el costo (no margen sobre el precio). Por defecto 30%; el redondeo por defecto es «Terminar en 900». Ambos se recuerdan en el navegador.
- En el formulario aparece el precio calculado y el botón «Usar este precio», que lo copia al precio detal. El precio se puede seguir escribiendo a mano.
- Con INC, el total usa (1 + IVA + INC) sobre la base, igual que el desglose.
- Probado: 76.000 da 117.572 y 117.900; 50.000 da 77.350 y 77.900. Sin probar en el navegador.
- Pendiente: si el precio mayorista usa otra ganancia.

## Códigos de barras que nunca se repiten (23 oct, noche)
- **La base lo impide**: índice único sobre `codigo_barras` (varios productos sin código sí se permiten). Si una base vieja ya trae repetidos, al abrirla se listan para corregirlos.
- **El consecutivo nunca baja**: se guarda un contador por prefijo en la base (`contador_barras`). Aunque se borre un producto o se genere un código sin guardarlo, ese número no se reutiliza (puede haber saltos, es lo esperado).
- **Eliminar un producto reserva su código** (`barras_reservadas`, origen «eliminado»): tampoco se puede volver a digitar a mano.
- **Códigos que ya existen en CRS o Siigo**: en «Código de barras propio» → «Cargar códigos existentes (CSV o TXT)». Toma todo número de 8 a 14 dígitos del archivo y los reserva; no se generan ni se aceptan. Para Excel, exportar antes a CSV.
- **«Seguir después del número»**: fija desde dónde continuar la serie (solo sube). Útil al empezar una base nueva si ya se usó la serie.
- **Varias bases o computadores**: cada archivo .sqlite lleva su propio contador. Si se trabaja en dos a la vez, usar un prefijo distinto en cada una (20, 21, ...) o una sola base en OneDrive.
- Probado con SQLite real: generación, borrado, reservados, duplicado bloqueado y contador que no baja. Sin probar en el navegador.

## Cómo vincular BarTender para imprimir (24 oct)
- Etiquetas de producto (no tickets de venta, esos son de Siigo).
- **Lo confirmado en la ayuda de BarTender 2021** (Command Line Parameter Reference): `bartend.exe /F=archivo.btw /P /X`; `/F=` carga el documento, `/P` imprime, `/C=n` copias, `/D=archivo` indica el archivo de datos. `/D` reemplaza la primera conexión a archivo de texto del documento (se asume que la primera línea trae los nombres de los campos). Una respuesta de soporte de Seagull dice que `/D` requiere la edición Automation o superior (post antiguo, verificar con la licencia).
- **No confirmado**: `/PRN` (no apareció en la ayuda que se leyó) y qué hace exactamente `/X` (aparece en los ejemplos; en la práctica cierra BarTender al terminar). El `.bat` de la herramienta solo envía `/PRN` si el campo «Impresora» tiene texto; si da error, dejarlo vacío y fijar la impresora dentro de la plantilla .btw. El `.bat` actual no lleva `/X`.
- **Pasos**: 1) en BarTender crear la etiqueta con código de barras EAN-13; 2) Conexión a base de datos -> archivo de texto -> el CSV que descarga la herramienta (coma, primera fila con nombres: referencia, nombre, codigo_barras, precio_detal, grupo, impuesto) y arrastrar los campos a los objetos; 3) guardar el .btw; 4) en «Configuración de BarTender» poner la ruta de bartend.exe y del .btw; 5) botón Etiqueta -> poner CSV y .bat en la misma carpeta -> doble clic en el .bat.
- **Si `/D` no funciona con la licencia**: conectar el .btw a un CSV de ruta fija (que la herramienta sobrescriba siempre) y quitar `/D` del .bat.
- **Impresión realmente automática**: BarTender Commander (vigila una carpeta y imprime al llegar un archivo) o la versión de carpeta instalable de la herramienta, que ejecuta bartend.exe sola. Ediciones que incluyen Commander: no confirmado en lo revisado; preguntar a Seagull o al distribuidor.
- Nada de esto se ha probado todavía en el PC con BarTender instalado.

## Versión 2: carpeta instalable (24 oct)
Mapa visual de cómo funciona: [[Mapa Alta de productos.canvas|Mapa Alta de productos]].

Opción elegida (A): app local con **Node.js incluido** (`node\node.exe`) y la interfaz en el navegador en `http://127.0.0.1:3789`. Se descartaron Python embebido (openpyxl puede dañar la plantilla, habría que reescribir la lógica) y Electron (150-250 MB y paso de build).

**Estructura**
- `iniciar.vbs` (abre sin ventana negra), `iniciar.bat`, `instalar.bat` + `instalar.ps1` (acceso directo en escritorio y menú Inicio; quita el bloqueo de Windows a los archivos del .zip), `LEEME.txt` (instrucciones cortas).
- `app\server.js`: servidor local (solo 127.0.0.1, con token por sesión y control del Host). `app\siigo.js`: motor del Excel. `app\public\index.html`: la interfaz de productos.html con los cambios mínimos. `app\public\vendor\`: sql.js 1.10.3 local (sin CDN). `app\node_modules\jszip` (única librería).
- `datos\productos.sqlite` (la base), `datos\copias\` (copias con fecha), `datos\config.json` (BarTender, columnas de Siigo, ruta de la base), `datos\etiquetas\etiquetas.csv`, `datos\registro.log`. `plantillas\` (plantilla de Siigo), `exportados\` (Excel generados). `app\pruebas\` (pruebas; no va en el .zip).

**Qué cambió frente a productos.html**
- **Guardado automático**: la lógica sigue con sql.js en el navegador; tras cada cambio la base completa se manda al servidor y se escribe en disco (temporal + renombrar, con reintentos si OneDrive bloquea, y se **relee para verificar** que quedó igual). Indicador «Guardado hh:mm» arriba.
- **Copias de seguridad**: al abrir el programa, cada hora de trabajo, antes de «Abrir otra base» y a mano. Se conservan las últimas 60.
- **Abrir otra base…** lee los .sqlite viejos (migra con ALTER TABLE: `unidad`, `exportado_siigo`) y los usa como base de trabajo; el archivo original no se modifica. «Descargar copia» sigue existiendo.
- **Ubicación de la base** configurable (por ejemplo, en OneDrive). Si cambia el archivo desde otra ventana u otro computador, la app no lo pisa: pide recargar (F5).
- **BarTender directo**: el servidor escribe `datos\etiquetas\etiquetas.csv` (ruta fija) y ejecuta bartend.exe. Los parámetros son editables (`/F="{plantilla}" /D="{datos}" {impresora} /C={copias} /P /X`). Si `/D` no sirve con la licencia, se quita de los parámetros y se enlaza el .btw a ese CSV fijo.
- **Excel para Siigo** (tarjeta nueva): carga la plantilla, detecta la hoja y la fila de encabezados, marca como obligatorias las de encabezado oscuro, lee las listas desplegables (también las de otra hoja o con rango con nombre) y relaciona cada columna con un dato de la app por su nombre. Pantalla para ajustar: dato, valor fijo (por ejemplo «Tipo de producto = Producto») y equivalencias (valor app = valor Siigo). «Revisar productos» lista los que fallan y por qué (falta obligatoria, valor que no está en la lista de Siigo, como un grupo que no existe). Exporta en lotes de 500 y marca la fecha de exportación en cada producto (columna «Siigo»); por defecto solo exporta los que no se han exportado.
- Cómo escribe el .xlsx: lo abre como zip y solo cambia `sheetData` de la hoja, agrega textos al final de `sharedStrings.xml` y, si hay una tabla de Excel, alarga su rango. Todo lo demás queda byte a byte igual. Códigos como texto, precios como número; cada celda conserva el estilo de la plantilla.

**Probado (24 oct)**
- Plantilla de prueba hecha con Excel (encabezados azul oscuro/claro, listas en hoja oculta, rango con nombre, columna en texto, celdas combinadas, paneles inmovilizados): detección correcta de 7 obligatorias y de las listas; comparación del zip: solo cambian la hoja (dentro de sheetData) y sharedStrings; Excel abre los archivos sin reparar y conserva formato, validaciones y hoja oculta; 1.203 productos → lotes 500 + 500 + 203.
- Playwright con Edge, la app abierta de verdad (22 pruebas OK, `app\pruebas\prueba_e2e.js`): crear producto con precio desde el costo (76.000 → 117.900), código generado, queda en disco, recargar, Plantilla, Eliminar (código reservado y bloqueado a mano), cargar códigos de CRS (los salta), imprimir con un BarTender simulado (parámetros y CSV correctos), exportar a Siigo y marcar exportados, conflicto entre dos pestañas, abrir una base vieja (migración y copia previa), sin errores de JavaScript.
- Instalación en limpio desde el .zip en una ruta con espacios: acceso directo, arranque con el node.exe incluido, segundo doble clic reutiliza el servidor, cerrar el programa.
- **Error encontrado y corregido**: con la ruta de bartend.exe en «C:\Program Files\...» Windows partía el comando por el espacio; ahora la ruta va entre comillas (`argv0`).

**No probado**
- Plantilla real de Siigo (falta el archivo; el video de la guía no deja ver las columnas). Solo se probó con la plantilla de prueba.
- BarTender real (no está instalado en este PC) ni `bartend /?`. `/PRN` sigue sin confirmar.
- Instalación en un computador sin Node instalado (el node.exe va incluido, así que no debería importar) y con Windows SmartScreen.

## Botón IMPRIMIR, historial y log (24 oct)
- Botón verde **IMPRIMIR** arriba en la ventana principal: abre la pestaña `imprimir.html`.
- Muestra **solo los productos guardados en esta sesión** (desde que se abrió el programa; si se elimina uno, sale de la lista). Por producto: marcar, **cantidad de etiquetas** y **precio en etiqueta**. Los que aún no se imprimieron vienen marcados. Pide confirmación con el resumen antes de imprimir.
- Decisión: cambiar el precio en esa pestaña **solo cambia la etiqueta**, no el producto guardado (la fila se resalta en amarillo).
- Cantidades: el CSV lleva **una fila por etiqueta** (cantidad 3 = 3 filas) y BarTender se llama con `/C=1`. Así cada producto sale con su propia cantidad en un solo trabajo. Máximo 1000 etiquetas por impresión.
- **Historial de la sesión**: hora, referencia, nombre, precio, cantidad, desde dónde (pestaña Imprimir, botón Etiqueta, reimpresión) y resultado. «Reimprimir» con cantidad y precio editables. Vive en la memoria del servidor: **se reinicia solo al cerrar el programa**. Todas las impresiones (también el botón Etiqueta) pasan por `/api/imprimir` y quedan en el historial.
- **Log en disco que no se borra**: `datos\impresiones.log`, una línea por producto impreso: `fecha | IMPRESO/ERROR | ref | nombre | barras | $precio | N etiquetas | impresora | desde [| error]`, más «Programa abierto» y «Programa cerrado (motivo)». Botón «Ver log de impresiones» lo abre en el Bloc de notas.
- Decisión: como la app vive en el navegador, si no queda **ninguna pestaña abierta durante 10 minutos** el programa se cierra solo (latido cada 30 s) y el historial se reinicia. También se cierra con «Cerrar el programa».
- **Ctrl+F7** (en la ventana principal o en la de impresión): reinicia la sesión y empieza de cero. Pide confirmación (decisión, para que no se borre por accidente), borra la lista de productos de la sesión y el historial, no toca los productos guardados y lo anota en el log («Sesión reiniciada (Ctrl+F7). Se borraron N productos y M impresiones»).
- Botón **← Volver** en la pestaña de impresión: la cierra y deja la ventana principal; si se abrió sola, va a la ventana principal en la misma pestaña. El botón dice «Imprimir» (ya no en mayúsculas).
- ~~Ojo: abrir una segunda ventana principal hace que la primera pida recargar (F5).~~ Corregido el 24 oct (ver abajo).
- **Error resuelto (24 oct): «No se pudo leer la sesión: Sesión no válida: recarga la página»** en la pestaña de impresión. Causa: la clave de seguridad (token) cambia cada vez que arranca el programa; si el programa se reinicia (cierre automático a los 10 min, nuevo doble clic, pestaña restaurada por el navegador) la pestaña vieja seguía con la clave anterior. Arreglo: la clave va en `<meta name="token">` y, si el servidor responde 403, la página pide la clave nueva y repite la operación sin recargar.
- Mismo arreglo para guardar: la «versión» de la base ahora es la **fecha + tamaño del archivo** (antes era la hora de arranque del servidor). Sigue valiendo tras reiniciar el programa, y abrir una segunda ventana ya no bloquea a la primera: solo se pide recargar si otra ventana u otro computador **guardó** de verdad.
- Para que el arreglo aplique, hay que cerrar el programa («Cerrar el programa») y abrirlo de nuevo: el que estaba abierto sigue con el código anterior.
- **Error resuelto (24 oct): «el imprimir funciona muy mal».** Causa: el programa abierto en la carpeta normal había arrancado a las 00:39, antes de que existiera la impresión. Las páginas se leen del disco en cada carga (se veía la pestaña nueva), pero el servidor en memoria era el viejo: `/api/sesion` respondía «Ruta desconocida». No era el .zip. Se reinició el programa.
- **Para que no se repita**: al arrancar, el programa compara la «firma» del código (fecha de `server.js` y `siigo.js`) con la del que ya está abierto en esa carpeta. Si es distinta, cierra el viejo (con la clave que deja en `datos\.token`), lo anota en el log («Programa cerrado (se abrió una versión actualizada del programa)») y abre el nuevo. Si es la misma, solo abre el navegador. Otra instalación en otra carpeta no se toca (usa otro puerto). Prueba: `app\pruebas\prueba_actualizacion.js` (5/5).
- Lección: después de cambiar `server.js` o `siigo.js` hay que reiniciar el programa; ahora basta con el doble clic.
- Pruebas: 46/46 en tres corridas (nuevas: reinicio del programa con pestañas abiertas, segunda ventana que no bloquea, ventana desactualizada que no pisa).
- Pruebas: 43/43 en cuatro corridas seguidas (se corrigieron dos pruebas que fallaban por tiempos, no por la app).
- Probado con Playwright: 14 pruebas nuevas (36/36 en total), incluida la reapertura (historial vacío, log intacto) y el cierre automático. Con BarTender simulado; falta con BarTender real.

## Carpeta de opciones guardadas (24 oct)
- Carpeta nueva **`configuracion\`** con `opciones.json` (y un LEEME): ruta de bartend.exe, plantilla .btw, impresora elegida, copias, parámetros, ubicación de la base, columnas de Siigo, **impresoras ya usadas** (las 10 últimas, la más reciente primero) y **última carpeta** por tipo de archivo (`base`, `plantillaSiigo`, `btw`, `bartender`, `codigos`). Copiar la carpeta lleva las opciones a otro PC. No va en el .zip (cada PC tiene las suyas).
- Paso automático: la primera vez, `datos\config.json` se copia a `configuracion\opciones.json` y el viejo queda como `datos\config.json.migrado` (no se borra).
- **Ventana de Windows para elegir archivos**: el navegador no deja fijar la carpeta inicial de su selector, así que «Abrir otra base…», «Cargar plantilla de Siigo», «Cargar códigos existentes» y los nuevos **Buscar…** (bartend.exe y .btw) abren un `OpenFileDialog` de Windows (PowerShell -STA, formulario dueño invisible y «siempre visible» para que salga encima y centrada) en la última carpeta usada. Si la ventana de Windows no se puede abrir, se usa el selector del navegador.
- **Impresora**: lista desplegable con las impresoras instaladas en Windows (`Win32_Printer`) más las ya usadas; en la ventana principal y en la de impresión.
- Probado: 54/54 con Playwright (ventana simulada; nuevas: paso de opciones viejas, LEEME, Buscar .btw, impresora/exe/.btw guardados, impresoras usadas, últimas carpetas de códigos, .btw y base, lista de impresoras reales). Ventana real de Windows probada aparte: abre en la carpeta recordada, filtra .btw, sale encima y centrada (corregido: al principio salía corrida y cortada), Esc devuelve «cancelado».
- Pendiente para el usuario: el programa abierto a la 1:30 sigue con el código anterior; el siguiente doble clic lo actualiza solo (se borra la lista de la sesión) y hace el paso de opciones.
## Sesión 24 oct (tarde): BarTender real, etiqueta V.YA, códigos de 6 dígitos y base de CRS
Carpeta en uso en el PC de la tienda: `C:\Users\VYASotano\Downloads\AltaDeProductos_v2_2026-10-24\AltaDeProductos\`.

## Código de barras = referencia (24 oct)
- En la base, la referencia (`codigo_interno`) y el código de barras son el mismo número (ej. 007759). El formulario ya no pide referencia aparte: usa el código de barras (escrito, «Generar» o automático al guardar).
- Campos nuevos: **Referencia** (del proveedor, ej. Vf2944) y **Descripción** (ej. Body). Se guardan juntos en `nombre` como «Body Vf2944», igual que los productos que ya había. No se cambió el esquema, así que Siigo, etiquetas y búsqueda siguen igual.
- «Plantilla» quita del nombre la última palabra que tenga un dígito (la referencia) y deja solo la descripción.
- **PHP no sirve para ver las impresoras del PC donde se abre**: PHP también corre en el servidor y el navegador no deja listar impresoras. Hoy ya salen las del PC porque la app corre en cada computador (127.0.0.1). Si algún día va en un servidor: hace falta un agente local por PC (el mismo Node recortado).
- Sin probar en el navegador todavía (solo la separación de nombres con datos reales).
**Sistema viejo de etiquetas (ENLACE-TECH)**
- `Documentos\ArchivosCodigoBarrasC\ENLACE-TECH\ArchivosCodigoBarrasC\`: `CodigosBarra.mdb` y `CB-Zebra.mdb` (Access, vienen de CRS, ruta `C:\CRS\CB-Zebra.mdb`) y `CBZebra.btw` (BarTender 11.0 / 2016 R1, Enterprise Automation). Tabla de etiquetas `Hablador` (Codigo, Referencia, Presentacion, Precio, Cantidad). La original no se tocó; se trabaja con una copia en `plantillas\CBZebra.btw`.

**Etiqueta V.YA (formato final, igual a las etiquetas impresas)**
- Ejemplo real: `Jean VFk11017` / código de barras / `007754` / `2*1079VY` / `$140900`.
- Columnas del CSV que se enlazan en BarTender:
  - texto de arriba → `referencia_descripcion` (descripción + referencia; si la descripción ya trae la referencia, como en los productos de CRS, va solo la descripción)
  - código de barras → `codigo_barras`
  - texto de abajo → `codigo_interno` (= código de barras)
  - precio al mayor → `precio_mayor_codigo` = `2*` + precio al mayor sin las dos últimas cifras + `VY` (65.000 → `2*650VY`, 107.900 → `2*1079VY`). También existe `precio_mayor_sin_ceros` (solo el número).
  - precio grande → `precio_detal_txt` (sin punto de miles: `140900`; el `$` va fijo en la plantilla)
- El CSV usa **punto y coma** (Excel en español lo abre en columnas) y UTF-8 con BOM. En BarTender: archivo de texto, delimitado por punto y coma, primera fila con nombres.
- Se mantienen las columnas viejas (`referencia, nombre, codigo_barras, precio_detal, grupo, impuesto`) por compatibilidad.

**Conectar la plantilla al CSV (cómo se hizo)**
- La plantilla estaba conectada a Access, por eso «Examinar» solo dejaba elegir .mdb. Hay que **quitar la conexión `CB-Zebra`** en Archivo → Configuración de base de datos y **agregar una nueva de tipo archivo de texto**. Si se agrega sin quitar la vieja, BarTender pide una «Fusión de bases de datos múltiples»: no se llena, se quita CB-Zebra.

**Impresión**
- Impresora real: **4BARCODE 4B-2054TF** (USB). La de la plantilla vieja era Gainscha GS-2406T.
- Decisión: la impresora **siempre se elige en el programa** (pestaña Imprimir o «Configuración de BarTender»); si no hay ninguna, no imprime y avisa. Ya no usa la que trae guardada la plantilla.
- `bartend.exe /F=... /D=... /PRN="..." /C=1 /P /X` **funciona** con esta licencia (`/D` y `/PRN` confirmados en la práctica). Una impresión real tarda unos 7–13 s.
- Cada impresión escribe su propio CSV en `datos\etiquetas\trabajos\etiquetas_<fecha>_<id>.csv` (se guardan los últimos 30) y se pasa con `/D`. `etiquetas.csv` se sigue actualizando si se puede.
- `registro.log` anota el comando y cómo terminó BarTender (código y milisegundos).
- Rollo de **3 etiquetas a lo ancho, 3 mm de separación**: se configura en BarTender, Archivo → Configurar página → Diseño (1 fila, 3 columnas, espacio horizontal y vertical 3 mm, etiqueta de ~32 mm de ancho; página ≈ 104 mm). Pendiente confirmar medidas exactas (se pueden copiar de la plantilla original).

**Lo que NO funcionó y por qué**
- **No imprimía nada aunque decía «IMPRESO»**: BarTender respondía en menos de 1 s. Causa: BarTender abierto (editando la plantilla) e instancias ocultas de `bartend.exe` de intentos anteriores; la orden se iba a esas instancias. Solución: cerrar BarTender y finalizar los `bartend.exe` en el Administrador de tareas (pestaña Detalles) antes de imprimir.
- **`EPERM ... rename etiquetas.csv.tmp -> etiquetas.csv`**: el CSV estaba bloqueado (Excel abierto o un BarTender oculto). Solución: un CSV distinto por impresión (ver arriba).
- **El código de barras no salía**: el objeto quedó apuntando a la conexión vieja de Access o con una simbología que no aceptaba 13 dígitos. Se decidió volver a códigos de 6 dígitos; el código de barras debe estar enlazado a `codigo_barras` (Code 128).
- **CSV en una sola columna en Excel**: estaba separado por comas; Excel en español usa punto y coma.
- **Contador pegado en 077586**: se digitó mal «Seguir después del número» y el contador solo podía subir. Ahora se puede bajar (pide confirmación) y nunca repite un código con producto.

**Códigos de barras: 6 dígitos (como CRS)**
- Ya **no se generan** EAN-13 de prefijo 20 (se quitó la opción). El código generado es un consecutivo de 6 dígitos con ceros adelante: `007760`, `007761`…
- A mano se siguen aceptando códigos de fabricante de 8, 12, 13 o 14 dígitos.
- El siguiente código = mayor entre el código más alto de 6 dígitos en productos y el contador (`contador_barras`, clave `CORTO`), saltando los que tengan producto o estén reservados. Los reservados no suben el contador (los archivos de CRS traen precios de 6 cifras).
- El último código usado se guarda **también en `configuracion\opciones.json`** (`barras.ultimoCorto`); al abrir el programa o una base, el contador toma el mayor de los dos.
- «Seguir después del número» pone el contador en el número exacto; si es menor al actual, pide confirmar.

**Base inicial desde CRS**
- Archivo de CRS `ProductosPreciosInventario-2026-10-24.csv` (`;`, Latin-1; CodProducto, Referencia, Descripcion, Categoria, Costo, PDetal, PMayor…): 7.760 filas.
- Base creada: `datos\productos_inicial_CRS_2026-10-24.sqlite`, y puesta como `datos\productos.sqlite`. **7.759 productos** (se dejó fuera el genérico «00 Producto»). Último código de CRS: **007759** → el siguiente es **007760**.
- Mapeo: CodProducto → código interno y código de barras; Descripcion → nombre (espacios limpiados; las 2 con «-» quedaron como «categoría + código»); Costo, PDetal, PMayor → costo, precio detal, precio mayorista (redondeados; ~30 tenían decimales como `70721,1098`); grupo «Confecciones», IVA 19%.
- Todos quedaron marcados como exportados a Siigo («2026-10-24 (importado de CRS)»), para que «Exportar a Excel» con «solo no exportados» saque solo los nuevos.
- No se importaron: cantidad en inventario ni la categoría de CRS (Blusas, Crop Top…).
- La base de pruebas anterior quedó en `datos\copias\productos_antes_de_CRS_2026-10-24.sqlite`.

**Exportación a Siigo (aclarado)**
- «Excel para Siigo» exporta los productos **nunca exportados** (no los de la sesión). «Exportar CSV» de arriba es toda la base para Excel, no para Siigo.

**Git**
- Repo `github.com/kori496/ALTA`: el push se rechazó porque GitHub tenía commits que no estaban en local (README). Solución: `git pull --rebase origin main` (o `--allow-unrelated-histories`) y luego `git push`. No subir `datos/`, `configuracion/`, `exportados/` ni `node/` (`.gitignore`).

**Archivos cambiados**: `app\server.js`, `app\public\index.html`, `app\public\imprimir.html`, `configuracion\opciones.json`, `datos\etiquetas\etiquetas.csv`, `datos\productos.sqlite`, `plantillas\CBZebra.btw` (copia; el logo nuevo lo puso el usuario). Revisados con `node --check` y pruebas de las fórmulas; no con Playwright.

## Opción «IVA 19% ya incluido en el costo» (26 oct)
- Nueva opción en **Tipo de impuesto**, para mercancía cuyo costo ya trae el IVA. Al elegirla, el campo dice «Costo de compra (con IVA 19% incluido)».
- Cálculo: costo sin IVA = costo ÷ 1,19; precio sugerido = costo con IVA × (1 + ganancia), es decir, solo se aplica la ganancia. Ejemplo: 90.440 con IVA → 76.000 sin IVA → 117.572 → **117.900** (igual que 76.000 sin IVA con el método normal).
- Se guarda en la base como **`IVA 19%`** y con el costo **sin IVA**, así que el Excel de Siigo, el CSV y la base lo leen como cualquier producto con IVA 19%. La opción no queda guardada en el producto: al usarlo como plantilla vuelve como «IVA 19%» con su costo sin IVA.
- Cambio solo en `app\public\index.html` (constante `IVA_EN_COSTO`, `leerForm`, `calcularPrecio`, `actualizarLblCosto`, texto de ayuda en «Reglas DIAN»). Probado con Playwright en una copia local: guarda TEST1 con IVA 19%, costo 76.000, detal 117.900, base 99.075,63, IVA 18.824,37.
- La subcarpeta duplicada `AltaDeProductos\AltaDeProductos` **no** se cambió.

## Sincronizar con CRS / wwwSyncro (27 oct)
- Probado en copias: si Alta escribe el producto en `BDSCRS.mde` (4 tablas, como CRS), wwwSyncro lo lleva a todas las cajas. Detalle y pasos en [[CRS - wwwSyncro y escribir productos desde Alta]].
- Para guardar en CRS: margen como % sobre la venta, código = referencia, bodega BP, motor ACE.OLEDB.16.0 del PC.
- Pendiente: conectarlo en `server.js` y decidir qué `BDSCRS` es la real (servidor o `D:\CRS`).

## Pendiente
- [ ] **Plantilla real de Siigo (.xlsx)**: cargarla en la app, revisar la detección de obligatorias y las listas, y comparar con Excel el archivo exportado.
- [ ] Lista real de grupos de inventario, impuestos y unidades (sale de las listas de la plantilla real).
- [x] BarTender en el PC de la tienda: `/D` y `/PRN` funcionan con la licencia; .btw enlazado al CSV (24 oct, tarde).
- [ ] Enlazar el código de barras de la plantilla a `codigo_barras` (Code 128) y confirmar que se imprime.
- [ ] Configurar el rollo de 3 columnas (3 mm) en la plantilla y probar alineación.
- [ ] Confirmar que la base de CRS abre bien en el programa y que el siguiente código es 007760.
- [ ] ¿Redondear la cantidad de etiquetas a múltiplos de 3? (propuesto, sin decidir)
- [ ] Preguntar si el precio mayorista usa otra ganancia y, si sí, agregarla. (En CRS, PMayor muchas veces es igual al costo.)
- [ ] Probar el .zip en un computador de la tienda.
- [x] Probar alta, guardar, abrir la base de nuevo (24 oct, Playwright).
- [x] 100 % offline (24 oct, versión 2).

## Decisiones
- (Hasta el 23 oct) Un solo HTML, sin Python: portable y fácil de copiar.
- **24 oct: ya no tiene que ser un solo archivo.** Puede ser una carpeta instalable con todo lo necesario, para pocas computadoras (poca distribución): sin internet, con guardado automático en disco, impresión directa con BarTender y exportación a Excel que conserve el formato de la plantilla de Siigo. Antes de reescribir se propone la estructura y se espera el OK. Ver [[Prompt - seguir Alta de productos con Claude Code]].
- La base es un .sqlite que se puede guardar en OneDrive.
- **24 oct: opción A** (Node.js incluido + navegador en localhost). Como la plantilla de Siigo es personalizable, la app no fija nombres de columnas: los lee de la plantilla y se ajustan en pantalla. Se decidió exportar por defecto solo los productos no exportados (Siigo actualiza los que ya existen, así que reexportar no duplica).

- **24 oct (tarde):** códigos de barras de **6 dígitos** como CRS (se quitó el EAN-13 de prefijo 20); impresora siempre elegida en el programa; base inicial = exportación de CRS, todos marcados como ya exportados a Siigo.

## Riesgos conocidos
- (v1) Los datos viven en memoria hasta descargar la base. **Resuelto en la v2** con guardado automático.
- Dos computadores con la misma base en OneDrive al mismo tiempo: la app detecta el cambio y pide recargar, pero no mezcla datos. Usar una a la vez o prefijos de código distintos.
- Si BarTender queda abierto o con instancias ocultas, la herramienta dice «IMPRESO» pero no sale nada: cerrar BarTender y los `bartend.exe` antes de imprimir.
- La detección de obligatorias por color depende de que la plantilla use dos tonos claramente distintos; se puede corregir a mano en «Columnas de la plantilla».
