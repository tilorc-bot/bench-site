# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# suite simplipy · category simplipy-complex-branch · system satrefine-refine (80 cases listed)
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
import satrefine
''', _SETUP1)

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

print(f"done: {sum(_n.values())} case run(s): {_n['true']} true, {_n['false']} false, {_n['null']} null")
