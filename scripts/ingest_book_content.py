"""
Script to ingest Docusaurus book content into Qdrant for RAG chatbot

This script reads MDX/MD files from the Docusaurus book directory,
creates embeddings, and stores them in Qdrant for retrieval.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import hashlib

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.services.qdrant_service import QdrantService
from src.services.openai_service import OpenAIService

load_dotenv()

def get_md_files(docs_dir: str):
    """Recursively find all .md and .mdx files in the docs directory"""
    docs_path = Path(docs_dir)
    md_files = list(docs_path.glob("**/*.md")) + list(docs_path.glob("**/*.mdx"))
    return md_files

def read_file_content(file_path: Path) -> str:
    """Read content from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def chunk_content(content: str, chunk_size: int = 1000) -> list:
    """Split content into chunks of approximately chunk_size characters

    This is a simple chunking strategy. For production, consider:
    - Semantic chunking
    - Overlap between chunks
    - Preserving paragraph boundaries
    """
    chunks = []
    words = content.split()
    current_chunk = []
    current_length = 0

    for word in words:
        current_chunk.append(word)
        current_length += len(word) + 1  # +1 for space

        if current_length >= chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_length = 0

    # Add remaining chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def generate_doc_id(content: str, source: str) -> str:
    """Generate a unique ID for a document chunk"""
    hash_input = f"{source}:{content[:100]}"
    return hashlib.md5(hash_input.encode()).hexdigest()

def ingest_documents(docs_dir: str, collection_name: str = "book_content"):
    """Main ingestion function"""
    print(f"Ingesting documents from: {docs_dir}")

    # Initialize services
    qdrant_service = QdrantService()
    openai_service = OpenAIService()

    # Ensure collection exists
    print("Ensuring Qdrant collection exists...")
    qdrant_service.ensure_collection_exists(collection_name)

    # Get all markdown files
    md_files = get_md_files(docs_dir)
    print(f"Found {len(md_files)} markdown files")

    documents = []
    total_chunks = 0

    for file_path in md_files:
        print(f"Processing: {file_path.relative_to(docs_dir)}")

        # Read content
        content = read_file_content(file_path)
        if not content:
            continue

        # Remove frontmatter if present
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2].strip()

        # Chunk content
        chunks = chunk_content(content, chunk_size=1000)
        total_chunks += len(chunks)

        # Create documents with embeddings
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) < 50:  # Skip very small chunks
                continue

            doc_id = generate_doc_id(chunk, str(file_path))
            source = str(file_path.relative_to(Path(docs_dir).parent))

            documents.append({
                "content": chunk,
                "source": source,
                "doc_id": doc_id
            })

    print(f"\nTotal chunks to process: {total_chunks}")
    print("Creating embeddings and uploading to Qdrant...")

    # Process documents in batches
    batch_size = 10
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")

        # Create embeddings for batch
        texts = [doc["content"] for doc in batch]
        try:
            embeddings = openai_service.create_embeddings_batch(texts)
        except Exception as e:
            print(f"Error creating embeddings: {e}")
            continue

        # Prepare documents for Qdrant
        qdrant_docs = []
        for doc, embedding in zip(batch, embeddings):
            qdrant_docs.append({
                "id": doc["doc_id"],
                "vector": embedding,
                "payload": {
                    "content": doc["content"],
                    "source": doc["source"]
                }
            })

        # Upload to Qdrant
        try:
            qdrant_service.upsert_documents(collection_name, qdrant_docs)
        except Exception as e:
            print(f"Error uploading to Qdrant: {e}")
            continue

    print(f"\nIngestion complete! Processed {len(documents)} document chunks.")

if __name__ == "__main__":
    # Default docs directory (adjust as needed)
    docs_dir = os.path.join(
        Path(__file__).resolve().parent.parent.parent,
        "docusaurus-book",
        "docs"
    )

    if len(sys.argv) > 1:
        docs_dir = sys.argv[1]

    if not os.path.exists(docs_dir):
        print(f"Error: Directory not found: {docs_dir}")
        print("Usage: python ingest_book_content.py [docs_directory]")
        sys.exit(1)

    ingest_documents(docs_dir)
