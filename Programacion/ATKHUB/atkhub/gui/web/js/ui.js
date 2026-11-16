// Componentes de la interfaz. Sin librerías: DOM + SVG + CSS.
// Regla de rendimiento: se construye el DOM una vez y luego solo se actualizan valores.

export function el(etiqueta, props = {}, ...hijos) {
  const n = etiqueta.startsWith("svg:")
    ? document.createElementNS("http://www.w3.org/2000/svg", etiqueta.slice(4))
    : document.createElement(etiqueta);
  for (const [k, v] of Object.entries(props || {})) {
    if (v == null || v === false) continue;
    if (k === "class") n.setAttribute("class", v);
    else if (k === "style" && typeof v === "object") Object.assign(n.style, v);
    else if (k.startsWith("on")) n.addEventListener(k.slice(2), v);
    else if (k === "html") n.innerHTML = v;
    else n.setAttribute(k, v === true ? "" : v);
  }
  for (const h of hijos.flat()) {
    if (h == null || h === false) continue;
    n.append(h instanceof Node ? h : document.createTextNode(String(h)));
  }
  return n;
}

export function svg(markup) {
  const t = document.createElement("template");
  t.innerHTML = markup.trim();
  return t.content.firstElementChild;
}

export const debounce = (fn, ms) => {
  let t;
  return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); };
};

export function panel(titulo, ...hijos) {
  return el("section", { class: "panel" },
    el("div", { class: "panel-cab" }, el("div", { class: "titulo-seccion" }, titulo)),
    ...hijos);
}

// ---------- avisos ----------
const ICONOS = {
  ok: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#3ddc84" stroke-width="2.5"><path d="M5 12l5 5 9-10"/></svg>',
  error: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ff4d4f" stroke-width="2.5"><path d="M12 7v6M12 17h.01"/><circle cx="12" cy="12" r="10"/></svg>',
  info: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ff5a1a" stroke-width="2.5"><path d="M12 11v6M12 7h.01"/><circle cx="12" cy="12" r="10"/></svg>',
};
export function aviso(texto, tipo = "info", ms = 3800) {
  const caja = document.querySelector(".avisos");
  const a = el("div", { class: `aviso ${tipo}`, role: "status" }, el("span", { html: ICONOS[tipo] }), el("div", {}, texto));
  caja.append(a);
  const quitar = () => { a.classList.add("fuera"); a.addEventListener("animationend", () => a.remove(), { once: true }); };
  setTimeout(quitar, tipo === "error" ? ms + 2500 : ms);
  a.addEventListener("click", quitar);
}

// ---------- modal de confirmación ----------
export function confirmar(titulo, texto, aceptar = "Continuar") {
  return new Promise((res) => {
    const cerrar = (v) => { velo.remove(); res(v); };
    const velo = el("div", { class: "velo", onclick: (e) => e.target === velo && cerrar(false) },
      el("div", { class: "modal", role: "dialog" },
        el("h3", {}, titulo), el("p", {}, texto),
        el("div", { class: "fila" },
          el("button", { class: "boton", onclick: () => cerrar(false) }, "Cancelar"),
          el("button", { class: "boton primario", onclick: () => cerrar(true) }, aceptar))));
    document.body.append(velo);
    velo.querySelector(".primario").focus();
    velo.addEventListener("keydown", (e) => { if (e.key === "Escape") cerrar(false); });
  });
}

// ---------- pestañas / segmentos con indicador deslizante ----------
function moverIndicador(ind, boton) {
  if (!boton) return;
  ind.style.width = boton.offsetWidth + "px";
  ind.style.transform = `translateX(${boton.offsetLeft}px)`;
}

export function pestanas(opciones, alCambiar, clase = "pestanas", claseBoton = "pestana", claseInd = "pestanas-indicador") {
  const ind = el("div", { class: claseInd });
  const botones = opciones.map(([id, texto]) =>
    el("button", { class: claseBoton, "data-id": id, onclick: () => elegir(id, true) }, texto));
  const caja = el("div", { class: clase, role: "tablist" }, ind, ...botones);
  let actual = null;
  function elegir(id, avisar) {
    if (id === actual && avisar) return;
    actual = id;
    const claseActiva = claseBoton === "pestana" ? "activa" : "activo";
    for (const b of botones) b.classList.toggle(claseActiva, b.dataset.id === String(id));
    moverIndicador(ind, botones.find((b) => b.dataset.id === String(id)));
    if (avisar) alCambiar(id);
  }
  // recolocar cuando el componente ya tiene tamaño
  new ResizeObserver(() => moverIndicador(ind, botones.find((b) => b.dataset.id === String(actual)))).observe(caja);
  caja.elegir = (id) => elegir(id, false);
  return caja;
}

