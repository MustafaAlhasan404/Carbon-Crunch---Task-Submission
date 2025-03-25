import re
import os
import ast

def analyze_python(file_path):
    """
    Analyze a Python file for code quality.
    
    Args:
        file_path (str): Path to the Python file
        
    Returns:
        dict: Analysis results with scores and recommendations
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Initialize scores for each category
    naming_score = 0
    modularity_score = 0
    comments_score = 0
    formatting_score = 0
    reusability_score = 0
    best_practices_score = 0
    
    # Initialize recommendations
    recommendations = []
    
    # Split content into lines for analysis
    lines = content.split('\n')
    
    # Parse the AST for better analysis
    try:
        tree = ast.parse(content)
        parsed_successfully = True
    except SyntaxError:
        parsed_successfully = False
        recommendations.append("Fix syntax errors in the code")
    
    # Analyze naming conventions (10 points)
    naming_score, naming_recs = analyze_naming_conventions(content, lines, tree if parsed_successfully else None)
    recommendations.extend(naming_recs)
    
    # Analyze function length and modularity (20 points)
    modularity_score, modularity_recs = analyze_modularity(content, lines, tree if parsed_successfully else None)
    recommendations.extend(modularity_recs)
    
    # Analyze comments and documentation (20 points)
    comments_score, comments_recs = analyze_comments(content, lines)
    recommendations.extend(comments_recs)
    
    # Analyze formatting/indentation (15 points)
    formatting_score, formatting_recs = analyze_formatting(content, lines)
    recommendations.extend(formatting_recs)
    
    # Analyze reusability and DRY (15 points)
    reusability_score, reusability_recs = analyze_reusability(content, lines, tree if parsed_successfully else None)
    recommendations.extend(reusability_recs)
    
    # Analyze best practices in web dev (20 points)
    best_practices_score, best_practices_recs = analyze_best_practices(content, lines)
    recommendations.extend(best_practices_recs)
    
    # Calculate overall score (out of 100)
    overall_score = (
        naming_score + 
        modularity_score + 
        comments_score + 
        formatting_score + 
        reusability_score + 
        best_practices_score
    )
    
    # Limit to top 5 recommendations
    recommendations = recommendations[:5]
    
    # Prepare result in required JSON format
    result = {
        "overall_score": overall_score,
        "breakdown": {
            "naming": naming_score,
            "modularity": modularity_score,
            "comments": comments_score,
            "formatting": formatting_score,
            "reusability": reusability_score,
            "best_practices": best_practices_score
        },
        "recommendations": recommendations
    }
    
    return result

def analyze_naming_conventions(content, lines, tree):
    """Analyze naming conventions in Python code."""
    score = 10  # Start with full score and deduct based on issues
    recommendations = []
    
    # Check for snake_case variables and functions (PEP8)
    camel_case_vars = re.findall(r'([a-z]+[A-Z][a-zA-Z0-9]*)\s*=', content)
    pascal_case_vars = re.findall(r'([A-Z][a-z]+[A-Za-z0-9]*)\s*=', content)
    
    # Check function names
    camel_case_funcs = re.findall(r'def\s+([a-z]+[A-Z][a-zA-Z0-9]*)\s*\(', content)
    pascal_case_funcs = re.findall(r'def\s+([A-Z][a-z]+[a-zA-Z0-9]*)\s*\(', content)
    
    non_snake_case = camel_case_vars + pascal_case_vars + camel_case_funcs + pascal_case_funcs
    
    if non_snake_case:
        score -= min(5, len(non_snake_case))
        recommendations.append(f"Use snake_case for variable and function names (found: {', '.join(non_snake_case[:3])})")
    
    # Check for UPPERCASE constants
    non_upper_constants = []
    constants_pattern = r'([a-z][A-Za-z0-9_]*)\s*=\s*(?:True|False|None|[\'"]{1,3}[^\'"]*[\'"]{1,3}|\d+)'
    
    for match in re.finditer(constants_pattern, content):
        var_name = match.group(1)
        # Look for constant declaration at module level
        if re.search(fr'^{var_name}\s*=', content, re.MULTILINE) and not var_name.isupper():
            non_upper_constants.append(var_name)
    
    if non_upper_constants:
        score -= min(3, len(non_upper_constants))
        recommendations.append("Use UPPERCASE for constant values")
    
    # Check class names (should be PascalCase)
    non_pascal_classes = re.findall(r'class\s+([a-z][a-zA-Z0-9_]*)\s*[:\(]', content)
    
    if non_pascal_classes:
        score -= min(2, len(non_pascal_classes))
        recommendations.append("Use PascalCase for class names")
    
    return max(0, score), recommendations

def analyze_modularity(content, lines, tree):
    """Analyze function length and modularity."""
    score = 20  # Start with full score
    recommendations = []
    
    # Check for function length
    function_blocks = re.findall(r'def\s+[a-zA-Z0-9_]+\s*\([^)]*\)(?:\s*->.*?)?\s*:\s*((?:\n\s+.*)+)', content)
    
    long_functions = []
    for func in function_blocks:
        func_lines = func.count('\n') + 1
        if func_lines > 30:
            long_functions.append(func_lines)
    
    if long_functions:
        deduction = min(10, len(long_functions) * 3)
        score -= deduction
        recommendations.append(f"Break down functions that are too long (found {len(long_functions)} functions over 30 lines)")
    
    # Check for too many arguments
    many_args_funcs = re.findall(r'def\s+([a-zA-Z0-9_]+)\s*\(([^)]{40,})\)', content)
    
    if many_args_funcs:
        score -= min(5, len(many_args_funcs))
        recommendations.append("Reduce the number of arguments in functions")
    
    # Check for deeply nested conditions/loops
    indentation_levels = []
    for line in lines:
        if line.strip() and not line.strip().startswith('#'):
            indent = len(line) - len(line.lstrip())
            indentation_levels.append(indent)
    
    if indentation_levels:
        # Check for deep nesting (more than 4 levels / 16 spaces)
        max_indent = max(indentation_levels) if indentation_levels else 0
        if max_indent > 16:
            score -= 5
            recommendations.append("Reduce nesting depth in conditions and loops")
    
    # Check for large file size
    if len(lines) > 300:
        score -= 5
        recommendations.append("Consider splitting this large file into multiple modules")
    
    return max(0, score), recommendations

def analyze_comments(content, lines):
    """Analyze comments and documentation."""
    score = 20  # Start with full score
    recommendations = []
    
    # Count comments
    single_line_comments = len(re.findall(r'^\s*#.*$', content, re.MULTILINE))
    
    # Check for docstrings
    docstrings = re.findall(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'', content)
    
    # Count functions and classes
    functions = re.findall(r'def\s+[a-zA-Z0-9_]+\s*\(', content)
    classes = re.findall(r'class\s+[a-zA-Z0-9_]+', content)
    
    # Check if each function/class has a docstring
    if functions and len(docstrings) < len(functions) + len(classes):
        score -= min(10, (len(functions) + len(classes) - len(docstrings)) * 2)
        recommendations.append("Add docstrings to document functions and classes")
    
    # Check code-to-comment ratio
    code_to_comment_ratio = len(lines) / max(1, single_line_comments + len(docstrings))
    
    if code_to_comment_ratio > 15:
        score -= 5
        recommendations.append(f"Add more comments to explain complex logic (current ratio: 1 comment per ~{code_to_comment_ratio:.1f} lines)")
    
    # Check for commented-out code
    commented_code = re.findall(r'^\s*#\s*(def|class|if|for|while|return|import)', content, re.MULTILINE)
    if commented_code:
        score -= min(5, len(commented_code))
        recommendations.append("Remove commented-out code that is no longer needed")
    
    # Check for module-level docstring
    if not content.lstrip().startswith('"""') and not content.lstrip().startswith("'''"):
        score -= 3
        recommendations.append("Add a module-level docstring at the beginning of the file")
    
    return max(0, score), recommendations

