# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# suite simplipy · category simplipy-f64-edge · system sympy-simplify (45 cases listed)
# 45 case run(s).  Each runs in a fresh copy of its setup's namespace, as in the
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


# ---- case sp-acj4-0-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-0-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = acosh(cosh(x)) - Abs(x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-115-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-115-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): x > 0
# dropped (not a unary fact about one symbol): ~Q.zero(real_root(x, -4))
Residual = log(x) / -4 - log(real_root(x, -4))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-116-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-116-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): x > 0
# dropped (not a unary fact about one symbol): ~Q.zero(real_root(x, -6))
Residual = log(x) / -6 - log(real_root(x, -6))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-130-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-130-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cos(x))
Residual = Abs(log(cos(x))) - log(1 / cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-151-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-151-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = acos(cos(asin(x))) - Abs(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-154-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-154-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = acos(cos(sin(x))) - Abs(sin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-156-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-156-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = acos(sin(acos(x))) - Abs(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-180-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-180-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(sinh(acosh(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(acosh(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(acosh(x)))
Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-183-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-183-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(sinh(log(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(log(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(log(x)))
Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-189-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-189-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(cos(asin(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(cos(asin(x)), -1, evaluate=False)
Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-190-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-190-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(cos(atan(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(cos(atan(x)), -1, evaluate=False)
Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-191-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-191-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Ne(sin(acos(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(acos(x)), -1, evaluate=False)
Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-203-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-203-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = cos(log(1 / x)) - cos(log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-229-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-229-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(pi, x))
Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-234-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
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
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-241-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(real_root(x, 3))
Residual = log(real_root(x, 3)) - (log(x) / 3)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-247-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-247-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(real_root(x, 9))
Residual = log(real_root(x, 9)) - (log(x) / 9)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-260-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-260-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cos(x))
Residual = -log(cos(x)) - log(1 / cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-261-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-261-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cosh(x))
Residual = -log(cosh(x)) - log(1 / cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-266-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = -sin(log(x)) - sin(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-267-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(1 / x)))
Residual = -tan(log(x)) - tan(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-29-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-29-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, 3))
Residual = 3 * log(x) - log(Pow(x, 3))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-3-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-3-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = asinh(sinh(x)) - x
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-343-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-343-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = Pow(1 / pi, x) - Pow(pi, -x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-344-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(1 / x), re(x) > 0)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(-x) > 0)
Residual = Pow(1 / x, x) - Pow(x, -x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-378-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-378-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(exp(x))
Residual = real_root(exp(x), -5) - exp(x / -5)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-380-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-380-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(exp(x))
Residual = real_root(exp(x), -7) - exp(x / -7)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-392-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-392-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-403-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
Residual = sin(-log(x)) - sin(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-410-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-410-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(sinh(x))
Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-416-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-416-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(acos(Abs(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(acos(x)))
Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-420-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(-log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(1 / x)))
Residual = tan(-log(x)) - tan(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-430-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, x))
Residual = log(x) * x - log(Pow(x, x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-433-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
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

# ---- case sp-acj4-442-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-442-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(log(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / log(x))
Residual = -log(log(x)) - log(1 / log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-449-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-449-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(-log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(log(1 / x)))
Residual = tanh(-log(x)) - tanh(log(1 / x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-450-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-450-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
Residual = x / x - 1
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-451-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-451-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
Residual = 0 / x - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-50-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-50-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(6, x))
Residual = log(6) * x - log(Pow(6, x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-55-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-55-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(exp(1)) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, exp(1)))
Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-56-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, pi))
Residual = log(x) * pi - log(Pow(x, pi))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-6-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-6-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(tanh(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(tanh(x), -1, evaluate=False)
Residual = atanh(tanh(x)) - x
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-806-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-806-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''Residual = cosh(0) - 1
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-813-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-813-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''Residual = sinh(0) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-816-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-816-ground', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''Residual = tanh(0) - 0
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

print(f"done: {sum(_n.values())} case run(s): {_n['true']} true, {_n['false']} false, {_n['null']} null")
