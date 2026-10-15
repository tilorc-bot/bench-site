# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# suite trig · every case · system satrefine-refine (13 cases listed)
# 13 case run(s).  Each runs in a fresh copy of its setup's namespace, as in the
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

_n = {'true': 0, 'false': 0, 'null': 0}


# ---- case trig-acos-01 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-024455 answered null (no verdict)
_n[_run('trig-acos-01', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-024455 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x), x < 3)
Residual = acos(cos(x)) - x
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case trig-asin-01 · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-024455 answered null (declined correctly)
_n[_run('trig-asin-01', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-024455 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = asin(sin(x)) - x
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case trig-asin-02 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-024455 answered null (no verdict)
_n[_run('trig-asin-02', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-024455 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x > -1, x < 1)
Residual = asin(sin(x)) - x
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case trig-atan-01 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-024455 answered null (no verdict)
_n[_run('trig-atan-01', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-024455 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x > -1, x < 1)
Residual = atan(tan(x)) - x
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case trig-double-01 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-024455 answered null (no verdict)
_n[_run('trig-double-01', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-024455 answered null (no verdict)', _SETUP1, r'''z = Symbol('z', complex=True)
Assum = And(Q.complex(z))
Residual = sin(2 * z) - (2 * (sin(z) * cos(z)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case trig-double-02 · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-024455 answered null (no verdict)
_n[_run('trig-double-02', 'satrefine-refine', 'false', 'the run satrefine-refine-20261015-024455 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x), x < 1)
Residual = sin(2 * x) - (2 * sin(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case trig-period-01 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-024455 answered true (solved)
_n[_run('trig-period-01', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-024455 answered true (solved)', _SETUP1, r'''z = Symbol('z', complex=True)
Assum = And(Q.complex(z))
Residual = sin(z + 2 * pi) - sin(z)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case trig-period-02 · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-024455 answered null (declined correctly)
_n[_run('trig-period-02', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-024455 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = cos(x + pi) - cos(x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case trig-period-03 · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-024455 answered null (declined correctly)
_n[_run('trig-period-03', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-024455 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x))
Residual = cos(x + pi) - cos(x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case trig-pyth-01 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-024455 answered null (no verdict)
_n[_run('trig-pyth-01', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-024455 answered null (no verdict)', _SETUP1, r'''z = Symbol('z', complex=True)
Assum = And(Q.complex(z))
Residual = sin(z) * sin(z) + cos(z) * cos(z) - 1
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case trig-shift-01 · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-024455 answered null (declined correctly)
_n[_run('trig-shift-01', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-024455 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(x + pi) - sin(x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case trig-sqrt-01 · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-024455 answered null (declined correctly)
_n[_run('trig-sqrt-01', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-024455 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sqrt(1 - sin(x) * sin(x)) - cos(x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case trig-tan-01 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-024455 answered null (no verdict)
_n[_run('trig-tan-01', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-024455 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(x)))
Residual = tan(x) - (sin(x) / cos(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

print(f"done: {sum(_n.values())} case run(s): {_n['true']} true, {_n['false']} false, {_n['null']} null")
