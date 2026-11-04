---
tags: [mapa, resumen, bitacora]
actualizado: 2026-10-25
---

Volver a [[Inicio]] · Registro día a día en [[Bitácora]]

# 🗓️ Resumen reciente · 21 al 25 oct 2026

Explicación de todo lo trabajado esta semana, ordenado por tema (mismos colores que el grafo). Para el detalle técnico, cada sección apunta a su nota.

---

## 🟣 Multimedia · beats y videos
**Idea de fondo:** hacer videos, medir cuáles rinden y cambiar de formato hasta dar con uno rentable. El tema no tiene que ser ropa; ahora son beats (boom bap, trap, experimental) hechos en FL Studio. Los visualizers son para subir contenido, no para vender el beat.

**Qué se hizo**
- **Estilos con receta**: vorty (breakdown 3D por stems; la paleta sale de la estética del beat, no es fija), make beat (menta, lila, glitch) y core/distorsionado. Todo con **Claude Code + Remotion**, no en el chat. Ver [[Estilo de videos de vorty]], [[Estilo make beat (menta, lila y glitch)]], [[Pipeline visualizer Remotion]].
- **«How to sound like eyesofdirty»** (22–23 oct): short con voz generada con IA y procesada, piano roll por capas y drop en el compás 9. Se corrigió el silencio antes de las drums, la paleta (azul intenso, letras blancas, fondo negro), los destellos (máximo 3 por segundo) y los 6 GIFs teñidos de azul. Ver [[Prompt vorty - how to sound like eyesofdirty (voz y drop)]] y [[Referencias de voz en shorts]].
- **Clean Eyes / CLEAN EYES** (23 oct): type beat de Eyes of Dirty, 151 BPM, La menor, oscuro y agresivo. Dos videos rojo sangre: A (loop seco → efectos → mezcla de los compases 9–12) y B (fragmento en bucle de los compases 57–64). Ver [[Clean Eyes - beat y publicación]] y [[CLEAN EYES - loop a mezcla y fragmento (oscuro rojo)]].
- **Tres estilos por beat**: prompt para repetir layer by layer, loop a mezcla y fragmento. Ver [[Prompt tres estilos por beat (layer, loop a mezcla, fragmento)]].
- **Marca**: productor **lagrimankv**, tag «prod. lagrimankv» (ya no «p4m»); títulos y descripciones 100 % en inglés, slang, sin emojis. Ver [[Marca y textos]].

**Qué aprendimos**: kill4meeee rindió flojo en YouTube (53 vistas) pero mejor en TikTok (289); woeklifeee se hizo en versión colorida sin MIDI. El disco C: se llenó durante el render de Clean Eyes (el proyecto vive en OneDrive). Mapa: [[Multimedia]].

---

## 🔵 Redes · métricas y datos propios
**Problema:** la alternativa de pago a Metricool le pareció cara, y Metricool da los datos mal (TikTok salía en 0 cuando eran 541 vistas). **Decisión:** hacer una analítica propia, «vibecodeada», llamada **lagrim-stats**.

**Cómo funciona hoy**
- **YouTube**: importa con la API de YouTube Analytics (va 2 días atrasada). Al 24 oct: 2 suscriptores, 1.567 vistas totales, 21 videos.
- **TikTok**: por ahora con CSV de TikTok Studio (botón «Subir CSV»). **Decisión nueva:** usar la **API oficial de TikTok** (Display API + Login Kit) para las métricas; ya estás creando la app de desarrollador. Pendiente: terminar de crear la app y conectar el token.
- **Instagram**: API de Meta. No funcionaba porque `meta_config.json` tenía el token como texto suelto; se reescribió en JSON y ya conecta como @lagrimankv (5 publicaciones). El panel ahora avisa si el archivo está mal escrito. Ver [[API de Instagram (Meta) - configuración y errores]].
- **Global**: panel «Todas las plataformas» con la suma de las tres redes (28 días: 2.301 vistas, 26 interacciones, 2,9 por cada 100 vistas) y progreso hacia las **metas de agosto 2027** (10.000 suscriptores en YouTube; 30.000 seguidores entre TikTok e Instagram). La tasa por 100 vistas solo cuenta redes que tienen vistas e interacciones, porque YouTube no da interacciones por día y la diluía.
- **Descargador de redes** integrado como pestaña «Descargas» (6 motores: yt-dlp, gallery-dl, Instaloader, you-get, Streamlink y automático). Antes era un proyecto aparte en `Documentos\lagrima dlp`. Ver [[Descargador de redes - motores, diseño y panel]].
- **Código limpio**: lo repetido de las 5 páginas pasó a `web/comun.php` y `web/comun.js` (TikTok bajó de 264 a 59 líneas).

