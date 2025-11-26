#!/usr/bin/env python3
"""
Test multiple free Twitter scraper actors from Apify
to find one that works and returns follower counts
"""

import requests
import json
import time
from typing import Dict, List, Any, Optional

# API Configuration
APIFY_API_TOKEN = "apify_api_8YXjcrdCIMuvbIdb9HdVXSOILePkyo06tZLh"
APIFY_BASE_URL = "https://api.apify.com/v2"

# Test profiles
TEST_HANDLES = ["ManCity", "Arsenal", "realmadrid"]

# Actors to test
ACTORS_TO_TEST = [
    {
        "id": "epctex~twitter-profile-scraper",
        "name": "epctex Twitter Profile Scraper",
        "input": {
            "startUrls": [
                {"url": f"https://twitter.com/{handle}"} for handle in TEST_HANDLES
            ],
            "maxItems": 3
        }
    },
    {
        "id": "logical_scrapers~x-twitter-user-profile-tweets-scraper",
        "name": "Logical Scrapers X Profile Scraper",
        "input": {
            "usernames": TEST_HANDLES,
            "maxTweets": 1
        }
    },
    {
        "id": "crawlerbros~twitter-profile-scraper",
        "name": "CrawlerBros Twitter Profile Scraper",
        "input": {
            "usernames": TEST_HANDLES,
            "maxTweets": 1
        }
    },
    {
        "id": "web.harvester~twitter-scraper",
        "name": "Web Harvester Twitter Scraper",
        "input": {
            "usernames": TEST_HANDLES,
            "maxTweets": 1
        }
    }
]

