<?php
/**
 * lagrim-stats · panel de analitica de YouTube.
 * Lee datos/youtube.db (lo llena yt_stats.py). Solo lectura.
 * Servir SIEMPRE con la carpeta web/ como raiz (abrir_dashboard.bat lo hace),
 * para que client_secret.json y token.json nunca queden accesibles por web.
 */
declare(strict_types=1);

$dbPath = getenv('LAGRIM_DB') ?: __DIR__ . '/../datos/youtube.db';
$flagPath = __DIR__ . '/../NECESITA_AUTORIZAR.txt';

function h($v): string { return htmlspecialchars((string)$v, ENT_QUOTES, 'UTF-8'); }
function n($v): string { return number_format((float)$v, 0, ',', '.'); }
function dur($s): string { $s = (int)round((float)$s); return intdiv($s, 60) . ':' . str_pad((string)($s % 60), 2, '0', STR_PAD_LEFT); }
function mins($m): string {
    $m = (int)round((float)$m);
    return $m >= 60 ? intdiv($m, 60) . ' h ' . ($m % 60) . ' min' : $m . ' min';
}

$FUENTES = [
    'SHORTS' => 'Feed de Shorts', 'RELATED_VIDEO' => 'Videos relacionados', 'YT_SEARCH' => 'Búsqueda de YouTube',
    'YT_OTHER_PAGE' => 'Otras páginas de YouTube', 'SUBSCRIBER' => 'Suscripciones', 'YT_CHANNEL' => 'Páginas de canales',
    'NO_LINK_OTHER' => 'Directo / sin enlace', 'PLAYLIST' => 'Listas de reproducción', 'EXT_URL' => 'Sitios externos',
    'NOTIFICATION' => 'Notificaciones', 'END_SCREEN' => 'Pantalla final', 'SHORTS_CONTENT_LINKS' => 'Enlaces desde Shorts',
    'ADVERTISING' => 'Publicidad', 'HASHTAGS' => 'Hashtags', 'PROMOTED' => 'Promocionado', 'CARDS' => 'Tarjetas',
    'ANNOTATION' => 'Anotaciones', 'CAMPAIGN_CARD' => 'Tarjetas de campaña', 'LIVE_REDIRECT' => 'Redirección de directo',
];

$error = null;
$channel = $diario = $videos = $trafico = $hist = [];
$ultimaFecha = null;

if (!is_file($dbPath)) {
    $error = 'Todavía no hay datos. Ejecuta primero: python yt_stats.py';
} else {
    try {
        $db = new PDO('sqlite:' . $dbPath);
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);

        $channel = $db->query('SELECT * FROM channel ORDER BY fecha')->fetchAll();
        $diario = $db->query('SELECT * FROM diario ORDER BY dia')->fetchAll();
        $ultimaFecha = $channel ? end($channel)['fecha'] : null;

        // Videos: analitica del ultimo dia + datos publicos del ultimo dia
        $va = $db->query('SELECT * FROM video_analitica WHERE fecha=(SELECT MAX(fecha) FROM video_analitica)')->fetchAll();
        $vp = $db->query('SELECT p.* FROM video_publico p WHERE p.fecha=(SELECT MAX(fecha) FROM video_publico WHERE video_id=p.video_id)')->fetchAll();
        foreach ($vp as $r) {
            $videos[$r['video_id']] = [
                'id' => $r['video_id'], 'titulo' => $r['titulo'], 'publicado' => $r['publicado'],
                'vistas_pub' => (int)$r['vistas'], 'likes_pub' => (int)$r['likes'], 'coment' => (int)$r['comentarios'],
            ];
        }
        foreach ($va as $r) {
            $id = $r['video_id'];
            $videos[$id] ??= ['id' => $id, 'titulo' => $id . ' (no público)', 'publicado' => '', 'vistas_pub' => null, 'likes_pub' => null, 'coment' => null];
            $videos[$id]['an'] = $r;
        }
        $videos = array_values($videos);
        usort($videos, fn($a, $b) => (($b['an']['vistas'] ?? -1) <=> ($a['an']['vistas'] ?? -1)) ?: (($b['vistas_pub'] ?? 0) <=> ($a['vistas_pub'] ?? 0)));

        $trafico = $db->query('SELECT * FROM trafico WHERE fecha=(SELECT MAX(fecha) FROM trafico) ORDER BY vistas DESC')->fetchAll();
        foreach ($db->query('SELECT video_id, fecha, vistas, likes, comentarios FROM video_publico ORDER BY fecha') as $r) {
            $hist[$r['video_id']][] = [$r['fecha'], (int)$r['vistas'], (int)$r['likes'], (int)$r['comentarios']];
        }
    } catch (Throwable $e) {
        $error = 'No se pudo leer la base de datos: ' . $e->getMessage();
    }
}

