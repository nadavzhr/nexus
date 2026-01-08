"""
Search service.

Handles the logic of finding matches in a document.
"""

from typing import List
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QTextCursor, QTextDocument

from ..models.search_model import SearchModel, SearchMatch


class SearchService:
    """
    Service layer for search functionality.
    
    Handles the logic of finding matches in a document without
    concerning itself with UI. Uses SearchModel to store state.
    """
    
    # Safety limit to prevent infinite loops
    MAX_ITERATIONS = 10000
    
    def __init__(self, document: QTextDocument):
        """
        Initialize the search service.
        
        Args:
            document: QTextDocument to search in
        """
        self.document = document
        self.model = SearchModel()
    
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
        # Update model
        self.model.pattern = pattern
        self.model.case_sensitive = case_sensitive
        self.model.use_regex = use_regex
        self.model.whole_word = whole_word
        self.model.clear_matches()
        
        if not pattern:
            return 0
        
        # Find all matches
        matches = self._find_all_matches(
            pattern, case_sensitive, use_regex, whole_word
        )
        
        self.model.set_matches(matches)
        return self.model.match_count
    
    def _find_all_matches(self, pattern: str, case_sensitive: bool,
                          use_regex: bool, whole_word: bool) -> List[SearchMatch]:
        """
        Find all matches in the document.
        
        Args:
            pattern: Search pattern
            case_sensitive: Case sensitivity flag
            use_regex: Regex mode flag
            whole_word: Whole word flag
            
        Returns:
            List of SearchMatch objects
        """
        matches = []
        
        # Build search flags
        flags = QTextDocument.FindFlags()
        if case_sensitive:
            flags |= QTextDocument.FindCaseSensitively
        if whole_word:
            flags |= QTextDocument.FindWholeWords
        
        cursor = QTextCursor(self.document)
        last_position = -1
        iteration_count = 0
        
        if use_regex:
            matches = self._find_regex_matches(pattern, flags, case_sensitive)
        else:
            matches = self._find_plain_matches(pattern, flags)
        
        return matches
    
    def _find_plain_matches(self, pattern: str,
                           flags: QTextDocument.FindFlags) -> List[SearchMatch]:
        """
        Find all plain text matches.
        
        Args:
            pattern: Plain text pattern
            flags: Search flags
            
        Returns:
            List of matches
        """
        matches = []
        cursor = QTextCursor(self.document)
        last_position = -1
        iteration_count = 0
        
        while iteration_count < self.MAX_ITERATIONS:
            cursor = self.document.find(pattern, cursor, flags)
            
            if cursor.isNull():
                break
            
            current_position = cursor.position()
            
            # Safety check: ensure we're making progress
            if current_position == last_position:
                break
            
            # Validate position is within document bounds
            if current_position >= self.document.characterCount():
                break
            
            matches.append(SearchMatch.from_cursor(cursor))
            last_position = current_position
            iteration_count += 1
        
        return matches
    
    def _find_regex_matches(self, pattern: str,
                           flags: QTextDocument.FindFlags,
                           case_sensitive: bool) -> List[SearchMatch]:
        """
        Find all regex matches.
        
        Args:
            pattern: Regex pattern
            flags: Search flags
            case_sensitive: Case sensitivity flag
            
        Returns:
            List of matches
        """
        matches = []
        
        try:
            regex = QRegExp(pattern)
            if not case_sensitive:
                regex.setCaseSensitivity(Qt.CaseInsensitive)
            
            cursor = QTextCursor(self.document)
            last_position = -1
            iteration_count = 0
            
            while iteration_count < self.MAX_ITERATIONS:
                cursor = self.document.find(regex, cursor, flags)
                
                if cursor.isNull():
                    break
                
                current_position = cursor.position()
                
                # Safety checks
                if current_position == last_position:
                    # Zero-width match - advance cursor
                    cursor.movePosition(QTextCursor.NextCharacter)
                    if cursor.position() == current_position:
                        # Can't advance further
                        break
                    continue
                
                # Validate position
                if current_position >= self.document.characterCount():
                    break
                
                matches.append(SearchMatch.from_cursor(cursor))
                last_position = current_position
                iteration_count += 1
                
        except Exception:
            # Invalid regex - return empty list
            pass
        
        return matches
    
    def next_match(self) -> SearchMatch:
        """
        Move to the next match.
        
        Returns:
            The next match, or None if no matches
        """
        return self.model.next_match()
    
    def previous_match(self) -> SearchMatch:
        """
        Move to the previous match.
        
        Returns:
            The previous match, or None if no matches
        """
        return self.model.previous_match()
    
    def clear(self) -> None:
        """Clear all search state."""
        self.model.clear_matches()
        self.model.pattern = ""
