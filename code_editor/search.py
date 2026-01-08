"""
Search functionality for the code editor.

This module provides search service and UI components.
"""

from typing import List, Optional
from PyQt5.QtCore import Qt, QRegExp, pyqtSignal
from PyQt5.QtGui import QTextCursor, QTextDocument, QColor
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QPushButton, 
    QCheckBox, QLabel, QVBoxLayout
)


class SearchMatch:
    """Represents a single search match."""
    
    def __init__(self, cursor: QTextCursor):
        """
        Initialize a search match.
        
        Args:
            cursor: QTextCursor positioned at the match
        """
        self.cursor = cursor
        self.start = cursor.selectionStart()
        self.end = cursor.selectionEnd()
        self.text = cursor.selectedText()


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
        
        if use_regex:
            # Use regex search
            regex = QRegExp(pattern)
            if not case_sensitive:
                regex.setCaseSensitivity(Qt.CaseInsensitive)
            
            cursor = self.document.find(regex, cursor, flags)
            while not cursor.isNull():
                match = SearchMatch(cursor)
                self._matches.append(match)
                cursor = self.document.find(regex, cursor, flags)
        else:
            # Use plain text search
            cursor = self.document.find(pattern, cursor, flags)
            while not cursor.isNull():
                match = SearchMatch(cursor)
                self._matches.append(match)
                cursor = self.document.find(pattern, cursor, flags)
        
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
    
    def clear(self) -> None:
        """Clear all search results."""
        self._matches.clear()
        self._current_index = -1


class SearchPopup(QWidget):
    """
    VS Code-style search popup widget.
    
    Appears in the top-right corner of the editor with search controls.
    """
    
    # Signals
    searchRequested = pyqtSignal(str, bool, bool, bool)  # pattern, case, regex, whole_word
    nextRequested = pyqtSignal()
    previousRequested = pyqtSignal()
    closeRequested = pyqtSignal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialize the search popup.
        
        Args:
            parent: Parent widget (the editor)
        """
        super().__init__(parent)
        self._setup_ui()
        self._last_pattern = ""
        
        # Make it a floating widget
        self.setWindowFlags(Qt.Widget)
        self.setAutoFillBackground(True)
    
    def _setup_ui(self) -> None:
        """Setup the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # First row: search input and buttons
        search_row = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Find...")
        self.search_input.setMinimumWidth(200)
        self.search_input.returnPressed.connect(self._on_search)
        search_row.addWidget(self.search_input)
        
        # Match count label
        self.match_label = QLabel("0 of 0")
        self.match_label.setMinimumWidth(50)
        search_row.addWidget(self.match_label)
        
        # Previous button
        self.prev_btn = QPushButton("↑")
        self.prev_btn.setMaximumWidth(30)
        self.prev_btn.clicked.connect(self.previousRequested.emit)
        search_row.addWidget(self.prev_btn)
        
        # Next button
        self.next_btn = QPushButton("↓")
        self.next_btn.setMaximumWidth(30)
        self.next_btn.clicked.connect(self.nextRequested.emit)
        search_row.addWidget(self.next_btn)
        
        # Close button
        close_btn = QPushButton("×")
        close_btn.setMaximumWidth(30)
        close_btn.clicked.connect(self.closeRequested.emit)
        search_row.addWidget(close_btn)
        
        layout.addLayout(search_row)
        
        # Second row: options
        options_row = QHBoxLayout()
        
        self.case_checkbox = QCheckBox("Case (Aa)")
        self.case_checkbox.toggled.connect(self._on_search)
        options_row.addWidget(self.case_checkbox)
        
        self.regex_checkbox = QCheckBox("Regex (.*)")
        self.regex_checkbox.toggled.connect(self._on_search)
        options_row.addWidget(self.regex_checkbox)
        
        self.whole_word_checkbox = QCheckBox("Word (ab)")
        self.whole_word_checkbox.toggled.connect(self._on_search)
        options_row.addWidget(self.whole_word_checkbox)
        
        options_row.addStretch()
        
        layout.addLayout(options_row)
        
        # Style
        self.setStyleSheet("""
            SearchPopup {
                background-color: #f0f0f0;
                border: 1px solid #999;
                border-radius: 4px;
            }
            QLineEdit {
                padding: 4px;
                border: 1px solid #ccc;
                border-radius: 2px;
            }
            QPushButton {
                padding: 4px;
                border: 1px solid #ccc;
                border-radius: 2px;
                background-color: white;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
    
    def _on_search(self) -> None:
        """Handle search request."""
        pattern = self.search_input.text()
        if pattern:
            self._last_pattern = pattern
            self.searchRequested.emit(
                pattern,
                self.case_checkbox.isChecked(),
                self.regex_checkbox.isChecked(),
                self.whole_word_checkbox.isChecked()
            )
    
    def set_pattern(self, pattern: str) -> None:
        """Set the search pattern."""
        self.search_input.setText(pattern)
        self._last_pattern = pattern
    
    def get_pattern(self) -> str:
        """Get the current search pattern."""
        return self.search_input.text()
    
    def update_match_count(self, current: int, total: int) -> None:
        """
        Update the match count display.
        
        Args:
            current: Current match index (1-based)
            total: Total number of matches
        """
        if total > 0:
            self.match_label.setText(f"{current} of {total}")
        else:
            self.match_label.setText("0 of 0")
    
    def show_popup(self) -> None:
        """Show the popup and restore last search."""
        if self._last_pattern:
            self.search_input.setText(self._last_pattern)
            self._on_search()
        self.show()
        self.search_input.setFocus()
        self.search_input.selectAll()
    
    def keyPressEvent(self, event) -> None:
        """Handle key press events."""
        if event.key() == Qt.Key_Escape:
            self.closeRequested.emit()
        else:
            super().keyPressEvent(event)
