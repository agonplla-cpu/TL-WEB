<?php
/* Usage unique : extrait les photos intégrées dans l'ancienne page tlproprete_v5.html
   vers assets/img/photos/, puis se supprime. */
declare(strict_types=1);
header('Content-Type: text/plain; charset=utf-8');
if (($_GET['k'] ?? '') !== 'tl-photos-1117') { http_response_code(404); exit; }
$src = __DIR__ . '/tlproprete_v5.html';
if (!is_readable($src)) { exit("source introuvable\n"); }
$html = (string) file_get_contents($src);
$dir = __DIR__ . '/assets/img/photos';
if (!is_dir($dir) && !mkdir($dir, 0755, true)) { exit("dossier impossible\n"); }
preg_match_all('~data:image/(jpeg|jpg|png|webp);base64,([A-Za-z0-9+/=]+)~', $html, $m, PREG_SET_ORDER);
$seen = []; $n = 0;
foreach ($m as $x) {
    $bin = base64_decode($x[2], true);
    if ($bin === false || strlen($bin) < 20000) { continue; }
    $h = md5($bin);
    if (isset($seen[$h])) { continue; }
    $seen[$h] = 1; $n++;
    $ext = $x[1] === 'png' ? 'png' : ($x[1] === 'webp' ? 'webp' : 'jpg');
    $f = sprintf('%s/p%02d.%s', $dir, $n, $ext);
    file_put_contents($f, $bin);
    $s = @getimagesize($f);
    echo basename($f), ' ', strlen($bin), ' ', $s ? $s[0] . 'x' . $s[1] : '?', "\n";
}
echo "total $n\n";
@unlink(__FILE__);
