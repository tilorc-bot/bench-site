# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# suite examples · category branch-cuts · system sympy-ask (5 cases listed)
# 5 case run(s).  Each runs in a fresh copy of its setup's namespace, as in the
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


# ---- case demo-atan2-01 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024429 answered null (no verdict)
_n[_run('demo-atan2-01', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024429 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
y = Symbol('y', real=True)
Assum = And(Q.real(x), Q.real(y), Q.positive(x))
Residual = atan2(y, x) - atan(y / x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case demo-atan2-02 · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024429 answered null (no verdict)
_n[_run('demo-atan2-02', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024429 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
y = Symbol('y', real=True)
Assum = And(Q.real(x), Q.real(y), Q.negative(x), Q.positive(y))
Residual = atan2(y, x) - atan(y / x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case demo-log-01 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024429 answered null (no verdict)
_n[_run('demo-log-01', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024429 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
y = Symbol('y', real=True)
Assum = And(Q.real(x), Q.real(y), Q.positive(x), Q.positive(y))
Residual = log(x * y) - (log(x) + log(y))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case demo-log-02 · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024429 answered null (declined correctly)
_n[_run('demo-log-02', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024429 answered null (declined correctly)', _SETUP1, r'''z = Symbol('z', complex=True)
w = Symbol('w', complex=True)
Assum = And(Q.complex(z), Q.complex(w), ~Q.zero(z), ~Q.zero(w))
Residual = log(z * w) - (log(z) + log(w))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case demo-log-03 · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024429 answered false (solved)
_n[_run('demo-log-03', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024429 answered false (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x))
Residual = log(x) - log(-x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

print(f"done: {sum(_n.values())} case run(s): {_n['true']} true, {_n['false']} false, {_n['null']} null")
