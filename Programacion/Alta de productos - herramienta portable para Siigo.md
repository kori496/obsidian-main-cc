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
