import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import styles from './Auth.module.css';
import { BACKEND_URL } from '../../config/env';

interface Conversation {
  id: number;
  user_id: number;
  title: string | null;
  created_at: string;
  updated_at: string;
}

interface Message {
  id: number;
  conversation_id: number;
  role: string;
  content: string;
  selected_text: string | null;
  sources: string | null;
  processing_time: number | null;
  created_at: string;
}

interface ConversationDetail extends Conversation {
  messages: Message[];
}

export default function ChatHistory() {
  const { isAuthenticated } = useAuth();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<ConversationDetail | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const getBaseURL = () => {
    return BACKEND_URL;
  };

  useEffect(() => {
    if (isAuthenticated) {
      loadConversations();
    }
  }, [isAuthenticated]);

  const getAuthHeaders = () => {
    const token = localStorage.getItem('auth_session_token');
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
  };

  const loadConversations = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`${getBaseURL()}/api/conversations`, {
        credentials: 'include',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        throw new Error('Failed to load conversations');
      }

      const data = await response.json();
      setConversations(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load conversations');
    } finally {
      setLoading(false);
    }
  };

  const loadConversationDetail = async (conversationId: number) => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`${getBaseURL()}/api/conversations/${conversationId}`, {
        credentials: 'include',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        throw new Error('Failed to load conversation');
      }

      const data = await response.json();
      setSelectedConversation(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load conversation');
    } finally {
      setLoading(false);
    }
  };

  const deleteConversation = async (conversationId: number) => {
    if (!confirm('Are you sure you want to delete this conversation?')) {
      return;
    }

    console.log(`Attempting to delete conversation with ID: ${conversationId}`);
    try {
      const response = await fetch(`${getBaseURL()}/api/conversations/${conversationId}`, {
        method: 'DELETE',
        credentials: 'include',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        console.error(`Failed to delete conversation: Server responded with status ${response.status}`);
        throw new Error('Failed to delete conversation');
      }

      console.log(`Successfully deleted conversation with ID: ${conversationId}`);
      setConversations(conversations.filter(c => c.id !== conversationId));
      if (selectedConversation?.id === conversationId) {
        setSelectedConversation(null);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to delete conversation');
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  if (!isAuthenticated) {
    return (
      <div className={styles.chatHistory}>
        <p>Please sign in to view your chat history.</p>
      </div>
    );
  }

  return (
    <div className={styles.chatHistory}>
      <div className={styles.chatHistoryHeader}>
        <h2>Chat History</h2>
        {conversations.length > 0 && (
          <button onClick={loadConversations} className={styles.refreshButton}>
            Refresh
          </button>
        )}
      </div>

      {error && <div className={styles.error}>{error}</div>}

      {loading && <div className={styles.loading}>Loading...</div>}

      <div className={styles.chatHistoryContent}>
        <div className={styles.conversationsList}>
          <h3>Conversations ({conversations.length})</h3>
          {conversations.length === 0 && !loading && (
            <p className={styles.emptyState}>No conversations yet. Start chatting to create your first conversation!</p>
          )}
          {conversations.map((conv) => (
            <div
              key={conv.id}
              className={`${styles.conversationItem} ${selectedConversation?.id === conv.id ? styles.active : ''}`}
              onClick={() => loadConversationDetail(conv.id)}
            >
              <div className={styles.conversationTitle}>
                {conv.title || 'Untitled Conversation'}
              </div>
              <div className={styles.conversationDate}>
                {formatDate(conv.updated_at)}
              </div>
              <button
                className={styles.deleteButton}
                onClick={(e) => {
                  e.stopPropagation();
                  deleteConversation(conv.id);
                }}
              >
                Delete
              </button>
            </div>
          ))}
        </div>

        {selectedConversation && (
          <div className={styles.conversationDetail}>
            <div className={styles.conversationDetailHeader}>
              <h3>{selectedConversation.title || 'Untitled Conversation'}</h3>
              <button onClick={() => setSelectedConversation(null)} className={styles.closeButton}>
                &times;
              </button>
            </div>
            <div className={styles.messagesList}>
              {selectedConversation.messages.map((msg) => (
                <div key={msg.id} className={`${styles.message} ${styles[msg.role]}`}>
                  <div className={styles.messageRole}>
                    {msg.role === 'user' ? 'You' : 'Assistant'}
                  </div>
                  <div className={styles.messageContent}>{msg.content}</div>
                  {msg.selected_text && (
                    <div className={styles.messageContext}>
                      <strong>Context:</strong> {msg.selected_text}
                    </div>
                  )}
                  {msg.sources && (
                    <div className={styles.messageSources}>
                      <strong>Sources:</strong> {JSON.parse(msg.sources).join(', ')}
                    </div>
                  )}
                  <div className={styles.messageTime}>{formatDate(msg.created_at)}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
