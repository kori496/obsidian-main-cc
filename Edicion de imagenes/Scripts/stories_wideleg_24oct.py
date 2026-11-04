from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps, ImageChops
import numpy as np, os, json, sys

SRC = "/mnt/user-data/uploads/drive vya septiembre-20261017T013642Z-1-001/drive vya septiembre-20261017T013642Z-1-001/drive vya septiembre/agrupadas/"
REF = "/mnt/user-data/uploads/drive vya septiembre-20261017T013642Z-1-001/ediciones_vya_19oct/02_grid_crema_p77.png"
OUT = "/home/claude/vya/out"
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
CREAM = (238, 230, 220)
CREAM2 = (244, 239, 232)
BROWN = (110, 74, 52)
ESPRESSO = (44, 34, 30)
WHITE = (255, 255, 255)

# offsets de recorte horizontal por foto (-1..1), ajustados a mano tras revisar
OFFX = json.load(open("/home/claude/vya/offx.json")) if os.path.exists("/home/claude/vya/offx.json") else {}

# ---------- logo ----------
def build_logo():
    im = Image.open(REF).convert("RGB").crop((330, 1705, 750, 1830))
    a = np.asarray(im).astype(float)
    bg = np.array(CREAM, float)
    br = np.array([110, 74, 52], float)
    # alfa = cuánto se acerca al marrón respecto del fondo
    d = np.linalg.norm(a - bg, axis=2) / np.linalg.norm(br - bg)
    alpha = np.clip((d - 0.12) / 0.75, 0, 1)
    m = Image.fromarray((alpha * 255).astype("uint8"))
    bbox = m.point(lambda v: 255 if v > 40 else 0).getbbox()
    return m.crop(bbox)

LOGO = build_logo()

def logo(canvas, cx, cy, width, color, shadow=False):
    m = LOGO.resize((width, int(LOGO.height * width / LOGO.width)), Image.LANCZOS)
    if shadow:
        pad = 40
        sm = Image.new("L", (m.width + 2 * pad, m.height + 2 * pad), 0)
        sm.paste(m, (pad, pad))
        sm = sm.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.55))
        canvas.paste((20, 15, 12), (int(cx - m.width / 2) - pad + 2, int(cy - m.height / 2) - pad + 4), sm)
    layer = Image.new("RGB", m.size, color)
    canvas.paste(layer, (int(cx - m.width / 2), int(cy - m.height / 2)), m)

# ---------- fotos ----------
def photo(name):
    im = Image.open(SRC + name).convert("RGB")
    im = ImageOps.exif_transpose(im)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Color(im).enhance(1.04)
    im = ImageEnhance.Brightness(im).enhance(1.03)
    return im

def fit(im, w, h, offx=0.0, offy=0.0, key=None):
    """recorte tipo cover; offx/offy en -1..1"""
    if key and key in OFFX:
        offx = OFFX[key]
    s = max(w / im.width, h / im.height)
    nw, nh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    r = im.resize((nw, nh), Image.LANCZOS)
    ex, ey = nw - w, nh - h
    x = int(ex / 2 * (1 + offx)); y = int(ey / 2 * (1 + offy))
    out = r.crop((x, y, x + w, y + h))
    return out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))

def P(n, k):
    return f"prenda_{n:02d}_{k:02d}.jpeg"

def put(canvas, im, x, y, border=0, bcol=WHITE, shadow=False, radius=0):
    if shadow:
        sh = Image.new("L", (im.width + 2 * border + 60, im.height + 2 * border + 60), 0)
        ImageDraw.Draw(sh).rectangle((30, 30, sh.width - 30, sh.height - 30), fill=90)
        sh = sh.filter(ImageFilter.GaussianBlur(18))
        canvas.paste((0, 0, 0), (x - border - 30 + 6, y - border - 30 + 12), sh)
    if border:
        ImageDraw.Draw(canvas).rectangle((x - border, y - border, x + im.width + border - 1, y + im.height + border - 1), fill=bcol)
    if radius:
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius, fill=255)
        canvas.paste(im, (x, y), m)
    else:
        canvas.paste(im, (x, y))

