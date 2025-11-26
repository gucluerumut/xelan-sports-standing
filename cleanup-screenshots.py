#!/usr/bin/env python3
"""
Cleanup script to delete Twitter screenshots when done
"""

import shutil
from pathlib import Path

def cleanup_screenshots():
    """Delete all Twitter screenshots"""
    screenshot_dir = Path('twitter-screenshots')
    
    if not screenshot_dir.exists():
        print("✓ No screenshots to clean up")
        return
    
    # Count files
    screenshots = list(screenshot_dir.glob('*.png'))
    count = len(screenshots)
    
    if count == 0:
        print("✓ No screenshots to clean up")
        return
    
    print("="*70)
    print("TWITTER SCREENSHOTS CLEANUP")
    print("="*70)
    print(f"\n⚠️  This will delete {count} screenshot files")
    print(f"   Directory: {screenshot_dir}/")
    
    response = input("\nAre you sure you want to delete all screenshots? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        # Delete directory
        shutil.rmtree(screenshot_dir)
        print(f"\n✓ Deleted {count} screenshots")
        print(f"✓ Removed directory: {screenshot_dir}/")
        
        # Also clean up debug screenshots
        debug_screenshots = list(Path('.').glob('debug_*.png'))
        if debug_screenshots:
            for screenshot in debug_screenshots:
                screenshot.unlink()
            print(f"✓ Deleted {len(debug_screenshots)} debug screenshots")
        
        print("\n✅ Cleanup complete!")
    else:
        print("\n❌ Cleanup cancelled")

if __name__ == "__main__":
    cleanup_screenshots()
