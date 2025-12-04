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
from datetime import datetime, timedelta
import secrets

router = APIRouter()

# Cookie settings for session (better-auth expects cookies)
SESSION_COOKIE_NAME = "better-auth.session_token"
SESSION_DURATION_DAYS = 7

# ============================================================================
# Request/Response Models
# ============================================================================

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
    def truncate_password(cls, v: str) -> str:
        """Truncate password to 70 characters to avoid bcrypt 72-byte limit"""
        if isinstance(v, str) and len(v) > 70:
            return v[:70]
        return v

class SignInEmailRequest(BaseModel):
    """Better-auth sign-in request model"""
    email: EmailStr
    password: str
    callbackURL: Optional[str] = None
    rememberMe: Optional[bool] = False

    @field_validator('password', mode='before')
    @classmethod
    def truncate_password(cls, v: str) -> str:
        """Truncate password to 70 characters to avoid bcrypt 72-byte limit"""
        if isinstance(v, str) and len(v) > 70:
            return v[:70]
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
    expires_at = datetime.utcnow() + expires_delta

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
    """Get valid session from cookie"""
    session_token = request.cookies.get(SESSION_COOKIE_NAME)

    if not session_token:
        return None

    session = db.query(DBSession).filter(DBSession.id == session_token).first()

    if not session:
        return None

    # Check if session has expired
    if session.expires_at < datetime.utcnow():
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
            httponly=True,
            samesite="lax",
            secure=False  # Set to True in production with HTTPS
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
    try:
        # Find user
        user = db.query(User).filter(User.email == body.email).first()

        if not user:
            return BetterAuthResponse(
                data=None,
                error={"message": "No account found with this email. Please sign up first."}
            )

        # Verify password (supports both old and new hash formats)
        if not AuthService.verify_password(body.password, user.password_hash):
            return BetterAuthResponse(
                data=None,
                error={"message": "Incorrect password. Please try again."}
            )

        # Upgrade old password hash to new format if needed
        if AuthService.needs_rehash(user.password_hash, body.password):
            user.password_hash = AuthService.hash_password(body.password)
            db.commit()
            print(f"[INFO] Upgraded password hash for user {user.email} to new format")

        # Create session
        session = create_session(db, user, request, remember_me=body.rememberMe)

        # Set session cookie
        max_age = (30 * 24 * 60 * 60) if body.rememberMe else (SESSION_DURATION_DAYS * 24 * 60 * 60)
        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=session.id,
            max_age=max_age,
            httponly=True,
            samesite="lax",
            secure=False  # Set to True in production with HTTPS
        )

        return BetterAuthResponse(
            data={
                "user": user_to_dict(user),
                "session": session_to_dict(session)
            },
            error=None
        )

    except Exception as e:
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

@router.get("/get-session", response_model=BetterAuthResponse)
async def get_session(
    request: Request,
    db: DBSessionType = Depends(get_db)
):
    """
    Better-auth compatible session retrieval endpoint
    GET /api/auth/get-session
    """
    try:
        session = get_session_from_cookie(request, db)

        if not session:
            return BetterAuthResponse(
                data=None,
                error=None  # No error, just no session
            )

        # Load user
        user = db.query(User).filter(User.id == session.user_id).first()

        if not user:
            # Session exists but user doesn't - cleanup
            db.delete(session)
            db.commit()
            return BetterAuthResponse(
                data=None,
                error=None
            )

        return BetterAuthResponse(
            data={
                "user": user_to_dict(user),
                "session": session_to_dict(session)
            },
            error=None
        )

    except Exception as e:
        return BetterAuthResponse(
            data=None,
            error={"message": str(e)}
        )

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

        user.updated_at = datetime.utcnow()
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
