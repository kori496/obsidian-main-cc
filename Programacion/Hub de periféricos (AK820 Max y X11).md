---
tags: [programacion, idea, perifericos]
actualizado: 2026-11-07
---

Volver a [[Programacion]]

# Hub de periféricos (AK820 Max y X11)

Idea: un programa propio que detecte mis periféricos y los configure todos desde un solo lugar, en vez de usar el software oficial de cada marca. Se llama **ATKHUB**. La v0.1 está hecha en Python (7 nov), en `Programacion/ATKHUB/`.

## Mis periféricos
- Teclado **Ajazz AK820 Max**. Ojo: hay dos modelos con el mismo nombre. El **Max HE** (switches magnéticos) y el **Max Plus** (tri-mode RGB, switches mecánicos). **El mío es el mecánico** (switches lineales Flying Fish, 82 teclas, batería de 8000 mAh, tri-mode). No es el HE. Falta ver si es igual al "Max Plus" que soporta `ak820ctl` (comparar VID/PID).
- Mouse **Attack Shark X11**.

## ATKHUB v0.1 (7 nov)
- Código: `Programacion/ATKHUB/` (leer su `README.md`). Python + `hidapi` (`pip install hidapi`). Se corre con `atkhub.bat <comando>` o `python -m atkhub <comando>`.
- Comandos: `detectar`, `teclado estado | efectos | luz | suspension`, `mouse info | polling | dpi`. Opciones al final: `--simular` (no toca nada) y `--debug` (muestra bytes).
- Teclado: confirmado que `1A2C:A036` es exactamente el cable del AK820 Max Plus de ak820ctl (el dongle es `1A2C:8FFF`). La interfaz de control es la MI_00 (usage page `0xFF02`).
- Mouse: comandos por reportes feature en la interfaz 2 (usage page `0x0B`). Confirmaciones y batería llegan por la colección de eventos (usage page `0x0A`). Para leer hay que pedir permiso con el reporte `0xA0`.
- **Peligro**: escribir el reporte `0x10` manda el X11 al bootloader y lo deja trabado. ATKHUB solo deja escribir los reportes conocidos.
- `mouse dpi` lee la config actual, verifica el checksum y cambia solo esa etapa.
- Las pruebas sin hardware pasan (`python -m unittest`). **Probado en el hardware real (7 nov): todo funciona** (teclado, `mouse info`, `mouse polling`, `mouse dpi`). Moverlo antes de cada comando si está por el dongle.
- Errores resueltos al hacerlo: la tabla DPI se copió mal la primera vez (el `fold` partió números); el checksum fijo del paquete DPI de ejemplo del driver (0x0F68) no cuadra con su propio byte 49, así que se recalcula siempre.
- **Error resuelto (7 nov, primera prueba real):** `teclado luz` congelaba la terminal. Causa: para vaciar respuestas viejas se leía con `read(n, 0)`, y en hidapi espera 0 **no** es "sin espera": llama a `hid_read`, que bloquea para siempre. Arreglo: función `vaciar()` en `hidutil.py` que lee con 1 ms y un tope de lecturas. Afectaba también al mouse. Prueba nueva con un HID falso que falla si alguien lee con espera 0 (14 pruebas pasan).
- **Mouse, primera prueba real (7 nov):** `mouse info` falló con "el mouse no dio permiso para leer el reporte 0x06" (por el dongle). Sospecha: el mouse estaba dormido (se duerme a los 30 s) o el dongle necesita más tiempo. Cambio: el permiso `0xA0` se pide hasta 3 veces con espera creciente (250/500/750 ms) y el error muestra los bytes recibidos. **Con ese cambio `mouse info` funcionó** (7 nov): era el mouse dormido o el dongle lento.
- Siguiente: luces del mouse, botones/macros, y después una interfaz gráfica.

