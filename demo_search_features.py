"""
Demo showing all search popup improvements.
This is a visual demo - run it manually to see the features.
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt

from code_editor import CodeEditor
from code_editor.highlighter import get_lexer_for_language


class SearchDemoWindow(QMainWindow):
    """Demo window for search features."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeEditor - Search Features Demo")
        self.setGeometry(100, 100, 900, 700)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Instructions
        instructions = QLabel(
            "<h2>Search Popup Features Demo</h2>"
            "<p><b>New Features:</b></p>"
            "<ul>"
            "<li><b>Live Search</b> - Search updates as you type (no Enter needed)</li>"
            "<li><b>Focus Handling</b> - Search popup takes focus when opened</li>"
            "<li><b>Enter Navigation</b> - Enter = Next, Shift+Enter = Previous</li>"
            "<li><b>Alt Shortcuts</b> - Alt+C (Case), Alt+R (Regex), Alt+W (Word)</li>"
            "<li><b>Regex Safety</b> - Pattern .* no longer crashes</li>"
            "<li><b>Escape to Close</b> - Esc closes the search popup</li>"
            "</ul>"
            "<p><b>Try it:</b> Press <b>Ctrl+F</b> to open search, then type 'def' or try regex '.*'</p>"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        open_search_btn = QPushButton("Open Search (Ctrl+F)")
        open_search_btn.clicked.connect(self.editor.show_search_popup)
        btn_layout.addWidget(open_search_btn)
        
        test_regex_btn = QPushButton("Test Regex .* (Safe)")
        test_regex_btn.clicked.connect(self.test_regex)
        btn_layout.addWidget(test_regex_btn)
        
        layout.addLayout(btn_layout)
        
        # Editor
        self.editor = CodeEditor()
        layout.addWidget(self.editor)
        
        # Setup editor
        self._setup_editor()
        
        # Status bar
        self.statusBar().showMessage("Ready - Press Ctrl+F to test search features!")
    
    def _setup_editor(self):
        """Setup the editor with sample code."""
        lexer = get_lexer_for_language('python')
        self.editor.register_language('python', lexer)
        self.editor.set_language('python')
        
        code = """# Multi-Language Code Editor
# Search Features Demo

def calculate_sum(numbers):
    \"\"\"Calculate the sum of numbers.\"\"\"
    total = sum(numbers)
    return total

def calculate_average(numbers):
    \"\"\"Calculate the average of numbers.\"\"\"
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
        self.editor.setPlainText(code)
    
    def test_regex(self):
        """Test regex .* pattern (previously crashed)."""
        self.editor.show_search_popup()
        popup = self.editor._search_popup
        popup.regex_checkbox.setChecked(True)
        popup.search_input.setText(".*")
        self.statusBar().showMessage("Regex .* tested - No crash! ✅")


def main():
    """Run the search features demo."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = SearchDemoWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
