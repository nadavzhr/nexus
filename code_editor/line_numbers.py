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
        self._editor.line_number_area_paint_event(event)
