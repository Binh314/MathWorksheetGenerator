from string import Template
from functools import reduce
import random
from pdflatex import PDFLaTeX
import os



def find_factors(n: int) -> list:
    """Finds and returns the factors of a number.
       Source: https://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python

    Args:
        n (int): number to find factors for

    Returns:
        list: list of factors for the number `n`
    """
    return list(set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0))))

def num_to_latex(num_digits: int, num: int) -> str:
    """Returns a LaTeX string of a number formatted for the worksheet.

    Args:
        num_digits (int): max number of digits in the math problems
        num (int): number to convert to LaTeX string

    Returns:
        str: LaTeX string of number `n` formatted for the worksheet
    """
    num_string = str(num)
    padding = "".join(['x' for _ in range(num_digits - len(num_string))]) # x will later be replaced with latex padding
    num_string = padding + num_string
    num_latex = '\\,'.join([digit if digit != 'x' else '\\phantom{0}' for digit in num_string]) #\phantom{0} is latex padding
    return num_latex

def operation_to_latex(operation: str) -> str:
    """Returns the math operation as a LaTeX string.

    Args:
        operation (str): operation

    Returns:
        str: LaTeX string for the math operation
    """
    if operation in {"add", "addition", "plus"}:
        return "+"
    if operation in {"sub", "subtract", "subtraction", "minus"}:
        return "-"
    if operation in {"multiply", "multiplication", "times", "x"}:
        return "\\times"
    if operation in {"div", "divide", "division", "\\"}:
        return "\\div"
    return operation

def create_problem_latex(num_digits: int, operation: str, num1: int, num2: int) -> str:
    """Creates and returns a LaTeX string of a math problem for the worksheet.

    Args:
        num_digits (int): max number of digits in a math problem for the worksheet.
        operation (str): math operation of the problem
        num1 (int): first operand of the math problem
        num2 (int): second operand of the math problem

    Returns:
        str: LaTeX string of the math problem, `num1` `operation` `num2` formatted for the worksheet
    """
    num1_latex = num_to_latex(num_digits, num1)
    num2_latex = num_to_latex(num_digits, num2)

    operation = operation_to_latex(operation)

    problem_latex = \
f'''\\begin{{myequation}}
    \\begin{{array}}{{r}}
        {num1_latex} \\\\
        {operation}\\phantom{{0}}{num2_latex} \\\\
        \\hline\\\\
        \\hline
    \\end{{array}}
\\end{{myequation}}'''

    return problem_latex

def create_random_problem_latex(num_digits: int, included_operations: list = ['+', '-'], limit_multiplication: bool = True) -> str:
    """Creates a random math problem and returns a LaTeX string of it.

    Args:
        num_digits (int): max number of digits for a math problem on the worksheet
        included_operations (list, optional): list of potential math operations for the problem. Defaults to ['+', '-'].
        limit_multiplication (bool, optional): if true, limits multiplication problems to 12 x 12 times table.

    Returns:
        str: LaTeX string of the randomly generated math problem
    """
    operation = operation_to_latex(random.choice(included_operations))
    max_num = 10**num_digits - 1

    num1 = random.randint(0, max_num)
    num2 = random.randint(0, max_num)

    if operation == '-' and operation == '\\times':
        num1 = random.randint(0, 12)
        num2 = random.randint(0, 12)

    if operation == '-':
        # swap places if first num is less than second num (no negative differences for now)
        if num1 < num2: num1, num2 = num2, num1 

    if operation == '\\div':
        quotient = random.randint(0, max_num)
        factors = find_factors(quotient)
        divisor = random.choice(factors)
        num1 = quotient
        num2 = divisor

    return create_problem_latex(num_digits, operation, num1, num2)

def create_worksheet_latex(num_digits: int, included_operations: list = ['+', '-'], limit_multiplication: bool = True) -> str:
    """Creates a LaTeX string of a worksheet with 20 math problems.

    Args:
        num_digits (int): max number of digits in the math problems
        included_operations (list, optional): math operations on the worksheet. Defaults to ['+', '-'].
        limit_multiplication (bool, optional): if true, limits multiplication problems to 12 x 12 times table. Defaults to True.

    Returns:
        str: LaTeX string of a worksheet with 20 math problems
    """
    problems_per_row = 4
    num_rows = 5
    worksheet_latex = ""
    count = 0
    for _ in range(num_rows):
        for j in range(problems_per_row):
            count += 1
            problem_latex = create_random_problem_latex(num_digits, included_operations, limit_multiplication)
            worksheet_latex += problem_latex + "&\n"
        worksheet_latex = worksheet_latex[:-2] # remove alignment character (&)
        worksheet_latex += "\\\\ \n"
    return worksheet_latex

def create_worksheet_pdf(num_digits: int, included_operations: list = ['+', '-'], limit_multiplication: bool = True):
    """Creates a pdf worksheet of 20 math problems.

    Args:
        num_digits (int): max number of digits in the math problems
        included_operations (list, optional): math operations on the worksheet. Defaults to ['+', '-'].
        limit_multiplication (bool, optional): if true, limits multiplication problems to 12 x 12 times table. Defaults to True.
    """

    with open('template.txt', 'r') as file:
        latex_string = file.read().replace('$', '$$').replace('#','$') # `#` used as identifier in template.txt

    template_latex_string = Template(latex_string)

    worksheet_problems = create_worksheet_latex(num_digits, included_operations, limit_multiplication)

    worksheet_latex = template_latex_string.substitute({'problems':worksheet_problems})

    with open('worksheet.tex', 'w') as file:
        file.write(worksheet_latex)

    os.system("pdflatex worksheet.tex")

if __name__ == '__main__':
    create_worksheet_pdf(3)