---
tags: [herramientas, rea, ingenieria-inversa, claude-code]
actualizado: 2026-10-25
---

Volver a [[Skills]]

# REA (rea-agents) - ingeniería inversa

Paquete npm `rea-agents` (repo morluto/rea, probado con la versión 6.7.0). CLI y servidor MCP para analizar apps (JavaScript/Electron, binarios, APK...).

## Instalación (24 oct 2026)
- **Instalado el 24 oct 2026** con `setup --client claude_code --yes`. `rea doctor`: registro de Claude Code y skill (v42, 207 herramientas) «aligned»; `claude mcp get rea` → Connected. Para quitarlo: `npx -y rea-agents@6.7.0 uninstall` o `claude mcp remove rea -s user`.
- Plan revisado antes con `npx -y rea-agents@6.7.0 setup --client claude_code --dry-run`: 2 acciones.
  1. Registrar el MCP en `C:\Users\sharo\.claude.json` (copia en `.claude.json.rea.backup`), comando `npx -y rea-agents@6.7.0 mcp`.
  2. Skill en `C:\Users\sharo\.claude\skills\reverse-engineer-anything`.
- Para aplicarlo: el mismo comando con `--yes` en vez de `--dry-run`, luego `rea doctor` y reiniciar Claude Code.
- El nombre del cliente es `claude_code` (con guion bajo); `claude-code` da error.
- Sin `setup` también funciona llamándolo con `npx -y rea-agents@6.7.0 <comando>`.

## Cómo trazar un botón de una app Electron (lo que funcionó)
1. `rea analyze-javascript-application <carpeta> --format json --full-output > app.json`
2. Archivo JSON `{"application": <app.json .data>, "seed": {"kind": "channel", "value": "<canal IPC>"}}` y `rea trace-application-feature <archivo>`.
- `rea trace <carpeta>` no acepta carpetas (solo archivos o apps de macOS).
- Buscar el texto del botón (`kind: string`) no encuentra nada: el HTML solo se inventaría, no se analiza. Hay que buscar por el **canal IPC**.
- En PowerShell el JSON inline se rompe; pasarlo como archivo.
- REA no enlazó el `click` de `renderer.js` ni la llamada `writeFileSync`; eso se confirma leyendo el código.

## Ejemplo probado: notes-example
Carpeta `metricool\rea-work\rea-work\example\notes-example\notes-example`.
- Botón `#export` (index.html:15) → `renderer.js:1-3` → `window.notes.exportCsv()` (preload.js:3-5) → `ipcRenderer.invoke("notes:export")` → `ipcMain.handle` (main.js:8-12).
- Escribe `notes.csv` en la carpeta de Descargas (`app.getPath("downloads")`, main.js:9) con `writeFileSync` en UTF-8, y lo sobrescribe sin preguntar.
- Columnas `id,title` (csv.js:5-6); el título va entre comillas con `"` duplicadas.

