---
tags: [programacion, alta, precios, dian]
actualizado: 2026-10-28
---

Volver a [[ALTA - Inicio]] · mapa: [[ALTA - mapa completo.canvas|Mapa de ALTA]] · registro en [[Bitácora]]

# Precio e impuestos

## Precio sugerido
**costo sin IVA × (1 + ganancia) × (1 + IVA + INC)**, y luego redondeo.
- La ganancia es **sobre el costo** (no margen sobre el precio). Por defecto 30 %.
- Redondeo por defecto: **terminar en 900, hacia arriba**.
- Ejemplo: 76.000 → ×1,30 = 98.800 → ×1,19 = 117.572 → **117.900**.
- 50.000 → 77.350 → **77.900**.
- «Usar este precio» lo copia al precio detal; se puede escribir a mano.

## IVA 19 % ya incluido en el costo
Para mercancía cuyo costo ya trae el IVA: costo sin IVA = costo ÷ 1,19; el precio sugerido solo aplica la ganancia. Ejemplo: 90.440 con IVA → 76.000 sin IVA → **117.900**. Se guarda como **IVA 19 %** con el costo sin IVA.

## Desglose (precio con IVA incluido)
**base = precio ÷ (1 + IVA + INC)**; IVA = base × tarifa. Ej.: 117.900 → base 99.075,63 + IVA 18.824,37. Se ve en el formulario y en las columnas «Base detal» e «IVA detal».

## Tipos de impuesto
IVA 19 % (por defecto), IVA 5 %, Exento (0 %), Excluido, No gravado. Panel plegable «Reglas DIAN que aplica esta herramienta» con referencias (E.T. arts. 468, 468-1, 477, 424; Res. DIAN 000042 de 2020). No reemplaza al contador.

## Cómo lo guarda CRS (al subir)
- CodIva: 19, 5 o 0.
- Margen en `PDetal`/`PEspecial1`/`PEspecial2` = **(venta − costo) ÷ venta × 100** (no sobre el costo). Ej.: 76.000 / 117.900 → 35,54 %.
- `PMayor` = margen del mayorista (0 si el mayorista es igual al costo).
- PVEspecial1 y 2 = precio detal; PVMayor = mayorista (o el costo si no hay).
