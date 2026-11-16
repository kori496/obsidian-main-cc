// Vistas del mouse Attack Shark X11.
import { el, svg, panel, segmento, deslizador, dialDpi, selectorColor, aviso, abrirPopover, cerrarPopover } from "./ui.js";

// ---------- diferencias (lo que hay que mandar) ----------
export function diffMouse(a, b) {
  if (!a || !b) return null;
  const c = {};
  if (a.polling !== b.polling) c.polling = b.polling;
  const dpi = {};
  b.dpi.etapas.forEach((e, i) => { if (e.dpi > 0 && e.dpi !== a.dpi.etapas[i].dpi) dpi[e.numero] = e.dpi; });
  if (Object.keys(dpi).length) c.dpi = dpi;
  const luz = {};
  for (const k of ["modo", "color", "brillo", "velocidad"]) if (a.luz[k] !== b.luz[k]) luz[k] = b.luz[k];
  if (Object.keys(luz).length) c.luz = luz;
  const sus = {};
  for (const k of ["normal", "profunda"]) if (a.suspension[k] !== b.suspension[k]) sus[k] = b.suspension[k];
  if (Object.keys(sus).length) c.suspension = sus;
  const bot = {};
  for (const [k, v] of Object.entries(b.botones)) if (a.botones[k]?.id !== v.id) bot[k] = v.id;
  if (Object.keys(bot).length) c.botones = bot;
  return Object.keys(c).length ? c : null;
}

export function vistaMouse(pestana, ctx) {
  return ({ rendimiento, iluminacion, botones, energia }[pestana] || rendimiento)(ctx);
}

// ---------- RENDIMIENTO ----------
function ondaSvg(hz) {
  const pulsos = { 125: 5, 250: 8, 500: 13, 1000: 22 }[hz] || 10;
  const w = 600, ancho = w / pulsos;
  let d = "M0 52";
  for (let i = 0; i < pulsos * 2; i++) {
    const x = i * ancho;
    d += ` L${x} 52 L${x} 18 L${x + ancho / 2} 18 L${x + ancho / 2} 52`;
  }
  return svg(`<svg viewBox="0 0 ${w * 2} 70" preserveAspectRatio="none" style="animation-duration:${hz >= 1000 ? 1.6 : 2.4}s">
    <path d="${d}" fill="none" stroke="#ff5a1a" stroke-width="2.2" vector-effect="non-scaling-stroke"/></svg>`);
}

function rendimiento(ctx) {
  const m = ctx.edit;
  const etapas = m.dpi.etapas.filter((e) => e.dpi > 0);
  const tarjetas = etapas.map((e) => {
    const d = dialDpi(e.dpi, (v) => { e.dpi = v; ctx.cambiar(); });
    return el("div", { class: `etapa ${e.numero === m.dpi.actual ? "actual" : ""} ${e.activa ? "" : "inactiva"}` },
      el("div", { class: "etapa-cab" },
        el("span", {}, `ETAPA ${e.numero}`),
        e.numero === m.dpi.actual ? el("span", { class: "chip" }, "ACTUAL")
          : el("span", { class: "etapa-color", style: { background: e.color, color: e.color } })),
      d.svg, d.entrada);
  });

  const onda = el("div", { class: "onda" }, ondaSvg(m.polling));
  const seg = segmento(ctx.catalogo.polling.map((p) => [p, p + " Hz"]), m.polling, (v) => {
    m.polling = v; onda.replaceChildren(ondaSvg(v)); ctx.cambiar();
  });
  const fila = (k, v) => el("div", { class: "fila entre", style: { padding: "7px 0", borderBottom: "1px solid var(--borde)" } },
    el("span", { class: "etiqueta" }, k), el("span", { class: "valor" }, v));

  return {
    nodo: el("div", { class: "rejilla", style: { gridTemplateColumns: "minmax(560px, 2fr) minmax(300px, 1fr)", alignItems: "start" } },
      el("section", { class: "panel" },
        el("div", { class: "panel-cab" }, el("div", { class: "titulo-seccion" }, "Sensibilidad (DPI)"),
          el("span", { class: "nota" }, "Arrastra el dial, usa la rueda o escribe el valor")),
        el("div", { class: "dpi-rejilla" }, tarjetas)),
      el("div", { class: "rejilla" },
        panel("Velocidad de respuesta (polling)", onda, el("div", { style: { marginTop: "14px" } }, seg),
          el("p", { class: "nota", style: { margin: "12px 0 0" } }, "Más Hz = menos retraso, pero más batería.")),
        panel("Información",
          fila("Conexión", ctx.extra.conexion || "—"),
          fila("Etapa DPI actual", m.dpi.actual),
          fila("Respuesta de botones", (m.respuesta_ms ?? "—") + " ms"),
          fila("Batería", ctx.extra.bateria ? `${ctx.extra.bateria.porcentaje} % · ${ctx.extra.bateria.estado}` : "sin aviso todavía")))),
  };
}

