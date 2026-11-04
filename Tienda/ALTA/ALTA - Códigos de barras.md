---
tags: [programacion, alta, codigos-de-barras]
actualizado: 2026-10-28
---

Volver a [[ALTA - Inicio]] · mapa: [[ALTA - mapa completo.canvas|Mapa de ALTA]] · registro en [[Bitácora]]

# Códigos de barras

## Formato
- **6 dígitos**, como CRS. Los de Alta van en su propia serie: **270001, 270002… hasta 279999** (la de CRS va por 0078xx con su propio consecutivo; no chocan).
- Referencia = código de barras (mismo número). Es lo que lee el escáner de la caja y lo que se imprime en la etiqueta.
- A mano también se aceptan códigos de fabricante de 8, 12, 13 o 14 dígitos (EAN/UPC).

## Nunca se repiten
- La base no deja guardar dos productos con el mismo código.
- El contador (`contador_barras`) **solo sube**; además el último usado queda en `opciones.json` → `barras`. Al abrir toma el mayor de los dos.
- Si se elimina un producto, su código queda **reservado** (`barras_reservadas`).
- Los códigos extra de CRS (cuando un producto tiene más de una referencia) también se reservan al [[ALTA - Actualizar desde CRS|actualizar desde CRS]].
- «Cargar códigos existentes (CSV o TXT)…»: toma todo número de 8 a 14 dígitos de un archivo y lo reserva.

## Panel «Código de barras propio»
- Casilla «Generar automáticamente al guardar si lo dejo vacío» (activada).
- **Seguir después del número** + Aplicar: fija desde dónde sigue la serie; solo acepta 270000 a 279998. Si es menor que el actual pide confirmar y nunca repite un código con producto.
- Muestra el último usado y el siguiente.

## Historia
EAN-13 con prefijo 20 (23 oct) → 6 dígitos siguiendo a CRS desde 007760 (24 oct) → serie propia **27xxxx** (27 oct) porque las etiquetas de Alta chocaban con códigos que CRS ya había asignado (ej. 007764).
