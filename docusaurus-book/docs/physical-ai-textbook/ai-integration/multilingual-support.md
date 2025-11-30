---
title: Multilingual Support
sidebar_label: Multilingual Support
sidebar_position: 3
description: Urdu translation and multilingual content delivery for Physical AI textbook
keywords: [multilingual, Urdu, translation, i18n, localization]
---

# Multilingual Support

## Introduction

This chapter covers implementing multilingual support for your Physical AI textbook, with a focus on Urdu translation as required by the constitution. The system allows logged-in users to translate content into Urdu by pressing a button at the start of each chapter.

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │───▶│   Translation    │───▶│   OpenAI        │
│   (Docusaurus)  │    │   Service        │    │   Translation   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Language        │
                    │  Preferences     │
                    └──────────────────┘
```

## Technology Stack

### OpenAI Translation API
- **Purpose**: AI-powered translation services
- **Model**: GPT-4 for accurate and contextual translation
- **Features**:
  - Context-aware translation
  - Technical terminology handling
  - Cultural adaptation
  - Quality consistency

### Translation Caching
- **Purpose**: Store translated content to reduce API costs and improve performance
- **Options**:
  - Redis for fast access
  - Database for persistent storage
  - CDN for global distribution

## Translation Service Implementation

### Core Translation Service

```python
# translation_service.py
import openai
import json
import logging
from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum
import asyncio
import aiohttp
from functools import lru_cache

logger = logging.getLogger(__name__)

class Language(Enum):
    ENGLISH = "en"
    URDU = "ur"

@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence: float
    timestamp: str

class TranslationService:
    def __init__(self, openai_api_key: str, cache_enabled: bool = True):
        openai.api_key = openai_api_key
        self.cache_enabled = cache_enabled
        self.translation_cache = {}
        
    async def translate_text(self, text: str, target_language: Language) -> TranslationResult:
        """
        Translate text to target language using OpenAI.
        
        Args:
            text: Text to translate
            target_language: Target language code
            
        Returns:
            TranslationResult with translated text and metadata
        """
        # Check cache first
        cache_key = f"{text[:50]}_{target_language.value}"
        if self.cache_enabled and cache_key in self.translation_cache:
            logger.info("Returning cached translation")
            return self.translation_cache[cache_key]
        
        try:
            # Prepare the translation prompt
            system_prompt = self._get_system_prompt(target_language)
            user_prompt = self._get_user_prompt(text, target_language)
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=len(text) * 2,  # Allow for longer Urdu text
                timeout=30
            )
            
            translated_text = response.choices[0].message.content.strip()
            
            # Remove any translation artifacts
            translated_text = self._clean_translation(translated_text)
            
            result = TranslationResult(
                original_text=text,
                translated_text=translated_text,
                source_language="en",
                target_language=target_language.value,
                confidence=0.9,  # GPT-4 is generally reliable
                timestamp=str(response.created)
            )
            
            # Cache the result
            if self.cache_enabled:
                self.translation_cache[cache_key] = result
            
            return result
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            # Return original text with error indication
            return TranslationResult(
                original_text=text,
                translated_text=f"[TRANSLATION ERROR: {text}]",
                source_language="en",
                target_language=target_language.value,
                confidence=0.0,
                timestamp=""
            )
    
    def _get_system_prompt(self, target_language: Language) -> str:
        """Get system prompt for translation."""
        if target_language == Language.URDU:
            return """
            You are a professional translator specializing in technical content, particularly for robotics, AI, and computer science education. 
            Translate the given text from English to Urdu while maintaining:
            1. Technical accuracy of terms (ROS 2, NVIDIA Isaac, etc.)
            2. Educational context and meaning
            3. Cultural appropriateness for Urdu-speaking audience
            4. Preservation of code snippets and technical examples in English
            5. Academic tone appropriate for textbook content
            
            For technical terms that don't have direct Urdu equivalents, keep the English term but provide context.
            """
        else:
            # Default to English explanation if needed
            return "You are a professional translator focusing on educational and technical content."
    
    def _get_user_prompt(self, text: str, target_language: Language) -> str:
        """Format user prompt for translation."""
        if target_language == Language.URDU:
            return f"""
            Translate the following English text to Urdu. Ensure technical accuracy for robotics and AI education:

            {text}

            Translation (Urdu):
            """
        else:
            return text
    
    def _clean_translation(self, text: str) -> str:
        """Clean translation artifacts."""
        # Remove common translation artifacts
        text = text.replace("(Urdu):", "").replace("Translation (Urdu):", "")
        text = text.strip()
        
        # Handle common formatting issues
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        
        return text
    
    async def translate_document(self, document: Dict[str, any], target_language: Language) -> Dict[str, any]:
        """
        Translate an entire document (with metadata, content structure).
        
        Args:
            document: Document with content, title, etc.
            target_language: Target language
            
        Returns:
            Translated document
        """
        translated_doc = document.copy()
        
        # Translate main content
        if 'content' in translated_doc:
            content_result = await self.translate_text(translated_doc['content'], target_language)
            translated_doc['content'] = content_result.translated_text
        
        # Translate title
        if 'title' in translated_doc:
            title_result = await self.translate_text(translated_doc['title'], target_language)
            translated_doc['title_ur'] = title_result.translated_text
        
        # Translate other metadata
        if 'description' in translated_doc:
            desc_result = await self.translate_text(translated_doc['description'], target_language)
            translated_doc['description_ur'] = desc_result.translated_text
        
        if 'keywords' in translated_doc:
            translated_keywords = []
            for keyword in translated_doc['keywords']:
                keyword_result = await self.translate_text(keyword, target_language)
                translated_keywords.append(keyword_result.translated_text)
            translated_doc['keywords_ur'] = translated_keywords
        
        return translated_doc
