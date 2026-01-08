"""
Core code editor widget implementation.

This module provides the main CodeEditor widget and LineData classes.
"""

from typing import Optional, Any, Dict, List
from PyQt5.QtCore import Qt, pyqtSignal, QRect
from PyQt5.QtGui import (
    QTextBlockUserData, QColor, QPainter, QTextFormat,
    QTextCursor, QPaintEvent, QMouseEvent, QResizeEvent, QTextDocument,
    QKeySequence
)
from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QTextEdit, QShortcut

from .line_numbers import LineNumberArea
from .highlighter import PygmentsHighlighter
from .theme import ThemeManager, Theme
from .search import SearchService, SearchPopup
from .shortcuts import EditorActions
from .goto_line_overlay import GotoLineOverlay


class LineData(QTextBlockUserData):
    """
    Per-line metadata storage.
    
    Each QTextBlock can have an associated LineData instance that stores:
    - Arbitrary user-defined payload data
    - Background color for the line
    - Tags for categorization
    
    This enables line-centric interaction similar to QListView items.
    """
    
    def __init__(self, payload: Any = None, bg_color: Optional[QColor] = None):
        """
        Initialize line data.
        
        Args:
            payload: User-defined data to associate with this line
            bg_color: Optional background color for this line
        """
        super().__init__()
        self.payload = payload
        self.bg_color = bg_color
        self.tags: set = set()
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to this line."""
        self.tags.add(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from this line."""
        self.tags.discard(tag)
    
    def has_tag(self, tag: str) -> bool:
        """Check if this line has a specific tag."""
        return tag in self.tags


