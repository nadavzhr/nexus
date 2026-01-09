"""
UI widgets for the code editor.

This package contains pure Qt UI widgets with minimal business logic.
"""

from .line_number_area import LineNumberArea
from .goto_line_overlay import GotoLineOverlay
from .search_popup import SearchPopup

__all__ = [
    'LineNumberArea',
    'GotoLineOverlay',
    'SearchPopup',
]
