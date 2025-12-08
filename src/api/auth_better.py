"""
Better-Auth compatible authentication endpoints for FastAPI
This implements the better-auth API contract to work with better-auth React client
"""
from fastapi import APIRouter, HTTPException, Depends, status, Response, Request
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session as DBSessionType
from ..database import get_db
from ..models.models import User, Session as DBSession
from ..services.auth_service import AuthService
from datetime import datetime, timedelta, timezone
import secrets

router = APIRouter()

# Cookie settings for session (better-auth expects cookies)
SESSION_COOKIE_NAME = "better-auth.session_token"
SESSION_DURATION_DAYS = 7

# ============================================================================
# Request/Response Models
# ============================================================================

def truncate_string_by_bytes(s: str, max_bytes: int) -> str:
    """Truncate a string to a maximum number of bytes, ensuring valid UTF-8."""
    encoded = s.encode('utf-8')
    if len(encoded) <= max_bytes:
        return s

    truncated_encoded = encoded[:max_bytes]
    # Ensure we don't cut a multi-byte character in half
    while True:
        try:
            return truncated_encoded.decode('utf-8')
        except UnicodeDecodeError:
            truncated_encoded = truncated_encoded[:-1] # Remove last byte and try again

class SignUpEmailRequest(BaseModel):
    """Better-auth sign-up request model"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str
    image: Optional[str] = None
    callbackURL: Optional[str] = None
    # Additional fields for our constitution requirements
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    learning_goals: Optional[str] = None
    experience_level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")

    @field_validator('password', mode='before')
    @classmethod
    def validate_password_length_bytes(cls, v: str) -> str:
        if isinstance(v, str):
            truncated_password = truncate_string_by_bytes(v, 70) # Truncate to 70 bytes
            if len(v.encode('utf-8')) > 70:
                print(f"[DEBUG] SignUp: Password (byte length {len(v.encode('utf-8'))}) truncated to {len(truncated_password.encode('utf-8'))} bytes.")
            return truncated_password
        return v

class SignInEmailRequest(BaseModel):
    """Better-auth sign-in request model"""
    email: EmailStr
    password: str
    callbackURL: Optional[str] = None
    rememberMe: Optional[bool] = False

    @field_validator('password', mode='before')
    @classmethod
    def validate_password_length_bytes(cls, v: str) -> str:
        if isinstance(v, str):
            truncated_password = truncate_string_by_bytes(v, 70) # Truncate to 70 bytes
            if len(v.encode('utf-8')) > 70:
                print(f"[DEBUG] SignIn: Password (byte length {len(v.encode('utf-8'))}) truncated to {len(truncated_password.encode('utf-8'))} bytes.")
            return truncated_password
        return v

class SessionData(BaseModel):
    """Better-auth session data model"""
    session: Dict[str, Any]
    user: Dict[str, Any]

class BetterAuthResponse(BaseModel):
    """Better-auth expects this response format"""
    data: Optional[Any] = None
    error: Optional[Dict[str, str]] = None

# ============================================================================
# Helper Functions
# ============================================================================

def create_session(
    db: DBSessionType,
    user: User,
    request: Request,
    remember_me: bool = False
) -> DBSession:
    """Create a new session for the user"""
    session_token = secrets.token_urlsafe(32)

    expires_delta = timedelta(days=30 if remember_me else SESSION_DURATION_DAYS)
    expires_at = datetime.now(timezone.utc) + expires_delta

    new_session = DBSession(
        id=session_token,
        user_id=user.id,
        expires_at=expires_at,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session

def get_session_from_cookie(
    request: Request,
    db: DBSessionType
) -> Optional[DBSession]:
    """Get valid session from cookie or Authorization header"""
    # Try cookie first
    session_token = request.cookies.get(SESSION_COOKIE_NAME)

    # Fallback to Authorization header
    if not session_token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            session_token = auth_header.replace("Bearer ", "")

    if not session_token:
        return None

    session = db.query(DBSession).filter(DBSession.id == session_token).first()

    if not session:
        return None

    # Check if session has expired - simple comparison, PostgreSQL handles timezones
    if session.expires_at < datetime.now(timezone.utc):
        db.delete(session)
        db.commit()
        return None

    return session

def user_to_dict(user: User) -> Dict[str, Any]:
    """Convert user model to dictionary for better-auth response"""
    return {
        "id": user.id,
        "email": user.email,
        "name": user.username,
        "image": user.image,
        "emailVerified": True,  # Simplified for now
        "createdAt": user.created_at.isoformat() if user.created_at else None,
        "updatedAt": user.updated_at.isoformat() if user.updated_at else None,
        # Custom fields
        "software_background": user.software_background,
        "hardware_background": user.hardware_background,
        "learning_goals": user.learning_goals,
        "experience_level": user.experience_level or "beginner",
        "personalization_enabled": user.personalization_enabled,
        "preferred_language": user.preferred_language,
    }

def session_to_dict(session: DBSession) -> Dict[str, Any]:
    """Convert session model to dictionary for better-auth response"""
    return {
        "token": session.id,
        "userId": session.user_id,
        "expiresAt": session.expires_at.isoformat() if session.expires_at else None,
        "ipAddress": session.ip_address,
        "userAgent": session.user_agent,
    }

# ============================================================================
# Better-Auth Compatible Endpoints
# ============================================================================

@router.post("/sign-up/email", response_model=BetterAuthResponse)
async def sign_up_email(
    request: Request,
    response: Response,
    body: SignUpEmailRequest,
    db: DBSessionType = Depends(get_db)
):
    """
    Better-auth compatible sign-up endpoint
    POST /api/auth/sign-up/email
    """
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(
            User.email == body.email
        ).first()

        if existing_user:
            return BetterAuthResponse(
                data=None,
                error={"message": "User with this email already exists"}
            )

        print(f"[DEBUG] SignUp: Password before hashing: {body.password[:10]}...")
        # Hash password using SHA-256 + bcrypt (supports unlimited length)
        hashed_password = AuthService.hash_password(body.password)

        new_user = User(
            username=body.name,  # better-auth uses 'name'
            email=body.email,
            password_hash=hashed_password,
            image=body.image,
            software_background=body.software_background,
            hardware_background=body.hardware_background,
            learning_goals=body.learning_goals,
            experience_level=body.experience_level or 'beginner',
            personalization_enabled=True,
            preferred_language='en'
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Create session
        session = create_session(db, new_user, request, remember_me=False)

        # Set session cookie
        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=session.id,
            max_age=SESSION_DURATION_DAYS * 24 * 60 * 60,
            httponly=False,  # Allow JS access for debugging
            samesite="lax",
            secure=False,
            path="/"
        )

        return BetterAuthResponse(
            data={
                "user": user_to_dict(new_user),
                "session": session_to_dict(session)
            },
            error=None
        )

    except Exception as e:
        import traceback
        print("=" * 70)
        print("SIGNUP ERROR:")
        print(traceback.format_exc())
        print("=" * 70)
        return BetterAuthResponse(
            data=None,
            error={"message": str(e)}
        )

@router.post("/sign-in/email", response_model=BetterAuthResponse)
async def sign_in_email(
    request: Request,
    response: Response,
    body: SignInEmailRequest,
    db: DBSessionType = Depends(get_db)
):
    """
    Better-auth compatible sign-in endpoint
    POST /api/auth/sign-in/email
    """
    print("=" * 70)
    print(f"[DEBUG] SIGN-IN ENDPOINT CALLED")
    print(f"[DEBUG] Email: {body.email}")
    print(f"[DEBUG] Password length: {len(body.password)}")
    print(f"[DEBUG] Password (first 10 chars): {body.password[:10]}...")
    print("=" * 70)

    try:
        # Find user
        user = db.query(User).filter(User.email == body.email).first()

        if not user:
            print(f"[DEBUG] User not found: {body.email}")
            return BetterAuthResponse(
                data=None,
                error={"message": "No account found with this email. Please sign up first."}
            )

        print(f"[DEBUG] User found: {user.email} (ID: {user.id})")
        print(f"[DEBUG] Stored password hash (first 20 chars): {user.password_hash[:20]}...")
        print(f"[DEBUG] About to call AuthService.verify_password()")

        # Verify password (supports both old and new hash formats)
        verification_result = AuthService.verify_password(body.password, user.password_hash)
        print(f"[DEBUG] Password verification result: {verification_result}")

        if not verification_result:
            print(f"[DEBUG] Password verification FAILED - returning error response")
            return BetterAuthResponse(
                data=None,
                error={"message": "Incorrect password. Please try again."}
            )

        print(f"[DEBUG] Password verification SUCCEEDED")

        # Upgrade old password hash to new format if needed
        if AuthService.needs_rehash(user.password_hash, body.password):
            user.password_hash = AuthService.hash_password(body.password)
            db.commit()
            print(f"[INFO] Upgraded password hash for user {user.email} to new format")

        # Create session
        session = create_session(db, user, request, remember_me=body.rememberMe)
        print(f"[DEBUG] Session created: {session.id}")

        # Set session cookie
        max_age = (30 * 24 * 60 * 60) if body.rememberMe else (SESSION_DURATION_DAYS * 24 * 60 * 60)
        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=session.id,
            max_age=max_age,
            httponly=False,
            samesite="lax",
            secure=False,
            path="/"
        )

        print(f"[DEBUG] Sign-in successful for {user.email}")
        return BetterAuthResponse(
            data={
                "user": user_to_dict(user),
                "session": session_to_dict(session)
            },
            error=None
        )

    except Exception as e:
        print("!" * 70)
        print(f"[ERROR] EXCEPTION CAUGHT IN SIGN-IN ENDPOINT")
        print(f"[ERROR] Exception type: {type(e).__name__}")
        print(f"[ERROR] Exception message: {str(e)}")
        import traceback
        print(f"[ERROR] Traceback:")
        traceback.print_exc()
        print("!" * 70)
        return BetterAuthResponse(
            data=None,
            error={"message": str(e)}
        )

@router.post("/sign-out", response_model=BetterAuthResponse)
async def sign_out(
    request: Request,
    response: Response,
    db: DBSessionType = Depends(get_db)
):
    """
    Better-auth compatible sign-out endpoint
    POST /api/auth/sign-out
    """
    try:
        session = get_session_from_cookie(request, db)

        if session:
            db.delete(session)
            db.commit()

        # Clear cookie
        response.delete_cookie(key=SESSION_COOKIE_NAME)

        return BetterAuthResponse(
            data={"success": True},
            error=None
        )

    except Exception as e:
        return BetterAuthResponse(
            data=None,
            error={"message": str(e)}
        )

@router.get("/get-session")
async def get_session(
    request: Request,
    db: DBSessionType = Depends(get_db)
):
    """
    Better-auth compatible session retrieval endpoint
    GET /api/auth/get-session
    """
    try:
        print("[GET SESSION] called")
        print(f"[GET SESSION] Cookies: {request.cookies}")
        print(f"[GET SESSION] Auth header: {request.headers.get('Authorization', 'None')}")

        session = get_session_from_cookie(request, db)
        print(f"[GET SESSION] Session found: {session is not None}")

        if not session:
            print("[GET SESSION] No session - returning null")
            return {"user": None, "session": None}

        # Load user
        user = db.query(User).filter(User.id == session.user_id).first()
        print(f"[GET SESSION] User found: {user.email if user else 'None'}")

        if not user:
            # Session exists but user doesn't - cleanup
            db.delete(session)
            db.commit()
            return {"user": None, "session": None}

        response_data = {
            "user": user_to_dict(user),
            "session": session_to_dict(session)
        }
        print(f"[GET SESSION] Returning user: {user.email}")
        return response_data

    except Exception as e:
        print(f"[GET SESSION ERROR] {e}")
        import traceback
        traceback.print_exc()
        return {"user": None, "session": None}

# ============================================================================
# Legacy Profile Endpoints (Keep for backward compatibility)
# ============================================================================

@router.get("/profile")
async def get_profile(
    request: Request,
    db: DBSessionType = Depends(get_db)
):
    """Get current user profile (legacy endpoint)"""
    session = get_session_from_cookie(request, db)

    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = db.query(User).filter(User.id == session.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user_to_dict(user)

class UpdateProfileRequest(BaseModel):
    """Profile update request model"""
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    learning_goals: Optional[str] = None
    experience_level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")
    personalization_enabled: Optional[bool] = None
    preferred_language: Optional[str] = Field(None, pattern="^(en|ur)$")

@router.put("/profile", response_model=BetterAuthResponse)
async def update_profile(
    request: Request,
    updates: UpdateProfileRequest,
    db: DBSessionType = Depends(get_db)
):
    """Update current user profile"""
    try:
        session = get_session_from_cookie(request, db)

        if not session:
            return BetterAuthResponse(
                data=None,
                error={"message": "Not authenticated"}
            )

        user = db.query(User).filter(User.id == session.user_id).first()

        if not user:
            return BetterAuthResponse(
                data=None,
                error={"message": "User not found"}
            )

        # Update allowed fields
        update_data = updates.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(user, field):
                setattr(user, field, value)

        user.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)

        return BetterAuthResponse(
            data={
                "user": user_to_dict(user)
            },
            error=None
        )
    except Exception as e:
        return BetterAuthResponse(
            data=None,
            error={"message": str(e)}
        )
