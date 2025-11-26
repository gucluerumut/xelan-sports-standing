#!/usr/bin/env python3
"""
Extract follower counts from Twitter screenshots using EasyOCR
Works without Tesseract - pure Python solution
"""

import json
import re
from pathlib import Path
import easyocr

# Initialize EasyOCR reader (English and Turkish)
print("Initializing EasyOCR (this may take a moment on first run)...")
reader = easyocr.Reader(['en', 'tr'], gpu=False)
print("✓ EasyOCR ready\n")

def extract_follower_count_from_image(image_path: Path) -> dict:
    """Extract follower count from a Twitter profile screenshot"""
    try:
        # Read text from image
        results = reader.readtext(str(image_path))
        
        # Combine all detected text
        all_text = ' '.join([text[1] for text in results])
        
        # Look for patterns in both English and Turkish
        patterns = [
            # English patterns
            r'([\d,.]+[KMB]?)\s*Followers?',
            r'Followers?\s*([\d,.]+[KMB]?)',
            
            # Turkish patterns  
            r'([\d,.]+\s*[KMB]?n?)\s*Takip[çc]i',
            r'Takip[çc]i\s*([\d,.]+\s*[KMB]?n?)',
            
            # Generic
            r'([\d,.]+[KMB]?)\s*(?:Followers?|Takip[çc]i)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            if matches:
                count_str = matches[0]
                follower_count = parse_count(count_str)
                if follower_count:
                    return {
                        'success': True,
                        'followers': follower_count,
                        'raw_text': count_str,
                        'detected_text': all_text[:200]
                    }
        
        return {
            'success': False,
            'error': 'No follower count found',
            'detected_text': all_text[:200]
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def parse_count(text: str) -> int:
    """Parse follower count from text"""
    try:
        original_text = text.strip().upper()
        
        # Handle Turkish 'Mn' (Milyon) and 'Bn' (Bin)
        text = original_text.replace('MN', 'M').replace('BN', 'K')
        
        multiplier = 1
        if 'K' in text:
            multiplier = 1000
            text = text.replace('K', '')
        elif 'M' in text:
            multiplier = 1000000
            text = text.replace('M', '')
        elif 'B' in text:
            multiplier = 1000000000
            text = text.replace('B', '')
        
        # Handle both English (1.2) and Turkish (1,2) decimal formats
        if ',' in text and '.' not in text:
            parts = text.split(',')
            if len(parts) == 2 and len(parts[1]) <= 2:
                text = parts[0] + '.' + parts[1]
            else:
                text = text.replace(',', '')
        else:
            text = text.replace(',', '')
        
        # Remove non-numeric except decimal
        text = re.sub(r'[^\d.]', '', text)
        
        if text:
            return int(float(text) * multiplier)
        return None
    except:
        return None

def extract_all_followers():
    """Extract follower counts from all screenshots"""
    print("="*70)
    print("EXTRACTING FOLLOWER COUNTS (EasyOCR)")
    print("="*70)
    
    screenshot_dir = Path('twitter-screenshots')
    screenshots = sorted(screenshot_dir.glob('*.png'))
    
    print(f"\n→ Found {len(screenshots)} screenshots")
    print(f"→ Starting extraction...\n")
    
    results = []
    successful = 0
    failed = 0
    
    for i, screenshot in enumerate(screenshots, 1):
        handle = screenshot.stem
        print(f"[{i}/{len(screenshots)}] @{handle}...", end=" ", flush=True)
        
        result = extract_follower_count_from_image(screenshot)
        
        if result['success']:
            followers = result['followers']
            print(f"✓ {followers:,}")
            results.append({
                'handle': handle,
                'name': '',  # To be filled manually if needed
                'followers': followers,
                'following': 0,  # To be filled manually if needed
                'verified': False,
                'screenshot': str(screenshot)
            })
            successful += 1
        else:
            print(f"✗ {result.get('error', 'Failed')}")
            failed += 1
    
    # Save results
    output = {
        'collected_at': '2025-11-24',
        'source': 'easyocr_from_screenshots',
        'total_profiles': len(screenshots),
        'successful': successful,
        'failed': failed,
        'data': results
    }
    
    with open('twitter-follower-data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n\n{'='*70}")
    print("EXTRACTION COMPLETE")
    print(f"{'='*70}")
    print(f"Successful: {successful}/{len(screenshots)} ({successful/len(screenshots)*100:.1f}%)")
    print(f"Failed: {failed}")
    
    if successful > 0:
        print(f"\n✓ Data saved to: twitter-follower-data.json")
        
        # Show top 10
        if results:
            top_10 = sorted(results, key=lambda x: x['followers'], reverse=True)[:10]
            print(f"\nTop 10 by followers:")
            for j, profile in enumerate(top_10, 1):
                print(f"  {j:2d}. @{profile['handle']:20s} {profile['followers']:>12,}")
    
    if failed > 0:
        print(f"\n⚠️  {failed} profiles need manual entry")
    
    return output

if __name__ == "__main__":
    try:
        result = extract_all_followers()
        print("\n✅ OCR extraction complete!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
