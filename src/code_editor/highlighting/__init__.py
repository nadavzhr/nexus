"""
Syntax highlighting components.

This module contains Pygments-based syntax highlighting and theme management.
"""

from .highlighter import PygmentsHighlighter, get_lexer_for_language
from .theme import Theme, ThemeManager

__all__ = ['PygmentsHighlighter', 'get_lexer_for_language', 'Theme', 'ThemeManager']
