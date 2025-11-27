import requests
import os
import re
import time
from pathlib import Path

# Create logos directory
logos_dir = Path('public/logos')
logos_dir.mkdir(parents=True, exist_ok=True)

# Read club data
with open('lib/club-data-real.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract club names
club_pattern = r"name: ['\"]([^'\"]+)['\"]"
clubs = re.findall(club_pattern, content)

print(f"Found {len(clubs)} clubs")

# Logo sources
def get_logo_sources(club_name):
    clean_name = club_name.lower().replace(' ', '').replace('-', '').replace('.', '')
    slug_name = club_name.lower().replace(' ', '-').replace('.', '')
    
    sources = []
    
    # 1. Clearbit (Official Domains)
    domain_map = {
        "manchestercity": "mancity.com",
        "arsenal": "arsenal.com",
        "liverpool": "liverpoolfc.com",
        "astonvilla": "avfc.co.uk",
        "tottenhamhotspur": "tottenhamhotspur.com",
        "chelsea": "chelseafc.com",
        "newcastleunited": "nufc.co.uk",
        "manchesterunited": "manutd.com",
        "westhamunited": "whufc.com",
        "brighton&hovealbion": "brightonandhovealbion.com",
        "bournemouth": "afcb.co.uk",
        "fulham": "fulhamfc.com",
        "wolverhamptonwanderers": "wolves.co.uk",
        "everton": "evertonfc.com",
        "brentford": "brentfordfc.com",
        "nottinghamforest": "nottinghamforest.co.uk",
        "crystalpalace": "cpfc.co.uk",
        "leicestercity": "lcfc.com",
        "ipswichtown": "itfc.co.uk",
        "southampton": "southamptonfc.com",
        "realmadrid": "realmadrid.com",
        "barcelona": "fcbarcelona.com",
        "atleticomadrid": "atleticodemadrid.com",
        "athleticbilbao": "athletic-club.eus",
        "realsociedad": "realsociedad.eus",
        "realbetis": "realbetisbalompie.es",
        "villarreal": "villarrealcf.es",
        "valencia": "valenciacf.com",
        "sevilla": "sevillafc.es",
        "girona": "gironafc.cat",
        "galatasaray": "galatasaray.org",
        "fenerbahce": "fenerbahce.org",
        "besiktas": "bjk.com.tr",
        "trabzonspor": "trabzonspor.org.tr",
        "juventus": "juventus.com",
        "intermilan": "inter.it",
        "acmilan": "acmilan.com",
        "napoli": "sscnapoli.it",
        "roma": "asroma.com",
        "lazio": "sslazio.it",
        "bayernmunich": "fcbayern.com",
        "borussiadortmund": "bvb.de",
        "rbleipzig": "rbleipzig.com",
        "bayerleverkusen": "bayer04.de",
        "parissaintgermain": "psg.fr",
        "marseille": "om.fr",
        "monaco": "asmonaco.com",
        "lyon": "ol.fr"
    }
    
    if clean_name in domain_map:
        sources.append(f"https://logo.clearbit.com/{domain_map[clean_name]}")
    
    # 2. Wikipedia Commons (Direct SVG/PNG)
    wiki_map = {
        "manchestercity": "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Manchester_City_FC_badge.svg/200px-Manchester_City_FC_badge.svg.png",
        "arsenal": "https://upload.wikimedia.org/wikipedia/en/thumb/5/53/Arsenal_FC.svg/200px-Arsenal_FC.svg.png",
        "liverpool": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0c/Liverpool_FC.svg/200px-Liverpool_FC.svg.png",
        "galatasaray": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Galatasaray_Sports_Club_Logo.png/200px-Galatasaray_Sports_Club_Logo.png",
        "fenerbahce": "https://upload.wikimedia.org/wikipedia/en/thumb/8/86/Fenerbahce_SK_Logo.svg/200px-Fenerbahce_SK_Logo.svg.png",
        "besiktas": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Besiktas_JK_logo.svg/200px-Besiktas_JK_logo.svg.png",
        "trabzonspor": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Trabzonspor_logo.svg/200px-Trabzonspor_logo.svg.png",
        "realmadrid": "https://upload.wikimedia.org/wikipedia/en/thumb/5/56/Real_Madrid_CF.svg/200px-Real_Madrid_CF.svg.png",
        "barcelona": "https://upload.wikimedia.org/wikipedia/en/thumb/4/47/FC_Barcelona_%28crest%29.svg/200px-FC_Barcelona_%28crest%29.svg.png",
        "bayernmunich": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg/200px-FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg.png",
        "parissaintgermain": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a7/Paris_Saint-Germain_F.C..svg/200px-Paris_Saint-Germain_F.C..svg.png",
        "juventus": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Juventus_FC_-_pictogram_black_%28Italy%2C_2017%29.svg/200px-Juventus_FC_-_pictogram_black_%28Italy%2C_2017%29.svg.png"
    }
    
    if clean_name in wiki_map:
        sources.append(wiki_map[clean_name])
        
    # 3. Generic Fallbacks
    sources.append(f"https://crests.football-data.org/{slug_name}.svg")
    
    return sources

def download_logo(club_name):
    # Create safe filename
    safe_name = club_name.lower().replace(' ', '-').replace('.', '').replace('&', 'and').replace('ç', 'c').replace('ğ', 'g').replace('ı', 'i').replace('ö', 'o').replace('ş', 's').replace('ü', 'u')
    filename = f"{safe_name}.png"
    filepath = logos_dir / filename
    
    if filepath.exists():
        print(f"✓ {club_name} - already exists")
        return True
        
    sources = get_logo_sources(club_name)
    
    for url in sources:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200 and len(response.content) > 1000:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"✓ {club_name} - downloaded from {url}")
                return True
        except Exception as e:
            continue
            
    print(f"✗ {club_name} - failed to download")
    return False

# Download all logos
print("\nDownloading logos...")
print("=" * 50)

success_count = 0
failed_clubs = []

for i, club in enumerate(clubs, 1):
    if download_logo(club):
        success_count += 1
    else:
        failed_clubs.append(club)
    time.sleep(0.2)

print("\n" + "=" * 50)
print(f"Success: {success_count}/{len(clubs)}")
print(f"Failed: {len(failed_clubs)}")

if failed_clubs:
    print("\nFailed clubs:")
    for club in failed_clubs:
        print(f"- {club}")
