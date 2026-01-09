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
- Centralized decoration management (fixes highlighting bugs)
"""

# Main widget and data model (backward compatible)
from .core import CodeEditor, LineData

# Import from new modular structure
from .highlighting.highlighter import PygmentsHighlighter
from .highlighting.theme import Theme, ThemeManager
from .ui.line_number_area import LineNumberArea
from .ui.search_popup import SearchService, SearchPopup
from .ui.goto_line_overlay import GotoLineOverlay
from .services.decoration_service import DecorationService, DecorationLayer
from .shortcuts import EditorActions

# Backward compatibility - also export from models and services
from .models.line_data import LineData as _LineDataModel
from .models.search_model import SearchModel

__all__ = [
    # Main API (backward compatible)
    'CodeEditor',
    'LineData',
    
    # UI Components
    'PygmentsHighlighter',
    'LineNumberArea',
    'Theme',
    'ThemeManager',
    'SearchService',
    'SearchPopup',
    'EditorActions',
    'GotoLineOverlay',
    
    # Services (new - for advanced users)
    'DecorationService',
    'DecorationLayer',
    'SearchModel',
]

__version__ = '0.3.0'  # Version bump for refactoring
