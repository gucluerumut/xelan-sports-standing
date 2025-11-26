#!/usr/bin/env python3
"""
Create JSON template for manual Twitter data entry
"""

import json

# Load handles
with open('twitter-scraper-input.json', 'r') as f:
    data = json.load(f)
    handles = data['twitterHandles']

# Create template
template = {
    "collected_at": "YYYY-MM-DD",
    "source": "manual_entry_from_screenshots",
    "total_profiles": len(handles),
    "data": []
}

# Add entry for each handle
for handle in handles:
    entry = {
        "handle": handle,
        "name": "",  # Fill in from screenshot
        "followers": 0,  # Fill in from screenshot
        "following": 0,  # Fill in from screenshot (optional)
        "verified": False,  # Fill in from screenshot (optional)
        "screenshot": f"twitter-screenshots/{handle}.png"
    }
    template["data"].append(entry)

# Save template
with open('twitter-manual-data-template.json', 'w', encoding='utf-8') as f:
    json.dump(template, f, indent=2, ensure_ascii=False)

print("="*70)
print("TWITTER MANUAL DATA TEMPLATE CREATED")
print("="*70)
print(f"\n✓ Template created: twitter-manual-data-template.json")
print(f"  Total profiles: {len(handles)}")
print("\nInstructions:")
print("  1. Open twitter-manual-data-template.json")
print("  2. For each profile, look at the screenshot in twitter-screenshots/")
print("  3. Fill in the follower count and other data")
print("  4. Save the file as twitter-follower-data.json")
print("\nExample entry:")
print("""
  {
    "handle": "ManCity",
    "name": "Manchester City",
    "followers": 15200000,
    "following": 234,
    "verified": true,
    "screenshot": "twitter-screenshots/ManCity.png"
  }
""")
