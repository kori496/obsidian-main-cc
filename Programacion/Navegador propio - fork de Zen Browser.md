---
tags: [programacion, navegador, zen, firefox]
actualizado: 2026-10-24
---

Volver a [[Programacion]]

# Navegador propio: fork de Zen Browser

## Decisión (24 oct)
- No hace falta ingeniería inversa: Zen es código abierto (MPL-2.0, `github.com/zen-browser/desktop`). Se hace un fork.
- Elegido el camino 3: fork completo y compilar (los otros eran `userChrome.css`/Zen Mods o una extensión).
- Reglas: no usar el nombre "Zen" ni su logo (marca propia); los archivos MPL modificados siguen siendo abiertos.

## Bloqueo: este PC no puede compilarlo (revisado 24 oct)
| Recurso | Hay | Hace falta (aprox.) |
|---|---|---|
| Disco libre | C: 9 GB, G: 8 GB, E: 4 GB | 40–60 GB |
| RAM | 8 GB | 16 GB o más |
| Núcleos | 4 lógicos | más, o horas de compilación |
| Visual Studio C++, Rust, MozillaBuild | no instalados | sí |

Opciones para seguir:
1. **Compilar en la nube** con GitHub Actions desde el fork (no ocupa el PC; hay que revisar si los runners gratis tienen disco suficiente).
2. **Liberar o añadir disco** (mín. ~60 GB) y usar una "artifact build" de Firefox: baja el motor ya compilado y solo construye la interfaz. Sirve porque casi todos los cambios de Zen son JS/CSS. La RAM sigue justa.
3. Volver a la opción ligera (Zen Mods / `userChrome.css`) si lo que se quiere es sobre todo diseño.

Pendiente: que elija una opción y el nombre del navegador.
