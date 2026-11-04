---
tags: [bitacora]
actualizado: 2026-11-03
---

# 📓 Bitácora

Registro corto de lo que Claude hace en este vault. Lo más reciente arriba. Reglas en `CLAUDE.md`.

## 2026-11-03 (unión de los dos vaults y carpetas por tema)
- Se unió el vault de Documentos con la copia de GitHub que estaba en Descargas (`obsidian-main-cc-main`). Las dos versiones se habían separado desde el 22 oct.
  - Traído de Descargas: ALTA (17 notas + canvas), notas de CRS, Prendas 95–119, scripts de stories/videos (24 oct – 3 nov), [[Referencias de stories de otras tiendas]], [[Video de stories (receta)]], 85 fotos nuevas en `Adjuntos/`, `logo_mask.png`, la carpeta `analitica` y el fragmento CSS de colores.
  - Unidas a mano (cambios de los dos lados): esta Bitácora, [[Alta de productos - herramienta portable para Siigo]], [[Edición de imágenes]], [[Programacion]], `Mapa Alta de productos.canvas`, `appearance.json`. En las demás se dejó la versión más completa.
- **Carpetas físicas por tema** (era el pendiente del [[Resumen reciente 21-25 oct 2026]]): `Multimedia/` (con `Recetas de video/`, `Beats/`, `Archivos/`), `Redes/`, `Webs/` (con `analitica/`), `Edicion de imagenes/` (igual), `Tienda/` (`ALTA/` y `CRS/`), `Programacion/`, `Herramientas y IA/`, `Sistema/`. La carpeta `Mapas/` desapareció: cada mapa quedó dentro de su carpeta.
- Rutas escritas actualizadas en notas, canvas, `CLAUDE.md`, `Inicio.md`, `.gitignore` (`Webs/analitica/`), colores del grafo y del explorador (`colores-vault.css`, activado).
- Los archivos viejos que se reemplazaron quedaron en `Descargas\obsidian-main-cc-main-...\_reorganizacion\respaldo\`. Se borró `....md` (vacío).

## 2026-11-03 (V.YA: 7 imágenes y 5 videos en `vya contenido\ia`)
- 7 stories con prendas sin editar de la sesión 19 oct (97, 98, 101, 104, 105, 109, 110) y 5 videos (clips de tienda de hoy + modelo 29 oct + fotos 19 oct), todos con formatos nuevos. Archivos `VYA_IA_*` en `Documents\vya contenido\ia`.
- Scripts nuevos: `Edicion de imagenes/Scripts/stories_03nov.py` y `videos_03nov.py`. Notas tocadas: [[Pendientes]] (registro de lotes) y [[Video de stories (receta)]] (variantes 3 nov y errores).
- No le gustó el video 4 (fotos fijas en movimiento): anotado como formato a no repetir en [[Preferencias de estilo]] y [[Video de stories (receta)]].

## 2026-10-30 (CRS: tiquete POS sin CUFE con `@` en el historial)
- Causa: la caja 1 está en modo FE.Net (`ConsecutivosLocales` 103 = 2 en BDLCRS). CRS imprime el tiquete antes de que FE.Net envíe la factura, y el CUFE del tiquete se lee de `FacturasFE` al imprimir. Después llega el envío y aparece `@`. Solución inmediata: reimprimir desde el historial. Cambiar a modo 1 (FE-CRS), solo después de hablar con Smart Data.
- Se leyeron copias de `CRS.mdb` y `BDLCRS.mde`; `D:\CRS` no se tocó. Nota actualizada: [[CRS - factura electrónica, CUFE y estado DIAN]] (sección del error).

## 2026-10-30 (CRS: estado DIAN en el historial de facturas)
- Leído el código de `D:\CRS\CRS.mdb` (copia de solo lectura, sin tocar `D:\CRS`): cómo CRS marca una factura como enviada a la DIAN (tabla `FacturasFE`, columna FE `@` en Búsqueda de Facturas), FE en bloque, FE Control (Buscar / Inyectar), botón DIAN y correo no enviado.
- Nueva nota [[CRS - factura electrónica, CUFE y estado DIAN]], enlazada desde [[Programacion]].
- Hallado (sin probar): en `FacturasConsultaFE` falta `Set BD`, así que enviar una factura sola podría dar error 91 y no guardarla en `FacturasFE` aunque sí haya llegado a Afacturar.
- No funcionó: el primer pedido de acceso a `D:\CRS` fue denegado (luego el usuario conectó la carpeta); pip sigue sin `access-parser`.

## 2026-10-29 (V.YA: video + 12 stories de la sesión del 29 oct)
- Video de 28 s (9:16, 11 planos de 2,5 s, cortes secos, logo chico abajo al centro, sin texto ni música) con los clips de `Documents\IA SOURCE IMAGES`. Nueva nota [[Video de stories (receta)]], enlazada desde [[Edición de imágenes]].
- 12 stories 1080×1920 con 12 formatos nuevos, hechas con fotogramas nítidos de los videos de la modelo (IMG_1569–1603) y las fotos del jean floral. Script `Edicion de imagenes/Scripts/stories_29oct.py`. Todo en `IA SOURCE IMAGES\editados_29oct`. Registrado en [[Pendientes]].
- No funcionó: pedir acceso a `Documents\obsidian vya` y `Documents\assets` (denegado); el vault se leyó desde `Downloads\obsidian-main-cc-main`. El video a `-crf 18` pesó 37 MB y no se podía copiar al PC (límite 30 MB): se exportó a `-crf 22`.

## 2026-10-29 (V.YA: análisis de stories de referencia)
- Analizadas 41 stories (25 videos, 16 fotos) de dyaboo, maemi y skarcha en `Documentos\referencias vya stories`: formatos, ritmo de video, tipografía, CTA y qué llevar a V.YA.
- Nueva nota [[Referencias de stories de otras tiendas]] con tableros de fotogramas en `Edicion de imagenes/Adjuntos/refs-stories/`. Enlazada desde [[Edición de imágenes]].
- Hallazgo principal: la calidad viene del set real, de mostrar la prenda en varios colores + detalle, y del texto corto en dos tipografías; los videos de gancho y maniquí de skarcha sirven sin modelo.
- Copiado a Notion como subpágina de V.YA: [Análisis de stories de referencia](https://app.notion.com/p/408d722a78338125a705e114f28264ef). Solo texto: las imágenes no se pudieron subir a Notion desde la sesión (red bloqueada), quedan en Obsidian.

## 2026-10-28 (ALTA: canvas y notas por parte)
- Nuevo canvas [[ALTA - mapa completo.canvas|Mapa de ALTA]] y 17 notas en `Programacion/ALTA/`, una por parte: inicio, instalación y arranque, archivos, servidor, base de datos, formulario, precio e impuestos, códigos de barras, lista, eliminar, BarTender, conexión con CRS, subir a CRS, actualizar desde CRS, sincronizar cajas y Revisar Dropbox, decisiones, pruebas y pendientes.
- Enlace en [[Programacion]]; el canvas viejo `Mapa Alta de productos` queda marcado como desactualizado (no se borró).

## 2026-10-28 (Alta: se quitó Siigo)
- Siigo nunca se compró: se quitó de Alta la tarjeta «Excel para Siigo», el botón de arriba, la columna Siigo de la lista, las rutas `/api/siigo*`, la plantilla y la configuración `siigo` (se borra sola de `opciones.json`). README y LEEME actualizados (ahora explican CRS y cajas).
- Archivos: `app\server.js`, `app\public\index.html`, `README.md`, `LEEME.txt`. Respaldo en `respaldo_antes_de_quitar_Siigo\`. `app\siigo.js` y `node_modules\jszip` ya no se usan: se pueden borrar a mano. La columna `exportado_siigo` queda en la base pero no se usa.
- Probado con Playwright: sin errores, guardar y actualizar desde CRS funcionan.

## 2026-10-28 (Alta: botón Subir productos)
- Nuevo botón **«Subir productos (N)»** en el panel morado de Alta: lista con casillas de los productos creados en Alta que no están en CRS y los sube a `BDSCRS.mde`. Archivo: `app\public\index.html`. Probado con Playwright (CRS simulado).
- Aclarado: «Sincronizar cajas» manda todo el catálogo de CRS, no la lista de Alta.
- Nota tocada: [[CRS - wwwSyncro y escribir productos desde Alta]].

## 2026-10-28 (V.YA: lote de 12 stories, formatos nuevos)
- 12 stories 1080×1920, solo logo, una prenda por pieza y 12 formatos que no estaban en los lotes del 24 y 26 oct: fotomatón inclinado, tres arcos, corte diagonal, lupa de detalle con líneas guía, cuadrícula 2×2 con sello central, abanico, tríptico a sangre, página de lookbook, escalera, mosaico 3×3, marco art déco (espresso + dorado), mitades horizontales con banda.
- Prendas: 08, 10, 16, 24, 31, 34, 43, 51, 77, 80, 84, 92 (no usadas antes).
- Fotos bajadas de Drive (`drive vya septiembre`, sesiones 081526/081826/090226/100926) con el conector de Google Drive; el permiso para `Documents\almacen fotos` y `Documents\assets` fue denegado. Logo: `logo_mask.png`.
- No funcionó: instalar rembg en la nube (pip no lo encuentra), así que no hubo pieza con silueta recortada.
- Script: `Edicion de imagenes/Scripts/stories_28oct.py`. Notas tocadas: [[Pendientes]] (registro de lotes).

## 2026-10-27 (noche: Alta conectado con CRS y Dropbox)
- Alta ahora: crea productos en `BDSCRS.mde` (opcional al guardar, o «Enviar a CRS»), botón **Sincronizar cajas** (como la subida de wwwSyncro hasta Dropbox, sin FTP, con copia, compactado y comprobación), panel **Revisar Dropbox** (qué tienen las cajas y qué falta) y **Actualizar desde CRS** al abrir y con botón (manda CRS).
- Archivos: nuevo `app\crs.ps1`; cambiados `app\server.js`, `app\public\index.html` (respaldo en `respaldo_antes_de_CRS\`). Probado con Playwright (CRS simulado) y en el PC con copias (`Documents\crs\prueba-sync`).
- No funcionó: uharc mete el archivo con su nombre (las cajas esperan `wwwProductos.mdb`); el .mdb se duplica sin compactar.
- Notas tocadas: [[CRS - wwwSyncro y escribir productos desde Alta]] (secciones nuevas).

## 2026-10-27 (CRS: wwwSyncro y escribir productos desde Alta)
- Se leyó `wwwSyncro.mdb`: copia el catálogo de `BDSCRS.mde` a `wwwProductos.mdb`, lo comprime con uharc, deja copia en Dropbox y lo sube por FTP a Smart Data; las otras cajas lo bajan y crean los productos nuevos (existencias 0) y reemplazan todos los códigos de barras.
- Prueba de la opción 2 en copias (`Documents\crs\prueba-sync\`): Alta escribe el producto 279999 en las 4 tablas de BDSCRS, se simula la subida y la descarga, y en la otra caja aparece al escanearlo. Resultado OK.
- No funcionó: SQL entre bases (`IN '...mde'` / `[;DATABASE=...]`) → hay que copiar fila por fila. Primer script con error de PowerShell (`return ,$t`).
- Notas tocadas: nueva [[CRS - wwwSyncro y escribir productos desde Alta]]; enlace en [[Programacion]] y en [[Alta de productos - herramienta portable para Siigo]] (sección nueva del 27 oct).

## 2026-10-27 (idea: juego de ritmo tipo ADOFAI)
- Guardada la lluvia de ideas sobre hacer un juego para celular: de Factorio/idle a ritmo tipo ADOFAI con modelo Geometry Dash (sets con mis beats desde el MIDI, biblioteca de productores, mapas de la comunidad, plan por fases).
- Notas: nueva [[Idea juego de ritmo tipo ADOFAI]]; enlaces en [[Programacion]] y [[Multimedia]].

## 2026-10-27 (LKV EQ: analizador de espectro, pendiente de compilar)
- Escrito el analizador FFT de fondo (Spectrum.h, FIFO en el procesador, dibujo en EqCurve) y su test. La compilación falló porque el disco C: se quedó a 0 bytes (algo ajeno ocupó unos 5,5 GB). Ver [[LKV EQ - plugin VST3 propio (JUCE)]].

## 2026-10-27 (LKV EQ instalado para FL Studio)
- Copiado `LKV EQ.vst3` a `C:\Program Files\Common Files\VST3` con permisos de administrador (UAC). Falta escanearlo desde el Plugin Manager de FL.
- Nota tocada: [[LKV EQ - plugin VST3 propio (JUCE)]].

## 2026-10-26 (alta de productos: IVA incluido en el costo)
- Nueva opción «IVA 19% ya incluido en el costo» en el tipo de impuesto: le quita el IVA al costo (÷ 1,19), el precio sugerido solo aplica la ganancia y el producto se guarda y exporta como `IVA 19%`.
- Archivo cambiado: `Downloads\AltaDeProductos_v2_2026-10-24\AltaDeProductos\app\public\index.html`. Probado con Playwright.
- Nota tocada: [[Alta de productos - herramienta portable para Siigo]] (sección nueva del 26 oct).

## 2026-10-26 (CRS: análisis del código)
- Se analizó `D:\CRS`: CRS está hecho en **VBA dentro de Microsoft Access 2000/2003**. No está encriptado: `CRS.mdb` trae todo el código fuente (767 módulos, unas 273.000 líneas) y `CRS.mde` es la versión compilada, sin código fuente.
- Se documentaron los archivos, las bases vinculadas (servidor `\\vyasas\CRS` y locales), los módulos, el arranque (`MenuEntrada`), la licencia, la facturación electrónica (Afacturar.com), los .bat y los puntos débiles (login con SQL armado a mano, claves en texto plano, credenciales FTP en el código).
- No funcionó instalar mdbtools/oletools (red bloqueada); se usó un lector propio de Jet 4 en Python.
- Notas tocadas: nueva [[CRS - cómo funciona el código]]; enlace añadido en [[Programacion]].

## 2026-10-26 (alta de productos: cambios recuperados)
- La carpeta `Downloads\AltaDeProductos_v2_2026-10-24\AltaDeProductos` tenía otra vez el código original del 24 oct (sin los cambios de la tarde); la versión final estaba en la subcarpeta `AltaDeProductos\AltaDeProductos`. Se copió a la principal: `app\server.js`, `app\public\index.html`, `app\public\imprimir.html`. Datos y configuración no se tocaron.
- Nuevos en la raíz: `README.md` (para el repo privado `kori496/ALTA`) y `.gitignore` (datos, configuracion, exportados, node, la subcarpeta duplicada). `LEEME.txt` actualizado con los campos de la etiqueta, CSV con punto y coma e impresora obligatoria.
- Ojo: la subcarpeta `AltaDeProductos\AltaDeProductos` es un duplicado; se puede borrar cuando se confirme que todo funciona.
- Nota relacionada: [[Alta de productos - herramienta portable para Siigo]].

## 2026-10-26 (LKV EQ: limpieza de disco)
- Borrada la carpeta de compilación `C:\devuild\LkvEQ` (405 MB); binarios guardados en `C:\dev\LkvEQ-bin`. Ahora quedan 701 MB libres en C:.
- Nota tocada: [[LKV EQ - plugin VST3 propio (JUCE)]].

## 2026-10-25 (reorganización por temas y colores)
- Nuevos mapas por tema en `Mapas/`: [[Multimedia]], [[Imágenes]], [[Webs]], [[Redes]], [[Tienda y negocio]], [[Herramientas y IA]], más [[Inicio]] y [[Resumen reciente 21-25 oct 2026]] (explicación detallada de la semana).
- Colores del grafo (`.obsidian/graph.json`): violeta multimedia, rosa imágenes, verde programación, turquesa webs, azul redes, ámbar tienda, naranja herramientas y IA, dorado mapas, gris bitácora. Copia del archivo anterior: `.obsidian/graph.antes-de-colores.json`.
- Enlace «Mapa general: [[Inicio]]» añadido arriba en [[Videos beats]], [[Programacion]] y [[Edición de imágenes]], y regla de mapas en `CLAUDE.md`.
- **No se movió ningún archivo**: desde la sesión no hay shell en el PC y mover fuera de Obsidian rompe enlaces. Mover carpetas físicas queda pendiente (ver final del resumen).

## 2026-10-25 (LKV EQ: plugin VST3 propio)
- EQ paramétrico propio en C++/JUCE 8.0.4 (8 bandas, curva arrastrable, VST3 + Standalone) en `Documentos\LkvEQ`; herramientas en `C:\dev`. Compila con VS 2022 + CMake portable y pasan los 6 tests. Resuelto el error C2280 (Filter no se puede copiar).
- Aviso: quedan 296 MB libres en C:.
- Notas: nueva [[LKV EQ - plugin VST3 propio (JUCE)]]; enlaces en [[Programacion]] y [[FabFilter Pro-Q 4]].

## 2026-10-25 (Pro-Q 4: FASE 2 bloque 2)
- Bloque 2 (opciones 11-20) trazado: MIDI Learn (`MidiControllerMap.ffm`), escalado (valores en HKCU), menú Help (`HelpFileName` en HKCU/HKLM; web y soporte en el navegador) y red: registro del dispositivo cada 7 días, que envía el nombre del PC y un ID basado en las MAC; deauthorize. Corregida la fila 54 (ProgramFilesDir es el plan B de la carpeta de datos).
- Nota tocada: [[FabFilter Pro-Q 4]].

## 2026-10-25 (Pro-Q 4: Ghidra OK y FASE 2 bloque 1)
- Ghidra 12.1.4 funciona con REA (timeout subido a 30 min). Como la CLI reanaliza en cada comando, se montó una sesión MCP persistente por script.
- Bloque 1 (opciones 1-10) trazado: menú de presets, cambio de carpeta (registro HKCU), Restore Factory Presets (extrae un archivo embebido y sobrescribe), Favorites.txt y Save As Default. Corregida la fila 9: Revert y Load Factory Settings son del menú MIDI Learn.
- Notas tocadas: [[FabFilter Pro-Q 4]], [[REA - ingeniería inversa]].

## 2026-10-25 (prueba de Ghidra para REA)
- Las variables nuevas apuntan a carpetas que no existen (Ghidra 12.1.4 sin extraer; `JAVA_HOME` con «jdk-21...»). Con el JDK 25 real, Java pasa; con la 12.2, REA solo rechaza la versión.
- Nota tocada: [[REA - ingeniería inversa]].

## 2026-10-25 (análisis de FabFilter Pro-Q 4 con REA, fase 1)
- Inventario de 60 opciones del plugin VST3 (cadenas, imports, recursos PE y registro). El binario real está en `Common Files\VST3`, no en `Program Files\FabFilter`. Es un producto de FabFilter, no propio: no se analizó la licencia.
- REA 6.7.0 no abre el binario con Ghidra 12.2 (pide 12.1.x) y le falta `JAVA_HOME`. Fases 2 y 3 en espera.
- Notas: nueva [[FabFilter Pro-Q 4]], nueva [[Análisis de apps con REA]], enlace en [[Programacion]], sección añadida en [[REA - ingeniería inversa]].

## 2026-10-25 (prompt para analizar apps con REA)
- Nueva nota [[Prompt - analizar app propia con REA]]: prompt en tres fases que inventaría las opciones de una app, traza el efecto de cada una en el sistema y guarda el resultado en el vault. Sin probar todavía con una app real. Enlazada desde [[REA - ingeniería inversa]].

## 2026-10-25 (REA: Ghidra funcionando)
- `GHIDRA_INSTALL_DIR` apuntaba al archivo `ghidraRun` en vez de a la carpeta raíz del release; corregido y `rea doctor` en verde para Ghidra 12.2.
- Nota tocada: [[REA - ingeniería inversa]].

## 2026-10-25 (REA: timeout al conectar)
- `claude mcp list` mostró `rea` con timeout de 30 s (npx lento); tras las pruebas sugeridas ya conectó. La carpeta `rust prueba\ghidra` resultó ser código fuente, no un release; sigue pendiente el release 12.1.x y `GHIDRA_INSTALL_DIR`.
- Nota tocada: [[REA - ingeniería inversa]].

## 2026-10-25 (REA: Ghidra y doctor)
- Instalar REA en el entorno en la nube no se pudo (npm bloqueado por política, 403). Sigue instalado solo en el PC.
- Interpretado el resultado de `rea doctor`: lo único que faltaba para Ghidra era `GHIDRA_INSTALL_DIR` (Ghidra 12.1.x extraído). Anotado cómo comprobar el JDK y qué avisos ignorar.
- Nota tocada: [[REA - ingeniería inversa]].

## 2026-10-24 (V.YA: lote de 12 stories wideleg)
- 12 stories 1080×1920 de jeans wideleg (semana 2 del calendario), una prenda por pieza y 12 formatos distintos tomados de los lotes del 19 y 21 oct: insets, foto grande + tira, difuminado, arco con círculos, tiras crema/espresso, dúo, marco espresso, columna, fondo B/N. Solo el logo, sin texto.
- Prendas: 09, 11, 20, 25, 30, 49, 64, 66, 68, 72, 87, 93 (elegidas a ojo por la forma del jean: las fotos en crudo no tienen la referencia VF anotada).
- Archivos: `Downloads\drive vya septiembre-...\ediciones_vya_24oct\` (12 PNG + preview.jpg). Script para rehacerlas: `Edicion de imagenes/Scripts/stories_wideleg_24oct.py`.
- El logo se sacó recortando `02_grid_crema_p77.png` (no hay archivo de logo). Los originales de `agrupadas` son de WhatsApp (960×1280) y quedan algo blandos a 1080 de ancho.
- Notas tocadas: [[Pendientes]] (registro de lotes).

## 2026-10-24 (alta de productos: botón IMPRIMIR)
- Botón IMPRIMIR que abre una pestaña con solo los productos de la sesión (cantidad y precio por etiqueta), historial de la sesión con reimpresión (se reinicia al cerrar el programa) y log permanente `datos\impresiones.log`. El programa se cierra solo tras 10 min sin pestañas. 36/36 pruebas con Playwright; .zip rehecho.
- Notas tocadas: [[Alta de productos - herramienta portable para Siigo]] (sección nueva «Botón IMPRIMIR, historial y log») y el canvas `Mapa Alta de productos` (tarjetas nuevas de la pestaña IMPRIMIR y el log; las que ya estaban no se movieron).

## 2026-10-24 (alta de productos: canvas)
- Nuevo canvas `Programacion/Mapa Alta de productos.canvas`: arranque, interfaz, servidor, disco, flujos (guardar, Siigo, BarTender, base vieja y conflictos), reglas de negocio y estado de las pruebas. Enlazado desde [[Programacion]] y [[Alta de productos - herramienta portable para Siigo]].

## 2026-10-24 (alta de productos: versión 2, carpeta instalable)
- Opción A elegida: Node.js incluido + interfaz en el navegador. Carpeta en `Documentos\alta de productos\` y paquete `paquete\AltaDeProductos_v2_2026-10-24.zip` (34 MB). Sin internet, guardado automático con copias, BarTender directo, Excel de Siigo escrito sobre la plantilla sin tocar su formato (lotes de 500, validación de obligatorias y listas).
- Probado con una plantilla de prueba hecha en Excel, con Playwright + Edge (22 pruebas) e instalando en limpio. Corregido un error con espacios en la ruta de bartend.exe. Falta la plantilla real de Siigo y probar BarTender en la tienda. `productos.html` sin cambios.
- Nota tocada: [[Alta de productos - herramienta portable para Siigo]] (secciones Archivo, Versión 2, Pendiente, Decisiones y Riesgos).

## 2026-10-24 (alta de productos: vincular BarTender)
- Revisada la ayuda de BarTender sobre la línea de comandos y anotados los pasos para imprimir etiquetas desde la herramienta, qué está confirmado (`/F`, `/P`, `/C`, `/D`) y qué no (`/PRN`, `/X`, ediciones con Commander). Ver [[Alta de productos - herramienta portable para Siigo]].

## 2026-10-24 (alta de productos: formato carpeta instalable)
- Decisión: el proyecto ya no tiene que ser un solo HTML; puede ser una carpeta instalable para pocas computadoras. Prompt actualizado en [[Prompt - seguir Alta de productos con Claude Code]] (propone estructura antes de reescribir) y decisión anotada en [[Alta de productos - herramienta portable para Siigo]].

## 2026-10-24 (alta de productos: prompt para Claude Code)
- Nueva nota [[Prompt - seguir Alta de productos con Claude Code]] con el prompt para continuar el proyecto en VS Code. Se volvieron a añadir el enlace en el índice [[Programacion]] y la sección de códigos que no se repiten en la nota del proyecto: el PC había vuelto a una versión vieja tras guardar.

## 2026-10-24 (navegador propio basado en Zen)
- Zen es open source, así que basta con un fork. Se eligió el fork completo, pero el PC no da para compilarlo (9 GB libres, 8 GB de RAM, sin VS/Rust/MozillaBuild). Pendiente elegir: nube, más disco con artifact build, o mods.
- Nota nueva: [[Navegador propio - fork de Zen Browser]] (enlazada desde [[Programacion]]).

## 2026-10-24 (REA instalado en Claude Code)
- Aplicado `rea-agents@6.7.0 setup --client claude_code --yes`: MCP `rea` registrado en `.claude.json` (copia en `.claude.json.rea.backup`) y skill `reverse-engineer-anything` instalado. Verificado con `rea doctor` (aligned) y `claude mcp get rea` (Connected).
- La tabla «Sep oct» de TikTok **se deja** (decidido: no borrarla).
- Nota tocada: [[REA - ingeniería inversa]].

## 2026-10-24 (skill analyze-apps-with-rea)
- Nuevo skill de Claude Code `analyze-apps-with-rea` (SKILL.md + `scripts/trace_input.py`) con el flujo de REA para apps Electron: analizar, sembrar por canal IPC, rastrear y confirmar en el código. Script probado con notes-example (1 coincidencia, 1 ruta, cobertura completa). Sin evals ni optimización de la descripción.
- Nota tocada: [[REA - ingeniería inversa]].

## 2026-10-24 (REA: plan de instalación y ejemplo notes)
- Revisado el plan de `rea-agents@6.7.0 setup` para Claude Code (2 acciones). **No aplicado**: falta tu aprobación.
- Descargado y descomprimido `notes-example.zip` en `metricool\rea-work\rea-work\example\`. Trazado con REA (vía `npx`) el botón «Export notes»: escribe `notes.csv` en Descargas, con columnas `id,title`.
- Nota nueva: [[REA - ingeniería inversa]], enlazada desde [[Skills]].

## 2026-10-24 (lagrim-stats: revisión de datos de fin de día)
- Se corrió `ejecutar_diario.bat` (sin errores). YouTube: 2 suscriptores, 1.567 vistas totales, 21 videos (la analítica llega hasta el 22 oct; YouTube va 2 días atrasado). TikTok: sin CSV nuevos, 797 vistas del 14 al 22 oct. Instagram API: 0 seguidores, 105 vistas y 101 de alcance, 5 publicaciones.
- Global (28 d): 2.301 vistas, 26 interacciones, 2,9 interacciones por cada 100 vistas (TikTok + Instagram).
- Arreglado: el rango de fechas de cada bloque (p. ej. «Api») ahora cubre todas las métricas (antes decía «1 día»).
- Pendiente: un CSV de Instagram (`Sep-24-2026_Oct-21-2026_979051954630492.csv`, reels de @lagrimankv) se importó por error en TikTok y sale como tabla «Sep oct» en esa pestaña. No afecta a las sumas. No se borró sin preguntar.
- Nota tocada: [[Panel web lagrim-stats]].

## 2026-10-24 (lagrim-stats: Instagram conectado)
- La API de Instagram no funcionaba: `meta_config.json` tenía el token como texto suelto, no JSON. Se reescribió en el formato correcto (copia del original en `meta_config.antes-de-arreglar.txt`, ignorada por git). Probado: conecta como @lagrimankv, el token se renovó y trajo 5 publicaciones; Global ya suma Instagram.
- El panel ahora avisa si el archivo de configuración está mal escrito, mostrando el motivo.
- Nota tocada: [[API de Instagram (Meta) - configuración y errores]].

## 2026-10-24 (lagrim-stats: panel «Todas las plataformas»)
- En Global, arriba del resumen por red, nuevo panel con la suma de YouTube + TikTok + Instagram (28 días): seguidores + suscriptores, vistas, interacciones e interacciones por cada 100 vistas. Debajo de cada número dice qué redes se sumaron; las que no tienen el dato no cuentan como cero.
- La tasa por cada 100 vistas solo usa redes que tienen vistas e interacciones (YouTube no da interacciones por día y la diluía de 3,1 a 1,1).
- Nota tocada: [[Panel web lagrim-stats]].

## 2026-10-24 (lagrim-stats: código del panel unificado)
- Se sacó el código repetido de las 5 páginas del panel a `web/comun.php` (funciones, base de datos, menú, subida de CSV, carga de TikTok/Instagram, tarjetas y tablas) y `web/comun.js` (tablas ordenables, colores y gráficos por métrica). TikTok pasó de 264 a 59 líneas; Instagram de 335 a 135.
- Comprobado: el HTML de las 5 páginas sale igual que antes, el JS corre sin errores (Chart.js simulado) y la subida de CSV rechaza bien archivos vacíos o que no son .csv. La velocidad ya era buena (~0,3 s), no hacía falta tocarla.
- Nota tocada: [[Panel web lagrim-stats]].

## 2026-10-24 (alta de productos: GitHub limpio)
- `kori496/ALTA` en GitHub volvió al «Initial commit» (solo LICENSE y README): sin rastro de la app ni de las bases en el historial de `main`. El usuario lo sube él mismo; local quedó sin commit, con `.gitignore` listo. Rama local `respaldo-antes-de-limpiar` guarda el historial viejo (con datos): no subirla.

## 2026-10-24 (alta de productos: logo y marcas de Siigo)
- Logo de texto «ALTA» arriba a la derecha (reemplaza el título «Alta de productos»; la pestaña también dice ALTA).
- Se quitó la fecha de «exportado a Siigo» a los 7759 productos (nada estaba subido). Copia previa: `datos\copias\productos_2026-10-24_203424_antes-quitar-siigo.sqlite`. Ahora «Exportar a Excel» (solo nuevos) los incluye todos.

## 2026-10-24 (alta de productos: .gitignore para GitHub)
- Repo privado `kori496/ALTA`: `.gitignore` nuevo (fuera: `datos/`, `exportados/`, `configuracion/opciones.json`, `node/`, `node_modules/`, `*.zip`). Archivos sacados del índice, siguen en disco. Ojo: el primer commit ya subido contiene las bases y node.exe; pendiente decidir si se limpia el historial.

## 2026-10-24 (alta de productos: código de barras = referencia)
- Formulario «Nuevo producto»: el código de barras se guarda también como referencia (`codigo_interno`); campos nuevos Referencia (Vf2944) y Descripción (Body), guardados juntos como nombre «Body Vf2944». Sin cambios en la base. También se explicó que pasar a PHP no muestra las impresoras del PC cliente. Nota: [[Alta de productos - herramienta portable para Siigo]] (sección «Código de barras = referencia»).

## 2026-10-24 (alta de productos: carpeta de opciones)
- Carpeta `configuracion\opciones.json`: BarTender, impresora elegida e impresoras usadas, última carpeta de cada tipo de archivo, ubicación de la base y columnas de Siigo. Ventana de Windows para abrir archivos en la última carpeta; lista de impresoras instaladas. Opciones viejas migradas solas. 54/54 pruebas + ventana real probada; .zip rehecho. Nota: [[Alta de productos - herramienta portable para Siigo]] (sección «Carpeta de opciones guardadas»).

## 2026-10-24 (alta de productos: imprimir fallaba por servidor viejo)
- El programa abierto (carpeta normal) seguía con el código de antes de la impresión: las páginas eran nuevas y el servidor viejo («Ruta desconocida»). Reiniciado. Ahora el doble clic detecta si el código cambió, cierra la versión vieja y abre la nueva (anotado en el log). Pruebas 46/46 y 5/5; .zip rehecho. Nota: [[Alta de productos - herramienta portable para Siigo]].

## 2026-10-24 (alta de productos: error «Sesión no válida»)
- Resuelto: tras reiniciarse el programa, las pestañas abiertas quedaban con la clave vieja. Ahora renuevan la clave solas; la versión de la base sale de la fecha y tamaño del archivo, así que reiniciar o abrir otra ventana ya no obliga a recargar. 46/46 pruebas; .zip rehecho. Nota: [[Alta de productos - herramienta portable para Siigo]].

## 2026-10-24 (alta de productos: Volver, Ctrl+F7 y texto del botón)
- Pestaña de impresión con botón «← Volver»; Ctrl+F7 reinicia la sesión de impresión (con confirmación, anotado en el log); el botón dice «Imprimir». 43/43 pruebas en cuatro corridas; .zip rehecho. Nota tocada: [[Alta de productos - herramienta portable para Siigo]] (sección «Botón IMPRIMIR, historial y log»).

## 2026-10-23 (alta de productos para Siigo)
- Herramienta portable para dar de alta productos, reemplazo de la creación de productos de CRS: `Programacion\Alta de productos\productos.html`. Un solo archivo, sin instalación, guarda una base `.sqlite` y exporta CSV. Nota: [[Alta de productos - herramienta portable para Siigo]].
- Revisada la guía de Siigo «Subir desde Excel Productos»: plantilla desde Configuración → Productos y servicios → Importación, máximo 500 registros, no modificar columnas. Falta la plantilla real para generar el Excel.

## 2026-10-23 (alta de productos: códigos que no se repiten)
- `productos.html`: índice único en la base, contador que nunca baja, códigos de productos eliminados reservados y carga de códigos existentes de CRS o Siigo. Detalles y límites en [[Alta de productos - herramienta portable para Siigo]].

## 2026-10-23 (alta de productos: precio con ganancia)
- `productos.html`: campo «Ganancia sobre el costo (%)» (30% por defecto) y redondeo (terminar en 900), con el precio calculado y botón «Usar este precio». Ejemplo: 76.000 → 117.572 → 117.900. Ver [[Alta de productos - herramienta portable para Siigo]].

## 2026-10-23 (alta de productos: código de barras propio)
- `productos.html`: botón Generar y generación automática de EAN-13 con prefijo 20 a 29 (uso interno GS1), sin repetir códigos. Notas y límites en [[Alta de productos - herramienta portable para Siigo]].

## 2026-10-23 (alta de productos: reglas DIAN)
- `productos.html`: precio con IVA incluido y desglose (base, IVA), tipos IVA 19%, 5%, exento, excluido y no gravado, unidad de medida, validación GS1 del código de barras y avisos de INC. Detalles y límites en [[Alta de productos - herramienta portable para Siigo]].

## 2026-10-23 (alta de productos: plantillas y BarTender)
- `Programacion\Alta de productos\productos.html`: botón Plantilla por producto, referencia en vez de código interno, grupo Confecciones con opción Otro, y etiqueta/impresión con BarTender vía CSV + .bat. Sin probar en el PC. Detalles en [[Alta de productos - herramienta portable para Siigo]].

## 2026-10-23 (descargador de redes)
- Descargador Node (`Documentos\lagrima dlp`): código arreglado, carpeta `descargas/`, botón «Ver descarga», 6 motores con barra y redes por motor, diseño tipo Apple con paleta de tres azules y animaciones. Resuelto: decía «falló» aunque descargaba (la ruta que imprime yt-dlp no sirve con caracteres especiales; ahora se busca el archivo nuevo en `descargas/`).
- Integrado en lagrim-stats como pestaña **Descargas** (`web/descargas.php`, `web/descargas_api.php`, `motores_descargas.py`) y enlace en el menú de las demás páginas. Sin probar en el PC. Notas: [[Descargador de redes - motores, diseño y panel]], [[Panel web lagrim-stats]], [[Descargador de YouTube con Node y yt-dlp]] (se agregó una actualización arriba y se marcó el Pendiente como resuelto).
- Se vio otra vez que el PC vuelve a una versión vieja de `server.js` e `index.html` tras guardar; verificar después de guardar.

## 2026-10-23 (programación)
- Aprendizaje guiado de un descargador de YouTube con Node.js, Express y yt-dlp (sin que Claude escribiera el código). Nueva nota [[Descargador de YouTube con Node y yt-dlp]], dentro de la nueva carpeta `Programacion/` con índice [[Programacion]]. Cubre npm/package.json/node_modules, `.gitignore`, Express y `app.listen`, formulario HTML, GET vs POST, `express.urlencoded` y `req.body`, el error "Cannot read properties of undefined", y el plan de `spawn` para yt-dlp (pendiente de escribir).
- Mismo contenido copiado a Notion como página privada (borrador).

## 2026-10-23
- CLEAN EYES (= cancer type beat): 2 videos oscuros rojo sangre en `Documentos\marketing\clean_eyes\` (A: loop seco → efectos → mezcla de los compases 9-12; B: fragmento en bucle de los compases 57-64). Nueva nota [[CLEAN EYES - loop a mezcla y fragmento (oscuro rojo)]], enlazada desde [[Videos beats]]. El disco C: se llenó durante el trabajo (proyecto en OneDrive).
- eyesofdirty: tras bajar las capas de GIF del drop, la verificación pasa entera (máximo 3 destellos por segundo).
- Video eyesofdirty (2): más destellos (uno por compás, hasta 3/s en el drop), pulso en cada tiempo, sacudida en cada compás y los 6 GIFs de `marketing` teñidos de azul (ciudad de fondo, tarjetas, explosión en el drop). Anotado en [[Prompt vorty - how to sound like eyesofdirty (voz y drop)]].
- Video eyesofdirty corregido: sin silencio antes de las drums (y sin congelado/oscurecido) y paleta azul intenso + letras blancas + fondo negro. Mismo archivo en `Documentos\marketing`. Anotado en [[Prompt vorty - how to sound like eyesofdirty (voz y drop)]].

## 2026-10-23
- Panel lagrim-stats: vista **Global** (`web/global.php`) con YouTube, TikTok e Instagram juntos y progreso hacia las metas de agosto 2027. Pestaña **Instagram** (`web/instagram.php`) con gráficos por publicación para el CSV de Meta. Se quitó `mb_strtolower` porque el PHP de Windows no tiene `mbstring`. Notas en [[Panel web lagrim-stats]] y [[API de Instagram (Meta) - configuración y errores]].
- Corregida la lectura de kill4meeee: sí funciona (338 vistas en YouTube y 127 y 162 en TikTok). Ver [[Métricas y revisiones]] y [[Estilo de videos de vorty]].
- Nuevo beat **Clean Eyes** (type beat de Eyes of Dirty, 151 BPM, A minor, oscuro y agresivo, en `marketing\`). Título, descripción, 20 tags y textos de TikTok. Ver [[Clean Eyes - beat y publicación]].
- Nuevo prompt para Claude Code: tres estilos por beat (layer by layer ya hecho, loop a mezcla final y fragmento con enlace). Ver [[Prompt tres estilos por beat (layer, loop a mezcla, fragmento)]].
- Revisado si se puede conectar lagrim-stats con Metricool. Metricool ya tiene datos de Instagram. Opción recomendada: exportar CSV y subirlo al panel. Y se puede programar videos desde Metricool con enlace público. Ver [[Publicar y conectar con Metricool]].
- Decisión: textos en inglés en títulos, descripciones y textos de video. Español solo como línea extra al final de la descripción.
- Aprendido: el primer guardado de un archivo existente en el PC no siempre se aplica. Verificar después de guardar (tamaño o contenido).

## 2026-10-22
- Hecho el video "how to sound like eyesofdirty" (voz IA + piano roll por capas + drop en el compás 9): `Documentos\marketing\lagrimankv_how_to_sound_like_eyesofdirty.mp4`, proyecto en `C:\Users\sharo\remotion\eyesofdirty`. Fase 0 confirmó BPM, desfases y drop. Resultados, verificación y errores (contraste, yuvj420p, oscurecido pegado en el drop) en [[Prompt vorty - how to sound like eyesofdirty (voz y drop)]].
- Pestaña Instagram del panel: gráficos por publicación (alcance, vistas, interacciones) para el CSV de Meta, que trae un dato por post. Respuesta "qué contenido funcionó más" anotada en [[Métricas y revisiones]]; corregida la lectura de kill4meeee en [[Estilo de videos de vorty]] (338 vistas, sí funciona). Nota: el primer guardado de un archivo existente en el PC a veces no se aplica; verificar después de guardar.
- Panel lagrim-stats: nueva pestaña **Instagram** (`web/instagram.php`, API de Meta o CSV) y nueva vista **Global** (`web/global.php`) con YouTube, TikTok e Instagram juntos: resumen por red, vistas por día, tabla comparativa y progreso hacia las metas de agosto 2027. Nuevo `importar_instagram.py`, añadido a `ejecutar_diario.bat`. Probado con datos de ejemplo, no con tu token real. Detalles en [[Panel web lagrim-stats]] y [[API de Instagram (Meta) - configuración y errores]].
- Panel TikTok (`analitica/web/tiktok.php`): botón "Subir CSV de TikTok" arriba a la derecha. Guarda el CSV en `tiktok/entrada/` y ejecuta `importar_tiktok.py` (ruta de Python configurable con `LAGRIM_PYTHON`, por defecto `python`). Estilos en `estilo.css`. Sin probar en el PC todavía; `php -l` sin errores.
- Anotados en [[Métricas y revisiones]] los datos de 22 oct (YouTube 1.338 vistas, TikTok 541) y recomendaciones.
- Anotados en [[Estilo de videos de vorty]] los resultados de kill4meeee: flojos en YouTube (53 vistas), mejores en TikTok (289). woeklifeee no aparece en el reporte.

## 2026-10-21
- Revisados los archivos del beat "eyes of dirty" (`Presets\Scores`) y actualizado [[Prompt vorty - how to sound like eyesofdirty (voz y drop)]] sin marcadores: 151 BPM, compás 1 del mp3 en 0,030 s, drop confirmado en el compás 9, tonalidad medida A# menor (el archivo dice Am), MIDI con notas. Dudas: el WAV de piano 1 coincide poco con su MIDI, y el archivo con cortes trae las notas del lead.
- Nuevo prompt [[Prompt vorty - how to sound like eyesofdirty (voz y drop)]]: voz IA al inicio, recuadros MIDI que se suman, piano 1 normal y con cortes, drop en el compás 9. Lleva Fase 0 de verificación porque los archivos del beat no se pudieron revisar; faltan datos del beat (BPM, escala, rutas). La voz dice "sound like", no "make a beat like".
- Voz del primer video lista: `analitica/eyes of dirty vox robotic.mp3` (Aria + preset robot, editada en FL) y sus tiempos por palabra en `eyes of dirty vox robotic.json` (alineados con correlación 0,91). `voz_gancho.py` confirmado funcionando en el PC. Anotado en [[Referencias de voz en shorts]]. Falta elegir beat y paleta.
- Decidido el primer video con gancho de voz: "how to sound like eyesofdirty", voz IA procesada. Nuevo script `Videos beats/Scripts voz/voz_gancho.py` (edge-tts + ffmpeg, 3 presets, JSON de tiempos por palabra, vista previa con beat). Documentado en [[Referencias de voz en shorts]]. La parte edge-tts sin probar.
- Nueva nota [[Referencias de voz en shorts]]: análisis de 3 referencias con voz al inicio (voz recortada ~3 s, drop con graves a ~3,2 s, texto sincronizado) y plan de prueba con/sin voz. Enlazada desde [[Videos beats]]. No se pudo escuchar el audio, solo ver el espectrograma.
- Módulo TikTok: `importar_tiktok.py` (CSV de TikTok Studio a la base de datos, genérico, probado con el Overview real) y página `web/tiktok.php` con pestañas YouTube/TikTok. Primer dato de TikTok anotado en [[Métricas y revisiones]]: 541 vistas el 19-20 oct (Metricool decía 0). Detalles en [[Herramienta analitica YouTube]].
- Panel web PHP (`analitica/web/index.php`) y ejecución diaria automática (`programar_tarea.bat`, `ejecutar_diario.bat`, `abrir_dashboard.bat`); `yt_stats.py` ahora acepta `--auto` (no abre el navegador si el permiso caducó). Documentado en [[Herramienta analitica YouTube]]. Panel probado solo con datos de ejemplo.
- `yt_stats.py` probado con el canal real: OK. Primer reporte anotado en [[Métricas y revisiones]]; corrige la lectura de Metricool (el Short top es "cooking boom bap at the skatepark", 315 vistas; Shorts retienen ~32 % vs ~14 % de los type beats). Actualizada [[Herramienta analitica YouTube]].
- Creado el script `Videos beats/analitica/yt_stats.py` y la nota [[Herramienta analitica YouTube]] (proyecto Google Cloud lagrim-stats, OAuth en modo prueba, `client_secret.json` armado a mano). Sin probar todavía con el canal real.
- Ejecutado [[Prompt vorty colorido - woeklifeee (3 videos sin MIDI)]]: 3 videos (v1_drop, v2_hits, v3_layers) en `marketing\woeklifeee-videos`, proyecto en `marketing\woeklifeee-remotion`. Desfase 0 confirmado (4,7 ms), -12 LUFS, pico objetivo bajado a -1,5 dBTP porque el AAC lo subía a -0,8. Anotado en la nota qué funcionó y qué no; propuesta de usar 41-56 para V2 (25-40 casi sin agudos).
- Decidido hacer primero una herramienta propia de analítica (YouTube primero) y dejar la web `lagrim.art` para después. Detalles en [[Alternativas a Metricool]].
- Nueva nota [[Alternativas a Metricool]] (Iconosquare, Buffer, Publer y nativas), enlazada desde [[Videos beats]].
- Proyecto **y-una-angelica-visualizer**: el vault pasa a ser su base de datos. Nueva nota [[Y una angelica - visualizer]] (BPM, secciones, montaje, estado), enlazada desde [[Videos beats]], y `CLAUDE.md` en la raíz del proyecto (desde [[Plantilla CLAUDE.md proyecto Remotion]]) con esa regla.
- Miniaturas de YouTube de woeklifeee (1280x720, 4 versiones A sunburst, B bold, C panels, D sun) en `Videos beats/Miniaturas woeklifeee/`, con el script `gen.py` para regenerarlas. La foto del atardecer se descartó: sin texto, oscura y de baja resolución para un beat alegre. Falta elegir y subir una.
- Anotado el rendimiento de Metricool (22 sep a 21 oct) en [[Métricas y revisiones]]: 227 vistas en YouTube, pico de 164 el 18/10, 2 suscriptores, TikTok sin datos. Metricool no devolvió lista de videos ni fuentes de tráfico.
- Beat **woeklifeee** (140 BPM, E mayor): medido el mp3 (compás 1 en 0 s, drop en el compás 9, 85 % graves) y escrito [[Prompt vorty colorido - woeklifeee (3 videos sin MIDI)]]: 3 videos de 16 compases (5-20, 25-40, 57-72), paleta colorida porque el beat es feliz. La versión oscura se retiró (queda como variante reutilizable). Sin ejecutar todavía.
- Nuevo prompt [[Prompt vorty oscuro - visualizer sin MIDI (Remotion)]]: estilo vorty en oscuro (casi negro + magenta/violeta) para beats sin MIDI ni stems; paneles LOW/MID/HIGH reactivos al audio, `FILTER_PARTS` opcional, 13 compases. Sin probar todavía con un beat real. Enlazado desde [[Videos beats]].
- Estilo vorty: la paleta ya no es siempre rosa. Se agregó el bloque "Estética del beat" (fondo, 3 acentos, texto, motivo de tarjetas, colores en `config.ts`, contraste 4.5:1) a [[Prompt vorty - breakdown rosa 3D (Remotion)]], [[Estilo de videos de vorty]] y la checklist de [[Proceso vorty - paso a paso]]. El rosa queda como paleta de referencia de kill4meeee. Los nombres de archivo conservan "rosa" para no romper enlaces.
- Guardado el chat **"estilo de videos de vorty"** (breakdown rosa 3D por stems): [[Estilo de videos de vorty]], [[Prompt vorty - breakdown rosa 3D (Remotion)]] (prompt final completo) y [[Proceso vorty - paso a paso]] (mis mensajes literales, errores y checklist). Antes había confundido "vorty" con el estilo make beat; corregido.
- Guardado el chat "Video editing style for beats" como [[Estilo make beat (menta, lila y glitch)]], con scripts en `Videos beats/Scripts make beat/` (`analyze.py`, `fit_beatgrid.py`, `render.py`, `glitch.py`), probados con video sintético. Tag cambiado a `lagrimankv`.
- Regla nueva en `CLAUDE.md`: para videos de estos estilos, usar las recetas del vault, no inventar.
- Cambio de marca: "prod. p4m" pasó a **prod. lagrimankv** en [[Marca y textos]], [[Pipeline visualizer Remotion]], [[Plan de funcionamiento]] y [[Videos beats]] (alias). También en el prompt de Cuerda en Notion.
- Pendiente: el archivo `beat_glitch_p4m.mp4` conserva el nombre antiguo (es el nombre real del archivo).
- Se creó `CLAUDE.md` en la raíz con la regla de usar siempre el vault y anotar novedades aquí y en notas.
