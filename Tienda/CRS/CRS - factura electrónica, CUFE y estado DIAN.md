---
tags: [programacion, crs, facturacion-electronica, dian, cufe]
actualizado: 2026-10-30
---

# CRS: factura electrónica, CUFE y estado DIAN

Volver a [[Programacion]] · registro en [[Bitácora]] · relacionado: [[CRS - cómo funciona el código]]

Leído el 30 oct 2026 del código fuente de `D:\CRS\CRS.mdb` (copia de solo lectura; en `D:\CRS` no se cambió nada). Ojo: lo que se usa a diario es `CRS.mde`. El `.mdb` es de nov 2025 y se supone que tiene el mismo código, pero no se puede comprobar.

## Dónde se guarda si una factura se envió
- Tabla **`FacturasFE`** (base BDFCRS): una fila por cada factura que el proveedor (Afacturar) aceptó. Columnas: `Cufe`, `IdFacturaFE`, `prefijo`, `url_representacion_qr_svg`, `url_xml`, `url_rg`, `url_notificacion_aceptacion_rechazo`, `FechaValidacionDIAN`, `IdResolucion`, `fecha_envio_correo`.
- Para CRS, una factura **es electrónica** solo si tiene fila en `FacturasFE` (función `EsFacturaElectronica`). Si no hay fila, no se envió o el envío no quedó guardado.
- `FechaValidacionDIAN` sale del XML que devuelve el proveedor (`<cbc:ValidationDate>` + `<cbc:ValidationTime>`). Lo lee `ConsultarFechaValidacionDIAN`, desde la carpeta de Configuraciones Id 101 (`…\FeQr\<IdFactura>.xml`).
- `fecha_envio_correo` vacía = no se envió el correo al cliente.

## En Búsqueda de Facturas (formulario `FacturasBuscar`)
- **Columna FE**: muestra **`@`** si la factura tiene fila en `FacturasFE`. Si está vacía, no se envió.
- **Botón Limpiar FE** (`btnLimpiarFE`): quita de la lista las que tienen `@`, así quedan solo las pendientes. No borra nada de la base, solo la lista temporal `zFacturasListado`.
- **Botón FE en bloque** (`btnFEBloque` → `FacturasBuscarFEBloque`): envía a la DIAN todas las facturas de la lista. Para cada una: `PrepararDataCufe` → `FE` → guarda en `FacturasFE` → `DescargarQR` → `ConsultarFechaValidacionDIAN`. Al final dice cuántas salieron bien y muestra los números de las que fallaron. Conviene usar Limpiar FE antes para no reenviar las que ya tienen `@`.
- **Botón FE Control** (`btnFeControl` → `FEControl`): revisión contra el proveedor.
  1. Al abrir, copia las facturas de la lista a `zCRSFEControl`.
  2. **Buscar**: por cada factura le pregunta a Afacturar (`FER2`, API `transacciones_emitidas_v3`, por prefijo + número) y llena tipo de documento, CUFE, cliente, fecha, XML y QR. Marca `FER` = sí cuando la factura ya está en `FacturasFE`.
  3. Mensajes: «Hay N Pendientes» = Afacturar no tiene esas facturas (no se enviaron; botón **ver** las filtra). «Hay N Pendientes» por inyectar = Afacturar sí las tiene, pero CRS no las guardó en `FacturasFE`.
  4. **Inyectar** / **Inyectar todas**: escribe en `FacturasFE` la respuesta que trajo de Afacturar (CUFE, QR, XML), baja el QR y la fecha de validación. Arregla las facturas que sí se enviaron y no quedaron marcadas.
  5. Doble clic en el CUFE: lo copia y abre la página de consulta (URL en `ConfiguracionesFE` Id -2, con `+cufe` reemplazado por el CUFE).

## Al abrir una factura (formulario `FacturasConsulta`)
- Si es electrónica, se ven la etiqueta **Factura Electrónica** y el botón **DIAN**.
  - **DIAN** (`btnDian`): copia el CUFE y abre la consulta en la página configurada (normalmente la de la DIAN). Si el CUFE está vacío: «Por Favor Descargue la Respuesta Nuevamente».
  - Clic en la etiqueta Factura Electrónica: vuelve a bajar el QR.
- Etiqueta **correo no enviado** (`lblCorreoNoEnviado`) si `fecha_envio_correo` está vacía.
- Botones de reintento (`btnFail` / `btnFail2`): «¿Desea descargar la respuesta de la Factura Electrónica nuevamente?». Consultan Afacturar (`FER` y luego `FER2`) y vuelven a guardar la fila en `FacturasFE`. Si responde «La Respuesta no ha podido ser verificada», Afacturar no la tiene.
- Botón de enviar una sola factura (`btnCRSFE`): «¿Desea Facturar Electrónicamente Este Documento?» → `PrepararDataCufe` → abre `FacturasConsultaFE`, que llama a `FE`.
- Doble clic en el número de factura: muestra el CUFE guardado y el que calcula CRS (`cufe()`, SHA-384), para compararlos.

