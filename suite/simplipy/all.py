# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# suite simplipy · every case · all Python systems (307 cases listed)
# 1224 case run(s).  Each runs in a fresh copy of its setup's namespace, as in the
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


# ---- case sp-acj4-0-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-0-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = acosh(cosh(x)) - Abs(x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-0-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-0-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = acosh(cosh(x)) - Abs(x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-0-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-0-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = acosh(cosh(x)) - Abs(x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-0-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-0-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Residual = acosh(cosh(x)) - Abs(x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-0-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-0-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = acosh(cosh(x)) - Abs(x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-0-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-0-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = acosh(cosh(x)) - Abs(x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-0-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-0-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = acosh(cosh(x)) - Abs(x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-0-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-0-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = acosh(cosh(x)) - Abs(x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-1-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = asin(Abs(x)) - Abs(asin(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-1-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = asin(Abs(x)) - Abs(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-1-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = asin(Abs(x)) - Abs(asin(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-1-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= 1
Residual = asin(Abs(x)) - Abs(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-1-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = asin(Abs(x)) - Abs(asin(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-1-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = asin(Abs(x)) - Abs(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-1-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = asin(Abs(x)) - Abs(asin(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-1-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = asin(Abs(x)) - Abs(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1007-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-1007-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = 0 / sin(5) - 0
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1007-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-1007-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = 0 / sin(5) - 0
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1007-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-1007-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = 0 / sin(5) - 0
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1007-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1007-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = 0 / sin(5) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-102-complex · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-102-complex', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Abs(x) / 6 - Abs(x / -6)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-102-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-102-complex', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Abs(x) / 6 - Abs(x / -6)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-102-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-102-complex', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Abs(x) / 6 - Abs(x / -6)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-102-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-102-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Residual = Abs(x) / 6 - Abs(x / -6)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-102-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-102-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Abs(x) / 6 - Abs(x / -6)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-102-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-102-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Abs(x) / 6 - Abs(x / -6)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-102-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-102-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Abs(x) / 6 - Abs(x / -6)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-102-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-102-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = Abs(x) / 6 - Abs(x / -6)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-108-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-108-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(Abs(x)))
Residual = Abs(x) / x - (x / Abs(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-108-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-108-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(Abs(x)))
Residual = Abs(x) / x - (x / Abs(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-108-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-108-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(Abs(x)))
Residual = Abs(x) / x - (x / Abs(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-108-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-108-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = Abs(x) / x - (x / Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-108-condf · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-108-condf', 'satrefine-refine', 'false', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), ~Q.zero(Abs(x)))
Residual = Abs(x) / x - (x / Abs(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-108-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-108-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), ~Q.zero(Abs(x)))
Residual = Abs(x) / x - (x / Abs(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-108-condf · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-108-condf', 'sympy-refine', 'false', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), ~Q.zero(Abs(x)))
Residual = Abs(x) / x - (x / Abs(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-108-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-108-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = Abs(x) / x - (x / Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-108-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-108-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Abs(x)))
Residual = Abs(x) / x - (x / Abs(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-108-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-108-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Abs(x)))
Residual = Abs(x) / x - (x / Abs(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-108-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-108-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Abs(x)))
Residual = Abs(x) / x - (x / Abs(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-108-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-108-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = Abs(x) / x - (x / Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1107-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-1107-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = asin(sin(Integer(1) / 10)) - Rational(1, 10)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1107-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-1107-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = asin(sin(Integer(1) / 10)) - Rational(1, 10)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1107-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-1107-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = asin(sin(Integer(1) / 10)) - Rational(1, 10)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1107-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1107-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = asin(sin(Integer(1) / 10)) - Rational(1, 10)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1148-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-1148-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''Assum = And()
Residual = cosh(log(Integer(1) / 4)) - Rational(17, 8)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1148-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-1148-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''Assum = And()
Residual = cosh(log(Integer(1) / 4)) - Rational(17, 8)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1148-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-1148-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''Assum = And()
Residual = cosh(log(Integer(1) / 4)) - Rational(17, 8)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1148-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1148-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = cosh(log(Integer(1) / 4)) - Rational(17, 8)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1149-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-1149-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = exp(Abs(log(2))) - 2
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1149-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-1149-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = exp(Abs(log(2))) - 2
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1149-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-1149-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = exp(Abs(log(2))) - 2
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1149-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1149-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = exp(Abs(log(2))) - 2
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-115-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-115-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -4)))
Residual = log(x) / -4 - log(real_root(x, -4))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-115-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-115-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -4)))
Residual = log(x) / -4 - log(real_root(x, -4))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-115-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-115-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -4)))
Residual = log(x) / -4 - log(real_root(x, -4))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-115-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-115-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): x > 0
# dropped (not a unary fact about one symbol): ~Q.zero(real_root(x, -4))
Residual = log(x) / -4 - log(real_root(x, -4))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-116-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-116-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -6)))
Residual = log(x) / -6 - log(real_root(x, -6))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-116-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-116-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -6)))
Residual = log(x) / -6 - log(real_root(x, -6))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-116-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-116-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -6)))
Residual = log(x) / -6 - log(real_root(x, -6))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-116-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-116-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): x > 0
# dropped (not a unary fact about one symbol): ~Q.zero(real_root(x, -6))
Residual = log(x) / -6 - log(real_root(x, -6))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1177-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-1177-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = Pow(0, asinh(10)) - 0
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1177-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-1177-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = Pow(0, asinh(10)) - 0
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1177-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-1177-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = Pow(0, asinh(10)) - 0
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1177-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1177-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = Pow(0, asinh(10)) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1195-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-1195-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = Pow(0, atan(7)) - 0
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1195-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-1195-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = Pow(0, atan(7)) - 0
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1195-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-1195-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = Pow(0, atan(7)) - 0
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1195-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1195-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = Pow(0, atan(7)) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-120-complex · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-120-complex', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = pi / Abs(x) - Abs(pi / x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-120-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-120-complex', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = pi / Abs(x) - Abs(pi / x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-120-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-120-complex', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = pi / Abs(x) - Abs(pi / x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-120-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-120-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = pi / Abs(x) - Abs(pi / x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-120-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-120-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = pi / Abs(x) - Abs(pi / x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-120-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-120-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = pi / Abs(x) - Abs(pi / x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-120-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-120-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = pi / Abs(x) - Abs(pi / x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-120-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-120-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = pi / Abs(x) - Abs(pi / x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1217-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-1217-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = Pow(0, exp(-1)) - 0
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1217-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-1217-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = Pow(0, exp(-1)) - 0
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1217-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-1217-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = Pow(0, exp(-1)) - 0
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1217-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1217-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = Pow(0, exp(-1)) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1238-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-1238-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = Pow(0, 1 / pi) - 0
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1238-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-1238-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = Pow(0, 1 / pi) - 0
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1238-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-1238-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = Pow(0, 1 / pi) - 0
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1238-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1238-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = Pow(0, 1 / pi) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-124-condf · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-124-condf', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)))
Residual = Abs(asin(tanh(x))) - acos(1 / cosh(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-124-condf · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-124-condf', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)))
Residual = Abs(asin(tanh(x))) - acos(1 / cosh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-124-condf · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-124-condf', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)))
Residual = Abs(asin(tanh(x))) - acos(1 / cosh(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-124-condf · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-124-condf', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = Abs(asin(tanh(x))) - acos(1 / cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1247-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-1247-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = Pow(0, log(9)) - 0
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1247-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-1247-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = Pow(0, log(9)) - 0
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1247-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-1247-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = Pow(0, log(9)) - 0
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1247-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1247-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = Pow(0, log(9)) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1254-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-1254-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = Pow(0, sin(2)) - 0
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1254-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-1254-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = Pow(0, sin(2)) - 0
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1254-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-1254-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = Pow(0, sin(2)) - 0
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1254-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1254-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = Pow(0, sin(2)) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1258-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-1258-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = Pow(0, sin(9)) - 0
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1258-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-1258-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = Pow(0, sin(9)) - 0
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1258-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-1258-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = Pow(0, sin(9)) - 0
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1258-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1258-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = Pow(0, sin(9)) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-127-condf · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-127-condf', 'satrefine-refine', 'false', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, Ne(exp(x), 1, evaluate=False), Ne(exp(x), -1, evaluate=False))
Residual = Abs(atanh(exp(x))) - atanh(exp(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-127-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-127-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, Ne(exp(x), 1, evaluate=False), Ne(exp(x), -1, evaluate=False))
Residual = Abs(atanh(exp(x))) - atanh(exp(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-127-condf · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-127-condf', 'sympy-refine', 'false', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, Ne(exp(x), 1, evaluate=False), Ne(exp(x), -1, evaluate=False))
Residual = Abs(atanh(exp(x))) - atanh(exp(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-127-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-127-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): re(x) >= 0
# dropped (not a unary fact about one symbol): Ne(exp(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(exp(x), -1, evaluate=False)
Residual = Abs(atanh(exp(x))) - atanh(exp(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-127-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-127-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(exp(x), 1, evaluate=False), Ne(exp(x), -1, evaluate=False))
Residual = Abs(atanh(exp(x))) - atanh(exp(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-127-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-127-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(exp(x), 1, evaluate=False), Ne(exp(x), -1, evaluate=False))
Residual = Abs(atanh(exp(x))) - atanh(exp(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-127-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-127-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(exp(x), 1, evaluate=False), Ne(exp(x), -1, evaluate=False))
Residual = Abs(atanh(exp(x))) - atanh(exp(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-127-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-127-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(exp(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(exp(x), -1, evaluate=False)
Residual = Abs(atanh(exp(x))) - atanh(exp(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-128-cond2 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-128-cond2', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = Abs(cos(asin(x))) - cos(asin(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-128-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-128-cond2', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = Abs(cos(asin(x))) - cos(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-128-cond2 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-128-cond2', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = Abs(cos(asin(x))) - cos(asin(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-128-cond2 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-128-cond2', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= 1
Residual = Abs(cos(asin(x))) - cos(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-128-condf · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-128-condf', 'satrefine-refine', 'false', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x > 1)
Residual = Abs(cos(asin(x))) - cos(asin(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-128-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-128-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x > 1)
Residual = Abs(cos(asin(x))) - cos(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-128-condf · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-128-condf', 'sympy-refine', 'false', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x > 1)
Residual = Abs(cos(asin(x))) - cos(asin(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-128-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-128-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): x > 1
Residual = Abs(cos(asin(x))) - cos(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-128-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-128-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Abs(cos(asin(x))) - cos(asin(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-128-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-128-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Abs(cos(asin(x))) - cos(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-128-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-128-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Abs(cos(asin(x))) - cos(asin(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-128-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-128-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = Abs(cos(asin(x))) - cos(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-129-cond · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-129-cond', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False))
Residual = Abs(cos(atan(x))) - cos(atan(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-129-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-129-cond', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False))
Residual = Abs(cos(atan(x))) - cos(atan(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-129-cond · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-129-cond', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False))
Residual = Abs(cos(atan(x))) - cos(atan(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-129-cond · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-129-cond', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True)
# dropped (not a unary fact about one symbol): Ne(x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -I, evaluate=False)
Residual = Abs(cos(atan(x))) - cos(atan(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-130-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-130-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = Abs(log(cos(x))) - log(1 / cos(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-130-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-130-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = Abs(log(cos(x))) - log(1 / cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-130-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-130-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = Abs(log(cos(x))) - log(1 / cos(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-130-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-130-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cos(x))
Residual = Abs(log(cos(x))) - log(1 / cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-130-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-130-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < pi / 2, ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = Abs(log(cos(x))) - log(1 / cos(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-130-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-130-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < pi / 2, ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = Abs(log(cos(x))) - log(1 / cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-130-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-130-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < pi / 2, ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = Abs(log(cos(x))) - log(1 / cos(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-130-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-130-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) < pi / 2
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cos(x))
Residual = Abs(log(cos(x))) - log(1 / cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-130-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-130-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = Abs(log(cos(x))) - log(1 / cos(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-130-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-130-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = Abs(log(cos(x))) - log(1 / cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-130-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-130-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = Abs(log(cos(x))) - log(1 / cos(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-130-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-130-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cos(x))
Residual = Abs(log(cos(x))) - log(1 / cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-131-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-131-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
Residual = Abs(log(cosh(x))) - log(cosh(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-131-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-131-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
Residual = Abs(log(cosh(x))) - log(cosh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-131-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-131-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
Residual = Abs(log(cosh(x))) - log(cosh(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-131-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-131-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = Abs(log(cosh(x))) - log(cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-131-condf · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-131-condf', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)))
Residual = Abs(log(cosh(x))) - log(cosh(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-131-condf · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-131-condf', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)))
Residual = Abs(log(cosh(x))) - log(cosh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-131-condf · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-131-condf', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)))
Residual = Abs(log(cosh(x))) - log(cosh(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-131-condf · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-131-condf', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = Abs(log(cosh(x))) - log(cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-131-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-131-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cosh(x)))
Residual = Abs(log(cosh(x))) - log(cosh(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-131-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-131-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cosh(x)))
Residual = Abs(log(cosh(x))) - log(cosh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-131-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-131-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cosh(x)))
Residual = Abs(log(cosh(x))) - log(cosh(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-131-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-131-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = Abs(log(cosh(x))) - log(cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-132-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-132-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(sin(x)))
Residual = Abs(log(sin(x))) - (-log(sin(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-132-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-132-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(sin(x)))
Residual = Abs(log(sin(x))) - (-log(sin(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-132-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-132-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(sin(x)))
Residual = Abs(log(sin(x))) - (-log(sin(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-132-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-132-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(sin(x))
Residual = Abs(log(sin(x))) - (-log(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-132-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-132-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x >= 0, x <= pi, ~Q.zero(sin(x)))
Residual = Abs(log(sin(x))) - (-log(sin(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-132-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-132-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x >= 0, x <= pi, ~Q.zero(sin(x)))
Residual = Abs(log(sin(x))) - (-log(sin(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-132-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-132-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x >= 0, x <= pi, ~Q.zero(sin(x)))
Residual = Abs(log(sin(x))) - (-log(sin(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-132-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-132-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): x >= 0
# dropped (not a unary fact about one symbol): x <= pi
# dropped (not a unary fact about one symbol): ~Q.zero(sin(x))
Residual = Abs(log(sin(x))) - (-log(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-132-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-132-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(sin(x)))
Residual = Abs(log(sin(x))) - (-log(sin(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-132-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-132-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(sin(x)))
Residual = Abs(log(sin(x))) - (-log(sin(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-132-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-132-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(sin(x)))
Residual = Abs(log(sin(x))) - (-log(sin(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-132-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-132-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(sin(x))
Residual = Abs(log(sin(x))) - (-log(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-133-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-133-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(tanh(x)))
Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-133-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-133-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(tanh(x)))
Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-133-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-133-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(tanh(x)))
Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-133-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-133-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(tanh(x))
Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-133-condf · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-133-condf', 'satrefine-refine', 'false', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)), ~Q.zero(tanh(x)))
Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-133-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-133-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)), ~Q.zero(tanh(x)))
Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-133-condf · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-133-condf', 'sympy-refine', 'false', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)), ~Q.zero(tanh(x)))
Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-133-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-133-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(tanh(x))
Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-133-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-133-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(tanh(x)))
Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-133-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-133-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(tanh(x)))
Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-133-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-133-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(tanh(x)))
Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-133-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-133-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(tanh(x))
Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-136-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-136-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.nonnegative(x), Or(~Q.zero(x), re(exp(1)) > 0))
Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-136-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-136-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.nonnegative(x), Or(~Q.zero(x), re(exp(1)) > 0))
Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-136-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-136-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.nonnegative(x), Or(~Q.zero(x), re(exp(1)) > 0))
Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-136-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-136-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True, nonnegative=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(exp(1)) > 0)
Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-136-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-136-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(exp(1)) > 0))
Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-136-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-136-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(exp(1)) > 0))
Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-136-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-136-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(exp(1)) > 0))
Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-136-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-136-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(exp(1)) > 0)
Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-137-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-137-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Or(~Q.zero(x), re(pi) > 0))
Residual = Abs(Pow(x, pi)) - Pow(x, pi)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-137-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-137-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Or(~Q.zero(x), re(pi) > 0))
Residual = Abs(Pow(x, pi)) - Pow(x, pi)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-137-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-137-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Or(~Q.zero(x), re(pi) > 0))
Residual = Abs(Pow(x, pi)) - Pow(x, pi)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-137-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-137-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
Residual = Abs(Pow(x, pi)) - Pow(x, pi)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-137-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-137-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.nonnegative(x), Or(~Q.zero(x), re(pi) > 0))
Residual = Abs(Pow(x, pi)) - Pow(x, pi)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-137-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-137-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.nonnegative(x), Or(~Q.zero(x), re(pi) > 0))
Residual = Abs(Pow(x, pi)) - Pow(x, pi)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-137-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-137-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.nonnegative(x), Or(~Q.zero(x), re(pi) > 0))
Residual = Abs(Pow(x, pi)) - Pow(x, pi)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-137-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-137-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True, nonnegative=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
Residual = Abs(Pow(x, pi)) - Pow(x, pi)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-137-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-137-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0))
Residual = Abs(Pow(x, pi)) - Pow(x, pi)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-137-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-137-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0))
Residual = Abs(Pow(x, pi)) - Pow(x, pi)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-137-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-137-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0))
Residual = Abs(Pow(x, pi)) - Pow(x, pi)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-137-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-137-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
Residual = Abs(Pow(x, pi)) - Pow(x, pi)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-14-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-14-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = -sin(x) - sin(-x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-14-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-14-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = -sin(x) - sin(-x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-14-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-14-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = -sin(x) - sin(-x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-14-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-14-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = -sin(x) - sin(-x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-145-cond2 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-145-cond2', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = Abs(sin(acos(x))) - cos(asin(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-145-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-145-cond2', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = Abs(sin(acos(x))) - cos(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-145-cond2 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-145-cond2', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = Abs(sin(acos(x))) - cos(asin(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-145-cond2 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-145-cond2', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= 1
Residual = Abs(sin(acos(x))) - cos(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-145-condf · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-145-condf', 'satrefine-refine', 'false', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x > 1)
Residual = Abs(sin(acos(x))) - cos(asin(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-145-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-145-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x > 1)
Residual = Abs(sin(acos(x))) - cos(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-145-condf · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-145-condf', 'sympy-refine', 'false', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x > 1)
Residual = Abs(sin(acos(x))) - cos(asin(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-145-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-145-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): x > 1
Residual = Abs(sin(acos(x))) - cos(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-145-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-145-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Abs(sin(acos(x))) - cos(asin(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-145-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-145-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Abs(sin(acos(x))) - cos(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-145-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-145-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Abs(sin(acos(x))) - cos(asin(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-145-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-145-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = Abs(sin(acos(x))) - cos(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-147-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-147-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(asinh(x))), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-147-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-147-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(asinh(x))), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-147-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-147-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(asinh(x))), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-147-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-147-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(asinh(x)))
# dropped (not a unary fact about one symbol): Ne(1 / x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, -I, evaluate=False)
Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-147-cond · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-147-cond', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(asinh(x))), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-147-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-147-cond', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(asinh(x))), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-147-cond · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-147-cond', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(asinh(x))), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-147-cond · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-147-cond', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(asinh(x)))
# dropped (not a unary fact about one symbol): Ne(1 / x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, -I, evaluate=False)
Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-151-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-151-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = acos(cos(asin(x))) - Abs(asin(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-151-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-151-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = acos(cos(asin(x))) - Abs(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-151-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-151-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = acos(cos(asin(x))) - Abs(asin(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-151-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-151-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Residual = acos(cos(asin(x))) - Abs(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-151-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-151-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = acos(cos(asin(x))) - Abs(asin(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-151-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-151-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = acos(cos(asin(x))) - Abs(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-151-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-151-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = acos(cos(asin(x))) - Abs(asin(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-151-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-151-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= 1
Residual = acos(cos(asin(x))) - Abs(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-151-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-151-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = acos(cos(asin(x))) - Abs(asin(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-151-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-151-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = acos(cos(asin(x))) - Abs(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-151-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-151-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = acos(cos(asin(x))) - Abs(asin(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-151-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-151-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = acos(cos(asin(x))) - Abs(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-153-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-153-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = acos(cos(cos(x))) - Abs(cos(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-153-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-153-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = acos(cos(cos(x))) - Abs(cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-153-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-153-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = acos(cos(cos(x))) - Abs(cos(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-153-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-153-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Residual = acos(cos(cos(x))) - Abs(cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-154-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-154-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = acos(cos(sin(x))) - Abs(sin(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-154-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-154-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = acos(cos(sin(x))) - Abs(sin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-154-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-154-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = acos(cos(sin(x))) - Abs(sin(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-154-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-154-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Residual = acos(cos(sin(x))) - Abs(sin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-154-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-154-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = acos(cos(sin(x))) - Abs(sin(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-154-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-154-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = acos(cos(sin(x))) - Abs(sin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-154-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-154-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = acos(cos(sin(x))) - Abs(sin(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-154-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-154-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = acos(cos(sin(x))) - Abs(sin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-156-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-156-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = acos(sin(acos(x))) - Abs(asin(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-156-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-156-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = acos(sin(acos(x))) - Abs(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-156-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-156-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = acos(sin(acos(x))) - Abs(asin(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-156-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-156-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= 1
Residual = acos(sin(acos(x))) - Abs(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-156-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-156-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = acos(sin(acos(x))) - Abs(asin(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-156-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-156-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = acos(sin(acos(x))) - Abs(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-156-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-156-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = acos(sin(acos(x))) - Abs(asin(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-156-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-156-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = acos(sin(acos(x))) - Abs(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-159-cond2 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-159-cond2', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x <= 1, ~Q.zero(cosh(x)))
Residual = acos(tanh(Abs(x))) - asin(1 / cosh(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-159-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-159-cond2', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x <= 1, ~Q.zero(cosh(x)))
Residual = acos(tanh(Abs(x))) - asin(1 / cosh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-159-cond2 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-159-cond2', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x <= 1, ~Q.zero(cosh(x)))
Residual = acos(tanh(Abs(x))) - asin(1 / cosh(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-159-cond2 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-159-cond2', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): x <= 1
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = acos(tanh(Abs(x))) - asin(1 / cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-159-cond3 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-159-cond3', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= pi / 2, ~Q.zero(cosh(x)))
Residual = acos(tanh(Abs(x))) - asin(1 / cosh(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-159-cond3 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-159-cond3', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= pi / 2, ~Q.zero(cosh(x)))
Residual = acos(tanh(Abs(x))) - asin(1 / cosh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-159-cond3 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-159-cond3', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= pi / 2, ~Q.zero(cosh(x)))
Residual = acos(tanh(Abs(x))) - asin(1 / cosh(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-159-cond3 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-159-cond3', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= pi / 2
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = acos(tanh(Abs(x))) - asin(1 / cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-162-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-162-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, Q.real(x))
Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-162-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-162-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, Q.real(x))
Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-162-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-162-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, Q.real(x))
Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-162-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-162-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, real=True)
# dropped (not a unary fact about one symbol): re(x) >= 0
Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-162-condf · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-162-condf', 'satrefine-refine', 'false', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x))
Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-162-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-162-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x))
Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-162-condf · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-162-condf', 'sympy-refine', 'false', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x))
Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-162-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-162-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True, negative=True)
Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-162-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-162-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-162-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-162-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-162-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-162-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-162-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-162-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-165-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-165-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = asin(cos(atan(x))) - Abs(atan(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-165-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-165-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = asin(cos(atan(x))) - Abs(atan(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-165-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-165-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = asin(cos(atan(x))) - Abs(atan(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-165-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-165-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, -I, evaluate=False)
Residual = asin(cos(atan(x))) - Abs(atan(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-171-cond · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-171-cond', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Abs(im(x)) < pi, ~Q.zero(cosh(x)))
Residual = asin(sin(tanh(x))) - tanh(x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-171-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-171-cond', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Abs(im(x)) < pi, ~Q.zero(cosh(x)))
Residual = asin(sin(tanh(x))) - tanh(x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-171-cond · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-171-cond', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Abs(im(x)) < pi, ~Q.zero(cosh(x)))
Residual = asin(sin(tanh(x))) - tanh(x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-171-cond · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-171-cond', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Abs(im(x)) < pi
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = asin(sin(tanh(x))) - tanh(x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-171-cond2 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-171-cond2', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)))
Residual = asin(sin(tanh(x))) - tanh(x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-171-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-171-cond2', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)))
Residual = asin(sin(tanh(x))) - tanh(x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-171-cond2 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-171-cond2', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)))
Residual = asin(sin(tanh(x))) - tanh(x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-171-cond2 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-171-cond2', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = asin(sin(tanh(x))) - tanh(x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-173-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-173-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
Residual = asin(tanh(Abs(x))) - acos(1 / cosh(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-173-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-173-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
Residual = asin(tanh(Abs(x))) - acos(1 / cosh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-173-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-173-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
Residual = asin(tanh(Abs(x))) - acos(1 / cosh(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-173-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-173-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = asin(tanh(Abs(x))) - acos(1 / cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-176-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-176-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
Residual = atan(Abs(sinh(x))) - acos(1 / cosh(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-176-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-176-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
Residual = atan(Abs(sinh(x))) - acos(1 / cosh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-176-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-176-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
Residual = atan(Abs(sinh(x))) - acos(1 / cosh(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-176-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-176-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = atan(Abs(sinh(x))) - acos(1 / cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-177-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-177-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cos(x)))
Residual = atan(Abs(tan(x))) - Abs(asin(sin(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-177-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-177-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cos(x)))
Residual = atan(Abs(tan(x))) - Abs(asin(sin(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-177-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-177-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cos(x)))
Residual = atan(Abs(tan(x))) - Abs(asin(sin(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-177-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-177-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
Residual = atan(Abs(tan(x))) - Abs(asin(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-179-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-179-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= pi / 2, Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-179-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-179-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= pi / 2, Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-179-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-179-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= pi / 2, Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-179-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-179-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= pi / 2
# dropped (not a unary fact about one symbol): Ne(sinh(acos(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(acos(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(acos(x)))
Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-179-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-179-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-179-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-179-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-179-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-179-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-179-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-179-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(sinh(acos(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(acos(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(acos(x)))
Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-180-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-180-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-180-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-180-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-180-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-180-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-180-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-180-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Ne(sinh(acosh(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(acosh(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(acosh(x)))
Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-180-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-180-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-180-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-180-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-180-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-180-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-180-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-180-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): re(x) > 0
# dropped (not a unary fact about one symbol): Ne(sinh(acosh(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(acosh(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(acosh(x)))
Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-180-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-180-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-180-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-180-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-180-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-180-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-180-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-180-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(sinh(acosh(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(acosh(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(acosh(x)))
Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-181-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-181-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= pi / 2, Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-181-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-181-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= pi / 2, Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-181-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-181-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= pi / 2, Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-181-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-181-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= pi / 2
# dropped (not a unary fact about one symbol): Ne(sinh(asin(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(asin(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(asin(x)))
Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-181-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-181-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-181-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-181-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-181-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-181-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-181-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-181-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(sinh(asin(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(asin(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(asin(x)))
Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-183-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-183-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-183-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-183-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-183-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-183-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-183-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-183-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(sinh(log(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(log(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(log(x)))
Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-183-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-183-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-183-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-183-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-183-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-183-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-183-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-183-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): re(x) > 0
# dropped (not a unary fact about one symbol): Ne(sinh(log(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(log(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(log(x)))
Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-183-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-183-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-183-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-183-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-183-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-183-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-183-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-183-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(sinh(log(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(log(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(log(x)))
Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-185-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-185-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(cos(x))), Ne(tan(cos(x)), I, evaluate=False), Ne(tan(cos(x)), -I, evaluate=False))
Residual = atan(tan(cos(x))) - cos(x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-185-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-185-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(cos(x))), Ne(tan(cos(x)), I, evaluate=False), Ne(tan(cos(x)), -I, evaluate=False))
Residual = atan(tan(cos(x))) - cos(x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-185-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-185-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(cos(x))), Ne(tan(cos(x)), I, evaluate=False), Ne(tan(cos(x)), -I, evaluate=False))
Residual = atan(tan(cos(x))) - cos(x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-185-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-185-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(cos(x)))
# dropped (not a unary fact about one symbol): Ne(tan(cos(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(tan(cos(x)), -I, evaluate=False)
Residual = atan(tan(cos(x))) - cos(x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-186-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-186-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cos(sin(x))), Ne(tan(sin(x)), I, evaluate=False), Ne(tan(sin(x)), -I, evaluate=False))
Residual = atan(tan(sin(x))) - sin(x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-186-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-186-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cos(sin(x))), Ne(tan(sin(x)), I, evaluate=False), Ne(tan(sin(x)), -I, evaluate=False))
Residual = atan(tan(sin(x))) - sin(x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-186-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-186-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cos(sin(x))), Ne(tan(sin(x)), I, evaluate=False), Ne(tan(sin(x)), -I, evaluate=False))
Residual = atan(tan(sin(x))) - sin(x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-186-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-186-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(sin(x)))
# dropped (not a unary fact about one symbol): Ne(tan(sin(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(tan(sin(x)), -I, evaluate=False)
Residual = atan(tan(sin(x))) - sin(x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-187-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-187-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)), ~Q.zero(cos(tanh(x))), Ne(tan(tanh(x)), I, evaluate=False), Ne(tan(tanh(x)), -I, evaluate=False))
Residual = atan(tan(tanh(x))) - tanh(x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-187-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-187-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)), ~Q.zero(cos(tanh(x))), Ne(tan(tanh(x)), I, evaluate=False), Ne(tan(tanh(x)), -I, evaluate=False))
Residual = atan(tan(tanh(x))) - tanh(x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-187-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-187-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)), ~Q.zero(cos(tanh(x))), Ne(tan(tanh(x)), I, evaluate=False), Ne(tan(tanh(x)), -I, evaluate=False))
Residual = atan(tan(tanh(x))) - tanh(x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-187-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-187-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(x)))
# dropped (not a unary fact about one symbol): Ne(tan(tanh(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(tan(tanh(x)), -I, evaluate=False)
Residual = atan(tan(tanh(x))) - tanh(x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-189-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-189-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-189-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-189-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-189-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-189-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-189-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-189-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(cos(asin(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(cos(asin(x)), -1, evaluate=False)
Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-189-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-189-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-189-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-189-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-189-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-189-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-189-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-189-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(cos(asin(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(cos(asin(x)), -1, evaluate=False)
Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-190-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-190-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-190-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-190-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-190-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-190-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-190-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-190-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(cos(atan(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(cos(atan(x)), -1, evaluate=False)
Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-190-condf · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-190-condf', 'satrefine-refine', 'false', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-190-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-190-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-190-condf · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-190-condf', 'sympy-refine', 'false', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-190-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-190-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(cos(atan(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(cos(atan(x)), -1, evaluate=False)
Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-190-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-190-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-190-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-190-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-190-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-190-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-190-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-190-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(cos(atan(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(cos(atan(x)), -1, evaluate=False)
Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-191-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-191-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-191-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-191-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-191-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-191-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-191-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-191-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(sin(acos(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(acos(x)), -1, evaluate=False)
Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-191-condf · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-191-condf', 'satrefine-refine', 'false', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-191-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-191-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-191-condf · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-191-condf', 'sympy-refine', 'false', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-191-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-191-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(sin(acos(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(acos(x)), -1, evaluate=False)
Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-191-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-191-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-191-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-191-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-191-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-191-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-191-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-191-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(sin(acos(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(acos(x)), -1, evaluate=False)
Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-194-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-194-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sin(cos(x)), 1, evaluate=False), Ne(sin(cos(x)), -1, evaluate=False), ~Q.zero(cos(cos(x))))
Residual = atanh(sin(cos(x))) - asinh(tan(cos(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-194-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-194-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sin(cos(x)), 1, evaluate=False), Ne(sin(cos(x)), -1, evaluate=False), ~Q.zero(cos(cos(x))))
Residual = atanh(sin(cos(x))) - asinh(tan(cos(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-194-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-194-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sin(cos(x)), 1, evaluate=False), Ne(sin(cos(x)), -1, evaluate=False), ~Q.zero(cos(cos(x))))
Residual = atanh(sin(cos(x))) - asinh(tan(cos(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-194-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-194-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(sin(cos(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(cos(x)), -1, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(cos(x)))
Residual = atanh(sin(cos(x))) - asinh(tan(cos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-195-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-195-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sin(sin(x)), 1, evaluate=False), Ne(sin(sin(x)), -1, evaluate=False), ~Q.zero(cos(sin(x))))
Residual = atanh(sin(sin(x))) - asinh(tan(sin(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-195-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-195-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sin(sin(x)), 1, evaluate=False), Ne(sin(sin(x)), -1, evaluate=False), ~Q.zero(cos(sin(x))))
Residual = atanh(sin(sin(x))) - asinh(tan(sin(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-195-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-195-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sin(sin(x)), 1, evaluate=False), Ne(sin(sin(x)), -1, evaluate=False), ~Q.zero(cos(sin(x))))
Residual = atanh(sin(sin(x))) - asinh(tan(sin(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-195-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-195-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(sin(sin(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(sin(x)), -1, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(sin(x)))
Residual = atanh(sin(sin(x))) - asinh(tan(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-196-cond2 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-196-cond2', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-196-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-196-cond2', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-196-cond2 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-196-cond2', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-196-cond2 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-196-cond2', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): Ne(sin(tanh(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(tanh(x)), -1, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(x)))
Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-196-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-196-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-196-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-196-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-196-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-196-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-196-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-196-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(sin(tanh(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(tanh(x)), -1, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(x)))
Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-20-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-20-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = sinh(Abs(x)) - Abs(sinh(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-20-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-20-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = sinh(Abs(x)) - Abs(sinh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-20-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-20-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = sinh(Abs(x)) - Abs(sinh(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-20-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-20-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Residual = sinh(Abs(x)) - Abs(sinh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-20-condf · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-20-condf', 'satrefine-refine', 'false', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = sinh(Abs(x)) - Abs(sinh(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-20-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-20-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = sinh(Abs(x)) - Abs(sinh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-20-condf · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-20-condf', 'sympy-refine', 'false', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = sinh(Abs(x)) - Abs(sinh(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-20-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-20-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True)
Residual = sinh(Abs(x)) - Abs(sinh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-200-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-200-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = cos(asin(sin(x))) - Abs(cos(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-200-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-200-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = cos(asin(sin(x))) - Abs(cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-200-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-200-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = cos(asin(sin(x))) - Abs(cos(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-200-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-200-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True)
Residual = cos(asin(sin(x))) - Abs(cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-202-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-202-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cos(x)), Ne(tan(x), I, evaluate=False), Ne(tan(x), -I, evaluate=False))
Residual = cos(atan(tan(x))) - Abs(cos(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-202-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-202-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cos(x)), Ne(tan(x), I, evaluate=False), Ne(tan(x), -I, evaluate=False))
Residual = cos(atan(tan(x))) - Abs(cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-202-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-202-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cos(x)), Ne(tan(x), I, evaluate=False), Ne(tan(x), -I, evaluate=False))
Residual = cos(atan(tan(x))) - Abs(cos(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-202-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-202-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): Ne(tan(x), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(tan(x), -I, evaluate=False)
Residual = cos(atan(tan(x))) - Abs(cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-203-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-203-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = cos(log(1 / x)) - cos(log(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-203-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-203-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = cos(log(1 / x)) - cos(log(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-203-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-203-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = cos(log(1 / x)) - cos(log(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-203-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-203-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = cos(log(1 / x)) - cos(log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-203-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-203-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(1 / x))
Residual = cos(log(1 / x)) - cos(log(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-203-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-203-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(1 / x))
Residual = cos(log(1 / x)) - cos(log(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-203-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-203-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(1 / x))
Residual = cos(log(1 / x)) - cos(log(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-203-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-203-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): re(x) >= 0
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = cos(log(1 / x)) - cos(log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-203-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-203-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = cos(log(1 / x)) - cos(log(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-203-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-203-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = cos(log(1 / x)) - cos(log(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-203-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-203-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = cos(log(1 / x)) - cos(log(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-203-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-203-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = cos(log(1 / x)) - cos(log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-205-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-205-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cos(x)))
Residual = cosh(asinh(tan(x))) - Abs(1 / cos(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-205-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-205-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cos(x)))
Residual = cosh(asinh(tan(x))) - Abs(1 / cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-205-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-205-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cos(x)))
Residual = cosh(asinh(tan(x))) - Abs(1 / cos(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-205-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-205-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
Residual = cosh(asinh(tan(x))) - Abs(1 / cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-213-complex · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-213-complex', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-10 / x))
Residual = 1 / (-10 / x) - (x / -10)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-213-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-213-complex', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-10 / x))
Residual = 1 / (-10 / x) - (x / -10)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-213-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-213-complex', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-10 / x))
Residual = 1 / (-10 / x) - (x / -10)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-213-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-213-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(-10 / x)
Residual = 1 / (-10 / x) - (x / -10)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-216-complex · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-216-complex', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-4 / x))
Residual = 1 / (-4 / x) - (x / -4)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-216-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-216-complex', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-4 / x))
Residual = 1 / (-4 / x) - (x / -4)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-216-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-216-complex', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-4 / x))
Residual = 1 / (-4 / x) - (x / -4)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-216-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-216-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(-4 / x)
Residual = 1 / (-4 / x) - (x / -4)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-218-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-218-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-6 / x))
Residual = 1 / (-6 / x) - (x / -6)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-218-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-218-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-6 / x))
Residual = 1 / (-6 / x) - (x / -6)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-218-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-218-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-6 / x))
Residual = 1 / (-6 / x) - (x / -6)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-218-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-218-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(-6 / x)
Residual = 1 / (-6 / x) - (x / -6)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-22-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-22-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
Residual = tanh(Abs(x)) - Abs(tanh(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-22-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-22-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
Residual = tanh(Abs(x)) - Abs(tanh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-22-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-22-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
Residual = tanh(Abs(x)) - Abs(tanh(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-22-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-22-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = tanh(Abs(x)) - Abs(tanh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-22-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-22-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = tanh(Abs(x)) - Abs(tanh(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-22-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-22-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = tanh(Abs(x)) - Abs(tanh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-22-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-22-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = tanh(Abs(x)) - Abs(tanh(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-22-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-22-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = tanh(Abs(x)) - Abs(tanh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-220-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-220-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-8 / x))
Residual = 1 / (-8 / x) - (x / -8)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-220-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-220-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-8 / x))
Residual = 1 / (-8 / x) - (x / -8)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-220-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-220-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-8 / x))
Residual = 1 / (-8 / x) - (x / -8)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-220-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-220-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(-8 / x)
Residual = 1 / (-8 / x) - (x / -8)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-229-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-229-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Pow(pi, x)))
Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-229-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-229-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Pow(pi, x)))
Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-229-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-229-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Pow(pi, x)))
Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-229-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-229-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(pi, x))
Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-233-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-233-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)), Or(~Q.zero(x), re(-pi) > 0))
Residual = 1 / Pow(x, pi) - Pow(x, -pi)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-233-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-233-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)), Or(~Q.zero(x), re(-pi) > 0))
Residual = 1 / Pow(x, pi) - Pow(x, -pi)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-233-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-233-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)), Or(~Q.zero(x), re(-pi) > 0))
Residual = 1 / Pow(x, pi) - Pow(x, -pi)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-233-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-233-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, pi))
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(-pi) > 0)
Residual = 1 / Pow(x, pi) - Pow(x, -pi)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-234-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-234-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-234-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-234-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, x))
# dropped (not a unary fact about one symbol): Or(~Q.zero(1 / x), re(x) > 0)
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-234-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-234-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-234-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-234-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): re(x) >= 0
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, x))
# dropped (not a unary fact about one symbol): Or(~Q.zero(1 / x), re(x) > 0)
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-cond2 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-234-cond2', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', integer=True)
Assum = And(Q.integer(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-234-cond2', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', integer=True)
Assum = And(Q.integer(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-cond2 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-234-cond2', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', integer=True)
Assum = And(Q.integer(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-cond2 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-234-cond2', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', integer=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, x))
# dropped (not a unary fact about one symbol): Or(~Q.zero(1 / x), re(x) > 0)
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-234-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-234-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-234-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-234-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, x))
# dropped (not a unary fact about one symbol): Or(~Q.zero(1 / x), re(x) > 0)
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-241-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-241-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(real_root(x, 3)), ~Q.zero(x))
Residual = log(real_root(x, 3)) - (log(x) / 3)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-241-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-241-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(real_root(x, 3)), ~Q.zero(x))
Residual = log(real_root(x, 3)) - (log(x) / 3)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-241-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-241-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(real_root(x, 3)), ~Q.zero(x))
Residual = log(real_root(x, 3)) - (log(x) / 3)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-241-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-241-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(real_root(x, 3))
Residual = log(real_root(x, 3)) - (log(x) / 3)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-243-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-243-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Q.real(x), ~Q.zero(real_root(x, 5)), ~Q.zero(x))
Residual = log(real_root(x, 5)) - (log(x) / 5)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-243-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-243-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Q.real(x), ~Q.zero(real_root(x, 5)), ~Q.zero(x))
Residual = log(real_root(x, 5)) - (log(x) / 5)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-243-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-243-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Q.real(x), ~Q.zero(real_root(x, 5)), ~Q.zero(x))
Residual = log(real_root(x, 5)) - (log(x) / 5)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-243-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-243-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, real=True, zero=False)
# dropped (not a unary fact about one symbol): re(x) > 0
# dropped (not a unary fact about one symbol): ~Q.zero(real_root(x, 5))
Residual = log(real_root(x, 5)) - (log(x) / 5)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-245-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-245-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Q.real(x), ~Q.zero(real_root(x, 7)), ~Q.zero(x))
Residual = log(real_root(x, 7)) - (log(x) / 7)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-245-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-245-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Q.real(x), ~Q.zero(real_root(x, 7)), ~Q.zero(x))
Residual = log(real_root(x, 7)) - (log(x) / 7)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-245-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-245-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Q.real(x), ~Q.zero(real_root(x, 7)), ~Q.zero(x))
Residual = log(real_root(x, 7)) - (log(x) / 7)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-245-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-245-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, real=True, zero=False)
# dropped (not a unary fact about one symbol): re(x) > 0
# dropped (not a unary fact about one symbol): ~Q.zero(real_root(x, 7))
Residual = log(real_root(x, 7)) - (log(x) / 7)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-247-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-247-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(real_root(x, 9)), ~Q.zero(x))
Residual = log(real_root(x, 9)) - (log(x) / 9)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-247-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-247-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(real_root(x, 9)), ~Q.zero(x))
Residual = log(real_root(x, 9)) - (log(x) / 9)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-247-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-247-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(real_root(x, 9)), ~Q.zero(x))
Residual = log(real_root(x, 9)) - (log(x) / 9)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-247-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-247-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(real_root(x, 9))
Residual = log(real_root(x, 9)) - (log(x) / 9)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-248-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-248-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = -Abs(asin(x)) - asin(-Abs(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-248-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-248-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = -Abs(asin(x)) - asin(-Abs(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-248-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-248-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = -Abs(asin(x)) - asin(-Abs(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-248-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-248-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= 1
Residual = -Abs(asin(x)) - asin(-Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-248-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-248-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = -Abs(asin(x)) - asin(-Abs(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-248-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-248-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = -Abs(asin(x)) - asin(-Abs(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-248-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-248-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = -Abs(asin(x)) - asin(-Abs(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-248-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-248-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = -Abs(asin(x)) - asin(-Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-249-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-249-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = -Abs(asinh(x)) - asinh(-Abs(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-249-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-249-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = -Abs(asinh(x)) - asinh(-Abs(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-249-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-249-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = -Abs(asinh(x)) - asinh(-Abs(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-249-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-249-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = -Abs(asinh(x)) - asinh(-Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-251-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-251-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
Residual = -Abs(atanh(x)) - atanh(-Abs(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-251-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-251-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
Residual = -Abs(atanh(x)) - atanh(-Abs(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-251-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-251-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
Residual = -Abs(atanh(x)) - atanh(-Abs(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-251-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-251-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) < 1
# dropped (not a unary fact about one symbol): Ne(x, 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(-Abs(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(-Abs(x), -1, evaluate=False)
Residual = -Abs(atanh(x)) - atanh(-Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-251-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-251-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
Residual = -Abs(atanh(x)) - atanh(-Abs(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-251-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-251-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
Residual = -Abs(atanh(x)) - atanh(-Abs(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-251-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-251-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
Residual = -Abs(atanh(x)) - atanh(-Abs(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-251-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-251-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(x, 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(-Abs(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(-Abs(x), -1, evaluate=False)
Residual = -Abs(atanh(x)) - atanh(-Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-252-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-252-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = -Abs(sinh(x)) - sinh(-Abs(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-252-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-252-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = -Abs(sinh(x)) - sinh(-Abs(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-252-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-252-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = -Abs(sinh(x)) - sinh(-Abs(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-252-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-252-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Residual = -Abs(sinh(x)) - sinh(-Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-252-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-252-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = -Abs(sinh(x)) - sinh(-Abs(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-252-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-252-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = -Abs(sinh(x)) - sinh(-Abs(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-252-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-252-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = -Abs(sinh(x)) - sinh(-Abs(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-252-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-252-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = -Abs(sinh(x)) - sinh(-Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-253-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-253-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
Residual = -Abs(tanh(x)) - tanh(-Abs(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-253-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-253-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
Residual = -Abs(tanh(x)) - tanh(-Abs(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-253-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-253-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
Residual = -Abs(tanh(x)) - tanh(-Abs(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-253-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-253-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = -Abs(tanh(x)) - tanh(-Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-253-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-253-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = -Abs(tanh(x)) - tanh(-Abs(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-253-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-253-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = -Abs(tanh(x)) - tanh(-Abs(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-253-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-253-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = -Abs(tanh(x)) - tanh(-Abs(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-253-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-253-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = -Abs(tanh(x)) - tanh(-Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-256-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-256-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(-exp(x)))
Residual = -exp(-x) - (1 / -exp(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-256-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-256-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(-exp(x)))
Residual = -exp(-x) - (1 / -exp(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-256-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-256-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(-exp(x)))
Residual = -exp(-x) - (1 / -exp(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-256-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-256-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(-exp(x))
Residual = -exp(-x) - (1 / -exp(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-260-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-260-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = -log(cos(x)) - log(1 / cos(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-260-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-260-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = -log(cos(x)) - log(1 / cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-260-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-260-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = -log(cos(x)) - log(1 / cos(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-260-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-260-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cos(x))
Residual = -log(cos(x)) - log(1 / cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-260-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-260-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Abs(re(x)) < pi / 2, ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = -log(cos(x)) - log(1 / cos(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-260-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-260-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Abs(re(x)) < pi / 2, ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = -log(cos(x)) - log(1 / cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-260-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-260-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Abs(re(x)) < pi / 2, ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = -log(cos(x)) - log(1 / cos(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-260-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-260-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Abs(re(x)) < pi / 2
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cos(x))
Residual = -log(cos(x)) - log(1 / cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-260-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-260-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = -log(cos(x)) - log(1 / cos(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-260-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-260-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = -log(cos(x)) - log(1 / cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-260-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-260-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = -log(cos(x)) - log(1 / cos(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-260-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-260-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cos(x))
Residual = -log(cos(x)) - log(1 / cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-261-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-261-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
Residual = -log(cosh(x)) - log(1 / cosh(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-261-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-261-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
Residual = -log(cosh(x)) - log(1 / cosh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-261-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-261-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
Residual = -log(cosh(x)) - log(1 / cosh(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-261-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-261-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cosh(x))
Residual = -log(cosh(x)) - log(1 / cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-261-cond · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-261-cond', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
Residual = -log(cosh(x)) - log(1 / cosh(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-261-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-261-cond', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
Residual = -log(cosh(x)) - log(1 / cosh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-261-cond · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-261-cond', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
Residual = -log(cosh(x)) - log(1 / cosh(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-261-cond · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-261-cond', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): re(x) > 0
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cosh(x))
Residual = -log(cosh(x)) - log(1 / cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-261-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-261-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
Residual = -log(cosh(x)) - log(1 / cosh(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-261-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-261-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
Residual = -log(cosh(x)) - log(1 / cosh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-261-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-261-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
Residual = -log(cosh(x)) - log(1 / cosh(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-261-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-261-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cosh(x))
Residual = -log(cosh(x)) - log(1 / cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-266-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = -sin(log(x)) - sin(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-266-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = -sin(log(x)) - sin(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-266-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = -sin(log(x)) - sin(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-266-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = -sin(log(x)) - sin(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-266-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(1 / x))
Residual = -sin(log(x)) - sin(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-266-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(1 / x))
Residual = -sin(log(x)) - sin(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-266-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(1 / x))
Residual = -sin(log(x)) - sin(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-266-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): re(x) >= 0
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = -sin(log(x)) - sin(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-condf · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-266-condf', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = -sin(log(x)) - sin(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-condf · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-266-condf', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = -sin(log(x)) - sin(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-condf · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-266-condf', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = -sin(log(x)) - sin(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-condf · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-266-condf', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True, negative=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = -sin(log(x)) - sin(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-266-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = -sin(log(x)) - sin(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-266-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = -sin(log(x)) - sin(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-266-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = -sin(log(x)) - sin(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-266-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = -sin(log(x)) - sin(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-267-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = -tan(log(x)) - tan(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-267-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = -tan(log(x)) - tan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-267-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = -tan(log(x)) - tan(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-267-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(1 / x)))
Residual = -tan(log(x)) - tan(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-267-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = -tan(log(x)) - tan(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-267-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = -tan(log(x)) - tan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-267-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = -tan(log(x)) - tan(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-267-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): re(x) >= 0
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(1 / x)))
Residual = -tan(log(x)) - tan(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-condf · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-267-condf', 'satrefine-refine', 'false', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = -tan(log(x)) - tan(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-267-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = -tan(log(x)) - tan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-condf · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-267-condf', 'sympy-refine', 'false', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = -tan(log(x)) - tan(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-267-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True, negative=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(1 / x)))
Residual = -tan(log(x)) - tan(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-267-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = -tan(log(x)) - tan(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-267-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = -tan(log(x)) - tan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-267-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = -tan(log(x)) - tan(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-267-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(1 / x)))
Residual = -tan(log(x)) - tan(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-274-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-274-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = Pow(Abs(x), -2) - Pow(x, -2)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-274-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-274-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = Pow(Abs(x), -2) - Pow(x, -2)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-274-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-274-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = Pow(Abs(x), -2) - Pow(x, -2)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-274-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-274-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = Pow(Abs(x), -2) - Pow(x, -2)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-275-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-275-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = Pow(Abs(x), -3) - Abs(Pow(x, -3))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-275-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-275-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = Pow(Abs(x), -3) - Abs(Pow(x, -3))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-275-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-275-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = Pow(Abs(x), -3) - Abs(Pow(x, -3))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-275-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-275-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = Pow(Abs(x), -3) - Abs(Pow(x, -3))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-276-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-276-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = Pow(Abs(x), -4) - Pow(x, -4)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-276-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-276-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = Pow(Abs(x), -4) - Pow(x, -4)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-276-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-276-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = Pow(Abs(x), -4) - Pow(x, -4)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-276-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-276-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = Pow(Abs(x), -4) - Pow(x, -4)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-278-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-278-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = Pow(Abs(x), -6) - Pow(x, -6)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-278-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-278-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = Pow(Abs(x), -6) - Pow(x, -6)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-278-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-278-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = Pow(Abs(x), -6) - Pow(x, -6)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-278-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-278-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = Pow(Abs(x), -6) - Pow(x, -6)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-283-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-283-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Pow(Abs(x), 2) - (x * x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-283-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-283-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Pow(Abs(x), 2) - (x * x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-283-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-283-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Pow(Abs(x), 2) - (x * x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-283-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-283-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Residual = Pow(Abs(x), 2) - (x * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-283-condf · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-283-condf', 'satrefine-refine', 'false', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = Pow(Abs(x), 2) - (x * x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-283-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-283-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = Pow(Abs(x), 2) - (x * x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-283-condf · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-283-condf', 'sympy-refine', 'false', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = Pow(Abs(x), 2) - (x * x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-283-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-283-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True)
Residual = Pow(Abs(x), 2) - (x * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-283-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-283-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Pow(Abs(x), 2) - (x * x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-283-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-283-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Pow(Abs(x), 2) - (x * x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-283-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-283-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Pow(Abs(x), 2) - (x * x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-283-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-283-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = Pow(Abs(x), 2) - (x * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-284-complex · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-284-complex', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Pow(Abs(x), 3) - Abs(Pow(x, 3))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-284-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-284-complex', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Pow(Abs(x), 3) - Abs(Pow(x, 3))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-284-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-284-complex', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Pow(Abs(x), 3) - Abs(Pow(x, 3))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-284-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-284-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Residual = Pow(Abs(x), 3) - Abs(Pow(x, 3))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-286-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-286-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Pow(Abs(x), 5) - Abs(Pow(x, 5))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-286-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-286-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Pow(Abs(x), 5) - Abs(Pow(x, 5))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-286-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-286-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Pow(Abs(x), 5) - Abs(Pow(x, 5))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-286-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-286-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = Pow(Abs(x), 5) - Abs(Pow(x, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-287-condf · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-287-condf', 'satrefine-refine', 'false', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = Pow(Abs(x), 6) - Pow(x, 6)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-287-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-287-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = Pow(Abs(x), 6) - Pow(x, 6)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-287-condf · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-287-condf', 'sympy-refine', 'false', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = Pow(Abs(x), 6) - Pow(x, 6)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-287-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-287-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True)
Residual = Pow(Abs(x), 6) - Pow(x, 6)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-288-complex · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-288-complex', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Pow(Abs(x), 7) - Abs(Pow(x, 7))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-288-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-288-complex', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Pow(Abs(x), 7) - Abs(Pow(x, 7))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-288-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-288-complex', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Pow(Abs(x), 7) - Abs(Pow(x, 7))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-288-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-288-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Residual = Pow(Abs(x), 7) - Abs(Pow(x, 7))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-289-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-289-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = Pow(Abs(x), 8) - Pow(x, 8)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-289-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-289-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = Pow(Abs(x), 8) - Pow(x, 8)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-289-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-289-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = Pow(Abs(x), 8) - Pow(x, 8)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-289-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-289-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True)
Residual = Pow(Abs(x), 8) - Pow(x, 8)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-289-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-289-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Pow(Abs(x), 8) - Pow(x, 8)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-289-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-289-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Pow(Abs(x), 8) - Pow(x, 8)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-289-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-289-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Pow(Abs(x), 8) - Pow(x, 8)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-289-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-289-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = Pow(Abs(x), 8) - Pow(x, 8)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-29-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-29-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
Residual = 3 * log(x) - log(Pow(x, 3))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-29-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-29-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
Residual = 3 * log(x) - log(Pow(x, 3))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-29-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-29-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
Residual = 3 * log(x) - log(Pow(x, 3))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-29-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-29-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True, positive=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, 3))
Residual = 3 * log(x) - log(Pow(x, 3))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-29-condf · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-29-condf', 'satrefine-refine', 'false', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
Residual = 3 * log(x) - log(Pow(x, 3))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-29-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-29-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
Residual = 3 * log(x) - log(Pow(x, 3))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-29-condf · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-29-condf', 'sympy-refine', 'false', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
Residual = 3 * log(x) - log(Pow(x, 3))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-29-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-29-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, 3))
Residual = 3 * log(x) - log(Pow(x, 3))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-29-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-29-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
Residual = 3 * log(x) - log(Pow(x, 3))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-29-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-29-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
Residual = 3 * log(x) - log(Pow(x, 3))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-29-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-29-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
Residual = 3 * log(x) - log(Pow(x, 3))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-29-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-29-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, 3))
Residual = 3 * log(x) - log(Pow(x, 3))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-3-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-3-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = asinh(sinh(x)) - x
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-3-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-3-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = asinh(sinh(x)) - x
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-3-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-3-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = asinh(sinh(x)) - x
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-3-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-3-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = asinh(sinh(x)) - x
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-30-complex · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-30-complex', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = 4 * Abs(x) - Abs(-4 * x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-30-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-30-complex', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = 4 * Abs(x) - Abs(-4 * x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-30-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-30-complex', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = 4 * Abs(x) - Abs(-4 * x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-30-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-30-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Residual = 4 * Abs(x) - Abs(-4 * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-31-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-31-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = 5 * Abs(x) - Abs(-5 * x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-31-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-31-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = 5 * Abs(x) - Abs(-5 * x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-31-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-31-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = 5 * Abs(x) - Abs(-5 * x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-31-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-31-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = 5 * Abs(x) - Abs(-5 * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-326-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-326-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Pow(exp(x), 2) - exp(2 * x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-326-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-326-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Pow(exp(x), 2) - exp(2 * x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-326-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-326-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Pow(exp(x), 2) - exp(2 * x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-326-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-326-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = Pow(exp(x), 2) - exp(2 * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-33-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-33-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = 6 * Abs(x) - Abs(-6 * x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-33-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-33-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = 6 * Abs(x) - Abs(-6 * x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-33-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-33-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = 6 * Abs(x) - Abs(-6 * x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-33-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-33-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = 6 * Abs(x) - Abs(-6 * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-334-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-334-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(exp(1)) > 0))
Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-334-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-334-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(exp(1)) > 0))
Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-334-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-334-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(exp(1)) > 0))
Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-334-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-334-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(exp(x)), re(exp(1)) > 0)
Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-334-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-334-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), Or(~Q.zero(exp(x)), re(exp(1)) > 0))
Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-334-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-334-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), Or(~Q.zero(exp(x)), re(exp(1)) > 0))
Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-334-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-334-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), Or(~Q.zero(exp(x)), re(exp(1)) > 0))
Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-334-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-334-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): And(im(x) > -pi, im(x) <= pi)
# dropped (not a unary fact about one symbol): Or(~Q.zero(exp(x)), re(exp(1)) > 0)
Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-335-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-335-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(pi) > 0))
Residual = Pow(exp(x), pi) - exp(pi * x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-335-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-335-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(pi) > 0))
Residual = Pow(exp(x), pi) - exp(pi * x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-335-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-335-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(pi) > 0))
Residual = Pow(exp(x), pi) - exp(pi * x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-335-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-335-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(exp(x)), re(pi) > 0)
Residual = Pow(exp(x), pi) - exp(pi * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-335-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-335-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), Or(~Q.zero(exp(x)), re(pi) > 0))
Residual = Pow(exp(x), pi) - exp(pi * x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-335-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-335-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), Or(~Q.zero(exp(x)), re(pi) > 0))
Residual = Pow(exp(x), pi) - exp(pi * x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-335-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-335-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), Or(~Q.zero(exp(x)), re(pi) > 0))
Residual = Pow(exp(x), pi) - exp(pi * x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-335-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-335-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): And(im(x) > -pi, im(x) <= pi)
# dropped (not a unary fact about one symbol): Or(~Q.zero(exp(x)), re(pi) > 0)
Residual = Pow(exp(x), pi) - exp(pi * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-336-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-336-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(x) > 0))
Residual = Pow(exp(x), x) - exp(x * x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-336-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-336-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(x) > 0))
Residual = Pow(exp(x), x) - exp(x * x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-336-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-336-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(x) > 0))
Residual = Pow(exp(x), x) - exp(x * x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-336-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-336-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(exp(x)), re(x) > 0)
Residual = Pow(exp(x), x) - exp(x * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-336-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-336-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), Or(~Q.zero(exp(x)), re(x) > 0))
Residual = Pow(exp(x), x) - exp(x * x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-336-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-336-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), Or(~Q.zero(exp(x)), re(x) > 0))
Residual = Pow(exp(x), x) - exp(x * x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-336-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-336-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), Or(~Q.zero(exp(x)), re(x) > 0))
Residual = Pow(exp(x), x) - exp(x * x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-336-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-336-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): And(im(x) > -pi, im(x) <= pi)
# dropped (not a unary fact about one symbol): Or(~Q.zero(exp(x)), re(x) > 0)
Residual = Pow(exp(x), x) - exp(x * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-343-complex · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-343-complex', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Pow(1 / pi, x) - Pow(pi, -x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-343-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-343-complex', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Pow(1 / pi, x) - Pow(pi, -x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-343-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-343-complex', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Pow(1 / pi, x) - Pow(pi, -x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-343-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-343-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Residual = Pow(1 / pi, x) - Pow(pi, -x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-343-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-343-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Pow(1 / pi, x) - Pow(pi, -x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-343-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-343-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Pow(1 / pi, x) - Pow(pi, -x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-343-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-343-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Pow(1 / pi, x) - Pow(pi, -x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-343-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-343-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = Pow(1 / pi, x) - Pow(pi, -x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-344-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
Residual = Pow(1 / x, x) - Pow(x, -x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-344-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
Residual = Pow(1 / x, x) - Pow(x, -x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-344-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
Residual = Pow(1 / x, x) - Pow(x, -x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-344-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(1 / x), re(x) > 0)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(-x) > 0)
Residual = Pow(1 / x, x) - Pow(x, -x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-344-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
Residual = Pow(1 / x, x) - Pow(x, -x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-344-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
Residual = Pow(1 / x, x) - Pow(x, -x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-344-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
Residual = Pow(1 / x, x) - Pow(x, -x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-344-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): re(x) >= 0
# dropped (not a unary fact about one symbol): Or(~Q.zero(1 / x), re(x) > 0)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(-x) > 0)
Residual = Pow(1 / x, x) - Pow(x, -x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-cond2 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-344-cond2', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', integer=True)
Assum = And(Q.integer(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
Residual = Pow(1 / x, x) - Pow(x, -x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-344-cond2', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', integer=True)
Assum = And(Q.integer(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
Residual = Pow(1 / x, x) - Pow(x, -x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-cond2 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-344-cond2', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', integer=True)
Assum = And(Q.integer(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
Residual = Pow(1 / x, x) - Pow(x, -x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-cond2 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-344-cond2', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', integer=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(1 / x), re(x) > 0)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(-x) > 0)
Residual = Pow(1 / x, x) - Pow(x, -x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-344-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
Residual = Pow(1 / x, x) - Pow(x, -x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-344-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
Residual = Pow(1 / x, x) - Pow(x, -x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-344-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
Residual = Pow(1 / x, x) - Pow(x, -x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-344-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(1 / x), re(x) > 0)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(-x) > 0)
Residual = Pow(1 / x, x) - Pow(x, -x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-35-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-35-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 7)))
Residual = 7 * log(x) - log(Pow(x, 7))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-35-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-35-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 7)))
Residual = 7 * log(x) - log(Pow(x, 7))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-35-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-35-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 7)))
Residual = 7 * log(x) - log(Pow(x, 7))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-35-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-35-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, 7))
Residual = 7 * log(x) - log(Pow(x, 7))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-354-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-354-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(log(5)) > 0), ~Q.zero(x))
Residual = Pow(x, log(5)) - Pow(5, log(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-354-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-354-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(log(5)) > 0), ~Q.zero(x))
Residual = Pow(x, log(5)) - Pow(5, log(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-354-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-354-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(log(5)) > 0), ~Q.zero(x))
Residual = Pow(x, log(5)) - Pow(5, log(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-354-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-354-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(log(5)) > 0)
Residual = Pow(x, log(5)) - Pow(5, log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-356-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-356-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(log(7)) > 0), ~Q.zero(x))
Residual = Pow(x, log(7)) - Pow(7, log(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-356-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-356-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(log(7)) > 0), ~Q.zero(x))
Residual = Pow(x, log(7)) - Pow(7, log(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-356-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-356-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(log(7)) > 0), ~Q.zero(x))
Residual = Pow(x, log(7)) - Pow(7, log(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-356-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-356-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(log(7)) > 0)
Residual = Pow(x, log(7)) - Pow(7, log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-359-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-359-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(log(pi)) > 0), ~Q.zero(x))
Residual = Pow(x, log(pi)) - Pow(pi, log(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-359-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-359-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(log(pi)) > 0), ~Q.zero(x))
Residual = Pow(x, log(pi)) - Pow(pi, log(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-359-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-359-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(log(pi)) > 0), ~Q.zero(x))
Residual = Pow(x, log(pi)) - Pow(pi, log(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-359-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-359-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(log(pi)) > 0)
Residual = Pow(x, log(pi)) - Pow(pi, log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-364-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-364-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = real_root(Abs(x), 3) - Abs(real_root(x, 3))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-364-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-364-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = real_root(Abs(x), 3) - Abs(real_root(x, 3))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-364-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-364-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = real_root(Abs(x), 3) - Abs(real_root(x, 3))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-364-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-364-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = real_root(Abs(x), 3) - Abs(real_root(x, 3))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-367-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-367-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = real_root(Abs(x), 9) - Abs(real_root(x, 9))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-367-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-367-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = real_root(Abs(x), 9) - Abs(real_root(x, 9))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-367-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-367-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = real_root(Abs(x), 9) - Abs(real_root(x, 9))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-367-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-367-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = real_root(Abs(x), 9) - Abs(real_root(x, 9))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-368-complex · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-368-complex', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(acos(x)), ~Q.zero(acos(x)))
Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-368-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-368-complex', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(acos(x)), ~Q.zero(acos(x)))
Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-368-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-368-complex', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(acos(x)), ~Q.zero(acos(x)))
Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-368-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-368-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Q.real(acos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(acos(x))
Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-368-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-368-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.real(acos(x)), ~Q.zero(acos(x)))
Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-368-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-368-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.real(acos(x)), ~Q.zero(acos(x)))
Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-368-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-368-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.real(acos(x)), ~Q.zero(acos(x)))
Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-368-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-368-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Q.real(acos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(acos(x))
Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-369-complex · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-369-complex', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(acos(x)))
Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-369-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-369-complex', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(acos(x)))
Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-369-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-369-complex', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(acos(x)))
Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-369-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-369-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Q.real(acos(x))
Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-369-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-369-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.real(acos(x)))
Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-369-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-369-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.real(acos(x)))
Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-369-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-369-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.real(acos(x)))
Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-369-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-369-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Q.real(acos(x))
Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-370-complex · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-370-complex', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-370-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-370-complex', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-370-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-370-complex', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-370-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-370-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Q.real(acosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(acosh(x))
Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-370-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-370-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-370-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-370-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-370-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-370-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-370-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-370-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Q.real(acosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(acosh(x))
Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-371-complex · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-371-complex', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(acosh(x)))
Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-371-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-371-complex', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(acosh(x)))
Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-371-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-371-complex', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(acosh(x)))
Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-371-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-371-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Q.real(acosh(x))
Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-371-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-371-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.real(acosh(x)))
Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-371-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-371-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.real(acosh(x)))
Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-371-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-371-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.real(acosh(x)))
Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-371-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-371-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Q.real(acosh(x))
Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-372-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-372-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(cosh(x)), ~Q.zero(cosh(x)))
Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-372-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-372-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(cosh(x)), ~Q.zero(cosh(x)))
Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-372-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-372-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(cosh(x)), ~Q.zero(cosh(x)))
Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-372-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-372-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Q.real(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-372-cond · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-372-cond', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Q.real(cosh(x)), ~Q.zero(cosh(x)))
Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-372-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-372-cond', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Q.real(cosh(x)), ~Q.zero(cosh(x)))
Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-372-cond · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-372-cond', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): re(x) > 0
# dropped (not a unary fact about one symbol): Q.real(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-372-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-372-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cosh(x)))
Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-372-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-372-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cosh(x)))
Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-372-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-372-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cosh(x)))
Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-372-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-372-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-373-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-373-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(cosh(x)))
Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-373-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-373-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(cosh(x)))
Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-373-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-373-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(cosh(x)))
Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-373-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-373-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Q.real(cosh(x))
Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-373-cond · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-373-cond', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Q.real(cosh(x)))
Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-373-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-373-cond', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Q.real(cosh(x)))
Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-373-cond · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-373-cond', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): re(x) > 0
# dropped (not a unary fact about one symbol): Q.real(cosh(x))
Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-373-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-373-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-373-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-373-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-373-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-373-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-373-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-373-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-376-cond2 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-376-cond2', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Abs(im(x)) < pi, Q.real(exp(x)), ~Q.zero(exp(x)))
Residual = real_root(exp(x), -3) - exp(x / -3)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-376-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-376-cond2', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Abs(im(x)) < pi, Q.real(exp(x)), ~Q.zero(exp(x)))
Residual = real_root(exp(x), -3) - exp(x / -3)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-376-cond2 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-376-cond2', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Abs(im(x)) < pi
# dropped (not a unary fact about one symbol): Q.real(exp(x))
# dropped (not a unary fact about one symbol): ~Q.zero(exp(x))
Residual = real_root(exp(x), -3) - exp(x / -3)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-378-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-378-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(exp(x)))
Residual = real_root(exp(x), -5) - exp(x / -5)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-378-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-378-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(exp(x)))
Residual = real_root(exp(x), -5) - exp(x / -5)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-378-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-378-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(exp(x)))
Residual = real_root(exp(x), -5) - exp(x / -5)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-378-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-378-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(exp(x))
Residual = real_root(exp(x), -5) - exp(x / -5)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-38-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-38-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 9)))
Residual = 9 * log(x) - log(Pow(x, 9))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-38-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-38-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 9)))
Residual = 9 * log(x) - log(Pow(x, 9))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-38-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-38-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 9)))
Residual = 9 * log(x) - log(Pow(x, 9))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-38-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-38-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, 9))
Residual = 9 * log(x) - log(Pow(x, 9))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-380-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-380-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(exp(x)))
Residual = real_root(exp(x), -7) - exp(x / -7)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-380-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-380-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(exp(x)))
Residual = real_root(exp(x), -7) - exp(x / -7)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-380-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-380-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(exp(x)))
Residual = real_root(exp(x), -7) - exp(x / -7)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-380-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-380-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(exp(x))
Residual = real_root(exp(x), -7) - exp(x / -7)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-385-cond · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-385-cond', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Q.real(exp(x)))
Residual = real_root(exp(x), 3) - exp(x / 3)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-385-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-385-cond', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Q.real(exp(x)))
Residual = real_root(exp(x), 3) - exp(x / 3)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-385-cond · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-385-cond', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): re(x) > 0
# dropped (not a unary fact about one symbol): Q.real(exp(x))
Residual = real_root(exp(x), 3) - exp(x / 3)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-387-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-387-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(exp(x)))
Residual = real_root(exp(x), 5) - exp(x / 5)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-387-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-387-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(exp(x)))
Residual = real_root(exp(x), 5) - exp(x / 5)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-387-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-387-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(exp(x)))
Residual = real_root(exp(x), 5) - exp(x / 5)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-387-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-387-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Q.real(exp(x))
Residual = real_root(exp(x), 5) - exp(x / 5)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-389-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-389-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(exp(x)))
Residual = real_root(exp(x), 7) - exp(x / 7)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-389-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-389-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(exp(x)))
Residual = real_root(exp(x), 7) - exp(x / 7)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-389-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-389-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.real(exp(x)))
Residual = real_root(exp(x), 7) - exp(x / 7)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-389-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-389-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Q.real(exp(x))
Residual = real_root(exp(x), 7) - exp(x / 7)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-392-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-392-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-392-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-392-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-392-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-392-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-392-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-392-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= 1
Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-392-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-392-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-392-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-392-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-392-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-392-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-392-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-392-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-394-cond · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-394-cond', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-394-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-394-cond', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-394-cond · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-394-cond', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-394-cond · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-394-cond', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) < 1
# dropped (not a unary fact about one symbol): Ne(x, 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -1, evaluate=False)
Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-394-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-394-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-394-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-394-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-394-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-394-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-394-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-394-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(x, 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -1, evaluate=False)
Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-395-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-395-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-395-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-395-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-395-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-395-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-395-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-395-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-396-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-396-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-396-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-396-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-396-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-396-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-396-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-396-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-396-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-396-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-396-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-396-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-396-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-396-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-396-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-396-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-397-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-397-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(Abs(tanh(x))) - Abs(sin(tanh(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-397-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-397-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(Abs(tanh(x))) - Abs(sin(tanh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-397-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-397-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(Abs(tanh(x))) - Abs(sin(tanh(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-397-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-397-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = sin(Abs(tanh(x))) - Abs(sin(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-399-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-399-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = sin(acos(sin(x))) - Abs(cos(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-399-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-399-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = sin(acos(sin(x))) - Abs(cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-399-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-399-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = sin(acos(sin(x))) - Abs(cos(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-399-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-399-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True)
Residual = sin(acos(sin(x))) - Abs(cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-40-complex · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-40-complex', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Abs(x) * pi - Abs(pi * x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-40-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-40-complex', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Abs(x) * pi - Abs(pi * x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-40-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-40-complex', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Abs(x) * pi - Abs(pi * x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-40-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-40-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Residual = Abs(x) * pi - Abs(pi * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-402-cond · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-402-cond', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-402-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-402-cond', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-402-cond · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-402-cond', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-402-cond · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-402-cond', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) < 1
# dropped (not a unary fact about one symbol): Ne(Abs(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -1, evaluate=False)
Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-402-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-402-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-402-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-402-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-402-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-402-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-402-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-402-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(Abs(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -1, evaluate=False)
Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-403-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = sin(-log(x)) - sin(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-403-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = sin(-log(x)) - sin(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-403-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = sin(-log(x)) - sin(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-403-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = sin(-log(x)) - sin(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-403-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(1 / x))
Residual = sin(-log(x)) - sin(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-403-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(1 / x))
Residual = sin(-log(x)) - sin(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-403-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(1 / x))
Residual = sin(-log(x)) - sin(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-403-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): re(x) >= 0
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = sin(-log(x)) - sin(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-condf · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-403-condf', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = sin(-log(x)) - sin(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-condf · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-403-condf', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = sin(-log(x)) - sin(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-condf · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-403-condf', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = sin(-log(x)) - sin(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-condf · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-403-condf', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True, negative=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = sin(-log(x)) - sin(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-403-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = sin(-log(x)) - sin(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-403-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = sin(-log(x)) - sin(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-403-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = sin(-log(x)) - sin(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-403-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = sin(-log(x)) - sin(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-404-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-404-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-404-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-404-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-404-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-404-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-404-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-404-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-404-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-404-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-404-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-404-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-404-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-404-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-404-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-404-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-410-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-410-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(sinh(x)))
Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-410-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-410-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(sinh(x)))
Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-410-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-410-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(sinh(x)))
Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-410-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-410-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(sinh(x))
Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-412-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-412-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-412-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-412-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-412-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-412-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-412-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-412-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) < 1
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(asin(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(asin(x)))
Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-412-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-412-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-412-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-412-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-412-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-412-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-412-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-412-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(asin(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(asin(x)))
Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-413-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-413-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(Abs(cos(x)))), ~Q.zero(cos(cos(x))))
Residual = tan(Abs(cos(x))) - Abs(tan(cos(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-413-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-413-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(Abs(cos(x)))), ~Q.zero(cos(cos(x))))
Residual = tan(Abs(cos(x))) - Abs(tan(cos(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-413-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-413-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(Abs(cos(x)))), ~Q.zero(cos(cos(x))))
Residual = tan(Abs(cos(x))) - Abs(tan(cos(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-413-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-413-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(cos(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(cos(x)))
Residual = tan(Abs(cos(x))) - Abs(tan(cos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-414-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-414-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-414-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-414-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-414-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-414-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-414-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-414-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(sin(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(sin(x)))
Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-414-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-414-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-414-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-414-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-414-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-414-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-414-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-414-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(sin(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(sin(x)))
Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-415-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-415-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-415-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-415-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-415-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-415-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-415-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-415-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(tanh(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(x)))
Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-415-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-415-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-415-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-415-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-415-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-415-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-415-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-415-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(tanh(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(x)))
Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-416-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-416-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1, ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-416-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-416-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1, ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-416-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-416-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1, ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-416-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-416-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= 1
# dropped (not a unary fact about one symbol): ~Q.zero(cos(acos(Abs(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(acos(x)))
Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-416-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-416-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-416-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-416-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-416-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-416-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-416-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-416-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(acos(Abs(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(acos(x)))
Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-417-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-417-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, ~Q.zero(cos(asin(Abs(x)))), ~Q.zero(cos(asin(x))))
Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-417-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-417-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, ~Q.zero(cos(asin(Abs(x)))), ~Q.zero(cos(asin(x))))
Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-417-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-417-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, ~Q.zero(cos(asin(Abs(x)))), ~Q.zero(cos(asin(x))))
Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-417-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-417-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) < 1
# dropped (not a unary fact about one symbol): ~Q.zero(cos(asin(Abs(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(asin(x)))
Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-417-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-417-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(asin(Abs(x)))), ~Q.zero(cos(asin(x))))
Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-417-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-417-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(asin(Abs(x)))), ~Q.zero(cos(asin(x))))
Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-417-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-417-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(asin(Abs(x)))), ~Q.zero(cos(asin(x))))
Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-417-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-417-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(asin(Abs(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(asin(x)))
Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-420-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = tan(-log(x)) - tan(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-420-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = tan(-log(x)) - tan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-420-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = tan(-log(x)) - tan(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-420-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(-log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(1 / x)))
Residual = tan(-log(x)) - tan(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-420-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = tan(-log(x)) - tan(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-420-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = tan(-log(x)) - tan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-420-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = tan(-log(x)) - tan(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-420-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): re(x) >= 0
# dropped (not a unary fact about one symbol): ~Q.zero(cos(-log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(1 / x)))
Residual = tan(-log(x)) - tan(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-condf · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-420-condf', 'satrefine-refine', 'false', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = tan(-log(x)) - tan(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-420-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = tan(-log(x)) - tan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-condf · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-420-condf', 'sympy-refine', 'false', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = tan(-log(x)) - tan(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-420-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True, negative=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(-log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(1 / x)))
Residual = tan(-log(x)) - tan(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-420-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = tan(-log(x)) - tan(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-420-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = tan(-log(x)) - tan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-420-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = tan(-log(x)) - tan(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-420-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(-log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(1 / x)))
Residual = tan(-log(x)) - tan(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-421-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-421-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cosh(x)), ~Q.zero(cos(tanh(x))))
Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-421-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-421-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cosh(x)), ~Q.zero(cos(tanh(x))))
Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-421-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-421-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cosh(x)), ~Q.zero(cos(tanh(x))))
Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-421-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-421-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(Abs(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(x)))
Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-421-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-421-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cos(tanh(x))))
Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-421-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-421-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cos(tanh(x))))
Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-421-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-421-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cos(tanh(x))))
Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-421-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-421-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(Abs(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(x)))
Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-422-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-422-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-422-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-422-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-422-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-422-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-422-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-422-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, -I, evaluate=False)
Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-422-condf · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-422-condf', 'satrefine-refine', 'false', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-422-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-422-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-422-condf · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-422-condf', 'sympy-refine', 'false', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-422-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-422-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, -I, evaluate=False)
Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-423-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-423-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(acosh(Abs(x)))), ~Q.zero(x))
Residual = tanh(acosh(Abs(x))) - cos(asin(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-423-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-423-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(acosh(Abs(x)))), ~Q.zero(x))
Residual = tanh(acosh(Abs(x))) - cos(asin(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-423-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-423-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(acosh(Abs(x)))), ~Q.zero(x))
Residual = tanh(acosh(Abs(x))) - cos(asin(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-423-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-423-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(acosh(Abs(x))))
Residual = tanh(acosh(Abs(x))) - cos(asin(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-424-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-424-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-424-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-424-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-424-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-424-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-424-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-424-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, -I, evaluate=False)
Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-424-condf · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-424-condf', 'satrefine-refine', 'false', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-424-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-424-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-424-condf · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-424-condf', 'sympy-refine', 'false', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-424-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-424-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, -I, evaluate=False)
Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-428-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-428-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x <= 1)
Residual = atan(sinh(x)) - asin(tanh(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-428-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-428-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x <= 1)
Residual = atan(sinh(x)) - asin(tanh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-428-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-428-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x <= 1)
Residual = atan(sinh(x)) - asin(tanh(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-428-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-428-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): x <= 1
Residual = atan(sinh(x)) - asin(tanh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-428-cond3 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-428-cond3', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x >= 0, x <= pi)
Residual = atan(sinh(x)) - asin(tanh(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-428-cond3 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-428-cond3', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x >= 0, x <= pi)
Residual = atan(sinh(x)) - asin(tanh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-428-cond3 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-428-cond3', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x >= 0, x <= pi)
Residual = atan(sinh(x)) - asin(tanh(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-428-cond3 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-428-cond3', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): x >= 0
# dropped (not a unary fact about one symbol): x <= pi
Residual = atan(sinh(x)) - asin(tanh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-430-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
Residual = log(x) * x - log(Pow(x, x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-430-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
Residual = log(x) * x - log(Pow(x, x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-430-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
Residual = log(x) * x - log(Pow(x, x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-430-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, x))
Residual = log(x) * x - log(Pow(x, x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-430-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
Residual = log(x) * x - log(Pow(x, x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-430-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
Residual = log(x) * x - log(Pow(x, x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-430-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
Residual = log(x) * x - log(Pow(x, x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-430-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True, positive=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, x))
Residual = log(x) * x - log(Pow(x, x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-cond2 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-430-cond2', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
Residual = log(x) * x - log(Pow(x, x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-430-cond2', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
Residual = log(x) * x - log(Pow(x, x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-cond2 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-430-cond2', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
Residual = log(x) * x - log(Pow(x, x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-cond2 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-430-cond2', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Abs(x) < 1
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, x))
Residual = log(x) * x - log(Pow(x, x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-430-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
Residual = log(x) * x - log(Pow(x, x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-430-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
Residual = log(x) * x - log(Pow(x, x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-430-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
Residual = log(x) * x - log(Pow(x, x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-430-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, x))
Residual = log(x) * x - log(Pow(x, x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-432-cond3 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-432-cond3', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= pi / 2, ~Q.zero(cosh(x)))
Residual = acos(Abs(tanh(x))) - asin(1 / cosh(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-432-cond3 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-432-cond3', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= pi / 2, ~Q.zero(cosh(x)))
Residual = acos(Abs(tanh(x))) - asin(1 / cosh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-432-cond3 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-432-cond3', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= pi / 2, ~Q.zero(cosh(x)))
Residual = acos(Abs(tanh(x))) - asin(1 / cosh(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-432-cond3 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-432-cond3', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= pi / 2
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = acos(Abs(tanh(x))) - asin(1 / cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-433-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
Residual = atan(-log(x)) - atan(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-433-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
Residual = atan(-log(x)) - atan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-433-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
Residual = atan(-log(x)) - atan(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-433-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(-log(x), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(-log(x), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): Ne(log(1 / x), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(log(1 / x), -I, evaluate=False)
Residual = atan(-log(x)) - atan(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-433-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
Residual = atan(-log(x)) - atan(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-433-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
Residual = atan(-log(x)) - atan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-433-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
Residual = atan(-log(x)) - atan(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-433-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): re(x) >= 0
# dropped (not a unary fact about one symbol): Ne(-log(x), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(-log(x), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): Ne(log(1 / x), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(log(1 / x), -I, evaluate=False)
Residual = atan(-log(x)) - atan(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-condf · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-433-condf', 'satrefine-refine', 'false', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
Residual = atan(-log(x)) - atan(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-433-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
Residual = atan(-log(x)) - atan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-condf · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-433-condf', 'sympy-refine', 'false', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
Residual = atan(-log(x)) - atan(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-433-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True, negative=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(-log(x), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(-log(x), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): Ne(log(1 / x), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(log(1 / x), -I, evaluate=False)
Residual = atan(-log(x)) - atan(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-433-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
Residual = atan(-log(x)) - atan(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-433-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
Residual = atan(-log(x)) - atan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-433-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
Residual = atan(-log(x)) - atan(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-433-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(-log(x), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(-log(x), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): Ne(log(1 / x), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(log(1 / x), -I, evaluate=False)
Residual = atan(-log(x)) - atan(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-442-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
Residual = -log(log(x)) - log(1 / log(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-442-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
Residual = -log(log(x)) - log(1 / log(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-442-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
Residual = -log(log(x)) - log(1 / log(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-442-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(log(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / log(x))
Residual = -log(log(x)) - log(1 / log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-442-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
Residual = -log(log(x)) - log(1 / log(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-442-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
Residual = -log(log(x)) - log(1 / log(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-442-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
Residual = -log(log(x)) - log(1 / log(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-442-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(log(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / log(x))
Residual = -log(log(x)) - log(1 / log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-cond4 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-442-cond4', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', integer=True)
Assum = And(Q.integer(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
Residual = -log(log(x)) - log(1 / log(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-cond4 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-442-cond4', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', integer=True)
Assum = And(Q.integer(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
Residual = -log(log(x)) - log(1 / log(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-cond4 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-442-cond4', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', integer=True)
Assum = And(Q.integer(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
Residual = -log(log(x)) - log(1 / log(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-cond4 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-442-cond4', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', integer=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(log(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / log(x))
Residual = -log(log(x)) - log(1 / log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-442-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
Residual = -log(log(x)) - log(1 / log(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-442-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
Residual = -log(log(x)) - log(1 / log(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-442-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
Residual = -log(log(x)) - log(1 / log(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-442-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(log(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / log(x))
Residual = -log(log(x)) - log(1 / log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-446-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-446-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(cos(Abs(atan(x)))))
Residual = tan(Abs(atan(x))) - Abs(x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-446-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-446-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(cos(Abs(atan(x)))))
Residual = tan(Abs(atan(x))) - Abs(x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-446-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-446-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(cos(Abs(atan(x)))))
Residual = tan(Abs(atan(x))) - Abs(x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-446-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-446-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Ne(x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(atan(x))))
Residual = tan(Abs(atan(x))) - Abs(x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-449-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-449-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cosh(-log(x))), ~Q.zero(1 / x), ~Q.zero(cosh(log(1 / x))))
Residual = tanh(-log(x)) - tanh(log(1 / x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-449-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-449-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cosh(-log(x))), ~Q.zero(1 / x), ~Q.zero(cosh(log(1 / x))))
Residual = tanh(-log(x)) - tanh(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-449-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-449-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cosh(-log(x))), ~Q.zero(1 / x), ~Q.zero(cosh(log(1 / x))))
Residual = tanh(-log(x)) - tanh(log(1 / x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-449-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-449-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(-log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(log(1 / x)))
Residual = tanh(-log(x)) - tanh(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-450-complex · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-450-complex', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x))
Residual = x / x - 1
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-450-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-450-complex', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x))
Residual = x / x - 1
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-450-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-450-complex', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x))
Residual = x / x - 1
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-450-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-450-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
Residual = x / x - 1
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-450-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-450-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x))
Residual = x / x - 1
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-450-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-450-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x))
Residual = x / x - 1
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-450-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-450-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x))
Residual = x / x - 1
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-450-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-450-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
Residual = x / x - 1
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-451-complex · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-451-complex', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x))
Residual = 0 / x - 0
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-451-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-451-complex', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x))
Residual = 0 / x - 0
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-451-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-451-complex', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x))
Residual = 0 / x - 0
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-451-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-451-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
Residual = 0 / x - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-451-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-451-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x))
Residual = 0 / x - 0
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-451-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-451-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x))
Residual = 0 / x - 0
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-451-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-451-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x))
Residual = 0 / x - 0
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-451-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-451-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
Residual = 0 / x - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-46-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-46-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), ~Q.zero(Pow(2, x)))
Residual = log(2) * x - log(Pow(2, x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-46-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-46-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), ~Q.zero(Pow(2, x)))
Residual = log(2) * x - log(Pow(2, x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-46-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-46-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), ~Q.zero(Pow(2, x)))
Residual = log(2) * x - log(Pow(2, x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-46-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-46-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): And(im(x) > -pi, im(x) <= pi)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(2, x))
Residual = log(2) * x - log(Pow(2, x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-5-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = atanh(Abs(x)) - Abs(atanh(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-5-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = atanh(Abs(x)) - Abs(atanh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-5-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = atanh(Abs(x)) - Abs(atanh(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-5-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) < 1
# dropped (not a unary fact about one symbol): Ne(Abs(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -1, evaluate=False)
Residual = atanh(Abs(x)) - Abs(atanh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-5-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = atanh(Abs(x)) - Abs(atanh(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-5-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = atanh(Abs(x)) - Abs(atanh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-5-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = atanh(Abs(x)) - Abs(atanh(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-5-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(Abs(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -1, evaluate=False)
Residual = atanh(Abs(x)) - Abs(atanh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-50-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-50-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Pow(6, x)))
Residual = log(6) * x - log(Pow(6, x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-50-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-50-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Pow(6, x)))
Residual = log(6) * x - log(Pow(6, x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-50-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-50-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Pow(6, x)))
Residual = log(6) * x - log(Pow(6, x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-50-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-50-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(6, x))
Residual = log(6) * x - log(Pow(6, x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-50-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-50-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Pow(6, x)))
Residual = log(6) * x - log(Pow(6, x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-50-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-50-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Pow(6, x)))
Residual = log(6) * x - log(Pow(6, x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-50-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-50-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Pow(6, x)))
Residual = log(6) * x - log(Pow(6, x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-50-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-50-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(6, x))
Residual = log(6) * x - log(Pow(6, x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-51-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-51-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Pow(7, x)))
Residual = log(7) * x - log(Pow(7, x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-51-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-51-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Pow(7, x)))
Residual = log(7) * x - log(Pow(7, x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-51-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-51-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Pow(7, x)))
Residual = log(7) * x - log(Pow(7, x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-51-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-51-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(7, x))
Residual = log(7) * x - log(Pow(7, x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5372-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-5372-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = sin(asin(Integer(1) / -4)) - Rational(-1, 4)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5372-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-5372-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = sin(asin(Integer(1) / -4)) - Rational(-1, 4)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5372-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-5372-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = sin(asin(Integer(1) / -4)) - Rational(-1, 4)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5372-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-5372-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = sin(asin(Integer(1) / -4)) - Rational(-1, 4)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5382-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-5382-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''Assum = And()
Residual = sinh(log(Integer(1) / 4)) - Rational(-15, 8)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5382-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-5382-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''Assum = And()
Residual = sinh(log(Integer(1) / 4)) - Rational(-15, 8)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5382-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-5382-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''Assum = And()
Residual = sinh(log(Integer(1) / 4)) - Rational(-15, 8)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5382-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-5382-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = sinh(log(Integer(1) / 4)) - Rational(-15, 8)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5385-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-5385-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''Assum = And()
Residual = sinh(-log(4)) - Rational(-15, 8)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5385-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-5385-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''Assum = And()
Residual = sinh(-log(4)) - Rational(-15, 8)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5385-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-5385-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''Assum = And()
Residual = sinh(-log(4)) - Rational(-15, 8)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5385-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-5385-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = sinh(-log(4)) - Rational(-15, 8)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-55-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-55-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-55-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-55-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-55-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-55-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-55-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-55-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(exp(1)) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, exp(1)))
Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-55-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-55-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-55-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-55-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-55-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-55-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-55-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-55-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True, positive=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(exp(1)) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, exp(1)))
Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-55-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-55-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-55-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-55-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-55-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-55-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-55-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-55-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(exp(1)) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, exp(1)))
Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-56-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
Residual = log(x) * pi - log(Pow(x, pi))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-56-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
Residual = log(x) * pi - log(Pow(x, pi))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-56-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
Residual = log(x) * pi - log(Pow(x, pi))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-56-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, pi))
Residual = log(x) * pi - log(Pow(x, pi))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-56-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
Residual = log(x) * pi - log(Pow(x, pi))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-56-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
Residual = log(x) * pi - log(Pow(x, pi))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-56-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
Residual = log(x) * pi - log(Pow(x, pi))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-56-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True, positive=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, pi))
Residual = log(x) * pi - log(Pow(x, pi))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-condf · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-56-condf', 'satrefine-refine', 'false', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
Residual = log(x) * pi - log(Pow(x, pi))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-56-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
Residual = log(x) * pi - log(Pow(x, pi))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-condf · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-56-condf', 'sympy-refine', 'false', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
Residual = log(x) * pi - log(Pow(x, pi))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-56-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True, imaginary=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, pi))
Residual = log(x) * pi - log(Pow(x, pi))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-real · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-56-real', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
Residual = log(x) * pi - log(Pow(x, pi))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-56-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
Residual = log(x) * pi - log(Pow(x, pi))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-56-real', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
Residual = log(x) * pi - log(Pow(x, pi))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-56-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, pi))
Residual = log(x) * pi - log(Pow(x, pi))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-6-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-6-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
Residual = atanh(tanh(x)) - x
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-6-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-6-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
Residual = atanh(tanh(x)) - x
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-6-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-6-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(cosh(x)), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
Residual = atanh(tanh(x)) - x
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-6-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-6-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): Ne(tanh(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(tanh(x), -1, evaluate=False)
Residual = atanh(tanh(x)) - x
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-6-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-6-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
Residual = atanh(tanh(x)) - x
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-6-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-6-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
Residual = atanh(tanh(x)) - x
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-6-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-6-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
Residual = atanh(tanh(x)) - x
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-6-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-6-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(tanh(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(tanh(x), -1, evaluate=False)
Residual = atanh(tanh(x)) - x
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-7-complex · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-7-complex', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = 1 / Abs(x) - Abs(1 / x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-7-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-7-complex', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = 1 / Abs(x) - Abs(1 / x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-7-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-7-complex', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = 1 / Abs(x) - Abs(1 / x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-7-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-7-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = 1 / Abs(x) - Abs(1 / x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-73-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-73-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(-Abs(x)))
Residual = -1 / Abs(x) - (1 / -Abs(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-73-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-73-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(-Abs(x)))
Residual = -1 / Abs(x) - (1 / -Abs(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-73-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-73-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(-Abs(x)))
Residual = -1 / Abs(x) - (1 / -Abs(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-73-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-73-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
# dropped (not a unary fact about one symbol): ~Q.zero(-Abs(x))
Residual = -1 / Abs(x) - (1 / -Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-80-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-80-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(-cos(x)))
Residual = -1 / cos(x) - (1 / -cos(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-80-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-80-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(-cos(x)))
Residual = -1 / cos(x) - (1 / -cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-80-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-80-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(-cos(x)))
Residual = -1 / cos(x) - (1 / -cos(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-80-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-80-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(-cos(x))
Residual = -1 / cos(x) - (1 / -cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-806-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-806-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = cosh(0) - 1
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-806-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-806-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = cosh(0) - 1
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-806-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-806-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = cosh(0) - 1
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-806-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-806-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = cosh(0) - 1
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-813-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-813-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = sinh(0) - 0
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-813-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-813-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = sinh(0) - 0
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-813-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-813-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = sinh(0) - 0
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-813-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-813-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = sinh(0) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-816-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-816-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = tanh(0) - 0
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-816-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-816-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = tanh(0) - 0
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-816-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-816-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = tanh(0) - 0
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-816-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-816-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = tanh(0) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-819-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-819-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = 0 / pi - 0
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-819-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-819-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = 0 / pi - 0
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-819-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-819-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = 0 / pi - 0
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-819-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-819-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = 0 / pi - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-83-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-83-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(-log(x)))
Residual = -1 / log(x) - (1 / -log(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-83-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-83-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(-log(x)))
Residual = -1 / log(x) - (1 / -log(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-83-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-83-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(-log(x)))
Residual = -1 / log(x) - (1 / -log(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-83-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-83-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(log(x))
# dropped (not a unary fact about one symbol): ~Q.zero(-log(x))
Residual = -1 / log(x) - (1 / -log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-837-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-837-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = Pow(0, pi) - 0
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-837-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-837-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = Pow(0, pi) - 0
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-837-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-837-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = Pow(0, pi) - 0
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-837-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-837-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = Pow(0, pi) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-848-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-848-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''Assum = And()
Residual = sinh(log(4)) - Rational(15, 8)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-848-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-848-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''Assum = And()
Residual = sinh(log(4)) - Rational(15, 8)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-848-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-848-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''Assum = And()
Residual = sinh(log(4)) - Rational(15, 8)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-848-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-848-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = sinh(log(4)) - Rational(15, 8)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-86-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-86-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(tan(x)), ~Q.zero(-tan(x)))
Residual = -1 / tan(x) - (1 / -tan(x))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-86-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-86-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(tan(x)), ~Q.zero(-tan(x)))
Residual = -1 / tan(x) - (1 / -tan(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-86-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-86-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(tan(x)), ~Q.zero(-tan(x)))
Residual = -1 / tan(x) - (1 / -tan(x))
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-86-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-86-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(tan(x))
# dropped (not a unary fact about one symbol): ~Q.zero(-tan(x))
Residual = -1 / tan(x) - (1 / -tan(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-868-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-868-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = 0 * acosh(7) - 0
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-868-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-868-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = 0 * acosh(7) - 0
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-868-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-868-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = 0 * acosh(7) - 0
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-868-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-868-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = 0 * acosh(7) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-9-complex · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (declined correctly)
_n[_run('sp-acj4-9-complex', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261015-025015 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(exp(x)))
Residual = log(exp(x)) - x
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-9-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-9-complex', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(exp(x)))
Residual = log(exp(x)) - x
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-9-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (declined correctly)
_n[_run('sp-acj4-9-complex', 'sympy-refine', 'contingent', 'the run sympy-refine-20261015-024816 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(exp(x)))
Residual = log(exp(x)) - x
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-9-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-9-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(exp(x))
Residual = log(exp(x)) - x
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-9-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered null (no verdict)
_n[_run('sp-acj4-9-cond', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), ~Q.zero(exp(x)))
Residual = log(exp(x)) - x
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-9-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-9-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), ~Q.zero(exp(x)))
Residual = log(exp(x)) - x
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-9-cond · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered null (no verdict)
_n[_run('sp-acj4-9-cond', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), ~Q.zero(exp(x)))
Residual = log(exp(x)) - x
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-9-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-9-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP2, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): And(im(x) > -pi, im(x) <= pi)
# dropped (not a unary fact about one symbol): ~Q.zero(exp(x))
Residual = log(exp(x)) - x
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-90-complex · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-90-complex', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = 3 / Abs(x) - Abs(-3 / x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-90-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-90-complex', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = 3 / Abs(x) - Abs(-3 / x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-90-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-90-complex', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = 3 / Abs(x) - Abs(-3 / x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-90-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-90-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = 3 / Abs(x) - Abs(-3 / x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-90-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-90-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = 3 / Abs(x) - Abs(-3 / x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-90-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-90-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = 3 / Abs(x) - Abs(-3 / x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-90-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-90-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = 3 / Abs(x) - Abs(-3 / x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-90-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-90-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = 3 / Abs(x) - Abs(-3 / x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-911-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-911-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = 0 / asin(-1) - 0
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-911-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-911-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = 0 / asin(-1) - 0
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-911-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-911-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = 0 / asin(-1) - 0
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-911-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-911-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = 0 / asin(-1) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-927-ground · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-927-ground', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = 0 / asinh(4) - 0
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-927-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-927-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = 0 / asinh(4) - 0
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-927-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-927-ground', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''Assum = And()
Residual = 0 / asinh(4) - 0
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-927-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-927-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''Residual = 0 / asinh(4) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-94-complex · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-94-complex', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = 7 / Abs(x) - Abs(-7 / x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-94-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-94-complex', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = 7 / Abs(x) - Abs(-7 / x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-94-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-94-complex', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
Residual = 7 / Abs(x) - Abs(-7 / x)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-94-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-94-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = 7 / Abs(x) - Abs(-7 / x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-99-complex · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-99-complex', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Abs(x) / 3 - Abs(x / -3)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-99-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-99-complex', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Abs(x) / 3 - Abs(x / -3)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-99-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-99-complex', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Abs(x) / 3 - Abs(x / -3)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-99-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-99-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', complex=True)
Residual = Abs(x) / 3 - Abs(x / -3)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-99-real · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261015-025015 answered true (solved)
_n[_run('sp-acj4-99-real', 'satrefine-refine', 'true', 'the run satrefine-refine-20261015-025015 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Abs(x) / 3 - Abs(x / -3)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-99-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-99-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Abs(x) / 3 - Abs(x / -3)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-99-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261015-024816 answered true (solved)
_n[_run('sp-acj4-99-real', 'sympy-refine', 'true', 'the run sympy-refine-20261015-024816 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Abs(x) / 3 - Abs(x / -3)
Result = refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-99-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-99-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP2, r'''x = Symbol('x', real=True)
Residual = Abs(x) / 3 - Abs(x / -3)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

print(f"done: {sum(_n.values())} case run(s): {_n['true']} true, {_n['false']} false, {_n['null']} null")