// ---------- dibujo del mouse: silueta real del Attack Shark X11 ----------
// Contorno sacado de la transparencia del PNG del usuario (referencias/mouse-recorte.png), borde derecho
// reflejado (es simétrico). Rueda, carcasa, línea de botones, costuras, LED y laterales medidos en el mismo PNG.
// Coordenadas locales: 150 x 286.7, centro x = 75.
const CUERPO = "M63.4 14.0 L86.6 14.0 L86.6 2.0 L90.6 2.0 L94.0 3.7 L98.1 5.3 L102.0 7.0 L105.7 8.6 L109.5 10.3 L113.1 11.9 L116.8 13.6 L120.4 15.2 L123.9 16.9 L127.4 18.5 L130.8 20.2 L134.0 21.8 L136.9 23.5 L139.3 25.1 L141.5 26.8 L143.1 28.4 L144.0 30.1 L144.6 31.8 L145.2 33.4 L145.5 35.1 L145.8 36.7 L146.0 38.4 L146.2 40.0 L146.3 41.7 L146.4 43.3 L146.5 45.0 L146.5 46.6 L146.6 48.3 L146.7 49.9 L146.7 51.6 L146.7 53.2 L146.7 54.9 L146.7 56.5 L146.7 58.2 L146.7 59.9 L146.7 61.5 L146.7 63.2 L146.5 64.8 L146.5 66.5 L146.5 68.1 L146.5 69.8 L146.5 71.4 L146.4 73.1 L146.3 74.7 L146.3 76.4 L146.2 78.0 L146.1 79.7 L146.1 81.3 L146.1 83.0 L145.9 84.6 L145.9 86.3 L145.8 88.0 L145.7 89.6 L145.7 91.3 L145.5 92.9 L145.5 94.6 L145.3 96.2 L145.2 97.9 L145.1 99.5 L145.0 101.2 L145.0 102.8 L144.8 104.5 L144.8 106.1 L144.7 107.8 L144.6 109.4 L144.5 111.1 L144.4 112.7 L144.3 114.4 L144.2 116.0 L144.2 117.7 L144.2 119.4 L144.2 121.0 L144.0 122.7 L144.0 124.3 L144.0 126.0 L144.0 127.6 L144.0 129.3 L144.0 130.9 L144.0 132.6 L144.0 134.2 L144.1 135.9 L144.2 137.5 L144.2 139.2 L144.3 140.8 L144.4 142.5 L144.4 144.1 L144.5 145.8 L144.6 147.5 L144.8 149.1 L144.9 150.8 L145.0 152.4 L145.2 154.1 L145.4 155.7 L145.5 157.4 L145.7 159.0 L145.8 160.7 L146.0 162.3 L146.2 164.0 L146.3 165.6 L146.5 167.3 L146.6 168.9 L146.8 170.6 L146.9 172.2 L147.1 173.9 L147.3 175.6 L147.4 177.2 L147.6 178.9 L147.8 180.5 L148.0 182.2 L148.1 183.8 L148.3 185.5 L148.4 187.1 L148.6 188.8 L148.8 190.4 L148.9 192.1 L149.0 193.7 L149.2 195.4 L149.3 197.0 L149.4 198.7 L149.5 200.3 L149.6 202.0 L149.7 203.7 L149.8 205.3 L149.8 207.0 L149.9 208.6 L150.0 210.3 L150.0 211.9 L149.8 213.6 L149.8 215.2 L149.8 216.9 L149.7 218.5 L149.5 220.2 L149.3 221.8 L149.1 223.5 L148.8 225.1 L148.6 226.8 L148.3 228.4 L147.9 230.1 L147.6 231.8 L147.1 233.4 L146.7 235.1 L146.2 236.7 L145.6 238.4 L145.0 240.0 L144.3 241.7 L143.6 243.3 L143.0 245.0 L142.1 246.6 L141.3 248.3 L140.3 249.9 L139.5 251.6 L138.4 253.2 L137.3 254.9 L136.2 256.5 L135.0 258.2 L133.6 259.9 L132.2 261.5 L130.7 263.2 L129.1 264.8 L127.5 266.5 L125.6 268.1 L123.6 269.8 L121.4 271.4 L119.2 273.1 L116.7 274.7 L113.8 276.4 L110.7 278.0 L107.4 279.7 L103.5 281.3 L98.7 283.0 L92.8 284.6 L84.8 286.3 L75 286.7 L65.2 286.3 L57.2 284.6 L51.3 283.0 L46.5 281.3 L42.6 279.7 L39.3 278.0 L36.2 276.4 L33.3 274.7 L30.8 273.1 L28.6 271.4 L26.4 269.8 L24.4 268.1 L22.5 266.5 L20.9 264.8 L19.3 263.2 L17.8 261.5 L16.4 259.9 L15.0 258.2 L13.8 256.5 L12.7 254.9 L11.6 253.2 L10.5 251.6 L9.7 249.9 L8.7 248.3 L7.9 246.6 L7.0 245.0 L6.4 243.3 L5.7 241.7 L5.0 240.0 L4.4 238.4 L3.8 236.7 L3.3 235.1 L2.9 233.4 L2.4 231.8 L2.1 230.1 L1.7 228.4 L1.4 226.8 L1.2 225.1 L0.9 223.5 L0.7 221.8 L0.5 220.2 L0.3 218.5 L0.2 216.9 L0.2 215.2 L0.2 213.6 L0.0 211.9 L0.0 210.3 L0.1 208.6 L0.2 207.0 L0.2 205.3 L0.3 203.7 L0.4 202.0 L0.5 200.3 L0.6 198.7 L0.7 197.0 L0.8 195.4 L1.0 193.7 L1.1 192.1 L1.2 190.4 L1.4 188.8 L1.6 187.1 L1.7 185.5 L1.9 183.8 L2.0 182.2 L2.2 180.5 L2.4 178.9 L2.6 177.2 L2.7 175.6 L2.9 173.9 L3.1 172.2 L3.2 170.6 L3.4 168.9 L3.5 167.3 L3.7 165.6 L3.8 164.0 L4.0 162.3 L4.2 160.7 L4.3 159.0 L4.5 157.4 L4.6 155.7 L4.8 154.1 L5.0 152.4 L5.1 150.8 L5.2 149.1 L5.4 147.5 L5.5 145.8 L5.6 144.1 L5.6 142.5 L5.7 140.8 L5.8 139.2 L5.8 137.5 L5.9 135.9 L6.0 134.2 L6.0 132.6 L6.0 130.9 L6.0 129.3 L6.0 127.6 L6.0 126.0 L6.0 124.3 L6.0 122.7 L5.8 121.0 L5.8 119.4 L5.8 117.7 L5.8 116.0 L5.7 114.4 L5.6 112.7 L5.5 111.1 L5.4 109.4 L5.3 107.8 L5.2 106.1 L5.2 104.5 L5.0 102.8 L5.0 101.2 L4.9 99.5 L4.8 97.9 L4.7 96.2 L4.5 94.6 L4.5 92.9 L4.3 91.3 L4.3 89.6 L4.2 88.0 L4.1 86.3 L4.1 84.6 L3.9 83.0 L3.9 81.3 L3.9 79.7 L3.8 78.0 L3.7 76.4 L3.7 74.7 L3.6 73.1 L3.5 71.4 L3.5 69.8 L3.5 68.1 L3.5 66.5 L3.5 64.8 L3.3 63.2 L3.3 61.5 L3.3 59.9 L3.3 58.2 L3.3 56.5 L3.3 54.9 L3.3 53.2 L3.3 51.6 L3.3 49.9 L3.4 48.3 L3.5 46.6 L3.5 45.0 L3.6 43.3 L3.7 41.7 L3.8 40.0 L4.0 38.4 L4.2 36.7 L4.5 35.1 L4.8 33.4 L5.4 31.8 L6.0 30.1 L6.9 28.4 L8.5 26.8 L10.7 25.1 L13.1 23.5 L16.0 21.8 L19.2 20.2 L22.6 18.5 L26.1 16.9 L29.6 15.2 L33.2 13.6 L36.9 11.9 L40.5 10.3 L44.3 8.6 L48.0 7.0 L51.9 5.3 L56.0 3.7 L59.4 2.0 L63.4 2.0 Z";
const LINEA_BOTONES = 137.7;
const PARTES = {
  izquierdo: { d: "M63.4 2.0 L59.4 2.0 L56.0 3.7 L51.9 5.3 L48.0 7.0 L44.3 8.6 L40.5 10.3 L36.9 11.9 L33.2 13.6 L29.6 15.2 L26.1 16.9 L22.6 18.5 L19.2 20.2 L16.0 21.8 L13.1 23.5 L10.7 25.1 L9.1 26.8 L9.1 133.2 Q9.1 137.7 13.6 137.7 L74.6 137.7 L74.6 85.1 L63.4 85.1 Z", ancla: [36, 85] },
  derecho: { d: "M86.6 2.0 L90.6 2.0 L94.0 3.7 L98.1 5.3 L102.0 7.0 L105.7 8.6 L109.5 10.3 L113.1 11.9 L116.8 13.6 L120.4 15.2 L123.9 16.9 L127.4 18.5 L130.8 20.2 L134.0 21.8 L136.9 23.5 L139.3 25.1 L140.9 26.8 L140.9 133.2 Q140.9 137.7 136.4 137.7 L75.4 137.7 L75.4 85.1 L86.6 85.1 Z", ancla: [114, 85] },
  medio: { rect: [67.8, 36.1, 14.2, 45.9, 6], ancla: [75, 59.0], clase: "mouse-rueda" },
  "rueda-arriba": { d: "M75 38.1 l4.5 5.5 h-9 Z", ancla: [75, 41.1], clase: "mouse-flecha" },
  "rueda-abajo": { d: "M75 80.0 l4.5 -5.5 h-9 Z", ancla: [75, 77.0], clase: "mouse-flecha" },
  adelante: { rect: [3.5, 96.4, 6.4, 40.3, 2.5], ancla: [3.5, 117.0] },
  atras: { rect: [3.5, 141.5, 6.4, 40.0, 2.5], ancla: [3.5, 161.5] },
  dpi: { rect: [57, 196, 36, 15, 5], ancla: [75, 203], clase: "mouse-debajo" },
};
const DETALLE = { carcasa: [63.4, 14.0, 23.2, 71.1], led: [70.2, 144.4, 9.8, 2.6],
  franjas: [[42.3, 28.5], [79.2, 28.5]] };