## Posible fallo encontrado (sin probar)
En `FacturasConsultaFE` (envío de una sola factura desde la consulta), `BD` se declara pero nunca se le asigna la base (`Set BD = …`). Si `FE` sale bien, el `BD.Execute` siguiente debería dar el **error 91** («Variable de objeto… no establecida»). En ese caso la factura sí llegó a Afacturar, pero no se guardó en `FacturasFE`: queda sin `@` y sin botón DIAN. Se arregla con FE Control → Buscar → Inyectar, o con el botón de descargar la respuesta. Si al enviar una factura sola sale el error 91, es esto. (En `FacturasBuscarFEBloque` sí está el `Set BD`, así que el envío en bloque no tiene este problema.)

## Error: el tiquete POS sale sin CUFE pero en el historial aparece `@` (30 oct)
**Causa (leída en el código y en la configuración de la caja 1, este PC):**
- El tiquete POS (reportes de factura POS) pone el CUFE con `=DLookUp("[Cufe]","FacturasFE","[IdFactura]=" & [idfactura])`, es decir, lo lee de `FacturasFE` **en el momento de imprimir**.
- Orden al cobrar con F10 (`FacturaPOSPago`): `GuardarFactura` → al final abre `FacturaPOSPagoFE` → luego `ImprimirFactura`.
- `FacturaPOSPagoFE` mira `ConsecutivosLocales` Id 103 («Fe.Net») en la base local BDLCRS:
  - 0 = no hace factura electrónica.
  - 1 = **FE-CRS**: CRS la envía en ese momento a Afacturar y guarda `FacturasFE` antes de imprimir.
  - 2 = **FE.Net**: CRS **no la envía**. Solo escribe el JSON en la carpeta `…\JSon` y una fila en `FacturasFENet`. Otro programa (FE.Net, no está en `D:\CRS`) la envía después y escribe `FacturasFE`.
- En este PC (caja 1) el valor es **2 (FE.Net)**. Por eso el tiquete se imprime antes de que exista el CUFE (sale vacío). Minutos después FE.Net la envía, se crea la fila en `FacturasFE` y en Búsqueda de Facturas aparece `@`.
- Conclusión: la factura **sí se envió**, pero después de imprimir. El `@` es correcto y lo que queda viejo es el tiquete. Para comprobarlo, abre la factura y usa el botón DIAN (o doble clic en el número para ver el CUFE).

**Qué se puede hacer:**
- Ya: reimprimir desde Búsqueda de Facturas cuando tenga `@`. La reimpresión (`ImprimirFactura` en `Funciones`) vuelve a leer el CUFE y también llama a `PintarQR`.
- Cambiar la caja a modo 1 (FE-CRS) haría que el CUFE salga en el primer tiquete, pero el cobro espera la respuesta de Afacturar y, si FE.Net sigue corriendo, podría intentar enviar la misma factura dos veces. Hablarlo con Smart Data antes; no se cambió nada.
- Ojo también con el QR: la impresión POS no llama a `PintarQR`. El reporte usa la imagen fija `D:\CRS\qr.png` (en este PC es de ene 2023), así que en el primer tiquete el QR tampoco es el de esa factura.

## Quién sube las facturas a la DIAN (30 oct)
Cadena en modo FE.Net (el de la caja 1): **CRS → FE.Net → Afacturar.com → DIAN**.
- **CRS** no envía nada en este modo. Arma el JSON en la carpeta `…\JSon` y deja la factura en la cola `FacturasFENet` (tabla del **servidor**, `\\vyasas\CRS\BDSCRS.mde`, con columnas `IdFactura`, `RutaJson` y `Correo`).
- **FE.Net** es un programa aparte que recoge esa cola y manda cada JSON a Afacturar. CRS no lo abre ni lo llama, y no está en `D:\CRS`: debe correr en el servidor `vyasas` u otro PC. Por el nombre y por cómo está hecho (como `CRS-Email.exe`, en .NET) parece de Smart Data, pero no se ha confirmado.
- **Afacturar.com** es el proveedor tecnológico: el que firma la factura y la transmite a la DIAN. La URL y el ambiente (`tipo_ambiente_dian`: 1 = producción, 2 = pruebas) están en `ConfiguracionesFE` (servidor, BDSCRS).
- El acceso a `\\vyasas\CRS` fue denegado; no se pudo ver la cola ni la configuración.

### Por qué podría haber `@` sin que la DIAN tenga la factura
- `@` solo significa que hay una fila en `FacturasFE`, es decir, que **Afacturar** respondió con un CUFE. No prueba que la DIAN la haya validado.
- `LeerJson` acepta como buena la respuesta de Afacturar con `codigo_error` 0 y también con **15**.
- Mirar `FechaValidacionDIAN` en `FacturasFE`: si está vacía, la DIAN no la validó.
- Si `tipo_ambiente_dian` = 2, las facturas van al ambiente de **pruebas** y nunca llegan a la DIAN real, aunque tengan CUFE y `@`.

## Cómo se sacó el código (para repetirlo)
- Copia de `CRS.mdb` al espacio de trabajo de Claude y lector propio de Jet 4 en Python: tabla `MSysObjects` (tdef 2) → `MSysAccessStorage` (tdef 149) → `VBA/VBAProject/VBA/dir`, más un stream por módulo, descomprimidos con MS-OVBA. Salieron 767 módulos sin errores.
- pip sigue sin poder instalar `access-parser` (red bloqueada).
