"""
Language service.

Manages programming language lexers and registration.
"""

from typing import Dict, Optional, Any
from pygments.lexer import Lexer

class LanguageService:
    """
    Service for managing programming language lexers.
    
    Provides a registry for Pygments lexers and language metadata.
    """
    
    def __init__(self):
        """Initialize the language service."""
        self._languages: Dict[str, Any] = {}
        self._current_language: Optional[str] = None
    
    def register_language(self, name: str, lexer: Lexer) -> None:
        """
        Register a language with its lexer.
        
        Args:
            name: Language name (e.g., 'python', 'javascript')
            lexer: Pygments lexer instance
        """
        self._languages[name] = lexer
    
    def get_lexer(self, name: str) -> Optional[Any]:
        """
        Get the lexer for a language.
        
        Args:
            name: Language name
            
        Returns:
            Lexer instance or None if not found
        """
        return self._languages.get(name)
    
    def set_current_language(self, name: str) -> bool:
        """
        Set the current active language.
        
        Args:
            name: Language name
            
        Returns:
            True if language exists and was set, False otherwise
        """
        if name in self._languages:
            self._current_language = name
            return True
        return False
    
    def get_current_language(self) -> Optional[str]:
        """
        Get the current language name.
        
        Returns:
            Current language name or None
        """
        return self._current_language
    
    def get_current_lexer(self) -> Optional[Any]:
        """
        Get the lexer for the current language.
        
        Returns:
            Current lexer or None
        """
        if self._current_language:
            return self._languages.get(self._current_language)
        return None
    
    def has_language(self, name: str) -> bool:
        """
        Check if a language is registered.
        
        Args:
            name: Language name
            
        Returns:
            True if language is registered
        """
        return name in self._languages
    
    def list_languages(self) -> list:
        """
        Get list of all registered language names.
        
        Returns:
            List of language names
        """
        return list(self._languages.keys())
    
    def clear(self) -> None:
        """Clear all registered languages."""
        self._languages.clear()
        self._current_language = None
