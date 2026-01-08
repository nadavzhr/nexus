"""
Keyboard shortcuts and editor actions for the code editor.

This module provides actions that can be triggered via keyboard shortcuts
or programmatically via the public API.
"""

from typing import Optional
from PyQt5.QtGui import QTextCursor, QKeySequence
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton


class GoToLineDialog(QDialog):
    """Dialog for jumping to a specific line number."""
    
    def __init__(self, max_line: int, current_line: int, parent=None):
        """
        Initialize the go to line dialog.
        
        Args:
            max_line: Maximum line number
            current_line: Current line number (1-based)
            parent: Parent widget
        """
        super().__init__(parent)
        self.setWindowTitle("Go to Line")
        self.setModal(True)
        self._line_number = current_line
        
        layout = QVBoxLayout(self)
        
        # Input row
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Line number:"))
        
        self.line_input = QLineEdit()
        self.line_input.setText(str(current_line))
        self.line_input.selectAll()
        self.line_input.returnPressed.connect(self.accept)
        input_layout.addWidget(self.line_input)
        
        layout.addLayout(input_layout)
        
        # Info label
        self.info_label = QLabel(f"(1 - {max_line})")
        layout.addWidget(self.info_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_btn = QPushButton("Go")
        ok_btn.clicked.connect(self.accept)
        ok_btn.setDefault(True)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setFixedSize(300, 120)
    
    def get_line_number(self) -> Optional[int]:
        """Get the entered line number (1-based) or None if invalid."""
        try:
            return int(self.line_input.text())
        except ValueError:
            return None


class EditorActions:
    """
    Collection of editor actions that can be triggered by shortcuts or API.
    
    This class provides the implementation for common code editor actions
    like comment/uncomment, duplicate line, move line, etc.
    """
    
    def __init__(self, editor):
        """
        Initialize editor actions.
        
        Args:
            editor: The CodeEditor instance
        """
        self.editor = editor
    
    def toggle_comment(self) -> None:
        """
        Toggle comment on the current line or selection.
        
        For Python, uses # as comment character.
        For other languages, tries to detect appropriate comment style.
        """
        cursor = self.editor.textCursor()
        
        # Get comment character based on language
        comment_char = self._get_comment_char()
        
        if cursor.hasSelection():
            # Comment/uncomment selected lines
            start = cursor.selectionStart()
            end = cursor.selectionEnd()
            
            # Get line numbers
            cursor.setPosition(start)
            start_line = cursor.blockNumber()
            cursor.setPosition(end)
            end_line = cursor.blockNumber()
            
            # Check if all lines are commented
            all_commented = True
            for line_num in range(start_line, end_line + 1):
                block = self.editor.document().findBlockByNumber(line_num)
                text = block.text().lstrip()
                if not text.startswith(comment_char):
                    all_commented = False
                    break
            
            # Toggle comments
            cursor.beginEditBlock()
            for line_num in range(start_line, end_line + 1):
                block = self.editor.document().findBlockByNumber(line_num)
                cursor.setPosition(block.position())
                text = block.text()
                
                if all_commented:
                    # Remove comment
                    stripped = text.lstrip()
                    if stripped.startswith(comment_char):
                        # Find position of comment char
                        indent = len(text) - len(stripped)
                        cursor.setPosition(block.position() + indent)
                        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor,
                                          len(comment_char) + (1 if stripped[len(comment_char):].startswith(' ') else 0))
                        cursor.removeSelectedText()
                else:
                    # Add comment
                    stripped = text.lstrip()
                    indent = len(text) - len(stripped)
                    cursor.setPosition(block.position() + indent)
                    cursor.insertText(comment_char + " ")
            
            cursor.endEditBlock()
        else:
            # Comment/uncomment current line
            block = cursor.block()
            text = block.text()
            stripped = text.lstrip()
            
            cursor.beginEditBlock()
            if stripped.startswith(comment_char):
                # Remove comment
                indent = len(text) - len(stripped)
                cursor.setPosition(block.position() + indent)
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor,
                                  len(comment_char) + (1 if stripped[len(comment_char):].startswith(' ') else 0))
                cursor.removeSelectedText()
            else:
                # Add comment
                indent = len(text) - len(stripped)
                cursor.setPosition(block.position() + indent)
                cursor.insertText(comment_char + " ")
            cursor.endEditBlock()
    
    def duplicate_line(self) -> None:
        """Duplicate the current line or selection."""
        cursor = self.editor.textCursor()
        
        if cursor.hasSelection():
            # Duplicate selection
            text = cursor.selectedText()
            # Replace paragraph separator with newline
            text = text.replace('\u2029', '\n')
            end = cursor.selectionEnd()
            cursor.setPosition(end)
            cursor.insertText('\n' + text)
        else:
            # Duplicate current line
            block = cursor.block()
            text = block.text()
            cursor.movePosition(QTextCursor.EndOfBlock)
            cursor.insertText('\n' + text)
    
    def move_line_up(self) -> None:
        """Move the current line up."""
        cursor = self.editor.textCursor()
        
        # Don't move if at first line
        if cursor.blockNumber() == 0:
            return
        
        cursor.beginEditBlock()
        
        # Get current line
        current_block = cursor.block()
        current_text = current_block.text()
        current_pos = cursor.positionInBlock()
        
        # Delete current line
        cursor.select(QTextCursor.LineUnderCursor)
        cursor.removeSelectedText()
        cursor.deletePreviousChar()  # Delete the newline
        
        # Move to previous line
        cursor.movePosition(QTextCursor.Up)
        cursor.movePosition(QTextCursor.StartOfBlock)
        
        # Insert the line
        cursor.insertText(current_text + '\n')
        
        # Restore cursor position
        cursor.movePosition(QTextCursor.Up)
        cursor.movePosition(QTextCursor.StartOfBlock)
        # Bound cursor position to line length
        line_length = cursor.block().length() - 1  # -1 for newline
        safe_pos = min(current_pos, line_length)
        cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, safe_pos)
        
        cursor.endEditBlock()
        self.editor.setTextCursor(cursor)
    
    def move_line_down(self) -> None:
        """Move the current line down."""
        cursor = self.editor.textCursor()
        
        # Don't move if at last line
        if cursor.blockNumber() == self.editor.document().blockCount() - 1:
            return
        
        cursor.beginEditBlock()
        
        # Get current line
        current_block = cursor.block()
        current_text = current_block.text()
        current_pos = cursor.positionInBlock()
        
        # Delete current line
        cursor.select(QTextCursor.LineUnderCursor)
        cursor.removeSelectedText()
        if cursor.blockNumber() < self.editor.document().blockCount() - 1:
            cursor.deleteChar()  # Delete the newline
        
        # Move to next line
        cursor.movePosition(QTextCursor.Down)
        cursor.movePosition(QTextCursor.EndOfBlock)
        
        # Insert the line
        cursor.insertText('\n' + current_text)
        
        # Restore cursor position
        cursor.movePosition(QTextCursor.StartOfBlock)
        # Bound cursor position to line length
        line_length = cursor.block().length() - 1  # -1 for newline
        safe_pos = min(current_pos, line_length)
        cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, safe_pos)
        
        cursor.endEditBlock()
        self.editor.setTextCursor(cursor)
    
    def go_to_line(self) -> None:
        """Show dialog and jump to a specific line."""
        cursor = self.editor.textCursor()
        current_line = cursor.blockNumber() + 1
        max_line = self.editor.document().blockCount()
        
        dialog = GoToLineDialog(max_line, current_line, self.editor)
        if dialog.exec_():
            line_num = dialog.get_line_number()
            if line_num and 1 <= line_num <= max_line:
                self.jump_to_line(line_num)
    
    def jump_to_line(self, line_number: int) -> None:
        """
        Jump to a specific line number.
        
        Args:
            line_number: Line number (1-based)
        """
        # Convert to 0-based
        line_num = line_number - 1
        
        if 0 <= line_num < self.editor.document().blockCount():
            block = self.editor.document().findBlockByNumber(line_num)
            cursor = QTextCursor(block)
            cursor.movePosition(QTextCursor.EndOfBlock)
            self.editor.setTextCursor(cursor)
            self.editor.centerCursor()
    
    def _get_comment_char(self) -> str:
        """
        Get the comment character for the current language.
        
        Returns:
            Comment character string
        """
        # Map languages to comment characters
        comment_map = {
            'python': '#',
            'ruby': '#',
            'bash': '#',
            'shell': '#',
            'perl': '#',
            'yaml': '#',
            'javascript': '//',
            'java': '//',
            'c': '//',
            'cpp': '//',
            'c++': '//',
            'csharp': '//',
            'go': '//',
            'rust': '//',
            'swift': '//',
            'kotlin': '//',
            'typescript': '//',
            'php': '//',
            'sql': '--',
            'lua': '--',
            'html': '<!--',
            'xml': '<!--',
        }
        
        current_lang = self.editor.get_current_language()
        return comment_map.get(current_lang, '#')
    
    def copy_line(self) -> None:
        """
        Copy the current line to clipboard if no selection.
        
        If there's a selection, this does nothing (Qt's native Ctrl+C handles it).
        """
        cursor = self.editor.textCursor()
        
        # Only copy line if there's no selection
        if not cursor.hasSelection():
            # Get current line text
            block = cursor.block()
            text = block.text()
            
            # Copy to clipboard
            from PyQt5.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
    
    def cut_line(self) -> None:
        """
        Cut the current line to clipboard if no selection.
        
        If there's a selection, this does nothing (Qt's native Ctrl+X handles it).
        """
        cursor = self.editor.textCursor()
        
        # Only cut line if there's no selection
        if not cursor.hasSelection():
            # Get current line text
            block = cursor.block()
            text = block.text()
            
            # Copy to clipboard
            from PyQt5.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            
            # Delete the line
            cursor.select(QTextCursor.LineUnderCursor)
            cursor.removeSelectedText()
            cursor.deleteChar()  # Delete the newline
