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

# Main widget (from ui/)
from .ui.editor_widget import CodeEditor

# Data models
from .models.line_data import LineData
from .models.search_model import SearchModel, SearchMatch
from .models.editor_config import EditorConfig

# Services
from .services.decoration_service import DecorationService, DecorationLayer
from .services.search_service import SearchService
from .services.language_service import LanguageService

# Controllers
from .controllers.shortcut_controller import EditorActions

# UI Components
from .ui.line_number_area import LineNumberArea
from .ui.search_popup import SearchPopup
from .ui.goto_line_overlay import GotoLineOverlay

# Highlighting
from .highlighting.highlighter import PygmentsHighlighter
from .highlighting.theme import Theme, ThemeManager

# Protocols (for type hinting and extensibility)
from .protocols import (
    SearchServiceProtocol,
    DecorationServiceProtocol,
    LanguageServiceProtocol,
    ThemeProtocol
)

__all__ = [
    # Main API
    'CodeEditor',
    'LineData',
    
    # Models
    'SearchModel',
    'SearchMatch',
    'EditorConfig',
    
    # Services
    'DecorationService',
    'DecorationLayer',
    'SearchService',
    'LanguageService',
    
    # Controllers
    'EditorActions',
    
    # UI Components
    'LineNumberArea',
    'SearchPopup',
    'GotoLineOverlay',
    
    # Highlighting
    'PygmentsHighlighter',
    'Theme',
    'ThemeManager',
    
    # Protocols (for extensibility)
    'SearchServiceProtocol',
    'DecorationServiceProtocol',
    'LanguageServiceProtocol',
    'ThemeProtocol',
]

__version__ = '1.0.0'
