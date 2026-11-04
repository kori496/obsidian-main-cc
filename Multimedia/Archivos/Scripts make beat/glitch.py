"""Glitchy beat-synced edit in the 'make beat' style (menta palette), video vertical completo (~51 s).
usage: python glitch.py <src> <env.npy> <out.mp4> <frame_start> <frame_end>   (solo video; el audio se une despues)
       python glitch.py <src> <env.npy> <prefix> preview                      (guarda cuadros de prueba)
- <env.npy> sale de analyze.py (columnas t, flux, rms).
- Ajustar a mano: BPM, PH (primer tiempo fuerte), DUR, DROP_BAR, CY0/CY1 (filas con contenido del video fuente) y TAG.
Render en 2 mitades en paralelo y union con ffmpeg (ver la nota 'Estilo make beat').
"""
import sys, math, subprocess, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC, ENV, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
PREVIEW = sys.argv[4] == 'preview'
FPS = 30
W, H = 1080, 1920
SW, SH = 1080, 1920
CY0, CY1 = 292, 1626            # content rows in source
CH = CY1 - CY0
BPM = 150.98; P = 60 / BPM; PH = 0.344   # first downbeat
DUR = 50.9
N = int(DUR * FPS)
DROP_BAR = 8
TAG = 'lagrimankv'              # antes 'p4m'. Marca del productor (ver 'Marca y textos')

PAL = dict(bg=(246, 255, 250), pri=(24, 196, 138), deep=(8, 96, 70), light=(206, 246, 229),
           acc=(255, 92, 190), cyan=(40, 230, 255))

# audio flux envelope -> glitch drive
env = np.load(ENV); et, ef = env[:, 0], env[:, 1]
k = 5; ef = np.convolve(ef, np.ones(k) / k, 'same')
lo, hi = np.percentile(ef, 40), np.percentile(ef, 99)
def flux(t):
    i = min(len(et) - 1, np.searchsorted(et, t))
    return float(np.clip((ef[i] - lo) / (hi - lo), 0, 1))

FB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
_fc = {}
def font(sz):
    if sz not in _fc: _fc[sz] = ImageFont.truetype(FB, sz)
    return _fc[sz]
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_out_back(x):
    x = clamp(x); c1 = 1.9; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3

