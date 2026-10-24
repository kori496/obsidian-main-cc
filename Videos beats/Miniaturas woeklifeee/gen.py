import random, math, asyncio
from playwright.async_api import async_playwright
F={
'W':["10001","10001","10001","10101","10101","11011","10001"],
'O':["01110","10001","10001","10001","10001","10001","01110"],
'E':["11111","10000","10000","11110","10000","10000","11111"],
'K':["10001","10010","10100","11000","10100","10010","10001"],
'L':["10000","10000","10000","10000","10000","10000","11111"],
'I':["11111","00100","00100","00100","00100","00100","11111"],
'F':["11111","10000","10000","11110","10000","10000","10000"],
}
NAVY="#1d1440";CORAL="#ff4f6d";TURQ="#12c2b3";VIO="#7c4dff";SUN="#ffc233";LIME="#6bd36b";CREAM="#fff6dc";PINK="#ffd9ec"
def px_text(text,x,y,ps,colors,outline=NAVY,shadow=0.45,sw=0.3,rot=0):
    out=[];sh=[];ol=[]
    cx=x
    for i,ch in enumerate(text):
        col=colors[i%len(colors)]
        for r,row in enumerate(F[ch]):
            for c,v in enumerate(row):
                if v=="1":
                    px=cx+c*ps;py=y+r*ps
                    sh.append(f'<rect x="{px+ps*shadow:.1f}" y="{py+ps*shadow:.1f}" width="{ps}" height="{ps}" fill="{outline}"/>')
                    ol.append(f'<rect x="{px:.1f}" y="{py:.1f}" width="{ps}" height="{ps}" fill="{outline}" stroke="{outline}" stroke-width="{ps*sw:.1f}" stroke-linejoin="round"/>')
                    out.append(f'<rect x="{px-0.4:.1f}" y="{py-0.4:.1f}" width="{ps+0.8}" height="{ps+0.8}" fill="{col}"/>')
        cx+=6*ps
    return "".join(sh+ol+out)
def width(text,ps): return len(text)*6*ps-ps
def confetti(seed,n,colors,area=(0,0,1280,720),avoid=None):
    r=random.Random(seed);s=[]
    for _ in range(n):
        x=r.uniform(area[0],area[2]);y=r.uniform(area[1],area[3])
        if avoid and avoid(x,y): continue
        c=r.choice(colors);k=r.random();a=r.uniform(0,360);z=r.uniform(10,26)
        if k<.4: s.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{z:.0f}" height="{z*.45:.0f}" rx="3" fill="{c}" transform="rotate({a:.0f} {x:.0f} {y:.0f})"/>')
        elif k<.7: s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{z*.38:.0f}" fill="{c}"/>')
        else: s.append(star(x,y,z*.7,c,a))
    return "".join(s)
def star(x,y,r,c,a=0):
    pts=[]
    for i in range(10):
        rr=r if i%2==0 else r*.45
        t=math.pi/5*i-math.pi/2
        pts.append(f"{x+rr*math.cos(t):.1f},{y+rr*math.sin(t):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{c}" transform="rotate({a:.0f} {x:.0f} {y:.0f})"/>'
def badge(x,y,text,bg,fg,size=34,rot=0,pad=22):
    w=len(text)*size*0.62+pad*2;h=size*1.7
    return (f'<g transform="rotate({rot} {x+w/2:.0f} {y+h/2:.0f})"><rect x="{x+5}" y="{y+6}" width="{w:.0f}" height="{h:.0f}" rx="14" fill="{NAVY}"/>'
            f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h:.0f}" rx="14" fill="{bg}" stroke="{NAVY}" stroke-width="4"/>'
            f'<text x="{x+w/2:.0f}" y="{y+h/2+size*.36:.0f}" text-anchor="middle" font-family="Poppins" font-weight="800" font-size="{size}" fill="{fg}" letter-spacing="1">{text}</text></g>'),w,h
def wrap(inner,defs=""):
    return f'<html><body style="margin:0;background:#000"><svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720"><defs>{defs}</defs>{inner}</svg></body></html>'
def rays(cx,cy,n,color,op,R=1400,off=0):
    s=[]
    for i in range(n):
        a0=(360/n)*i+off;a1=a0+360/n/2
        p=lambda a:(cx+R*math.cos(math.radians(a)),cy+R*math.sin(math.radians(a)))
        x0,y0=p(a0);x1,y1=p(a1)
        s.append(f'<polygon points="{cx},{cy} {x0:.0f},{y0:.0f} {x1:.0f},{y1:.0f}" fill="{color}" opacity="{op}"/>')
    return "".join(s)
def bars(x,y,n,w,gap,maxh,colors,seed,base="bottom"):
    r=random.Random(seed);s=[]
    for i in range(n):
        h=maxh*(0.25+0.75*abs(math.sin(i*.55+r.random())))
        s.append(f'<rect x="{x+i*(w+gap):.0f}" y="{y-h:.0f}" width="{w}" height="{h:.0f}" rx="{w/2:.0f}" fill="{colors[i%len(colors)]}"/>')
    return "".join(s)
def sub(text,x,y,size,fill=NAVY,anchor="start",weight=800,ls=2):
    return f'<text x="{x}" y="{y}" font-family="Poppins" font-weight="{weight}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}">{text}</text>'
