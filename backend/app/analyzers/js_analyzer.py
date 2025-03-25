import re
import os
import json

def analyze_javascript(file_path):
    """
    Analyze a JavaScript/React file for code quality.
    
    Args:
        file_path (str): Path to the JavaScript file
        
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
    
    # Analyze naming conventions (10 points)
    naming_score, naming_recs = analyze_naming_conventions(content, lines)
    recommendations.extend(naming_recs)
    
    # Analyze function length and modularity (20 points)
    modularity_score, modularity_recs = analyze_modularity(content, lines)
    recommendations.extend(modularity_recs)
    
    # Analyze comments and documentation (20 points)
    comments_score, comments_recs = analyze_comments(content, lines)
    recommendations.extend(comments_recs)
    
    # Analyze formatting/indentation (15 points)
    formatting_score, formatting_recs = analyze_formatting(content, lines)
    recommendations.extend(formatting_recs)
    
    # Analyze reusability and DRY (15 points)
    reusability_score, reusability_recs = analyze_reusability(content, lines)
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

def analyze_naming_conventions(content, lines):
    """Analyze naming conventions in JavaScript code."""
    score = 10  # Start with full score and deduct based on issues
    recommendations = []
    
    # Check for camelCase variables (common in JS)
    non_camel_case_vars = re.findall(r'(?:let|var|const)\s+([A-Z][a-zA-Z0-9_]*|[a-z][a-z0-9_]*_[a-z0-9_]*)\s*=', content)
    
    if non_camel_case_vars:
        score -= min(5, len(non_camel_case_vars))
        recommendations.append(f"Use camelCase for variable names (found: {', '.join(non_camel_case_vars[:3])})")
    
    # Check for PascalCase components (React convention)
    component_declarations = re.findall(r'(?:function|const)\s+([a-z][a-zA-Z0-9_]*)\s*(?:=\s*\([^)]*\)\s*=>|\([^)]*\)\s*{)', content)
    
    if component_declarations and any("render" in line or "return <" in line or "React" in line for line in lines):
        non_pascal_components = [name for name in component_declarations if name[0].islower()]
        if non_pascal_components:
            score -= min(3, len(non_pascal_components))
            recommendations.append("Use PascalCase for React component names")
    
    # Check for ALL_CAPS constants
    non_caps_constants = re.findall(r'const\s+([a-z][a-zA-Z0-9_]*)\s*=\s*[\'"]?[A-Z0-9_]+[\'"]?', content)
    
    if non_caps_constants:
        score -= min(2, len(non_caps_constants))
        recommendations.append("Consider using ALL_CAPS for constant values")
    
    return max(0, score), recommendations

def analyze_modularity(content, lines):
    """Analyze function length and modularity."""
    score = 20  # Start with full score
    recommendations = []
    
    # Find all function declarations
    function_blocks = re.findall(r'(function\s+\w+\s*\([^)]*\)\s*{[^}]*}|const\s+\w+\s*=\s*(?:\([^)]*\)|function\s*)\s*=>\s*{[^}]*}|const\s+\w+\s*=\s*function\s*\([^)]*\)\s*{[^}]*})', content, re.DOTALL)
    
    # Check function length
    long_functions = []
    for func in function_blocks:
        func_lines = func.count('\n') + 1
        if func_lines > 30:
            long_functions.append(func_lines)
    
    if long_functions:
        deduction = min(10, len(long_functions) * 3)
        score -= deduction
        recommendations.append(f"Break down functions that are too long (found {len(long_functions)} functions over 30 lines)")
    
    # Check for deeply nested conditions/loops
    nested_pattern = r'if\s*\([^)]*\)\s*{(?:[^{}]|{[^{}]*})*{(?:[^{}]|{[^{}]*})*{[^}]*}'
    deep_nesting = re.findall(nested_pattern, content)
    
    if deep_nesting:
        deduction = min(5, len(deep_nesting) * 2)
        score -= deduction
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
    single_line_comments = len(re.findall(r'^\s*//.*$', content, re.MULTILINE))
    multi_line_comments = len(re.findall(r'/\*[\s\S]*?\*/', content))
    jsdoc_comments = len(re.findall(r'/\*\*[\s\S]*?\*/', content))
    
    total_comments = single_line_comments + multi_line_comments
    code_to_comment_ratio = len(lines) / max(1, total_comments)
    
    # Check if functions have JSDoc comments
    function_count = len(re.findall(r'function\s+\w+|const\s+\w+\s*=\s*(?:function|\([^)]*\)\s*=>)', content))
    
    if function_count > jsdoc_comments:
        score -= min(10, (function_count - jsdoc_comments) * 2)
        recommendations.append("Add JSDoc comments to document functions and their parameters")
    
    # Check code-to-comment ratio
    if code_to_comment_ratio > 15:
        score -= 5
        recommendations.append("Add more comments to explain complex logic (current ratio: 1 comment per ~{:.1f} lines)".format(code_to_comment_ratio))
    
    # Check for commented-out code
    commented_code = re.findall(r'^\s*//\s*(const|let|var|function|if|for|while)', content, re.MULTILINE)
    if commented_code:
        score -= min(5, len(commented_code))
        recommendations.append("Remove commented-out code that is no longer needed")
    
    return max(0, score), recommendations

def analyze_formatting(content, lines):
    """Analyze code formatting and indentation."""
    score = 15  # Start with full score
    recommendations = []
    
    # Check consistent indentation
    indent_levels = []
    for line in lines:
        if line.strip() and not line.strip().startswith('//'):
            indent = len(line) - len(line.lstrip())
            if indent > 0:
                indent_levels.append(indent)
    
    if indent_levels:
        # Check if indentation is consistently divisible by 2 or 4
        indent_divisible_by_2 = all(level % 2 == 0 for level in indent_levels)
        indent_divisible_by_4 = all(level % 4 == 0 for level in indent_levels)
        
        if not (indent_divisible_by_2 or indent_divisible_by_4):
            score -= 5
            recommendations.append("Use consistent indentation (2 or 4 spaces)")
    
    # Check for consistent semicolon usage
    lines_with_semicolon = len(re.findall(r';\s*$', content, re.MULTILINE))
    lines_without_semicolon = len(re.findall(r'(const|let|var|return|await).*[^;]\s*$', content, re.MULTILINE))
    
    semicolon_consistency = max(lines_with_semicolon, lines_without_semicolon) / max(1, lines_with_semicolon + lines_without_semicolon)
    
    if semicolon_consistency < 0.8:  # Less than 80% consistent
        score -= 5
        recommendations.append("Be consistent with semicolon usage")
    
    # Check for long lines
    long_lines = [i for i, line in enumerate(lines, 1) if len(line) > 100]
    if long_lines:
        score -= min(5, len(long_lines))
        recommendations.append(f"Break down long lines that exceed 100 characters (found on lines: {', '.join(str(x) for x in long_lines[:3])})")
    
    return max(0, score), recommendations

def analyze_reusability(content, lines):
    """Analyze code reusability and DRY principles."""
    score = 15  # Start with full score
    recommendations = []
    
    # Check for repeated code blocks
    code_blocks = []
    current_block = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('//') and not stripped.startswith('/*'):
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
    
    # Check for hardcoded values that should be constants
    hardcoded_values = re.findall(r'["\']\w+["\']\s*:|=\s*["\'][^"\']+["\']', content)
    if len(hardcoded_values) > 5:
        score -= min(4, (len(hardcoded_values) - 5) // 2)
        recommendations.append("Extract hardcoded strings/values into named constants")
    
    # Check for helper/utility functions
    if len(lines) > 100 and len(re.findall(r'function\s+\w+|const\s+\w+\s*=\s*function', content)) < 3:
        score -= 4
        recommendations.append("Create utility functions for common operations")
    
    return max(0, score), recommendations

def analyze_best_practices(content, lines):
    """Analyze adherence to web development best practices."""
    score = 20  # Start with full score
    recommendations = []
    
    # Check for React-specific best practices if it seems to be a React file
    is_react = 'import React' in content or 'from "react"' in content or 'from \'react\'' in content
    
    if is_react:
        # Check for useEffect dependencies
        effects_without_deps = re.findall(r'useEffect\(\s*\(\)\s*=>\s*{[^}]*}\s*\)', content)
        if effects_without_deps:
            score -= min(5, len(effects_without_deps))
            recommendations.append("Specify dependency arrays in useEffect hooks")
        
        # Check for large components
        component_sizes = []
        for component in re.findall(r'(?:function|const)\s+([A-Z]\w*)[^{]*{[^}]*return\s*\([\s\S]*?\);', content, re.DOTALL):
            component_code = re.search(rf'{component}[^{{]*{{[\s\S]*?return\s*\([\s\S]*?\);', content, re.DOTALL)
            if component_code:
                size = component_code.group(0).count('\n')
                component_sizes.append((component, size))
        
        large_components = [(name, size) for name, size in component_sizes if size > 100]
        if large_components:
            score -= min(5, len(large_components))
            recommendations.append(f"Break down large React components ({', '.join(name for name, _ in large_components[:2])}) into smaller ones")
    
    # Check for console.log statements
    console_logs = re.findall(r'console\.log\(', content)
    if console_logs:
        score -= min(3, len(console_logs))
        recommendations.append("Remove console.log statements before production")
    
    # Check for error handling
    try_catch_blocks = re.findall(r'try\s*{', content)
    promise_calls = re.findall(r'\.then\(', content)
    async_funcs = re.findall(r'async\s+\w+|async\s*\(', content)
    
    if (promise_calls or async_funcs) and not try_catch_blocks:
        score -= 4
        recommendations.append("Add error handling for asynchronous operations")
    
    # Check for undefined/null checks
    if re.search(r'\.\w+\s*\.\w+', content) and not re.search(r'[?!]\.\w+', content):
        score -= 3
        recommendations.append("Add null/undefined checks for nested object properties")
    
    # Check for accessibility in React components
    if is_react and ('<img' in content or '<button' in content):
        if '<img' in content and not 'alt=' in content:
            score -= 3
            recommendations.append("Add alt attributes to img elements for accessibility")
        
        if '<button' in content and not 'aria-' in content:
            score -= 2
            recommendations.append("Add ARIA attributes for better accessibility")
    
    return max(0, score), recommendations 