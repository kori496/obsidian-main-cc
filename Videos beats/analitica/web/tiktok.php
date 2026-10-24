<?php
/**
 * lagrim-stats · TikTok. Lee las tablas tiktok_* de datos/youtube.db
 * (las llena importar_tiktok.py a partir de los CSV de TikTok Studio).
 */
declare(strict_types=1);

/**
 * Guarda el CSV subido en tiktok/entrada/ y ejecuta importar_tiktok.py.
 * Devuelve el mensaje para mostrar; $ok queda en true si la importacion termino bien.
 */
function subirCsv(?array $f, bool &$ok): string {
    $ok = false;
    if (!$f || ($f['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK) {
        return 'No se recibió el archivo (código de error ' . ($f['error'] ?? '?') . ').';
    }
    if (strtolower(pathinfo((string)$f['name'], PATHINFO_EXTENSION)) !== 'csv') {
        return 'Solo se aceptan archivos .csv de TikTok Studio.';
    }
    if ((int)$f['size'] > 5 * 1024 * 1024) {
        return 'El archivo pesa más de 5 MB; un CSV de TikTok debería pesar mucho menos.';
    }
    $dir = __DIR__ . '/../tiktok/entrada';
    if (!is_dir($dir) && !mkdir($dir, 0777, true)) {
        return 'No se pudo crear la carpeta tiktok/entrada.';
    }
    $nombre = preg_replace('/[^A-Za-z0-9_. -]/', '_', basename((string)$f['name']));
    $destino = $dir . '/' . date('Ymd_His') . '_' . $nombre;
    if (!move_uploaded_file($f['tmp_name'], $destino)) {
        return 'No se pudo guardar el archivo en tiktok/entrada.';
    }
    $py = getenv('LAGRIM_PYTHON') ?: 'python';
    $script = __DIR__ . '/../importar_tiktok.py';
    $salida = [];
    $codigo = 0;
    exec(escapeshellcmd($py) . ' ' . escapeshellarg($script) . ' 2>&1', $salida, $codigo);
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
    header('Location: tiktok.php?' . http_build_query(['msg' => $msg, 'ok' => $ok ? '1' : '0']));
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
    $error = 'Todavía no hay datos. Ejecuta primero: python yt_stats.py (crea la base de datos) y luego python importar_tiktok.py';
} else {
    try {
        $db = new PDO('sqlite:' . $dbPath);
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
        $has = (bool)$db->query("SELECT 1 FROM sqlite_master WHERE type='table' AND name='tiktok_archivo'")->fetch();
        if ($has) {
            foreach ($db->query('SELECT tipo, metrica, fecha, valor FROM tiktok_serie ORDER BY rowid') as $r) {
                $series[$r['tipo']][$r['metrica']][] = [$r['fecha'], (float)$r['valor']];
            }
            foreach ($series as $t => $mets) {            // puntos en orden cronologico
                foreach ($mets as $m => $pts) { usort($pts, fn($x, $y) => strcmp($x[0], $y[0])); $series[$t][$m] = $pts; }
            }
            uksort($series, fn($x, $y) => ($y === 'overview') <=> ($x === 'overview') ?: strcmp($x, $y));
            $importaciones = $db->query('SELECT nombre, tipo, importado, filas, es_serie FROM tiktok_archivo ORDER BY id DESC LIMIT 12')->fetchAll();
            $ult = $db->query('SELECT a.* FROM tiktok_archivo a WHERE es_serie=0 AND id=(SELECT MAX(id) FROM tiktok_archivo WHERE tipo=a.tipo) ORDER BY tipo')->fetchAll();
            foreach ($ult as $a) {
                $filas = [];
                $q = $db->prepare('SELECT datos FROM tiktok_fila WHERE archivo_id=? ORDER BY n');
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
$ultImport = $importaciones ? $importaciones[0]['importado'] : null;
?><!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>lagrim-stats · TikTok</title>
<link rel="stylesheet" href="estilo.css">
</head>
<body>
<div class="wrap">
<header>
  <h1>lagrim-stats</h1>
  <nav class="nav"><a href="global.php">Global</a><a href="index.php">YouTube</a><a class="on" href="tiktok.php">TikTok</a><a href="instagram.php">Instagram</a><a href="descargas.php">Descargas</a></nav>
  <div class="acciones">
    <div class="sub"><?php if ($ultImport): ?>Última importación: <?= h(str_replace('T', ' ', $ultImport)) ?><?php endif; ?></div>
    <form method="post" enctype="multipart/form-data" class="subir">
      <input type="hidden" name="accion" value="subir">
      <label class="btn-subir">Subir CSV de TikTok<input type="file" name="csv" accept=".csv,text/csv" onchange="this.form.submit()"></label>
    </form>
  </div>
</header>

<?php if ($msgSubida !== null): ?>
  <div class="<?= $msgSubidaOk ? 'msg-ok' : 'error' ?>"><?= h($msgSubida) ?></div>
<?php endif; ?>

<?php if ($error): ?>
  <div class="error"><?= h($error) ?></div>
<?php elseif (!$series && !$tablas): ?>
  <div class="card">
    <h3>Aún no hay datos de TikTok</h3>
    <p>1. En <b>TikTok Studio → Analytics → Descargar datos</b> exporta el CSV.<br>
       2. Suéltalo en la carpeta <code>analitica/tiktok/entrada/</code>.<br>
       3. Ejecuta <code>python importar_tiktok.py</code> y recarga esta página.</p>
    <p class="sub">TikTok solo deja exportar los últimos 7, 28 o 60 días. Cada importación se une con las anteriores, así el historial va creciendo.</p>
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
