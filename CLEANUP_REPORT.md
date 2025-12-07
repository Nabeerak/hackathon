# Project Cleanup Report

Generated: December 7, 2025

## Summary

This report identifies files and directories that can be safely removed to optimize the project structure and reduce repository size.

---

## ✅ SAFE TO DELETE (Recommended)

### 1. Python Cache Files
**Impact:** No impact on functionality. These are regenerated automatically.

```bash
# Backend cache directories
backend/src/__pycache__/
backend/src/api/__pycache__/
backend/src/models/__pycache__/
backend/src/services/__pycache__/

# Python compiled files
backend/src/api/__pycache__/auth_better.cpython-313.pyc
backend/src/api/__pycache__/chat.cpython-313.pyc
backend/src/api/__pycache__/user_data.cpython-313.pyc
backend/src/models/__pycache__/models.cpython-313.pyc
backend/src/services/__pycache__/auth_service.cpython-313.pyc
backend/src/services/__pycache__/openai_service.cpython-313.pyc
backend/src/services/__pycache__/qdrant_service.cpython-313.pyc
# ... and all other .pyc files
```

**Delete Command:**
```bash
# From project root
find backend -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find backend -type f -name "*.pyc" -delete
find backend -type f -name "*.pyo" -delete
```

---

### 2. Frontend Build Artifacts
**Impact:** No impact. These are regenerated with `npm run build`.

```bash
docusaurus-book/.docusaurus/
docusaurus-book/build/
docusaurus-book/node_modules/  # Can be regenerated with npm install
```

**Delete Command:**
```bash
# From docusaurus-book directory
rm -rf .docusaurus build
# node_modules can be deleted but requires npm install to regenerate
```

---

### 3. Test Files (Development/Debugging Scripts)
**Impact:** Low. These are development utilities not needed in production.

```bash
backend/check_users.py              # User database inspection utility
backend/delete_all_users.py         # Database reset utility
backend/drop_tables.py              # Database cleanup utility
backend/test_connection.py          # Connection testing script
backend/test_legacy_compatibility.py # Legacy password testing
backend/test_password_fix.py        # Password hashing testing
backend/test_services.py            # Service testing script
backend/test_signup.py              # Signup flow testing
backend/fix_conversation_ownership.py # Database migration utility
backend/rehash_password.py          # Password rehashing utility
```

**Recommendation:** Move to a `scripts/` or `dev-tools/` directory instead of deleting, OR delete if you have these in version control and can retrieve them later.

**Move Command:**
```bash
mkdir backend/scripts
mv backend/*.py backend/scripts/
# Move back only main.py if accidentally moved
mv backend/scripts/gunicorn_conf.py backend/
```

---

## ⚠️ MAYBE UNUSED (Review Before Deleting)

### 1. Old Unused Source Files
These files may be legacy or duplicate implementations:

```bash
backend/src/qdrant_client.py        # Possibly superseded by qdrant_service.py
backend/src/llm_factory.py          # Possibly superseded by openai_service.py
```

**Action Required:**
- Check if these are imported anywhere
- Run: `grep -r "import qdrant_client" backend/src/`
- Run: `grep -r "import llm_factory" backend/src/`
- If no imports found, safe to delete

---

### 2. Frontend Duplicate .env Files
```bash
docusaurus-book/.env               # Possibly duplicate of .env.development
```

**Action Required:**
- Review and consolidate into `.env.development` and `.env.production`
- Keep only the necessary environment files

---

### 3. Multiple Alembic Migration Files
```bash
backend/alembic/versions/4607d1cf9799_create_initial_tables.py
backend/alembic/versions/174d8055ab95_add_user_authentication_and_profile_.py
backend/alembic/versions/35d5c98ab1a3_add_session_model_and_image_field_for_.py
backend/alembic/versions/39938e4330c6_add_reading_progress_bookmarks_and_.py
```

**Status:** ✅ KEEP - These are migration history files required by Alembic

**Note:** Only delete old migrations if you're sure you don't need rollback capability. For production, KEEP ALL.

---

## 🔒 DO NOT DELETE (Critical Files)

```bash
# Backend Core
backend/src/main.py
backend/src/database.py
backend/src/models/models.py
backend/src/services/*.py
backend/src/api/*.py
backend/requirements.txt
backend/alembic.ini
backend/alembic/env.py
backend/alembic/versions/*.py  # Migration history

# Frontend Core
docusaurus-book/src/
docusaurus-book/docs/
docusaurus-book/static/
docusaurus-book/package.json
docusaurus-book/docusaurus.config.js
docusaurus-book/sidebars.js

# Configuration
backend/.env (but gitignore it!)
docusaurus-book/.env.development
docusaurus-book/.env.production
.gitignore
README.md
```

---

## 🧹 Recommended Cleanup Actions

### Step 1: Clean Python Cache (Safe)
```bash
cd backend
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null
find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null
```

### Step 2: Clean Frontend Build Artifacts (Safe)
```bash
cd docusaurus-book
rm -rf .docusaurus build
# Optional: rm -rf node_modules (requires npm install to restore)
```

### Step 3: Organize Test Scripts (Recommended)
```bash
cd backend
mkdir -p scripts
mv check_users.py scripts/
mv delete_all_users.py scripts/
mv drop_tables.py scripts/
mv test_*.py scripts/
mv fix_conversation_ownership.py scripts/
mv rehash_password.py scripts/
```

### Step 4: Add to .gitignore (Critical)
Ensure the following is in your `.gitignore`:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
.pytest_cache/
.ruff_cache/

# Environment
.env
.env.local
backend/.env
*.env

# Frontend
node_modules/
.docusaurus/
build/
.cache/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
```

---

## 📊 Estimated Space Savings

| Category | Estimated Size | Safe to Delete? |
|----------|---------------|-----------------|
| Python cache (`__pycache__`) | ~2-5 MB | ✅ Yes |
| Frontend build artifacts | ~200-500 MB | ✅ Yes |
| node_modules | ~300-800 MB | ⚠️ Requires reinstall |
| Test scripts | ~50 KB | ⚠️ Move to scripts/ |

**Total Potential Savings:** ~500-1300 MB

---

## 🎯 Final Recommendations

1. **Run cleanup commands** from Step 1 and Step 2 above
2. **Move test scripts** to `backend/scripts/` directory
3. **Add comprehensive .gitignore** to prevent cache files from being committed
4. **Review unused source files** (`qdrant_client.py`, `llm_factory.py`) and remove if confirmed unused
5. **Keep all Alembic migrations** for production database management

---

## 🔍 Files Requiring Manual Review

Before deleting, manually verify these files are not imported:

```bash
# Check if qdrant_client.py is used
grep -r "from.*qdrant_client import\|import qdrant_client" backend/src/

# Check if llm_factory.py is used
grep -r "from.*llm_factory import\|import llm_factory" backend/src/

# If no results, safe to delete
```

---

**Report Generated By:** Claude Code Agent
**Date:** December 7, 2025
**Project:** Book-Embedded RAG Chatbot
