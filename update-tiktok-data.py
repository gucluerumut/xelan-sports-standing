#!/usr/bin/env python3
"""
Update club-data-real.ts with actual TikTok follower data
"""

import json
import re

# Load TikTok data
with open('tiktok-follower-data.json', 'r') as f:
    tiktok_data = json.load(f)

# Create username to data mapping
tiktok_map = {profile['username']: profile for profile in tiktok_data['data']}

print(f"Loaded {len(tiktok_map)} TikTok profiles")
print(f"\nSample data:")
for username in list(tiktok_map.keys())[:5]:
    profile = tiktok_map[username]
    print(f"  @{username}: {profile['follower_count']:,} followers")

# Read the TypeScript file
with open('lib/club-data-real.ts', 'r') as f:
    content = f.read()

# Track updates
updates = []
not_found = []

# Find all instagramUsername entries and update their tiktokFollowers
lines = content.split('\n')
updated_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # Look for instagramUsername
    instagram_match = re.search(r"instagramUsername:\s*['\"]([^'\"]+)['\"]", line)
    
    if instagram_match:
        instagram_username = instagram_match.group(1)
        
        # Find the corresponding TikTok username (usually same as Instagram)
        # Look ahead for tiktokFollowers line
        j = i + 1
        found_tiktok_line = False
        
        while j < len(lines) and j < i + 20:  # Look within next 20 lines
            if 'tiktokFollowers:' in lines[j]:
                # Check if we have data for this username
                if instagram_username in tiktok_map:
                    tiktok_profile = tiktok_map[instagram_username]
                    new_followers = tiktok_profile['follower_count']
                    
                    # Extract current value for comparison
                    current_match = re.search(r'tiktokFollowers:\s*(\d+)', lines[j])
                    current_value = int(current_match.group(1)) if current_match else 0
                    
                    # Update the line
                    lines[j] = re.sub(
                        r'tiktokFollowers:\s*\d+',
                        f'tiktokFollowers: {new_followers}',
                        lines[j]
                    )
                    
                    updates.append({
                        'username': instagram_username,
                        'old': current_value,
                        'new': new_followers,
                        'change': new_followers - current_value
                    })
                    
                    found_tiktok_line = True
                else:
                    not_found.append(instagram_username)
                
                break
            j += 1
    
    i += 1

# Write updated content
updated_content = '\n'.join(lines)

with open('lib/club-data-real.ts', 'w') as f:
    f.write(updated_content)

# Print summary
print(f"\n{'='*70}")
print("UPDATE SUMMARY")
print(f"{'='*70}")

print(f"\n✓ Updated {len(updates)} clubs with real TikTok data")

if updates:
    print(f"\nTop 10 changes:")
    sorted_updates = sorted(updates, key=lambda x: abs(x['change']), reverse=True)[:10]
    for update in sorted_updates:
        change_str = f"+{update['change']:,}" if update['change'] > 0 else f"{update['change']:,}"
        print(f"  @{update['username']:20s}: {update['old']:>12,} → {update['new']:>12,} ({change_str})")

if not_found:
    print(f"\n⚠ Could not find TikTok data for {len(not_found)} clubs:")
    print(f"  {', '.join(not_found[:10])}")
    if len(not_found) > 10:
        print(f"  ... and {len(not_found) - 10} more")

print(f"\n✓ File updated: lib/club-data-real.ts")
print(f"\nNext step: Review changes and commit")
