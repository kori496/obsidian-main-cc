---
tags: [programacion, rea, ingenieria-inversa, analisis-de-apps, vst3, fabfilter]
actualizado: 2026-10-25
---

Volver a [[Análisis de apps con REA]]

# FabFilter Pro-Q 4 (VST3, versión 4.13)

## Resumen
- **No es una app propia**: es un plugin comercial de FabFilter B.V. (lo dice el `Readme.txt`). El análisis es estático y se limita a qué hace el plugin en el sistema. No se analiza la lógica de licencia ni de activación.
- `C:\Program Files\FabFilter\Pro-Q 4` solo tiene la ayuda (`FabFilter Pro-Q 4.chm`), el icono, el `Readme.txt` y el desinstalador. El código real está en `C:\Program Files\Common Files\VST3\FabFilter\FabFilter Pro-Q 4.vst3`: una DLL PE32+ x86-64 de un solo archivo (no es una carpeta-bundle), 4 784 128 bytes, SHA-256 `292580739f88e8d48662aa25b5b4022a03657a0c2d4331f2f1216db9b6229271`.
- Exporta `GetPluginFactory` (0x180106f90, VST3) y `VSTPluginMain` (0x180106fa0, punto de entrada VST2).
- Estado: FASE 1 hecha. **FASE 2: bloques 1 y 2 (opciones 1-20) hechos** con Ghidra 12.1.4 vía REA (25 oct 2026). Siguen los bloques 3-6 y la FASE 3.

## Tabla de opciones (FASE 1)
La evidencia es la dirección virtual (VA) de la cadena dentro de la DLL, o el import o valor de registro. **confirmado** = la opción existe en el binario (cadena de UI o menú, import) o se vio en el registro o en disco. **probable** = deducido por asociación, sin traza de código.

