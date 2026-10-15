# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# suite examples · every case · system satrefine-refine (27 cases listed)
# 27 case run(s).  Each runs in a fresh copy of its setup's namespace, as in the
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


# ---- case demo-atan2-01 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered true (solved)
_n[_run('demo-atan2-01', 'satrefine-refine', 'true', 'the run satrefine-refine-20261014-174229 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
y = Symbol('y', real=True)
Assum = And(Q.real(x), Q.real(y), Q.positive(x))
Residual = atan2(y, x) - atan(y / x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-atan2-02 · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered false (solved)
_n[_run('demo-atan2-02', 'satrefine-refine', 'false', 'the run satrefine-refine-20261014-174229 answered false (solved)', _SETUP1, r'''x = Symbol('x', real=True)
y = Symbol('y', real=True)
Assum = And(Q.real(x), Q.real(y), Q.negative(x), Q.positive(y))
Residual = atan2(y, x) - atan(y / x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-abs-01 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered true (solved)
_n[_run('demo-eq-abs-01', 'satrefine-refine', 'true', 'the run satrefine-refine-20261014-174229 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x))
Residual = Abs(x) - (-x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-abs-02 · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered null (no verdict)
_n[_run('demo-eq-abs-02', 'satrefine-refine', 'false', 'the run satrefine-refine-20261014-174229 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x))
Residual = Abs(x) - x
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-log-01 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered true (solved)
_n[_run('demo-eq-log-01', 'satrefine-refine', 'true', 'the run satrefine-refine-20261014-174229 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x))
Residual = log(exp(x)) - x
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-pow-01 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered true (solved)
_n[_run('demo-eq-pow-01', 'satrefine-refine', 'true', 'the run satrefine-refine-20261014-174229 answered true (solved)', _SETUP1, r'''n = Symbol('n', integer=True)
Assum = And(Q.integer(n))
Residual = Pow(-1, 2 * n) - 1
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-sqrt-01 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered true (solved)
_n[_run('demo-eq-sqrt-01', 'satrefine-refine', 'true', 'the run satrefine-refine-20261014-174229 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x))
Residual = sqrt(Pow(x, 2)) - x
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-sqrt-02 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered true (solved)
_n[_run('demo-eq-sqrt-02', 'satrefine-refine', 'true', 'the run satrefine-refine-20261014-174229 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sqrt(Pow(x, 2)) - Abs(x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-sqrt-03 · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered null (declined correctly)
_n[_run('demo-eq-sqrt-03', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261014-174229 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x))
Residual = sqrt(Pow(x, 2)) - x
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-sqrt-04 · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered false (solved)
_n[_run('demo-eq-sqrt-04', 'satrefine-refine', 'false', 'the run satrefine-refine-20261014-174229 answered false (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.positive(x))
Residual = sqrt(Pow(x, 2)) + 1 - x
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-trig-01 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered null (no verdict)
_n[_run('demo-eq-trig-01', 'satrefine-refine', 'true', 'the run satrefine-refine-20261014-174229 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = Pow(sin(x), 2) + Pow(cos(x), 2) - 1
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-trig-02 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered null (no verdict)
_n[_run('demo-eq-trig-02', 'satrefine-refine', 'true', 'the run satrefine-refine-20261014-174229 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x))
Residual = 2 * sin(x) * cos(x) - sin(2 * x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-log-01 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered true (solved)
_n[_run('demo-log-01', 'satrefine-refine', 'true', 'the run satrefine-refine-20261014-174229 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
y = Symbol('y', real=True)
Assum = And(Q.real(x), Q.real(y), Q.positive(x), Q.positive(y))
Residual = log(x * y) - (log(x) + log(y))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-log-02 · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered null (declined correctly)
_n[_run('demo-log-02', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261014-174229 answered null (declined correctly)', _SETUP1, r'''z = Symbol('z', complex=True)
w = Symbol('w', complex=True)
Assum = And(Q.complex(z), Q.complex(w), ~Q.zero(z), ~Q.zero(w))
Residual = log(z * w) - (log(z) + log(w))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-log-03 · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered false (solved)
_n[_run('demo-log-03', 'satrefine-refine', 'false', 'the run satrefine-refine-20261014-174229 answered false (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), Q.negative(x))
Residual = log(x) - log(-x)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-nonzero-01 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered true (solved)
_n[_run('demo-nonzero-01', 'satrefine-refine', 'true', 'the run satrefine-refine-20261014-174229 answered true (solved)', _SETUP1, r'''z = Symbol('z', complex=True)
Assum = And(Q.complex(z), Q.imaginary(z))
Residual = Abs(sign(z)) - 1
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-parity-01 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered true (solved)
_n[_run('demo-parity-01', 'satrefine-refine', 'true', 'the run satrefine-refine-20261014-174229 answered true (solved)', _SETUP1, r'''n = Symbol('n', integer=True)
Assum = And(Q.integer(n), Q.odd(n))
Residual = Pow(-1, n + 1) - 1
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-parity-02 · expected false · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered false (solved)
_n[_run('demo-parity-02', 'satrefine-refine', 'false', 'the run satrefine-refine-20261014-174229 answered false (solved)', _SETUP1, r'''n = Symbol('n', integer=True)
m = Symbol('m', integer=True)
Assum = And(Q.integer(n), Q.integer(m), Q.odd(n), Q.odd(m))
Residual = Pow(-1, n * m) - 1
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-parity-03 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered true (solved)
_n[_run('demo-parity-03', 'satrefine-refine', 'true', 'the run satrefine-refine-20261014-174229 answered true (solved)', _SETUP1, r'''n = Symbol('n', integer=True)
Assum = And(Q.integer(n))
Residual = Pow(-1, n * (n + 1)) - 1
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-parity-04 · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered null (declined correctly)
_n[_run('demo-parity-04', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261014-174229 answered null (declined correctly)', _SETUP1, r'''n = Symbol('n', integer=True)
Assum = And(Q.integer(n), Q.even(n))
Residual = Pow(I, n) - 1
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-parity-05 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered true (solved)
_n[_run('demo-parity-05', 'satrefine-refine', 'true', 'the run satrefine-refine-20261014-174229 answered true (solved)', _SETUP1, r'''n = Symbol('n', integer=True)
m = Symbol('m', integer=True)
Assum = And(Q.integer(n), Q.integer(m), Q.odd(n), Q.odd(m))
Residual = Pow(-1, n * m) - (-1)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-prime-01 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered null (no verdict)
_n[_run('demo-prime-01', 'satrefine-refine', 'true', 'the run satrefine-refine-20261014-174229 answered null (no verdict)', _SETUP1, r'''p = Symbol('p', integer=True)
Assum = And(Q.integer(p), Q.prime(p), p > 2)
Residual = Pow(-1, p) - (-1)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-prime-02 · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered null (declined correctly)
_n[_run('demo-prime-02', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261014-174229 answered null (declined correctly)', _SETUP1, r'''p = Symbol('p', integer=True)
Assum = And(Q.integer(p), Q.prime(p))
Residual = Pow(-1, p) - (-1)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-sign-02 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered true (solved)
_n[_run('demo-sign-02', 'satrefine-refine', 'true', 'the run satrefine-refine-20261014-174229 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Assum = And(Q.real(x), ~Q.zero(x))
Residual = sign(Pow(x, 2)) - 1
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-sign-03 · expected contingent · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered null (declined correctly)
_n[_run('demo-sign-03', 'satrefine-refine', 'contingent', 'the run satrefine-refine-20261014-174229 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True)
Assum = And(Q.complex(x), ~Q.zero(x))
Residual = sign(Pow(x, 2)) - 1
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-sign-04 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered true (solved)
_n[_run('demo-sign-04', 'satrefine-refine', 'true', 'the run satrefine-refine-20261014-174229 answered true (solved)', _SETUP1, r'''z = Symbol('z', complex=True)
Assum = And(Q.complex(z))
Residual = Abs(z * conjugate(z)) - (z * conjugate(z))
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-sign-05 · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261014-174229 answered true (solved)
_n[_run('demo-sign-05', 'satrefine-refine', 'true', 'the run satrefine-refine-20261014-174229 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
y = Symbol('y', real=True)
Assum = And(Q.real(x), Q.real(y), Q.positive(x), Q.negative(y))
Residual = Abs(x - y) - (x - y)
Result = satrefine.refine(Residual, Assum)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

print(f"done: {sum(_n.values())} case run(s): {_n['true']} true, {_n['false']} false, {_n['null']} null")