def analyze_formatting(content, lines):
    """Analyze code formatting and indentation."""
    score = 15  # Start with full score
    recommendations = []
    
    # Check consistent indentation
    indent_levels = []
    for line in lines:
        if line.strip() and not line.strip().startswith('#'):
            indent = len(line) - len(line.lstrip())
            if indent > 0:
                indent_levels.append(indent)
    
    if indent_levels:
        # Check if indentation is consistently divisible by 4 (PEP8)
        indent_divisible_by_4 = all(level % 4 == 0 for level in indent_levels)
        
        if not indent_divisible_by_4:
            score -= 5
            recommendations.append("Use consistent indentation (4 spaces per PEP8)")
    
    # Check line length (should be <= 79 characters as per PEP8)
    long_lines = [i for i, line in enumerate(lines, 1) if len(line) > 100]
    if long_lines:
        score -= min(5, len(long_lines))
        recommendations.append(f"Break down long lines that exceed 100 characters (found on lines: {', '.join(str(x) for x in long_lines[:3])})")
    
    # Check for trailing whitespace
    trailing_whitespace = sum(1 for line in lines if line.rstrip() != line)
    if trailing_whitespace > 5:
        score -= 2
        recommendations.append("Remove trailing whitespace from lines")
    
    # Check for consistent use of quotes
    single_quotes = len(re.findall(r"'[^']*'", content))
    double_quotes = len(re.findall(r'"[^"]*"', content))
    
    if single_quotes > 0 and double_quotes > 0:
        quote_consistency = max(single_quotes, double_quotes) / (single_quotes + double_quotes)
        if quote_consistency < 0.8:  # Less than 80% consistent
            score -= 3
            recommendations.append("Be consistent with string quotes (either single or double)")
    
    return max(0, score), recommendations

