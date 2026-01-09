# Architecture Documentation

## Professional Code Editor Widget - Refactored Architecture

This document describes the professionally refactored architecture of the code editor widget, which follows SOLID principles, PyQt5 best practices, and provides a rich, self-contained API.

## Design Principles

### 1. Model/View Separation

The architecture cleanly separates data models from UI components:

#### Models (`code_editor.models`)
- **LineData**: Per-line metadata storage (payload, color, tags)
- **SearchModel**: Search state and results
- **SearchMatch**: Individual search match representation
- **EditorConfig**: Configuration settings (dataclass)

#### Views (`code_editor.ui`)
- **CodeEditor**: Main editor widget (QPlainTextEdit-based)
- **SearchPopup**: VS Code-style search/replace popup
- **GotoLineOverlay**: Quick line navigation overlay
- **LineNumberArea**: Line numbering gutter

### 2. SOLID Principles

#### Single Responsibility Principle
Each component has one clear purpose:
- **Services**: Handle business logic (search, decoration, language management)
- **Controllers**: Manage keyboard shortcuts and actions
- **Models**: Store data with minimal logic
- **UI**: Presentation and user interaction

#### Open/Closed Principle
Components are open for extension, closed for modification:
- Protocol-based interfaces allow custom implementations
- Services can be replaced without modifying core code
- Theme system supports custom themes
- Language system supports custom lexers

#### Liskov Substitution Principle
All services follow defined protocols:
```python
# Any class implementing SearchServiceProtocol can replace the default
class CustomSearchService(SearchServiceProtocol):
    # Implement protocol methods
    pass

editor._search_service = CustomSearchService(editor.document())
```

#### Interface Segregation Principle
Clear, focused protocols for each service:
- `SearchServiceProtocol`: Search operations only
- `DecorationServiceProtocol`: Decoration management only
- `LanguageServiceProtocol`: Language/lexer management only
- `ThemeProtocol`: Theme properties only

#### Dependency Inversion Principle
High-level modules depend on abstractions (protocols):
```python
# Editor depends on protocols, not concrete implementations
def __init__(self):
    self._search_service: SearchServiceProtocol = SearchService(...)
    self._decoration_service: DecorationServiceProtocol = DecorationService(...)
```

### 3. PyQt5 Idiomatic Patterns

#### Qt Properties
Key settings exposed as Qt properties for Designer/QML integration:
```python
editor = CodeEditor()
editor.currentLanguage = 'python'  # Qt property
editor.hoverEnabled = True          # Qt property
editor.currentLineHighlightEnabled = True  # Qt property
```

#### Signals & Slots
Rich signal-based API for loose coupling:
```python
# Cursor movement signal
editor.cursorMoved.connect(lambda line: print(f"Line {line}"))

# Line activation (double-click in read-only mode)
editor.lineActivated.connect(lambda line, data: print(f"Activated: {data}"))
```

#### Native Qt Features
- Uses `QPlainTextEdit` as base (native performance)
- Leverages `QTextDocument` for text storage
- Uses `ExtraSelections` for decorations (native)
- Uses `QSyntaxHighlighter` for syntax highlighting
- Uses `setFocusProxy()` for focus management
- Uses `QShortcut` with proper context for keyboard shortcuts

### 4. Service-Oriented Architecture

#### Services Layer (`code_editor.services`)

**DecorationService**
- Centralized decoration management with layers
- Atomic updates (clear + apply together)
- Prevents highlighting conflicts
- Supports: CUSTOM, CURRENT_LINE, SEARCH_MATCHES, CURRENT_MATCH

**SearchService**
- Business logic for text search
- Supports: regex, case-sensitive, whole-word matching
- Manages search results and navigation
- Independent of UI

**LanguageService**
- Manages programming language lexers
- Language registration and switching
- Pygments integration

#### Controllers Layer (`code_editor.controllers`)

**EditorActions**
- Keyboard shortcut implementations
- Actions: comment/uncomment, duplicate line, move line, copy/cut/paste
- Reusable action methods (callable from code or shortcuts)

### 5. Self-Contained Widgets

Each widget is fully self-contained and reusable:

#### SearchPopup
- Complete search/replace UI
- Keyboard navigation (Tab, Enter, Escape)
- Alt shortcuts (Alt+C, Alt+R, Alt+W)
- Rich signals for integration
- Can be used standalone or embedded

#### GotoLineOverlay
- Quick line navigation
- Live preview as you type
- Input validation
- Auto-positioning
- Can be used standalone

#### LineNumberArea
- Auto-sizing based on line count
- Theme-aware coloring
- Efficient painting (only visible lines)
- Can be used with any QPlainTextEdit

## API Design

### Public Methods API

**Document & Lines**
```python
editor.get_line_data(line_number) -> Optional[LineData]
editor.set_line_data(line_number, data) -> bool
editor.create_line_data(line_number, payload=None, bg_color=None) -> bool
editor.get_line_text(line_number) -> Optional[str]
editor.line_count() -> int
```

**Language & Highlighting**
```python
editor.register_language(name, lexer, file_extensions=[])
editor.set_language(name) -> bool
editor.get_current_language() -> Optional[str]
editor.disable_highlighting()
```

