<?php
/* Usage unique : télécharge trois photos libres de droit (licence Unsplash) dans assets/img/photos/, puis se supprime. */
declare(strict_types=1);
header('Content-Type: text/plain; charset=utf-8');
if (($_GET['k'] ?? '') !== 'tl-libres-1117') { http_response_code(404); exit; }
$dir = __DIR__ . '/assets/img/photos';
if (!is_dir($dir)) { mkdir($dir, 0755, true); }
$list = ['s1-vitres' => 'photo-1721620958961-cccc239cbb49', 's2-hall' => 'photo-1630703125789-6416b14d1705', 's3-bureaux' => 'photo-1631248988030-141c05a37dd2'];
$ok = 0;
foreach ($list as $name => $id) {
    $ch = curl_init("https://images.unsplash.com/$id?w=1000&h=1333&fit=crop&q=82&fm=jpg");
    curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_FOLLOWLOCATION => true, CURLOPT_MAXREDIRS => 5,
        CURLOPT_TIMEOUT => 40, CURLOPT_USERAGENT => 'Mozilla/5.0 (tlproprete.fr)']);
    $bin = curl_exec($ch); $code = curl_getinfo($ch, CURLINFO_HTTP_CODE); curl_close($ch);
    if ($code === 200 && is_string($bin) && strlen($bin) > 30000 && substr($bin, 0, 2) === "\xFF\xD8") {
        file_put_contents("$dir/$name.jpg", $bin);
        $s = getimagesize("$dir/$name.jpg");
        echo "$name.jpg ", strlen($bin), ' ', $s[0], 'x', $s[1], "\n"; $ok++;
    } else {
        echo "$name ECHEC code $code taille ", is_string($bin) ? strlen($bin) : 0, "\n";
    }
}
echo "total $ok\n";
if ($ok === count($list)) { @unlink(__FILE__); }
