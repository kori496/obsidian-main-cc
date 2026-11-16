---
tags: [redes, instagram, publico-objetivo, v-ya]
actualizado: 2026-11-13
---

Volver a [[Redes]] · Relacionado: [[Edición de imágenes]] · [[Referencias de stories de otras tiendas]]

# Público objetivo de @v.yafashion (Instagram de V.YA)

Prueba hecha el 13 nov 2026 para ver si Claude puede deducir el **público objetivo** de una cuenta de Instagram a partir del perfil público. Se abrió el perfil en Chrome. Todo lo de abajo es **inferencia** a partir de lo que se ve, no datos reales de audiencia (edad, género y ciudades reales solo salen de las estadísticas de la propia cuenta).

## Datos del perfil (13 nov 2026)
- 1.007 posts · 14.9K seguidores · sigue a 58.
- Bio: "JEANS PARA MUJER" / "Jeans que realzan tu estilo". Mayor y al detal, punto físico Cra 17 # 33-40, envíos nacionales, Centro de Bucaramanga. TikTok: @v.yafashion. Enlace a WhatsApp.
- Destacadas: Destacada, métodos de pago, página web, créditos, escríbenos, envíos.
- Feed reciente: reels con una sola modelo en el local (pared de madera clara y planta), enterizos, conjuntos y jeans. Un post anuncia "Muy pronto, nueva tienda". Reels tipo "¿Qué tipo de jeans están en tendencia?" y "Dónde encontrar outfits".
- Un reel visto tenía 46 likes y 3 comentarios (una sola muestra, no un promedio).

## Público objetivo (inferido)
- **Principal:** mujeres de unos 18 a 40 años que buscan jeans y outfits en tendencia, de Bucaramanga y Santander, con alcance nacional por los envíos.
- **Secundario:** revendedoras y dueñas de tiendas pequeñas de otras ciudades (mayor, envíos nacionales, WhatsApp, créditos).

## Observaciones
- El perfil habla a dos públicos a la vez (clienta final y mayorista) con el mismo feed.
- La bio vende "jeans para mujer"; la línea elegante / fancy / colores neutros de las piezas (ver [[Edición de imágenes]]) no se lee en la bio, solo en el logo y en el local.
- Con 14.9K seguidores, 46 likes en un reel es poco; parte de la venta parece ir por WhatsApp. Falta confirmarlo con más publicaciones y con las estadísticas reales.

## Ideas para mejorar el alcance (propuesta de Claude, 13 nov 2026)
Basadas solo en la bio, unos 8 posts del feed y un dato de likes. Son hipótesis para probar, no algo medido.
1. **Gancho con texto en todos los reels.** Los que ya llevan pregunta en pantalla ("¿Qué tipo de jeans están en tendencia?", "Dónde encontrar outfits") tienen el formato correcto. Los de modelo posando sin texto no dan motivo para quedarse. Convertirlos en respuesta a una duda: "qué jean según tu cuerpo", "barrel: 3 formas de usarlo", "tallas reales".
2. **Contenido para guardar y enviar.** El alcance a no seguidoras sale de retención y de envíos por DM. Guías por tipo de cuerpo, por ocasión y por talla funcionan mejor que mostrar la prenda sola.
3. **Búsqueda local.** Poner "Bucaramanga" en el campo de nombre ("Jeans para mujer · Bucaramanga"), etiquetar la ubicación en cada post y escribir captions con las palabras que busca la clienta (jeans barrel, wide leg, tiro alto, Bucaramanga).
4. **Serie de la nueva tienda.** Convertir el "Muy pronto" en serie: avances de obra, cuenta regresiva, día de apertura. Las series dan motivo para seguir la cuenta.
5. **Llamado a comentar.** "Comenta BARREL y te envío precio y tallas". Sube comentarios (el reel visto tenía 3) y lleva la venta al DM/WhatsApp.
6. **Separar a la mayorista.** Destacada "Mayoristas" y un reel fijado para ellas; el resto del feed para la clienta final.
7. **Variar caras y fondo.** Misma modelo y misma pared en casi todo: el feed se ve repetido. Probador con cuerpos distintos, clientas reales y colaboraciones (post "Collab") con microinfluencers de Bucaramanga.
- Cómo medirlo: 4 semanas, mirando reproducciones de no seguidoras, envíos y guardados por reel (no likes).

## Pendiente
- Revisar la pestaña de reels para ver qué videos ya tienen más reproducciones y repetir ese formato.
- Sacar los datos reales de audiencia (edad, género, ciudades, horarios) desde las estadísticas de Instagram o Metricool y compararlos con esta inferencia. Ojo: en este vault se anotó que Metricool da datos incorrectos (ver [[Redes]]).

## Cómo se hizo (y qué no funcionó)
- Funcionó: abrir `instagram.com/<usuario>/` en Claude in Chrome, expandir la bio ("more"), bajar el feed y leer con capturas.
- No funcionó: `get_page_text` devuelve vacío en Instagram; hay que leer con capturas de pantalla / zoom.
- No funcionó: `browser_batch` falló con "input couldn't be safely checked"; se hizo acción por acción.
- Error de Claude: en el chat trató la cuenta como competencia de V.YA; es la cuenta de la propia tienda.
- Repetible con cualquier otro @ (por ejemplo competencia): dar el usuario y pedir el análisis de público objetivo.
