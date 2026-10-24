---
tags: [programacion, siigo, inventario, crs, herramienta]
actualizado: 2026-10-24
---

# Alta de productos: herramienta portable para Siigo

Volver a [[Programacion]] · registro en [[Bitácora]]

## Objetivo
Reemplazar la pantalla de creación de productos de CRS (software de inventario, cartera y facturación de Smart Data, Colombia). Cada producto nuevo se digita en una herramienta propia, queda guardado en una base de datos portable (.sqlite) y, más adelante, se exporta a un Excel listo para importar en Siigo Nube / Siigo Facturación.

## Archivo
- **Versión 2 (actual, 24 oct): carpeta instalable** en `C:\Users\sharo\OneDrive\Documentos\alta de productos\`. Paquete para otras computadoras: `paquete\AltaDeProductos_v2_2026-10-24.zip`. Ver «Versión 2» abajo.
- Versión 1 (se deja igual como referencia): `Programacion/Alta de productos/productos.html`, un solo archivo HTML. Se abre con doble clic en cualquier navegador, sin instalar nada ni Python.
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

## Pendiente
- [ ] **Plantilla real de Siigo (.xlsx)**: cargarla en la app, revisar la detección de obligatorias y las listas, y comparar con Excel el archivo exportado.
- [ ] Lista real de grupos de inventario, impuestos y unidades (sale de las listas de la plantilla real).
- [ ] BarTender en el PC de la tienda: `bartend /?`, probar `/D` y `/PRN` con la licencia, enlazar el .btw a `datos\etiquetas\etiquetas.csv`.
- [ ] Preguntar si el precio mayorista usa otra ganancia y, si sí, agregarla.
- [ ] Probar el .zip en un computador de la tienda.
- [x] Probar alta, guardar, abrir la base de nuevo (24 oct, Playwright).
- [x] 100 % offline (24 oct, versión 2).

## Decisiones
- (Hasta el 23 oct) Un solo HTML, sin Python: portable y fácil de copiar.
- **24 oct: ya no tiene que ser un solo archivo.** Puede ser una carpeta instalable con todo lo necesario, para pocas computadoras (poca distribución): sin internet, con guardado automático en disco, impresión directa con BarTender y exportación a Excel que conserve el formato de la plantilla de Siigo. Antes de reescribir se propone la estructura y se espera el OK. Ver [[Prompt - seguir Alta de productos con Claude Code]].
- La base es un .sqlite que se puede guardar en OneDrive.
- **24 oct: opción A** (Node.js incluido + navegador en localhost). Como la plantilla de Siigo es personalizable, la app no fija nombres de columnas: los lee de la plantilla y se ajustan en pantalla. Se decidió exportar por defecto solo los productos no exportados (Siigo actualiza los que ya existen, así que reexportar no duplica).

## Riesgos conocidos
- (v1) Los datos viven en memoria hasta descargar la base. **Resuelto en la v2** con guardado automático.
- Dos computadores con la misma base en OneDrive al mismo tiempo: la app detecta el cambio y pide recargar, pero no mezcla datos. Usar una a la vez o prefijos de código distintos.
- La detección de obligatorias por color depende de que la plantilla use dos tonos claramente distintos; se puede corregir a mano en «Columnas de la plantilla».
