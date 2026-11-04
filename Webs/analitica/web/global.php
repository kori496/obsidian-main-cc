<?php
/**
 * lagrim-stats · visión global: YouTube, TikTok e Instagram juntos.
 * Solo lectura de datos/youtube.db (lo llenan yt_stats.py, importar_tiktok.py e importar_instagram.py).
 */
declare(strict_types=1);

$dbPath = getenv('LAGRIM_DB') ?: __DIR__ . '/../datos/youtube.db';

// Metas (agosto 2027): 10k suscriptores en YouTube y 30k seguidores sumando las demás redes.
const META_YT = 10000;
const META_OTRAS = 30000;
const FECHA_META = '2027-08-31';
const DIAS = 28;

function h($v): string { return htmlspecialchars((string)$v, ENT_QUOTES, 'UTF-8'); }
function n($v): string { return number_format((float)$v, 0, ',', '.'); }
function existe(PDO $db, string $t): bool {
    $q = $db->prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?");
    $q->execute([$t]);
    return (bool)$q->fetch();
}
/** Suma de una serie [fecha => valor] sobre las fechas dadas: [suma, días con dato]. */
function ventana(array $serie, array $fechas): array {
    $s = 0.0; $d = 0;
    foreach ($fechas as $f) { if (isset($serie[$f])) { $s += $serie[$f]; $d++; } }
    return [$s, $d];
}
/** Serie [fecha => valor] desde una consulta con columnas fecha, valor (suma si se repite el día). */
function serie(PDO $db, string $sql, array $args = []): array {
    $q = $db->prepare($sql);
    $q->execute($args);
    $out = [];
    foreach ($q as $r) {
        $f = substr((string)$r['fecha'], 0, 10);
        $out[$f] = ($out[$f] ?? 0.0) + (float)$r['valor'];
    }
    ksort($out);
    return $out;
}

$error = null;
$redes = [
    'youtube'   => ['nombre' => 'YouTube',   'vistas' => [], 'inter' => [], 'seg' => null, 'segFecha' => null, 'ultimo' => null, 'hay' => false],
    'tiktok'    => ['nombre' => 'TikTok',    'vistas' => [], 'inter' => [], 'seg' => null, 'segFecha' => null, 'ultimo' => null, 'hay' => false],
    'instagram' => ['nombre' => 'Instagram', 'vistas' => [], 'inter' => [], 'seg' => null, 'segFecha' => null, 'ultimo' => null, 'hay' => false],
];
$ytMinutos = [];
$igMedida = 'Vistas';

