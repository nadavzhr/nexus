"""
Search model.

Stores search state and results.
"""

from typing import List, Optional
from dataclasses import dataclass
from PyQt5.QtGui import QTextCursor


@dataclass
class SearchMatch:
    """Represents a single search match."""
    cursor: QTextCursor
    start: int
    end: int
    text: str
    
    @classmethod
    def from_cursor(cls, cursor: QTextCursor) -> 'SearchMatch':
        """Create a SearchMatch from a QTextCursor."""
        return cls(
            cursor=cursor,
            start=cursor.selectionStart(),
            end=cursor.selectionEnd(),
            text=cursor.selectedText()
        )


class SearchModel:
    """
    Model for search state and results.
    
    Stores the current search pattern, options, and found matches.
    Separate from UI and search logic.
    """
    
    def __init__(self):
        """Initialize the search model."""
        self._pattern: str = ""
        self._case_sensitive: bool = False
        self._use_regex: bool = False
        self._whole_word: bool = False
        self._matches: List[SearchMatch] = []
        self._current_index: int = -1
    
    @property
    def pattern(self) -> str:
        """Get the current search pattern."""
        return self._pattern
    
    @pattern.setter
    def pattern(self, value: str) -> None:
        """Set the search pattern."""
        self._pattern = value
    
    @property
    def case_sensitive(self) -> bool:
        """Check if search is case-sensitive."""
        return self._case_sensitive
    
    @case_sensitive.setter
    def case_sensitive(self, value: bool) -> None:
        """Set case sensitivity."""
        self._case_sensitive = value
    
    @property
    def use_regex(self) -> bool:
        """Check if regex mode is enabled."""
        return self._use_regex
    
    @use_regex.setter
    def use_regex(self, value: bool) -> None:
        """Set regex mode."""
        self._use_regex = value
    
    @property
    def whole_word(self) -> bool:
        """Check if whole word matching is enabled."""
        return self._whole_word
    
    @whole_word.setter
    def whole_word(self, value: bool) -> None:
        """Set whole word matching."""
        self._whole_word = value
    
    @property
    def matches(self) -> List[SearchMatch]:
        """Get the list of matches."""
        return self._matches
    
    @property
    def current_index(self) -> int:
        """Get the index of the current match."""
        return self._current_index
    
    @current_index.setter
    def current_index(self, value: int) -> None:
        """Set the current match index."""
        self._current_index = value
    
    @property
    def current_match(self) -> Optional[SearchMatch]:
        """Get the current match."""
        if 0 <= self._current_index < len(self._matches):
            return self._matches[self._current_index]
        return None
    
    @property
    def match_count(self) -> int:
        """Get the total number of matches."""
        return len(self._matches)
    
    def clear_matches(self) -> None:
        """Clear all matches."""
        self._matches.clear()
        self._current_index = -1
    
    def set_matches(self, matches: List[SearchMatch]) -> None:
        """Set the list of matches."""
        self._matches = matches
        self._current_index = 0 if matches else -1
    
    def next_match(self) -> Optional[SearchMatch]:
        """Move to the next match."""
        if not self._matches:
            return None
        self._current_index = (self._current_index + 1) % len(self._matches)
        return self.current_match
    
    def previous_match(self) -> Optional[SearchMatch]:
        """Move to the previous match."""
        if not self._matches:
            return None
        self._current_index = (self._current_index - 1) % len(self._matches)
        return self.current_match
    
    def has_matches(self) -> bool:
        """Check if there are any matches."""
        return len(self._matches) > 0