## Skill de Claude Code
- Skill `analyze-apps-with-rea` en `C:\Users\sharo\.claude\skills\analyze-apps-with-rea\` (24 oct 2026): flujo de arriba + `scripts/trace_input.py` (arma el JSON de entrada del rastreo). Probado con notes-example. Ver [[Skills]].

## Ghidra y `rea doctor` (25 oct 2026)
- Intento de instalar REA en el entorno en la nube: **bloqueado** (403 de la política de seguridad al pedir `rea-agents` a npm). Solo funciona en el PC.
- `rea doctor` tras instalar Ghidra: `claude_code` y skill (v42, 207 herramientas) «aligned», pero `ghidra` salía `missing_analysis_engine` con `GHIDRA_INSTALL_DIR is not set`. Instalar Ghidra no basta: hay que apuntar la variable a la carpeta extraída (la que tiene `ghidraRun.bat`), versión **12.1.x**: `setx GHIDRA_INSTALL_DIR "C:\ruta\ghidra_12.1_PUBLIC"`, luego reabrir PowerShell y reiniciar Claude Code. Variable agregada por el usuario el 25 oct; falta volver a pasar `rea doctor` para confirmar.
- Comprobar JDK (lo pide Ghidra reciente, JDK 21+): `java -version`, `javac -version`, `where.exe java`. Instalar: `winget install EclipseAdoptium.Temurin.21.JDK`.
- Ignorables si solo se usa Claude Code + Ghidra: Hopper, IDA, JADX (solo APK; pide el JAR `jadx-headless-mcp` 0.7.1), Kuna, y los registros de Codex, Gemini CLI, Copilot CLI, VS Code y Antigravity (`missing`; se arreglan con `rea setup`).
- Claude Desktop sale `invalid`: su paquete MSIX (`AnthropicPBC.Claude_fnn82j28hfe8t`) no es la identidad que REA reconoce. No afecta a Claude Code.
- `installations: multiple` (`rea` y `rea.cmd` en `AppData\Roaming\npm`) es normal en Windows.

## Problemas al conectar y Ghidra (25 oct 2026, noche)
- `claude mcp list` dio `rea: ✘ Failed to connect - connection timed out after 30000ms` con el comando `cmd.exe /d /c npx -y rea-agents@6.7.0 mcp`: npx tarda más de 30 s en arrancar. Se solucionó (conectó después) con las pruebas sugeridas: calentar la caché con `npx -y rea-agents@6.7.0 --version`, subir `MCP_TIMEOUT` (`setx MCP_TIMEOUT 120000`) o usar la CLI global en el registro (`claude mcp add rea -s user -- cmd /c rea mcp`). No quedó anotado cuál de las tres fue la que funcionó.
- La carpeta `Documentos\rust prueba\ghidra` NO sirve para `GHIDRA_INSTALL_DIR`: es el código fuente (clon de GitHub, versión 12.3 DEV, pide JDK 25 y Gradle para compilar), sin `ghidraRun.bat`. Hace falta el release 12.1.x ya compilado desde la página de releases de NationalSecurityAgency/ghidra.
- Verificar que Claude Code lee REA: `claude mcp list` / `claude mcp get rea`, `/mcp` dentro de Claude Code (≈207 herramientas) y `/skills`. Tras cambiar variables de entorno hay que abrir Claude Code desde una terminal nueva.

## Resuelto: Ghidra verde en `rea doctor` (25 oct 2026)
- Ghidra instalado en `C:\tools\ghidra_12.2_PUBLIC_20261016\ghidra_12.2_PUBLIC` (release 12.2, no 12.1.x; REA lo aceptó).
- Error que salió: `GHIDRA_INSTALL_DIR` terminaba en `\ghidraRun` (el archivo lanzador). REA buscaba `...\ghidraRun\Ghidra\application.properties` y marcaba `ghidra-installation` y `ghidra-java` como `config_drift`. La variable debe apuntar a la **carpeta raíz** que contiene `ghidraRun.bat`, `support` y `Ghidra`. Corregido con `setx` sin `\ghidraRun`; el usuario confirmó que ya funciona.

## Corrección: Ghidra 12.2 NO sirve para abrir binarios (25 oct 2026, Pro-Q 4)
- `rea doctor` sale verde con 12.2, pero `rea inspect <dll> --provider ghidra` falla con `provider_unavailable` → `unsupported_version`: REA 6.7.0 solo acepta **Ghidra 12.1.x** (verificado 12.1.4). Hay que bajar el release 12.1.4 y apuntar `GHIDRA_INSTALL_DIR` a su carpeta raíz.
- Segundo fallo en la misma comprobación: `java.exe: Owned Windows process requires an absolute executable path`. Solución probable: `setx JAVA_HOME "C:\Program Files\Eclipse Adoptium\jdk-25.0.4.101-hotspot"` (o un JDK 21 si Ghidra 12.1 lo pide) y reiniciar Claude Code.
- Prueba del 25 oct (noche): las variables de usuario apuntaban a rutas que **no existen**: `GHIDRA_INSTALL_DIR=C:	ools\ghidra_12.1.4_PUBLIC` (no hay carpeta; en `C:	ools` solo está la 12.2) y `JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-21...` (con «...» literal; solo existe `jdk-25.0.4.101-hotspot`). Con `JAVA_HOME` apuntando al JDK 25 real, la comprobación de Java **pasa**; lo único que falla con la 12.2 es la versión. Falta descargar y extraer de verdad Ghidra 12.1.4.
- Sin Ghidra sí funcionan `rea inspect-pe-resources` y, por fuera de REA, `pefile` para imports, exports y cadenas. Ver [[FabFilter Pro-Q 4]].

## Prompt para analizar apps propias
- Plantilla en tres fases (inventario, efectos en el sistema, resumen) que guarda todo en el vault: [[Prompt - analizar app propia con REA]].
