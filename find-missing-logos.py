import json
import re
from pathlib import Path

# Read club data to get all club names
with open('lib/club-data-real.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract club names
club_pattern = r"name: ['\"]([^'\"]+)['\"]"
all_clubs = re.findall(club_pattern, content)

# Read existing logos
with open('lib/club-logo-helper.ts', 'r', encoding='utf-8') as f:
    helper_content = f.read()

# Find clubs with logos
clubs_with_logos = []
for club in all_clubs:
    if f'"{club}":' in helper_content:
        clubs_with_logos.append(club)

# Find clubs without logos
clubs_without_logos = [club for club in all_clubs if club not in clubs_with_logos]

print(f"Total clubs: {len(all_clubs)}")
print(f"Clubs with logos: {len(clubs_with_logos)}")
print(f"Clubs without logos: {len(clubs_without_logos)}")
print("\n" + "="*60)
print("\nClubs WITHOUT logos:")
print("="*60)

# Group by league
from collections import defaultdict
clubs_by_league = defaultdict(list)

# Extract league for each club
league_pattern = r"name: ['\"]([^'\"]+)['\"],\s*league: ['\"]([^'\"]+)['\"]"
matches = re.findall(league_pattern, content)
club_to_league = {name: league for name, league in matches}

for club in clubs_without_logos:
    league = club_to_league.get(club, "Unknown")
    clubs_by_league[league].append(club)

# Print by league
for league in sorted(clubs_by_league.keys()):
    print(f"\n{league} ({len(clubs_by_league[league])} clubs):")
    for club in sorted(clubs_by_league[league]):
        print(f"  - {club}")

# Save to file for reference
with open('missing-logos.txt', 'w', encoding='utf-8') as f:
    f.write(f"Missing Logos Report\n")
    f.write(f"="*60 + "\n\n")
    f.write(f"Total clubs: {len(all_clubs)}\n")
    f.write(f"Clubs with logos: {len(clubs_with_logos)}\n")
    f.write(f"Clubs without logos: {len(clubs_without_logos)}\n\n")
    
    for league in sorted(clubs_by_league.keys()):
        f.write(f"\n{league} ({len(clubs_by_league[league])} clubs):\n")
        for club in sorted(clubs_by_league[league]):
            f.write(f"  - {club}\n")

print("\n" + "="*60)
print(f"\nReport saved to: missing-logos.txt")
