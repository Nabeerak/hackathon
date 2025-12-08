from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
import os
import hashlib
from fastapi import HTTPException, Request, Depends, status
from sqlalchemy.orm import Session

# Configure password hashing with bcrypt
# We pre-hash with SHA-256 to avoid bcrypt's 72-byte limitation
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__ident="2b",  # Use 2b variant
    bcrypt__min_rounds=12,  # Secure rounds
)

# Legacy context for old password hashes (with truncation disabled)
pwd_context_legacy = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__truncate_error=False,
    bcrypt__ident="2b"
)

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

class AuthService:
    @staticmethod
    def _prehash_password(password: str) -> str:
        print(f"[DEBUG] _prehash_password: Incoming password length: {len(password)}")
        """
        Pre-hash password with SHA-256 before bcrypt.
        This allows unlimited password length while staying under bcrypt's 72-byte limit.
        The SHA-256 hash is always 64 hex characters (64 bytes), well under the limit.
        """
        prehashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
        print(f"[DEBUG] _prehash_password: Pre-hashed password length: {len(prehashed)}")
        return prehashed

    @staticmethod
    def _truncate_password_legacy(password: str) -> str:
        print(f"[DEBUG] _truncate_password_legacy: Incoming password length: {len(password)}")
        """
        Legacy truncation method for backward compatibility with old password hashes.
        Only used for verifying existing passwords.
        """
        password_bytes = password.encode('utf-8')
        print(f"[DEBUG] _truncate_password_legacy: Password bytes length: {len(password_bytes)}")
        if len(password_bytes) <= 72:
            print(f"[DEBUG] _truncate_password_legacy: Password bytes length <= 72, no truncation.")
            return password

        truncated_bytes = password_bytes[:72]
        print(f"[DEBUG] _truncate_password_legacy: Truncated password bytes length: {len(truncated_bytes)}")
        try:
            decoded_truncated = truncated_bytes.decode('utf-8')
            print(f"[DEBUG] _truncate_password_legacy: Successfully decoded truncated password. Length: {len(decoded_truncated)}")
            return decoded_truncated
        except UnicodeDecodeError:
            print("[DEBUG] _truncate_password_legacy: UnicodeDecodeError during truncation. Attempting further truncation.")
            for i in range(1, 4):
                try:
                    decoded_further_truncated = truncated_bytes[:-i].decode('utf-8')
                    print(f"[DEBUG] _truncate_password_legacy: Successfully decoded further truncated password (i={i}). Length: {len(decoded_further_truncated)}")
                    return decoded_further_truncated
                except UnicodeDecodeError:
                    print(f"[DEBUG] _truncate_password_legacy: UnicodeDecodeError for further truncation (i={i}).")
                    continue
            print("[DEBUG] _truncate_password_legacy: Failed to decode after multiple truncations, returning first 60 chars.")
            return password[:60]

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash password using SHA-256 pre-hashing + bcrypt.
        SHA-256 produces a 64-character hex string (64 bytes), safely under bcrypt's 72-byte limit.
        """
        print(f"[DEBUG] hash_password: Calling _prehash_password...")
        prehashed = AuthService._prehash_password(password)
        print(f"[DEBUG] hash_password: Pre-hashed password for bcrypt (length {len(prehashed)}): {prehashed[:10]}...")

        # Double-check byte length (SHA-256 hex is always 64 bytes, but be safe)
        prehashed_bytes = prehashed.encode('utf-8')
        if len(prehashed_bytes) > 72:
            # Truncate to 72 bytes safely (shouldn't happen with SHA-256, but defensive)
            prehashed = prehashed_bytes[:72].decode('utf-8', errors='ignore')
            print(f"[WARNING] Pre-hashed password truncated to 72 bytes")

        return pwd_context.hash(prehashed)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        print(f"[DEBUG] verify_password: Verifying password. Plain password length: {len(plain_password)}")
        """
        Verify a password using SHA-256 + bcrypt.
        Falls back to legacy truncation method for old password hashes.
        """
        # Try new method first (SHA-256 pre-hashing)
        print(f"[DEBUG] verify_password: Attempting verification with new method (SHA-256 pre-hashing). Plain password (first 10 chars): {plain_password[:10]}...")
        try:
            prehashed = AuthService._prehash_password(plain_password)
            if pwd_context.verify(prehashed, hashed_password):
                print("[DEBUG] verify_password: New method verification successful.")
                return True
        except Exception as e:
            print(f"[DEBUG] verify_password: New method failed with error: {e}")

        # Fall back to legacy method (truncation) for old passwords
        print("[DEBUG] verify_password: New method failed. Falling back to legacy method (truncation).")
        try:
            truncated = AuthService._truncate_password_legacy(plain_password)
            print(f"[DEBUG] verify_password: Legacy truncated password length: {len(truncated)}")
            if pwd_context_legacy.verify(truncated, hashed_password):
                print("[DEBUG] verify_password: Legacy method verification successful.")
                return True
        except Exception as e:
            print(f"[DEBUG] verify_password: Legacy method failed with error: {e}")
            return False
        print("[DEBUG] verify_password: Both new and legacy methods failed.")
        return False

    @staticmethod
    def needs_rehash(hashed_password: str, plain_password: str) -> bool:
        """
        Check if a password hash needs to be upgraded to the new format.
        Returns True if the password was verified using the legacy method.
        """
        # Try new method
        prehashed = AuthService._prehash_password(plain_password)
        if pwd_context.verify(prehashed, hashed_password):
            return False

        # If legacy method works, it needs rehash
        try:
            truncated = AuthService._truncate_password_legacy(plain_password)
            if pwd_context_legacy.verify(truncated, hashed_password):
                return True
        except:
            pass

        return False

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> Optional[dict]:
        """Decode a JWT access token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None

async def get_current_user(request: Request, db: Session = Depends(lambda: None)):
    """
    Dependency to get current user from session cookie.
    Better-auth compatible - reads session token from cookie.
    """
    from ..database import get_db
    from ..models.models import User, Session as DBSession

    if db is None:
        db = next(get_db())

    # Get session token from cookie
    session_token = request.cookies.get("better-auth.session_token")
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Find session in database
    db_session = db.query(DBSession).filter(DBSession.id == session_token).first()
    if not db_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session"
        )

    # Check if session expired
    if db_session.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired"
        )

    # Get user
    user = db.query(User).filter(User.id == db_session.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
