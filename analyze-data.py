#!/usr/bin/env python3
import json

# Read the Instagram data
with open('instagram-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Define the leagues and their clubs
leagues = {
    'Premier League': [
        'mancity', 'arsenal', 'liverpoolfc', 'manchesterunited', 'chelseafc',
        'spursofficial', 'nufc', 'westham', 'avfcofficial', 'officialbhafc',
        'fulhamfc', 'brentfordfc', 'cpfc', 'afcb', 'wolves', 'everton',
        'ipswichtown', 'southamptonfc', 'lcfc', 'nottinghamforest'
    ],
    'La Liga': [
        'realmadrid', 'fcbarcelona', 'atleticodemadrid', 'villarrealcf',
        'realbetisbalompie', 'realsociedad', 'valenciacf', 'sevillafc',
        'gironafc', 'rccelta', 'rcdmallorcaoficial', 'rcdespanyol',
        'getafecf', 'cdleganes', 'realvalladolid', 'osasuna',
        'deportivoalaves', 'rayo_vallecano', 'laspalmasoficial', 'cadiz_cf'
    ],
    'Süper Lig': [
        'galatasaray', 'fenerbahce', 'besiktas', 'trabzonspor',
        'basaksehirfk', 'konyaspor', 'sivasspor', 'alanyaspor',
        'antalyaspor', 'samsunspor', 'gaziantepfk', 'goztepe',
        'kasimpasa', 'hatayspor', 'pendikspor', 'adanademirspor',
        'kayserispor', 'rizespor', 'eyupspor', 'bodrumspor'
    ]
}

# Create a mapping of username to data
username_map = {club.get('username'): club for club in data if club.get('username')}

# Analyze each league
print("=" * 80)
print("INSTAGRAM DATA ANALYSIS FOR XELAN SPORTS STANDING")
print("=" * 80)

for league_name, usernames in leagues.items():
    print(f"\n{league_name}")
    print("-" * 80)
    
    found = []
    not_found = []
    low_followers = []
    
    for username in usernames:
        if username in username_map:
            club_data = username_map[username]
            followers = club_data.get('followersCount', 0)
            verified = club_data.get('verified', False)
            
            if followers < 10000:
                low_followers.append((username, followers, verified))
            else:
                found.append((username, followers, verified))
        else:
            not_found.append(username)
    
    print(f"\n✅ FOUND ({len(found)} clubs):")
    for username, followers, verified in sorted(found, key=lambda x: x[1], reverse=True):
        verify_mark = "✓" if verified else "✗"
        print(f"  {username:30s} {followers:>12,} followers [{verify_mark}]")
    
    if low_followers:
        print(f"\n⚠️  LOW FOLLOWERS ({len(low_followers)} clubs - might be wrong accounts):")
        for username, followers, verified in low_followers:
            verify_mark = "✓" if verified else "✗"
            print(f"  {username:30s} {followers:>12,} followers [{verify_mark}]")
    
    if not_found:
        print(f"\n❌ NOT FOUND ({len(not_found)} clubs):")
        for username in not_found:
            print(f"  {username}")

# Find 2025-26 season clubs that should be in each league
print("\n" * 2)
print("=" * 80)
print("2025-26 SEASON RECOMMENDATIONS")
print("=" * 80)

print("\n📋 Premier League 2025-26:")
print("Current top teams that should be included:")
print("  - Manchester City, Arsenal, Liverpool, Chelsea, Manchester United")
print("  - Tottenham, Newcastle, Aston Villa, Brighton, Brentford")
print("  - Fulham, Crystal Palace, Bournemouth, West Ham, Wolves")
print("  - Everton, Nottingham Forest, Ipswich Town, Southampton, Leicester City")

print("\n📋 La Liga 2025-26:")
print("Current top teams that should be included:")
print("  - Real Madrid, Barcelona, Atlético Madrid, Athletic Bilbao")
print("  - Real Sociedad, Real Betis, Villarreal, Valencia, Sevilla")
print("  - Girona, Celta Vigo, Mallorca, Espanyol, Getafe")
print("  - Leganés, Valladolid, Osasuna, Alavés, Rayo Vallecano, Las Palmas")

print("\n📋 Süper Lig 2025-26:")
print("Current top teams that should be included:")
print("  - Galatasaray, Fenerbahçe, Beşiktaş, Trabzonspor")
print("  - Başakşehir, Samsunspor, Göztepe, Sivasspor")
print("  - Konyaspor, Alanyaspor, Antalyaspor, Gaziantep FK")
print("  - Kasımpaşa, Hatayspor, Pendikspor, Kayserispor")
print("  - Eyüpspor, Bodrum FK, Adana Demirspor, Rizespor")

print("\n" * 2)
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total clubs in JSON: {len(data)}")
print(f"Clubs with >100k followers: {len([c for c in data if c.get('followersCount', 0) > 100000])}")
print(f"Verified clubs: {len([c for c in data if c.get('verified', False)])}")
