# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# suite simplipy · category simplipy-conditional · system sympy-ask (92 cases listed)
# 92 case run(s).  Each runs in a fresh copy of its setup's namespace, as in the
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


# ---- case sp-acj4-1-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-1-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = asin(Abs(x)) - Abs(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-108-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-108-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), ~Q.zero(Abs(x)))
Residual = Abs(x) / x - (x / Abs(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-124-condf · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-124-condf', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)))
Residual = Abs(asin(tanh(x))) - acos(1 / cosh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-127-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-127-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, Ne(exp(x), 1, evaluate=False), Ne(exp(x), -1, evaluate=False))
Residual = Abs(atanh(exp(x))) - atanh(exp(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-128-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-128-cond2', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = Abs(cos(asin(x))) - cos(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-128-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-128-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x > 1)
Residual = Abs(cos(asin(x))) - cos(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-129-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-129-cond', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False))
Residual = Abs(cos(atan(x))) - cos(atan(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-130-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-130-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < pi / 2, ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = Abs(log(cos(x))) - log(1 / cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-131-condf · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-131-condf', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)))
Residual = Abs(log(cosh(x))) - log(cosh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-132-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-132-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x >= 0, x <= pi, ~Q.zero(sin(x)))
Residual = Abs(log(sin(x))) - (-log(sin(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-133-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-133-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)), ~Q.zero(tanh(x)))
Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-136-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-136-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.nonnegative(x), Or(~Q.zero(x), re(exp(1)) > 0))
Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-137-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-137-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.nonnegative(x), Or(~Q.zero(x), re(pi) > 0))
Residual = Abs(Pow(x, pi)) - Pow(x, pi)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-145-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-145-cond2', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = Abs(sin(acos(x))) - cos(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-145-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-145-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x > 1)
Residual = Abs(sin(acos(x))) - cos(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-147-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-147-cond', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(asinh(x))), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-151-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-151-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = acos(cos(asin(x))) - Abs(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-156-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-156-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = acos(sin(acos(x))) - Abs(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-159-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-159-cond2', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x <= 1, ~Q.zero(cosh(x)))
Residual = acos(tanh(Abs(x))) - asin(1 / cosh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-159-cond3 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-159-cond3', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= pi / 2, ~Q.zero(cosh(x)))
Residual = acos(tanh(Abs(x))) - asin(1 / cosh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-162-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-162-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, Q.real(x))
Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-162-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-162-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x))
Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-171-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-171-cond', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Abs(im(x)) < pi, ~Q.zero(cosh(x)))
Residual = asin(sin(tanh(x))) - tanh(x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-171-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-171-cond2', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)))
Residual = asin(sin(tanh(x))) - tanh(x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-179-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-179-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= pi / 2, Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-180-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-180-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-181-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-181-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= pi / 2, Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-183-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-183-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-186-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-186-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cos(sin(x))), Ne(tan(sin(x)), I, evaluate=False), Ne(tan(sin(x)), -I, evaluate=False))
Residual = atan(tan(sin(x))) - sin(x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-187-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-187-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)), ~Q.zero(cos(tanh(x))), Ne(tan(tanh(x)), I, evaluate=False), Ne(tan(tanh(x)), -I, evaluate=False))
Residual = atan(tan(tanh(x))) - tanh(x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-190-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-190-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-191-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-191-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-196-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-196-cond2', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-20-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-20-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = sinh(Abs(x)) - Abs(sinh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-200-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-200-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = cos(asin(sin(x))) - Abs(cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-202-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-202-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cos(x)), Ne(tan(x), I, evaluate=False), Ne(tan(x), -I, evaluate=False))
Residual = cos(atan(tan(x))) - Abs(cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-203-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-203-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(1 / x))
Residual = cos(log(1 / x)) - cos(log(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-205-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-205-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cos(x)))
Residual = cosh(asinh(tan(x))) - Abs(1 / cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-234-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-234-cond2', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP1, r'''x = Symbol('x', integer=True)
Assum = And(Q.integer(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-243-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-243-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Q.real(x), ~Q.zero(real_root(x, 5)), ~Q.zero(x))
Residual = log(real_root(x, 5)) - (log(x) / 5)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-245-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-245-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Q.real(x), ~Q.zero(real_root(x, 7)), ~Q.zero(x))
Residual = log(real_root(x, 7)) - (log(x) / 7)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-248-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-248-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = -Abs(asin(x)) - asin(-Abs(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-251-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-251-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
Residual = -Abs(atanh(x)) - atanh(-Abs(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-260-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-260-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Abs(re(x)) < pi / 2, ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = -log(cos(x)) - log(1 / cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-261-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-261-cond', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
Residual = -log(cosh(x)) - log(1 / cosh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-266-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(1 / x))
Residual = -sin(log(x)) - sin(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-condf · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-266-condf', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = -sin(log(x)) - sin(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-267-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = -tan(log(x)) - tan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-267-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = -tan(log(x)) - tan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-283-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-283-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = Pow(Abs(x), 2) - (x * x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-287-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-287-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = Pow(Abs(x), 6) - Pow(x, 6)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-289-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-289-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = Pow(Abs(x), 8) - Pow(x, 8)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-29-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-29-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
Residual = 3 * log(x) - log(Pow(x, 3))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-29-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-29-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
Residual = 3 * log(x) - log(Pow(x, 3))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-334-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-334-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), Or(~Q.zero(exp(x)), re(exp(1)) > 0))
Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-335-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-335-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), Or(~Q.zero(exp(x)), re(pi) > 0))
Residual = Pow(exp(x), pi) - exp(pi * x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-336-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-336-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), Or(~Q.zero(exp(x)), re(x) > 0))
Residual = Pow(exp(x), x) - exp(x * x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-344-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
Residual = Pow(1 / x, x) - Pow(x, -x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-344-cond2', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP1, r'''x = Symbol('x', integer=True)
Assum = And(Q.integer(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
Residual = Pow(1 / x, x) - Pow(x, -x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-372-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-372-cond', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Q.real(cosh(x)), ~Q.zero(cosh(x)))
Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-373-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-373-cond', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Q.real(cosh(x)))
Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-376-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-376-cond2', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Abs(im(x)) < pi, Q.real(exp(x)), ~Q.zero(exp(x)))
Residual = real_root(exp(x), -3) - exp(x / -3)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-385-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-385-cond', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) > 0, Q.real(exp(x)))
Residual = real_root(exp(x), 3) - exp(x / 3)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-392-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-392-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1)
Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-394-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-394-cond', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-399-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-399-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x))
Residual = sin(acos(sin(x))) - Abs(cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-402-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-402-cond', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-403-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(1 / x))
Residual = sin(-log(x)) - sin(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-condf · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-403-condf', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = sin(-log(x)) - sin(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-412-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-412-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-416-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-416-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= 1, ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-417-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-417-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, ~Q.zero(cos(asin(Abs(x)))), ~Q.zero(cos(asin(x))))
Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-420-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = tan(-log(x)) - tan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-420-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = tan(-log(x)) - tan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-422-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-422-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-424-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-424-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-428-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-428-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x <= 1)
Residual = atan(sinh(x)) - asin(tanh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-428-cond3 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-428-cond3', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), x >= 0, x <= pi)
Residual = atan(sinh(x)) - asin(tanh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-430-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
Residual = log(x) * x - log(Pow(x, x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-430-cond2', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
Residual = log(x) * x - log(Pow(x, x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-432-cond3 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-432-cond3', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) <= pi / 2, ~Q.zero(cosh(x)))
Residual = acos(Abs(tanh(x))) - asin(1 / cosh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-433-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
Residual = atan(-log(x)) - atan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-433-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
Residual = atan(-log(x)) - atan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-442-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
Residual = -log(log(x)) - log(1 / log(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-cond4 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-442-cond4', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', integer=True)
Assum = And(Q.integer(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
Residual = -log(log(x)) - log(1 / log(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-46-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-46-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), ~Q.zero(Pow(2, x)))
Residual = log(2) * x - log(Pow(2, x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-5-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-5-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Abs(x) < 1, Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
Residual = atanh(Abs(x)) - Abs(atanh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-55-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-55-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-56-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
Residual = log(x) * pi - log(Pow(x, pi))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-56-condf', 'sympy-ask', 'false', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
Residual = log(x) * pi - log(Pow(x, pi))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-9-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-9-cond', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), ~Q.zero(exp(x)))
Residual = log(exp(x)) - x
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

print(f"done: {sum(_n.values())} case run(s): {_n['true']} true, {_n['false']} false, {_n['null']} null")
