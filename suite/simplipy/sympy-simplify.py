# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# suite simplipy · every case · system sympy-simplify (307 cases listed)
# 307 case run(s).  Each runs in a fresh copy of its setup's namespace, as in the
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


# ---- case sp-acj4-0-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-0-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = acosh(cosh(x)) - Abs(x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-0-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-0-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = acosh(cosh(x)) - Abs(x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-1-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= 1
Residual = asin(Abs(x)) - Abs(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-1-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = asin(Abs(x)) - Abs(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1007-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1007-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = 0 / sin(5) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-102-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-102-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = Abs(x) / 6 - Abs(x / -6)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-102-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-102-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = Abs(x) / 6 - Abs(x / -6)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-108-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-108-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = Abs(x) / x - (x / Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-108-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-108-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = Abs(x) / x - (x / Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-108-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-108-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = Abs(x) / x - (x / Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1107-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1107-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = asin(sin(Integer(1) / 10)) - Rational(1, 10)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1148-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1148-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = cosh(log(Integer(1) / 4)) - Rational(17, 8)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1149-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1149-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = exp(Abs(log(2))) - 2
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-115-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-115-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): x > 0
# dropped (not a unary fact about one symbol): ~Q.zero(real_root(x, -4))
Residual = log(x) / -4 - log(real_root(x, -4))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-116-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-116-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): x > 0
# dropped (not a unary fact about one symbol): ~Q.zero(real_root(x, -6))
Residual = log(x) / -6 - log(real_root(x, -6))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1177-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1177-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = Pow(0, asinh(10)) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1195-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1195-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = Pow(0, atan(7)) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-120-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-120-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = pi / Abs(x) - Abs(pi / x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-120-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-120-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = pi / Abs(x) - Abs(pi / x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1217-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1217-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = Pow(0, exp(-1)) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1238-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1238-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = Pow(0, 1 / pi) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-124-condf · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-124-condf', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = Abs(asin(tanh(x))) - acos(1 / cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1247-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1247-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = Pow(0, log(9)) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1254-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1254-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = Pow(0, sin(2)) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-1258-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-1258-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = Pow(0, sin(9)) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-127-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-127-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): re(x) >= 0
# dropped (not a unary fact about one symbol): Ne(exp(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(exp(x), -1, evaluate=False)
Residual = Abs(atanh(exp(x))) - atanh(exp(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-127-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-127-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(exp(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(exp(x), -1, evaluate=False)
Residual = Abs(atanh(exp(x))) - atanh(exp(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-128-cond2 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-128-cond2', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= 1
Residual = Abs(cos(asin(x))) - cos(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-128-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-128-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): x > 1
Residual = Abs(cos(asin(x))) - cos(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-128-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-128-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = Abs(cos(asin(x))) - cos(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-129-cond · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-129-cond', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True)
# dropped (not a unary fact about one symbol): Ne(x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -I, evaluate=False)
Residual = Abs(cos(atan(x))) - cos(atan(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-130-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-130-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cos(x))
Residual = Abs(log(cos(x))) - log(1 / cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-130-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-130-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) < pi / 2
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cos(x))
Residual = Abs(log(cos(x))) - log(1 / cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-130-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-130-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cos(x))
Residual = Abs(log(cos(x))) - log(1 / cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-131-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-131-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = Abs(log(cosh(x))) - log(cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-131-condf · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-131-condf', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = Abs(log(cosh(x))) - log(cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-131-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-131-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = Abs(log(cosh(x))) - log(cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-132-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-132-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(sin(x))
Residual = Abs(log(sin(x))) - (-log(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-132-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-132-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): x >= 0
# dropped (not a unary fact about one symbol): x <= pi
# dropped (not a unary fact about one symbol): ~Q.zero(sin(x))
Residual = Abs(log(sin(x))) - (-log(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-132-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-132-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(sin(x))
Residual = Abs(log(sin(x))) - (-log(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-133-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-133-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(tanh(x))
Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-133-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-133-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(tanh(x))
Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-133-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-133-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(tanh(x))
Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-136-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-136-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, nonnegative=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(exp(1)) > 0)
Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-136-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-136-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(exp(1)) > 0)
Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-137-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-137-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
Residual = Abs(Pow(x, pi)) - Pow(x, pi)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-137-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-137-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, nonnegative=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
Residual = Abs(Pow(x, pi)) - Pow(x, pi)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-137-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-137-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
Residual = Abs(Pow(x, pi)) - Pow(x, pi)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-14-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-14-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = -sin(x) - sin(-x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-145-cond2 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-145-cond2', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= 1
Residual = Abs(sin(acos(x))) - cos(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-145-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-145-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): x > 1
Residual = Abs(sin(acos(x))) - cos(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-145-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-145-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = Abs(sin(acos(x))) - cos(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-147-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-147-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(asinh(x)))
# dropped (not a unary fact about one symbol): Ne(1 / x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, -I, evaluate=False)
Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-147-cond · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-147-cond', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(asinh(x)))
# dropped (not a unary fact about one symbol): Ne(1 / x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, -I, evaluate=False)
Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-151-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-151-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = acos(cos(asin(x))) - Abs(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-151-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-151-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= 1
Residual = acos(cos(asin(x))) - Abs(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-151-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-151-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = acos(cos(asin(x))) - Abs(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-153-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-153-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = acos(cos(cos(x))) - Abs(cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-154-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-154-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = acos(cos(sin(x))) - Abs(sin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-154-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-154-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = acos(cos(sin(x))) - Abs(sin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-156-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-156-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= 1
Residual = acos(sin(acos(x))) - Abs(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-156-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-156-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = acos(sin(acos(x))) - Abs(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-159-cond2 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-159-cond2', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): x <= 1
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = acos(tanh(Abs(x))) - asin(1 / cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-159-cond3 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-159-cond3', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= pi / 2
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = acos(tanh(Abs(x))) - asin(1 / cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-162-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-162-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, real=True)
# dropped (not a unary fact about one symbol): re(x) >= 0
Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-162-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-162-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True, negative=True)
Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-162-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-162-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-165-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-165-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
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

# ---- case sp-acj4-171-cond · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-171-cond', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Abs(im(x)) < pi
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = asin(sin(tanh(x))) - tanh(x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-171-cond2 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-171-cond2', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = asin(sin(tanh(x))) - tanh(x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-173-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-173-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = asin(tanh(Abs(x))) - acos(1 / cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-176-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-176-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = atan(Abs(sinh(x))) - acos(1 / cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-177-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-177-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
Residual = atan(Abs(tan(x))) - Abs(asin(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-179-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-179-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
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

# ---- case sp-acj4-179-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-179-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(sinh(acos(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(acos(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(acos(x)))
Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-180-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-180-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Ne(sinh(acosh(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(acosh(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(acosh(x)))
Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-180-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-180-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
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

# ---- case sp-acj4-180-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-180-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(sinh(acosh(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(acosh(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(acosh(x)))
Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-181-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-181-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
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

# ---- case sp-acj4-181-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-181-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(sinh(asin(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(asin(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(asin(x)))
Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-183-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-183-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(sinh(log(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(log(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(log(x)))
Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-183-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-183-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
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

# ---- case sp-acj4-183-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-183-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(sinh(log(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(log(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(log(x)))
Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-185-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-185-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(cos(x)))
# dropped (not a unary fact about one symbol): Ne(tan(cos(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(tan(cos(x)), -I, evaluate=False)
Residual = atan(tan(cos(x))) - cos(x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-186-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-186-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(sin(x)))
# dropped (not a unary fact about one symbol): Ne(tan(sin(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(tan(sin(x)), -I, evaluate=False)
Residual = atan(tan(sin(x))) - sin(x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-187-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-187-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True)
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

# ---- case sp-acj4-189-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-189-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(cos(asin(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(cos(asin(x)), -1, evaluate=False)
Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-189-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-189-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(cos(asin(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(cos(asin(x)), -1, evaluate=False)
Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-190-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-190-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
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

# ---- case sp-acj4-190-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-190-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True, zero=False)
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

# ---- case sp-acj4-190-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-190-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(cos(atan(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(cos(atan(x)), -1, evaluate=False)
Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-191-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-191-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(sin(acos(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(acos(x)), -1, evaluate=False)
Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-191-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-191-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(sin(acos(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(acos(x)), -1, evaluate=False)
Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-191-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-191-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(sin(acos(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(acos(x)), -1, evaluate=False)
Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-194-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-194-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(sin(cos(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(cos(x)), -1, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(cos(x)))
Residual = atanh(sin(cos(x))) - asinh(tan(cos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-195-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-195-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(sin(sin(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(sin(x)), -1, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(sin(x)))
Residual = atanh(sin(sin(x))) - asinh(tan(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-196-cond2 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-196-cond2', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True)
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

# ---- case sp-acj4-196-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-196-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(sin(tanh(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(tanh(x)), -1, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(x)))
Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-20-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-20-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = sinh(Abs(x)) - Abs(sinh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-20-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-20-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True)
Residual = sinh(Abs(x)) - Abs(sinh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-200-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-200-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True)
Residual = cos(asin(sin(x))) - Abs(cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-202-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-202-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): Ne(tan(x), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(tan(x), -I, evaluate=False)
Residual = cos(atan(tan(x))) - Abs(cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-203-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-203-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = cos(log(1 / x)) - cos(log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-203-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-203-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): re(x) >= 0
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = cos(log(1 / x)) - cos(log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-203-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-203-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = cos(log(1 / x)) - cos(log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-205-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-205-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
Residual = cosh(asinh(tan(x))) - Abs(1 / cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-213-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-213-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(-10 / x)
Residual = 1 / (-10 / x) - (x / -10)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-216-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-216-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(-4 / x)
Residual = 1 / (-4 / x) - (x / -4)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-218-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-218-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(-6 / x)
Residual = 1 / (-6 / x) - (x / -6)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-22-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-22-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = tanh(Abs(x)) - Abs(tanh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-22-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-22-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = tanh(Abs(x)) - Abs(tanh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-220-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-220-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(-8 / x)
Residual = 1 / (-8 / x) - (x / -8)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-229-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-229-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(pi, x))
Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-233-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-233-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, pi))
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(-pi) > 0)
Residual = 1 / Pow(x, pi) - Pow(x, -pi)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-234-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, x))
# dropped (not a unary fact about one symbol): Or(~Q.zero(1 / x), re(x) > 0)
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-234-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
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

# ---- case sp-acj4-234-cond2 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-234-cond2', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', integer=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, x))
# dropped (not a unary fact about one symbol): Or(~Q.zero(1 / x), re(x) > 0)
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-234-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, x))
# dropped (not a unary fact about one symbol): Or(~Q.zero(1 / x), re(x) > 0)
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-241-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-241-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(real_root(x, 3))
Residual = log(real_root(x, 3)) - (log(x) / 3)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-243-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-243-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, real=True, zero=False)
# dropped (not a unary fact about one symbol): re(x) > 0
# dropped (not a unary fact about one symbol): ~Q.zero(real_root(x, 5))
Residual = log(real_root(x, 5)) - (log(x) / 5)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-245-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-245-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, real=True, zero=False)
# dropped (not a unary fact about one symbol): re(x) > 0
# dropped (not a unary fact about one symbol): ~Q.zero(real_root(x, 7))
Residual = log(real_root(x, 7)) - (log(x) / 7)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-247-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-247-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(real_root(x, 9))
Residual = log(real_root(x, 9)) - (log(x) / 9)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-248-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-248-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= 1
Residual = -Abs(asin(x)) - asin(-Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-248-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-248-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = -Abs(asin(x)) - asin(-Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-249-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-249-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = -Abs(asinh(x)) - asinh(-Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-251-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-251-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
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

# ---- case sp-acj4-251-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-251-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
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

# ---- case sp-acj4-252-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-252-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = -Abs(sinh(x)) - sinh(-Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-252-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-252-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = -Abs(sinh(x)) - sinh(-Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-253-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-253-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = -Abs(tanh(x)) - tanh(-Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-253-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-253-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = -Abs(tanh(x)) - tanh(-Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-256-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-256-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(-exp(x))
Residual = -exp(-x) - (1 / -exp(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-260-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-260-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cos(x))
Residual = -log(cos(x)) - log(1 / cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-260-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-260-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Abs(re(x)) < pi / 2
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cos(x))
Residual = -log(cos(x)) - log(1 / cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-260-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-260-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cos(x))
Residual = -log(cos(x)) - log(1 / cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-261-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-261-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cosh(x))
Residual = -log(cosh(x)) - log(1 / cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-261-cond · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-261-cond', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): re(x) > 0
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cosh(x))
Residual = -log(cosh(x)) - log(1 / cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-261-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-261-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cosh(x))
Residual = -log(cosh(x)) - log(1 / cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-266-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = -sin(log(x)) - sin(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-266-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): re(x) >= 0
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = -sin(log(x)) - sin(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-condf · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-266-condf', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, negative=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = -sin(log(x)) - sin(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-266-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = -sin(log(x)) - sin(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-267-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(1 / x)))
Residual = -tan(log(x)) - tan(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-267-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
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

# ---- case sp-acj4-267-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-267-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True, negative=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(1 / x)))
Residual = -tan(log(x)) - tan(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-267-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(1 / x)))
Residual = -tan(log(x)) - tan(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-274-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-274-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = Pow(Abs(x), -2) - Pow(x, -2)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-275-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-275-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = Pow(Abs(x), -3) - Abs(Pow(x, -3))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-276-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-276-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = Pow(Abs(x), -4) - Pow(x, -4)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-278-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-278-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = Pow(Abs(x), -6) - Pow(x, -6)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-283-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-283-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = Pow(Abs(x), 2) - (x * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-283-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-283-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True)
Residual = Pow(Abs(x), 2) - (x * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-283-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-283-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = Pow(Abs(x), 2) - (x * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-284-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-284-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = Pow(Abs(x), 3) - Abs(Pow(x, 3))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-286-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-286-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = Pow(Abs(x), 5) - Abs(Pow(x, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-287-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-287-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True)
Residual = Pow(Abs(x), 6) - Pow(x, 6)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-288-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-288-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = Pow(Abs(x), 7) - Abs(Pow(x, 7))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-289-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-289-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True)
Residual = Pow(Abs(x), 8) - Pow(x, 8)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-289-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-289-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = Pow(Abs(x), 8) - Pow(x, 8)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-29-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-29-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, positive=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, 3))
Residual = 3 * log(x) - log(Pow(x, 3))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-29-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-29-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, 3))
Residual = 3 * log(x) - log(Pow(x, 3))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-29-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-29-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, 3))
Residual = 3 * log(x) - log(Pow(x, 3))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-3-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-3-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = asinh(sinh(x)) - x
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-30-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-30-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = 4 * Abs(x) - Abs(-4 * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-31-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-31-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = 5 * Abs(x) - Abs(-5 * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-326-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-326-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = Pow(exp(x), 2) - exp(2 * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-33-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-33-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = 6 * Abs(x) - Abs(-6 * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-334-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-334-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(exp(x)), re(exp(1)) > 0)
Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-334-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-334-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): And(im(x) > -pi, im(x) <= pi)
# dropped (not a unary fact about one symbol): Or(~Q.zero(exp(x)), re(exp(1)) > 0)
Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-335-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-335-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(exp(x)), re(pi) > 0)
Residual = Pow(exp(x), pi) - exp(pi * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-335-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-335-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): And(im(x) > -pi, im(x) <= pi)
# dropped (not a unary fact about one symbol): Or(~Q.zero(exp(x)), re(pi) > 0)
Residual = Pow(exp(x), pi) - exp(pi * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-336-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-336-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(exp(x)), re(x) > 0)
Residual = Pow(exp(x), x) - exp(x * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-336-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-336-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): And(im(x) > -pi, im(x) <= pi)
# dropped (not a unary fact about one symbol): Or(~Q.zero(exp(x)), re(x) > 0)
Residual = Pow(exp(x), x) - exp(x * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-343-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-343-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = Pow(1 / pi, x) - Pow(pi, -x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-343-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-343-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = Pow(1 / pi, x) - Pow(pi, -x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-344-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(1 / x), re(x) > 0)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(-x) > 0)
Residual = Pow(1 / x, x) - Pow(x, -x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-344-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): re(x) >= 0
# dropped (not a unary fact about one symbol): Or(~Q.zero(1 / x), re(x) > 0)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(-x) > 0)
Residual = Pow(1 / x, x) - Pow(x, -x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-cond2 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-344-cond2', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', integer=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(1 / x), re(x) > 0)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(-x) > 0)
Residual = Pow(1 / x, x) - Pow(x, -x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-344-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(1 / x), re(x) > 0)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(-x) > 0)
Residual = Pow(1 / x, x) - Pow(x, -x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-35-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-35-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, 7))
Residual = 7 * log(x) - log(Pow(x, 7))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-354-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-354-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(log(5)) > 0)
Residual = Pow(x, log(5)) - Pow(5, log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-356-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-356-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(log(7)) > 0)
Residual = Pow(x, log(7)) - Pow(7, log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-359-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-359-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(log(pi)) > 0)
Residual = Pow(x, log(pi)) - Pow(pi, log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-364-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-364-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = real_root(Abs(x), 3) - Abs(real_root(x, 3))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-367-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-367-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = real_root(Abs(x), 9) - Abs(real_root(x, 9))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-368-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-368-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Q.real(acos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(acos(x))
Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-368-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-368-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Q.real(acos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(acos(x))
Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-369-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-369-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Q.real(acos(x))
Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-369-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-369-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Q.real(acos(x))
Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-370-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-370-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Q.real(acosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(acosh(x))
Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-370-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-370-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Q.real(acosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(acosh(x))
Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-371-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-371-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Q.real(acosh(x))
Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-371-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-371-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Q.real(acosh(x))
Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-372-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-372-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Q.real(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-372-cond · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-372-cond', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): re(x) > 0
# dropped (not a unary fact about one symbol): Q.real(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-372-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-372-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-373-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-373-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Q.real(cosh(x))
Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-373-cond · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-373-cond', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): re(x) > 0
# dropped (not a unary fact about one symbol): Q.real(cosh(x))
Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-373-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-373-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-376-cond2 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-376-cond2', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Abs(im(x)) < pi
# dropped (not a unary fact about one symbol): Q.real(exp(x))
# dropped (not a unary fact about one symbol): ~Q.zero(exp(x))
Residual = real_root(exp(x), -3) - exp(x / -3)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-378-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-378-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(exp(x))
Residual = real_root(exp(x), -5) - exp(x / -5)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-38-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-38-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, 9))
Residual = 9 * log(x) - log(Pow(x, 9))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-380-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-380-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(exp(x))
Residual = real_root(exp(x), -7) - exp(x / -7)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-385-cond · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-385-cond', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): re(x) > 0
# dropped (not a unary fact about one symbol): Q.real(exp(x))
Residual = real_root(exp(x), 3) - exp(x / 3)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-387-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-387-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Q.real(exp(x))
Residual = real_root(exp(x), 5) - exp(x / 5)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-389-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-389-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Q.real(exp(x))
Residual = real_root(exp(x), 7) - exp(x / 7)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-392-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-392-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= 1
Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-392-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-392-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-394-cond · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-394-cond', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) < 1
# dropped (not a unary fact about one symbol): Ne(x, 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -1, evaluate=False)
Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-394-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-394-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(x, 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -1, evaluate=False)
Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-395-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-395-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-396-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-396-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-396-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-396-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-397-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-397-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = sin(Abs(tanh(x))) - Abs(sin(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-399-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-399-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True)
Residual = sin(acos(sin(x))) - Abs(cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-40-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-40-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = Abs(x) * pi - Abs(pi * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-402-cond · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-402-cond', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
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

# ---- case sp-acj4-402-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-402-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(Abs(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -1, evaluate=False)
Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-403-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = sin(-log(x)) - sin(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-403-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): re(x) >= 0
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = sin(-log(x)) - sin(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-condf · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-403-condf', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, negative=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = sin(-log(x)) - sin(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-403-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = sin(-log(x)) - sin(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-404-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-404-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-404-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-404-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-410-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-410-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(sinh(x))
Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-412-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-412-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) < 1
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(asin(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(asin(x)))
Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-412-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-412-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(asin(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(asin(x)))
Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-413-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-413-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(cos(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(cos(x)))
Residual = tan(Abs(cos(x))) - Abs(tan(cos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-414-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-414-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(sin(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(sin(x)))
Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-414-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-414-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(sin(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(sin(x)))
Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-415-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-415-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(tanh(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(x)))
Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-415-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-415-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(tanh(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(x)))
Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-416-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-416-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= 1
# dropped (not a unary fact about one symbol): ~Q.zero(cos(acos(Abs(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(acos(x)))
Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-416-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-416-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(acos(Abs(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(acos(x)))
Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-417-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-417-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) < 1
# dropped (not a unary fact about one symbol): ~Q.zero(cos(asin(Abs(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(asin(x)))
Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-417-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-417-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(asin(Abs(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(asin(x)))
Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-420-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(-log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(1 / x)))
Residual = tan(-log(x)) - tan(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-420-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
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

# ---- case sp-acj4-420-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-420-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True, negative=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(-log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(1 / x)))
Residual = tan(-log(x)) - tan(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-420-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(-log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(1 / x)))
Residual = tan(-log(x)) - tan(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-421-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-421-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(Abs(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(x)))
Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-421-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-421-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(Abs(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(x)))
Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-422-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-422-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, -I, evaluate=False)
Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-422-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-422-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, -I, evaluate=False)
Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-423-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-423-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(acosh(Abs(x))))
Residual = tanh(acosh(Abs(x))) - cos(asin(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-424-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-424-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, -I, evaluate=False)
Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-424-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-424-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, -I, evaluate=False)
Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-428-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-428-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): x <= 1
Residual = atan(sinh(x)) - asin(tanh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-428-cond3 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-428-cond3', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): x >= 0
# dropped (not a unary fact about one symbol): x <= pi
Residual = atan(sinh(x)) - asin(tanh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-430-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, x))
Residual = log(x) * x - log(Pow(x, x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-430-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, positive=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, x))
Residual = log(x) * x - log(Pow(x, x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-cond2 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-430-cond2', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Abs(x) < 1
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, x))
Residual = log(x) * x - log(Pow(x, x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-430-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, x))
Residual = log(x) * x - log(Pow(x, x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-432-cond3 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-432-cond3', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Abs(x) <= pi / 2
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = acos(Abs(tanh(x))) - asin(1 / cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-433-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
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

# ---- case sp-acj4-433-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-433-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
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

# ---- case sp-acj4-433-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-433-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True, negative=True, zero=False)
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

# ---- case sp-acj4-433-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-433-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
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

# ---- case sp-acj4-442-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-442-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(log(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / log(x))
Residual = -log(log(x)) - log(1 / log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-442-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(log(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / log(x))
Residual = -log(log(x)) - log(1 / log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-cond4 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-442-cond4', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', integer=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(log(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / log(x))
Residual = -log(log(x)) - log(1 / log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-442-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(log(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / log(x))
Residual = -log(log(x)) - log(1 / log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-446-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-446-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): Ne(x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(atan(x))))
Residual = tan(Abs(atan(x))) - Abs(x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-449-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-449-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(-log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(log(1 / x)))
Residual = tanh(-log(x)) - tanh(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-450-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-450-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
Residual = x / x - 1
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-450-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-450-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
Residual = x / x - 1
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-451-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-451-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
Residual = 0 / x - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-451-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-451-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
Residual = 0 / x - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-46-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-46-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): And(im(x) > -pi, im(x) <= pi)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(2, x))
Residual = log(2) * x - log(Pow(2, x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-5-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
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

# ---- case sp-acj4-5-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-5-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(Abs(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -1, evaluate=False)
Residual = atanh(Abs(x)) - Abs(atanh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-50-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-50-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(6, x))
Residual = log(6) * x - log(Pow(6, x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-50-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-50-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(6, x))
Residual = log(6) * x - log(Pow(6, x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-51-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-51-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(7, x))
Residual = log(7) * x - log(Pow(7, x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5372-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-5372-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = sin(asin(Integer(1) / -4)) - Rational(-1, 4)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5382-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-5382-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = sinh(log(Integer(1) / 4)) - Rational(-15, 8)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5385-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-5385-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = sinh(-log(4)) - Rational(-15, 8)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-55-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-55-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(exp(1)) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, exp(1)))
Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-55-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-55-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, positive=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(exp(1)) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, exp(1)))
Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-55-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-55-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(exp(1)) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, exp(1)))
Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-56-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, pi))
Residual = log(x) * pi - log(Pow(x, pi))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-56-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, positive=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, pi))
Residual = log(x) * pi - log(Pow(x, pi))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-condf · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-56-condf', 'sympy-simplify', 'false', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True, imaginary=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, pi))
Residual = log(x) * pi - log(Pow(x, pi))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-56-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, pi))
Residual = log(x) * pi - log(Pow(x, pi))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-6-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-6-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): Ne(tanh(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(tanh(x), -1, evaluate=False)
Residual = atanh(tanh(x)) - x
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-6-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-6-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(tanh(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(tanh(x), -1, evaluate=False)
Residual = atanh(tanh(x)) - x
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-7-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-7-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = 1 / Abs(x) - Abs(1 / x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-73-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-73-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
# dropped (not a unary fact about one symbol): ~Q.zero(-Abs(x))
Residual = -1 / Abs(x) - (1 / -Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-80-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-80-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(-cos(x))
Residual = -1 / cos(x) - (1 / -cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-806-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-806-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = cosh(0) - 1
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-813-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-813-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = sinh(0) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-816-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-816-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = tanh(0) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-819-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-819-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = 0 / pi - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-83-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-83-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(log(x))
# dropped (not a unary fact about one symbol): ~Q.zero(-log(x))
Residual = -1 / log(x) - (1 / -log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-837-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-837-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = Pow(0, pi) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-848-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-848-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = sinh(log(4)) - Rational(15, 8)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-86-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-86-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(tan(x))
# dropped (not a unary fact about one symbol): ~Q.zero(-tan(x))
Residual = -1 / tan(x) - (1 / -tan(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-868-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-868-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = 0 * acosh(7) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-9-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-9-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): ~Q.zero(exp(x))
Residual = log(exp(x)) - x
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-9-cond · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-9-cond', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
# dropped (not a unary fact about one symbol): And(im(x) > -pi, im(x) <= pi)
# dropped (not a unary fact about one symbol): ~Q.zero(exp(x))
Residual = log(exp(x)) - x
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-90-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-90-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = 3 / Abs(x) - Abs(-3 / x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-90-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-90-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = 3 / Abs(x) - Abs(-3 / x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-911-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-911-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = 0 / asin(-1) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-927-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-927-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''Residual = 0 / asinh(4) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-94-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-94-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = 7 / Abs(x) - Abs(-7 / x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-99-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-99-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = Abs(x) / 3 - Abs(x / -3)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-99-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-99-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = Abs(x) / 3 - Abs(x / -3)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

print(f"done: {sum(_n.values())} case run(s): {_n['true']} true, {_n['false']} false, {_n['null']} null")
