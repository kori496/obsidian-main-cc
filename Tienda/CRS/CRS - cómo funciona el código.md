---
tags: [programacion, crs, access, vba, inventario, siigo]
actualizado: 2026-10-26
---

# CRS: cómo funciona el código

Volver a [[Programacion]] · registro en [[Bitácora]] · relacionado: [[Alta de productos - herramienta portable para Siigo]]

CRS es el software de inventario, punto de venta, cartera y facturación de **Smart Data Ltda.** (Colombia) que usa V.YA. Está instalado en `D:\CRS`. Esta nota resume el análisis del código hecho el 26 oct 2026 a partir de `CRS.mdb` y `CRS.mde`.

## Resumen rápido
- **Lenguaje:** VBA (Visual Basic for Applications) dentro de **Microsoft Access 2000/2003** (formato Jet 4, `.mdb` / `.mde`). No es un programa en un lenguaje independiente.
- **¿Encriptado?** **No.** Ni la base ni el proyecto VBA tienen contraseña ni cifrado.
  - `CRS.mdb` (192 MB) trae **todo el código fuente legible**. Se extrajeron los 767 módulos completos (unas 273.000 líneas).
  - `CRS.mde` (108 MB) es la versión **compilada** que se usa en el día a día. No está encriptada: Access le borra el código fuente al compilarla y solo le deja el código ya compilado (p-code), así que no se puede leer ni editar.
- **Antigüedad:** el objeto más viejo es de 2001 y la última modificación del `.mdb` es de nov 2025.

