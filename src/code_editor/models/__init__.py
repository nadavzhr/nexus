"""
Data models for the code editor.

This module contains pure data models with no Qt UI dependencies.
"""

from .line_data import LineData
from .search_model import SearchModel

__all__ = ['LineData', 'SearchModel']
