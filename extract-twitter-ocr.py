#!/usr/bin/env python3
"""
Extract follower counts from Twitter screenshots using OCR
"""

import json
import re
from pathlib import Path
from PIL import Image
import pytesseract

# Set tesseract path for Homebrew installation
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def extract_follower_count_from_image(image_path: Path) -> dict:
    """Extract follower count from a Twitter profile screenshot"""
    try:
        # Open image
        img = Image.open(image_path)
        
        # Extract text using OCR
        text = pytesseract.image_to_string(img)
        
        # Look for patterns in both English and Turkish
        # English: "15.2M Followers" or "1,234,567 Followers"
        # Turkish: "15,2 Mn Takipçi" or "1.234.567 Takipçi"
        patterns = [
            # English patterns
            r'([\d,.]+[KMB]?)\s*Followers?',  # "15.2M Followers"
            r'Followers?\s*([\d,.]+[KMB]?)',  # "Followers 15.2M"
            
            # Turkish patterns
            r'([\d,.]+\s*[KMB]?n?)\s*Takip[çc]i',  # "15,2 Mn Takipçi" or "15.2M Takipci"
            r'Takip[çc]i\s*([\d,.]+\s*[KMB]?n?)',  # "Takipçi 15,2 Mn"
            
            # Generic number before common words
            r'([\d,.]+[KMB]?)\s*(?:Followers?|Takip[çc]i)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Take the first match
                count_str = matches[0]
                follower_count = parse_count(count_str)
                if follower_count:
                    return {
                        'success': True,
                        'followers': follower_count,
                        'raw_text': count_str,
                        'full_text': text[:200]  # First 200 chars for debugging
                    }
        
        return {
            'success': False,
            'error': 'No follower count found',
            'full_text': text[:200]
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def parse_count(text: str) -> int:
    """Parse follower count from text like '1.2M', '45.3K', or Turkish '1,2 Mn'"""
    try:
        original_text = text.strip().upper()
        
        # Handle Turkish 'Mn' (Milyon) and 'Bn' (Bin = thousand)
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
        # If there's a comma followed by 1-2 digits, it's likely a decimal separator
        if ',' in text and '.' not in text:
            # Turkish format: 1,2 -> 1.2
            parts = text.split(',')
            if len(parts) == 2 and len(parts[1]) <= 2:
                text = parts[0] + '.' + parts[1]
            else:
                # Otherwise it's a thousands separator, remove it
                text = text.replace(',', '')
        else:
            # Remove commas (thousands separators)
            text = text.replace(',', '')
        
        # Remove any non-numeric characters except decimal point
        text = re.sub(r'[^\d.]', '', text)
        
        if text:
            return int(float(text) * multiplier)
        return None
    except:
        return None

def extract_all_followers():
    """Extract follower counts from all screenshots"""
    print("="*70)
    print("EXTRACTING FOLLOWER COUNTS FROM SCREENSHOTS (OCR)")
    print("="*70)
    
    screenshot_dir = Path('twitter-screenshots')
    screenshots = sorted(screenshot_dir.glob('*.png'))
    
    print(f"\n→ Found {len(screenshots)} screenshots")
    print(f"→ Starting OCR extraction...\n")
    
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
                'followers': followers,
                'raw_text': result['raw_text'],
                'screenshot': str(screenshot)
            })
            successful += 1
        else:
            print(f"✗ {result.get('error', 'Failed')}")
            failed += 1
    
    # Save results
    output = {
        'collected_at': '2025-11-24',
        'source': 'ocr_from_screenshots',
        'total_profiles': len(screenshots),
        'successful': successful,
        'failed': failed,
        'data': results
    }
    
    with open('twitter-follower-data-ocr.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n\n{'='*70}")
    print("EXTRACTION COMPLETE")
    print(f"{'='*70}")
    print(f"Successful: {successful}/{len(screenshots)}")
    print(f"Failed: {failed}")
    
    if successful > 0:
        print(f"\n✓ Data saved to: twitter-follower-data-ocr.json")
        
        # Show top 5
        if results:
            top_5 = sorted(results, key=lambda x: x['followers'], reverse=True)[:5]
            print(f"\nTop 5 by followers:")
            for profile in top_5:
                print(f"  @{profile['handle']:20s} {profile['followers']:>12,}")
    
    return output

if __name__ == "__main__":
    print("\n⚠️  NOTE: This requires pytesseract to be installed")
    print("   Install with: brew install tesseract && pip install pytesseract pillow\n")
    
    try:
        result = extract_all_followers()
        
        if result['successful'] > 0:
            print("\n✅ OCR extraction successful!")
        else:
            print("\n❌ OCR extraction failed")
            print("\nTroubleshooting:")
            print("  1. Make sure tesseract is installed: brew install tesseract")
            print("  2. Install Python packages: pip install pytesseract pillow")
            print("  3. Check screenshot quality")
    except ImportError as e:
        print(f"\n❌ Missing dependency: {e}")
        print("\nInstall required packages:")
        print("  brew install tesseract")
        print("  pip install pytesseract pillow")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
