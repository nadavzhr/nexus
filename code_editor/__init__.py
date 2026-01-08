"""
Standalone Multi-Language Code Editor Widget

A professional, reusable code editor widget built with PyQt5, designed for
embedding into large-scale applications.

Features:
- Multi-language syntax highlighting via Pygments
- Line-aware interaction and metadata
- Search, decorations, and line numbering
- Clean, stable public API
- Support for custom user-defined languages
- VS Code-style search popup
- Keyboard shortcuts for common actions
- Theme support (light/dark)
- Current line highlighting
"""

from .core import CodeEditor, LineData
from .highlighter import PygmentsHighlighter
from .line_numbers import LineNumberArea
from .theme import Theme, ThemeManager
from .search import SearchService, SearchPopup
from .shortcuts import EditorActions

__all__ = [
    'CodeEditor',
    'LineData',
    'PygmentsHighlighter',
    'LineNumberArea',
    'Theme',
    'ThemeManager',
    'SearchService',
    'SearchPopup',
    'EditorActions',
]

__version__ = '0.2.0'
