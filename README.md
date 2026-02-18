# AI Code Analyzer

An AI-powered command-line tool that analyzes Python code using Abstract Syntax Trees (AST) and a Large Language Model (LLM) to generate explanations, docstrings, and improvement suggestions.

This tool is perfect for understanding legacy code, reviewing pull requests, or quickly documenting your own projects.

![AI Code Analyzer Demo](https://user-images.githubusercontent.com/11265217/233045501-1e9d8e7d-3a1b-4d7a-8d01-6f6a7d8c4a5c.gif) 
*(Demo GIF placeholder - a real demo would show the command being run and the colorful output)*

## Features

- **AST-Powered Parsing**: Accurately isolates functions and classes from your Python file.
- **In-Depth Explanations**: Generates clear, step-by-step logic explanations for complex code.
- **Automatic Docstrings**: Creates professional, Google-style docstrings for functions and classes.
- **Refactoring Suggestions**: Provides actionable advice on improving code clarity, efficiency, and style.
- **Bug Detection**: Highlights potential bugs and unhandled edge cases.
- **Rich Terminal Output**: Uses colors to make the analysis easy to read.

## Installation

1.  **Clone the repository:**
    bash
    git clone https://github.com/your-username/ai-code-analyzer.git
    cd ai-code-analyzer
    

2.  **Install dependencies:**
    bash
    pip install -r requirements.txt
    

3.  **Set up your API Key:**
    Create a file named `.env` in the project root and add your OpenAI API key:
    
    OPENAI_API_KEY="sk-YourSecretKeyHere"
    

## Usage

Run the analyzer by passing the path to a Python file as an argument.

bash
python main.py path/to/your/python_file.py


### Example

Let's analyze an example file, `example_code.py`:

python
# example_code.py

class DataProcessor:
    def __init__(self, data_list):
        self.d = data_list

    def process(self):
        # A complex and inefficient way to get unique, sorted, even numbers
        temp = []
        for x in self.d:
            if x not in temp:
                temp.append(x)
        
        res = []
        for x in temp:
            if x % 2 == 0:
                res.append(x)
        
        res.sort()
        return res

def fib(n):
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()



Now, run the analyzer on it:

bash
python main.py example_code.py


#### Example Output


Parsing 'example_code.py'...

Found 2 functions/classes to analyze. Contacting AI...

--- Analyzing Class: `DataProcessor` (line 3) ---

### Summary
This class processes a list of data to return a sorted list of unique even numbers.

### Logic Explanation
1. The `__init__` method initializes an instance with a list of data, storing it as `self.d`.
2. The `process` method first creates a new list `temp` containing only the unique elements from the input list `self.d` by iterating and checking for existence before appending.
3. It then initializes another list `res`.
4. It iterates through the unique elements in `temp`, checks if an element is even (`x % 2 == 0`), and appends it to `res`.
5. Finally, it sorts the list `res` in place and returns it.

### Refactoring Suggestions
- The variable `self.d` in the constructor could be renamed to `self.data` for better clarity.
- The process of finding unique elements and then filtering for even numbers can be significantly simplified using Python's built-in `set` for uniqueness and a list comprehension for filtering and sorting.

A more Pythonic version of the `process` method would be:
python
def process(self):
    unique_numbers = set(self.data)
    even_numbers = [num for num in unique_numbers if num % 2 == 0]
    return sorted(even_numbers)


### Potential Bugs
No obvious bugs found, but the current implementation is inefficient for large lists due to the repeated `x not in temp` checks, which have O(n) complexity, leading to an overall O(n^2) uniqueness step.

### Generated Docstring
python
"""Processes a list of numerical data.

Attributes:
    data (list): A list of numbers to be processed.
"""

--- End of Analysis for `DataProcessor` ---

--- Analyzing Function: `fib` (line 21) ---

### Summary
This function prints the Fibonacci sequence up to a given number `n`.

### Logic Explanation
1. It initializes two variables, `a` and `b`, to 0 and 1, respectively, which are the first two numbers in the Fibonacci sequence.
2. It enters a `while` loop that continues as long as `a` is less than the input `n`.
3. Inside the loop, it prints the current value of `a`.
4. It then updates `a` and `b` for the next iteration: `a` takes the value of `b`, and `b` becomes the sum of the old `a` and `b`.
5. After the loop finishes, it prints a newline character for clean formatting.

### Refactoring Suggestions
- The function prints the sequence directly instead of returning it. It would be more versatile as a generator function using `yield` or if it returned a list of the numbers.

### Potential Bugs
- If a negative number is passed as `n`, the loop condition `a < n` (e.g., `0 < -5`) will be false immediately, and the function will print nothing, which might be unexpected behavior. It would be good to add a check for non-positive input.

### Generated Docstring
python
"""Generates and prints the Fibonacci sequence up to a limit.

Args:
    n (int): The upper limit for the sequence. Numbers in the sequence
        will be printed as long as they are less than n.
"""

--- End of Analysis for `fib` ---



## How It Works

1.  **File Reading**: The script starts by reading the target Python file provided as a command-line argument.
2.  **AST Parsing**: It uses Python's built-in `ast` module to parse the source code into an Abstract Syntax Tree. This tree is a structured representation of the code that's easy to traverse programmatically.
3.  **Node Visiting**: A custom `ast.NodeVisitor` class walks the tree and identifies all top-level `FunctionDef` (function) and `ClassDef` (class) nodes.
4.  **Code Extraction**: For each identified node, the script reconstructs the original source code snippet for just that function or class using `ast.unparse()`.
5.  **LLM Prompting**: The extracted code snippet is embedded into a carefully engineered prompt that instructs a powerful LLM (like GPT-4o) to act as an expert code reviewer and provide analysis in a specific Markdown format.
6.  **Output Formatting**: The Markdown response from the LLM is received and printed to the console with color formatting for readability.

## License

This project is licensed under the MIT License.