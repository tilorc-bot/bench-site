# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# case demo-log-02 · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024429 answered null (declined correctly)
# Runs on its own: python3 this-file.py (or paste it into python).

# setup (the harness's warm-up, version capture and cache clearing left out)
from sympy import *
import sympy

# the query code, exactly as it ran
z = Symbol('z', complex=True)
w = Symbol('w', complex=True)
Assum = And(Q.complex(z), Q.complex(w), ~Q.zero(z), ~Q.zero(w))
Residual = log(z * w) - (log(z) + log(w))
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

_verdict(Answer, 'contingent', 'the run sympy-ask-20261015-024429 answered null (declined correctly)')
