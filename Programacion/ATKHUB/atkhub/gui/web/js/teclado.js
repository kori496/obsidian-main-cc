// Vistas del teclado Ajazz AK820 Max.
import { el, svg, panel, segmento, deslizador } from "./ui.js";

export function diffTeclado(a, b) {
  if (!a || !b) return null;
  const c = {};
  for (const k of ["efecto", "brillo", "velocidad", "color", "direccion", "suspension"]) if (String(a[k]) !== String(b[k])) c[k] = b[k];
  return Object.keys(c).length ? c : null;
}

export function vistaTeclado(pestana, ctx) {
  return pestana === "energia" ? energia(ctx) : iluminacion(ctx);
}

const PALETA = [[255, 0, 0], [0, 255, 0], [0, 80, 255], [255, 230, 0], [255, 0, 255], [0, 255, 255], [255, 255, 255], null];
const NOMBRE_COLOR = ["Rojo", "Verde", "Azul", "Amarillo", "Magenta", "Cian", "Blanco", "Arcoíris"];

// ---------- geometría real del AK820 Max (medida sobre la foto de arriba) ----------
// [leyenda, x (u), ancho (u), tipo, dy] · tipo: c = crema, g = salvia, o = naranja
const FILAS = [
  [["Esc", 0, 1, "o"], ["F1", 1.25], ["F2", 2.25], ["F3", 3.25], ["F4", 4.25],
   ["F5", 5.5, 1, "g"], ["F6", 6.5, 1, "g"], ["F7", 7.5, 1, "g"], ["F8", 8.5, 1, "g"],
   ["F9", 9.75], ["F10", 10.75], ["F11", 11.75], ["F12", 12.75], ["Delete", 14, 1, "g"]],
  [["~`", 0], ["!1", 1], ["@2", 2], ["#3", 3], ["$4", 4], ["%5", 5], ["^6", 6], ["&7", 7], ["*8", 8], ["(9", 9], [")0", 10],
   ["_-", 11], ["+=", 12], ["Backspace", 13, 2, "g"], ["Home", 15.4, 1, "g"]],
  [["Tab", 0, 1.5, "g"], ..."QWERTYUIOP".split("").map((l, i) => [l, 1.5 + i]), ["{[", 11.5], ["}]", 12.5],
   ["|\\", 13.5, 1.5], ["PgUp", 15.4, 1, "g"]],
  [["Caps Lock", 0, 1.75, "g"], ..."ASDFGHJKL".split("").map((l, i) => [l, 1.75 + i]), [":;", 10.75], ['"\'', 11.75],
   ["Enter", 12.75, 2.25, "o"], ["PgDn", 15.4, 1, "g"]],
  [["Shift", 0, 2.25, "g"], ..."ZXCVBNM".split("").map((l, i) => [l, 2.25 + i]), ["<,", 9.25], [">.", 10.25], ["?/", 11.25],
   ["Shift", 12.25, 1.75, "g"], ["↑", 14.2, 1, "g", 0.2], ["End", 15.4, 1, "g"]],
  [["Ctrl", 0, 1.25, "g"], ["Win", 1.25, 1.25, "g"], ["Alt", 2.5, 1.25, "g"], ["", 3.75, 6.25, "o"],
   ["Alt", 10, 1, "g"], ["Fn", 11, 1, "g"], ["Ctrl", 12, 1, "g"],
   ["←", 13.2, 1, "g", 0.25], ["↓", 14.2, 1, "g", 0.25], ["→", 15.2, 1, "g", 0.25]],
];
const Y_FILA = [0, 1.27, 2.27, 3.27, 4.27, 5.27];
const U = 46, ANCHO_U = 16.4, ALTO_U = 6.52;
const M_LADO = 0.55 * U, M_ARRIBA = 0.52 * U, M_ABAJO = 0.7 * U;
const COLORES_TECLA = {
  c: { top: "#ece6d9", lado: "#d0c8b8", texto: "#8c877a" },
  g: { top: "#b7b8a2", lado: "#999a85", texto: "#f5f3ea" },
  o: { top: "#ef7b31", lado: "#cf5f1c", texto: "#fff1e4" },
};

