import re
import sys


def clean_code(code):
    """
    Correctly cleans the code by removing comments (both Python and C++ style) and unnecessary whitespace,
    while handling string literals correctly.
    """
    cleaned_code = []
    in_string = False
    string_char = ''
    escape = False
    comment = False
    line = ''

    for char in code:
        if char == '\n' and not in_string:
            if line.strip():
                cleaned_code.append(line.strip())
            line = ''
            comment = False
            continue

        if comment:
            continue

        if char == '\\' and in_string:
            escape = not escape
        elif char in ('"', "'") and not escape:
            if in_string:
                if char == string_char:
                    in_string = False
            else:
                in_string = True
                string_char = char
        elif char == '#' and not in_string:
            comment = True
            continue
        elif char == '/' and not in_string and line.endswith('/'):
            line = line[:-1]
            comment = True
            continue

        if not comment:
            line += char

        if escape and char != '\\':
            escape = False

    if line.strip() and not comment:
        cleaned_code.append(line.strip())

    return '\n'.join(cleaned_code)


def tokenize_code(code):
    """
    Tokenizes the given code snippet into categories: Keywords, Identifiers, Operators, Delimiters, and Literals.
    This version aims to be more versatile to handle both Python and C++ code.
    """
    # Regular expressions for different types of tokens
    patterns = {
        'Keywords': r'\b(def|return|print|if|else|while|for|include|using|namespace|int|cout|endl)\b',
        'Identifiers': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
        'Operators': r'[\+\=\-*/<>]',
        'Delimiters': r'[\(\)\[\]{};:,]',
        'Literals': r'\b\d+\b'
    }

    tokens = {
        'Keywords': set(),
        'Identifiers': set(),
        'Operators': set(),
        'Delimiters': set(),
        'Literals': set()
    }

    excluded_keywords = patterns['Keywords'].replace(r'\b', '').split('|')

    for category, pattern in patterns.items():
        matches = re.findall(pattern, code)
        for match in matches:
            if category == 'Identifiers' and match in excluded_keywords:
                continue
            tokens[category].add(match)

    for category in tokens:
        tokens[category] = sorted(tokens[category])

    return tokens


def read_code_from_file(file_path):
    """
    Reads code from a given file path and returns the content as a string.
    Adds exception handling for cases where the file might not exist or be inaccessible.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied to read the file '{file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred while reading '{file_path}': {e}")
    sys.exit(1)


def display_tokens_in_tabular_form(tokens):
    """
    Displays tokens in a simple tabular form using print statements.
    For a more sophisticated table, consider using the pandas library.
    """
    print("Category\t\tTokens")
    print("-" * 50)
    for category, tokens_list in tokens.items():
        print(f"{category}\t\t{', '.join(tokens_list)}")


file_path = input("Enter file name: ")
code = read_code_from_file(file_path)

cleaned_code = clean_code(code)

code_tokens = tokenize_code(cleaned_code)

display_tokens_in_tabular_form(code_tokens)
