// Club logo helper - provides logo URLs with multiple fallbacks
// Priority: Clearbit (fast, reliable) -> Wikipedia (backup) -> Initials

export function getClubLogoUrl(clubName: string): string | null {
    // Primary source: Clearbit Logo API (works for most clubs)
    const clearbitLogos: Record<string, string> = {
        // Premier League
        "Manchester City": "https://logo.clearbit.com/mancity.com",
        "Arsenal": "https://logo.clearbit.com/arsenal.com",
        "Liverpool": "https://logo.clearbit.com/liverpoolfc.com",
        "Aston Villa": "https://logo.clearbit.com/avfc.co.uk",
        "Tottenham Hotspur": "https://logo.clearbit.com/tottenhamhotspur.com",
        "Chelsea": "https://logo.clearbit.com/chelseafc.com",
        "Newcastle United": "https://logo.clearbit.com/nufc.co.uk",
        "Manchester United": "https://logo.clearbit.com/manutd.com",
        "West Ham United": "https://logo.clearbit.com/whufc.com",
        "Brighton & Hove Albion": "https://logo.clearbit.com/brightonandhovealbion.com",
        "Bournemouth": "https://logo.clearbit.com/afcb.co.uk",
        "Fulham": "https://logo.clearbit.com/fulhamfc.com",
        "Wolverhampton Wanderers": "https://logo.clearbit.com/wolves.co.uk",
        "Everton": "https://logo.clearbit.com/evertonfc.com",
        "Brentford": "https://logo.clearbit.com/brentfordfc.com",
        "Nottingham Forest": "https://logo.clearbit.com/nottinghamforest.co.uk",
        "Crystal Palace": "https://logo.clearbit.com/cpfc.co.uk",
        "Leicester City": "https://logo.clearbit.com/lcfc.com",
        "Ipswich Town": "https://logo.clearbit.com/itfc.co.uk",
        "Southampton": "https://logo.clearbit.com/southamptonfc.com",

        // La Liga
        "Real Madrid": "https://logo.clearbit.com/realmadrid.com",
        "Barcelona": "https://logo.clearbit.com/fcbarcelona.com",
        "Atlético Madrid": "https://logo.clearbit.com/atleticodemadrid.com",
        "Athletic Bilbao": "https://logo.clearbit.com/athletic-club.eus",
        "Real Sociedad": "https://logo.clearbit.com/realsociedad.eus",
        "Real Betis": "https://logo.clearbit.com/realbetisbalompie.es",
        "Villarreal": "https://logo.clearbit.com/villarrealcf.es",
        "Valencia": "https://logo.clearbit.com/valenciacf.com",
        "Sevilla": "https://logo.clearbit.com/sevillafc.es",
        "Girona": "https://logo.clearbit.com/gironafc.cat",
        "Osasuna": "https://logo.clearbit.com/osasuna.es",
        "Getafe": "https://logo.clearbit.com/getafecf.com",
        "Rayo Vallecano": "https://logo.clearbit.com/rayovallecano.es",
        "Celta Vigo": "https://logo.clearbit.com/celtavigo.net",
        "Mallorca": "https://logo.clearbit.com/rcdmallorca.es",
        "Las Palmas": "https://logo.clearbit.com/udlaspalmas.es",
        "Alavés": "https://logo.clearbit.com/deportivoalaves.com",
        "Espanyol": "https://logo.clearbit.com/rcdespanyol.com",
        "Leganés": "https://logo.clearbit.com/cdleganes.com",
        "Valladolid": "https://logo.clearbit.com/realvalladolid.es",

        // Süper Lig
        "Galatasaray": "https://logo.clearbit.com/galatasaray.org",
        "Fenerbahçe": "https://logo.clearbit.com/fenerbahce.org",
        "Beşiktaş": "https://logo.clearbit.com/bjk.com.tr",
        "Trabzonspor": "https://logo.clearbit.com/trabzonspor.org.tr",
        "İstanbul Başakşehir": "https://logo.clearbit.com/ibfk.org.tr",
        "Samsunspor": "https://logo.clearbit.com/samsunspor.org.tr",
        "Göztepe": "https://logo.clearbit.com/goztepe.org.tr",
        "Kasımpaşa": "https://logo.clearbit.com/kasimpasa.com.tr",
        "Sivasspor": "https://logo.clearbit.com/sivasspor.org.tr",
        "Alanyaspor": "https://logo.clearbit.com/alanyaspor.org.tr",
        "Antalyaspor": "https://logo.clearbit.com/antalyaspor.com.tr",
        "Konyaspor": "https://logo.clearbit.com/konyaspor.org.tr",
        "Gaziantep FK": "https://logo.clearbit.com/gaziantepfk.org.tr",
        "Kayserispor": "https://logo.clearbit.com/kayserispor.com.tr",
        "Çaykur Rizespor": "https://logo.clearbit.com/rizespor.org.tr",
        "Hatayspor": "https://logo.clearbit.com/hatayspor.com.tr",
        "Eyüpspor": "https://logo.clearbit.com/eyupspor.org.tr",
        "Pendikspor": "https://logo.clearbit.com/pendikspor.com.tr",
        "Bodrum FK": "https://logo.clearbit.com/bodrumfk.com.tr",

        // Serie A
        "Juventus": "https://logo.clearbit.com/juventus.com",
        "Inter Milan": "https://logo.clearbit.com/inter.it",
        "AC Milan": "https://logo.clearbit.com/acmilan.com",
        "Napoli": "https://logo.clearbit.com/sscnapoli.it",
        "Roma": "https://logo.clearbit.com/asroma.com",
        "Lazio": "https://logo.clearbit.com/sslazio.it",
        "Atalanta": "https://logo.clearbit.com/atalanta.it",
        "Fiorentina": "https://logo.clearbit.com/acffiorentina.com",
        "Bologna": "https://logo.clearbit.com/bolognafc.it",
        "Torino": "https://logo.clearbit.com/torinofc.it",
        "Udinese": "https://logo.clearbit.com/udinese.it",
        "Genoa": "https://logo.clearbit.com/genoacfc.it",
        "Monza": "https://logo.clearbit.com/acmonza.com",
        "Lecce": "https://logo.clearbit.com/uslecce.it",
        "Verona": "https://logo.clearbit.com/hellasverona.it",
        "Cagliari": "https://logo.clearbit.com/cagliaricalcio.com",
        "Parma": "https://logo.clearbit.com/parmacalcio1913.com",
        "Como": "https://logo.clearbit.com/comocalcio1907.it",
        "Venezia": "https://logo.clearbit.com/veneziafc.it",
        "Empoli": "https://logo.clearbit.com/empolifc.com",

        // Bundesliga
        "Bayern Munich": "https://logo.clearbit.com/fcbayern.com",
        "Borussia Dortmund": "https://logo.clearbit.com/bvb.de",
        "RB Leipzig": "https://logo.clearbit.com/rbleipzig.com",
        "Bayer Leverkusen": "https://logo.clearbit.com/bayer04.de",
        "VfB Stuttgart": "https://logo.clearbit.com/vfb.de",
        "Eintracht Frankfurt": "https://logo.clearbit.com/eintracht.de",
        "Borussia Mönchengladbach": "https://logo.clearbit.com/borussia.de",
        "VfL Wolfsburg": "https://logo.clearbit.com/vfl-wolfsburg.de",
        "SC Freiburg": "https://logo.clearbit.com/scfreiburg.com",
        "TSG Hoffenheim": "https://logo.clearbit.com/achtzehn99.de",
        "1. FC Union Berlin": "https://logo.clearbit.com/fc-union-berlin.de",
        "SV Werder Bremen": "https://logo.clearbit.com/werder.de",
        "FC Augsburg": "https://logo.clearbit.com/fcaugsburg.de",
        "1. FSV Mainz 05": "https://logo.clearbit.com/mainz05.de",
        "VfL Bochum": "https://logo.clearbit.com/vfl-bochum.de",
        "1. FC Heidenheim": "https://logo.clearbit.com/fc-heidenheim.de",
        "FC St. Pauli": "https://logo.clearbit.com/fcstpauli.com",
        "Holstein Kiel": "https://logo.clearbit.com/holstein-kiel.de",

        // Ligue 1
        "Paris Saint-Germain": "https://logo.clearbit.com/psg.fr",
        "Marseille": "https://logo.clearbit.com/om.fr",
        "Monaco": "https://logo.clearbit.com/asmonaco.com",
        "Lyon": "https://logo.clearbit.com/ol.fr",
        "Lille": "https://logo.clearbit.com/losc.fr",
        "Lens": "https://logo.clearbit.com/rclens.fr",
        "Nice": "https://logo.clearbit.com/ogcnice.com",
        "Rennes": "https://logo.clearbit.com/staderennais.com",
        "Strasbourg": "https://logo.clearbit.com/rcstrasbourg.fr",
        "Brest": "https://logo.clearbit.com/sb29.bzh",
        "Nantes": "https://logo.clearbit.com/fcnantes.com",
        "Toulouse": "https://logo.clearbit.com/toulousefc.com",
        "Reims": "https://logo.clearbit.com/stade-de-reims.com",
        "Montpellier": "https://logo.clearbit.com/mhscfoot.com",
        "Auxerre": "https://logo.clearbit.com/aja.fr",
        "Angers": "https://logo.clearbit.com/angers-sco.fr",
        "Saint-Étienne": "https://logo.clearbit.com/asse.fr",
        "Le Havre": "https://logo.clearbit.com/hac-foot.com",
    };

    // Return Clearbit logo if available
    return clearbitLogos[clubName] || null;
}

export function getClubInitials(clubName: string): string {
    return clubName
        .split(' ')
        .map(word => word[0])
        .join('')
        .substring(0, 2)
        .toUpperCase();
}
