#!/usr/bin/env python3
"""
Extract social media usernames and create mapping for club-data-real.ts update
"""

import json
from pathlib import Path

def load_tiktok_data():
    """Load TikTok follower data"""
    with open('tiktok-follower-data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create mapping: username -> follower_count
    tiktok_map = {}
    for profile in data.get('data', []):
        username = profile.get('username') or profile.get('unique_id')
        if username:
            tiktok_map[username.lower()] = {
                'username': username,
                'followers': profile.get('follower_count', 0)
            }
    
    return tiktok_map

def load_twitter_handles():
    """Load Twitter handles from input file"""
    with open('twitter-scraper-input.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data.get('twitterHandles', [])

def load_instagram_data():
    """Load Instagram data to help with mapping"""
    instagram_file = Path('/Users/umutgucluer/Downloads/dataset_instagram-profile-scraper_2025-11-23_05-15-59-181.json')
    
    if instagram_file.exists():
        with open(instagram_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Create mapping: username -> data
        instagram_map = {}
        for profile in data:
            username = profile.get('username')
            if username:
                instagram_map[username.lower()] = {
                    'username': username,
                    'full_name': profile.get('full_name', ''),
                    'followers': profile.get('followersCount', 0)
                }
        
        return instagram_map
    
    return {}

def create_social_media_mapping():
    """Create comprehensive social media mapping"""
    
    print("="*70)
    print("SOCIAL MEDIA USERNAME MAPPING")
    print("="*70)
    
    tiktok_map = load_tiktok_data()
    twitter_handles = load_twitter_handles()
    instagram_map = load_instagram_data()
    
    print(f"\n✓ Loaded {len(tiktok_map)} TikTok profiles")
    print(f"✓ Loaded {len(twitter_handles)} Twitter handles")
    print(f"✓ Loaded {len(instagram_map)} Instagram profiles")
    
    # Create mapping by club name patterns
    # This will need manual verification but gives us a starting point
    
    mapping = {
        # Premier League
        'Manchester City': {'instagram': 'mancity', 'tiktok': 'mancity', 'twitter': 'ManCity'},
        'Arsenal': {'instagram': 'arsenal', 'tiktok': 'arsenal', 'twitter': 'Arsenal'},
        'Liverpool FC': {'instagram': 'liverpoolfc', 'tiktok': 'liverpoolfc', 'twitter': 'LFC'},
        'Manchester United': {'instagram': 'manchesterunited', 'tiktok': 'manutd', 'twitter': 'ManUtd'},
        'Chelsea FC': {'instagram': 'chelseafc', 'tiktok': 'chelseafc', 'twitter': 'ChelseaFC'},
        'Tottenham': {'instagram': 'spursofficial', 'tiktok': 'spursofficial', 'twitter': 'SpursOfficial'},
        'Newcastle United': {'instagram': 'nufc', 'tiktok': 'nufc', 'twitter': 'NUFC'},
        'Aston Villa': {'instagram': 'avfcofficial', 'tiktok': 'avfcofficial', 'twitter': 'AVFCOfficial'},
        'Brighton': {'instagram': 'officialbhafc', 'tiktok': 'officialbhafc', 'twitter': 'OfficialBHAFC'},
        'Wolves': {'instagram': 'wolves', 'tiktok': 'wolves', 'twitter': 'Wolves'},
        'West Ham': {'instagram': 'westham', 'tiktok': 'westham', 'twitter': 'WestHam'},
        'Crystal Palace': {'instagram': 'cpfc', 'tiktok': 'cpfc', 'twitter': 'CPFC'},
        'Fulham': {'instagram': 'fulhamfc', 'tiktok': 'fulhamfc', 'twitter': 'FulhamFC'},
        'Everton': {'instagram': 'everton', 'tiktok': 'everton', 'twitter': 'Everton'},
        'Brentford': {'instagram': 'brentfordfc', 'tiktok': 'brentfordfc', 'twitter': 'BrentfordFC'},
        'Nottingham Forest': {'instagram': 'nffc', 'tiktok': None, 'twitter': 'NFFC'},  # No TikTok
        'Bournemouth': {'instagram': 'afcbournemouth', 'tiktok': 'afcbournemouth', 'twitter': 'afcbournemouth'},
        
        # Add more leagues...
        # This is a starting template
    }
    
    # Save mapping
    with open('social-media-mapping.json', 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Created mapping for {len(mapping)} clubs")
    print(f"✓ Saved to: social-media-mapping.json")
    
    # Show sample
    print(f"\nSample mapping:")
    for club_name, handles in list(mapping.items())[:5]:
        print(f"\n{club_name}:")
        print(f"  Instagram: @{handles['instagram']}")
        print(f"  TikTok: @{handles['tiktok'] if handles['tiktok'] else 'N/A'}")
        print(f"  Twitter: @{handles['twitter']}")
    
    return mapping

if __name__ == "__main__":
    mapping = create_social_media_mapping()
    
    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    print("\n1. Review social-media-mapping.json")
    print("2. Add missing clubs and verify usernames")
    print("3. Run update script to add to club-data-real.ts")