```

### Translation API Endpoints

```python
# translation_api.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import logging

from .translation_service import TranslationService, Language, TranslationResult
from app.core.config import settings
from app.dependencies import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

class TranslateRequest(BaseModel):
    text: str
    target_language: str = "ur"  # Default to Urdu
    preserve_code: bool = True

class TranslateResponse(BaseModel):
    original: str
    translated: str
    source_language: str
    target_language: str
    confidence: float

class TranslateDocumentRequest(BaseModel):
    title: str
    content: str
    description: Optional[str] = ""
    keywords: Optional[List[str]] = []
    target_language: str = "ur"

class TranslateDocumentResponse(BaseModel):
    title: str
    content: str
    description: Optional[str] = ""
    keywords: Optional[List[str]] = []
    source_language: str
    target_language: str

@router.post("/translate", response_model=TranslateResponse)
async def translate_text(
    request: TranslateRequest,
    user = Depends(get_current_user)
):
    """Translate text to target language (Urdu by default)."""
    try:
        if request.target_language.lower() != "ur":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Currently only Urdu translation is supported"
            )
        
        translation_service = TranslationService(settings.OPENAI_API_KEY)
        result = await translation_service.translate_text(
            request.text,
            Language.URDU
        )
        
        return TranslateResponse(
            original=result.original_text,
            translated=result.translated_text,
            source_language=result.source_language,
            target_language=result.target_language,
            confidence=result.confidence
        )
    except Exception as e:
        logger.error(f"Translation API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Translation service error"
        )

@router.post("/translate-document", response_model=TranslateDocumentResponse)
async def translate_document(
    request: TranslateDocumentRequest,
    user = Depends(get_current_user)
):
    """Translate an entire document."""
    try:
        translation_service = TranslationService(settings.OPENAI_API_KEY)
        
        # Create document structure
        document = {
            "title": request.title,
            "content": request.content,
            "description": request.description,
            "keywords": request.keywords
        }
        
        translated_doc = await translation_service.translate_document(
            document,
            Language.URDU
        )
        
        # Build response
        response = TranslateDocumentResponse(
            title=translated_doc.get('title_ur', request.title),
            content=translated_doc.get('content', request.content),
            description=translated_doc.get('description_ur', request.description),
            keywords=translated_doc.get('keywords_ur', request.keywords),
            source_language="en",
            target_language="ur"
        )
        
        return response
    except Exception as e:
        logger.error(f"Document translation API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Document translation service error"
        )

@router.get("/supported-languages")
async def get_supported_languages():
    """Get list of supported languages."""
    return {
        "supported": [
            {"code": "en", "name": "English", "default": True},
            {"code": "ur", "name": "Urdu", "default": False}
        ],
        "default": "en"
    }
```

## Frontend Translation Component

### Translation Button Component

```tsx
// src/components/TranslationButton.tsx
import React, { useState, useEffect } from 'react';
import { useSession } from 'better-auth/react';
import { useLanguage } from '../contexts/LanguageContext';

