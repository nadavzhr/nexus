"""
Test the new copy/cut line features.
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

from code_editor import CodeEditor
from code_editor.highlighting.highlighter import get_lexer_for_language

app = QApplication([])

print("Testing Copy/Cut Line Features")
print("=" * 60)

# Create editor
editor = CodeEditor()
lexer = get_lexer_for_language('python')
editor.register_language('python', lexer)
editor.set_language('python')

# Set test code
code = """line one
line two
line three
"""
editor.setPlainText(code)

# Test 1: Copy line without selection
print("\n1. Testing copy_line() without selection...")
cursor = editor.textCursor()
cursor.movePosition(cursor.Start)
editor.setTextCursor(cursor)
editor.copy_line()

clipboard = app.clipboard()
copied = clipboard.text()
assert copied == "line one", f"Expected 'line one', got '{copied}'"
print("   ✅ Copy line works")

# Test 2: Copy with selection (should use native)
print("\n2. Testing native copy with selection...")
cursor = editor.textCursor()
cursor.movePosition(cursor.Start)
cursor.movePosition(cursor.Right, cursor.KeepAnchor, 4)  # Select "line"
editor.setTextCursor(cursor)
editor.copy()  # Native Qt copy
copied = clipboard.text()
assert copied == "line", f"Expected 'line', got '{copied}'"
print("   ✅ Native copy with selection works")

# Test 3: Cut line without selection
print("\n3. Testing cut_line() without selection...")
cursor = editor.textCursor()
cursor.movePosition(cursor.Start)
editor.setTextCursor(cursor)
editor.cut_line()

copied = clipboard.text()
assert copied == "line one", f"Expected 'line one', got '{copied}'"

# Check line was deleted
remaining = editor.toPlainText()
assert "line one" not in remaining, "Line should be deleted"
assert "line two" in remaining, "Other lines should remain"
print("   ✅ Cut line works")

# Test 4: Public API methods exist
print("\n4. Testing public API...")
assert hasattr(editor, 'copy_line')
assert hasattr(editor, 'cut_line')
print("   ✅ Public API methods available")

print("\n" + "=" * 60)
print("ALL COPY/CUT TESTS PASSED! ✅")
print("=" * 60)

sys.exit(0)
