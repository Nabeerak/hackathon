#!/usr/bin/env python
"""
Test script to verify signup works without password length errors
"""
import requests
import json

# Test with a regular password
def test_signup():
    url = "http://localhost:8000/api/auth/sign-up/email"

    # Test 1: Normal password
    print("\n" + "="*70)
    print("TEST 1: Normal password (should work)")
    print("="*70)

    payload1 = {
        "email": "testuser@example.com",
        "password": "SecurePass123!",
        "name": "Test User",
        "experience_level": "beginner",
        "software_background": "Python, JavaScript",
        "learning_goals": "Learn AI and machine learning"
    }

    response1 = requests.post(url, json=payload1)
    print(f"Status Code: {response1.status_code}")
    print(f"Response: {json.dumps(response1.json(), indent=2)}")

    # Test 2: Very long password (>72 bytes) - should work now without error
    print("\n" + "="*70)
    print("TEST 2: Very long password (>72 bytes) - should work without error")
    print("="*70)

    long_password = "ThisIsAVeryLongPasswordThatExceeds72BytesWhenEncodedInUTF8AndShouldBeAutomaticallyTruncatedByOurCodeWithoutShowingAnyErrorToTheUser123456789"
    print(f"Password length: {len(long_password)} chars, {len(long_password.encode('utf-8'))} bytes")

    payload2 = {
        "email": "longpass@example.com",
        "password": long_password,
        "name": "Long Pass User",
        "experience_level": "intermediate"
    }

    response2 = requests.post(url, json=payload2)
    print(f"Status Code: {response2.status_code}")
    print(f"Response: {json.dumps(response2.json(), indent=2)}")

    # Verify no error message about password length
    response_data = response2.json()
    if "error" in response_data and response_data["error"]:
        error_msg = response_data["error"].get("message", "")
        if "72 bytes" in error_msg.lower():
            print("\n❌ FAILED: Still showing password length error!")
        else:
            print(f"\n⚠️  Error occurred (but not password length): {error_msg}")
    else:
        print("\n✅ SUCCESS: No password length error! Signup worked.")

    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    try:
        test_signup()
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
