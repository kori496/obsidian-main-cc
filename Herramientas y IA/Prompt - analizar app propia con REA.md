---
tags: [herramientas, rea, ingenieria-inversa, prompts, claude-code]
actualizado: 2026-10-25
---

Volver a [[REA - ingeniería inversa]]

# Prompt - analizar una app propia con REA (y Ghidra)

Plantilla para pedirle a Claude Code que inventaríe las opciones de una app y diga qué hace cada una en el sistema. Sin probar todavía con una app grande: anotar aquí qué funcionó y qué no.

## Cuándo usa cada motor
- Electron / JavaScript y .NET: herramientas propias de REA (sin Ghidra). Buscar por **canal IPC**, no por el texto del botón.
- Binarios nativos (C, C++, Rust, Go): Ghidra vía REA (`GHIDRA_INSTALL_DIR` = carpeta raíz del release, ver [[REA - ingeniería inversa]]).
- APK: JADX (pendiente de configurar `REA_JADX_MCP_JAR`).
- Mixta (Electron con `.node`/`.dll`): JS con REA y los módulos nativos con Ghidra.

## Prompt (copiar y rellenar lo que va entre < >)

```
Quiero entender a fondo la app <nombre> que está en <ruta completa de la carpeta o del .exe>.
Es una app mía. Tipo: <Electron/JS | .NET | nativa (exe/dll) | APK | mixta>.
Usa REA; si es nativa usa Ghidra a través de REA. Antes de empezar lee la nota
"REA - ingeniería inversa" del vault (main cc) y sigue lo que dice.

FASE 1 - Inventario (sin explicar todavía)
Lista TODAS las opciones y funciones que ofrece la app: menús, botones, ajustes,
comandos, canales IPC, endpoints, argumentos de línea de comandos, tareas al iniciar.
Dame una tabla numerada con: nº, nombre de la opción, dónde la encontraste
(archivo:línea o función/dirección), y si es «confirmado» o «probable».
Para y espera mi visto bueno antes de seguir.

FASE 2 - Qué hace cada opción y cómo afecta al sistema
Procesa la tabla en bloques de 5 a 10 opciones. Por cada una:
1. Traza qué código se ejecuta (de la interfaz hasta el efecto final).
2. Resume en una frase qué hace.
3. Efectos en el sistema: archivos que lee o escribe (con ruta), red (a qué hosts o
   URLs), registro de Windows, procesos que lanza, permisos o privilegios,
   variables de entorno, tareas programadas, inicio con Windows.
4. Cita siempre la evidencia (archivo y línea, o función/dirección en Ghidra).
5. Marca «confirmado» solo si lo viste en el código; «probable» si lo dedujiste.
   Si REA o Ghidra no pudo enlazar algo, dilo en vez de adivinar.

FASE 3 - Resumen
Configuración (dónde se guarda y qué claves tiene), dependencias, qué cosas
dependen de datos en tiempo de ejecución y no se pudieron resolver, y riesgos
de seguridad que veas en mi propia app.

GUARDADO EN EL VAULT (obligatorio, sin que te lo pida)
- Crea o actualiza una nota por app en `Herramientas y IA/Análisis de apps/<nombre de la app>.md`
  con frontmatter (`tags`, `actualizado: AAAA-MM-DD`), «Volver a [[Análisis de apps con REA]]»
  y esta estructura: resumen, tabla de opciones, detalle por opción, configuración,
  límites del análisis y qué NO funcionó.
- Enlázala desde la nota índice «Análisis de apps con REA» (créala si no existe).
- Guarda las rutas y comandos que usaste y los parámetros que funcionaron.
- Añade una entrada corta en `Bitácora.md` (fecha, qué se hizo, notas tocadas).
- No borres ni sobrescribas notas mías sin avisar; si cambias algo, di qué.

Reglas: no inventes funciones que no aparezcan en el código; no ejecutes la app
fuera de una carpeta de prueba; respuestas cortas, dime qué hiciste y dónde quedó
cada nota.
```

## Verificación recomendada
Ejecutar la app en una carpeta de prueba o máquina virtual con Process Monitor para comprobar que los efectos «confirmados» coinciden con lo que hace de verdad.

## Límites conocidos
- Se recuperan pseudocódigo y ensamblador, no el código original ni los nombres de variables.
- En binarios nativos Ghidra no sabe qué opción de la interfaz corresponde a cada función: esa parte suele quedar como «probable».
- Lo que se calcula en tiempo de ejecución (rutas armadas dinámicamente, configuración remota) no se resuelve.
