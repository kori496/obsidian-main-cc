"""V.YA · lote 29 oct · 12 stories 1080x1920, solo logo (chico, abajo al centro),
12 formatos nuevos (distintos de los lotes 24, 26 y 28 oct), con la linea de
[[Referencias de stories de otras tiendas]]: foto real como protagonista, neutros.
Fotos: fotogramas nitidos sacados de los videos de la sesion 29 oct
(IA SOURCE IMAGES, IMG_1569..IMG_1603) -> src/<video>_<n>.jpg, y 3 fotos de jeans
floral (foto_171458/171711/171725.jpeg).
Logo: logo_mask.png.
Uso: python stories_29oct.py [filtro]
"""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "src")
OUT = os.path.join(BASE, "out")
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
CREAM = (238, 231, 222)
CREAM2 = (245, 240, 233)
OFF = (251, 249, 245)
SAND = (222, 210, 194)
TAUPE = (205, 191, 175)
BROWN = (108, 72, 52)
MOCHA = (150, 118, 92)
WHITE = (255, 255, 255)
LOGO = Image.open(os.path.join(BASE, "logo_mask.png")).convert("L")
LOGO_W = 230
LOGO_Y = 1795


def logo(cv, color, cx=W // 2, cy=LOGO_Y, width=LOGO_W, shadow=False):
    m = LOGO.resize((width, int(LOGO.height * width / LOGO.width)), Image.LANCZOS)
    if shadow:
        pad = 40
        sm = Image.new("L", (m.width + 2 * pad, m.height + 2 * pad), 0)
        sm.paste(m, (pad, pad))
        sm = sm.filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.45))
        cv.paste((20, 15, 12), (int(cx - m.width / 2) - pad + 2, int(cy - m.height / 2) - pad + 3), sm)
    cv.paste(Image.new("RGB", m.size, color), (int(cx - m.width / 2), int(cy - m.height / 2)), m)


def photo(name):
    p = os.path.join(SRC, name if "." in name else name + ".jpg")
    im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
    im = ImageEnhance.Contrast(im).enhance(1.04)
    im = ImageEnhance.Color(im).enhance(1.02)
    return ImageEnhance.Brightness(im).enhance(1.02)


def fit(im, w, h, ox=0.0, oy=0.0, zoom=1.0):
    s = max(w / im.width, h / im.height) * zoom
    nw, nh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    r = im.resize((nw, nh), Image.LANCZOS)
    ex, ey = nw - w, nh - h
    x = int(ex / 2 * (1 + ox)); y = int(ey / 2 * (1 + oy))
    return r.crop((x, y, x + w, y + h)).filter(ImageFilter.UnsharpMask(radius=1.3, percent=50, threshold=2))


def rmask(w, h, r):
    m = Image.new("L", (w * 2, h * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * 2 - 1, h * 2 - 1), r * 2, fill=255)
    return m.resize((w, h), Image.LANCZOS)


def cmask(d):
    m = Image.new("L", (d * 3, d * 3), 0)
    ImageDraw.Draw(m).ellipse((0, 0, d * 3 - 1, d * 3 - 1), fill=255)
    return m.resize((d, d), Image.LANCZOS)


def shadow(cv, box, blur=22, alpha=80, off=(8, 14), radius=0, mask=None):
    x0, y0, x1, y1 = box
    pad = blur * 3
    sh = Image.new("L", (x1 - x0 + 2 * pad, y1 - y0 + 2 * pad), 0)
    if mask is not None:
        sh.paste(mask.point(lambda v: int(v * alpha / 255)), (pad, pad))
    else:
        ImageDraw.Draw(sh).rounded_rectangle((pad, pad, pad + x1 - x0, pad + y1 - y0), radius, fill=alpha)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    cv.paste((0, 0, 0), (x0 - pad + off[0], y0 - pad + off[1]), sh)


def put(cv, im, x, y, radius=0, sh=False, mask=None, border=0, bcol=WHITE):
    if border:
        b = Image.new("RGB", (im.width + 2 * border, im.height + 2 * border), bcol)
        b.paste(im, (border, border))
        im = b; x -= border; y -= border
        if radius:
            radius += border
    if mask is None and radius:
        mask = rmask(im.width, im.height, radius)
    if sh:
        shadow(cv, (x, y, x + im.width, y + im.height), radius=radius, mask=mask)
    cv.paste(im, (x, y), mask)


