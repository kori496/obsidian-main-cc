<?php
/**
 * lagrim-stats · Descargas. Interfaz del descargador (motores_descargas.py vía descargas_api.php).
 */
declare(strict_types=1);
?>
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>lagrim-stats · Descargas</title>
<link rel="stylesheet" href="estilo.css">
<style>
  .dl-motores{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px}
  .dl-motores button{font:inherit;font-size:14px;color:var(--muted);background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:6px 14px;cursor:pointer;transition:background .15s,color .15s,border-color .15s,transform .15s}
  .dl-motores button:hover:not(:disabled){color:var(--ink);border-color:var(--accent)}
  .dl-motores button[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}
  .dl-motores button:disabled{opacity:.4;cursor:default}
  .dl-card label{display:block;font-size:13px;color:var(--muted);margin-bottom:6px}
  .dl-fila{display:flex;flex-wrap:wrap;gap:10px}
  .dl-fila input[type=text]{flex:1 1 280px;font:inherit;color:var(--ink);background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:10px 14px;outline:none;transition:border-color .15s,box-shadow .15s}
  .dl-fila input[type=text]:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
  button.btn-subir{border:0;font:inherit;font-size:14px;font-weight:600;padding:10px 20px;transition:filter .15s,transform .1s,opacity .15s}
  button.btn-subir:active{transform:scale(.97)}
  button.btn-subir:disabled{opacity:.5;cursor:default}
  #estado{margin-top:16px}
  #estado:empty{display:none}
  #estado .msg-ok,#estado .error{margin:0}
  .dl-ok-fila{display:flex;flex-wrap:wrap;align-items:center;gap:12px;justify-content:space-between}
  .dl-archivo{color:var(--ink);overflow-wrap:anywhere;font-size:14px}
  .dl-ver{font:inherit;font-size:14px;font-weight:600;color:var(--accent);background:var(--accent-soft);border:0;border-radius:999px;padding:6px 14px;cursor:pointer;transition:filter .15s}
  .dl-ver:hover:not(:disabled){filter:brightness(.95)}
  .dl-ver:disabled{opacity:.5;cursor:default}
  .dl-redes{margin-top:22px;padding-top:16px;border-top:1px solid var(--line)}
  .dl-redes h2{margin:0 0 4px;font-size:15px}
  .dl-chips{display:flex;flex-wrap:wrap;gap:6px;max-height:170px;overflow-y:auto;margin-top:12px}
  .dl-chip{font-size:13px;padding:3px 10px;border-radius:999px;border:1px solid var(--line);background:var(--surface);transition:border-color .15s,color .15s,transform .15s}
  .dl-chip:hover{border-color:var(--accent);color:var(--accent);transform:translateY(-1px)}
  .dl-chip.mas{color:var(--muted);border-style:dashed}
  .dl-pie{margin-top:14px}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>lagrim-stats</h1>
  <nav class="nav"><a href="global.php">Global</a><a href="index.php">YouTube</a><a href="tiktok.php">TikTok</a><a href="instagram.php">Instagram</a><a class="on" href="descargas.php">Descargas</a></nav>
  <div class="sub">Los archivos se guardan en la carpeta <code>descargas</code></div>
</header>

<div class="dl-motores" id="motores" role="group" aria-label="Motor de descarga"></div>

<section class="card dl-card">
  <form id="formulario" novalidate>
    <label for="url">Enlace</label>
    <div class="dl-fila">
      <input id="url" type="text" inputmode="url" autocomplete="off" spellcheck="false" placeholder="https://…">
      <button id="boton" class="btn-subir" type="submit">Descargar</button>
    </div>
  </form>

  <div id="estado" role="status" aria-live="polite"></div>

  <div class="dl-redes">
    <h2 id="redesTitulo"></h2>
    <div class="sub" id="redesDescripcion"></div>
    <div class="dl-chips" id="redes"></div>
  </div>
</section>

<p class="sub dl-pie">
  Herramientas: <code>pip install yt-dlp gallery-dl instaloader you-get streamlink</code>.
  Para contenido con sesión (stories, cuentas privadas) guarda un <code>cookies.txt</code> junto a <code>motores_descargas.py</code>.
</p>
</div>

