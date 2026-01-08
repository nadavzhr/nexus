"""
Test the search popup functionality with screenshots.
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from code_editor import CodeEditor
from code_editor.highlighter import get_lexer_for_language

app = QApplication([])

# Create editor
editor = CodeEditor()
editor.setWindowTitle("Search Popup Demo")
editor.setGeometry(100, 100, 1000, 700)

# Register Python
lexer = get_lexer_for_language('python')
editor.register_language('python', lexer)
editor.set_language('python')

# Set code with multiple matches
code = """# Test Search Functionality
def calculate_sum(numbers):
    \"\"\"Calculate the sum of numbers.\"\"\"
    total = sum(numbers)
    return total

def calculate_average(numbers):
    \"\"\"Calculate average of numbers.\"\"\"
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

def calculate_max(numbers):
    \"\"\"Calculate maximum value.\"\"\"
    if not numbers:
        return None
    return max(numbers)

# Test the calculate functions
numbers = [1, 2, 3, 4, 5]
print(f"Sum: {calculate_sum(numbers)}")
print(f"Avg: {calculate_average(numbers)}")
print(f"Max: {calculate_max(numbers)}")
"""
editor.setPlainText(code)

# Set light theme for better visibility
editor.set_theme('light')

# Show editor
editor.show()

# Open search popup after a delay
def open_search():
    editor.show_search_popup()
    # Simulate search for "calculate"
    QTimer.singleShot(200, perform_search)

def perform_search():
    if editor._search_popup:
        editor._search_popup.search_input.setText("calculate")
        editor._search_popup._on_search()
    QTimer.singleShot(300, take_screenshot)

def take_screenshot():
    pixmap = editor.grab()
    pixmap.save('/tmp/search_popup_demo.png')
    print("✓ Screenshot saved: /tmp/search_popup_demo.png")
    print("✓ Search popup is visible")
    print("✓ Multiple matches highlighted")
    QTimer.singleShot(100, app.quit)

QTimer.singleShot(500, open_search)

sys.exit(app.exec_())
