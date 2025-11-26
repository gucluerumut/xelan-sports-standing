#!/usr/bin/env python3
import json
from collections import defaultdict

# Read the Instagram data
with open('instagram-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# League keywords to identify clubs
league_keywords = {
    'Premier League': ['premier', 'england', 'epl'],
    'La Liga': ['laliga', 'spain', 'españa'],
    'Süper Lig': ['turkey', 'turkish', 'süper'],
    'Serie A': ['italy', 'italian', 'serie'],
    'Bundesliga': ['germany', 'german', 'bundesliga'],
    'Ligue 1': ['france', 'french', 'ligue'],
}

# Manual club assignments based on known teams
known_clubs = {
    # Premier League
    'mancity': 'Premier League',
    'arsenal': 'Premier League',
    'liverpoolfc': 'Premier League',
    'manchesterunited': 'Premier League',
    'chelseafc': 'Premier League',
    'spursofficial': 'Premier League',
    'nufc': 'Premier League',
    'westham': 'Premier League',
    'avfcofficial': 'Premier League',
    'officialbhafc': 'Premier League',
    'fulhamfc': 'Premier League',
    'brentfordfc': 'Premier League',
    'cpfc': 'Premier League',
    'afcb': 'Premier League',
    'wolves': 'Premier League',
    'everton': 'Premier League',
    'ipswichtown': 'Premier League',
    'southamptonfc': 'Premier League',
    'lcfc': 'Premier League',
    
    # La Liga
    'realmadrid': 'La Liga',
    'fcbarcelona': 'La Liga',
    'atleticodemadrid': 'La Liga',
    'athleticclub': 'La Liga',
    'realsociedad': 'La Liga',
    'realbetisbalompie': 'La Liga',
    'villarrealcf': 'La Liga',
    'valenciacf': 'La Liga',
    'sevillafc': 'La Liga',
    'gironafc': 'La Liga',
    'rccelta': 'La Liga',
    'rcdmallorcaoficial': 'La Liga',
    'rcdespanyol': 'La Liga',
    'getafecf': 'La Liga',
    'cdleganes': 'La Liga',
    'realvalladolid': 'La Liga',
    'deportivoalaves': 'La Liga',
    
    # Süper Lig
    'galatasaray': 'Süper Lig',
    'fenerbahce': 'Süper Lig',
    'besiktas': 'Süper Lig',
    'trabzonspor': 'Süper Lig',
    'samsunspor': 'Süper Lig',
    'goztepe': 'Süper Lig',
    'konyaspor': 'Süper Lig',
    'hatayspor': 'Süper Lig',
    'sivasspor': 'Süper Lig',
    'gaziantepfk': 'Süper Lig',
    'antalyaspor': 'Süper Lig',
    'alanyaspor': 'Süper Lig',
    'pendikspor': 'Süper Lig',
    
    # Serie A
    'acmilan': 'Serie A',
    'inter': 'Serie A',
    'juventus': 'Serie A',
    'officialasroma': 'Serie A',
    'official_sslazio': 'Serie A',
    'acffiorentina': 'Serie A',
    'atalantabc': 'Serie A',
    'bolognafc1909': 'Serie A',
    'cagliaricalcio': 'Serie A',
    'acmonza': 'Serie A',
    'udinesecalcio': 'Serie A',
    'veneziafc': 'Serie A',
    'hellasveronafc': 'Serie A',
    'genoacfc': 'Serie A',
    'parmacalcio1913': 'Serie A',
    'torinofc1906': 'Serie A',
    'uslecce': 'Serie A',
    'comofootball': 'Serie A',
    
    # Bundesliga
    'fcbayern': 'Bundesliga',
    'bvb09': 'Bundesliga',
    'rbleipzig': 'Bundesliga',
    'bayer04fussball': 'Bundesliga',
    'eintrachtfrankfurt': 'Bundesliga',
    'borussia': 'Bundesliga',
    'vfl.wolfsburg': 'Bundesliga',
    'vfb': 'Bundesliga',
    'werderbremen': 'Bundesliga',
    'scfreiburg': 'Bundesliga',
    'tsghoffenheim': 'Bundesliga',
    '1fsvmainz05': 'Bundesliga',
    'fcaugsburg1907': 'Bundesliga',
    'fcstpauli': 'Bundesliga',
    'holsteinkiel': 'Bundesliga',
    'vflbochum1848.official': 'Bundesliga',
    
    # Ligue 1
    'psg': 'Ligue 1',
    'olympiquedemarseille': 'Ligue 1',
    'asmonaco': 'Ligue 1',
    'ol': 'Ligue 1',
    'losclive': 'Ligue 1',
    'fcnantes': 'Ligue 1',
    'toulousefc': 'Ligue 1',
    'ogcnice': 'Ligue 1',
    'rclens': 'Ligue 1',
    'rcsa': 'Ligue 1',
    'asseofficiel': 'Ligue 1',
    'hac_foot': 'Ligue 1',
}

# Organize clubs by league
leagues = defaultdict(list)

for club in data:
    username = club.get('username')
    followers = club.get('followersCount', 0)
    verified = club.get('verified', False)
    full_name = club.get('fullName', '')
    
    if not username or followers < 10000:
        continue
    
    # Assign to league
    league = known_clubs.get(username, 'Other')
    
    leagues[league].append({
        'username': username,
        'name': full_name or username,
        'followers': followers,
        'verified': verified
    })

# Sort each league by followers
for league in leagues:
    leagues[league].sort(key=lambda x: x['followers'], reverse=True)

# Print results
print("=" * 100)
print("COMPLETE LEAGUE ANALYSIS - ALL CLUBS BY FOLLOWERS")
print("=" * 100)

for league_name in ['Premier League', 'La Liga', 'Süper Lig', 'Serie A', 'Bundesliga', 'Ligue 1', 'Other']:
    if league_name not in leagues:
        continue
    
    clubs = leagues[league_name]
    print(f"\n{'='*100}")
    print(f"{league_name} - {len(clubs)} clubs")
    print(f"{'='*100}")
    print(f"{'Rank':<6} {'Username':<30} {'Name':<40} {'Followers':<15} {'Verified'}")
    print("-" * 100)
    
    for i, club in enumerate(clubs, 1):
        verify_mark = "✓" if club['verified'] else "✗"
        followers_str = f"{club['followers']:,}"
        print(f"{i:<6} {club['username']:<30} {club['name']:<40} {followers_str:<15} {verify_mark}")

# Generate summary
print("\n" * 2)
print("=" * 100)
print("SUMMARY")
print("=" * 100)
for league_name in ['Premier League', 'La Liga', 'Süper Lig', 'Serie A', 'Bundesliga', 'Ligue 1']:
    if league_name in leagues:
        print(f"{league_name:<20} {len(leagues[league_name]):>3} clubs")
print(f"{'Other':<20} {len(leagues.get('Other', [])):>3} clubs")
print(f"{'TOTAL':<20} {sum(len(clubs) for clubs in leagues.values()):>3} clubs")
