#!/usr/bin/env python3
"""
Improved OCR extraction with validation and suspicious data flagging
"""

import json
import re
from pathlib import Path
from PIL import Image
import pytesseract

# Set tesseract path
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def extract_follower_count_from_image(image_path: Path) -> dict:
    """Extract follower count with improved parsing"""
    try:
        # Read image
        img = Image.open(image_path)
        
        # Extract text
        text = pytesseract.image_to_string(img)
        
        # Look for patterns
        patterns = [
            r'([\d,.]+[KMB]?)\s*Followers?',
            r'Followers?\s*([\d,.]+[KMB]?)',
            r'([\d,.]+\s*[KMB]?n?)\s*Takip[çc]i',
            r'Takip[çc]i\s*([\d,.]+\s*[KMB]?n?)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                count_str = matches[0]
                follower_count = parse_count_improved(count_str)
                if follower_count:
                    return {
                        'success': True,
                        'followers': follower_count,
                        'raw_text': count_str,
                        'detected_text': text[:200]
                    }
        
        return {
            'success': False,
            'error': 'No follower count found',
            'detected_text': text[:200]
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def parse_count_improved(text: str) -> int:
    """Improved number parsing with K/M/B support"""
    try:
        original = text.strip().upper()
        
        # Handle Turkish 'Mn' (Milyon) and 'Bn' (Bin = thousand)
        text = original.replace('MN', 'M').replace('BN', 'K')
        
        # Detect multiplier BEFORE cleaning
        multiplier = 1
        if 'B' in text:
            # B can mean Billion or Turkish Bin (thousand)
            # If number is small (< 1000), likely Bin, else Billion
            multiplier = 1000000000
            text = text.replace('B', '')
        elif 'M' in text:
            multiplier = 1000000
            text = text.replace('M', '')
        elif 'K' in text:
            multiplier = 1000
            text = text.replace('K', '')
        
        # Clean the number - remove all non-numeric except . and ,
        text = re.sub(r'[^\d.,]', '', text)
        
        if not text:
            return None
        
        # Handle decimal separators
        # Strategy: if we have both . and ,, determine which is decimal
        if '.' in text and ',' in text:
            # Find which comes last - that's likely the decimal separator
            last_dot = text.rfind('.')
            last_comma = text.rfind(',')
            
            if last_comma > last_dot:
                # European: 1.234,5 -> remove dots, replace comma
                text = text.replace('.', '').replace(',', '.')
            else:
                # US: 1,234.5 -> remove commas
                text = text.replace(',', '')
        elif ',' in text:
            # Only commas
            parts = text.split(',')
            if len(parts) == 2 and len(parts[1]) <= 2:
                # Decimal: 1,5 or 500,4 -> 1.5 or 500.4
                text = text.replace(',', '.')
            else:
                # Thousands: 1,234 or 1,234,567 -> 1234 or 1234567
                text = text.replace(',', '')
        elif '.' in text:
            # Only dots
            parts = text.split('.')
            if len(parts) == 2 and len(parts[1]) <= 2:
                # Decimal: 1.5 or 500.4 -> keep as is
                pass
            else:
                # Thousands: 1.234.567 -> 1234567
                text = text.replace('.', '')
        
        if not text:
            return None
            
        number = float(text)
        result = int(number * multiplier)
        
        # Relaxed validation: allow 100 to 500M
        # Some clubs might have very few followers, some might be huge
        if result < 100:
            return None
        
        # Cap at 500M (no club has more than this)
        if result > 500_000_000:
            return None
            
        return result
        
    except Exception as e:
        return None

def is_suspicious(followers: int, handle: str) -> tuple[bool, str]:
    """Check if follower count seems suspicious"""
    
    # Known big clubs (should have >5M)
    big_clubs = [
        'realmadrid', 'FCBarcelona', 'ManUtd', 'ManCity', 'LFC', 'Arsenal',
        'ChelseaFC', 'juventusfc', 'acmilan', 'Inter', 'FCBayern', 'BVB',
        'PSG_inside', 'Atleti', 'SpursOfficial'
    ]
    
    # Known medium clubs (should have 500K-5M)
    medium_clubs = [
        'Wolves', 'Everton', 'NUFC', 'WestHam', 'AVFCOfficial',
        'sscnapoli', 'OfficialASRoma', 'Atalanta_BC'
    ]
    
    if handle in big_clubs:
        if followers < 5_000_000:
            return True, f"Big club with only {followers:,} followers"
        if followers > 100_000_000:
            return True, f"Unrealistically high: {followers:,}"
    
    if handle in medium_clubs:
        if followers < 500_000:
            return True, f"Medium club with only {followers:,} followers"
    
    # General validation
    if followers > 100_000_000:
        return True, f"Unrealistically high: {followers:,}"
    
    if followers < 10_000:
        return True, f"Very low for a football club: {followers:,}"
    
    return False, ""

def extract_all_followers_improved():
    """Extract with validation and flagging"""
    print("="*70)
    print("TWITTER FOLLOWER EXTRACTION (Improved OCR)")
    print("="*70)
    
    screenshot_dir = Path('twitter-screenshots')
    screenshots = sorted(screenshot_dir.glob('*.png'))
    
    print(f"\n→ Found {len(screenshots)} screenshots")
    print(f"→ Starting extraction...\n")
    
    results = []
    suspicious = []
    failed = []
    
    for i, screenshot in enumerate(screenshots, 1):
        handle = screenshot.stem
        print(f"[{i}/{len(screenshots)}] @{handle}...", end=" ", flush=True)
        
        result = extract_follower_count_from_image(screenshot)
        
        if result['success']:
            followers = result['followers']
            is_susp, reason = is_suspicious(followers, handle)
            
            if is_susp:
                print(f"⚠️  {followers:,} - SUSPICIOUS: {reason}")
                suspicious.append({
                    'handle': handle,
                    'followers': followers,
                    'reason': reason,
                    'raw_text': result['raw_text'],
                    'screenshot': str(screenshot)
                })
            else:
                print(f"✓ {followers:,}")
                results.append({
                    'handle': handle,
                    'name': '',
                    'followers': followers,
                    'following': 0,
                    'verified': False,
                    'screenshot': str(screenshot)
                })
        else:
            print(f"✗ {result.get('error', 'Failed')}")
            failed.append(handle)
    
    # Save results
    output = {
        'collected_at': '2025-11-24',
        'source': 'improved_ocr',
        'total_profiles': len(screenshots),
        'successful': len(results),
        'suspicious': len(suspicious),
        'failed': len(failed),
        'data': results,
        'suspicious_data': suspicious,
        'failed_handles': failed
    }
    
    with open('twitter-follower-data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n\n{'='*70}")
    print("EXTRACTION COMPLETE")
    print(f"{'='*70}")
    print(f"✅ Successful: {len(results)}/{len(screenshots)}")
    print(f"⚠️  Suspicious: {len(suspicious)} (need manual review)")
    print(f"❌ Failed: {len(failed)}")
    
    if results:
        print(f"\n✓ Data saved to: twitter-follower-data.json")
        print(f"\nTop 10 (validated):")
        top_10 = sorted(results, key=lambda x: x['followers'], reverse=True)[:10]
        for j, profile in enumerate(top_10, 1):
            print(f"  {j:2d}. @{profile['handle']:20s} {profile['followers']:>12,}")
    
    if suspicious:
        print(f"\n⚠️  SUSPICIOUS DATA (need manual review):")
        for item in suspicious[:10]:
            print(f"  @{item['handle']:20s} {item['followers']:>12,} - {item['reason']}")
        if len(suspicious) > 10:
            print(f"  ... and {len(suspicious) - 10} more")
    
    if failed:
        print(f"\n❌ FAILED ({len(failed)} profiles need manual entry)")
    
    print(f"\n📝 Next steps:")
    print(f"  1. Review suspicious data in twitter-follower-data.json")
    print(f"  2. Manually correct {len(suspicious) + len(failed)} profiles")
    print(f"  3. Merge with validated data")
    
    return output

if __name__ == "__main__":
    try:
        result = extract_all_followers_improved()
        print("\n✅ Extraction complete!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
