import React, { useState } from 'react';
import { searchAPI, SearchResponse, SearchResponseItem } from '../services/search_api';
import './BookSearch.css';

interface BookSearchProps {
  onResultClick?: (content: string) => void;
}

export const BookSearch: React.FC<BookSearchProps> = ({ onResultClick }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResponseItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showResults, setShowResults] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    setError(null);
    try {
      const response = await searchAPI.search(query);
      setResults(response.results);
      setShowResults(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to search');
      setResults([]);
      setShowResults(true);
    } finally {
      setIsLoading(false);
    }
  };

  const handleResultClick = (content: string) => {
    if (onResultClick) {
      onResultClick(content);
    }
  };

  return (
    <div className="book-search">
      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search book content..."
          className="search-input"
        />
        <button type="submit" className="search-button" disabled={isLoading}>
          {isLoading ? 'Searching...' : 'Search'}
        </button>
      </form>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {showResults && (
        <div className="search-results">
          {results.length === 0 && !error && (
            <div className="no-results">No results found for "{query}"</div>
          )}
          
          {results.map((result, index) => (
            <div key={result.id || index} className="search-result-item">
              <div 
                className="result-content" 
                onClick={() => handleResultClick(result.content)}
              >
                <h4 className="result-title">Match {index + 1}</h4>
                <p className="result-preview">{result.content}</p>
                <div className="result-meta">
                  <span className="result-source">Source: {result.source}</span>
                  <span className="result-score">Relevance: {(result.score * 100).toFixed(1)}%</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default BookSearch;