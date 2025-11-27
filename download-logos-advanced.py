import requests
import os
import time
from pathlib import Path
import json

# Create logos directory
logos_dir = Path('public/logos')
logos_dir.mkdir(parents=True, exist_ok=True)

# Club to ID mappings for various APIs
# This helps us get accurate logos from specific sports APIs
club_mappings = {
    # Premier League
    "manchester-city": {"tsdb": "133613", "fotmob": "8456"},
    "arsenal": {"tsdb": "133604", "fotmob": "9825"},
    "liverpool": {"tsdb": "133602", "fotmob": "8650"},
    "aston-villa": {"tsdb": "133601", "fotmob": "10252"},
    "tottenham-hotspur": {"tsdb": "133616", "fotmob": "8586"},
    "chelsea": {"tsdb": "133610", "fotmob": "8455"},
    "newcastle-united": {"tsdb": "133615", "fotmob": "10261"},
    "manchester-united": {"tsdb": "133612", "fotmob": "10260"},
    "west-ham-united": {"tsdb": "133621", "fotmob": "8654"},
    "brighton-and-hove-albion": {"tsdb": "133619", "fotmob": "10204"},
    "bournemouth": {"tsdb": "133600", "fotmob": "8678"},
    "fulham": {"tsdb": "133607", "fotmob": "9879"},
    "wolverhampton-wanderers": {"tsdb": "133622", "fotmob": "8602"},
    "everton": {"tsdb": "133606", "fotmob": "8668"},
    "brentford": {"tsdb": "134108", "fotmob": "9937"},
    "nottingham-forest": {"tsdb": "133617", "fotmob": "10203"},
    "crystal-palace": {"tsdb": "133632", "fotmob": "9826"},
    "leicester-city": {"tsdb": "133626", "fotmob": "8197"},
    "ipswich-town": {"tsdb": "133624", "fotmob": "9850"},
    "southampton": {"tsdb": "133614", "fotmob": "8466"},

    # La Liga
    "real-madrid": {"tsdb": "133729", "fotmob": "8633"},
    "barcelona": {"tsdb": "133739", "fotmob": "8634"},
    "atletico-madrid": {"tsdb": "133727", "fotmob": "9906"},
    "athletic-bilbao": {"tsdb": "133723", "fotmob": "8315"},
    "real-sociedad": {"tsdb": "133730", "fotmob": "8560"},
    "real-betis": {"tsdb": "133722", "fotmob": "8603"},
    "villarreal": {"tsdb": "133741", "fotmob": "10205"},
    "valencia": {"tsdb": "133738", "fotmob": "10267"},
    "sevilla": {"tsdb": "133736", "fotmob": "8302"},
    "girona": {"tsdb": "134313", "fotmob": "9812"},
    "osasuna": {"tsdb": "133731", "fotmob": "8371"},
    "getafe": {"tsdb": "133726", "fotmob": "8305"},
    "rayo-vallecano": {"tsdb": "133733", "fotmob": "8370"},
    "celta-vigo": {"tsdb": "133724", "fotmob": "9910"},
    "mallorca": {"tsdb": "133728", "fotmob": "8306"},
    "las-palmas": {"tsdb": "133734", "fotmob": "8372"},
    "alaves": {"tsdb": "133725", "fotmob": "9866"},
    "espanyol": {"tsdb": "133740", "fotmob": "8558"},
    "leganes": {"tsdb": "134701", "fotmob": "9869"},
    "valladolid": {"tsdb": "133737", "fotmob": "10281"},

    # Süper Lig
    "galatasaray": {"tsdb": "133960", "fotmob": "8637"},
    "fenerbahce": {"tsdb": "133958", "fotmob": "8640"},
    "besiktas": {"tsdb": "133954", "fotmob": "8609"},
    "trabzonspor": {"tsdb": "133967", "fotmob": "8746"},
    "istanbul-basaksehir": {"tsdb": "133962", "fotmob": "8666"},
    "samsunspor": {"tsdb": "133965", "fotmob": "10166"},
    "goztepe": {"tsdb": "133961", "fotmob": "9909"},
    "kasimpasa": {"tsdb": "133963", "fotmob": "8489"},
    "sivasspor": {"tsdb": "133966", "fotmob": "8426"},
    "alanyaspor": {"tsdb": "134460", "fotmob": "10173"},
    "antalyaspor": {"tsdb": "133953", "fotmob": "8121"},
    "konyaspor": {"tsdb": "133957", "fotmob": "9908"},
    "gaziantep-fk": {"tsdb": "134459", "fotmob": "8539"},
    "kayserispor": {"tsdb": "133956", "fotmob": "10165"},
    "caykur-rizespor": {"tsdb": "133955", "fotmob": "10164"},
    "hatayspor": {"tsdb": "136979", "fotmob": "7701"},
    "eyupspor": {"tsdb": "136980", "fotmob": "10170"},
    "pendikspor": {"tsdb": "138089", "fotmob": "10171"},
    "bodrum-fk": {"tsdb": "138090", "fotmob": "159333"},

    # Serie A
    "juventus": {"tsdb": "133676", "fotmob": "9885"},
    "inter-milan": {"tsdb": "133670", "fotmob": "8636"},
    "ac-milan": {"tsdb": "133667", "fotmob": "8564"},
    "napoli": {"tsdb": "133673", "fotmob": "9875"},
    "roma": {"tsdb": "133682", "fotmob": "8686"},
    "lazio": {"tsdb": "133668", "fotmob": "8543"},
    "atalanta": {"tsdb": "133664", "fotmob": "8524"},
    "fiorentina": {"tsdb": "133669", "fotmob": "8535"},
    "bologna": {"tsdb": "133665", "fotmob": "9857"},
    "torino": {"tsdb": "133685", "fotmob": "9804"},
    "udinese": {"tsdb": "133686", "fotmob": "8600"},
    "genoa": {"tsdb": "133671", "fotmob": "10233"},
    "monza": {"tsdb": "134702", "fotmob": "6504"},
    "lecce": {"tsdb": "133672", "fotmob": "9888"},
    "verona": {"tsdb": "133687", "fotmob": "9876"},
    "cagliari": {"tsdb": "133666", "fotmob": "8529"},
    "parma": {"tsdb": "133678", "fotmob": "10217"},
    "como": {"tsdb": "134703", "fotmob": "8282"},
    "venezia": {"tsdb": "134704", "fotmob": "7881"},
    "empoli": {"tsdb": "133675", "fotmob": "8534"},

    # Bundesliga
    "bayern-munich": {"tsdb": "133746", "fotmob": "9823"},
    "borussia-dortmund": {"tsdb": "133750", "fotmob": "9789"},
    "rb-leipzig": {"tsdb": "134705", "fotmob": "178475"},
    "bayer-leverkusen": {"tsdb": "133745", "fotmob": "8178"},
    "vfb-stuttgart": {"tsdb": "133762", "fotmob": "10269"},
    "eintracht-frankfurt": {"tsdb": "133751", "fotmob": "9810"},
    "borussia-monchengladbach": {"tsdb": "133754", "fotmob": "9788"},
    "vfl-wolfsburg": {"tsdb": "133764", "fotmob": "8721"},
    "sc-freiburg": {"tsdb": "133752", "fotmob": "8358"},
    "tsg-hoffenheim": {"tsdb": "133758", "fotmob": "8226"},
    "union-berlin": {"tsdb": "134706", "fotmob": "8177"},
    "sv-werder-bremen": {"tsdb": "133763", "fotmob": "8697"},
    "fc-augsburg": {"tsdb": "133743", "fotmob": "9829"},
    "mainz-05": {"tsdb": "133756", "fotmob": "9905"},
    "vfl-bochum": {"tsdb": "133748", "fotmob": "9911"},
    "heidenheim": {"tsdb": "134707", "fotmob": "5885"},
    "fc-st-pauli": {"tsdb": "133760", "fotmob": "8464"},
    "holstein-kiel": {"tsdb": "134708", "fotmob": "8166"},

    # Ligue 1
    "psg": {"tsdb": "133714", "fotmob": "9847"},
    "marseille": {"tsdb": "133710", "fotmob": "8592"},
    "monaco": {"tsdb": "133711", "fotmob": "9827"},
    "lyon": {"tsdb": "133709", "fotmob": "8605"},
    "lille": {"tsdb": "133707", "fotmob": "8639"},
    "lens": {"tsdb": "133706", "fotmob": "8588"},
    "nice": {"tsdb": "133713", "fotmob": "9831"},
    "rennes": {"tsdb": "133715", "fotmob": "9851"},
    "strasbourg": {"tsdb": "133717", "fotmob": "9837"},
    "brest": {"tsdb": "133702", "fotmob": "8521"},
    "nantes": {"tsdb": "133712", "fotmob": "9830"},
    "toulouse": {"tsdb": "133718", "fotmob": "9941"},
    "reims": {"tsdb": "133716", "fotmob": "9838"},
    "montpellier": {"tsdb": "133719", "fotmob": "10249"},
    "auxerre": {"tsdb": "133700", "fotmob": "8583"},
    "angers": {"tsdb": "133701", "fotmob": "8122"},
    "saint-etienne": {"tsdb": "133720", "fotmob": "8696"},
    "le-havre": {"tsdb": "133705", "fotmob": "9747"},
}

