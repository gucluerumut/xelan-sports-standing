#!/usr/bin/env python3
"""
Identify suspicious TikTok accounts that likely need correction
"""

import json

# Load TikTok data
with open('tiktok-follower-data.json', 'r') as f:
    tiktok_data = json.load(f)

# Threshold for suspicious accounts (less than 10,000 followers is suspicious for major clubs)
SUSPICIOUS_THRESHOLD = 10000

suspicious = []
for profile in tiktok_data['data']:
    if profile['follower_count'] < SUSPICIOUS_THRESHOLD:
        suspicious.append(profile)

# Sort by follower count
suspicious.sort(key=lambda x: x['follower_count'])

print("="*80)
print(f"⚠️  SUSPICIOUS TIKTOK ACCOUNTS (< {SUSPICIOUS_THRESHOLD:,} followers)")
print("="*80)
print(f"\nFound {len(suspicious)} accounts that may be incorrect:\n")

for profile in suspicious:
    followers = profile['follower_count']
    nickname = profile.get('nickname', 'N/A')
    username = profile['username']
    
    print(f"@{username:30s} | {followers:>8,} followers | {nickname}")

print("\n" + "="*80)
print("RECOMMENDATIONS")
print("="*80)
print("\nThese accounts likely need manual verification:")
print("1. Check if the TikTok username matches the club's official account")
print("2. Search for the club name on TikTok to find the correct account")
print("3. Update tiktok-scraper-input.json with correct usernames")
print("\nMajor clubs that look suspicious:")

# Highlight major clubs
major_clubs = [
    'besiktas', 'officialasroma', 'atalantabc', 'official_sslazio', 'ol',
    'hsv', 'bolognafc1909', 'eintrachtfrankfurt', 'fcaugsburg1907',
    'olympiquedemarseille', 'vfbstuttgart', 'bayer04fussball', 'bvb09',
    'losclive', 'comofootball', 'nffc'
]

print("\n" + "-"*80)
for username in major_clubs:
    matching = [p for p in suspicious if p['username'] == username]
    if matching:
        p = matching[0]
        print(f"  • @{p['username']:25s} - Only {p['follower_count']:,} followers (likely wrong account)")

print("\n" + "="*80)
print("NEXT STEPS")
print("="*80)
print("\n1. Create a list of correct TikTok usernames for these clubs")
print("2. Update tiktok-scraper-input.json")
print("3. Re-run: python3 collect-tiktok-data.py")
print("4. Update site: python3 update-tiktok-data.py")
