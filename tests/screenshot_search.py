"""Generate screenshot of search popup with features."""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from code_editor import CodeEditor
from code_editor.highlighter import get_lexer_for_language

app = QApplication(sys.argv)

# Create editor
editor = CodeEditor()
editor.setGeometry(100, 100, 800, 600)
editor.setWindowTitle("CodeEditor - Search Features")

# Setup Python syntax highlighting
lexer = get_lexer_for_language('python')
editor.register_language('python', lexer)
editor.set_language('python')

# Add sample code
code = """# Search Features Demo

def calculate_sum(numbers):
    total = sum(numbers)
    return total

def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

# Test
numbers = [1, 2, 3, 4, 5]
print(f"Sum: {calculate_sum(numbers)}")
"""

editor.setPlainText(code)
editor.show()

# Open search popup and set it up
def setup_search():
    editor.show_search_popup()
    popup = editor._search_popup
    popup.search_input.setText("calculate")
    
    # Take screenshot after a moment
    QTimer.singleShot(500, take_screenshot)

def take_screenshot():
    pixmap = editor.grab()
    pixmap.save('/tmp/search_popup_features.png')
    print("Screenshot saved to /tmp/search_popup_features.png")
    QTimer.singleShot(100, app.quit)

# Setup search after window is shown
QTimer.singleShot(100, setup_search)

sys.exit(app.exec_())