// Totales del periodo
$tot = ['vistas' => 0, 'min' => 0.0, 'gan' => 0, 'per' => 0];
foreach ($diario as $d) {
    $tot['vistas'] += (int)$d['vistas'];
    $tot['min'] += (float)$d['minutos'];
    $tot['gan'] += (int)$d['subs_ganados'];
    $tot['per'] += (int)$d['subs_perdidos'];
}
$ult = $channel ? end($channel) : null;
$desde = $diario ? $diario[0]['dia'] : null;
$hasta = $diario ? end($diario)['dia'] : null;
$durMedia = $tot['vistas'] > 0 ? $tot['min'] * 60 / $tot['vistas'] : 0;
$diasViejo = $ultimaFecha ? (int)((time() - strtotime($ultimaFecha)) / 86400) : null;

$js = [
    'dias' => array_column($diario, 'dia'),
    'vistas' => array_map('intval', array_column($diario, 'vistas')),
    'min' => array_map('floatval', array_column($diario, 'minutos')),
    'gan' => array_map('intval', array_column($diario, 'subs_ganados')),
    'per' => array_map('intval', array_column($diario, 'subs_perdidos')),
    'chFechas' => array_column($channel, 'fecha'),
    'chSubs' => array_map('intval', array_column($channel, 'suscriptores')),
    'chVistas' => array_map('intval', array_column($channel, 'vistas_totales')),
    'hist' => $hist,
];
?><!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>lagrim-stats · YouTube</title>
<link rel="stylesheet" href="estilo.css">
</head>
<body>
<div class="wrap">
<header>
  <h1>lagrim-stats</h1>
  <nav class="nav"><a href="global.php">Global</a><a class="on" href="index.php">YouTube</a><a href="tiktok.php">TikTok</a><a href="instagram.php">Instagram</a><a href="descargas.php">Descargas</a></nav>
  <div class="sub">
    <?php if ($ultimaFecha): ?>Actualizado: <?= h($ultimaFecha) ?><?php endif; ?>
    <?php if ($desde): ?> · Periodo analizado: <?= h($desde) ?> a <?= h($hasta) ?><?php endif; ?>
  </div>
</header>

<?php if (is_file($flagPath)): ?>
  <div class="banner"><b>Hay que volver a autorizar YouTube.</b> El permiso caducó (en modo prueba dura 7 días). Abre una terminal en la carpeta <code>analitica</code> y ejecuta <code>python yt_stats.py</code>.</div>
<?php elseif ($diasViejo !== null && $diasViejo >= 2): ?>
  <div class="banner">Los datos tienen <?= $diasViejo ?> días. Si la tarea programada no está corriendo, ejecuta <code>python yt_stats.py</code>.</div>
<?php endif; ?>

<?php if ($error): ?>
  <div class="error"><?= h($error) ?></div>
<?php else: ?>

<div class="kpis">
  <div class="kpi"><small>Suscriptores</small><b><?= n($ult['suscriptores'] ?? 0) ?></b><small>+<?= n($tot['gan']) ?> / −<?= n($tot['per']) ?> en el periodo</small></div>
  <div class="kpi"><small>Vistas totales del canal</small><b><?= n($ult['vistas_totales'] ?? 0) ?></b><small><?= n($ult['videos'] ?? 0) ?> videos públicos</small></div>
  <div class="kpi"><small>Vistas en el periodo</small><b><?= n($tot['vistas']) ?></b><small><?= count($diario) ?> días</small></div>
  <div class="kpi"><small>Tiempo visto</small><b><?= h(mins($tot['min'])) ?></b><small>duración media <?= h(dur($durMedia)) ?> por vista</small></div>
  <div class="kpi"><small>Vistas por suscriptor ganado</small><b><?= $tot['gan'] > 0 ? n($tot['vistas'] / $tot['gan']) : '—' ?></b><small>menos es mejor</small></div>
</div>

<h2>Evolución diaria</h2>
<div class="grid2">
  <div class="card"><h3>Vistas por día (línea: media de 7 días)</h3><div class="chart"><canvas id="cVistas"></canvas></div></div>
  <div class="card"><h3>Minutos vistos por día</h3><div class="chart"><canvas id="cMin"></canvas></div></div>
  <div class="card"><h3>Suscriptores ganados y perdidos por día</h3><div class="chart"><canvas id="cSubs"></canvas></div></div>
  <div class="card"><h3>Historial del canal (se llena con cada ejecución)</h3>
    <?php if (count($channel) < 2): ?><div class="note">Se necesitan al menos 2 días de datos guardados.</div>
    <?php else: ?><div class="chart"><canvas id="cCanal"></canvas></div><?php endif; ?>
  </div>
