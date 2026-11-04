# Stories V.YA 31 oct 2026 - 7 piezas 1080x1920, varias fotos por pieza, solo logo
import csv
from PIL import Image, ImageOps, ImageDraw, ImageFilter, ImageEnhance

W, H = 1080, 1920
OUT = "/home/claude/w/out"
CSV = "/mnt/user-data/attachments/78940575-13db-5e7b-8377-a4336b998e77/90e42cc7-mapa_renombrado.csv"
FOT = "/mnt/user-data/uploads/vya contenido/fotos/"
LOGO = "/mnt/user-data/uploads/obsidian-main-cc-main/obsidian-main-cc-main/Edicion de imagenes/logo_mask.png"
CREAM, SAND, CHOC, INK = (239, 233, 225), (222, 208, 189), (52, 41, 35), (60, 52, 46)

rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
def fotos(g):
    out = []
    for x in rows:
        if x["grupo"] == g:
            im = ImageOps.exif_transpose(Image.open(FOT + x["carpeta_origen"] + "/" + x["nombre_original"])).convert("RGB")
            # mismo tono calido-neutro de las ediciones anteriores
            im = ImageEnhance.Contrast(im).enhance(1.04); im = ImageEnhance.Color(im).enhance(1.03)
            out.append(im)
    return out

def fit(im, w, h, fy=0.35, zoom=1.0, fx=0.5):
    """Recorta a w x h; fy/fx = punto de interes (0 arriba/izq, 1 abajo/der)."""
    s = max(w / im.width, h / im.height) * zoom
    r = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = int((r.width - w) * fx); y = int((r.height - h) * fy)
    return r.crop((x, y, x + w, y + h))

def rounded(im, rad):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), rad, fill=255)
    return im, m

def shadow(canvas, box, rad=0, blur=22, op=70):
    sh = Image.new("L", canvas.size, 0)
    x0, y0, x1, y1 = box
    ImageDraw.Draw(sh).rounded_rectangle((x0 + 6, y0 + 14, x1 + 6, y1 + 14), rad, fill=op)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    canvas.paste(Image.new("RGB", canvas.size, (0, 0, 0)), (0, 0), sh)