PAL=[CORAL,SUN,TURQ,VIO,LIME]
versions={}
# A: sunburst + two-line colored pixel title
ps=30
l1,l2="WOEK","LIFEEE"
x1=(1280-width(l1,ps))/2;x2=(1280-width(l2,ps))/2
inner=(f'<rect width="1280" height="720" fill="url(#bgA)"/>'+rays(640,430,28,"#ffffff",.55)
 +confetti(3,38,PAL,avoid=lambda x,y:150<x<1130 and 70<y<640)
 +px_text(l1,x1,70,ps,[CORAL,SUN,TURQ,VIO])+px_text(l2,x2,330,ps,[VIO,TURQ,SUN,CORAL,LIME,VIO])
 +sub("FREE FOR NON PROFIT",640,640,40,anchor="middle")
 +sub("140 BPM · E MAJOR",640,690,28,anchor="middle",fill=VIO)
)
versions["A_sunburst"]=wrap(inner,f'<linearGradient id="bgA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CREAM}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>')
# B: bold gradient, single-line navy title big, bars, sticker
ps=17
t="WOEKLIFEEE"
xb=(1280-width(t,ps))/2
b1,_,_=badge(70,560,"FREE FOR NON PROFIT",SUN,NAVY,38,-3)
b2,_,_=badge(840,60,"140 BPM",TURQ,NAVY,40,3)
inner=(f'<rect width="1280" height="720" fill="url(#bgB)"/>'
 +confetti(9,26,["#ffffff",SUN,TURQ,VIO],avoid=lambda x,y:(y>150 and y<470) or (780<x<1120 and y<150) or (y>520 and x<600))
 +bars(40,720,38,20,12,250,["#ffffff","#fff1a8","#ffd1dc"],5)
 +px_text(t,xb,200,ps,["#ffffff"],shadow=.6)
 +sub("HAPPY TRAP BEAT",640,420,52,fill=NAVY,anchor="middle",ls=4)+b1+b2
)
versions["B_bold"]=wrap(inner,f'<linearGradient id="bgB" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CORAL}"/><stop offset=".55" stop-color="#ff8a5c"/><stop offset="1" stop-color="{SUN}"/></linearGradient>')
# C: vorty panels
def panel(x,y,w,h,col,label,rot,bar_seed):
    inner=(f'<g transform="rotate({rot} {x+w/2} {y+h/2})"><rect x="{x+8}" y="{y+10}" width="{w}" height="{h}" rx="22" fill="{NAVY}" opacity=".35"/>'
     f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="#ffffff" stroke="{col}" stroke-width="6"/>'
     +sub(label,x+24,y+46,32,fill=col if col!=SUN else NAVY,ls=3)
     +bars(x+24,y+h-22,int((w-48)/18),10,8,h-100,[col],bar_seed)+'</g>')
    return inner
inner=(f'<rect width="1280" height="720" fill="url(#bgC)"/>'+rays(640,360,20,"#ffffff",.12)
 +confetti(21,22,[SUN,"#ffffff",LIME,CORAL],avoid=lambda x,y:y>330 or (y>40 and y<300 and 100<x<1180))
 +px_text("WOEKLIFEEE",(1280-width("WOEKLIFEEE",17))/2,70,17,[SUN,"#ffffff"],shadow=.6)
 +sub("HAPPY TRAP BEAT",640,300,46,fill="#ffffff",anchor="middle",ls=4)
 +panel(60,380,330,230,CORAL,"LOW",-6,1)+panel(475,410,330,230,TURQ,"MID",2,2)+panel(890,380,330,230,VIO,"HIGH",6,3)
 +sub("FREE FOR NON PROFIT",640,676,36,fill="#ffffff",anchor="middle"))
versions["C_panels"]=wrap(inner,f'<linearGradient id="bgC" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{VIO}"/><stop offset="1" stop-color="{TURQ}"/></linearGradient>')
# D: happy sun over waves (echo of sunset pic, but bright)
sun=f'<circle cx="640" cy="330" r="190" fill="url(#sunG)"/>'
waves="".join(f'<path d="M0 {440+i*46} Q 160 {410+i*46} 320 {440+i*46} T 640 {440+i*46} T 960 {440+i*46} T 1280 {440+i*46} V720 H0Z" fill="{c}"/>' for i,c in enumerate([TURQ,"#0fa89b",VIO,"#5b34d6"]))
ps=22
inner=(f'<rect width="1280" height="720" fill="url(#bgD)"/>'+rays(640,330,24,"#fff3b0",.35)+sun
 +confetti(33,24,[SUN,"#ffffff",CORAL,LIME],avoid=lambda x,y:y>420 or (40<x<1240 and 60<y<230) or (300<x<980 and 250<y<350))
 +waves
 +px_text("WOEKLIFEEE",(1280-width("WOEKLIFEEE",20))/2,70,20,["#ffffff"],shadow=.55)
 +sub("HAPPY TRAP BEAT",640,330,58,fill=NAVY,anchor="middle",ls=4)
 +sub("FREE FOR NON PROFIT",640,540,40,fill="#ffffff",anchor="middle")
 +sub("140 BPM · E MAJOR",640,596,30,fill=SUN,anchor="middle")
)
versions["D_sun"]=wrap(inner,f'<linearGradient id="bgD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff7a59"/><stop offset=".6" stop-color="{SUN}"/><stop offset="1" stop-color="{PINK}"/></linearGradient><radialGradient id="sunG"><stop offset="0" stop-color="#fffbe0"/><stop offset="1" stop-color="{SUN}"/></radialGradient>')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium",args=["--no-sandbox"])
        pg=await b.new_page(viewport={"width":1280,"height":720})
        for k,v in versions.items():
            open(f"{k}.html","w").write(v)
            await pg.goto(f"file:///{__import__('os').getcwd()}/{k}.html")
            await pg.screenshot(path=f"woeklifeee_miniatura_{k}.png")
        await b.close()
asyncio.run(main())
