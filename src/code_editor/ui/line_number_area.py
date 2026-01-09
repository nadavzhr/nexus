"""
Line number gutter widget.

This module provides the line number area that displays alongside the editor.
"""

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPaintEvent


class LineNumberArea(QWidget):
    """
    Line number gutter widget - self-contained and reusable.
    
    A widget that displays line numbers alongside a code editor.
    Automatically updates when the editor scrolls or content changes.
    
    The widget is designed to be docked to the left side of a QPlainTextEdit
    and uses the parent editor's theme settings for coloring.
    
    Features:
    - Auto-sizing based on number of lines (width adjusts dynamically)
    - Theme-aware coloring (uses editor's theme for background and text)
    - Efficient painting (only paints visible line numbers)
    - Right-aligned line numbers with padding
    
    Usage:
        This widget is typically created and managed by the CodeEditor.
        It can also be used standalone with any QPlainTextEdit:
        
        ```python
        editor = QPlainTextEdit()
        line_area = LineNumberArea(editor)
        # Position it in the editor's layout
        # Connect to editor's signals for updates
        ```
    
    Note:
        The widget expects the parent editor to have:
        - _line_number_area_width() method
        - get_current_theme() method
        - blockBoundingGeometry(), contentOffset(), blockBoundingRect() methods
    """
    
    def __init__(self, editor):
        """
        Initialize the line number area.
        
        Args:
            editor: The CodeEditor instance this widget is attached to
        """
        super().__init__(editor)
        self._editor = editor
    
    def sizeHint(self) -> QSize:
        """Return the recommended size for this widget."""
        return QSize(self._editor._line_number_area_width(), 0)
    
    def paintEvent(self, event: QPaintEvent) -> None:
        """
        Paint the line numbers.
        
        Args:
            event: The paint event
        """
        from PyQt5.QtGui import QPainter
        from PyQt5.QtCore import Qt
        
        painter = QPainter(self)
        
        # Get theme colors
        theme = self._editor.get_current_theme()
        painter.fillRect(event.rect(), theme.line_number_bg)
        painter.setPen(theme.line_number)
        
        # Paint line numbers (delegate to editor)
        block = self._editor.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self._editor.blockBoundingGeometry(block).translated(
            self._editor.contentOffset()).top())
        bottom = top + int(self._editor.blockBoundingRect(block).height())
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(0, top, self.width() - 3,
                               self._editor.fontMetrics().height(),
                               Qt.AlignRight, number)
            
            block = block.next()
            top = bottom
            bottom = top + int(self._editor.blockBoundingRect(block).height())
            block_number += 1
