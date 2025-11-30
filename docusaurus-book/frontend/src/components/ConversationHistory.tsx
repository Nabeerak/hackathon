import React, { useState, useEffect } from 'react';
import { conversationAPI, Conversation, ConversationDetail } from '../services/conversation_api';
import './ConversationHistory.css';

interface ConversationHistoryProps {
  onConversationSelect?: (conversationId: string) => void;
  currentConversationId?: string;
}

export const ConversationHistory: React.FC<ConversationHistoryProps> = ({
  onConversationSelect,
  currentConversationId
}) => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<ConversationDetail | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearchActive, setIsSearchActive] = useState(false);

  const loadConversations = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await conversationAPI.getConversations();
      setConversations(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load conversations');
    } finally {
      setIsLoading(false);
    }
  };

  const searchConversations = async () => {
    if (!searchQuery.trim()) return;

    setIsLoading(true);
    setError(null);
    try {
      const response = await conversationAPI.searchConversations(searchQuery);
      setConversations(response);
      setIsSearchActive(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to search conversations');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    searchConversations();
  };

  const clearSearch = () => {
    setSearchQuery('');
    setIsSearchActive(false);
    loadConversations();
  };

  const handleConversationSelect = async (conversationId: string) => {
    try {
      const detail = await conversationAPI.getConversation(conversationId);
      setSelectedConversation(detail);
      if (onConversationSelect) {
        onConversationSelect(conversationId);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load conversation');
    }
  };

  const handleDeleteConversation = async (conversationId: string) => {
    if (window.confirm('Are you sure you want to delete this conversation?')) {
      try {
        await conversationAPI.deleteConversation(conversationId);
        if (conversationId === selectedConversation?.id) {
          setSelectedConversation(null);
        }
        loadConversations(); // Reload the list
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to delete conversation');
      }
    }
  };

  const handleExportConversation = async (conversationId: string, title: string) => {
    setIsExporting(true);
    setError(null);
    try {
      const filename = `${title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}_${conversationId}.json`;
      await conversationAPI.downloadConversation(conversationId, filename);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to export conversation');
    } finally {
      setIsExporting(false);
    }
  };

  const handleNewConversation = () => {
    setSelectedConversation(null);
    if (onConversationSelect) {
      onConversationSelect(''); // Signal to start new conversation
    }
  };

  useEffect(() => {
    loadConversations();
  }, []);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="conversation-history">
      <div className="conversation-header">
        <h3>Conversation History</h3>
        <button onClick={handleNewConversation} className="btn-new-conversation">
          New Chat
        </button>
      </div>

      <form onSubmit={handleSearchSubmit} className="search-form">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search conversations..."
          className="search-input"
        />
        <button type="submit" className="search-button">Search</button>
        {isSearchActive && (
          <button type="button" onClick={clearSearch} className="clear-search-button">
            Clear
          </button>
        )}
      </form>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {isLoading ? (
        <div className="loading">Loading conversations...</div>
      ) : (
        <div className="conversations-list">
          {conversations.length === 0 ? (
            <div className="no-conversations">No conversations found</div>
          ) : (
            conversations.map((conv) => (
              <div
                key={conv.id}
                className={`conversation-item ${
                  selectedConversation?.id === conv.id ? 'selected' : ''
                } ${
                  currentConversationId === conv.id ? 'current' : ''
                }`}
              >
                <div
                  className="conversation-preview"
                  onClick={() => handleConversationSelect(conv.id)}
                >
                  <h4>{conv.title}</h4>
                  <div className="conversation-meta">
                    <span className="date">{formatDate(conv.updated_at)}</span>
                    <span className="message-count">{conv.message_count} messages</span>
                  </div>
                </div>
                <div className="conversation-actions">
                  <button
                    onClick={() => handleExportConversation(conv.id, conv.title)}
                    className="export-button"
                    title="Export conversation"
                    disabled={isExporting}
                  >
                    {isExporting ? 'Exporting...' : '↓'}
                  </button>
                  <button
                    onClick={() => handleDeleteConversation(conv.id)}
                    className="delete-button"
                    title="Delete conversation"
                  >
                    ×
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {selectedConversation && (
        <div className="conversation-detail">
          <div className="conversation-detail-header">
            <h4>{selectedConversation.title}</h4>
            <div className="conversation-actions">
              <button
                onClick={() => handleExportConversation(selectedConversation.id, selectedConversation.title)}
                className="export-button"
                title="Export conversation"
                disabled={isExporting}
              >
                {isExporting ? 'Exporting...' : 'Export'}
              </button>
              <span className="conversation-date">
                {formatDate(selectedConversation.created_at)}
              </span>
            </div>
          </div>

          <div className="conversation-messages">
            {selectedConversation.messages.map((msg, index) => (
              <div key={index} className={`message ${msg.role}`}>
                <div className="message-content">{msg.content}</div>
                <div className="message-timestamp">
                  {formatDate(msg.timestamp)}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ConversationHistory;