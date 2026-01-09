"""
Line number gutter widget.

This module provides the line number area that displays alongside the editor.
"""

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPaintEvent


class LineNumberArea(QWidget):
    """
    Widget that displays line numbers alongside the code editor.
    
    This widget is docked to the left of the CodeEditor and updates
    automatically when the editor scrolls or the content changes.
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
