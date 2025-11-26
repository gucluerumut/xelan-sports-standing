#!/usr/bin/env python3
"""
Test Twitter scraper with a few profiles before running full collection
"""

import json
import time
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright

# Test with just 5 profiles
TEST_HANDLES = ["ManCity", "Arsenal", "realmadrid", "Galatasaray", "Fenerbahce"]

async def scrape_twitter_profile(page, handle: str):
    """Scrape a single Twitter profile"""
    url = f"https://twitter.com/{handle}"
    
    try:
        print(f"  → Scraping @{handle}...")
        
        # Navigate to profile
        await page.goto(url, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)
        
        follower_count = None
        following_count = None
        name = None
        
        # Try multiple methods to find follower count
        try:
            # Method 1: Look for followers link
            followers_link = page.locator('a[href$="/verified_followers"]').first
            if await followers_link.count() > 0:
                followers_span = followers_link.locator('span').first
                followers_text = await followers_span.inner_text()
                follower_count = parse_count(followers_text)
        except:
            pass
        
        if not follower_count:
            try:
                # Method 2: Look in profile header stats
                stats_area = page.locator('[data-testid="UserProfileHeader_Items"]')
                if await stats_area.count() > 0:
                    stats_text = await stats_area.inner_text()
                    lines = stats_text.split('\n')
                    for i, line in enumerate(lines):
                        if 'Followers' in line and i > 0:
                            follower_count = parse_count(lines[i-1])
                            break
            except:
                pass
        
        # Get following count
        try:
            following_link = page.locator('a[href$="/following"]').first
            if await following_link.count() > 0:
                following_span = following_link.locator('span').first
                following_text = await following_span.inner_text()
                following_count = parse_count(following_text)
        except:
            pass
        
        # Get name
        try:
            name_elem = page.locator('[data-testid="UserName"]').first
            if await name_elem.count() > 0:
                name_text = await name_elem.inner_text()
                name = name_text.split('\n')[0]
        except:
            pass
        
        if follower_count is not None:
            print(f"    ✓ {follower_count:,} followers")
            return {
                'handle': handle,
                'name': name or handle,
                'followers': follower_count,
                'following': following_count,
                'url': url
            }
        else:
            print(f"    ✗ Could not extract follower count")
            return None
            
    except Exception as e:
        print(f"    ✗ Error: {str(e)[:100]}")
        return None

def parse_count(text: str):
    """Parse follower count from text like '1.2M' or '45.3K'"""
    try:
        text = text.strip().upper().replace(',', '')
        
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
        
        number = float(text)
        return int(number * multiplier)
    except:
        return None

async def test_scraper():
    """Test the scraper with a few profiles"""
    print("="*70)
    print("TESTING TWITTER SCRAPER")
    print("="*70)
    print(f"\nTesting with {len(TEST_HANDLES)} profiles: {TEST_HANDLES}\n")
    
    results = []
    
    async with async_playwright() as p:
        print("→ Launching browser...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        page = await context.new_page()
        print("✓ Browser ready\n")
        
        for i, handle in enumerate(TEST_HANDLES, 1):
            print(f"[{i}/{len(TEST_HANDLES)}]", end=" ")
            result = await scrape_twitter_profile(page, handle)
            
            if result:
                results.append(result)
            
            # Wait between requests
            if i < len(TEST_HANDLES):
                await asyncio.sleep(3)
        
        await browser.close()
    
    # Show results
    print("\n" + "="*70)
    print("TEST RESULTS")
    print("="*70)
    
    if results:
        print(f"\n✅ Successfully scraped {len(results)}/{len(TEST_HANDLES)} profiles:\n")
        for profile in results:
            followers = profile.get('followers', 0)
            following = profile.get('following', 0)
            print(f"  @{profile['handle']:20s} {followers:>12,} followers")
        
        print("\n✅ Test successful! Ready to run full collection.")
        print("\nTo collect all profiles, run:")
        print("  python3 scrape-twitter-browser.py")
        
        return True
    else:
        print("\n❌ Test failed - no profiles scraped")
        print("\nPossible issues:")
        print("  - Twitter may be blocking automated access")
        print("  - Selectors may have changed")
        print("  - Network issues")
        
        return False

if __name__ == "__main__":
    success = asyncio.run(test_scraper())
    exit(0 if success else 1)
