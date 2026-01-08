# Code Editor Refactoring Plan

## Executive Summary

This document outlines the comprehensive refactoring of the code_editor package to address:
1. Monolithic files (core.py has 700+ lines mixing UI/model/logic)
2. No separation between UI and model layers
3. Highlighting bugs due to scattered decoration management
4. Tight coupling between components

## Phase 1: Repository Cleanup ✅ COMPLETE

- ✅ Moved test files to `tests/`
- ✅ Moved demo files to `examples/`
- ✅ Moved documentation to `docs/`
- ✅ Created `.gitignore`
- ✅ Clean root directory

## Phase 2: Extract Models & Services ✅ COMPLETE

**Models Created:**
- ✅ `models/line_data.py` - LineData class (extracted from core.py)
- ✅ `models/search_model.py` - SearchModel for search state

**Services Created:**
- ✅ `services/decoration_service.py` - **Critical fix for highlighting bugs**
- ✅ `services/search_service.py` - Refactored with proper safety checks
- ✅ `services/language_service.py` - Language registry

**Highlighting Reorganized:**
- ✅ Moved to `highlighting/` directory
- ✅ `highlighting/highlighter.py`
- ✅ `highlighting/theme.py`

## Phase 3: Refactor Core Editor (IN PROGRESS)

### Current State
- `core.py`: 700+ lines
- Mixed concerns: UI rendering, business logic, event handling, state management

### Target State
Split into:

1. **`ui/editor_widget.py`** (200-250 lines)
   - Pure Qt widget
   - Rendering only
   - Delegates to controllers

2. **`controllers/editor_controller.py`** (150-200 lines)
   - Coordinates between UI and services
   - Handles user interactions
   - Updates DecorationService

3. **Simplified `core.py`** (100 lines)
   - Facade for backward compatibility
   - Delegates to EditorWidget
   - Maintains public API

### Implementation Steps

#### Step 3.1: Create EditorWidget
- Extract QPlainTextEdit subclass
- Keep only Qt-specific rendering logic
- Use dependency injection for services

#### Step 3.2: Create EditorController
- Handle all business logic
- Coordinate search, decorations, shortcuts
- Manage state transitions

#### Step 3.3: Integrate DecorationService
- Replace scattered decoration code
- Use layer-based system
- Atomic updates (clear + apply)

#### Step 3.4: Maintain Public API
- Keep all existing public methods in CodeEditor
- Delegate to EditorWidget/Controllers
- No breaking changes

## Phase 4: Refactor Search Components

### Current State
- `search.py`: 390 lines mixing SearchService and SearchPopup

### Target State

1. **`ui/search_popup.py`** (150 lines)
   - Pure UI widget
   - Event emission only
   - No business logic

2. **`controllers/search_controller.py`** (100 lines)
   - Connects SearchPopup ↔ SearchService
   - Manages DecorationService for highlights
   - Handles navigation

3. **Keep `services/search_service.py`** (already refactored)
   - Pure search logic
   - Uses SearchModel

### Implementation Steps

#### Step 4.1: Extract SearchPopup UI
- Move to `ui/search_popup.py`
- Remove all business logic
- Emit signals for user actions

#### Step 4.2: Create SearchController
- Handle search requests
- Update decorations via DecorationService
- Coordinate next/prev navigation

#### Step 4.3: Integrate with EditorController
- EditorController owns SearchController
- Clean lifecycle management
- Proper cleanup on close

## Phase 5: Refactor Other UI Components

### GotoLineOverlay
- Move `goto_line_overlay.py` → `ui/goto_line_overlay.py`
- Extract controller if needed
- Integrate with EditorController

### LineNumberArea
- Move `line_numbers.py` → `ui/line_number_area.py`
- Already fairly clean (minimal logic)

### Shortcuts
- Move `shortcuts.py` → `controllers/shortcut_controller.py`
- Separate EditorActions (logic) from key bindings (UI)

## Phase 6: Update Public API

