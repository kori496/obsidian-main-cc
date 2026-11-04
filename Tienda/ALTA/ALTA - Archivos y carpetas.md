---
tags: [programacion, alta, carpetas]
actualizado: 2026-10-28
---

Volver a [[ALTA - Inicio]] · mapa: [[ALTA - mapa completo.canvas|Mapa de ALTA]] · registro en [[Bitácora]]

# Archivos y carpetas

Raíz: `C:\Users\VYASotano\Downloads\AltaDeProductos_v2_2026-10-24\AltaDeProductos\`

```
AltaDeProductos/
├── app/
│   ├── server.js          servidor local (127.0.0.1): base, BarTender, CRS
│   ├── crs.ps1            trabajo con Access: lee/escribe CRS y arma el archivo de las cajas
│   ├── siigo.js           (sin uso desde el 28 oct, se puede borrar)
│   ├── node_modules/      jszip (sin uso desde el 28 oct)
│   └── public/
│       ├── index.html     la pantalla principal
│       ├── imprimir.html  la pestaña IMPRIMIR
│       └── vendor/        sql.js 1.10.3 (SQLite en el navegador, sin internet)
├── node/node.exe          Node.js incluido
├── datos/
│   ├── productos.sqlite   la base de Alta
│   ├── copias/            copias de la base con fecha (últimas 60)
│   ├── copias_wwwProductos/ copias del wwwProductos.mdb antes de cada «Sincronizar cajas» (últimas 10)
│   ├── etiquetas/etiquetas.csv + trabajos/  CSV para BarTender (últimos 30 trabajos)
│   ├── registro.log       arranques, errores, BarTender, CRS, sincronizaciones
│   └── impresiones.log    todo lo impreso, nunca se borra
├── configuracion/opciones.json   todas las opciones (ver abajo)
├── plantillas/CBZebra.btw        etiqueta de BarTender (copia de la original)
├── respaldo_antes_de_CRS/        server.js e index.html antes del 27 oct
├── respaldo_antes_de_quitar_Siigo/ server.js e index.html antes del 28 oct
├── iniciar.vbs / iniciar.bat / instalar.bat / instalar.ps1
├── README.md / LEEME.txt
```

## configuracion\opciones.json
- `puerto` (3789), `rutaBase` (vacío = `datos\productos.sqlite`).
- `bartender`: exe, plantilla .btw, impresora, copias, argumentos.
- `barras`: último código corto usado (respaldo fuera de la base).
- `formulario`: últimas opciones elegidas (IVA, unidad, grupo, ganancia, redondeo, casilla del mayorista).
- `crs`: activo, ruta de BDSCRS, proveedor, marca, categoría, www, uharc, dropbox, nombreUha, ultimaSync.
- `impresorasUsadas`, `ultimasCarpetas` (por tipo: base, btw, bartender, codigos, bdscrs, www, uharc).
- La clave vieja `siigo` se borra sola al abrir.
- Para llevar las opciones a otro PC: copiar la carpeta `configuracion`.

## Archivos externos que usa
- CRS: `\\vyasas\CRS\BDSCRS.mde`, `\\vyasas\CRS\wwwProductos.mdb`, `\\vyasas\CRS\uharc.exe`.
- Dropbox: `D:\Dropbox\CRS-BK-2019\VYA\VYAwwwProductos.uha`.
- BarTender: `C:\Program Files\Seagull\BarTender Suite\bartend.exe`.
