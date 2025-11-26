#!/usr/bin/env python3
"""
Update social media mapping with manual TikTok data
"""

import json

# Load existing mapping
with open('social-media-username-map.json', 'r') as f:
    mapping = json.load(f)

# Manual TikTok corrections from user
MANUAL_TIKTOK_UPDATES = {
    # Büyük Kulüpler
    'besiktas': 'besiktasjk',  # 1.3M
    'atalantabc': 'atalanta_be',  # 1.2M
    'sslazio': 'sslazio',  # 335.6K
    '1_fc_heidenheim': 'fch_achtzehn_46',  # 90.8K
    'ol': 'ol_officiel',  # 2.3M
    'hsv': 'hsv_official',  # 1.3M
    'nffc': 'officialnffc',  # 1.7M
    'como1907': 'comofootball1907',  # 423.9K
    
    # Türk Kulüpleri
    'rizespor': 'crizesporas',  # 3.8K
    'kayserispor': 'kysrtv',  # 3.3K
    'kasimpasask': None,  # Resmi hesap yok
    'genclerbirligi': 'genclerbirligisk',  # 8.7K
    'antalyaspor': None,  # Resmi hesap yok
    'kocaelispor': None,  # Resmi hesap yok
    'gaziantepfk': None,  # Resmi hesap yok
    'fatihkaragumruk': None,  # Resmi hesap yok
    'goztepe': 'goztepesporkulubu',  # 7.7K
    'eyupspor': 'ikaseyupspor',  # 24.9K
    'alanyaspor': None,  # Resmi hesap yok
    
    # Diğer
    'sb29': 'stadebrestois',  # 532.5K
    'rcdmallorca': 'realmallorcaoficial',  # 6.9M
    'ajauxerre': 'ajauxerre.officiel',  # 158.1K
    
    # Eksikler
    'bolognafc1909': 'bolobolognafootballclub',  # 615.4K
    '1_fc_union_berlin': 'fcunion',  # 165.1K
}

# Update mapping
updated_count = 0
for instagram_username, tiktok_username in MANUAL_TIKTOK_UPDATES.items():
    if instagram_username in mapping:
        mapping[instagram_username]['tiktok'] = tiktok_username
        updated_count += 1
        print(f"✓ Updated {instagram_username}: TikTok = {tiktok_username}")
    else:
        print(f"⚠️  {instagram_username} not found in mapping")

# Save updated mapping
with open('social-media-username-map.json', 'w') as f:
    json.dump(mapping, f, indent=2)

print(f"\n✅ Updated {updated_count} TikTok usernames")
print(f"✓ Saved to social-media-username-map.json")

# Show statistics
total_clubs = len(mapping)
with_tiktok = sum(1 for m in mapping.values() if m.get('tiktok'))
with_twitter = sum(1 for m in mapping.values() if m.get('twitter'))

print(f"\nFinal statistics:")
print(f"  Total clubs: {total_clubs}")
print(f"  With TikTok: {with_tiktok} ({with_tiktok/total_clubs*100:.1f}%)")
print(f"  With Twitter: {with_twitter} ({with_twitter/total_clubs*100:.1f}%)")
