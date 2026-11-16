---
tags: [programacion, python, aprendizaje]
actualizado: 2026-11-12
---

Volver a [[Programacion]]

# 🐍 Curso de Python: progreso

El curso está en Notion: página **pythn** → "Curso de Python desde cero". El orden que sigo es el de "Ruta para ti (empieza aquí)", no el de 1 a 26. Lo que entendí en cada módulo lo anoto en el registro de esa página.

## Dónde voy (12 nov 2026)
- Etapa 1 ("dejar de depender"): M8 Errores ✅ · M16 Depuración ✅ · M7 Funciones ✅ · M12 Git ✅ · M17 pytest ✅.
- Etapa 2: **M13 Clases en curso**. Hechos los ejercicios 1 (clase `Producto`) y 2 (métodos `esta_agotado` y `vender`) en `practica_git/clases.py`. Siguiente: `__str__` (por qué `print(falda)` sale raro).
- Pendiente en todos los módulos: el ejercicio "En tu propio código", que es aplicar lo aprendido en el inventario ([[ALTA - Inicio]]).
- Práctica en `C:\Users\sharo\OneDrive\Documentos\curso cc\practica_git` (repo `practica_git` en GitHub). Corro `pytest` desde **dentro** de `practica_git`, con el venv activado.

## M17 pytest: errores que resolví (5 nov)
Resultado final: `14 passed` (`test_inventario.py` + `test_numeros.py`).

1. **`fixture 'productos' not found`**: tenía tres causas juntas.
   - Escribí `pytest.fixture` sin la `@`. Sin la arroba la línea no hace nada.
   - Las funciones de `inventario.py` se llamaban `test_valor_total`, etc. Pytest toma como test **toda función que empiece por `test_`**, así que las corría como tests y les buscaba la fixture.
   - En `test_inventario.py` importaba esos "tests" en vez de las funciones.
   - **Arreglo:** `inventario.py` solo tiene el código (`valor_total`, `mas_caro`, `mas_barato`). `test_inventario.py` tiene el `import`, la `@pytest.fixture` y los `def test_...` con `assert`.
2. **Solo corría 1 test:** los otros dos no estaban escritos. Si un test no aparece en `pytest -v`, revisar que exista, que empiece por `test_` y que el archivo esté guardado.
3. **`assert 'VES-02' == 95000`:** comparaba el SKU (texto) que devuelve la función con un precio (número). La línea `E` muestra a la izquierda lo que devolvió la función y a la derecha lo que yo esperaba.

## M17 pytest: ejercicio "test primero" (12 nov)
Resultado final: `15 passed`. `mas_caro` ahora ignora los productos con `stock: 0`.

1. **Un test puede pasar por suerte.** `mas_caro` tenía `p['stock'] > mejor['stock']` (más stock *que el mejor*, no "tiene stock"). Pasaba solo porque FAL-03 tenía más unidades que BLU-01. Se destapó con un test con otra lista (BLU-01 con `stock: 5`).
2. **La fixture es compartida.** Puse la lista nueva en la fixture y se rompió `test_valor_total` (`685000 == 445000`). Si un test necesita datos distintos, la lista va **dentro de ese test** (sin pedir la fixture).
3. **El signo al revés.** `p['stock'] <= 0` elegía el agotado (`'VES-02' == 'FAL-03'`). Lo correcto: `p['stock'] > 0`. Truco: leer la condición en voz alta y preguntar "¿describe lo que quiero o lo que no quiero?".
4. No hacía falta una función nueva `mas_caro_ignora_sin_stock` en `inventario.py`: el test nuevo prueba la misma `mas_caro`.
5. Lo que me faltaba: **filtrar una lista** (`for` + `if` + `append`, o `[p for p in lista if ...]`).

## M13 Clases: lo que entendí y errores (12 nov)
- Clase = molde; objeto = cada galleta. `self` = la galleta que se está creando o usando, **nunca el molde**. Desde afuera se llama `falda`; desde adentro, `self`.
- Python pone `self` solo, por eso `__init__(self, sku, nombre, precio, stock)` recibe 4 valores y no 5.
- **Orden de argumentos:** `Producto('CAM-02', 90000, 5, 'Camisera')` guardó el precio en `nombre` y el nombre en `stock`, y no dio error (Python solo cuenta cuántos llegan). Arreglo: mismo orden que el `__init__` o usar nombres (`precio=...`).
- `-=` es una orden, no un valor: no va con `return`. Lo que va a la izquierda es lo que cambia: `self.stock -= cantidad`.
- **`assert` ≠ `raise`.** `assert ValueError(...)` no avisa nada; para lanzar el error es `raise ValueError(...)`.
- `None` = la función terminó sin `return`. Una comparación ya es un valor: `return self.stock == 0` (no hace falta escribir `True`/`False` a mano).

## Ideas para seguir
- Caso que aún falla: si el **primer** producto es el más caro y tiene `stock: 0`, `mejor = productos[0]` nunca cambia. Probarlo con un test y arreglarlo filtrando la lista antes de buscar el máximo.
- En `test_numeros.py` ya uso `@pytest.mark.parametrize`, con casos borde (precio 0, descuento del 100 %).
