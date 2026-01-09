"""
Go to line overlay widget.

Provides a VS Code-style inline overlay for jumping to a specific line number.
"""

from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPalette, QIntValidator


class GotoLineOverlay(QWidget):
    """
    VS Code-style goto line overlay widget - self-contained and reusable.
    
    A floating overlay that appears at the top-center of the parent widget,
    allowing users to jump to a specific line number with live preview.
    
    The widget is fully self-contained and manages its own:
    - Line number input with validation (integers only, 1-max range)
    - Live feedback showing current/max line numbers
    - Live preview (emits jumpRequested as user types)
    - Keyboard handling (Enter to confirm, Escape to cancel)
    
    Signals:
        jumpRequested(int): Emitted when user types/confirms a valid line number.
            Args: line_number (int, 1-based)
            Note: Emitted during typing for live preview AND on Enter confirmation
        
        closeRequested(): Emitted when user cancels or closes the overlay.
            Triggered by: Escape key, empty input + Enter
    
    Public API Methods:
        - show_overlay(int): Show overlay with specified max line number
        - hide_overlay(): Hide the overlay
    
    Usage Example:
        ```python
        overlay = GotoLineOverlay(parent_widget)
        overlay.jumpRequested.connect(lambda line: print(f"Jump to {line}"))
        overlay.closeRequested.connect(lambda: editor.setFocus())
        overlay.show_overlay(max_line=100)
        ```
    
    The overlay automatically positions itself at the top-center of its parent
    and provides visual feedback as the user types.
    """
    
    jumpRequested = pyqtSignal(int)  # line_number (1-based)
    closeRequested = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize the goto line overlay.
        
        Args:
            parent: Parent widget (the editor)
        """
        super().__init__(parent)
        self._setup_ui()
        self.setWindowFlags(Qt.Widget)
        self.setAutoFillBackground(True)
        self.hide()
    
    def _setup_ui(self) -> None:
        """Setup the UI components."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)
        
        # Label
        label = QLabel("Go to line:")
        layout.addWidget(label)
        
        # Line number input
        self.line_input = QLineEdit()
        self.line_input.setPlaceholderText("Enter line number...")
        self.line_input.setMinimumWidth(150)
        self.line_input.setMaximumWidth(200)
        
        # Only allow positive integers
        validator = QIntValidator(1, 999999, self)
        self.line_input.setValidator(validator)
        
        # Connect signals
        self.line_input.textChanged.connect(self._on_text_changed)
        
        # Install event filter for Enter and Escape
        self.line_input.installEventFilter(self)
        
        layout.addWidget(self.line_input)
        
        self.info_label = QLabel("")
        self.info_label.setMinimumWidth(150)  # Increased from 100 to 150
        layout.addWidget(self.info_label)
    
    def show_overlay(self, max_line: int) -> None:
        """Show the overlay and take focus.
        
        Args:
            max_line: Maximum line number in the document
        """
        self._max_line = max_line
        self.line_input.clear()
        self.info_label.setText(f"(1-{max_line})")
        
        # Position at top-center of parent
        self._position_overlay()
        
        # Show and take focus
        self.show()
        self.raise_()
        self.line_input.setFocus()

    def hide_overlay(self) -> None:
        """Hide the overlay."""
        self.hide()
    
    def _position_overlay(self) -> None:
        """Position the overlay at the top-center of the parent."""
        if not self.parent():
            return
        
        parent = self.parent()
        
        # Get the size hint to know how wide the overlay needs to be
        size_hint = self.sizeHint()
        
        # Calculate top-center position
        # Leave some margin from the top (20px)
        x = (parent.width() - size_hint.width()) // 2
        y = 20
        
        self.move(x, y)
        self.setFixedSize(size_hint)
    
    def _on_text_changed(self, text: str) -> None:
        """Handle text changes in the input - provide live feedback.
        
        Args:
            text: Current text in the input
        """
        if not text:
            self.info_label.setText(f"(1-{self._max_line})")
            return
        
        try:
            line_num = int(text)
            if line_num < 1:
                line_num = 1
            elif line_num > self._max_line:
                line_num = self._max_line
            self.jumpRequested.emit(line_num)  # Live jump signal
            self.info_label.setText(f"✓ Line {line_num}")
                
        except ValueError:
            self.info_label.setText("✗ Invalid")
    
    def _emit_live_jump(self, line_num: int) -> None:
        """Emit a live jump signal to move cursor as user types.
        
        Args:
            line_num: Line number to jump to
        """
        # Notify parent to update cursor position (live preview)
        if self.parent() and hasattr(self.parent(), '_preview_goto_line'):
            self.parent()._preview_goto_line(line_num)
    
    def _on_enter(self) -> None:
        """Handle Enter key press."""
        text = self.line_input.text().strip()
        if not text:
            self.closeRequested.emit()
            return
        
        try:
            line_num = int(text)
            if line_num < 1:
                line_num = 1
            elif line_num > self._max_line:
                line_num = self._max_line
            self.jumpRequested.emit(line_num)
            self.hide()
        except ValueError:
            self.info_label.setText("✗ Invalid number")
    
    def eventFilter(self, obj, event) -> bool:
        """Filter events for child widgets.
        
        Args:
            obj: Object that received the event
            event: Event
            
        Returns:
            True if event was handled, False otherwise
        """
        if obj == self.line_input and event.type() == event.KeyPress:
            # Handle Enter
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                self._on_enter()
                return True  # Consume event so it doesn't propagate to editor
            
            # Handle Escape
            elif event.key() == Qt.Key_Escape:
                self.closeRequested.emit()
                self.hide()
                return True
        
        return super().eventFilter(obj, event)
