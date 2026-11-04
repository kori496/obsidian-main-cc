---
tags: [beats, metricas, herramientas]
actualizado: 2026-10-21
---

Volver a [[Videos beats]] · Ver [[Métricas y revisiones]]

# Alternativas a Metricool (analítica de cuentas)

**Por qué buscar:** Metricool conectado desde el 18/10 solo devolvió totales (227 vistas YouTube, TikTok sin datos), sin lista de videos ni fuentes de tráfico.

## Opciones (precios de lista al 21/10/2026, verificar antes de pagar)
| Herramienta | Plan gratis | Desde | Nota |
| --- | --- | --- | --- |
| Iconosquare | Sí (2 perfiles) | 33 €/mes | Analítica Instagram, TikTok, YouTube y Facebook confirmada; 40+ métricas de YouTube |
| Buffer | Sí (3 canales) | 6 $/canal/mes | Analítica básica |
| Publer | Sí (3 cuentas) | 5 $/mes | Analítica básica |
| Postoria | Sí | 10 $/mes | Analítica ligera |
| SocialPilot | No (14 días) | 20 $/mes | |
| Sprout / Hootsuite / Agorapulse | No | 79-99 $/mes | Caros para una cuenta |

## Gratis y nativo (complemento)
- YouTube Studio: retención, fuentes de tráfico, por video.
- TikTok Analytics y Instagram Insights (cuenta profesional).

## Pendiente
- Probar una opción y anotar qué datos devuelve (lista de videos, retención, TikTok).

## Idea: analítica propia (decisión 2026-10-21)
- Se puede vibecodear: script diario en Python que guarda números en SQLite/CSV + dashboard simple.
- **YouTube:** APIs oficiales gratis (Data + Analytics): vistas, retención, fuentes de tráfico por video. Empezar por aquí.
- **Instagram/Facebook:** Graph API gratis con cuenta profesional; el token caduca cada ~60 días.
- **TikTok:** sin API de analítica accesible para uso personal. Opción: CSV semanal de TikTok Studio soltado en una carpeta que la herramienta procesa sola (~1 h). Automatizar la descarga con navegador (2-4 h) es frágil (login, captcha); solo si molesta. Servicios de terceros de pago por consulta solo dan datos públicos (vistas, likes), no retención.
- Metricool usa las mismas APIs oficiales, pero como socio registrado tiene acceso ampliado a TikTok. Guarda copias diarias, por eso conserva historial largo: conviene empezar a guardar datos pronto.
- La ventaja de la herramienta propia: medir por estilo (vorty, make beat, visualizer) y por beat.
- **Decisión:** primero la herramienta, la web después. La web (dominio `lagrim.art`) está en [[Web lagrim.art]]. El tag "prod. lagrimankv" no cambia por ahora.
