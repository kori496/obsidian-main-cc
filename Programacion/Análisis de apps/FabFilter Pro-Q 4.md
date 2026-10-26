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
- Estado: **FASE 1 hecha** (inventario). Fases 2 y 3 pendientes del visto bueno y de tener Ghidra funcionando en REA (ver «Qué NO funcionó»).

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
| 9 | Refresh / Revert / Load Factory Settings / Restore Factory Presets | 0x180238718, 0x180238734, 0x180238740, 0x1802382b0 | confirmado |
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
| 54 | Lee `ProgramFilesDir` de `HKLM\Software\Microsoft\Windows\CurrentVersion` (para encontrar la ayuda) | 0x18023d028, 0x18022d050 | probable |
| 55 | Log de depuración `FabFilter.log` («*** Begin debug session ***») | 0x18022cd88, 0x18022cd98 | probable (no se sabe si se activa en esta build) |
| 56 | Aceleración gráfica OpenGL / escalado HiDPI | registro `GraphicsAcceleration`, `RetinaEnabled` (0x18023a638, 0x18023a650); imports OPENGL32 | confirmado |
| 57 | Ajuste oculto `VST2_DefaultToNoSideChain` | 0x18023a660 | probable |
| 58 | Consulta `Software\Classes\CLSID\` | 0x18023ceb0 | probable (propósito desconocido) |
| 59 | Arrastrar y soltar archivos en la ventana | imports `DragAcceptFiles`/`DragQueryFileW` | probable (qué archivos acepta) |
| 60 | Valores guardados que no tienen botón visible en esta tabla: `showWelcomeHint`, `PresetBrowserTypeToSearch`, `ShowOutputLevelMeter`, `InterfaceLayout` | registro `HKCU\...\Pro-Q\4.0`; 0x180239d98, 0x180239dc0, 0x18023a6a8 | confirmado |

**No encontrado** (búsqueda acotada a cadenas e imports): argumentos de línea de comandos (es una DLL que carga el host), claves `Run` o inicio con Windows, tareas programadas, lanzamiento de procesos aparte de `ShellExecuteW` (abrir URL o ayuda), endpoints distintos de `www.fabfilter.com`.

## Detalle por opción
Pendiente (FASE 2), en bloques de 5 a 10 opciones, cuando REA pueda abrir el binario con Ghidra.

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
- Copia de prueba (no se ejecutó nada): `...\scratchpad\proq4\bin\ProQ4.vst3`.
- `rea inspect-pe-resources <dll> --format json`: funcionó sin Ghidra. Resultado: 361 recursos (358 PNG/RCDATA tipo 10, 1 diálogo `WINDOWSLICENSEDIALOG`, versión, 2 manifiestos).
- Imports, exports y cadenas con offsets y VA: script Python con `pefile` 2024.8.26 (`scratchpad\scripts\pe_dump.py <dll> <prefijo>`), ejecutado con `python -I`. Da 20 486 cadenas ASCII y UTF-16.
- Registro (solo lectura, ocultando los valores de licencia): `Get-ItemProperty 'HKCU:\Software\FabFilter\Pro-Q\4.0'`.
