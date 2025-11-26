#!/usr/bin/env python3
"""
Retry TikTok data collection with corrected usernames
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

# API Configuration
APIFY_API_TOKEN = "apify_api_8YXjcrdCIMuvbIdb9HdVXSOILePkyo06tZLh"
APIFY_BASE_URL = "https://api.apify.com/v2"
TIKTOK_ACTOR_ID = "xtdata~tiktok-user-information-scraper"

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

def wait_for_run(actor_id: str, run_id: str, timeout: int = 300) -> Optional[Dict[str, Any]]:
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

def main():
    print("="*80)
    print("RETRYING TIKTOK DATA COLLECTION WITH CORRECTIONS")
    print("="*80)
    
    # Load retry input
    with open('tiktok-retry-input.json', 'r') as f:
        retry_input = json.load(f)
    
    usernames = retry_input['usernames']
    print(f"\n→ Retrying {len(usernames)} accounts with corrections")
    
    # Start the run
    print(f"\n→ Starting TikTok scraper...")
    run_id = run_apify_actor(TIKTOK_ACTOR_ID, {'usernames': usernames})
    
    if not run_id:
        print("\n❌ Failed to start actor")
        return
    
    print(f"✓ Run ID: {run_id}")
    
    # Wait for completion
    print(f"\n→ Waiting for completion...")
    run_result = wait_for_run(TIKTOK_ACTOR_ID, run_id, timeout=300)
    
    if not run_result or run_result['data']['status'] != 'SUCCEEDED':
        print(f"\n❌ Run failed")
        return
    
    # Get results
    dataset_id = run_result['data']['defaultDatasetId']
    print(f"\n→ Fetching results...")
    
    items = get_dataset_items(dataset_id)
    
    if not items:
        print("\n❌ No data returned")
        return
    
    print(f"✓ Retrieved {len(items)} profiles")
    
    # Analyze results
    print("\n" + "="*80)
    print("RETRY RESULTS")
    print("="*80)
    
    successful = []
    still_suspicious = []
    
    for item in items:
        username = item.get('unique_id')
        followers = item.get('follower_count', 0)
        nickname = item.get('nickname', '')
        
        if followers > 10000:
            successful.append({
                'username': username,
                'followers': followers,
                'nickname': nickname
            })
        else:
            still_suspicious.append({
                'username': username,
                'followers': followers,
                'nickname': nickname
            })
    
    print(f"\n✅ SUCCESSFUL ({len(successful)} accounts with >10K followers):")
    for profile in sorted(successful, key=lambda x: x['followers'], reverse=True):
        print(f"  @{profile['username']:25s} {profile['followers']:>12,} - {profile['nickname']}")
    
    if still_suspicious:
        print(f"\n⚠️  STILL SUSPICIOUS ({len(still_suspicious)} accounts with <10K followers):")
        for profile in sorted(still_suspicious, key=lambda x: x['followers'], reverse=True):
            print(f"  @{profile['username']:25s} {profile['followers']:>8,} - {profile['nickname']}")
    
    # Check what's missing
    collected_usernames = {item.get('unique_id') for item in items}
    requested_usernames = set(usernames)
    missing = requested_usernames - collected_usernames
    
    if missing:
        print(f"\n❌ STILL MISSING ({len(missing)} accounts):")
        for username in sorted(missing):
            print(f"  • @{username}")
    
    # Save retry results
    retry_results = {
        'collected_at': datetime.now().isoformat(),
        'source': f'apify:{TIKTOK_ACTOR_ID}',
        'total_requested': len(usernames),
        'total_collected': len(items),
        'successful': successful,
        'still_suspicious': still_suspicious,
        'missing': list(missing)
    }
    
    with open('tiktok-retry-results.json', 'w', encoding='utf-8') as f:
        json.dump(retry_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Results saved to tiktok-retry-results.json")
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Requested: {len(usernames)}")
    print(f"Collected: {len(items)}")
    print(f"Successful (>10K): {len(successful)}")
    print(f"Still suspicious (<10K): {len(still_suspicious)}")
    print(f"Missing: {len(missing)}")
    
    if successful:
        print(f"\n✅ {len(successful)} corrections worked!")
    
    if still_suspicious or missing:
        print(f"\n⚠️  {len(still_suspicious) + len(missing)} accounts still need manual collection")

if __name__ == "__main__":
    main()
