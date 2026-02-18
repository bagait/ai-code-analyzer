import os
import argparse
import ast
from openai import OpenAI
from dotenv import load_dotenv
import sys

# --- Configuration and Setup ---
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    print("Error: OPENAI_API_KEY not found. Please set it in a .env file.")
    sys.exit(1)

client = OpenAI(api_key=API_KEY)

# --- ANSI Color Codes for Rich Terminal Output ---
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# --- Core Logic: AST Visitor and LLM Interaction ---

class CodeAnalyzerVisitor(ast.NodeVisitor):
    """An AST visitor that identifies functions and classes for analysis."""
    def __init__(self, source_code):
        self.source_lines = source_code.splitlines()
        self.nodes_to_analyze = []

    def visit_FunctionDef(self, node):
        self.nodes_to_analyze.append(node)
        self.generic_visit(node)  # Continue traversing inside the function

    def visit_ClassDef(self, node):
        self.nodes_to_analyze.append(node)
        self.generic_visit(node)  # Continue traversing inside the class

def get_node_source(node, source_lines):
    """Extracts the full source code of an AST node."""
    try:
        # ast.unparse is the modern way for Python 3.9+
        return ast.unparse(node)
    except AttributeError:
        # Fallback for older Python versions (less accurate)
        start_line = node.lineno - 1
        end_line = node.end_lineno
        return "\n".join(source_lines[start_line:end_line])

def generate_analysis(code_snippet):
    """Sends the code to an LLM and returns the analysis."""
    prompt = f"""
    You are an expert Python code reviewer. Analyze the following code snippet.
    Provide a detailed analysis in the following Markdown format:

    ### Summary
    A brief, one-sentence summary of what this code does.

    ### Logic Explanation
    A step-by-step explanation of the code's logic. Use a numbered list.

    ### Refactoring Suggestions
    Suggest improvements for clarity, efficiency, and Pythonic style (e.g., better variable names, simpler logic). If none, state "No major suggestions.".

    ### Potential Bugs
    Identify any potential bugs, edge cases not handled, or logical errors. If none, state "No obvious bugs found.".

    ### Generated Docstring
    Create a professional, Google-style Python docstring for the function or class.

    --- Code to Analyze ---
    python
    {code_snippet}
    
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert Python code reviewer providing detailed analysis in Markdown format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error communicating with OpenAI API: {e}"

def print_analysis(node, analysis):
    """Prints the analysis in a formatted way."""
    node_type = "Class" if isinstance(node, ast.ClassDef) else "Function"
    name = node.name
    line_number = node.lineno

    print(f"{Color.HEADER}{Color.BOLD}--- Analyzing {node_type}: `{name}` (line {line_number}) ---{Color.ENDC}\n")
    print(analysis)
    print(f"{Color.HEADER}{Color.BOLD}--- End of Analysis for `{name}` ---\{Color.ENDC}\n\n")


def main():
    """Main function to run the code analyzer."""
    parser = argparse.ArgumentParser(description="Analyze a Python file using AI.")
    parser.add_argument("file_path", help="The path to the Python file to analyze.")
    args = parser.parse_args()

    try:
        with open(args.file_path, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"{Color.FAIL}Error: File not found at '{args.file_path}'{Color.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"{Color.FAIL}Error reading file: {e}{Color.ENDC}")
        sys.exit(1)

    print(f"{Color.GREEN}Parsing '{args.file_path}'...{Color.ENDC}\n")
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        print(f"{Color.FAIL}Error: Invalid Python syntax in file: {e}{Color.ENDC}")
        sys.exit(1)

    analyzer_visitor = CodeAnalyzerVisitor(source_code)
    analyzer_visitor.visit(tree)

    nodes = analyzer_visitor.nodes_to_analyze
    if not nodes:
        print(f"{Color.WARNING}No functions or classes found to analyze in '{args.file_path}'.{Color.ENDC}")
        return

    print(f"{Color.GREEN}Found {len(nodes)} functions/classes to analyze. Contacting AI...{Color.ENDC}\n")

    for node in nodes:
        code_snippet = get_node_source(node, source_code.splitlines())
        analysis = generate_analysis(code_snippet)
        print_analysis(node, analysis)

if __name__ == "__main__":
    main()
