"""V.YA · lote 30 oct · 12 stories 1080x1920, solo logo.
Fotos: sesion 19 oct (Documents\\almacen fotos\\192026 FOTOS ALMACEN), renombradas
prenda_XX_YY segun mapa_renombrado.csv -> src/prenda_XX_YY.jpg
Prendas: 95, 96, 99, 100, 102, 103, 106, 108, 111, 114, 115, 118.
12 formatos nuevos (distintos de los lotes 24, 26, 28 y 29 oct).
Logo: logo_mask.png (V.YA FASHION) y 'vya logo vertical.png' de Documents\\assets.
Uso: python stories_30oct.py [filtro]
"""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "src")
OUT = os.path.join(BASE, "out")
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
CREAM = (238, 231, 222)
OFF = (250, 247, 242)
SAND = (224, 212, 196)
PEARL = (228, 230, 232)
BUTTER = (243, 236, 214)
CHOC = (46, 32, 27)
BROWN = (96, 66, 50)
MOCHA = (146, 116, 92)
INK = (28, 33, 44)
WHITE = (255, 255, 255)
LOGO = Image.open(os.path.join(BASE, "logo_mask.png")).convert("L")
_v = Image.open(os.path.join(BASE, "vya logo vertical.png")).convert("RGBA")
LOGO_V = _v.split()[3]


def logo(cv, color, cx=W // 2, cy=1800, width=230, mask=None):
    mk = LOGO if mask is None else mask
    m = mk.resize((width, int(mk.height * width / mk.width)), Image.LANCZOS)
    cv.paste(Image.new("RGB", m.size, color), (int(cx - m.width / 2), int(cy - m.height / 2)), m)


def photo(n):
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, f"prenda_{n}.jpg"))).convert("RGB")
    im = ImageEnhance.Contrast(im).enhance(1.05)
    im = ImageEnhance.Color(im).enhance(1.02)
    return ImageEnhance.Brightness(im).enhance(1.02)


def fit(im, w, h, ox=0.0, oy=0.0, zoom=1.0):
    s = max(w / im.width, h / im.height) * zoom
    nw, nh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    r = im.resize((nw, nh), Image.LANCZOS)
    ex, ey = nw - w, nh - h
    x = int(ex / 2 * (1 + ox)); y = int(ey / 2 * (1 + oy))
    return r.crop((x, y, x + w, y + h)).filter(ImageFilter.UnsharpMask(radius=1.3, percent=55, threshold=2))


def rmask(w, h, r):
    m = Image.new("L", (w * 2, h * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * 2 - 1, h * 2 - 1), r * 2, fill=255)
    return m.resize((w, h), Image.LANCZOS)


def shadow(cv, box, blur=24, alpha=70, off=(6, 14), radius=0):
    x0, y0, x1, y1 = box
    pad = blur * 3
    sh = Image.new("L", (x1 - x0 + 2 * pad, y1 - y0 + 2 * pad), 0)
    ImageDraw.Draw(sh).rounded_rectangle((pad, pad, pad + x1 - x0, pad + y1 - y0), radius, fill=alpha)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    cv.paste((30, 22, 18), (x0 - pad + off[0], y0 - pad + off[1]), sh)


def put(cv, im, x, y, radius=0, sh=False, border=0, bcol=WHITE):
    if border:
        bw, bh = im.width + 2 * border, im.height + 2 * border
        if sh:
            shadow(cv, (x - border, y - border, x - border + bw, y - border + bh), radius=radius)
        b = Image.new("RGB", (bw, bh), bcol)
        cv.paste(b, (x - border, y - border), rmask(bw, bh, radius) if radius else None)
        radius = max(0, radius - border)
    elif sh:
        shadow(cv, (x, y, x + im.width, y + im.height), radius=radius)
    cv.paste(im, (x, y), rmask(im.width, im.height, radius) if radius else None)


def line(cv, xy, col, w=2):
    ImageDraw.Draw(cv).line(xy, fill=col, width=w)


def save(cv, name):
    cv.save(os.path.join(OUT, name), quality=95)


# ---------------- 12 piezas ----------------

