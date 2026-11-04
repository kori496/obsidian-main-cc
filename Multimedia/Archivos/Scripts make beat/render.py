"""Beat-synced vertical edit in the 'make beat' style (version 15.9 s, FL Studio horizontal).
usage: python render.py <variant: menta|lila> <src.mp4> <out.mp4> [--preview]
Entrada: grabacion de pantalla horizontal 1280x720 (se reescala). Salida: 1080x1920, 30 fps, audio del original.
Ajustar a mano en la seccion 'timing': BPM, START (donde empieza el tramo) y BEATS.
"""
import sys, math, subprocess, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

VARIANT, SRC, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
PREVIEW = '--preview' in sys.argv

# ---------------- timing ----------------
BPM = 150.9
P = 60.0 / BPM            # beat seconds
START = 89.025 - 4 * P    # one bar of intro before the drop (el drop estaba en 89.025 s del original)
BEATS = 40                # 10 bars
DUR = BEATS * P
FPS = 30
W, H = 1080, 1920
SW, SH = 1280, 720

PAL = {
    'menta': dict(bg=(246, 255, 250), pri=(24, 196, 138), deep=(8, 96, 70),
                  light=(206, 246, 229), acc=(255, 122, 198), acc2=(255, 214, 236)),
    'lila':  dict(bg=(251, 248, 255), pri=(150, 104, 255), deep=(64, 34, 160),
                  light=(232, 222, 255), acc=(255, 196, 46), acc2=(255, 238, 190)),
}[VARIANT]

FB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
FCJK = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
_fc = {}
def font(sz, path=FB):
    k = (sz, path)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(path, sz)
    return _fc[k]

# ---------------- easing ----------------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_out_back(x):
    x = clamp(x); c1 = 1.9; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3

