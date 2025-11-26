#!/usr/bin/env python3
"""
Clean up all English account screenshots
"""

from pathlib import Path

# All English handles that were replaced
ENGLISH_HANDLES = [
    # German clubs
    'FCBayernEN', 'bayer04_en', 'RBLeipzig_EN', 'eintracht_eng',
    'borussia_en', 'VfB_int', 'scfreiburg_en', 'werderbremen_en',
    'achtzehn99_en', 'fcstpauli_EN', 'Mainz05en', 'FCA_World',
    'fcunion_en', 'FCH1846_en', 'HSV_English', 'fckoeln_en',
    
    # French clubs
    'PSG_English', 'OM_English', 'AS_Monaco_EN', 'OL_English',
    'LOSC_EN', 'ogcnice_eng', 'FCNantesEN', 'RCSA_Eng', 'staderennais_en'
]

screenshot_dir = Path('twitter-screenshots')

print("="*70)
print("CLEANING UP ALL ENGLISH ACCOUNT SCREENSHOTS")
print("="*70)

deleted = []
for handle in ENGLISH_HANDLES:
    screenshot_path = screenshot_dir / f"{handle}.png"
    if screenshot_path.exists():
        screenshot_path.unlink()
        deleted.append(handle)
        print(f"✓ Deleted: {handle}.png")

print(f"\n✓ Deleted {len(deleted)} English account screenshots")

# Check remaining
existing = list(screenshot_dir.glob('*.png'))
print(f"✓ Remaining screenshots: {len(existing)}")

# Load total
import json
with open('twitter-scraper-input.json', 'r') as f:
    data = json.load(f)
    total = len(data['twitterHandles'])

print(f"✓ Total needed: {total}")
print(f"✓ Still need: {total - len(existing)} screenshots")
