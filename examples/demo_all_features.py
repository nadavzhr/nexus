"""
Comprehensive demo of all CodeEditor features.

This demo showcases:
1. Search popup with Alt shortcuts (fixed)
2. Goto line overlay (new)
3. All keyboard shortcuts
4. Themes
5. Current line highlighting
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QSplitter
)
from PyQt5.QtCore import Qt

from code_editor import CodeEditor
from code_editor.highlighter import get_lexer_for_language


class AllFeaturesDemo(QMainWindow):
    """Demo window for all features."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeEditor - All Features Demo")
        self.setGeometry(100, 100, 1000, 700)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Instructions
        instructions = QLabel(
            "<h2>CodeEditor - Complete Feature Demo</h2>"
            "<p><b>Keyboard Shortcuts:</b></p>"
            "<ul>"
            "<li><b>Ctrl+F</b> - Open search popup (live search, Alt+C/R/W for toggles)</li>"
            "<li><b>Ctrl+G</b> - Open goto line overlay (live preview as you type)</li>"
            "<li><b>Ctrl+/</b> - Comment/uncomment line</li>"
            "<li><b>Ctrl+D</b> - Duplicate line</li>"
            "<li><b>Ctrl+C/X</b> - Smart copy/cut (copies line if no selection)</li>"
            "<li><b>Alt+Up/Down</b> - Move line up/down</li>"
            "</ul>"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Controls
        controls = QHBoxLayout()
        
        # Theme selector
        controls.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['light', 'dark'])
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        controls.addWidget(self.theme_combo)
        
        controls.addStretch()
        
        # Action buttons
        search_btn = QPushButton("Search (Ctrl+F)")
        search_btn.clicked.connect(lambda: self.editor.show_search_popup())
        controls.addWidget(search_btn)
        
        goto_btn = QPushButton("Go to Line (Ctrl+G)")
        goto_btn.clicked.connect(lambda: self.editor.go_to_line())
        controls.addWidget(goto_btn)
        
        layout.addLayout(controls)
        
        # Editor
        self.editor = CodeEditor()
        layout.addWidget(self.editor)
        
        # Setup editor
        self._setup_editor()
        
        # Status bar
        self.statusBar().showMessage("Ready - Try Ctrl+F for search or Ctrl+G for goto line!")
    
    def _setup_editor(self):
        """Setup the editor with sample code."""
        lexer = get_lexer_for_language('python')
        self.editor.register_language('python', lexer)
        self.editor.set_language('python')
        
        code = """# Multi-Language Code Editor - Feature Demo
# This demo showcases all the new features

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

def calculate_min(numbers):
    \"\"\"Calculate minimum value.\"\"\"
    if not numbers:
        return None
    return min(numbers)

# Test the calculate functions
numbers = [1, 2, 3, 4, 5]
print(f"Sum: {calculate_sum(numbers)}")
print(f"Avg: {calculate_average(numbers)}")
print(f"Max: {calculate_max(numbers)}")
print(f"Min: {calculate_min(numbers)}")

# Try these features:
# 1. Press Ctrl+F and search for "calculate"
#    - Use Alt+C for case sensitivity
#    - Use Alt+R for regex mode
#    - Use Alt+W for whole word
#
# 2. Press Ctrl+G and type "15"
#    - Watch the cursor move LIVE as you type!
#    - Press Enter to confirm or Escape to cancel
#
# 3. Press Ctrl+/ to comment/uncomment a line
#
# 4. Press Alt+Up or Alt+Down to move lines
#
# 5. Press Ctrl+D to duplicate a line
"""
        self.editor.setPlainText(code)
    
    def change_theme(self, theme_name):
        """Change the editor theme."""
        self.editor.set_theme(theme_name)
        self.statusBar().showMessage(f"Theme changed to: {theme_name}")


def main():
    """Run the complete features demo."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = AllFeaturesDemo()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
