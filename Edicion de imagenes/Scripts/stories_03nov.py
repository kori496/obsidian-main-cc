# Stories V.YA 03 nov 2026 - 7 piezas 1080x1920, varias fotos por pieza, solo logo
# Prendas de la sesion 19 oct que no se habian editado: 97, 98, 101, 104, 105, 109, 110
import csv
from PIL import Image, ImageOps, ImageDraw, ImageFilter, ImageEnhance

W, H = 1080, 1920
OUT = "/home/claude/w/out"
CSV = "/mnt/user-data/uploads/vya contenido/assets/mapa_renombrado.csv"
FOT = "/mnt/user-data/uploads/vya contenido/fotos/192026 FOTOS ALMACEN/"
LOGO = "/mnt/user-data/uploads/obsidian-main-cc-main/obsidian-main-cc-main/Edicion de imagenes/logo_mask.png"
CREAM, SAND, CHOC, INK, LINE = (239, 233, 225), (226, 214, 198), (52, 41, 35), (60, 52, 46), (176, 150, 118)

rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
def fotos(g):
    out = []
    for x in rows:
        if x["grupo"] == g:
            im = ImageOps.exif_transpose(Image.open(FOT + x["nombre_original"])).convert("RGB")
            im = ImageEnhance.Contrast(im).enhance(1.05); im = ImageEnhance.Color(im).enhance(1.02)
            im = ImageEnhance.Sharpness(im).enhance(1.15)
            out.append(im)
    return out

def fit(im, w, h, fy=0.35, zoom=1.0, fx=0.5):
    s = max(w / im.width, h / im.height) * zoom
    r = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = int((r.width - w) * fx); y = int((r.height - h) * fy)
    return r.crop((x, y, x + w, y + h))

def shadow(c, box, rad=0, blur=22, op=60):
    sh = Image.new("L", c.size, 0); x0, y0, x1, y1 = box
    ImageDraw.Draw(sh).rounded_rectangle((x0 + 4, y0 + 12, x1 + 4, y1 + 12), rad, fill=op)
    c.paste(Image.new("RGB", c.size, (0, 0, 0)), (0, 0), sh.filter(ImageFilter.GaussianBlur(blur)))

