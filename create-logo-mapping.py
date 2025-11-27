import json

# Club logo mapping - using official sources
CLUB_LOGOS = {
    # Premier League
    "Manchester City": "https://resources.premierleague.com/premierleague/badges/50/t43.png",
    "Arsenal": "https://resources.premierleague.com/premierleague/badges/50/t3.png",
    "Liverpool": "https://resources.premierleague.com/premierleague/badges/50/t14.png",
    "Aston Villa": "https://resources.premierleague.com/premierleague/badges/50/t7.png",
    "Tottenham Hotspur": "https://resources.premierleague.com/premierleague/badges/50/t6.png",
    "Chelsea": "https://resources.premierleague.com/premierleague/badges/50/t8.png",
    "Newcastle United": "https://resources.premierleague.com/premierleague/badges/50/t4.png",
    "Manchester United": "https://resources.premierleague.com/premierleague/badges/50/t1.png",
    "West Ham United": "https://resources.premierleague.com/premierleague/badges/50/t21.png",
    "Brighton & Hove Albion": "https://resources.premierleague.com/premierleague/badges/50/t36.png",
    "Bournemouth": "https://resources.premierleague.com/premierleague/badges/50/t91.png",
    "Fulham": "https://resources.premierleague.com/premierleague/badges/50/t54.png",
    "Wolverhampton Wanderers": "https://resources.premierleague.com/premierleague/badges/50/t39.png",
    "Everton": "https://resources.premierleague.com/premierleague/badges/50/t11.png",
    "Brentford": "https://resources.premierleague.com/premierleague/badges/50/t94.png",
    "Nottingham Forest": "https://resources.premierleague.com/premierleague/badges/50/t17.png",
    "Luton Town": "https://resources.premierleague.com/premierleague/badges/50/t102.png",
    "Burnley": "https://resources.premierleague.com/premierleague/badges/50/t90.png",
    "Crystal Palace": "https://resources.premierleague.com/premierleague/badges/50/t31.png",
    "Sheffield United": "https://resources.premierleague.com/premierleague/badges/50/t49.png",
    
    # La Liga
    "Real Madrid": "https://assets.laliga.com/squad/2024/t186/p186_badge.png",
    "Barcelona": "https://assets.laliga.com/squad/2024/t178/p178_badge.png",
    "Atlético Madrid": "https://assets.laliga.com/squad/2024/t175/p175_badge.png",
    "Athletic Bilbao": "https://assets.laliga.com/squad/2024/t173/p173_badge.png",
    "Real Sociedad": "https://assets.laliga.com/squad/2024/t188/p188_badge.png",
    "Real Betis": "https://assets.laliga.com/squad/2024/t185/p185_badge.png",
    "Villarreal": "https://assets.laliga.com/squad/2024/t449/p449_badge.png",
    "Valencia": "https://assets.laliga.com/squad/2024/t191/p191_badge.png",
    "Osasuna": "https://assets.laliga.com/squad/2024/t179/p179_badge.png",
    "Getafe": "https://assets.laliga.com/squad/2024/t182/p182_badge.png",
    "Sevilla": "https://assets.laliga.com/squad/2024/t559/p559_badge.png",
    "Girona": "https://assets.laliga.com/squad/2024/t2922/p2922_badge.png",
    "Rayo Vallecano": "https://assets.laliga.com/squad/2024/t184/p184_badge.png",
    "Las Palmas": "https://assets.laliga.com/squad/2024/t2920/p2920_badge.png",
    "Alavés": "https://assets.laliga.com/squad/2024/t180/p180_badge.png",
    "Mallorca": "https://assets.laliga.com/squad/2024/t181/p181_badge.png",
    "Cádiz": "https://assets.laliga.com/squad/2024/t2934/p2934_badge.png",
    "Celta Vigo": "https://assets.laliga.com/squad/2024/t558/p558_badge.png",
    "Granada": "https://assets.laliga.com/squad/2024/t2933/p2933_badge.png",
    "Almería": "https://assets.laliga.com/squad/2024/t2935/p2935_badge.png",
    
    # Süper Lig - using generic football logo API
    "Galatasaray": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Galatasaray_Sports_Club_Logo.png/100px-Galatasaray_Sports_Club_Logo.png",
    "Fenerbahçe": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Fenerbahce.png/100px-Fenerbahce.png",
    "Beşiktaş": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Besiktas_JK_logo.svg/100px-Besiktas_JK_logo.svg.png",
    "Trabzonspor": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Trabzonspor_logo.svg/100px-Trabzonspor_logo.svg.png",
}

# Generate logo mapping JSON
with open('club-logo-mapping.json', 'w', encoding='utf-8') as f:
    json.dump(CLUB_LOGOS, f, indent=2, ensure_ascii=False)

print(f"Created logo mapping for {len(CLUB_LOGOS)} clubs")
print("\nNote: This is a starter mapping. You'll need to add more clubs manually.")
print("For clubs without logos, the component will fall back to initials.")
