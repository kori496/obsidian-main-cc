---
tags: [programacion, alta, servidor]
actualizado: 2026-10-28
---

Volver a [[ALTA - Inicio]] · mapa: [[ALTA - mapa completo.canvas|Mapa de ALTA]] · registro en [[Bitácora]]

# Servidor local y seguridad (`app\server.js`)

La pantalla es una página web; el servidor (Node.js) hace lo que el navegador no puede: escribir en disco, llamar a BarTender y hablar con CRS.

## Seguridad
- Solo escucha en **127.0.0.1** (no se puede entrar desde otro PC).
- Rechaza peticiones con otro `Host` (evita que una página web use el servidor).
- Toda ruta `/api/*` exige el **token** de la sesión (se inyecta en la página al abrirla; también queda en `datos\.token`).
- Un solo trabajo con CRS a la vez (cola), con tiempo máximo (2 min; sincronizar 15 min).

## Rutas (API)
| Ruta | Para qué |
|---|---|
| `GET /api/ping` | saber si Alta ya está abierto y con qué versión |
| `POST /api/latido` | la pestaña sigue abierta |
| `GET/PUT /api/base` | leer / guardar la base .sqlite (con versión para no pisar cambios) |
| `GET /api/estado` · `POST /api/copia` | estado de la base · copia manual |
| `GET/PUT /api/config` | leer / guardar `opciones.json` |
| `POST /api/elegir` · `GET /api/elegido` | ventana de Windows para elegir archivos |
| `GET /api/impresoras` | impresoras instaladas + usadas |
| `POST /api/imprimir` | todas las impresiones (BarTender) |
| `GET /api/sesion` · `POST /api/sesion/*` | productos e historial de la sesión (pestaña Imprimir) |
| `POST /api/carpeta` | abrir una carpeta o el log |
| `GET /api/crs/estado` | Probar conexión con CRS |
| `POST /api/crs/productos` | subir productos a CRS |
| `GET /api/crs/catalogo` | leer el catálogo de CRS (Actualizar desde CRS) |
| `POST /api/crs/revisar` | Revisar Dropbox |
| `POST /api/crs/sincronizar` | Sincronizar cajas |
| `POST /api/crs/elegir` | elegir BDSCRS / wwwProductos / uharc |
| `POST /api/salir` | cerrar el programa |

## crs.ps1
Todo lo de Access lo hace `app\crs.ps1` en **PowerShell de 64 bits** con el motor **Microsoft.ACE.OLEDB.16.0** del PC. El servidor le pasa un JSON en un archivo temporal y lee un JSON de respuesta. Acciones: `estado`, `crear`, `leer`, `revisar`, `subir`. Ver [[ALTA - Conexión con CRS]].
