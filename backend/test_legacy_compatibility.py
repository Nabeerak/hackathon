#!/usr/bin/env python3
"""
Test backward compatibility with old password hashes (truncation method)
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.auth_service import AuthService

def test_legacy_compatibility():
    """Test that old password hashes still work"""

    print("=" * 70)
    print("Testing Backward Compatibility with Legacy Password Hashes")
    print("=" * 70)

    # Simulate an old password hash created with the truncation method
    # This is what would exist in your database for existing users
    test_password = "MyOldPassword123!"

    print("\nStep 1: Create a legacy hash using old truncation method")
    print("-" * 70)

    # Import legacy context directly
    from passlib.context import CryptContext
    pwd_context_legacy = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
        bcrypt__truncate_error=False
    )

    # Create hash using OLD method (what exists in DB)
    old_hash = pwd_context_legacy.hash(test_password)
    print(f"Legacy hash created: {old_hash[:50]}...")

    print("\nStep 2: Verify password using NEW hybrid method")
    print("-" * 70)

    # This should work with the new AuthService that has backward compatibility
    if AuthService.verify_password(test_password, old_hash):
        print("[OK] Successfully verified old password with new method!")
    else:
        print("[FAIL] Failed to verify old password")
        return False

    print("\nStep 3: Check if password needs rehashing")
    print("-" * 70)

    if AuthService.needs_rehash(old_hash, test_password):
        print("[OK] Correctly detected that password needs rehashing")
    else:
        print("[FAIL] Failed to detect that password needs rehashing")
        return False

    print("\nStep 4: Create new hash and verify it doesn't need rehashing")
    print("-" * 70)

    new_hash = AuthService.hash_password(test_password)
    print(f"New hash created: {new_hash[:50]}...")

    if not AuthService.needs_rehash(new_hash, test_password):
        print("[OK] New hash correctly identified as up-to-date")
    else:
        print("[FAIL] New hash incorrectly flagged as needing rehash")
        return False

    print("\nStep 5: Test with long password (>72 bytes)")
    print("-" * 70)

    long_password = "A" * 100
    print(f"Testing with password: {len(long_password)} characters")

    # Old method would truncate this
    old_long_hash = pwd_context_legacy.hash(long_password[:72])
    print("Created legacy hash with truncated password")

    # New method should still verify it
    if AuthService.verify_password(long_password, old_long_hash):
        print("[OK] Long password verified with legacy hash")
    else:
        print("[FAIL] Long password failed verification")
        return False

    print("\n" + "=" * 70)
    print("[SUCCESS] ALL BACKWARD COMPATIBILITY TESTS PASSED")
    print("Old password hashes will work seamlessly and auto-upgrade on login!")
    print("=" * 70)

    return True

if __name__ == "__main__":
    success = test_legacy_compatibility()
    sys.exit(0 if success else 1)