function construirTeclas() {
  const teclas = [];
  FILAS.forEach((fila, f) => fila.forEach(([leyenda, x, ancho = 1, tipo = "c", dy = 0]) => {
    teclas.push({ leyenda, tipo, f, x: M_LADO + x * U, y: M_ARRIBA + (Y_FILA[f] + dy) * U, w: ancho * U, h: U });
  }));
  const W = Math.round(M_LADO * 2 + ANCHO_U * U), H = Math.round(M_ARRIBA + M_ABAJO + ALTO_U * U);
  let semilla = 7;
  const azar = () => ((semilla = (semilla * 16807) % 2147483647) / 2147483647);
  for (const k of teclas) {
    k.nx = (k.x + k.w / 2) / W; k.ny = (k.y + k.h / 2) / H;
    k.s = azar(); k.s2 = azar(); k.col = Math.round((k.x - M_LADO) / U);
  }
  return { teclas, W, H };
}

// HSV -> RGB (h en grados)
function hsv(h, s = 1, v = 1) {
  h = ((h % 360) + 360) % 360;
  const f = (n) => { const k = (n + h / 60) % 6; return v - v * s * Math.max(0, Math.min(k, 4 - k, 1)); };
  return [f(5) * 255, f(3) * 255, f(1) * 255];
}
const fr = (x) => x - Math.floor(x);

// Intensidad (0..1) y color de cada tecla según el efecto. Aproximación visual de lo que hace el teclado.
function luzTecla(efecto, k, t, dir, colorFijo) {
  const sgn = dir ? -1 : 1;
  let i = 1, h = null;
  const ang = Math.atan2(k.ny - 0.5, (k.nx - 0.5) * 2.5);
  const dist = Math.hypot((k.nx - 0.5) * 2.5, k.ny - 0.5);
  switch (efecto) {
    case 1: i = 0.15 + 0.85 * Math.max(0, Math.sin((Math.abs(k.nx - 0.5) * 6 - t * 1.6 * sgn) * Math.PI)) ** 2; h = Math.abs(k.nx - 0.5) * 300 + t * 40; break;
    case 2: i = Math.max(0, Math.sin(t * 1.4 + k.s * 40)) ** 10; h = k.s * 360; break;
    case 3: i = 0.15 + 0.85 * Math.max(0, Math.sin((k.ny * 3 - t * 1.4 * sgn) * Math.PI)) ** 2; h = k.ny * 200 + t * 40; break;
    case 4: i = 0.1 + 0.9 * Math.max(0, Math.sin((dist * 4 - t * 1.8 * sgn) * Math.PI)) ** 3; h = dist * 260 - t * 50; break;
    case 5: i = 1; h = t * 60; break;
    case 6: i = 0.6 + 0.4 * Math.sin(dist * 10 - t * 2 * sgn); h = (ang * 180) / Math.PI + t * 50 * sgn; break;
    case 7: i = 1; h = k.nx * 300 + k.ny * 60; break;
    case 8: i = 0.08 + 0.92 * (0.5 + 0.5 * Math.sin(t * 1.6)) ** 2; h = t * 25; break;
    case 9: { const px = fr(t * 0.18 * sgn), py = 0.5 + 0.4 * Math.sin(t * 0.9);
      i = Math.max(Math.exp(-((k.nx - px) ** 2) * 900), Math.exp(-((k.ny - py) ** 2) * 220)); h = px * 360; break; }
    case 11: i = (0.5 + 0.5 * Math.sin(t * 1.8 + k.s * 30)) ** 3; h = k.s2 * 360; break;
    case 12: i = 1; h = k.nx * 360 - t * 70; break;
    case 15: { const arriba = k.f < 3, fase = Math.floor(t * 0.7) % 2 === 0; i = arriba === fase ? 1 : 0.06; h = arriba ? t * 30 : t * 30 + 180; break; }
    case 16: { const gota = fr(t * 0.55 + k.col * 0.37 + Math.sin(k.col * 12.9) * 0.5); i = Math.max(0, 1 - Math.abs(gota * 1.3 - k.ny) * 5) ** 2; h = 200 + k.col * 8; break; }
    case 17: i = 0.15 + 0.85 * Math.max(0, Math.sin(ang * 2 - t * 2.2 * sgn)) ** 4; h = (ang * 180) / Math.PI * 2 + t * 40; break;
    case 18: { const yc = 0.5 + 0.32 * Math.sin(k.nx * Math.PI * 2 + t * 2 * sgn); i = Math.max(0, 1 - Math.abs(k.ny - yc) * 6); h = k.nx * 360 + t * 30; break; }
    case 19: { const bx = fr(t * 0.35 * sgn); const d = Math.min(Math.abs(k.nx - bx), 1 - Math.abs(k.nx - bx)); i = 0.05 + 0.95 * Math.max(0, 1 - d * 9); h = bx * 360; break; }
    default: i = 1; h = 0;
  }
  const rgb = colorFijo || hsv(h ?? 0);
  return [rgb, Math.max(0, Math.min(1, i))];
}

