"""
Editor Model - Pure data/state container with change notifications.

This model holds all editor state and emits signals when state changes.
The presenter listens to these signals and updates the view accordingly.
"""

from typing import Optional
from PyQt5.QtCore import QObject, pyqtSignal


class EditorModel(QObject):
    """
    Model holding all editor state.
    
    This is a pure data model that:
    - Holds state (read-only, language, hover, etc.)
    - Emits signals when state changes
    - Has no knowledge of the view
    - Has no business logic (that's in services)
    
    Signals:
        readOnlyChanged(bool): Emitted when read-only state changes
        languageChanged(str): Emitted when language changes
        hoverEnabledChanged(bool): Emitted when hover state changes
        currentLineHighlightChanged(bool): Emitted when highlight state changes
        themeChanged(str): Emitted when theme changes
    """
    
    # Signals for state changes
    readOnlyChanged = pyqtSignal(bool)
    languageChanged = pyqtSignal(str)
    hoverEnabledChanged = pyqtSignal(bool)
    currentLineHighlightChanged = pyqtSignal(bool)
    themeChanged = pyqtSignal(str)
    
    def __init__(self):
        """Initialize the editor model with default state."""
        super().__init__()
        
        # State variables
        self._read_only = False
        self._language: Optional[str] = None
        self._hover_enabled = True
        self._current_line_highlight_enabled = True
        self._theme = "light"
    
    # Read-only property
    @property
    def read_only(self) -> bool:
        """Get read-only state."""
        return self._read_only
    
    @read_only.setter
    def read_only(self, value: bool) -> None:
        """Set read-only state and emit signal if changed."""
        if self._read_only != value:
            self._read_only = value
            self.readOnlyChanged.emit(value)
    
    # Language property
    @property
    def language(self) -> Optional[str]:
        """Get current language."""
        return self._language
    
    @language.setter
    def language(self, value: Optional[str]) -> None:
        """Set language and emit signal if changed."""
        if self._language != value:
            self._language = value
            if value:
                self.languageChanged.emit(value)
    
    # Hover enabled property
    @property
    def hover_enabled(self) -> bool:
        """Get hover enabled state."""
        return self._hover_enabled
    
    @hover_enabled.setter
    def hover_enabled(self, value: bool) -> None:
        """Set hover enabled and emit signal if changed."""
        if self._hover_enabled != value:
            self._hover_enabled = value
            self.hoverEnabledChanged.emit(value)
    
    # Current line highlight property
    @property
    def current_line_highlight_enabled(self) -> bool:
        """Get current line highlight state."""
        return self._current_line_highlight_enabled
    
    @current_line_highlight_enabled.setter
    def current_line_highlight_enabled(self, value: bool) -> None:
        """Set current line highlight and emit signal if changed."""
        if self._current_line_highlight_enabled != value:
            self._current_line_highlight_enabled = value
            self.currentLineHighlightChanged.emit(value)
    
    # Theme property
    @property
    def theme(self) -> str:
        """Get current theme."""
        return self._theme
    
    @theme.setter
    def theme(self, value: str) -> None:
        """Set theme and emit signal if changed."""
        if self._theme != value:
            self._theme = value
            self.themeChanged.emit(value)
