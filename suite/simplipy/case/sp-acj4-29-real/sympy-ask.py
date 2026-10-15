# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# case sp-acj4-29-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
# Runs on its own: python3 this-file.py (or paste it into python).

# setup (the harness's warm-up, version capture and cache clearing left out)
from sympy import *
import sympy

# the query code, exactly as it ran
x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
Residual = 3 * log(x) - log(Pow(x, 3))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')

def _verdict(answer, expected, stored):
    kind = type(answer).__name__
    got = ("true" if answer is True or kind == "BooleanTrue" else
           "false" if answer is False or kind == "BooleanFalse" else "null")
    outcome = (("declined correctly" if expected == "contingent" else "no verdict") if got == "null" else
               "solved" if got == expected else "wrong" if expected in ("true", "false", "contingent") else "?")
    print(f"verdict: {got} (expected {expected}: {outcome}; {stored})")
    return got

_verdict(Answer, 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)')