interface TranslationButtonProps {
  content: string;
  title: string;
  onTranslationComplete?: (translatedContent: string, title: string) => void;
}

const TranslationButton: React.FC<TranslationButtonProps> = ({ 
  content, 
  title, 
  onTranslationComplete 
}) => {
  const [isTranslating, setIsTranslating] = useState(false);
  const [isTranslated, setIsTranslated] = useState(false);
  const [translatedContent, setTranslatedContent] = useState('');
  const [translatedTitle, setTranslatedTitle] = useState('');
  const { session } = useSession();
  const { currentLanguage, setLanguage } = useLanguage();
  
  const handleTranslate = async () => {
    if (!session) {
      alert('Please log in to access translation features');
      return;
    }
    
    if (currentLanguage === 'ur' && isTranslated) {
      // Switch back to English
      setTranslatedContent('');
      setTranslatedTitle('');
      setIsTranslated(false);
      setLanguage('en');
      return;
    }
    
    setIsTranslating(true);
    
    try {
      // Call translation API
      const response = await fetch('/api/translate/translate-document', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.access_token}`, // if using tokens
        },
        body: JSON.stringify({
          title,
          content,
          target_language: 'ur'
        }),
      });
      
      if (response.ok) {
        const data = await response.json();
        setTranslatedContent(data.content);
        setTranslatedTitle(data.title);
        setIsTranslated(true);
        setLanguage('ur');
        
        // Notify parent component
        if (onTranslationComplete) {
          onTranslationComplete(data.content, data.title);
        }
      } else {
        const error = await response.json();
        throw new Error(error.detail || 'Translation failed');
      }
    } catch (error) {
      console.error('Translation error:', error);
      alert(`Translation error: ${error.message}`);
    } finally {
      setIsTranslating(false);
    }
  };
  
  // Effect to reset when content changes
  useEffect(() => {
    if (!isTranslating) {
      setIsTranslated(false);
      setTranslatedContent('');
      setTranslatedTitle('');
    }
  }, [content]);
  
  // Get button text based on current state
  let buttonText = 'Translate to Urdu';
  if (isTranslating) {
    buttonText = 'Translating...';
  } else if (isTranslated && currentLanguage === 'ur') {
    buttonText = 'Switch to English';
  }
  
  return (
    <div className="translation-controls">
      <button 
        onClick={handleTranslate}
        disabled={isTranslating || !session}
        className={`translate-btn ${isTranslating ? 'loading' : ''} ${isTranslated ? 'translated' : ''}`}
      >
        {buttonText}
      </button>
      
      {isTranslating && (
        <div className="translation-progress">
          <div className="spinner"></div>
          <span>Translating content...</span>
        </div>
      )}
    </div>
  );
};

export default TranslationButton;
```

### Language Context Provider

```tsx
// src/contexts/LanguageContext.tsx
import React, { createContext, useContext, useState, ReactNode } from 'react';

interface LanguageContextType {
  currentLanguage: string;
  availableLanguages: Array<{ code: string; name: string }>;
  setLanguage: (lang: string) => void;
  isUrdu: boolean;
  getTextDirection: (lang?: string) => 'ltr' | 'rtl';
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

const defaultAvailableLanguages = [
  { code: 'en', name: 'English' },
  { code: 'ur', name: 'Urdu' },
];

export const LanguageProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState<string>('en');
  const [availableLanguages] = useState(defaultAvailableLanguages);
  
  const setLanguage = (lang: string) => {
    if (availableLanguages.some(l => l.code === lang)) {
      setCurrentLanguage(lang);
    }
  };
  
  const isUrdu = currentLanguage === 'ur';
  
  const getTextDirection = (lang?: string): 'ltr' | 'rtl' => {
    const checkLang = lang || currentLanguage;
    return checkLang === 'ur' ? 'rtl' : 'ltr';
  };
  
  const value: LanguageContextType = {
    currentLanguage,
    availableLanguages,
    setLanguage,
    isUrdu,
    getTextDirection,
  };
  
  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};
```

### Urdu-Specific Styling

```css
/* src/components/UrduContent.module.css */
.urdu-content {
  font-family: 'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', 'Urdu Typesetting', serif;
  direction: rtl;
  text-align: right;
  line-height: 1.8;
}

.urdu-content h1,
.urdu-content h2,
.urdu-content h3 {
  font-family: 'Noto Sans Arabic', sans-serif;
  font-weight: bold;
  margin: 1.5em 0 0.5em 0;
}

.urdu-content p {
  margin: 0.8em 0;
}

.urdu-content li {
  margin: 0.5em 0;
}

/* Ensure code blocks remain LTR */
.urdu-content pre,
.urdu-content code {
  direction: ltr;
  text-align: left;
  font-family: 'Courier New', Consolas, monospace;
}

.urdu-content .code-block {
  text-align: left;
  direction: ltr;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .urdu-content {
    font-size: 16px;
    padding: 10px;
  }
}
```

## Advanced Translation Features

### Smart Content Detection

```python
# translation_intelligence.py
import re
from typing import Dict, List
from enum import Enum

class ContentCategory(Enum):
    CODE = "code"
    MATH = "math"
    TECHNICAL = "technical"
    EDUCATIONAL = "educational"
    GENERAL = "general"

class TranslationIntelligence:
    def __init__(self):
        self.code_patterns = [
            r'```.*?```',  # Code blocks
            r'`[^`]+`',    # Inline code
            r'function\s+\w+',  # Function definitions
            r'class\s+\w+',     # Class definitions
            r'import\s+\w+',    # Imports
        ]
        
        self.tech_terms = {
            'ROS 2': 'ROS 2',
            'NVIDIA Isaac': 'NVIDIA آئزیک',
            'Gazebo': 'گزیبو',
            'Unity': 'یونیٹی',
            'SLAM': 'SLAM',
            'PID': 'PID',
            'URDF': 'URDF',
            # Add more technical terms as needed
        }
    
    def categorize_content(self, text: str) -> List[ContentCategory]:
        """Categorize content segments for appropriate translation."""
        categories = []
        
        # Check for code patterns
        for pattern in self.code_patterns:
            if re.search(pattern, text, re.DOTALL | re.IGNORECASE):
                categories.append(ContentCategory.CODE)
        
        # Check for math expressions
        if re.search(r'\$\$.*?\$\$|\$.*?\$', text) or re.search(r'\\begin\{equation\}.*?\\end\{equation\}', text):
            categories.append(ContentCategory.MATH)
        
        # Check for technical terms
        text_lower = text.lower()
        for term in ['function', 'class', 'variable', 'algorithm', 'protocol']:
            if term in text_lower:
                categories.append(ContentCategory.TECHNICAL)
                break
        
        # Default to educational if not specifically identified
        if not categories:
            categories.append(ContentCategory.EDUCATIONAL)
        
        return categories
    
    def preprocess_for_translation(self, text: str) -> Dict[str, any]:
        """Preprocess text to preserve code and technical elements."""
        segments = []
        current_pos = 0
        preserved_elements = {}
        
        # Find code blocks and preserve them
        for pattern in self.code_patterns:
            for match in re.finditer(pattern, text, re.DOTALL):
                # Add text before match
                if match.start() > current_pos:
                    segments.append({
                        'type': 'text',
                        'content': text[current_pos:match.start()]
                    })
                
                # Preserve the code block
                placeholder = f"{{CODE_BLOCK_{len(preserved_elements)}}}"
                segments.append({
                    'type': 'code',
                    'content': placeholder
                })
                
                preserved_elements[placeholder] = match.group(0)
                current_pos = match.end()
        
        # Add remaining text
        if current_pos < len(text):
            segments.append({
                'type': 'text',
                'content': text[current_pos:]
            })
        
        return {
            'segments': segments,
            'preserved_elements': preserved_elements
        }
    
    def postprocess_translation(self, translation: str, preserved_elements: Dict[str, str]) -> str:
        """Restore preserved elements to translated text."""
        result = translation
        for placeholder, original_content in preserved_elements.items():
            result = result.replace(placeholder, original_content)
        
        return result
```

### Translation Quality Assurance

```python
# quality_assurance.py
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class QualityIssue:
    type: str
    severity: str  # 'critical', 'warning', 'info'
    message: str
    position: int

class TranslationQualityAssurance:
    def __init__(self):
        self.urdu_unicode_range = r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]'
    
    def check_urdu_quality(self, text: str) -> List[QualityIssue]:
        """Check translation quality for Urdu text."""
        issues = []
        
        # Check if text contains Urdu characters
        if not re.search(self.urdu_unicode_range, text):
            issues.append(QualityIssue(
                type='language_check',
                severity='critical',
                message='Translation does not contain Urdu characters',
                position=0
            ))
        
        # Check for English words in Urdu text (should be minimal)
        english_words = re.findall(r'\b[A-Za-z]{3,}\b', text)
        if len(english_words) > len(text.split()) * 0.3:  # More than 30% English
            issues.append(QualityIssue(
                type='language_mixing',
                severity='warning',
                message=f'High percentage of English words: {english_words[:5]} (showing first 5)',
                position=0
            ))
        
        # Check for common translation artifacts
        if 'TRANSLATION ERROR' in text:
            issues.append(QualityIssue(
                type='translation_error',
                severity='critical',
                message='Translation contains error placeholders',
                position=text.find('TRANSLATION ERROR')
            ))
        
        # Check for proper Urdu punctuation
        if re.search(r'[.,!?;:]\s*[^\s]', text):  # English punctuation followed by non-space
            issues.append(QualityIssue(
                type='punctuation',
                severity='warning',
                message='Possible punctuation issue - English punctuation in Urdu text',
                position=0
            ))
        
        return issues
    
    def suggest_improvements(self, original: str, translation: str) -> List[str]:
        """Suggest improvements for the translation."""
        suggestions = []
        
        # Check if technical terms were translated appropriately
        tech_terms = ['ROS 2', 'NVIDIA Isaac', 'Gazebo', 'Unity', 'SLAM', 'PID', 'URDF']
        for term in tech_terms:
            if term in original and term not in translation:
                suggestions.append(f'Consider keeping "{term}" in English as it is a technical term')
        
        return suggestions
```

## Integration with Docusaurus

### Docusaurus Plugin for Translation

```js
// docusaurus.config.js - Add to plugins
module.exports = {
  // ... other config
  plugins: [
    // ... other plugins
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'translation',
        path: 'docs/translation',
        routeBasePath: 'translation',
        sidebarPath: require.resolve('./sidebarsTranslation.js'),
      },
    ],
  ],
  
  themeConfig: {
    navbar: {
      items: [
        // ... other navbar items
        {
          type: 'dropdown',
          label: 'Translate',
          position: 'right',
          items: [
            {
              label: 'Urdu',
              to: '/translation/urdu',
            },
            {
              label: 'English',
              to: '/translation/english',
            },
          ],
        },
      ],
    },
  },
};
```

### Translation-Aware Layout

```jsx
// src/theme/Layout/index.js
import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import { LanguageProvider } from '@site/src/contexts/LanguageContext';
import { UserProfileProvider } from '@site/src/contexts/UserProfileContext';
import TranslationButton from '@site/src/components/TranslationButton';

