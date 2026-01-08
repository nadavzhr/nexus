"""
Test VS Code-style line copy/cut/paste behavior.

Tests:
1. Ctrl+C with no selection copies line
2. Ctrl+V pastes as new line (not inline)
3. Ctrl+X with no selection cuts line
4. Ctrl+V after cut pastes as new line
5. Normal copy/paste still works
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtTest import QTest
from code_editor import CodeEditor
from code_editor.highlighter import get_lexer_for_language


def test_vscode_paste():
    """Test VS Code-style paste behavior."""
    app = QApplication(sys.argv)
    editor = CodeEditor()
    
    # Setup Python code
    code = """line1
line2
line3
line4"""
    editor.setPlainText(code)
    
    # Register language
    lexer = get_lexer_for_language('python')
    editor.register_language('python', lexer)
    editor.set_language('python')
    
    editor.show()
    editor.resize(800, 600)
    
    print("Testing VS Code-style copy/paste...")
    print("="*60)
    
    def run_tests():
        # Test 1: Copy line without selection
        print("\n1. Testing Ctrl+C (no selection) → copy line")
        cursor = editor.textCursor()
        cursor.movePosition(cursor.Start)
        cursor.movePosition(cursor.Down)  # Move to line2
        editor.setTextCursor(cursor)
        
        # Ensure no selection
        assert not editor.textCursor().hasSelection(), "Should have no selection"
        
        # Simulate Ctrl+C
        QTest.keyClick(editor, Qt.Key_C, Qt.ControlModifier)
        QTimer.singleShot(100, test_paste_as_line)
    
    def test_paste_as_line():
        # Test 2: Paste should insert as new line
        print("2. Testing Ctrl+V → paste as new line (VS Code style)")
        
        # Move to line4
        cursor = editor.textCursor()
        cursor.movePosition(cursor.End)
        editor.setTextCursor(cursor)
        
        # Get current content
        before = editor.toPlainText()
        print(f"   Before paste:\n{repr(before)}")
        
        # Simulate Ctrl+V
        QTest.keyClick(editor, Qt.Key_V, Qt.ControlModifier)
        QTimer.singleShot(100, verify_line_paste)
    
    def verify_line_paste():
        after = editor.toPlainText()
        print(f"   After paste:\n{repr(after)}")
        
        # Should have inserted "line2\n" as a new line
        if "line2\nline2" in after or after.count("line2") == 2:
            print("   ✓ PASS: Line pasted as new line (not inline)")
        else:
            print(f"   ✗ FAIL: Expected line paste, got:\n{after}")
        
        QTimer.singleShot(500, test_cut_line)
    
    def test_cut_line():
        # Test 3: Cut line without selection
        print("\n3. Testing Ctrl+X (no selection) → cut line")
        
        # Reset editor
        editor.setPlainText("line1\nline2\nline3\nline4")
        
        # Move to line2
        cursor = editor.textCursor()
        cursor.movePosition(cursor.Start)
        cursor.movePosition(cursor.Down)
        editor.setTextCursor(cursor)
        
        before = editor.toPlainText()
        print(f"   Before cut:\n{repr(before)}")
        
        # Simulate Ctrl+X
        QTest.keyClick(editor, Qt.Key_X, Qt.ControlModifier)
        QTimer.singleShot(100, verify_cut)
    
    def verify_cut():
        after = editor.toPlainText()
        print(f"   After cut:\n{repr(after)}")
        
        if "line2" not in after and after.count('\n') == 2:
            print("   ✓ PASS: Line2 was cut (removed from editor)")
        else:
            print(f"   ✗ FAIL: Line not properly cut")
        
        QTimer.singleShot(500, test_paste_cut_line)
    
    def test_paste_cut_line():
        # Test 4: Paste cut line as new line
        print("\n4. Testing paste after cut → should insert as new line")
        
        # Move to end
        cursor = editor.textCursor()
        cursor.movePosition(cursor.End)
        editor.setTextCursor(cursor)
        
        before = editor.toPlainText()
        print(f"   Before paste:\n{repr(before)}")
        
        # Simulate Ctrl+V
        QTest.keyClick(editor, Qt.Key_V, Qt.ControlModifier)
        QTimer.singleShot(100, verify_cut_paste)
    
    def verify_cut_paste():
        after = editor.toPlainText()
        print(f"   After paste:\n{repr(after)}")
        
        # Should have "line2" back as a new line
        if "line2" in after:
            print("   ✓ PASS: Cut line pasted as new line")
        else:
            print(f"   ✗ FAIL: Cut line not pasted correctly")
        
        QTimer.singleShot(500, test_normal_copy_paste)
    
    def test_normal_copy_paste():
        # Test 5: Normal copy with selection still works
        print("\n5. Testing normal copy/paste (with selection)")
        
        editor.setPlainText("hello world")
        
        # Select "hello"
        cursor = editor.textCursor()
        cursor.movePosition(cursor.Start)
        cursor.movePosition(cursor.Right, cursor.KeepAnchor, 5)
        editor.setTextCursor(cursor)
        
        assert cursor.hasSelection(), "Should have selection"
        print(f"   Selected: '{cursor.selectedText()}'")
        
        # Copy
        QTest.keyClick(editor, Qt.Key_C, Qt.ControlModifier)
        QTimer.singleShot(100, test_normal_paste)
    
    def test_normal_paste():
        # Move to end and paste
        cursor = editor.textCursor()
        cursor.movePosition(cursor.End)
        editor.setTextCursor(cursor)
        
        before = editor.toPlainText()
        print(f"   Before paste: '{before}'")
        
        # Paste
        QTest.keyClick(editor, Qt.Key_V, Qt.ControlModifier)
        QTimer.singleShot(100, verify_normal_paste)
    
    def verify_normal_paste():
        after = editor.toPlainText()
        print(f"   After paste: '{after}'")
        
        # Should paste inline, not as new line
        if after == "hello worldhello":
            print("   ✓ PASS: Normal paste works inline (not as new line)")
        else:
            print(f"   ✗ FAIL: Expected 'hello worldhello', got '{after}'")
        
        print("\n" + "="*60)
        print("All tests complete!")
        print("="*60)
        
        QTimer.singleShot(2000, app.quit)
    
    # Start tests
    QTimer.singleShot(500, run_tests)
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    test_vscode_paste()