| nº | Opción / función | Dónde | Estado |
|---|---|---|---|
| 1 | Undo | cadena 0x180236840 | confirmado |
| 2 | Redo | 0x1802368b8 | confirmado |
| 3 | A/B (dos estados) | 0x1802368f0 | confirmado |
| 4 | Copy (guarda en A y B) | 0x1802369a0 | confirmado |
| 5 | Preset anterior / siguiente | 0x180236a70 / 0x180236b50 | confirmado |
| 6 | Menú y navegador de presets (Search, favoritos, etiquetas, Author..., Description...) | 0x180236ac0, 0x180233380-0x1802336d0 | confirmado |
| 7 | Open Other Preset... / Save As... (.ffp) | 0x1802386e8, 0x180233408, filtro 0x180238998; imports `GetOpenFileNameW`/`GetSaveFileNameW` | confirmado |
| 8 | Change Preset Folder... | 0x180238700, 0x180238438; `SHBrowseForFolderW`; registro `PresetFolder` | confirmado |
| 9 | Refresh / Restore Factory Presets (**corregido**: Revert y Load Factory Settings son del menú MIDI Learn, ver nº 13) | 0x180238718, 0x1802382b0 | confirmado |
| 10 | Options > Save As Default / Favorite (Favorites.txt) | 0x180238278, 0x180238268, 0x18022d160, cabecera 0x18022d3e8 | confirmado |
| 11 | Enable MIDI Program Changes | 0x180238460; registro `EnableMIDIProgramChanges` | confirmado |
| 12 | Presets de componente (.ffpresetmap, «Component Presets») | 0x180238a80, 0x180239e00, 0x18023a5b8; carpeta `%APPDATA%\FabFilter\Pro-Q 4\Component Presets` | confirmado |
| 13 | MIDI Learn: botón y menú (Enable MIDI, Clear, Clear All) | 0x180236d40, 0x180237070, 0x180238988, 0x180238720/28; archivo `MidiControllerMap.ffm` (0x18023a470) | confirmado |
| 14 | Resize / Scaling (tamaños, Custom Size, Monitor Default) | 0x180237180, 0x1802358d8, 0x180238840; registro `InterfaceWidth/Height`, `ScalingAdjustments` | confirmado |
| 15 | Full Screen | 0x180236c40 | confirmado |
| 16 | Menú Help: Help Topics (CHM), Show Interactive Help Hints, Show Component Displays, FabFilter Web Site, FabFilter Support, About | 0x1802388d0-0x18023897c, `HelpFileName` 0x18023cf00; import `ShellExecuteW` | confirmado |
| 17 | Enter License... / Purchase / Evaluate (diálogo `WINDOWSLICENSEDIALOG`) | 0x180238968, 0x180238958, 0x180235e40; recurso tipo 5; URL `https://www.fabfilter.com/activate/?c=` 0x18022d598 | confirmado (no se analiza por dentro) |
| 18 | Deauthorize... | 0x180238948; `https://www.fabfilter.com/api/v1/device-registration/unregister` 0x180238890 | confirmado |
| 19 | Registro del dispositivo (`deviceName`, `deviceId`) | `.../device-registration/register` 0x1802389e0, 0x1802389d0, 0x180238870; imports WinINet, `GetAdaptersInfo`, `GetComputerNameExW` | probable (cuándo se llama) |
| 20 | Enlaces Shop / Beta | 0x1802387a0, 0x1802387c0 | confirmado |
| 21 | Banda EQ: Frequency, Gain, Q (arrastrar o escribir el valor) | 0x1802436e0, 0x180243ba0, 0x180243860 | confirmado |
| 22 | Shape y Slope de banda (menú de pendiente) | 0x180242de0, 0x180243180, 0x180243360 | confirmado |
| 23 | Stereo Placement / Surround / altavoces (All, LFE) | 0x180242930, 0x180242cd0, 0x180242bb0 | confirmado |
| 24 | Split, Delete, Bypass y Solo de banda | 0x180243050, 0x180243510, 0x1802435d0, 0x180245000 | confirmado |
| 25 | Gain-Q Interaction | 0x1802439b0; registro `GainQInteraction` | confirmado |
| 26 | Dinámica: Dynamic Range, auto/manual (<< >>), Threshold, Attack/Release, Delete/Bypass Dynamics | 0x180243f10, 0x180243d40, 0x180244340, 0x180244650, 0x180244210, 0x180244290 | confirmado |
| 27 | Side chain externo y filtrado (Low/High, Audition) | 0x180244590, 0x180244870, 0x18024d410 | confirmado |
| 28 | Spectral (botón, Density, Tilt) | 0x180244090, 0x1802449d0, 0x180244c40 | confirmado |
| 29 | Menú desplegable de banda (Select All, Invert Gain, Make Dynamic/Spectral, Paste, Delete Disabled...) | 0x180244b40, 0x18022d988-0x18022db28; portapapeles (`OpenClipboard`/`SetClipboardData`) | confirmado |
| 30 | Banda anterior / siguiente | 0x1802427c0, 0x18024b710 | confirmado |
| 31 | Analizador: Pre/Post, SC/Ext, Resolution, Range, Tilt, Speed, Freeze, Collisions, Spectrum Grab | 0x180246960, 0x180246800, 0x180246a00-0x180246d70, 0x18024d4f0-0x18024d5f0 | confirmado |
| 32 | Display Range y Auto-Adjust Display Range | 0x180245b00, 0x18024b7b8; registro `AutoAdjustDisplayRange` | confirmado |
| 33 | Piano Roll | 0x180245ff0; registro `PianoRoll` | confirmado |
| 34 | EQ Sketch y Auto-EQ Sketch | 0x180245d50, 0x18024b7d8; registro `AutoEQSketch` | confirmado |
| 35 | EQ Match (referencia: Input, Other Instance, Sidechain, espectro guardado; Save Input As Reference Spectrum...; Load File... wav/aiff/flac) | 0x180246130, 0x1802408d8, 0x180240900, 0x18023f268-0x18023f6f8 | confirmado |
| 36 | Collision Reference | 0x180245c30 | confirmado |
| 37 | Show Frequency On Hover / Show EQ Parameter Display / Use Accessible Colors | 0x18024b780, 0x18024b798, 0x18024b7f0; registro `ShowMouseFrequency`, `UseAccessibleColors` | confirmado |
| 38 | Processing Mode (Zero Latency / Natural / Linear Phase) y Resolution | 0x180247610, 0x180247450, 0x18024d1c8 | confirmado |
| 39 | Character (Clean / Subtle / Warm) | 0x180247bc0, 0x18024d6f8 | confirmado |
| 40 | Salida: Level, Pan, Pan Mode (L/R o M/S), Phase Invert, Gain Scale, Auto Gain, Global Bypass | 0x1802480f0, 0x180248030, 0x180248830, 0x1802484c0, 0x180248620, 0x1802483d0 | confirmado |
| 41 | Emphasize (+6 dB temporal) | 0x1802376c0 | confirmado |
| 42 | Lista de instancias (Pro-Q 4, Pro-C 3, Pro-G, Pro-DS): abrir/cerrar, zoom, Auto Zoom, Minimap, filtro, Maximize | 0x180244e50, 0x180245220-0x180245920; registro `InstanceListZoomLevel`, `InstanceListAutoZoom`, `InstanceListShowMinimap` | confirmado |
| 43 | Pin, Filter Pinned, Pin Similar Colors, Save Pinned Set (.pinset), Unpin All | 0x1802459c0, 0x1802458b0, 0x18024a738, 0x180249318, 0x18024a9e8, 0x18024aa20; carpeta `Pinned Instance Sets` | confirmado |
| 44 | Quick Jump / opciones de teclado de la lista | 0x1802455a0, 0x18024aa30; registro `InstanceListKeyAction` | confirmado |
| 45 | Menú de instancia: copiar/pegar ajustes entre instancias | 0x1802374a0 | confirmado |
| 46 | Bypass de instancia (desde la lista) | 0x180237550 | confirmado |
| 47 | Parámetros VST3 automatizables (Band N Frequency/Gain/..., Analyzer..., Auto Gain, Receive Midi...) | 0x18024d2b4-0x18024d6d0 | confirmado |
| 48 | Mensajes internos controlador ↔ procesador VST3 (`FF_Msg_*`: Setup, SampleRate, PresetName, RealTimeData, LatencyChange, MidiMessage...) | 0x18023c098-0x18023c1f8 | confirmado (existen); uso: probable |
| 49 | Memoria compartida entre instancias («FabFilterInstances2», «FabFilterProcess2») | 0x1802381e0, 0x180239b98; imports `CreateFileMappingW`/`MapViewOfFile` | probable |
| 50 | Entrada MIDI (Midi In, Pitch Bend, Channel Pressure) | 0x18023c368, 0x18023c2e0, 0x18023c2f0 | confirmado |
| 51 | Nombre/color/índice de pista del host y detección del host (Cubase, Ableton, Bitwig, WaveLab...) | 0x18023bf98-0x18023bfe0, 0x18023a8e0-0x18023a930, 0x18023c394-0x18023c3d8 | confirmado (cadenas); uso: probable |
| 52 | Al iniciar: lee y escribe ajustes en `HKCU\Software\FabFilter\Pro-Q\4.0` | 0x18022ce18; imports `RegOpenKeyExW`/`RegCreateKeyExW`/`RegSetValueExW`; valores vistos en el registro | confirmado |
| 53 | Al iniciar: indexa presets (`PresetCache.dat`, «Indexing Presets...») | 0x180233418, 0x18023a5e8; archivo en `%APPDATA%\FabFilter\Pro-Q 4\` | confirmado |
| 54 | Lee `ProgramFilesDir` de `HKLM\Software\Microsoft\Windows\CurrentVersion` (**corregido**: es el plan B para la carpeta de datos si falla `%APPDATA%`, `FUN_18001fc80`) | 0x18023d028, 0x18022d050 | confirmado |
| 55 | Log de depuración `FabFilter.log` («*** Begin debug session ***») | 0x18022cd88, 0x18022cd98 | probable (no se sabe si se activa en esta build) |
| 56 | Aceleración gráfica OpenGL / escalado HiDPI | registro `GraphicsAcceleration`, `RetinaEnabled` (0x18023a638, 0x18023a650); imports OPENGL32 | confirmado |
| 57 | Ajuste oculto `VST2_DefaultToNoSideChain` | 0x18023a660 | probable |
| 58 | Consulta `Software\Classes\CLSID\` | 0x18023ceb0 | probable (propósito desconocido) |
| 59 | Arrastrar y soltar archivos en la ventana | imports `DragAcceptFiles`/`DragQueryFileW` | probable (qué archivos acepta) |
| 60 | Valores guardados que no tienen botón visible en esta tabla: `showWelcomeHint`, `PresetBrowserTypeToSearch`, `ShowOutputLevelMeter`, `InterfaceLayout` | registro `HKCU\...\Pro-Q\4.0`; 0x180239d98, 0x180239dc0, 0x18023a6a8 | confirmado |

**No encontrado** (búsqueda acotada a cadenas e imports): argumentos de línea de comandos (es una DLL que carga el host), claves `Run` o inicio con Windows, tareas programadas, lanzamiento de procesos aparte de `ShellExecuteW` (abrir URL o ayuda), endpoints distintos de `www.fabfilter.com`.

## Detalle por opción (FASE 2)
Funciones con el nombre que les pone Ghidra (`FUN_<dirección>`). «Confirmado» = visto en el pseudocódigo. «Probable» = el salto pasa por una llamada virtual o una tabla de funciones (vtable) que Ghidra no resuelve sola.

### Bloque 1 (opciones 1-10): barra superior y presets
- **Menú de presets**: lo construye `FUN_1800d7050`. Cada opción guarda la dirección de su manejador: Enable MIDI Program Changes → `FUN_1800d4b40`; Save As Default → 0x1800ddb14; Open Other Preset → `FUN_1800d81e0`; Change Preset Folder → 0x1800ddb74; Restore Factory Presets → `FUN_1800da090`; Refresh → `FUN_1800da060` (confirmado). 0x1800ddb14 y 0x1800ddb74 son mini-funciones que solo saltan a una entrada de la vtable (`mov rax,[rcx]; jmp [rax+0x170]` y `[rax+0x120]`). Leyendo las vtables (0x1802390a8 y otras dos iguales) se llega a `FUN_1800da160` y `FUN_1800d47e0` (probable).

1. **Undo**, 2. **Redo**: REA/Ghidra **no pudo enlazarlos**. Las únicas referencias a `IconUndo`/`IconRedo` están en una tabla de datos (0x180227e00/08) que ningún código usa directamente. Probable: solo cambian el estado en memoria, sin efectos en el sistema.
3. **A/B**, 4. **Copy**: no enlazados. Solo se encontró el tooltip. Probable: estado en memoria.
5. **Preset anterior/siguiente**: no enlazado directamente. Probable: carga el `.ffp` anterior o siguiente de la lista indexada (ver 6).
6. **Navegador e indexado de presets**: `FUN_18002af90` recorre la carpeta de presets (`FUN_18002a020`, con un límite de 0x9c4 = 2500 entradas; probable) y `FUN_18001e3c0` lista archivos con `FindFirstFileW` (confirmado). Caché en `PresetCache.dat` (`FUN_1800e6060`). Ruta en disco vista: `%APPDATA%\FabFilter\Pro-Q 4\PresetCache.dat`. El enlace entre la función y esa ruta es probable. Si falla la lectura, muestra «Unable to read presets…» (`FUN_1800af370`).
   - Efectos: lee la carpeta de presets y escribe `PresetCache.dat`. Sin red ni registro.
7. **Open Other Preset… / Save As…**:
   - Open: `FUN_1800d81e0` abre un diálogo con el filtro `FabFilter Presets (*.ffp)` y empieza en la carpeta de presets. `GetOpenFileNameW` solo se llama en `FUN_18014bd60` (0x18014bfd6). El salto hasta ahí es una llamada virtual (probable). Solo lee el `.ffp` elegido.
   - Save As: lo arma `FUN_1800dbb50`. El de presets de componente es `FUN_1800dc0b0` (filtro «Component Preset»). `GetSaveFileNameW` está en `FUN_18014bd60` (0x18014bfde). Escribe el `.ffp` donde elijas.
8. **Change Preset Folder…** → `FUN_1800d47e0` (confirmado):
   - Abre el diálogo «Select a folder to store your presets». `SHBrowseForFolderW` solo se usa en `FUN_18014c240` (probable).
   - Si aceptas: reindexa la carpeta (`FUN_18002af90`), guarda los ajustes (`FUN_1800eacc0`) y actualiza favoritos y caché (`FUN_18002b160`).
   - `FUN_1800eacc0` usa un `RegistryWriter` sobre `HKCU` (0x80000001) y la clave `Software\FabFilter\<producto>\<versión>` que arma `FUN_180020c00`; en tu PC es `HKCU\Software\FabFilter\Pro-Q\4.0`. Escritura con `RegCreateKeyExW` (permiso total, 0xF003F) + `RegSetValueExW` (`FUN_18014cdb0`, `FUN_18014ced0`, `FUN_18014cff0`).
   - El valor se llama `PresetFolder` (`FUN_1800ead60`, que también comprueba que la carpeta existe con `GetFileAttributesW`).
   - Carpeta por defecto (`FUN_180020990`): Documentos (`SHGetSpecialFolderLocation` con CSIDL 5, en `FUN_18001fe80`) + `FabFilter\Presets\<producto>\`. Si falla, usa `C:\My Documents`. Por eso en tu PC queda en `OneDrive\Documentos\...`, porque Documentos está redirigido a OneDrive.
   - Las carpetas se crean de forma recursiva con `CreateDirectoryW` (`FUN_18001f330`); que se use justo aquí es probable.
9. **Refresh**: `FUN_1800da060` → `FUN_18002b060` vuelve a leer la lista de presets. **Restore Factory Presets**: `FUN_1800da090` pide confirmación; al aceptar, `FUN_1800dd7b0` → `FUN_1800e8340(sobrescribir=1)`:
   - Saca del recurso RCDATA `WINDOWSSETUPDOCS` (415 841 bytes, formato de archivo comprimido con firma `FS/ISB/3`; `FUN_18001f690`, `FUN_18001f190` con `FindResourceW`, `FUN_18014d150`) dos carpetas:
     - `ApplicationData` → carpeta de datos del plugin (probable `%APPDATA%\FabFilter\Pro-Q 4`).
     - `FactoryPresets` → tu carpeta de presets.
   - **Sobrescribe** los presets de fábrica y el preset por defecto, y luego reindexa. Si la carpeta es de solo lectura, sale «Unable to restore all factory presets».
10. **Save As Default** → `FUN_1800da160` (probable por la vtable): serializa el estado actual (`FUN_180022e20`) y lo guarda como preset dentro de la carpeta de presets. Es lo que abren las instancias nuevas. **Favorite** → `FUN_1800dafb0` / `FUN_180028ab0`: escribe `Favorites.txt` en la carpeta de presets, con la cabecera «# == FabFilter Preset Favorites File ==» (confirmado).

**Extra (nº 11)**: `FUN_1800d4b40` cambia el indicador de Program Changes en memoria (`DAT_1802bdfe8+0x78`). `FUN_1800ec870` es el que guarda todos los ajustes en el registro; ahí se ven los nombres `EnableMIDIProgramChanges`, `GraphicsAcceleration`, `LicenseError`, `RetinaEnabled`, `showInteractiveHelp`, `showWelcomeHint`, `ShowComponentDisplays`, `PresetBrowserTypeToSearch`… (confirmado). `FUN_1800e9450` lee `GraphicsAcceleration` y `RetinaEnabled` de `HKCU\Software\FabFilter` y, según un indicador interno, también lee de **HKLM** (solo lectura).

**Bloque 1 sin**: red, procesos lanzados, variables de entorno, tareas programadas, inicio con Windows ni privilegios elevados (todo se escribe en HKCU y en tus carpetas).

### Bloque 2 (opciones 11-20): MIDI, interfaz, ayuda, licencia y red
La licencia y la activación se describen solo por sus efectos (URL, datos enviados, cuándo). No se analizó cómo se valida la clave.

- **Carpeta de datos del plugin** (`FUN_180020770` → `FUN_18001fc80`): `SHGetSpecialFolderLocation` con CSIDL 0x1A (`%APPDATA%`) + `FabFilter\<producto>`. Si falla, usa `ProgramFilesDir` de `HKLM\Software\Microsoft\Windows\CurrentVersion` y, si también falla, `C:\Program Files` (confirmado). En tu PC: `C:\Users\sharo\AppData\Roaming\FabFilter\Pro-Q 4`.

11. **Enable MIDI Program Changes**: `FUN_1800d4b40` cambia el indicador en memoria y `FUN_1800ec870` lo guarda en `HKCU\Software\FabFilter\Pro-Q\4.0\EnableMIDIProgramChanges` (confirmado).
12. **Presets de componente**: `FUN_1800f09f0` arma los nombres `PresetMap_<n>.ffpresetmap`. Dentro de la DLL hay tres recursos `PRESETMAP_FQ3P_1..3`; probablemente sirven para traducir presets de Pro-Q 3. `FUN_1800dbdc0` busca el componente «Default» (si no existe: «Default component preset not found.»). Para guardar se usa `FUN_1800dc0b0` (diálogo «Component Preset»). Carpeta vista en disco: `%APPDATA%\FabFilter\Pro-Q 4\Component Presets`.
13. **MIDI Learn** (menú `FUN_1800d6490`):
    - Enable MIDI → `FUN_1800d7f90`: pone a 1.0 o 0.0 el parámetro «Receive Midi». Sin efecto en el sistema.
    - Clear: un submenú por parámetro (`FUN_1800ce830`).
    - Revert, Save, Load Factory Settings y Clear All: saltan a funciones del controlador de MIDI (vtable +0x118, +0xf8, `FUN_1800d7f80`, +0x100). Qué opción va a qué entrada es probable.
    - Archivo `MidiControllerMap.ffm` en la carpeta de datos: se lee con `FUN_1800e8e70` (`BinaryFileReader`); si no existe, se usa el mapa de fábrica que va dentro de la DLL (`FUN_1800e8ce0`, `BinaryResourceReader`); se escribe con `FUN_1800ea900` (crea la carpeta con `FUN_18001f330` + `BinaryFileWriter`). Confirmado.
14. **Resize / Scaling**: el botón lo arma `FUN_1800c2110` y el menú de escalado `FUN_1800d4130`. `FUN_1800ec340` guarda en HKCU `InterfaceLayout`, `InterfacePanels`, `InterfaceWidth`, `InterfaceHeight` y `ScalingAdjustments` (confirmado). `FUN_1800e6dc0` lee `InterfaceDefaults.ffd` de la carpeta de datos (probable: tamaño por defecto).
15. **Full Screen**: el botón lo arma `FUN_1800c26a0`. No se encontraron efectos fuera de la ventana (probable).
16. **Menú Help** (`FUN_1800d5bc0`):
    - Help Topics → 0x1800d5aa0 (mini-función: llama al sistema de ayuda con −2). La ruta del `.chm` se lee del valor `HelpFileName` en `HKCU` y luego en `HKLM\Software\FabFilter\Pro-Q\4.0` (`FUN_1801071e0`, confirmado). Que se abra con `ShellExecuteW` (`FUN_1800e41b0`) es probable.
    - Show Interactive Help Hints → `FUN_1800d58a0` y Show Component Displays → `FUN_1800d57d0`: cambian indicadores que `FUN_1800ec870` guarda como `showInteractiveHelp` y `ShowComponentDisplays` (confirmado).
    - FabFilter Web Site → `FUN_1800d59c0` y Support → `FUN_1800d5a30`: piden la URL a `FUN_1800d4e70` (índice 0 = `https://www.fabfilter.com/`, 1 = `/support/`) y la abren en el navegador por defecto (`ShellExecuteW` con verbo nulo = abrir; la función exacta es probable).
