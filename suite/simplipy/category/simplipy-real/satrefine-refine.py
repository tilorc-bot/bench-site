# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# suite simplipy · category simplipy-real · system satrefine-refine (70 cases listed)
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
import satrefine
''', _SETUP1)

_n = {'true': 0, 'false': 0, 'null': 0}


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

print(f"done: {sum(_n.values())} case run(s): {_n['true']} true, {_n['false']} false, {_n['null']} null")
