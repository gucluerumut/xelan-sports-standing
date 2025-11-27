// Club logo helper - provides logo URLs for all clubs
// Using Wikipedia Commons (works in browsers) with proper URLs

export function getClubLogoUrl(clubName: string): string | null {
    const logoMap: Record<string, string> = {
        // Premier League - Wikipedia Commons (browser-friendly URLs)
        "Manchester City": "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg",
        "Arsenal": "https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg",
        "Liverpool": "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg",
        "Aston Villa": "https://upload.wikimedia.org/wikipedia/en/f/f9/Aston_Villa_FC_crest_%282016%29.svg",
        "Tottenham Hotspur": "https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg",
        "Chelsea": "https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg",
        "Newcastle United": "https://upload.wikimedia.org/wikipedia/en/5/56/Newcastle_United_Logo.svg",
        "Manchester United": "https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg",
        "West Ham United": "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg",
        "Brighton & Hove Albion": "https://upload.wikimedia.org/wikipedia/en/f/fd/Brighton_%26_Hove_Albion_logo.svg",
        "Bournemouth": "https://upload.wikimedia.org/wikipedia/en/e/e5/AFC_Bournemouth_%282013%29.svg",
        "Fulham": "https://upload.wikimedia.org/wikipedia/en/e/eb/Fulham_FC_%28shield%29.svg",
        "Wolverhampton Wanderers": "https://upload.wikimedia.org/wikipedia/en/f/fc/Wolverhampton_Wanderers.svg",
        "Everton": "https://upload.wikimedia.org/wikipedia/en/7/7c/Everton_FC_logo.svg",
        "Brentford": "https://upload.wikimedia.org/wikipedia/en/2/2a/Brentford_FC_crest.svg",
        "Nottingham Forest": "https://upload.wikimedia.org/wikipedia/en/e/e5/Nottingham_Forest_F.C._logo.svg",
        "Crystal Palace": "https://upload.wikimedia.org/wikipedia/en/a/a2/Crystal_Palace_FC_logo_%282022%29.svg",
        "Leicester City": "https://upload.wikimedia.org/wikipedia/en/2/2d/Leicester_City_crest.svg",
        "Ipswich Town": "https://upload.wikimedia.org/wikipedia/en/4/43/Ipswich_Town.svg",
        "Southampton": "https://upload.wikimedia.org/wikipedia/en/c/c9/FC_Southampton.svg",

        // La Liga
        "Real Madrid": "https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg",
        "Barcelona": "https://upload.wikimedia.org/wikipedia/en/4/47/FC_Barcelona_%28crest%29.svg",
        "Atlético Madrid": "https://upload.wikimedia.org/wikipedia/en/f/f4/Atletico_Madrid_2017_logo.svg",
        "Athletic Bilbao": "https://upload.wikimedia.org/wikipedia/en/9/98/Club_Athletic_Bilbao_logo.svg",
        "Real Sociedad": "https://upload.wikimedia.org/wikipedia/en/f/f1/Real_Sociedad_logo.svg",
        "Real Betis": "https://upload.wikimedia.org/wikipedia/en/1/13/Real_betis_logo.svg",
        "Villarreal": "https://upload.wikimedia.org/wikipedia/en/b/b9/Villarreal_CF_logo-en.svg",
        "Valencia": "https://upload.wikimedia.org/wikipedia/en/c/ce/Valenciacf.svg",
        "Sevilla": "https://upload.wikimedia.org/wikipedia/en/3/3b/Sevilla_FC_logo.svg",
        "Girona": "https://upload.wikimedia.org/wikipedia/en/7/79/Girona_FC_logo.svg",
        "Osasuna": "https://upload.wikimedia.org/wikipedia/en/c/c2/CA_Osasuna_logo.svg",
        "Getafe": "https://upload.wikimedia.org/wikipedia/en/2/2e/Getafe_logo.svg",
        "Rayo Vallecano": "https://upload.wikimedia.org/wikipedia/en/6/6b/Rayo_Vallecano_logo.svg",
        "Celta Vigo": "https://upload.wikimedia.org/wikipedia/en/1/12/RC_Celta_de_Vigo_logo.svg",
        "Mallorca": "https://upload.wikimedia.org/wikipedia/en/e/e0/RCD_Mallorca.svg",
        "Las Palmas": "https://upload.wikimedia.org/wikipedia/en/2/20/UD_Las_Palmas_logo.svg",
        "Alavés": "https://upload.wikimedia.org/wikipedia/en/7/79/Deportivo_Alav%C3%A9s_logo.svg",
        "Espanyol": "https://upload.wikimedia.org/wikipedia/en/a/a7/RCD_Espanyol_logo.svg",
        "Leganés": "https://upload.wikimedia.org/wikipedia/en/c/c6/CD_Legan%C3%A9s_logo.svg",
        "Valladolid": "https://upload.wikimedia.org/wikipedia/en/8/8c/Real_Valladolid_Logo.svg",

        // Süper Lig
        "Galatasaray": "https://upload.wikimedia.org/wikipedia/commons/f/f6/Galatasaray_Sports_Club_Logo.png",
        "Fenerbahçe": "https://upload.wikimedia.org/wikipedia/en/8/86/Fenerbahce_SK_Logo.svg",
        "Beşiktaş": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Besiktas_JK_logo.svg",
        "Trabzonspor": "https://upload.wikimedia.org/wikipedia/commons/3/31/Trabzonspor_logo.svg",
        "İstanbul Başakşehir": "https://upload.wikimedia.org/wikipedia/en/0/0a/Istanbul_Basaksehir_FK.svg",
        "Samsunspor": "https://upload.wikimedia.org/wikipedia/en/9/9d/Samsunspor_logo.svg",
        "Göztepe": "https://upload.wikimedia.org/wikipedia/en/3/3b/G%C3%B6ztepe_SK_logo.svg",
        "Kasımpaşa": "https://upload.wikimedia.org/wikipedia/en/e/e8/Kasimpasa_SK.svg",
        "Sivasspor": "https://upload.wikimedia.org/wikipedia/en/0/0d/Sivasspor_logo.svg",
        "Alanyaspor": "https://upload.wikimedia.org/wikipedia/en/e/e2/Alanyaspor_logo.svg",
        "Antalyaspor": "https://upload.wikimedia.org/wikipedia/en/8/8f/Antalyaspor_logo.svg",
        "Konyaspor": "https://upload.wikimedia.org/wikipedia/en/5/5f/Konyaspor.svg",
        "Gaziantep FK": "https://upload.wikimedia.org/wikipedia/en/8/8d/Gaziantep_FK_logo.svg",
        "Kayserispor": "https://upload.wikimedia.org/wikipedia/en/e/e7/Kayserispor_logo.svg",
        "Çaykur Rizespor": "https://upload.wikimedia.org/wikipedia/en/a/a0/%C3%87aykur_Rizespor_logo.svg",
        "Hatayspor": "https://upload.wikimedia.org/wikipedia/en/5/5f/Hatayspor_logo.svg",
        "Eyüpspor": "https://upload.wikimedia.org/wikipedia/en/8/8a/Ey%C3%BCpspor_logo.svg",
        "Pendikspor": "https://upload.wikimedia.org/wikipedia/en/3/3f/Pendikspor_logo.svg",
        "Bodrum FK": "https://upload.wikimedia.org/wikipedia/en/4/4e/Bodrum_FK_logo.svg",

        // Serie A
        "Juventus": "https://upload.wikimedia.org/wikipedia/commons/a/a8/Juventus_FC_-_pictogram_black_%28Italy%2C_2017%29.svg",
        "Inter Milan": "https://upload.wikimedia.org/wikipedia/commons/0/05/FC_Internazionale_Milano_2021.svg",
        "AC Milan": "https://upload.wikimedia.org/wikipedia/commons/d/d0/Logo_of_AC_Milan.svg",
        "Napoli": "https://upload.wikimedia.org/wikipedia/commons/2/2d/SSC_Neapel.svg",
        "Roma": "https://upload.wikimedia.org/wikipedia/en/f/f7/AS_Roma_logo_%282017%29.svg",
        "Lazio": "https://upload.wikimedia.org/wikipedia/en/c/ce/S.S._Lazio_badge.svg",
        "Atalanta": "https://upload.wikimedia.org/wikipedia/en/6/66/Atalanta_BC_logo.svg",
        "Fiorentina": "https://upload.wikimedia.org/wikipedia/commons/d/d2/ACF_Fiorentina.svg",
        "Bologna": "https://upload.wikimedia.org/wikipedia/commons/c/c8/Bologna_FC_1909_logo.svg",
        "Torino": "https://upload.wikimedia.org/wikipedia/en/2/2e/Torino_FC_Logo.svg",
        "Udinese": "https://upload.wikimedia.org/wikipedia/en/c/ce/Udinese_Calcio_logo.svg",
        "Genoa": "https://upload.wikimedia.org/wikipedia/en/e/e0/Genoa_CFC_logo.svg",
        "Monza": "https://upload.wikimedia.org/wikipedia/commons/4/4a/AC_Monza_Logo.svg",
        "Lecce": "https://upload.wikimedia.org/wikipedia/en/8/87/US_Lecce_logo.svg",
        "Verona": "https://upload.wikimedia.org/wikipedia/en/6/61/Hellas_Verona_FC_logo.svg",
        "Cagliari": "https://upload.wikimedia.org/wikipedia/en/7/71/Cagliari_Calcio_1920.svg",
        "Parma": "https://upload.wikimedia.org/wikipedia/en/4/43/Parma_Calcio_1913_logo.svg",
        "Como": "https://upload.wikimedia.org/wikipedia/commons/2/22/Como_1907_logo.svg",
        "Venezia": "https://upload.wikimedia.org/wikipedia/en/8/8f/Venezia_FC_logo.svg",
        "Empoli": "https://upload.wikimedia.org/wikipedia/en/3/37/Empoli_FC_logo.svg",

        // Bundesliga
        "Bayern Munich": "https://upload.wikimedia.org/wikipedia/commons/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg",
        "Borussia Dortmund": "https://upload.wikimedia.org/wikipedia/commons/6/67/Borussia_Dortmund_logo.svg",
        "RB Leipzig": "https://upload.wikimedia.org/wikipedia/en/0/04/RB_Leipzig_2014_logo.svg",
        "Bayer Leverkusen": "https://upload.wikimedia.org/wikipedia/en/5/59/Bayer_04_Leverkusen_logo.svg",
        "VfB Stuttgart": "https://upload.wikimedia.org/wikipedia/commons/e/eb/VfB_Stuttgart_1893_Logo.svg",
        "Eintracht Frankfurt": "https://upload.wikimedia.org/wikipedia/commons/0/04/Eintracht_Frankfurt_Logo.svg",
        "Borussia Mönchengladbach": "https://upload.wikimedia.org/wikipedia/commons/8/81/Borussia_M%C3%B6nchengladbach_logo.svg",
        "VfL Wolfsburg": "https://upload.wikimedia.org/wikipedia/commons/f/f3/Logo-VfL-Wolfsburg.svg",
        "SC Freiburg": "https://upload.wikimedia.org/wikipedia/en/1/11/SC_Freiburg_logo.svg",
        "TSG Hoffenheim": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Logo_TSG_Hoffenheim.svg",
        "1. FC Union Berlin": "https://upload.wikimedia.org/wikipedia/commons/4/44/1._FC_Union_Berlin_Logo.svg",
        "SV Werder Bremen": "https://upload.wikimedia.org/wikipedia/commons/b/be/SV-Werder-Bremen-Logo.svg",
        "FC Augsburg": "https://upload.wikimedia.org/wikipedia/en/a/a4/FC_Augsburg_logo.svg",
        "1. FSV Mainz 05": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Logo_Mainz_05.svg",
        "VfL Bochum": "https://upload.wikimedia.org/wikipedia/commons/7/7b/VfL_Bochum_logo.svg",
        "1. FC Heidenheim": "https://upload.wikimedia.org/wikipedia/commons/e/e2/1._FC_Heidenheim_1846_logo.svg",
        "FC St. Pauli": "https://upload.wikimedia.org/wikipedia/commons/e/e1/FC_St._Pauli_logo.svg",
        "Holstein Kiel": "https://upload.wikimedia.org/wikipedia/commons/c/cd/Holstein_Kiel_Logo.svg",

        // Ligue 1
        "Paris Saint-Germain": "https://upload.wikimedia.org/wikipedia/en/a/a7/Paris_Saint-Germain_F.C..svg",
        "Marseille": "https://upload.wikimedia.org/wikipedia/commons/d/d8/Olympique_Marseille_logo.svg",
        "Monaco": "https://upload.wikimedia.org/wikipedia/commons/4/4a/Logo_AS_Monaco.svg",
        "Lyon": "https://upload.wikimedia.org/wikipedia/en/e/e2/Olympique_Lyonnais_logo.svg",
        "Lille": "https://upload.wikimedia.org/wikipedia/en/b/b9/Lille_OSC_%282018%29_logo.svg",
        "Lens": "https://upload.wikimedia.org/wikipedia/en/5/5a/RC_Lens_logo.svg",
        "Nice": "https://upload.wikimedia.org/wikipedia/en/a/a4/OGC_Nice_logo.svg",
        "Rennes": "https://upload.wikimedia.org/wikipedia/en/2/25/Stade_Rennais_F.C._logo.svg",
        "Strasbourg": "https://upload.wikimedia.org/wikipedia/commons/7/72/Racing_Club_de_Strasbourg_Alsace_logo.svg",
        "Brest": "https://upload.wikimedia.org/wikipedia/en/b/b9/Stade_Brestois_29_logo.svg",
        "Nantes": "https://upload.wikimedia.org/wikipedia/commons/6/66/FC_Nantes_logo.svg",
        "Toulouse": "https://upload.wikimedia.org/wikipedia/commons/5/55/Toulouse_FC_2018_logo.svg",
        "Reims": "https://upload.wikimedia.org/wikipedia/en/7/72/Stade_Reims_logo.svg",
        "Montpellier": "https://upload.wikimedia.org/wikipedia/commons/3/35/Montpellier_H%C3%A9rault_Sport_Club_%28logo%2C_2000%29.svg",
        "Auxerre": "https://upload.wikimedia.org/wikipedia/en/3/30/AJ_Auxerre_Logo.svg",
        "Angers": "https://upload.wikimedia.org/wikipedia/en/3/30/Angers_SCO_logo.svg",
        "Saint-Étienne": "https://upload.wikimedia.org/wikipedia/en/2/2a/AS_Saint-%C3%89tienne_logo.svg",
        "Le Havre": "https://upload.wikimedia.org/wikipedia/en/7/71/Le_Havre_AC_logo.svg",
    };

    return logoMap[clubName] || null;
}

export function getClubInitials(clubName: string): string {
    return clubName
        .split(' ')
        .map(word => word[0])
        .join('')
        .substring(0, 2)
        .toUpperCase();
}