export function segmento(opciones, valor, alCambiar) {
  const s = pestanas(opciones.map((o) => [String(o[0]), o[1]]), (id) => {
    const o = opciones.find((x) => String(x[0]) === id);
    alCambiar(o[0]);
  }, "segmento", "seg-btn", "seg-ind");
  requestAnimationFrame(() => s.elegir(String(valor)));
  s.poner = (v) => s.elegir(String(v));
  return s;
}

// ---------- deslizador ----------
export function deslizador({ etiqueta, min, max, paso = 1, valor, formato = (v) => v, marcas, alCambiar }) {
  const salida = el("span", { class: "valor" });
  const input = el("input", { type: "range", min, max, step: paso, value: valor, "aria-label": etiqueta });
  const pintar = () => {
    const p = ((input.value - min) / (max - min)) * 100;
    input.style.setProperty("--p", p + "%");
    salida.textContent = formato(Number(input.value));
  };
  input.addEventListener("input", () => { pintar(); alCambiar(Number(input.value)); });
  const caja = el("div", { class: "deslizador" },
    el("div", { class: "fila entre" }, el("span", { class: "etiqueta" }, etiqueta), salida),
    input,
    marcas ? el("div", { class: "marcas" }, ...marcas.map((m) => el("span", {}, m))) : null);
  pintar();
  caja.poner = (v) => { input.value = v; pintar(); };
  caja.habilitar = (si) => { input.disabled = !si; caja.style.opacity = si ? "" : ".4"; };
  return caja;
}

export function interruptor(texto, valor, alCambiar) {
  const input = el("input", { type: "checkbox" });
  input.checked = valor;
  input.addEventListener("change", () => alCambiar(input.checked));
  const l = el("label", { class: "interruptor" }, input, el("span", { class: "pista" }), el("span", {}, texto));
  l.poner = (v) => { input.checked = v; };
  return l;
}

// ---------- dial de DPI (como el "medidor" de SteelSeries) ----------
const DIAL_MIN = 50, DIAL_MAX = 22000, BARRIDO = 270, R = 58, C = 75;
const LARGO_ARCO = (2 * Math.PI * R * BARRIDO) / 360;
const aT = (v) => Math.sqrt((v - DIAL_MIN) / (DIAL_MAX - DIAL_MIN));          // escala suave: más precisión abajo
const deT = (t) => DIAL_MIN + (DIAL_MAX - DIAL_MIN) * t * t;
export const redondearDpi = (v) => {
  v = Math.max(DIAL_MIN, Math.min(DIAL_MAX, v));
  return v <= 10000 ? Math.round(v / 50) * 50 : Math.round(v / 100) * 100;
};

