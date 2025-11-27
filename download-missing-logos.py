import requests
import os
import time
from pathlib import Path

# Create logos directory
logos_dir = Path('public/logos')
logos_dir.mkdir(parents=True, exist_ok=True)

# Manual mapping for missing logos (Wikipedia Commons)
missing_logos = {
    # Premier League
    "manchester-city": "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Manchester_City_FC_badge.svg/200px-Manchester_City_FC_badge.svg.png",
    "liverpool": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0c/Liverpool_FC.svg/200px-Liverpool_FC.svg.png",
    "manchester-united": "https://upload.wikimedia.org/wikipedia/en/thumb/7/7a/Manchester_United_FC_crest.svg/200px-Manchester_United_FC_crest.svg.png",
    "chelsea": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Chelsea_FC.svg/200px-Chelsea_FC.svg.png",
    "tottenham-hotspur": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b4/Tottenham_Hotspur.svg/200px-Tottenham_Hotspur.svg.png",
    "newcastle-united": "https://upload.wikimedia.org/wikipedia/en/thumb/5/56/Newcastle_United_Logo.svg/200px-Newcastle_United_Logo.svg.png",
    "west-ham-united": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c2/West_Ham_United_FC_logo.svg/200px-West_Ham_United_FC_logo.svg.png",
    "aston-villa": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f9/Aston_Villa_FC_crest_%282016%29.svg/200px-Aston_Villa_FC_crest_%282016%29.svg.png",
    "brighton-and-hove-albion": "https://upload.wikimedia.org/wikipedia/en/thumb/f/fd/Brighton_%26_Hove_Albion_logo.svg/200px-Brighton_%26_Hove_Albion_logo.svg.png",
    "fulham": "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Fulham_FC_%28shield%29.svg/200px-Fulham_FC_%28shield%29.svg.png",
    "brentford": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2a/Brentford_FC_crest.svg/200px-Brentford_FC_crest.svg.png",
    "crystal-palace": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/Crystal_Palace_FC_logo_%282022%29.svg/200px-Crystal_Palace_FC_logo_%282022%29.svg.png",
    "bournemouth": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e5/AFC_Bournemouth_%282013%29.svg/200px-AFC_Bournemouth_%282013%29.svg.png",
    "wolverhampton-wanderers": "https://upload.wikimedia.org/wikipedia/en/thumb/f/fc/Wolverhampton_Wanderers.svg/200px-Wolverhampton_Wanderers.svg.png",
    "southampton": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c9/FC_Southampton.svg/200px-FC_Southampton.svg.png",
    "leicester-city": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2d/Leicester_City_crest.svg/200px-Leicester_City_crest.svg.png",
    "nottingham-forest": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e5/Nottingham_Forest_F.C._logo.svg/200px-Nottingham_Forest_F.C._logo.svg.png",
    
    # La Liga
    "barcelona": "https://upload.wikimedia.org/wikipedia/en/thumb/4/47/FC_Barcelona_%28crest%29.svg/200px-FC_Barcelona_%28crest%29.svg.png",
    "atletico-madrid": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f4/Atletico_Madrid_2017_logo.svg/200px-Atletico_Madrid_2017_logo.svg.png",
    "athletic-bilbao": "https://upload.wikimedia.org/wikipedia/en/thumb/9/98/Club_Athletic_Bilbao_logo.svg/200px-Club_Athletic_Bilbao_logo.svg.png",
    "real-betis": "https://upload.wikimedia.org/wikipedia/en/thumb/1/13/Real_betis_logo.svg/200px-Real_betis_logo.svg.png",
    "villarreal": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/Villarreal_CF_logo-en.svg/200px-Villarreal_CF_logo-en.svg.png",
    "valencia": "https://upload.wikimedia.org/wikipedia/en/thumb/c/ce/Valenciacf.svg/200px-Valenciacf.svg.png",
    "sevilla": "https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/Sevilla_FC_logo.svg/200px-Sevilla_FC_logo.svg.png",
    "girona": "https://upload.wikimedia.org/wikipedia/en/thumb/7/79/Girona_FC_logo.svg/200px-Girona_FC_logo.svg.png",
    "celta-vigo": "https://upload.wikimedia.org/wikipedia/en/thumb/1/12/RC_Celta_de_Vigo_logo.svg/200px-RC_Celta_de_Vigo_logo.svg.png",
    "mallorca": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e0/RCD_Mallorca.svg/200px-RCD_Mallorca.svg.png",
    "espanyol": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a7/RCD_Espanyol_logo.svg/200px-RCD_Espanyol_logo.svg.png",
    "getafe": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2e/Getafe_logo.svg/200px-Getafe_logo.svg.png",
    "leganes": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c6/CD_Legan%C3%A9s_logo.svg/200px-CD_Legan%C3%A9s_logo.svg.png",
    "valladolid": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8c/Real_Valladolid_Logo.svg/200px-Real_Valladolid_Logo.svg.png",
    "osasuna": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c2/CA_Osasuna_logo.svg/200px-CA_Osasuna_logo.svg.png",
    "alaves": "https://upload.wikimedia.org/wikipedia/en/thumb/7/79/Deportivo_Alav%C3%A9s_logo.svg/200px-Deportivo_Alav%C3%A9s_logo.svg.png",
    "rayo-vallecano": "https://upload.wikimedia.org/wikipedia/en/thumb/6/6b/Rayo_Vallecano_logo.svg/200px-Rayo_Vallecano_logo.svg.png",
    
    # Süper Lig
    "galatasaray": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Galatasaray_Sports_Club_Logo.png/200px-Galatasaray_Sports_Club_Logo.png",
    "fenerbahce": "https://upload.wikimedia.org/wikipedia/en/thumb/8/86/Fenerbahce_SK_Logo.svg/200px-Fenerbahce_SK_Logo.svg.png",
    "besiktas": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Besiktas_JK_logo.svg/200px-Besiktas_JK_logo.svg.png",
    "istanbul-basaksehir": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0a/Istanbul_Basaksehir_FK.svg/200px-Istanbul_Basaksehir_FK.svg.png",
    "samsunspor": "https://upload.wikimedia.org/wikipedia/en/thumb/9/9d/Samsunspor_logo.svg/200px-Samsunspor_logo.svg.png",
    "goztepe": "https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/G%C3%B6ztepe_SK_logo.svg/200px-G%C3%B6ztepe_SK_logo.svg.png",
    "sivasspor": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0d/Sivasspor_logo.svg/200px-Sivasspor_logo.svg.png",
    "konyaspor": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5f/Konyaspor.svg/200px-Konyaspor.svg.png",
    "alanyaspor": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e2/Alanyaspor_logo.svg/200px-Alanyaspor_logo.svg.png",
    "antalyaspor": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8f/Antalyaspor_logo.svg/200px-Antalyaspor_logo.svg.png",
    "gaziantep-fk": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8d/Gaziantep_FK_logo.svg/200px-Gaziantep_FK_logo.svg.png",
    "kasimpasa": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e8/Kasimpasa_SK.svg/200px-Kasimpasa_SK.svg.png",
    "hatayspor": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5f/Hatayspor_logo.svg/200px-Hatayspor_logo.svg.png",
    "pendikspor": "https://upload.wikimedia.org/wikipedia/en/thumb/3/3f/Pendikspor_logo.svg/200px-Pendikspor_logo.svg.png",
    "kayserispor": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e7/Kayserispor_logo.svg/200px-Kayserispor_logo.svg.png",
    "eyupspor": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8a/Ey%C3%BCpspor_logo.svg/200px-Ey%C3%BCpspor_logo.svg.png",
    "caykur-rizespor": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a0/%C3%87aykur_Rizespor_logo.svg/200px-%C3%87aykur_Rizespor_logo.svg.png",
    
    # Serie A
    "inter-milan": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/FC_Internazionale_Milano_2021.svg/200px-FC_Internazionale_Milano_2021.svg.png",
    "napoli": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/SSC_Neapel.svg/200px-SSC_Neapel.svg.png",
    "roma": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f7/AS_Roma_logo_%282017%29.svg/200px-AS_Roma_logo_%282017%29.svg.png",
    "fiorentina": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/ACF_Fiorentina.svg/200px-ACF_Fiorentina.svg.png",
    "lazio": "https://upload.wikimedia.org/wikipedia/en/thumb/c/ce/S.S._Lazio_badge.svg/200px-S.S._Lazio_badge.svg.png",
    "atalanta": "https://upload.wikimedia.org/wikipedia/en/thumb/6/66/Atalanta_BC_logo.svg/200px-Atalanta_BC_logo.svg.png",
    "como": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Como_1907_logo.svg/200px-Como_1907_logo.svg.png",
    "parma": "https://upload.wikimedia.org/wikipedia/en/thumb/4/43/Parma_Calcio_1913_logo.svg/200px-Parma_Calcio_1913_logo.svg.png",
    "bologna": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Bologna_FC_1909_logo.svg/200px-Bologna_FC_1909_logo.svg.png",
    "cagliari": "https://upload.wikimedia.org/wikipedia/en/thumb/7/71/Cagliari_Calcio_1920.svg/200px-Cagliari_Calcio_1920.svg.png",
    "torino": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2e/Torino_FC_Logo.svg/200px-Torino_FC_Logo.svg.png",
    "genoa": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e0/Genoa_CFC_logo.svg/200px-Genoa_CFC_logo.svg.png",
    "venezia": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8f/Venezia_FC_logo.svg/200px-Venezia_FC_logo.svg.png",
    "udinese": "https://upload.wikimedia.org/wikipedia/en/thumb/c/ce/Udinese_Calcio_logo.svg/200px-Udinese_Calcio_logo.svg.png",
    "verona": "https://upload.wikimedia.org/wikipedia/en/thumb/6/61/Hellas_Verona_FC_logo.svg/200px-Hellas_Verona_FC_logo.svg.png",
    "monza": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/AC_Monza_Logo.svg/200px-AC_Monza_Logo.svg.png",
    "lecce": "https://upload.wikimedia.org/wikipedia/en/thumb/8/87/US_Lecce_logo.svg/200px-US_Lecce_logo.svg.png",
    
    # Bundesliga
    "bayern-munich": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg/200px-FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg.png",
    "borussia-dortmund": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Borussia_Dortmund_logo.svg/200px-Borussia_Dortmund_logo.svg.png",
    "bayer-leverkusen": "https://upload.wikimedia.org/wikipedia/en/thumb/5/59/Bayer_04_Leverkusen_logo.svg/200px-Bayer_04_Leverkusen_logo.svg.png",
    "eintracht-frankfurt": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Eintracht_Frankfurt_Logo.svg/200px-Eintracht_Frankfurt_Logo.svg.png",
    "borussia-monchengladbach": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Borussia_M%C3%B6nchengladbach_logo.svg/200px-Borussia_M%C3%B6nchengladbach_logo.svg.png",
    "vfl-wolfsburg": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Logo-VfL-Wolfsburg.svg/200px-Logo-VfL-Wolfsburg.svg.png",
    "vfb-stuttgart": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/VfB_Stuttgart_1893_Logo.svg/200px-VfB_Stuttgart_1893_Logo.svg.png",
    "sc-freiburg": "https://upload.wikimedia.org/wikipedia/en/thumb/1/11/SC_Freiburg_logo.svg/200px-SC_Freiburg_logo.svg.png",
    "sv-werder-bremen": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/SV-Werder-Bremen-Logo.svg/200px-SV-Werder-Bremen-Logo.svg.png",
    "tsg-hoffenheim": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Logo_TSG_Hoffenheim.svg/200px-Logo_TSG_Hoffenheim.svg.png",
    "fc-st-pauli": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/FC_St._Pauli_logo.svg/200px-FC_St._Pauli_logo.svg.png",
    "mainz-05": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Logo_Mainz_05.svg/200px-Logo_Mainz_05.svg.png",
    "fc-augsburg": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/FC_Augsburg_logo.svg/200px-FC_Augsburg_logo.svg.png",
    "vfl-bochum": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/VfL_Bochum_logo.svg/200px-VfL_Bochum_logo.svg.png",
    "holstein-kiel": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Holstein_Kiel_Logo.svg/200px-Holstein_Kiel_Logo.svg.png",
    "union-berlin": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/1._FC_Union_Berlin_Logo.svg/200px-1._FC_Union_Berlin_Logo.svg.png",
    "heidenheim": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/1._FC_Heidenheim_1846_logo.svg/200px-1._FC_Heidenheim_1846_logo.svg.png",
    
    # Ligue 1
    "psg": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a7/Paris_Saint-Germain_F.C..svg/200px-Paris_Saint-Germain_F.C..svg.png",
    "marseille": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Olympique_Marseille_logo.svg/200px-Olympique_Marseille_logo.svg.png",
    "monaco": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Logo_AS_Monaco.svg/200px-Logo_AS_Monaco.svg.png",
    "lyon": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e2/Olympique_Lyonnais_logo.svg/200px-Olympique_Lyonnais_logo.svg.png",
    "lille": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/Lille_OSC_%282018%29_logo.svg/200px-Lille_OSC_%282018%29_logo.svg.png",
    "nice": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/OGC_Nice_logo.svg/200px-OGC_Nice_logo.svg.png",
    "nantes": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/FC_Nantes_logo.svg/200px-FC_Nantes_logo.svg.png",
    "strasbourg": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Racing_Club_de_Strasbourg_Alsace_logo.svg/200px-Racing_Club_de_Strasbourg_Alsace_logo.svg.png",
    "lens": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5a/RC_Lens_logo.svg/200px-RC_Lens_logo.svg.png",
    "saint-etienne": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2a/AS_Saint-%C3%89tienne_logo.svg/200px-AS_Saint-%C3%89tienne_logo.svg.png",
    "toulouse": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Toulouse_FC_2018_logo.svg/200px-Toulouse_FC_2018_logo.svg.png",
    "le-havre": "https://upload.wikimedia.org/wikipedia/en/thumb/7/71/Le_Havre_AC_logo.svg/200px-Le_Havre_AC_logo.svg.png",
    "rennes": "https://upload.wikimedia.org/wikipedia/en/thumb/2/25/Stade_Rennais_F.C._logo.svg/200px-Stade_Rennais_F.C._logo.svg.png",
    "brest": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/Stade_Brestois_29_logo.svg/200px-Stade_Brestois_29_logo.svg.png",
    "angers": "https://upload.wikimedia.org/wikipedia/en/thumb/3/30/Angers_SCO_logo.svg/200px-Angers_SCO_logo.svg.png",
    "auxerre": "https://upload.wikimedia.org/wikipedia/en/thumb/3/30/AJ_Auxerre_Logo.svg/200px-AJ_Auxerre_Logo.svg.png",
}

def download_logo(name, url):
    filename = f"{name}.png"
    filepath = logos_dir / filename
    
    if filepath.exists():
        print(f"✓ {name} - already exists")
        return True
        
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"✓ {name} - downloaded")
            return True
    except Exception as e:
        print(f"✗ {name} - error: {e}")
        
    print(f"✗ {name} - failed to download")
    return False

# Download missing logos
print("\nDownloading missing logos...")
print("=" * 50)

success_count = 0

for name, url in missing_logos.items():
    if download_logo(name, url):
        success_count += 1
    time.sleep(0.5)

print("\n" + "=" * 50)
print(f"Success: {success_count}/{len(missing_logos)}")
