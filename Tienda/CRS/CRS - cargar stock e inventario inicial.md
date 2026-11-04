---
tags: [programacion, crs, inventario, kardex]
actualizado: 2026-10-30
---

# CRS: cargar stock e inventario inicial

Volver a [[Programacion]] · registro en [[Bitácora]] · relacionado: [[CRS - cómo funciona el código]] · mapa: [[CRS - mapa cargar stock.canvas|Mapa del proceso]]

## La ficha de Productos no carga stock (comprobado en pantalla el 30 oct)
- **Inventario → Productos** («Registro de Productos») crea la ficha. El producto queda con **Existencias = 0**.
- **Existencias** es de solo lectura: CRS la calcula con los movimientos (entradas, ventas, devoluciones, ajustes).
- **Cant Detal / Cant. Mayor / Cant. Esp. A / Cant. Esp. B** no son stock: son la cantidad a la que aplica cada nivel de precio. Se dejan en 1.
- **Stock Mínimo / Stock Máximo** son límites para alertas y pedidos, no cantidades reales.

## Cómo cargar las prendas que llegaron
1. Crear la prenda (solo si es nueva). En V.YA se hace así: Varios → **Listado de Precios de Venta** → Adicionar → buscar la última referencia → clonar → CRS asigna código nuevo → cambiar precio, descripción, etc. (otra forma: Inventario → Productos → Adicionar/Duplicar). Queda con existencias 0.
2. Inventario → **Entrada de Mercancía**: proveedor, bodega BP, factura del proveedor, referencia + cantidad + costo, grabar.
- Referencia que vuelve a llegar: solo el paso 2.
3. Varias prendas de la misma factura: crearlas todas y hacer una sola entrada.
- Mercancía que ya estaba en la tienda (stock inicial o corrección): Varios → **Ajustes de Inventario**, tipo Conteo. El conteo reemplaza la cantidad, no la suma.

## Kardex
- Inventario → Kardex de Productos: historial de un producto (fecha, documento, entra, sale, saldo).
- No se configura: se llena solo con cada documento.
- Arranque: contar todo el inventario sin ventas en curso → ajuste tipo Conteo (Importar con `Codigo` y `Existencias`) → verificar en Informe de Inventario / Kardex → desde ahí registrar todo por documento.
- Sin comprobar todavía: el formato exacto del archivo de importación del ajuste y qué pasa con los productos que no vienen en el archivo. Probar antes con 2 o 3 productos.

## Situación en V.YA (31 oct 2026)
- Los productos se crean clonando en Varios → Listado de Precios de Venta, pero **nunca se hicieron Entradas de Mercancía**. Por eso todos los productos están en 0 o en negativo: las ventas descuentan solas y nada sumó.
- Arreglo: hacer el inventario inicial (conteo general + ajuste tipo Conteo). Los productos que no estén en la tienda deben ir en el archivo con 0, para que no queden negativos.
- Desde ese día: Entrada de Mercancía cada vez que llegue mercancía.
