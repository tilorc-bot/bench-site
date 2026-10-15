# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# case sp-acj4-29-condf · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
# Runs on its own: python3 this-file.py (or paste it into python).

# setup (the harness's warm-up, version capture and cache clearing left out)
from sympy import *
import sympy
import satrefine

# the query code, exactly as it ran
x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
Residual = 3 * log(x) - log(Pow(x, 3))
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

_verdict(Answer, 'false', 'the run satrefine-refine-20261015-025015 answered null (no verdict)')
