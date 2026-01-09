"""
Basic functionality tests for CodeEditor widget.

This script tests the core features without requiring a GUI display.
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from code_editor import CodeEditor, LineData
from code_editor.highlighting.highlighter import get_lexer_for_language

# Create QApplication (required even for non-GUI tests)
app = QApplication(sys.argv)

def test_basic_creation():
    """Test basic editor creation."""
    editor = CodeEditor()
    assert editor is not None
    print("✓ Editor creation successful")

def test_line_data():
    """Test line data functionality."""
    editor = CodeEditor()
    editor.setPlainText("Line 1\nLine 2\nLine 3")
    
    # Create line data
    data = LineData(payload={"test": "data"})
    success = editor.set_line_data(0, data)
    assert success, "Failed to set line data"
    
    # Retrieve line data
    retrieved = editor.get_line_data(0)
    assert retrieved is not None, "Failed to retrieve line data"
    assert retrieved.payload == {"test": "data"}, "Line data payload mismatch"
    
    print("✓ Line data creation and retrieval works")

def test_language_registration():
    """Test language registration and switching."""
    editor = CodeEditor()
    
    # Register Python language
    python_lexer = get_lexer_for_language('python')
    editor.register_language('python', python_lexer)
    
    # Set language
    success = editor.set_language('python')
    assert success, "Failed to set language"
    assert editor.get_current_language() == 'python', "Current language mismatch"
    
    print("✓ Language registration and switching works")

def test_read_only_mode():
    """Test read-only mode switching."""
    editor = CodeEditor()
    
    # Default is editable
    assert not editor.isReadOnly(), "Editor should start in editable mode"
    
    # Switch to read-only
    editor.setReadOnly(True)
    assert editor.isReadOnly(), "Failed to switch to read-only mode"
    
    # Switch back to editable
    editor.setEditable(True)
    assert not editor.isReadOnly(), "Failed to switch back to editable mode"
    
    print("✓ Read-only mode switching works")

def test_search():
    """Test search functionality."""
    editor = CodeEditor()
    editor.setPlainText("hello world\nhello python\ntest")
    
    # Search for "hello"
    matches = editor.search("hello")
    assert matches == 2, f"Expected 2 matches, got {matches}"
    
    # Clear search
    editor.clear_search()
    
    print("✓ Search functionality works")

def test_decorations():
    """Test decoration functionality."""
    editor = CodeEditor()
    editor.setPlainText("Line 1\nLine 2\nLine 3")
    
    # Add decoration
    color = QColor(255, 200, 200)
    editor.add_decoration(0, color, 'custom')
    
    # Clear decoration
    editor.clear_decorations('custom')
    
    print("✓ Decoration system works")

def test_line_operations():
    """Test line-related operations."""
    editor = CodeEditor()
    editor.setPlainText("Line 1\nLine 2\nLine 3")
    
    # Test line count
    assert editor.line_count() == 3, "Line count mismatch"
    
    # Test get line text
    text = editor.get_line_text(0)
    assert text == "Line 1", f"Line text mismatch: {text}"
    
    # Test create_line_data
    success = editor.create_line_data(1, payload="test", bg_color=QColor(255, 0, 0))
    assert success, "Failed to create line data"
    
    data = editor.get_line_data(1)
    assert data is not None, "Line data not created"
    assert data.payload == "test", "Line data payload mismatch"
    
    print("✓ Line operations work")

def test_multiple_languages():
    """Test multiple language support."""
    editor = CodeEditor()
    
    # Register multiple languages
    languages = ['python', 'javascript', 'java']
    for lang in languages:
        lexer = get_lexer_for_language(lang)
        editor.register_language(lang, lexer)
    
    # Switch between languages
    for lang in languages:
        success = editor.set_language(lang)
        assert success, f"Failed to set {lang}"
        assert editor.get_current_language() == lang, f"Language mismatch for {lang}"
    
    print("✓ Multiple language support works")

def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 50)
    print("Running CodeEditor Tests")
    print("=" * 50 + "\n")
    
    tests = [
        test_basic_creation,
        test_line_data,
        test_language_registration,
        test_read_only_mode,
        test_search,
        test_decorations,
        test_line_operations,
        test_multiple_languages,
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    print("\n" + "=" * 50)
    print("All tests passed! ✓")
    print("=" * 50 + "\n")
    return True

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
