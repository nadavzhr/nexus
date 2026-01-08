"""
Core code editor widget implementation.

This module provides the main CodeEditor widget and LineData classes.
"""

from typing import Optional, Any, Dict, List
from PyQt5.QtCore import Qt, pyqtSignal, QRect
from PyQt5.QtGui import (
    QTextBlockUserData, QColor, QPainter, QTextFormat,
    QTextCursor, QPaintEvent, QMouseEvent, QResizeEvent, QTextDocument
)
from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QTextEdit

from .line_numbers import LineNumberArea
from .highlighter import PygmentsHighlighter


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
        
        # Decoration tracking
        self._decorations: Dict[str, List[QTextEdit.ExtraSelection]] = {
            'search': [],
            'hover': [],
            'custom': []
        }
        
        # Search state
        self._search_pattern: Optional[str] = None
        self._search_regex: bool = False
        
        # Hover state
        self._hover_enabled: bool = True
        self._last_hover_line: int = -1
        
        # Setup UI
        self._setup_ui()
        self._connect_signals()
    
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
    
    def line_number_area_paint_event(self, event: QPaintEvent) -> None:
        """Paint the line number area. Called by LineNumberArea."""
        painter = QPainter(self._line_number_area)
        painter.fillRect(event.rect(), Qt.lightGray)
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(
            self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self._line_number_area.width() - 3,
                               self.fontMetrics().height(),
                               Qt.AlignRight, number)
            
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1
    
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
