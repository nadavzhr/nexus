```markdown
# Standalone Multi-Language Code Editor Widget — Architecture & Implementation Plan

## 1. Purpose & Scope

This document defines a **right-sized, professional architecture** for a **standalone code editor widget** built with **PyQt5**, designed to be embedded into **large-scale applications**.

The goal is **not** to build an IDE or a VS Code clone, but to provide:

- A robust, reusable **code editor widget**
- Multi-language **syntax highlighting** (via Pygments, including custom languages)
- Line-aware interaction and metadata (list-like behavior in read-only mode)
- Search, background highlighting, and line numbering
- A **clean, stable, and complete public API** suitable for long-term reuse

The editor must be **self-contained**, extensible, and predictable in behavior.

---

## 2. Design Principles

### 2.1 Core Principles

- **Stand-alone widget**  
  The editor is a single reusable component, not an app-level subsystem.

- **Separation of concerns**
  - Qt owns text storage, layout, and painting
  - The editor owns metadata, interaction, and APIs

- **Line-centric mental model**
  - Visual unit = `QTextBlock` (line)
  - Each line can carry its own data model

- **Incremental, lightweight behavior**
  - No full-document reprocessing on keystrokes
  - No ASTs or heavy semantic analysis

- **API-first design**
  - External applications must be able to observe, query, and control behavior
  - No reliance on subclassing for integration

---

## 3. Technology Choice

### 3.1 Base Widget

**`QPlainTextEdit` (mandatory)**

Reasons:
- One `QTextBlock` per visual line
- Predictable layout and scrolling
- High performance for large documents
- Same foundation used by Qt Creator

---

## 4. High-Level Architecture

```

CodeEditor (QPlainTextEdit)
├── QTextDocument (Qt-owned)
│   └── QTextBlock (1 per line)
│       └── QTextBlockUserData (line model)
├── Syntax Highlighting (Pygments → QSyntaxHighlighter)
├── Decorations (ExtraSelections)
├── Line Number Gutter (QWidget)
├── Search Service
└── Public API Facade

````

This architecture intentionally avoids Qt’s Model/View framework while still providing **list-like semantics**.

---

## 5. Line-as-Data-Model Concept

### 5.1 QTextBlock as “Item”

Each `QTextBlock` represents a logical line and acts as the equivalent of a `QListView` row.

### 5.2 Per-Line Data Model

Each block may store metadata via `QTextBlockUserData`:

```python
class LineData(QTextBlockUserData):
    payload: object        # user-defined data
    bg_color: QColor | None
    tags: set[str]
````

This enables:

* Line-specific data retrieval
* Double-click interaction
* Background coloring
* External annotations

---

## 6. Editable vs Read-Only Modes

### Editable Mode

* Normal text editing
* Syntax highlighting
* Optional decorations

### Read-Only Mode

* No text mutation
* Lines behave like selectable items
* Double-click emits line data
* Optional hover highlighting

This is achieved via:

```python
editor.setReadOnly(True)
```

---

## 7. Syntax Highlighting & Language Support

### 7.1 Highlighting Strategy

* Use **Pygments** exclusively for syntax highlighting
* Wrap Pygments lexers inside a `QSyntaxHighlighter`
* Highlighting is **purely visual**
* No semantic meaning stored in the document

### 7.2 Custom Language Support (Key Requirement)

The editor must support **custom user-defined languages** via custom Pygments lexers.

#### Language Registration API

```python
editor.register_language(
    name="MyLang",
    file_extensions=[".mlg"],
    lexer=my_pygments_lexer
)
```

#### Design Goals

* No editor modification required for new languages
* Language switching at runtime
* Multiple languages supported across different editor instances

---

## 8. Background Coloring & Decorations

### 8.1 Decoration Mechanism

Use `QTextEdit.ExtraSelection` exclusively for overlays:

* Background coloring
* Search result highlighting
* Hover highlighting
* Active line indicators

Benefits:

* No document mutation
* Fast repaint
* Layerable and removable

---

## 9. Search Capabilities

### 9.1 Search UI

* Lightweight popup widget (VS Code–style)
* Supports:

  * Plain text search
  * Regex search
  * Next / previous navigation

### 9.2 Search Engine

* Based on `QTextDocument.find()`
* Results highlighted using `ExtraSelections`
* Fully incremental and fast

Search logic is implemented as a **service**, not embedded in the editor core.

---

## 10. Line Number Gutter

### 10.1 Structure

* Separate `QWidget` docked to the left of the editor
* Synced with editor scrolling

### 10.2 Responsibilities

* Line numbers
* Optional markers (errors, bookmarks, custom icons)
* Driven by `QTextBlock` iteration and metadata

---

## 11. Interaction Model

### 11.1 Mouse Interaction

* Hover → highlight line
* Double-click → emit associated line data
* Cursor-to-block mapping via `cursorForPosition()`

### 11.2 Signals

```python
lineActivated(line_number: int, line_data: object)
cursorMoved(line_number: int)
```

These mirror `QListView`-style interactions.

---

## 12. Public API Design (Critical)

The widget must expose a **stable and complete API**.

### 12.1 Document & Line Access

```python
editor.document()
editor.get_line_data(line_number)
editor.set_line_data(line_number, data)
```

### 12.2 Language & Highlighting

```python
editor.register_language(...)
editor.set_language(name)
```

### 12.3 Decorations

```python
editor.add_decoration(range, style)
editor.clear_decorations(type)
```

### 12.4 Search

```python
editor.search(pattern, regex=False)
editor.clear_search()
```

### 12.5 Mode Control

```python
editor.setReadOnly(True)
editor.setEditable(True)
```

All advanced behavior must be accessible **without subclassing**.

---

## 13. Extensibility Strategy

Future features must integrate via:

* Block user data
* Decorations
* Gutter painting
* Public APIs

Examples:

* Bookmarks
* Diagnostics
* Execution highlights
* Diff overlays

No architectural rewrite required.

---

## 14. Complexity & Feasibility

### Estimated Effort

* Core editor & API: 1–2 weeks
* Syntax highlighting & language system: 1 week
* Search & decorations: 1 week
* Gutter & interactions: 1 week

**Total: ~3–5 weeks**

This remains a **medium-complexity project**, not an IDE.

---

## 15. Final Summary

This plan defines a **standalone, reusable, professional-grade code editor widget** that:

* Leverages Qt’s strengths instead of fighting them
* Treats lines as interactive data objects
* Supports multi-language and custom syntax highlighting
* Provides search, background coloring, and line numbering
* Exposes a clean API suitable for large applications

The result is a **powerful yet maintainable editor component**, positioned exactly between a simple text editor and a full IDE.

```
```
