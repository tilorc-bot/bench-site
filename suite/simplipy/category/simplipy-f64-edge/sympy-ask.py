# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# suite simplipy · category simplipy-f64-edge · system sympy-ask (45 cases listed)
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


# ---- case sp-acj4-0-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-0-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = acosh(cosh(x)) - Abs(x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-115-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-115-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -4)))
Residual = log(x) / -4 - log(real_root(x, -4))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-116-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-116-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -6)))
Residual = log(x) / -6 - log(real_root(x, -6))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-130-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-130-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = Abs(log(cos(x))) - log(1 / cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-151-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-151-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = acos(cos(asin(x))) - Abs(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-154-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-154-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = acos(cos(sin(x))) - Abs(sin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-156-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-156-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = acos(sin(acos(x))) - Abs(asin(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-180-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-180-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-183-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-183-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-189-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-189-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-190-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-190-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-191-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-191-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-203-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-203-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = cos(log(1 / x)) - cos(log(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-229-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-229-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Pow(pi, x)))
Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-234-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-234-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
Residual = 1 / Pow(x, x) - Pow(1 / x, x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-241-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-241-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(real_root(x, 3)), ~Q.zero(x))
Residual = log(real_root(x, 3)) - (log(x) / 3)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-247-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-247-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(real_root(x, 9)), ~Q.zero(x))
Residual = log(real_root(x, 9)) - (log(x) / 9)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-260-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-260-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
Residual = -log(cos(x)) - log(1 / cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-261-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-261-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
Residual = -log(cosh(x)) - log(1 / cosh(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-266-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-266-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = -sin(log(x)) - sin(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-267-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-267-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = -tan(log(x)) - tan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-29-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-29-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
Residual = 3 * log(x) - log(Pow(x, 3))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-3-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-3-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = asinh(sinh(x)) - x
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-343-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-343-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = Pow(1 / pi, x) - Pow(pi, -x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-344-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-344-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
Residual = Pow(1 / x, x) - Pow(x, -x)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-378-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-378-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(exp(x)))
Residual = real_root(exp(x), -5) - exp(x / -5)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-380-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-380-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(exp(x)))
Residual = real_root(exp(x), -7) - exp(x / -7)
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-392-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-392-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-403-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-403-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
Residual = sin(-log(x)) - sin(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-410-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-410-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(sinh(x)))
Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-416-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-416-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-420-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-420-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
Residual = tan(-log(x)) - tan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-430-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-430-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
Residual = log(x) * x - log(Pow(x, x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-433-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-433-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
Residual = atan(-log(x)) - atan(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-442-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-442-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
Residual = -log(log(x)) - log(1 / log(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-449-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-449-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cosh(-log(x))), ~Q.zero(1 / x), ~Q.zero(cosh(log(1 / x))))
Residual = tanh(-log(x)) - tanh(log(1 / x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-450-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-450-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x))
Residual = x / x - 1
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-451-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-451-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x))
Residual = 0 / x - 0
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-50-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-50-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(Pow(6, x)))
Residual = log(6) * x - log(Pow(6, x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-55-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-55-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-56-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
_n[_run('sp-acj4-56-real', 'sympy-ask', 'contingent', 'the run sympy-ask-20261015-024703 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
Residual = log(x) * pi - log(Pow(x, pi))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-6-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
_n[_run('sp-acj4-6-real', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
Residual = atanh(tanh(x)) - x
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-806-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-806-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = cosh(0) - 1
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-813-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-813-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = sinh(0) - 0
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

# ---- case sp-acj4-816-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
_n[_run('sp-acj4-816-ground', 'sympy-ask', 'true', 'the run sympy-ask-20261015-024703 answered true (solved)', _SETUP1, r'''Assum = And()
Residual = tanh(0) - 0
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
Answer = ask(Q.zero(Residual), Assum)
print(Residual, Answer, sep='\n')
''')] += 1

print(f"done: {sum(_n.values())} case run(s): {_n['true']} true, {_n['false']} false, {_n['null']} null")
