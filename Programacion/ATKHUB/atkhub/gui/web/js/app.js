// ATKHUB · núcleo de la interfaz.
import { el, aviso, pestanas, interruptor, debounce, cerrarPopover } from "./ui.js";
import { vistaMouse, diffMouse } from "./mouse.js";
import { vistaTeclado, diffTeclado } from "./teclado.js";

const TOKEN = document.querySelector('meta[name="atkhub-token"]').content;

export async function api(metodo, ...args) {
  try {
    const r = await fetch("/api/" + metodo, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-ATKHUB-Token": TOKEN },
      body: JSON.stringify(args),
    });
    if (!r.ok) return { ok: false, error: `El servidor respondió ${r.status}` };
    return await r.json();
  } catch {
    return { ok: false, error: "Se perdió la conexión con ATKHUB. ¿Cerraste la ventana de la consola?" };
  }
}

const ICONO = {
  teclado: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="2" y="6" width="20" height="12" rx="2"/><path d="M6 10h.01M10 10h.01M14 10h.01M18 10h.01M6 14h.01M8 14h8M18 14h.01"/></svg>',
  mouse: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="6" y="2.5" width="12" height="19" rx="6"/><path d="M12 2.5v6.5M6 9h12"/></svg>',
};

const DISPOSITIVOS = {
  mouse: { nombre: "Attack Shark X11", tipo: "Mouse", vista: vistaMouse, diff: diffMouse,
           leer: "mouse_leer", aplicar: "mouse_aplicar",
           pestanas: [["rendimiento", "Rendimiento"], ["iluminacion", "Iluminación"], ["botones", "Botones"], ["energia", "Energía"]] },
  teclado: { nombre: "Ajazz AK820 Max", tipo: "Teclado", vista: vistaTeclado, diff: diffTeclado,
             leer: "teclado_leer", aplicar: "teclado_aplicar",
             pestanas: [["iluminacion", "Iluminación"], ["energia", "Energía"]] },
};

// Estado por dispositivo:
//  base     = lo confirmado (al cargar o al GUARDAR)  -> REVERTIR vuelve aquí
//  aplicado = lo que tiene el dispositivo ahora
//  edit     = lo que se ve en la ventana
const E = {
  catalogo: null, info: null, disp: {}, actual: null, pestana: {},
  estado: {}, ocupado: {}, pendiente: {}, vistaPrevia: true,
};
const $ = (s) => document.querySelector(s);
const clonar = (o) => structuredClone(o);

// ---------- arranque ----------
async function iniciar() {
  const [info, cat] = await Promise.all([api("info"), api("catalogo")]);
  if (!info.ok || !cat.ok) return aviso(info.error || cat.error, "error");
  E.info = info; E.catalogo = cat;
  E.vistaPrevia = info.preferencias.vista_previa !== false;
  if (info.simular) $(".lateral-pie").append(el("span", { class: "insignia" }, "Simulado"));
  $("#version").textContent = "v" + info.version;
  montarBarra();
  await refrescarDispositivos();
  const primero = ["mouse", "teclado"].find((d) => E.disp[d]?.conectado) || "mouse";
  seleccionar(primero);
  setInterval(refrescarDispositivos, 5000);
}

async function refrescarDispositivos() {
  const r = await api("dispositivos");
  if (!r.ok) return;
  const antes = JSON.stringify(E.disp);
  E.disp = { mouse: r.mouse, teclado: r.teclado };
  if (antes !== JSON.stringify(E.disp)) pintarLateral();
}

function pintarLateral() {
  const lista = $("#lista-disp");
  lista.replaceChildren(...Object.entries(DISPOSITIVOS).map(([id, d]) => {
    const info = E.disp[id] || {};
    return el("div", {
      class: `disp ${E.actual === id ? "activo" : ""} ${info.conectado ? "" : "desconectado"}`,
      tabindex: 0, role: "button", onclick: () => seleccionar(id),
      onkeydown: (e) => (e.key === "Enter" || e.key === " ") && seleccionar(id),
    },
      el("div", { class: "disp-icono", html: ICONO[id] }),
      el("div", {},
        el("div", { class: "disp-nombre" }, d.nombre),
        el("div", { class: "disp-sub" }, el("span", { class: `punto ${info.conectado ? "on" : ""}` }),
          info.conectado ? `${d.tipo} · ${info.conexion}` : `${d.tipo} · desconectado`)));
  }));
}

