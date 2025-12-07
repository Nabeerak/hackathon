"""
Rehash user password with new SHA-256 + bcrypt method
Run this to update your existing password hash
"""
from src.database import SessionLocal
from src.models.models import User
from src.services.auth_service import AuthService

def rehash_user_password(email: str, password: str):
    """Rehash a user's password using the new method"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()

        if not user:
            print(f"❌ User {email} not found!")
            return

        # Hash password with new SHA-256 + bcrypt method
        new_hash = AuthService.hash_password(password)
        user.password_hash = new_hash
        db.commit()

        print(f"✅ Password updated successfully for {email}")
        print(f"   New hash method: SHA-256 + bcrypt")
        print(f"   Hash (first 20 chars): {new_hash[:20]}...")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python rehash_password.py <email> <password>")
        print("Example: python rehash_password.py user@example.com mypassword123")
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]

    print(f"Rehashing password for {email}...")
    rehash_user_password(email, password)
