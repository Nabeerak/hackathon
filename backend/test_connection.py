#!/usr/bin/env python3
"""
Test backend API connectivity
"""
import requests

def test_backend():
    """Test if backend is accessible"""

    print("=" * 70)
    print("Testing Backend API Connectivity")
    print("=" * 70)

    base_url = "http://localhost:8000"

    tests = [
        ("Root endpoint", f"{base_url}/"),
        ("Get session (no auth)", f"{base_url}/api/auth/get-session"),
    ]

    for name, url in tests:
        print(f"\n{name}:")
        print(f"  URL: {url}")
        try:
            response = requests.get(url, timeout=5)
            print(f"  Status: {response.status_code}")
            print(f"  Response: {response.text[:100]}")
            print("  [OK]")
        except requests.exceptions.ConnectionError:
            print("  [FAIL] Connection refused - server not responding")
        except Exception as e:
            print(f"  [FAIL] {type(e).__name__}: {e}")

    # Test CORS
    print("\n" + "-" * 70)
    print("Testing CORS Headers:")
    try:
        response = requests.options(
            f"{base_url}/api/auth/get-session",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        print(f"  Status: {response.status_code}")
        cors_headers = {k: v for k, v in response.headers.items() if 'access-control' in k.lower()}
        if cors_headers:
            print("  CORS Headers:")
            for key, value in cors_headers.items():
                print(f"    {key}: {value}")
            print("  [OK]")
        else:
            print("  [WARN] No CORS headers found")
    except Exception as e:
        print(f"  [FAIL] {e}")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_backend()
