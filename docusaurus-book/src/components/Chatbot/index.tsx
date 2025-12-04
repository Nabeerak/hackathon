import React, { useState, useRef, useEffect } from 'react';
import styles from './styles.module.css';
import { chatAPI } from '../../services/chat_api';
import { useAuth } from '../../contexts/AuthContext';
import AuthModal from '../Auth/AuthModal';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function Chatbot() {
  const { isAuthenticated, isPending } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);
  const [selectedText, setSelectedText] = useState<string>('');
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Add text selection listener only to book content areas
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const selectedText = selection?.toString().trim() || '';

      if (selectedText && selectedText.length > 10 && selection && selection.rangeCount > 0) {
        // Check if the selection is within book content (not chatbot UI)
        const range = selection.getRangeAt(0);
        const container = range.commonAncestorContainer;
        const element = container.nodeType === Node.ELEMENT_NODE
          ? container as Element
          : container.parentElement;

        // Only allow selection from book content areas
        // Exclude chatbot UI and other non-content areas
        const isInBookContent = element?.closest('article, .markdown, main') !== null;
        const isInChatbot = element?.closest('[class*="chatbot"], [class*="Chatbot"]') !== null;
        const isInNavbar = element?.closest('.navbar, nav') !== null;
        const isInSidebar = element?.closest('.theme-doc-sidebar-container, aside') !== null;
        const isInFooter = element?.closest('.footer, footer') !== null;

        // Only set selected text if it's from book content and not from excluded areas
        if (isInBookContent && !isInChatbot && !isInNavbar && !isInSidebar && !isInFooter) {
          setSelectedText(selectedText);
        } else {
          setSelectedText('');
        }
      } else {
        setSelectedText('');
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
        content: typeof response.message === 'string' ? response.message : JSON.stringify(response.message, null, 2),
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
          style={{
            position: 'fixed',
            bottom: '100px',
            right: '20px',
            background: 'linear-gradient(135deg, #C2185B 0%, #1565C0 100%)',
            color: 'white',
            padding: '12px 20px',
            borderRadius: '12px',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.2)',
            maxWidth: '300px',
            zIndex: 999,
            display: 'flex',
            flexDirection: 'column',
            gap: '8px',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '8px' }}>
            <div style={{ fontSize: '12px', opacity: 0.9, flex: 1 }}>
              Selected: "{selectedText.substring(0, 60)}{selectedText.length > 60 ? '...' : ''}"
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation();
                setSelectedText('');
              }}
              style={{
                background: 'transparent',
                border: 'none',
                color: 'white',
                cursor: 'pointer',
                fontSize: '20px',
                padding: '0',
                lineHeight: '1',
                opacity: 0.8,
                transition: 'opacity 0.2s',
              }}
              onMouseEnter={(e) => e.currentTarget.style.opacity = '1'}
              onMouseLeave={(e) => e.currentTarget.style.opacity = '0.8'}
              aria-label="Clear selection"
            >
              ×
            </button>
          </div>
          <button
            onClick={handleAskAboutSelection}
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
            {!isAuthenticated && !isPending && (
              <div className={styles.chatbotWelcome}>
                <p style={{ fontSize: '16px', marginBottom: '16px' }}>🔒 Sign in Required</p>
                <p style={{ marginBottom: '20px' }}>Please sign in to use the AI Assistant and get personalized responses about the Physical AI textbook.</p>
                <button
                  onClick={() => setAuthModalOpen(true)}
                  style={{
                    display: 'inline-block',
                    padding: '12px 24px',
                    background: 'linear-gradient(135deg, #C2185B 0%, #1565C0 100%)',
                    color: 'white',
                    border: 'none',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    fontWeight: 600,
                    fontSize: '14px',
                  }}
                >
                  Sign In / Sign Up
                </button>
              </div>
            )}

            {isAuthenticated && messages.length === 0 && (
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

            {isPending && (
              <div className={styles.chatbotWelcome}>
                <p>Loading...</p>
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

          {isAuthenticated && (
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
          )}
        </div>
      )}

      {/* Auth Modal */}
      <AuthModal
        isOpen={authModalOpen}
        onClose={() => setAuthModalOpen(false)}
        initialMode="signin"
      />
    </>
  );
}
