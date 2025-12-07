"""
Delete all users from the database
This allows you to start fresh with SHA-256 + bcrypt hashing
"""
from src.database import SessionLocal
from src.models.models import User, Session, Conversation, Message

def delete_all_users():
    """Delete all users and related data"""
    db = SessionLocal()
    try:
        # Count users before deletion
        user_count = db.query(User).count()
        session_count = db.query(Session).count()
        conversation_count = db.query(Conversation).count()
        message_count = db.query(Message).count()

        print(f"[INFO] Current database state:")
        print(f"   Users: {user_count}")
        print(f"   Sessions: {session_count}")
        print(f"   Conversations: {conversation_count}")
        print(f"   Messages: {message_count}")
        print()

        if user_count == 0:
            print("[OK] Database is already empty - no users to delete")
            return

        # Ask for confirmation
        response = input(f"[WARNING] Delete ALL {user_count} users and their data? [y/N]: ")

        if response.lower() != 'y':
            print("[CANCELLED] No changes made")
            return

        # Delete all data (cascade will handle related records)
        print("\n[DELETING] Removing all users and related data...")

        # Delete messages first
        db.query(Message).delete()
        print(f"   [OK] Deleted {message_count} messages")

        # Delete conversations
        db.query(Conversation).delete()
        print(f"   [OK] Deleted {conversation_count} conversations")

        # Delete sessions
        db.query(Session).delete()
        print(f"   [OK] Deleted {session_count} sessions")

        # Delete users
        db.query(User).delete()
        print(f"   [OK] Deleted {user_count} users")

        db.commit()

        print("\n[SUCCESS] All users deleted successfully!")
        print("[INFO] New signups will use SHA-256 + bcrypt hashing")
        print("[INFO] You can now re-register with the same email")

    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Delete All Users - Start Fresh with SHA-256 + Bcrypt")
    print("=" * 60)
    print()
    delete_all_users()