## ATKHUB v0.2: luz y suspensión del mouse (7 nov)
- Reporte `0x05` (15 bytes por dongle, 13 por cable). Byte 3 = modo (nibble alto); 4 = sueño profundo alto | velocidad (1-5); 5 = sueño profundo bajo | brillo (1-8); 6-8 = RGB; 9 = sueño normal × 2; 10 = respuesta de botones ÷ 2; 11-12 = checksum (suma de 3 a 10).
- Modos que sirven en el X11: apagado, fijo, respiracion, neon, respiracion-color, fijo-dpi, respiracion-dpi. Los modos 7-11 del protocolo no hacen nada en este mouse.
- Comandos nuevos: `mouse modos`, `mouse luz MODO --color --brillo --velocidad`, `mouse suspension --normal MIN --profunda MIN`. `mouse info` ahora muestra luz y suspensión.
- Leen el paquete actual y cambian solo lo pedido (no pisa la suspensión al cambiar la luz).
- **La luz de la base de carga no se puede controlar desde el PC** (confirmado 7 nov): ni el software oficial de Attack Shark la maneja. Solo se apaga/enciende con el botón físico debajo de la base. Descartado para ATKHUB.
- El mouse se duerme por defecto a los 0,5 min; con `mouse suspension --normal 5` deja de dormirse tan rápido.
- 21 pruebas pasan, probado en el hardware (incluye el checksum del ejemplo documentado, `01 AF`).

## ATKHUB v0.4: interfaz gráfica estilo SteelSeries (7 nov)
![[gui-mouse-rendimiento.png]]
![[gui-teclado.png]]
- **Siluetas reales (7 nov, con fotos del usuario en `ATKHUB/referencias/`):**
  - Teclado AK820 Max: carcasa crema redondeada, teclas crema (`#ece6d9`), modificadores verde salvia (`#b7b8a2`: F5-F8, Delete, Backspace, Tab, Caps, Shift, Ctrl/Win/Alt/Fn, flechas, columna de navegación), naranja (`#ef7b31`: Esc, Enter, Espacio). Perilla plateada sobre la columna Home/PgUp, Delete a su izquierda, 3 luces indicadoras (C, W, batería) entre Backspace y Home. **No tiene pantalla.** Posiciones medidas en la foto de arriba (u = paso de tecla): F1 1.25, F5 5.5, F9 9.75, Delete 14, columna de navegación 15.4, flechas 13.2-16.2 bajadas 0.25u, ↑ en 14.2.
  - La vista previa del teclado es en 3 capas: carcasa+placa oscura (una vez), luces RGB entre teclas (cada cuadro), teclas con su color real (una vez). Las teclas son opacas, así que la luz se ve en los bordes, como en el real.
  - Mouse X11: blanco, frente más angosto que la parte trasera, botones principales rectos que terminan a media altura, rueda de goma negra, dos laterales largos a la izquierda, luz = dos franjas finas bajo los botones + LED. **El botón DPI está debajo** (junto al de modo BT/2.4G), se dibuja punteado.
  - **Silueta exacta del mouse (8 nov):** sale del PNG con **fondo transparente** que pasó el usuario (`referencias/mouse-recorte.png`): el contorno se toma de la transparencia (borde derecho reflejado, el X11 es simétrico) y se convierte en un trazo SVG; rueda, carcasa gris, costuras laterales, línea de botones (≈51 % del largo), LED y laterales medidos en el mismo PNG. Código en `gui/web/js/mouse.js` (`CUERPO`, `PARTES`, `DETALLE`).
  - Lo que **no sirvió**: el SVG trazado que mandó (potrace) solo tenía las líneas de adentro, no el contorno, porque el mouse es blanco sobre blanco. Sacar el contorno de una foto con fondo blanco tampoco es fiable (se "come" partes muy blancas del botón). **Para siluetas: pedir PNG con fondo transparente.**
  - Para el 3D futuro: usar estas mismas fotos y medidas.
