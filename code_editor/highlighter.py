"""
Syntax highlighting implementation using Pygments.

This module wraps Pygments lexers in a QSyntaxHighlighter for use with Qt.
"""

from typing import Optional
from PyQt5.QtGui import QSyntaxHighlighter, QTextDocument, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import Qt

try:
    from pygments import lex
    from pygments.lexers import get_lexer_by_name, PythonLexer
    from pygments.token import Token
    from pygments.style import Style
    from pygments.styles import get_style_by_name
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False


class PygmentsHighlighter(QSyntaxHighlighter):
    """
    Syntax highlighter that uses Pygments lexers.
    
    This class bridges Pygments syntax highlighting with Qt's QSyntaxHighlighter.
    It supports any Pygments lexer and provides reasonable default styling.
    """
    
    def __init__(self, document: Optional[QTextDocument] = None, 
                 lexer=None, style_name: str = 'default'):
        """
        Initialize the highlighter.
        
        Args:
            document: The QTextDocument to highlight
            lexer: Pygments lexer instance or None
            style_name: Name of Pygments style to use
        """
        super().__init__(document)
        
        if not PYGMENTS_AVAILABLE:
            raise ImportError("Pygments is required for syntax highlighting")
        
        self._lexer = lexer or PythonLexer()
        self._style = get_style_by_name(style_name) if PYGMENTS_AVAILABLE else None
        self._format_cache = {}
        self._build_format_cache()
    
    def set_lexer(self, lexer) -> None:
        """
        Change the lexer and re-highlight the document.
        
        Args:
            lexer: New Pygments lexer instance
        """
        self._lexer = lexer
        self.rehighlight()
    
    def set_style(self, style_name: str) -> None:
        """
        Change the highlighting style.
        
        Args:
            style_name: Name of Pygments style
        """
        self._style = get_style_by_name(style_name)
        self._format_cache.clear()
        self._build_format_cache()
        self.rehighlight()
    
    def _build_format_cache(self) -> None:
        """Pre-build format cache for common token types."""
        if not self._style:
            return
        
        # Build formats for common token types
        for token_type in [Token.Keyword, Token.Name, Token.Comment, 
                          Token.String, Token.Number, Token.Operator,
                          Token.Name.Function, Token.Name.Class]:
            self._get_format_for_token(token_type)
    
    def _get_format_for_token(self, token_type) -> QTextCharFormat:
        """
        Get or create a QTextCharFormat for a token type.
        
        Args:
            token_type: Pygments token type
            
        Returns:
            QTextCharFormat for the token
        """
        if token_type in self._format_cache:
            return self._format_cache[token_type]
        
        fmt = QTextCharFormat()
        
        if self._style:
            # Get style for this token type
            style_dict = self._style.style_for_token(token_type)
            
            if style_dict.get('color'):
                color = QColor(f"#{style_dict['color']}")
                fmt.setForeground(color)
            
            if style_dict.get('bold'):
                fmt.setFontWeight(QFont.Bold)
            
            if style_dict.get('italic'):
                fmt.setFontItalic(True)
            
            if style_dict.get('underline'):
                fmt.setFontUnderline(True)
        else:
            # Default fallback colors
            fmt = self._get_default_format(token_type)
        
        self._format_cache[token_type] = fmt
        return fmt
    
    def _get_default_format(self, token_type) -> QTextCharFormat:
        """
        Get a default format for token types when no style is available.
        
        Args:
            token_type: Pygments token type
            
        Returns:
            QTextCharFormat with default colors
        """
        fmt = QTextCharFormat()
        
        # Map token types to default colors
        if token_type in Token.Keyword:
            fmt.setForeground(QColor(0, 0, 255))  # Blue
            fmt.setFontWeight(QFont.Bold)
        elif token_type in Token.Comment:
            fmt.setForeground(QColor(0, 128, 0))  # Green
            fmt.setFontItalic(True)
        elif token_type in Token.String:
            fmt.setForeground(QColor(163, 21, 21))  # Dark red
        elif token_type in Token.Number:
            fmt.setForeground(QColor(176, 96, 0))  # Orange
        elif token_type in Token.Name.Function:
            fmt.setForeground(QColor(0, 128, 128))  # Teal
        elif token_type in Token.Name.Class:
            fmt.setForeground(QColor(0, 0, 255))  # Blue
            fmt.setFontWeight(QFont.Bold)
        elif token_type in Token.Operator:
            fmt.setForeground(QColor(128, 128, 128))  # Gray
        
        return fmt
    
    def highlightBlock(self, text: str) -> None:
        """
        Highlight a single block (line) of text.
        
        This is called by Qt whenever a block needs to be highlighted.
        
        Args:
            text: The text of the block to highlight
        """
        if not text or not self._lexer:
            return
        
        # Use Pygments to tokenize the text
        try:
            tokens = lex(text, self._lexer)
            
            offset = 0
            for token_type, value in tokens:
                length = len(value)
                if length > 0:
                    fmt = self._get_format_for_token(token_type)
                    self.setFormat(offset, length, fmt)
                    offset += length
        except Exception:
            # If highlighting fails, just skip it
            pass


def get_lexer_for_language(language: str):
    """
    Get a Pygments lexer for a given language name.
    
    Args:
        language: Language name (e.g., 'python', 'javascript', 'java')
        
    Returns:
        Pygments lexer instance
        
    Raises:
        ImportError: If Pygments is not available
        ValueError: If language is not recognized
    """
    if not PYGMENTS_AVAILABLE:
        raise ImportError("Pygments is required for syntax highlighting")
    
    try:
        return get_lexer_by_name(language)
    except Exception as e:
        raise ValueError(f"Unknown language: {language}") from e