def run_apify_actor(actor_id: str, input_data: Dict[str, Any]) -> Optional[str]:
    """
    Start an Apify actor run
    Returns: run_id or None if failed
    """
    url = f"{APIFY_BASE_URL}/acts/{actor_id}/runs"
    headers = {
        "Authorization": f"Bearer {APIFY_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=input_data, timeout=10)
        
        if response.status_code != 201:
            print(f"  ✗ Error {response.status_code}: {response.text[:200]}")
            return None
        
        run_data = response.json()
        return run_data['data']['id']
    except Exception as e:
        print(f"  ✗ Exception: {str(e)}")
        return None

def wait_for_run(actor_id: str, run_id: str, timeout: int = 120) -> Optional[Dict[str, Any]]:
    """
    Wait for actor run to complete
    Returns: run status data or None if failed/timeout
    """
    url = f"{APIFY_BASE_URL}/acts/{actor_id}/runs/{run_id}"
    headers = {
        "Authorization": f"Bearer {APIFY_API_TOKEN}"
    }
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            run_data = response.json()
            status = run_data['data']['status']
            
            if status in ['SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT']:
                return run_data
            
            time.sleep(5)
        except Exception as e:
            print(f"  ⚠ Error checking status: {str(e)}")
            time.sleep(5)
    
    print(f"  ✗ Timeout after {timeout}s")
    return None

def get_dataset_items(dataset_id: str) -> Optional[List[Dict[str, Any]]]:
    """
    Get items from dataset
    """
    url = f"{APIFY_BASE_URL}/datasets/{dataset_id}/items"
    headers = {
        "Authorization": f"Bearer {APIFY_API_TOKEN}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"  ✗ Error getting dataset: {str(e)}")
        return None

def extract_follower_info(items: List[Dict[str, Any]], actor_name: str) -> Optional[List[Dict[str, Any]]]:
    """
    Try to extract follower information from various data formats
    """
    results = []
    
    for item in items:
        # Try different field names that might contain follower data
        follower_fields = [
            'followers', 'follower_count', 'followers_count', 
            'followersCount', 'public_metrics', 'user'
        ]
        
        username_fields = [
            'username', 'userName', 'screen_name', 'handle', 'name'
        ]
        
        followers = None
        username = None
        
        # Extract followers
        for field in follower_fields:
            if field in item:
                if isinstance(item[field], dict):
                    # Handle nested structures like public_metrics
                    followers = item[field].get('followers_count') or item[field].get('followers')
                else:
                    followers = item[field]
                if followers is not None:
                    break
        
        # Extract username
        for field in username_fields:
            if field in item:
                username = item[field]
                if username:
                    break
        
        if followers is not None and username:
            results.append({
                'username': username,
                'followers': followers,
                'raw_data_sample': {k: v for k, v in list(item.items())[:5]}  # First 5 fields for debugging
            })
    
    return results if results else None

def test_actor(actor_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Test a single actor and return results
    """
    actor_id = actor_config['id']
    actor_name = actor_config['name']
    input_data = actor_config['input']
    
    print(f"\n{'='*70}")
    print(f"Testing: {actor_name}")
    print(f"Actor ID: {actor_id}")
    print(f"{'='*70}")
    
    result = {
        'actor_id': actor_id,
        'actor_name': actor_name,
        'success': False,
        'error': None,
        'data': None
    }
    
    # Start the run
    print(f"\n  → Starting actor...")
    run_id = run_apify_actor(actor_id, input_data)
    
    if not run_id:
        result['error'] = 'Failed to start actor'
        return result
    
    print(f"  ✓ Run ID: {run_id}")
    
    # Wait for completion
    print(f"  → Waiting for completion...")
    run_result = wait_for_run(actor_id, run_id, timeout=120)
    
    if not run_result:
        result['error'] = 'Run timeout or error'
        return result
    
    status = run_result['data']['status']
    print(f"  → Status: {status}")
    
    if status != 'SUCCEEDED':
        result['error'] = f'Run failed with status: {status}'
        return result
    
    # Get results
    dataset_id = run_result['data']['defaultDatasetId']
    print(f"  → Dataset ID: {dataset_id}")
    
    items = get_dataset_items(dataset_id)
    
    if not items:
        result['error'] = 'No data returned'
        return result
    
    print(f"  ✓ Found {len(items)} items")
    
    # Try to extract follower info
    follower_data = extract_follower_info(items, actor_name)
    
    if follower_data:
        result['success'] = True
        result['data'] = follower_data
        print(f"\n  ✅ SUCCESS! Extracted follower data:")
        for profile in follower_data:
            print(f"     @{profile['username']}: {profile['followers']:,} followers")
    else:
        result['error'] = 'Could not extract follower counts from data'
        print(f"\n  ⚠ Data returned but no follower counts found")
        print(f"     Sample data: {json.dumps(items[0] if items else {}, indent=2)[:500]}")
    
    return result

def main():
    """
    Test all actors and report results
    """
    print("="*70)
    print("TESTING TWITTER SCRAPER ACTORS")
    print("="*70)
    print(f"\nTesting {len(ACTORS_TO_TEST)} actors with profiles: {TEST_HANDLES}")
    
    results = []
    
    for actor_config in ACTORS_TO_TEST:
        result = test_actor(actor_config)
        results.append(result)
        time.sleep(3)  # Brief pause between tests
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    successful_actors = [r for r in results if r['success']]
    
    if successful_actors:
        print(f"\n✅ Found {len(successful_actors)} working actor(s):\n")
        for r in successful_actors:
            print(f"  • {r['actor_name']}")
            print(f"    ID: {r['actor_id']}")
            print(f"    Sample data: {len(r['data'])} profiles")
            print()
        
        # Save the best one
        best_actor = successful_actors[0]
        print(f"💡 Recommended actor: {best_actor['actor_id']}")
        
        # Save config
        config = {
            'recommended_actor': best_actor['actor_id'],
            'actor_name': best_actor['actor_name'],
            'test_results': best_actor['data']
        }
        
        with open('twitter-actor-config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✓ Configuration saved to twitter-actor-config.json")
        
    else:
        print("\n❌ No working actors found!")
        print("\nFailed actors:")
        for r in results:
            print(f"  • {r['actor_name']}: {r['error']}")
        
        print("\n💡 Next step: Use browser automation to scrape Twitter profiles")

if __name__ == "__main__":
    main()
