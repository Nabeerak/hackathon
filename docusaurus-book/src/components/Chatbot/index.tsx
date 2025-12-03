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
  const [conversationId, setConversationId] = useState<number | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);
  const [selectedText, setSelectedText] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Add text selection listener
  useEffect(() => {
    const handleSelection = () => {
      const selectedText = window.getSelection()?.toString().trim() || '';
      if (selectedText && selectedText.length > 10) {
        setSelectedText(selectedText);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', handleSelection);
    };
  }, []);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    const messageText = input;
    const contextText = selectedText;
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      // Call the real backend API with selected text if available
      const response = await chatAPI.sendMessage({
        conversation_id: conversationId,
        message: messageText,
        selected_text: contextText || undefined,
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

      // Clear selected text after sending
      setSelectedText('');
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

  const handleAskAboutSelection = () => {
    if (!selectedText.trim()) return;
    setInput(`Explain this: "${selectedText.substring(0, 150)}${selectedText.length > 150 ? '...' : ''}"`);
    setIsOpen(true);
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

      {/* Selected text indicator */}
      {selectedText && !isOpen && (
        <div
          className={styles.selectedTextIndicator}
          onClick={handleAskAboutSelection}
          style={{
            position: 'fixed',
            bottom: '100px',
            right: '20px',
            background: 'linear-gradient(135deg, #C2185B 0%, #1565C0 100%)',
            color: 'white',
            padding: '12px 20px',
            borderRadius: '12px',
            cursor: 'pointer',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.2)',
            maxWidth: '300px',
            zIndex: 999,
            display: 'flex',
            flexDirection: 'column',
            gap: '8px',
          }}
        >
          <div style={{ fontSize: '12px', opacity: 0.9 }}>
            Selected: "{selectedText.substring(0, 60)}{selectedText.length > 60 ? '...' : ''}"
          </div>
          <button
            style={{
              background: 'rgba(255, 255, 255, 0.2)',
              border: 'none',
              color: 'white',
              padding: '6px 12px',
              borderRadius: '6px',
              fontSize: '13px',
              fontWeight: 'bold',
              cursor: 'pointer',
            }}
          >
            💡 Ask about this
          </button>
        </div>
      )}

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
                {selectedText && (
                  <div style={{
                    marginTop: '15px',
                    padding: '12px',
                    background: 'rgba(194, 24, 91, 0.1)',
                    borderRadius: '8px',
                    fontSize: '14px',
                  }}>
                    <strong>📌 Text Selected:</strong>
                    <p style={{ marginTop: '8px', fontSize: '13px' }}>
                      "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"
                    </p>
                  </div>
                )}
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
            {selectedText && (
              <div style={{
                fontSize: '12px',
                padding: '8px 12px',
                background: 'rgba(194, 24, 91, 0.1)',
                borderRadius: '6px',
                marginBottom: '8px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
              }}>
                <span>📎 Using: "{selectedText.substring(0, 50)}{selectedText.length > 50 ? '...' : ''}"</span>
                <button
                  onClick={() => setSelectedText('')}
                  style={{
                    background: 'transparent',
                    border: 'none',
                    color: '#C2185B',
                    cursor: 'pointer',
                    fontSize: '16px',
                    padding: '0 4px',
                  }}
                >
                  ×
                </button>
              </div>
            )}
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={selectedText ? "Ask about the selected text..." : "Ask a question about the book..."}
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
