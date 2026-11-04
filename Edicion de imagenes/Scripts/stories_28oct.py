"""V.YA · lote 28 oct · 12 stories 1080x1920, solo logo, 12 formatos nuevos
(distintos de los lotes 24 y 26 oct).
Fotos: originales de Drive (sesiones 081526 / 081826 / 090226 / 100926) renombradas
prenda_XX_YY segun mapa_renombrado.csv -> carpeta src/.
Logo: logo_mask.png (recortado de una pieza vieja).
Uso: python stories_28oct.py [filtro]
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
ESPRESSO = (43, 33, 28)
WHITE = (255, 255, 255)
LOGO = Image.open(os.path.join(BASE, "logo_mask.png")).convert("L")


def logo(cv, cx, cy, width, color, rotate=0, shadow=False):
    m = LOGO.resize((width, int(LOGO.height * width / LOGO.width)), Image.LANCZOS)
    if rotate:
        m = m.rotate(rotate, expand=True, resample=Image.BICUBIC)
    if shadow:
        pad = 40
        sm = Image.new("L", (m.width + 2 * pad, m.height + 2 * pad), 0)
        sm.paste(m, (pad, pad))
        sm = sm.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.5))
        cv.paste((20, 15, 12), (int(cx - m.width / 2) - pad + 2, int(cy - m.height / 2) - pad + 4), sm)
    cv.paste(Image.new("RGB", m.size, color), (int(cx - m.width / 2), int(cy - m.height / 2)), m)


def photo(n, k):
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, f"prenda_{n:02d}_{k:02d}.jpeg"))).convert("RGB")
    im = ImageEnhance.Contrast(im).enhance(1.05)
    im = ImageEnhance.Color(im).enhance(1.03)
    return ImageEnhance.Brightness(im).enhance(1.03)


def fit(im, w, h, ox=0.0, oy=0.0, zoom=1.0):
    s = max(w / im.width, h / im.height) * zoom
    nw, nh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    r = im.resize((nw, nh), Image.LANCZOS)
    ex, ey = nw - w, nh - h
    x = int(ex / 2 * (1 + ox)); y = int(ey / 2 * (1 + oy))
    return r.crop((x, y, x + w, y + h)).filter(ImageFilter.UnsharpMask(radius=1.4, percent=55, threshold=2))


def rmask(w, h, r):
    m = Image.new("L", (w * 2, h * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * 2 - 1, h * 2 - 1), r * 2, fill=255)
    return m.resize((w, h), Image.LANCZOS)


def arch_mask(w, h):
    m = Image.new("L", (w * 2, h * 2), 0)
    d = ImageDraw.Draw(m)
    d.ellipse((0, 0, w * 2 - 1, w * 2 - 1), fill=255)
    d.rectangle((0, w, w * 2 - 1, h * 2 - 1), fill=255)
    return m.resize((w, h), Image.LANCZOS)


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


def put(cv, im, x, y, radius=0, sh=False, mask=None):
    if mask is None and radius:
        mask = rmask(im.width, im.height, radius)
    if sh:
        shadow(cv, (x, y, x + im.width, y + im.height), radius=radius, mask=mask)
    cv.paste(im, (x, y), mask)


def paste_rot(cv, im, cx, cy, angle, sh=True, alpha=0.35):
    a = Image.new("L", im.size, 255)
    r = im.rotate(angle, expand=True, resample=Image.BICUBIC)
    ra = a.rotate(angle, expand=True, resample=Image.BICUBIC)
    x, y = int(cx - r.width / 2), int(cy - r.height / 2)
    if sh:
        pad = 60
        s = Image.new("L", (r.width + 2 * pad, r.height + 2 * pad), 0)
        s.paste(ra.point(lambda v: int(v * alpha)), (pad, pad))
        s = s.filter(ImageFilter.GaussianBlur(22))
        cv.paste((0, 0, 0), (x - pad + 8, y - pad + 18), s)
    cv.paste(r, (x, y), ra)


def grain(cv, amount=6):
    import random
    n = Image.effect_noise((W, H), 40).convert("L")
    n = n.point(lambda v: 128 + int((v - 128) * amount / 40))
    return Image.blend(cv, Image.merge("RGB", (n, n, n)), 0.04)


# ---------------- 12 piezas ----------------

def p01():  # 08 · tira de fotomaton inclinada sobre foto grande desenfocada suave
    a, b, c = photo(8, 1), photo(8, 2), photo(8, 3)
    cv = Image.new("RGB", (W, H), SAND)
    # foto grande a la izquierda, a sangre arriba-abajo
    cv.paste(fit(a, 640, H, ox=-0.1), (0, 0))
    # tira blanca con 3 cuadros
    fw, fh, g, p = 330, 430, 22, 26
    strip = Image.new("RGB", (fw + 2 * p, 3 * fh + 2 * g + p + 120), OFF)
    strip.paste(fit(c, fw, fh, oy=-0.2), (p, p))
    strip.paste(fit(b, fw, fh, oy=-0.35, zoom=1.25), (p, p + fh + g))
    strip.paste(fit(a, fw, fh, oy=0.85, zoom=1.6), (p, p + 2 * (fh + g)))
    lm = LOGO.resize((200, int(LOGO.height * 200 / LOGO.width)), Image.LANCZOS)
    strip.paste(Image.new("RGB", lm.size, BROWN), ((strip.width - 200) // 2, strip.height - 60 - lm.height // 2), lm)
    paste_rot(cv, strip, 770, 930, -4, alpha=0.45)
    return cv


def p02():  # 24 · tres ventanas en arco
    ims = [photo(24, 1), photo(24, 2), photo(24, 3)]
    cv = Image.new("RGB", (W, H), CREAM)
    aw, ah, g = 300, 1180, 30
    x0 = (W - 3 * aw - 2 * g) // 2
    y0 = 300
    for i, im in enumerate(ims):
        m = arch_mask(aw, ah)
        x = x0 + i * (aw + g)
        yy = y0 + (0 if i == 1 else 90)
        put(cv, fit(im, aw, ah, oy=-0.05), x, yy, mask=m, sh=True)
    d = ImageDraw.Draw(cv)
    d.line((x0, 1650, W - x0, 1650), fill=MOCHA, width=2)
    logo(cv, W // 2, 1760, 300, BROWN)
    return cv


def p03():  # 31 · corte diagonal entre dos fotos con linea crema
    a, b = photo(31, 1), photo(31, 3)
    cv = fit(a, W, H, ox=0.0)
    right = fit(b, W, H, ox=0.0, oy=0.1, zoom=1.08)
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon([(W * 0.62, 0), (W, 0), (W, H), (W * 0.18, H)], fill=255)
    cv.paste(right, (0, 0), m)
    d = ImageDraw.Draw(cv)
    d.line((W * 0.62, 0, W * 0.18, H), fill=CREAM2, width=14)
    # banda inferior suave para el logo
    grad = Image.new("L", (1, H), 0)
    for y in range(H):
        grad.putpixel((0, y), int(max(0, (y - 1560) / 360) ** 1.3 * 150))
    cv.paste((25, 18, 14), (0, 0), grad.resize((W, H)))
    logo(cv, 780, 1800, 280, WHITE, shadow=True)
    return cv


def p04():  # 51 · foto completa + lupa de detalle con lineas guia
    a, b, c = photo(51, 1), photo(51, 2), photo(51, 3)
    cv = Image.new("RGB", (W, H), CREAM2)
    px, py, pw, ph = 70, 90, 600, 1580
    put(cv, fit(a, pw, ph), px, py, sh=True)
    d = ImageDraw.Draw(cv)
    # recuadro de detalle (pierna) sobre la foto
    bx0, by0, bx1, by1 = px + 150, py + 980, px + 450, py + 1340
    d.rectangle((bx0, by0, bx1, by1), outline=WHITE, width=4)
    # lupa: tela a rayas
    zx, zy, zw, zh = 700, 900, 320, 460
    put(cv, fit(b, zw, zh, oy=0.2, zoom=1.35), zx, zy, sh=True)
    d.rectangle((zx, zy, zx + zw - 1, zy + zh - 1), outline=BROWN, width=3)
    d.line((bx1, by0, zx, zy), fill=BROWN, width=2)
    d.line((bx1, by1, zx, zy + zh), fill=BROWN, width=2)
    # segunda lupa: top
    tx, ty, tw, th = 700, 240, 320, 460
    put(cv, fit(c, tw, th, oy=-0.3, zoom=1.15), tx, ty, sh=True)
    d.rectangle((tx, ty, tx + tw - 1, ty + th - 1), outline=BROWN, width=3)
    logo(cv, 860, 1640, 260, BROWN)
    return cv


def p05():  # 80 · cuadricula 2x2 a sangre con sello circular central
    ims = [photo(80, 2), photo(80, 5), photo(80, 1), photo(80, 4)]
    cv = Image.new("RGB", (W, H), CREAM)
    g = 10
    cw, ch = (W - g) // 2, (H - g) // 2
    offs = [(0, -0.2), (0, -0.4), (0, 0.1), (0, 0.0)]
    for i, im in enumerate(ims):
        x = (i % 2) * (cw + g); y = (i // 2) * (ch + g)
        cv.paste(fit(im, cw, ch, ox=offs[i][0], oy=offs[i][1]), (x, y))
    r = 175
    cx, cy = W // 2, H // 2
    d = ImageDraw.Draw(cv)
    shadow(cv, (cx - r, cy - r, cx + r, cy + r), blur=20, alpha=90, radius=r)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=CREAM)
    d.ellipse((cx - r + 16, cy - r + 16, cx + r - 16, cy + r - 16), outline=MOCHA, width=2)
    logo(cv, cx, cy, 250, BROWN)
    return cv


def p06():  # 92 · abanico de tres fotos
    a, b, c, e = photo(92, 1), photo(92, 2), photo(92, 3), photo(92, 4)
    cv = Image.new("RGB", (W, H), (230, 233, 236))  # gris perla frio que acompana el denim claro
    def card(im, w, h, **k):
        cd = Image.new("RGB", (w + 28, h + 28), OFF)
        cd.paste(fit(im, w, h, **k), (14, 14))
        return cd
    paste_rot(cv, card(c, 430, 760), 270, 860, 13)
    paste_rot(cv, card(b, 430, 760), 810, 840, -13)
    paste_rot(cv, card(a, 520, 900, oy=-0.05), W // 2, 760, 0, alpha=0.45)
    put(cv, fit(e, 560, 380, oy=-0.35, zoom=1.05), (W - 560) // 2, 1300, sh=True)
    logo(cv, W // 2, 1790, 290, (70, 74, 82))
    return cv


def p07():  # 34 · triptico vertical a sangre con banda central para el logo
    ims = [photo(34, 1), photo(34, 3), photo(34, 4)]
    cv = Image.new("RGB", (W, H), CREAM)
    g = 8
    cw = (W - 2 * g) // 3
    top, bot = 0, 1500
    for i, im in enumerate(ims):
        cv.paste(fit(im, cw, bot - top, oy=-0.05), (i * (cw + g), top))
    # franja inferior con detalle panoramico (pantalon) y logo
    d = ImageDraw.Draw(cv)
    d.rectangle((0, bot, W, H), fill=CREAM)
    d.line((90, bot + 70, W - 90, bot + 70), fill=MOCHA, width=2)
    logo(cv, W // 2, bot + 215, 330, BROWN)
    d.line((90, H - 70, W - 90, H - 70), fill=MOCHA, width=2)
    return cv


def p08():  # 77 · pagina de lookbook: aire, una grande y dos chicas desalineadas
    a, b, c, e = photo(77, 1), photo(77, 2), photo(77, 3), photo(77, 4)
    cv = Image.new("RGB", (W, H), OFF)
    put(cv, fit(a, 620, 1180, oy=0.0), 80, 120)
    put(cv, fit(e, 300, 400, oy=-0.1, zoom=1.0), 720, 120)
    put(cv, fit(b, 300, 560, oy=0.1), 720, 560)
    put(cv, fit(c, 460, 470, oy=0.75, zoom=1.35), 540, 1340)
    d = ImageDraw.Draw(cv)
    d.line((80, 1360, 80, 1810), fill=BROWN, width=2)
    logo(cv, 300, 1590, 300, BROWN)
    return cv


def p09():  # 84 · escalera: tres fotos escalonadas en diagonal
    a, b, c = photo(84, 1), photo(84, 2), photo(84, 3)
    cv = Image.new("RGB", (W, H), TAUPE)
    pw, ph = 470, 700
    pos = [(60, 80), (305, 610), (550, 1140)]
    for (x, y), im, k in zip(pos, [a, c, b], [dict(oy=-0.3), dict(oy=-0.1), dict(oy=0.1)]):
        put(cv, fit(im, pw, ph, **k), x, y, sh=True)
    logo(cv, 790, 380, 300, OFF)
    return cv


def p10():  # 43 · mosaico 3x3 de recortes (cuerpo, espalda, detalle)
    a, b, c = photo(43, 1), photo(43, 2), photo(43, 3)
    cv = Image.new("RGB", (W, H), CREAM)
    m, g = 40, 14
    cw = (W - 2 * m - 2 * g) // 3
    chh = 520
    tiles = [
        (b, dict(oy=-0.6, zoom=1.6)), (b, dict(zoom=1.0)), (a, dict(oy=-0.55, zoom=1.7)),
        (c, dict(oy=-0.1, zoom=1.4)), (a, dict(oy=0.15, zoom=1.0)), (b, dict(oy=0.2, zoom=1.7)),
        (a, dict(oy=0.9, zoom=1.8)), (c, dict(zoom=1.0)), (b, dict(oy=0.95, zoom=1.9)),
    ]
    for i, (im, k) in enumerate(tiles):
        x = m + (i % 3) * (cw + g); y = m + (i // 3) * (chh + g)
        put(cv, fit(im, cw, chh, **k), x, y, radius=10)
    logo(cv, W // 2, m + 3 * chh + 2 * g + (H - (m + 3 * chh + 2 * g)) // 2, 300, BROWN)
    return cv


def p11():  # 16 · marco art deco de doble linea, foto grande + dos ventanitas
    a, b, c = photo(16, 1), photo(16, 2), photo(16, 3)
    cv = Image.new("RGB", (W, H), ESPRESSO)
    d = ImageDraw.Draw(cv)
    gold = (196, 168, 128)
    d.rectangle((40, 40, W - 41, H - 41), outline=gold, width=2)
    d.rectangle((56, 56, W - 57, H - 57), outline=gold, width=1)
    for (x, y) in [(40, 40), (W - 41, 40), (40, H - 41), (W - 41, H - 41)]:
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=gold)
    put(cv, fit(a, 640, 1460), 100, 100)
    d.rectangle((88, 88, 100 + 640 + 11, 100 + 1460 + 11), outline=gold, width=2)
    sw, sh_ = 250, 560
    put(cv, fit(b, sw, sh_, oy=-0.2, zoom=1.15), 770, 260)
    put(cv, fit(c, sw, sh_, oy=0.2, zoom=1.05), 770, 260 + sh_ + 40)
    d.rectangle((762, 252, 770 + sw + 7, 260 + sh_ + 7), outline=gold, width=1)
    d.rectangle((762, 260 + sh_ + 32, 770 + sw + 7, 260 + 2 * sh_ + 47), outline=gold, width=1)
    logo(cv, W // 2, 1730, 320, gold)
    return cv


def p12():  # 10 · mitades horizontales con banda crema y logo
    a, b, c = photo(10, 1), photo(10, 2), photo(10, 3)
    cv = Image.new("RGB", (W, H), CREAM)
    hh = 870
    cv.paste(fit(a, W, hh, oy=-0.45, zoom=1.0), (0, 0))
    cv.paste(fit(c, W, hh, oy=0.6, zoom=1.0), (0, H - hh))
    d = ImageDraw.Draw(cv)
    band_y = hh
    d.rectangle((0, band_y, W, H - hh), fill=CREAM)
    # ventanita redondeada que cruza la banda
    put(cv, fit(b, 250, 330, oy=-0.4, zoom=1.3), W - 90 - 250, band_y - 130, radius=20, sh=True)
    logo(cv, 330, H // 2, 300, BROWN)
    return cv


PIEZAS = [
    ("01_fotomaton_p08", p01), ("02_arcos_p24", p02), ("03_diagonal_p31", p03),
    ("04_lupa_detalle_p51", p04), ("05_cuadricula_sello_p80", p05), ("06_abanico_p92", p06),
    ("07_triptico_p34", p07), ("08_lookbook_p77", p08), ("09_escalera_p84", p09),
    ("10_mosaico_3x3_p43", p10), ("11_marco_deco_p16", p11), ("12_mitades_horizontales_p10", p12),
]

if __name__ == "__main__":
    only = sys.argv[1:]
    for name, fn in PIEZAS:
        if only and not any(o in name for o in only):
            continue
        fn().save(os.path.join(OUT, f"{name}.png"), optimize=True)
        print("ok", name)
