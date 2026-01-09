"""
Search functionality for the code editor.

This module provides the search popup UI component.
"""

from typing import Optional
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QPushButton, 
    QCheckBox, QLabel, QVBoxLayout
)


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
        # Live search as user types
        self.search_input.textChanged.connect(self._on_search)
        # Install event filter to handle Alt shortcuts when input has focus
        self.search_input.installEventFilter(self)
        search_row.addWidget(self.search_input)
        
        # Match count label
        self.match_label = QLabel("No results")
        self.match_label.setMinimumWidth(100)
        search_row.addWidget(self.match_label)
        
        # Previous button
        self.prev_btn = QPushButton("↑")
        self.prev_btn.setMaximumWidth(30)
        self.prev_btn.setToolTip("Previous (Shift+Enter)")
        self.prev_btn.clicked.connect(self.previousRequested.emit)
        search_row.addWidget(self.prev_btn)
        
        # Next button
        self.next_btn = QPushButton("↓")
        self.next_btn.setMaximumWidth(30)
        self.next_btn.setToolTip("Next (Enter)")
        self.next_btn.clicked.connect(self.nextRequested.emit)
        search_row.addWidget(self.next_btn)
        
        # Close button
        close_btn = QPushButton("×")
        close_btn.setMaximumWidth(30)
        close_btn.setToolTip("Close (Esc)")
        close_btn.clicked.connect(self.closeRequested.emit)
        search_row.addWidget(close_btn)
        
        layout.addLayout(search_row)
        
        # Second row: options
        options_row = QHBoxLayout()
        
        self.case_checkbox = QCheckBox("Case (Aa)")
        self.case_checkbox.setToolTip("Match case (Alt+C)")
        self.case_checkbox.toggled.connect(self._on_search)
        options_row.addWidget(self.case_checkbox)
        
        self.regex_checkbox = QCheckBox("Regex (.*)")
        self.regex_checkbox.setToolTip("Use regular expression (Alt+R)")
        self.regex_checkbox.toggled.connect(self._on_search)
        options_row.addWidget(self.regex_checkbox)
        
        self.whole_word_checkbox = QCheckBox("Word (ab)")
        self.whole_word_checkbox.setToolTip("Match whole word (Alt+W)")
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
    
    def get_case_sensitive(self) -> bool:
        """Get the current case sensitivity state."""
        return self.case_checkbox.isChecked()
    
    def get_use_regex(self) -> bool:
        """Get the current regex mode state."""
        return self.regex_checkbox.isChecked()
    
    def get_whole_word(self) -> bool:
        """Get the current whole word matching state."""
        return self.whole_word_checkbox.isChecked()
    
    def set_case_sensitive(self, value: bool) -> None:
        """Set the case sensitivity state."""
        self.case_checkbox.setChecked(value)
    
    def set_use_regex(self, value: bool) -> None:
        """Set the regex mode state."""
        self.regex_checkbox.setChecked(value)
    
    def set_whole_word(self, value: bool) -> None:
        """Set the whole word matching state."""
        self.whole_word_checkbox.setChecked(value)
    
    def update_match_count(self, current: int, total: int) -> None:
        """
        Update the match count display.
        
        Args:
            current: Current match index (1-based)
            total: Total number of matches
        """
        if total > 0:
            self.match_label.setText(f"{current} of {total}")
            self.match_label.setStyleSheet("")  # Reset style
        else:
            # Show "No results" in red when search has no matches
            pattern = self.search_input.text()
            if pattern:  # Only show "No results" if there's a search query
                self.match_label.setText("No results")
                self.match_label.setStyleSheet("color: #cc0000;")  # Red text
            else:
                self.match_label.setText("No results")
                self.match_label.setStyleSheet("")  # Reset style
    
    def show_popup(self) -> None:
        """Show the popup and restore last search."""
        if self._last_pattern:
            self.search_input.setText(self._last_pattern)
            # Don't trigger search on restore, it will trigger via textChanged
        self.show()
        self.raise_()  # Bring to front
        self.activateWindow()  # Activate window
        self.search_input.setFocus(Qt.OtherFocusReason)
        self.search_input.selectAll()
    
    def eventFilter(self, obj, event) -> bool:
        """Filter events for child widgets to handle shortcuts.
        
        This is necessary because keyboard shortcuts need to work even when
        the search_input has focus.
        """
        # Don't process events if popup is hidden
        if not self.isVisible():
            return super().eventFilter(obj, event)
        
        if obj == self.search_input and event.type() == event.KeyPress:
            # Handle Alt+C, Alt+R, Alt+W shortcuts
            if event.modifiers() == Qt.AltModifier:
                if event.key() == Qt.Key_C:
                    self.case_checkbox.setChecked(not self.case_checkbox.isChecked())
                    return True
                elif event.key() == Qt.Key_R:
                    self.regex_checkbox.setChecked(not self.regex_checkbox.isChecked())
                    return True
                elif event.key() == Qt.Key_W:
                    self.whole_word_checkbox.setChecked(not self.whole_word_checkbox.isChecked())
                    return True
            
            # Handle Enter/Shift+Enter
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if event.modifiers() == Qt.ShiftModifier:
                    self.previousRequested.emit()
                else:
                    self.nextRequested.emit()
                return True
            
            # Handle Escape
            elif event.key() == Qt.Key_Escape:
                self.closeRequested.emit()
                return True
        
        return super().eventFilter(obj, event)
    
    def keyPressEvent(self, event) -> None:
        """Handle key press events."""
        # Don't process events if popup is hidden
        if not self.isVisible():
            super().keyPressEvent(event)
            return
        
        # Enter - Next match
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if event.modifiers() == Qt.ShiftModifier:
                # Shift+Enter - Previous match
                self.previousRequested.emit()
            else:
                # Enter - Next match
                self.nextRequested.emit()
            event.accept()
            return
        
        # Escape - Close
        elif event.key() == Qt.Key_Escape:
            self.closeRequested.emit()
            event.accept()
            return
        
        # Alt+C - Toggle case sensitivity
        elif event.key() == Qt.Key_C and event.modifiers() == Qt.AltModifier:
            self.case_checkbox.setChecked(not self.case_checkbox.isChecked())
            event.accept()
            return
        
        # Alt+R - Toggle regex
        elif event.key() == Qt.Key_R and event.modifiers() == Qt.AltModifier:
            self.regex_checkbox.setChecked(not self.regex_checkbox.isChecked())
            event.accept()
            return
        
        # Alt+W - Toggle whole word
        elif event.key() == Qt.Key_W and event.modifiers() == Qt.AltModifier:
            self.whole_word_checkbox.setChecked(not self.whole_word_checkbox.isChecked())
            event.accept()
            return
        
        # Default behavior
        super().keyPressEvent(event)