**Pendiente/decidido**: la tabla «Sep oct» de TikTok (un CSV de Instagram importado por error) **se deja**, no afecta a las sumas. Descargas sin probar en el PC. Notas: [[Panel web lagrim-stats]], [[Métricas y revisiones]], [[Alternativas a Metricool]]. Mapa: [[Redes]].

---

## 🩵 Webs · lagrim.art y panel
- Quieres el dominio **lagrim.art** (juego de palabras; «lagrimankv» te parece largo, prefieres «lagrim») para dos cosas: página para vender beats y tracking de redes en un subdominio privado tipo `stats.lagrim.art`.
- **Orden decidido:** primero la analítica, después ver si vale la pena la web. No comprar el dominio hasta tener algo que mostrar; no pagar la protección de GoDaddy (usar 2FA, bloqueo de transferencia y WHOIS gratis). Ver [[Web lagrim.art]].
- El panel debe correr solo en `localhost`: `descargas_api.php` ejecuta comandos. Si algún día se sube, solo `web/`, con contraseña. Mapa: [[Webs]].

---

## 🟡 Tienda y negocio · Alta de productos para Siigo
**Qué es:** herramienta propia, portable y con base de datos, para **reemplazar la creación de productos de CRS** y generar el Excel que se importa a **Siigo**, con etiquetas impresas en **BarTender**. CRS solo sirvió para hacer ingeniería inversa; ya no es necesario.

**Reglas de negocio que quedaron fijas**
- Grupo por defecto **Confecciones**; se usa **Referencia** en vez de código interno (ejemplo: «Body Vf2944»).
- **Precio:** costo sin IVA + 30 % de ganancia sobre el costo, luego + 19 % de IVA, redondeado hacia arriba a terminación 900 (76.000 → 117.572 → 117.900).
- **Códigos de barras de 6 dígitos** como los de CRS (no los EAN-13 que empiezan por 2000000), que **nunca se repiten**: índice único, contador que no baja y códigos eliminados reservados. El código de barras se guarda también como referencia.
- Siigo: máximo 500 registros por importación, plantilla desde Configuración → Productos y servicios → Importación, sin modificar columnas.

**Versión 2 (24 oct):** carpeta instalable con Node.js incluido e interfaz en el navegador, sin internet, guardado automático con copias, BarTender directo, Excel escrito sobre la plantilla sin tocar su formato (lotes de 500). Botón **Imprimir** con historial de sesión y log permanente; Ctrl+F7 reinicia la sesión de impresión; carpeta `configuracion\opciones.json` con impresora, BarTender y columnas de Siigo. Se corrigieron «Sesión no válida» y un servidor viejo que no imprimía. La impresora no se fija: se usa la de la tienda.

**Código y futuro:** repo privado de GitHub **kori496/ALTA** (dos personas con acceso, una sola mantiene la herramienta); `.gitignore` deja fuera `datos/`, `exportados/`, `node/` y las bases. Quieren integrarlo después a un **ERP en Laravel + PHP** en un servidor privado de la tienda (hoy maneja facturas y funciona como nube tipo drive). **Pendiente tuyo:** preguntar al desarrollador del ERP si tiene API. **Pendiente técnico:** plantilla real de Siigo y probar BarTender en la tienda. Ver [[Alta de productos - herramienta portable para Siigo]], [[Prompt - seguir Alta de productos con Claude Code]] y `Mapa Alta de productos.canvas`. Mapa: [[Tienda y negocio]].