const LLAMADAS = {
  izquierdo: ["B1", "izq", 60], adelante: ["B4", "izq", 115], atras: ["B5", "izq", 165],
  "rueda-arriba": ["B7", "der", -8], medio: ["B3", "der", 30], "rueda-abajo": ["B8", "der", 68],
  derecho: ["B2", "der", 110], dpi: ["B6", "der", 210],
};

function dibujoMouse({ llamadas = false, alElegir } = {}) {
  // con llamadas el mouse va más grande (escala 1.2) para que se lea mejor
  const POS = llamadas ? { x: 182.5, y: -22, e: 1.3 } : { x: 205, y: 30, e: 1 };
  const partes = Object.entries(PARTES).map(([id, p]) => {
    const clase = `mouse-parte ${p.clase || ""}`;
    return p.rect
      ? `<rect class="${clase}" data-id="${id}" x="${p.rect[0]}" y="${p.rect[1]}" width="${p.rect[2]}" height="${p.rect[3]}" rx="${p.rect[4]}"><title>${id === "dpi" ? "Botón DPI (está debajo del mouse)" : id}</title></rect>`
      : `<path class="${clase}" data-id="${id}" d="${p.d}"/>`;
  }).join("");
  let notas = "";
  if (llamadas) {
    notas = Object.entries(LLAMADAS).map(([id, [txt, lado, y]]) => {
      const [ax, ay] = PARTES[id].ancla, gx = ax * POS.e + POS.x, gy = ay * POS.e + POS.y;
      const bx = lado === "izq" ? 40 : 486, cy = y + 11;
      const sx = lado === "izq" ? 74 : 486, mx = lado === "izq" ? 150 : 410;
      return `<g class="llamada" data-id="${id}">
        <polyline points="${sx},${cy} ${mx},${cy} ${gx},${gy}"/>
        <circle cx="${gx}" cy="${gy}" r="2.5" fill="#6d84ad"/>
        <rect x="${bx}" y="${y}" width="34" height="22" rx="3"/>
        <text x="${bx + 17}" y="${y + 15}" text-anchor="middle">${txt}</text></g>`;
    }).join("");
  }
  const caja = llamadas ? "30 -32 500 392" : "170 14 220 312";
  const s = svg(`<svg class="mouse-svg" viewBox="${caja}" style="max-width:${llamadas ? 600 : 230}px">
    <defs>
      <linearGradient id="gradCuerpo" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="#c9ccd2"/><stop offset=".18" stop-color="#eef0f3"/><stop offset=".5" stop-color="#fbfbfc"/>
        <stop offset=".82" stop-color="#eceef1"/><stop offset="1" stop-color="#c3c6cc"/></linearGradient>
      <radialGradient id="gradJoroba" cx="50%" cy="62%" r="55%"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
      <linearGradient id="gradRueda" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0c0c0e"/><stop offset=".5" stop-color="#3a3b40"/><stop offset="1" stop-color="#0c0c0e"/></linearGradient>
    </defs>
    ${notas}
    <g transform="translate(${POS.x} ${POS.y}) scale(${POS.e})">
      <path class="mouse-cuerpo" d="${CUERPO}"/>
      <ellipse cx="75" cy="188" rx="56" ry="72" fill="url(#gradJoroba)" pointer-events="none"/>
      <rect x="${DETALLE.carcasa[0]}" y="${DETALLE.carcasa[1]}" width="${DETALLE.carcasa[2]}" height="${DETALLE.carcasa[3]}" rx="6" fill="#e4e6ea" stroke="#3a3b40" stroke-width=".8" pointer-events="none"/>
      ${partes}
      <g stroke="#55565c" stroke-width="1.4" pointer-events="none">${Array.from({ length: 9 }, (_, i) => 44 + i * 4.2).map((y) => `<line x1="69.5" y1="${y}" x2="80.5" y2="${y}"/>`).join("")}</g>
      <line x1="140.9" y1="25" x2="140.9" y2="133.7" stroke="#3a3b40" stroke-width=".9" pointer-events="none"/>
      <line x1="9.1" y1="25" x2="9.1" y2="133.7" stroke="#3a3b40" stroke-width=".9" pointer-events="none"/>
      ${DETALLE.franjas.map(([x, w]) => `<rect class="brillo-mouse franja" x="${x}" y="${LINEA_BOTONES - 0.9}" width="${w}" height="1.8" rx=".9" fill="var(--c, #3aa0ff)"/>`).join("")}
      <rect class="brillo-mouse led" x="${DETALLE.led[0]}" y="${DETALLE.led[1]}" width="${DETALLE.led[2]}" height="${DETALLE.led[3]}" rx="1.3" fill="var(--c, #3aa0ff)"/>
      <text x="75" y="224" text-anchor="middle" fill="#9a9ea6" font-size="7" letter-spacing="1.4" pointer-events="none">${llamadas ? "DPI · DEBAJO" : ""}</text>
    </g></svg>`);
  if (alElegir) {
    s.addEventListener("click", (e) => {
      const g = e.target.closest("[data-id]");
      if (g) alElegir(g.dataset.id, g);
    });
  }
  s.marcar = (id) => s.querySelectorAll("[data-id]").forEach((n) => n.classList.toggle("sel", n.dataset.id === id));
  return s;
}

