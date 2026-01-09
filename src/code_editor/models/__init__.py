"""
Data models for the code editor.

This module contains pure data structures with minimal logic.
"""

from .line_data import LineData
from .search_model import SearchModel, SearchMatch
from .editor_config import EditorConfig

__all__ = ['LineData', 'SearchModel', 'SearchMatch', 'EditorConfig']
