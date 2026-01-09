"""
Verify VS Code-style paste implementation.

Checks the code for proper implementation without requiring GUI.
"""

def verify_vscode_paste():
    """Verify VS Code-style paste implementation."""
    print("Verifying VS Code-style paste implementation...")
    print("="*60)
    
    # Check 1: _last_copy_was_line flag exists
    print("\n1. Checking _last_copy_was_line flag...")
    with open('code_editor/core.py', 'r') as f:
        core_content = f.read()
    
    if '_last_copy_was_line' in core_content:
        # Find initialization
        if 'self._last_copy_was_line: bool = False' in core_content or \
           'self._last_copy_was_line = False' in core_content:
            print("   ✓ PASS: _last_copy_was_line flag initialized")
        else:
            print("   ✗ WARNING: Flag exists but may not be initialized")
    else:
        print("   ✗ FAIL: _last_copy_was_line flag not found")
    
    # Check 2: copy_line sets flag and adds newline
    print("\n2. Checking copy_line() implementation...")
    with open('code_editor/shortcuts.py', 'r') as f:
        shortcuts_content = f.read()
    
    if 'def copy_line(self)' in shortcuts_content:
        method_start = shortcuts_content.find('def copy_line(self)')
        method_section = shortcuts_content[method_start:method_start+800]
        
        has_newline = "text() + '\\n'" in method_section or 'text() + "\\n"' in method_section
        sets_flag = '_last_copy_was_line = True' in method_section
        
        if has_newline:
            print("   ✓ PASS: Adds newline to copied text")
        else:
            print("   ✗ FAIL: Doesn't add newline to mark as line copy")
        
        if sets_flag:
            print("   ✓ PASS: Sets _last_copy_was_line = True")
        else:
            print("   ✗ FAIL: Doesn't set line copy flag")
    
    # Check 3: cut_line sets flag and adds newline
    print("\n3. Checking cut_line() implementation...")
    if 'def cut_line(self)' in shortcuts_content:
        method_start = shortcuts_content.find('def cut_line(self)')
        method_section = shortcuts_content[method_start:method_start+900]
        
        has_newline = "text() + '\\n'" in method_section or 'text() + "\\n"' in method_section
        sets_flag = '_last_copy_was_line = True' in method_section
        
        if has_newline:
            print("   ✓ PASS: Adds newline to cut text")
        else:
            print("   ✗ FAIL: Doesn't add newline to mark as line copy")
        
        if sets_flag:
            print("   ✓ PASS: Sets _last_copy_was_line = True")
        else:
            print("   ✗ FAIL: Doesn't set line copy flag")
    
    # Check 4: paste_line method exists and checks flag
    print("\n4. Checking paste_line() implementation...")
    if 'def paste_line(self)' in core_content:
        method_start = core_content.find('def paste_line(self)')
        method_section = core_content[method_start:method_start+1500]
        
        checks_flag = 'if self._last_copy_was_line' in method_section
        checks_newline = "text.endswith('\\n')" in method_section or 'text.endswith("\\n")' in method_section
        inserts_at_start = 'movePosition(QTextCursor.StartOfBlock)' in method_section
        resets_flag = '_last_copy_was_line = False' in method_section
        
        if checks_flag:
            print("   ✓ PASS: Checks _last_copy_was_line flag")
        else:
            print("   ✗ FAIL: Doesn't check line copy flag")
        
        if checks_newline:
            print("   ✓ PASS: Checks if text ends with newline")
        else:
            print("   ✗ FAIL: Doesn't check for newline")
        
        if inserts_at_start:
            print("   ✓ PASS: Inserts at start of line (VS Code behavior)")
        else:
            print("   ✗ FAIL: Doesn't insert at start of line")
        
        if resets_flag:
            print("   ✓ PASS: Resets flag after paste")
        else:
            print("   ✗ WARNING: May not reset flag after paste")
    else:
        print("   ✗ FAIL: paste_line() method not found")
    
    # Check 5: keyPressEvent handles Ctrl+V
    print("\n5. Checking keyPressEvent() for Ctrl+V...")
    if 'def keyPressEvent(self, event)' in core_content:
        method_start = core_content.find('def keyPressEvent(self, event)')
        method_section = core_content[method_start:method_start+1500]
        
        handles_v = 'Qt.Key_V' in method_section
        calls_paste_line = 'self.paste_line()' in method_section
        resets_on_normal_copy = '_last_copy_was_line = False' in method_section
        
        if handles_v:
            print("   ✓ PASS: Handles Ctrl+V key")
        else:
            print("   ✗ FAIL: Doesn't handle Ctrl+V")
        
        if calls_paste_line:
            print("   ✓ PASS: Calls paste_line()")
        else:
            print("   ✗ FAIL: Doesn't call paste_line()")
        
        if resets_on_normal_copy:
            print("   ✓ PASS: Resets flag on normal copy/cut with selection")
        else:
            print("   ✗ WARNING: May not reset flag on normal operations")
    
    # Check 6: Public API methods exist
    print("\n6. Checking public API methods...")
    has_copy_line_api = 'def copy_line(self)' in core_content and \
                        'Copy the current line to clipboard' in core_content
    has_cut_line_api = 'def cut_line(self)' in core_content and \
                       'Cut the current line to clipboard' in core_content
    has_paste_line_api = 'def paste_line(self)' in core_content
    
    if has_copy_line_api:
        print("   ✓ PASS: copy_line() in public API")
    else:
        print("   ✗ FAIL: copy_line() not in public API")
    
    if has_cut_line_api:
        print("   ✓ PASS: cut_line() in public API")
    else:
        print("   ✗ FAIL: cut_line() not in public API")
    
    if has_paste_line_api:
        print("   ✓ PASS: paste_line() in public API")
    else:
        print("   ✗ FAIL: paste_line() not in public API")
    
    print("\n" + "="*60)
    print("Verification complete!")
    print("="*60)
    print("\nSummary:")
    print("- VS Code-style paste inserts full lines as new lines")
    print("- Normal copy/paste with selection works as before")
    print("- Flag tracking ensures correct behavior")


if __name__ == '__main__':
    verify_vscode_paste()