def get_logo_sources(club_name):
    safe_name = club_name.lower().replace(' ', '-').replace('.', '').replace('&', 'and').replace('ç', 'c').replace('ğ', 'g').replace('ı', 'i').replace('ö', 'o').replace('ş', 's').replace('ü', 'u')
    
    sources = []
    
    # 1. TheSportsDB (High Quality)
    if safe_name in club_mappings and "tsdb" in club_mappings[safe_name]:
        tsdb_id = club_mappings[safe_name]["tsdb"]
        sources.append(f"https://www.thesportsdb.com/images/media/team/badge/{tsdb_id}.png") # Try ID based (hypothetical)
        sources.append(f"https://www.thesportsdb.com/images/media/team/badge/{safe_name.replace('-', '_')}.png")
    
    # 2. FotMob (Reliable CDN)
    if safe_name in club_mappings and "fotmob" in club_mappings[safe_name]:
        fotmob_id = club_mappings[safe_name]["fotmob"]
        sources.append(f"https://images.fotmob.com/image_resources/logo/teamlogo/{fotmob_id}.png")
        
    # 3. Clearbit (Official Domain)
    # ... (existing logic)
    
    # 4. Wikipedia (Fallback)
    # ... (existing logic)
    
    return sources

def download_logos():
    print("Starting multi-source logo download...")
    
    for name, ids in club_mappings.items():
        filename = f"{name}.png"
        filepath = logos_dir / filename
        
        if filepath.exists():
            print(f"✓ {name} - already exists")
            continue
            
        # Try FotMob first (very reliable)
        if "fotmob" in ids:
            url = f"https://images.fotmob.com/image_resources/logo/teamlogo/{ids['fotmob']}.png"
            try:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(r.content)
                    print(f"✓ {name} - downloaded from FotMob")
                    continue
            except:
                pass
                
        # Try TheSportsDB
        # ...
        
        print(f"✗ {name} - failed to download")

if __name__ == "__main__":
    download_logos()
