"""Test Alt shortcuts in search popup."""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

from code_editor import CodeEditor
from code_editor.highlighter import get_lexer_for_language

app = QApplication([])

editor = CodeEditor()
lexer = get_lexer_for_language('python')
editor.register_language('python', lexer)
editor.set_language('python')
editor.setPlainText("def test():\n    pass")

print("Testing Alt shortcuts in search popup...")
print("=" * 60)

# Open search popup
editor.show_search_popup()
popup = editor._search_popup
app.processEvents()

print(f"Search popup visible: {popup.isVisible()}")
print(f"Search popup has focus: {popup.hasFocus()}")
print(f"Search input has focus: {popup.search_input.hasFocus()}")

# Test Alt+C
print("\n1. Testing Alt+C (Case sensitivity)...")
initial_case = popup.case_checkbox.isChecked()
print(f"   Initial case: {initial_case}")

# Try sending Alt+C to the popup
QTest.keyPress(popup, Qt.Key_C, Qt.AltModifier)
app.processEvents()
after_case = popup.case_checkbox.isChecked()
print(f"   After Alt+C: {after_case}")
print(f"   Changed: {initial_case != after_case}")

# Test Alt+R
print("\n2. Testing Alt+R (Regex)...")
initial_regex = popup.regex_checkbox.isChecked()
print(f"   Initial regex: {initial_regex}")

QTest.keyPress(popup, Qt.Key_R, Qt.AltModifier)
app.processEvents()
after_regex = popup.regex_checkbox.isChecked()
print(f"   After Alt+R: {after_regex}")
print(f"   Changed: {initial_regex != after_regex}")

# Test Alt+W
print("\n3. Testing Alt+W (Whole word)...")
initial_word = popup.whole_word_checkbox.isChecked()
print(f"   Initial word: {initial_word}")

QTest.keyPress(popup, Qt.Key_W, Qt.AltModifier)
app.processEvents()
after_word = popup.whole_word_checkbox.isChecked()
print(f"   After Alt+W: {after_word}")
print(f"   Changed: {initial_word != after_word}")

print("\n" + "=" * 60)

# Now test sending to search_input specifically
print("\nTesting Alt shortcuts on search_input widget...")
popup.search_input.setFocus()
app.processEvents()

print("\n4. Testing Alt+C on search_input...")
initial_case2 = popup.case_checkbox.isChecked()
QTest.keyPress(popup.search_input, Qt.Key_C, Qt.AltModifier)
app.processEvents()
after_case2 = popup.case_checkbox.isChecked()
print(f"   Changed: {initial_case2 != after_case2}")

sys.exit(0)