// Vista previa en 3 capas para que cada cuadro cueste poco:
//   base (carcasa + placa oscura, una vez) -> luces RGB entre las teclas (cada cuadro) -> teclas (una vez)
class VistaPreviaTeclado {
  constructor() {
    const { teclas, W, H } = construirTeclas();
    this.teclas = teclas; this.W = W; this.H = H;
    this.dpr = Math.min(2, window.devicePixelRatio || 1);
    this.lienzo = el("canvas", { class: "teclado-lienzo", width: W * this.dpr, height: H * this.dpr, "aria-label": "Vista previa del teclado" });
    this.ctx = this.lienzo.getContext("2d");
    this.cfg = { efecto: 8, brillo: 5, velocidad: 4, color: 7, direccion: 0 };
    this.t = 0; this.ultimo = 0; this.activo = false;
    this.base = this.capa((g) => this.dibujarBase(g));
    this.tapas = this.capa((g) => this.dibujarTeclas(g));
    this.cuadro = this.cuadro.bind(this);
    // solo anima si se ve en pantalla
    this.obs = new IntersectionObserver(([e]) => (e.isIntersecting ? this.iniciar() : this.parar()));
    this.obs.observe(this.lienzo);
  }
  capa(dibujar) {
    const c = document.createElement("canvas");
    c.width = this.W * this.dpr; c.height = this.H * this.dpr;
    const g = c.getContext("2d"); g.scale(this.dpr, this.dpr); dibujar(g);
    return c;
  }
  dibujarBase(g) {
    const r = 0.5 * U;
    // sombra y carcasa crema
    g.save(); g.shadowColor = "rgba(0,0,0,.55)"; g.shadowBlur = 22; g.shadowOffsetY = 10;
    const grad = g.createLinearGradient(0, 0, 0, this.H);
    grad.addColorStop(0, "#f1ece2"); grad.addColorStop(1, "#d9d1c3");
    g.fillStyle = grad; g.beginPath(); g.roundRect(6, 4, this.W - 12, this.H - 16, r); g.fill(); g.restore();
    g.strokeStyle = "rgba(255,255,255,.6)"; g.lineWidth = 1.2;
    g.beginPath(); g.roundRect(6.5, 4.5, this.W - 13, this.H - 17, r); g.stroke();
    // placa oscura bajo las teclas (ahí se ve la luz RGB)
    g.fillStyle = "#24221f";
    for (const k of this.teclas) { g.beginPath(); g.roundRect(k.x - 2, k.y - 2, k.w + 4, k.h + 4, 7); g.fill(); }
    // luces indicadoras entre Backspace y la columna de navegación
    g.font = "600 8px Bahnschrift, 'Segoe UI', sans-serif"; g.textAlign = "center"; g.fillStyle = "#6f6a60";
    ["C", "W", "▯"].forEach((l, i) => {
      const x = M_LADO + 15.2 * U, y = M_ARRIBA + (Y_FILA[i + 1] + 0.32) * U;
      g.beginPath(); g.arc(x, y, 2.2, 0, Math.PI * 2); g.fill();
      g.fillText(l, x, y + 13);
    });
  }
  dibujarTeclas(g) {
    for (const k of this.teclas) {
      const c = COLORES_TECLA[k.tipo];
      // lado (perfil de la tecla) y cara superior
      g.fillStyle = c.lado; g.beginPath(); g.roundRect(k.x + 1, k.y + 1, k.w - 2, k.h - 2, 5); g.fill();
      g.fillStyle = c.top; g.beginPath(); g.roundRect(k.x + 5, k.y + 3, k.w - 10, k.h - 11, 5); g.fill();
      g.strokeStyle = "rgba(255,255,255,.35)"; g.lineWidth = 1; g.stroke();
      if (k.leyenda) {
        g.fillStyle = c.texto; g.textBaseline = "middle";
        const largo = k.leyenda.length > 2 || k.tipo !== "c";
        if (k.leyenda.length === 2 && /[^A-Za-z0-9]/.test(k.leyenda) && k.tipo === "c") {
          // tecla con dos símbolos (como !1): arriba y abajo a la izquierda
          g.font = "500 10px Bahnschrift, 'Segoe UI', sans-serif"; g.textAlign = "left";
          g.fillText(k.leyenda[0], k.x + 10, k.y + 12); g.fillText(k.leyenda[1], k.x + 10, k.y + 25);
        } else {
          g.font = `${largo ? 600 : 500} ${largo ? 9.5 : 13}px Bahnschrift, 'Segoe UI', sans-serif`;
          g.textAlign = "left";
          g.fillText(k.leyenda, k.x + 10, k.y + (largo ? 17 : 15));
        }
      }
    }
    // perilla de metal sobre la columna de navegación
    const px = M_LADO + 15.9 * U, py = M_ARRIBA + 0.5 * U, R = 0.48 * U;
    g.save(); g.shadowColor = "rgba(0,0,0,.35)"; g.shadowBlur = 8; g.shadowOffsetY = 3;
    const aro = g.createLinearGradient(px - R, py - R, px + R, py + R);
    aro.addColorStop(0, "#fbfbfb"); aro.addColorStop(0.45, "#9c9ea3"); aro.addColorStop(0.55, "#e9eaec"); aro.addColorStop(1, "#6f7176");
    g.fillStyle = aro; g.beginPath(); g.arc(px, py, R, 0, Math.PI * 2); g.fill(); g.restore();
    const centro = g.createRadialGradient(px - 4, py - 5, 1, px, py, R * 0.72);
    centro.addColorStop(0, "#f7f4ec"); centro.addColorStop(1, "#d8d2c5");
    g.fillStyle = centro; g.beginPath(); g.arc(px, py, R * 0.7, 0, Math.PI * 2); g.fill();
  }
  poner(cfg) { Object.assign(this.cfg, cfg); if (!this.activo) this.pintar(); }
  iniciar() { if (this.activo) return; this.activo = true; this.ultimo = performance.now(); requestAnimationFrame(this.cuadro); }
  parar() { this.activo = false; }
  destruir() { this.parar(); this.obs.disconnect(); }
  cuadro(ahora) {
    if (!this.activo) return;
    if (!document.hidden) {
      const vel = 0.35 + (this.cfg.velocidad - 1) * 0.32;
      this.t += Math.min(0.05, (ahora - this.ultimo) / 1000) * vel;
      this.pintar();
    }
    this.ultimo = ahora;
    requestAnimationFrame(this.cuadro);
  }
  pintar() {
    const g = this.ctx, { efecto, brillo, color, direccion } = this.cfg;
    const b = 0.25 + 0.75 * (brillo / 5);
    const fijo = PALETA[color] || null;
    g.setTransform(1, 0, 0, 1, 0, 0);
    g.clearRect(0, 0, this.lienzo.width, this.lienzo.height);
    g.drawImage(this.base, 0, 0);
    g.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
    // la luz se asoma por los bordes de cada tecla, como en el teclado real (teclas opacas)
    for (const k of this.teclas) {
      const [[r, gg, bb], i] = luzTecla(Number(efecto), k, this.t, Number(direccion), fijo);
      const a = i * b;
      if (a < 0.02) continue;
      g.fillStyle = `rgba(${r | 0},${gg | 0},${bb | 0},${(a * 0.35).toFixed(3)})`;
      g.beginPath(); g.roundRect(k.x - 5, k.y - 5, k.w + 10, k.h + 10, 10); g.fill();
      g.fillStyle = `rgba(${r | 0},${gg | 0},${bb | 0},${a.toFixed(3)})`;
      g.beginPath(); g.roundRect(k.x - 2, k.y - 2, k.w + 4, k.h + 4, 7); g.fill();
    }
    g.setTransform(1, 0, 0, 1, 0, 0);
    g.drawImage(this.tapas, 0, 0);
  }
}