// ---------- ILUMINACIÓN ----------
const ICONO_MODO = {
  0: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="8"/><path d="M6 6l12 12"/></svg>',
  1: '<svg viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="7"/></svg>',
  2: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12c3-8 6-8 10 0s7 8 10 0"/></svg>',
  3: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12a8 8 0 0116 0"/><path d="M8 12a4 4 0 018 0"/></svg>',
  4: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12c3-8 6-8 10 0s7 8 10 0"/><circle cx="12" cy="12" r="2" fill="currentColor"/></svg>',
  5: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="7" y="3" width="10" height="18" rx="5"/><path d="M12 7v3"/></svg>',
  6: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="7" y="3" width="10" height="18" rx="5"/><path d="M12 7v3M3 12h2M19 12h2"/></svg>',
};
const CON_COLOR = new Set([1, 2]);
const CON_VELOCIDAD = new Set([2, 3, 4, 6]);

function colorDeEtapa(m) {
  return m.dpi.etapas.find((e) => e.numero === m.dpi.actual)?.color || "#ff5a1a";
}

function iluminacion(ctx) {
  const m = ctx.edit;
  const escena = el("div", { class: "escena", style: { minHeight: "360px", padding: "12px 0" } });
  const glow = el("div", { style: {
    position: "absolute", width: "230px", height: "120px", borderRadius: "50%", left: "50%", top: "50%",
    transform: "translate(-50%, -48%)", filter: "blur(38px)", willChange: "opacity, transform", pointerEvents: "none" } });
  glow.className = "brillo-mouse";
  const dibujo = dibujoMouse();
  escena.append(glow, dibujo);

  function pintarLuz() {
    const l = m.luz;
    const color = l.modo === 5 || l.modo === 6 ? colorDeEtapa(m) : l.color;
    escena.className = `escena luz-${l.modo}`;
    escena.style.setProperty("--c", color);
    escena.style.setProperty("--b", (0.15 + 0.5 * (l.brillo / 8)).toFixed(2));
    escena.style.setProperty("--vel", (6 - l.velocidad) * 0.9 + 0.6);
    const arcoiris = l.modo === 3 || l.modo === 4;
    glow.style.background = arcoiris ? "conic-gradient(from 0deg, #f00, #ff0, #0f0, #0ff, #00f, #f0f, #f00)" : color;
    glow.style.opacity = l.modo === 0 ? 0 : l.modo === 1 || l.modo === 5 ? "var(--b)" : "";
    dibujo.querySelectorAll(".franja, .led").forEach((n) => { n.style.fill = arcoiris ? "#ff4fd8" : color; });
    // neón: el arcoíris gira (solo transform y opacity: lo hace la GPU)
    const t = ((6 - l.velocidad) * 0.9 + 0.6).toFixed(2);
    glow.style.animation = l.modo === 3 ? `girar-centro ${t * 2}s linear infinite`
      : l.modo === 4 ? `girar-centro ${t * 2}s linear infinite, respirar ${t}s ease-in-out infinite` : "";
    selColor.habilitar(CON_COLOR.has(l.modo));
    vel.habilitar(CON_VELOCIDAD.has(l.modo));
    brillo.habilitar(l.modo !== 0);
    lista.querySelectorAll(".item").forEach((n) => n.classList.toggle("activo", Number(n.dataset.id) === l.modo));
  }

  const lista = el("div", { class: "lista" }, ctx.catalogo.modos_luz.map((modo) =>
    el("div", { class: "item", "data-id": modo.id, tabindex: 0,
      onclick: () => { m.luz.modo = modo.id; pintarLuz(); ctx.cambiar(); } },
      el("span", { class: "item-icono", html: ICONO_MODO[modo.id] }), modo.nombre)));

  const selColor = selectorColor(m.luz.color, (c) => { m.luz.color = c; pintarLuz(); ctx.cambiar(); },
    ctx.preferencias.historial_colores || []);
  selColor.addEventListener("historial", (e) => {
    ctx.preferencias.historial_colores = e.detail;
    ctx.api("guardar_preferencias", { historial_colores: e.detail });
  });
  const presets = el("div", { class: "muestras", style: { marginBottom: "12px" } },
    Object.entries(ctx.catalogo.colores).map(([n, c]) => el("button", { class: "muestra", title: n, style: { background: c },
      onclick: () => { m.luz.color = c; selColor.poner(c); pintarLuz(); ctx.cambiar(); } })));
  const brillo = deslizador({ etiqueta: "Brillo", min: 1, max: 8, valor: m.luz.brillo, formato: (v) => `${v}/8`,
    alCambiar: (v) => { m.luz.brillo = v; pintarLuz(); ctx.cambiar(); } });
  const vel = deslizador({ etiqueta: "Velocidad", min: 1, max: 5, valor: m.luz.velocidad, formato: (v) => `${v}/5`,
    alCambiar: (v) => { m.luz.velocidad = v; pintarLuz(); ctx.cambiar(); } });

  requestAnimationFrame(pintarLuz);
  return {
    nodo: el("div", { class: "rejilla", style: { gridTemplateColumns: "250px minmax(360px, 1fr) 300px", alignItems: "start" } },
      panel("Efectos", lista),
      el("div", { class: "rejilla" },
        el("section", { class: "panel", style: { padding: 0, overflow: "hidden", isolation: "isolate" } }, escena,
          el("div", { class: "nota", style: { padding: "0 16px 14px" } }, "Vista previa aproximada · la luz de la base de carga se maneja con su botón físico")),
        el("section", { class: "panel" }, el("div", { class: "titulo-seccion" }, "Ajustes"),
          el("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px" } }, brillo, vel))),
      panel("Color", presets, selColor)),
  };
}

