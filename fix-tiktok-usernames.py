#!/usr/bin/env python3
"""
Research and fix TikTok usernames for suspicious/missing accounts
Based on common patterns and official club social media
"""

import json

# Known corrections based on research
TIKTOK_USERNAME_CORRECTIONS = {
    # Missing accounts
    '1fcunion': 'fcunion1966',  # Union Berlin
    'fch1846': 'fc.heidenheim',  # Heidenheim
    
    # Major European clubs - likely wrong
    'bvb09': 'bvb',  # Borussia Dortmund
    'losclive': 'losc',  # Lille
    'besiktas': 'besiktas',  # Beşiktaş - might be correct but verify
    'officialasroma': 'asroma',  # AS Roma
    'atalantabc': 'atalantabc',  # Atalanta - might be correct
    'official_sslazio': 'official_sslazio',  # Lazio - might be correct
    'ol': 'ol',  # Lyon - might be correct (very short username)
    'hsv': 'hsv',  # Hamburg - might be correct
    'bolognafc1909': 'bolognafc',  # Bologna
    'eintrachtfrankfurt': 'eintracht',  # Frankfurt
    'fcaugsburg1907': 'fcaugsburg',  # Augsburg
    'olympiquedemarseille': 'om',  # Marseille
    'vfbstuttgart': 'vfb',  # Stuttgart
    'bayer04fussball': 'bayer04',  # Leverkusen
    'comofootball': 'como1907',  # Como
    'nffc': 'nottinghamforest',  # Nottingham Forest
    
    # Turkish clubs
    'crizesporas': 'rizespor',  # Rizespor
    'goztepe': 'goztepespor',  # Göztepe
    'antalyaspor': 'antalyaspor',  # Antalyaspor - might be correct
    'alanyaspor': 'alanyaspor',  # Alanyaspor - might be correct
    'kasimpasask': 'kasimpasask',  # Kasımpaşa - might be correct
    'eyupsporkulubu': 'eyupspor',  # Eyüpspor
    'genclerbirligi': 'genclerbirligi',  # Gençlerbirliği - might be correct
    'kocaelispor': 'kocaelispor',  # Kocaelispor - might be correct
    'gaziantepfk': 'gaziantepfk',  # Gaziantep - might be correct
    'kayserisporfk': 'kayserispor',  # Kayserispor
    'fatihkaragumruk': 'fatihkaragumruk',  # Fatih Karagümrük - might be correct
    
    # Other leagues
    'rcdmallorca': 'rcdmallorca',  # Mallorca - might be correct
    'ajauxerre': 'ajauxerre',  # Auxerre - might be correct
    'stadebrestois29': 'sb29',  # Brest
    'angers_sco': 'angerssco',  # Angers
}

# Priority clubs to fix (major clubs with very low followers)
PRIORITY_FIXES = [
    'bvb09',  # Dortmund - 2 followers
    'losclive',  # Lille - 2 followers
    'besiktas',  # Beşiktaş - 2,414 followers
    'officialasroma',  # Roma - 1,117 followers
    'olympiquedemarseille',  # Marseille - 21 followers
    'vfbstuttgart',  # Stuttgart - 20 followers
    'bayer04fussball',  # Leverkusen - 10 followers
    'nffc',  # Nottingham Forest - 3 followers
    'comofootball',  # Como - 6 followers
]

def create_retry_list():
    """Create a list of usernames to retry with corrections"""
    
    # Load current suspicious accounts
    with open('tiktok-follower-data.json', 'r') as f:
        current_data = json.load(f)
    
    suspicious_usernames = []
    for profile in current_data['data']:
        if profile['follower_count'] < 10000:
            suspicious_usernames.append(profile['username'])
    
    # Add missing accounts
    suspicious_usernames.extend(['1fcunion', 'fch1846'])
    
    # Create retry input with corrections
    retry_usernames = []
    corrections_applied = []
    no_correction_found = []
    
    for username in suspicious_usernames:
        if username in TIKTOK_USERNAME_CORRECTIONS:
            new_username = TIKTOK_USERNAME_CORRECTIONS[username]
            if new_username != username:
                retry_usernames.append(new_username)
                corrections_applied.append({
                    'old': username,
                    'new': new_username,
                    'priority': username in PRIORITY_FIXES
                })
            else:
                # Username might be correct, keep it
                retry_usernames.append(username)
                no_correction_found.append(username)
        else:
            # No correction known, keep original
            retry_usernames.append(username)
            no_correction_found.append(username)
    
    # Save retry input
    retry_input = {
        'usernames': retry_usernames
    }
    
    with open('tiktok-retry-input.json', 'w') as f:
        json.dump(retry_input, f, indent=2)
    
    # Create report
    print("="*80)
    print("TIKTOK USERNAME CORRECTIONS")
    print("="*80)
    print(f"\nTotal suspicious accounts: {len(suspicious_usernames)}")
    print(f"Corrections applied: {len(corrections_applied)}")
    print(f"No correction found: {len(no_correction_found)}")
    print()
    
    if corrections_applied:
        print("="*80)
        print("CORRECTIONS TO TRY")
        print("="*80)
        print()
        
        # Priority first
        priority_corrections = [c for c in corrections_applied if c['priority']]
        other_corrections = [c for c in corrections_applied if not c['priority']]
        
        if priority_corrections:
            print("🔴 PRIORITY (Major clubs):")
            for correction in priority_corrections:
                print(f"  {correction['old']:30s} → {correction['new']}")
            print()
        
        if other_corrections:
            print("⚪ OTHER:")
            for correction in other_corrections:
                print(f"  {correction['old']:30s} → {correction['new']}")
            print()
    
    if no_correction_found:
        print("="*80)
        print("⚠️  NO CORRECTION FOUND (Need manual research)")
        print("="*80)
        print()
        for username in sorted(no_correction_found):
            print(f"  • @{username}")
        print()
    
    print("="*80)
    print("NEXT STEPS")
    print("="*80)
    print()
    print("1. Review corrections in tiktok-retry-input.json")
    print("2. Run: python3 collect-tiktok-retry.py")
    print("3. Check results and identify remaining issues")
    print("4. Manually collect data for accounts that still fail")
    print()
    
    # Save corrections report
    report = {
        'total_suspicious': len(suspicious_usernames),
        'corrections_applied': corrections_applied,
        'no_correction_found': no_correction_found,
        'retry_usernames': retry_usernames
    }
    
    with open('tiktok-corrections-report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("✅ Files created:")
    print("   - tiktok-retry-input.json (input for retry)")
    print("   - tiktok-corrections-report.json (detailed report)")

if __name__ == "__main__":
    create_retry_list()
