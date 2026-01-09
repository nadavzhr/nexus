"""
Protocol definitions for the code editor.

These protocols define interfaces that services and components can implement,
following the Interface Segregation and Dependency Inversion principles from SOLID.

Using Python's Protocol (PEP 544) allows for structural subtyping without
explicit inheritance, making the codebase more flexible and testable.
"""

from typing import Protocol, List, Optional, Any
from PyQt5.QtGui import QTextCursor, QColor, QTextDocument


class SearchServiceProtocol(Protocol):
    """
    Protocol for search service implementations.
    
    Any class implementing these methods can be used as a search service,
    enabling easy testing and alternative implementations.
    """
    
    def search(self, pattern: str, case_sensitive: bool = False,
               use_regex: bool = False, whole_word: bool = False) -> int:
        """Search for a pattern and return match count."""
        ...
    
    def get_matches(self) -> List[Any]:
        """Get all search matches."""
        ...
    
    def get_current_match(self) -> Optional[Any]:
        """Get the current match."""
        ...
    
    def next_match(self) -> Optional[Any]:
        """Move to next match."""
        ...
    
    def previous_match(self) -> Optional[Any]:
        """Move to previous match."""
        ...
    
    def get_last_pattern(self) -> str:
        """Get the last search pattern."""
        ...
    
    def clear(self) -> None:
        """Clear search state."""
        ...


class DecorationServiceProtocol(Protocol):
    """
    Protocol for decoration service implementations.
    
    Defines the interface for managing text decorations (highlights).
    """
    
    def add_decoration(self, layer: Any, cursor: QTextCursor,
                      bg_color: QColor, full_width: bool = False) -> None:
        """Add a decoration to a layer."""
        ...
    
    def clear_layer(self, layer: Any) -> None:
        """Clear all decorations from a layer."""
        ...
    
    def clear_all(self) -> None:
        """Clear all decorations."""
        ...
    
    def apply(self) -> None:
        """Apply decorations to the editor."""
        ...


class LanguageServiceProtocol(Protocol):
    """
    Protocol for language service implementations.
    
    Defines the interface for managing programming languages and lexers.
    """
    
    def register_language(self, name: str, lexer: Any) -> None:
        """Register a language with its lexer."""
        ...
    
    def get_lexer(self, name: str) -> Optional[Any]:
        """Get lexer for a language."""
        ...
    
    def set_current_language(self, name: str) -> bool:
        """Set the current language."""
        ...
    
    def get_current_language(self) -> Optional[str]:
        """Get current language name."""
        ...
    
    def has_language(self, name: str) -> bool:
        """Check if language is registered."""
        ...
    
    def list_languages(self) -> List[str]:
        """List all registered languages."""
        ...


class ThemeProtocol(Protocol):
    """
    Protocol for theme implementations.
    
    Defines the interface that all themes must implement.
    """
    
    @property
    def name(self) -> str:
        """Theme name."""
        ...
    
    @property
    def background(self) -> QColor:
        """Background color."""
        ...
    
    @property
    def text(self) -> QColor:
        """Text color."""
        ...
    
    @property
    def selection(self) -> QColor:
        """Selection color."""
        ...
    
    @property
    def current_line(self) -> QColor:
        """Current line highlight color."""
        ...
    
    @property
    def search_match(self) -> QColor:
        """Search match highlight color."""
        ...
    
    @property
    def current_match(self) -> QColor:
        """Current search match highlight color."""
        ...
    
    @property
    def line_number(self) -> QColor:
        """Line number text color."""
        ...
    
    @property
    def line_number_bg(self) -> QColor:
        """Line number background color."""
        ...