def p01():  # 95 · columna doble asimetrica: alta a la izquierda, dos apiladas a la derecha
    cv = Image.new("RGB", (W, H), BUTTER)
    g = 22
    lw = 620
    put(cv, fit(photo("95_02"), lw, H - 2 * 60, oy=0.1), 0, 60)
    rw = W - lw - g
    h1 = 760
    put(cv, fit(photo("95_03"), rw, h1, oy=-0.6), lw + g, 60)
    put(cv, fit(photo("95_04"), rw, H - 60 - h1 - g - 240, oy=0.2, zoom=1.15), lw + g, 60 + h1 + g)
    logo(cv, BROWN, cx=lw + g + rw // 2, cy=H - 60 - 120, width=300 if rw > 400 else 330)
    save(cv, "01_p95_columna_doble.jpg")


def p02():  # 96 · lamina de galeria con paspartu y dos detalles tipo sello en esquinas
    cv = Image.new("RGB", (W, H), PEARL)
    mw, mh = 820, 1300
    x, y = (W - mw) // 2, 190
    put(cv, fit(photo("96_02"), mw, mh, oy=0.0), x, y, border=34, bcol=WHITE, sh=True)
    d1 = fit(photo("96_03"), 300, 300, oy=-0.12, zoom=2.0, ox=-0.05)
    put(cv, d1, x - 70, y + mh - 260, border=14, sh=True)
    d2 = fit(photo("96_04"), 300, 420, oy=0.4, zoom=1.0)
    put(cv, d2, x + mw - 230, y + mh - 120, border=14, sh=True)
    logo(cv, INK, cy=1810)
    save(cv, "02_p96_galeria_sellos.jpg")


def p03():  # 99 · zigzag: tres fotos alternadas izquierda-derecha con lineas guia
    cv = Image.new("RGB", (W, H), CREAM)
    pw, ph = 560, 560
    ys = [70, 640, 1210]
    xs = [70, W - 70 - pw, 70]
    names = [("99_01", 0, -0.35, 1.0), ("99_03", 0, 0.2, 1.0), ("99_04", 0, -0.2, 1.0)]
    for (n, ox, oy, z), x, y in zip(names, xs, ys):
        put(cv, fit(photo(n), pw, ph, ox=ox, oy=oy, zoom=z), x, y, radius=4)
    # lineas finas que enlazan
    line(cv, (70 + pw + 30, ys[0] + ph // 2, W - 70, ys[0] + ph // 2), MOCHA)
    line(cv, (70, ys[1] + ph // 2, W - 70 - pw - 30, ys[1] + ph // 2), MOCHA)
    # detalle de lunares en el hueco derecho inferior
    det = fit(photo("99_02"), 300, 470, oy=0.55, zoom=1.7)
    put(cv, det, W - 70 - 300, ys[2] + 20, radius=150)
    logo(cv, BROWN, cx=70 + pw + (W - 70 - pw) // 2 + 10, cy=ys[2] + ph + 70, width=210)
    save(cv, "03_p99_zigzag.jpg")


def p04():  # 100 · foto a sangre + columna de detalle de las rayas a la derecha
    cv = fit(photo("100_01"), W, H, ox=-0.2)
    cw, ch = 300, 980
    x, y = W - cw - 60, 300
    det = fit(photo("100_02"), cw, ch, oy=0.55, zoom=1.35)
    put(cv, det, x, y, border=10, sh=True)
    # degradado inferior suave para el logo
    gr = Image.new("L", (1, 360))
    for i in range(360):
        gr.putpixel((0, i), int(140 * (i / 359) ** 1.6))
    cv.paste((20, 24, 32), (0, H - 360), gr.resize((W, 360)))
    logo(cv, WHITE, cy=1810)
    save(cv, "04_p100_columna_detalle.jpg")


def p05():  # 102 · detalle a sangre arriba + dos cuerpos en tarjetas redondeadas que suben sobre la foto
    cv = Image.new("RGB", (W, H), SAND)
    top = fit(photo("102_03"), W, 900, oy=-0.1)
    cv.paste(top, (0, 0))
    cw, chh = 450, 820
    put(cv, fit(photo("102_01"), cw, chh, oy=0.15), 60, 720, radius=28, sh=True, border=10)
    put(cv, fit(photo("102_02"), cw, chh, oy=0.15), W - 60 - cw, 780, radius=28, sh=True, border=10)
    logo(cv, BROWN, cy=1790)
    save(cv, "05_p102_detalle_tarjetas.jpg")


def p06():  # 103 · trio centrado: panel central grande adelante, laterales detras
    cv = Image.new("RGB", (W, H), (226, 231, 238))
    sw, shh = 340, 1000
    put(cv, fit(photo("103_01"), sw, shh, oy=0.1), 40, 420, radius=18)
    put(cv, fit(photo("103_03"), sw, shh, oy=0.1), W - 40 - sw, 420, radius=18)
    mw, mh = 560, 1300
    put(cv, fit(photo("103_02"), mw, mh, oy=0.05), (W - mw) // 2, 230, radius=22, sh=True, border=12)
    logo(cv, INK, cy=1760)
    save(cv, "06_p103_trio_centrado.jpg")


def p07():  # 106 · editorial oscuro: una grande + tres chicas en columna
    cv = Image.new("RGB", (W, H), CHOC)
    m = 56
    bw = 640
    put(cv, fit(photo("106_01"), bw, 1560, oy=0.05), m, m + 40)
    sw = W - bw - 2 * m - 24
    shh = (1560 - 2 * 24) // 3
    for i, (n, oy, z) in enumerate([("106_03", -0.2, 1.0), ("106_04", 0.0, 1.0), ("106_02", 0.35, 1.25)]):
        put(cv, fit(photo(n), sw, shh, oy=oy, zoom=z), m + bw + 24, m + 40 + i * (shh + 24))
    line(cv, (m, 1720, W - m, 1720), (120, 96, 80), 1)
    logo(cv, CREAM, cy=1810, width=240)
    save(cv, "07_p106_editorial_oscuro.jpg")


def p08():  # 108 · frente y espalda 50/50 con pestana central para el logo
    cv = Image.new("RGB", (W, H), OFF)
    g = 14
    hw = (W - g) // 2
    cv.paste(fit(photo("108_03"), hw, H, oy=0.0), (0, 0))
    cv.paste(fit(photo("108_02"), hw, H, oy=0.0), (hw + g, 0))
    tw, th = 300, 110
    tab = Image.new("RGB", (tw, th), OFF)
    put(cv, tab, (W - tw) // 2, H - th - 90, radius=55, sh=True)
    logo(cv, BROWN, cy=H - 90 - th // 2, width=210)
    save(cv, "08_p108_frente_espalda.jpg")


def p09():  # 111 · dos fotos de alto completo con banda central y logo vertical
    cv = Image.new("RGB", (W, H), PEARL)
    band = 150
    pw = (W - band) // 2
    cv.paste(fit(photo("111_01"), pw, H, oy=0.0, ox=-0.1), (0, 0))
    cv.paste(fit(photo("111_02"), pw, H, oy=0.0), (pw + band, 0))
    logo(cv, (60, 66, 78), cx=W // 2, cy=H // 2, width=96, mask=LOGO_V)
    line(cv, (W // 2, 230, W // 2, H // 2 - 200), (150, 154, 160), 1)
    line(cv, (W // 2, H // 2 + 200, W // 2, H - 230), (150, 154, 160), 1)
    save(cv, "09_p111_banda_vertical.jpg")


def p10():  # 114 · portada con esquinas guia + dos miniaturas en la base
    cv = fit(photo("114_01"), W, H, oy=0.0)
    # esquinas tipo visor
    d = ImageDraw.Draw(cv)
    m, L = 60, 90
    for (x, y, sx, sy) in [(m, m, 1, 1), (W - m, m, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)]:
        d.line((x, y, x + sx * L, y), fill=WHITE, width=4)
        d.line((x, y, x, y + sy * L), fill=WHITE, width=4)
    tw, th = 250, 360
    put(cv, fit(photo("114_02"), tw, th, oy=0.45, zoom=1.5), 110, H - th - 260, border=8, sh=True)
    put(cv, fit(photo("114_03"), tw, th, oy=0.1), W - 110 - tw, H - th - 260, border=8, sh=True)
    gr = Image.new("L", (1, 300))
    for i in range(300):
        gr.putpixel((0, i), int(150 * (i / 299) ** 1.5))
    cv.paste((20, 24, 32), (0, H - 300), gr.resize((W, 300)))
    logo(cv, WHITE, cy=H - 150, width=230)
    save(cv, "10_p114_portada_visor.jpg")


def p11():  # 115 · franja ancha arriba (detalle) + dos cuerpos abajo, aire crema
    cv = Image.new("RGB", (W, H), OFF)
    m, g = 50, 20
    cv.paste(fit(photo("115_03"), W - 2 * m, 700, oy=0.15), (m, m))
    bw = (W - 2 * m - g) // 2
    bh = 920
    cv.paste(fit(photo("115_01"), bw, bh, oy=0.1), (m, m + 700 + g))
    cv.paste(fit(photo("115_02"), bw, bh, oy=0.1), (m + bw + g, m + 700 + g))
    logo(cv, (70, 92, 118), cy=m + 700 + g + bh + (H - (m + 700 + g + bh)) // 2, width=230)
    save(cv, "11_p115_franja_y_dos.jpg")


def p12():  # 118 · piramide: una arriba centrada, dos abajo, fondo arena
    cv = Image.new("RGB", (W, H), SAND)
    tw, th = 600, 860
    top = fit(photo("118_02"), tw, th, oy=0.0)
    cv.paste(top, ((W - tw) // 2, 80), rmask(tw, th, 300))  # arco: redondo arriba
    cv.paste(top.crop((0, th // 2, tw, th)), ((W - tw) // 2, 80 + th // 2))
    bw, bh = 450, 700
    put(cv, fit(photo("118_01"), bw, bh, oy=0.1), 70, 990, radius=10, sh=True)
    put(cv, fit(photo("118_03"), bw, bh, oy=0.1), W - 70 - bw, 990, radius=10, sh=True)
    logo(cv, BROWN, cy=1805)
    save(cv, "12_p118_piramide.jpg")


if __name__ == "__main__":
    f = sys.argv[1] if len(sys.argv) > 1 else ""
    for fn in [p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12]:
        if f in fn.__name__:
            fn()
            print("ok", fn.__name__)
