#!/usr/bin/env python3
"""
Update remaining TikTok follower counts - complete update
"""

import re

# Complete manual TikTok follower data
MANUAL_TIKTOK_FOLLOWERS = {
    # Previously updated
    'besiktas': 1_300_000,
    'atalantabc': 1_200_000,
    'sslazio': 335_600,
    '1_fc_heidenheim': 90_800,
    'ol': 2_300_000,
    'hsv': 1_300_000,
    'nffc': 1_700_000,
    'como1907': 423_900,
    'rizespor': 3_800,
    'kayserispor': 3_300,
    'genclerbirligi': 8_700,
    'goztepe': 7_700,
    'eyupspor': 24_900,
    'sb29': 532_500,
    'rcdmallorca': 6_900_000,
    'ajauxerre': 158_100,
    'bolognafc1909': 615_400,
    '1_fc_union_berlin': 165_100,
}

# Read file
with open('lib/club-data-real.ts', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Process line by line
updated_count = 0
for i, line in enumerate(lines):
    # Check if this line has instagramUsername
    if 'instagramUsername:' in line:
        # Extract username
        match = re.search(r"instagramUsername: '([^']+)'", line)
        if match:
            instagram_username = match.group(1)
            
            # Check if we have manual data for this club
            if instagram_username in MANUAL_TIKTOK_FOLLOWERS:
                new_followers = MANUAL_TIKTOK_FOLLOWERS[instagram_username]
                
                # Find the tiktokFollowers line (should be within next 10 lines)
                for j in range(i, min(i+15, len(lines))):
                    if 'tiktokFollowers:' in lines[j]:
                        # Update the line
                        old_line = lines[j]
                        lines[j] = re.sub(
                            r'tiktokFollowers: \d+',
                            f'tiktokFollowers: {new_followers}',
                            lines[j]
                        )
                        if lines[j] != old_line:
                            updated_count += 1
                            print(f"✓ Updated {instagram_username}: {new_followers:,} followers")
                        break

# Write back
with open('lib/club-data-real.ts', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"\n✅ Updated {updated_count} TikTok follower counts")
print(f"✓ Saved to club-data-real.ts")
