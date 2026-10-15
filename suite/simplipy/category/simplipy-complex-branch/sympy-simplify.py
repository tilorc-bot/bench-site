# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# suite simplipy · category simplipy-complex-branch · system sympy-simplify (80 cases listed)
# 80 case run(s).  Each runs in a fresh copy of its setup's namespace, as in the
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

# ---- case sp-acj4-102-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-102-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
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

# ---- case sp-acj4-151-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-151-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
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

# ---- case sp-acj4-20-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-20-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = sinh(Abs(x)) - Abs(sinh(x))
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

# ---- case sp-acj4-252-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-252-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
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

# ---- case sp-acj4-284-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (no verdict)
_n[_run('sp-acj4-284-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = Pow(Abs(x), 3) - Abs(Pow(x, 3))
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

# ---- case sp-acj4-30-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-30-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = 4 * Abs(x) - Abs(-4 * x)
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

# ---- case sp-acj4-343-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-343-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
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

# ---- case sp-acj4-396-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered null (declined correctly)
_n[_run('sp-acj4-396-complex', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261015-024958 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
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

# ---- case sp-acj4-450-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261015-024958 answered true (solved)
_n[_run('sp-acj4-450-complex', 'sympy-simplify', 'true', 'the run sympy-simplify-20261015-024958 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
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

print(f"done: {sum(_n.values())} case run(s): {_n['true']} true, {_n['false']} false, {_n['null']} null")
