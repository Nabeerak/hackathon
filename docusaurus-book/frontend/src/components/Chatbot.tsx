import React, { useState, useRef, useEffect } from 'react';
import { chatAPI, ChatResponse } from '../services/chat_api';
import { ConversationHistory } from './ConversationHistory';
import './Chatbot.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
  timestamp?: string;
}

export const Chatbot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState<number | undefined>(undefined);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isOpen, setIsOpen] = useState(false);
  const [selectedText, setSelectedText] = useState<string>('');
  const [showHistory, setShowHistory] = useState(false);
  const [selectionPosition, setSelectionPosition] = useState<{ x: number; y: number } | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Add text selection listener only to book content areas
  useEffect(() => {
    const handleSelection = (e: MouseEvent | KeyboardEvent) => {
      const selection = window.getSelection();
      const selectedText = selection?.toString().trim() || '';

      if (selectedText && selection && selection.rangeCount > 0) {
        // Check if the selection is within book content (not chatbot UI)
        const range = selection.getRangeAt(0);
        const container = range.commonAncestorContainer;
        const element = container.nodeType === Node.ELEMENT_NODE
          ? container as Element
          : container.parentElement;

        // Only allow selection from book content areas
        // Exclude chatbot UI and other non-content areas
        const isInBookContent = element?.closest('article, .markdown, main') !== null;
        const isInChatbot = element?.closest('.chatbot-container, .chatbot-toggle, .ask-in-chat-btn, .ask-in-chat-container, .close-selection-btn, .selected-text-indicator') !== null;
        const isInNavbar = element?.closest('.navbar, nav') !== null;
        const isInSidebar = element?.closest('.theme-doc-sidebar-container, aside') !== null;
        const isInFooter = element?.closest('.footer, footer') !== null;

        // Only set selected text if it's from book content and not from excluded areas
        if (isInBookContent && !isInChatbot && !isInNavbar && !isInSidebar && !isInFooter) {
          setSelectedText(selectedText);

          // Get the position of the selection
          const rect = range.getBoundingClientRect();

          // Position the button at the end of the selection
          setSelectionPosition({
            x: rect.right + window.scrollX,
            y: rect.bottom + window.scrollY
          });
        } else {
          setSelectedText('');
          setSelectionPosition(null);
        }
      } else {
        setSelectedText('');
        setSelectionPosition(null);
      }
    };

    document.addEventListener('mouseup', handleSelection as EventListener);
    document.addEventListener('keyup', handleSelection as EventListener);

    return () => {
      document.removeEventListener('mouseup', handleSelection as EventListener);
      document.removeEventListener('keyup', handleSelection as EventListener);
    };
  }, []);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    // If there's selected text, include it in the request
    const userMessage: Message = {
      role: 'user',
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      const response: ChatResponse = await chatAPI.sendMessage({
        conversation_id: conversationId,
        message: input,
        selected_text: selectedText, // Include selected text if available
      });

      setConversationId(response.conversation_id);

      const assistantMessage: Message = {
        role: 'assistant',
        content: typeof response.message === 'string' ? response.message : JSON.stringify(response.message, null, 2),
        sources: response.sources,
        timestamp: response.timestamp,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      // Clear selected text after sending message
      setSelectedText('');
      setSelectionPosition(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
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

  const handleNewConversation = () => {
    setConversationId(undefined);
    setMessages([]);
    setError(null);
    setSelectedText('');
    setSelectionPosition(null);
  };

  const handleConversationSelect = (selectedConvId: number) => {
    // If selecting a conversation, we might want to load its messages
    // For now, just set the conversation ID to connect to that conversation
    setConversationId(selectedConvId);
    setShowHistory(false); // Close history after selection
  };

  // Function to ask a question about selected text
  const handleAskAboutSelection = () => {
    if (!selectedText.trim()) return;

    // Pre-fill the input with a question about the selected text
    setInput(`Explain this: "${selectedText.substring(0, 200)}${selectedText.length > 200 ? '...' : ''}"`);
    // Clear the selection after pre-filling the input
    setSelectedText('');
    setSelectionPosition(null);
  };

  // Function to directly send selected text as a question
  const handleSendSelectedText = async () => {
    if (!selectedText.trim()) return;

    const questionText = `Explain this: "${selectedText}"`;

    const userMessage: Message = {
      role: 'user',
      content: questionText,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    // Clear selected text immediately
    const textToSend = selectedText;
    setSelectedText('');
    setSelectionPosition(null);

    try {
      const response: ChatResponse = await chatAPI.sendMessage({
        conversation_id: conversationId,
        message: questionText,
        selected_text: textToSend,
      });

      setConversationId(response.conversation_id);

      const assistantMessage: Message = {
        role: 'assistant',
        content: typeof response.message === 'string' ? response.message : JSON.stringify(response.message, null, 2),
        sources: response.sources,
        timestamp: response.timestamp,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
    } finally {
      setIsLoading(false);
    }
  };

  // Function to open chatbot with selected text
  const handleAskInChat = () => {
    if (!selectedText.trim()) return;

    // Open the chatbot if it's not already open
    setIsOpen(true);
    // Keep the selected text so it gets included in the context
    // User can then type their question
  };

  return (
    <>
      <button
        className="chatbot-toggle"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle chatbot"
      >
        💬
      </button>

      {/* Ask in Chat button at selection position */}
      {selectedText && selectionPosition && (
        <div
          className="ask-in-chat-container"
          style={{
            position: 'absolute',
            left: `${selectionPosition.x}px`,
            top: `${selectionPosition.y + 5}px`,
            display: 'flex',
            gap: '8px',
            alignItems: 'center',
          }}
        >
          <button
            className="ask-in-chat-btn"
            onClick={handleAskInChat}
          >
            Ask in Chat
          </button>
          <button
            className="close-selection-btn"
            onClick={() => {
              setSelectedText('');
              setSelectionPosition(null);
            }}
            aria-label="Clear selection"
          >
            ×
          </button>
        </div>
      )}

      {/* Display selected text indicator when text is selected */}
      {selectedText && (
        <div className="selected-text-indicator" onClick={handleAskAboutSelection}>
          <span className="selected-text-preview">Selected: "{selectedText.substring(0, 60)}{selectedText.length > 60 ? '...' : ''}"</span>
          <button className="ask-about-selection-btn">Ask about this</button>
        </div>
      )}

      {isOpen && (
        <div className="chatbot-container">
          <div className="chatbot-header">
            <h3>AI Assistant</h3>
            <div className="chatbot-header-actions">
              <button onClick={() => setShowHistory(!showHistory)} className="btn-history">
                {showHistory ? 'Back to Chat' : 'History'}
              </button>
              <button onClick={handleNewConversation} className="btn-new-chat">
                New Chat
              </button>
              <button onClick={() => setIsOpen(false)} className="btn-close">
                ×
              </button>
            </div>
          </div>

          {showHistory ? (
            <div className="chatbot-history-panel">
              <ConversationHistory
                onConversationSelect={handleConversationSelect}
                currentConversationId={conversationId}
              />
            </div>
          ) : (
            <div className="chatbot-messages">
              {messages.length === 0 && !selectedText && (
                <div className="chatbot-welcome">
                  <p>Welcome! Ask me anything about the Physical AI textbook.</p>
                </div>
              )}

              {/* Show selected text card when text is selected */}
              {selectedText && (
                <div className="selected-text-card">
                  <div className="selected-text-header">
                    <span className="selected-text-label">📄 Selected Text</span>
                    <button onClick={() => { setSelectedText(''); setSelectionPosition(null); }} className="close-selected-text">×</button>
                  </div>
                  <div className="selected-text-content">
                    "{selectedText.substring(0, 300)}{selectedText.length > 300 ? '...' : ''}"
                  </div>
                  <div className="selected-text-actions">
                    <button
                      onClick={handleSendSelectedText}
                      className="btn-send-selected"
                      disabled={isLoading}
                    >
                      ✉️ Send Now
                    </button>
                    <button
                      onClick={handleAskAboutSelection}
                      className="btn-ask-about"
                      disabled={isLoading}
                    >
                      ✏️ Edit Question
                    </button>
                  </div>
                </div>
              )}

              {messages.map((msg, index) => (
                <div key={index} className={`message message-${msg.role}`}>
                  <div className="message-content">{msg.content}</div>
                  {msg.sources && msg.sources.length > 0 && (
                    <div className="message-sources">
                      <small>Sources: {msg.sources.join(', ')}</small>
                    </div>
                  )}
                </div>
              ))}

              {isLoading && (
                <div className="message message-assistant">
                  <div className="message-content typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              )}

              {error && (
                <div className="chatbot-error">
                  <p>{error}</p>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>
          )}

          {!showHistory && (
            <div className="chatbot-input-container">
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
                className="btn-send"
              >
                Send
              </button>
            </div>
          )}
        </div>
      )}
    </>
  );
};

export default Chatbot;
