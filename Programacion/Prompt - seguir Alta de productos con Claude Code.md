---
tags: [programacion, siigo, inventario, prompt]
actualizado: 2026-10-24
---

# Prompt para seguir «Alta de productos» con Claude Code (VS Code)

Volver a [[Programacion]] · proyecto en [[Alta de productos - herramienta portable para Siigo]] · registro en [[Bitácora]]

Pegar tal cual en Claude Code, abierto en la carpeta `C:\Users\sharo\OneDrive\Documentos\obsidian\main cc`. Si ya tienes la plantilla de Siigo, déjala en esa carpeta y menciona su nombre en el punto 1.

Cambio del 24 oct: el proyecto ya no tiene que ser un solo archivo HTML. Puede ser una carpeta instalable, pensada para pocas computadoras.

```
Vamos a seguir el proyecto «Alta de productos» de mi tienda de ropa. Responde en español, directo y corto.

ANTES DE EMPEZAR
- Lee CLAUDE.md de este vault y la nota Programacion/Alta de productos - herramienta portable para Siigo.md (tiene el historial, las decisiones y lo pendiente).
- Abre Programacion/Alta de productos/productos.html. Es la versión actual y la referencia de todo lo que ya funciona.

QUÉ ES
Una herramienta que reemplaza la pantalla de creación de productos de CRS. Guarda los productos en una base SQLite y debe terminar generando un Excel que Siigo Nube pueda importar. Las etiquetas se imprimen con BarTender. Hoy es un solo archivo HTML (JavaScript sin build; sql.js desde cdnjs; hay que descargar el .sqlite a mano para guardar).

FORMATO NUEVO (decisión del 24 oct)
- Ya no tiene que ser un solo archivo. Puede ser una carpeta con todo lo necesario, instalable con doble clic (por ejemplo instalar.bat / iniciar.bat y un acceso directo), en Windows.
- Es para POCA DISTRIBUCIÓN: unas pocas computadoras de la tienda. No necesita tienda de aplicaciones, firma de código ni actualizaciones automáticas; sí un .zip y unas instrucciones cortas de instalación.
- Debe funcionar SIN internet: sin CDN, todas las librerías dentro de la carpeta.
- Los datos deben guardarse solos en disco (hoy se pierden si cierro la pestaña sin descargar el .sqlite) y hacer copia de seguridad con fecha. Debe seguir leyendo mis .sqlite actuales.
- Aprovecha que ahora hay programa local: imprimir directo con BarTender (que la app ejecute bartend.exe, sin descargar CSV y .bat) y escribir el Excel de Siigo con una librería que conserve el formato de la plantilla, sin depender del navegador.
- ANTES de programar, propón en pocas líneas 2 o 3 opciones de estructura (por ejemplo: app local con Node.js y node.exe incluido en la carpeta, con la interfaz en el navegador en localhost; alternativas con Python o con una app de escritorio), con pros y contras para este caso, recomienda una y espera mi OK. No empieces a reescribir hasta que te responda.
- Reutiliza la lógica y la interfaz de productos.html; no rehagas lo que ya funciona.

YA HECHO (en productos.html)
- Formulario: referencia (la columna de la base se llama codigo_interno), código de barras, nombre, grupo (Confecciones por defecto u «Otro…»), unidad de medida, impuesto, costo sin IVA, ganancia, precio detal y mayorista con IVA incluido.
- Botón «Plantilla» por producto: copia sus datos a uno nuevo sin referencia ni código de barras.
- Impuestos: IVA 19% (por defecto), IVA 5%, exento, excluido, no gravado; INC solo avisa. Desglose en vivo: base = precio / (1 + IVA + INC).
- Precio desde el costo: costo sin IVA x (1 + ganancia) x (1 + IVA), con ganancia 30% sobre el costo y redondeo hacia arriba a terminación 900. Ejemplo: 76.000 -> 98.800 -> 117.572 -> 117.900.
- Código de barras propio: EAN-13 con prefijo 20 a 29 + consecutivo de 10 dígitos + dígito verificador GS1. Índice único en la base, contador que nunca baja, códigos de productos eliminados reservados y carga de códigos existentes de CRS o Siigo.
- Guardar y abrir la base .sqlite (migra bases viejas), exportar CSV, e imprimir con BarTender mediante un CSV y un .bat que llama a bartend.exe.

PENDIENTE (en este orden)
0. Proponer la estructura de la carpeta (ver FORMATO NUEVO) y esperar mi OK.
1. Exportar a Excel con la plantilla oficial de Siigo (se descarga en Siigo: Configuración -> Productos y servicios -> Importación -> Productos y Servicios -> Crear plantilla; si no la tienes, pídemela antes de seguir). Reglas de Siigo: llenar las columnas por su nombre exacto, sin modificar, borrar ni agregar columnas ni fórmulas; encabezados azul oscuro = obligatorios; máximo 500 registros por archivo (partir en lotes); el grupo de inventario debe existir ya en Siigo; los combos no se importan. Usa una forma de escribir el .xlsx que NO dañe el formato de la plantilla (prueba con la plantilla real y compara). Valida las obligatorias antes de exportar y avísame qué productos fallan.
2. Probar la herramienta de verdad, abierta y usada (hasta ahora solo se probó la lógica y el SQL): crear producto, generar código, guardar, reabrir, usar plantilla, eliminar, cargar códigos reservados. Si puedes, automatiza con Playwright.
3. Verificar la impresión con BarTender: confirmar con `bartend /?` los parámetros de línea de comandos (/F, /D, /PRN, /C, /P) y que la plantilla .btw lea los datos (campos: referencia, nombre, codigo_barras, precio_detal, grupo, impuesto).
4. Preguntarme si el precio mayorista usa otra ganancia y, si sí, agregarla.
5. Preparar el paquete: carpeta final, instalador, instrucciones cortas y .zip para llevar a otra computadora; probar la instalación en limpio.

REGLAS
- No cambies el nombre de la columna codigo_interno y mantén la compatibilidad con bases .sqlite viejas (migraciones con ALTER TABLE). Deja productos.html como está hasta que la versión nueva funcione.
- No borres ni sobrescribas mis archivos .sqlite ni mis notas sin avisarme.
- No inventes códigos ni reglas de la DIAN. Los tipos de impuesto de cada referencia los confirma mi contador; las referencias normativas del panel de la herramienta están por verificar.
- Después de cada cambio: revisa la sintaxis, prueba la lógica con casos reales y dime qué probaste y qué no.
- Al terminar: actualiza la nota del proyecto y añade una entrada en Bitácora.md. Después de guardar en este PC, verifica el tamaño o el contenido del archivo: a veces el primer guardado no se aplica y vuelve una versión vieja.
- Si algo es ambiguo y barato de rehacer, decide y anótalo; si es caro de rehacer, pregúntame.
```