// ---------- selección de dispositivo y pestañas ----------
async function seleccionar(id) {
  if (E.actual === id && E.estado[id]) return;
  cerrarPopover();
  E.actual = id;
  pintarLateral();
  const d = DISPOSITIVOS[id];
  $("#titulo").textContent = d.nombre;
  $("#subtitulo").textContent = d.tipo;
  E.pestana[id] ||= d.pestanas[0][0];
  const tabs = pestanas(d.pestanas, (p) => { E.pestana[id] = p; mostrarVista(); });
  $("#pestanas").replaceWith(Object.assign(tabs, { id: "pestanas" }));
  tabs.elegir(E.pestana[id]);
  if (!E.estado[id]) await cargar(id);
  else mostrarVista();
  pintarBarra();
}

async function cargar(id) {
  const d = DISPOSITIVOS[id];
  ponerCargando(id === "mouse" ? "Leyendo el mouse…" : "Leyendo el teclado…");
  const r = await api(d.leer);
  if (E.actual !== id) return;
  if (!r.ok) {
    E.estado[id] = null;
    return mostrarError(id, r.error);
  }
  const datos = id === "teclado" ? { ...r.config } : r;
  E.estado[id] = { base: clonar(datos), aplicado: clonar(datos), edit: clonar(datos), extra: r };
  pintarCabecera(id);
  mostrarVista();
  pintarBarra();
}

function ponerCargando(texto) {
  const c = $("#contenido");
  c.replaceChildren(el("div", { class: "cargando" }, el("div", { class: "cargando-caja" }, el("div", { class: "anillo" }), texto)));
}

function mostrarError(id, error) {
  const consejo = id === "mouse" ? "Si está por el dongle, mueve el mouse para despertarlo." : "Revisa que el teclado esté conectado por cable o por el dongle.";
  $("#contenido").replaceChildren(el("div", { class: "vista" }, el("div", { class: "vacio" }, el("div", {},
    el("div", { class: "icono-grande", html: ICONO[id].replace(/26/g, "64") }),
    el("h2", {}, "No pude leer el dispositivo"),
    el("p", {}, error), el("p", { class: "nota" }, consejo),
    el("button", { class: "boton primario", onclick: () => cargar(id) }, "Reintentar")))));
  pintarBarra();
}

function pintarCabecera(id) {
  const r = E.estado[id]?.extra || {};
  const bat = id === "mouse" ? r.bateria?.porcentaje : r.bateria;
  const caja = $("#bateria");
  if (bat == null) { caja.hidden = true; return; }
  caja.hidden = false;
  caja.querySelector("i").style.transform = `scaleX(${bat / 100})`;
  caja.querySelector("i").style.background = bat < 20 ? "var(--rojo)" : "";
  caja.querySelector("b").textContent = bat + " %";
  caja.querySelector("span").textContent = (id === "mouse" ? r.bateria?.estado : r.energia) || "";
  $("#subtitulo").textContent = `${DISPOSITIVOS[id].tipo} · ${r.conexion || ""}`;
}

let vistaActual = null;
function mostrarVista() {
  const id = E.actual, est = E.estado[id];
  if (!est) return;
  cerrarPopover();
  const c = $("#contenido");
  const vieja = c.querySelector(".vista");
  vistaActual?.destruir?.();
  const ctx = {
    catalogo: E.catalogo[id], edit: est.edit, base: est.base, extra: est.extra, info: E.info,
    cambiar: () => alCambiar(id),
    api, recargar: () => { E.estado[id] = null; cargar(id); },
    preferencias: E.info.preferencias,
  };
  vistaActual = DISPOSITIVOS[id].vista(E.pestana[id], ctx);
  const nueva = el("div", { class: "vista" }, vistaActual.nodo);
  if (vieja) {
    vieja.classList.add("saliendo");
    vieja.addEventListener("animationend", () => vieja.remove(), { once: true });
  }
  c.querySelectorAll(".cargando, .vacio").forEach((n) => n.closest(".vista, .cargando")?.remove());
  c.append(nueva);
}

// ---------- cambios, vista previa, guardar, revertir ----------
const aplicarEnVivo = {
  mouse: debounce(() => aplicar("mouse", "aplicado"), 450),
  teclado: debounce(() => aplicar("teclado", "aplicado"), 160),
};