<script>
  const API = 'descargas_api.php';
  const motoresEl = document.getElementById('motores');
  const formulario = document.getElementById('formulario');
  const campo = document.getElementById('url');
  const boton = document.getElementById('boton');
  const estado = document.getElementById('estado');
  const redesTitulo = document.getElementById('redesTitulo');
  const redesDescripcion = document.getElementById('redesDescripcion');
  const redesEl = document.getElementById('redes');

  let motores = [];
  let motorActual = 'auto';

  function el(tag, clase, texto) {
    const e = document.createElement(tag);
    if (clase) e.className = clase;
    if (texto !== undefined) e.textContent = texto;
    return e;
  }

  async function llamar(cuerpo) {
    const r = await fetch(API, { method: 'POST', body: new URLSearchParams(cuerpo) });
    let datos = null;
    try { datos = await r.json(); } catch (e) { /* respuesta no JSON */ }
    if (!datos || !r.ok || !datos.ok) throw new Error((datos && datos.mensaje) || 'Error en la descarga.');
    return datos;
  }

  async function cargarMotores() {
    try {
      const r = await fetch(API + '?accion=motores');
      const datos = await r.json();
      if (!datos.ok) throw new Error(datos.mensaje);
      motores = datos.motores;
    } catch (err) {
      motores = [];
      mostrarError(err.message || 'No se pudo cargar la lista de motores.');
    }
    renderMotores();
    renderRedes();
  }

  function renderMotores() {
    motoresEl.replaceChildren();
    for (const m of motores) {
      const b = el('button', '', m.nombre);
      b.type = 'button';
      b.disabled = !m.instalado;
      b.title = m.instalado ? m.descripcion : 'No está instalado en este equipo';
      b.setAttribute('aria-pressed', String(m.id === motorActual));
      b.addEventListener('click', () => { motorActual = m.id; renderMotores(); renderRedes(); });
      motoresEl.append(b);
    }
  }

  function renderRedes() {
    redesEl.replaceChildren();
    const m = motores.find((x) => x.id === motorActual);
    if (!m) { redesTitulo.textContent = ''; redesDescripcion.textContent = ''; return; }

    redesTitulo.textContent = 'Redes compatibles · ' + m.nombre;
    redesDescripcion.textContent = m.instalado ? m.descripcion : m.nombre + ' no está instalado en este equipo.';
    if (!m.instalado) return;

    const limite = 120;
    m.redes.slice(0, limite).forEach((n) => redesEl.append(el('span', 'dl-chip', n)));
    if (m.redes.length > limite) redesEl.append(el('span', 'dl-chip mas', '+' + (m.redes.length - limite) + ' más'));
  }

  function mostrarCargando() {
    estado.replaceChildren(el('div', 'msg-ok', 'Descargando… puede tardar unos minutos según el tamaño del archivo.'));
  }

  function mostrarError(mensaje) {
    estado.replaceChildren(el('div', 'error', mensaje));
  }

  function mostrarExito(archivo, motor) {
    const caja = el('div', 'msg-ok');
    const fila = el('div', 'dl-ok-fila');
    const texto = el('div');
    texto.append(el('b', '', 'Descarga completada · ' + motor), el('div', 'dl-archivo', archivo));
    const ver = el('button', 'dl-ver', 'Ver descarga');
    ver.type = 'button';
    ver.addEventListener('click', async () => {
      ver.disabled = true;
      try {
        await llamar({ accion: 'abrir', archivo });
        ver.disabled = false;
      } catch (err) {
        ver.textContent = err.message;
      }
    });
    fila.append(texto, ver);
    caja.append(fila);
    estado.replaceChildren(caja);
  }

  formulario.addEventListener('submit', async (e) => {
    e.preventDefault();
    const url = campo.value.trim();
    if (!url) { mostrarError('Pega un enlace para continuar.'); campo.focus(); return; }

    boton.disabled = true;
    campo.disabled = true;
    mostrarCargando();
    try {
      const datos = await llamar({ accion: 'descargar', url, motor: motorActual });
      mostrarExito(datos.archivo, datos.motor);
      campo.value = '';
    } catch (err) {
      mostrarError(err.message);
    } finally {
      boton.disabled = false;
      campo.disabled = false;
    }
  });

  cargarMotores();
</script>
</body>
</html>
