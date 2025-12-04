#!/usr/bin/env python
"""
Quick script to check all users in Neon PostgreSQL database
Usage: python check_users.py
"""

from src.database import SessionLocal
from src.models.models import User, Session as DBSession, Conversation
from sqlalchemy import func

def main():
    db = SessionLocal()

    try:
        # Get all users
        users = db.query(User).all()

        print("\n" + "="*70)
        print(f"{'NEON POSTGRESQL - USER DATABASE':^70}")
        print("="*70)
        print(f"\nTotal Users: {len(users)}\n")

        if not users:
            print("No users found in database.\n")
            return

        for i, user in enumerate(users, 1):
            # Get user's session count
            session_count = db.query(DBSession).filter(
                DBSession.user_id == user.id
            ).count()

            # Get user's conversation count
            conv_count = db.query(Conversation).filter(
                Conversation.user_id == user.id
            ).count()

            print(f"\n{'User #' + str(i):-^70}")
            print(f"ID:                  {user.id}")
            print(f"Username:            {user.username}")
            print(f"Email:               {user.email}")
            print(f"Experience Level:    {user.experience_level or 'Not set'}")
            print(f"Preferred Language:  {user.preferred_language or 'en'}")
            print(f"Personalization:     {'Enabled' if user.personalization_enabled else 'Disabled'}")
            print(f"\nProfile Information:")
            print(f"  Software BG:       {user.software_background or 'Not provided'}")
            print(f"  Hardware BG:       {user.hardware_background or 'Not provided'}")
            print(f"  Learning Goals:    {user.learning_goals or 'Not provided'}")
            print(f"\nActivity:")
            print(f"  Sessions:          {session_count}")
            print(f"  Conversations:     {conv_count}")
            print(f"  Account Created:   {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Last Updated:      {user.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 70)

        print("\n" + "="*70 + "\n")

    finally:
        db.close()

if __name__ == "__main__":
    main()