// ---------- BOTONES ----------
const GRUPOS = [
  ["Mouse", ["clic-izq", "clic-der", "clic-medio", "atras", "adelante", "doble-clic", "disparo", "rueda-arriba", "rueda-abajo", "desactivar"]],
  ["DPI y rendimiento", ["dpi-ciclo", "dpi-mas", "dpi-menos", "francotirador", "polling-ciclo"]],
  ["Multimedia", ["reproductor", "play-pausa", "siguiente", "anterior", "detener", "volumen-mas", "volumen-menos", "silenciar"]],
  ["Sistema", ["inicio", "calculadora", "correo", "mi-pc", "luz-ciclo", "luz-on-off", "perfil-ciclo"]],
  ["Navegador", ["navegador-atras", "navegador-adelante", "navegador-recargar"]],
];
const TECLAS_JS = {
  Enter: "enter", Escape: "esc", Backspace: "borrar", Tab: "tab", Space: "espacio", Minus: "-", Equal: "=",
  BracketLeft: "[", BracketRight: "]", Backslash: "\\", Semicolon: ";", Quote: "'", Backquote: "`", Comma: ",",
  Period: ".", Slash: "/", CapsLock: "bloqmayus", PrintScreen: "imprpant", Pause: "pausa", Insert: "insert",
  Home: "inicio", PageUp: "repag", Delete: "supr", End: "fin", PageDown: "avpag", ArrowRight: "derecha",
  ArrowLeft: "izquierda", ArrowDown: "abajo", ArrowUp: "arriba",
};
const MODS_JS = { ControlLeft: "ctrl", ControlRight: "ctrl", ShiftLeft: "shift", ShiftRight: "shift", AltLeft: "alt", AltRight: "alt", MetaLeft: "win", MetaRight: "win" };
export function teclaDeEvento(e) {
  if (MODS_JS[e.code]) return MODS_JS[e.code];
  if (/^Key[A-Z]$/.test(e.code)) return e.code.slice(3).toLowerCase();
  if (/^Digit\d$/.test(e.code)) return e.code.slice(5);
  if (/^F([1-9]|1[0-2])$/.test(e.code)) return e.code.toLowerCase();
  return TECLAS_JS[e.code] || null;
}