lm = Image.open(LOGO).convert("L")
def logo(canvas, w, color, cy, a=1.0, cx=None):
    m = lm.resize((w, round(lm.height * w / lm.width)), Image.LANCZOS).point(lambda v: int(v * a))
    x = (W - m.width) // 2 if cx is None else cx - m.width // 2
    canvas.paste(Image.new("RGB", m.size, color), (x, cy - m.height // 2), m)

def save(c, n):
    c.save(f"{OUT}/VYA_story{n}.jpg", quality=94); print("ok", n)

# 1 - prenda 35 (top encaje blanco): foto principal a sangre + fila de 4 miniaturas sobre crema
f = fotos("prenda_35"); c = Image.new("RGB", (W, H), CREAM)
c.paste(fit(f[3], W, 1380, 0.2), (0, 0))
tw = (W - 5 * 14) // 4
for i, im in enumerate([f[0], f[1], f[2], f[4]]):
    c.paste(fit(im, tw, 330, 0.25), (14 + i * (tw + 14), 1380 + 14))
logo(c, 230, INK, 1380 + 14 + 330 + (H - 1380 - 344) // 2)
save(c, "1_contactos_bajo_portada")

# 2 - prenda 58 (top lunares): capas superpuestas con sombra suave
f = fotos("prenda_58"); c = Image.new("RGB", (W, H), CREAM)
b1 = (90, 120, 90 + 640, 120 + 1000)
shadow(c, b1); c.paste(fit(f[0], 640, 1000, 0.2), b1[:2])
b2 = (430, 760, 430 + 560, 760 + 880)
c.paste(Image.new("RGB", (580, 900), (255, 255, 255)), (420, 750)); shadow(c, (420, 750, 1000, 1650))
c.paste(Image.new("RGB", (580, 900), (255, 255, 255)), (420, 750)); c.paste(fit(f[3], 560, 880, 0.3), b2[:2])
c.paste(Image.new("RGB", (330, 470), (255, 255, 255)), (110, 1180));
shadow(c, (110, 1180, 440, 1650), blur=16, op=60)
c.paste(Image.new("RGB", (330, 470), (255, 255, 255)), (110, 1180)); c.paste(fit(f[2], 310, 450, 0.25), (120, 1190))
logo(c, 210, INK, 1790)
save(c, "2_capas_superpuestas")

# 3 - prenda 75 (set rayas vino): composicion en L
f = fotos("prenda_75"); g = 12; c = Image.new("RGB", (W, H), CREAM)
bw, bh = 700, 1240
c.paste(fit(f[3], bw, bh, 0.15), (g, g))
rw = W - bw - 3 * g
c.paste(fit(f[0], rw, (bh - g) // 2, 0.3), (bw + 2 * g, g))
c.paste(fit(f[1], rw, (bh - g) // 2, 0.3), (bw + 2 * g, g + (bh - g) // 2 + g))
c.paste(fit(f[2], bw, H - bh - 3 * g, 0.42), (g, bh + 2 * g))
logo(c, 200, INK, bh + 2 * g + (H - bh - 3 * g) // 2, cx=bw + 2 * g + rw // 2)
save(c, "3_composicion_en_L")

# 4 - prenda 79 (chaleco blanco): fondo desenfocado de la misma prenda + 3 tarjetas
f = fotos("prenda_79")
bg = fit(f[1], W, H, 0.3).filter(ImageFilter.GaussianBlur(38))
c = Image.blend(bg, Image.new("RGB", (W, H), CREAM), 0.35)
cw, ch = 620, 860
shadow(c, (230, 110, 230 + cw, 110 + ch), 18); im, m = rounded(fit(f[0], cw, ch, 0.15), 18); c.paste(im, (230, 110), m)
sw, sh_ = 470, 700
shadow(c, (60, 1010, 60 + sw, 1010 + sh_), 18); im, m = rounded(fit(f[2], sw, sh_, 0.3), 18); c.paste(im, (60, 1010), m)
shadow(c, (550, 1010, 550 + sw, 1010 + sh_), 18); im, m = rounded(fit(f[3], sw, sh_, 0.3), 18); c.paste(im, (550, 1010), m)
logo(c, 210, INK, 1820, 0.9)
save(c, "4_fondo_desenfocado")

# 5 - prenda 86 (set camel): cascada diagonal sobre arena
f = fotos("prenda_86"); c = Image.new("RGB", (W, H), SAND)
pos = [(70, 80), (430, 640), (70, 1150)]
for (x, y), im, fy in zip(pos, [f[1], f[0], f[2]], [0.2, 0.25, 0.3]):
    shadow(c, (x, y, x + 580, y + 690), 0, 18, 55)
    c.paste(fit(im, 580, 690, fy), (x, y))
logo(c, 200, CHOC, 1500, cx=870)
save(c, "5_cascada_diagonal")

# 6 - prenda 89 (vestido satin cafe): columna desplazada sobre chocolate
f = fotos("prenda_89"); c = Image.new("RGB", (W, H), CHOC)
c.paste(fit(f[1], 640, H, 0.3, fx=0.55), (0, 0))
c.paste(fit(f[0], 400, 760, 0.3, 1.25, fx=0.62), (660, 150))
c.paste(fit(f[2], 400, 760, 0.3, 1.25, fx=0.62), (660, 150 + 760 + 20))
logo(c, 190, CREAM, 1780, 0.9, cx=860)
save(c, "6_columna_desplazada")

# 7 - prenda 90 (top cafe + short floral): encabezado panoramico + trio de cuerpo entero
f = fotos("prenda_90"); g = 14; c = Image.new("RGB", (W, H), CREAM)
c.paste(fit(f[1], W - 2 * g, 720, 0.3, 1.0), (g, g))
tw = (W - 4 * g) // 3
for i, im in enumerate([f[0], f[2], f[3]]):
    c.paste(fit(im, tw, 1000, 0.45), (g + i * (tw + g), 720 + 2 * g))
logo(c, 230, INK, 720 + 3 * g + 1000 + (H - 1762) // 2)
save(c, "7_encabezado_y_trio")