function alCambiar(id) {
  pintarBarra();
  if (E.vistaPrevia) aplicarEnVivo[id]();
}

// Manda al dispositivo la diferencia entre "edit" y lo que ya tiene. Si hay otra
// escritura en curso, marca pendiente y vuelve a intentarlo al terminar (agrupa cambios).
async function aplicar(id, motivo) {
  const est = E.estado[id];
  if (!est) return true;
  if (E.ocupado[id]) { E.pendiente[id] = motivo; return true; }
  const d = DISPOSITIVOS[id];
  const objetivo = clonar(est.edit);
  const cambios = d.diff(est.aplicado, objetivo);
  if (!cambios) return true;
  if (id === "mouse" && cambios.botones?.izquierdo && cambios.botones.izquierdo !== "clic-izq") {
    const { confirmar } = await import("./ui.js");
    const si = await confirmar("Cambiar el clic izquierdo",
      "Si le quitas el clic al botón izquierdo puedes quedarte sin clic. Se arregla con REVERTIR o restaurando los botones. ¿Seguir?", "Cambiar");
    if (!si) { est.edit.botones.izquierdo = clonar(est.aplicado.botones.izquierdo); mostrarVista(); pintarBarra(); return false; }
    cambios.forzar_izquierdo = true;
  }
  E.ocupado[id] = true; pintarBarra();
  const r = await api(d.aplicar, cambios);
  E.ocupado[id] = false;
  if (r.ok) {
    est.aplicado = objetivo;
    if (r.sin_confirmar?.length) aviso(`Enviado sin confirmación del mouse: ${r.sin_confirmar.join(", ")}.`, "info");
  } else {
    aviso(r.error, "error");
  }
  const otra = E.pendiente[id]; E.pendiente[id] = null;
  if (otra && r.ok) return aplicar(id, otra);
  pintarBarra();
  return r.ok;
}

async function guardar() {
  const id = E.actual, est = E.estado[id];
  if (!est) return;
  const ok = await aplicar(id, "guardar");
  if (!ok) return;
  if (E.ocupado[id]) await new Promise((res) => { const t = setInterval(() => { if (!E.ocupado[id]) { clearInterval(t); res(); } }, 60); });
  est.base = clonar(est.edit);
  pintarBarra();
  aviso("Configuración guardada en el dispositivo.", "ok");
}

async function revertir() {
  const id = E.actual, est = E.estado[id];
  if (!est) return;
  est.edit = clonar(est.base);
  mostrarVista();
  pintarBarra();
  await aplicar(id, "revertir");
}

function hayCambios(id) {
  const est = E.estado[id];
  return !!(est && DISPOSITIVOS[id].diff(est.base, est.edit));
}

function montarBarra() {
  const vp = interruptor("Vista previa en vivo", E.vistaPrevia, (v) => {
    E.vistaPrevia = v;
    api("guardar_preferencias", { vista_previa: v });
    if (v && E.actual) aplicarEnVivo[E.actual]();
  });
  $("#barra-centro").append(vp);
  $("#revertir").addEventListener("click", revertir);
  $("#guardar").addEventListener("click", guardar);
  addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "s") { e.preventDefault(); if (!$("#guardar").disabled) guardar(); }
  });
}

function pintarBarra() {
  const id = E.actual;
  const sucio = hayCambios(id), ocupado = !!E.ocupado[id];
  const punto = $("#estado-punto"), txt = $("#estado-texto");
  punto.className = "punto " + (ocupado ? "ocupado" : sucio ? "sucio" : "on");
  txt.textContent = !E.estado[id] ? "Sin datos del dispositivo"
    : ocupado ? "Enviando al dispositivo…"
    : sucio ? (E.vistaPrevia ? "Cambios en vista previa sin guardar" : "Cambios sin guardar")
    : "Todo guardado";
  $("#revertir").disabled = !sucio || ocupado;
  const g = $("#guardar");
  g.disabled = !sucio || ocupado;
  g.innerHTML = ocupado ? '<span class="girando"></span>Guardando' : "Guardar";
}

// la ventana se puede cerrar con cambios en vista previa: avisar
addEventListener("beforeunload", (e) => { if (Object.keys(E.estado).some(hayCambios)) e.preventDefault(); });
// pausar animaciones costosas si la ventana no está visible
document.addEventListener("visibilitychange", () => document.body.classList.toggle("oculta", document.hidden));

iniciar();
