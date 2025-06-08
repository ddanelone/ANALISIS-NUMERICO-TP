# services/utils.py

from sympy import sympify, symbols
from typing import Callable

def eval_func(expr: str) -> Callable[[float], float]:
    x = symbols('x')
    f = sympify(expr)
    return lambda val: float(f.subs(x, val))
