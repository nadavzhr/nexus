"""
Enhanced demo showcasing all new features:
- VS Code-style search popup
- Keyboard shortcuts (comment, duplicate, move lines, go to line)
- Theme switching (light/dark)
- Current line highlighting
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QTextEdit, QSplitter, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from code_editor import CodeEditor
from code_editor.highlighter import get_lexer_for_language

# Sample Python code
SAMPLE_CODE = """# Enhanced Code Editor Demo
from typing import List, Optional

class Calculator:
    \"\"\"A simple calculator class.\"\"\"
    
    def __init__(self):
        self.history: List[str] = []
    
    def add(self, a: float, b: float) -> float:
        \"\"\"Add two numbers.\"\"\"
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a: float, b: float) -> float:
        \"\"\"Subtract b from a.\"\"\"
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a: float, b: float) -> float:
        \"\"\"Multiply two numbers.\"\"\"
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
    
    def divide(self, a: float, b: float) -> Optional[float]:
        \"\"\"Divide a by b.\"\"\"
        if b == 0:
            return None
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result

# Example usage
calc = Calculator()
print(calc.add(10, 5))       # Output: 15
print(calc.multiply(3, 4))   # Output: 12
print(calc.divide(20, 4))    # Output: 5.0
"""


class EnhancedDemoWindow(QMainWindow):
    """Demo window showing enhanced features."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhanced CodeEditor Demo - v0.2.0")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Create splitter
        splitter = QSplitter(Qt.Vertical)
        layout.addWidget(splitter)
        
        # Editor section
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        splitter.addWidget(editor_widget)
        
        # Create editor first (needed by controls)
        self.editor = CodeEditor()
        
        # Create controls (references editor)
        controls = self._create_controls()
        editor_layout.addLayout(controls)
        
        # Add editor to layout
        editor_layout.addWidget(self.editor)
        
        # Output section
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)
        splitter.addWidget(output_widget)
        
        output_layout.addWidget(QLabel("Event Log:"))
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setMaximumHeight(200)
        output_layout.addWidget(self.output)
        
        # Setup editor
        self._setup_editor()
        
        # Status bar
        self.statusBar().showMessage("Ready - Try: Ctrl+F (search), Ctrl+/ (comment), Ctrl+D (duplicate), Alt+Up/Down (move), Ctrl+G (go to line)")
        
        self.log("Enhanced CodeEditor v0.2.0 loaded!")
        self.log("New Features:")
        self.log("  • VS Code-style search (Ctrl+F)")
        self.log("  • Keyboard shortcuts (Ctrl+/, Ctrl+D, Alt+Up/Down, Ctrl+G)")
        self.log("  • Theme switching (light/dark)")
        self.log("  • Current line highlighting")
    
    def _create_controls(self) -> QHBoxLayout:
        """Create control buttons and options."""
        layout = QHBoxLayout()
        
        # Theme selector
        layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["light", "dark"])
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        layout.addWidget(self.theme_combo)
        
        # Current line highlight toggle
        self.current_line_cb = QCheckBox("Highlight Current Line")
        self.current_line_cb.setChecked(True)
        self.current_line_cb.toggled.connect(self.on_current_line_toggled)
        layout.addWidget(self.current_line_cb)
        
        # Shortcut buttons (for demonstration)
        layout.addWidget(QLabel("   Shortcuts:"))
        
        comment_btn = QPushButton("Comment (Ctrl+/)")
        comment_btn.clicked.connect(self.editor.toggle_comment)
        layout.addWidget(comment_btn)
        
        dup_btn = QPushButton("Duplicate (Ctrl+D)")
        dup_btn.clicked.connect(self.editor.duplicate_line)
        layout.addWidget(dup_btn)
        
        search_btn = QPushButton("Search (Ctrl+F)")
        search_btn.clicked.connect(self.editor.show_search_popup)
        layout.addWidget(search_btn)
        
        goto_btn = QPushButton("Go To Line (Ctrl+G)")
        goto_btn.clicked.connect(self.editor.go_to_line)
        layout.addWidget(goto_btn)
        
        layout.addStretch()
        
        return layout
    
    def _setup_editor(self):
        """Setup the editor with Python code."""
        # Register Python
        lexer = get_lexer_for_language('python')
        self.editor.register_language('python', lexer)
        self.editor.set_language('python')
        
        # Set code
        self.editor.setPlainText(SAMPLE_CODE)
        
        # Add metadata to some lines
        self.editor.create_line_data(2, payload={"type": "import"})
        self.editor.create_line_data(4, payload={"type": "class", "name": "Calculator"})
        self.editor.create_line_data(8, payload={"type": "method", "name": "__init__"})
        
        # Connect signals
        self.editor.lineActivated.connect(self.on_line_activated)
        self.editor.cursorMoved.connect(self.on_cursor_moved)
    
    def on_theme_changed(self, theme_name: str):
        """Handle theme change."""
        self.editor.set_theme(theme_name)
        self.log(f"Theme changed to: {theme_name}")
    
    def on_current_line_toggled(self, enabled: bool):
        """Handle current line highlight toggle."""
        self.editor.set_current_line_highlight_enabled(enabled)
        self.log(f"Current line highlighting: {'enabled' if enabled else 'disabled'}")
    
    def on_line_activated(self, line_num: int, data):
        """Handle line activation."""
        self.log(f"Line {line_num + 1} activated with data: {data}")
    
    def on_cursor_moved(self, line_num: int):
        """Handle cursor movement."""
        self.statusBar().showMessage(f"Line {line_num + 1}")
    
    def log(self, message: str):
        """Add message to log."""
        self.output.append(message)


def main():
    """Run the enhanced demo."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = EnhancedDemoWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
