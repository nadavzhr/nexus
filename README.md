# Multi-Language Code Editor Widget

A professional, standalone code editor widget built with PyQt5, designed for embedding into large-scale applications.

## Features

- **Multi-language syntax highlighting** via Pygments (Python, JavaScript, Java, HTML, and more)
- **Custom language support** - register your own Pygments lexers
- **Line-aware data model** - attach metadata to individual lines
- **Read-only and editable modes** - switch between editing and browsing
- **Line numbering gutter** - professional code editor appearance
- **Search functionality** - find and highlight text
- **Decorations** - custom background colors and highlights
- **Clean public API** - easy integration without subclassing

## Architecture

Built on `QPlainTextEdit` with a line-centric design:

```
CodeEditor (QPlainTextEdit)
├── QTextDocument (Qt-owned)
│   └── QTextBlock (1 per line)
│       └── QTextBlockUserData (line metadata)
├── Syntax Highlighting (Pygments → QSyntaxHighlighter)
├── Decorations (ExtraSelections)
├── Line Number Gutter (QWidget)
└── Search Service
```

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from PyQt5.QtWidgets import QApplication
from code_editor import CodeEditor
from code_editor.highlighter import get_lexer_for_language

app = QApplication([])

# Create editor
editor = CodeEditor()

# Register and set language
python_lexer = get_lexer_for_language('python')
editor.register_language('python', python_lexer)
editor.set_language('python')

# Set code
editor.setPlainText("""
def hello():
    print("Hello, World!")
""")

editor.show()
app.exec_()
```

### Line Data and Metadata

```python
from code_editor import LineData

# Create line data
data = LineData(payload={"type": "function", "name": "main"})
editor.set_line_data(0, data)

# Or create directly
editor.create_line_data(1, payload={"important": True})

# Retrieve line data
line_data = editor.get_line_data(0)
if line_data:
    print(line_data.payload)
```

### Read-Only Mode with Line Activation

```python
# Enable read-only mode
editor.setReadOnly(True)

# Connect to line activation signal
def on_line_activated(line_number, data):
    print(f"Line {line_number} clicked: {data}")

editor.lineActivated.connect(on_line_activated)
```

### Search

```python
# Search for text
matches = editor.search("hello")
print(f"Found {matches} matches")

# Clear search
editor.clear_search()
```

### Custom Decorations

```python
from PyQt5.QtGui import QColor

# Add custom background color to a line
pink = QColor(255, 200, 200)
editor.add_decoration(line_number=5, bg_color=pink, decoration_type='custom')

# Clear decorations
editor.clear_decorations('custom')
```

### Custom Language Registration

```python
from pygments.lexer import RegexLexer
from pygments import token

class MyCustomLexer(RegexLexer):
    tokens = {
        'root': [
            (r'KEYWORD', token.Keyword),
            (r'[a-zA-Z_]\w*', token.Name),
            # ... more rules
        ]
    }

editor.register_language('mycustom', MyCustomLexer(), ['.mc'])
editor.set_language('mycustom')
```

## Demo Application

Run the comprehensive demo to see all features:

```bash
python demo.py
```

The demo showcases:
- Multiple language support (Python, JavaScript, Java, HTML)
- Syntax highlighting
- Read-only/editable mode switching
- Search functionality
- Custom decorations
- Line metadata and activation
- Hover highlighting

## Public API

### Document & Line Access

- `editor.get_line_data(line_number)` - Get LineData for a line
- `editor.set_line_data(line_number, data)` - Set LineData for a line
- `editor.create_line_data(line_number, payload, bg_color)` - Create and set LineData
- `editor.get_line_text(line_number)` - Get text of a specific line
- `editor.line_count()` - Get total number of lines

### Language & Highlighting

- `editor.register_language(name, lexer, file_extensions)` - Register a language
- `editor.set_language(name)` - Set active language
- `editor.get_current_language()` - Get current language name
- `editor.disable_highlighting()` - Disable syntax highlighting

### Decorations

- `editor.add_decoration(line_number, bg_color, type)` - Add line decoration
- `editor.clear_decorations(type)` - Clear decorations of a type

### Search

- `editor.search(pattern, regex)` - Search and highlight matches
- `editor.clear_search()` - Clear search highlighting

### Mode Control

- `editor.setReadOnly(bool)` - Set read-only mode
- `editor.setEditable(bool)` - Set editable mode
- `editor.set_hover_enabled(bool)` - Enable/disable hover in read-only mode

### Signals

- `lineActivated(line_number, data)` - Emitted on double-click in read-only mode
- `cursorMoved(line_number)` - Emitted when cursor position changes

## Design Principles

1. **Standalone widget** - Self-contained, reusable component
2. **Separation of concerns** - Qt handles text, editor handles metadata and APIs
3. **Line-centric model** - Each line is a data object with metadata
4. **Incremental behavior** - No full-document reprocessing
5. **API-first design** - Full control without subclassing

## License

See repository license.

## Contributing

This is a professional implementation following the architecture defined in `plan.md`. 
Contributions should maintain the design principles and API stability.