function textoAccion(id, catalogo) {
  if (id.startsWith("tecla:")) return "Tecla " + id.slice(6).toUpperCase();
  if (id.startsWith("macro:")) return "Macro " + id.slice(6);
  return catalogo.acciones.find((a) => a.id === id)?.nombre || id;
}

function selectorAccion(ancla, actual, catalogo, alElegir) {
  const busca = el("input", { class: "campo", placeholder: "Buscar acción…", spellcheck: "false" });
  const lista = el("div", { class: "popover-lista" });
  const nombres = Object.fromEntries(catalogo.acciones.map((a) => [a.id, a.nombre]));
  const captura = el("div", { class: "captura", tabindex: 0 }, "Atajo de teclado: haz clic y presiona la combinación");
  let escuchando = false, mods = new Set();
  const finCaptura = () => { escuchando = false; captura.classList.remove("escuchando"); removeEventListener("keydown", tecla, true); };
  function tecla(e) {
    e.preventDefault(); e.stopPropagation();
    const t = teclaDeEvento(e);
    if (!t) return;
    if (["ctrl", "shift", "alt", "win"].includes(t)) { mods.add(t); captura.textContent = [...mods].join(" + ").toUpperCase() + " + …"; return; }
    finCaptura();
    alElegir("tecla:" + [...mods, t].join("+"));
    cerrarPopover();
  }
  captura.addEventListener("click", () => {
    if (escuchando) return;
    escuchando = true; mods = new Set(); captura.classList.add("escuchando"); captura.textContent = "Escuchando… presiona la combinación";
    addEventListener("keydown", tecla, true);
  });

  function pintar(filtro = "") {
    const f = filtro.trim().toLowerCase();
    const bloques = [];
    for (const [grupo, ids] of [...GRUPOS, ["Macros", Array.from({ length: 8 }, (_, i) => `macro:${i + 1}`)]]) {
      const vis = ids.filter((id) => !f || (nombres[id] || id).toLowerCase().includes(f) || id.includes(f));
      if (!vis.length) continue;
      bloques.push(el("div", { class: "grupo" }, grupo));
      for (const id of vis) {
        bloques.push(el("div", { class: `opcion ${id === actual ? "activa" : ""}`, onclick: () => { alElegir(id); cerrarPopover(); } },
          el("span", {}, nombres[id] || textoAccion(id, catalogo)), el("small", {}, id === actual ? "actual" : "")));
      }
    }
    lista.replaceChildren(el("div", { class: "grupo" }, "Atajo de teclado"), captura, ...bloques);
  }
  busca.addEventListener("input", () => pintar(busca.value));
  pintar();
  const p = abrirPopover(ancla, el("div", { style: { display: "contents" } }, el("div", { class: "popover-busca" }, busca), lista));
  busca.focus();
  const obs = new MutationObserver(() => { if (!p.isConnected) { finCaptura(); obs.disconnect(); } });
  obs.observe(document.body, { childList: true });
}