export default function Layout(props) {
  return (
    <LanguageProvider>
      <UserProfileProvider>
        <OriginalLayout {...props} />
        <TranslationButton 
          content={props.children?.props?.content || ''}
          title={props.children?.props?.title || 'Content'}
        />
      </UserProfileProvider>
    </LanguageProvider>
  );
}
```

### Chapter-Level Translation Component

```jsx
// src/components/ChapterTranslation.jsx
import React from 'react';
import { useLocation } from '@docusaurus/router';
import TranslationButton from './TranslationButton';

const ChapterTranslation = ({ children, title }) => {
  const location = useLocation();
  
  // Extract chapter path for potential caching/identification
  const chapterPath = location.pathname;
  
  return (
    <div className="chapter-with-translation">
      <TranslationButton 
        content={children}
        title={title || chapterPath}
      />
      <div className="chapter-content">
        {children}
      </div>
    </div>
  );
};

export default ChapterTranslation;
```

## Performance Optimization

### Translation Caching Strategy

```python
# translation_cache.py
import redis
import json
from typing import Optional, Dict, Any
import hashlib
import time

class TranslationCache:
    def __init__(self, redis_url: str = "redis://localhost:6379/0", ttl: int = 86400):  # 24 hours
        self.redis_client = redis.from_url(redis_url)
        self.ttl = ttl
    
    def _generate_cache_key(self, text: str, target_lang: str) -> str:
        """Generate a cache key for the text and language combination."""
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return f"translation:{target_lang}:{text_hash}"
    
    def get(self, text: str, target_lang: str) -> Optional[Dict[str, Any]]:
        """Get cached translation if available."""
        cache_key = self._generate_cache_key(text, target_lang)
        cached_data = self.redis_client.get(cache_key)
        
        if cached_data:
            return json.loads(cached_data)
        return None
    
    def set(self, text: str, target_lang: str, translation: str, confidence: float) -> bool:
        """Cache the translation."""
        cache_key = self._generate_cache_key(text, target_lang)
        data = {
            "translation": translation,
            "confidence": confidence,
            "timestamp": time.time()
        }
        
        return self.redis_client.setex(cache_key, self.ttl, json.dumps(data))
    
    def invalidate(self, text: str, target_lang: str) -> bool:
        """Invalidate a specific cache entry."""
        cache_key = self._generate_cache_key(text, target_lang)
        return bool(self.redis_client.delete(cache_key))
