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
"""

from .core import CodeEditor, LineData
from .highlighter import PygmentsHighlighter
from .line_numbers import LineNumberArea

__all__ = [
    'CodeEditor',
    'LineData',
    'PygmentsHighlighter',
    'LineNumberArea',
]

__version__ = '0.1.0'
