import requests
import json
import os
from pathlib import Path
import time

# Create logos directory
logos_dir = Path('public/logos')
logos_dir.mkdir(parents=True, exist_ok=True)

# Read club data
with open('lib/club-data-real.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract club names
import re
club_pattern = r"name: ['\"]([^'\"]+)['\"]"
clubs = re.findall(club_pattern, content)

print(f"Found {len(clubs)} clubs")

# Logo sources - using free logo APIs
def get_logo_url(club_name):
    """Get logo URL from various sources"""
    # Clean club name for URL
    clean_name = club_name.lower().replace(' ', '-').replace('ç', 'c').replace('ğ', 'g').replace('ı', 'i').replace('ö', 'o').replace('ş', 's').replace('ü', 'u')
    
    # Try multiple sources
    sources = [
        f"https://logo.clearbit.com/{clean_name}.com",
        f"https://img.icons8.com/color/96/{clean_name}-fc.png",
        f"https://www.thesportsdb.com/images/media/team/badge/{clean_name}.png"
    ]
    
    return sources

def download_logo(club_name, index):
    """Download logo for a club"""
    clean_name = club_name.lower().replace(' ', '-').replace('ç', 'c').replace('ğ', 'g').replace('ı', 'i').replace('ö', 'o').replace('ş', 's').replace('ü', 'u')
    filename = f"{clean_name}.png"
    filepath = logos_dir / filename
    
    # Skip if already exists
    if filepath.exists():
        print(f"✓ {club_name} - already exists")
        return True
    
    # Try to download from sources
    urls = get_logo_url(club_name)
    
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200 and len(response.content) > 1000:  # Valid image
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"✓ {club_name} - downloaded from {url}")
                return True
        except Exception as e:
            continue
    
    print(f"✗ {club_name} - no logo found")
    return False

# Download logos
print("\nDownloading logos...")
print("=" * 50)

success_count = 0
failed_clubs = []

for i, club in enumerate(clubs, 1):
    print(f"\n[{i}/{len(clubs)}] {club}")
    if download_logo(club, i):
        success_count += 1
    else:
        failed_clubs.append(club)
    
    # Rate limiting
    time.sleep(0.5)

print("\n" + "=" * 50)
print(f"\nDownload Summary:")
print(f"✓ Success: {success_count}/{len(clubs)}")
print(f"✗ Failed: {len(failed_clubs)}")

if failed_clubs:
    print(f"\nFailed clubs:")
    for club in failed_clubs:
        print(f"  - {club}")
    
    print(f"\nCreating list of failed clubs for manual download...")
    with open('logos-to-download-manually.txt', 'w', encoding='utf-8') as f:
        f.write("Clubs that need manual logo download:\n")
        f.write("=" * 50 + "\n\n")
        for club in failed_clubs:
            clean_name = club.lower().replace(' ', '-').replace('ç', 'c').replace('ğ', 'g').replace('ı', 'i').replace('ö', 'o').replace('ş', 's').replace('ü', 'u')
            f.write(f"{club}\n")
            f.write(f"  Filename: {clean_name}.png\n")
            f.write(f"  Search: '{club} logo png'\n\n")

print("\nDone!")
