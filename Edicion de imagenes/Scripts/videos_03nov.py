# Videos V.YA 03 nov 2026 - 5 videos verticales 1080x1920, 30 fps, pista muda, solo logo
# python3 videos_03nov.py 3  -> rehace solo el video 3
import subprocess, os, sys, csv
from PIL import Image, ImageDraw
ONLY = set(sys.argv[1:]); want = lambda n: not ONLY or str(n) in ONLY

V = "/mnt/user-data/uploads/vya contenido/videosYimagenesParaClaude/"
FOT = "/mnt/user-data/uploads/vya contenido/fotos/192026 FOTOS ALMACEN/"
CSV = "/mnt/user-data/uploads/vya contenido/assets/mapa_renombrado.csv"
OUT = "/home/claude/w/out"; TMP = "/home/claude/w/tmp"
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
LOGO = "/mnt/user-data/uploads/obsidian-main-cc-main/obsidian-main-cc-main/Edicion de imagenes/logo_mask.png"
COLOR = "eq=contrast=1.04:saturation=1.03:brightness=0.01,colorbalance=rs=0.015:bs=-0.015:rm=0.01:bm=-0.01"
CREAM = "0xEFE9E1"; CHOC = "0x342923"; LINE = (176, 150, 118)

m = Image.open(LOGO).convert("L")
def logo(w, rgb, a, path):
    mm = m.resize((w, round(m.height * w / m.width)), Image.LANCZOS)
    im = Image.new("RGBA", mm.size, rgb + (0,)); im.putalpha(mm.point(lambda v: int(v * a))); im.save(path)
logo(190, (255, 255, 255), 0.8, f"{TMP}/logo_w.png")
logo(190, (60, 52, 46), 0.9, f"{TMP}/logo_d.png")
logo(190, (239, 233, 225), 0.95, f"{TMP}/logo_c.png")

def src(n):
    if n.startswith("IMG"): return V + n + ".MOV"
    return V + ("20261029_" if n.startswith("29_") else "20261103_") + n[3:] + ".mp4"

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-1500:]); raise SystemExit(1)

def seg(name, start, dur, out, w=1080, h=1920, push=0.0):
    """Corta un plano. Tienda (Samsung 60 fps) a 0,75x; modelo normal. push = acercamiento lento."""
    slow = not name.startswith("IMG")
    srcdur = dur * 0.75 if slow else dur
    pts = "setpts=PTS/0.75," if slow else ""
    if push:
        z = f"(1+{push}*t/{dur})"
        sc = (f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},"
              f"scale=w='trunc({w}*{z}/2)*2':h='trunc({h}*{z}/2)*2':eval=frame,crop={w}:{h}")
    else:
        sc = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
    vf = f"{pts}fps=30,{sc},{COLOR},setsar=1,format=yuv420p"
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(start), "-t", str(srcdur + 0.1),
         "-i", src(name), "-vf", vf, "-t", str(dur), "-an", "-c:v", "libx264", "-crf", "16",
         "-preset", "veryfast", out])

def concat(parts, out):
    lst = f"{TMP}/list.txt"; open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out])

def finish(body, out, logo_file=f"{TMP}/logo_w.png", y=1735):
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                       "-of", "csv=p=0", body]).decode())
    fc = (f"[0:v][1:v]overlay=(W-w)/2:{y},fade=t=in:st=0:d=0.25,"
          f"fade=t=out:st={d-0.6:.2f}:d=0.6,format=yuv420p[v]")
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", body, "-i", logo_file,
         "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-filter_complex", fc,
         "-map", "[v]", "-map", "2:a", "-t", f"{d:.2f}", "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "22", "-maxrate", "7M", "-bufsize", "14M", "-c:a", "aac", "-b:a", "96k",
         "-movflags", "+faststart", out])
    print(out, round(os.path.getsize(out) / 1e6, 1), "MB", round(d, 2), "s")