17. **Purchase / Enter License / About**:
    - Purchase → `FUN_1800d5950`: URL índice 2 = `https://www.fabfilter.com/shop/` + sufijo del producto. Solo aparece si no hay licencia.
    - Enter License → `FUN_1800d5850`: abre el diálogo y, si se acepta, guarda los ajustes en HKCU (`FUN_1800eacc0`). El contenido de la validación no se analizó.
    - About → `FUN_180054450` (abre la vista «Acerca de»).
    - `FUN_180035d50` abre en el navegador `https://www.fabfilter.com/activate/?c=<código>` (`ShellExecuteW`, confirmado).
18. **Deauthorize…**: `FUN_1800d5220` pide confirmación («This will deauthorize all plug-ins on this computer…») → `FUN_1800dd950` → `FUN_1800d52e0`. Este hace un GET a `https://www.fabfilter.com/api/v1/device-registration/unregister?code=<…>&deviceId=<…>`, borra la licencia guardada (`FUN_180034db0`) y avisa «deauthorized successfully» (confirmado).
19. **Registro del dispositivo** (red, confirmado):
    - **Cuándo**: `FUN_1800d75e0` (probablemente al abrir la interfaz). Si hay licencia y pasaron más de **604 800 s (7 días)** desde el último registro, llama a `FUN_1800d88e0`.
    - **Qué envía**: GET a `https://www.fabfilter.com/api/v1/device-registration/register?code=<…>&deviceId=<…>&deviceName=<…>`.
      - `deviceName` = **nombre del PC** (`GetComputerNameExW`, ComputerNamePhysicalDnsHostname).
      - `deviceId` = identificador con forma de GUID que arma `FUN_180036180` a partir de las **direcciones MAC** de las tarjetas de red (`FUN_180020410`: `GetAdaptersInfo`, bytes en `%.2x` unidos con `-`).
    - **Cómo**: `FUN_18001e950` usa `InternetOpenUrlW` (flags 0x40200) en otro hilo (`FUN_18001ee40`) y lee la respuesta en bloques de 1 KB.
    - **Sin licencia**: el mismo `FUN_1800d75e0` arma un temporizador de 600 000 ms (10 min) y un aviso (`FUN_1800d8e90`; del 16 al 31 de diciembre usa otra variante, `FUN_1800d9070`). Ambos pueden abrir el navegador con `ShellExecuteW`.
