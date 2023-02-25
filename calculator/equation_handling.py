import logging
import sys
from enum import Enum
from typing import List

ARITHMETIC_OPERATOR_MAP = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "^": lambda x, y: x ** y,
}


class Arithmetics(tuple, Enum):
    OPERATORS = "^", "*", "/", "-", "+"
    """Operators in descending order of priority"""
    NUMERALS = "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
    EQUALS = "=",
    BRACKETS = "(", ")"
    ALLOWEDS = OPERATORS + NUMERALS + EQUALS + BRACKETS


def solve_equation(equation: List[str]):
    while len(equation) > 1:

        bracket_crawl = 0
        bracket_pairs = []
        opening_index = None
        for index, arithmetic in enumerate(equation):
            if arithmetic == "(":
                if bracket_crawl == 0:
                    opening_index = index
                bracket_crawl += 1
            elif arithmetic == ")":
                bracket_crawl -= 1
                if bracket_crawl == 0:
                    bracket_pairs.append((opening_index, index))
        if bracket_crawl != 0:
            raise ValueError(f"Unmatched brackets in equation {' '.join(equation)}")

        shift = 0
        for left_bracket, right_bracket in bracket_pairs:
            sub_equation = equation[
                           left_bracket + 1 + shift: right_bracket + shift]  # Don't include the brackets itself
            result = solve_equation(sub_equation)
            del equation[left_bracket + shift: right_bracket + shift + 1]
            # Insert the result where the sub equation was:
            equation.insert(left_bracket + shift, result)
            # Reduce shift by the removed slice but also incorporate the added inserted result:
            shift = shift - (right_bracket - left_bracket)

        operator_index = None
        for search_operator in Arithmetics.OPERATORS.value:
            try:
                operator_index = equation.index(search_operator)
            except ValueError:
                operator_index = None
            else:
                break
        if operator_index is None:
            raise ValueError("Cannot solve equations with two consecutive numbers.")
        operation = ARITHMETIC_OPERATOR_MAP[equation[operator_index]]
        left_value = float(equation[operator_index - 1])
        right_value = float(equation[operator_index + 1])
        equation = (
                equation[:operator_index - 1]
                + [operation(left_value, right_value)]
                + equation[operator_index + 2:]
        )
    return equation[0]


def equation_from_string(string_equation: str) -> List[str]:
    """
    Creates a properly formatted equation from a passed String.
    The equation will be formatted by seperating operators from numbers.

    This function does not validate the syntax of the parsed equation.
    """
    equation = []
    current_number = ""
    for char in string_equation:
        if char == " ":
            continue  # Ignore spaces

        # >> When an operator occurs, the parsing of the current number has finished so first the
        # `current_number` will be appended and then the operator.
        if char in Arithmetics.OPERATORS.value or Arithmetics.BRACKETS.value:
            if current_number != "":
                equation.append(current_number)
                current_number = ""
            equation.append(char)
        # <<
        elif char in Arithmetics.NUMERALS.value:
            current_number += char
        else:
            raise ValueError(f"Unexpected arithmetic encountered: {char}")

    if current_number != "":
        equation.append(current_number)
    return equation


BASIC_EQUATIONS = [
    ("2 + 4", 6),
    ("2 - 4", -2),
    ("2 * 4", 8),
    ("2 / 4", 0.5),
    ("2 ^ 4", 16),
]
"""Equations with just one operator."""
LINEAR_EQUATIONS = [
    ("3 * 2 + 4", 10),
    ("3 * 2 - 4", 2),
    ("3 / 2 + 4", 5.5),
    ("3 / 2 - 4", -2.5),
    ("3 ^ 2 - 4", 5),
]
"""Equations with mixed operators.
The operators are ordered so they will be resolved correctly with left-to-right parsing."""
NONLINEAR_EQUATIONS = [
    ("3 + 2 * 4", 11),
    ("3 - 2 * 4", -5),
    ("3 + 2 / 4", 3.5),
    ("3 - 2 / 4", 2.5),
    ("3 + 2 ^ 4", 19),
    ("3 + 2 * 4 + 8", 19),
    ("3 - 2 * 4 + 8", 3),
    ("3 + 2 / 4 + 8", 11.5),
    ("3 - 2 / 4 + 8", 10.5),
    ("3 + 2 ^ 4 + 8", 27),
]
"""Equations with mixed operators.
The operators are ordered so they will be resolved correctly only with priority parsing."""
BASIC_BRACKETED_EQUATIONS = [
    ("(3 + 2) * 4", 20),
    ("(3 - 2) * 4", 4),
    ("(3 + 2) / 4", 1.25),
    ("(3 - 2) / 4", 0.25),
    ("(3 + 2) ^ 4", 625),
    ("(3 + 2) * (4 + 8)", 60),
    ("(3 - 2) * (4 + 8)", 12),
    ("(3 + 2) / (4 + 8)", 5 / 12),
    ("(3 - 2) / (4 + 8)", 1 / 12),
    ("(1 + 2) ^ (2 + 2)", 81),
]
"""Equations with mixed operators.
Each equation contains brackets."""

NESTED_BRACKETED_EQUATIONS = [
    ("((3 + 1) * (2 + 1) + 1) * 2", 26),
    ("((3 - 1) * (2 + 1) - 1) * 2", 10),
    ("((3 + 1) * (2 + 1) + 1) / 2", 6.5),
    ("((3 - 1) * (2 + 1) - 1) / 2", 2.5),
]
"""Equations with mixed operators, excluding exponential operators.
Each equation contains nested brackets."""



