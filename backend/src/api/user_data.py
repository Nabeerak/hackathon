from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import User, ReadingProgress, Bookmark, Note
from ..services.auth_service import get_current_user

router = APIRouter()

# Pydantic models
class ProgressUpdate(BaseModel):
    page_path: str
    progress_percentage: int
    last_position: Optional[str] = None
    completed: bool = False
    time_spent_seconds: int = 0

class BookmarkCreate(BaseModel):
    page_path: str
    page_title: str
    section: Optional[str] = None
    note: Optional[str] = None

class NoteCreate(BaseModel):
    page_path: str
    content: str
    highlighted_text: Optional[str] = None
    position: Optional[str] = None
    color: str = 'yellow'

class NoteUpdate(BaseModel):
    content: Optional[str] = None
    color: Optional[str] = None

# Reading Progress Endpoints
@router.get("/progress")
async def get_reading_progress(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    progress = db.query(ReadingProgress).filter(
        ReadingProgress.user_id == user.id
    ).all()
    return [
        {
            "id": p.id,
            "page_path": p.page_path,
            "progress_percentage": p.progress_percentage,
            "last_position": p.last_position,
            "completed": p.completed,
            "time_spent_seconds": p.time_spent_seconds,
            "updated_at": p.updated_at.isoformat()
        }
        for p in progress
    ]

@router.post("/progress")
async def update_reading_progress(
    data: ProgressUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(ReadingProgress).filter(
        ReadingProgress.user_id == user.id,
        ReadingProgress.page_path == data.page_path
    ).first()

    if existing:
        existing.progress_percentage = data.progress_percentage
        existing.last_position = data.last_position
        existing.completed = data.completed
        existing.time_spent_seconds += data.time_spent_seconds
    else:
        progress = ReadingProgress(
            user_id=user.id,
            page_path=data.page_path,
            progress_percentage=data.progress_percentage,
            last_position=data.last_position,
            completed=data.completed,
            time_spent_seconds=data.time_spent_seconds
        )
        db.add(progress)

    db.commit()
    return {"success": True}

# Bookmark Endpoints
@router.get("/bookmarks")
async def get_bookmarks(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bookmarks = db.query(Bookmark).filter(
        Bookmark.user_id == user.id
    ).order_by(Bookmark.created_at.desc()).all()
    return [
        {
            "id": b.id,
            "page_path": b.page_path,
            "page_title": b.page_title,
            "section": b.section,
            "note": b.note,
            "created_at": b.created_at.isoformat()
        }
        for b in bookmarks
    ]

@router.post("/bookmarks")
async def create_bookmark(
    data: BookmarkCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bookmark = Bookmark(
        user_id=user.id,
        page_path=data.page_path,
        page_title=data.page_title,
        section=data.section,
        note=data.note
    )
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return {"id": bookmark.id, "success": True}

@router.delete("/bookmarks/{bookmark_id}")
async def delete_bookmark(
    bookmark_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bookmark = db.query(Bookmark).filter(
        Bookmark.id == bookmark_id,
        Bookmark.user_id == user.id
    ).first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    db.delete(bookmark)
    db.commit()
    return {"success": True}

# Notes Endpoints
@router.get("/notes")
async def get_notes(
    page_path: Optional[str] = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Note).filter(Note.user_id == user.id)
    if page_path:
        query = query.filter(Note.page_path == page_path)
    notes = query.order_by(Note.created_at.desc()).all()
    return [
        {
            "id": n.id,
            "page_path": n.page_path,
            "content": n.content,
            "highlighted_text": n.highlighted_text,
            "position": n.position,
            "color": n.color,
            "created_at": n.created_at.isoformat(),
            "updated_at": n.updated_at.isoformat()
        }
        for n in notes
    ]

@router.post("/notes")
async def create_note(
    data: NoteCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note = Note(
        user_id=user.id,
        page_path=data.page_path,
        content=data.content,
        highlighted_text=data.highlighted_text,
        position=data.position,
        color=data.color
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return {"id": note.id, "success": True}

@router.put("/notes/{note_id}")
async def update_note(
    note_id: int,
    data: NoteUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == user.id
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if data.content is not None:
        note.content = data.content
    if data.color is not None:
        note.color = data.color

    db.commit()
    return {"success": True}

@router.delete("/notes/{note_id}")
async def delete_note(
    note_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == user.id
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"success": True}

# Recommendations based on user profile
@router.get("/recommendations")
async def get_recommendations(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    recommendations = []

    # Recommend based on experience level
    if user.experience_level == "beginner":
        recommendations.extend([
            {"title": "ROS 2 Basics", "path": "/docs/ros2/basics", "reason": "Perfect for beginners"},
            {"title": "Getting Started Guide", "path": "/docs/getting-started", "reason": "Start here"}
        ])
    elif user.experience_level == "advanced":
        recommendations.extend([
            {"title": "Advanced VLA Models", "path": "/docs/vla/advanced", "reason": "Advanced content"},
            {"title": "Custom Implementations", "path": "/docs/custom", "reason": "For experts"}
        ])

    # Recommend based on learning goals
    if user.learning_goals and "ros" in user.learning_goals.lower():
        recommendations.append({"title": "ROS 2 Deep Dive", "path": "/docs/ros2", "reason": "Matches your goals"})

    return recommendations
