#!/usr/bin/env python3
"""
Test script for the Python Code Executor API
"""

import requests
import json
import sys


def test_basic_execution(base_url):
    """Test basic script execution"""
    url = f"{base_url}/execute"
    script = """
def main():
    return {"message": "Hello World", "status": "success"}
"""

    response = requests.post(url, json={"script": script})
    print(f"Basic execution test: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200


def test_with_print(base_url):
    """Test script with print statements"""
    url = f"{base_url}/execute"
    script = """
def main():
    print("Starting calculation...")
    result = 2 + 2
    print(f"Result: {result}")
    return {"sum": result, "message": "Calculation completed"}
"""

    response = requests.post(url, json={"script": script})
    print(f"Print statement test: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200


def test_pandas_numpy(base_url):
    """Test with pandas and numpy"""
    url = f"{base_url}/execute"
    script = """
import pandas as pd
import numpy as np

def main():
    print("Creating DataFrame...")
    data = {'name': ['Alice', 'Bob', 'Charlie'], 'age': [25, 30, 35]}
    df = pd.DataFrame(data)
    print(f"DataFrame shape: {df.shape}")
    avg_age = np.mean(df['age'])
    print(f"Average age: {avg_age}")
    return {
        "data": df.to_dict('records'),
        "average_age": float(avg_age),
        "total_records": len(df)
    }
"""

    response = requests.post(url, json={"script": script})
    print(f"Pandas/Numpy test: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200


def test_error_handling(base_url):
    """Test error handling"""
    url = f"{base_url}/execute"

    # Test missing main function
    script1 = "print('No main function')"
    response1 = requests.post(url, json={"script": script1})
    print(f"Missing main function test: {response1.status_code}")
    print(f"Response: {response1.json()}")

    # Test dangerous operation
    script2 = """
def main():
    import subprocess
    return "dangerous"
"""
    response2 = requests.post(url, json={"script": script2})
    print(f"Dangerous operation test: {response2.status_code}")
    print(f"Response: {response2.json()}")

    return response1.status_code == 400 and response2.status_code == 400


def test_health_endpoint(base_url):
    """Test health endpoint"""
    url = f"{base_url}/health"
    response = requests.get(url)
    print(f"Health endpoint test: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200


if __name__ == "__main__":
    # Default to localhost, but allow command line argument for Cloud Run URL
    base_url = "http://localhost:8080"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]

    print(f"Running Python Code Executor API tests against: {base_url}")
    print("=" * 60)

    tests = [
        lambda: test_basic_execution(base_url),
        lambda: test_with_print(base_url),
        lambda: test_pandas_numpy(base_url),
        lambda: test_error_handling(base_url),
        lambda: test_health_endpoint(base_url),
    ]

    passed = 0
    total = len(tests)

    for i, test in enumerate(tests):
        print(f"Running test {i+1}/{total}...")
        try:
            if test():
                passed += 1
                print("✅ PASSED")
            else:
                print("❌ FAILED")
        except Exception as e:
            print(f"❌ ERROR: {e}")
        print("-" * 30)

    print(f"Results: {passed}/{total} tests passed")
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed")

    print(f"\nUsage:")
    print(f"  python test_script.py                    # Test localhost:8080")
    print(f"  python test_script.py https://your-url   # Test Cloud Run URL")
