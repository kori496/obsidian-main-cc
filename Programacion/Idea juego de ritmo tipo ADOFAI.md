---
tags: [programacion, juego, idea, beats, ritmo]
actualizado: 2026-10-27
---

Volver a [[Programacion]] · Mapa general: [[Inicio]]

# Idea: juego de ritmo tipo ADOFAI para celular

Idea en fase de exploración (27 oct 2026). Juego de ritmo para celular estilo *A Dance of Fire and Ice*, con el modelo de contenido de *Geometry Dash*: sets oficiales con mis beats y mapas de la comunidad.

## Cómo llegamos aquí (ideas descartadas o en pausa)
- **Factorio/Satisfactory para celular**: versión completa = proyecto de más de 1 año (simular miles de objetos, controles táctiles, balance). Versión idle de fábricas = 2-4 meses. Nicho con competencia (Builderment, Mindustry, shapez).
- **Otros nichos**: hypercasual y match-3 dominados por estudios grandes. Para indie funcionan mejor idle temático, survivor tipo Vampire Survivors, hybrid-casual y cozy.
- **Ritmo tipo Piano Tiles / osu!**: el problema del género son las licencias de música. Yo hago la música, así que me lo salto. Esto inclinó la decisión hacia ritmo.

## Concepto
- Mecánica ADOFAI: dos planetas en órbita, un solo toque al llegar a cada casilla. Ideal para pantalla táctil.
- **Diferenciador**: boom bap y beats urbanos (ADOFAI usa sobre todo electrónica). El swing del boom bap da caminos distintos. Estética propia ligada a la de mis videos de beats. Cada nivel lleva **prod. lagrimankv**.
- Ya existe ADOFAI oficial en Android/iOS (de pago): prueba de que la mecánica funciona en móvil, pero no hay que hacer un clon.

## Truco clave: niveles desde el MIDI
- En ADOFAI el ángulo entre casillas = tiempo entre notas (180° = 1 tiempo, 90° = medio tiempo).
- Leer el MIDI del beat (bombo, caja, melodía) → tiempo entre notas → ángulos → el camino se arma solo. Después solo se pulen a mano las partes difíciles.
- Cada beat nuevo = un nivel casi gratis.

## Modelo de contenido (estilo Geometry Dash)
1. **Sets oficiales** con mis beats, generados desde el MIDI y pulidos. Organizados por packs (boom bap, trap, experimental).
2. **Biblioteca propia de música tipo Newgrounds**: productores suben beats y aceptan su uso en el juego. Ellos ganan exposición, la comunidad tiene música legal y el juego se vuelve un punto de encuentro de productores.
3. **Mapas de la comunidad**: editor donde se elige un beat de la biblioteca y se arma el nivel. Publicar, likes, dificultad, destacados.
4. **Opcional, importar tu canción**: solo para jugar en el propio teléfono, **sin compartir** (compartir niveles con audio ajeno = alojar música con derechos = reclamos). Si algún día se comparten, solo el nivel sin audio (como GD) y comprobar que el otro tenga la misma canción y ajustar el desfase.
   - Sin MIDI hay que detectar beats/onsets del audio (menos preciso). Alternativas: generador automático + ajuste manual, o editor de "toca al ritmo".

## Lo difícil
- **Sincronización de audio**: crítica. Android tiene latencia variable (Bluetooth peor). Calibración de latencia obligatoria.
- **Diseño de niveles legibles** y una curva de dificultad que suba bien.
- **Efectos visuales** que reaccionan a la música (lo que más tiempo toma; sirve lo aprendido con visualizers en [[Pipeline visualizer Remotion]]).
- **Editor y servidores** (cuentas, subida, moderación): es la parte más grande del proyecto.
- La comunidad no aparece sola: el juego tiene que ser divertido sin ella.

## Cobro
- Como Geometry Dash: versión gratis con algunos niveles + versión completa de pago único (niveles y editor). Más paquetes de canciones.
- El público de ADOFAI paga; los anuncios suelen caer mal.

## Herramienta
- **Godot** (gratis, liviano, exporta a Android/iOS; GDScript se parece a Python, ver aprendizaje de Python).

## Plan por fases (cada fase es publicable)
1. Juego base con 5-10 niveles míos, sin internet. Prototipo primero: **1 beat convertido desde MIDI** para probar si se siente bien.
2. Editor local (crear y jugar en el propio teléfono).
3. Compartir niveles en línea.
4. Biblioteca abierta a otros productores.

## Promoción
- Devlog en TikTok/Shorts desde el día uno. Clips de niveles difíciles = promo del juego + de la canción.
- Relacionado con el canal: [[Videos beats]] · [[Multimedia]].

## Estado
- Solo idea. Nada programado todavía. Siguiente paso posible: prototipo en Godot con un beat.
