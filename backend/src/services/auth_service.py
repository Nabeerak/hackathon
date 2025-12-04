from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
import hashlib

# Configure password hashing with bcrypt
# We pre-hash with SHA-256 to avoid bcrypt's 72-byte limitation
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# Legacy context for old password hashes (with truncation disabled)
pwd_context_legacy = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__truncate_error=False
)

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

class AuthService:
    @staticmethod
    def _prehash_password(password: str) -> str:
        """
        Pre-hash password with SHA-256 before bcrypt.
        This allows unlimited password length while staying under bcrypt's 72-byte limit.
        The SHA-256 hash is always 64 hex characters (64 bytes), well under the limit.
        """
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def _truncate_password_legacy(password: str) -> str:
        """
        Legacy truncation method for backward compatibility with old password hashes.
        Only used for verifying existing passwords.
        """
        password_bytes = password.encode('utf-8')
        if len(password_bytes) <= 72:
            return password

        truncated_bytes = password_bytes[:72]
        try:
            return truncated_bytes.decode('utf-8')
        except UnicodeDecodeError:
            for i in range(1, 4):
                try:
                    return truncated_bytes[:-i].decode('utf-8')
                except UnicodeDecodeError:
                    continue
            return password[:60]

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using SHA-256 + bcrypt for unlimited length support."""
        prehashed = AuthService._prehash_password(password)
        return pwd_context.hash(prehashed)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password using SHA-256 + bcrypt.
        Falls back to legacy truncation method for old password hashes.
        """
        # Try new method first (SHA-256 pre-hashing)
        prehashed = AuthService._prehash_password(plain_password)
        if pwd_context.verify(prehashed, hashed_password):
            return True

        # Fall back to legacy method (truncation) for old passwords
        try:
            truncated = AuthService._truncate_password_legacy(plain_password)
            return pwd_context_legacy.verify(truncated, hashed_password)
        except:
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
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

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
