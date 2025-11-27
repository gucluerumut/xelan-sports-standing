// Club logo helper - provides multiple logo URL candidates for all clubs
// Priority: Clearbit -> Wikipedia -> TheSportsDB -> Initials

export function getClubLogoUrls(clubName: string): string[] {
    const urls: string[] = [];

    // Helper to clean name for URL generation
    const cleanName = clubName.toLowerCase().replace(/ /g, '').replace(/[^a-z0-9]/g, '');
    const slugName = clubName.toLowerCase().replace(/ /g, '-').replace(/[^a-z0-9-]/g, '');

    // 1. Clearbit (Official Domain Guessing)
    const domainMap: Record<string, string> = {
        // Premier League
        "Manchester City": "mancity.com",
        "Arsenal": "arsenal.com",
        "Liverpool": "liverpoolfc.com",
        "Aston Villa": "avfc.co.uk",
        "Tottenham Hotspur": "tottenhamhotspur.com",
        "Chelsea": "chelseafc.com",
        "Newcastle United": "nufc.co.uk",
        "Manchester United": "manutd.com",
        "West Ham United": "whufc.com",
        "Brighton & Hove Albion": "brightonandhovealbion.com",
        "Bournemouth": "afcb.co.uk",
        "Fulham": "fulhamfc.com",
        "Wolverhampton Wanderers": "wolves.co.uk",
        "Everton": "evertonfc.com",
        "Brentford": "brentfordfc.com",
        "Nottingham Forest": "nottinghamforest.co.uk",
        "Crystal Palace": "cpfc.co.uk",
        "Leicester City": "lcfc.com",
        "Ipswich Town": "itfc.co.uk",
        "Southampton": "southamptonfc.com",

        // La Liga
        "Real Madrid": "realmadrid.com",
        "Barcelona": "fcbarcelona.com",
        "Atlético Madrid": "atleticodemadrid.com",
        "Athletic Bilbao": "athletic-club.eus",
        "Real Sociedad": "realsociedad.eus",
        "Real Betis": "realbetisbalompie.es",
        "Villarreal": "villarrealcf.es",
        "Valencia": "valenciacf.com",
        "Sevilla": "sevillafc.es",
        "Girona": "gironafc.cat",

        // Süper Lig
        "Galatasaray": "galatasaray.org",
        "Fenerbahçe": "fenerbahce.org",
        "Beşiktaş": "bjk.com.tr",
        "Trabzonspor": "trabzonspor.org.tr",
        "İstanbul Başakşehir": "ibfk.org.tr",
        "Samsunspor": "samsunspor.org.tr",

        // Serie A
        "Juventus": "juventus.com",
        "Inter Milan": "inter.it",
        "AC Milan": "acmilan.com",
        "Napoli": "sscnapoli.it",
        "Roma": "asroma.com",
        "Lazio": "sslazio.it",

        // Bundesliga
        "Bayern Munich": "fcbayern.com",
        "Borussia Dortmund": "bvb.de",
        "RB Leipzig": "rbleipzig.com",
        "Bayer Leverkusen": "bayer04.de",

        // Ligue 1
        "Paris Saint-Germain": "psg.fr",
        "Marseille": "om.fr",
        "Monaco": "asmonaco.com",
        "Lyon": "ol.fr"
    };

    if (domainMap[clubName]) {
        urls.push(`https://logo.clearbit.com/${domainMap[clubName]}`);
    }

    // 2. Wikipedia Commons (Known URLs)
    const wikiMap: Record<string, string> = {
        "Manchester City": "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg",
        "Arsenal": "https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg",
        "Liverpool": "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg",
        "Galatasaray": "https://upload.wikimedia.org/wikipedia/commons/f/f6/Galatasaray_Sports_Club_Logo.png",
        "Fenerbahçe": "https://upload.wikimedia.org/wikipedia/en/8/86/Fenerbahce_SK_Logo.svg",
        "Beşiktaş": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Besiktas_JK_logo.svg",
        "Trabzonspor": "https://upload.wikimedia.org/wikipedia/commons/3/31/Trabzonspor_logo.svg",
        "Real Madrid": "https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg",
        "Barcelona": "https://upload.wikimedia.org/wikipedia/en/4/47/FC_Barcelona_%28crest%29.svg",
        "Bayern Munich": "https://upload.wikimedia.org/wikipedia/commons/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg",
        "Paris Saint-Germain": "https://upload.wikimedia.org/wikipedia/en/a/a7/Paris_Saint-Germain_F.C..svg",
        "Juventus": "https://upload.wikimedia.org/wikipedia/commons/a/a8/Juventus_FC_-_pictogram_black_%28Italy%2C_2017%29.svg"
    };

    if (wikiMap[clubName]) {
        urls.push(wikiMap[clubName]);
    }

    // 3. Generic Fallbacks (TheSportsDB, FotMob patterns)
    // These are guesses but might work for missing ones
    urls.push(`https://media.api-sports.io/football/teams/${cleanName}.png`); // Hypothetical
    urls.push(`https://crests.football-data.org/${cleanName}.svg`); // Hypothetical

    return urls;
}

export function getClubInitials(clubName: string): string {
    return clubName
        .split(' ')
        .map(word => word[0])
        .join('')
        .substring(0, 2)
        .toUpperCase();
}
