"""
Test search highlighting fixes.

Tests:
1. Highlights cleared when search popup closed
2. "No results" shown in red when no matches
3. Highlights cleared when query changes to no matches
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from code_editor import CodeEditor
from code_editor.highlighting.highlighter import get_lexer_for_language


def test_search_highlighting_fixes():
    """Test all search highlighting fixes."""
    app = QApplication(sys.argv)
    editor = CodeEditor()
    
    # Setup Python code
    code = """def hello():
    print("Hello, World!")
    return True

# Call function
hello()
"""
    editor.setPlainText(code)
    
    # Register language
    lexer = get_lexer_for_language('python')
    editor.register_language('python', lexer)
    editor.set_language('python')
    
    editor.show()
    editor.resize(800, 600)
    
    def run_tests():
        print("Testing search highlighting fixes...")
        
        # Test 1: Search for "hello"
        print("\n1. Searching for 'hello'...")
        editor.show_search_popup()
        QTimer.singleShot(100, lambda: test_search_results())
    
    def test_search_results():
        # Type search query
        if editor._search_popup:
            editor._search_popup.search_input.setText("hello")
            QTimer.singleShot(100, lambda: verify_highlights())
    
    def verify_highlights():
        print("   ✓ Search highlights should be visible")
        search_decorations = editor._decorations.get('search', [])
        current_decorations = editor._decorations.get('current_match', [])
        print(f"   Found {len(search_decorations)} search highlights")
        print(f"   Found {len(current_decorations)} current match highlight")
        
        # Test 2: Close popup and verify highlights are cleared
        QTimer.singleShot(500, lambda: test_close_popup())
    
    def test_close_popup():
        print("\n2. Closing search popup...")
        if editor._search_popup:
            editor._search_popup.closeRequested.emit()
            QTimer.singleShot(100, lambda: verify_cleared())
    
    def verify_cleared():
        search_decorations = editor._decorations.get('search', [])
        current_decorations = editor._decorations.get('current_match', [])
        if len(search_decorations) == 0 and len(current_decorations) == 0:
            print("   ✓ PASS: Highlights cleared after closing popup")
        else:
            print(f"   ✗ FAIL: Highlights still present ({len(search_decorations)} search, {len(current_decorations)} current)")
        
        # Test 3: Search for non-existent pattern
        QTimer.singleShot(500, lambda: test_no_results())
    
    def test_no_results():
        print("\n3. Searching for 'zzzzzzz' (no matches)...")
        editor.show_search_popup()
        QTimer.singleShot(100, lambda: type_no_match())
    
    def type_no_match():
        if editor._search_popup:
            editor._search_popup.search_input.setText("zzzzzzz")
            QTimer.singleShot(100, lambda: verify_no_results())
    
    def verify_no_results():
        if editor._search_popup:
            label_text = editor._search_popup.match_label.text()
            label_style = editor._search_popup.match_label.styleSheet()
            
            if label_text == "No results" and "cc0000" in label_style:
                print(f"   ✓ PASS: Shows '{label_text}' in red")
            else:
                print(f"   ✗ FAIL: Expected 'No results' in red, got '{label_text}' with style '{label_style}'")
        
        search_decorations = editor._decorations.get('search', [])
        if len(search_decorations) == 0:
            print("   ✓ PASS: No highlights for empty results")
        else:
            print(f"   ✗ FAIL: Found {len(search_decorations)} highlights for query with no matches")
        
        # Test 4: Change query from matches to no matches
        QTimer.singleShot(500, lambda: test_query_change())
    
    def test_query_change():
        print("\n4. Changing query from 'hello' to 'zzzzz'...")
        if editor._search_popup:
            editor._search_popup.search_input.setText("hello")
            QTimer.singleShot(200, lambda: change_to_no_match())
    
    def change_to_no_match():
        if editor._search_popup:
            # Should have highlights now
            search_decorations = editor._decorations.get('search', [])
            print(f"   Search 'hello': {len(search_decorations)} highlights")
            
            # Change to no-match query
            editor._search_popup.search_input.setText("zzzzz")
            QTimer.singleShot(200, lambda: verify_cleared_on_change())
    
    def verify_cleared_on_change():
        search_decorations = editor._decorations.get('search', [])
        if len(search_decorations) == 0:
            print("   ✓ PASS: Previous highlights cleared when query changes to no matches")
        else:
            print(f"   ✗ FAIL: Still have {len(search_decorations)} highlights from previous query")
        
        print("\n" + "="*60)
        print("All tests complete!")
        print("="*60)
        
        # Close after all tests
        QTimer.singleShot(2000, app.quit)
    
    # Start tests after a short delay
    QTimer.singleShot(500, run_tests)
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    test_search_highlighting_fixes()