function botones(ctx) {
  const m = ctx.edit;
  let sel = null;
  const dibujo = dibujoMouse({ llamadas: true, alElegir: (id, nodo) => elegir(id, filas[id] || nodo) });
  const filas = {};
  const tabla = el("div", { class: "acciones-tabla" }, ctx.catalogo.botones.map((b) => {
    const fila = el("div", { class: "accion-fila", "data-id": b.id, tabindex: 0,
      onclick: () => elegir(b.id, fila), onmouseenter: () => dibujo.marcar(b.id), onmouseleave: () => dibujo.marcar(sel),
      onkeydown: (e) => e.key === "Enter" && elegir(b.id, fila) },
      el("div", { class: "nombre" }, b.nombre),
      el("div", { class: "asignada" }, el("span", {})));
    filas[b.id] = fila;
    return fila;
  }));
  function pintarFilas() {
    for (const [id, fila] of Object.entries(filas)) {
      fila.querySelector(".asignada span").textContent = textoAccion(m.botones[id].id, ctx.catalogo);
      fila.classList.toggle("cambiada", m.botones[id].id !== ctx.base.botones[id].id);
      fila.classList.toggle("sel", id === sel);
    }
  }
  function elegir(id, ancla) {
    sel = id; dibujo.marcar(id); pintarFilas();
    selectorAccion(ancla.querySelector?.(".asignada") || ancla, m.botones[id].id, ctx.catalogo, (accion) => {
      m.botones[id] = { id: accion, texto: textoAccion(accion, ctx.catalogo) };
      pintarFilas(); ctx.cambiar();
    });
  }
  pintarFilas();

  const restaurar = el("button", { class: "boton chico peligro", style: { marginTop: "14px", width: "100%" }, onclick: async () => {
    restaurar.disabled = true;
    const r = await ctx.api("mouse_restaurar_botones");
    restaurar.disabled = false;
    if (r.ok) { aviso("Botones de fábrica restaurados.", "ok"); ctx.recargar(); } else aviso(r.error, "error");
  } }, "Restaurar botones de fábrica");

  return {
    nodo: el("div", { class: "rejilla", style: { gridTemplateColumns: "300px minmax(280px, 1fr) 290px", alignItems: "start" } },
      panel("Acciones", tabla, restaurar),
      el("section", { class: "panel" }, el("div", { class: "escena" }, dibujo),
        el("div", { class: "nota", style: { textAlign: "center" } }, "Haz clic en un botón del mouse o en la lista para cambiar su acción")),
      editorMacros(ctx)),
  };
}

