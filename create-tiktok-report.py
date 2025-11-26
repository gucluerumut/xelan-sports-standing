#!/usr/bin/env python3
"""
Create a comprehensive report of TikTok data collection
Shows which clubs were updated and which need manual data collection
"""

import json

# Load TikTok data
with open('tiktok-follower-data.json', 'r') as f:
    tiktok_data = json.load(f)

# Load TikTok input (requested usernames)
with open('tiktok-scraper-input.json', 'r') as f:
    tiktok_input = json.load(f)

# Load club data to get club names
with open('lib/club-data-real.ts', 'r') as f:
    club_data_content = f.read()

# Create mapping of collected data
collected_usernames = {profile['username'] for profile in tiktok_data['data']}
requested_usernames = set(tiktok_input['usernames'])

# Find missing
missing_usernames = requested_usernames - collected_usernames

# Create report
report = []
report.append("="*80)
report.append("TIKTOK DATA COLLECTION REPORT")
report.append("="*80)
report.append("")
report.append(f"Total Requested: {len(requested_usernames)}")
report.append(f"Successfully Collected: {len(collected_usernames)}")
report.append(f"Missing/Failed: {len(missing_usernames)}")
report.append("")

# Section 1: Successfully Collected (sorted by followers)
report.append("="*80)
report.append("✅ SUCCESSFULLY COLLECTED ({} clubs)".format(len(collected_usernames)))
report.append("="*80)
report.append("")

sorted_profiles = sorted(tiktok_data['data'], key=lambda x: x['follower_count'], reverse=True)

for i, profile in enumerate(sorted_profiles, 1):
    followers = profile['follower_count']
    following = profile['following_count']
    nickname = profile.get('nickname', '')
    
    report.append(f"{i:3d}. @{profile['username']:25s} | {followers:>12,} followers | {nickname}")

report.append("")

# Section 2: Missing/Failed
if missing_usernames:
    report.append("="*80)
    report.append("❌ MISSING/FAILED ({} clubs)".format(len(missing_usernames)))
    report.append("="*80)
    report.append("")
    report.append("These clubs need manual data collection:")
    report.append("")
    
    for username in sorted(missing_usernames):
        report.append(f"  • @{username}")
    
    report.append("")
    report.append("Manual Data Collection Template:")
    report.append("-" * 80)
    report.append("")
    
    # Create template for manual data entry
    template = []
    template.append("[")
    for i, username in enumerate(sorted(missing_usernames)):
        comma = "," if i < len(missing_usernames) - 1 else ""
        template.append("  {")
        template.append(f'    "username": "{username}",')
        template.append('    "nickname": "",')
        template.append('    "follower_count": 0,')
        template.append('    "following_count": 0,')
        template.append('    "video_count": 0,')
        template.append('    "likes_count": 0,')
        template.append('    "verified": false,')
        template.append('    "bio": "",')
        template.append('    "bio_url": ""')
        template.append(f"  }}{comma}")
    template.append("]")
    
    # Save template to separate file
    with open('tiktok-manual-data-template.json', 'w') as f:
        f.write('\n'.join(template))
    
    report.append("Template saved to: tiktok-manual-data-template.json")
    report.append("")

# Section 3: Top Performers
report.append("="*80)
report.append("🏆 TOP 20 BY FOLLOWERS")
report.append("="*80)
report.append("")

for i, profile in enumerate(sorted_profiles[:20], 1):
    followers = profile['follower_count']
    nickname = profile.get('nickname', '')
    report.append(f"{i:2d}. {nickname:30s} @{profile['username']:20s} {followers:>12,}")

report.append("")

# Section 4: Statistics by League (if we can infer)
report.append("="*80)
report.append("📊 STATISTICS")
report.append("="*80)
report.append("")

total_followers = sum(p['follower_count'] for p in tiktok_data['data'])
avg_followers = total_followers / len(tiktok_data['data'])
median_idx = len(sorted_profiles) // 2
median_followers = sorted_profiles[median_idx]['follower_count']

report.append(f"Total Followers: {total_followers:,}")
report.append(f"Average Followers: {avg_followers:,.0f}")
report.append(f"Median Followers: {median_followers:,}")
report.append(f"Highest: {sorted_profiles[0]['follower_count']:,} (@{sorted_profiles[0]['username']})")
report.append(f"Lowest: {sorted_profiles[-1]['follower_count']:,} (@{sorted_profiles[-1]['username']})")
report.append("")

# Save report
report_text = '\n'.join(report)

with open('TIKTOK_COLLECTION_REPORT.txt', 'w', encoding='utf-8') as f:
    f.write(report_text)

print(report_text)
print("\n" + "="*80)
print("✅ Report saved to: TIKTOK_COLLECTION_REPORT.txt")
print("✅ Manual template saved to: tiktok-manual-data-template.json")
print("="*80)
