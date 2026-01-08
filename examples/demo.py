"""
Demo application for the CodeEditor widget.

This demo showcases:
- Basic editor usage
- Syntax highlighting with multiple languages
- Line data and metadata
- Read-only mode with line activation
- Search functionality
- Custom decorations
- Custom language registration
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QTextEdit, QSplitter
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from code_editor import CodeEditor, LineData
from code_editor.highlighter import get_lexer_for_language

# Sample code for different languages
SAMPLE_PYTHON = """def hello_world():
    \"\"\"Print a greeting message.\"\"\"
    name = "World"
    message = f"Hello, {name}!"
    print(message)
    return True

# Call the function
if __name__ == "__main__":
    result = hello_world()
"""

SAMPLE_JAVASCRIPT = """function helloWorld() {
    // Print a greeting message
    const name = "World";
    const message = `Hello, ${name}!`;
    console.log(message);
    return true;
}

// Call the function
const result = helloWorld();
"""

SAMPLE_JAVA = """public class HelloWorld {
    /**
     * Main entry point
     */
    public static void main(String[] args) {
        String name = "World";
        String message = "Hello, " + name + "!";
        System.out.println(message);
    }
}
"""

SAMPLE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hello World</title>
    <style>
        body { font-family: Arial, sans-serif; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <h1>Hello, World!</h1>
    <script>
        console.log('Page loaded');
    </script>
</body>
</html>
"""


class DemoWindow(QMainWindow):
    """Main demo window showcasing CodeEditor features."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeEditor Demo - Multi-Language Editor Widget")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Create splitter for editor and output
        splitter = QSplitter(Qt.Vertical)
        layout.addWidget(splitter)
        
        # Editor section
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        splitter.addWidget(editor_widget)
        
        # Controls
        controls_layout = QHBoxLayout()
        editor_layout.addLayout(controls_layout)
        
        # Language selector
        controls_layout.addWidget(QLabel("Language:"))
        self.language_combo = QComboBox()
        self.language_combo.addItems(["python", "javascript", "java", "html"])
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        controls_layout.addWidget(self.language_combo)
        
        # Mode toggle
        self.mode_button = QPushButton("Switch to Read-Only")
        self.mode_button.clicked.connect(self.toggle_mode)
        controls_layout.addWidget(self.mode_button)
        
        # Search controls
        controls_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term...")
        self.search_input.returnPressed.connect(self.perform_search)
        controls_layout.addWidget(self.search_input)
        
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.perform_search)
        controls_layout.addWidget(search_btn)
        
        clear_search_btn = QPushButton("Clear Search")
        clear_search_btn.clicked.connect(self.clear_search)
        controls_layout.addWidget(clear_search_btn)
        
        controls_layout.addStretch()
        
        # Decoration controls
        decoration_layout = QHBoxLayout()
        editor_layout.addLayout(decoration_layout)
        
        add_decoration_btn = QPushButton("Highlight Line 3")
        add_decoration_btn.clicked.connect(self.add_line_decoration)
        decoration_layout.addWidget(add_decoration_btn)
        
        clear_decoration_btn = QPushButton("Clear Decorations")
        clear_decoration_btn.clicked.connect(self.clear_decorations)
        decoration_layout.addWidget(clear_decoration_btn)
        
        add_data_btn = QPushButton("Add Line Data")
        add_data_btn.clicked.connect(self.add_line_data)
        decoration_layout.addWidget(add_data_btn)
        
        decoration_layout.addStretch()
        
        # Code editor
        self.editor = CodeEditor()
        editor_layout.addWidget(self.editor)
        
        # Connect editor signals
        self.editor.lineActivated.connect(self.on_line_activated)
        self.editor.cursorMoved.connect(self.on_cursor_moved)
        
        # Output area
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)
        splitter.addWidget(output_widget)
        
        output_layout.addWidget(QLabel("Output / Event Log:"))
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setMaximumHeight(200)
        output_layout.addWidget(self.output)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        # Initialize with Python code
        self.samples = {
            "python": SAMPLE_PYTHON,
            "javascript": SAMPLE_JAVASCRIPT,
            "java": SAMPLE_JAVA,
            "html": SAMPLE_HTML
        }
        
        # Register languages and set initial code
        self.setup_languages()
        self.load_sample("python")
        
        self.log("CodeEditor initialized with Python syntax highlighting")
        self.log("Try switching languages, searching, or toggling read-only mode")
    
    def setup_languages(self):
        """Register all supported languages."""
        try:
            # Register built-in languages
            for lang in ["python", "javascript", "java", "html"]:
                lexer = get_lexer_for_language(lang)
                self.editor.register_language(lang, lexer, [f".{lang}"])
            
            self.log("Registered languages: python, javascript, java, html")
        except Exception as e:
            self.log(f"Error registering languages: {e}")
    
    def load_sample(self, language: str):
        """Load sample code for a language."""
        if language in self.samples:
            self.editor.setPlainText(self.samples[language])
            if self.editor.set_language(language):
                self.log(f"Loaded {language} sample with syntax highlighting")
            else:
                self.log(f"Loaded {language} sample (highlighting failed)")
    
    def on_language_changed(self, language: str):
        """Handle language selection change."""
        self.load_sample(language)
    
    def toggle_mode(self):
        """Toggle between editable and read-only modes."""
        if self.editor.isReadOnly():
            self.editor.setReadOnly(False)
            self.mode_button.setText("Switch to Read-Only")
            self.log("Switched to EDITABLE mode")
        else:
            self.editor.setReadOnly(True)
            self.mode_button.setText("Switch to Editable")
            self.log("Switched to READ-ONLY mode (try double-clicking lines with data)")
    
    def perform_search(self):
        """Perform a search in the editor."""
        pattern = self.search_input.text()
        if pattern:
            count = self.editor.search(pattern)
            self.log(f"Search for '{pattern}': found {count} matches")
            self.statusBar().showMessage(f"Found {count} matches")
        else:
            self.log("No search pattern entered")
    
    def clear_search(self):
        """Clear search results."""
        self.editor.clear_search()
        self.search_input.clear()
        self.log("Search results cleared")
        self.statusBar().showMessage("Search cleared")
    
    def add_line_decoration(self):
        """Add a custom decoration to line 3."""
        color = QColor(255, 200, 200)  # Light pink
        self.editor.add_decoration(2, color, 'custom')  # Line 3 (0-indexed)
        self.log("Added pink background decoration to line 3")
    
    def clear_decorations(self):
        """Clear all custom decorations."""
        self.editor.clear_decorations('custom')
        self.log("Cleared custom decorations")
    
    def add_line_data(self):
        """Add metadata to specific lines."""
        # Add data to lines 1, 3, and 5
        self.editor.create_line_data(0, {"type": "function", "name": "hello_world"})
        self.editor.create_line_data(2, {"type": "comment", "importance": "high"})
        self.editor.create_line_data(4, {"type": "variable", "name": "message"})
        
        self.log("Added metadata to lines 1, 3, and 5")
        self.log("Switch to read-only mode and double-click these lines to see the data")
    
    def on_line_activated(self, line_number: int, data):
        """Handle line activation (double-click in read-only mode)."""
        line_text = self.editor.get_line_text(line_number)
        self.log(f"Line {line_number + 1} activated:")
        self.log(f"  Text: {line_text}")
        self.log(f"  Data: {data}")
    
    def on_cursor_moved(self, line_number: int):
        """Handle cursor position changes."""
        self.statusBar().showMessage(f"Line {line_number + 1}")
    
    def log(self, message: str):
        """Add a message to the output log."""
        self.output.append(message)


def main():
    """Run the demo application."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = DemoWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
