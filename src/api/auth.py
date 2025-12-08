from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from sqlalchemy.orm import Session as DBSessionType
from ..database import get_db
from ..models.models import User, Session as DBSession
from ..services.auth_service import AuthService
from datetime import datetime, timedelta
import secrets

router = APIRouter()
security = HTTPBearer(auto_error=False)

# Request and Response Models
class SignupRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    # Additional fields for our use case
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    learning_goals: Optional[str] = None
    experience_level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")

class SigninRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    access_token: str
    user: "UserProfile"

class UserProfile(BaseModel):
    id: int
    username: str
    email: str
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    learning_goals: Optional[str] = None
    experience_level: Optional[str] = None
    personalization_enabled: bool = True
    preferred_language: str = 'en'
    created_at: datetime
    updated_at: datetime

class UpdateProfileRequest(BaseModel):
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    learning_goals: Optional[str] = None
    experience_level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")
    personalization_enabled: Optional[bool] = None
    preferred_language: Optional[str] = Field(None, pattern="^(en|ur)$")

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    payload = AuthService.decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: int = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == request.email) | (User.username == request.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )

    # Create new user
    hashed_password = AuthService.hash_password(request.password)
    new_user = User(
        username=request.username,
        email=request.email,
        password_hash=hashed_password,
        software_background=request.software_background,
        hardware_background=request.hardware_background,
        learning_goals=request.learning_goals,
        experience_level=request.experience_level or 'beginner',
        personalization_enabled=True,
        preferred_language='en'
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create access token
    access_token = AuthService.create_access_token(
        data={"user_id": new_user.id, "email": new_user.email}
    )

    return AuthResponse(
        access_token=access_token,
        user=UserProfile(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            software_background=new_user.software_background,
            hardware_background=new_user.hardware_background,
            learning_goals=new_user.learning_goals,
            experience_level=new_user.experience_level,
            personalization_enabled=new_user.personalization_enabled,
            preferred_language=new_user.preferred_language,
            created_at=new_user.created_at,
            updated_at=new_user.updated_at
        )
    )

@router.post("/signin", response_model=AuthResponse)
async def signin(request: SigninRequest, db: Session = Depends(get_db)):
    """Sign in an existing user"""
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    if not AuthService.verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Upgrade old password hash to new format if needed
    if AuthService.needs_rehash(user.password_hash, request.password):
        user.password_hash = AuthService.hash_password(request.password)
        db.commit()
        print(f"[INFO] Upgraded password hash for user {user.email} to new format")

    # Create access token
    access_token = AuthService.create_access_token(
        data={"user_id": user.id, "email": user.email}
    )

    return AuthResponse(
        access_token=access_token,
        user=UserProfile(
            id=user.id,
            username=user.username,
            email=user.email,
            software_background=user.software_background,
            hardware_background=user.hardware_background,
            learning_goals=user.learning_goals,
            experience_level=user.experience_level,
            personalization_enabled=user.personalization_enabled,
            preferred_language=user.preferred_language,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    )

@router.get("/profile", response_model=UserProfile)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return UserProfile(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        software_background=current_user.software_background,
        hardware_background=current_user.hardware_background,
        learning_goals=current_user.learning_goals,
        experience_level=current_user.experience_level,
        personalization_enabled=current_user.personalization_enabled,
        preferred_language=current_user.preferred_language,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )

@router.put("/profile", response_model=UserProfile)
async def update_profile(
    request: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    # Update only provided fields
    if request.software_background is not None:
        current_user.software_background = request.software_background
    if request.hardware_background is not None:
        current_user.hardware_background = request.hardware_background
    if request.learning_goals is not None:
        current_user.learning_goals = request.learning_goals
    if request.experience_level is not None:
        current_user.experience_level = request.experience_level
    if request.personalization_enabled is not None:
        current_user.personalization_enabled = request.personalization_enabled
    if request.preferred_language is not None:
        current_user.preferred_language = request.preferred_language

    db.commit()
    db.refresh(current_user)

    return UserProfile(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        software_background=current_user.software_background,
        hardware_background=current_user.hardware_background,
        learning_goals=current_user.learning_goals,
        experience_level=current_user.experience_level,
        personalization_enabled=current_user.personalization_enabled,
        preferred_language=current_user.preferred_language,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout user (client should delete token)"""
    return {"message": "Successfully logged out"}
