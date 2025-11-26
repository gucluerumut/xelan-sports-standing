#!/usr/bin/env python3
"""
Test script for Apify TikTok and Twitter scrapers
Tests with limited profiles to check follower count extraction
"""

import requests
import json
import time
from typing import Dict, List, Any

# API Configuration
import os

APIFY_API_TOKEN = os.getenv('APIFY_API_TOKEN', 'your_token_here')
APIFY_BASE_URL = "https://api.apify.com/v2"

# Actor IDs - verified from Apify store (profile-specific scrapers)
TIKTOK_ACTOR_ID = "xtdata~tiktok-user-information-scraper"  # Returns profile info with follower_count
TWITTER_ACTOR_ID = "apidojo~twitter-user-scraper"  # Returns user info with followers count

def run_apify_actor(actor_id: str, input_data: Dict[str, Any]) -> str:
    """
    Start an Apify actor run
    Returns: run_id
    """
    url = f"{APIFY_BASE_URL}/acts/{actor_id}/runs"
    headers = {
        "Authorization": f"Bearer {APIFY_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=input_data)
    
    if response.status_code != 201:
        print(f"Error response: {response.text}")
    
    response.raise_for_status()
    
    run_data = response.json()
    return run_data['data']['id']

def wait_for_run(actor_id: str, run_id: str, timeout: int = 300) -> Dict[str, Any]:
    """
    Wait for actor run to complete
    Returns: run status data
    """
    url = f"{APIFY_BASE_URL}/acts/{actor_id}/runs/{run_id}"
    headers = {
        "Authorization": f"Bearer {APIFY_API_TOKEN}"
    }
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        run_data = response.json()
        status = run_data['data']['status']
        
        print(f"Status: {status}")
        
        if status in ['SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT']:
            return run_data
        
        time.sleep(5)
    
    raise TimeoutError(f"Run did not complete within {timeout} seconds")

def get_dataset_items(dataset_id: str) -> List[Dict[str, Any]]:
    """
    Get items from dataset
    """
    url = f"{APIFY_BASE_URL}/datasets/{dataset_id}/items"
    headers = {
        "Authorization": f"Bearer {APIFY_API_TOKEN}"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json()

def test_tiktok_scraper():
    """
    Test TikTok profile scraper with a few profiles
    """
    print("\n" + "="*60)
    print("TESTING TIKTOK SCRAPER")
    print("="*60)
    
    # Test with just 3 profiles
    test_profiles = ["mancity", "arsenal", "realmadrid"]
    
    input_data = {
        "usernames": test_profiles
    }
    
    print(f"\nTesting with profiles: {test_profiles}")
    print(f"Input data: {json.dumps(input_data, indent=2)}")
    
    try:
        # Start the run
        print("\nStarting TikTok scraper...")
        run_id = run_apify_actor(TIKTOK_ACTOR_ID, input_data)
        print(f"Run ID: {run_id}")
        
        # Wait for completion
        print("\nWaiting for completion...")
        run_result = wait_for_run(TIKTOK_ACTOR_ID, run_id)
        
        if run_result['data']['status'] == 'SUCCEEDED':
            dataset_id = run_result['data']['defaultDatasetId']
            print(f"\n✓ Run succeeded! Dataset ID: {dataset_id}")
            
            # Get results
            items = get_dataset_items(dataset_id)
            print(f"\nFound {len(items)} profiles")
            
            # Display results
            for item in items:
                username = item.get('unique_id') or item.get('nickname')
                followers = item.get('follower_count')
                following = item.get('following_count')
                print(f"\n  Profile: @{username}")
                print(f"  Followers: {followers:,}" if followers else "  Followers: N/A")
                print(f"  Following: {following:,}" if following else "  Following: N/A")
            
            return items
        else:
            print(f"\n✗ Run failed with status: {run_result['data']['status']}")
            return None
            
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return None

def test_twitter_scraper():
    """
    Test Twitter profile scraper with a few profiles
    """
    print("\n" + "="*60)
    print("TESTING TWITTER SCRAPER")
    print("="*60)
    
    # Test with just 3 profiles
    test_handles = ["ManCity", "Arsenal", "realmadrid"]
    
    input_data = {
        "twitterHandles": test_handles,
        "getFollowers": False,
        "getFollowing": False,
        "maxItems": 3
    }
    
    print(f"\nTesting with handles: {test_handles}")
    print(f"Input data: {json.dumps(input_data, indent=2)}")
    
    try:
        # Start the run
        print("\nStarting Twitter scraper...")
        run_id = run_apify_actor(TWITTER_ACTOR_ID, input_data)
        print(f"Run ID: {run_id}")
        
        # Wait for completion
        print("\nWaiting for completion...")
        run_result = wait_for_run(TWITTER_ACTOR_ID, run_id)
        
        if run_result['data']['status'] == 'SUCCEEDED':
            dataset_id = run_result['data']['defaultDatasetId']
            print(f"\n✓ Run succeeded! Dataset ID: {dataset_id}")
            
            # Get results
            items = get_dataset_items(dataset_id)
            print(f"\nFound {len(items)} profiles")
            
            # Display results
            for item in items:
                username = item.get('userName') or item.get('name')
                followers = item.get('followers')
                following = item.get('following')
                print(f"\n  Profile: @{username}")
                print(f"  Followers: {followers:,}" if followers else "  Followers: N/A")
                print(f"  Following: {following:,}" if following else "  Following: N/A")
            
            return items
        else:
            print(f"\n✗ Run failed with status: {run_result['data']['status']}")
            return None
            
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return None

def main():
    """
    Main test function
    """
    print("Starting Apify Scraper Tests")
    print("Testing with limited profiles to verify functionality\n")
    
    # Test TikTok
    tiktok_results = test_tiktok_scraper()
    
    # Wait a bit between tests
    time.sleep(3)
    
    # Test Twitter
    twitter_results = test_twitter_scraper()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"TikTok: {'✓ Success' if tiktok_results else '✗ Failed'}")
    print(f"Twitter: {'✓ Success' if twitter_results else '✗ Failed'}")

if __name__ == "__main__":
    main()
