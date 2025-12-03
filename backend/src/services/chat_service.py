from .qdrant_service import QdrantService
from .openai_service import OpenAIService
from typing import List, Dict, Any, Optional
import time

class ChatService:
    def __init__(self):
        self.qdrant_service = QdrantService()
        self.openai_service = OpenAIService()
        self.collection_name = "book_content"

        # Ensure collection exists
        try:
            self.qdrant_service.ensure_collection_exists(self.collection_name)
        except Exception as e:
            print(f"Warning: Could not ensure Qdrant collection exists: {e}")

    def is_on_topic(self, question: str) -> bool:
        """Check if the question is related to the book content using LLM

        Returns:
            True if the question is on-topic, False otherwise
        """
        guardrail_prompt = [
            {
                "role": "system",
                "content": (
                    "You are a content guardrail for a chatbot about a book on 'Physical AI & Humanoid Robotics'. "
                    "Your job is to determine if a user's question is related to this book's topics, which include: "
                    "physical AI, humanoid robots, robotics, artificial intelligence, machine learning in robotics, "
                    "robot hardware, robot software, sensors, actuators, computer vision for robots, "
                    "robot control systems, and related technical topics. "
                    "\n\nRespond with ONLY 'YES' if the question is related to these topics, or 'NO' if it's off-topic. "
                    "Do not provide any explanation."
                )
            },
            {
                "role": "user",
                "content": f"Is this question related to the book topics? Question: {question}"
            }
        ]

        try:
            response = self.openai_service.chat_completion(guardrail_prompt, temperature=0, max_tokens=5)
            return response.strip().upper() == "YES"
        except Exception as e:
            print(f"Error in guardrail check: {e}")
            # Default to allowing the question if guardrail fails
            return True

    def retrieve_context(
        self,
        question: str,
        selected_text: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant context from Qdrant

        If selected_text is provided, prioritize it in the context.
        """
        # Create embedding for the question
        query_vector = self.openai_service.create_embedding(question)

        # Search Qdrant for relevant documents
        results = self.qdrant_service.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )

        # If selected_text is provided, add it as the first context item
        if selected_text:
            # Create a synthetic result for selected text
            selected_result = {
                "id": "selected_text",
                "score": 1.0,  # Highest priority
                "payload": {
                    "content": selected_text,
                    "source": "User Selection"
                }
            }
            # Insert at the beginning
            results = [selected_result] + results[:limit-1]

        return results

    def generate_response(
        self,
        question: str,
        context_results: List[Dict[str, Any]],
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        """Generate a response using RAG

        Args:
            question: User's question
            context_results: Retrieved context from Qdrant
            conversation_history: Previous messages in the conversation

        Returns:
            Generated response
        """
        # Build context string from retrieved documents
        context_parts = []
        for i, result in enumerate(context_results):
            content = result["payload"].get("content", "")
            source = result["payload"].get("source", "Unknown")
            context_parts.append(f"[Source {i+1} - {source}]:\n{content}")

        context_str = "\n\n".join(context_parts)

        # Build messages for chat completion
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant for the book 'Physical AI & Humanoid Robotics'. "
                    "Answer questions based ONLY on the provided context from the book. "
                    "If the context doesn't contain enough information to answer the question, "
                    "say so honestly. Do not make up information. "
                    "Be concise, accurate, and helpful."
                )
            },
            {
                "role": "system",
                "content": f"Context from the book:\n\n{context_str}"
            }
        ]

        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)

        # Add current question
        messages.append({
            "role": "user",
            "content": question
        })

        # Generate response
        response = self.openai_service.chat_completion(messages)
        return response

    def chat(
        self,
        question: str,
        selected_text: Optional[str] = None,
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Main chat method that combines guardrails, retrieval, and generation

        Returns:
            Dict with response, sources, processing_time, and error info
        """
        start_time = time.time()

        # Check if question is on-topic
        if not self.is_on_topic(question):
            return {
                "response": (
                    "I apologize, but I can only answer questions related to the 'Physical AI & Humanoid Robotics' book. "
                    "Your question appears to be outside this scope. "
                    "Please ask about topics like robotics, AI, humanoid robots, sensors, actuators, or related technical subjects."
                ),
                "sources": [],
                "processing_time": int((time.time() - start_time) * 1000),
                "off_topic": True
            }

        # Retrieve relevant context
        try:
            context_results = self.retrieve_context(question, selected_text)
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return {
                "response": "I'm having trouble accessing the book content. Please try again later.",
                "sources": [],
                "processing_time": int((time.time() - start_time) * 1000),
                "error": str(e)
            }

        # Generate response
        try:
            response = self.generate_response(question, context_results, conversation_history)
        except Exception as e:
            print(f"Error generating response: {e}")
            return {
                "response": "I'm having trouble generating a response. Please try again later.",
                "sources": [],
                "processing_time": int((time.time() - start_time) * 1000),
                "error": str(e)
            }

        # Extract sources
        sources = [
            result["payload"].get("source", "Unknown")
            for result in context_results
        ]

        processing_time = int((time.time() - start_time) * 1000)

        return {
            "response": response,
            "sources": sources,
            "processing_time": processing_time,
            "off_topic": False
        }
