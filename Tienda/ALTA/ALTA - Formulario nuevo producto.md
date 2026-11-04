---
tags: [programacion, alta, formulario]
actualizado: 2026-10-28
---

Volver a [[ALTA - Inicio]] · mapa: [[ALTA - mapa completo.canvas|Mapa de ALTA]] · registro en [[Bitácora]]

# Formulario «Nuevo producto»

## Campos
- **Código de barras / Referencia**: un solo campo. La referencia (`codigo_interno`) es siempre el código de barras. Vacío = se genera solo al guardar (serie 27xxxx). Botón **Generar**. Ver [[ALTA - Códigos de barras]].
- **Nombre** (obligatorio): sin abreviaturas.
- **Grupo**: por defecto **Confecciones**; «Otro…» para escribir uno.
- **Tipo de impuesto**: IVA 19 % (general), IVA 19 % ya incluido en el costo, IVA 5 %, Exento, Excluido. Ver [[ALTA - Precio e impuestos]].
- **Unidad de medida** (obligatoria, por defecto Unidad).
- **Costo de compra (sin IVA)** — cambia a «con IVA 19 % incluido» si se elige esa opción.
- **Ganancia sobre el costo (%)** (por defecto 30) y **Redondeo** (por defecto «Terminar en 900») → precio sugerido y botón **Usar este precio**.
- **Precio detal (con IVA)** (obligatorio), con el desglose de base e IVA en vivo.
- **Precio mayorista (con IVA)** + casilla **«Precio mayorista igual al costo de compra»** (activada por defecto: el mayorista copia el costo tal como se escribió y queda de solo lectura).
- **INC %** (vuelve siempre a 0).

## Opciones que se recuerdan
IVA, unidad, grupo, ganancia, redondeo y la casilla del mayorista se guardan en `opciones.json` → `formulario` y se mantienen para el siguiente producto, también al cerrar y abrir.

## Botones
- **Guardar**: valida, guarda, agrega el producto a la sesión de impresión y, si está activo «Crear en CRS cada producto que guarde», lo crea en CRS.
- **Limpiar**: vacía el formulario y vuelve a las opciones recordadas.
- **Imprimir con BarTender**: imprime la etiqueta del producto del formulario.
- **Plantilla** (en la lista) → llena el formulario con nombre, grupo, costo, precios, impuesto e INC de otro producto, sin código. **Quitar** deja de usarla.

## Validaciones
- Bloquean: falta nombre o precio detal, precio negativo, código de barras repetido o reservado, código fuera de formato.
- Solo avisan: base sin IVA menor que el costo, INC distinto de 0, impuesto exento/excluido, dígito verificador GS1 que no cuadra.

## Al guardar
Mensaje «Producto guardado. Código de barras generado: 270005». Con CRS activo agrega «Creado en CRS: 270005» o el error.
