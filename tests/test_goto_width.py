"""
Test goto line overlay width fix.

Verifies that "Out of range" text is fully visible.
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from code_editor import CodeEditor
from code_editor.highlighting.highlighter import get_lexer_for_language


def test_goto_overlay_width():
    """Test goto line overlay width."""
    app = QApplication(sys.argv)
    editor = CodeEditor()
    
    # Setup some code
    code = "\n".join([f"line {i}" for i in range(1, 11)])
    editor.setPlainText(code)
    
    # Register language
    lexer = get_lexer_for_language('python')
    editor.register_language('python', lexer)
    editor.set_language('python')
    
    editor.show()
    editor.resize(800, 600)
    
    def run_test():
        print("Testing goto line overlay width...")
        
        # Show goto overlay
        print("\n1. Opening goto line overlay...")
        editor.go_to_line()
        
        QTimer.singleShot(200, test_out_of_range)
    
    def test_out_of_range():
        print("\n2. Testing 'Out of range' message...")
        if editor._goto_line_overlay:
            # Type an out of range number
            editor._goto_line_overlay.line_input.setText("999")
            QTimer.singleShot(200, verify_width)
    
    def verify_width():
        if editor._goto_line_overlay:
            info_text = editor._goto_line_overlay.info_label.text()
            info_width = editor._goto_line_overlay.info_label.width()
            min_width = editor._goto_line_overlay.info_label.minimumWidth()
            
            print(f"   Info label text: '{info_text}'")
            print(f"   Info label width: {info_width}px")
            print(f"   Info label min width: {min_width}px")
            
            if min_width >= 150:
                print(f"   ✓ PASS: Info label wide enough ({min_width}px >= 150px)")
            else:
                print(f"   ✗ FAIL: Info label too narrow ({min_width}px < 150px)")
            
            # Check if text is truncated
            if "..." in info_text or info_text.endswith("ran"):
                print("   ✗ WARNING: Text appears truncated")
            else:
                print("   ✓ Text is not truncated")
        
        print("\n" + "="*60)
        print("Test complete!")
        print("Overlay will remain open for visual verification...")
        print("Close window to exit")
        print("="*60)
    
    # Start test
    QTimer.singleShot(500, run_test)
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    test_goto_overlay_width()