def on_bg(layers, dur, out, bg=CREAM, still=None):
    """Pone clips (path, x, y, mask_png|None) sobre un fondo liso (o una imagen fija)."""
    inp = ["-f", "lavfi", "-i", f"color=c={bg}:s=1080x1920:r=30:d={dur}"]
    fc = ""; last = "0:v"; k = 1
    if still:
        inp += ["-loop", "1", "-t", str(dur), "-i", still]; fc += f"[{last}][{k}:v]overlay=0:0[s{k}];"; last = f"s{k}"; k += 1
    for i, (p, x, y, mask) in enumerate(layers):
        inp += ["-i", p]; vin = f"{k}:v"; k += 1
        if mask:
            inp += ["-loop", "1", "-t", str(dur), "-i", mask]
            fc += f"[{k}:v]format=gray[m{i}];[{vin}][m{i}]alphamerge[a{i}];"; vin = f"a{i}"; k += 1
        fc += f"[{last}][{vin}]overlay={x}:{y}[o{i}];"; last = f"o{i}"
    fc += f"[{last}]format=yuv420p[v]"
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", *inp, "-filter_complex", fc, "-map", "[v]",
         "-t", str(dur), "-r", "30", "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", out])

def simple(tag, shots, out, push=0.0):
    parts = []
    for i, s in enumerate(shots):
        p = f"{TMP}/{tag}_{i:02d}.mp4"; seg(s[0], s[1], s[2], p, push=push); parts.append(p)
    concat(parts, f"{TMP}/{tag}_body.mp4"); finish(f"{TMP}/{tag}_body.mp4", out)

# 1 - Nueva coleccion: solo los clips de hoy (3 nov), 0,75x, cada plano con un acercamiento lento
if want(1): simple("v1", [("03_173856", 0.5, 2.5), ("03_173614", 0.3, 2.5), ("03_173734", 0.3, 2.5),
              ("03_174007", 0.5, 2.5), ("03_173645", 0.5, 2.5), ("03_173614", 5.5, 2.5),
              ("03_173734", 6.5, 2.5), ("03_173645", 12.5, 2.5), ("03_173856", 6.0, 2.5),
              ("03_174007", 6.5, 3.0)], f"{OUT}/VYA_IA_video1_nueva_coleccion.mp4", push=0.07)

