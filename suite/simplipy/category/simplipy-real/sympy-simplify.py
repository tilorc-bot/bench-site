# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# suite simplipy · category simplipy-real · system sympy-simplify (70 cases listed)
# 70 case run(s).  Each runs in a fresh copy of its setup's namespace, as in the
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


# ---- case sp-acj4-1-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-1-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = asin(Abs(x)) - Abs(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-102-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-102-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = Abs(x) / 6 - Abs(x / -6)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-108-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-108-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = Abs(x) / x - (x / Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-120-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-120-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = pi / Abs(x) - Abs(pi / x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-127-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-127-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(exp(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(exp(x), -1, evaluate=False)
Residual = Abs(atanh(exp(x))) - atanh(exp(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-128-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-128-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = Abs(cos(asin(x))) - cos(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-131-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-131-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = Abs(log(cosh(x))) - log(cosh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-132-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-132-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(sin(x))
Residual = Abs(log(sin(x))) - (-log(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-133-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-133-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(tanh(x))
Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-136-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-136-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(exp(1)) > 0)
Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-137-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-137-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
Residual = Abs(Pow(x, pi)) - Pow(x, pi)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-14-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-14-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = -sin(x) - sin(-x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-145-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-145-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = Abs(sin(acos(x))) - cos(asin(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-162-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-162-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-179-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-179-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(sinh(acos(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(acos(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(acos(x)))
Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-181-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-181-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(sinh(asin(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(asin(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(asin(x)))
Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-185-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-185-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(cos(x)))
# dropped (not a unary fact about one symbol): Ne(tan(cos(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(tan(cos(x)), -I, evaluate=False)
Residual = atan(tan(cos(x))) - cos(x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-194-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-194-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
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
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-195-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(sin(sin(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(sin(x)), -1, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(sin(x)))
Residual = atanh(sin(sin(x))) - asinh(tan(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-196-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-196-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(sin(tanh(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(tanh(x)), -1, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(x)))
Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-218-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-218-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(-6 / x)
Residual = 1 / (-6 / x) - (x / -6)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-22-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-22-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = tanh(Abs(x)) - Abs(tanh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-220-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-220-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(-8 / x)
Residual = 1 / (-8 / x) - (x / -8)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-233-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-233-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, pi))
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(-pi) > 0)
Residual = 1 / Pow(x, pi) - Pow(x, -pi)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-248-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-248-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = -Abs(asin(x)) - asin(-Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-249-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-249-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = -Abs(asinh(x)) - asinh(-Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-251-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-251-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
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

# ---- case sp-acj4-252-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-252-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = -Abs(sinh(x)) - sinh(-Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-253-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-253-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = -Abs(tanh(x)) - tanh(-Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-256-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-256-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(-exp(x))
Residual = -exp(-x) - (1 / -exp(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-275-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-275-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = Pow(Abs(x), -3) - Abs(Pow(x, -3))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-276-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-276-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = Pow(Abs(x), -4) - Pow(x, -4)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-283-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-283-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = Pow(Abs(x), 2) - (x * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-286-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-286-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = Pow(Abs(x), 5) - Abs(Pow(x, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-289-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-289-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = Pow(Abs(x), 8) - Pow(x, 8)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-31-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-31-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = 5 * Abs(x) - Abs(-5 * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-326-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-326-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = Pow(exp(x), 2) - exp(2 * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-33-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-33-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = 6 * Abs(x) - Abs(-6 * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-35-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-35-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, 7))
Residual = 7 * log(x) - log(Pow(x, 7))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-354-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-354-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(log(5)) > 0)
Residual = Pow(x, log(5)) - Pow(5, log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-356-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-356-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(log(7)) > 0)
Residual = Pow(x, log(7)) - Pow(7, log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-359-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-359-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(log(pi)) > 0)
Residual = Pow(x, log(pi)) - Pow(pi, log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-364-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-364-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = real_root(Abs(x), 3) - Abs(real_root(x, 3))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-367-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-367-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = real_root(Abs(x), 9) - Abs(real_root(x, 9))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-368-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-368-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Q.real(acos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(acos(x))
Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-369-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-369-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Q.real(acos(x))
Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-370-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-370-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Q.real(acosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(acosh(x))
Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-371-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-371-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Q.real(acosh(x))
Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-372-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-372-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-373-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-373-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-38-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-38-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, 9))
Residual = 9 * log(x) - log(Pow(x, 9))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-394-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-394-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(x, 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -1, evaluate=False)
Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-395-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-395-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-396-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-396-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-397-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-397-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = sin(Abs(tanh(x))) - Abs(sin(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-402-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-402-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(Abs(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -1, evaluate=False)
Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-404-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-404-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-412-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-412-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(asin(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(asin(x)))
Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-413-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-413-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(cos(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(cos(x)))
Residual = tan(Abs(cos(x))) - Abs(tan(cos(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-414-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-414-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(sin(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(sin(x)))
Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-415-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-415-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(tanh(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(x)))
Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-417-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-417-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(asin(Abs(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(asin(x)))
Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-421-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (no verdict)
_n[_run('sp-acj4-421-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(Abs(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(x)))
Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered null (declined correctly)
_n[_run('sp-acj4-5-real', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174713 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): Ne(Abs(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -1, evaluate=False)
Residual = atanh(Abs(x)) - Abs(atanh(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-73-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-73-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
# dropped (not a unary fact about one symbol): ~Q.zero(-Abs(x))
Residual = -1 / Abs(x) - (1 / -Abs(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-80-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-80-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(-cos(x))
Residual = -1 / cos(x) - (1 / -cos(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-83-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-83-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(log(x))
# dropped (not a unary fact about one symbol): ~Q.zero(-log(x))
Residual = -1 / log(x) - (1 / -log(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-86-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-86-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(tan(x))
# dropped (not a unary fact about one symbol): ~Q.zero(-tan(x))
Residual = -1 / tan(x) - (1 / -tan(x))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-90-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-90-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
Residual = 3 / Abs(x) - Abs(-3 / x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-99-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174713 answered true (solved)
_n[_run('sp-acj4-99-real', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174713 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = Abs(x) / 3 - Abs(x / -3)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

print(f"done: {sum(_n.values())} case run(s): {_n['true']} true, {_n['false']} false, {_n['null']} null")