</div>

<h2>Videos <span class="sub">(clic en una columna para ordenar)</span></h2>
<div class="tablewrap">
<table id="tVideos">
  <thead><tr>
    <th>Video</th><th>Publicado</th><th>Vistas periodo</th><th>Min. vistos</th><th>Duración media</th><th>% visto</th>
    <th>Likes periodo</th><th>Subs</th><th>Vistas totales</th><th>Likes totales</th><th>Comentarios</th>
  </tr></thead>
  <tbody>
  <?php foreach ($videos as $v): $a = $v['an'] ?? null; ?>
    <tr>
      <td><a href="https://www.youtube.com/watch?v=<?= h($v['id']) ?>" target="_blank" rel="noopener" style="color:inherit"><?= h($v['titulo']) ?></a></td>
      <td data-v="<?= h($v['publicado']) ?>"><?= h($v['publicado'] ?: '—') ?></td>
      <td data-v="<?= $a ? (float)$a['vistas'] : -1 ?>"><?= $a ? n($a['vistas']) : '<span class="muted">0</span>' ?></td>
      <td data-v="<?= $a ? (float)$a['minutos'] : -1 ?>"><?= $a ? n($a['minutos']) : '—' ?></td>
      <td data-v="<?= $a ? (float)$a['dur_media'] : -1 ?>"><?= $a ? h(dur($a['dur_media'])) : '—' ?></td>
      <td data-v="<?= $a ? (float)$a['pct_visto'] : -1 ?>"><?= $a ? h(number_format((float)$a['pct_visto'], 1, ',', '.')) . ' %' : '—' ?></td>
      <td data-v="<?= $a ? (float)$a['likes'] : -1 ?>"><?= $a ? n($a['likes']) : '—' ?></td>
      <td data-v="<?= $a ? (float)$a['subs_ganados'] : -1 ?>"><?= $a ? n($a['subs_ganados']) : '—' ?></td>
      <td data-v="<?= $v['vistas_pub'] ?? -1 ?>"><?= $v['vistas_pub'] !== null ? n($v['vistas_pub']) : '—' ?></td>
      <td data-v="<?= $v['likes_pub'] ?? -1 ?>"><?= $v['likes_pub'] !== null ? n($v['likes_pub']) : '—' ?></td>
      <td data-v="<?= $v['coment'] ?? -1 ?>"><?= $v['coment'] !== null ? n($v['coment']) : '—' ?></td>
    </tr>
  <?php endforeach; ?>
  </tbody>
</table>
</div>
<p class="sub">Un % visto alto con pocas vistas no significa nada: la muestra es demasiado pequeña. «Vistas periodo» es lo de la ventana analizada; «Vistas totales» es lo acumulado del video.</p>

<h2>Un video a lo largo del tiempo</h2>
<div class="card">
  <select id="selVideo">
    <?php foreach ($videos as $v): if (!isset($hist[$v['id']])) continue; ?>
      <option value="<?= h($v['id']) ?>"><?= h($v['titulo']) ?></option>
    <?php endforeach; ?>
  </select>
  <div id="histMsg" class="note" style="display:none">Se necesitan al menos 2 días de datos guardados de este video.</div>
  <div class="chart" id="histBox" style="margin-top:12px"><canvas id="cHist"></canvas></div>
</div>

<h2>De dónde llegan las vistas</h2>
<?php if (!$trafico): ?>
  <div class="note">Sin datos de tráfico.</div>
<?php else: $maxT = max(array_map(fn($t) => (int)$t['vistas'], $trafico)) ?: 1; $sumT = array_sum(array_map(fn($t) => (int)$t['vistas'], $trafico)) ?: 1; ?>
<div class="tablewrap">
<table>
  <thead><tr><th>Fuente</th><th></th><th>Vistas</th><th>%</th><th>Min. vistos</th></tr></thead>
  <tbody>
  <?php foreach ($trafico as $t): ?>
    <tr>
      <td><?= h($FUENTES[$t['fuente']] ?? $t['fuente']) ?></td>
      <td style="width:30%"><div class="bar"><i style="width:<?= round(100 * (int)$t['vistas'] / $maxT) ?>%"></i></div></td>
      <td><?= n($t['vistas']) ?></td>
      <td><?= h(number_format(100 * (int)$t['vistas'] / $sumT, 1, ',', '.')) ?> %</td>
      <td><?= n($t['minutos']) ?></td>
    </tr>
  <?php endforeach; ?>
  </tbody>
</table>
</div>
<?php endif; ?>

<?php endif; ?>
</div>

<?php if (!$error): ?>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
const D = <?= json_encode($js, JSON_HEX_TAG | JSON_HEX_AMP | JSON_UNESCAPED_UNICODE) ?>;