# 2 - Ventana en arco: los looks dentro de un arco sobre crema, con linea fina
AW, AH, AX, AY = 820, 1340, 130, 200
if want(2):
    am = Image.new("L", (AW, AH), 0); d = ImageDraw.Draw(am)
    d.ellipse((0, 0, AW - 1, AW - 1), fill=255); d.rectangle((0, AW // 2, AW - 1, AH - 1), fill=255)
    am.save(f"{TMP}/arch.png")
    bg = Image.new("RGB", (1080, 1920), (239, 233, 225)); d = ImageDraw.Draw(bg)
    x0, y0, x1, y1 = AX - 22, AY - 22, AX + AW + 22, AY + AH + 22; w = x1 - x0
    d.arc((x0, y0, x1, y0 + w), 180, 360, fill=LINE, width=2)
    d.line((x0, y0 + w // 2, x0, y1), fill=LINE, width=2); d.line((x1, y0 + w // 2, x1, y1), fill=LINE, width=2)
    bg.save(f"{TMP}/arch_bg.png")
    looks = [("IMG_1602", 0.2), ("IMG_1597", 0.2), ("IMG_1595", 0.5), ("IMG_1600", 0.2),
             ("IMG_1599", 0.3), ("IMG_1603", 0.2), ("IMG_1598", 11.4), ("IMG_1601", 3.2)]
    parts = []
    for i, (n, s) in enumerate(looks):
        a = f"{TMP}/v2a_{i}.mp4"; seg(n, s, 2.5, a, AW, AH)
        p = f"{TMP}/v2_{i:02d}.mp4"; on_bg([(a, AX, AY, f"{TMP}/arch.png")], 2.5, p, still=f"{TMP}/arch_bg.png")
        parts.append(p)
    concat(parts, f"{TMP}/v2_body.mp4")
    finish(f"{TMP}/v2_body.mp4", f"{OUT}/VYA_IA_video2_ventana_arco.mp4", f"{TMP}/logo_d.png", AY + AH + 95)

# 3 - Triptico en movimiento: tres looks a la vez en columnas escalonadas, cambia cada 3,5 s
if want(3):
    CW, CH, GAP = 316, 1420, 18; X0 = (1080 - 3 * CW - 2 * GAP) // 2; YS = [170, 70, 230]
    sets = [[("IMG_1597", 0.2), ("IMG_1602", 0.2), ("IMG_1603", 0.2)],
            [("IMG_1595", 0.5), ("IMG_1600", 0.2), ("IMG_1596", 0.2)],
            [("IMG_1598", 11.0), ("IMG_1599", 0.3), ("IMG_1601", 3.2)],
            [("IMG_1603", 6.0), ("IMG_1597", 7.0), ("IMG_1602", 6.0)]]
    parts = []
    for i, st in enumerate(sets):
        lay = []
        for j, (n, s) in enumerate(st):
            p = f"{TMP}/v3c_{i}{j}.mp4"; seg(n, s, 3.5, p, CW, CH); lay.append((p, X0 + j * (CW + GAP), YS[j], None))
        p = f"{TMP}/v3_{i:02d}.mp4"; on_bg(lay, 3.5, p); parts.append(p)
    concat(parts, f"{TMP}/v3_body.mp4")
    finish(f"{TMP}/v3_body.mp4", f"{OUT}/VYA_IA_video3_triptico.mp4", f"{TMP}/logo_d.png", 1765)

# 4 - Fotos en movimiento: fotos de la sesion 19 oct a sangre, 1,25 s c/u con acercamiento lento
if want(4):
    rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
    pick = {"prenda_97": [0, 1], "prenda_98": [0, 2], "prenda_101": [1, 2], "prenda_104": [0, 1],
            "prenda_105": [1, 0], "prenda_109": [0, 1], "prenda_110": [0, 2]}
    parts = []; k = 0
    for g, idx in pick.items():
        fs = [x["nombre_original"] for x in rows if x["grupo"] == g]
        for i in idx:
            dur = 1.25; p = f"{TMP}/v4_{k:02d}.mp4"; k += 1
            z = f"(1+0.06*t/{dur})"
            vf = (f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920:(iw-1080)/2:(ih-1920)*0.3,"
                  f"scale=w='trunc(1080*{z}/2)*2':h='trunc(1920*{z}/2)*2':eval=frame,crop=1080:1920,"
                  f"{COLOR},setsar=1,format=yuv420p")
            run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-t", str(dur),
                 "-i", FOT + fs[i], "-vf", vf, "-t", str(dur), "-c:v", "libx264", "-crf", "16",
                 "-preset", "veryfast", p])
            parts.append(p)
    concat(parts, f"{TMP}/v4_body.mp4"); finish(f"{TMP}/v4_body.mp4", f"{OUT}/VYA_IA_video4_fotos_en_movimiento.mp4", y=90)

# 5 - Denim en 4:5: ventana 1080x1350 con bandas crema arriba y abajo, logo en la banda de abajo
if want(5):
    FW, FH, FY = 1080, 1350, 250
    shots = [("IMG_1596", 0.2, 2.5), ("03_173856", 0.5, 2.5), ("03_173734", 2.5, 2.5),
             ("IMG_1601", 8.6, 2.5), ("29_173823", 11.0, 2.5), ("03_173645", 13.0, 2.5),
             ("IMG_1596", 2.4, 2.5), ("03_173856", 7.0, 2.5), ("IMG_1596", 9.0, 3.0)]
    parts = []
    for i, (n, s, du) in enumerate(shots):
        a = f"{TMP}/v5a_{i}.mp4"; seg(n, s, du, a, FW, FH)
        p = f"{TMP}/v5_{i:02d}.mp4"; on_bg([(a, 0, FY, None)], du, p); parts.append(p)
    concat(parts, f"{TMP}/v5_body.mp4")
    finish(f"{TMP}/v5_body.mp4", f"{OUT}/VYA_IA_video5_denim_4x5.mp4", f"{TMP}/logo_d.png", FY + FH + 120)
