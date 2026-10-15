# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# suite trig · category periodicity · system sympy-refine (4 cases listed)
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
''', _SETUP1)

_n = {'true': 0, 'false': 0, 'null': 0}


# ---- case trig-period-01 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024452 answered true (solved)
_n[_run('trig-period-01', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024452 answered true (solved)', _SETUP1, r'''z = Symbol('z', complex=True)
Assum = And(Q.complex(z))
Residual = sin(z + 2 * pi) - sin(z)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case trig-period-02 · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024452 answered null (declined correctly)
_n[_run('trig-period-02', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024452 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = cos(x + pi) - cos(x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case trig-period-03 · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024452 answered null (declined correctly)
_n[_run('trig-period-03', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024452 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x))
Residual = cos(x + pi) - cos(x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case trig-shift-01 · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024452 answered null (declined correctly)
_n[_run('trig-shift-01', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024452 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(x + pi) - sin(x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

print(f"done: {sum(_n.values())} case run(s): {_n['true']} true, {_n['false']} false, {_n['null']} null")
