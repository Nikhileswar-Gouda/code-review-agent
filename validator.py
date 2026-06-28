import ast
import difflib

# Function to validate a proposed fix against the original code, generating a diff and a score.
def validate_fix(original: str, fix: str) -> dict:
    """
    Validates a proposed code fix by checking syntax, comparing lines,
    generating a unified diff, and calculating a score.
    
    Parameters:
        original (str): The original Python code.
        fix (str): The proposed code fix.
        
    Returns:
        dict: A dictionary containing validity status, unified diff, lines changed, and score.
    """
    try:
        # Check syntax using ast.parse
        ast.parse(fix)
        is_valid = True
        has_warnings = False  # Using only ast and difflib as requested
        
        # Count lines in original and fix
        original_lines = original.splitlines()
        fix_lines = fix.splitlines()
        original_line_count = len(original_lines)
        fix_line_count = len(fix_lines)
        
        # Generate unified diff
        diff_lines = list(difflib.unified_diff(
            original_lines,
            fix_lines,
            fromfile='original',
            tofile='fix',
            lineterm=''
        ))
        diff_str = "\n".join(diff_lines)
        
        # Calculate lines_changed as absolute difference in line count
        lines_changed = abs(fix_line_count - original_line_count)
        
        # Score logic
        score = 0.5
        if fix_line_count <= original_line_count:
            score = 0.8
        if len(fix) < len(original) and not has_warnings:
            score = 1.0
            
        return {
            "is_valid": is_valid,
            "diff": diff_str,
            "lines_changed": lines_changed,
            "score": score
        }
        
    except Exception:
        return {
            "is_valid": False,
            "diff": "",
            "lines_changed": 0,
            "score": 0.0
        }
