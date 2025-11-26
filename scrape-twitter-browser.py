#!/usr/bin/env python3
"""
Twitter scraper with updated selectors for 2024 Twitter/X interface
"""

import json
import time
import asyncio
import random
from datetime import datetime
from playwright.async_api import async_playwright

def load_twitter_handles():
    """Load Twitter handles from input file"""
    with open('twitter-scraper-input.json', 'r') as f:
        data = json.load(f)
        return data['twitterHandles']

async def scrape_twitter_profile(page, handle: str):
    """Scrape a single Twitter profile"""
    url = f"https://twitter.com/{handle}"
    
    try:
        print(f"  → @{handle}...", end=" ", flush=True)
        
        # Navigate
        response = await page.goto(url, wait_until='domcontentloaded', timeout=60000)
        
        if not response or response.status >= 400:
            print(f"✗ HTTP {response.status if response else 'error'}")
            return None
        
        # Wait for content to load
        await page.wait_for_timeout(random.randint(3000, 5000))
        
        follower_count = None
        following_count = None
        name = None
        
        try:
            # Method 1: Look for all links and find the one with "Followers"
            all_links = await page.query_selector_all('a[href*="followers"]')
            for link in all_links:
                try:
                    link_text = await link.inner_text()
                    if 'Follower' in link_text:
                        # Extract number from text like "15.2M Followers"
                        parts = link_text.split()
                        if len(parts) >= 1:
                            follower_count = parse_count(parts[0])
                            if follower_count:
                                break
                except:
                    continue
        except:
            pass
        
        # Method 2: Try to find in any span containing follower info
        if not follower_count:
            try:
                page_text = await page.content()
                # Look for pattern like "15.2M" followed by "Followers"
                import re
                pattern = r'([\d,.]+[KMB]?)\s*Followers?'
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                if matches:
                    follower_count = parse_count(matches[0])
            except:
                pass
        
        # Method 3: Look in all text content
        if not follower_count:
            try:
                # Get all span elements
                spans = await page.query_selector_all('span')
                for i, span in enumerate(spans):
                    try:
                        text = await span.inner_text()
                        if 'Follower' in text and i > 0:
                            # Check previous span for number
                            prev_span = spans[i-1]
                            prev_text = await prev_span.inner_text()
                            follower_count = parse_count(prev_text)
                            if follower_count:
                                break
                    except:
                        continue
            except:
                pass
        
        # Get following count similarly
        try:
            all_links = await page.query_selector_all('a[href*="following"]')
            for link in all_links:
                try:
                    link_text = await link.inner_text()
                    if 'Following' in link_text:
                        parts = link_text.split()
                        if len(parts) >= 1:
                            following_count = parse_count(parts[0])
                            if following_count:
                                break
                except:
                    continue
        except:
            pass
        
        # Get name
        try:
            # Look for the display name in the page
            h2_elements = await page.query_selector_all('h2')
            for h2 in h2_elements:
                try:
                    text = await h2.inner_text()
                    if text and len(text) < 50 and not text.startswith('@'):
                        name = text
                        break
                except:
                    continue
        except:
            pass
        
        if follower_count is not None:
            print(f"✓ {follower_count:,}")
            return {
                'handle': handle,
                'name': name or handle,
                'followers': follower_count,
                'following': following_count,
                'url': url
            }
        else:
            print(f"✗ No data")
            # Save screenshot for debugging
            try:
                await page.screenshot(path=f'debug_{handle}.png')
                print(f" (screenshot saved)")
            except:
                pass
            return None
            
    except asyncio.TimeoutError:
        print(f"✗ Timeout")
        return None
    except Exception as e:
        print(f"✗ {str(e)[:50]}")
        return None

def parse_count(text: str):
    """Parse follower count from text"""
    try:
        text = str(text).strip().upper().replace(',', '').replace(' ', '')
        
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
        
        # Remove any non-numeric characters except decimal point
        import re
        text = re.sub(r'[^\d.]', '', text)
        
        if text:
            return int(float(text) * multiplier)
        return None
    except:
        return None

async def collect_twitter_data():
    """Collect Twitter data"""
    print("="*70)
    print("TWITTER DATA COLLECTION (Updated Selectors)")
    print("="*70)
    
    handles = load_twitter_handles()
    print(f"\n→ Loading {len(handles)} handles")
    print(f"→ Estimated time: {len(handles) * 8 / 60:.1f} minutes\n")
    
    results = []
    failed = []
    
    async with async_playwright() as p:
        print("→ Launching browser...")
        browser = await p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """)
        
        page = await context.new_page()
        print("✓ Browser ready\n")
        
        for i, handle in enumerate(handles, 1):
            print(f"[{i}/{len(handles)}]", end=" ")
            
            result = await scrape_twitter_profile(page, handle)
            
            if result:
                results.append(result)
            else:
                failed.append(handle)
            
            # Save progress every 10 profiles
            if i % 10 == 0:
                save_progress(results, failed, i, len(handles))
            
            # Delay between requests
            if i < len(handles):
                delay = random.randint(5, 8)
                await asyncio.sleep(delay)
        
        await browser.close()
    
    # Save final results
    output = {
        'collected_at': datetime.now().isoformat(),
        'source': 'browser_automation_updated',
        'total_profiles': len(results),
        'failed_profiles': len(failed),
        'data': results,
        'failed': failed
    }
    
    with open('twitter-follower-data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n\n{'='*70}")
    print("COLLECTION COMPLETE")
    print(f"{'='*70}")
    print(f"Successful: {len(results)}/{len(handles)}")
    print(f"Failed: {len(failed)}")
    print(f"\n✓ Data saved to twitter-follower-data.json")
    
    if results:
        print(f"\nTop 5 by followers:")
        top_5 = sorted(results, key=lambda x: x['followers'], reverse=True)[:5]
        for profile in top_5:
            print(f"  @{profile['handle']:20s} {profile['followers']:>12,}")
    
    return output

def save_progress(results, failed, current, total):
    """Save progress"""
    progress = {
        'timestamp': datetime.now().isoformat(),
        'progress': f"{current}/{total}",
        'successful': len(results),
        'failed': len(failed),
        'data': results,
        'failed_handles': failed
    }
    
    with open('twitter-progress.json', 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)
    
    print(f"\n  💾 Progress: {len(results)}/{current} successful")

if __name__ == "__main__":
    try:
        result = asyncio.run(collect_twitter_data())
        print("\n✅ Collection successful!")
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted - progress saved in twitter-progress.json")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