if (!is_file($dbPath)) {
    $error = 'Todavía no hay datos. Ejecuta primero: python yt_stats.py (crea la base de datos).';
} else {
    try {
        $db = new PDO('sqlite:' . $dbPath);
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);

        // YouTube
        if (existe($db, 'diario')) {
            $redes['youtube']['vistas'] = serie($db, 'SELECT dia AS fecha, vistas AS valor FROM diario');
            $ytMinutos = serie($db, 'SELECT dia AS fecha, minutos AS valor FROM diario');
        }
        if (existe($db, 'channel')) {
            $r = $db->query('SELECT suscriptores, fecha FROM channel ORDER BY fecha DESC LIMIT 1')->fetch();
            if ($r) { $redes['youtube']['seg'] = (float)$r['suscriptores']; $redes['youtube']['segFecha'] = substr((string)$r['fecha'], 0, 10); }
        }

        // TikTok (CSV de TikTok Studio)
        if (existe($db, 'tiktok_serie')) {
            $redes['tiktok']['vistas'] = serie($db,
                "SELECT fecha, valor FROM tiktok_serie WHERE lower(metrica) IN ('video views','views','vistas de video','vistas')");
            $redes['tiktok']['inter'] = serie($db,
                "SELECT fecha, valor FROM tiktok_serie WHERE lower(metrica) IN ('likes','comments','shares','me gusta','comentarios','compartidos')");
            $r = $db->query("SELECT valor, fecha FROM tiktok_serie WHERE (lower(metrica) LIKE '%follower%' OR lower(metrica) LIKE '%seguidor%')
                AND lower(metrica) NOT LIKE '%new%' AND lower(metrica) NOT LIKE '%diff%' AND lower(metrica) NOT LIKE '%net%'
                AND lower(metrica) NOT LIKE '%gain%' AND lower(metrica) NOT LIKE '%lost%' AND lower(metrica) NOT LIKE '%nuev%'
                AND lower(metrica) NOT LIKE '%gan%' AND lower(metrica) NOT LIKE '%perd%'
                ORDER BY fecha DESC LIMIT 1")->fetch();
            if ($r) { $redes['tiktok']['seg'] = (float)$r['valor']; $redes['tiktok']['segFecha'] = substr((string)$r['fecha'], 0, 10); }
        }

        // Instagram (API de Meta)
        if (existe($db, 'instagram_serie')) {
            // API y CSV pueden traer la misma métrica el mismo día: se toma el mayor, no la suma.
            $ig = fn(string $lista) => serie($db,
                "SELECT fecha, MAX(valor) AS valor FROM instagram_serie WHERE lower(metrica) IN ($lista) GROUP BY fecha");
            $v = $ig("'vistas','views','visualizaciones'");
            if (!$v) {
                $v = $ig("'alcance (cuentas únicas)','alcance','reach'");
                if ($v) $igMedida = 'Alcance';
            }
            $redes['instagram']['vistas'] = $v;
            $redes['instagram']['inter'] = $ig("'interacciones','total interactions','interactions'");
            $r = $db->query("SELECT valor, fecha FROM instagram_serie WHERE lower(metrica) IN ('seguidores','followers') ORDER BY fecha DESC LIMIT 1")->fetch();
            if ($r) { $redes['instagram']['seg'] = (float)$r['valor']; $redes['instagram']['segFecha'] = $r['fecha']; }
        }
    } catch (Throwable $e) {
        $error = 'No se pudo leer la base de datos: ' . $e->getMessage();
    }
}

// Ventana de los últimos DIAS días (hoy incluido)
$hoy = new DateTimeImmutable('today');
$fechas = [];
for ($i = DIAS - 1; $i >= 0; $i--) $fechas[] = $hoy->modify("-$i days")->format('Y-m-d');

foreach ($redes as $k => &$r) {
    [$r['sumVistas'], $r['diasVistas']] = ventana($r['vistas'], $fechas);
    [$r['sumInter'], $r['diasInter']] = ventana($r['inter'], $fechas);
    $todas = array_merge(array_keys($r['vistas']), array_keys($r['inter']));
    $r['ultimo'] = $todas ? max($todas) : null;
    $r['hay'] = $r['vistas'] || $r['inter'] || $r['seg'] !== null;
}
unset($r);
[$ytMin, ] = ventana($ytMinutos, $fechas);

// Metas
$otras = 0.0; $otrasFaltan = [];
foreach (['tiktok', 'instagram'] as $k) {
    if ($redes[$k]['seg'] === null) $otrasFaltan[] = $redes[$k]['nombre']; else $otras += $redes[$k]['seg'];
}
$ytSeg = $redes['youtube']['seg'] ?? 0.0;
$diasMeta = max(0, (int)$hoy->diff(new DateTimeImmutable(FECHA_META))->format('%r%a'));
$ritmoYt = $diasMeta > 0 ? max(0, META_YT - $ytSeg) / $diasMeta : 0;
$ritmoOtras = $diasMeta > 0 ? max(0, META_OTRAS - $otras) / $diasMeta : 0;

