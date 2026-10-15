# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# suite simplipy · case sp-acj4-395-real · all Python systems
# 4 case run(s).  Each runs in a fresh copy of its setup's namespace, as in the
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
import satrefine
''', _SETUP1)

# setup 2 (the harness's warm-up, version capture and cache clearing left out)
_SETUP2 = {'__name__': '__reproducer__'}
exec(r'''from sympy import *
import sympy
''', _SETUP2)

_n = {'true': 0, 'false': 0, 'null': 0}


# ---- case sp-acj4-395-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174730 answered null (no verdict)
_n[_run('sp-acj4-395-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261014-174730 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-395-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261014-174423 answered null (no verdict)
_n[_run('sp-acj4-395-real', 'sympy-ask', 'true', 'the run sympy-ask-20261014-174423 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-395-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261014-174535 answered null (no verdict)
_n[_run('sp-acj4-395-real', 'sympy-refine', 'true', 'the run sympy-refine-20261014-174535 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-395-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-395-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

print(f"done: {sum(_n.values())} case run(s): {_n['true']} true, {_n['false']} false, {_n['null']} null")
