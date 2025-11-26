#!/usr/bin/env python3
"""
Apply social media usernames to club-data-real.ts
"""

import json
import re

# Load mapping
with open('social-media-username-map.json', 'r') as f:
    mapping = json.load(f)

# Read club-data-real.ts
with open('lib/club-data-real.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Function to add social media usernames after instagramUsername
def add_social_media_usernames(match):
    indent = match.group(1)
    instagram_username = match.group(2)
    
    # Look up in mapping
    social = mapping.get(instagram_username, {})
    tiktok = social.get('tiktok')
    twitter = social.get('twitter')
    
    # Build replacement
    result = f"{indent}instagramUsername: '{instagram_username}',\n"
    
    if tiktok:
        result += f"{indent}tiktokUsername: '{tiktok}',\n"
    
    if twitter:
        result += f"{indent}twitterUsername: '{twitter}',\n"
    
    return result

# Pattern to match instagramUsername lines
pattern = r"(\s+)instagramUsername: '([^']+)',\n"

# Replace all occurrences
new_content = re.sub(pattern, add_social_media_usernames, content)

# Write back
with open('lib/club-data-real.ts', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("="*70)
print("SOCIAL MEDIA USERNAMES APPLIED")
print("="*70)

# Count updates
tiktok_added = new_content.count('tiktokUsername')
twitter_added = new_content.count('twitterUsername')

print(f"\n✅ Updated club-data-real.ts")
print(f"   TikTok usernames added: {tiktok_added}")
print(f"   Twitter usernames added: {twitter_added}")
print(f"\n✓ All social media links ready!")