```

### Batch Translation for Performance

```python
# batch_translation.py
from typing import List, Dict
import asyncio
from .translation_service import TranslationService, Language

class BatchTranslationService:
    def __init__(self, translation_service: TranslationService):
        self.service = translation_service
    
    async def translate_batch(
        self, 
        texts: List[str], 
        target_language: Language,
        max_concurrent: int = 5
    ) -> List[str]:
        """Translate multiple texts concurrently with rate limiting."""
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def translate_with_semaphore(text: str):
            async with semaphore:
                result = await self.service.translate_text(text, target_language)
                return result.translated_text
        
        tasks = [translate_with_semaphore(text) for text in texts]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions
        translated_texts = []
        for result in results:
            if isinstance(result, Exception):
                translated_texts.append(f"[TRANSLATION ERROR: {str(result)}]")
            else:
                translated_texts.append(result)
        
        return translated_texts
```

## Deployment and Scaling

### Containerized Translation Service

```dockerfile
# Dockerfile.translation
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose translation API port
EXPOSE 8001

# Run the translation service
CMD ["uvicorn", "app.translation.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Multi-Service Architecture

```yaml
# docker-compose.translation.yml
version: '3.8'

services:
  translation-api:
    build:
      context: .
      dockerfile: Dockerfile.translation
    ports:
      - "8001:8001"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
    volumes:
      - ./logs:/app/logs

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

## Security Considerations

### API Rate Limiting for Translation

```python
# rate_limiting.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

# Rate limits for translation API
@limiter.limit("100/minute")  # 100 translations per minute per IP
async def translate_text_endpoint():
    # ... translation logic
    pass

@limiter.limit("50/hour")  # 50 document translations per hour
async def translate_document_endpoint():
    # ... document translation logic
    pass
```

### Content Validation

```python
# content_validation.py
import re
from typing import List

class ContentValidator:
    def __init__(self):
        self.sensitive_patterns = [
            r'hate[ -_]speech',
            r'profanity',
            r'violence',
            # Add more patterns as needed
        ]
    
    def validate_for_translation(self, text: str) -> bool:
        """Validate content before translation."""
        text_lower = text.lower()
        
        for pattern in self.sensitive_patterns:
            if re.search(pattern, text_lower):
                return False
        
        return True
    
    def sanitize_content(self, text: str) -> str:
        """Sanitize content for translation."""
        # Remove any potentially harmful content
        sanitized = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
        sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
        
        return sanitized
```

## Summary

The multilingual support system provides:

- ✅ OpenAI-powered Urdu translation for textbook content
- ✅ User authentication requirement for translation access
- ✅ Translation caching for performance and cost optimization
- ✅ Content preservation (code blocks, technical terms) during translation
- ✅ Quality assurance and validation for translations
- ✅ RTL (right-to-left) layout support for Urdu
- ✅ Integration with Docusaurus documentation framework
- ✅ Rate limiting and security measures

## Implementation Steps

1. **Setup Translation Service**: Configure OpenAI API for translation
2. **Create Translation API**: Build endpoints for document translation
3. **Develop Frontend Component**: Create translation button UI
4. **Implement Caching**: Add Redis for translation caching
5. **Add Language Context**: Create context for language management
6. **Integrate with Authentication**: Ensure only logged-in users can translate
7. **Test Translation Quality**: Validate Urdu translations for accuracy
8. **Deploy**: Set up translation microservice in production

## Next Steps

- Integrate with the RAG chatbot for multilingual responses
- Add more languages beyond Urdu
- Implement Claude Code subagents for translation quality assurance
- Connect to the full Physical AI textbook content