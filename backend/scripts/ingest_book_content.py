import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env')) # Load environment variables from .env file

import argparse
from qdrant_client import QdrantClient, models
from openai import OpenAI
from bs4 import BeautifulSoup
import markdown
import re

# Initialize OpenAI and Qdrant clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

COLLECTION_NAME = "book_content"

def get_embedding(text: str) -> list[float]:
    """Generates an embedding for the given text using OpenAI's API."""
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def clean_text(text: str) -> str:
    """Cleans text by removing markdown artifacts and excess whitespace."""
    # Convert markdown to plain text
    html = markdown.markdown(text)
    soup = BeautifulSoup(html, features="html.parser")
    clean_text = soup.get_text()
    # Remove excess whitespace and newlines
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """
    Chunks text into smaller pieces with optional overlap.
    A simple approach for demonstration. For production, consider more advanced chunking strategies.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        if end >= len(text):
            break
        start += (chunk_size - overlap)
    return chunks

def ingest_document(file_path: str, document_id: int, book_path: str, global_doc_counter: int):
    """
    Reads a document, chunks its content, generates embeddings, and uploads to Qdrant.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    cleaned_content = clean_text(content)
    chunks = chunk_text(cleaned_content)

    points = []
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)

        # Create metadata - relative path and chunk index
        relative_path = os.path.relpath(file_path, book_path)
        metadata = {
            "source_file": relative_path,
            "chunk_index": i,
            "text_preview": chunk[:200] + "..." if len(chunk) > 200 else chunk
        }

        points.append(
            models.PointStruct(
                id=global_doc_counter * 1000 + i, # Unique integer ID for each chunk
                vector=embedding,
                payload=metadata
            )
        )

    if points:
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
            wait=True
        )
        print(f"Ingested {len(points)} chunks from {file_path}")

def main(book_path: str):
    """
    Main function to process all markdown files in the book path and ingest them.
    """
    # Ensure the collection exists
    qdrant_client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
    )
    print(f"Collection '{COLLECTION_NAME}' ensured.")

    document_id_counter = 0
    for root, _, files in os.walk(book_path):
        for file in files:
            if file.endswith((".md", ".mdx")):
                file_path = os.path.join(root, file)
                ingest_document(file_path, document_id_counter, book_path, document_id_counter)
                document_id_counter += 1
    print(f"Finished ingesting {document_id_counter} documents from {book_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest book content into Qdrant.")
    parser.add_argument("--book-path", type=str, required=True,
                        help="Path to the Docusaurus book content (e.g., 'docusaurus-book/docs').")
    args = parser.parse_args()

    # Make sure environment variables are set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set.")
        exit(1)
    if not os.getenv("QDRANT_URL"):
        print("Error: QDRANT_URL environment variable not set.")
        exit(1)
    if not os.getenv("QDRANT_API_KEY"):
        print("Error: QDRANT_API_KEY environment variable not set.")
        exit(1)

    main(args.book_path)
