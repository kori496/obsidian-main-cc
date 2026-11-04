"""V.YA · lote 26 oct · 12 stories 1080x1920, solo logo, formatos nuevos.
Fotos: originales de Drive (drive vya septiembre, sesiones 081826 / 090226 / 092426 / 100926)
renombradas a prenda_XX_YY segun mapa_renombrado.csv.
Logo: recortado de una pieza del lote 23 oct (231011.png) -> logo_mask.png
"""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
import os, sys, math, random

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src") + "/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
CREAM = (238, 231, 222)
CREAM2 = (245, 240, 233)
TAUPE = (214, 202, 188)
BROWN = (108, 72, 52)
ESPRESSO = (43, 33, 28)
WHITE = (255, 255, 255)
LOGO = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo_mask.png")).convert("L")


def logo(cv, cx, cy, width, color, shadow=False, rotate=0):
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
    im = Image.open(SRC + f"prenda_{n:02d}_{k:02d}.jpeg").convert("RGB")
    im = ImageOps.exif_transpose(im)
    im = ImageEnhance.Contrast(im).enhance(1.05)
    im = ImageEnhance.Color(im).enhance(1.03)
    im = ImageEnhance.Brightness(im).enhance(1.03)
    return im


def fit(im, w, h, ox=0.0, oy=0.0, zoom=1.0):
    """cover crop; ox/oy -1..1 desplazan el recorte; zoom>1 acerca"""
    s = max(w / im.width, h / im.height) * zoom
    nw, nh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    r = im.resize((nw, nh), Image.LANCZOS)
    ex, ey = nw - w, nh - h
    x = int(ex / 2 * (1 + ox)); y = int(ey / 2 * (1 + oy))
    out = r.crop((x, y, x + w, y + h))
    return out.filter(ImageFilter.UnsharpMask(radius=1.4, percent=55, threshold=2))


def rmask(w, h, r):
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
    return m


def shadow(cv, box, blur=22, alpha=80, off=(8, 14), radius=0):
    x0, y0, x1, y1 = box
    pad = blur * 3
    sh = Image.new("L", (x1 - x0 + 2 * pad, y1 - y0 + 2 * pad), 0)
    ImageDraw.Draw(sh).rounded_rectangle((pad, pad, pad + x1 - x0, pad + y1 - y0), radius, fill=alpha)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    cv.paste((0, 0, 0), (x0 - pad + off[0], y0 - pad + off[1]), sh)


def put(cv, im, x, y, radius=0, sh=False):
    if sh:
        shadow(cv, (x, y, x + im.width, y + im.height), radius=radius)
    if radius:
        cv.paste(im, (x, y), rmask(im.width, im.height, radius))
    else:
        cv.paste(im, (x, y))


def paste_rot(cv, im, cx, cy, angle, sh=True):
    """pega una imagen RGB rotada (con sombra) centrada en cx,cy"""
    a = Image.new("L", im.size, 255)
    r = im.rotate(angle, expand=True, resample=Image.BICUBIC)
    ra = a.rotate(angle, expand=True, resample=Image.BICUBIC)
    x, y = int(cx - r.width / 2), int(cy - r.height / 2)
    if sh:
        pad = 60
        s = Image.new("L", (r.width + 2 * pad, r.height + 2 * pad), 0)
        s.paste(ra.point(lambda v: int(v * 0.35)), (pad, pad))
        s = s.filter(ImageFilter.GaussianBlur(20))
        cv.paste((0, 0, 0), (x - pad + 8, y - pad + 16), s)
    cv.paste(r, (x, y), ra)


def ellipse_mask(w, h):
    m = Image.new("L", (w * 3, h * 3), 0)
    ImageDraw.Draw(m).ellipse((0, 0, w * 3 - 1, h * 3 - 1), fill=255)
    return m.resize((w, h), Image.LANCZOS)


# ---------------- 12 piezas ----------------

