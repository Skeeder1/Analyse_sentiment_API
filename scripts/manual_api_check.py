#!/usr/bin/env python
"""
Manual API test script to debug endpoints locally or on Render.

Not a pytest suite: it is a standalone script, kept out of the test collection
path on purpose.

Usage:
    python scripts/manual_api_check.py                 # Test local API (default: http://127.0.0.1:8003)
    python scripts/manual_api_check.py https://your-render-url.onrender.com    # Test cloud API
"""

import requests
import json
import sys
from typing import Dict, Any

# Default to local API
API_URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8003"

print(f"Testing API at: {API_URL}\n")
print("=" * 70)


def test_health() -> bool:
    """Test /health endpoint"""
    print("\n[TEST 1] GET /health")
    print("-" * 70)
    try:
        r = requests.get(f"{API_URL}/health", timeout=10)
        print(f"Status: {r.status_code}")
        print(f"Response: {json.dumps(r.json(), indent=2)}")
        return r.status_code == 200
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_predict(text: str) -> bool:
    """Test /predict endpoint"""
    print(f"\n[TEST 2] POST /predict")
    print(f"Text: '{text}'")
    print("-" * 70)
    try:
        payload = {"text": text}
        r = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
        print(f"Status: {r.status_code}")
        if r.status_code >= 400:
            print(f"Response (raw): {r.text[:500]}")  # Show error response
        else:
            print(f"Response: {json.dumps(r.json(), indent=2)}")
        return r.status_code == 200
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_explain(text: str) -> bool:
    """Test /explain endpoint"""
    print("\n[TEST 3] POST /explain")
    print(f"Text: '{text}'")
    print("-" * 70)
    try:
        payload = {"text": text}
        r = requests.post(f"{API_URL}/explain", json=payload, timeout=60)
        print(f"Status: {r.status_code}")
        if r.status_code >= 400:
            print(f"Response (raw): {r.text[:500]}")  # Show error response
        else:
            data = r.json()
            print(f"Sentiment: {data.get('sentiment')}")
            print(f"Explanation (list): {json.dumps(data.get('explanation', [])[:5], indent=2)}...")  # First 5 items
            print(f"HTML (first 200 chars): {data.get('html_explanation', '')[:200]}...")
        return r.status_code == 200
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_root() -> bool:
    """Test / endpoint (homepage)"""
    print(f"\n[TEST 4] GET / (homepage)")
    print("-" * 70)
    try:
        r = requests.get(f"{API_URL}/", timeout=10)
        print(f"Status: {r.status_code}")
        print(f"Content (first 300 chars): {r.text[:300]}...")
        return r.status_code == 200
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("SENTIMENT ANALYSIS API - MANUAL TEST SUITE")
    print("=" * 70)

    results = {}

    # Test 1: Health
    results["health"] = test_health()

    # Test 2: Predict - positive
    results["predict_positive"] = test_predict("I love this product! It's amazing!")

    # Test 3: Predict - negative
    results["predict_negative"] = test_predict("This is terrible, I hate it.")

    # Test 4: Predict - neutral
    results["predict_neutral"] = test_predict("The weather is nice today.")

    # Test 5: Explain - simple
    results["explain_simple"] = test_explain("This movie is great!")

    # Test 6: Explain - longer
    results["explain_longer"] = test_explain("I absolutely love this restaurant. The food is delicious and the service is excellent!")

    # Test 7: Root
    results["root"] = test_root()

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:25} {status}")

    total_tests = len(results)
    passed_tests = sum(1 for p in results.values() if p)
    print(f"\nTotal: {passed_tests}/{total_tests} tests passed")

    if passed_tests == total_tests:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Check logs above for details.")


if __name__ == "__main__":
    main()
