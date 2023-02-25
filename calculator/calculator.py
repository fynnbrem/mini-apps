"""
A simple Calculator
"""
from enum import Enum
from typing import TYPE_CHECKING, List
from equation_handling import Arithmetics

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton
import PySide6





class CalculatorLabel(QLabel):
    def __init__(self):
        super().__init__()
        font = self.font()
        font.setFamily("Lucida Console")
        font.setPixelSize(40)
        self.setFont(font)


class NumberPad(QWidget):
    grid_base = [
        [7, 8, 9],
        [4, 5, 6, "+", "-"],
        [1, 2, 3, "/", "+"],
        [None, 0, None, "="]
    ]
    assert all(
        (str(arithmetic) in Arithmetics.ALLOWEDS.value or arithmetic is None) for row in grid_base for arithmetic in
        row)

    def __init__(self):
        super().__init__()
        self.setLayout(QGridLayout())
        self.operation_buttons = []
        self.equals_button = None
        for row_index, row_content in enumerate(NumberPad.grid_base):
            for column_index, cell_content in enumerate(row_content):
                button = QPushButton(str(cell_content))
                self.layout().addWidget(button, row_index, column_index)
                if cell_content != "=":
                    self.operation_buttons.append(button)
                else:
                    self.equals_button = button

    if TYPE_CHECKING:
        def layout(self) -> PySide6.QtWidgets.QGridLayout:
            ...


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        # >>> Content:
        self.calc_label = CalculatorLabel()
        self.num_pad = NumberPad()
        # <<<
        # >>> Layout:
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.calc_label)
        self.layout().addWidget(self.num_pad)
        # <<<
        # >>> Style:
        # <<<
        # >>> Control:
        [button.pressed.connect(lambda b=button: self.append_to_equation(b.text()))
         for button in self.num_pad.operation_buttons]
        def ParseEquation():
            result = solve_equation(self._equation)
            if result.is_integer():
                # If applicable, cast to `int` to remove the trailing `0`:
                result = int(result)
            self.calc_label.setText(str(result))
            self._equation = []
        self.num_pad.equals_button.pressed.connect(lambda: ParseEquation())
        self.calc_label.setText("Hello")
        # <<<
        # >>> Data:
        self._equation = []
        # <<<

    @property
    def equation(self):
        return tuple(self._equation)

    def set_equation(self, value: List[str]):
        self._equation = value
        self.calc_label.setText(" ".join(self._equation))

    def append_to_equation(self, value: str):
        # >>> Decide where the value should be inserted into the `_equation` by the following criteria:
        #   1. If the `value` is an operator:
        #       a. If the last item in `equation` is an operator, *replace* it with the operator.
        #       b. Else append the operator as its own item.
        #   2. If the `value` is a numeral:
        #       a. If the last item in `equation` is an operator, append the numeral as its own item
        #       b. Else expand the last item with the `value`
        if value not in Arithmetics.ALLOWEDS.value:
            raise ValueError(f"Tried to add an unknown arithmetic `{value}` to `equation`.")

        value_is_operator = value in Arithmetics.OPERATORS.value
        if len(self._equation) == 0:
            # Just add the `value` if it is the first item:
            if value_is_operator:
                # Add a `0` if trying to add an operator as first item.
                # This allows for expected operation even for odd syntax:
                self._equation.append("0")
            self._equation.append(value)
        else:
            last_is_operator = self._equation[-1] in Arithmetics.OPERATORS.value
            if value_is_operator and last_is_operator:
                self._equation[-1] = value  # Replace
            elif value_is_operator and not last_is_operator:
                self._equation.append(value)  # Append
            elif not value_is_operator and last_is_operator:
                self._equation.append(value)  # Append
            elif not value_is_operator and not last_is_operator:
                self._equation[-1] += value  # Expand
        # <<<

        self.calc_label.setText(" ".join(self._equation))


def solve_equation(equation: List[str]) -> float:
    arithmetic_map = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y
    }
    result = None
    next_operation = None
    for arithmetic in equation:
        if result is None:
            result = float(arithmetic)
        else:
            if arithmetic in Arithmetics.OPERATORS.value:
                next_operation = arithmetic_map[arithmetic]
            else:
                arithmetic = float(arithmetic)
                result = next_operation(result, arithmetic)
    if result is None:
        result = 0
    return result



if __name__ == "__main__":
    # >>> Content:
    app = QApplication()
    window = QMainWindow()
    main = Calculator()
    # <<<
    # >>> Layout:
    window.setCentralWidget(main)
    # <<<
    window.show()
    app.exec()
