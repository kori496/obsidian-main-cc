---
tags: [programacion, audio, vst3, juce, cpp, plugin]
actualizado: 2026-10-25
---

Volver a [[Programacion]]

# LKV EQ: plugin VST3 propio (C++ / JUCE)

Ecualizador paramétrico propio, base para ir añadiendo herramientas. Idea sacada del inventario de [[FabFilter Pro-Q 4]], pero **hecho desde cero** con los filtros públicos de JUCE (biquads RBJ). No lleva código, gráficos, presets ni el nombre de FabFilter. Por eso no hizo falta seguir con la ingeniería inversa del procesado de audio.

## Dónde está
- Código (en OneDrive, con respaldo): `C:\Users\sharo\OneDrive\Documentos\LkvEQ`
- Herramientas (fuera de OneDrive): `C:\dev\JUCE` (JUCE 8.0.4, sin `examples`, `docs` ni `AudioPluginHost`) y `C:\dev\cmake-3.30.5-windows-x86_64` (CMake portable).
- Compilación: `C:\dev\build\LkvEQ`. Plugin: `...\LkvEQ_artefacts\Release\VST3\LKV EQ.vst3`. App suelta: `...\Release\Standalone\LKV EQ.exe`.
- Compilador: Visual Studio 2022 Community (MSVC 14.44, Windows SDK 10.0.26100). No hace falta Rust.

## Comandos que funcionaron (25 oct 2026)
```
C:\dev\cmake-3.30.5-windows-x86_64\bin\cmake.exe -S "C:\Users\sharo\OneDrive\Documentos\LkvEQ" -B C:\dev\build\LkvEQ -G "Visual Studio 17 2022" -A x64 -DJUCE_DIR=C:/dev/JUCE
C:\dev\cmake-3.30.5-windows-x86_64\bin\cmake.exe --build C:\dev\build\LkvEQ --config Release --target LkvEQTests LkvEQ_VST3 LkvEQ_Standalone -- -m:2
C:\dev\build\LkvEQ\LkvEQTests_artefacts\Release\LkvEQTests.exe   → "Todo OK" (6 comprobaciones)
```
- Configurar tarda unos 2,5 min (compila `juceaide`). La primera compilación completa tarda varios minutos.

## Qué hace la versión 0.1
- 8 bandas: Bell, Low Shelf, High Shelf, Low Cut, High Cut, Notch, Band Pass. Cada una con On, Frequency (10 Hz-30 kHz, escala log), Gain (±30 dB) y Q (0,1-30).
- Output Level (±36 dB, con rampa de 50 ms) y Bypass (también como bypass del host).
- Pantalla: curva de respuesta, rejilla ±30 dB y 20 Hz-20 kHz.
  - Arrastrar un punto cambia frecuencia y ganancia.
  - La rueda del ratón cambia la Q.
  - Doble clic en un hueco crea una banda; doble clic en un punto la apaga.
- Debajo: controles de la banda seleccionada (On, tipo, Freq, Gain, Q) y salida.
- Estado guardado dentro del proyecto del DAW. Sin archivos, registro ni red (al revés que el Pro-Q 4).

## Atajos conocidos (para mejorar)
- Cortes de 12 dB/oct solamente (un biquad). Para 24-96 dB/oct: encadenar etapas.
- Sin suavizado de coeficientes: con automatización muy rápida puede oírse un "zipper".
- Sin analizador de espectro, dinámica por banda, M/S, fase lineal, EQ Match ni presets propios.

## Siguientes herramientas posibles (de la tabla del Pro-Q 4)
Analizador de espectro (FFT) → pendientes de corte mayores → modo M/S/L/R por banda → EQ dinámico → Auto Gain → presets en archivo.

## Errores resueltos
- `error C2280` al compilar: `juce::dsp::IIR::Filter` no se puede copiar y `std::vector::assign(n, {})` lo copia. Solución: `filters = decltype (filters) (channels);`.
- Sin CMake en el PC: bastó con el zip portable de Kitware y el generador "Visual Studio 17 2022" (no hace falta Ninja).

## Disco
- Antes de empezar quedaban 1,4 GB libres en C:; después de compilar, **296 MB**. Hay que liberar espacio antes de seguir compilando.
- 26 oct: se borró `C:\dev\build\LkvEQ` (405 MB) y quedaron **701 MB libres**. Los binarios se guardaron en `C:\dev\LkvEQ-bin` (`LKV EQ.vst3`, `LKV EQ.exe`, `LkvEQTests.exe`; los tests siguen en «Todo OK»). La próxima compilación tendrá que volver a configurar y compilar JUCE entero (unos 10 min).
- Para FL Studio: añadir `C:\dev\LkvEQ-bin` a las rutas de búsqueda de plugins.

## Analizador de espectro (27 oct 2026): código escrito, SIN compilar
- `Source/Spectrum.h`: FFT de 4096 puntos con ventana Hann (`juce::dsp::FFT`), dB calibrado (seno de amplitud 1 = 0 dB).
- El procesador deja muestras mono después del EQ en un `AbstractFifo` (`pushAnalyzerSamples`/`pullAnalyzerSamples`).
- `EqCurve` dibuja el espectro relleno detrás de la curva: escala de 0 a −90 dB, inclinación de 4,5 dB/oct (así el ruido rosa se ve plano) y caída de 1,5 dB por fotograma.
- Idea tomada de la lista de funciones del Pro-Q 4 (analizador «Post», Tilt, Speed); el código es propio.
- Test nuevo en `EqTests.cpp`: un seno en el bin 85 debe medir 0 dB y el bin 400 menos de −60 dB.
- **No compiló**: el disco C: pasó de 5,6 GB libres a 0 durante la configuración (`error C1085 … No space left on device` al compilar `juceaide`). La compilación solo había usado 93 MB; el resto lo ocupó otra cosa. Se borró `C:\dev\build\LkvEQ`. El plugin instalado sigue siendo la v0.1, sin analizador.

## Instalado para FL Studio (27 oct 2026)
- Copiado a la carpeta VST3 estándar, que FL Studio 21 revisa por defecto: `C:\Program Files\Common Files\VST3\LKV EQ.vst3` (carpeta-bundle con `Contents\x86_64-win\LKV EQ.vst3` y `Contents\Resources\moduleinfo.json`).
- Hace falta administrador: `Start-Process robocopy -Verb RunAs` (aparece la ventana de UAC). Código 1 de robocopy = archivos copiados, no es error.
- En FL: Options → Manage plugins → Find installed plugins (o Find more plugins). Aparece como **LKV EQ** de **lagrimankv**, en efectos. Se carga en un slot del mixer.
- Para actualizar tras recompilar: repetir la copia (con FL cerrado o con el plugin descargado, porque Windows bloquea la DLL en uso).
