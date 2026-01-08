"""
Theme support for the code editor.

This module provides theme definitions and management for the CodeEditor widget.
"""

from typing import Dict
from PyQt5.QtGui import QColor, QPalette
from dataclasses import dataclass


@dataclass
class Theme:
    """
    Theme definition for the code editor.
    
    Attributes:
        name: Theme name
        background: Editor background color
        text: Default text color
        current_line: Current line highlight color
        line_number: Line number text color
        line_number_bg: Line number background color
        selection: Text selection background color
        search_match: Search match highlight color
        current_match: Current search match highlight color
        comment: Comment text color (for highlighter)
        keyword: Keyword text color
        string: String literal color
        number: Number literal color
        function: Function name color
        operator: Operator color
    """
    name: str
    background: QColor
    text: QColor
    current_line: QColor
    line_number: QColor
    line_number_bg: QColor
    selection: QColor
    search_match: QColor
    current_match: QColor
    # Syntax highlighting colors
    comment: QColor
    keyword: QColor
    string: QColor
    number: QColor
    function: QColor
    operator: QColor


class ThemeManager:
    """
    Manages themes for the code editor.
    """
    
    def __init__(self):
        """Initialize the theme manager with built-in themes."""
        self._themes: Dict[str, Theme] = {}
        self._current_theme_name: str = "light"
        self._register_builtin_themes()
    
    def _register_builtin_themes(self) -> None:
        """Register built-in light and dark themes."""
        # Light theme
        light = Theme(
            name="light",
            background=QColor(255, 255, 255),
            text=QColor(0, 0, 0),
            current_line=QColor(245, 245, 245),
            line_number=QColor(100, 100, 100),
            line_number_bg=QColor(240, 240, 240),
            selection=QColor(173, 214, 255),
            search_match=QColor(255, 255, 0, 100),
            current_match=QColor(255, 165, 0, 150),
            comment=QColor(0, 128, 0),
            keyword=QColor(0, 0, 255),
            string=QColor(163, 21, 21),
            number=QColor(176, 96, 0),
            function=QColor(0, 128, 128),
            operator=QColor(128, 128, 128)
        )
        
        # Dark theme
        dark = Theme(
            name="dark",
            background=QColor(30, 30, 30),
            text=QColor(212, 212, 212),
            current_line=QColor(45, 45, 45),
            line_number=QColor(150, 150, 150),
            line_number_bg=QColor(40, 40, 40),
            selection=QColor(58, 91, 138),
            search_match=QColor(100, 100, 0, 100),
            current_match=QColor(180, 100, 0, 150),
            comment=QColor(106, 153, 85),
            keyword=QColor(86, 156, 214),
            string=QColor(206, 145, 120),
            number=QColor(181, 206, 168),
            function=QColor(78, 201, 176),
            operator=QColor(180, 180, 180)
        )
        
        self._themes["light"] = light
        self._themes["dark"] = dark
    
    def register_theme(self, theme: Theme) -> None:
        """
        Register a custom theme.
        
        Args:
            theme: Theme to register
        """
        self._themes[theme.name] = theme
    
    def get_theme(self, name: str) -> Theme:
        """
        Get a theme by name.
        
        Args:
            name: Theme name
            
        Returns:
            Theme object
            
        Raises:
            KeyError: If theme doesn't exist
        """
        if name not in self._themes:
            raise KeyError(f"Theme '{name}' not found")
        return self._themes[name]
    
    def set_current_theme(self, name: str) -> None:
        """
        Set the current active theme.
        
        Args:
            name: Theme name
            
        Raises:
            KeyError: If theme doesn't exist
        """
        if name not in self._themes:
            raise KeyError(f"Theme '{name}' not found")
        self._current_theme_name = name
    
    def get_current_theme(self) -> Theme:
        """Get the currently active theme."""
        return self._themes[self._current_theme_name]
    
    def list_themes(self) -> list:
        """Get a list of available theme names."""
        return list(self._themes.keys())
