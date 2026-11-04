---
tags: [programacion, alta, instalacion]
actualizado: 2026-10-28
---

Volver a [[ALTA - Inicio]] · mapa: [[ALTA - mapa completo.canvas|Mapa de ALTA]] · registro en [[Bitácora]]

# Instalación y arranque

## Instalar en un PC
1. Descomprimir el `.zip` en una carpeta fija (no usarlo desde dentro del .zip).
2. Doble clic en `instalar.bat` → corre `instalar.ps1`: quita el bloqueo de Windows a los archivos del .zip y crea el acceso directo **Alta de productos** en el escritorio y en el menú Inicio.
3. Si sale «Windows protegió su PC»: *Más información → Ejecutar de todas formas*.
- Trae su propio Node.js (`node\node.exe`): no hay que instalar nada. Funciona sin internet (Windows 10/11).

## Arrancar
1. El acceso directo ejecuta `wscript.exe iniciar.vbs` (sin ventana negra; también sirve `iniciar.bat`).
2. `iniciar.vbs` revisa que exista `node\node.exe` y lanza `node.exe app\server.js`.
3. **¿Ya estaba abierto?** El servidor prueba `/api/ping` en los puertos **3789 a 3798**:
   - si responde Alta con el **mismo código** → solo abre el navegador;
   - si responde Alta con **código viejo** (cambió `server.js` o `crs.ps1`) → cierra la versión vieja y arranca la nueva;
   - si el puerto lo usa otro programa → prueba el siguiente.
4. Al arrancar: crea las carpetas que falten (`datos`, `copias`, `etiquetas`, `exportados`, `plantillas`, `configuracion`), hace una **copia de la base «al-abrir»**, anota en `datos\registro.log` y abre `http://127.0.0.1:3789/`.

## Cerrar
- Botón **Cerrar el programa** (Configuración → Base de datos y copias).
- O solo: si **no queda ninguna pestaña abierta durante 10 minutos**, se cierra (las pestañas mandan un **latido** cada 30 s). Al cerrar se borra el historial de impresión de la sesión; el log en disco queda.

## Después de una actualización
Cerrar Alta y volverlo a abrir (o abrir el acceso directo: detecta el código nuevo y reinicia solo). En el navegador, F5.
