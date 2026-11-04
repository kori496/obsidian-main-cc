<?php
/**
 * lagrim-stats · API de descargas (la usa web/descargas.php).
 *   GET  ?accion=motores                      -> lista de motores y redes compatibles
 *   POST accion=descargar, url, motor         -> descarga con motores_descargas.py
 *   POST accion=abrir, archivo                -> abre el Explorador con el archivo seleccionado
 */
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
set_time_limit(0);

function responder(array $datos, int $codigo = 200): void {
    http_response_code($codigo);
    echo json_encode($datos, JSON_UNESCAPED_UNICODE);
    exit;
}

/** Ejecuta motores_descargas.py y devuelve el JSON que imprime (o null si falla). */
function correrPython(string $argumentos): ?array {
    $py = getenv('LAGRIM_PYTHON') ?: 'python';
    $script = __DIR__ . '/../motores_descargas.py';
    $salida = [];
    $codigo = 0;
    exec('"' . str_replace('"', '', $py) . '" ' . escapeshellarg($script) . ' ' . $argumentos, $salida, $codigo);
    $json = json_decode(implode("\n", $salida), true);
    return is_array($json) ? $json : null;
}

$accion = (string)($_REQUEST['accion'] ?? 'motores');
$esPost = $_SERVER['REQUEST_METHOD'] === 'POST';

if ($accion === 'motores') {
    $lista = correrPython('listar');
    if ($lista === null) {
        responder(['ok' => false, 'mensaje' => 'No se pudo leer la lista de motores. ¿Está instalado Python?'], 500);
    }
    responder(['ok' => true, 'motores' => $lista]);
}

if ($accion === 'descargar' && $esPost) {
    $url = trim((string)($_POST['url'] ?? ''));
    $motor = (string)($_POST['motor'] ?? 'auto');
    if (!preg_match('~^https?://\S+$~i', $url)) {
        responder(['ok' => false, 'mensaje' => 'Escribe un enlace que empiece por http:// o https://'], 400);
    }
    $resultado = correrPython('descargar ' . escapeshellarg($motor) . ' ' . escapeshellarg($url));
    if ($resultado === null) {
        responder(['ok' => false, 'mensaje' => 'La descarga no devolvió respuesta. Revisa que Python y las herramientas estén instaladas.'], 500);
    }
    responder($resultado, !empty($resultado['ok']) ? 200 : 500);
}

if ($accion === 'abrir' && $esPost) {
    $base = realpath(__DIR__ . '/../descargas');
    $ruta = $base ? realpath($base . DIRECTORY_SEPARATOR . (string)($_POST['archivo'] ?? '')) : false;

    // Solo se puede abrir algo que esté dentro de la carpeta descargas
    if (!$ruta || strncmp($ruta, $base . DIRECTORY_SEPARATOR, strlen($base) + 1) !== 0 || !is_file($ruta)) {
        responder(['ok' => false, 'mensaje' => 'No encontré el archivo.'], 404);
    }

    if (PHP_OS_FAMILY === 'Windows') {
        pclose(popen('start "" explorer.exe /select,"' . $ruta . '"', 'r'));
    } elseif (PHP_OS_FAMILY === 'Darwin') {
        exec('open -R ' . escapeshellarg($ruta));
    } else {
        exec('xdg-open ' . escapeshellarg(dirname($ruta)));
    }
    responder(['ok' => true]);
}

responder(['ok' => false, 'mensaje' => 'Acción no válida.'], 400);
