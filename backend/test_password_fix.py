#!/usr/bin/env python3
"""
Test script to verify the bcrypt 72-byte password fix using SHA-256 pre-hashing
"""
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.auth_service import AuthService

def test_password_hashing():
    """Test password hashing with various lengths"""

    print("=" * 70)
    print("Testing Password Hashing with SHA-256 + bcrypt")
    print("=" * 70)

    # Test cases with passwords of different lengths
    test_cases = [
        {
            "name": "Short password",
            "password": "Pass123!",
            "description": "8 characters"
        },
        {
            "name": "Normal password",
            "password": "MySecurePassword123!@#",
            "description": "22 characters"
        },
        {
            "name": "Long password (>72 bytes)",
            "password": "A" * 100,
            "description": "100 characters (100 bytes)"
        },
        {
            "name": "Very long password (>200 bytes)",
            "password": "SecurePass!" * 50,
            "description": "550 characters (550 bytes)"
        },
        {
            "name": "Unicode password (multi-byte chars)",
            "password": "🔒🔑" * 40 + "SecurePassword123",
            "description": "Multi-byte unicode characters"
        }
    ]

    all_passed = True

    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['name']} ({test['description']})")
        print("-" * 70)

        password = test["password"]
        byte_length = len(password.encode('utf-8'))
        print(f"  Password length: {len(password)} characters, {byte_length} bytes")

        try:
            # Hash the password
            print("  Hashing password...", end=" ")
            hashed = AuthService.hash_password(password)
            print("[OK] SUCCESS")
            print(f"  Hash: {hashed[:50]}...")

            # Verify correct password
            print("  Verifying correct password...", end=" ")
            if AuthService.verify_password(password, hashed):
                print("[OK] SUCCESS")
            else:
                print("[FAIL] Password verification failed")
                all_passed = False

            # Verify incorrect password
            print("  Verifying incorrect password...", end=" ")
            if not AuthService.verify_password(password + "wrong", hashed):
                print("[OK] SUCCESS (correctly rejected)")
            else:
                print("[FAIL] Incorrect password was accepted")
                all_passed = False

        except Exception as e:
            print(f"[FAIL] Exception: {e}")
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("[SUCCESS] ALL TESTS PASSED")
        print("The 72-byte bcrypt limitation has been successfully resolved!")
    else:
        print("[FAILED] SOME TESTS FAILED")
        print("There are still issues with password hashing.")
    print("=" * 70)

    return all_passed

if __name__ == "__main__":
    success = test_password_hashing()
    sys.exit(0 if success else 1)
