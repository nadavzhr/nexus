"""
Editor configuration model.

Stores editor settings and preferences in a data class.
"""

from dataclasses import dataclass
from typing import Optional
from PyQt5.QtGui import QColor


@dataclass
class EditorConfig:
    """
    Configuration settings for the CodeEditor.
    
    This data class separates configuration from the editor widget itself,
    following the Model/View separation principle.
    
    Attributes:
        tab_width: Width of tab character in spaces (default: 4)
        line_wrap_enabled: Enable line wrapping (default: False)
        hover_enabled: Enable hover highlighting in read-only mode (default: True)
        current_line_highlight_enabled: Enable current line highlighting (default: True)
        read_only: Editor is read-only (default: False)
        font_family: Font family name (default: "Courier New")
        font_size: Font size in points (default: 10)
        theme_name: Active theme name (default: "light")
    """
    
    # Display settings
    tab_width: int = 4
    line_wrap_enabled: bool = False
    font_family: str = "Courier New"
    font_size: int = 10
    
    # Interaction settings
    read_only: bool = False
    hover_enabled: bool = True
    current_line_highlight_enabled: bool = True
    
    # Theme
    theme_name: str = "light"
    
    def copy(self) -> 'EditorConfig':
        """
        Create a copy of this configuration.
        
        Returns:
            New EditorConfig instance with same values
        """
        return EditorConfig(
            tab_width=self.tab_width,
            line_wrap_enabled=self.line_wrap_enabled,
            font_family=self.font_family,
            font_size=self.font_size,
            read_only=self.read_only,
            hover_enabled=self.hover_enabled,
            current_line_highlight_enabled=self.current_line_highlight_enabled,
            theme_name=self.theme_name
        )
    
    @staticmethod
    def default() -> 'EditorConfig':
        """
        Create a default configuration.
        
        Returns:
            EditorConfig with default values
        """
        return EditorConfig()
