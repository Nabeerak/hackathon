import os
import markdown
from bs4 import BeautifulSoup
import re

from .openai_service import OpenAIService
from .qdrant_service import QdrantService

class ChatService:
    def __init__(self):
        self.openai_service = OpenAIService()
        self.qdrant_service = QdrantService()

    def clean_text(self, text: str) -> str:
        """Cleans text by removing markdown artifacts and excess whitespace."""
        html = markdown.markdown(text)
        soup = BeautifulSoup(html, features="html.parser")
        clean_text = soup.get_text()
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        return clean_text

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
        """Chunks text into smaller pieces with optional overlap."""
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

    def retrieve_context(self, query: str, limit: int = 5) -> tuple[list[str], list[str]]:
        """Retrieve context and return both text chunks and source references."""
        query_embedding = self.openai_service.get_embedding(query)
        search_results = self.qdrant_service.search_vectors(query_embedding, limit=limit)
        context = []
        sources = []
        for point in search_results:
            if "text_preview" in point.payload:
                context.append(point.payload["text_preview"])
                source = point.payload.get("source", "Unknown")
                sources.append(source)
        return context, sources

    def is_on_topic(self, user_question: str) -> bool:
        """Check if the question is related to the book content."""
        messages = [
            {"role": "system", "content": "You are a content moderator. Determine if the following question is related to physical AI, robotics, embodied AI, humanoid robots, or technical/scientific topics covered in an AI textbook. Respond with only 'yes' or 'no'."},
            {"role": "user", "content": user_question}
        ]
        response = self.openai_service.get_chat_completion(messages, model="gpt-3.5-turbo")
        return response.strip().lower() == "yes"

    def get_rag_response(self, user_question: str) -> tuple[str, list[str]]:
        """Get RAG response with guardrails."""
        # Check if question is on-topic
        if not self.is_on_topic(user_question):
            return ("I can only answer questions related to the book content about physical AI, robotics, and embodied AI. Please ask a question related to these topics.", [])

        context, sources = self.retrieve_context(user_question)

        messages = [
            {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided book content. If the question cannot be answered from the provided context, state that you cannot answer from the book content."},
            {"role": "user", "content": f"Book Content: {' '.join(context)}\n\nQuestion: {user_question}"}
        ]

        response = self.openai_service.get_chat_completion(messages)
        return response, sources

    def get_rag_response_with_selection(self, user_question: str, selected_text: str) -> tuple[str, list[str]]:
        """Get RAG response prioritizing selected text."""
        # Check if question is on-topic
        if not self.is_on_topic(user_question):
            return ("I can only answer questions related to the book content about physical AI, robotics, and embodied AI. Please ask a question related to these topics.", [])

        # Get additional context from vector search
        context, sources = self.retrieve_context(user_question, limit=3)

        # Prioritize selected text
        messages = [
            {"role": "system", "content": "You are a helpful assistant that answers questions based on provided book content. Prioritize information from the Selected Text section, but also use Additional Context when it adds value."},
            {"role": "user", "content": f"Selected Text: {selected_text}\n\nAdditional Context: {' '.join(context)}\n\nQuestion: {user_question}"}
        ]

        response = self.openai_service.get_chat_completion(messages)
        return response, ["Selected Text"] + sources