### `code_editor/__init__.py`
Update exports to maintain backward compatibility:

```python
# Main editor (backward compatible)
from .core import CodeEditor

# Models (for advanced users)
from .models import LineData

# Highlighting
from .highlighting import PygmentsHighlighter, Theme, ThemeManager

# Utils
from .highlighting.highlighter import get_lexer_for_language

# Expose layers for custom decorations
from .services import DecorationLayer

__all__ = [
    'CodeEditor',
    'LineData',
    'PygmentsHighlighter',
    'Theme',
    'ThemeManager',
    'DecorationLayer',
    'get_lexer_for_language',
]
```

## Phase 7: Testing & Validation

### Fix Example Imports
Update all examples to use new structure:
- Fix import paths
- Test each demo application
- Ensure no regressions

### Create Unit Tests
Now that we have proper separation:
- Test services without Qt (SearchService, LanguageService)
- Test models (SearchModel, LineData)
- Test DecorationService with mock editor

### Integration Tests
- Test full editor workflow
- Verify highlighting fixes
- Test all keyboard shortcuts

## Critical: Fixing Highlighting Bugs

### Root Cause
Decorations scattered across multiple methods:
- `_update_current_line_highlight()` - sets ExtraSelections
- `_on_search_requested()` - sets ExtraSelections
- `add_decoration()` - modifies ExtraSelections
- Race conditions and conflicts

### Solution: DecorationService

**Before (buggy):**
```python
def _update_decorations(self):
    selections = []
    # Add current line
    selections.append(self._current_line_selection)
    # Add search matches
    selections.extend(self._search_selections)
    # Add custom
    selections.extend(self._custom_selections)
    self.setExtraSelections(selections)

# Problem: Called from multiple places, state inconsistent
```

**After (fixed):**
```python
def _update_current_line(self):
    decoration_service.clear_layer(DecorationLayer.CURRENT_LINE)
    decoration_service.add_decoration(
        DecorationLayer.CURRENT_LINE, cursor, color, full_width=True
    )
    decoration_service.apply()  # Atomic

def _on_search_requested(self):
    decoration_service.clear_layer(DecorationLayer.SEARCH_MATCHES)
    decoration_service.clear_layer(DecorationLayer.CURRENT_MATCH)
    
    for match in matches:
        decoration_service.add_decoration(
            DecorationLayer.SEARCH_MATCHES, match.cursor, yellow
        )
    
    if current_match:
        decoration_service.add_decoration(
            DecorationLayer.CURRENT_MATCH, current_match.cursor, orange
        )
    
    decoration_service.apply()  # Atomic
```

**Benefits:**
- ✅ Single source of truth
- ✅ Proper layering (CURRENT_LINE < SEARCH < CURRENT_MATCH)
- ✅ Atomic updates
- ✅ No race conditions
- ✅ Easy to clear by layer
- ✅ **Fixes all persistence bugs**

## Timeline

- **Phase 1**: ✅ Complete (cleanup)
- **Phase 2**: ✅ Complete (models & services)
- **Phase 3**: 🔄 In Progress (refactor core.py) - **2-3 hours**
- **Phase 4**: ⏳ Pending (refactor search.py) - **1 hour**
- **Phase 5**: ⏳ Pending (other UI) - **1 hour**
- **Phase 6**: ⏳ Pending (update API) - **30 min**
- **Phase 7**: ⏳ Pending (testing) - **1 hour**

**Total estimated time**: 5-6 hours for complete refactoring

## Success Criteria

- ✅ No file > 300 lines
- ✅ Clear separation: models → services → controllers → UI
- ✅ All highlighting bugs fixed
- ✅ Backward compatible public API
- ✅ All examples work
- ✅ Code is testable (services can be unit tested)
- ✅ Clean architecture suitable for enterprise use

## Next Steps

1. Continue with Phase 3 (refactor core.py)
2. Integrate DecorationService
3. Test highlighting fixes
4. Proceed with remaining phases