export function dialDpi(valor, alCambiar) {
  const marcas = [];
  for (let i = 0; i <= 18; i++) {
    const ang = (135 + (BARRIDO * i) / 18) * Math.PI / 180;
    const r1 = i % 3 === 0 ? 66 : 68, r2 = 72;
    marcas.push(`<line x1="${C + r1 * Math.cos(ang)}" y1="${C + r1 * Math.sin(ang)}" x2="${C + r2 * Math.cos(ang)}" y2="${C + r2 * Math.sin(ang)}" stroke="${i % 3 === 0 ? "#6a6b73" : "#3a3b42"}" stroke-width="1.5"/>`);
  }
  const arco = `M ${C + R * Math.cos(135 * Math.PI / 180)} ${C + R * Math.sin(135 * Math.PI / 180)} A ${R} ${R} 0 1 1 ${C + R * Math.cos(45 * Math.PI / 180)} ${C + R * Math.sin(45 * Math.PI / 180)}`;
  const s = svg(`<svg class="dial" viewBox="0 0 150 150" role="slider" aria-label="DPI" tabindex="0">
    <defs><radialGradient id="gDial" cx="50%" cy="40%"><stop offset="0" stop-color="#26272c"/><stop offset="1" stop-color="#141518"/></radialGradient></defs>
    <circle cx="75" cy="75" r="46" fill="url(#gDial)" stroke="#2f3036"/>
    ${marcas.join("")}
    <path class="dial-pista" d="${arco}" fill="none" stroke-width="9" stroke-linecap="round"/>
    <path class="dial-valor" d="${arco}" fill="none" stroke-width="9" stroke-linecap="round" stroke-dasharray="${LARGO_ARCO}" stroke-dashoffset="${LARGO_ARCO}"/>
    <g class="dial-aguja"><line x1="75" y1="75" x2="75" y2="36" stroke="#ff6a33" stroke-width="2.5" stroke-linecap="round"/></g>
    <circle cx="75" cy="75" r="6" fill="#e9e9ec" stroke="#141518" stroke-width="2"/>
    <text x="75" y="100" text-anchor="middle" fill="#ff6a33" font-size="10" font-weight="700" letter-spacing="1.5">DPI</text>
  </svg>`);
  const val = s.querySelector(".dial-valor"), aguja = s.querySelector(".dial-aguja");
  const entrada = el("input", { class: "dial-entrada", inputmode: "numeric", "aria-label": "Valor DPI" });
  let v = valor;
  function pintar() {
    const t = aT(v);
    val.style.strokeDashoffset = LARGO_ARCO * (1 - t);
    aguja.style.transform = `rotate(${-135 + BARRIDO * t}deg)`;
    if (document.activeElement !== entrada) entrada.value = v;
    s.setAttribute("aria-valuenow", v);
  }
  function poner(nv, avisar) {
    nv = redondearDpi(nv);
    if (nv === v) return;
    v = nv; pintar();
    if (avisar) alCambiar(v);
  }
  function desdePuntero(e) {
    const r = s.getBoundingClientRect();
    let ang = Math.atan2(e.clientY - (r.top + r.height / 2), e.clientX - (r.left + r.width / 2)) * 180 / Math.PI;
    ang = (ang - 135 + 360) % 360;
    if (ang > BARRIDO) ang = ang > BARRIDO + (360 - BARRIDO) / 2 ? 0 : BARRIDO;
    poner(deT(ang / BARRIDO), true);
  }
  let pendiente = null;
  s.addEventListener("pointerdown", (e) => {
    s.setPointerCapture(e.pointerId); s.classList.add("arrastrando"); desdePuntero(e);
  });
  s.addEventListener("pointermove", (e) => {
    if (!s.classList.contains("arrastrando")) return;
    // a lo sumo un cálculo por cuadro
    pendiente = e;
    requestAnimationFrame(() => { if (pendiente) { desdePuntero(pendiente); pendiente = null; } });
  });
  const soltar = () => s.classList.remove("arrastrando");
  s.addEventListener("pointerup", soltar);
  s.addEventListener("pointercancel", soltar);
  s.addEventListener("wheel", (e) => { e.preventDefault(); poner(v + (e.deltaY < 0 ? 1 : -1) * (v < 10000 ? 50 : 100), true); }, { passive: false });
  s.addEventListener("keydown", (e) => {
    const d = { ArrowUp: 1, ArrowRight: 1, ArrowDown: -1, ArrowLeft: -1 }[e.key];
    if (d) { e.preventDefault(); poner(v + d * (e.shiftKey ? 500 : 50), true); }
  });
  const confirmarEntrada = () => { const n = parseInt(entrada.value, 10); if (!isNaN(n)) poner(n, true); entrada.value = v; };
  entrada.addEventListener("change", confirmarEntrada);
  entrada.addEventListener("keydown", (e) => { if (e.key === "Enter") entrada.blur(); });
  requestAnimationFrame(pintar);
  return { svg: s, entrada, poner: (nv) => poner(nv, false) };
}

// ---------- selector de color (cuadro SV + matiz + hex + historial) ----------
export function hexARgb(h) { const n = parseInt(h.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; }
export function rgbAHex(r, g, b) { return "#" + [r, g, b].map((x) => Math.round(x).toString(16).padStart(2, "0")).join("").toUpperCase(); }
function rgbAHsv(r, g, b) {
  r /= 255; g /= 255; b /= 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b), d = max - min;
  let h = 0;
  if (d) h = max === r ? ((g - b) / d) % 6 : max === g ? (b - r) / d + 2 : (r - g) / d + 4;
  return [(h * 60 + 360) % 360, max ? d / max : 0, max];
}
function hsvARgb(h, s, v) {
  const f = (n) => { const k = (n + h / 60) % 6; return v - v * s * Math.max(0, Math.min(k, 4 - k, 1)); };
  return [f(5) * 255, f(3) * 255, f(1) * 255];
}

