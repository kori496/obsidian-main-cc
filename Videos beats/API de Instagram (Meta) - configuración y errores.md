---
tags: [beats, metricas, herramienta, web, instagram]
actualizado: 2026-10-24
---

Volver a [[Panel web lagrim-stats]] · Skills en [[Skills]]

# API de Instagram (Meta) - configuración y errores

Cómo se conectó la cuenta de Instagram (producer lagrimankv) a lagrim-stats y qué falló.

## Lo que funcionó
- Usar **Instagram API con inicio de sesión de Instagram** (`graph.instagram.com`, v26.0). La vía con inicio de sesión de Facebook pide una Página de Facebook (`me/accounts` salía vacío) y no hay Página.
- Permisos de la app: `instagram_business_basic` e `instagram_business_manage_insights`, listos para pruebas en modo desarrollo.
- Tu cuenta añadida con el rol **Evaluador de Instagram** y aceptada.
- Token corto sacado con "Generar identificador" de la app. Con él se leen los insights.
- ID de usuario de Instagram: 17841423737094601.

## Lo que falló
- Canjear el token corto por uno largo (`ig_exchange_token`) da **error 452**. Sin resolver. Opciones: soporte o comunidad de Meta, usar Metricool, o renovar el token corto a mano.
- Pegar la URL de `graph.instagram.com` en el Graph API Explorer da "Cannot parse access token". Hay que pegarla en la barra de direcciones del navegador.
- Al añadir permisos en Meta a veces sale error; reintentar funciona.
- Metricool tiene métricas de Instagram, pero los datos seguían en cero. Revisar otra vez.

## Cómo se usa
- `meta_config.json` (junto a `importar_instagram.py`): `access_token`, `user_id`, `token_largo`, `token_actualizado`. Modelo: `meta_config.ejemplo.json`.
- Las métricas diarias traen la hora 07:00 UTC y cuentan el día anterior; el script lo corrige.
- Token caducado (errores 190/452/463/467): el script crea `NECESITA_TOKEN_META.txt` y el panel lo avisa.

## Error resuelto (24 oct 2026): meta_config.json en texto suelto
- **Síntoma:** Instagram no traía datos de la API y el panel no avisaba nada. El log decía «meta_config.json no se pudo leer».
- **Causa:** el token se pegó como texto («identificador lagrimankv2 IGAA…» / «id profile …») en vez de JSON.
- **Arreglo:** el archivo quedó en el formato de `meta_config.ejemplo.json` (`access_token`, `user_id` 17841423737094601, `token_largo: true`). Copia del original en `analitica/meta_config.antes-de-arreglar.txt` (tiene el token: está en `.gitignore`; bórrala cuando quieras).
- **Resultado:** conecta como @lagrimankv; el token se renovó solo (con `token_largo: true` se renueva cada 7 días y no caduca a los 60). Trae alcance de 30 días, vistas/interacciones de 7 días y 5 publicaciones. Meta da **0 seguidores**.
- **Mejora:** si el archivo vuelve a estar mal escrito, `importar_instagram.py` crea `NECESITA_TOKEN_META.txt` y la pestaña Instagram muestra el motivo exacto (el aviso ya no dice siempre «token caducado»).
