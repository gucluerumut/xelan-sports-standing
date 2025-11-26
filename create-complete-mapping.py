#!/usr/bin/env python3
"""
Create complete social media mapping for all clubs by matching Instagram usernames
"""

import json
import re

def normalize_name(name):
    """Normalize club name for matching"""
    return re.sub(r'[^a-z0-9]', '', name.lower())

def load_club_data():
    """Load club data from TypeScript file"""
    with open('lib/club-data-real.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract club names and Instagram usernames
    clubs = []
    lines = content.split('\n')
    
    current_club = {}
    for i, line in enumerate(lines):
        if 'name:' in line and "'" in line:
            name = line.split("'")[1]
            current_club['name'] = name
        elif 'instagramUsername:' in line and "'" in line:
            username = line.split("'")[1]
            current_club['instagram'] = username
            clubs.append(current_club.copy())
            current_club = {}
    
    return clubs

def load_tiktok_data():
    """Load TikTok data"""
    with open('tiktok-follower-data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    tiktok_map = {}
    for profile in data.get('data', []):
        username = (profile.get('username') or profile.get('unique_id', '')).lower()
        if username:
            tiktok_map[username] = profile.get('username') or profile.get('unique_id')
    
    return tiktok_map

def load_twitter_handles():
    """Load Twitter handles"""
    with open('twitter-scraper-input.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data.get('twitterHandles', [])

def create_complete_mapping():
    """Create complete mapping"""
    
    print("="*70)
    print("CREATING COMPLETE SOCIAL MEDIA MAPPING")
    print("="*70)
    
    clubs = load_club_data()
    tiktok_map = load_tiktok_data()
    twitter_handles = load_twitter_handles()
    
    print(f"\n✓ Found {len(clubs)} clubs in club-data-real.ts")
    print(f"✓ Loaded {len(tiktok_map)} TikTok profiles")
    print(f"✓ Loaded {len(twitter_handles)} Twitter handles")
    
    # Try to match TikTok and Twitter to clubs
    mapping = []
    
    for i, club in enumerate(clubs):
        club_name = club['name']
        instagram = club['instagram']
        
        # Try to find TikTok - often same as Instagram
        tiktok = None
        if instagram.lower() in tiktok_map:
            tiktok = tiktok_map[instagram.lower()]
        
        # Try to find Twitter - use index from twitter handles list
        twitter = None
        if i < len(twitter_handles):
            twitter = twitter_handles[i]
        
        mapping.append({
            'name': club_name,
            'instagram': instagram,
            'tiktok': tiktok,
            'twitter': twitter
        })
    
    # Save mapping
    with open('complete-social-media-mapping.json', 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Created mapping for {len(mapping)} clubs")
    print(f"✓ Saved to: complete-social-media-mapping.json")
    
    # Statistics
    with_tiktok = sum(1 for m in mapping if m['tiktok'])
    with_twitter = sum(1 for m in mapping if m['twitter'])
    
    print(f"\nStatistics:")
    print(f"  Instagram: {len(mapping)}/113 (100%)")
    print(f"  TikTok: {with_tiktok}/113 ({with_tiktok/len(mapping)*100:.1f}%)")
    print(f"  Twitter: {with_twitter}/113 ({with_twitter/len(mapping)*100:.1f}%)")
    
    # Show samples
    print(f"\nSample mappings:")
    for club in mapping[:10]:
        print(f"\n{club['name']}:")
        print(f"  Instagram: @{club['instagram']}")
        print(f"  TikTok: @{club['tiktok'] if club['tiktok'] else 'N/A'}")
        print(f"  Twitter: @{club['twitter'] if club['twitter'] else 'N/A'}")
    
    return mapping

if __name__ == "__main__":
    mapping = create_complete_mapping()