# ---------------- text ----------------
def text_sprite(txt, sz, color, path=FB):
    f = font(sz, path)
    if VARIANT == 'lila':
        txt = txt.upper()
    bb = f.getbbox(txt, stroke_width=0)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad = 30
    im = Image.new('RGBA', (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x, y = pad - bb[0], pad - bb[1]
    if VARIANT == 'menta':   # soft white outline sticker text
        d.text((x, y), txt, font=f, fill=color, stroke_width=max(4, sz // 14), stroke_fill=(255, 255, 255))
    else:                    # hard offset shadow, chunky
        o = max(4, sz // 16)
        d.text((x + o, y + o), txt, font=f, fill=PAL['deep'])
        d.text((x, y), txt, font=f, fill=color, stroke_width=max(2, sz // 30), stroke_fill=PAL['deep'])
    return im

_tc = {}
def put_text(canvas, txt, sz, color, cx, cy, t_in, t, path=FB, out_t=None):
    """pop-in text centred at cx,cy that appears at t_in"""
    if t < t_in or (out_t is not None and t >= out_t):
        return
    k = (txt, sz, color, path)
    if k not in _tc:
        _tc[k] = text_sprite(txt, sz, color, path)
    sp = _tc[k]
    a = (t - t_in) / 0.16
    s = 0.35 + 0.65 * ease_out_back(a) if a < 1 else 1.0
    if s != 1.0:
        sp = sp.resize((max(1, int(sp.width * s)), max(1, int(sp.height * s))), Image.BILINEAR)
    canvas.alpha_composite(sp, (int(cx - sp.width / 2), int(cy - sp.height / 2)))

# ---------------- stickers ----------------
def sticker(kind, size, col, rng):
    S = size * 2
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = S / 2
    deep = PAL['deep']
    if kind == 'daisy':
        r = S * 0.2
        for i in range(8):
            a = i * math.pi / 4
            x, y = c + math.cos(a) * r * 1.25, c + math.sin(a) * r * 1.25
            d.ellipse([x - r * 0.75, y - r * 0.75, x + r * 0.75, y + r * 0.75], fill=(255, 255, 255), outline=col, width=max(3, S // 40))
        d.ellipse([c - r * 0.7, c - r * 0.7, c + r * 0.7, c + r * 0.7], fill=col)
    elif kind == 'sparkle':
        pts = []
        for i in range(8):
            a = i * math.pi / 4 - math.pi / 2
            rr = S * 0.46 if i % 2 == 0 else S * 0.11
            pts.append((c + math.cos(a) * rr, c + math.sin(a) * rr))
        d.polygon(pts, fill=col)
    elif kind == 'heart':
        r = S * 0.2
        d.ellipse([c - 2 * r, c - 1.6 * r, c, c + 0.4 * r], fill=col)
        d.ellipse([c, c - 1.6 * r, c + 2 * r, c + 0.4 * r], fill=col)
        d.polygon([(c - 1.93 * r, c - 0.3 * r), (c + 1.93 * r, c - 0.3 * r), (c, c + 2.1 * r)], fill=col)
    elif kind == 'star':
        pts = []
        for i in range(10):
            a = i * math.pi / 5 - math.pi / 2
            rr = S * 0.46 if i % 2 == 0 else S * 0.2
            pts.append((c + math.cos(a) * rr, c + math.sin(a) * rr))
        d.polygon(pts, fill=col, outline=deep, width=max(3, S // 45))
    elif kind == 'ring':
        for k, rr in enumerate([0.44, 0.31, 0.18]):
            d.ellipse([c - S * rr, c - S * rr, c + S * rr, c + S * rr], outline=col, width=max(5, S // 22))
    elif kind == 'bubble':
        rr = S * 0.42
        d.ellipse([c - rr, c - rr, c + rr, c + rr], fill=col + (90,), outline=col, width=max(4, S // 30))
        d.ellipse([c - rr * 0.55, c - rr * 0.6, c - rr * 0.15, c - rr * 0.2], fill=(255, 255, 255, 230))
    return im.resize((size, size), Image.LANCZOS)

KINDS = {'menta': ['daisy', 'sparkle', 'heart', 'sparkle'],
         'lila': ['star', 'ring', 'bubble', 'star']}[VARIANT]

def make_layout(seed, n=11):
    rng = random.Random(seed)
    items = []
    # place around edges, avoid central panel zone
    zones = [(40, 1040, 40, 300), (40, 1040, 1620, 1880), (20, 170, 300, 1620), (910, 1060, 300, 1620)]
    cols = [PAL['pri'], PAL['acc'], PAL['pri'], PAL['light']]
    for i in range(n):
        z = zones[i % 4]
        x, y = rng.uniform(z[0], z[1]), rng.uniform(z[2], z[3])
        kind = rng.choice(KINDS)
        size = rng.randint(70, 150)
        col = rng.choice(cols)
        items.append(dict(x=x, y=y, spr=sticker(kind, size, col, rng), rot0=rng.uniform(-30, 30),
                          spin=rng.choice([-1, 1]) * rng.uniform(5, 15), delay=rng.uniform(0, 0.25),
                          ph=rng.uniform(0, 6.28)))
    return items

LAYOUTS = [make_layout(s) for s in range(6)]

def draw_stickers(canvas, layout, t, t0, beat_pulse):
    for it in layout:
        a = (t - t0 - it['delay']) / 0.2
        if a <= 0:
            continue
        s = ease_out_back(a) if a < 1 else 1.0
        s *= 1 + 0.12 * beat_pulse
        rot = it['rot0'] + it['spin'] * math.sin(t * 2 + it['ph'])
        sp = it['spr']
        sz = max(2, int(sp.width * s))
        sp = sp.resize((sz, sz), Image.BILINEAR).rotate(rot, resample=Image.BILINEAR, expand=True)
        bob = 10 * math.sin(t * 3 + it['ph'])
        canvas.alpha_composite(sp, (int(it['x'] - sp.width / 2), int(it['y'] + bob - sp.height / 2)))

# ---------------- footage ----------------
PRI = np.array(PAL['pri'], np.float32); WHITE = np.array([255, 255, 255], np.float32)
DEEP = np.array(PAL['deep'], np.float32)
def duotone(rgb):
    L = rgb.astype(np.float32) @ np.array([0.299, 0.587, 0.114], np.float32) / 255.0
    m = (np.clip((L - 0.07) / 0.22, 0, 1) ** 0.8)[..., None]
    out = PRI + (WHITE - PRI) * m
    # keep the very brightest bits (playhead, text) as deep accent lines
    hi = np.clip((L - 0.8) / 0.15, 0, 1)[..., None]
    out = out + (DEEP - out) * hi * 0.6
    return out.astype(np.uint8)

def crop(frame, cx, cy, w, aspect):
    h = w / aspect
    if h > SH: h = SH; w = h * aspect
    if w > SW: w = SW; h = w / aspect
    x0 = int(clamp(cx - w / 2, 0, SW - w)); y0 = int(clamp(cy - h / 2, 0, SH - h))
    return frame[y0:y0 + int(h), x0:x0 + int(w)]

def rounded_mask(w, h, r):
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
    return m

def screen_img(frame, cx, cy, cw, sw, sh):
    c = crop(frame, cx, cy, cw, sw / sh)
    im = Image.fromarray(duotone(c)).resize((sw, sh), Image.BILINEAR)
    # scanlines (reference has the CRT banding)
    a = np.asarray(im).copy()
    a[::6] = (a[::6].astype(np.int16) * 0.9).astype(np.uint8)
    return Image.fromarray(a)

def panel(canvas, frame, box, crop_spec, t, scale=1.0, slide=0.0):
    """box=(cx,cy,w,h) of the screen; draws TV (menta) or window (lila) chrome"""
    cx, cy, w, h = box
    w2, h2 = int(w * scale), int(h * scale)
    cx = cx + slide
    scr = screen_img(frame, *crop_spec, w2, h2)
    if VARIANT == 'menta':
        bz = int(40 * scale); bot = int(110 * scale)
        tw, th = w2 + bz * 2, h2 + bz * 2 + bot
        tv = Image.new('RGBA', (tw + 20, th + 20), (0, 0, 0, 0))
        d = ImageDraw.Draw(tv)
        d.rounded_rectangle([10, 18, tw + 10, th + 18], int(70 * scale), fill=PAL['deep'] + (60,))
        d.rounded_rectangle([0, 0, tw, th], int(70 * scale), fill=PAL['light'], outline=PAL['deep'], width=6)
        d.rounded_rectangle([bz - 10, bz - 10, bz + w2 + 10, bz + h2 + 10], int(48 * scale), fill=PAL['deep'])
        tv.paste(scr, (bz, bz), rounded_mask(w2, h2, int(40 * scale)))
        ky = bz + h2 + bz // 2 + bot // 2
        for kx in (bz + 50 * scale, tw - bz - 50 * scale):
            r = 32 * scale
            d.ellipse([kx - r, ky - r, kx + r, ky + r], fill=PAL['pri'], outline=PAL['deep'], width=5)
            d.ellipse([kx - r * 0.35, ky - r * 0.9, kx + r * 0.35, ky - r * 0.3], fill=(255, 255, 255))
        for i in range(5):
            x = tw / 2 - 80 * scale + i * 40 * scale
            d.rounded_rectangle([x, ky - 22 * scale, x + 16 * scale, ky + 22 * scale], 6, fill=PAL['pri'])
        canvas.alpha_composite(tv, (int(cx - tw / 2), int(cy - h2 / 2 - bz)))
    else:
        bar = int(64 * scale); bd = 7; o = 16
        tw, th = w2 + bd * 2, h2 + bar + bd
        win = Image.new('RGBA', (tw + o, th + o), (0, 0, 0, 0))
        d = ImageDraw.Draw(win)
        d.rounded_rectangle([o, o, tw + o - 1, th + o - 1], 22, fill=PAL['deep'])
        d.rounded_rectangle([0, 0, tw - 1, th - 1], 22, fill=PAL['pri'], outline=PAL['deep'], width=bd)
        for i, col in enumerate([PAL['acc'], (255, 255, 255), PAL['light']]):
            x = 34 + i * 44; y = bar // 2 + 2; r = 13
            d.ellipse([x - r, y - r, x + r, y + r], fill=col, outline=PAL['deep'], width=3)
        d.rounded_rectangle([tw - 230, bar // 2 - 9, tw - 40, bar // 2 + 11], 10, fill=PAL['light'])
        win.paste(scr, (bd, bar))
        d.rectangle([bd, bar, bd + w2, bar + 3], fill=PAL['deep'])
        canvas.alpha_composite(win, (int(cx - tw / 2), int(cy - th / 2 + bar / 2)))

# ---------------- timeline ----------------
# beat index -> section
def section(b):
    if b < 4: return 0       # intro title
    if b < 12: return 1      # drop - big screen
    if b < 20: return 2      # loop
    if b < 28: return 3      # melody / 808 stacked
    if b < 36: return 4      # drums stutter
    return 5                 # outro

def render(t, frame):
    tb = t / P; b = int(tb); fr = tb - b
    pulse = math.exp(-fr * 5.0)
    sec = section(b)
    sec_start_beat = [0, 4, 12, 20, 28, 36][sec]
    ts = sec_start_beat * P
    cv = Image.new('RGBA', (W, H), PAL['bg'] + (255,))

    # soft dotted texture background
    d = ImageDraw.Draw(cv)
    for yy in range(0, H, 60):
        for xx in range((yy // 60) % 2 * 30, W, 60):
            d.ellipse([xx - 3, yy - 3, xx + 3, yy + 3], fill=PAL['light'])

    draw_stickers(cv, LAYOUTS[sec], t, ts, pulse)

    since = t - ts
    slide = (1 - ease_out(since / 0.18)) * 700 if sec > 1 else 0
    sc = 1 + 0.035 * pulse

    pan = since / (8 * P)  # 0..1 across a section
    if sec == 0:
        put_text(cv, 'make', 210, PAL['pri'], 590, 780, 0.0, t)
        put_text(cv, 'beat', 260, PAL['deep'], 470, 1010, P * 1, t)
        put_text(cv, '비트 메이커', 60, PAL['acc'], 760, 1180, P * 2, t, FCJK)
        put_text(cv, '♪', 120, PAL['acc'], 190, 560, P * 3, t, FCJK)
    elif sec == 1:
        put_text(cv, 'new beat', 70, PAL['pri'], W / 2, 360, ts, t)
        panel(cv, frame, (W / 2, 900, 840, 620), (640 + 120 * pan, 380, 1200), t, sc)
        word = ['drop', 'drop', 'drop!', 'drop!']
        put_text(cv, word[(b - 4) % 4], 190 + (b % 2) * 20, PAL['deep'], W / 2, 1560, b * P, t)
    elif sec == 2:
        put_text(cv, 'loop', 150, PAL['pri'], W / 2, 330, ts, t)
        panel(cv, frame, (W / 2, 850, 840, 520), (460 + 300 * pan, 210, 760), t, sc, slide)
        put_text(cv, 'all sounds', 70, PAL['deep'], 640, 1400, ts + 2 * P, t)
        put_text(cv, 'by me', 70, PAL['acc'], 640, 1490, ts + 3 * P, t)
        # small thumbnail grid
        if since > P:
            g = screen_img(frame, 160, 360, 300, 260, 220).convert('RGBA')
            g = g.resize((int(260 * (1 + 0.06 * pulse)), int(220 * (1 + 0.06 * pulse))))
            gm = rounded_mask(g.width, g.height, 26)
            bgc = Image.new('RGBA', (g.width + 12, g.height + 12), PAL['deep'] + (255,))
            cv.paste(bgc, (300 - g.width // 2 - 6, 1440 - g.height // 2 - 6), rounded_mask(g.width + 12, g.height + 12, 30))
            cv.paste(g, (300 - g.width // 2, 1440 - g.height // 2), gm)
    elif sec == 3:
        active = (b // 2) % 2
        s1 = 1.0 + (0.05 * pulse if active == 0 else -0.04)
        s2 = 1.0 + (0.05 * pulse if active == 1 else -0.04)
        panel(cv, frame, (W / 2, 560, 780, 400), (520 + 200 * pan, 170, 820), t, s1, slide)
        panel(cv, frame, (W / 2, 1330, 780, 400), (760 - 200 * pan, 600, 820), t, s2, -slide)
        put_text(cv, 'melody', 110 if active == 0 else 90, PAL['pri'], W / 2, 190, ts, t)
        put_text(cv, '808', 130 if active == 1 else 100, PAL['acc'] if VARIANT == 'menta' else PAL['deep'], W / 2, 1760, ts + P, t)
    elif sec == 4:
        put_text(cv, 'drums', 160, PAL['deep'], W / 2, 320, ts, t)
        stut = 1 + 0.12 * pulse  # hard stutter zoom on every beat
        cw = 900 / stut
        panel(cv, frame, (W / 2, 920, 860, 700), (640, 470, cw), t, 1 + 0.02 * pulse, slide)
        put_text(cv, 'bum', 120, PAL['pri'], 250 + (b % 4) * 190, 1590, b * P, t)
    else:
        panel(cv, frame, (W / 2, 820, 860, 640), (640, 380, 1280), t, sc * ease_out(since / 0.2 + 0.3), 0)
        put_text(cv, 'link in bio', 110, PAL['deep'], W / 2, 1440, ts + P, t)
        put_text(cv, 'full beat', 70, PAL['acc'] if VARIANT == 'menta' else PAL['pri'], W / 2, 1570, ts + 2 * P, t)

    out = cv.convert('RGB')
    # flash on drop and on each section downbeat
    for fb, strength in [(4, 0.9), (12, 0.45), (20, 0.45), (28, 0.6), (36, 0.45)]:
        dt = t - fb * P
        if 0 <= dt < 0.12:
            col = PAL['pri'] if fb == 4 else (255, 255, 255)
            out = Image.blend(out, Image.new('RGB', (W, H), col), strength * (1 - dt / 0.12))
    # fade out
    if t > DUR - 0.35:
        out = Image.blend(out, Image.new('RGB', (W, H), PAL['bg']), clamp((t - (DUR - 0.35)) / 0.35))
    return out

# ---------------- io ----------------
def main():
    n = int(round(DUR * FPS))
    dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-ss', f'{START:.3f}', '-i', SRC, '-t', f'{DUR:.3f}',
                            '-vf', f'fps={FPS},scale={SW}:{SH}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                           stdout=subprocess.PIPE)
    if PREVIEW:
        want = {int(x * FPS) for x in [0.5, 1.4, 1.62, 2.5, 5.0, 8.0, 10.0, 12.3, 13.0, 15.2]}
        i = 0
        while True:
            buf = dec.stdout.read(SW * SH * 3)
            if len(buf) < SW * SH * 3: break
            if i in want:
                fr = np.frombuffer(buf, np.uint8).reshape(SH, SW, 3)
                render(i / FPS, fr).resize((360, 640)).save(f'{OUT}_{i:04d}.png')
            i += 1
        return
    enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y',
                            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-ss', f'{START:.3f}', '-t', f'{DUR:.3f}', '-i', SRC,
                            '-map', '0:v', '-map', '1:a',
                            '-af', f'afade=t=in:d=0.03,afade=t=out:st={DUR - 0.4:.3f}:d=0.4',
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
                            '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-shortest', OUT],
                           stdin=subprocess.PIPE)
    last = None
    for i in range(n):
        buf = dec.stdout.read(SW * SH * 3)
        if len(buf) == SW * SH * 3:
            last = np.frombuffer(buf, np.uint8).reshape(SH, SW, 3)
        enc.stdin.write(render(i / FPS, last).tobytes())
    enc.stdin.close(); enc.wait(); dec.wait()

if __name__ == '__main__':
    main()
