#!/usr/bin/env python3
"""
Resume screenshot collection - only collect missing screenshots
"""

import json
import asyncio
import random
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

def load_twitter_handles():
    """Load Twitter handles"""
    with open('twitter-scraper-input.json', 'r') as f:
        data = json.load(f)
        return data['twitterHandles']

def get_missing_handles(all_handles):
    """Get handles that don't have screenshots yet"""
    screenshot_dir = Path('twitter-screenshots')
    existing_screenshots = {f.stem for f in screenshot_dir.glob('*.png')}
    
    missing = [h for h in all_handles if h not in existing_screenshots]
    return missing

async def capture_profile_screenshot(page, handle: str, output_dir: Path):
    """Capture screenshot"""
    url = f"https://twitter.com/{handle}"
    screenshot_path = output_dir / f"{handle}.png"
    
    try:
        print(f"  → @{handle}...", end=" ", flush=True)
        
        response = await page.goto(url, wait_until='domcontentloaded', timeout=60000)
        
        if not response or response.status >= 400:
            print(f"✗ HTTP {response.status if response else 'error'}")
            return False
        
        await page.wait_for_timeout(random.randint(3000, 5000))
        await page.mouse.wheel(0, 200)
        await page.wait_for_timeout(1000)
        
        await page.screenshot(path=str(screenshot_path), full_page=False)
        
        print(f"✓")
        return True
        
    except Exception as e:
        print(f"✗ {str(e)[:50]}")
        return False

async def resume_collection():
    """Resume screenshot collection for missing handles"""
    print("="*70)
    print("RESUMING TWITTER SCREENSHOT COLLECTION")
    print("="*70)
    
    output_dir = Path('twitter-screenshots')
    output_dir.mkdir(exist_ok=True)
    
    all_handles = load_twitter_handles()
    missing_handles = get_missing_handles(all_handles)
    
    print(f"\n→ Total handles: {len(all_handles)}")
    print(f"→ Already collected: {len(all_handles) - len(missing_handles)}")
    print(f"→ Still need: {len(missing_handles)}")
    print(f"→ Estimated time: {len(missing_handles) * 8 / 60:.1f} minutes\n")
    
    if not missing_handles:
        print("✅ All screenshots already collected!")
        return
    
    successful = []
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
        
        for i, handle in enumerate(missing_handles, 1):
            print(f"[{i}/{len(missing_handles)}]", end=" ")
            
            success = await capture_profile_screenshot(page, handle, output_dir)
            
            if success:
                successful.append(handle)
            else:
                failed.append(handle)
            
            if i % 20 == 0:
                print(f"\n  💾 Progress: {i}/{len(missing_handles)}")
            
            if i < len(missing_handles):
                delay = random.randint(5, 8)
                await asyncio.sleep(delay)
        
        await browser.close()
    
    print(f"\n\n{'='*70}")
    print("COLLECTION COMPLETE")
    print(f"{'='*70}")
    print(f"Newly collected: {len(successful)}")
    print(f"Failed: {len(failed)}")
    
    # Check total
    total_collected = len(list(output_dir.glob('*.png')))
    print(f"Total screenshots: {total_collected}/{len(all_handles)}")
    
    if total_collected == len(all_handles):
        print("\n✅ All screenshots collected!")
    else:
        print(f"\n⚠️  Still missing {len(all_handles) - total_collected} screenshots")

if __name__ == "__main__":
    try:
        asyncio.run(resume_collection())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
