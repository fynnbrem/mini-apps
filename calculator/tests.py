"""This module contains tests for `equation_handling.py`"""
import unittest
from typing import Callable

from equation_handling import equation_from_string, Arithmetics, solve_equation


class test_solve_equation(unittest.TestCase):

    def assertion_helper(self, equationsAndResults):
        """
        Takes pairs `equationsAndResults`, each consisting of an equation (`str`) and the expected result (`float`).
        The equation will be formatted using `equation_from_string()` and then solved using `solve_equation()`.
        The expected result will be compared to the result of `solve_equation()`
        """
        for equation, expected_result in equationsAndResults:
            resulted_result = solve_equation(equation_from_string(equation))
            if resulted_result != expected_result:
                errorText = (
                    "Equation solved incorrectly:"
                    f"{equation} =\n"
                    f"\tIs:\t\t{resulted_result}"
                    f"\tShould:\t{float(expected_result)}"
                )
                raise AssertionError(errorText)

    def test_basic(self):
        """
        Premise: Solve equations which have only one Operator.
        """
        equations = [
            ("2 + 4", 6),
            ("2 - 4", -2),
            ("2 * 4", 8),
            ("2 / 4", 0.5),
            ("2 ^ 4", 16),
        ]
        self.assertion_helper(equations)

    def test_linear(self):
        """
        Premise: Solve equations, which have mixed operators, but can be solved correctly
            by strictly solving from left-to-right.
        """
        equations = [
            ("3 * 2 + 4", 10),
            ("3 * 2 - 4", 2),
            ("3 / 2 + 4", 5.5),
            ("3 / 2 - 4", -2.5),
            ("3 ^ 2 - 4", 5),
        ]
        self.assertion_helper(equations)

    def test_nonlinear(self):
        """
        Premise: Solve equations, which have mixed operators and cannot be solved strictly from left-to-right.

        Should-Do: Calculate Terms with a higher priority first.
        """
        equations = [
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
        self.assertion_helper(equations)

    def test_basic_bracket(self):
        """
        Premise: Solve equations with bracketed Terms.

        Should-Do: Solve the bracketed Term first.
        """
        equations = [
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
        self.assertion_helper(equations)

    def test_nested_bracket(self):
        """
        Premise: Solve equations which have bracketed Terms within bracketed Terms.

        Should-Do: Solve the deepest bracketed Terms first.
        """
        equations = [
            ("((3 + 1) * (2 + 1) + 1) * 2", 26),
            ("((3 - 1) * (2 + 1) - 1) * 2", 10),
            ("((3 + 1) * (2 + 1) + 1) / 2", 6.5),
            ("((3 - 1) * (2 + 1) - 1) / 2", 2.5),
        ]
        self.assertion_helper(equations)


class test_equation_from_string(unittest.TestCase):

    def test_format(self):
        string_equations = (
            "2 + 4",
            "3 * 2 + 4",
            "3 + 2 * 4",
            "(3 + 2) * 4",
            "((3 + 1) * (2 + 1) + 1) * 2",
            "2 ^ 4"
        )
        for string_equation in string_equations:
            equation = equation_from_string(string_equation)
            self.assertIsInstance(equation, list, f"`{equation}` is not a `list`.")
            [self.assertIsInstance(atom, str, f"`{atom}` in `{string_equation}` is not a `str`.") for atom in equation]
            for atom in equation:
                if atom in Arithmetics.ALLOWEDS.value:
                    valid = True
                else:
                    try:
                        float(atom)
                    except ValueError:
                        valid = False
                    else:
                        valid = True
                self.assertTrue(valid, f"`{atom}` in `{string_equation}` is not a valid Arithmetic.")


if __name__ == "__main__":
    unittest.main()
