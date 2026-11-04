---
tags: [programacion, alta, decisiones]
actualizado: 2026-10-28
---

Volver a [[ALTA - Inicio]] · mapa: [[ALTA - mapa completo.canvas|Mapa de ALTA]] · registro en [[Bitácora]]

# Decisiones e historial

| Fecha | Qué |
|---|---|
| 23 oct | v1: un solo HTML con SQLite en el navegador (sql.js), sin Python. Referencia, grupo Confecciones, precio desde el costo, reglas DIAN, EAN-13 propio. |
| 24 oct | **v2: carpeta instalable** con Node.js incluido y la pantalla en el navegador (`127.0.0.1:3789`). Guardado automático, copias, BarTender directo, pestaña IMPRIMIR, historial y log. Códigos de **6 dígitos** como CRS. Base inicial desde la exportación de CRS. Impresora siempre elegida en el programa. |
| 26 oct | Opción «IVA 19 % ya incluido en el costo». Análisis de CRS (Access + VBA). |
| 27 oct | Referencia = código de barras (un solo campo). Mayorista = costo (casilla). Opciones recordadas. Selección múltiple. Serie **27xxxx**. Conexión con CRS: crear en CRS, Sincronizar cajas, Revisar Dropbox, Actualizar desde CRS. |
| 28 oct | Botón **Subir productos** con lista. **Se quitó Siigo** (no se compró). |

## Decisiones vigentes
- Base real de CRS: `\\vyasas\CRS\BDSCRS.mde`. Este PC hace la sincronización.
- Si un dato difiere entre Alta y CRS, **manda CRS**.
- Sincronizar solo hasta Dropbox, **sin el FTP** de Smart Data.
- Se acepta que Alta escriba en CRS (agregar productos) y en `wwwProductos.mdb`. BDSCRS se abre solo lectura en lo demás.
- Alta nunca borra ni modifica productos existentes en CRS.
- Mantiene una sola persona; repo privado `kori496/ALTA` (no subir `datos/`, `configuracion/`, `exportados/`, `node/`).