def p01():  # 82 · bento de 5 fotos con esquinas redondeadas
    ims = [photo(82, k) for k in range(1, 6)]
    cv = Image.new("RGB", (W, H), CREAM)
    g, m, r = 18, 44, 26
    cw = (W - 2 * m - g) // 2  # 487
    # columna izquierda: alta + baja ; derecha: baja + alta (escalonado)
    put(cv, fit(ims[0], cw, 1020, ox=-0.1), m, m, r)
    put(cv, fit(ims[4], cw, 560, oy=-0.6, zoom=1.0), m, m + 1020 + g, r)
    put(cv, fit(ims[2], cw, 640, oy=-0.3), m + cw + g, m, r)
    put(cv, fit(ims[3], cw, 450, oy=0.85, zoom=1.35), m + cw + g, m + 640 + g, r)
    put(cv, fit(ims[1], cw, 472, oy=0.95, zoom=1.6), m + cw + g, m + 640 + g + 450 + g, r)
    logo(cv, W // 2, 1790, 300, BROWN)
    return cv


def polaroid(im, w, h, side=26, bottom=110):
    card = Image.new("RGB", (w + 2 * side, h + side + bottom), (252, 250, 246))
    card.paste(fit(im, w, h), (side, side))
    return card


def p02():  # 83 · polaroids
    a, b, c = photo(83, 4), photo(83, 1), photo(83, 3)
    cv = Image.new("RGB", (W, H), CREAM)
    paste_rot(cv, polaroid(c, 400, 600), 760, 1300, -7)
    paste_rot(cv, polaroid(b, 380, 470, bottom=90), 300, 1430, 6)
    paste_rot(cv, polaroid(a, 580, 900), 480, 760, -2.5)
    logo(cv, W // 2, 1800, 290, BROWN)
    return cv


def p03():  # 50 · portada: foto a sangre + columna de 3 a la derecha + logo abajo
    ims = [photo(50, k) for k in range(1, 5)]
    cv = fit(ims[2], W, H, ox=-0.15)
    grad = Image.new("L", (1, H), 0)
    for y in range(H):
        v = int(min(1, max(0, (y - 1450) / 470)) ** 1.2 * 170)
        grad.putpixel((0, y), v)
    cv.paste((25, 18, 14), (0, 0), grad.resize((W, H)))
    tw, th, g = 250, 340, 22
    x = W - tw - 50
    for i, im in enumerate([ims[0], ims[1], ims[3]]):
        y = 90 + i * (th + g)
        put(cv, fit(im, tw, th, oy=-0.2), x, y, 12, sh=True)
        ImageDraw.Draw(cv).rounded_rectangle((x, y, x + tw - 1, y + th - 1), 12, outline=(244, 238, 230), width=3)
    logo(cv, W // 2, 1800, 360, WHITE, shadow=True)
    return cv


def p04():  # 17 · desglose: cuerpo entero + 3 detalles, fondo espresso
    a, b, c = photo(17, 1), photo(17, 2), photo(17, 3)
    cv = Image.new("RGB", (W, H), ESPRESSO)
    put(cv, fit(a, 600, 1560, ox=0.0), 60, 60)
    dw, dh, g = 340, 506, 21
    x = 60 + 600 + 20
    put(cv, fit(b, dw, dh, oy=-0.55, zoom=1.9, ox=0.0), x, 60)          # torso
    put(cv, fit(c, dw, dh, oy=0.15, zoom=1.9, ox=0.1), x, 60 + dh + g)  # cintura / caida
    put(cv, fit(b, dw, dh, oy=0.95, zoom=1.9), x, 60 + 2 * (dh + g))    # bota
    d = ImageDraw.Draw(cv)
    d.line((60, 1700, W - 60, 1700), fill=(150, 120, 96), width=2)
    logo(cv, W // 2, 1800, 300, CREAM)
    return cv


def p05():  # 23 · circulo grande + rectangulo de cuerpo entero
    a, b, c = photo(23, 1), photo(23, 2), photo(23, 3)
    cv = Image.new("RGB", (W, H), CREAM2)
    # rectangulo cuerpo entero a la izquierda
    put(cv, fit(a, 560, 1300), 70, 470, sh=True)
    # circulo grande arriba a la derecha (torso)
    r = 290
    cx, cy = 720, 430
    d = ImageDraw.Draw(cv)
    d.ellipse((cx - r - 12, cy - r - 12, cx + r + 12, cy + r + 12), fill=(252, 249, 244))
    cv.paste(fit(b, 2 * r, 2 * r, oy=-0.55, zoom=1.15), (cx - r, cy - r), ellipse_mask(2 * r, 2 * r))
    # foto media a la derecha abajo
    put(cv, fit(c, 360, 640, oy=0.35, zoom=1.2), 660, 1000, sh=True)
    logo(cv, 840, 1780, 260, BROWN)
    return cv


def tape(cv, cx, cy, w, h, angle):
    t = Image.new("RGBA", (w, h), (236, 226, 208, 170))
    d = ImageDraw.Draw(t)
    for x in range(0, w, 7):  # bordes dentados suaves
        d.rectangle((x, 0, x + 3, 2), fill=(0, 0, 0, 0))
        d.rectangle((x + 3, h - 3, x + 6, h), fill=(0, 0, 0, 0))
    t = t.rotate(angle, expand=True, resample=Image.BICUBIC)
    cv.paste(t, (int(cx - t.width / 2), int(cy - t.height / 2)), t)


def p06():  # 18 · collage con cintas
    a, b, c = photo(18, 1), photo(18, 2), photo(18, 4)
    cv = Image.new("RGB", (W, H), (233, 225, 214))
    paste_rot(cv, fit(a, 560, 900), 360, 600, 3)
    paste_rot(cv, fit(c, 470, 760), 760, 1130, -4)
    paste_rot(cv, fit(b, 430, 560, oy=0.3, zoom=1.1), 330, 1450, 2)
    tape(cv, 360, 160, 190, 52, -6)
    tape(cv, 800, 760, 170, 50, 8)
    tape(cv, 330, 1180, 170, 50, -4)
    logo(cv, 800, 1720, 270, BROWN)
    return cv


def p07():  # 28 · foto a sangre + banda lateral crema con 2 fotos
    a, b, c = photo(28, 1), photo(28, 2), photo(28, 3)
    cv = Image.new("RGB", (W, H), CREAM)
    cv.paste(fit(a, 740, H, ox=0.05), (0, 0))
    bx = 740 + 36
    bw = W - bx - 36  # 268
    put(cv, fit(b, bw, 560, ox=0.1, oy=-0.1, zoom=1.15), bx, 140)
    put(cv, fit(c, bw, 560, oy=0.6, zoom=1.25), bx, 140 + 560 + 26)
    logo(cv, bx + bw // 2, 1620, 230, BROWN, rotate=90)
    return cv


def p08():  # 78 · tarjeta blanca sobre fondo difuminado
    a, b, c = photo(78, 1), photo(78, 2), photo(78, 3)
    bg = fit(a, W, H).filter(ImageFilter.GaussianBlur(38))
    cv = ImageEnhance.Brightness(ImageEnhance.Color(bg).enhance(0.6)).enhance(0.92)
    cx0, cy0, cw, ch = 90, 150, 900, 1620
    shadow(cv, (cx0, cy0, cx0 + cw, cy0 + ch), blur=26, alpha=110, radius=34)
    cv.paste((251, 249, 245), (cx0, cy0), rmask(cw, ch, 34))
    p = 36
    put(cv, fit(a, cw - 2 * p, 980, oy=-0.1), cx0 + p, cy0 + p, 18)
    sw = (cw - 2 * p - 22) // 2
    put(cv, fit(b, sw, 420, oy=0.35, zoom=1.15), cx0 + p, cy0 + p + 980 + 22, 18)
    put(cv, fit(c, sw, 420, oy=0.2, zoom=1.1), cx0 + p + sw + 22, cy0 + p + 980 + 22, 18)
    logo(cv, W // 2, cy0 + ch - 70, 250, BROWN)
    return cv


def p09():  # 46 · ovalos tipo espejo
    a, b, c = photo(46, 1), photo(46, 2), photo(46, 3)
    cv = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(cv)
    ow, oh = 640, 1240
    ox, oy = 90, 190
    d.ellipse((ox + 26, oy + 26, ox + ow + 26, oy + oh + 26), outline=BROWN, width=3)
    cv.paste(fit(b, ow, oh), (ox, oy), ellipse_mask(ow, oh))
    sw, shh = 360, 560
    sx, sy = 640, 1150
    d.ellipse((sx - 12, sy - 12, sx + sw + 12, sy + shh + 12), fill=CREAM2)
    cv.paste(fit(a, sw, shh, oy=0.4, zoom=1.15), (sx, sy), ellipse_mask(sw, shh))
    logo(cv, 330, 1680, 280, BROWN)
    return cv


def mat_print(im, w, h, mat=46, line=True):
    card = Image.new("RGB", (w + 2 * mat, h + 2 * mat), (250, 247, 241))
    card.paste(fit(im, w, h), (mat, mat))
    if line:
        ImageDraw.Draw(card).rectangle((mat - 14, mat - 14, mat + w + 13, mat + h + 13), outline=(196, 178, 158), width=2)
    return card


def p10():  # 81 · laminas tipo galeria (passe-partout)
    a, b, c = photo(81, 1), photo(81, 2), photo(81, 3)
    cv = Image.new("RGB", (W, H), TAUPE)
    big = mat_print(c, 560, 1000)
    small = mat_print(a, 360, 520, mat=34)
    x1, y1 = 70, 110
    shadow(cv, (x1, y1, x1 + big.width, y1 + big.height), blur=22, alpha=90)
    cv.paste(big, (x1, y1))
    x2, y2 = 590, 980
    shadow(cv, (x2, y2, x2 + small.width, y2 + small.height), blur=22, alpha=90)
    cv.paste(small, (x2, y2))
    logo(cv, 330, 1720, 290, (92, 62, 45))
    return cv


def p11():  # 65 · dos mitades a sangre + circulo de detalle + banda con logo
    a, b, c = photo(65, 1), photo(65, 2), photo(65, 3)
    cv = Image.new("RGB", (W, H), CREAM)
    hh = 1640
    cv.paste(fit(b, 537, hh, ox=0.05), (0, 0))
    cv.paste(fit(c, 537, hh, ox=0.0), (543, 0))
    d = ImageDraw.Draw(cv)
    d.rectangle((537, 0, 542, hh), fill=CREAM)
    r = 150
    cx, cy = W // 2, 1300
    d.ellipse((cx - r - 10, cy - r - 10, cx + r + 10, cy + r + 10), fill=CREAM)
    cv.paste(fit(a, 2 * r, 2 * r, oy=0.75, zoom=1.0), (cx - r, cy - r), ellipse_mask(2 * r, 2 * r))
    logo(cv, W // 2, 1782, 290, BROWN)
    return cv


def p12():  # 55 · duo desfasado sobre taupe, logo en el hueco
    a, b, c = photo(55, 1), photo(55, 2), photo(55, 3)
    cv = Image.new("RGB", (W, H), (226, 216, 203))
    pw, ph = 470, 1560
    put(cv, fit(a, pw, ph, oy=-0.7), 50, 60, sh=True)
    put(cv, fit(c, pw, ph, ox=-0.1), W - 50 - pw, H - 60 - ph, sh=True)
    d = ImageDraw.Draw(cv)
    d.line((W - 50 - pw + 60, 245, W - 110, 245), fill=BROWN, width=2)
    logo(cv, W - 50 - pw // 2, 165, 270, BROWN)
    d.line((110, 1720, 50 + pw - 60, 1720), fill=BROWN, width=2)
    return cv


PIEZAS = [
    ("01_bento_p82", p01), ("02_polaroids_p83", p02), ("03_portada_p50", p03),
    ("04_desglose_p17", p04), ("05_circulo_p23", p05), ("06_cintas_p18", p06),
    ("07_banda_lateral_p28", p07), ("08_tarjeta_p78", p08), ("09_ovalos_p46", p09),
    ("10_laminas_p81", p10), ("11_mitades_circulo_p65", p11), ("12_duo_desfasado_p55", p12),
]

if __name__ == "__main__":
    only = sys.argv[1:]
    for name, fn in PIEZAS:
        if only and not any(o in name for o in only):
            continue
        fn().save(f"{OUT}/{name}.png", optimize=True)
        print("ok", name)
