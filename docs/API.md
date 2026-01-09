# API Reference

## CodeEditor Class

The main editor widget that extends `QPlainTextEdit`.

### Constructor

```python
CodeEditor(parent: Optional[QWidget] = None)
```

Creates a new code editor instance.

### Properties

- `blockCount()` - Number of text blocks (lines) in the document
- `isReadOnly()` - Whether the editor is in read-only mode

### Methods

#### Document & Line Access

##### `get_line_data(line_number: int) -> Optional[LineData]`

Get the LineData object for a specific line.

**Parameters:**
- `line_number` (int): 0-based line index

**Returns:**
- `LineData` object if exists, `None` otherwise

**Example:**
```python
data = editor.get_line_data(5)
if data:
    print(data.payload)
```

##### `set_line_data(line_number: int, data: LineData) -> bool`

Set the LineData for a specific line.

**Parameters:**
- `line_number` (int): 0-based line index
- `data` (LineData): LineData object to attach

**Returns:**
- `True` if successful, `False` if line doesn't exist

##### `create_line_data(line_number: int, payload: Any = None, bg_color: Optional[QColor] = None) -> bool`

Convenience method to create and set LineData in one call.

**Parameters:**
- `line_number` (int): 0-based line index
- `payload` (Any): User-defined data
- `bg_color` (QColor): Optional background color

**Returns:**
- `True` if successful, `False` if line doesn't exist

**Example:**
```python
editor.create_line_data(10, payload={"type": "important"}, bg_color=QColor(255, 255, 0))
```

##### `get_line_text(line_number: int) -> Optional[str]`

Get the text content of a specific line.

**Parameters:**
- `line_number` (int): 0-based line index

**Returns:**
- Line text as string, or `None` if line doesn't exist

##### `line_count() -> int`

Get the total number of lines in the document.

**Returns:**
- Number of lines

#### Language & Highlighting

##### `register_language(name: str, lexer, file_extensions: Optional[List[str]] = None) -> None`

Register a language for syntax highlighting.

**Parameters:**
- `name` (str): Language identifier
- `lexer`: Pygments lexer instance or class
- `file_extensions` (List[str]): Optional file extensions (e.g., `['.py', '.pyw']`)

**Example:**
```python
from pygments.lexers import PythonLexer

editor.register_language('python', PythonLexer(), ['.py', '.pyw'])
```

##### `set_language(name: str) -> bool`

Set the active syntax highlighting language.

**Parameters:**
- `name` (str): Language identifier (must be registered first)

**Returns:**
- `True` if successful, `False` if language not found

**Example:**
```python
if editor.set_language('python'):
    print("Python highlighting enabled")
```

##### `get_current_language() -> Optional[str]`

Get the name of the currently active language.

**Returns:**
- Language name or `None` if no language is set

##### `disable_highlighting() -> None`

Disable syntax highlighting completely.

#### Decorations

##### `add_decoration(line_number: int, bg_color: QColor, decoration_type: str = 'custom') -> None`

Add a background color decoration to a line.

**Parameters:**
- `line_number` (int): 0-based line index
- `bg_color` (QColor): Background color
- `decoration_type` (str): Type of decoration ('search', 'hover', 'custom')

**Example:**
```python
from PyQt5.QtGui import QColor

# Highlight line 5 with yellow background
editor.add_decoration(4, QColor(255, 255, 0), 'custom')
```

##### `clear_decorations(decoration_type: Optional[str] = None) -> None`

Clear decorations of a specific type or all decorations.

**Parameters:**
- `decoration_type` (str): Type to clear, or `None` to clear all

**Example:**
```python
# Clear only custom decorations
editor.clear_decorations('custom')

# Clear all decorations
editor.clear_decorations()
```

#### Search

##### `search(pattern: str, regex: bool = False) -> int`

Search for a pattern and highlight all matches.

**Parameters:**
- `pattern` (str): Text to search for
- `regex` (bool): If `True`, treat pattern as regex (not fully implemented)

**Returns:**
- Number of matches found

**Example:**
```python
matches = editor.search("def ")
print(f"Found {matches} function definitions")
```

##### `clear_search() -> None`

Clear search highlighting.

#### Mode Control

##### `setReadOnly(readonly: bool) -> None`

Set read-only mode. Inherited from `QPlainTextEdit`.