// Tabla ordenable
(function () {
  const t = document.getElementById('tVideos'); if (!t) return;
  const body = t.tBodies[0];
  t.tHead.querySelectorAll('th').forEach((th, i) => {
    let asc = false;
    th.addEventListener('click', () => {
      asc = !asc;
      const rows = [...body.rows];
      rows.sort((a, b) => {
        const x = a.cells[i], y = b.cells[i];
        const vx = x.dataset.v ?? x.textContent.trim(), vy = y.dataset.v ?? y.textContent.trim();
        const nx = parseFloat(vx), ny = parseFloat(vy);
        const c = (!isNaN(nx) && !isNaN(ny) && String(nx) === String(vx) ) ? nx - ny : String(vx).localeCompare(String(vy), 'es');
        return asc ? c : -c;
      });
      rows.forEach(r => body.appendChild(r));
    });
  });
})();

if (typeof Chart !== 'undefined') {
  const css = getComputedStyle(document.documentElement);
  const col = n => css.getPropertyValue(n).trim();
  Chart.defaults.color = col('--muted');
  Chart.defaults.borderColor = col('--line');
  Chart.defaults.font.family = 'system-ui, sans-serif';
  const base = { responsive: true, maintainAspectRatio: false, interaction: { mode: 'index', intersect: false },
    plugins: { legend: { display: false } }, scales: { x: { ticks: { maxTicksLimit: 8 }, grid: { display: false } }, y: { beginAtZero: true } } };
  const ma = (a, k) => a.map((_, i) => { const s = a.slice(Math.max(0, i - k + 1), i + 1); return +(s.reduce((x, y) => x + y, 0) / s.length).toFixed(2); });
  const el = id => document.getElementById(id);

  if (el('cVistas')) new Chart(el('cVistas'), { data: { labels: D.dias, datasets: [
    { type: 'bar', label: 'Vistas', data: D.vistas, backgroundColor: col('--accent'), borderRadius: 2 },
    { type: 'line', label: 'Media 7 días', data: ma(D.vistas, 7), borderColor: col('--ink'), borderWidth: 1.5, pointRadius: 0, tension: .3 } ] },
    options: { ...base, plugins: { legend: { display: true, labels: { boxWidth: 10 } } } } });

  if (el('cMin')) new Chart(el('cMin'), { type: 'line', data: { labels: D.dias, datasets: [
    { label: 'Minutos', data: D.min, borderColor: col('--accent'), backgroundColor: col('--accent-soft'), fill: true, pointRadius: 0, tension: .3 } ] }, options: base });

  if (el('cSubs')) new Chart(el('cSubs'), { type: 'bar', data: { labels: D.dias, datasets: [
    { label: 'Ganados', data: D.gan, backgroundColor: col('--good') },
    { label: 'Perdidos', data: D.per.map(x => -x), backgroundColor: col('--bad') } ] },
    options: { ...base, plugins: { legend: { display: true, labels: { boxWidth: 10 } } }, scales: { x: base.scales.x, y: { beginAtZero: true, ticks: { precision: 0 } } } } });

  if (el('cCanal')) new Chart(el('cCanal'), { type: 'line', data: { labels: D.chFechas, datasets: [
    { label: 'Vistas totales', data: D.chVistas, borderColor: col('--accent'), yAxisID: 'y', tension: .2 },
    { label: 'Suscriptores', data: D.chSubs, borderColor: col('--good'), yAxisID: 'y2', tension: .2 } ] },
    options: { ...base, plugins: { legend: { display: true, labels: { boxWidth: 10 } } },
      scales: { x: base.scales.x, y: { beginAtZero: false, position: 'left' }, y2: { beginAtZero: false, position: 'right', grid: { display: false }, ticks: { precision: 0 } } } } });

  let hist;
  const sel = el('selVideo');
  function drawHist() {
    if (!sel) return;
    const rows = D.hist[sel.value] || [];
    const ok = rows.length >= 2;
    el('histMsg').style.display = ok ? 'none' : 'block';
    el('histBox').style.display = ok ? 'block' : 'none';
    if (hist) hist.destroy();
    if (!ok) return;
    hist = new Chart(el('cHist'), { type: 'line', data: { labels: rows.map(r => r[0]), datasets: [
      { label: 'Vistas', data: rows.map(r => r[1]), borderColor: col('--accent'), tension: .2 },
      { label: 'Likes', data: rows.map(r => r[2]), borderColor: col('--good'), tension: .2 } ] },
      options: { ...base, plugins: { legend: { display: true, labels: { boxWidth: 10 } } } } });
  }
  if (sel) { sel.addEventListener('change', drawHist); drawHist(); }
}
</script>
<?php endif; ?>
</body>
</html>
