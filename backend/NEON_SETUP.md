# Neon PostgreSQL Setup Guide

## Why Neon?
The project constitution requires: **"Neon Serverless Postgres database"**

## Step-by-Step Setup (5-10 minutes)

### 1. Create Neon Account (Free Tier)

1. Go to https://neon.tech/
2. Click **"Sign Up"** (top right)
3. Sign up with:
   - GitHub (recommended - fastest)
   - Google
   - Or email

### 2. Create Your First Project

After signing up, you'll be on the Neon dashboard:

1. Click **"Create a project"** or **"New Project"**
2. Fill in:
   - **Project name**: `hackathon-chatbot` (or any name)
   - **Database name**: `chatbot`
   - **Region**: Choose closest to you (e.g., US East, EU West)
3. Click **"Create Project"**

### 3. Get Your Connection String

Once the project is created:

1. You'll see a **"Connection Details"** section
2. Look for **"Connection string"**
3. Click the **copy icon** to copy the full connection string
4. It looks like:
   ```
   postgresql://username:password@ep-xxx-xxx-xxx.us-east-2.aws.neon.tech/chatbot?sslmode=require
   ```

### 4. Update Your .env File

1. Open `backend/.env` in your editor
2. Find the line that says:
   ```env
   NEON_DATABASE_URL="postgresql://username:password@..."
   ```
3. Replace it with your copied connection string:
   ```env
   NEON_DATABASE_URL="postgresql://your-actual-connection-string-here"
   ```
4. Save the file

### 5. Run Database Migrations

Open terminal in the `backend` directory:

```bash
cd backend

# Activate your virtual environment
./venv/Scripts/python.exe -m alembic upgrade head
```

You should see output like:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> e4759d7755ca, create user conversation and message tables
```

### 6. Verify Connection

Test that it works:

```bash
./venv/Scripts/python.exe -c "from src.database import engine; print('✅ Connected to Neon!', engine.url)"
```

You should see:
```
✅ Connected to Neon! postgresql://username:***@ep-xxx-xxx.us-east-2.aws.neon.tech/chatbot
```

## Troubleshooting

### Error: "No database URL found!"
- Make sure you saved the `.env` file
- Check that `NEON_DATABASE_URL` is uncommented (no `#` at the start)

### Error: "connection refused" or "timeout"
- Check your internet connection
- Verify the connection string is correct (no extra spaces)
- Make sure you copied the **entire** connection string including `?sslmode=require`

### Error: "authentication failed"
- Your password might have special characters
- Try regenerating the password in Neon dashboard:
  1. Go to your project settings
  2. Click "Connection Details"
  3. Click "Reset Password"
  4. Copy the new connection string

### Error: "database does not exist"
- Make sure you created a database named `chatbot` in Neon
- Or change the database name in your connection string to match what you created

## Neon Free Tier Limits

The free tier includes:
- ✅ 0.5 GB storage (plenty for this project)
- ✅ Unlimited queries
- ✅ Serverless autoscaling
- ✅ Branching (like git for databases)
- ✅ Always-on compute

Perfect for development and this hackathon project!

## Next Steps

After Neon is set up:
1. ✅ Database configured
2. ⏭️ Fix Qdrant connection (get Qdrant credentials)
3. ⏭️ Rotate OpenAI API key
4. ⏭️ Ingest book content
5. ⏭️ Run the chatbot!

## Need Help?

- Neon Docs: https://neon.tech/docs/introduction
- Neon Discord: https://discord.gg/neon
- This project's docs: See `backend/README.md`