20. **Shop / Beta**: `FUN_1800d4e70` índice 2 = `/shop/`, índice 3 = `/beta/`. Dónde se usa `/beta/` es probable (avisos de beta caducada).

**Bloque 2 sin**: procesos lanzados aparte del navegador o la ayuda (vía `ShellExecuteW`), variables de entorno, tareas programadas, inicio con Windows ni privilegios elevados. HKLM solo se **lee**.

## Configuración (lo visto hasta ahora)
- Registro: `HKCU\Software\FabFilter\Pro-Q\4.0`. Valores vistos: `EnableMIDIProgramChanges, GraphicsAcceleration, LicenseError, RetinaEnabled, showInteractiveHelp, showWelcomeHint, ShowComponentDisplays, PresetBrowserTypeToSearch, AutoAdjustDisplayRange, AutoEQSketch, InstanceListAutoZoom, InstanceListKeyAction, InstanceListZoomLevel, InstanceListShowMinimap, ShowMouseFrequency, UseAccessibleColors, InterfaceLayout, InterfaceWidth, InterfaceHeight, ScalingAdjustments, GainQInteraction, PianoRoll, ShowOutputLevelMeter, PresetFolder, CurrentVersion`. Los valores de licencia no se leyeron.
- `%APPDATA%\FabFilter\Pro-Q 4\`: `MidiControllerMap.ffm`, `PresetCache.dat`, `Component Presets\Spectrum`, `Pinned Instance Sets`.
- Carpeta de presets: `PresetFolder` = `C:\Users\sharo\OneDrive\Documentos\FabFilter\Presets\Pro-Q 4\`.

## Límites del análisis
- Sin Ghidra no hay xrefs ni pseudocódigo: las direcciones son de **cadenas**, no de funciones. No se sabe qué función usa cada cadena ni en qué orden se ejecuta.
- La licencia y la activación quedan fuera a propósito (solo se listan como opciones).
- Lo que depende del host (nombres de pista, colores, layouts de canales) solo se ve en ejecución.

## Qué NO funcionó
- El MCP `rea` no conectó en esta sesión (timeout de 30 s). Se usó la CLI `rea` 6.7.0 (`C:\Users\sharo\AppData\Roaming\npm\rea`).
- `rea inspect <dll> --provider ghidra` → `provider_unavailable` por dos motivos:
  1. `unsupported_version`: REA 6.7.0 solo acepta **Ghidra 12.1.x** (verificado con 12.1.4). Con 12.2 `rea doctor` sale verde, pero `open_binary` lo rechaza.
  2. `runtime_unavailable` de Java: «Owned Windows process requires an absolute executable path [java.exe]». Falta `JAVA_HOME` (el JDK es Temurin 25.0.4 en `C:\Program Files\Eclipse Adoptium\jdk-25.0.4.101-hotspot`).
- Hopper no está soportado en Windows; IDA y Kuna no están configurados (Kuna además no admite PE).

## Comandos y parámetros usados
- **Lo que funcionó para la FASE 2**: la CLI repite el análisis de Ghidra (unos 5 min) en **cada** comando. Solución: `scratchpad\scripts\mcp_daemon.js` arranca `rea --mcp` por stdio, llama `open_binary` (con `provider_id: "ghidra"`) una sola vez y atiende consultas en cola (`rea_q\in\*.json` → `out\*.json`). La primera tarda unos 6,5 min; las siguientes, milisegundos. `scripts\q.js` encola un lote y espera la respuesta.
- Herramientas MCP útiles: `xrefs` (dirección de una cadena → quién la usa), `resolve_containing_procedure`, `procedure_pseudo_code`, `procedure_callees`. `find_xrefs_to_name` **no** encuentra imports: hay que usar `xrefs` con la dirección de la entrada en la tabla de imports (IAT) que da `pefile` (`imp.address`).
- Copia de prueba (no se ejecutó nada): `...\scratchpad\proq4\bin\ProQ4.vst3`.
- `rea inspect-pe-resources <dll> --format json`: funcionó sin Ghidra. Resultado: 361 recursos (358 PNG/RCDATA tipo 10, 1 diálogo `WINDOWSLICENSEDIALOG`, versión, 2 manifiestos).
- Imports, exports y cadenas con offsets y VA: script Python con `pefile` 2024.8.26 (`scratchpad\scripts\pe_dump.py <dll> <prefijo>`), ejecutado con `python -I`. Da 20 486 cadenas ASCII y UTF-16.
- Registro (solo lectura, ocultando los valores de licencia): `Get-ItemProperty 'HKCU:\Software\FabFilter\Pro-Q\4.0'`.
