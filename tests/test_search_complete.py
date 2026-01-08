"""Complete test of search functionality."""
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

code = """def calculate():
    result = 0
    return result
"""
editor.setPlainText(code)

print("=" * 70)
print("COMPLETE SEARCH FUNCTIONALITY TEST")
print("=" * 70)

# Test 1: Open search
print("\n✅ Test 1: Search popup opens")
editor.show_search_popup()
popup = editor._search_popup
app.processEvents()
print("   Search popup created ✓")

# Test 2: Alt+C on search input
print("\n✅ Test 2: Alt+C toggles case (from search input)")
initial = popup.case_checkbox.isChecked()
QTest.keyPress(popup.search_input, Qt.Key_C, Qt.AltModifier)
app.processEvents()
assert popup.case_checkbox.isChecked() != initial, "Alt+C should toggle"
print(f"   Case toggled: {initial} -> {popup.case_checkbox.isChecked()} ✓")

# Test 3: Alt+R on search input
print("\n✅ Test 3: Alt+R toggles regex (from search input)")
initial = popup.regex_checkbox.isChecked()
QTest.keyPress(popup.search_input, Qt.Key_R, Qt.AltModifier)
app.processEvents()
assert popup.regex_checkbox.isChecked() != initial, "Alt+R should toggle"
print(f"   Regex toggled: {initial} -> {popup.regex_checkbox.isChecked()} ✓")

# Test 4: Alt+W on search input
print("\n✅ Test 4: Alt+W toggles whole word (from search input)")
initial = popup.whole_word_checkbox.isChecked()
QTest.keyPress(popup.search_input, Qt.Key_W, Qt.AltModifier)
app.processEvents()
assert popup.whole_word_checkbox.isChecked() != initial, "Alt+W should toggle"
print(f"   Whole word toggled: {initial} -> {popup.whole_word_checkbox.isChecked()} ✓")

# Test 5: Live search
print("\n✅ Test 5: Live search (no Enter needed)")
popup.search_input.setText("result")
app.processEvents()
matches = len(editor._search_service.get_matches())
assert matches > 0, "Should find matches"
print(f"   Found {matches} matches automatically ✓")

# Test 6: Enter navigation (shouldn't modify editor)
print("\n✅ Test 6: Enter navigation doesn't modify editor")
original = editor.toPlainText()
QTest.keyPress(popup.search_input, Qt.Key_Return)
app.processEvents()
assert editor.toPlainText() == original, "Editor text unchanged"
print("   Editor text unchanged ✓")

# Test 7: Regex .* safety
print("\n✅ Test 7: Regex .* doesn't crash")
popup.regex_checkbox.setChecked(True)
popup.search_input.setText(".*")
for _ in range(10):
    app.processEvents()
matches = len(editor._search_service.get_matches())
assert matches < 1000, "Should not create excessive matches"
print(f"   Regex .* found {matches} matches (safe) ✓")

print("\n" + "=" * 70)
print("ALL TESTS PASSED! ✅")
print("=" * 70)
print("\nFixed issues:")
print("  1. ✅ Alt+C/R/W shortcuts work from search input")
print("  2. ✅ Live search updates as you type")
print("  3. ✅ Enter navigates without affecting editor")
print("  4. ✅ Regex .* handled safely")

sys.exit(0)
