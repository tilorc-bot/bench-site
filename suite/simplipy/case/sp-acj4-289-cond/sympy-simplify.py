# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# case sp-acj4-289-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
# Runs on its own: python3 this-file.py (or paste it into python).

# setup (the harness's warm-up, version capture and cache clearing left out)
from sympy import *
import sympy

# the query code, exactly as it ran
x = Symbol('x', complex=True, imaginary=True)
Residual = Pow(Abs(x), 8) - Pow(x, 8)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')

def _verdict(answer, expected, stored):
    kind = type(answer).__name__
    got = ("true" if answer is True or kind == "BooleanTrue" else
           "false" if answer is False or kind == "BooleanFalse" else "null")
    outcome = (("declined correctly" if expected == "contingent" else "no verdict") if got == "null" else
               "solved" if got == expected else "wrong" if expected in ("true", "false", "contingent") else "?")
    print(f"verdict: {got} (expected {expected}: {outcome}; {stored})")
    return got

_verdict(Answer, 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)')
