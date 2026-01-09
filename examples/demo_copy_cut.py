"""
Demo of smart copy/cut line features.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit
)

from code_editor import CodeEditor
from code_editor.highlighting.highlighter import get_lexer_for_language

SAMPLE_CODE = """# Smart Copy/Cut Demo
def calculate(x, y):
    result = x + y
    return result

# Try:
# - Position cursor on any line (no selection)
# - Press Ctrl+C to copy the line
# - Press Ctrl+X to cut the line
# - Press Ctrl+V to paste

print("Test the shortcuts!")
"""

class CopyCutDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Copy/Cut Line Demo")
        self.setGeometry(100, 100, 900, 600)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Instructions
        instructions = QLabel(
            "<b>Smart Copy/Cut Features:</b><br>"
            "• <b>Ctrl+C</b> with no selection → Copy current line<br>"
            "• <b>Ctrl+X</b> with no selection → Cut current line<br>"
            "• <b>Ctrl+C/X</b> with selection → Normal Qt behavior<br>"
            "• <b>Ctrl+V</b> → Paste (works natively)"
        )
        instructions.setStyleSheet("padding: 10px; background-color: #e8f4f8; border-radius: 5px;")
        layout.addWidget(instructions)
        
        # Editor
        self.editor = CodeEditor()
        layout.addWidget(self.editor)
        
        # Setup
        lexer = get_lexer_for_language('python')
        self.editor.register_language('python', lexer)
        self.editor.set_language('python')
        self.editor.setPlainText(SAMPLE_CODE)
        
        # Output log
        layout.addWidget(QLabel("Clipboard Monitor:"))
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(100)
        layout.addWidget(self.log)
        
        # Monitor clipboard
        app.clipboard().dataChanged.connect(self.on_clipboard_changed)
        
        self.log.append("Ready! Try Ctrl+C and Ctrl+X without selecting text.")
    
    def on_clipboard_changed(self):
        text = app.clipboard().text()
        if text:
            preview = text[:50] + "..." if len(text) > 50 else text
            self.log.append(f"Clipboard: {repr(preview)}")

app = QApplication(sys.argv)
window = CopyCutDemo()
window.show()
sys.exit(app.exec_())
