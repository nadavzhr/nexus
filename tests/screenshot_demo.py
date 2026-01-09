"""
Simple screenshot script to demonstrate the CodeEditor widget.
Creates a minimal window with the editor and saves a screenshot.
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from code_editor import CodeEditor
from code_editor.highlighting.highlighter import get_lexer_for_language

# Sample Python code to display
SAMPLE_CODE = """# Multi-Language Code Editor Widget
from typing import Optional, List

class HelloWorld:
    \"\"\"A simple hello world class.\"\"\"
    
    def __init__(self, name: str = "World"):
        self.name = name
        self.greeting = "Hello"
    
    def greet(self) -> str:
        \"\"\"Generate a greeting message.\"\"\"
        return f"{self.greeting}, {self.name}!"
    
    def greet_all(self, names: List[str]) -> None:
        \"\"\"Greet multiple people.\"\"\"
        for name in names:
            print(f"{self.greeting}, {name}!")

# Example usage
if __name__ == "__main__":
    greeter = HelloWorld("Python Developer")
    message = greeter.greet()
    print(message)
    
    # Greet multiple people
    greeter.greet_all(["Alice", "Bob", "Charlie"])
"""

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Create main window
    window = QMainWindow()
    window.setWindowTitle("CodeEditor Widget - Python Syntax Highlighting Demo")
    window.setGeometry(100, 100, 900, 700)
    
    # Create central widget
    central = QWidget()
    window.setCentralWidget(central)
    layout = QVBoxLayout(central)
    
    # Create editor
    editor = CodeEditor()
    layout.addWidget(editor)
    
    # Register and set Python language
    python_lexer = get_lexer_for_language('python')
    editor.register_language('python', python_lexer)
    editor.set_language('python')
    
    # Set the sample code
    editor.setPlainText(SAMPLE_CODE)
    
    # Add some line decorations to demonstrate the feature
    from PyQt5.QtGui import QColor
    editor.add_decoration(0, QColor(255, 255, 200), 'custom')  # Highlight first line
    editor.add_decoration(15, QColor(200, 255, 200), 'custom')  # Highlight if __name__
    
    # Add line metadata to some lines
    editor.create_line_data(2, payload={"type": "class_definition", "name": "HelloWorld"})
    editor.create_line_data(6, payload={"type": "method", "name": "__init__"})
    editor.create_line_data(10, payload={"type": "method", "name": "greet"})
    
    window.show()
    
    # Take screenshot after a short delay
    def take_screenshot():
        pixmap = window.grab()
        pixmap.save('/tmp/code_editor_screenshot.png')
        print("Screenshot saved to /tmp/code_editor_screenshot.png")
        QTimer.singleShot(100, app.quit)
    
    QTimer.singleShot(500, take_screenshot)
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
