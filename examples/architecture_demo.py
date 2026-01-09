"""
Architecture Demo - Showcasing SOLID Principles & Professional Design

This example demonstrates:
1. Model/View separation with EditorConfig
2. Protocol-based service extensibility
3. Qt properties for configuration
4. Rich signal-based API
5. Self-contained, reusable widgets
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from code_editor import (
    CodeEditor, 
    EditorConfig,
    LineData,
    SearchServiceProtocol,
    DecorationServiceProtocol
)
from code_editor.highlighting.highlighter import get_lexer_for_language


class ArchitectureDemo(QMainWindow):
    """Demo showcasing the professional architecture."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Code Editor - Professional Architecture Demo")
        self.setGeometry(100, 100, 1000, 700)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Info label
        info = QLabel(
            "<b>Architecture Demo</b><br>"
            "This demonstrates:<br>"
            "• Model/View separation (EditorConfig)<br>"
            "• Qt properties for settings<br>"
            "• Protocol-based extensibility<br>"
            "• Rich signal API<br>"
            "• Self-contained widgets"
        )
        info.setStyleSheet("padding: 10px; background: #f0f0f0; border-radius: 5px;")
        layout.addWidget(info)
        
        # Create editor with configuration
        config = EditorConfig(
            tab_width=4,
            font_family="Courier New",
            font_size=11,
            hover_enabled=True,
            current_line_highlight_enabled=True,
            theme_name="light"
        )
        
        self.editor = CodeEditor()
        
        # Apply config via Qt properties (idiomatic PyQt5)
        self.editor.hoverEnabled = config.hover_enabled
        self.editor.currentLineHighlightEnabled = config.current_line_highlight_enabled
        
        # Setup language
        python_lexer = get_lexer_for_language('python')
        self.editor.register_language('python', python_lexer)
        self.editor.currentLanguage = 'python'  # Use Qt property!
        
        # Add sample code
        self.editor.setPlainText("""
# Professional Code Editor Widget
# Demonstrates SOLID principles and PyQt5 best practices

class Example:
    '''Example class showcasing syntax highlighting.'''
    
    def __init__(self, name: str):
        self.name = name
    
    def greet(self) -> str:
        '''Return a greeting message.'''
        return f"Hello, {self.name}!"
    
    def process_data(self, data: list) -> dict:
        '''Process and return data statistics.'''
        return {
            'count': len(data),
            'sum': sum(data),
            'average': sum(data) / len(data) if data else 0
        }


# Usage
example = Example("World")
print(example.greet())
""")
        
        # Connect signals (rich API)
        self.editor.cursorMoved.connect(self._on_cursor_moved)
        self.editor.lineActivated.connect(self._on_line_activated)
        
        layout.addWidget(self.editor)
        
        # Status bar showing signals
        self.status = QLabel("Status: Ready")
        layout.addWidget(self.status)
        
        # Control panel
        controls = QHBoxLayout()
        
        # Demonstrate protocol-based service access
        service_btn = QPushButton("Show Service Info")
        service_btn.clicked.connect(self._show_service_info)
        controls.addWidget(service_btn)
        
        # Demonstrate Qt properties
        prop_btn = QPushButton("Toggle Properties")
        prop_btn.clicked.connect(self._toggle_properties)
        controls.addWidget(prop_btn)
        
        # Demonstrate search API
        search_btn = QPushButton("Search 'def' (Ctrl+F)")
        search_btn.clicked.connect(lambda: self.editor.show_search_popup())
        controls.addWidget(search_btn)
        
        # Demonstrate goto API
        goto_btn = QPushButton("Go to Line (Ctrl+G)")
        goto_btn.clicked.connect(lambda: self.editor.go_to_line())
        controls.addWidget(goto_btn)
        
        controls.addStretch()
        layout.addLayout(controls)
    
    def _on_cursor_moved(self, line_number: int):
        """Handle cursor movement signal."""
        self.status.setText(f"Cursor at line {line_number + 1}")
    
    def _on_line_activated(self, line_number: int, data):
        """Handle line activation signal."""
        self.status.setText(f"Line {line_number + 1} activated!")
    
    def _show_service_info(self):
        """Demonstrate service access (SOLID - Dependency Inversion)."""
        # Services follow protocols and can be accessed/replaced
        search_svc = self.editor._search_service
        decor_svc = self.editor._decoration_service
        theme_mgr = self.editor._theme_manager
        
        info = (
            f"<b>Services (Protocol-based):</b><br>"
            f"• SearchService: {type(search_svc).__name__}<br>"
            f"• DecorationService: {type(decor_svc).__name__}<br>"
            f"• ThemeManager: {type(theme_mgr).__name__}<br>"
            f"• Current Theme: {theme_mgr.get_current_theme().name}<br>"
            f"<br><i>All services follow defined protocols and can be replaced!</i>"
        )
        self.status.setText(info.replace('<br>', ' | ').replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', ''))
    
    def _toggle_properties(self):
        """Demonstrate Qt properties (PyQt5 idiomatic)."""
        # Toggle via Qt properties
        current_hover = self.editor.hoverEnabled
        current_highlight = self.editor.currentLineHighlightEnabled
        
        self.editor.hoverEnabled = not current_hover
        self.editor.currentLineHighlightEnabled = not current_highlight
        
        self.status.setText(
            f"Properties toggled! Hover: {self.editor.hoverEnabled}, "
            f"Line highlight: {self.editor.currentLineHighlightEnabled}"
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = ArchitectureDemo()
    demo.show()
    sys.exit(app.exec_())