def arch_mask(w, h):
    m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
    d.ellipse((0, 0, w - 1, w - 1), fill=255); d.rectangle((0, w // 2, w - 1, h - 1), fill=255)
    return m

def arch_line(c, box, color, width=3):
    x0, y0, x1, y1 = box; w = x1 - x0; d = ImageDraw.Draw(c)
    d.arc((x0, y0, x1, y0 + w), 180, 360, fill=color, width=width)
    d.line((x0, y0 + w // 2, x0, y1), fill=color, width=width)
    d.line((x1, y0 + w // 2, x1, y1), fill=color, width=width)

def rounded(w, h, rad):
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), rad, fill=255)
    return m

lm = Image.open(LOGO).convert("L")
def logo(c, w, color, cy, a=1.0, cx=None):
    m = lm.resize((w, round(lm.height * w / lm.width)), Image.LANCZOS).point(lambda v: int(v * a))
    x = (W - m.width) // 2 if cx is None else cx - m.width // 2
    c.paste(Image.new("RGB", m.size, color), (x, cy - m.height // 2), m)

def save(c, n):
    c.save(f"{OUT}/VYA_IA_story{n}.jpg", quality=94); print("ok", n)

# 1 - prenda 97 (top blanco botones dorados): zoom progresivo, de cuerpo entero al detalle
f = fotos("prenda_97"); c = Image.new("RGB", (W, H), CREAM); g = 14
c.paste(fit(f[0], W - 2 * g, 1060, 0.12), (g, g))
hw = (W - 3 * g) // 2; hh = 600
c.paste(fit(f[1], hw, hh, 0.35), (g, 1060 + 2 * g))
c.paste(fit(f[1], hw, hh, 0.42, 1.9, 0.48), (2 * g + hw, 1060 + 2 * g))   # botones dorados de cerca
logo(c, 220, INK, 1060 + 3 * g + hh + (H - (1060 + 3 * g + hh)) // 2)
save(c, "1_zoom_progresivo")

# 2 - prenda 98 (chaleco negro): triptico escalonado, tres columnas altas a distinta altura
f = fotos("prenda_98"); c = Image.new("RGB", (W, H), CREAM)
cw, gap = 316, 18; x0 = (W - 3 * cw - 2 * gap) // 2
for i, (im, fy, z, dy) in enumerate([(f[0], 0.12, 1.0, 170), (f[1], 0.2, 1.0, 70), (f[2], 0.12, 1.0, 230)]):
    x = x0 + i * (cw + gap); hh = 1420
    shadow(c, (x, dy, x + cw, dy + hh), 0, 16, 45)
    c.paste(fit(im, cw, hh, fy, z), (x, dy))
ImageDraw.Draw(c).line((x0, 1720, W - x0, 1720), fill=LINE, width=2)
logo(c, 210, INK, 1810)
save(c, "2_triptico_escalonado")

# 3 - prenda 101 (enterizo blanco halter): a sangre con marco fino que la tarjeta rompe
f = fotos("prenda_101"); c = fit(f[1], W, H, 0.3)
c = ImageEnhance.Brightness(c).enhance(1.02)
d = ImageDraw.Draw(c); d.rectangle((44, 44, W - 45, H - 45), outline=(255, 255, 255), width=3)
cw, ch = 400, 600; x, y = 80, 1180
shadow(c, (x - 12, y - 12, x + cw + 12, y + ch + 12), 0, 18, 70)
c.paste(Image.new("RGB", (cw + 24, ch + 24), (255, 255, 255)), (x - 12, y - 12))
c.paste(fit(f[2], cw, ch, 0.15, 1.05), (x, y))
logo(c, 210, (255, 255, 255), 150, 0.95, cx=W - 220)
save(c, "3_marco_roto")

# 4 - prenda 104 (jean barrel claro): arcos gemelos + franja del jean
f = fotos("prenda_104"); c = Image.new("RGB", (W, H), CREAM)
aw, ah, ay = 470, 1080, 110; x1, x2 = 50, W - 50 - aw
for x, im, fx in ((x1, f[0], 0.5), (x2, f[1], 0.5)):
    c.paste(fit(im, aw, ah, 0.1, 1.0, fx), (x, ay), arch_mask(aw, ah))
    arch_line(c, (x - 14, ay - 14, x + aw + 14, ay + ah + 14), LINE, 2)
bhh, by = 430, ay + ah + 60; bw = (W - 100 - 20) // 2
c.paste(fit(f[0], bw, bhh, 0.62, 1.9, 0.5), (50, by), rounded(bw, bhh, 8))      # el barrel de cerca
c.paste(fit(f[1], bw, bhh, 0.85, 1.9, 0.5), (70 + bw, by), rounded(bw, bhh, 8))
logo(c, 210, INK, by + bhh + (H - by - bhh) // 2)
save(c, "4_arcos_gemelos")

# 5 - prenda 105 (halter negro + culotte floral): tiras de distinto ancho, ritmo de lomo de libro
f = fotos("prenda_105"); c = Image.new("RGB", (W, H), SAND)
widths = [300, 140, 230, 120, 190]; gap = 10; x = (W - sum(widths) - gap * (len(widths) - 1)) // 2
plan = [(f[1], 0.12, 1.0, 0.5), (f[0], 0.4, 1.5, 0.5), (f[2], 0.15, 1.0, 0.5),
        (f[2], 0.8, 1.6, 0.5), (f[0], 0.15, 1.0, 0.5)]
tops = [100, 220, 140, 300, 180]
for wdt, t, (im, fy, z, fx) in zip(widths, tops, plan):
    hh = 1560 - (t - 100)
    c.paste(fit(im, wdt, hh, fy, z, fx), (x, t)); x += wdt + gap
logo(c, 220, CHOC, 1810)
save(c, "5_tiras_ritmo")

# 6 - prenda 109 (vestido denim largo): cuadricula 2x2 con una celda para el logo
f = fotos("prenda_109"); g = 14; c = Image.new("RGB", (W, H), CREAM)
cw, ch = (W - 3 * g) // 2, (H - 3 * g) // 2
c.paste(fit(f[0], cw, ch, 0.2), (g, g))
c.paste(fit(f[0], cw, ch, 0.3, 2.0, 0.5), (2 * g + cw, g))       # botones y textura del denim
c.paste(fit(f[1], cw, ch, 0.2), (2 * g + cw, 2 * g + ch))
c.paste(Image.new("RGB", (cw, ch), CHOC), (g, 2 * g + ch))
d = ImageDraw.Draw(c); d.rectangle((g + 40, 2 * g + ch + 40, g + cw - 41, 2 * g + 2 * ch - 41), outline=LINE, width=2)
logo(c, 280, CREAM, 2 * g + ch + ch // 2, cx=g + cw // 2)
save(c, "6_cuadricula_con_sello")

# 7 - prenda 110 (top vino tejido + pantalon rayas): arco grande con doble linea + dos tarjetas
f = fotos("prenda_110"); c = Image.new("RGB", (W, H), CHOC)
aw, ah, ax, ay = 760, 1300, (W - 760) // 2, 120
c.paste(fit(f[0], aw, ah, 0.15), (ax, ay), arch_mask(aw, ah))
arch_line(c, (ax - 22, ay - 22, ax + aw + 22, ay + ah + 22), LINE, 2)
for x, im, fy in ((90, f[1], 0.25), (W - 90 - 360, f[2], 0.2)):
    y = 1240
    shadow(c, (x, y, x + 360, y + 470), 10, 20, 110)
    c.paste(fit(im, 360, 470, fy), (x, y), rounded(360, 470, 10))
logo(c, 200, CREAM, 1820, 0.95)
save(c, "7_arco_y_tarjetas")
