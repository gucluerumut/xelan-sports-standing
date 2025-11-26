#!/usr/bin/env python3
"""
Collect screenshots of all Twitter profiles for manual data entry
Saves screenshots to twitter-screenshots/ folder
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

async def capture_profile_screenshot(page, handle: str, output_dir: Path):
    """Capture screenshot of a Twitter profile"""
    url = f"https://twitter.com/{handle}"
    screenshot_path = output_dir / f"{handle}.png"
    
    try:
        print(f"  → @{handle}...", end=" ", flush=True)
        
        # Navigate
        response = await page.goto(url, wait_until='domcontentloaded', timeout=60000)
        
        if not response or response.status >= 400:
            print(f"✗ HTTP {response.status if response else 'error'}")
            return False
        
        # Wait for page to load
        await page.wait_for_timeout(random.randint(3000, 5000))
        
        # Scroll to show follower stats
        await page.mouse.wheel(0, 200)
        await page.wait_for_timeout(1000)
        
        # Take screenshot
        await page.screenshot(path=str(screenshot_path), full_page=False)
        
        print(f"✓ Screenshot saved")
        return True
        
    except Exception as e:
        print(f"✗ {str(e)[:50]}")
        return False

async def collect_all_screenshots():
    """Collect all screenshots"""
    print("="*70)
    print("TWITTER PROFILE SCREENSHOT COLLECTION")
    print("="*70)
    
    # Create output directory
    output_dir = Path('twitter-screenshots')
    output_dir.mkdir(exist_ok=True)
    
    handles = load_twitter_handles()
    print(f"\n→ Collecting screenshots for {len(handles)} profiles")
    print(f"→ Output: {output_dir}/")
    print(f"→ Estimated time: {len(handles) * 8 / 60:.1f} minutes\n")
    
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
        
        for i, handle in enumerate(handles, 1):
            print(f"[{i}/{len(handles)}]", end=" ")
            
            success = await capture_profile_screenshot(page, handle, output_dir)
            
            if success:
                successful.append(handle)
            else:
                failed.append(handle)
            
            # Save progress every 20 screenshots
            if i % 20 == 0:
                save_progress(successful, failed, i, len(handles))
            
            # Delay between requests
            if i < len(handles):
                delay = random.randint(5, 8)
                await asyncio.sleep(delay)
        
        await browser.close()
    
    # Final summary
    print(f"\n\n{'='*70}")
    print("SCREENSHOT COLLECTION COMPLETE")
    print(f"{'='*70}")
    print(f"Successful: {len(successful)}/{len(handles)}")
    print(f"Failed: {len(failed)}")
    print(f"\n✓ Screenshots saved to: {output_dir}/")
    
    # Create summary
    summary = {
        'collected_at': datetime.now().isoformat(),
        'total_handles': len(handles),
        'successful': len(successful),
        'failed': len(failed),
        'successful_handles': successful,
        'failed_handles': failed,
        'screenshot_directory': str(output_dir)
    }
    
    with open('twitter-screenshots-summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✓ Summary saved to: twitter-screenshots-summary.json")
    
    return summary

def save_progress(successful, failed, current, total):
    """Save progress"""
    progress = {
        'timestamp': datetime.now().isoformat(),
        'progress': f"{current}/{total}",
        'successful': len(successful),
        'failed': len(failed),
        'successful_handles': successful,
        'failed_handles': failed
    }
    
    with open('twitter-screenshots-progress.json', 'w') as f:
        json.dump(progress, f, indent=2)
    
    print(f"\n  💾 Progress: {len(successful)}/{current} screenshots")

if __name__ == "__main__":
    print("\n⚠️  This will open a visible browser and collect 113 screenshots")
    print("   Estimated time: ~15 minutes\n")
    
    try:
        result = asyncio.run(collect_all_screenshots())
        print("\n✅ Screenshot collection complete!")
        print("\nNext steps:")
        print("  1. Review screenshots in twitter-screenshots/")
        print("  2. Fill in twitter-manual-data-template.json")
        print("  3. Run: python3 cleanup-screenshots.py (when done)")
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted - progress saved")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
