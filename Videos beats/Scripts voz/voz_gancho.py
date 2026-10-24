"""Genera el gancho de voz de los shorts: voz con IA (edge-tts) + efectos para que suene
sintetica/distorsionada, y los tiempos de cada palabra para animar el texto en Remotion.

Uso:
    python voz_gancho.py "how to sound like eyesofdirty"
    python voz_gancho.py "how to sound like eyesofdirty" --beat mi_beat.wav --beat-inicio 12.5
    python voz_gancho.py "frase" --voces en-US-GuyNeural en-US-AriaNeural en-GB-RyanNeural
    python voz_gancho.py "frase" --entrada mi_grabacion.wav      (usa tu voz, sin IA)

Necesita: ffmpeg en el PATH, numpy/scipy y (para la voz IA) `pip install edge-tts`.
Salida en voz/salida/: una pareja por voz y preset:
    <voz>_<preset>.wav       voz procesada
    <voz>_<preset>.json      palabras con inicio/duracion en segundos (para el texto animado)
    prev_<voz>_<preset>.mp3  (solo con --beat) voz + silencio corto + drop del beat
Presets: robot (metalica), glitch (recortada palabra por palabra), radio (telefono sucio).
"""
import argparse
import asyncio
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from scipy.io import wavfile

HERE = Path(__file__).resolve().parent
SALIDA = HERE / "voz" / "salida"
SR = 44100

# Cadenas de efectos de ffmpeg (el tono sube sin cambiar la velocidad: asetrate + atempo)
def pitch(semitonos):
    f = 2 ** (semitonos / 12)
    return f"asetrate={SR}*{f:.4f},aresample={SR},atempo={1 / f:.4f}"

PRESETS = {
    "robot": dict(
        chop=False,
        fx=f"{pitch(3)},highpass=f=220,volume=12dB,acrusher=bits=8:samples=2:mode=log:aa=0,"
           "asoftclip=type=tanh,treble=g=4:f=3500,alimiter=limit=0.9",
    ),
    "glitch": dict(
        chop=True,
        fx=f"{pitch(5)},highpass=f=300,volume=10dB,acrusher=bits=10:samples=1:mode=lin,"
           "asoftclip=type=hard,alimiter=limit=0.9",
    ),
    "radio": dict(
        chop=False,
        fx="highpass=f=420,lowpass=f=3200,volume=14dB,asoftclip=type=hard,"
           "acrusher=bits=6:samples=4:mode=lin,alimiter=limit=0.9",
    ),
}


def ffmpeg(*args):
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", *map(str, args)], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"ffmpeg fallo: {r.stderr.strip()}")


def a_wav_mono(src, dst):
    ffmpeg("-i", src, "-ac", "1", "-ar", SR, "-sample_fmt", "s16", dst)


def leer(path):
    sr, x = wavfile.read(path)
    x = x.astype(np.float32) / 32768
    return x if x.ndim == 1 else x.mean(axis=1)


def escribir(path, x):
    wavfile.write(path, SR, (np.clip(x, -1, 1) * 32767).astype(np.int16))


def segmentos_por_silencio(x, min_gap=0.06, min_len=0.05):
    """Devuelve [(ini, fin)] en segundos de los tramos con voz."""
    paso = int(SR * 0.01)
    n = len(x) // paso
    rms = np.array([np.sqrt(np.mean(x[i * paso:(i + 1) * paso] ** 2)) for i in range(n)])
    if rms.size == 0 or rms.max() == 0:
        return []
    activo = rms > rms.max() * 0.05
    segs, ini = [], None
    for i, a in enumerate(activo):
        if a and ini is None:
            ini = i
        if not a and ini is not None:
            segs.append([ini, i])
            ini = None
    if ini is not None:
        segs.append([ini, n])
    fus = []
    for s in segs:
        if fus and (s[0] - fus[-1][1]) * 0.01 < min_gap:
            fus[-1][1] = s[1]
        else:
            fus.append(s)
    return [(a * 0.01, b * 0.01) for a, b in fus if (b - a) * 0.01 >= min_len]


def palabras_desde_audio(x, frase):
    """Tiempos por palabra a partir del silencio; si no coinciden, reparte por numero de letras."""
    palabras = frase.split()
    segs = segmentos_por_silencio(x)
    if not segs:
        return []
    if len(segs) == len(palabras):
        return [{"texto": p, "ini": a, "dur": b - a} for p, (a, b) in zip(palabras, segs)]
    a0, b0 = segs[0][0], segs[-1][1]
    total = sum(len(p) for p in palabras)
    t, out = a0, []
    for p in palabras:
        d = (b0 - a0) * len(p) / total
        out.append({"texto": p, "ini": t, "dur": d})
        t += d
    return out


