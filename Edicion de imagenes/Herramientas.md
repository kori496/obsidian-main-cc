---
tags: [vya, edicion, herramientas]
---

# 🧰 Herramientas

Volver a [[Edición de imágenes]] · Skills de Claude: [[Skills]]

| Herramienta | Para qué | Estado |
| --- | --- | --- |
| Pillow / OpenCV / ImageMagick | Luz, contraste, balance de blancos, recortes 9:16, filtro de marca uniforme | ✅ Disponibles en el espacio de Claude |
| rembg | Quitar fondos | ⚠️ Bloqueado en el espacio de Claude; se puede instalar en el PC |
| Real-ESRGAN | Subir resolución y nitidez | ⚠️ Bloqueado en el espacio de Claude; versión portable para el PC |
| Adobe (conector) | Fondos, luz, color, lotes | ⏳ Conexión empezada sin terminar |
| Canva (conector) | Piezas con plantillas de marca | Opcional |

## Instalar en el PC
- `pip install "rembg[cpu,cli]"` → `rembg p carpeta_fotos carpeta_resultado`
- Real-ESRGAN: zip `realesrgan-ncnn-vulkan` desde GitHub Releases → `realesrgan-ncnn-vulkan -i foto.jpg -o foto_hd.png -n realesrgan-x4plus`

Ver también [[Pendientes]]
