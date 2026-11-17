<?php
/**
 * TL Propreté — réception des demandes de devis
 * Envoie la demande par e-mail à contact@tlproprete.fr.
 * Répond en JSON (envoi depuis la page) ou redirige vers /merci/ (navigateur sans JavaScript).
 */
declare(strict_types=1);

const DESTINATAIRE = 'contact@tlproprete.fr';
const EXPEDITEUR   = 'site@tlproprete.fr';      // adresse du domaine (elle n'a pas besoin de boîte de réception)
const MAX_PAR_HEURE = 6;                         // par adresse IP
date_default_timezone_set('Europe/Paris');

$wantsJson = isset($_SERVER['HTTP_ACCEPT']) && strpos($_SERVER['HTTP_ACCEPT'], 'application/json') !== false;

function repondre(bool $ok, string $erreur = '', int $code = 200): void {
    global $wantsJson;
    http_response_code($code);
    if ($wantsJson) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode($ok ? ['ok' => true] : ['ok' => false, 'error' => $erreur], JSON_UNESCAPED_UNICODE);
    } else {
        header('Location: ' . ($ok ? '/merci/' : '/contact/?erreur=1'), true, 303);
    }
    exit;
}

function champ(string $nom, int $max): string {
    $v = isset($_POST[$nom]) && is_string($_POST[$nom]) ? $_POST[$nom] : '';
    $v = str_replace(["\r\n", "\r"], "\n", $v);
    $v = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $v) ?? '';
    $v = trim($v);
    return function_exists('mb_substr') ? mb_substr($v, 0, $max, 'UTF-8') : substr($v, 0, $max);
}

function uneLigne(string $v): string {
    return trim(preg_replace('/\s+/u', ' ', $v) ?? '');
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    repondre(false, 'Méthode non autorisée.', 405);
}

/* --- Anti-robots --- */
if (champ('site_web', 200) !== '') {
    repondre(true); // champ piège rempli : on fait comme si tout allait bien
}
$t = (int) champ('t', 20);
if ($t > 0 && (time() - $t) < 3) {
    repondre(false, "L'envoi a été trop rapide. Patientez quelques secondes et réessayez.", 429);
}

/* --- Limite par IP --- */
$ip = $_SERVER['REMOTE_ADDR'] ?? '0';
$fichier = rtrim(sys_get_temp_dir(), '/') . '/tlp_devis_' . hash('sha256', $ip . __FILE__);
$horodatages = [];
if (is_readable($fichier)) {
    $horodatages = array_filter(array_map('intval', explode(',', (string) file_get_contents($fichier))), function ($x) { return $x > time() - 3600; });
}
if (count($horodatages) >= MAX_PAR_HEURE) {
    repondre(false, 'Trop de demandes envoyées depuis votre connexion. Écrivez-nous directement à ' . DESTINATAIRE . '.', 429);
}

/* --- Champs --- */
$prestations = [
    'nettoyage-copropriete-lyon' => 'Copropriétés et immeubles',
    'nettoyage-bureaux-lyon' => 'Bureaux et locaux professionnels',
    'nettoyage-commerces-hotels-lyon' => 'Commerces et hôtels',
    'nettoyage-fin-de-chantier-lyon' => 'Fin de chantier',
    'nettoyage-vitres-lyon' => 'Vitrerie',
    'remise-en-etat-lyon' => 'Remise en état',
    'remplacement-gardien-lyon' => 'Remplacement de gardien',
    'autre' => 'Autre besoin',
];
$nom       = uneLigne(champ('nom', 120));
$societe   = uneLigne(champ('societe', 160));
$email     = uneLigne(champ('email', 160));
$tel       = uneLigne(champ('telephone', 40));
$lieu      = uneLigne(champ('lieu', 200));
$taille    = uneLigne(champ('taille', 80));
$qui       = uneLigne(champ('qui', 80));
$frequence = uneLigne(champ('frequence', 80));
$message   = champ('message', 4000);
$cle       = champ('prestation', 60);
$prestation = $prestations[$cle] ?? 'Non précisée';

if ($nom === '' || $email === '' || $lieu === '' || $message === '') {
    repondre(false, 'Merci de remplir le nom, l’e-mail, l’adresse du lieu et votre besoin.', 422);
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    repondre(false, 'Cette adresse e-mail n’est pas valide. Exemple : nom@domaine.fr', 422);
}
if (preg_match_all('~https?://~i', $message) > 3) {
    repondre(false, 'Votre message contient trop de liens. Retirez-les et réessayez.', 422);
}

/* --- E-mail --- */
$lignes = [
    'Nouvelle demande de devis depuis tlproprete.fr',
    '',
    'Prestation : ' . $prestation,
    'Demandeur : ' . ($qui !== '' ? $qui : '—'),
    'Nom : ' . $nom,
    'Société / résidence : ' . ($societe !== '' ? $societe : '—'),
    'E-mail : ' . $email,
    'Téléphone : ' . ($tel !== '' ? $tel : '—'),
    'Lieu : ' . $lieu,
    'Surface / logements : ' . ($taille !== '' ? $taille : '—'),
    'Fréquence souhaitée : ' . ($frequence !== '' ? $frequence : '—'),
    '',
    'Besoin :',
    $message,
    '',
    '—',
    'Reçu le ' . date('d/m/Y à H:i') . ' — IP ' . $ip,
];
$corps = implode("\r\n", $lignes);

$sujet = 'Demande de devis — ' . $prestation . ' — ' . $lieu;
$sujetEncode = '=?UTF-8?B?' . base64_encode($sujet) . '?=';
$nomEncode = '=?UTF-8?B?' . base64_encode('Site TL Propreté') . '?=';

$entetes = [
    'From: ' . $nomEncode . ' <' . EXPEDITEUR . '>',
    'Reply-To: ' . $email,       // validé par filter_var : pas de retour à la ligne possible
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'X-Mailer: tlproprete.fr',
];

$envoye = @mail(DESTINATAIRE, $sujetEncode, $corps, implode("\r\n", $entetes), '-f' . EXPEDITEUR);
if (!$envoye) {
    repondre(false, 'L’envoi n’a pas abouti. Écrivez-nous directement à ' . DESTINATAIRE . '.', 500);
}

$horodatages[] = time();
@file_put_contents($fichier, implode(',', $horodatages), LOCK_EX);
repondre(true);