function iluminacion(ctx) {
  const c = ctx.edit;
  const efectos = ctx.catalogo.efectos;
  const previa = new VistaPreviaTeclado();
  previa.poner(c);

  const muestras = el("div", { class: "muestras" }, PALETA.map((rgb, i) => el("button", {
    class: `muestra ${rgb ? "" : "arcoiris"}`, title: NOMBRE_COLOR[i], "data-i": i,
    style: rgb ? { background: `rgb(${rgb})` } : {},
    onclick: () => { c.color = i; actualizar(); ctx.cambiar(); } })));
  const nombreColor = el("span", { class: "valor" });
  const brillo = deslizador({ etiqueta: "Brillo", min: 1, max: 5, valor: c.brillo, formato: (v) => `${v}/5`,
    alCambiar: (v) => { c.brillo = v; actualizar(); ctx.cambiar(); } });
  const vel = deslizador({ etiqueta: "Velocidad", min: 1, max: 5, valor: c.velocidad, formato: (v) => `${v}/5`,
    alCambiar: (v) => { c.velocidad = v; actualizar(); ctx.cambiar(); } });
  const dir = segmento([[0, "Izq → Der"], [1, "Der → Izq"]], c.direccion, (v) => { c.direccion = v; actualizar(); ctx.cambiar(); });
  const cajaDir = el("div", {}, el("div", { class: "etiqueta", style: { margin: "14px 0 8px" } }, "Dirección"), dir);
  const cajaColor = panel("Color", el("div", { class: "fila entre", style: { marginBottom: "10px" } }, el("span", { class: "etiqueta" }, "Paleta del teclado"), nombreColor), muestras,
    el("p", { class: "nota", style: { margin: "12px 0 0" } }, "El teclado solo acepta estos 8 colores en sus efectos."));

  const lista = el("div", { class: "lista" }, efectos.map((e) => el("div", { class: "item", "data-id": e.id, tabindex: 0,
    onclick: () => { c.efecto = e.id; actualizar(); ctx.cambiar(); },
    onkeydown: (ev) => { if (ev.key === "Enter") { c.efecto = e.id; actualizar(); ctx.cambiar(); } } },
    el("span", { class: "item-icono", html: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="7" width="18" height="10" rx="2"/><path d="M7 12h.01M11 12h.01M15 12h.01"/></svg>' }),
    e.nombre, el("small", {}, e.id))));

  function actualizar() {
    const e = efectos.find((x) => x.id === Number(c.efecto));
    lista.querySelectorAll(".item").forEach((n) => n.classList.toggle("activo", Number(n.dataset.id) === Number(c.efecto)));
    muestras.querySelectorAll(".muestra").forEach((n) => n.classList.toggle("activa", Number(n.dataset.i) === Number(c.color)));
    nombreColor.textContent = NOMBRE_COLOR[c.color];
    cajaColor.style.opacity = e?.color ? "" : ".4";
    cajaColor.style.pointerEvents = e?.color ? "" : "none";
    cajaDir.style.display = e?.direccion ? "" : "none";
    vel.habilitar(Number(c.efecto) !== 7);
    previa.poner(c);
  }
  requestAnimationFrame(actualizar);

  return {
    nodo: el("div", { class: "rejilla", style: { gridTemplateColumns: "250px minmax(520px, 1fr)", alignItems: "start" } },
      panel("Efectos", lista),
      el("div", { class: "rejilla" },
        el("div", { class: "teclado-escena" }, previa.lienzo, el("div", { class: "leyenda-previa" }, "Vista previa aproximada")),
        el("div", { class: "rejilla", style: { gridTemplateColumns: "1fr 1fr" } },
          cajaColor,
          panel("Ajustes", brillo, vel, cajaDir)))),
    destruir: () => previa.destruir(),
  };
}

function energia(ctx) {
  const c = ctx.edit, r = ctx.extra;
  const seg = segmento([["5", "5 min"], ["15", "15 min"], ["30", "30 min"], ["nunca", "Nunca"]], String(c.suspension),
    (v) => { c.suspension = v; ctx.cambiar(); });
  const l = 2 * Math.PI * 60, pct = r.bateria;
  const anillo = svg(`<svg class="anillo-bat" viewBox="0 0 150 150">
    <circle class="fondo-a" cx="75" cy="75" r="60"/>
    <circle class="valor-a" cx="75" cy="75" r="60" stroke-dasharray="${l}" stroke-dashoffset="${pct == null ? l : l * (1 - pct / 100)}"/>
    <text x="75" y="80" text-anchor="middle" fill="#e8e8ea" font-size="24" font-weight="700">${pct == null ? "—" : pct + "%"}</text>
    <text x="75" y="100" text-anchor="middle" fill="#8b8c94" font-size="9" letter-spacing="2">BATERÍA</text></svg>`);
  return {
    nodo: el("div", { class: "rejilla", style: { gridTemplateColumns: "minmax(420px, 1.4fr) minmax(280px, 1fr)", alignItems: "start" } },
      panel("Suspensión", el("p", { class: "nota", style: { margin: "0 0 14px" } }, "Tiempo sin uso antes de que el teclado se apague (en inalámbrico)."), seg),
      el("section", { class: "panel", style: { display: "grid", justifyItems: "center", gap: "8px" } },
        el("div", { class: "panel-cab", style: { width: "100%" } }, el("div", { class: "titulo-seccion" }, "Batería")),
        anillo, el("div", { class: "nota" }, r.energia || ""))),
  };
}