def recortar(x, palabras, hueco=0.07):
    """Corta cada palabra y las separa con un hueco: efecto 'recortado'. Reajusta los tiempos."""
    piezas, nuevas, t = [], [], 0.0
    for w in palabras:
        a = int(max(0, w["ini"] - 0.01) * SR)
        b = int(min(len(x) / SR, w["ini"] + w["dur"] + 0.02) * SR)
        p = x[a:b].copy()
        f = min(len(p) // 4, int(0.005 * SR))
        if f > 0:
            p[:f] *= np.linspace(0, 1, f)
            p[-f:] *= np.linspace(1, 0, f)
        nuevas.append({"texto": w["texto"], "ini": round(t, 3), "dur": round(len(p) / SR, 3)})
        piezas += [p, np.zeros(int(hueco * SR), dtype=np.float32)]
        t += len(p) / SR + hueco
    return np.concatenate(piezas), nuevas


async def tts(frase, voz, mp3):
    import edge_tts
    try:
        com = edge_tts.Communicate(frase, voz, boundary="WordBoundary")
    except TypeError:  # version antigua de edge-tts: ya emite palabras por defecto
        com = edge_tts.Communicate(frase, voz)
    audio, palabras = bytearray(), []
    async for ch in com.stream():
        if ch["type"] == "audio":
            audio += ch["data"]
        elif ch["type"] == "WordBoundary":
            palabras.append({"texto": ch["text"], "ini": ch["offset"] / 1e7, "dur": ch["duration"] / 1e7})
    Path(mp3).write_bytes(bytes(audio))
    return palabras


def procesar(x, palabras, preset, tmp):
    cfg = PRESETS[preset]
    if cfg["chop"]:
        x, palabras = recortar(x, palabras)
    crudo, fx = Path(tmp) / "crudo.wav", Path(tmp) / "fx.wav"
    escribir(crudo, x)
    ffmpeg("-i", crudo, "-af", cfg["fx"], "-ar", SR, "-ac", 1, fx)
    y = leer(fx)
    pico = np.abs(y).max() or 1
    return y / pico * 0.9, [{"texto": w["texto"], "ini": round(w["ini"], 3), "dur": round(w["dur"], 3)} for w in palabras]


def vista_previa(voz, palabras, beat_wav, beat_inicio, pausa, dst, tmp):
    """Voz + una pausa corta + el beat desde `beat_inicio` (el drop), con los graves completos."""
    fin_voz = max(w["ini"] + w["dur"] for w in palabras)
    b = Path(tmp) / "beat.wav"
    ffmpeg("-ss", beat_inicio, "-i", beat_wav, "-t", 6, "-ac", 2, "-ar", SR, "-sample_fmt", "s16", b)
    sr, bt = wavfile.read(b)
    bt = bt.astype(np.float32) / 32768
    inicio = int((fin_voz + pausa) * SR)
    total = inicio + len(bt)
    mezcla = np.zeros((total, 2), dtype=np.float32)
    v = np.pad(voz, (0, max(0, total - len(voz))))[:total]
    mezcla[:, 0] += v * 0.8
    mezcla[:, 1] += v * 0.8
    mezcla[inicio:] += bt * 0.85
    wav = Path(tmp) / "mezcla.wav"
    wavfile.write(wav, SR, (np.clip(mezcla, -1, 1) * 32767).astype(np.int16))
    ffmpeg("-i", wav, "-b:a", "192k", dst)


def main():
    ap = argparse.ArgumentParser(description="Gancho de voz para shorts")
    ap.add_argument("frase")
    ap.add_argument("--voces", nargs="+", default=["en-US-GuyNeural", "en-US-AriaNeural"])
    ap.add_argument("--presets", nargs="+", default=list(PRESETS), choices=list(PRESETS))
    ap.add_argument("--entrada", help="usar este wav/mp3 en vez de generar voz con IA")
    ap.add_argument("--beat", help="wav/mp3 del beat para la vista previa")
    ap.add_argument("--beat-inicio", type=float, default=0.0, help="segundo del beat donde esta el drop")
    ap.add_argument("--pausa", type=float, default=0.15, help="silencio entre la voz y el drop (s)")
    a = ap.parse_args()
    SALIDA.mkdir(parents=True, exist_ok=True)

    fuentes = [("propia", a.entrada)] if a.entrada else [(v, None) for v in a.voces]
    with tempfile.TemporaryDirectory() as tmp:
        for nombre, entrada in fuentes:
            wav = Path(tmp) / f"{nombre}.wav"
            palabras = []
            if entrada:
                a_wav_mono(entrada, wav)
            else:
                mp3 = Path(tmp) / f"{nombre}.mp3"
                palabras = asyncio.run(tts(a.frase, nombre, mp3))
                a_wav_mono(mp3, wav)
            x = leer(wav)
            if len(palabras) < len(a.frase.split()):  # sin tiempos fiables: sacarlos del audio
                palabras = palabras_desde_audio(x, a.frase)
            if not palabras:
                print(f"{nombre}: no se detecto voz, se omite")
                continue
            for preset in a.presets:
                y, pal = procesar(x, palabras, preset, tmp)
                base = SALIDA / f"{nombre}_{preset}"
                escribir(base.with_suffix(".wav"), y)
                base.with_suffix(".json").write_text(
                    json.dumps({"frase": a.frase, "voz": nombre, "preset": preset, "palabras": pal,
                                "duracion": round(len(y) / SR, 3)}, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"{base.name}.wav  ({len(y) / SR:.1f} s)")
                if a.beat:
                    vista_previa(y, pal, a.beat, a.beat_inicio, a.pausa, SALIDA / f"prev_{nombre}_{preset}.mp3", tmp)
    print(f"Listo. Escucha los archivos de {SALIDA}")


if __name__ == "__main__":
    main()
