# ATKHUB

Hub propio, en Python, para configurar mis periféricos sin el software oficial:

| Periférico | ID USB | Qué hace ATKHUB |
| --- | --- | --- |
| Teclado Ajazz AK820 Max (mecánico) | `1A2C:A036` cable, `1A2C:8FFF` dongle | batería, efectos de luz, suspensión |
| Mouse Attack Shark X11 | `1D57:FA60` dongle, `1D57:FA55` cable | leer todo; cambiar polling, DPI por etapa, luz, suspensión, botones y macros |

## Instalar (una vez)

```
pip install hidapi pywebview
```

## Interfaz gráfica

Doble clic en **`ATKHUB GUI.bat`** (o `atkhub gui`). Ventana estilo SteelSeries con:
- **Mouse:** Rendimiento (diales de DPI por etapa, polling), Iluminación (efectos, selector de color con historial, brillo, velocidad, vista previa), Botones (dibujo del mouse B1-B8, lista de acciones, atajos de teclado capturados, editor y grabadora de macros), Energía (suspensión, batería).
- **Teclado:** Iluminación (16 efectos con vista previa animada del teclado, paleta, brillo, velocidad, dirección) y Energía.
- Barra inferior: **Vista previa en vivo** (aplica al instante), **Revertir** (vuelve a lo último guardado) y **Guardar** (Ctrl+S).

Opciones: `atkhub gui --simular` (sin tocar los periféricos), `atkhub gui --navegador` (en el navegador en vez de ventana).
Sin `pywebview`, o si la ventana nativa falla, se abre sola en el navegador.
El estado del teclado (que no se puede leer del dispositivo) y el historial de colores se guardan en `%APPDATA%\ATKHUB\estado.json`.

## Usar

Abrir una terminal en esta carpeta (`ATKHUB`) y escribir `atkhub` (o `python -m atkhub`):

```
atkhub detectar                       # qué periféricos ve
atkhub teclado estado                 # batería (solo lectura)
atkhub teclado efectos                # lista de efectos y colores
atkhub teclado luz respiracion --color azul --brillo 4
atkhub teclado luz espectro --velocidad 2
atkhub teclado suspension 15          # 5, 15, 30 o nunca
atkhub mouse info                     # polling, DPI, luz, suspensión y batería (solo lectura)
atkhub mouse polling 1000             # 125, 250, 500 o 1000
atkhub mouse dpi 2 1600               # etapa 2 = 1600 DPI
atkhub mouse modos                    # modos de luz y colores
atkhub mouse luz respiracion --color rosa --brillo 6 --velocidad 3
atkhub mouse luz fijo --color C8B49A  # color en hex, SIN # (en PowerShell # es comentario)
atkhub mouse luz apagado
atkhub mouse suspension --normal 5 --profunda 30   # minutos
atkhub mouse acciones                 # botones y acciones disponibles
atkhub mouse botones                  # qué hace cada botón ahora
atkhub mouse boton adelante tecla:ctrl+c
atkhub mouse boton atras play-pausa
atkhub mouse boton dpi volumen-mas
atkhub mouse botones --restaurar      # todos los botones de fábrica
atkhub mouse macro 1 "ctrl+c 100ms ctrl+v" --boton atras
```

Macros (`mouse macro N "secuencia"`), palabras separadas por espacios:
- `a` pulsa y suelta · `ctrl+c` combinación · `+shift` / `-shift` solo pulsar / soltar
- `clic-izq`, `clic-der`, `clic-medio`, `clic-atras`, `clic-adelante`
- `200ms` cambia la espera del paso anterior (por defecto 30 ms, o `--espera`)
- `--modo veces --veces 3`, `--modo mientras` (mientras se mantiene), `--modo hasta-tecla`
- Caben unos 50 pasos (100 bytes).

```
```

Opciones (van al final del comando):
- `--simular`: no toca nada; muestra los bytes que se enviarían.
- `--debug`: muestra los bytes enviados y recibidos.
- `atkhub detectar --todo`: lista todos los dispositivos HID con interfaces y usage pages.

Con el mouse por el dongle, moverlo justo antes de cada comando (si está dormido no responde).
La luz de la base de carga no se controla desde el PC: no está en el protocolo.

## Antes de probar
1. Cerrar el software oficial de Ajazz y de Attack Shark.
2. Empezar por los comandos de solo lectura: `detectar`, `teclado estado`, `mouse info`.
3. Si algo falla, correrlo con `--debug` y guardar lo que sale.

## Seguridad
- El mouse solo acepta escrituras a reportes conocidos (`REPORTES_PERMITIDOS` en `mouse_attackshark.py`).
  El reporte `0x10` está bloqueado: escribirlo manda el X11 al bootloader y lo deja trabado.
- `mouse dpi`, `mouse luz` y `mouse suspension` primero leen la configuración actual, verifica el checksum y cambian solo lo pedido.
- El firmware guarda los botones en otro orden del que se escriben; ATKHUB usa la tabla del
  driver de referencia (`mouse_botones.py`) y nunca escribe la tecla de modo `0x3C`.
- Cambiar el clic izquierdo pide `--forzar`. Si algo queda mal: `atkhub mouse botones --restaurar`.
- No hay comandos de firmware.

## Pruebas (sin hardware)

```
python -m unittest
```

## Créditos
Los protocolos salen de dos proyectos con licencia MIT:
- Teclado: [ak820ctl / openajazz](https://github.com/shrey715/ak820ctl) (shrey715).
- Mouse: [attack-shark-x11-driver](https://github.com/HarukaYamamoto0/attack-shark-x11-driver) (HarukaYamamoto0).

## Archivos
- `atkhub/teclado_ajazz.py`: protocolo del teclado (`AA 55 CC 33` + comando, 64 bytes).
- `atkhub/mouse_attackshark.py`: protocolo del mouse (reportes feature, permiso `0xA0` para leer).
- `atkhub/mouse_botones.py`: botones y macros del mouse.
- `atkhub/dpi_tabla.py`: tabla de DPI del sensor PAW3311.
- `atkhub/cli.py`: los comandos.
- `atkhub/gui/`: interfaz gráfica. `api.py` (puente con los periféricos, en hilos), `servidor.py` (servidor local con token), `app.py` (ventana), `web/` (HTML, CSS y JS).
- `tests/`: pruebas de los paquetes.
