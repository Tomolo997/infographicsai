#!/usr/bin/env python
"""
Test script for fal.ai client integration.

Usage:
    python test_fal_client.py --test [blocking|async|webhook]

Requirements:
    - Set FAL_AI_API_KEY in .env file
    - For webhook test: Set SITE_URL to public URL (use ngrok for local)
"""

import asyncio
import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings.development')
django.setup()

from infographs.infographs.client.fal_ai import FalAI
from django.conf import settings


def test_blocking_generation():
    """
    Test 1: Blocking generation with progress updates.
    
    WARNING: This will block for 30-60 seconds!
    Only use this for testing, NOT in production.
    """
    print("\n" + "="*60)
    print("TEST 1: Blocking Generation (with progress)")
    print("="*60)
    print("⚠️  This will block for 30-60 seconds...\n")
    
    client = FalAI()
    
    def on_progress(message):
        print(f"📊 Progress: {message}")
    
    try:
        result = client.generate_infographic_blocking(
            prompt="A modern infographic showing the benefits of renewable energy, with solar panels and wind turbines",
            on_progress_update=on_progress
        )
        
        print("\n✅ Generation Complete!")
        print(f"Image URL: {result['images'][0]['url']}")
        print(f"Dimensions: {result['images'][0]['width']}x{result['images'][0]['height']}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None


def test_async_submission():
    """
    Test 2: Async submission (returns immediately).
    
    This is the RECOMMENDED approach for production.
    You get a request_id immediately, then poll or use webhook.
    """
    print("\n" + "="*60)
    print("TEST 2: Async Submission (non-blocking)")
    print("="*60)
    print("⚡ This returns immediately!\n")
    
    client = FalAI()
    
    try:
        result = client.submit_generation_sync(
            prompt="A sleek infographic about artificial intelligence, featuring neural networks and data visualization",
            # No webhook_url = we'll poll for result
        )
        
        print("✅ Job Submitted!")
        print(f"Request ID: {result['request_id']}")
        print(f"Status URL: {result['status_url']}")
        print("\n💡 Use this request_id to poll for results:")
        print(f"   result = client.get_result_sync('{result['request_id']}')")
        
        return result['request_id']
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None


def test_async_with_webhook():
    """
    Test 3: Async submission with webhook.
    
    fal.ai will call your webhook when generation completes.
    Requires publicly accessible URL (use ngrok for local dev).
    """
    print("\n" + "="*60)
    print("TEST 3: Async Submission with Webhook")
    print("="*60)
    
    site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
    webhook_url = f"{site_url}/api/infographs/webhook/999/"  # Test infograph ID
    
    print(f"📡 Webhook URL: {webhook_url}")
    
    if 'localhost' in webhook_url:
        print("\n⚠️  WARNING: localhost webhooks won't work!")
        print("   fal.ai can't reach your local machine.")
        print("   Solutions:")
        print("   1. Use ngrok: ngrok http 8000")
        print("   2. Set SITE_URL in .env to ngrok URL")
        print("   3. Or skip webhook and poll for results instead\n")
        
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Skipped.")
            return None
    
    client = FalAI()
    
    try:
        result = client.submit_generation_sync(
            prompt="An infographic about climate change with statistics and charts",
            webhook_url=webhook_url
        )
        
        print("\n✅ Job Submitted with Webhook!")
        print(f"Request ID: {result['request_id']}")
        print(f"Status URL: {result['status_url']}")
        print(f"\n💡 fal.ai will POST results to: {webhook_url}")
        print("   when generation completes (30-60 seconds)")
        
        return result['request_id']
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None


def test_poll_result(request_id):
    """
    Test 4: Poll for result using request_id.
    
    Use this if you didn't use a webhook.
    """
    print("\n" + "="*60)
    print("TEST 4: Poll for Result")
    print("="*60)
    print(f"Request ID: {request_id}\n")
    
    client = FalAI()
    
    print("⏳ Polling for result (this may take 30-60 seconds)...")
    print("   Press Ctrl+C to cancel\n")
    
    import time
    max_attempts = 30
    
    for attempt in range(max_attempts):
        try:
            result = client.get_result_sync(request_id)
            
            if result:
                print("\n✅ Generation Complete!")
                print(f"Image URL: {result['images'][0]['url']}")
                print(f"Dimensions: {result['images'][0]['width']}x{result['images'][0]['height']}")
                return result
            
        except Exception as e:
            # Still processing
            print(f"⏳ Attempt {attempt + 1}/{max_attempts}... ", end='', flush=True)
            time.sleep(2)
    
    print("\n⏱️  Timeout: Generation took longer than expected")
    print("   Try again later or check fal.ai dashboard")
    return None


def main():
    """Main test runner."""
    print("\n" + "="*60)
    print("🧪 Fal.ai Client Test Suite")
    print("="*60)
    
    # Check API key
    api_key = getattr(settings, 'FAL_AI_API_KEY', None)
    if not api_key:
        print("\n❌ ERROR: FAL_AI_API_KEY not found in settings!")
        print("   Add it to your .env file:\n")
        print("   FAL_AI_API_KEY=your_key_here\n")
        return
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Parse command line args
    import argparse
    parser = argparse.ArgumentParser(description='Test fal.ai client')
    parser.add_argument('--test', choices=['blocking', 'async', 'webhook', 'poll', 'all'],
                        default='async', help='Which test to run')
    parser.add_argument('--request-id', help='Request ID for polling test')
    args = parser.parse_args()
    
    # Run tests
    if args.test == 'blocking' or args.test == 'all':
        test_blocking_generation()
    
    if args.test == 'async' or args.test == 'all':
        request_id = test_async_submission()
        
        if request_id and args.test == 'all':
            response = input("\n⏳ Poll for result now? (y/N): ")
            if response.lower() == 'y':
                test_poll_result(request_id)
    
    if args.test == 'webhook':
        test_async_with_webhook()
    
    if args.test == 'poll':
        if not args.request_id:
            print("❌ ERROR: --request-id required for poll test")
            print("   Usage: python test_fal_client.py --test poll --request-id YOUR_ID")
            return
        test_poll_result(args.request_id)
    
    print("\n" + "="*60)
    print("✅ Tests Complete")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()


