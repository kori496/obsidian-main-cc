# Videos V.YA 31 oct 2026 - 5 videos verticales 1080x1920, 30 fps, sin audio real (pista muda)
import subprocess, os, sys
ONLY = set(sys.argv[1:])  # p. ej. "python3 videos_31oct.py 4" rehace solo el video 4
want = lambda n: not ONLY or str(n) in ONLY
from PIL import Image

V = "/mnt/user-data/uploads/vya contenido/videos/"
OUT = "/home/claude/w/out"; TMP = "/home/claude/w/tmp"
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
LOGO = "/mnt/user-data/uploads/obsidian-main-cc-main/obsidian-main-cc-main/Edicion de imagenes/logo_mask.png"
COLOR = "eq=contrast=1.04:saturation=1.03:brightness=0.01,colorbalance=rs=0.015:bs=-0.015:rm=0.01:bm=-0.01"
CREAM = "0xEFE9E1"

# logo blanco al 80 % y version oscura para fondos claros
m = Image.open(LOGO).convert("L")
def logo(w, rgb, a, path):
    mm = m.resize((w, round(m.height * w / m.width)), Image.LANCZOS)
    im = Image.new("RGBA", mm.size, rgb + (0,)); im.putalpha(mm.point(lambda v: int(v * a)))
    im.save(path)
logo(190, (255, 255, 255), 0.8, f"{TMP}/logo_w.png")
logo(170, (60, 52, 46), 0.9, f"{TMP}/logo_d.png")

def src(n):
    return V + (n + ".MOV" if n.startswith("IMG") else "20261029_" + n + ".mp4")

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-1500:]); raise SystemExit(1)

def seg(name, start, dur, out, w=1080, h=1920, zoom=1.0):
    """Corta un plano: tienda (Samsung 60 fps) a 0,75x; modelo a velocidad normal."""
    slow = not name.startswith("IMG")
    srcdur = dur * 0.75 if slow else dur
    pts = "setpts=PTS/0.75," if slow else ""
    sw, sh = int(w * zoom), int(h * zoom)
    vf = (f"{pts}scale={sw}:{sh}:force_original_aspect_ratio=increase,crop={w}:{h},"
          f"fps=30,{COLOR},setsar=1,format=yuv420p")
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(start), "-t", str(srcdur + 0.1),
         "-i", src(name), "-vf", vf, "-t", str(dur), "-an", "-c:v", "libx264", "-crf", "16",
         "-preset", "veryfast", out])

def concat(parts, out):
    lst = f"{TMP}/list.txt"
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
         "-c", "copy", out])

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

def simple(tag, shots, out):
    parts = []
    for i, s in enumerate(shots):
        name, start, dur = s[:3]; zoom = s[3] if len(s) > 3 else 1.0
        p = f"{TMP}/{tag}_{i:02d}.mp4"; seg(name, start, dur, p, zoom=zoom); parts.append(p)
    body = f"{TMP}/{tag}_body.mp4"; concat(parts, body); finish(body, out)

# 1 - Lookbook a ritmo: 16 planos de 1,25 s (medio compas a 96 BPM), cuerpo entero
if want(1): simple("v1", [("IMG_1597", 0.2, 1.25), ("IMG_1595", 0.5, 1.25), ("IMG_1596", 0.2, 1.25),
              ("IMG_1598", 12.6, 1.25), ("IMG_1599", 0.3, 1.25), ("IMG_1600", 0.2, 1.25),
              ("IMG_1601", 3.2, 1.25), ("IMG_1602", 0.2, 1.25), ("IMG_1603", 0.2, 1.25),
              ("IMG_1597", 8.0, 1.25), ("IMG_1595", 11.0, 1.25), ("IMG_1596", 8.0, 1.25),
              ("IMG_1600", 12.8, 1.25), ("IMG_1601", 11.0, 1.25), ("IMG_1602", 12.0, 1.25),
              ("IMG_1603", 1.8, 1.5)], f"{OUT}/VYA_video1_lookbook.mp4")

# 2 - Recorrido por la tienda: solo tienda, camara lenta 0,75x, cierra en la vitrina
if want(2): simple("v2", [("173432", 1.0, 2.5), ("171207", 3.0, 2.5), ("171247", 0.5, 2.5),
              ("171434", 5.0, 2.5), ("172300", 5.0, 2.5), ("173559", 6.0, 2.5),
              ("173456", 2.0, 2.5), ("173823", 4.0, 2.5), ("173901", 0.3, 2.5),
              ("174011", 1.0, 3.0)], f"{OUT}/VYA_video2_recorrido_tienda.mp4")

# 3 - Detalles: primeros planos (botones, hombro, cinturon, cierre, broche, espalda, volantes, escote)
if want(3): simple("v3", [("IMG_1598", 5.0, 2.5), ("IMG_1595", 8.3, 2.5, 1.12), ("IMG_1597", 3.0, 2.5),
              ("IMG_1600", 5.0, 2.5), ("IMG_1603", 10.0, 2.5, 1.1), ("IMG_1596", 5.0, 2.5),
              ("IMG_1601", 8.3, 2.5), ("IMG_1602", 5.6, 3.0)], f"{OUT}/VYA_video3_detalles.mp4")

# 4 - Diptico: frente y espalda a la vez sobre fondo crema, 6 looks x 3 s
PW, PH = 524, 932; GAP = 16; X1 = (1080 - 2 * PW - GAP) // 2; Y = 450
pairs = [(("IMG_1597", 0.2), ("IMG_1597", 6.0)), (("IMG_1595", 1.0), ("IMG_1595", 3.0)),
         (("IMG_1596", 0.2), ("IMG_1596", 5.0)), (("IMG_1598", 11.4), ("IMG_1598", 4.0)),
         (("IMG_1603", 0.2), ("IMG_1603", 3.0)), (("IMG_1602", 0.2), ("IMG_1602", 2.0))]
parts = []
for i, (a, b) in (enumerate(pairs) if want(4) else []):
    pa, pb = f"{TMP}/v4a_{i}.mp4", f"{TMP}/v4b_{i}.mp4"
    seg(a[0], a[1], 3.0, pa, PW, PH); seg(b[0], b[1], 3.0, pb, PW, PH)
    p = f"{TMP}/v4_{i:02d}.mp4"
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i",
         f"color=c={CREAM}:s=1080x1920:r=30:d=3", "-i", pa, "-i", pb, "-filter_complex",
         f"[0:v][1:v]overlay={X1}:{Y}[t];[t][2:v]overlay={X1+PW+GAP}:{Y},format=yuv420p[v]",
         "-map", "[v]", "-t", "3", "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", p])
    parts.append(p)
if want(4):
    concat(parts, f"{TMP}/v4_body.mp4")
    finish(f"{TMP}/v4_body.mp4", f"{OUT}/VYA_video4_diptico_frente_espalda.mp4",
           f"{TMP}/logo_d.png", Y + PH + 90)

# 5 - Jeans: modelo con jean + jeans en gancho y maniqui
if want(5): simple("v5", [("IMG_1596", 0.2, 2.5), ("171808", 0.2, 2.5), ("IMG_1601", 8.6, 2.5),
              ("173901", 0.2, 2.5), ("IMG_1596", 2.4, 2.5), ("173823", 11.0, 2.5),
              ("173559", 3.3, 2.5), ("IMG_1601", 3.0, 2.5), ("173456", 3.3, 2.0),
              ("IMG_1596", 9.0, 3.0)], f"{OUT}/VYA_video5_jeans.mp4")