// ---------- editor de macros (con grabadora) ----------
function editorMacros(ctx) {
  const numero = el("select", { class: "campo" }, Array.from({ length: 8 }, (_, i) => el("option", { value: i + 1 }, `Macro ${i + 1}`)));
  const texto = el("textarea", { class: "campo", rows: 4, spellcheck: "false", placeholder: "ej.  ctrl+c 100ms ctrl+v",
    style: { resize: "vertical", fontFamily: "Consolas, monospace", fontSize: "12.5px" } });
  const boton = el("select", { class: "campo" }, el("option", { value: "" }, "No asignar"),
    ctx.catalogo.botones.filter((b) => b.id !== "izquierdo").map((b) => el("option", { value: b.id }, b.nombre)));
  let modo = "veces";
  const veces = deslizador({ etiqueta: "Repeticiones", min: 1, max: 20, valor: 1, alCambiar: () => {} });
  const seg = segmento([["veces", "Veces"], ["mientras", "Mantener"], ["hasta-tecla", "Hasta tecla"]], modo, (v) => {
    modo = v; veces.habilitar(v === "veces");
  });

  // grabadora: guarda pulsaciones con sus tiempos
  let grabando = false, pasos = [], ultimo = 0;
  const grabar = el("button", { class: "boton chico", onclick: () => (grabando ? parar() : empezar()) }, "● Grabar");
  function reg(e, soltar) {
    if (!grabando) return;
    e.preventDefault(); e.stopPropagation();
    if (e.repeat) return;
    const t = teclaDeEvento(e);
    if (!t) return;
    const ahora = performance.now();
    if (pasos.length) pasos[pasos.length - 1].espera = Math.max(10, Math.round((ahora - ultimo) / 10) * 10);
    ultimo = ahora;
    pasos.push({ t: (soltar ? "-" : "+") + t, espera: 30 });
    texto.value = pasos.map((p) => p.t + (p.espera !== 30 ? ` ${p.espera}ms` : "")).join(" ");
  }
  const abajo = (e) => reg(e, false), arriba = (e) => reg(e, true);
  function empezar() {
    grabando = true; pasos = []; texto.value = "";
    grabar.textContent = "■ Detener"; grabar.classList.add("primario");
    addEventListener("keydown", abajo, true); addEventListener("keyup", arriba, true);
  }
  function parar() {
    grabando = false; grabar.textContent = "● Grabar"; grabar.classList.remove("primario");
    removeEventListener("keydown", abajo, true); removeEventListener("keyup", arriba, true);
  }

  const guardar = el("button", { class: "boton primario", style: { width: "100%", marginTop: "14px" }, onclick: async () => {
    if (grabando) parar();
    if (!texto.value.trim()) return aviso("Escribe o graba la secuencia de la macro.", "info");
    guardar.disabled = true; guardar.innerHTML = '<span class="girando"></span>Guardando';
    const r = await ctx.api("mouse_macro", Number(numero.value), texto.value, modo, veces.querySelector("input").valueAsNumber, boton.value || null);
    guardar.disabled = false; guardar.textContent = "Guardar macro";
    if (!r.ok) return aviso(r.error, "error");
    aviso(`Macro ${numero.value} guardada${boton.value ? " y asignada" : ""}.`, "ok");
    if (boton.value) ctx.recargar();
  } }, "Guardar macro");

  const sec = el("section", { class: "panel" },
    el("div", { class: "panel-cab" }, el("div", { class: "titulo-seccion" }, "Macros"), grabar),
    el("div", { class: "rejilla", style: { gap: "10px" } },
      numero, texto,
      el("div", { class: "nota" }, "a = tecla · ctrl+c = combinación · +shift / -shift = pulsar / soltar · clic-izq · 200ms = espera"),
      seg, veces,
      el("div", { class: "etiqueta", style: { marginTop: "6px" } }, "Asignar al botón"), boton),
    guardar);
  return sec;
}

// ---------- ENERGÍA ----------
function anilloBateria(pct) {
  const r = 60, l = 2 * Math.PI * r;
  return svg(`<svg class="anillo-bat" viewBox="0 0 150 150">
    <circle class="fondo-a" cx="75" cy="75" r="${r}"/>
    <circle class="valor-a" cx="75" cy="75" r="${r}" stroke-dasharray="${l}" stroke-dashoffset="${pct == null ? l : l * (1 - pct / 100)}"/>
    <text x="75" y="80" text-anchor="middle" fill="#e8e8ea" font-size="24" font-weight="700">${pct == null ? "—" : pct + "%"}</text>
    <text x="75" y="100" text-anchor="middle" fill="#8b8c94" font-size="9" letter-spacing="2">BATERÍA</text></svg>`);
}

function energia(ctx) {
  const m = ctx.edit;
  const normal = deslizador({ etiqueta: "Suspensión", min: 0.5, max: 30, paso: 0.5, valor: m.suspension.normal,
    formato: (v) => (v < 1 ? "30 s" : `${v} min`), marcas: ["30 s", "10 min", "20 min", "30 min"],
    alCambiar: (v) => { m.suspension.normal = v; ctx.cambiar(); } });
  const profunda = deslizador({ etiqueta: "Suspensión profunda", min: 1, max: 60, valor: m.suspension.profunda,
    formato: (v) => `${v} min`, marcas: ["1", "20", "40", "60 min"],
    alCambiar: (v) => { m.suspension.profunda = v; ctx.cambiar(); } });
  const b = ctx.extra.bateria;
  return {
    nodo: el("div", { class: "rejilla", style: { gridTemplateColumns: "minmax(420px, 1.4fr) minmax(280px, 1fr)", alignItems: "start" } },
      panel("Ahorro de energía", normal, profunda,
        el("p", { class: "nota", style: { marginTop: "14px" } },
          "Con el dongle, un mouse dormido no responde a ATKHUB. Si lo usas mucho desde aquí, sube la suspensión normal a unos minutos.")),
      el("section", { class: "panel", style: { display: "grid", justifyItems: "center", gap: "8px" } },
        el("div", { class: "panel-cab", style: { width: "100%" } }, el("div", { class: "titulo-seccion" }, "Batería")),
        anilloBateria(b?.porcentaje ?? null),
        el("div", { class: "nota" }, b ? b.estado : "El mouse avisa la batería cada cierto tiempo"))),
  };
}