- Abrir: doble clic en `ATKHUB GUI.bat` (o `atkhub gui`). Requiere `pip install hidapi pywebview`. `--simular` para verla sin periféricos, `--navegador` para abrirla en el navegador.
- **Decisión:** Qt no se pudo instalar ni probar en la sesión, así que la ventana es HTML/CSS/JS dentro de una ventana nativa (pywebview + WebView2 de Windows), igual que SteelSeries GG. Python sigue siendo el núcleo. Así pude renderizarla y probarla con Chrome + Playwright.
- Arquitectura: `atkhub/gui/api.py` (métodos que devuelven JSON, un candado por dispositivo para que nunca haya dos comandos a la vez), `servidor.py` (servidor local solo en 127.0.0.1, con **token** aleatorio en cada llamada para que ninguna web pueda mandar comandos), `app.py` (ventana; si falla, abre el navegador), `web/` (index.html, estilo.css, js/app.js, ui.js, mouse.js, teclado.js).
- Pantallas: Mouse → Rendimiento (diales de DPI arrastrables/rueda/teclado, polling con onda animada), Iluminación (efectos, selector de color con historial, brillo, velocidad, brillo animado del mouse), Botones (dibujo del mouse con llamadas B1-B8, selector de acciones con búsqueda, captura de atajos, editor y **grabadora** de macros), Energía. Teclado → Iluminación (vista previa animada de los 16 efectos en canvas) y Energía.
- Barra inferior como SteelSeries: **Vista previa en vivo** (aplica al instante, agrupando cambios), **Revertir** (vuelve a lo último guardado), **Guardar** (Ctrl+S). Solo se manda lo que cambió.
- Rendimiento: animaciones solo con transform/opacity; el teclado se dibuja a 60 fps con una capa estática pre-pintada y se pausa si no se ve; las lecturas del mouse van en hilos (la ventana no se congela).
- El teclado no deja leer su luz: la última config se guarda en `%APPDATA%\ATKHUB\estado.json` (con el historial de colores).
- Errores resueltos: el brillo del mouse tapaba el dibujo (faltaba `z-index` al SVG); columnas que no cabían en 1280 px; la lista de efectos movía toda la página (ahora tiene su propio scroll); en Windows el registro puede servir `.js` como `text/plain` y romper los módulos → tipos fijos en el servidor; `ATKHUB.bat` chocaba con `atkhub.bat` (Windows no distingue mayúsculas) → `ATKHUB GUI.bat`.
- 36 pruebas pasan (incluye servidor: token, no salir de la carpeta web, flujo completo). Capturas en `Programacion/ATKHUB/capturas/`.

## ATKHUB v0.3: botones y macros del mouse (7 nov)
- Código en `atkhub/mouse_botones.py`. Comandos: `mouse acciones`, `mouse botones [--restaurar]`, `mouse boton BOTON ACCION`, `mouse macro N "secuencia" [--boton] [--modo] [--veces]`.
- Botones (reporte `0x08`, 59 bytes): 18 slots de 3 bytes (acción, modificadores, tecla), checksum en 57-58. Botones del X11 por slot de escritura: izquierdo 1, derecho 2, medio 3, dpi 6, adelante 7, atrás 8, rueda arriba 17, rueda abajo 18.
- **El firmware reordena al leer**: escribir 7→leer 5, 8→6, 6→8, 17↔18; escribir 5 no hace nada; leer 7 = `0x3C` (tecla de modo, protegida). **Error del driver de referencia**: al releer y reescribir pone el `0x3C` en el slot 7 (botón adelante). ATKHUB usa la tabla de la doc y nunca escribe `0x3C`.
- Acciones: clics, DPI, multimedia, navegador, `tecla:ctrl+c` (acción `0x11`), `macro:N` (`0x12`).
- Macros (reporte `0x09`, 3 paquetes de 64): modo, color, repeticiones, nombre (20 bytes), cuenta de pasos, 100 bytes de pasos. Paso = 2 bytes (soltar|espera/10, código) o 4 bytes si espera > 1270 ms. Checksum: suma de p1[4:64] + p2[4:64] + p3[4:9]. Clics en macro: F1-F5.
- Cambiar el clic izquierdo pide `--forzar`. Arreglo si algo queda mal: `mouse botones --restaurar`.
- 31 pruebas pasan (incluye que la lectura de fábrica de la doc se convierte exactamente en la escritura de fábrica).