def blurred_bg(im, amount=40, darken=0.85, bw=False):
    b = fit(im, W, H).filter(ImageFilter.GaussianBlur(amount))
    if bw:
        b = ImageOps.grayscale(b).convert("RGB")
    return ImageEnhance.Brightness(b).enhance(darken)

def arch_mask(w, h):
    m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
    d.ellipse((0, 0, w - 1, w - 1), fill=255)
    d.rectangle((0, w // 2, w - 1, h - 1), fill=255)
    return m

def circle(canvas, im, cx, cy, r, ring=8, col=WHITE):
    c = fit(im, 2 * r, 2 * r, key=None)
    ImageDraw.Draw(canvas).ellipse((cx - r - ring, cy - r - ring, cx + r + ring, cy + r + ring), fill=col)
    m = Image.new("L", (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
    canvas.paste(c, (cx - r, cy - r), m)

def lines_logo(canvas, cy, color, width=300):
    logo(canvas, W // 2, cy, width, color)
    d = ImageDraw.Draw(canvas)
    d.line((90, cy, W // 2 - width // 2 - 40, cy), fill=color, width=2)
    d.line((W // 2 + width // 2 + 40, cy, W - 90, cy), fill=color, width=2)

# ---------- 12 piezas ----------
def p01():  # 49 · a sangre + 2 insets a la izquierda
    a, b, c = photo(P(49, 1)), photo(P(49, 2)), photo(P(49, 3))
    cv = fit(a, W, H, key="49_1")
    for i, im in enumerate([b, c]):
        put(cv, fit(im, 270, 400, key=f"49_{i+2}"), 60, 520 + i * 460, border=8, shadow=True)
    logo(cv, W // 2, 1790, 330, WHITE, shadow=True)
    return cv

def p02():  # 25 · crema: foto grande + tira de 3
    ims = [photo(P(25, k)) for k in range(1, 5)]
    cv = Image.new("RGB", (W, H), CREAM)
    put(cv, fit(ims[0], 960, 1050, key="25_1"), 60, 60)
    for i in range(3):
        put(cv, fit(ims[i + 1], 304, 540, key=f"25_{i+2}"), 60 + i * 324, 1130)
    logo(cv, W // 2, 1800, 300, BROWN)
    return cv

def p03():  # 09 · fondo difuminado + 2 recuadros escalonados
    a, b = photo(P(9, 1)), photo(P(9, 2))
    cv = blurred_bg(a, 45, 0.9)
    put(cv, fit(a, 560, 820, key="9_1"), 80, 300, border=12, shadow=True)
    put(cv, fit(b, 520, 760, key="9_2"), 470, 960, border=12, shadow=True)
    logo(cv, W // 2, 150, 330, WHITE, shadow=True)
    return cv

def p04():  # 64 · a sangre + 1 inset grande a la derecha
    a, b = photo(P(64, 1)), photo(P(64, 2))
    cv = fit(a, W, H, key="64_1")
    put(cv, fit(b, 360, 560, key="64_2"), 660, 1080, border=10, shadow=True)
    logo(cv, 300, 1800, 300, WHITE, shadow=True)
    return cv

def p05():  # 11 · crema: 3 tiras verticales
    ims = [photo(P(11, k)) for k in range(1, 4)]
    cv = Image.new("RGB", (W, H), CREAM2)
    for i in range(3):
        put(cv, fit(ims[i], 312, 1520, key=f"11_{i+1}"), 54 + i * 330, 70)
    logo(cv, W // 2, 1770, 320, BROWN)
    return cv

def p06():  # 72 · espresso: 3 tiras a distinta altura
    ims = [photo(P(72, k)) for k in range(1, 4)]
    cv = Image.new("RGB", (W, H), ESPRESSO)
    tops = [140, 260, 140]
    for i in range(3):
        put(cv, fit(ims[i], 300, 1300, key=f"72_{i+1}"), 60 + i * 340, tops[i])
    logo(cv, W // 2, 1760, 330, CREAM)
    return cv

def p07():  # 87 · crema: arco + 2 círculos
    ims = [photo(P(87, k)) for k in range(1, 4)]
    cv = Image.new("RGB", (W, H), CREAM)
    aw, ah = 700, 1380
    ax, ay = (W - aw) // 2, 140
    d = ImageDraw.Draw(cv)
    m = arch_mask(aw + 24, ah + 24)
    cv.paste((250, 247, 242), (ax - 12, ay - 12), m)
    cv.paste(fit(ims[0], aw, ah, key="87_1"), (ax, ay), arch_mask(aw, ah))
    circle(cv, ims[1], 190, 1440, 125)
    circle(cv, ims[2], 890, 1440, 125)
    logo(cv, W // 2, 1760, 280, BROWN)
    return cv

def p08():  # 68 · difuminado: arco + 1 círculo
    a, b = photo(P(68, 1)), photo(P(68, 2))
    cv = blurred_bg(a, 50, 0.8)
    aw, ah = 760, 1400
    ax, ay = (W - aw) // 2, 170
    cv.paste(WHITE, (ax - 10, ay - 10), arch_mask(aw + 20, ah + 20))
    cv.paste(fit(a, aw, ah, key="68_1"), (ax, ay), arch_mask(aw, ah))
    circle(cv, b, 850, 1430, 150, ring=10)
    logo(cv, W // 2, 1790, 320, WHITE, shadow=True)
    return cv

def p09():  # 30 · crema: 2 fotos lado a lado + logo con líneas
    a, b = photo(P(30, 1)), photo(P(30, 2))
    cv = Image.new("RGB", (W, H), CREAM2)
    put(cv, fit(a, 470, 1540, key="30_1"), 60, 70)
    put(cv, fit(b, 470, 1540, key="30_2"), 550, 70)
    lines_logo(cv, 1775, BROWN, 300)
    return cv

def p10():  # 93 · espresso: foto grande con marco fino + 3 abajo
    ims = [photo(P(93, k)) for k in range(1, 5)]
    cv = Image.new("RGB", (W, H), ESPRESSO)
    d = ImageDraw.Draw(cv)
    d.rectangle((40, 40, W - 41, H - 41), outline=(150, 120, 95), width=2)
    put(cv, fit(ims[0], 920, 1060, key="93_1"), 80, 80)
    for i in range(3):
        put(cv, fit(ims[i + 1], 293, 440, key=f"93_{i+2}"), 80 + i * 313, 1170)
    logo(cv, W // 2, 1760, 320, CREAM)
    return cv

def p11():  # 66 · crema: grande a la izquierda + columna de 2
    ims = [photo(P(66, k)) for k in range(1, 4)]
    cv = Image.new("RGB", (W, H), CREAM)
    put(cv, fit(ims[0], 620, 1500, key="66_1"), 50, 260)
    put(cv, fit(ims[1], 340, 735, key="66_2"), 690, 260)
    put(cv, fit(ims[2], 340, 735, key="66_3"), 690, 1025)
    logo(cv, W // 2, 140, 300, BROWN)
    return cv

def p12():  # 20 · fondo B/N + foto a color con marco + inset
    a, b = photo(P(20, 1)), photo(P(20, 2))
    cv = ImageEnhance.Brightness(ImageOps.grayscale(fit(b, W, H, key="20_2").filter(ImageFilter.GaussianBlur(10))).convert("RGB")).enhance(0.72)
    put(cv, fit(a, 700, 1160, key="20_1"), 190, 330, border=14, shadow=True)
    logo(cv, W // 2, 170, 330, WHITE, shadow=True)
    return cv

PIEZAS = [
    ("01_insets_p49", p01), ("02_grande_tira_p25", p02), ("03_difuminado_p09", p03),
    ("04_sangre_inset_p64", p04), ("05_tiras_crema_p11", p05), ("06_tiras_espresso_p72", p06),
    ("07_arco_circulos_p87", p07), ("08_arco_difuminado_p68", p08), ("09_duo_crema_p30", p09),
    ("10_marco_espresso_p93", p10), ("11_columna_p66", p11), ("12_bn_color_p20", p12),
]

if __name__ == "__main__":
    only = sys.argv[1:]
    for name, fn in PIEZAS:
        if only and not any(o in name for o in only):
            continue
        fn().save(f"{OUT}/{name}.png", optimize=True)
        print("ok", name)