// Datos del gráfico (null = sin dato ese día)
$grafico = [
    'labels' => $fechas,
    'yt' => array_map(fn($f) => $redes['youtube']['vistas'][$f] ?? null, $fechas),
    'tt' => array_map(fn($f) => $redes['tiktok']['vistas'][$f] ?? null, $fechas),
    'ig' => array_map(fn($f) => $redes['instagram']['vistas'][$f] ?? null, $fechas),
    'igNombre' => 'Instagram (' . strtolower($igMedida) . ')',
];
$hayAlgo = $redes['youtube']['hay'] || $redes['tiktok']['hay'] || $redes['instagram']['hay'];
$fmt = fn($v) => $v === null ? '—' : n($v);
$fechaTxt = fn($f) => $f ?: '—';
?><!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>lagrim-stats · Global</title>
<link rel="stylesheet" href="estilo.css">
</head>
<body>
<div class="wrap">
<header>
  <h1>lagrim-stats</h1>
  <nav class="nav"><a class="on" href="global.php">Global</a><a href="index.php">YouTube</a><a href="tiktok.php">TikTok</a><a href="instagram.php">Instagram</a><a href="descargas.php">Descargas</a></nav>
  <div class="sub">Últimos <?= DIAS ?> días · hasta <?= h($hoy->format('Y-m-d')) ?></div>
</header>

<?php if ($error): ?>
  <div class="error"><?= h($error) ?></div>
<?php elseif (!$hayAlgo): ?>
  <div class="card"><h3>Aún no hay datos</h3><p>Ejecuta <code>python yt_stats.py</code>, <code>python importar_tiktok.py</code> y <code>python importar_instagram.py</code>, o usa el botón de subir CSV de cada pestaña.</p></div>
<?php else: ?>

<h2>Resumen por red</h2>
<div class="redes">
  <?php foreach (['youtube' => 'yt', 'tiktok' => 'tt', 'instagram' => 'ig'] as $k => $c): $r = $redes[$k]; ?>
    <div class="card red red-<?= $c ?>">
      <h3><?= h($r['nombre']) ?></h3>
      <?php if (!$r['hay']): ?>
        <div class="note">Sin datos todavía.</div>
      <?php else: ?>
        <div class="kpi2">
          <div class="kpi"><small><?= $k === 'youtube' ? 'Suscriptores' : 'Seguidores' ?></small><b><?= h($fmt($r['seg'])) ?></b>
            <small><?= $r['segFecha'] ? 'al ' . h($r['segFecha']) : 'sin dato' ?></small></div>
          <div class="kpi"><small><?= $k === 'instagram' ? h($igMedida) : 'Vistas' ?> (<?= DIAS ?> d)</small><b><?= $r['diasVistas'] ? h(n($r['sumVistas'])) : '—' ?></b>
            <small><?= (int)$r['diasVistas'] ?> días con dato</small></div>
          <div class="kpi"><small>Interacciones (<?= DIAS ?> d)</small><b><?= $r['diasInter'] ? h(n($r['sumInter'])) : '—' ?></b>
            <small><?= $k === 'youtube' ? 'sin dato diario' : (int)$r['diasInter'] . ' días con dato' ?></small></div>
        </div>
        <div class="sub">Último dato: <?= h($fechaTxt($r['ultimo'])) ?><?= $k === 'youtube' ? ' · ' . h(n($ytMin)) . ' min vistos' : '' ?></div>
      <?php endif; ?>
    </div>
  <?php endforeach; ?>
</div>

<h2>Vistas por día</h2>
<div class="card">
  <div class="chart"><canvas id="cGlobal"></canvas></div>
  <?php if ($redes['instagram']['vistas'] && $igMedida === 'Alcance'): ?>
    <p class="sub">En Instagram se muestra el <b>alcance</b> (cuentas únicas), no las vistas: la API aún no devuelve vistas por día.</p>
  <?php endif; ?>
  <p class="sub">Los días sin dato quedan en blanco; no se rellenan con cero.</p>
</div>

