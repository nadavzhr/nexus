# Proper Architecture Demonstration

This document shows how to properly implement MVP with protocols and signal-based communication.

## Issue 1: Protocols Not Used

**Problem**: Protocols defined but not enforced with type hints.

**Solution**: Use Protocol types everywhere

```python
# BEFORE (protocols.py exists but unused)
class EditorPresenter:
    def __init__(self, search_service):
        self.search_service = search_service  # No type hint!

# AFTER (proper Protocol usage)
from ..protocols import SearchServiceProtocol

class EditorPresenter:
    def __init__(self, search_service: SearchServiceProtocol):
        self.search_service: SearchServiceProtocol = search_service
        # Now enforced! Can inject any implementation following protocol
```

## Issue 2: Tab Navigation Broken

**Problem**: Tab adds '\t' when search popup is open.

**Root cause**: Search popup not properly preventing Tab from reaching editor.

**Solution**: Ensure event filter stops Tab propagation

```python
# In SearchPopup.eventFilter():
if event.key() == Qt.Key_Tab:
    # Let Qt handle focus navigation within popup
    return False  # Don't consume, let it navigate
    
# But in editor.keyPressEvent():
if self._search_popup and self._search_popup.isVisible():
    # Don't process Tab when popup is open
    if event.key() == Qt.Key_Tab:
        return  # Ignore Tab
```

## Issue 3: Poor Model/View Separation

**Problem**: Editor widget has too much responsibility.

**Solution**: Implement MVP pattern

```python
# Model (pure data + signals)
class EditorModel(QObject):
    languageChanged = pyqtSignal(str)
    
    @property
    def language(self):
        return self._language
    
    @language.setter
    def language(self, value):
        if self._language != value:
            self._language = value
            self.languageChanged.emit(value)

# Presenter (coordination)
class EditorPresenter:
    def __init__(self, model, view, language_service: LanguageServiceProtocol):
        self.model = model
        self.view = view
        self.language_service = language_service
        
        # Model → View
        model.languageChanged.connect(self._update_view_language)
    
    def _update_view_language(self, language):
        lexer = self.language_service.get_lexer(language)
        self.view.set_highlighter(lexer)

# View (pure UI)
class CodeEditorView(QPlainTextEdit):
    # Just UI, no business logic
    def set_highlighter(self, lexer):
        self._highlighter.set_lexer(lexer)
```

## Issue 4: Poor Signal Communication

**Problem**: Widgets call each other's methods directly.

**Solution**: Signal-based communication only

```python
# BEFORE (tight coupling)
class SearchPopup:
    def on_next_clicked(self):
        self.parent().goto_next_match()  # Direct call!

# AFTER (loose coupling via signals)
class SearchPopup:
    nextMatchRequested = pyqtSignal()
    
    def on_next_clicked(self):
        self.nextMatchRequested.emit()  # Just emit signal

# Presenter connects them
class EditorPresenter:
    def __init__(self, ...):
        self.search_popup.nextMatchRequested.connect(self._on_next_match)
    
    def _on_next_match(self):
        # Coordinator handles the logic
        match = self.search_service.next_match()
        self.view.scroll_to_match(match)
```

## Complete Example

See `examples/mvp_demo.py` for a working demonstration of proper architecture.

## Migration Path

1. **Phase 1**: Fix Tab navigation (immediate)
2. **Phase 2**: Add Protocol type hints to existing code
3. **Phase 3**: Create EditorModel with signals
4. **Phase 4**: Create EditorPresenter
5. **Phase 5**: Refactor editor widget to be pure view
6. **Phase 6**: Convert all widgets to signal-based communication

Each phase can be done incrementally without breaking existing code.