def circle(cv, im, cx, cy, d, border=10, sh=True, **k):
    tot = d + 2 * border
    if sh:
        shadow(cv, (cx - tot // 2, cy - tot // 2, cx + tot // 2, cy + tot // 2), radius=tot // 2, alpha=90)
    ImageDraw.Draw(cv).ellipse((cx - tot // 2, cy - tot // 2, cx + tot // 2, cy + tot // 2), fill=WHITE)
    cv.paste(fit(im, d, d, **k), (cx - d // 2, cy - d // 2), cmask(d))


def bottom_fade(cv, start=1560, strength=140):
    g = Image.new("L", (1, H), 0)
    for y in range(H):
        g.putpixel((0, y), int(max(0, (y - start) / (H - start)) ** 1.4 * strength))
    cv.paste((25, 18, 14), (0, 0), g.resize((W, H)))


# ---------------- 12 piezas ----------------

def p01():  # 1597 rojo · a sangre + circulo de detalle + marco de linea fina
    cv = fit(photo("1597_0"), W, H, oy=-0.1)
    bottom_fade(cv)
    d = ImageDraw.Draw(cv)
    d.rectangle((40, 40, W - 41, H - 41), outline=WHITE, width=2)
    circle(cv, photo("1597_2"), 790, 1300, 380, oy=0.25, zoom=1.15)
    logo(cv, WHITE, shadow=True)
    return cv


def p02():  # 1602 blanco · secuencia de giro en 4 tiras verticales
    names = ["1602_3", "1602_2", "1602_6", "1602_5"]
    offs = [dict(ox=0.25, oy=-0.2), dict(oy=-0.2), dict(oy=-0.2), dict(oy=-0.1)]
    cv = Image.new("RGB", (W, H), CREAM)
    g, m = 8, 0
    cw = (W - 3 * g) // 4
    hh = 1660
    for i, (n, k) in enumerate(zip(names, offs)):
        cv.paste(fit(photo(n), cw, hh, **k), (i * (cw + g), 0))
    logo(cv, BROWN, cy=hh + (H - hh) // 2)
    return cv


def p03():  # 1577 denim · detalle a sangre + cuerpo entero en tarjeta alta
    cv = fit(photo("1577_2"), W, H, ox=0.0, oy=0.0, zoom=1.0)
    bottom_fade(cv, start=1500, strength=120)
    put(cv, fit(photo("1577_3"), 330, 640, oy=-0.05), 690, 1060, radius=18, border=12, sh=True)
    logo(cv, WHITE, shadow=True)
    return cv


def p04():  # 1600 negro · grilla 2x2 frente/espalda con margen crema
    names = [("1600_6", dict(oy=-0.1)), ("1600_1", dict(oy=-0.1)),
             ("1600_3", dict(oy=0.0)), ("1600_2", dict(oy=0.0))]
    cv = Image.new("RGB", (W, H), CREAM2)
    m, g = 44, 14
    cw = (W - 2 * m - g) // 2
    ch = 790
    for i, (n, k) in enumerate(names):
        x = m + (i % 2) * (cw + g); y = m + (i // 2) * (ch + g)
        cv.paste(fit(photo(n), cw, ch, **k), (x, y))
    logo(cv, BROWN, cy=m + 2 * ch + g + (H - (m + 2 * ch + g)) // 2)
    return cv


def p05():  # 1599 · dos capsulas desfasadas
    cv = Image.new("RGB", (W, H), SAND)
    cw, ch = 440, 1180
    put(cv, fit(photo("1599_5"), cw, ch, oy=-0.1), 70, 150, radius=cw // 2, sh=True)
    put(cv, fit(photo("1599_4"), cw, ch, oy=0.0), W - 70 - cw, 470, radius=cw // 2, sh=True)
    logo(cv, BROWN, cy=1790)
    return cv


def p06():  # 1595 · lectura de arriba abajo: 3 bandas del mismo look
    cv = Image.new("RGB", (W, H), CREAM)
    g = 10
    hh = [600, 520, 560]
    y = 0
    bands = [("1595_6", dict(oy=-0.35, zoom=1.0)), ("1595_2", dict(oy=0.15, zoom=1.35)),
             ("1595_4", dict(oy=0.75, zoom=1.0))]
    for (n, k), h in zip(bands, hh):
        cv.paste(fit(photo(n), W, h, **k), (0, y)); y += h + g
    logo(cv, BROWN, cy=y + (H - y) // 2 - 4)
    return cv


def p07():  # 1598 · cinta de contactos arriba + foto grande
    cv = Image.new("RGB", (W, H), OFF)
    m, g = 40, 12
    sq = (W - 2 * m - 3 * g) // 4
    for i, (n, k) in enumerate([("1598_1", dict(oy=-0.3, zoom=1.2)), ("1598_2", dict(oy=-0.1, zoom=1.1)),
                                 ("1598_5", dict(oy=0.1, zoom=1.1)), ("1598_3", dict(oy=0.2))]):
        cv.paste(fit(photo(n), sq, sq, **k), (m + i * (sq + g), m))
    top = m + sq + 26
    cv.paste(fit(photo("1598_6"), W - 2 * m, 1620 - top, oy=-0.05), (m, top))
    logo(cv, BROWN, cy=1770)
    return cv


def p08():  # 1603 · espejo redondeado + espalda superpuesta
    cv = Image.new("RGB", (W, H), TAUPE)
    mw, mh = 760, 1380
    put(cv, fit(photo("1603_1"), mw, mh, oy=-0.1), (W - mw) // 2 + 60, 130, radius=60, sh=True)
    put(cv, fit(photo("1603_4"), 330, 520, oy=0.0), 70, 1020, radius=14, border=12, sh=True)
    logo(cv, OFF, cy=1760)
    return cv


def p09():  # 1601 · a sangre + franja clara con 3 miniaturas
    cv = fit(photo("1601_4"), W, H, oy=0.0)
    band_y, band_h = 1280, 640
    band = cv.crop((0, band_y, W, H)).filter(ImageFilter.GaussianBlur(18))
    band = Image.blend(band, Image.new("RGB", band.size, CREAM2), 0.72)
    cv.paste(band, (0, band_y))
    m, g = 70, 24
    sw = (W - 2 * m - 2 * g) // 3
    sh_ = 340
    for i, (n, k) in enumerate([("1601_0", dict(oy=-0.1)), ("1601_5", dict(oy=-0.3)), ("1601_2", dict(oy=0.3, zoom=1.2))]):
        put(cv, fit(photo(n), sw, sh_, **k), m + i * (sw + g), band_y + 50, radius=10)
    logo(cv, BROWN, cy=LOGO_Y)
    return cv


def p10():  # 1596 · cruz: foto alta centrada + espalda horizontal que la cruza
    cv = Image.new("RGB", (W, H), CREAM)
    tw, th = 640, 1420
    put(cv, fit(photo("1596_3"), tw, th, oy=-0.05), (W - tw) // 2, 90, sh=True)
    hw, hh = 940, 470
    put(cv, fit(photo("1596_2"), hw, hh, oy=0.15, zoom=1.0), (W - hw) // 2, 1150, sh=True, border=12)
    logo(cv, BROWN, cy=1790)
    return cv


def p11():  # 1569 · cuadro dentro del cuadro
    bg = fit(photo("1569_5"), W, H, oy=-0.1)
    bg = ImageEnhance.Brightness(bg).enhance(0.82)
    cv = bg
    fw, fh = 620, 900
    put(cv, fit(photo("1569_2"), fw, fh, oy=0.1, zoom=1.0), (W - fw) // 2, 420, border=16, sh=True)
    logo(cv, WHITE, shadow=True)
    return cv


def p12():  # jeans floral · tela a sangre + jean en tarjeta + circulo de tienda
    cv = fit(photo("jean_0"), W, H, oy=-0.2, zoom=2.2)
    cv = ImageEnhance.Brightness(cv).enhance(0.9)
    put(cv, fit(photo("foto_171711.jpeg"), 600, 1140, oy=0.0, zoom=1.05), 110, 180, border=14, sh=True)
    circle(cv, photo("foto_171725.jpeg"), 790, 1330, 340, zoom=1.0)
    bottom_fade(cv, start=1600, strength=110)
    logo(cv, WHITE, shadow=True)
    return cv


PIEZAS = [
    ("01_sangre_circulo_marco_1597", p01), ("02_giro_4_tiras_1602", p02),
    ("03_detalle_sangre_tarjeta_1577", p03), ("04_grilla_2x2_1600", p04),
    ("05_capsulas_1599", p05), ("06_tres_bandas_1595", p06),
    ("07_contactos_1598", p07), ("08_espejo_1603", p08),
    ("09_franja_miniaturas_1601", p09), ("10_cruz_1596", p10),
    ("11_cuadro_en_cuadro_1569", p11), ("12_jean_floral", p12),
]

if __name__ == "__main__":
    only = sys.argv[1:]
    for name, fn in PIEZAS:
        if only and not any(o in name for o in only):
            continue
        fn().save(os.path.join(OUT, f"{name}.png"), optimize=True)
        print("ok", name)
