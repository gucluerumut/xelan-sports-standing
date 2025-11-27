import requests
import json
from pathlib import Path

# Read the logo helper file
with open('lib/club-logo-helper.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract logo URLs
import re
url_pattern = r'"([^"]+)": "(https://[^"]+)"'
matches = re.findall(url_pattern, content)

print(f"Testing {len(matches)} logo URLs...")
print("=" * 60)

broken_logos = []
working_logos = []

for club_name, url in matches:
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        if response.status_code == 200:
            working_logos.append((club_name, url))
            print(f"✓ {club_name}")
        else:
            broken_logos.append((club_name, url, response.status_code))
            print(f"✗ {club_name} - Status: {response.status_code}")
    except Exception as e:
        broken_logos.append((club_name, url, str(e)))
        print(f"✗ {club_name} - Error: {str(e)[:50]}")

print("\n" + "=" * 60)
print(f"\nResults:")
print(f"✓ Working: {len(working_logos)}/{len(matches)}")
print(f"✗ Broken: {len(broken_logos)}/{len(matches)}")

if broken_logos:
    print(f"\nBroken logos:")
    with open('broken-logos.txt', 'w', encoding='utf-8') as f:
        f.write("Broken Logo URLs\n")
        f.write("=" * 60 + "\n\n")
        for club, url, error in broken_logos:
            print(f"  - {club}")
            f.write(f"{club}\n")
            f.write(f"  URL: {url}\n")
            f.write(f"  Error: {error}\n\n")
    
    print(f"\nReport saved to: broken-logos.txt")
