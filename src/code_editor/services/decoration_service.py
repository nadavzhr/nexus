"""
Decoration service.

Centralized management of text decorations (ExtraSelections) with layer support.
This fixes the highlighting bugs by providing a single source of truth for decorations.
"""

from typing import Dict, List, Optional
from enum import Enum, auto
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QColor, QTextCursor


class DecorationLayer(Enum):
    """
    Layers for organizing decorations.
    
    Lower values are rendered first (bottom layer).
    Higher values are rendered last (top layer).
    """
    CUSTOM = auto()          # User-defined custom decorations
    CURRENT_LINE = auto()    # Current line highlight
    SEARCH_MATCHES = auto()  # All search matches
    CURRENT_MATCH = auto()   # The currently selected search match
    

class Decoration:
    """Represents a single text decoration."""
    
    def __init__(self, cursor: QTextCursor, bg_color: QColor, 
                 full_width: bool = False):
        """
        Initialize a decoration.
        
        Args:
            cursor: Text cursor defining the decorated range
            bg_color: Background color for the decoration
            full_width: If True, decoration spans the full line width
        """
        self.cursor = cursor
        self.bg_color = bg_color
        self.full_width = full_width
    
    def to_extra_selection(self) -> 'QTextEdit.ExtraSelection':
        """Convert to QTextEdit.ExtraSelection."""
        from PyQt5.QtWidgets import QTextEdit
        selection = QTextEdit.ExtraSelection()
        selection.cursor = self.cursor
        selection.format.setBackground(self.bg_color)
        if self.full_width:
            selection.format.setProperty(
                selection.format.FullWidthSelection, True
            )
        return selection


class DecorationService:
    """
    Centralized decoration manager.
    
    Manages all text decorations (ExtraSelections) in layers, ensuring:
    - Proper ordering (current line < search < current match)
    - No conflicts or race conditions
    - Atomic updates (clear + apply together)
    - Easy clearing by layer
    
    This fixes the highlighting persistence bugs.
    """
    
    def __init__(self, editor: QPlainTextEdit):
        """
        Initialize the decoration service.
        
        Args:
            editor: The QPlainTextEdit widget to apply decorations to
        """
        self.editor = editor
        self._layers: Dict[DecorationLayer, List[Decoration]] = {
            layer: [] for layer in DecorationLayer
        }
    
    def add_decoration(self, layer: DecorationLayer, cursor: QTextCursor,
                      bg_color: QColor, full_width: bool = False) -> None:
        """
        Add a decoration to a specific layer.
        
        Args:
            layer: The layer to add to
            cursor: Text cursor defining the range
            bg_color: Background color
            full_width: If True, span full line width
        """
        decoration = Decoration(cursor, bg_color, full_width)
        self._layers[layer].append(decoration)
    
    def clear_layer(self, layer: DecorationLayer) -> None:
        """
        Clear all decorations from a specific layer.
        
        Args:
            layer: The layer to clear
        """
        self._layers[layer].clear()
    
    def clear_all(self) -> None:
        """Clear all decorations from all layers."""
        for layer in DecorationLayer:
            self._layers[layer].clear()
    
    def apply(self) -> None:
        """
        Apply all decorations to the editor.
        
        This method collects decorations from all layers in order
        and applies them to the editor in a single operation.
        This ensures atomic updates and proper layering.
        """
        # Collect all decorations in layer order
        all_decorations = []
        for layer in sorted(DecorationLayer, key=lambda x: x.value):
            all_decorations.extend(self._layers[layer])
        
        # Convert to ExtraSelections
        selections = [d.to_extra_selection() for d in all_decorations]
        
        # Apply to editor atomically
        self.editor.setExtraSelections(selections)
    
    def get_layer_count(self, layer: DecorationLayer) -> int:
        """
        Get the number of decorations in a layer.
        
        Args:
            layer: The layer to check
            
        Returns:
            Number of decorations in the layer
        """
        return len(self._layers[layer])
    
    def has_decorations(self, layer: Optional[DecorationLayer] = None) -> bool:
        """
        Check if there are any decorations.
        
        Args:
            layer: Specific layer to check, or None for all layers
            
        Returns:
            True if decorations exist
        """
        if layer is not None:
            return len(self._layers[layer]) > 0
        return any(len(decorations) > 0 for decorations in self._layers.values())
