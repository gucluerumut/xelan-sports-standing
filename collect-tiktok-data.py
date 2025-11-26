#!/usr/bin/env python3
"""
Collect TikTok follower data for all football clubs
using the verified Apify actor
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

# API Configuration
import os

APIFY_API_TOKEN = os.getenv('APIFY_API_TOKEN', 'your_token_here')
APIFY_BASE_URL = "https://api.apify.com/v2"
TIKTOK_ACTOR_ID = "xtdata~tiktok-user-information-scraper"

def load_tiktok_usernames() -> List[str]:
    """Load TikTok usernames from input file"""
    with open('tiktok-scraper-input.json', 'r') as f:
        data = json.load(f)
        return data['usernames']

def run_apify_actor(actor_id: str, input_data: Dict[str, Any]) -> Optional[str]:
    """Start an Apify actor run"""
    url = f"{APIFY_BASE_URL}/acts/{actor_id}/runs"
    headers = {
        "Authorization": f"Bearer {APIFY_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=input_data, timeout=30)
        
        if response.status_code != 201:
            print(f"✗ Error {response.status_code}: {response.text[:200]}")
            return None
        
        run_data = response.json()
        return run_data['data']['id']
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return None

def wait_for_run(actor_id: str, run_id: str, timeout: int = 600) -> Optional[Dict[str, Any]]:
    """Wait for actor run to complete"""
    url = f"{APIFY_BASE_URL}/acts/{actor_id}/runs/{run_id}"
    headers = {
        "Authorization": f"Bearer {APIFY_API_TOKEN}"
    }
    
    start_time = time.time()
    last_status = None
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            run_data = response.json()
            status = run_data['data']['status']
            
            if status != last_status:
                print(f"  Status: {status}")
                last_status = status
            
            if status in ['SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT']:
                return run_data
            
            time.sleep(5)
        except Exception as e:
            print(f"  ⚠ Error checking status: {str(e)}")
            time.sleep(5)
    
    print(f"✗ Timeout after {timeout}s")
    return None

def get_dataset_items(dataset_id: str) -> Optional[List[Dict[str, Any]]]:
    """Get items from dataset"""
    url = f"{APIFY_BASE_URL}/datasets/{dataset_id}/items"
    headers = {
        "Authorization": f"Bearer {APIFY_API_TOKEN}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"✗ Error getting dataset: {str(e)}")
        return None

def process_tiktok_data(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Process raw TikTok data into clean format"""
    processed = []
    
    for item in items:
        try:
            profile = {
                'username': item.get('unique_id') or item.get('uniqueId'),
                'nickname': item.get('nickname'),
                'follower_count': item.get('follower_count') or item.get('followerCount'),
                'following_count': item.get('following_count') or item.get('followingCount'),
                'video_count': item.get('aweme_count') or item.get('videoCount'),
                'likes_count': item.get('total_favorited') or item.get('heartCount'),
                'verified': item.get('verification_type', 0) > 0 or item.get('isVerified', False),
                'bio': item.get('signature', ''),
                'bio_url': item.get('bio_url', ''),
            }
            
            # Only add if we have essential data
            if profile['username'] and profile['follower_count'] is not None:
                processed.append(profile)
            else:
                print(f"  ⚠ Skipping incomplete profile: {item.get('unique_id', 'unknown')}")
        except Exception as e:
            print(f"  ⚠ Error processing item: {str(e)}")
    
    return processed

def collect_tiktok_data():
    """Main function to collect all TikTok data"""
    print("="*70)
    print("COLLECTING TIKTOK FOLLOWER DATA")
    print("="*70)
    
    # Load usernames
    print("\n→ Loading TikTok usernames...")
    usernames = load_tiktok_usernames()
    print(f"✓ Found {len(usernames)} usernames to scrape")
    
    # Prepare input
    input_data = {
        "usernames": usernames
    }
    
    # Start the run
    print(f"\n→ Starting TikTok scraper...")
    print(f"  Actor: {TIKTOK_ACTOR_ID}")
    print(f"  Profiles: {len(usernames)}")
    
    run_id = run_apify_actor(TIKTOK_ACTOR_ID, input_data)
    
    if not run_id:
        print("\n❌ Failed to start actor")
        return None
    
    print(f"✓ Run ID: {run_id}")
    print(f"  View at: https://console.apify.com/actors/runs/{run_id}")
    
    # Wait for completion
    print(f"\n→ Waiting for completion (this may take several minutes)...")
    run_result = wait_for_run(TIKTOK_ACTOR_ID, run_id, timeout=600)
    
    if not run_result:
        print("\n❌ Run failed or timed out")
        return None
    
    status = run_result['data']['status']
    
    if status != 'SUCCEEDED':
        print(f"\n❌ Run failed with status: {status}")
        return None
    
    # Get results
    dataset_id = run_result['data']['defaultDatasetId']
    print(f"\n→ Fetching results from dataset {dataset_id}...")
    
    items = get_dataset_items(dataset_id)
    
    if not items:
        print("\n❌ No data returned")
        return None
    
    print(f"✓ Retrieved {len(items)} profiles")
    
    # Process data
    print(f"\n→ Processing data...")
    processed_data = process_tiktok_data(items)
    
    print(f"✓ Successfully processed {len(processed_data)} profiles")
    
    # Create output
    output = {
        'collected_at': datetime.now().isoformat(),
        'source': f'apify:{TIKTOK_ACTOR_ID}',
        'total_profiles': len(processed_data),
        'data': processed_data
    }
    
    # Save to file
    output_file = 'tiktok-follower-data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Data saved to {output_file}")
    
    # Show summary statistics
    print("\n" + "="*70)
    print("SUMMARY STATISTICS")
    print("="*70)
    
    total_followers = sum(p['follower_count'] for p in processed_data)
    avg_followers = total_followers / len(processed_data) if processed_data else 0
    
    # Top 10 by followers
    top_10 = sorted(processed_data, key=lambda x: x['follower_count'], reverse=True)[:10]
    
    print(f"\nTotal profiles: {len(processed_data)}")
    print(f"Total followers: {total_followers:,}")
    print(f"Average followers: {avg_followers:,.0f}")
    
    print(f"\nTop 10 by followers:")
    for i, profile in enumerate(top_10, 1):
        print(f"  {i:2d}. @{profile['username']:20s} - {profile['follower_count']:>12,} followers")
    
    # Failed profiles
    failed = len(usernames) - len(processed_data)
    if failed > 0:
        print(f"\n⚠ Failed to scrape {failed} profiles")
        scraped_usernames = {p['username'] for p in processed_data}
        missing = [u for u in usernames if u not in scraped_usernames]
        print(f"  Missing: {', '.join(missing[:10])}")
        if len(missing) > 10:
            print(f"  ... and {len(missing) - 10} more")
    
    return output

if __name__ == "__main__":
    result = collect_tiktok_data()
    
    if result:
        print("\n" + "="*70)
        print("✅ SUCCESS!")
        print("="*70)
        print("\nNext steps:")
        print("  1. Review tiktok-follower-data.json")
        print("  2. Integrate data into the website")
        print("  3. Collect Twitter data (browser automation)")
    else:
        print("\n" + "="*70)
        print("❌ FAILED")
        print("="*70)
