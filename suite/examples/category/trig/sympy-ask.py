# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# suite examples · category trig · system sympy-ask (2 cases listed)
# 2 case run(s).  Each runs in a fresh copy of its setup's namespace, as in the
# harness, so no variable carries over; an error in one is printed and the rest still run.
# Run: python3 this-file.py

import traceback

def _verdict(answer, expected, stored):
    kind = type(answer).__name__
    got = ("true" if answer is True or kind == "BooleanTrue" else
           "false" if answer is False or kind == "BooleanFalse" else "null")
    outcome = (("declined correctly" if expected == "contingent" else "no verdict") if got == "null" else
               "solved" if got == expected else "wrong" if expected in ("true", "false", "contingent") else "?")
    print(f"verdict: {got} (expected {expected}: {outcome}; {stored})")
    return got


def _run(case, system, expected, stored, setup, code):
    print(f'== {case} · {system} · expected {expected}')
    ns = dict(setup)
    try:
        exec(compile(code, case, 'exec'), ns)
        answer = ns.get('Answer')
    except Exception:
        traceback.print_exc()
        answer = None
    return _verdict(answer, expected, stored)


# setup 1 (the harness's warm-up, version capture and cache clearing left out)
_SETUP1 = {'__name__': '__reproducer__'}
exec(r'''from sympy import *
import sympy
''', _SETUP1)

_n = {'true': 0, 'false': 0, 'null': 0}


# ---- case demo-eq-trig-01 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024429 answered null (no verdict)
_n[_run('demo-eq-trig-01', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024429 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Pow(sin(x), 2) + Pow(cos(x), 2) - 1
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-trig-02 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024429 answered null (no verdict)
_n[_run('demo-eq-trig-02', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024429 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = 2 * sin(x) * cos(x) - sin(2 * x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

print(f"done: {sum(_n.values())} case run(s): {_n['true']} true, {_n['false']} false, {_n['null']} null")
