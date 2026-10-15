# -*- coding: utf-8 -*-
# assume-eval: a runnable script from the results browser
# suite examples · every case · system sympy-simplify (27 cases listed)
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
''', _SETUP1)

_n = {'true': 0, 'false': 0, 'null': 0}


# ---- case demo-atan2-01 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered true (solved)
_n[_run('demo-atan2-01', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174228 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, positive=True)
y = Symbol('y', real=True)
Residual = atan2(y, x) - atan(y / x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-atan2-02 · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered false (solved)
_n[_run('demo-atan2-02', 'sympy-simplify', 'false', 'the run sympy-simplify-20261014-174228 answered false (solved)', _SETUP1, r'''x = Symbol('x', real=True, negative=True)
y = Symbol('y', real=True, positive=True)
Residual = atan2(y, x) - atan(y / x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-abs-01 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered true (solved)
_n[_run('demo-eq-abs-01', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174228 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, negative=True)
Residual = Abs(x) - (-x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-abs-02 · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered null (no verdict)
_n[_run('demo-eq-abs-02', 'sympy-simplify', 'false', 'the run sympy-simplify-20261014-174228 answered null (no verdict)', _SETUP1, r'''x = Symbol('x', real=True, negative=True)
Residual = Abs(x) - x
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-log-01 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered true (solved)
_n[_run('demo-eq-log-01', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174228 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, positive=True)
Residual = log(exp(x)) - x
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-pow-01 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered true (solved)
_n[_run('demo-eq-pow-01', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174228 answered true (solved)', _SETUP1, r'''n = Symbol('n', integer=True)
Residual = Pow(-1, 2 * n) - 1
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-sqrt-01 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered true (solved)
_n[_run('demo-eq-sqrt-01', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174228 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, positive=True)
Residual = sqrt(Pow(x, 2)) - x
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-sqrt-02 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered true (solved)
_n[_run('demo-eq-sqrt-02', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174228 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = sqrt(Pow(x, 2)) - Abs(x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-sqrt-03 · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered null (declined correctly)
_n[_run('demo-eq-sqrt-03', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174228 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', real=True)
Residual = sqrt(Pow(x, 2)) - x
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-sqrt-04 · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered false (solved)
_n[_run('demo-eq-sqrt-04', 'sympy-simplify', 'false', 'the run sympy-simplify-20261014-174228 answered false (solved)', _SETUP1, r'''x = Symbol('x', real=True, positive=True)
Residual = sqrt(Pow(x, 2)) + 1 - x
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-trig-01 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered true (solved)
_n[_run('demo-eq-trig-01', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174228 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = Pow(sin(x), 2) + Pow(cos(x), 2) - 1
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-eq-trig-02 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered true (solved)
_n[_run('demo-eq-trig-02', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174228 answered true (solved)', _SETUP1, r'''x = Symbol('x', complex=True)
Residual = 2 * sin(x) * cos(x) - sin(2 * x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-log-01 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered true (solved)
_n[_run('demo-log-01', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174228 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, positive=True)
y = Symbol('y', real=True, positive=True)
Residual = log(x * y) - (log(x) + log(y))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-log-02 · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered null (declined correctly)
_n[_run('demo-log-02', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174228 answered null (declined correctly)', _SETUP1, r'''z = Symbol('z', complex=True, zero=False)
w = Symbol('w', complex=True, zero=False)
Residual = log(z * w) - (log(z) + log(w))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-log-03 · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered false (solved)
_n[_run('demo-log-03', 'sympy-simplify', 'false', 'the run sympy-simplify-20261014-174228 answered false (solved)', _SETUP1, r'''x = Symbol('x', real=True, negative=True)
Residual = log(x) - log(-x)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-nonzero-01 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered true (solved)
_n[_run('demo-nonzero-01', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174228 answered true (solved)', _SETUP1, r'''z = Symbol('z', complex=True, imaginary=True)
Residual = Abs(sign(z)) - 1
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-parity-01 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered true (solved)
_n[_run('demo-parity-01', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174228 answered true (solved)', _SETUP1, r'''n = Symbol('n', integer=True, odd=True)
Residual = Pow(-1, n + 1) - 1
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-parity-02 · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered false (solved)
_n[_run('demo-parity-02', 'sympy-simplify', 'false', 'the run sympy-simplify-20261014-174228 answered false (solved)', _SETUP1, r'''n = Symbol('n', integer=True, odd=True)
m = Symbol('m', integer=True, odd=True)
Residual = Pow(-1, n * m) - 1
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-parity-03 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered true (solved)
_n[_run('demo-parity-03', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174228 answered true (solved)', _SETUP1, r'''n = Symbol('n', integer=True)
Residual = Pow(-1, n * (n + 1)) - 1
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-parity-04 · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered null (declined correctly)
_n[_run('demo-parity-04', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174228 answered null (declined correctly)', _SETUP1, r'''n = Symbol('n', integer=True, even=True)
Residual = Pow(I, n) - 1
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-parity-05 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered true (solved)
_n[_run('demo-parity-05', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174228 answered true (solved)', _SETUP1, r'''n = Symbol('n', integer=True, odd=True)
m = Symbol('m', integer=True, odd=True)
Residual = Pow(-1, n * m) - (-1)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-prime-01 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered null (no verdict)
_n[_run('demo-prime-01', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174228 answered null (no verdict)', _SETUP1, r'''p = Symbol('p', integer=True, prime=True)
# dropped (not a unary fact about one symbol): p > 2
Residual = Pow(-1, p) - (-1)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-prime-02 · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered null (declined correctly)
_n[_run('demo-prime-02', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174228 answered null (declined correctly)', _SETUP1, r'''p = Symbol('p', integer=True, prime=True)
Residual = Pow(-1, p) - (-1)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-sign-02 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered true (solved)
_n[_run('demo-sign-02', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174228 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, zero=False)
Residual = sign(Pow(x, 2)) - 1
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-sign-03 · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered null (declined correctly)
_n[_run('demo-sign-03', 'sympy-simplify', 'contingent', 'the run sympy-simplify-20261014-174228 answered null (declined correctly)', _SETUP1, r'''x = Symbol('x', complex=True, zero=False)
Residual = sign(Pow(x, 2)) - 1
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-sign-04 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered null (no verdict)
_n[_run('demo-sign-04', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174228 answered null (no verdict)', _SETUP1, r'''z = Symbol('z', complex=True)
Residual = Abs(z * conjugate(z)) - (z * conjugate(z))
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

# ---- case demo-sign-05 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261014-174228 answered true (solved)
_n[_run('demo-sign-05', 'sympy-simplify', 'true', 'the run sympy-simplify-20261014-174228 answered true (solved)', _SETUP1, r'''x = Symbol('x', real=True, positive=True)
y = Symbol('y', real=True, negative=True)
Residual = Abs(x - y) - (x - y)
Result = simplify(Residual)
# true iff the result is 0; false only if it is a definite nonzero number
Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
print(Result, Answer, sep='\n')
''')] += 1

print(f"done: {sum(_n.values())} case run(s): {_n['true']} true, {_n['false']} false, {_n['null']} null")
