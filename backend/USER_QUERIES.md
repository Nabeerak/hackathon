# Neon PostgreSQL - User Database Queries

## Quick Access

**Web Console:** https://console.neon.tech/
**Database:** neondb
**Region:** Singapore (ap-southeast-1)

---

## Basic User Queries

### 1. View All Users
```sql
SELECT
    id,
    username,
    email,
    experience_level,
    personalization_enabled,
    created_at
FROM users
ORDER BY created_at DESC;
```

### 2. View User Details with Profile
```sql
SELECT
    id,
    username,
    email,
    experience_level,
    software_background,
    hardware_background,
    learning_goals,
    preferred_language,
    personalization_enabled,
    created_at,
    updated_at
FROM users
ORDER BY created_at DESC;
```

### 3. Count Total Users
```sql
SELECT COUNT(*) as total_users FROM users;
```

### 4. Users Created Today
```sql
SELECT
    username,
    email,
    created_at
FROM users
WHERE DATE(created_at) = CURRENT_DATE
ORDER BY created_at DESC;
```

### 5. Users by Experience Level
```sql
SELECT
    experience_level,
    COUNT(*) as count
FROM users
GROUP BY experience_level
ORDER BY count DESC;
```

---

## Advanced User Analytics

### 6. Users with Most Conversations
```sql
SELECT
    u.username,
    u.email,
    COUNT(c.id) as conversation_count
FROM users u
LEFT JOIN conversations c ON u.id = c.user_id
GROUP BY u.id, u.username, u.email
ORDER BY conversation_count DESC
LIMIT 10;
```

### 7. User Activity Report
```sql
SELECT
    u.username,
    u.email,
    COUNT(DISTINCT c.id) as conversations,
    COUNT(m.id) as total_messages,
    MAX(m.created_at) as last_message
FROM users u
LEFT JOIN conversations c ON u.id = c.user_id
LEFT JOIN messages m ON c.id = m.conversation_id
GROUP BY u.id, u.username, u.email
ORDER BY total_messages DESC;
```

### 8. Active Sessions
```sql
SELECT
    u.username,
    u.email,
    s.expires_at,
    s.ip_address,
    s.created_at as session_started
FROM users u
JOIN sessions s ON u.id = s.user_id
WHERE s.expires_at > NOW()
ORDER BY s.created_at DESC;
```

### 9. User Engagement Metrics
```sql
SELECT
    DATE(u.created_at) as signup_date,
    COUNT(DISTINCT u.id) as new_users,
    COUNT(DISTINCT c.id) as conversations_created
FROM users u
LEFT JOIN conversations c ON u.id = c.user_id AND DATE(c.created_at) = DATE(u.created_at)
WHERE u.created_at >= NOW() - INTERVAL '30 days'
GROUP BY DATE(u.created_at)
ORDER BY signup_date DESC;
```

### 10. Personalization Preferences
```sql
SELECT
    preferred_language,
    personalization_enabled,
    COUNT(*) as user_count
FROM users
GROUP BY preferred_language, personalization_enabled
ORDER BY user_count DESC;
```

---

## User Management Queries

### 11. Find User by Email
```sql
SELECT * FROM users WHERE email = 'user@example.com';
```

### 12. Find Users with Specific Background
```sql
SELECT
    username,
    email,
    software_background,
    hardware_background
FROM users
WHERE
    software_background ILIKE '%python%' OR
    hardware_background ILIKE '%raspberry pi%';
```

### 13. Inactive Users (No Conversations)
```sql
SELECT
    u.username,
    u.email,
    u.created_at
FROM users u
LEFT JOIN conversations c ON u.id = c.user_id
WHERE c.id IS NULL
ORDER BY u.created_at DESC;
```

### 14. Delete Old Sessions (Cleanup)
```sql
DELETE FROM sessions WHERE expires_at < NOW();
```

### 15. User Growth Over Time
```sql
SELECT
    DATE_TRUNC('day', created_at) as date,
    COUNT(*) as new_users,
    SUM(COUNT(*)) OVER (ORDER BY DATE_TRUNC('day', created_at)) as cumulative_users
FROM users
GROUP BY DATE_TRUNC('day', created_at)
ORDER BY date DESC;
```

---

## Python Alternative (Use from backend directory)

```bash
# Quick check
python check_users.py

# Or inline query
python -c "from src.database import SessionLocal; from src.models.models import User; db = SessionLocal(); users = db.query(User).all(); print(f'Total: {len(users)}'); [print(f'{u.username}: {u.email}') for u in users]; db.close()"
```

---

## Database Tools

You can also connect using these tools:

1. **pgAdmin** - https://www.pgadmin.org/
2. **DBeaver** - https://dbeaver.io/
3. **TablePlus** - https://tableplus.com/
4. **VS Code Extension** - PostgreSQL by Chris Kolkman

Connection String:
```
postgresql://neondb_owner:npg_bn2H0AqWeNpv@ep-lingering-meadow-a1l67fjv-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
```

---

## Quick Stats Command

```bash
cd backend && python -c "
from src.database import SessionLocal
from src.models.models import User, Conversation, Message
db = SessionLocal()
print(f'''
DATABASE STATISTICS
===================
Users:          {db.query(User).count()}
Conversations:  {db.query(Conversation).count()}
Messages:       {db.query(Message).count()}
''')
db.close()
"
```