## Archivos de la carpeta `D:\CRS`
| Archivo                                                                            | Qué es                                                                                        |
| ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `CRS.mde`                                                                          | La aplicación (pantallas, reportes y código compilado). Es la que se abre.                    |
| `CRS.mdb`                                                                          | La misma aplicación con el código fuente.                                                     |
| `BDSCRS.mde`, `BDWCRS.mde`, `BDACRS.mde`, `BDFCRS.mde`, `BDDCRS.mde`, `BDRCRS.mde` | Bases de datos **compartidas**, en el servidor `\\vyasas\CRS\`.                               |
| `BDMCRS.mde`, `BDLCRS.mde`, `BDBCRS.mde`                                           | Bases de datos **locales** de este PC (`D:\CRS`).                                             |
| `CodigosBarra.mdb`, `CB-Zebra.mdb`, `CBZebra.btw`                                  | Datos y plantilla de BarTender para las etiquetas de código de barras (tabla `Hablador`).     |
| `wwwProductos.mdb`, `wwwSyncro.mdb`                                                | Sincronización de productos con la web / otras sedes.                                         |
| `CRS-Email.exe` + `CRSEmail.mdb`                                                   | Programa aparte en **.NET Framework 4** que envía correos (facturas electrónicas al cliente). |
| `MSACCESS.EXE`, `sw\Access 2003.rar`, `sw\AccessDatabaseEngine_X64.exe`            | Access y su motor de datos, necesarios para que CRS corra.                                    |
| `dynapdf.dll`, `StrStorage.dll`, `Plugins\ImPDF.dll`, `Plugins\CS_SVG.dll`         | Librerías nativas: generar PDF y manejar SVG (QR de la factura).                              |
| `7z.exe`, `Rar.exe`, `uharc.exe`, `i_view32.exe`                                   | Comprimir copias y archivos, y convertir imágenes (IrfanView).                                |
| `*.bat`                                                                            | Tareas auxiliares (ver abajo).                                                                |

## Cómo está organizado
Es el esquema clásico de Access: **la interfaz va separada de los datos**. `CRS.mde` casi no guarda datos propios (18 tablas locales) y trabaja con **705 tablas vinculadas** a las bases `BD?CRS.mde`. Así varios equipos comparten la misma información.

### Bases de datos vinculadas
| Base | Dónde | Tablas | Para qué |
|---|---|---|---|
| `BDSCRS.mde` | servidor | 255 | **Maestra compartida:** productos, clientes, proveedores, producción, entradas de mercancía, cajas, órdenes, configuraciones. |
| `BDMCRS.mde` | local | 186 | Tablas de trabajo (`z…`, `w…`), listados e informes. |
| `BDLCRS.mde` | local | 130 | Copias locales de perfiles, configuraciones, consecutivos y tablas temporales `z…`. |
| `BDBCRS.mde` | local | 67 | Tablas temporales (`zw…`, `x…`). |
| `BDWCRS.mde` | servidor | 35 | Registro de las llamadas a internet (tablas `http…`). |
| `BDACRS.mde` | servidor | 18 | Tablas auxiliares `xx…` y cajas. |
| `BDFCRS.mde` | servidor | 7 | Facturas. |
| `BDDCRS.mde`, `BDRCRS.mde` | servidor | 3 | Domicilios y productos. |
| `CRSEmail.mdb` | local | 4 | Datos para el envío de correos. |

Convención de nombres de tablas: `z…` = temporales de trabajo, `w…` = copias para web/sincronizar, `x…`/`xls…` = exportaciones, `…S` (por ejemplo `ConfiguracionesS`, `PerfilesS`) = la versión compartida que se copia a la local al arrancar.

### Objetos de la aplicación
- **487 formularios** y **281 reportes**. Casi todo el código (unas 242.000 líneas) está **dentro de los propios formularios**, en eventos como `btnGrabar_Click` o `Form_Open`.
- Áreas según los nombres de los formularios: Productos (88), Clientes (34), Producción (34), Entradas de mercancía (24), Facturas y POS (≈47), Órdenes (14), Garantías (13), Proveedores (12), Cajas (10), Ubicaciones (10), Devoluciones, Salidas de bodega, Nómina, Préstamos, Cotizaciones, Bancos, Domicilios, Gastos, Cierres de caja e inventario.
- Formularios más grandes: `ProcesosEspeciales` (5.900 líneas), `FacturaPOSDetalle` (3.800), `EntradaMcia` (3.600), `ClientesCartera`, `ProductosRotacion`, `Productos`, `FacturasBuscarOk`, `Devoluciones`.
- **226 consultas** guardadas.

### Módulos compartidos (34)
- `Funciones` (4.900 líneas): caja de herramientas general (si un formulario está abierto, utilidades, activación de licencia, `Encriptar`/`DesEncriptar`).
- `Funciones3k`, `Funciones4k`, `FuncionesC`, `FuncionesR`, `FuncionesStr`: más utilidades (texto, reportes, etc.).
- `FacturaElectronica` (3.400 líneas), `FacturaElectronicaJ`, `FacturaElectronicaSHA1`, `FacturaElectronicaSHA384`: **facturación electrónica** con la DIAN (ver abajo).
- `Cartera`, `ProgramacionAbonosClientes`, `OrdenesDeTrabajo`, `Aportes`: lógica de negocio.
- `Permisos`: qué puede hacer cada perfil (`PAdicionar`, `PModificar`, `PBuscar`, `PImprimir`, `PExportar`, `EsAdministrador`…).
- `WebHelpers`, `WebClient`, `WebRequest`, `WebResponse`, `WebAsyncWrapper`, `IWebAuthenticator`, `JsonConverter`, `http`: librería libre **VBA-Web / VBA-JSON** (licencia MIT) para hablar con APIs REST.
- `modReportToPDF`: exporta reportes a PDF con `dynapdf.dll` + `StrStorage.dll`.
- `clsCommonDialog`, `FileDialog`: ventanas de abrir/guardar archivo.
- `mdlLlamaCalendario`, `mdlLlamarHora`, `mdlPosicionado`, `Animaciones`, `Componentes`, `Encabezado`, `ModuloRuta`, `MLlamar`: utilidades de interfaz.

## Cómo funciona al arrancar
1. Access abre `CRS.mde`, que muestra el formulario de inicio **`MenuEntrada`**.
2. En `Form_Open`, copia desde las bases compartidas a las locales: `ConfiguracionesS` → `Configuraciones`, `ObservacionesGeneralesS` → `ObservacionesGenerales` y, si cambió el consecutivo de actualización (ID 34), `PerfilesS` → `Perfiles`.
3. Pide **usuario y clave** y los valida contra la tabla de usuarios.
4. Según el perfil (módulo `Permisos`), habilita menús y botones.
5. Todo lo que el usuario hace (vender, dar de alta productos, abonos, cierres…) se graba **directamente** en las bases `BD?CRS.mde` por medio de las tablas vinculadas, con SQL (DAO `.Execute` y `OpenRecordset`).

## Licencia y activación
- Formulario `Activacion` + función `Activado()`.
- Lee el **serial del disco duro** con WMI (`Win32_PhysicalMedia`). Lo reordena, lo rellena con letras al azar y lo ofusca con `Encriptar`: una sustitución de caracteres propia basada en la tabla `nS` + XOR.
- El resultado se compara con dos seriales de activación (`s1`, `s2`, de 30 caracteres o más).
- Es una protección simple de licencia por equipo, no encriptación fuerte.
- Ninguna parte del código VBA llama a `Activado()`. Puede que se llame desde una macro o una propiedad de un formulario, o que esté desactivada. No se comprobó.

## Facturación electrónica
- Funciones principales en `FacturaElectronica`: `FE` (enviar factura), `NotaCreditoE`, `NotaDebitoE`, `NotaDCFE`, `cufe` / `DataCufe` (cálculo del CUFE), `ConsultarFechaValidacionDIAN`, `DescargarQR` / `PintarQR`, `CorreoEnviado`, `LeerJson`, `FER…` (reenvíos y consultas por fechas).
- Proveedor tecnológico: **Afacturar.com** (API REST con JSON, con la librería VBA-Web).
- Firma y hashes con las librerías de .NET llamadas desde VBA (`SHA384Managed`, `HMACSHA256`, `HMACSHA1`, `MD5`).
- El QR llega como SVG. `descargarsvg.bat` lo recorta y convierte a JPG con IrfanView y lo guarda en `Recursos\FeQr\`. `comprimir.bat` junta PDF + XML de la factura en un `.zip` (con 7-Zip) y `CRS-Email.exe` lo envía por correo.

## Relación con Siigo
CRS **no se conecta** con Siigo: no hay ninguna llamada a la API de Siigo en el código. Lo que trae son botones **SIIGO** que **exportan un archivo** (`.xls`/`.csv` en `D:\CRS`) con el formato que pide Siigo, para que el contador lo importe en la contabilidad.
- **Facturas** (formularios `FacturasBuscar` y `FacturasBuscarOk`, botón `btnSIIGO`): arma las tablas `zSIIGOFacturasListadoT` y `zSIIGODocumentosT` con número, fecha, cliente, vendedor, productos, cantidades, valores e impuestos de cada factura.
- **Compras / entradas de mercancía** (formulario `EntradaMciaBuscar`, botón `btnSIIGO`): arma `zDocumentosSIIGO` (comprobante tipo `P`) y lo exporta como `Compras-AAAAMMDDhhmmss`. Toma las cuentas contables de Siigo de la tabla `ConfiguracionesC` (columna `SIIGO`): cuentas por pagar, compras y retención.
- **Equivalencias** (formulario `ConfiguracionesSIIGOFE`, que se abre desde `FacturasBuscar`): traduce los datos de CRS a los de Siigo: tipo de comprobante, NIT del tercero, prefijo que hay que quitarle al consecutivo, códigos de impuesto, etc.
- `zSIIGONits` es una tabla auxiliar que le quita el dígito de verificación al NIT (`900123456-7` → `900123456`). La facturación electrónica también la usa, aunque no tiene nada que ver con Siigo; solo comparte el nombre.

## Tareas auxiliares (.bat)
- `CRS-Bk.bat` ("Sistema de Backup CRS v3.0"): copia `BDSCRS`, `BDFCRS` y `BDBCRS` a `E:\CRS-Bk\` y las comprime en un `.zip` con fecha y hora.
- `Compactar.bat`: compacta todas las `BD?CRS.mde` con `msaccess.exe /compact` (Access engorda los archivos con el uso).
- `wwwComprimir.bat`: comprime `wwwProductos.mdb` con uharc y lo copia a `D:\Dropbox\CRS-BK-2019\VYA\`.
- Desde el código también se lanzan `C:\Datos.bat`, `limpiarEmail.bat`, el Explorador y `ftp` (para bajar actualizaciones y recursos del FTP de Smart Data).

## Características del código
- **Estilo VBA de los años 2000.** Variables casi siempre de tipo libre: `Dim i, j, n As Integer` deja `i` y `j` como Variant. `Option Explicit` está en 515 de 767 módulos.
- 8.055 `Sub` y 319 `Function`. Errores manejados con `On Error GoTo` (unas 3.400 veces) y avisos con `MsgBox` (unas 5.800).
- Muy comentado: unas 12.600 líneas de comentarios.
- **El SQL se arma pegando texto:** unas 6.300 instrucciones `.Execute` con **DAO**, y no usa ADO. También usa mucho `DLookup` (unas 1.170 veces). Es eficiente en Access, pero difícil de mantener.
- **Llamadas al sistema:** 141 llamadas directas a Windows (`kernel32`, `user32`, `comdlg32`, `gdi32`, `WinHTTP`) y objetos como `Scripting.FileSystemObject`, `Shell.Application`, WIA para imágenes y `MSXML2.DOMDocument`.

## Puntos débiles
- **El login se puede saltar:** la consulta pega directamente lo que el usuario escribe en usuario y clave. Alguien que escriba un texto especial en esos campos puede entrar sin saber la clave.
- **Las claves no se protegen:** se comparan tal cual, así que están guardadas en texto plano en la tabla de usuarios.
- **Credenciales escritas en el código:** el usuario y la contraseña del FTP de Smart Data están dentro de un módulo (`Get2Fichero`). Cualquiera con el `.mdb` puede verlos. (No se copian aquí a propósito.)
- Hay rutas fijas a carpetas como `C:\VisualCsource\Debug\StrStorage.dll`, `C:\Datos.bat` o `E:\CRS-Bk`. Si cambian las unidades o las carpetas, esas partes fallan.

## Cómo se hizo el análisis (por si hay que repetirlo)
- No hay que instalar nada en Windows: se copió `CRS.mdb` al espacio de trabajo de Claude y se leyó con un lector propio de Jet 4 escrito en Python, porque mdbtools y oletools no se pudieron instalar.
  - Catálogo de objetos: tabla `MSysObjects`.
  - Código VBA: tabla `MSysAccessStorage` → `VBA/VBAProject` → stream `dir` (lista de módulos) y un stream por módulo, comprimidos con el formato MS-OVBA.
  - Las contraseñas: la clave de cifrado de la base (`db_key`) vale 0 y la contraseña de la base está vacía. En el stream `PROJECT`, `DPB` es corto (`787A976898689868`), así que el proyecto VBA no tiene contraseña.
- Lo que NO funcionó: instalar `mdbtools` (apt) y `oletools` / `access-parser` (pip), porque la red del espacio de trabajo los bloqueó. En el `.mde` no hay stream `dir` ni texto fuente, así que de ahí no se puede sacar código.
- El código extraído (767 archivos `.bas`) quedó solo en el espacio de trabajo de esa sesión. Si se necesita, hay que pedir que se guarde en `D:\CRS\codigo-fuente`.
