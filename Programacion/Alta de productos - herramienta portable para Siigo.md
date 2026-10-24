---
tags: [programacion, siigo, inventario, crs, herramienta]
actualizado: 2026-10-23
---

# Alta de productos: herramienta portable para Siigo

Volver a [[Programacion]] · registro en [[Bitácora]]

## Objetivo
Reemplazar la pantalla de creación de productos de CRS (software de inventario, cartera y facturación de Smart Data, Colombia). Cada producto nuevo se digita en una herramienta propia, queda guardado en una base de datos portable (.sqlite) y, más adelante, se exporta a un Excel listo para importar en Siigo Nube / Siigo Facturación.

## Archivo
- `Programacion/Alta de productos/productos.html`: un solo archivo HTML. Se abre con doble clic en cualquier navegador, sin instalar nada ni Python.
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

## Pendiente
- [ ] Plantilla de Siigo con todos los campos (.xlsx): para fijar nombres exactos de columnas y cuáles son obligatorias.
- [ ] Exportar a Excel usando esa plantilla, llenando columnas por nombre, sin tocar el formato; partir en lotes de 500.
- [ ] Lista real de grupos de inventario, impuestos y campos (hoy son provisionales).
- [ ] Probar en el PC: alta, guardar, abrir la base de nuevo.
- [ ] Decidir si se quiere 100 % offline (incluir sql.js dentro del archivo).

## Decisiones
- Un solo HTML, sin Python: portable y fácil de copiar.
- La base es un .sqlite que se puede guardar en OneDrive.

## Riesgos conocidos
- Los datos viven en memoria hasta descargar la base. Si se cierra la pestaña sin guardar, se pierden (la herramienta avisa al salir y al abrir otra base).
- Versiones de la base: cada guardado genera un archivo nuevo; conservar la última.
