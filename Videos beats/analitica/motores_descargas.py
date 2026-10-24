"""
lagrim-stats · descargador de redes.

Lo llama web/descargas_api.php:
    python motores_descargas.py listar
    python motores_descargas.py descargar <motor|auto> <url>

Por stdout imprime SOLO JSON. Todo lo demás (salida de cada herramienta) se guarda en
descargas/ultimo_log.txt para poder revisar errores.

Instalar las herramientas (una vez):
    pip install yt-dlp gallery-dl instaloader you-get streamlink

Opcional:
    cookies.txt (junto a este archivo)  -> sesión del navegador para contenido con login
    LAGRIM_IG_USUARIO                   -> usuario de Instagram para Instaloader
                                           (primero: instaloader --login TU_USUARIO)
"""
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

RAIZ = Path(__file__).resolve().parent
DESTINO = RAIZ / 'descargas'
COOKIES = RAIZ / 'cookies.txt'
INSTAGRAM_USUARIO = os.environ.get('LAGRIM_IG_USUARIO', '')

DESTINO.mkdir(exist_ok=True)


def cookies_args(flag):
    return [flag, str(COOKIES)] if COOKIES.is_file() else []


# ---------- argumentos de cada herramienta ----------

def args_yt_dlp(url):
    return ['--no-playlist', '--js-runtimes', 'node',
            '-P', str(DESTINO), '-o', '%(title)s.%(ext)s',
            *cookies_args('--cookies'), '--', url]


def args_gallery_dl(url):
    return ['-d', str(DESTINO), *cookies_args('--cookies'), url]


def args_instaloader(url):
    base = ['--no-metadata-json', '--no-captions',
            '--dirname-pattern', str(DESTINO / 'instagram' / '{target}')]
    if INSTAGRAM_USUARIO:
        base += ['--login', INSTAGRAM_USUARIO]
    m = re.search(r'instagram\.com/stories/([^/?#]+)', url, re.I)
    if m:
        return base + ['--stories', m.group(1)]
    m = re.search(r'instagram\.com/(?:[^/]+/)?(?:p|reel|reels|tv)/([^/?#]+)', url, re.I)
    if m:
        return base + ['--', '-' + m.group(1)]
    return None  # solo posts, reels y stories


def args_you_get(url):
    return ['-o', str(DESTINO), *cookies_args('-c'), url]


def args_streamlink(url):
    return ['--hls-duration', '01:00:00',
            '-o', str(DESTINO / f'directo-{int(time.time())}.ts'),
            url, 'best']


