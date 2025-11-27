import os
import re
from pathlib import Path

# Read club-data-real.ts to get exact club names
with open('lib/club-data-real.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract club names
name_pattern = r"name: ['\"]([^'\"]+)['\"]"
club_names = re.findall(name_pattern, content)

print(f"Found {len(club_names)} clubs in club-data-real.ts")

# Create mapping from normalized name to actual name
logos_dir = Path('public/logos')

def normalize_name(name):
    """Normalize club name to match downloaded logo filenames"""
    return name.lower().replace(' ', '-').replace('.', '').replace('&', 'and').replace('ç', 'c').replace('ğ', 'g').replace('ı', 'i').replace('ö', 'o').replace('ş', 's').replace('ü', 'u')

# Check which logos exist and which need to be created/renamed
existing_logos = {f.stem: f for f in logos_dir.glob('*.png')}
print(f"\nExisting logos: {len(existing_logos)}")

missing = []
for club_name in club_names:
    normalized = normalize_name(club_name)
    
    # Check if logo exists with this exact name
    if normalized not in existing_logos:
        # Try to find a similar logo
        # Remove common suffixes like FC, CF, etc.
        base_name = club_name.replace(' FC', '').replace(' CF', '').replace(' SK', '').replace(' AS', '').replace(' SC', '').replace(' AC', '').replace(' SS', '').replace(' US', '').replace(' RC', '').replace(' RCD', '').replace(' CD', '').replace(' CA', '').replace(' FK', '').replace(' 1.', '').replace(' SV', '').replace(' TSG', '').replace(' VfL', '').replace(' VfB', '').strip()
        base_normalized = normalize_name(base_name)
        
        if base_normalized in existing_logos:
            # Copy the logo with the full name
            src = existing_logos[base_normalized]
            dst = logos_dir / f"{normalized}.png"
            if not dst.exists():
                import shutil
                shutil.copy(src, dst)
                print(f"✓ Copied: {base_normalized}.png → {normalized}.png")
        else:
            missing.append(club_name)
            print(f"✗ Missing: {club_name} (looking for {normalized}.png or {base_normalized}.png)")

print(f"\nMissing logos: {len(missing)}")
if missing:
    print("\nMissing clubs:")
    for club in missing:
        print(f"  - {club}")
