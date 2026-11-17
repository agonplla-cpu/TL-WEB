# -*- coding: utf-8 -*-
"""Contenus du site TL Propreté (textes rédigés pour la refonte)."""

SITE = "https://www.tlproprete.fr"
EMAIL = "contact@tlproprete.fr"
PHONE = "06 05 03 10 96"
PHONE_INTL = "+33605031096"
STREET = "19 avenue du Nord"
POSTCODE = "69160"
CITY = "Tassin-la-Demi-Lune"
HOURS = "Du lundi au vendredi, de 8 h à 18 h"

# Mentions légales (registre national des entreprises, novembre 2026)
LEGAL_NAME = "TL Propreté"
LEGAL_FORM = "SAS"
CAPITAL = "1 000 €"
SIRET = "982 433 294 00013"
RCS = "RCS Lyon 982 433 294"
TVA = "FR96982433294"
PUBLISHER = "Agon Pllana, directeur général"
HOST = ("SAS PulseHeberg, 9 boulevard de Strasbourg, 83000 Toulon. Téléphone : 04 22 14 13 60. "
        "RCS Toulon 824 070 619.")

ZONES = [
    ("Lyon", ["Tous les arrondissements, du 1er au 9e"]),
    ("Ouest lyonnais", ["Tassin-la-Demi-Lune", "Écully"]),
    ("Nord et est", ["Caluire-et-Cuire", "Rillieux-la-Pape", "Villeurbanne", "Bron"]),
    ("Sud", ["Vénissieux", "Oullins-Pierre-Bénite"]),
]
AREA_SERVED = ["Lyon", "Tassin-la-Demi-Lune", "Écully", "Caluire-et-Cuire", "Rillieux-la-Pape",
               "Villeurbanne", "Bron", "Vénissieux", "Oullins-Pierre-Bénite"]

