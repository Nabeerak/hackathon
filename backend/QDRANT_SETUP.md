# Qdrant Cloud Setup Guide

## Why Qdrant?
The project constitution requires: **"Qdrant Cloud Free Tier"** for vector search.

## Step-by-Step Setup (5-10 minutes)

### 1. Create Qdrant Cloud Account (Free)

1. Go to https://cloud.qdrant.io/
2. Click **"Get Started"** or **"Sign Up"**
3. Sign up with:
   - GitHub (recommended - fastest)
   - Google
   - Or email
4. Verify your email if required

### 2. Create Your First Cluster

After signing in to the Qdrant Cloud dashboard:

1. Click **"Create Cluster"** or **"New Cluster"**
2. Choose **Free Tier**:
   - **Cluster name**: `hackathon-chatbot` (or any name)
   - **Region**: Choose closest to you (e.g., US East, Europe West)
   - **Node size**: Free tier (1 GB RAM, sufficient for this project)
3. Click **"Create"**

The cluster will take 1-2 minutes to provision.

### 3. Get Your API Credentials

Once the cluster is ready:

1. Click on your cluster name to open details
2. You'll see:
   - **Cluster URL**: `https://xxx-xxx-xxx.us-east.aws.cloud.qdrant.io`
   - **API Key**: Click **"Generate API Key"** or **"Show API Key"**
3. Copy both the URL and API Key

### 4. Update Your .env File

1. Open `backend/.env` in your editor
2. Find these lines:
   ```env
   QDRANT_URL="https://your-instance.qdrant.io"
   QDRANT_API_KEY="your_qdrant_api_key_here"
   ```
3. Replace with your actual values:
   ```env
   QDRANT_URL="https://your-actual-cluster-url.aws.cloud.qdrant.io"
   QDRANT_API_KEY="your-actual-api-key-here"
   ```
4. Save the file

### 5. Test Connection

Open terminal in the `backend` directory:

```bash
cd backend

# Test Qdrant connection
./venv/Scripts/python.exe -c "from qdrant_client import QdrantClient; import os; from dotenv import load_dotenv; load_dotenv(); client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY')); print('✅ Connected to Qdrant!'); print('Collections:', [c.name for c in client.get_collections().collections])"
```

You should see:
```
✅ Connected to Qdrant!
Collections: []
```

(Empty list is normal - we haven't ingested data yet)

### 6. Ingest Book Content

Now load your book content into Qdrant:

```bash
# Still in backend directory
./venv/Scripts/python.exe scripts/ingest_book_content.py --book-path ../docusaurus-book/docs/physical-ai-textbook/
```

This will:
- Read all `.md` and `.mdx` files from your book
- Chunk the content
- Generate embeddings using OpenAI
- Upload to Qdrant

Expected output:
```
Collection 'book_content' ensured.
Ingested 15 chunks from path/to/file1.md
Ingested 22 chunks from path/to/file2.md
...
Finished ingesting 50 documents from ../docusaurus-book/docs/physical-ai-textbook/
```

**Note**: This step requires a valid OpenAI API key and may take 5-15 minutes depending on book size.

### 7. Verify Data Ingestion

Check that data was uploaded:

```bash
./venv/Scripts/python.exe -c "from qdrant_client import QdrantClient; import os; from dotenv import load_dotenv; load_dotenv(); client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY')); collection = client.get_collection('book_content'); print(f'✅ Collection has {collection.points_count} chunks!')"
```

You should see:
```
✅ Collection has 847 chunks!
```

(Number will vary based on your book size)

## Troubleshooting

### Error: "Connection refused" or "timeout"
- Check your internet connection
- Verify the Qdrant cluster is running (check dashboard)
- Make sure you copied the full URL including `https://`

### Error: "Unauthorized" or "403 Forbidden"
- Your API key might be incorrect
- Try regenerating the API key in Qdrant dashboard
- Make sure there are no extra spaces in `.env`

### Error: "Collection not found" during ingestion
- This is normal on first run - the script creates it
- If it persists, check Qdrant dashboard for error logs

### Error: "OPENAI_API_KEY not set" during ingestion
- Make sure your OpenAI API key is set in `.env`
- See `NEON_SETUP.md` for OpenAI setup

### Ingestion is very slow
- This is normal - generating embeddings takes time
- Each chunk requires an OpenAI API call
- Expect 2-10 chunks per second depending on API limits

### Error: "Rate limit exceeded" during ingestion
- OpenAI has rate limits on free tier
- Wait a few minutes and try again
- Or upgrade OpenAI plan for higher limits

## Qdrant Free Tier Limits

The free tier includes:
- ✅ 1 GB RAM
- ✅ 10 GB storage
- ✅ Unlimited requests
- ✅ High availability
- ✅ HTTPS encryption

Perfect for this project! Can store ~100,000+ chunks.

## What's in Qdrant?

After ingestion, your Qdrant collection contains:
- **Vectors**: 1536-dimensional embeddings (from OpenAI text-embedding-ada-002)
- **Metadata**:
  - `source_file`: Which markdown file the chunk came from
  - `chunk_index`: Position in the original file
  - `text_preview`: First 200 characters of the chunk

## How the Chatbot Uses Qdrant

1. User asks a question: "What is ROS 2?"
2. Backend generates embedding of the question
3. Qdrant finds the 5 most similar chunks (vector search)
4. Backend sends those chunks + question to OpenAI
5. OpenAI generates answer based on the context
6. User sees the answer!

## Next Steps

After Qdrant is set up:
1. ✅ Qdrant configured and data ingested
2. ⏭️ Test chatbot backend
3. ⏭️ Make chatbot UI responsive
4. ⏭️ Run full end-to-end test

## Need Help?

- Qdrant Docs: https://qdrant.tech/documentation/
- Qdrant Discord: https://discord.gg/qdrant
- This project's docs: See `backend/README.md`
