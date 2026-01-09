"""
Comprehensive example showing all CodeEditor features.

This example demonstrates:
1. Multi-language support (switching between languages)
2. Line metadata and activation
3. Search and highlighting
4. Decorations
5. Read-only mode interaction
"""

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor
from code_editor import CodeEditor, LineData
from code_editor.highlighting.highlighter import get_lexer_for_language

# Initialize QApplication
app = QApplication([])

# Create editor
editor = CodeEditor()
editor.setWindowTitle("CodeEditor - Feature Demonstration")
editor.setGeometry(100, 100, 800, 600)

# Register multiple languages
print("Registering languages...")
for lang in ['python', 'javascript', 'java', 'html', 'css']:
    try:
        lexer = get_lexer_for_language(lang)
        editor.register_language(lang, lexer)
        print(f"  ✓ Registered {lang}")
    except:
        print(f"  ✗ Failed to register {lang}")

# Set Python as default
editor.set_language('python')
print(f"Current language: {editor.get_current_language()}")

# Set sample code
code = """def fibonacci(n):
    \"\"\"Calculate Fibonacci number.\"\"\"
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Test the function
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
"""
editor.setPlainText(code)

# Add line metadata
print("\nAdding line metadata...")
editor.create_line_data(0, payload={"type": "function", "name": "fibonacci", "complexity": "O(2^n)"})
editor.create_line_data(7, payload={"type": "loop", "iterations": 10})
print("  ✓ Added metadata to lines 1 and 8")

# Add decorations
print("\nAdding decorations...")
editor.add_decoration(0, QColor(255, 255, 200), 'custom')  # Yellow for function
editor.add_decoration(7, QColor(200, 255, 200), 'custom')  # Green for loop
print("  ✓ Added decorations")

# Perform search
print("\nPerforming search...")
matches = editor.search("fibonacci")
print(f"  ✓ Found {matches} matches for 'fibonacci'")

# Get editor stats
print(f"\nEditor Statistics:")
print(f"  Lines: {editor.line_count()}")
print(f"  Language: {editor.get_current_language()}")
print(f"  Read-only: {editor.isReadOnly()}")

# Test line operations
print(f"\nLine Operations:")
for i in range(min(3, editor.line_count())):
    text = editor.get_line_text(i)
    data = editor.get_line_data(i)
    print(f"  Line {i+1}: {text[:50]}...")
    if data:
        print(f"    Metadata: {data.payload}")

# Connect signals
def on_line_activated(line_num, data):
    print(f"\n[Signal] Line {line_num + 1} activated with data: {data}")

def on_cursor_moved(line_num):
    print(f"[Signal] Cursor moved to line {line_num + 1}", end='\r')

editor.lineActivated.connect(on_line_activated)
editor.cursorMoved.connect(on_cursor_moved)

print("\n" + "="*60)
print("Editor ready! All features demonstrated successfully.")
print("="*60)
print("\nFeatures available:")
print("  ✓ Multi-language syntax highlighting")
print("  ✓ Line numbering")
print("  ✓ Line metadata storage")
print("  ✓ Search with highlighting")
print("  ✓ Custom decorations")
print("  ✓ Read-only/editable modes")
print("  ✓ Signal emissions (lineActivated, cursorMoved)")
print("\nSwitch to read-only mode and double-click lines to see activation!")

# Show editor
editor.show()

# Don't run event loop in test mode
if __name__ == '__main__':
    print("\n[Press Ctrl+C to exit]")
    try:
        app.exec_()
    except KeyboardInterrupt:
        print("\nExiting...")
