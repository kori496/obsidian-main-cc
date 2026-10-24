<?php
/**
 * lagrim-stats · Instagram. Lee las tablas instagram_* de datos/youtube.db
 * (las llena importar_instagram.py: API de Meta + CSV de Meta Business Suite).
 */
declare(strict_types=1);

/**
 * Guarda el CSV subido en instagram/entrada/ y ejecuta importar_instagram.py.
 * Devuelve el mensaje para mostrar; $ok queda en true si la importacion termino bien.
 */
function subirCsv(?array $f, bool &$ok): string {
    $ok = false;
    if (!$f || ($f['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK) {
        return 'No se recibió el archivo (código de error ' . ($f['error'] ?? '?') . ').';
    }
    if (strtolower(pathinfo((string)$f['name'], PATHINFO_EXTENSION)) !== 'csv') {
        return 'Solo se aceptan archivos .csv de Instagram (Meta Business Suite).';
    }
    if ((int)$f['size'] > 5 * 1024 * 1024) {
        return 'El archivo pesa más de 5 MB; un CSV de Instagram debería pesar mucho menos.';
    }
    $dir = __DIR__ . '/../instagram/entrada';
    if (!is_dir($dir) && !mkdir($dir, 0777, true)) {
        return 'No se pudo crear la carpeta instagram/entrada.';
    }
    $nombre = preg_replace('/[^A-Za-z0-9_. -]/', '_', basename((string)$f['name']));
    $destino = $dir . '/' . date('Ymd_His') . '_' . $nombre;
    if (!move_uploaded_file($f['tmp_name'], $destino)) {
        return 'No se pudo guardar el archivo en instagram/entrada.';
    }
    $py = getenv('LAGRIM_PYTHON') ?: 'python';
    $script = __DIR__ . '/../importar_instagram.py';
    $salida = [];
    $codigo = 0;
    exec(escapeshellcmd($py) . ' ' . escapeshellarg($script) . ' --solo-csv 2>&1', $salida, $codigo);
    $ok = $codigo === 0;
    $resumen = $salida ? implode(' · ', array_slice(array_filter(array_map('trim', $salida)), -3)) : '';
    if (!$ok) {
        return 'El archivo se guardó, pero la importación falló: ' . ($resumen ?: 'sin salida. ¿Está instalado Python y en el PATH?');
    }
    return 'CSV importado: ' . $nombre . ($resumen ? ' (' . $resumen . ')' : '');
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && ($_POST['accion'] ?? '') === 'subir') {
    $ok = false;
    $msg = subirCsv($_FILES['csv'] ?? null, $ok);
    header('Location: instagram.php?' . http_build_query(['msg' => $msg, 'ok' => $ok ? '1' : '0']));
    exit;
}
$msgSubida = isset($_GET['msg']) ? (string)$_GET['msg'] : null;
$msgSubidaOk = ($_GET['ok'] ?? '0') === '1';

$dbPath = getenv('LAGRIM_DB') ?: __DIR__ . '/../datos/youtube.db';

function h($v): string { return htmlspecialchars((string)$v, ENT_QUOTES, 'UTF-8'); }
function num($v): string {
    $f = (float)$v;
    return number_format($f, floor($f) == $f ? 0 : 1, ',', '.');
}
/** Texto -> numero si lo es (para ordenar y alinear), si no null. */
function aNum(string $s): ?float {
    $s = trim(str_replace(["\u{a0}", ' '], '', $s));
    $s = rtrim($s, '%');
    if ($s === '') return null;
    if (preg_match('/^-?\d+$/', $s)) return (float)$s;
    if (preg_match('/^-?\d{1,3}(,\d{3})+(\.\d+)?$/', $s)) return (float)str_replace(',', '', $s);
    if (preg_match('/^-?\d{1,3}(\.\d{3})+(,\d+)?$/', $s)) return (float)str_replace(['.', ','], ['', '.'], $s);
    if (preg_match('/^-?\d+[.,]\d+$/', $s)) return (float)str_replace(',', '.', $s);
    return null;
}
/** Metricas acumuladas (seguidores totales): se muestra el cambio en vez de la suma. */
function esAcumulada(string $m): bool {
    return (bool)preg_match('/follower|seguidor/i', $m) && !preg_match('/diff|net|new|nuev|gain|gan|lost|perd/i', $m);
}

$error = null;
$series = [];   // tipo => metrica => [[fecha, valor], ...]
$tablas = [];   // tipo => ['nombre' =>, 'importado' =>, 'cols' => [], 'filas' => []]
$importaciones = [];

if (!is_file($dbPath)) {
    $error = 'Todavía no hay datos. Ejecuta primero: python yt_stats.py (crea la base de datos) y luego python importar_instagram.py';
} else {
    try {
        $db = new PDO('sqlite:' . $dbPath);
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
        $has = (bool)$db->query("SELECT 1 FROM sqlite_master WHERE type='table' AND name='instagram_archivo'")->fetch();
        if ($has) {
            foreach ($db->query('SELECT tipo, metrica, fecha, valor FROM instagram_serie ORDER BY rowid') as $r) {
                $series[$r['tipo']][$r['metrica']][] = [$r['fecha'], (float)$r['valor']];
            }
            foreach ($series as $t => $mets) {            // puntos en orden cronologico
                foreach ($mets as $m => $pts) { usort($pts, fn($x, $y) => strcmp($x[0], $y[0])); $series[$t][$m] = $pts; }
            }
            uksort($series, fn($x, $y) => ($y === 'overview') <=> ($x === 'overview') ?: strcmp($x, $y));
            $importaciones = $db->query('SELECT nombre, tipo, importado, filas, es_serie FROM instagram_archivo ORDER BY id DESC LIMIT 12')->fetchAll();
            $ult = $db->query('SELECT a.* FROM instagram_archivo a WHERE es_serie=0 AND id=(SELECT MAX(id) FROM instagram_archivo WHERE tipo=a.tipo) ORDER BY tipo')->fetchAll();
            foreach ($ult as $a) {
                $filas = [];
                $q = $db->prepare('SELECT datos FROM instagram_fila WHERE archivo_id=? ORDER BY n');
                $q->execute([$a['id']]);
                foreach ($q as $f) $filas[] = json_decode($f['datos'], true) ?: [];
                $tablas[$a['tipo']] = ['nombre' => $a['nombre'], 'importado' => $a['importado'], 'cols' => json_decode($a['columnas'], true) ?: [], 'filas' => $filas];
            }
        }
    } catch (Throwable $e) {
        $error = 'No se pudo leer la base de datos: ' . $e->getMessage();
    }
}

$js = [];       // para los graficos
$bloques = [];  // tarjetas por tipo de serie
$i = 0;
foreach ($series as $tipo => $mets) {
    $kp = []; $charts = [];
    foreach ($mets as $m => $pts) {
        $vals = array_column($pts, 1);
        $acum = esAcumulada($m);
        $kp[] = [
            'm' => $m, 'ultimo' => end($vals),
            'extra' => $acum ? (end($vals) - $vals[0]) : array_sum($vals),
            'extraTxt' => $acum ? 'cambio en el rango' : 'suma en el rango',
            'acum' => $acum,
        ];
        $id = 'ts' . $i++;
        $charts[] = ['id' => $id, 'm' => $m];
        $js[] = ['id' => $id, 'm' => $m, 'labels' => array_column($pts, 0), 'data' => $vals, 'line' => $acum];
    }
    $rango = reset($mets);
    $bloques[$tipo] = ['kpis' => $kp, 'charts' => $charts, 'desde' => $rango[0][0], 'hasta' => end($rango)[0], 'dias' => count($rango)];
}

// Visual de publicaciones: cualquier tabla con una fecha de publicación y columnas numéricas por post.
$pubs = []; $pj = [];
foreach ($tablas as $tipo => $t) {
    $filas = $t['filas']; if (count($filas) < 1) continue;
    $colFecha = null; $metr = [];
    foreach ($t['cols'] as $c) {
        if ($colFecha === null && preg_match('/publish|public|fecha|date.?time|^date$/i', $c)) {
            $okf = 0; foreach ($filas as $f) if (strtotime((string)($f[$c] ?? '')) !== false && ($f[$c] ?? '') !== '') $okf++;
            if ($okf === count($filas)) { $colFecha = $c; continue; }
        }
        if (preg_match('/(^|\W)id(\W|$)|duration|duraci|permalink|url|descr/i', $c)) continue;
        $vals = array_map(fn($f) => aNum((string)($f[$c] ?? '')), $filas);
        if (in_array(null, $vals, true)) continue;
        if (count(array_unique($vals)) < 1) continue;
        $metr[$c] = $vals;
    }
    if ($colFecha === null || !$metr) continue;
    $idx = range(0, count($filas) - 1);
    usort($idx, fn($a, $b) => strtotime((string)$filas[$a][$colFecha]) <=> strtotime((string)$filas[$b][$colFecha]));
    $labels = array_map(fn($i) => date('d/m', strtotime((string)$filas[$i][$colFecha])), $idx);
    $colPost = null; foreach ($t['cols'] as $c) if (preg_match('/post.?type|tipo/i', $c)) { $colPost = $c; break; }
    $tot = []; foreach ($metr as $c => $v) $tot[$c] = array_sum($v);
    $ord = array_map(fn($c) => array_map(fn($i) => $metr[$c][$i], $idx), array_keys($metr));
    $series_ = array_combine(array_keys($metr), $ord);
    $verCol = null; foreach (['Views','Vistas','Reproducciones'] as $c) if (isset($series_[$c])) { $verCol = $c; break; }
    $mejor = null;
    if ($verCol) { $mx = max($series_[$verCol]); $k = array_search($mx, $series_[$verCol]); $mejor = [$labels[$k], $mx]; }
    $pubs[$tipo] = ['n' => count($filas), 'tot' => $tot, 'mejor' => $mejor, 'verCol' => $verCol, 'id' => 'pub' . count($pubs)];
    $pj[] = ['id' => 'pub' . (count($pubs) - 1), 'labels' => $labels, 'series' => $series_];
}
$ultImport = $importaciones ? $importaciones[0]['importado'] : null;
?><!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>lagrim-stats · Instagram</title>
<link rel="stylesheet" href="estilo.css">
</head>
<body>
<div class="wrap">
<header>
  <h1>lagrim-stats</h1>
  <nav class="nav"><a href="global.php">Global</a><a href="index.php">YouTube</a><a href="tiktok.php">TikTok</a><a class="on" href="instagram.php">Instagram</a><a href="descargas.php">Descargas</a></nav>
  <div class="acciones">
    <div class="sub"><?php if ($ultImport): ?>Última importación: <?= h(str_replace('T', ' ', $ultImport)) ?><?php endif; ?></div>
    <form method="post" enctype="multipart/form-data" class="subir">
      <input type="hidden" name="accion" value="subir">
      <label class="btn-subir">Subir CSV de Instagram<input type="file" name="csv" accept=".csv,text/csv" onchange="this.form.submit()"></label>
    </form>
  </div>
</header>

<?php if (is_file(__DIR__ . '/../NECESITA_TOKEN_META.txt')): ?>
  <div class="banner"><b>El token de Instagram caducó o fue revocado.</b> Genera uno nuevo en developers.facebook.com (lagrim-stats → Casos de uso → Instagram → <i>Generar identificador</i>), pégalo en <code>analitica/meta_config.json</code> y ejecuta <code>python importar_instagram.py</code>.</div>
<?php endif; ?>

<?php if ($msgSubida !== null): ?>
  <div class="<?= $msgSubidaOk ? 'msg-ok' : 'error' ?>"><?= h($msgSubida) ?></div>
<?php endif; ?>

<?php if ($error): ?>
  <div class="error"><?= h($error) ?></div>
<?php elseif (!$series && !$tablas): ?>
  <div class="card">
    <h3>Aún no hay datos de Instagram</h3>
    <p><b>Opción A (API):</b> copia <code>analitica/meta_config.ejemplo.json</code> como <code>meta_config.json</code>, pega el token de Instagram y ejecuta <code>python importar_instagram.py</code>.<br>
       <b>Opción B (CSV):</b> exporta el CSV desde Meta Business Suite (Insights) o el panel profesional de Instagram.<br>
       2. Suéltalo en la carpeta <code>analitica/instagram/entrada/</code>.<br>
       3. Ejecuta <code>python importar_instagram.py</code> y recarga esta página.</p>
    <p class="sub">Cada importación se une con las anteriores, así el historial va creciendo aunque la fuente solo entregue unos días.</p>
  </div>
<?php else: ?>

<?php foreach ($bloques as $tipo => $b): ?>
  <h2><?= h(ucfirst($tipo)) ?> <span class="sub">· <?= h($b['desde']) ?> a <?= h($b['hasta']) ?> (<?= (int)$b['dias'] ?> días)</span></h2>
  <div class="kpi2">
    <?php foreach ($b['kpis'] as $k): ?>
      <div class="kpi"><small><?= h($k['m']) ?></small><b><?= h(num($k['ultimo'])) ?></b>
        <small>último día · <?= $k['acum'] && $k['extra'] > 0 ? '+' : '' ?><?= h(num($k['extra'])) ?> <?= h($k['extraTxt']) ?></small></div>
    <?php endforeach; ?>
  </div>
  <div class="grid2">
    <?php foreach ($b['charts'] as $c): ?>
      <div class="card"><h3><?= h($c['m']) ?></h3><div class="chart s"><canvas id="<?= h($c['id']) ?>"></canvas></div></div>
    <?php endforeach; ?>
  </div>
<?php endforeach; ?>

<?php foreach ($pubs as $tipo => $pb): ?>
  <h2>Publicaciones <span class="sub">· <?= h($tipo) ?> · <?= (int)$pb['n'] ?> publicaciones</span></h2>
  <div class="kpi2">
    <div class="kpi"><small>Publicaciones</small><b><?= (int)$pb['n'] ?></b></div>
    <?php foreach ($pb['tot'] as $c => $v): ?>
      <div class="kpi"><small><?= h($c) ?> (total)</small><b><?= h(num($v)) ?></b>
        <small>media <?= h(number_format($v / $pb['n'], 1, ',', '.')) ?> por publicación</small></div>
    <?php endforeach; ?>
  </div>
  <div class="grid2">
    <div class="card"><h3>Alcance y vistas por publicación (por fecha)</h3><div class="chart s"><canvas id="<?= h($pb['id']) ?>a"></canvas></div></div>
    <div class="card"><h3>Interacciones por publicación</h3><div class="chart s"><canvas id="<?= h($pb['id']) ?>b"></canvas></div></div>
  </div>
  <?php if ($pb['mejor']): ?><p class="sub">Mejor publicación: la del <b><?= h($pb['mejor'][0]) ?></b> con <?= h(num($pb['mejor'][1])) ?> <?= h(strtolower($pb['verCol'])) ?>.</p><?php endif; ?>
<?php endforeach; ?>

<?php $ti = 0; foreach ($tablas as $tipo => $t): $ti++; ?>
  <h2><?= h(ucfirst($tipo)) ?> <span class="sub">· <?= h($t['nombre']) ?> · importado <?= h(substr(str_replace('T', ' ', $t['importado']), 0, 16)) ?></span></h2>
  <div class="tablewrap">
  <table class="ord" id="tab<?= $ti ?>">
    <thead><tr><?php foreach ($t['cols'] as $c): ?><th><?= h($c) ?></th><?php endforeach; ?></tr></thead>
    <tbody>
    <?php foreach ($t['filas'] as $f): ?>
      <tr>
      <?php foreach ($t['cols'] as $c): $v = (string)($f[$c] ?? ''); $nv = aNum($v); ?>
        <td data-v="<?= h($nv ?? $v) ?>"><?= h($v) ?></td>
      <?php endforeach; ?>
      </tr>
    <?php endforeach; ?>
    </tbody>
  </table>
  </div>
<?php endforeach; ?>

<?php if ($importaciones): ?>
  <h2>Importaciones recientes</h2>
  <div class="tablewrap"><table>
    <thead><tr><th>Archivo</th><th>Tipo</th><th>Filas</th><th>Importado</th></tr></thead>
    <tbody>
    <?php foreach ($importaciones as $m): ?>
      <tr><td><?= h($m['nombre']) ?></td><td><?= h($m['tipo']) ?> <?= $m['es_serie'] ? '(serie)' : '(tabla)' ?></td><td><?= (int)$m['filas'] ?></td><td><?= h(str_replace('T', ' ', $m['importado'])) ?></td></tr>
    <?php endforeach; ?>
    </tbody>
  </table></div>
<?php endif; ?>

<?php endif; ?>
</div>

<?php if (!$error && ($series || $tablas)): ?>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
const S = <?= json_encode($js, JSON_HEX_TAG | JSON_HEX_AMP | JSON_UNESCAPED_UNICODE) ?>;
const P = <?= json_encode($pj, JSON_HEX_TAG | JSON_HEX_AMP | JSON_UNESCAPED_UNICODE) ?>;

// Tablas ordenables
document.querySelectorAll('table.ord').forEach(t => {
  const body = t.tBodies[0];
  t.tHead.querySelectorAll('th').forEach((th, i) => {
    let asc = false;
    th.addEventListener('click', () => {
      asc = !asc;
      [...body.rows].sort((a, b) => {
        const vx = a.cells[i].dataset.v ?? '', vy = b.cells[i].dataset.v ?? '';
        const nx = parseFloat(vx), ny = parseFloat(vy);
        const c = (!isNaN(nx) && !isNaN(ny) && String(nx) === String(vx) && String(ny) === String(vy)) ? nx - ny : String(vx).localeCompare(String(vy), 'es');
        return asc ? c : -c;
      }).forEach(r => body.appendChild(r));
    });
  });
});

if (typeof Chart !== 'undefined') {
  const css = getComputedStyle(document.documentElement);
  const col = n => css.getPropertyValue(n).trim();
  Chart.defaults.color = col('--muted');
  Chart.defaults.borderColor = col('--line');
  Chart.defaults.font.family = 'system-ui, sans-serif';
  // Publicaciones: barras agrupadas (alcance/vistas) y apiladas (interacciones)
  const paleta = ['--accent', '--ig', '--tt', '--yt', '--good', '--muted'];
  const esInter = n => /like|me gusta|share|compart|follow|segui|comment|coment|save|guard/i.test(n);
  const esAlc = n => /view|vista|reach|alcance|reprod/i.test(n);
  P.forEach(p => {
    const mk = (suf, filtro, apilado) => {
      const el = document.getElementById(p.id + suf); if (!el) return;
      const nombres = Object.keys(p.series).filter(filtro);
      if (!nombres.length) { el.closest('.card').style.display = 'none'; return; }
      new Chart(el, { type: 'bar',
        data: { labels: p.labels, datasets: nombres.map((n, i) => ({ label: n, data: p.series[n], backgroundColor: col(paleta[i % paleta.length]), borderRadius: 2 })) },
        options: { responsive: true, maintainAspectRatio: false, interaction: { mode: 'index', intersect: false },
          plugins: { legend: { display: true, labels: { boxWidth: 10 } } },
          scales: { x: { stacked: apilado, grid: { display: false } }, y: { stacked: apilado, beginAtZero: true, ticks: { precision: 0 } } } } });
    };
    mk('a', esAlc, false);
    mk('b', n => esInter(n) && !esAlc(n), true);
  });
  S.forEach(s => {
    const el = document.getElementById(s.id); if (!el) return;
    new Chart(el, {
      type: s.line ? 'line' : 'bar',
      data: { labels: s.labels, datasets: [{ label: s.m, data: s.data, borderColor: col('--accent'),
        backgroundColor: s.line ? col('--accent-soft') : col('--accent'), fill: s.line, pointRadius: s.line ? 2 : 0, tension: .25, borderRadius: 2 }] },
      options: { responsive: true, maintainAspectRatio: false, interaction: { mode: 'index', intersect: false },
        plugins: { legend: { display: false } },
        scales: { x: { ticks: { maxTicksLimit: 7 }, grid: { display: false } }, y: { beginAtZero: !s.line, ticks: { precision: 0 } } } }
    });
  });
}
</script>
<?php endif; ?>
</body>
</html>
