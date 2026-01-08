"""
Line data model.

Per-line metadata storage for the code editor.
"""

from typing import Any, Optional, Set
from PyQt5.QtGui import QTextBlockUserData, QColor


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
        self.tags: Set[str] = set()
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to this line."""
        self.tags.add(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from this line."""
        self.tags.discard(tag)
    
    def has_tag(self, tag: str) -> bool:
        """Check if this line has a specific tag."""
        return tag in self.tags