**Parameters:**
- `readonly` (bool): `True` for read-only, `False` for editable

##### `setEditable(editable: bool) -> None`

Convenience method to set editable mode.

**Parameters:**
- `editable` (bool): `True` for editable, `False` for read-only

##### `set_hover_enabled(enabled: bool) -> None`

Enable or disable hover highlighting in read-only mode.

**Parameters:**
- `enabled` (bool): `True` to enable hover, `False` to disable

### Signals

#### `lineActivated(line_number: int, data: object)`

Emitted when a line is activated (double-clicked in read-only mode).

**Parameters:**
- `line_number` (int): 0-based line index
- `data` (object): The payload from the line's LineData, or `None`

**Example:**
```python
def handle_activation(line_num, data):
    print(f"Line {line_num} activated with data: {data}")

editor.lineActivated.connect(handle_activation)
```

#### `cursorMoved(line_number: int)`

Emitted when the cursor position changes.

**Parameters:**
- `line_number` (int): 0-based line index of new cursor position

**Example:**
```python
def handle_cursor(line_num):
    print(f"Cursor at line {line_num + 1}")

editor.cursorMoved.connect(handle_cursor)
```

---

## LineData Class

Per-line metadata storage, extends `QTextBlockUserData`.

### Constructor

```python
LineData(payload: Any = None, bg_color: Optional[QColor] = None)
```

**Parameters:**
- `payload` (Any): User-defined data
- `bg_color` (QColor): Optional background color

### Attributes

- `payload` (Any): User-defined data object
- `bg_color` (Optional[QColor]): Background color for the line
- `tags` (set): Set of string tags

### Methods

##### `add_tag(tag: str) -> None`

Add a tag to this line.

##### `remove_tag(tag: str) -> None`

Remove a tag from this line.

##### `has_tag(tag: str) -> bool`

Check if this line has a specific tag.

**Example:**
```python
data = LineData(payload={"important": True})
data.add_tag("todo")
data.add_tag("urgent")

if data.has_tag("urgent"):
    print("This is urgent!")
```

---

## PygmentsHighlighter Class

Syntax highlighter that uses Pygments lexers. Extends `QSyntaxHighlighter`.

### Constructor

```python
PygmentsHighlighter(document: Optional[QTextDocument] = None, 
                   lexer=None, 
                   style_name: str = 'default')
```

**Parameters:**
- `document` (QTextDocument): Document to highlight
- `lexer`: Pygments lexer instance
- `style_name` (str): Pygments style name

### Methods

##### `set_lexer(lexer) -> None`

Change the lexer and re-highlight the document.

##### `set_style(style_name: str) -> None`

Change the highlighting style.

**Example:**
```python
from code_editor.highlighter import PygmentsHighlighter
from pygments.lexers import PythonLexer

highlighter = PygmentsHighlighter(editor.document(), PythonLexer())
highlighter.set_style('monokai')
```

---

## Utility Functions

### `get_lexer_for_language(language: str)`

Get a Pygments lexer for a language name.

**Parameters:**
- `language` (str): Language name (e.g., 'python', 'javascript')

**Returns:**
- Pygments lexer instance

**Raises:**
- `ImportError`: If Pygments is not available
- `ValueError`: If language is not recognized

**Example:**
```python
from code_editor.highlighter import get_lexer_for_language

lexer = get_lexer_for_language('python')
```

---

## Complete Example

```python
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor
from code_editor import CodeEditor, LineData
from code_editor.highlighter import get_lexer_for_language

app = QApplication([])

# Create and configure editor
editor = CodeEditor()
editor.setGeometry(100, 100, 800, 600)

# Register languages
for lang in ['python', 'javascript', 'java']:
    lexer = get_lexer_for_language(lang)
    editor.register_language(lang, lexer)

# Set Python
editor.set_language('python')

# Add code
editor.setPlainText("""
def hello():
    print("Hello, World!")

hello()
""")

# Add metadata
editor.create_line_data(1, payload={"type": "function"})

# Add decoration
editor.add_decoration(1, QColor(255, 255, 200))

# Search
matches = editor.search("hello")

# Connect signals
editor.lineActivated.connect(lambda ln, data: print(f"Line {ln}: {data}"))

editor.show()
app.exec_()
```