class CodeEditor(QPlainTextEdit):
    """
    Standalone multi-language code editor widget.
    
    A professional code editor built on QPlainTextEdit with:
    - Multi-language syntax highlighting via Pygments
    - Line-aware data model (QTextBlock + LineData)
    - Line numbering gutter
    - Search and decoration support
    - Read-only and editable modes
    - Clean public API for integration
    
    Signals:
        lineActivated: Emitted when a line is activated (double-clicked in read-only mode)
        cursorMoved: Emitted when the cursor position changes
    """
    
    # Signals
    lineActivated = pyqtSignal(int, object)  # line_number, line_data
    cursorMoved = pyqtSignal(int)  # line_number
    
    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialize the code editor.
        
        Args:
            parent: Optional parent widget
        """
        super().__init__(parent)
        
        # Initialize components
        self._line_number_area = LineNumberArea(self)
        self._highlighter: Optional[PygmentsHighlighter] = None
        self._languages: Dict[str, Any] = {}
        self._current_language: Optional[str] = None
        
        # Theme management
        self._theme_manager = ThemeManager()
        
        # Search components
        self._search_service = SearchService(self.document())
        self._search_popup: Optional[SearchPopup] = None
        
        # Goto line overlay
        self._goto_line_overlay: Optional[GotoLineOverlay] = None
        
        # Editor actions
        self._actions = EditorActions(self)
        
        # Decoration tracking
        self._decorations: Dict[str, List[QTextEdit.ExtraSelection]] = {
            'search': [],
            'current_match': [],
            'current_line': [],
            'hover': [],
            'custom': []
        }
        
        # Search state (legacy - kept for compatibility)
        self._search_pattern: Optional[str] = None
        self._search_regex: bool = False
        
        # Hover state
        self._hover_enabled: bool = True
        self._last_hover_line: int = -1
        
        # Current line highlighting
        self._current_line_highlight_enabled: bool = True
        
        # Setup UI
        self._setup_ui()
        self._connect_signals()
        self._setup_shortcuts()
        
        # Apply initial theme
        self._apply_theme()
    
    def _setup_ui(self) -> None:
        """Configure the editor's appearance and behavior."""
        # Set monospace font
        from PyQt5.QtGui import QFont
        font = QFont("Courier New", 10)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
        
        # Enable line wrapping (can be disabled if needed)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        
        # Set tab width to 4 spaces
        from PyQt5.QtGui import QFontMetrics
        metrics = QFontMetrics(self.font())
        self.setTabStopWidth(4 * metrics.width(' '))
    
    def _connect_signals(self) -> None:
        """Connect internal signals."""
        self.blockCountChanged.connect(self._update_line_number_area_width)
        self.updateRequest.connect(self._update_line_number_area)
        self.cursorPositionChanged.connect(self._on_cursor_position_changed)
    
    def _setup_shortcuts(self) -> None:
        """Setup keyboard shortcuts."""
        # Comment/Uncomment - Ctrl+/
        self._shortcut_comment = QShortcut(QKeySequence("Ctrl+/"), self)
        self._shortcut_comment.activated.connect(self.toggle_comment)
        
        # Duplicate line - Ctrl+D
        self._shortcut_duplicate = QShortcut(QKeySequence("Ctrl+D"), self)
        self._shortcut_duplicate.activated.connect(self.duplicate_line)
        
        # Move line up - Alt+Up
        self._shortcut_move_up = QShortcut(QKeySequence("Alt+Up"), self)
        self._shortcut_move_up.activated.connect(self.move_line_up)
        
        # Move line down - Alt+Down
        self._shortcut_move_down = QShortcut(QKeySequence("Alt+Down"), self)
        self._shortcut_move_down.activated.connect(self.move_line_down)
        
        # Go to line - Ctrl+G
        self._shortcut_goto = QShortcut(QKeySequence("Ctrl+G"), self)
        self._shortcut_goto.activated.connect(self.go_to_line)
        
        # Search - Ctrl+F
        self._shortcut_search = QShortcut(QKeySequence("Ctrl+F"), self)
        self._shortcut_search.activated.connect(self.show_search_popup)
    
    # ==================== Line Number Area Methods ====================
    
    def _update_line_number_area_width(self, _: int = 0) -> None:
        """Update the viewport margins to accommodate the line number area."""
        self.setViewportMargins(self._line_number_area_width(), 0, 0, 0)
    
    def _line_number_area_width(self) -> int:
        """Calculate the required width for the line number area."""
        digits = len(str(max(1, self.blockCount())))
        space = 3 + self.fontMetrics().width('9') * digits
        return space
    
    def _update_line_number_area(self, rect: QRect, dy: int) -> None:
        """Update the line number area when the editor scrolls or updates."""
        if dy:
            self._line_number_area.scroll(0, dy)
        else:
            self._line_number_area.update(0, rect.y(), 
                                         self._line_number_area.width(), 
                                         rect.height())
        
        if rect.contains(self.viewport().rect()):
            self._update_line_number_area_width()
    
    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize events to update the line number area."""
        super().resizeEvent(event)
        cr = self.contentsRect()
        self._line_number_area.setGeometry(
            cr.left(), cr.top(), 
            self._line_number_area_width(), 
            cr.height()
        )
    
    # ==================== Line Data API ====================
    
    def get_line_data(self, line_number: int) -> Optional[LineData]:
        """
        Get the LineData for a specific line.
        
        Args:
            line_number: 0-based line index
            
        Returns:
            LineData object if it exists, None otherwise
        """
        block = self.document().findBlockByNumber(line_number)
        if not block.isValid():
            return None
        return block.userData()
    
    def set_line_data(self, line_number: int, data: LineData) -> bool:
        """
        Set the LineData for a specific line.
        
        Args:
            line_number: 0-based line index
            data: LineData object to associate with the line
            
        Returns:
            True if successful, False if line doesn't exist
        """
        block = self.document().findBlockByNumber(line_number)
        if not block.isValid():
            return False
        block.setUserData(data)
        return True
    
    def create_line_data(self, line_number: int, payload: Any = None,
                        bg_color: Optional[QColor] = None) -> bool:
        """
        Create and set LineData for a specific line.
        
        Args:
            line_number: 0-based line index
            payload: User-defined data
            bg_color: Optional background color
            
        Returns:
            True if successful, False if line doesn't exist
        """
        data = LineData(payload, bg_color)
        return self.set_line_data(line_number, data)
    
    # ==================== Language & Highlighting API ====================
    
    def register_language(self, name: str, lexer, 
                         file_extensions: Optional[List[str]] = None) -> None:
        """
        Register a custom language for syntax highlighting.
        
        Args:
            name: Language identifier
            lexer: Pygments lexer instance or class
            file_extensions: Optional list of file extensions (e.g., ['.py', '.pyw'])
        """
        self._languages[name] = {
            'lexer': lexer,
            'extensions': file_extensions or []
        }
    
    def set_language(self, name: str) -> bool:
        """
        Set the current syntax highlighting language.
        
        Args:
            name: Language identifier (must be registered first)
            
        Returns:
            True if successful, False if language not found
        """
        if name not in self._languages:
            return False
        
        lang_info = self._languages[name]
        lexer = lang_info['lexer']
        
        # Create or update highlighter
        if self._highlighter:
            self._highlighter.set_lexer(lexer)
        else:
            self._highlighter = PygmentsHighlighter(self.document(), lexer)
        
        self._current_language = name
        return True
    
    def get_current_language(self) -> Optional[str]:
        """Get the name of the currently active language."""
        return self._current_language
    
    def disable_highlighting(self) -> None:
        """Disable syntax highlighting."""
        if self._highlighter:
            self._highlighter.setDocument(None)
            self._highlighter = None
        self._current_language = None
    
    # ==================== Decoration API ====================
    
    def add_decoration(self, line_number: int, bg_color: QColor, 
                      decoration_type: str = 'custom') -> None:
        """
        Add a background color decoration to a line.
        
        Args:
            line_number: 0-based line index
            bg_color: Background color for the line
            decoration_type: Type of decoration ('search', 'hover', 'custom')
        """
        block = self.document().findBlockByNumber(line_number)
        if not block.isValid():
            return
        
        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(bg_color)
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = QTextCursor(block)
        selection.cursor.clearSelection()
        
        if decoration_type not in self._decorations:
            self._decorations[decoration_type] = []
        
        self._decorations[decoration_type].append(selection)
        self._apply_decorations()
    
    def clear_decorations(self, decoration_type: Optional[str] = None) -> None:
        """
        Clear decorations.
        
        Args:
            decoration_type: Type to clear, or None to clear all
        """
        if decoration_type:
            self._decorations[decoration_type] = []
        else:
            for key in self._decorations:
                self._decorations[key] = []
        self._apply_decorations()
    
    def _apply_decorations(self) -> None:
        """Apply all decorations to the editor."""
        all_selections = []
        for selections in self._decorations.values():
            all_selections.extend(selections)
        self.setExtraSelections(all_selections)
    
    # ==================== Search API ====================
    
    def search(self, pattern: str, regex: bool = False) -> int:
        """
        Search for a pattern and highlight all matches.
        
        Args:
            pattern: Search pattern
            regex: If True, treat pattern as regex
            
        Returns:
            Number of matches found
        """
        self._search_pattern = pattern
        self._search_regex = regex
        self.clear_decorations('search')
        
        if not pattern:
            return 0
        
        # Find all matches
        matches = 0
        cursor = QTextCursor(self.document())
        highlight_color = QColor(Qt.yellow)
        
        flags = QTextDocument.FindFlags()
        if regex:
            # For regex support, we'd need to use QRegExp or QRegularExpression
            # For now, use plain text
            pass
        
        while True:
            cursor = self.document().find(pattern, cursor, flags)
            if cursor.isNull():
                break
            
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(highlight_color)
            selection.cursor = cursor
            self._decorations['search'].append(selection)
            matches += 1
        
        self._apply_decorations()
        return matches
    
    def clear_search(self) -> None:
        """Clear search highlighting."""
        self._search_pattern = None
        self.clear_decorations('search')
    
    # ==================== Mode Control ====================
    
    def setEditable(self, editable: bool) -> None:
        """
        Set the editor to editable mode.
        
        Args:
            editable: If True, enable editing; if False, make read-only
        """
        self.setReadOnly(not editable)
    
    # ==================== Interaction Handlers ====================
    
    def _on_cursor_position_changed(self) -> None:
        """Handle cursor position changes."""
        cursor = self.textCursor()
        line_number = cursor.blockNumber()
        self.cursorMoved.emit(line_number)
        
        # Update current line highlighting
        if self._current_line_highlight_enabled:
            self._highlight_current_line()
    
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        """Handle double-click events."""
        super().mouseDoubleClickEvent(event)
        
        if self.isReadOnly():
            cursor = self.cursorForPosition(event.pos())
            line_number = cursor.blockNumber()
            line_data = self.get_line_data(line_number)
            
            payload = line_data.payload if line_data else None
            self.lineActivated.emit(line_number, payload)
    
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Handle mouse move events for hover highlighting."""
        super().mouseMoveEvent(event)
        
        if self.isReadOnly() and self._hover_enabled:
            cursor = self.cursorForPosition(event.pos())
            line_number = cursor.blockNumber()
            
            if line_number != self._last_hover_line:
                self.clear_decorations('hover')
                if line_number >= 0:
                    hover_color = QColor(230, 230, 250)  # Light lavender
                    self.add_decoration(line_number, hover_color, 'hover')
                self._last_hover_line = line_number
    
    def leaveEvent(self, event) -> None:
        """Handle mouse leave events."""
        super().leaveEvent(event)
        if self._hover_enabled:
            self.clear_decorations('hover')
            self._last_hover_line = -1
    
    def keyPressEvent(self, event) -> None:
        """Handle key press events for smart copy/cut."""
        from PyQt5.QtCore import Qt
        
        # Handle Ctrl+C when no selection - copy current line
        if event.key() == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
            if not self.textCursor().hasSelection():
                self.copy_line()
                return
        
        # Handle Ctrl+X when no selection - cut current line
        elif event.key() == Qt.Key_X and event.modifiers() == Qt.ControlModifier:
            if not self.textCursor().hasSelection() and not self.isReadOnly():
                self.cut_line()
                return
        
        # Default behavior for all other keys
        super().keyPressEvent(event)
    
    # ==================== Utility Methods ====================
    
    def line_count(self) -> int:
        """Get the total number of lines in the document."""
        return self.blockCount()
    
    def get_line_text(self, line_number: int) -> Optional[str]:
        """
        Get the text of a specific line.
        
        Args:
            line_number: 0-based line index
            
        Returns:
            Line text, or None if line doesn't exist
        """
        block = self.document().findBlockByNumber(line_number)
        if not block.isValid():
            return None
        return block.text()
    
    def set_hover_enabled(self, enabled: bool) -> None:
        """Enable or disable hover highlighting in read-only mode."""
        self._hover_enabled = enabled
        if not enabled:
            self.clear_decorations('hover')
    
    # ==================== Theme Management ====================
    
    def set_theme(self, theme_name: str) -> None:
        """
        Set the editor theme.
        
        Args:
            theme_name: Name of the theme ('light' or 'dark' or custom)
        """
        self._theme_manager.set_current_theme(theme_name)
        self._apply_theme()
    
    def get_current_theme(self) -> Theme:
        """Get the currently active theme."""
        return self._theme_manager.get_current_theme()
    
    def register_theme(self, theme: Theme) -> None:
        """
        Register a custom theme.
        
        Args:
            theme: Theme object to register
        """
        self._theme_manager.register_theme(theme)
    
    def list_themes(self) -> List[str]:
        """Get a list of available theme names."""
        return self._theme_manager.list_themes()
    
    def _apply_theme(self) -> None:
        """Apply the current theme to the editor."""
        theme = self._theme_manager.get_current_theme()
        
        # Set editor colors
        palette = self.palette()
        palette.setColor(palette.Base, theme.background)
        palette.setColor(palette.Text, theme.text)
        palette.setColor(palette.Highlight, theme.selection)
        palette.setColor(palette.HighlightedText, theme.text)
        self.setPalette(palette)
        
        # Update line number area
        self._line_number_area.update()
        
        # Re-highlight current line
        if self._current_line_highlight_enabled:
            self._highlight_current_line()
        
        # Update syntax highlighter if present
        if self._highlighter:
            self._highlighter.set_theme(theme)
    
    # ==================== Current Line Highlighting ====================
    
    def _highlight_current_line(self) -> None:
        """Highlight the current line."""
        self.clear_decorations('current_line')
        
        if not self.isReadOnly():
            cursor = self.textCursor()
            theme = self._theme_manager.get_current_theme()
            
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(theme.current_line)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = cursor
            selection.cursor.clearSelection()
            
            self._decorations['current_line'].append(selection)
            self._apply_decorations()
    
    def set_current_line_highlight_enabled(self, enabled: bool) -> None:
        """
        Enable or disable current line highlighting.
        
        Args:
            enabled: True to enable, False to disable
        """
        self._current_line_highlight_enabled = enabled
        if enabled:
            self._highlight_current_line()
        else:
            self.clear_decorations('current_line')
    
    # ==================== Enhanced Search with Popup ====================
    
    def show_search_popup(self) -> None:
        """Show the search popup widget."""
        if not self._search_popup:
            self._search_popup = SearchPopup(self)
            self._search_popup.searchRequested.connect(self._on_search_requested)
            self._search_popup.nextRequested.connect(self._on_next_match)
            self._search_popup.previousRequested.connect(self._on_previous_match)
            self._search_popup.closeRequested.connect(self._on_search_closed)
        
        # Position popup at top-right corner
        popup_width = self._search_popup.sizeHint().width()
        popup_height = self._search_popup.sizeHint().height()
        x = self.width() - popup_width - 20
        y = 10
        self._search_popup.setGeometry(x, y, popup_width, popup_height)
        
        # Restore last search
        last_pattern = self._search_service.get_last_pattern()
        if last_pattern:
            self._search_popup.set_pattern(last_pattern)
        
        self._search_popup.show_popup()
    
    def _on_search_requested(self, pattern: str, case_sensitive: bool,
                             use_regex: bool, whole_word: bool) -> None:
        """Handle search request from popup."""
        # Clear previous highlights first (always clear when pattern changes)
        self.clear_decorations('search')
        self.clear_decorations('current_match')
        
        # If pattern is empty, just clear and update UI
        if not pattern:
            if self._search_popup:
                self._search_popup.update_match_count(0, 0)
            return
        
        # Perform search
        count = self._search_service.search(pattern, case_sensitive, use_regex, whole_word)
        
        if count > 0:
            # Highlight all matches
            theme = self._theme_manager.get_current_theme()
            for match in self._search_service.get_matches():
                selection = QTextEdit.ExtraSelection()
                selection.format.setBackground(theme.search_match)
                selection.cursor = match.cursor
                self._decorations['search'].append(selection)
            
            # Highlight current match distinctly
            current_match = self._search_service.get_current_match()
            if current_match:
                selection = QTextEdit.ExtraSelection()
                selection.format.setBackground(theme.current_match)
                selection.cursor = current_match.cursor
                self._decorations['current_match'].append(selection)
                
                # Move editor to current match
                self.setTextCursor(current_match.cursor)
                self.centerCursor()
            
            self._apply_decorations()
            
            # Update match count in popup
            if self._search_popup:
                current_idx = 1
                self._search_popup.update_match_count(current_idx, count)
        else:
            # No matches found - show "No results"
            if self._search_popup:
                self._search_popup.update_match_count(0, 0)
    
    def _on_next_match(self) -> None:
        """Jump to next search match."""
        match = self._search_service.next_match()
        if match:
            self._update_current_match(match)
    
    def _on_previous_match(self) -> None:
        """Jump to previous search match."""
        match = self._search_service.previous_match()
        if match:
            self._update_current_match(match)
    
    def _update_current_match(self, match) -> None:
        """Update highlighting for current match."""
        # Clear current match highlighting
        self.clear_decorations('current_match')
        
        # Highlight new current match
        theme = self._theme_manager.get_current_theme()
        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(theme.current_match)
        selection.cursor = match.cursor
        self._decorations['current_match'].append(selection)
        
        self._apply_decorations()
        
        # Move editor to match
        self.setTextCursor(match.cursor)
        self.centerCursor()
        
        # Update popup match count
        if self._search_popup:
            matches = self._search_service.get_matches()
            current_idx = matches.index(match) + 1 if match in matches else 0
            self._search_popup.update_match_count(current_idx, len(matches))
    
    def _on_search_closed(self) -> None:
        """Handle search popup close."""
        # Clear all search highlights when closing
        self.clear_decorations('search')
        self.clear_decorations('current_match')
        self._apply_decorations()
        
        # Hide the popup
        if self._search_popup:
            self._search_popup.hide()
    
    # ==================== Keyboard Shortcut Actions (Public API) ====================
    
    def toggle_comment(self) -> None:
        """Toggle comment on the current line or selection."""
        if not self.isReadOnly():
            self._actions.toggle_comment()
    
    def duplicate_line(self) -> None:
        """Duplicate the current line or selection."""
        if not self.isReadOnly():
            self._actions.duplicate_line()
    
    def move_line_up(self) -> None:
        """Move the current line up."""
        if not self.isReadOnly():
            self._actions.move_line_up()
    
    def move_line_down(self) -> None:
        """Move the current line down."""
        if not self.isReadOnly():
            self._actions.move_line_down()
    
    def go_to_line(self) -> None:
        """Show overlay and jump to a specific line."""
        # Create overlay if it doesn't exist
        if self._goto_line_overlay is None:
            self._goto_line_overlay = GotoLineOverlay(self)
            self._goto_line_overlay.jumpRequested.connect(self.jump_to_line)
            self._goto_line_overlay.closeRequested.connect(self._on_goto_overlay_closed)
        
        # Show the overlay with current max line
        max_line = self.document().blockCount()
        self._goto_line_overlay.show_overlay(max_line)
    
    def _preview_goto_line(self, line_number: int) -> None:
        """Preview jump to line (called by overlay for live updates).
        
        Args:
            line_number: Line number to preview (1-based)
        """
        # Move cursor to line as user types (live preview)
        block = self.document().findBlockByLineNumber(line_number - 1)
        if block.isValid():
            cursor = self.textCursor()
            cursor.setPosition(block.position())
            self.setTextCursor(cursor)
            self.centerCursor()
    
    def _on_goto_overlay_closed(self) -> None:
        """Handle goto line overlay being closed."""
        # Return focus to editor
        self.setFocus()
    
    def jump_to_line(self, line_number: int) -> None:
        """
        Jump to a specific line number (public API).
        
        Args:
            line_number: Line number (1-based)
        """
        self._actions.jump_to_line(line_number)
    
    def copy_line(self) -> None:
        """
        Copy the current line to clipboard if no selection.
        
        If there's a selection, use Qt's native copy (Ctrl+C).
        """
        self._actions.copy_line()
    
    def cut_line(self) -> None:
        """
        Cut the current line to clipboard if no selection.
        
        If there's a selection, use Qt's native cut (Ctrl+X).
        """
        if not self.isReadOnly():
            self._actions.cut_line()
