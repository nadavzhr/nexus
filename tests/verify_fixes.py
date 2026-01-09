"""
Simple verification of the search highlighting fixes.

This script verifies the code changes without requiring GUI.
"""

def verify_search_fixes():
    """Verify search highlighting fix implementation."""
    print("Verifying search highlighting fixes...")
    print("="*60)
    
    # Check 1: _on_search_closed clears highlights
    print("\n1. Checking _on_search_closed() implementation...")
    with open('code_editor/core.py', 'r') as f:
        content = f.read()
        
    # Find the _on_search_closed method
    if 'def _on_search_closed(self)' in content:
        method_start = content.find('def _on_search_closed(self)')
        method_section = content[method_start:method_start+500]
        
        has_clear_search = "clear_decorations('search')" in method_section
        has_clear_current = "clear_decorations('current_match')" in method_section
        has_apply = "_apply_decorations()" in method_section
        
        if has_clear_search and has_clear_current and has_apply:
            print("   ✓ PASS: Clears 'search' decorations")
            print("   ✓ PASS: Clears 'current_match' decorations")
            print("   ✓ PASS: Applies decorations (refreshes display)")
        else:
            print(f"   ✗ FAIL: Missing clear calls")
            print(f"      - clear_search: {has_clear_search}")
            print(f"      - clear_current: {has_clear_current}")
            print(f"      - apply: {has_apply}")
    
    # Check 2: _on_search_requested clears highlights at start
    print("\n2. Checking _on_search_requested() implementation...")
    if 'def _on_search_requested(self, pattern: str' in content:
        method_start = content.find('def _on_search_requested(self, pattern: str')
        method_section = content[method_start:method_start+1500]
        
        # Find position of first clear_decorations call
        first_clear = method_section.find("clear_decorations('search')")
        # Find position of search service call
        search_call = method_section.find("self._search_service.search(")
        
        if first_clear < search_call and first_clear > 0:
            print("   ✓ PASS: Clears decorations BEFORE searching")
        else:
            print("   ✗ FAIL: Decorations not cleared early enough")
        
        # Check for empty pattern handling
        if "if not pattern:" in method_section:
            print("   ✓ PASS: Handles empty pattern")
        else:
            print("   ✗ WARNING: May not handle empty pattern")
    
    # Check 3: update_match_count shows "No results"
    print("\n3. Checking update_match_count() in SearchPopup...")
    with open('code_editor/search.py', 'r') as f:
        search_content = f.read()
    
    if 'def update_match_count(self, current: int, total: int)' in search_content:
        method_start = search_content.find('def update_match_count(self, current: int, total: int)')
        method_section = search_content[method_start:method_start+800]
        
        has_no_results = '"No results"' in method_section or "'No results'" in method_section
        has_red_color = '#cc0000' in method_section or 'cc0000' in method_section
        
        if has_no_results and has_red_color:
            print("   ✓ PASS: Shows 'No results' text")
            print("   ✓ PASS: Uses red color (#cc0000)")
        else:
            print(f"   ✗ FAIL: Missing proper 'No results' display")
            print(f"      - 'No results' text: {has_no_results}")
            print(f"      - Red color: {has_red_color}")
    
    # Check 4: Goto line overlay width
    print("\n4. Checking GotoLineOverlay info_label width...")
    with open('code_editor/goto_line_overlay.py', 'r') as f:
        goto_content = f.read()
    
    if 'self.info_label.setMinimumWidth(' in goto_content:
        # Extract the width value
        width_start = goto_content.find('self.info_label.setMinimumWidth(')
        width_section = goto_content[width_start:width_start+100]
        
        # Look for the number
        import re
        match = re.search(r'setMinimumWidth\((\d+)\)', width_section)
        if match:
            width = int(match.group(1))
            if width >= 150:
                print(f"   ✓ PASS: Info label width set to {width}px (>= 150px)")
            else:
                print(f"   ✗ FAIL: Info label width only {width}px (should be >= 150px)")
        else:
            print("   ✗ FAIL: Could not parse width value")
    else:
        print("   ✗ FAIL: Info label minimum width not set")
    
    print("\n" + "="*60)
    print("Verification complete!")
    print("="*60)


if __name__ == '__main__':
    verify_search_fixes()
