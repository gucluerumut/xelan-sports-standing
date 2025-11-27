// Club logo helper - provides logo URLs for all clubs
// Using Wikipedia Commons as primary source (reliable and permanent URLs)

export function getClubLogoUrl(clubName: string): string | null {
    const logoMap: Record<string, string> = {
        // Premier League (20 clubs) - All clubs
        "Manchester City": "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Manchester_City_FC_badge.svg/100px-Manchester_City_FC_badge.svg.png",
        "Arsenal": "https://upload.wikimedia.org/wikipedia/en/thumb/5/53/Arsenal_FC.svg/100px-Arsenal_FC.svg.png",
        "Liverpool": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0c/Liverpool_FC.svg/100px-Liverpool_FC.svg.png",
        "Aston Villa": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f9/Aston_Villa_FC_crest_%282016%29.svg/100px-Aston_Villa_FC_crest_%282016%29.svg.png",
        "Tottenham Hotspur": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b4/Tottenham_Hotspur.svg/100px-Tottenham_Hotspur.svg.png",
        "Chelsea": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Chelsea_FC.svg/100px-Chelsea_FC.svg.png",
        "Newcastle United": "https://upload.wikimedia.org/wikipedia/en/thumb/5/56/Newcastle_United_Logo.svg/100px-Newcastle_United_Logo.svg.png",
        "Manchester United": "https://upload.wikimedia.org/wikipedia/en/thumb/7/7a/Manchester_United_FC_crest.svg/100px-Manchester_United_FC_crest.svg.png",
        "West Ham United": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c2/West_Ham_United_FC_logo.svg/100px-West_Ham_United_FC_logo.svg.png",
        "Brighton & Hove Albion": "https://upload.wikimedia.org/wikipedia/en/thumb/f/fd/Brighton_%26_Hove_Albion_logo.svg/100px-Brighton_%26_Hove_Albion_logo.svg.png",
        "Bournemouth": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e5/AFC_Bournemouth_%282013%29.svg/100px-AFC_Bournemouth_%282013%29.svg.png",
        "Fulham": "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Fulham_FC_%28shield%29.svg/100px-Fulham_FC_%28shield%29.svg.png",
        "Wolverhampton Wanderers": "https://upload.wikimedia.org/wikipedia/en/thumb/f/fc/Wolverhampton_Wanderers.svg/100px-Wolverhampton_Wanderers.svg.png",
        "Everton": "https://upload.wikimedia.org/wikipedia/en/thumb/7/7c/Everton_FC_logo.svg/100px-Everton_FC_logo.svg.png",
        "Brentford": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2a/Brentford_FC_crest.svg/100px-Brentford_FC_crest.svg.png",
        "Nottingham Forest": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e5/Nottingham_Forest_F.C._logo.svg/100px-Nottingham_Forest_F.C._logo.svg.png",
        "Crystal Palace": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/Crystal_Palace_FC_logo_%282022%29.svg/100px-Crystal_Palace_FC_logo_%282022%29.svg.png",
        "Leicester City": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2d/Leicester_City_crest.svg/100px-Leicester_City_crest.svg.png",
        "Ipswich Town": "https://upload.wikimedia.org/wikipedia/en/thumb/4/43/Ipswich_Town.svg/100px-Ipswich_Town.svg.png",
        "Southampton": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c9/FC_Southampton.svg/100px-FC_Southampton.svg.png",

        // La Liga (20 clubs) - All clubs
        "Real Madrid": "https://upload.wikimedia.org/wikipedia/en/thumb/5/56/Real_Madrid_CF.svg/100px-Real_Madrid_CF.svg.png",
        "Barcelona": "https://upload.wikimedia.org/wikipedia/en/thumb/4/47/FC_Barcelona_%28crest%29.svg/100px-FC_Barcelona_%28crest%29.svg.png",
        "Atlético Madrid": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f4/Atletico_Madrid_2017_logo.svg/100px-Atletico_Madrid_2017_logo.svg.png",
        "Athletic Bilbao": "https://upload.wikimedia.org/wikipedia/en/thumb/9/98/Club_Athletic_Bilbao_logo.svg/100px-Club_Athletic_Bilbao_logo.svg.png",
        "Real Sociedad": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f1/Real_Sociedad_logo.svg/100px-Real_Sociedad_logo.svg.png",
        "Real Betis": "https://upload.wikimedia.org/wikipedia/en/thumb/1/13/Real_betis_logo.svg/100px-Real_betis_logo.svg.png",
        "Villarreal": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/Villarreal_CF_logo-en.svg/100px-Villarreal_CF_logo-en.svg.png",
        "Valencia": "https://upload.wikimedia.org/wikipedia/en/thumb/c/ce/Valenciacf.svg/100px-Valenciacf.svg.png",
        "Sevilla": "https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/Sevilla_FC_logo.svg/100px-Sevilla_FC_logo.svg.png",
        "Girona": "https://upload.wikimedia.org/wikipedia/en/thumb/7/79/Girona_FC_logo.svg/100px-Girona_FC_logo.svg.png",
        "Osasuna": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c2/CA_Osasuna_logo.svg/100px-CA_Osasuna_logo.svg.png",
        "Getafe": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2e/Getafe_logo.svg/100px-Getafe_logo.svg.png",
        "Rayo Vallecano": "https://upload.wikimedia.org/wikipedia/en/thumb/6/6b/Rayo_Vallecano_logo.svg/100px-Rayo_Vallecano_logo.svg.png",
        "Celta Vigo": "https://upload.wikimedia.org/wikipedia/en/thumb/1/12/RC_Celta_de_Vigo_logo.svg/100px-RC_Celta_de_Vigo_logo.svg.png",
        "Mallorca": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e0/RCD_Mallorca.svg/100px-RCD_Mallorca.svg.png",
        "Las Palmas": "https://upload.wikimedia.org/wikipedia/en/thumb/2/20/UD_Las_Palmas_logo.svg/100px-UD_Las_Palmas_logo.svg.png",
        "Alavés": "https://upload.wikimedia.org/wikipedia/en/thumb/7/79/Deportivo_Alav%C3%A9s_logo.svg/100px-Deportivo_Alav%C3%A9s_logo.svg.png",
        "Espanyol": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a7/RCD_Espanyol_logo.svg/100px-RCD_Espanyol_logo.svg.png",
        "Leganés": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c6/CD_Legan%C3%A9s_logo.svg/100px-CD_Legan%C3%A9s_logo.svg.png",
        "Valladolid": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8c/Real_Valladolid_Logo.svg/100px-Real_Valladolid_Logo.svg.png",

        // Süper Lig (20 clubs) - All clubs
        "Galatasaray": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Galatasaray_Sports_Club_Logo.png/100px-Galatasaray_Sports_Club_Logo.png",
        "Fenerbahçe": "https://upload.wikimedia.org/wikipedia/en/thumb/8/86/Fenerbahce_SK_Logo.svg/100px-Fenerbahce_SK_Logo.svg.png",
        "Beşiktaş": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Besiktas_JK_logo.svg/100px-Besiktas_JK_logo.svg.png",
        "Trabzonspor": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Trabzonspor_logo.svg/100px-Trabzonspor_logo.svg.png",
        "İstanbul Başakşehir": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0a/Istanbul_Basaksehir_FK.svg/100px-Istanbul_Basaksehir_FK.svg.png",
        "Samsunspor": "https://upload.wikimedia.org/wikipedia/en/thumb/9/9d/Samsunspor_logo.svg/100px-Samsunspor_logo.svg.png",
        "Göztepe": "https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/G%C3%B6ztepe_SK_logo.svg/100px-G%C3%B6ztepe_SK_logo.svg.png",
        "Kasımpaşa": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e8/Kasimpasa_SK.svg/100px-Kasimpasa_SK.svg.png",
        "Sivasspor": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0d/Sivasspor_logo.svg/100px-Sivasspor_logo.svg.png",
        "Alanyaspor": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e2/Alanyaspor_logo.svg/100px-Alanyaspor_logo.svg.png",
        "Antalyaspor": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8f/Antalyaspor_logo.svg/100px-Antalyaspor_logo.svg.png",
        "Konyaspor": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5f/Konyaspor.svg/100px-Konyaspor.svg.png",
        "Gaziantep FK": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8d/Gaziantep_FK_logo.svg/100px-Gaziantep_FK_logo.svg.png",
        "Kayserispor": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e7/Kayserispor_logo.svg/100px-Kayserispor_logo.svg.png",
        "Çaykur Rizespor": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a0/%C3%87aykur_Rizespor_logo.svg/100px-%C3%87aykur_Rizespor_logo.svg.png",
        "Hatayspor": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5f/Hatayspor_logo.svg/100px-Hatayspor_logo.svg.png",
        "Eyüpspor": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8a/Ey%C3%BCpspor_logo.svg/100px-Ey%C3%BCpspor_logo.svg.png",
        "Pendikspor": "https://upload.wikimedia.org/wikipedia/en/thumb/3/3f/Pendikspor_logo.svg/100px-Pendikspor_logo.svg.png",
        "Bodrum FK": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4e/Bodrum_FK_logo.svg/100px-Bodrum_FK_logo.svg.png",

        // Serie A (20 clubs) - All clubs
        "Juventus": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Juventus_FC_-_pictogram_black_%28Italy%2C_2017%29.svg/100px-Juventus_FC_-_pictogram_black_%28Italy%2C_2017%29.svg.png",
        "Inter Milan": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/FC_Internazionale_Milano_2021.svg/100px-FC_Internazionale_Milano_2021.svg.png",
        "AC Milan": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Logo_of_AC_Milan.svg/100px-Logo_of_AC_Milan.svg.png",
        "Napoli": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/SSC_Neapel.svg/100px-SSC_Neapel.svg.png",
        "Roma": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f7/AS_Roma_logo_%282017%29.svg/100px-AS_Roma_logo_%282017%29.svg.png",
        "Lazio": "https://upload.wikimedia.org/wikipedia/en/thumb/c/ce/S.S._Lazio_badge.svg/100px-S.S._Lazio_badge.svg.png",
        "Atalanta": "https://upload.wikimedia.org/wikipedia/en/thumb/6/66/Atalanta_BC_logo.svg/100px-Atalanta_BC_logo.svg.png",
        "Fiorentina": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/ACF_Fiorentina.svg/100px-ACF_Fiorentina.svg.png",
        "Bologna": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Bologna_FC_1909_logo.svg/100px-Bologna_FC_1909_logo.svg.png",
        "Torino": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2e/Torino_FC_Logo.svg/100px-Torino_FC_Logo.svg.png",
        "Udinese": "https://upload.wikimedia.org/wikipedia/en/thumb/c/ce/Udinese_Calcio_logo.svg/100px-Udinese_Calcio_logo.svg.png",
        "Genoa": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e0/Genoa_CFC_logo.svg/100px-Genoa_CFC_logo.svg.png",
        "Monza": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/AC_Monza_Logo.svg/100px-AC_Monza_Logo.svg.png",
        "Lecce": "https://upload.wikimedia.org/wikipedia/en/thumb/8/87/US_Lecce_logo.svg/100px-US_Lecce_logo.svg.png",
        "Verona": "https://upload.wikimedia.org/wikipedia/en/thumb/6/61/Hellas_Verona_FC_logo.svg/100px-Hellas_Verona_FC_logo.svg.png",
        "Cagliari": "https://upload.wikimedia.org/wikipedia/en/thumb/7/71/Cagliari_Calcio_1920.svg/100px-Cagliari_Calcio_1920.svg.png",
        "Parma": "https://upload.wikimedia.org/wikipedia/en/thumb/4/43/Parma_Calcio_1913_logo.svg/100px-Parma_Calcio_1913_logo.svg.png",
        "Como": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Como_1907_logo.svg/100px-Como_1907_logo.svg.png",
        "Venezia": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8f/Venezia_FC_logo.svg/100px-Venezia_FC_logo.svg.png",
        "Empoli": "https://upload.wikimedia.org/wikipedia/en/thumb/3/37/Empoli_FC_logo.svg/100px-Empoli_FC_logo.svg.png",

        // Bundesliga (18 clubs) - All clubs
        "Bayern Munich": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg/100px-FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg.png",
        "Borussia Dortmund": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Borussia_Dortmund_logo.svg/100px-Borussia_Dortmund_logo.svg.png",
        "RB Leipzig": "https://upload.wikimedia.org/wikipedia/en/thumb/0/04/RB_Leipzig_2014_logo.svg/100px-RB_Leipzig_2014_logo.svg.png",
        "Bayer Leverkusen": "https://upload.wikimedia.org/wikipedia/en/thumb/5/59/Bayer_04_Leverkusen_logo.svg/100px-Bayer_04_Leverkusen_logo.svg.png",
        "VfB Stuttgart": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/VfB_Stuttgart_1893_Logo.svg/100px-VfB_Stuttgart_1893_Logo.svg.png",
        "Eintracht Frankfurt": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Eintracht_Frankfurt_Logo.svg/100px-Eintracht_Frankfurt_Logo.svg.png",
        "Borussia Mönchengladbach": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Borussia_M%C3%B6nchengladbach_logo.svg/100px-Borussia_M%C3%B6nchengladbach_logo.svg.png",
        "VfL Wolfsburg": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Logo-VfL-Wolfsburg.svg/100px-Logo-VfL-Wolfsburg.svg.png",
        "SC Freiburg": "https://upload.wikimedia.org/wikipedia/en/thumb/1/11/SC_Freiburg_logo.svg/100px-SC_Freiburg_logo.svg.png",
        "TSG Hoffenheim": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Logo_TSG_Hoffenheim.svg/100px-Logo_TSG_Hoffenheim.svg.png",
        "1. FC Union Berlin": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/1._FC_Union_Berlin_Logo.svg/100px-1._FC_Union_Berlin_Logo.svg.png",
        "SV Werder Bremen": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/SV-Werder-Bremen-Logo.svg/100px-SV-Werder-Bremen-Logo.svg.png",
        "FC Augsburg": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/FC_Augsburg_logo.svg/100px-FC_Augsburg_logo.svg.png",
        "1. FSV Mainz 05": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Logo_Mainz_05.svg/100px-Logo_Mainz_05.svg.png",
        "VfL Bochum": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/VfL_Bochum_logo.svg/100px-VfL_Bochum_logo.svg.png",
        "1. FC Heidenheim": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/1._FC_Heidenheim_1846_logo.svg/100px-1._FC_Heidenheim_1846_logo.svg.png",
        "FC St. Pauli": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/FC_St._Pauli_logo.svg/100px-FC_St._Pauli_logo.svg.png",
        "Holstein Kiel": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Holstein_Kiel_Logo.svg/100px-Holstein_Kiel_Logo.svg.png",

        // Ligue 1 (18 clubs) - All clubs
        "Paris Saint-Germain": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a7/Paris_Saint-Germain_F.C..svg/100px-Paris_Saint-Germain_F.C..svg.png",
        "Marseille": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Olympique_Marseille_logo.svg/100px-Olympique_Marseille_logo.svg.png",
        "Monaco": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Logo_AS_Monaco.svg/100px-Logo_AS_Monaco.svg.png",
        "Lyon": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e2/Olympique_Lyonnais_logo.svg/100px-Olympique_Lyonnais_logo.svg.png",
        "Lille": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/Lille_OSC_%282018%29_logo.svg/100px-Lille_OSC_%282018%29_logo.svg.png",
        "Lens": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5a/RC_Lens_logo.svg/100px-RC_Lens_logo.svg.png",
        "Nice": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/OGC_Nice_logo.svg/100px-OGC_Nice_logo.svg.png",
        "Rennes": "https://upload.wikimedia.org/wikipedia/en/thumb/2/25/Stade_Rennais_F.C._logo.svg/100px-Stade_Rennais_F.C._logo.svg.png",
        "Strasbourg": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Racing_Club_de_Strasbourg_Alsace_logo.svg/100px-Racing_Club_de_Strasbourg_Alsace_logo.svg.png",
        "Brest": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/Stade_Brestois_29_logo.svg/100px-Stade_Brestois_29_logo.svg.png",
        "Nantes": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/FC_Nantes_logo.svg/100px-FC_Nantes_logo.svg.png",
        "Toulouse": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Toulouse_FC_2018_logo.svg/100px-Toulouse_FC_2018_logo.svg.png",
        "Reims": "https://upload.wikimedia.org/wikipedia/en/thumb/7/72/Stade_Reims_logo.svg/100px-Stade_Reims_logo.svg.png",
        "Montpellier": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Montpellier_H%C3%A9rault_Sport_Club_%28logo%2C_2000%29.svg/100px-Montpellier_H%C3%A9rault_Sport_Club_%28logo%2C_2000%29.svg.png",
        "Auxerre": "https://upload.wikimedia.org/wikipedia/en/thumb/3/30/AJ_Auxerre_Logo.svg/100px-AJ_Auxerre_Logo.svg.png",
        "Angers": "https://upload.wikimedia.org/wikipedia/en/thumb/3/30/Angers_SCO_logo.svg/100px-Angers_SCO_logo.svg.png",
        "Saint-Étienne": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2a/AS_Saint-%C3%89tienne_logo.svg/100px-AS_Saint-%C3%89tienne_logo.svg.png",
        "Le Havre": "https://upload.wikimedia.org/wikipedia/en/thumb/7/71/Le_Havre_AC_logo.svg/100px-Le_Havre_AC_logo.svg.png",
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
