import requests
from pathlib import Path

logos_dir = Path('public/logos')

manual_fixes = {
    "hatayspor": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5f/Hatayspor_logo.svg/200px-Hatayspor_logo.svg.png",
    "bodrum-fk": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4e/Bodrum_FK_logo.svg/200px-Bodrum_FK_logo.svg.png",
    "angers": "https://upload.wikimedia.org/wikipedia/en/thumb/3/30/Angers_SCO_logo.svg/200px-Angers_SCO_logo.svg.png"
}

print("Fixing remaining logos...")

for name, url in manual_fixes.items():
    filepath = logos_dir / f"{name}.png"
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(r.content)
            print(f"✓ {name} - fixed manually")
    except Exception as e:
        print(f"✗ {name} - failed: {e}")

# Verify count
files = list(logos_dir.glob('*.png'))
print(f"\nTotal logos: {len(files)}")
