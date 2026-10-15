# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# case sp-acj4-229-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174730 answered true (solved)
# Runs on its own: python3 this-file.py (or paste it into python).

# setup (the harness's warm-up, version capture and cache clearing left out)
from sympy import *
import sympy
import satrefine

# the query code, exactly as it ran
x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Pow(pi, x)))
Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
Result = satrefine.refine(Residual, Assum)
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

_verdict(Answer, 'true', 'the run satrefine-refine-20261014-174730 answered true (solved)')