# ------------------------------------------------------------------ prestations
SERVICES = [
    {
        "slug": "nettoyage-copropriete-lyon",
        "name": "Copropriétés et immeubles",
        "short": "Halls, escaliers, ascenseurs, locaux poubelles et sortie des containers, selon un cahier des charges écrit pour chaque résidence.",
        "title": "Nettoyage de copropriété à Lyon : parties communes et containers | TL Propreté",
        "desc": "Entretien des parties communes de copropriétés à Lyon et dans la métropole : halls, escaliers, ascenseurs, containers, lavage des bacs suivi par QR code. Devis gratuit.",
        "h1": "Nettoyage de copropriétés à Lyon",
        "lead": "Halls, escaliers, paliers, ascenseurs, locaux poubelles, parkings : l'entretien des parties communes, organisé dans un cahier des charges propre à chaque résidence et validé avec le syndic.",
        "image": True,
        "items": [
            ("Halls d'entrée", "sols, portes vitrées, boîtes aux lettres, miroirs, tapis"),
            ("Escaliers et paliers", "balayage, lavage, rampes et mains courantes"),
            ("Ascenseurs", "cabine, miroirs, portes palières, seuils"),
            ("Locaux poubelles", "nettoyage et désinfection"),
            ("Containers", "sortie et rentrée selon le calendrier de collecte"),
            ("Lavage des bacs", "chaque lavage validé par QR code dans le local"),
            ("Parkings et caves", "balayage, enlèvement des déchets abandonnés"),
            ("Abords et pelouses", "selon les prestations mensuelles prévues"),
            ("Vitrerie des parties communes", "portes de hall, cages d'escalier"),
            ("Remplacement du gardien", "pendant ses congés ou une absence"),
        ],
        "freqs": ["Halls : jusqu'à 5 jours sur 7", "Containers : au rythme de la collecte", "Prestations mensuelles", "Vitrerie : 1 à 4 fois par an"],
        "for": "Syndics, gestionnaires de copropriété, conseils syndicaux, bailleurs.",
        "body": [
            ("Un cahier des charges par résidence",
             ["Avant de commencer, nous visitons la résidence avec vous. Chaque espace est relevé avec sa fréquence d'entretien : halls 5 jours sur 7, ordures ménagères les lundis, jeudis et samedis, tri sélectif les mardis et vendredis, vitrerie du hall chaque trimestre. Ce document sert de référence à nos agents, au syndic et au conseil syndical.",
              "Si vous reprenez la résidence d'un autre prestataire, nous partons du planning existant, nous le vérifions sur place et nous reprenons les passages sans interruption pour les résidents."]),
            ("Les containers, sans oubli",
             ["La sortie et la rentrée des containers suivent le calendrier de collecte de la Métropole. Pour le lavage des bacs, l'agent valide chaque passage en scannant le QR code affiché dans le local : chaque lavage est daté, et l'historique peut être présenté au conseil syndical."]),
        ],
        "faq": [
            ("Comment est établi le cahier des charges ?", "Lors de la visite, nous relevons chaque espace et sa fréquence d'entretien. Le document est validé avec le syndic, et si vous le souhaitez avec le conseil syndical, avant le premier passage."),
            ("Pouvez-vous reprendre le contrat d'un autre prestataire ?", "Oui. Nous partons du planning en place, nous le vérifions sur place, puis nous reprenons les passages sans interruption."),
            ("Comment savoir que les bacs ont été lavés ?", "Chaque lavage est validé par l'agent avec le QR code affiché dans le local poubelles. La date de chaque passage est enregistrée."),
            ("Intervenez-vous le samedi ?", "Oui, lorsque le calendrier de collecte l'exige : sortie des ordures ménagères le samedi, par exemple."),
        ],
    },
    {
        "slug": "nettoyage-bureaux-lyon",
        "name": "Bureaux et locaux professionnels",
        "short": "Open spaces, salles de réunion, sanitaires et cuisines, entretenus avant ou après vos horaires.",
        "title": "Nettoyage de bureaux à Lyon, avant ou après vos horaires | TL Propreté",
        "desc": "Entretien de bureaux et locaux professionnels à Lyon : postes de travail, sols, sanitaires, cuisines, salles de réunion. Passages planifiés en dehors de vos horaires. Devis gratuit.",
        "h1": "Nettoyage de bureaux à Lyon",
        "lead": "Open spaces, salles de réunion, sanitaires, cuisines : un entretien régulier, réalisé avant l'arrivée de vos équipes ou après leur départ.",
        "items": [
            ("Postes de travail", "dépoussiérage des surfaces dégagées"),
            ("Sols", "aspiration des moquettes, lavage des sols durs"),
            ("Sanitaires", "nettoyage, désinfection, réassort des consommables fournis"),
            ("Cuisines et espaces de pause", "plans de travail, éviers, électroménager en façade"),
            ("Corbeilles", "vidage et respect du tri en place"),
            ("Salles de réunion", "tables, chaises, tableaux blancs sur demande"),
            ("Points de contact", "poignées, interrupteurs, boutons d'ascenseur"),
            ("Accueil et vitres intérieures", "comptoir, portes vitrées, cloisons"),
        ],
        "freqs": ["Quotidien", "2 à 3 fois par semaine", "Hebdomadaire", "Tôt le matin ou en soirée"],
        "for": "Entreprises, cabinets, agences, professions libérales, associations.",
        "body": [
            ("Des passages qui ne gênent personne",
             ["Nous intervenons en dehors de vos horaires, ou pendant si vos locaux l'exigent. Si vous le souhaitez, nos agents interviennent en votre absence, avec un accès confié selon une procédure convenue ensemble.",
              "La fréquence se règle sur l'usage réel des lieux : un passage quotidien pour un plateau très fréquenté, deux ou trois par semaine pour des bureaux plus calmes. Elle peut évoluer en cours de contrat."]),
        ],
        "faq": [
            ("Intervenez-vous en dehors des heures de bureau ?", "Oui. La plupart de nos passages ont lieu tôt le matin ou en fin de journée, pour que vos équipes arrivent dans des locaux propres."),
            ("Peut-on changer la fréquence en cours de contrat ?", "Oui. Si l'occupation de vos locaux évolue, nous ajustons le nombre de passages."),
            ("Faut-il être présent pendant l'intervention ?", "Non. L'accès est organisé avec vous lors de la mise en place : clés, badge ou code, selon votre procédure."),
        ],
    },
    {
        "slug": "nettoyage-commerces-hotels-lyon",
        "name": "Commerces et hôtels",
        "short": "Surfaces de vente, vitrines, sanitaires clients, halls et couloirs d'hôtels, au rythme de vos horaires d'ouverture.",
        "title": "Nettoyage de commerces et d'hôtels à Lyon | TL Propreté",
        "desc": "Nettoyage de boutiques, restaurants et hôtels à Lyon : surfaces de vente, vitrines, sanitaires, halls et parties communes. Interventions calées sur vos horaires. Devis gratuit.",
        "h1": "Nettoyage de commerces et d'hôtels à Lyon",
        "lead": "Boutiques, restaurants, hôtels : des interventions calées sur vos horaires d'ouverture, pour accueillir vos clients dans un lieu impeccable.",
        "items": [
            ("Surfaces de vente", "sols, rayonnages, présentoirs"),
            ("Vitrines et devantures", "intérieur et extérieur"),
            ("Cabines et sanitaires clients", "nettoyage et désinfection"),
            ("Salles de restaurant", "sols, banquettes, abords des tables"),
            ("Halls et réception d'hôtel", "sols, comptoir, mobilier, vitres"),
            ("Couloirs et escaliers d'hôtel", "aspiration, lavage, plinthes"),
            ("Salles de petit-déjeuner", "remise en état après le service"),
            ("Espaces du personnel", "vestiaires, salles de pause"),
        ],
        "freqs": ["Avant l'ouverture", "Après la fermeture", "Plusieurs fois par semaine", "7 jours sur 7 si nécessaire"],
        "for": "Boutiques, restaurants, hôtels, résidences de tourisme, showrooms.",
        "body": [
            ("Le lieu est prêt quand vous ouvrez",
             ["Un commerce se juge en quelques secondes : la vitrine, le sol, l'odeur, les sanitaires. Nous planifions nos passages avant l'ouverture ou après la fermeture, y compris le week-end pour les lieux ouverts tous les jours.",
              "Dans les hôtels, nous prenons en charge le hall, la réception, les couloirs et les espaces communs, en coordination avec votre équipe."]),
        ],
        "faq": [
            ("Intervenez-vous le dimanche ?", "Oui, pour les lieux ouverts tous les jours. Le planning est défini avec vous lors du devis."),
            ("Nettoyez-vous les chambres d'hôtel ?", "Nous intervenons surtout sur les parties communes : hall, réception, couloirs, salles de petit-déjeuner. Parlez-nous de votre besoin lors de la demande de devis."),
            ("Pouvez-vous nettoyer la vitrine côté rue ?", "Oui, à l'intérieur comme à l'extérieur, au rythme que vous choisissez."),
        ],
    },
    {
        "slug": "nettoyage-fin-de-chantier-lyon",
        "name": "Fin de chantier",
        "short": "Poussière, traces de peinture, adhésifs et résidus enlevés : des locaux prêts pour la réception ou la remise des clés.",
        "title": "Nettoyage de fin de chantier à Lyon, avant livraison | TL Propreté",
        "desc": "Nettoyage après travaux à Lyon : dépoussiérage complet, décollement des films et adhésifs, vitres, sols et sanitaires. Locaux prêts pour la réception ou la remise des clés.",
        "h1": "Nettoyage de fin de chantier à Lyon",
        "lead": "Après les travaux, nous livrons des locaux prêts à être occupés : poussière, traces de peinture, films de protection et résidus de chantier enlevés.",
        "items": [
            ("Dépoussiérage complet", "murs, plinthes, huisseries, radiateurs"),
            ("Films et adhésifs", "décollement sur vitres, menuiseries, équipements"),
            ("Traces de peinture et de plâtre", "sur sols, vitres et menuiseries"),
            ("Vitres et menuiseries", "intérieur et extérieur accessible"),
            ("Sols", "aspiration et lavage adaptés au revêtement"),
            ("Sanitaires et cuisines", "appareils, faïences, robinetterie"),
            ("Parties communes", "halls, escaliers, ascenseurs avant livraison"),
            ("Déchets légers", "évacuation des résidus de nettoyage"),
        ],
        "freqs": ["Intervention ponctuelle", "Nettoyage en deux temps", "Avant réception ou remise des clés"],
        "for": "Promoteurs, maîtres d'ouvrage, entreprises du bâtiment, syndics après travaux.",
        "body": [
            ("Le bon moment pour intervenir",
             ["Nous intervenons après le départ des corps de métier, avant la réception des travaux ou la remise des clés. Sur les chantiers importants, un premier nettoyage pendant les finitions, puis un nettoyage fin avant la livraison, évitent de refaire deux fois le même travail."]),
        ],
        "faq": [
            ("Quand faut-il prévoir le nettoyage ?", "Après le départ des derniers corps de métier et avant la réception ou la remise des clés. Prévenez-nous dès que la date de livraison est connue."),
            ("Intervenez-vous en plusieurs fois ?", "Oui, si le chantier le demande : un nettoyage pendant les finitions, puis un nettoyage fin avant la livraison."),
            ("Évacuez-vous les gravats ?", "Non. Nous évacuons les résidus du nettoyage ; les gravats et déchets de chantier relèvent des entreprises de travaux."),
        ],
    },
    {
        "slug": "nettoyage-vitres-lyon",
        "name": "Vitrerie",
        "short": "Devantures, baies vitrées, portes de hall et verrières, à l'intérieur comme à l'extérieur.",
        "title": "Nettoyage de vitres à Lyon : vitrines, baies, halls | TL Propreté",
        "desc": "Nettoyage de vitres à Lyon pour commerces, bureaux et copropriétés : vitrines, baies vitrées, portes de hall, verrières. Intérieur et extérieur, ponctuel ou régulier.",
        "h1": "Nettoyage de vitres à Lyon",
        "lead": "Devantures, baies vitrées, portes de hall, verrières : un nettoyage sans traces, à l'intérieur comme à l'extérieur, partout où l'accès se fait en sécurité.",
        "items": [
            ("Vitres et encadrements", "vitrage, joints, rebords"),
            ("Vitrines commerciales", "côté rue et côté boutique"),
            ("Portes de hall", "portes vitrées, impostes, sas"),
            ("Baies vitrées et cloisons", "bureaux, salles de réunion"),
            ("Cages d'escalier", "fenêtres des parties communes"),
            ("Verrières et parties hautes", "accessibles à la perche ou à l'escabeau"),
        ],
        "freqs": ["Mensuel", "Trimestriel", "Annuel", "Ponctuel"],
        "for": "Commerces, bureaux, copropriétés, hôtels.",
        "body": [
            ("Selon la hauteur et l'accès",
             ["Nous travaillons depuis le sol, à la perche ou à l'escabeau. Pour une façade qui demande une nacelle ou des cordistes, nous vous le disons dès la visite, avant tout devis."]),
        ],
        "faq": [
            ("Nettoyez-vous les vitres en hauteur ?", "Oui, tant que l'accès se fait en sécurité depuis le sol, à la perche ou à l'escabeau. Pour une façade nécessitant une nacelle, nous vous le signalons lors de la visite."),
            ("À quelle fréquence nettoyer une vitrine ?", "Une vitrine de commerce se nettoie souvent chaque semaine ; les vitres d'un hall de copropriété, une à quatre fois par an selon l'exposition."),
            ("Le nettoyage des vitres peut-il s'ajouter à un contrat existant ?", "Oui, en prestation régulière ou ponctuelle."),
        ],
    },
    {
        "slug": "remise-en-etat-lyon",
        "name": "Remise en état",
        "short": "Décapage, cristallisation du marbre, shampoing moquette, remise en état locative : quand l'entretien courant ne suffit plus.",
        "title": "Remise en état de locaux à Lyon : décapage, cristallisation | TL Propreté",
        "desc": "Remise en état de locaux à Lyon : décapage des sols, cristallisation du marbre, shampoing moquette, remise en état avant ou après état des lieux. Devis gratuit.",
        "h1": "Remise en état de locaux à Lyon",
        "lead": "Décapage, cristallisation, shampoing moquette, remise en état avant un état des lieux : quand un nettoyage courant ne suffit plus.",
        "items": [
            ("Décapage des sols", "élimination des anciennes couches et salissures incrustées"),
            ("Protection des sols", "pose d'une émulsion après décapage"),
            ("Cristallisation", "sols en marbre et pierre calcaire, halls d'immeuble"),
            ("Shampoing moquette", "bureaux, couloirs, salles de réunion"),
            ("Remise en état locative", "avant ou après un état des lieux"),
            ("Détartrage des sanitaires", "faïences, robinetterie, appareils"),
        ],
        "freqs": ["Intervention ponctuelle", "Une à deux fois par an"],
        "for": "Copropriétés, bureaux, commerces, bailleurs, agences immobilières.",
        "body": [
            ("Rendre son éclat à un sol",
             ["La cristallisation est un traitement des sols en marbre ou en pierre calcaire : elle leur rend leur brillant et les protège de l'usure. Elle convient particulièrement aux halls d'immeuble, très fréquentés.",
              "Le décapage élimine les couches de cire et les salissures incrustées des sols plastiques ou thermoplastiques, avant la pose d'une nouvelle protection."]),
        ],
        "faq": [
            ("Qu'est-ce que la cristallisation ?", "Un traitement des sols en marbre ou en pierre calcaire, qui leur rend leur brillant et les rend plus résistants à l'usure."),
            ("Faut-il libérer les lieux ?", "Pour un décapage ou une cristallisation, la zone traitée doit rester libre de passage le temps de l'intervention et du séchage. Nous planifions selon vos contraintes."),
            ("Faites-vous la remise en état avant un état des lieux ?", "Oui, pour les bailleurs, les agences et les locataires sortants."),
        ],
    },
    {
        "slug": "remplacement-gardien-lyon",
        "name": "Remplacement de gardien",
        "short": "Congés, arrêt ou départ : les tâches d'entretien du gardien sont assurées et la résidence reste tenue.",
        "title": "Remplacement de gardien d'immeuble à Lyon | TL Propreté",
        "desc": "Remplacement de gardien de copropriété à Lyon pendant les congés, un arrêt ou un recrutement : entretien des parties communes, containers, signalement des anomalies au syndic.",
        "h1": "Remplacement de gardien d'immeuble à Lyon",
        "lead": "Congés, arrêt, départ : nous assurons les tâches d'entretien du gardien pour que la résidence reste tenue jusqu'à son retour ou jusqu'au recrutement.",
        "items": [
            ("Entretien des parties communes", "halls, escaliers, paliers, ascenseurs"),
            ("Containers", "sortie et rentrée selon la collecte"),
            ("Locaux poubelles", "nettoyage et lavage des bacs"),
            ("Abords de la résidence", "entrées, cours, parkings"),
            ("Signalement au syndic", "éclairage en panne, porte bloquée, dégradation constatée"),
        ],
        "freqs": ["Quelques jours", "Plusieurs semaines", "Le temps d'un recrutement"],
        "for": "Syndics et gestionnaires de copropriété.",
        "body": [
            ("Un périmètre fixé avec le syndic",
             ["Nous reprenons les tâches d'entretien prévues au contrat du gardien ou au cahier des charges de la résidence. Le périmètre et la durée sont définis avec le syndic avant le premier jour."]),
        ],
        "faq": [
            ("Pour quelle durée ?", "Ponctuellement pendant des congés, ou dans la durée, le temps d'un recrutement."),
            ("Les tâches sont-elles les mêmes qu'avec le gardien ?", "Nous reprenons les tâches d'entretien prévues. Le périmètre exact est validé avec le syndic avant le début."),
            ("Pouvez-vous intervenir rapidement ?", "Contactez-nous dès que l'absence est connue : nous organisons la visite et le démarrage avec vous."),
        ],
    },
]

HOME_FAQ = [
    ("Le devis est-il payant ?", "Non. La visite et le devis sont gratuits et sans engagement."),
    ("Travaillez-vous avec les syndics ?", "Oui, c'est l'essentiel de notre activité : nous entretenons des copropriétés gérées par plusieurs cabinets lyonnais, avec un cahier des charges par résidence."),
    ("Pouvez-vous reprendre le contrat d'un autre prestataire ?", "Oui. Nous partons du planning en place, nous le vérifions sur place, puis nous reprenons les passages sans interruption pour les résidents."),
    ("Intervenez-vous le week-end ?", "Oui, quand le lieu l'exige : sortie des containers le samedi, commerces et hôtels ouverts tous les jours. Notre bureau répond du lundi au vendredi, de 8 h à 18 h."),
    ("Dans quelles communes intervenez-vous ?", "À Lyon et dans la métropole, depuis Tassin-la-Demi-Lune. Pour une commune qui ne figure pas dans la liste, demandez-nous."),
]
