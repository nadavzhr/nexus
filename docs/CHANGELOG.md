# Changelog - CodeEditor Widget

## Version 0.2.0 (January 2026)

### New Features

#### 1. VS Code-Style Search Popup
- **Location:** Top-right corner of editor
- **Features:**
  - Case sensitive search toggle
  - Regex search support
  - Whole word matching
  - Match counter (e.g., "3 of 15")
  - Previous/Next navigation buttons
  - Visual highlighting (yellow for all matches, orange for current)
  - Remembers last search query
- **Keyboard Shortcut:** Ctrl+F
- **API:** `editor.show_search_popup()`

#### 2. Keyboard Shortcuts
All shortcuts scoped to widget context only:

| Shortcut | Action | Description |
|----------|--------|-------------|
| Ctrl+/ | Comment/Uncomment | Language-aware (supports #, //, --, <!--) |
| Ctrl+D | Duplicate Line | Duplicates current line or selection |
| Ctrl+C | Smart Copy | Copies line when no selection, normal copy otherwise |
| Ctrl+X | Smart Cut | Cuts line when no selection, normal cut otherwise |
| Alt+Up | Move Line Up | Moves current line up, preserves cursor position |
| Alt+Down | Move Line Down | Moves current line down, preserves cursor position |
| Ctrl+G | Go to Line | Opens dialog to jump to specific line number |
| Ctrl+F | Find | Opens search popup |

**Public API:**
- `editor.toggle_comment()`
- `editor.duplicate_line()`
- `editor.copy_line()`
- `editor.cut_line()`
- `editor.move_line_up()`
- `editor.move_line_down()`
- `editor.go_to_line()`
- `editor.jump_to_line(line_number)`

#### 3. Theme Support
- **Built-in themes:** Light, Dark
- **Custom theme support:** Register your own themes
- **Dynamic switching:** Change themes at runtime
- **Comprehensive coverage:** Affects all editor components
  - Background and text colors
  - Line numbers and gutter
  - Current line highlight
  - Search match colors
  - Syntax highlighting colors

**API:**
- `editor.set_theme(name)`
- `editor.get_current_theme()`
- `editor.register_theme(theme)`
- `editor.list_themes()`

#### 4. Current Line Highlighting
- Subtle background highlight for the line containing cursor
- Auto-updates on cursor movement
- Theme-aware colors
- Can be toggled on/off

**API:**
- `editor.set_current_line_highlight_enabled(enabled)`

### Architecture Enhancements

**New Modules:**
- `code_editor/theme.py` - Theme management system
- `code_editor/search.py` - Search service and popup widget
- `code_editor/shortcuts.py` - Editor actions and keyboard shortcuts

**Design Principles Maintained:**
- ✅ Modular design (separate concerns)
- ✅ Decoupled components (service vs. UI)
- ✅ Line-centric behavior
- ✅ API-first approach
- ✅ 100% backward compatible

### Bug Fixes
1. Fixed potential infinite loop in regex search with zero-width matches
2. Fixed highlighter theme attribute initialization
3. Fixed cursor positioning when moving lines with different lengths
4. Improved search robustness with edge case handling

### Testing
- Added comprehensive test suite
- All v0.1.0 APIs remain unchanged
- No breaking changes
- Performance: No regressions, all features optimized

### Documentation
- Complete API reference in API.md
- Feature guide in ENHANCEMENTS.md
- Multiple demo applications
- Code examples for all new features

---

## Version 0.1.0 (Initial Release)

### Core Features
- Multi-language syntax highlighting via Pygments
- Line-aware data model (QTextBlock + LineData)
- Line numbering gutter
- Search and decoration support
- Read-only and editable modes
- Clean public API for integration
- Custom language registration

### Components
- CodeEditor widget (QPlainTextEdit-based)
- LineData class (per-line metadata)
- PygmentsHighlighter (syntax highlighting)
- LineNumberArea (gutter widget)

### API
- Document and line access
- Language registration and switching
- Decoration system
- Search functionality
- Mode control
- Signals (lineActivated, cursorMoved)

---

## Upgrade Guide: 0.1.0 → 0.2.0

**No code changes required!** All v0.1.0 APIs remain fully compatible.

**Optional enhancements to adopt:**
```python
# Use new themes
editor.set_theme('dark')

# Use new search popup
editor.show_search_popup()  # or press Ctrl+F

# Use new shortcuts (automatic)
# Just press Ctrl+/, Ctrl+D, etc.

# Enable/disable current line highlighting
editor.set_current_line_highlight_enabled(True)
```

All new features are additive and opt-in.
