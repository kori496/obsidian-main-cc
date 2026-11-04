---
tags: [programacion, alta, base-de-datos]
actualizado: 2026-10-28
---

Volver a [[ALTA - Inicio]] · mapa: [[ALTA - mapa completo.canvas|Mapa de ALTA]] · registro en [[Bitácora]]

# Base de datos y guardado

## Dónde vive
- La base es un archivo **SQLite**: `datos\productos.sqlite` (o la ruta elegida en «Cambiar ubicación», por ejemplo OneDrive).
- La pantalla la abre en el navegador con **sql.js**; cada cambio se manda entero al servidor y se escribe en disco.

## Tablas
- `productos`: `id`, `codigo_interno` (en pantalla «Referencia», único), `codigo_barras` (único si no está vacío), `nombre`, `grupo`, `unidad`, `costo` (siempre **sin IVA**), `precio_detal`, `precio_mayorista`, `impuesto`, `inc`, `creado`, `en_crs` (fecha en que se subió o se encontró en CRS), `exportado_siigo` (vieja, sin uso).
- `barras_reservadas`: códigos que no se pueden volver a usar (`eliminado`, `crs`, cargados de un archivo).
- `contador_barras`: el consecutivo de los códigos generados (nunca baja).
- Las bases viejas se **migran solas** al abrir (columnas `unidad`, `en_crs`).

## Guardado automático
- Arriba a la derecha: «Guardando…» → «Guardado hh:mm». Si falla: «No se guardó (clic para reintentar)».
- **Escritura segura**: escribe un `.tmp`, lo renombra (reintenta si OneDrive o el antivirus bloquean) y **relee el archivo** para verificar que quedó igual.
- **No pisa cambios ajenos**: si otra ventana u otro PC cambió la base, pide recargar (F5).

## Copias de seguridad
- En `datos\copias\productos_AAAA-MM-DD_HHMMSS[_motivo].sqlite`: al abrir el programa, cada hora de trabajo, antes de «Abrir otra base…» y con «Hacer copia ahora». Se guardan las **últimas 60**.
- Para volver atrás: cerrar Alta y copiar una de esas copias como `datos\productos.sqlite`.

## Botones
- **Abrir otra base…**: usa un .sqlite viejo como base de trabajo (antes hace copia de la actual; el archivo elegido no se modifica).
- **Descargar copia**: baja la base al navegador.
- **Cambiar ubicación** (Configuración → Base de datos): si en la nueva ruta no hay base, copia la actual allá.
- Si dos PCs usan la misma base en OneDrive: no trabajar a la vez.

## Base inicial
Se creó el 24 oct desde la exportación de CRS (7.759 productos, `datos\productos_inicial_CRS_2026-10-24.sqlite`). Ahora se mantiene al día con [[ALTA - Actualizar desde CRS]].