export function selectorColor(valor, alCambiar, historial = []) {
  let [h, s, v] = rgbAHsv(...hexARgb(valor));
  const tirSv = el("div", { class: "tirador" }), tirH = el("div", { class: "tirador" });
  const sv = el("div", { class: "sv" }, tirSv), matiz = el("div", { class: "matiz" }, tirH);
  const muestra = el("div", { class: "hex-muestra" });
  const hex = el("input", { class: "campo", maxlength: 7, spellcheck: "false", "aria-label": "Color hex" });
  const caja = el("div", { class: "muestras" });
  const hist = [...historial];
  let actual = valor;

  function pintar(avisar) {
    const [r, g, b] = hsvARgb(h, s, v);
    actual = rgbAHex(r, g, b);
    sv.style.setProperty("--matiz", `hsl(${h} 100% 50%)`);
    tirSv.style.transform = `translate(${s * sv.clientWidth}px, ${(1 - v) * sv.clientHeight}px)`;
    tirH.style.transform = `translateX(${(h / 360) * matiz.clientWidth}px)`;
    muestra.style.background = actual;
    if (document.activeElement !== hex) hex.value = actual;
    if (avisar) alCambiar(actual);
  }
  function arrastre(zona, fn) {
    let pend = null;
    const mover = (e) => {
      const r = zona.getBoundingClientRect();
      fn(Math.min(1, Math.max(0, (e.clientX - r.left) / r.width)), Math.min(1, Math.max(0, (e.clientY - r.top) / r.height)));
      pintar(true);
    };
    zona.addEventListener("pointerdown", (e) => { zona.setPointerCapture(e.pointerId); zona.dataset.a = "1"; mover(e); });
    zona.addEventListener("pointermove", (e) => {
      if (!zona.dataset.a) return;
      pend = e; requestAnimationFrame(() => { if (pend) { mover(pend); pend = null; } });
    });
    const fin = () => { if (zona.dataset.a) { delete zona.dataset.a; recordar(actual); } };
    zona.addEventListener("pointerup", fin);
    zona.addEventListener("pointercancel", fin);
  }
  arrastre(sv, (x, y) => { s = x; v = 1 - y; });
  arrastre(matiz, (x) => { h = x * 360; });
  hex.addEventListener("change", () => {
    const t = hex.value.trim().replace(/^#?/, "#");
    if (/^#[0-9a-fA-F]{6}$/.test(t)) { [h, s, v] = rgbAHsv(...hexARgb(t)); pintar(true); recordar(actual); }
    else hex.value = actual;
  });

  function pintarHistorial() {
    caja.replaceChildren(...Array.from({ length: 10 }, (_, i) => {
      const c = hist[i];
      return c ? el("button", { class: "muestra", title: c, style: { background: c },
        onclick: () => { [h, s, v] = rgbAHsv(...hexARgb(c)); pintar(true); } })
        : el("span", { class: "muestra vacia" });
    }));
  }
  function recordar(c) {
    const i = hist.indexOf(c);
    if (i === 0) return;
    if (i > 0) hist.splice(i, 1);
    hist.unshift(c); hist.length = Math.min(hist.length, 10);
    pintarHistorial();
    caja.dispatchEvent(new CustomEvent("historial", { bubbles: true, detail: [...hist] }));
  }
  pintarHistorial();
  new ResizeObserver(() => pintar(false)).observe(sv);
  const raiz = el("div", { class: "selector-color" }, sv, matiz,
    el("div", { class: "hex" }, muestra, hex),
    el("div", { class: "etiqueta" }, "Historial"), caja);
  raiz.poner = (c) => { [h, s, v] = rgbAHsv(...hexARgb(c)); pintar(false); };
  raiz.habilitar = (si) => { raiz.style.opacity = si ? "" : ".35"; raiz.style.pointerEvents = si ? "" : "none"; };
  return raiz;
}

// ---------- popover genérico anclado a un elemento ----------
let popoverAbierto = null;
export function cerrarPopover() { if (popoverAbierto) { popoverAbierto(); popoverAbierto = null; } }

export function abrirPopover(ancla, contenido) {
  cerrarPopover();
  const p = el("div", { class: "popover" }, contenido);
  document.body.append(p);
  const r = ancla.getBoundingClientRect();
  const alto = Math.min(420, p.offsetHeight);
  let top = r.bottom + 6;
  if (top + alto > innerHeight - 70) top = Math.max(10, r.top - alto - 6);
  p.style.top = top + "px";
  p.style.left = Math.min(innerWidth - 310, Math.max(10, r.left)) + "px";
  const fuera = (e) => { if (!p.contains(e.target) && !ancla.contains(e.target)) cerrarPopover(); };
  const esc = (e) => { if (e.key === "Escape") cerrarPopover(); };
  setTimeout(() => document.addEventListener("pointerdown", fuera), 0);
  document.addEventListener("keydown", esc);
  popoverAbierto = () => {
    document.removeEventListener("pointerdown", fuera);
    document.removeEventListener("keydown", esc);
    p.remove();
  };
  return p;
}