def redes_yt_dlp():
    """Lista real de sitios que conoce la versión instalada de yt-dlp."""
    r = subprocess.run([sys.executable, '-m', 'yt_dlp', '--list-extractors'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    nombres = {l.strip().split(':')[0].lower() for l in r.stdout.splitlines() if l.strip()}
    nombres.discard('generic')
    return sorted(nombres)


MOTORES = {
    'yt-dlp': {
        'nombre': 'yt-dlp', 'modulo': 'yt_dlp',
        'descripcion': 'Videos de YouTube, TikTok, X, Facebook, Vimeo y cientos de sitios más.',
        'argumentos': args_yt_dlp, 'redes': redes_yt_dlp,
    },
    'gallery-dl': {
        'nombre': 'gallery-dl', 'modulo': 'gallery_dl',
        'descripcion': 'Fotos, galerías y stories de redes como Instagram, Reddit y Pinterest.',
        'argumentos': args_gallery_dl,
        'redes': ['Instagram', 'X (Twitter)', 'Reddit', 'Pinterest', 'Flickr', 'DeviantArt',
                  'Tumblr', 'Imgur', 'Facebook', 'Mastodon', 'Bluesky'],
    },
    'instaloader': {
        'nombre': 'Instaloader', 'modulo': 'instaloader',
        'descripcion': 'Posts, reels y stories de Instagram.',
        'argumentos': args_instaloader,
        'redes': ['Instagram (posts, reels y stories)'],
    },
    'you-get': {
        'nombre': 'you-get', 'modulo': 'you_get',
        'descripcion': 'Videos de muchos sitios, incluidos algunos que yt-dlp no cubre.',
        'argumentos': args_you_get,
        'redes': ['YouTube', 'Vimeo', 'Dailymotion', 'Facebook', 'X (Twitter)', 'Instagram',
                  'TikTok', 'SoundCloud', 'Bilibili', 'Niconico', 'Youku'],
    },
    'streamlink': {
        'nombre': 'Streamlink', 'modulo': 'streamlink',
        'descripcion': 'Graba transmisiones en vivo (directos). Se corta a la hora si el directo sigue.',
        'argumentos': args_streamlink,
        'redes': ['Twitch', 'YouTube (directos)', 'Kick', 'Dailymotion (directos)'],
    },
}


def instalado(motor):
    return importlib.util.find_spec(motor['modulo']) is not None


def listar():
    salida = []
    for id_, m in MOTORES.items():
        ok = instalado(m)
        redes = []
        if ok:
            redes = m['redes']() if callable(m['redes']) else m['redes']
        salida.append({'id': id_, 'nombre': m['nombre'], 'descripcion': m['descripcion'],
                       'instalado': ok, 'redes': redes})

    por_id = {m['id']: m for m in salida}
    auto_redes = sorted(set(por_id['yt-dlp']['redes']) | set(por_id['gallery-dl']['redes']))
    auto = {'id': 'auto', 'nombre': 'Automático',
            'descripcion': 'Prueba yt-dlp y, si falla, gallery-dl.',
            'instalado': por_id['yt-dlp']['instalado'] or por_id['gallery-dl']['instalado'],
            'redes': auto_redes}
    return [auto] + salida


# ---------- descarga ----------

def archivos_nuevos(desde):
    encontrados = []
    for ruta in DESTINO.rglob('*'):
        if not ruta.is_file():
            continue
        if re.search(r'(\.part(-\w+)?|\.ytdl|\.temp)$|^ultimo_log\.txt$', ruta.name, re.I):
            continue
        if ruta.stat().st_mtime >= desde - 2:
            encontrados.append(ruta)
    return sorted(encontrados, key=lambda p: p.stat().st_mtime, reverse=True)


def ejecutar(id_, url):
    m = MOTORES[id_]
    if not instalado(m):
        paquete = m['modulo'].replace('_', '-')
        return {'ok': False, 'error': f"{m['nombre']} no está instalado (pip install {paquete})."}

    args = m['argumentos'](url)
    if args is None:
        return {'ok': False, 'error': f"{m['nombre']} no soporta este enlace."}

    inicio = time.time()
    r = subprocess.run([sys.executable, '-m', m['modulo'], *args],
                       stdin=subprocess.DEVNULL, capture_output=True,
                       text=True, encoding='utf-8', errors='replace')

    (DESTINO / 'ultimo_log.txt').write_text(
        f"[{id_}] código de salida: {r.returncode}\n\n--- stdout ---\n{r.stdout}\n\n--- stderr ---\n{r.stderr}\n",
        encoding='utf-8')

    nuevos = archivos_nuevos(inicio)
    if nuevos:
        return {'ok': True, 'archivo': str(nuevos[0].relative_to(DESTINO)), 'motor': m['nombre']}

    lineas = [l for l in (r.stderr.strip() or r.stdout.strip()).splitlines() if l.strip()]
    return {'ok': False, 'error': f"{m['nombre']}: {lineas[-1] if lineas else 'sin detalles'}"}


def descargar(motor, url):
    if not re.match(r'^https?://\S+$', url, re.I):
        return {'ok': False, 'mensaje': 'Escribe un enlace que empiece por http:// o https://'}
    if motor != 'auto' and motor not in MOTORES:
        return {'ok': False, 'mensaje': 'Motor no válido.'}

    orden = ['yt-dlp', 'gallery-dl'] if motor == 'auto' else [motor]
    ultimo = 'La descarga falló.'
    for id_ in orden:
        r = ejecutar(id_, url)
        if r['ok']:
            return {'ok': True, 'archivo': r['archivo'], 'motor': r['motor'],
                    'mensaje': 'Descarga completada'}
        ultimo = r['error']
    return {'ok': False, 'mensaje': ultimo + ' Revisa descargas/ultimo_log.txt para ver el motivo.'}


def main():
    accion = sys.argv[1] if len(sys.argv) > 1 else ''
    if accion == 'listar':
        resultado = listar()
    elif accion == 'descargar' and len(sys.argv) == 4:
        resultado = descargar(sys.argv[2], sys.argv[3])
    else:
        resultado = {'ok': False, 'mensaje': 'Uso: motores_descargas.py listar | descargar <motor> <url>'}
    print(json.dumps(resultado, ensure_ascii=False))


if __name__ == '__main__':
    main()
