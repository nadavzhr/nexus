"""
Search service.

Handles the logic of finding matches in a document.
"""

from typing import List, Optional
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QTextCursor, QTextDocument

from ..models.search_model import SearchMatch


class SearchService:
    """
    Service layer for search functionality.
    
    Handles the logic of finding matches in a document without
    concerning itself with UI.
    """
    
    def __init__(self, document: QTextDocument):
        """
        Initialize the search service.
        
        Args:
            document: QTextDocument to search in
        """
        self.document = document
        self._matches: List[SearchMatch] = []
        self._current_index: int = -1
        self._last_pattern: str = ""
        self._case_sensitive: bool = False
        self._use_regex: bool = False
        self._whole_word: bool = False
    
    def search(self, pattern: str, case_sensitive: bool = False,
               use_regex: bool = False, whole_word: bool = False) -> int:
        """
        Search for a pattern in the document.
        
        Args:
            pattern: Search pattern
            case_sensitive: If True, search is case-sensitive
            use_regex: If True, treat pattern as regex
            whole_word: If True, match whole words only
            
        Returns:
            Number of matches found
        """
        self._matches.clear()
        self._current_index = -1
        self._last_pattern = pattern
        self._case_sensitive = case_sensitive
        self._use_regex = use_regex
        self._whole_word = whole_word
        
        if not pattern:
            return 0
        
        # Build search flags
        flags = QTextDocument.FindFlags()
        if case_sensitive:
            flags |= QTextDocument.FindCaseSensitively
        if whole_word:
            flags |= QTextDocument.FindWholeWords
        
        # Find all matches
        cursor = QTextCursor(self.document)
        last_position = -1
        max_iterations = 10000  # Safety limit to prevent infinite loops
        iteration_count = 0
        
        if use_regex:
            # Use regex search
            regex = QRegExp(pattern)
            if not case_sensitive:
                regex.setCaseSensitivity(Qt.CaseInsensitive)
            
            cursor = self.document.find(regex, cursor, flags)
            while not cursor.isNull() and iteration_count < max_iterations:
                # Prevent infinite loop with zero-width matches
                current_pos = cursor.position()
                if current_pos == last_position:
                    # Move forward to avoid infinite loop
                    next_pos = current_pos + 1
                    # Check if we've reached the end of the document
                    if next_pos >= self.document.characterCount():
                        break
                    cursor.setPosition(next_pos)
                    cursor = self.document.find(regex, cursor, flags)
                    iteration_count += 1
                    continue
                
                # Validate cursor position is within document
                if current_pos < 0 or current_pos >= self.document.characterCount():
                    break
                
                match = SearchMatch.from_cursor(cursor)
                self._matches.append(match)
                last_position = current_pos
                cursor = self.document.find(regex, cursor, flags)
                iteration_count += 1
        else:
            # Use plain text search
            cursor = self.document.find(pattern, cursor, flags)
            while not cursor.isNull() and iteration_count < max_iterations:
                # Prevent infinite loop
                current_pos = cursor.position()
                if current_pos == last_position:
                    break
                
                # Validate cursor position
                if current_pos < 0 or current_pos >= self.document.characterCount():
                    break
                
                match = SearchMatch.from_cursor(cursor)
                self._matches.append(match)
                last_position = current_pos
                cursor = self.document.find(pattern, cursor, flags)
                iteration_count += 1
        
        if self._matches:
            self._current_index = 0
        
        return len(self._matches)
    
    def get_matches(self) -> List[SearchMatch]:
        """Get all search matches."""
        return self._matches
    
    def get_current_match(self) -> Optional[SearchMatch]:
        """Get the current match."""
        if 0 <= self._current_index < len(self._matches):
            return self._matches[self._current_index]
        return None
    
    def next_match(self) -> Optional[SearchMatch]:
        """Move to the next match."""
        if not self._matches:
            return None
        self._current_index = (self._current_index + 1) % len(self._matches)
        return self._matches[self._current_index]
    
    def previous_match(self) -> Optional[SearchMatch]:
        """Move to the previous match."""
        if not self._matches:
            return None
        self._current_index = (self._current_index - 1) % len(self._matches)
        return self._matches[self._current_index]
    
    def get_last_pattern(self) -> str:
        """Get the last search pattern."""
        return self._last_pattern
    
    def get_last_case_sensitive(self) -> bool:
        """Get the last case sensitivity setting."""
        return self._case_sensitive
    
    def get_last_use_regex(self) -> bool:
        """Get the last regex mode setting."""
        return self._use_regex
    
    def get_last_whole_word(self) -> bool:
        """Get the last whole word setting."""
        return self._whole_word
    
    def get_current_index(self) -> int:
        """Get the current match index (0-based)."""
        return self._current_index
    
    def has_matches(self) -> bool:
        """Check if there are any matches."""
        return len(self._matches) > 0
    
    def match_count(self) -> int:
        """Get the total number of matches."""
        return len(self._matches)
    
    def needs_research(self, pattern: str, case_sensitive: bool, 
                      use_regex: bool, whole_word: bool) -> bool:
        """
        Check if a new search is needed for the given criteria.
        
        Returns True if the search parameters have changed or no matches exist.
        Returns False if we already have matches for these exact parameters.
        """
        return (
            pattern != self._last_pattern or
            case_sensitive != self._case_sensitive or
            use_regex != self._use_regex or
            whole_word != self._whole_word or
            len(self._matches) == 0
        )
    
    def clear(self) -> None:
        """Clear all search results."""
        self._matches.clear()
        self._current_index = -1
