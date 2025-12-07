"""
Fix conversation ownership - reassign conversations to the authenticated user
This fixes the issue where old conversations have user_id=1 but the authenticated user has a different ID
"""
from src.database import SessionLocal
from src.models.models import Conversation, User
from sqlalchemy import text

def fix_conversations():
    db = SessionLocal()
    try:
        # Find the authenticated user (nabeera600@gmail.com)
        user = db.query(User).filter(User.email == "nabeera600@gmail.com").first()

        if not user:
            print("[ERROR] User nabeera600@gmail.com not found!")
            return

        print(f"[OK] Found user: {user.email} (ID: {user.id})")

        # Find all conversations that aren't owned by this user
        orphaned_convos = db.query(Conversation).filter(Conversation.user_id != user.id).all()

        if not orphaned_convos:
            print("[OK] No orphaned conversations found - all conversations are correctly assigned!")
            return

        print(f"\n[INFO] Found {len(orphaned_convos)} orphaned conversations")

        for convo in orphaned_convos:
            print(f"   - Conversation {convo.id}: '{convo.title[:50] if convo.title else 'Untitled'}...' (current user_id={convo.user_id})")

        # Ask for confirmation
        response = input(f"\n[CONFIRM] Reassign all {len(orphaned_convos)} conversations to user {user.email} (ID: {user.id})? [y/N]: ")

        if response.lower() != 'y':
            print("[CANCEL] Cancelled - no changes made")
            return

        # Reassign all orphaned conversations
        count = 0
        for convo in orphaned_convos:
            convo.user_id = user.id
            count += 1

        db.commit()
        print(f"\n[SUCCESS] Reassigned {count} conversations to {user.email}!")
        print(f"[INFO] User can now delete these conversations from the dashboard.")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Conversation Ownership Fix Script")
    print("=" * 60)
    fix_conversations()