---

## 🩷 Imágenes · V.YA
- V.YA es la tienda de ropa femenina elegante; el enfoque de venta son los **jeans barrel** y modelos con diseños o telas raras ([[Referencias de jeans]]).
- Solo se puede promocionar por **stories de Instagram y TikTok**; el público son clientas que ya conocen la tienda.
- Horario: días intercalados, un día de fotos/posts y al siguiente edición de video/fotos, de 17:30 a 19:00 (también en Google Calendar). Calendario de contenido en Notion hasta el **15 de noviembre**.
- Fotos en crudo en `agrupadas` (renombradas `prenda_XX_YY`), referencias de estilo en `VYA FOTOS SEPTIEMBRE`, salida vertical 1080×1920, solo el logo. Todo el trabajo de V.YA va en **un mismo chat/proyecto** («edición de stories»). Ver [[Edición de imágenes]]. Mapa: [[Imágenes]].

---

## 🟢 Programación · aprendizaje
Descargador de YouTube con Node, Express y yt-dlp aprendido paso a paso, sin que Claude escribiera el código (npm, `.gitignore`, GET vs POST, `req.body`, `spawn`). Lección práctica: la ruta que imprime yt-dlp falla con caracteres especiales en Windows, así que se busca el archivo nuevo en la carpeta de descargas. Ver [[Descargador de YouTube con Node y yt-dlp]] y [[Programacion]].

---

## 🟠 Herramientas y IA · REA, Ghidra y navegador propio
- **REA (reverse-engineer-anything)** instalado en Claude Code (`rea-agents@6.7.0`, MCP `rea` conectado) más un skill propio `analyze-apps-with-rea` para apps Electron. Ghidra: `GHIDRA_INSTALL_DIR` apuntaba al archivo `ghidraRun` y no a la carpeta raíz; arreglado y `rea doctor` en verde con Ghidra 12.2, aunque REA 6.7.0 pide 12.1.x para abrir binarios. Ver [[REA - ingeniería inversa]].
- **Primer análisis:** inventario de 60 opciones de [[FabFilter Pro-Q 4]] (fase 1; fases 2 y 3 en espera). Prompt en tres fases para analizar una app propia: [[Prompt - analizar app propia con REA]]. Índice: [[Análisis de apps con REA]].
- **Navegador propio** (fork de Zen, MPL-2.0): bloqueado, el PC tiene 9 GB libres y 8 GB de RAM. Opciones: compilar en la nube, más disco con artifact build, o solo mods. Ver [[Navegador propio - fork de Zen Browser]].
- Mapa: [[Herramientas y IA]].

---

## ⚪ Otros temas fuera del vault
- **Armado de PC:** lista «To-Do List: Armado de PC» en Notion (página Compras), componentes comprados sobre todo en Amazon.
- **Trampa conocida:** el PC a veces vuelve a una versión vieja de un archivo tras guardar (pasó con `server.js` e `index.html`). Verificar tamaño o contenido después de guardar.

---

## ~~Pendiente: ordenar carpetas físicas~~ · hecho el 3 nov 2026 (ver [[Inicio]] y [[Bitácora]])
Los mapas ya ordenan por tema, pero las carpetas siguen igual (`Videos beats/` mezcla multimedia, redes y webs). Mover archivos desde fuera de Obsidian rompe enlaces; hacerlo **arrastrando dentro de Obsidian** los actualiza solo. Propuesta de carpetas: `Multimedia/`, `Imagenes/`, `Programacion/`, `Webs/`, `Redes/`, `Tienda/`, `Herramientas y IA/`, `Sistema/`.