def analyze_reusability(content, lines, tree):
    """Analyze code reusability and DRY principles."""
    score = 15  # Start with full score
    recommendations = []
    
    # Check for repeated code blocks
    code_blocks = []
    current_block = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('#'):
            current_block.append(stripped)
        elif current_block:
            if len(current_block) >= 3:  # Only consider blocks of 3+ lines
                code_blocks.append('\n'.join(current_block))
            current_block = []
    
    # Add the last block if there is one
    if current_block and len(current_block) >= 3:
        code_blocks.append('\n'.join(current_block))
    
    # Check for duplicated blocks
    seen_blocks = set()
    duplicated_blocks = []
    
    for block in code_blocks:
        if block in seen_blocks and len(block.split('\n')) >= 3:
            duplicated_blocks.append(block)
        seen_blocks.add(block)
    
    if duplicated_blocks:
        score -= min(7, len(duplicated_blocks) * 2)
        recommendations.append("Extract repeated code blocks into reusable functions")
    
    # Check for magic numbers
    magic_numbers = re.findall(r'[^_a-zA-Z0-9](\d+)[^_a-zA-Z0-9]', content)
    magic_numbers = [num for num in magic_numbers if num not in ['0', '1', '2']]
    
    if len(magic_numbers) > 5:
        score -= min(4, (len(magic_numbers) - 5) // 2)
        recommendations.append("Replace magic numbers with named constants")
    
    # Check for utility functions and helper classes
    if len(lines) > 100 and len(re.findall(r'def\s+[a-zA-Z0-9_]+\s*\(', content)) < 3:
        score -= 4
        recommendations.append("Create utility functions for common operations")
    
    return max(0, score), recommendations

def analyze_best_practices(content, lines):
    """Analyze adherence to web development best practices."""
    score = 20  # Start with full score
    recommendations = []
    
    # Check for FastAPI-specific best practices if it seems to be a FastAPI file
    is_fastapi = 'from fastapi import' in content or 'import fastapi' in content
    
    if is_fastapi:
        # Check for proper path parameters
        path_params = re.findall(r'@\w+\.(?:get|post|put|delete)\s*\(["\']{1}([^"\']*\{[^}]*\}[^"\']*)["\']', content)
        
        missing_type_path_params = []
        for path in path_params:
            params = re.findall(r'\{([^}:]*)\}', path)
            params_with_type = re.findall(r'\{([^}:]*:[^}]*)\}', path)
            
            if len(params) > len(params_with_type):
                missing_type_path_params.append(path)
        
        if missing_type_path_params:
            score -= min(4, len(missing_type_path_params) * 2)
            recommendations.append("Add type hints to path parameters in FastAPI routes")
        
        # Check for response_model usage
        if 'def' in content and '@app.' in content and 'response_model=' not in content:
            score -= 3
            recommendations.append("Use response_model parameter in FastAPI route decorators for better API documentation")
    
    # Check for print statements
    print_statements = re.findall(r'print\s*\(', content)
    if print_statements:
        score -= min(3, len(print_statements))
        recommendations.append("Replace print statements with proper logging")
    
    # Check for exception handling
    try_blocks = re.findall(r'try\s*:', content)
    except_blocks = re.findall(r'except\s+', content)
    
    if try_blocks and not except_blocks:
        score -= 3
        recommendations.append("Add proper exception handling (except blocks) after try statements")
    
    # Check for bare except clauses
    bare_excepts = re.findall(r'except\s*:', content)
    if bare_excepts:
        score -= 3
        recommendations.append("Avoid bare 'except:' clauses; catch specific exceptions")
    
    # Check for wildcard imports
    wildcard_imports = re.findall(r'from\s+[a-zA-Z0-9_.]+\s+import\s+\*', content)
    if wildcard_imports:
        score -= 2
        recommendations.append("Avoid wildcard imports (from module import *)")
    
    # Check for proper type hints in Python 3
    function_defs = re.findall(r'def\s+[a-zA-Z0-9_]+\s*\(([^)]*)\)(?:\s*->.*?)?:', content)
    functions_with_hints = re.findall(r'def\s+[a-zA-Z0-9_]+\s*\([^)]*\)\s*->', content)
    
    if function_defs and len(functions_with_hints) < len(function_defs) / 2:
        score -= 3
        recommendations.append("Add return type hints to functions")
    
    # Check for properly annotated arguments
    param_annotations = sum(param.strip().count(':') for param in function_defs if param.strip())
    total_params = sum(len(re.findall(r'[a-zA-Z0-9_]+', param)) for param in function_defs if param.strip())
    
    if total_params > 5 and param_annotations < total_params / 2:
        score -= 2
        recommendations.append("Add type annotations to function parameters")
    
    return max(0, score), recommendations 