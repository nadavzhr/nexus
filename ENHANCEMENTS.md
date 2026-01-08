# CodeEditor v0.2.0 - Enhanced Features

## What's New in v0.2.0

This release adds professional-grade enhancements requested in the review feedback:

### 1. VS Code-Style Search Popup ✨

A fully-featured search popup that appears in the top-right corner of the editor.

**Features:**
- **Multiple search modes:** Exact match, regex, case sensitivity, whole word
- **Match navigation:** Previous/Next buttons to jump between matches
- **Visual highlighting:** All matches highlighted in yellow, current match in orange
- **Match counter:** Shows "X of Y" matches
- **Persistent:** Remembers last search query when reopened
- **Keyboard shortcut:** Ctrl+F

**Usage:**
```python
editor = CodeEditor()

# Show search popup
editor.show_search_popup()

# Or use keyboard shortcut: Ctrl+F
```

**Screenshot:**
![Search Popup](https://github.com/user-attachments/assets/fd14683c-2414-48ea-b8ca-cd5fe86fed16)

---

### 2. Keyboard Shortcuts ⌨️

Professional code editor shortcuts for common operations.

| Shortcut | Action | Description |
|----------|--------|-------------|
| **Ctrl+/** | Toggle Comment | Comment/uncomment current line or selection |
| **Ctrl+D** | Duplicate Line | Duplicate current line or selection |
| **Alt+Up** | Move Line Up | Move current line up |
| **Alt+Down** | Move Line Down | Move current line down |
| **Ctrl+G** | Go to Line | Open dialog to jump to specific line |
| **Ctrl+F** | Find | Open search popup |

**All actions also available via public API:**
```python
editor.toggle_comment()      # Comment/uncomment
editor.duplicate_line()       # Duplicate line
editor.move_line_up()        # Move line up
editor.move_line_down()      # Move line down
editor.go_to_line()          # Show go-to-line dialog
editor.jump_to_line(42)      # Jump directly to line 42
```

**Smart comment detection:**
- Python, Ruby, Bash: `#`
- JavaScript, Java, C++: `//`
- SQL, Lua: `--`
- HTML, XML: `<!--`

---

### 3. Theme Support 🎨

Dynamic light and dark themes with full customization support.

**Built-in themes:**
- **Light** - Clean, professional light theme
- **Dark** - Modern dark theme with comfortable contrast

**Theme affects:**
- Editor background and text
- Line numbers and gutter
- Current line highlight
- Search match colors
- Syntax highlighting colors

**Usage:**
```python
editor = CodeEditor()

# Switch to dark theme
editor.set_theme('dark')

# Switch to light theme
editor.set_theme('light')

# List available themes
themes = editor.list_themes()  # ['light', 'dark']

# Get current theme
theme = editor.get_current_theme()
print(theme.name)  # 'dark'
```

**Custom themes:**
```python
from code_editor import Theme
from PyQt5.QtGui import QColor

custom_theme = Theme(
    name="ocean",
    background=QColor(0, 43, 54),
    text=QColor(131, 148, 150),
    current_line=QColor(7, 54, 66),
    line_number=QColor(88, 110, 117),
    line_number_bg=QColor(0, 43, 54),
    selection=QColor(38, 139, 210),
    search_match=QColor(181, 137, 0, 100),
    current_match=QColor(203, 75, 22, 150),
    comment=QColor(88, 110, 117),
    keyword=QColor(38, 139, 210),
    string=QColor(42, 161, 152),
    number=QColor(211, 54, 130),
    function=QColor(133, 153, 0),
    operator=QColor(147, 161, 161)
)

editor.register_theme(custom_theme)
editor.set_theme('ocean')
```

**Screenshots:**

**Dark Theme:**
![Dark Theme](https://github.com/user-attachments/assets/9b1a6241-a6e6-4dd9-9ae9-f60bdc2c0e4d)

**Light Theme:**
![Light Theme](https://github.com/user-attachments/assets/2276f113-83ed-46bd-abed-325137649a99)

---

### 4. Current Line Highlighting 📍

Visual indicator showing the currently active line.

**Features:**
- Subtle background highlight for the line containing the cursor
- Updates automatically as cursor moves
- Themeable colors (different for light/dark themes)
- Can be toggled on/off

**Usage:**
```python
editor = CodeEditor()

# Enable current line highlighting (enabled by default)
editor.set_current_line_highlight_enabled(True)

# Disable
editor.set_current_line_highlight_enabled(False)
```

---

## Enhanced Demo

Run the enhanced demo to see all new features:

```bash
python demo_enhanced.py
```

The demo includes:
- Theme switcher (light/dark)
- Current line highlight toggle
- All keyboard shortcuts demonstrated
- Search popup integration
- Interactive controls

---

## API Reference Updates

### New Classes

#### `Theme`
```python
@dataclass
class Theme:
    name: str
    background: QColor
    text: QColor
    current_line: QColor
    line_number: QColor
    line_number_bg: QColor
    selection: QColor
    search_match: QColor
    current_match: QColor
    comment: QColor
    keyword: QColor
    string: QColor
    number: QColor
    function: QColor
    operator: QColor
```

#### `SearchPopup`
VS Code-style search widget with controls.

#### `SearchService`
Backend search logic (independent of UI).

#### `EditorActions`
Collection of editor actions (comment, duplicate, move lines, etc.).

---

### New Methods

#### Theme Management
```python
editor.set_theme(name: str) -> None
editor.get_current_theme() -> Theme
editor.register_theme(theme: Theme) -> None
editor.list_themes() -> List[str]
```

#### Search
```python
editor.show_search_popup() -> None
```

#### Line Operations
```python
editor.toggle_comment() -> None
editor.duplicate_line() -> None
editor.move_line_up() -> None
editor.move_line_down() -> None
editor.go_to_line() -> None
editor.jump_to_line(line_number: int) -> None
```

#### Current Line
```python
editor.set_current_line_highlight_enabled(enabled: bool) -> None
```

---

## Architecture

All enhancements maintain the original architecture principles:

```
CodeEditor (QPlainTextEdit)
├── ThemeManager (light/dark themes)
├── SearchService (search logic)
├── SearchPopup (VS Code-style UI)
├── EditorActions (keyboard shortcuts)
├── QTextDocument → QTextBlock → LineData
├── PygmentsHighlighter (theme-aware)
├── ExtraSelections (decorations + current line)
├── LineNumberArea (theme-aware gutter)
└── Public API (50+ methods)
```

**Design Principles Maintained:**
- ✅ Modular (separate files: theme.py, search.py, shortcuts.py)
- ✅ Decoupled (SearchService independent of SearchPopup)
- ✅ Line-centric behavior preserved
- ✅ API-first (all features accessible programmatically)
- ✅ No breaking changes to existing API

---

## Migration from v0.1.0

All v0.1.0 APIs remain fully compatible. New features are additive:

```python
# v0.1.0 code still works
editor = CodeEditor()
editor.register_language('python', lexer)
editor.set_language('python')

# v0.2.0 additions (optional)
editor.set_theme('dark')              # NEW
editor.show_search_popup()            # NEW
editor.toggle_comment()               # NEW
editor.set_current_line_highlight_enabled(True)  # NEW
```

---

## Testing

All features have been tested:

```bash
# Test enhanced features
python test_enhanced.py

# Test search popup
python test_search_popup.py

# Interactive demo
python demo_enhanced.py
```

**Test Results:**
- ✅ Theme switching (light/dark)
- ✅ Search popup with match highlighting
- ✅ Keyboard shortcuts (all 6 shortcuts)
- ✅ Current line highlighting
- ✅ API compatibility with v0.1.0

---

## Performance

All enhancements are designed for minimal overhead:

- **Theme switching:** O(1) - instant palette update
- **Current line highlighting:** O(1) - single decoration update
- **Search:** O(n) where n = document length (Qt's native search)
- **Shortcuts:** O(1) - direct cursor manipulation

No performance regression compared to v0.1.0.

---

## Credits

Enhanced based on review feedback from @nadavzhr.

Version 0.2.0 - January 2026