## IDs USB (sacados con PowerShell, 7 nov)
- **Mouse X11 (dongle):** `VID_1D57&PID_FA60`. **Coincide** con `attack-shark-x11-driver`, que soporta 1d57:fa60 y 1d57:fa55. Ese driver hace DPI, polling (125–1000 Hz), remapeo, macros y luces. Todavía no lee la batería ni la configuración actual.
- **Teclado AK820 Max:** `VID_1A2C&PID_A036`. Tiene interfaces "definidas por el proveedor" (MI_00 y MI_02 COL05), que es por donde se le mandan los comandos. `ak820ctl` no publica su lista de IDs, pero dice que la mayoría de los Ajazz usan el mismo protocolo. Falta probarlo.
- Comando para listar: `Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match 'VID_' -and ($_.Class -in 'Keyboard','Mouse','HIDClass') } | Select-Object Class, FriendlyName, InstanceId`
- Ojo: "Teclado PS/2 estándar" no es el Ajazz (es del sistema, no tiene VID/PID).

## Qué ya existe (código abierto, sirve para copiar el protocolo)
- **Mouse X11:**
  - `attack-shark-x11-driver` (HarukaYamamoto0, TypeScript, MIT): librería para configurar el X11.
  - `attack-shark-x11-electron` (dressedinblack5, MIT): driver multiplataforma con interfaz Electron (Rust + libusb).
- **Teclado:**
  - `ak820ctl` (shrey715, Python, MIT, en PyPI): para el **AK820 Max Plus**. Hace luces, colores por tecla, remapeo, macros, sleep, tiempo de respuesta y batería, por cable o dongle 2.4G. Los comandos son reportes HID de 64 bytes que empiezan con `aa 55 cc 33`, a la interfaz vendor (usage page `0xff02`). Tiene `PROTOCOL.md` con la tabla de comandos. Le falta: firmware, botones de mouse y un comando sin identificar (`0x0A`).
  - `openajazz` (Rust): RGB y sincronizar la hora en AK820, AK35i y AULA F75 Max.
  - `ak820pro-modder` (Tauri): para el AK820 **Pro**. Su protocolo puede servir de pista para la pantalla TFT.
  - Si mi teclado es el **Max HE** (magnético), puede que no haya nada hecho para el punto de activación y el rapid trigger. Eso tocaría sacarlo capturando el tráfico USB del driver oficial (Wireshark + USBPcap).

## Cómo lo armaría
1. Detectar los dispositivos por VID/PID con `hidapi`.
2. Un módulo por dispositivo, que se base en el protocolo de los proyectos de arriba.
3. Interfaz con Tauri o Electron.
4. Probar primero con comandos de solo lectura (batería, información) antes de escribir en la memoria del dispositivo.
5. Cerrar el software oficial mientras se prueba, para que no choquen.

## Pendiente
- Orden acordado: (1) luces del mouse ✅ v0.2, (2) botones/macros del mouse ✅ v0.3, (3) interfaz gráfica ✅ v0.4 (las dos últimas sin probar en el hardware).
- v0.2 probada en el hardware (7 nov): `mouse luz` y `mouse suspension` funcionan.
- **PowerShell:** `#` empieza un comentario, así que `--color #C8B49A` llega vacío. Usar el hex sin `#` (`--color C8B49A`) o entre comillas.
- Siguiente: probar en el hardware v0.3 (botones/macros) y v0.4 (interfaz gráfica).
