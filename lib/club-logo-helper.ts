// Club logo helper - provides logo URLs for all clubs
// Using a combination of official sources and fallbacks

export function getClubLogoUrl(clubName: string): string | null {
    const logoMap: Record<string, string> = {
        // Premier League
        "Manchester City": "https://resources.premierleague.com/premierleague/badges/100/t43.png",
        "Arsenal": "https://resources.premierleague.com/premierleague/badges/100/t3.png",
        "Liverpool": "https://resources.premierleague.com/premierleague/badges/100/t14.png",
        "Aston Villa": "https://resources.premierleague.com/premierleague/badges/100/t7.png",
        "Tottenham Hotspur": "https://resources.premierleague.com/premierleague/badges/100/t6.png",
        "Chelsea": "https://resources.premierleague.com/premierleague/badges/100/t8.png",
        "Newcastle United": "https://resources.premierleague.com/premierleague/badges/100/t4.png",
        "Manchester United": "https://resources.premierleague.com/premierleague/badges/100/t1.png",
        "West Ham United": "https://resources.premierleague.com/premierleague/badges/100/t21.png",
        "Brighton & Hove Albion": "https://resources.premierleague.com/premierleague/badges/100/t36.png",
        "Bournemouth": "https://resources.premierleague.com/premierleague/badges/100/t91.png",
        "Fulham": "https://resources.premierleague.com/premierleague/badges/100/t54.png",
        "Wolverhampton Wanderers": "https://resources.premierleague.com/premierleague/badges/100/t39.png",
        "Everton": "https://resources.premierleague.com/premierleague/badges/100/t11.png",
        "Brentford": "https://resources.premierleague.com/premierleague/badges/100/t94.png",
        "Nottingham Forest": "https://resources.premierleague.com/premierleague/badges/100/t17.png",
        "Luton Town": "https://resources.premierleague.com/premierleague/badges/100/t102.png",
        "Burnley": "https://resources.premierleague.com/premierleague/badges/100/t90.png",
        "Crystal Palace": "https://resources.premierleague.com/premierleague/badges/100/t31.png",
        "Sheffield United": "https://resources.premierleague.com/premierleague/badges/100/t49.png",

        // La Liga - using Wikipedia Commons (reliable source)
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

        // Süper Lig
        "Galatasaray": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Galatasaray_Sports_Club_Logo.png/100px-Galatasaray_Sports_Club_Logo.png",
        "Fenerbahçe": "https://upload.wikimedia.org/wikipedia/en/thumb/8/86/Fenerbahce_SK_Logo.svg/100px-Fenerbahce_SK_Logo.svg.png",
        "Beşiktaş": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Besiktas_JK_logo.svg/100px-Besiktas_JK_logo.svg.png",
        "Trabzonspor": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Trabzonspor_logo.svg/100px-Trabzonspor_logo.svg.png",

        // Serie A
        "Juventus": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Juventus_FC_-_pictogram_black_%28Italy%2C_2017%29.svg/100px-Juventus_FC_-_pictogram_black_%28Italy%2C_2017%29.svg.png",
        "Inter Milan": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/FC_Internazionale_Milano_2021.svg/100px-FC_Internazionale_Milano_2021.svg.png",
        "AC Milan": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Logo_of_AC_Milan.svg/100px-Logo_of_AC_Milan.svg.png",
        "Napoli": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/SSC_Neapel.svg/100px-SSC_Neapel.svg.png",
        "Roma": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f7/AS_Roma_logo_%282017%29.svg/100px-AS_Roma_logo_%282017%29.svg.png",
        "Lazio": "https://upload.wikimedia.org/wikipedia/en/thumb/c/ce/S.S._Lazio_badge.svg/100px-S.S._Lazio_badge.svg.png",

        // Bundesliga
        "Bayern Munich": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg/100px-FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg.png",
        "Borussia Dortmund": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Borussia_Dortmund_logo.svg/100px-Borussia_Dortmund_logo.svg.png",
        "RB Leipzig": "https://upload.wikimedia.org/wikipedia/en/thumb/0/04/RB_Leipzig_2014_logo.svg/100px-RB_Leipzig_2014_logo.svg.png",
        "Bayer Leverkusen": "https://upload.wikimedia.org/wikipedia/en/thumb/5/59/Bayer_04_Leverkusen_logo.svg/100px-Bayer_04_Leverkusen_logo.svg.png",

        // Ligue 1
        "Paris Saint-Germain": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a7/Paris_Saint-Germain_F.C..svg/100px-Paris_Saint-Germain_F.C..svg.png",
        "Marseille": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Olympique_Marseille_logo.svg/100px-Olympique_Marseille_logo.svg.png",
        "Monaco": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Logo_AS_Monaco.svg/100px-Logo_AS_Monaco.svg.png",
        "Lyon": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e2/Olympique_Lyonnais_logo.svg/100px-Olympique_Lyonnais_logo.svg.png",
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
