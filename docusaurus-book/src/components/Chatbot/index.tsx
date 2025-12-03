import React, { useState, useRef, useEffect } from 'react';
import styles from './styles.module.css';
import { chatAPI } from '../../services/chat_api';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function Chatbot() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    const messageText = input;
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      // Call the real backend API
      const response = await chatAPI.sendMessage({
        conversation_id: conversationId,
        message: messageText,
      });

      // Store conversation ID for future messages
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.message,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Failed to send message:', err);
      const errorMessage: Message = {
        role: 'assistant',
        content: `Error: ${err instanceof Error ? err.message : 'Failed to connect to backend. Make sure the backend server is running at http://localhost:8000'}`,
      };
      setMessages((prev) => [...prev, errorMessage]);
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <>
      <button
        className={styles.chatbotToggle}
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle chatbot"
      >
        💬
      </button>

      {isOpen && (
        <div className={styles.chatbotContainer}>
          <div className={styles.chatbotHeader}>
            <h3>AI Assistant</h3>
            <button onClick={() => setIsOpen(false)} className={styles.btnClose}>
              ×
            </button>
          </div>

          <div className={styles.chatbotMessages}>
            {messages.length === 0 && (
              <div className={styles.chatbotWelcome}>
                <p>Welcome! Ask me anything about the Physical AI textbook.</p>
                <p style={{ fontSize: '12px', color: '#999', marginTop: '10px' }}>
                  (Backend server required for live responses)
                </p>
              </div>
            )}

            {messages.map((msg, index) => (
              <div key={index} className={`${styles.message} ${styles[`message${msg.role.charAt(0).toUpperCase() + msg.role.slice(1)}`]}`}>
                <div className={styles.messageContent}>{msg.content}</div>
              </div>
            ))}

            {isLoading && (
              <div className={`${styles.message} ${styles.messageAssistant}`}>
                <div className={styles.messageContent}>
                  <div className={styles.typingIndicator}>
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <div className={styles.chatbotInputContainer}>
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question about the book..."
              disabled={isLoading}
              rows={3}
            />
            <button
              onClick={handleSendMessage}
              disabled={isLoading || !input.trim()}
              className={styles.btnSend}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </>
  );
}