GLYPHS = '#%&@$!?/\\<>[]01'
_tc = {}
def text_sprite(txt, sz, color):
    k = (txt, sz, color)
    if k in _tc: return _tc[k]
    f = font(sz); bb = f.getbbox(txt)
    pad = 30
    im = Image.new('RGBA', (bb[2] - bb[0] + pad * 2, bb[3] - bb[1] + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad - bb[0], pad - bb[1]), txt, font=f, fill=color,
                            stroke_width=max(4, sz // 14), stroke_fill=(255, 255, 255))
    _tc[k] = im
    return im

def put_text(cv, txt, sz, color, cx, cy, t_in, t, rng, scramble=True):
    if t < t_in: return
    a = (t - t_in)
    if scramble and a < 0.1:   # glitch-in: scrambled characters for 3 frames
        txt = ''.join(rng.choice(GLYPHS) if ch != ' ' and rng.random() < 0.6 else ch for ch in txt)
    sp = text_sprite(txt, sz, color)
    s = 0.4 + 0.6 * ease_out_back(a / 0.16) if a < 0.16 else 1.0
    if s != 1.0:
        sp = sp.resize((max(1, int(sp.width * s)), max(1, int(sp.height * s))), Image.BILINEAR)
    # nombres largos (lagrimankv): que nunca se salgan del cuadro
    if sp.width > W - 80:
        kk = (W - 80) / sp.width
        sp = sp.resize((int(sp.width * kk), int(sp.height * kk)), Image.BILINEAR)
    cv.alpha_composite(sp, (int(cx - sp.width / 2), int(cy - sp.height / 2)))

# ---------- stickers ----------
def sticker(kind, size, col):
    S = size * 2; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = S / 2
    if kind == 'daisy':
        r = S * 0.2
        for i in range(8):
            a = i * math.pi / 4; x, y = c + math.cos(a) * r * 1.25, c + math.sin(a) * r * 1.25
            d.ellipse([x - r * .75, y - r * .75, x + r * .75, y + r * .75], fill=(255, 255, 255), outline=col, width=max(3, S // 40))
        d.ellipse([c - r * .7, c - r * .7, c + r * .7, c + r * .7], fill=col)
    elif kind == 'sparkle':
        pts = [(c + math.cos(i * math.pi / 4 - math.pi / 2) * (S * .46 if i % 2 == 0 else S * .11),
                c + math.sin(i * math.pi / 4 - math.pi / 2) * (S * .46 if i % 2 == 0 else S * .11)) for i in range(8)]
        d.polygon(pts, fill=col)
    elif kind == 'heart':
        r = S * 0.2
        d.ellipse([c - 2 * r, c - 1.6 * r, c, c + .4 * r], fill=col); d.ellipse([c, c - 1.6 * r, c + 2 * r, c + .4 * r], fill=col)
        d.polygon([(c - 1.93 * r, c - .3 * r), (c + 1.93 * r, c - .3 * r), (c, c + 2.1 * r)], fill=col)
    elif kind == 'pixel':   # glitch-themed: pixel cross
        u = S // 7
        for (i, j) in [(3, 1), (3, 2), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (3, 4), (3, 5)]:
            d.rectangle([i * u, j * u, i * u + u - 2, j * u + u - 2], fill=col)
    return im.resize((size, size), Image.LANCZOS)

def make_layout(seed, n=10):
    rng = random.Random(seed); items = []
    zones = [(40, 1040, 40, 250), (40, 1040, 1680, 1880), (20, 120, 260, 1660), (960, 1060, 260, 1660)]
    for i in range(n):
        z = zones[i % 4]
        items.append(dict(x=rng.uniform(z[0], z[1]), y=rng.uniform(z[2], z[3]),
                          spr=sticker(rng.choice(['daisy', 'sparkle', 'heart', 'pixel', 'sparkle']), rng.randint(70, 140),
                                      rng.choice([PAL['pri'], PAL['acc'], PAL['pri'], PAL['light']])),
                          rot0=rng.uniform(-30, 30), spin=rng.uniform(5, 15) * rng.choice([-1, 1]),
                          delay=rng.uniform(0, .25), ph=rng.uniform(0, 6.28)))
    return items
LAYOUTS = [make_layout(s) for s in range(12)]

def draw_stickers(cv, layout, t, t0, pulse):
    for it in layout:
        a = (t - t0 - it['delay']) / 0.2
        if a <= 0: continue
        s = (ease_out_back(a) if a < 1 else 1.0) * (1 + .12 * pulse)
        sp = it['spr']; sz = max(2, int(sp.width * s))
        sp = sp.resize((sz, sz), Image.BILINEAR).rotate(it['rot0'] + it['spin'] * math.sin(t * 2 + it['ph']), expand=True)
        cv.alpha_composite(sp, (int(it['x'] - sp.width / 2), int(it['y'] + 10 * math.sin(t * 3 + it['ph']) - sp.height / 2)))

# ---------- footage ----------
PRI = np.array(PAL['pri'], np.float32); WHITE = np.full(3, 255, np.float32); DEEP = np.array(PAL['deep'], np.float32)
def duotone(rgb):
    L = rgb.astype(np.float32) @ np.array([.299, .587, .114], np.float32) / 255
    m = (np.clip((L - 0.07) / 0.30, 0, 1) ** 0.8)[..., None]
    out = PRI + (WHITE - PRI) * m
    hi = np.clip((L - .82) / .15, 0, 1)[..., None]
    return (out + (DEEP - out) * hi * .6).astype(np.uint8)

def crop(content, cx, cy, w, aspect):
    h = w / aspect
    if h > CH: h = CH; w = h * aspect
    if w > SW: w = SW; h = w / aspect
    x0 = int(clamp(cx - w / 2, 0, SW - w)); y0 = int(clamp(cy - h / 2, 0, CH - h))
    return content[y0:y0 + int(h), x0:x0 + int(w)]

def rmask(w, h, r):
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255); return m

def screen(content, spec, sw, sh, raw=False):
    c = crop(content, *spec, sw / sh)
    a = c if raw else duotone(c)
    im = Image.fromarray(np.ascontiguousarray(a)).resize((sw, sh), Image.BILINEAR)
    a = np.asarray(im).copy(); a[::6] = (a[::6] * .9).astype(np.uint8)
    return Image.fromarray(a)

def tv(cv, content, cx, cy, w, h, spec, scale=1.0, slide=0, raw=False):
    w2, h2 = int(w * scale), int(h * scale); cx += slide
    scr = screen(content, spec, w2, h2, raw)
    bz = int(36 * scale); bot = int(100 * scale)
    tw, th = w2 + bz * 2, h2 + bz * 2 + bot
    im = Image.new('RGBA', (tw + 20, th + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([10, 18, tw + 10, th + 18], int(64 * scale), fill=PAL['deep'] + (60,))
    d.rounded_rectangle([0, 0, tw, th], int(64 * scale), fill=PAL['light'], outline=PAL['deep'], width=6)
    d.rounded_rectangle([bz - 10, bz - 10, bz + w2 + 10, bz + h2 + 10], int(44 * scale), fill=PAL['deep'])
    im.paste(scr, (bz, bz), rmask(w2, h2, int(36 * scale)))
    ky = bz + h2 + bz // 2 + bot // 2
    for kx in (bz + 46 * scale, tw - bz - 46 * scale):
        r = 30 * scale
        d.ellipse([kx - r, ky - r, kx + r, ky + r], fill=PAL['pri'], outline=PAL['deep'], width=5)
        d.ellipse([kx - r * .35, ky - r * .9, kx + r * .35, ky - r * .3], fill=(255, 255, 255))
    for i in range(5):
        x = tw / 2 - 80 * scale + i * 40 * scale
        d.rounded_rectangle([x, ky - 20 * scale, x + 16 * scale, ky + 20 * scale], 6, fill=PAL['pri'])
    cv.alpha_composite(im, (int(cx - tw / 2), int(cy - h2 / 2 - bz)))

def window(cv, content, cx, cy, w, h, spec, scale=1.0, slide=0):
    w2, h2 = int(w * scale), int(h * scale); cx += slide
    scr = screen(content, spec, w2, h2)
    bar, bd, o = int(56 * scale), 6, 14
    tw, th = w2 + bd * 2, h2 + bar + bd
    im = Image.new('RGBA', (tw + o, th + o), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([o, o, tw + o - 1, th + o - 1], 20, fill=PAL['deep'])
    d.rounded_rectangle([0, 0, tw - 1, th - 1], 20, fill=PAL['pri'], outline=PAL['deep'], width=bd)
    for i, col in enumerate([PAL['acc'], (255, 255, 255), PAL['light']]):
        x, y, r = 30 + i * 40, bar // 2 + 2, 12
        d.ellipse([x - r, y - r, x + r, y + r], fill=col, outline=PAL['deep'], width=3)
    im.paste(scr, (bd, bar))
    cv.alpha_composite(im, (int(cx - tw / 2), int(cy - th / 2 + bar / 2)))

# ---------- glitch fx (numpy on final frame) ----------
def glitch(a, amt, rng, t):
    if amt <= 0.02: return a
    a = a.copy()
    # 1. horizontal slice displacement
    for _ in range(int(2 + amt * 14)):
        y = rng.randrange(0, H - 10); hh = rng.randrange(6, int(20 + amt * 120))
        dx = int(rng.uniform(-1, 1) * amt * 160)
        a[y:y + hh] = np.roll(a[y:y + hh], dx, axis=1)
        if rng.random() < amt * 0.35:   # tinted band
            col = np.array(rng.choice([PAL['acc'], PAL['cyan'], PAL['pri']]), np.float32)
            a[y:y + hh] = (a[y:y + hh] * .55 + col * .45).astype(np.uint8)
    # 2. macroblocks copied from elsewhere
    for _ in range(int(amt * 8)):
        bw, bh = rng.randrange(40, 240), rng.randrange(20, 120)
        x0, y0 = rng.randrange(0, W - bw), rng.randrange(0, H - bh)
        x1, y1 = clamp(x0 + rng.randrange(-200, 200), 0, W - bw), clamp(y0 + rng.randrange(-120, 120), 0, H - bh)
        a[int(y1):int(y1) + bh, int(x1):int(x1) + bw] = a[y0:y0 + bh, x0:x0 + bw]
    # 3. RGB split
    dx = int(4 + amt * 26)
    out = a.copy()
    out[..., 0] = np.roll(a[..., 0], dx, axis=1)
    out[..., 2] = np.roll(a[..., 2], -dx, axis=1)
    if amt > .5:
        out[..., 1] = np.roll(a[..., 1], int(amt * 8), axis=0)
    # 4. noise scanlines
    if amt > .3:
        ys = rng.sample(range(H), int(amt * 40))
        out[ys] = np.clip(out[ys].astype(np.int16) + 70, 0, 255).astype(np.uint8)
    return out

# ---------- timeline ----------
LABELS = ['kick', 'hats', 'clap', 'melody', '808', 'perc']
def scene(t, content, held):
    rng = random.Random(int(t * 15))     # chunky 15fps randomness
    tb = (t - PH) / P
    b = math.floor(tb); fr = tb - b
    bar = b // 4; beat_in_bar = b % 4
    pulse = math.exp(-fr * 5)
    cv = Image.new('RGBA', (W, H), PAL['bg'] + (255,))
    d = ImageDraw.Draw(cv)
    for yy in range(0, H, 60):
        for xx in range((yy // 60) % 2 * 30, W, 60):
            d.ellipse([xx - 3, yy - 3, xx + 3, yy + 3], fill=PAL['light'])

    # section = 2 bars before drop, 4 bars after
    if bar < 1:
        sec, s0 = -1, 0
    elif bar < DROP_BAR:
        sec, s0 = (bar - 1) // 2, 1 + ((bar - 1) // 2) * 2
    else:
        sec, s0 = 10 + (bar - DROP_BAR) // 4, DROP_BAR + ((bar - DROP_BAR) // 4) * 4
    ts = PH + s0 * 4 * P if sec != -1 else 0
    since = t - ts
    draw_stickers(cv, LAYOUTS[(sec + 1) % len(LAYOUTS)], t, ts, pulse)
    slide = (1 - ease_out(since / .18)) * (700 if sec % 2 else -700) if sec > 0 and since < .2 else 0
    sc = 1 + .035 * pulse
    pan = clamp(since / (16 * P))
    src = held if held is not None else content

    if sec == -1:   # intro title
        put_text(cv, 'make', 210, PAL['pri'], 590, 760, 0, t, rng)
        put_text(cv, 'beat', 260, PAL['deep'], 470, 990, PH + P, t, rng)
        put_text(cv, 'prod. ' + TAG, 80, PAL['acc'], 700, 1180, PH + 2 * P, t, rng)
    elif sec < 10:  # pre-drop: one big TV, label per 2 bars
        tv(cv, src, W / 2, 900, 820, 900, (540, 666 + 150 * (pan - .5), 1000 - 150 * pan), sc, slide)
        put_text(cv, LABELS[sec % len(LABELS)], 150, PAL['pri'], W / 2, 240, ts, t, rng)
        put_text(cv, TAG, 90, PAL['acc'], W / 2, 1640, ts + P, t, rng)
    else:
        m = (sec - 10) % 4
        last = bar >= 30
        if last:
            tv(cv, src, W / 2, 820, 820, 840, (540, 666, 1080), sc)
            put_text(cv, 'link in bio', 110, PAL['deep'], W / 2, 1530, ts, t, rng)
            put_text(cv, 'prod. ' + TAG, 80, PAL['acc'], W / 2, 1660, ts + P, t, rng)
        elif m == 0:   # DROP / big screen + stutter word
            tv(cv, src, W / 2, 860, 860, 960, (540, 666, 1080 / (1 + .15 * pulse)), 1 + .02 * pulse, slide)
            put_text(cv, 'drop!' if sec == 10 else TAG, 110, PAL['pri'], W / 2, 200, ts, t, rng)
            put_text(cv, ['bum', 'bum', 'bum!', TAG][beat_in_bar], 170, PAL['deep'], W / 2, 1650, PH + b * P, t, rng)
        elif m == 1:   # two stacked windows, alternate every 2 beats
            act = (b // 2) % 2
            window(cv, src, W / 2, 560, 820, 560, (540, 330 + 100 * pan, 900), 1 + (.05 * pulse if act == 0 else -.04), slide)
            window(cv, src, W / 2, 1290, 820, 560, (540, 1000 - 100 * pan, 900), 1 + (.05 * pulse if act == 1 else -.04), -slide)
            put_text(cv, LABELS[(sec + b // 4) % len(LABELS)], 110, PAL['pri'], W / 2, 170, PH + (b - b % 4) * P, t, rng)
            put_text(cv, '808', 120, PAL['acc'], W / 2, 1720, ts + P, t, rng)
        elif m == 2:   # zoom on track names (left) + playhead
            tv(cv, src, W / 2, 780, 820, 760, (230 + 500 * pan, 620, 520), sc, slide)
            put_text(cv, 'loop', 160, PAL['deep'], W / 2, 220, ts, t, rng)
            put_text(cv, 'all sounds', 70, PAL['pri'], W / 2, 1480, ts + 2 * P, t, rng)
            put_text(cv, 'by ' + TAG, 70, PAL['acc'], W / 2, 1580, ts + 3 * P, t, rng)
        else:          # RAW footage beat (unfiltered colours) - contrast moment
            tv(cv, src, W / 2, 880, 860, 960, (540, 666, 900), sc, slide, raw=(beat_in_bar % 2 == 0))
            put_text(cv, 'glitch', 150, PAL['acc'], W / 2, 220, ts, t, rng)
            put_text(cv, LABELS[b % len(LABELS)], 120, PAL['deep'], W / 2, 1660, PH + b * P, t, rng)

    out = np.asarray(cv.convert('RGB'))

    # glitch amount: driven by beat pulse + audio flux; heavier after drop
    f = flux(t)
    base = 0.15 if bar < DROP_BAR else 0.35
    amt = base * pulse + 0.45 * f * pulse
    if bar >= DROP_BAR and beat_in_bar in (1, 3): amt += 0.25 * pulse        # snare/clap hits
    if b % 8 == 7 and fr > .5: amt = max(amt, 0.7)                           # fill before each 2-bar
    if bar == DROP_BAR - 1 and beat_in_bar == 3: amt = max(amt, 0.4 + fr * .6)  # build into drop
    drop_t = t - (PH + DROP_BAR * 4 * P)
    if 0 <= drop_t < .5: amt = max(amt, 1.0 - drop_t * 1.4)
    if rng.random() < 0.06 * (1 + f): amt = max(amt, rng.uniform(.4, .8))   # random bursts
    out = glitch(out, min(amt, 1.0), rng, t)

    # inversion / colour flash on drop and each 4-bar downbeat after
    if 0 <= drop_t < 2 / FPS or (bar >= DROP_BAR and beat_in_bar == 0 and bar % 4 == 0 and fr * P < 1.5 / FPS):
        out = 255 - out
    elif 2 / FPS <= drop_t < .15:
        out = (out * .4 + np.array(PAL['pri']) * .6).astype(np.uint8)
    if t > DUR - .4:
        k = clamp((t - (DUR - .4)) / .4)
        out = (out * (1 - k) + np.array(PAL['bg']) * k).astype(np.uint8)
    return out

def stutter_hold(t):
    """returns True on 1/8-note stutter windows (footage freezes & repeats)"""
    tb = (t - PH) / P; b = math.floor(tb); bar = b // 4
    return bar >= DROP_BAR and (b % 8 == 7 or (b % 16 == 15))

def main():
    if PREVIEW:
        fs, fe = 0, N
        want = {int(x * FPS) for x in [0.6, 1.5, 5.0, 12.9, 13.1, 13.3, 16.0, 21.0, 27.0, 33.0, 39.0, 49.5]}
    else:
        fs, fe = int(sys.argv[4]), int(sys.argv[5])
    t0 = fs / FPS
    dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-ss', f'{t0:.4f}', '-i', SRC, '-t', f'{(fe - fs) / FPS + .2:.3f}',
                            '-vf', f'fps={FPS}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = None
    if not PREVIEW:
        enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                                '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                                '-pix_fmt', 'yuv420p', OUT], stdin=subprocess.PIPE)
    last = None; held = None; held_until = -1
    for i in range(fs, fe):
        buf = dec.stdout.read(SW * SH * 3)
        if len(buf) == SW * SH * 3:
            last = np.frombuffer(buf, np.uint8).reshape(SH, SW, 3)[CY0:CY1]
        t = i / FPS
        # stutter: freeze footage on 1/8 grid
        if stutter_hold(t):
            e = (t - PH) / (P / 2)
            key = math.floor(e)
            if key != held_until: held, held_until = last, key
            if (e - key) > .55: held = last          # small chop, re-grab
            use = held
        else:
            use = None
        if PREVIEW:
            if i in want:
                Image.fromarray(scene(t, last, use)).resize((360, 640)).save(f'{OUT}_{i:04d}.png')
            continue
        enc.stdin.write(scene(t, last, use).tobytes())
    dec.stdout.close(); dec.wait()
    if enc: enc.stdin.close(); enc.wait()

if __name__ == '__main__':
    main()
