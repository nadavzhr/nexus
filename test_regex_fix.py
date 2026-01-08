"""Test regex .* crash fix"""
import sys
from PyQt5.QtWidgets import QApplication
from code_editor import CodeEditor
from code_editor.highlighter import get_lexer_for_language

app = QApplication([])
editor = CodeEditor()
lexer = get_lexer_for_language('python')
editor.register_language('python', lexer)
editor.set_language('python')

# Set test code
code = """def hello():
    print("Hello")
    return True
"""
editor.setPlainText(code)

# Test regex .* - this used to crash
print("Testing regex .* pattern...")
editor.show_search_popup()
popup = editor._search_popup
popup.regex_checkbox.setChecked(True)
popup.search_input.setText(".*")

for _ in range(20):
    app.processEvents()

matches = len(editor._search_service.get_matches())
print(f"Found {matches} matches")
print("✅ No crash!")

sys.exit(0)