<h2>Comparación</h2>
<div class="tablewrap">
<table>
  <thead><tr><th>Métrica</th><th>YouTube</th><th>TikTok</th><th>Instagram</th></tr></thead>
  <tbody>
    <tr><td>Seguidores / suscriptores</td>
      <?php foreach (['youtube', 'tiktok', 'instagram'] as $k): ?><td><?= h($fmt($redes[$k]['seg'])) ?></td><?php endforeach; ?></tr>
    <tr><td>Vistas (<?= DIAS ?> días)<?= $igMedida === 'Alcance' && $redes['instagram']['vistas'] ? ' · Instagram: alcance' : '' ?></td>
      <?php foreach (['youtube', 'tiktok', 'instagram'] as $k): ?><td><?= $redes[$k]['diasVistas'] ? h(n($redes[$k]['sumVistas'])) : '—' ?></td><?php endforeach; ?></tr>
    <tr><td>Interacciones (<?= DIAS ?> días)</td>
      <?php foreach (['youtube', 'tiktok', 'instagram'] as $k): ?><td><?= $redes[$k]['diasInter'] ? h(n($redes[$k]['sumInter'])) : '—' ?></td><?php endforeach; ?></tr>
    <tr><td>Interacciones por cada 100 vistas</td>
      <?php foreach (['youtube', 'tiktok', 'instagram'] as $k): $r = $redes[$k]; ?>
        <td><?= ($r['diasVistas'] && $r['diasInter'] && $r['sumVistas'] > 0) ? h(number_format(100 * $r['sumInter'] / $r['sumVistas'], 1, ',', '.')) : '—' ?></td>
      <?php endforeach; ?></tr>
    <tr><td>Último dato</td>
      <?php foreach (['youtube', 'tiktok', 'instagram'] as $k): ?><td><?= h($fechaTxt($redes[$k]['ultimo'])) ?></td><?php endforeach; ?></tr>
  </tbody>
</table>
</div>
<p class="sub">Cada red cuenta distinto (por ejemplo, una vista de YouTube no equivale a una de TikTok), así que la comparación es orientativa. Un «—» significa que esa red no tiene ese dato, no que sea cero.</p>

<h2>Metas · <?= h(FECHA_META) ?> <span class="sub">(<?= $diasMeta ?> días)</span></h2>
<div class="grid2">
  <div class="card">
    <h3>YouTube: <?= h(n(META_YT)) ?> suscriptores</h3>
    <div class="prog"><i style="width:<?= min(100, round(100 * $ytSeg / META_YT, 1)) ?>%"></i></div>
    <p><b><?= h(n($ytSeg)) ?></b> de <?= h(n(META_YT)) ?> · ritmo necesario: <b><?= h(number_format($ritmoYt, 1, ',', '.')) ?></b> por día</p>
  </div>
  <div class="card">
    <h3>Otras redes: <?= h(n(META_OTRAS)) ?> seguidores en total</h3>
    <div class="prog"><i style="width:<?= min(100, round(100 * $otras / META_OTRAS, 1)) ?>%"></i></div>
    <p><b><?= h(n($otras)) ?></b> de <?= h(n(META_OTRAS)) ?> · ritmo necesario: <b><?= h(number_format($ritmoOtras, 1, ',', '.')) ?></b> por día</p>
    <?php if ($otrasFaltan): ?><p class="sub">Falta el dato de seguidores de: <?= h(implode(', ', $otrasFaltan)) ?>.</p><?php endif; ?>
  </div>
</div>

<?php endif; ?>
</div>

<?php if (!$error && $hayAlgo): ?>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
const G = <?= json_encode($grafico, JSON_HEX_TAG | JSON_HEX_AMP | JSON_UNESCAPED_UNICODE) ?>;
if (typeof Chart !== 'undefined') {
  const css = getComputedStyle(document.documentElement);
  const col = n => css.getPropertyValue(n).trim();
  Chart.defaults.color = col('--muted');
  Chart.defaults.borderColor = col('--line');
  Chart.defaults.font.family = 'system-ui, sans-serif';
  const ds = (label, data, c) => ({ label, data, borderColor: col(c), backgroundColor: col(c), pointRadius: 2, tension: .25, spanGaps: false });
  new Chart(document.getElementById('cGlobal'), {
    type: 'line',
    data: { labels: G.labels, datasets: [ds('YouTube', G.yt, '--yt'), ds('TikTok', G.tt, '--tt'), ds(G.igNombre, G.ig, '--ig')] },
    options: { responsive: true, maintainAspectRatio: false, interaction: { mode: 'index', intersect: false },
      plugins: { legend: { display: true, labels: { boxWidth: 10 } } },
      scales: { x: { ticks: { maxTicksLimit: 8 }, grid: { display: false } }, y: { beginAtZero: true, ticks: { precision: 0 } } } }
  });
}
</script>
<?php endif; ?>
</body>
</html>