**Search & Navigation**
```python
editor.show_search_popup()  # Ctrl+F
editor.show_replace_popup()  # Ctrl+H
editor.search(pattern, regex=False) -> int
editor.clear_search()
editor.go_to_line()  # Ctrl+G
editor.jump_to_line(line_number)
```

**Decorations**
```python
editor.add_decoration(line_number, bg_color, type='custom')
editor.clear_decorations(type=None)
```

**Themes**
```python
editor.set_theme('dark')
editor.get_current_theme() -> Theme
editor.register_theme(custom_theme)
editor.list_themes() -> List[str]
```

**Actions**
```python
editor.toggle_comment()   # Ctrl+/
editor.duplicate_line()   # Ctrl+D
editor.move_line_up()     # Alt+Up
editor.move_line_down()   # Alt+Down
editor.copy_line()        # Ctrl+C (no selection)
editor.cut_line()         # Ctrl+X (no selection)
editor.paste_line()       # Ctrl+V (line-aware)
```

### Signals API

**lineActivated(int, object)**
- Emitted on double-click in read-only mode
- Args: line_number (0-based), line_data (payload or None)

**cursorMoved(int)**
- Emitted when cursor position changes
- Args: line_number (0-based)

### Qt Properties API

**currentLanguage** (str)
- Get/set the active language for syntax highlighting

**hoverEnabled** (bool)
- Get/set hover highlighting in read-only mode

**currentLineHighlightEnabled** (bool)
- Get/set current line highlighting

## Extension Points

### Custom Search Implementation
```python
from code_editor.protocols import SearchServiceProtocol

class MySearchService:
    """Custom search with advanced features."""
    
    def search(self, pattern, case_sensitive=False, use_regex=False, whole_word=False):
        # Custom search logic
        pass
    
    # Implement other protocol methods...

editor = CodeEditor()
editor._search_service = MySearchService(editor.document())
```

### Custom Theme
```python
from code_editor import Theme
from PyQt5.QtGui import QColor

custom_theme = Theme(
    name="custom",
    background=QColor("#1e1e1e"),
    text=QColor("#d4d4d4"),
    # ... other colors
)

editor.register_theme(custom_theme)
editor.set_theme("custom")
```

### Custom Language
```python
from pygments.lexer import RegexLexer
from pygments import token

class MyLexer(RegexLexer):
    tokens = {
        'root': [
            (r'KEYWORD', token.Keyword),
            # ... more rules
        ]
    }

editor.register_language('mylang', MyLexer(), ['.ml'])
editor.set_language('mylang')
```

## Testing Strategy

### Protocol-Based Testing
Services follow protocols, making them easy to mock:
```python
class MockSearchService:
    """Mock for testing without Qt dependencies."""
    
    def search(self, pattern, **kwargs):
        return 0  # Mock implementation

# Use in tests
editor._search_service = MockSearchService()
```

### Signal Testing
Rich signals enable integration testing:
```python
def test_cursor_signal():
    editor = CodeEditor()
    signals_received = []
    editor.cursorMoved.connect(lambda line: signals_received.append(line))
    # Test cursor movement
    assert len(signals_received) > 0
```

## Performance Considerations

1. **Lazy Initialization**: Widgets created on first use (SearchPopup, GotoLineOverlay)
2. **Efficient Painting**: LineNumberArea only paints visible lines
3. **Atomic Decoration Updates**: DecorationService applies all changes at once
4. **Native Qt Features**: Leverages Qt's optimized text handling

## Best Practices

1. **Use Qt Properties**: For settings that may be configured in Qt Designer
2. **Connect to Signals**: For loose coupling between components
3. **Access Services via Protocols**: For flexibility and testing
4. **Use EditorConfig**: For managing configuration state
5. **Extend via Protocols**: For custom implementations without modifying core

## Example: Complete Integration

```python
from PyQt5.QtWidgets import QApplication, QMainWindow
from code_editor import CodeEditor, EditorConfig
from code_editor.highlighting.highlighter import get_lexer_for_language

# 1. Create application
app = QApplication([])

# 2. Configure editor
config = EditorConfig(
    tab_width=4,
    font_size=11,
    hover_enabled=True,
    theme_name='dark'
)

# 3. Create and configure editor
editor = CodeEditor()
editor.hoverEnabled = config.hover_enabled
editor.set_theme(config.theme_name)

# 4. Setup language
python_lexer = get_lexer_for_language('python')
editor.register_language('python', python_lexer)
editor.currentLanguage = 'python'  # Qt property!

# 5. Connect signals
editor.cursorMoved.connect(lambda line: print(f"Line {line + 1}"))
editor.lineActivated.connect(lambda line, data: print(f"Activated: {data}"))

# 6. Set content
editor.setPlainText("def hello():\\n    print('World!')")

# 7. Show and run
editor.show()
app.exec_()
```

## Summary

This architecture provides:
- ✅ **SOLID principles**: Clean separation of concerns
- ✅ **PyQt5 idiomatic**: Native Qt features, properties, signals
- ✅ **Self-contained**: Each widget is independent and reusable
- ✅ **Rich API**: Comprehensive methods AND signals
- ✅ **Extensible**: Protocol-based services can be replaced
- ✅ **Well-documented**: Every component has detailed docs
- ✅ **Production-ready**: Professional quality for large applications
