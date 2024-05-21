import re
from turtle import pos

# Token types
TOKEN_TYPES = {
    'KEYWORD': r'\b(if|else|for|do|while|switch|case|default|break|return|end|read|write|then|repeat)\b',
    'INT_LIT': r'\b\d+\b',
    'REAL_LIT': r'\b\d+\.\d+\b',
    'STRING_LIT': r'"[^"]*"',
    'IDENTIFIER': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
    'SPECIAL': r'[(){},;]',
        # KEYWORDS = ['else', 'end', 'if', 'repeat', 'then', 'until', 'read', 'write']
    "OPERATORS" : r'[:=<>+-/*{}();]',
    # {
        # '+': 'Plus',
        # '-': 'Minus',
        # '*': 'Mult',
        # '/': 'Div',
        # ':': 'Colon',
        # '=': 'Equal',
        # ':=': 'Assign',
        # '>': 'Greater',
        # '<': 'Lessthan',
        # ';': 'Semicolon',
        # '(': 'OpenBracket',
        # ')': 'ClosedBracket'
    # }
}

def check_lexical_errors(code):
    # Define patterns for recognized tokens
    token_patterns = '|'.join(f'(?P<{tok}>{pattern})' for tok, pattern in TOKEN_TYPES.items())
    token_regex = re.compile(token_patterns)
    pos = 0
    errors = []
    while pos < len(code):
        match = token_regex.match(code, pos)
        if match:
            pos = match.end()
        else:
            if code[pos].isspace():  # Skip whitespace
                pos += 1
            else:
                # Accumulate unrecognized sequences
                start = pos
                while pos < len(code) and not code[pos].isspace() and token_regex.match(code, pos) is None:
                    pos += 1
                errors.append(code[start:pos])
    return errors

def lexical_analysis(file_path):
    try:
        with open(file_path, 'r') as file:
            code = file.read()
        lexical_errors = check_lexical_errors(code)
        if lexical_errors:
            error_message = "Lexical Errors Found:\n" + '\n'.join(f"Unrecognized sequence: {error}" for error in lexical_errors)
        else:
            error_message = "No lexical errors found."
        return error_message
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
