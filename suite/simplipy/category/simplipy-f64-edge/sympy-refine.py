# assume-eval: a runnable script from the results browser
# Run: python3 this-file.py (or paste it into python or Jupyter).
# suite simplipy · category simplipy-f64-edge · system sympy-refine (45 cases listed)
# 45 case run(s), a function each (listed in CASES).  Each runs in a fresh copy of
# its setup's namespace, so no variable carries over (module state other than SymPy's
# cache does), and an error in one is printed and the rest still run.
# Arguments, if any: the case ids to run (only those; pasted into python or Jupyter: all).
# It prints the CAS version that runs (with a warning if no stored run used it), a verdict per
# case, CHANGED: <stored> -> <got> where an answer is not the stored run's, and a tally.
# Exit status: 0 when every answer is the stored run's (wrong ones too: the tally counts them;
# an error answers null, as in the harness), 1 when any changed, 125 when a setup the cases
# need fails (SymPy does not import, say), 128 for an unknown case id.  So PYTHONPATH=<sympy
# checkout> git bisect run python3 this-file.py, with this script from a run of the good commit,
# finds the commit that changed an answer (125: skipped; 128: bisect stops).  Pasted into python
# or Jupyter it never exits.

import os as _os
import sys as _sys
import traceback as _traceback
import types as _types


if hasattr(_sys.stdout, 'reconfigure'):
    _sys.stdout.reconfigure(errors='backslashreplace')      # case text on an ascii / cp1252 stdout


def _version(name, *stored, _done=set()):
    """Print (once) the version of `name` that runs here, with a warning if no stored run used it."""
    if name in _done:
        return
    _done.add(name)
    got = getattr(_sys.modules.get(name), '__version__', None)
    if got is None:
        try:
            from importlib.metadata import version
            got = version(name)
        except Exception:
            got = '(not found)'
    used = f"{name} {' / '.join(stored)}"
    print(f'running {name} {got}' + (f'; WARNING: no stored run used it (they used {used})'
                                     if stored and got not in stored else ''))


def _verdict(answer, expected, stored, run):
    """Print the verdict and, if it is not `stored`, CHANGED; return (outcome, 'stored -> got' or '')."""
    kind = type(answer).__name__
    got = ("true" if answer is True or kind == "BooleanTrue" else
           "false" if answer is False or kind == "BooleanFalse" else "null")
    outcome = (("declined correctly" if expected == "contingent" else "no verdict") if got == "null" else
               "solved" if got == expected else "wrong" if expected in ("true", "false", "contingent") else
               "ungraded")
    print(f"verdict: {got} (expected {expected}: {outcome}; the run {run} answered {stored})")
    change = f"{stored} -> {got}" if got != stored else ""
    if change:
        print(f"CHANGED: {change}")
    return outcome, change


def _as_script():
    """True when this file runs as a script (python3 this-file.py), not pasted into python or Jupyter."""
    f = globals().get('__file__')
    return bool(f and _sys.argv and _os.path.realpath(f) == _os.path.realpath(_sys.argv[0]))


def _exit(status):
    """Exit with `status` when run as a script, not interactively (pasted: never)."""
    if status and _as_script() and not _sys.flags.interactive:
        raise SystemExit(status)


class _SetupFailed(BaseException):
    """A setup raised (SymPy does not import, say): exit 125, which git bisect run reads as skip."""


class _Setup:
    """A setup's namespace: its code run once, when a case first needs it; then its CAS versions."""

    def __init__(self, code, *versions):
        self.code, self.versions, self.ns = code, versions, None

    def __call__(self):
        if self.ns is None:
            ns = {'__name__': '__reproducer__'}
            try:
                exec(compile(self.code, 'setup', 'exec'), ns)
            except Exception:
                _traceback.print_exc()
                raise _SetupFailed() from None
            self.ns = ns
            for v in self.versions:
                _version(*v)
        return self.ns


def _in(setup):
    """The decorated case runs with a fresh copy of `setup`'s namespace as its globals."""
    def deco(fn):
        def case():
            return _types.FunctionType(fn.__code__, dict(setup()), fn.__name__)()
        case.setup = setup
        return case
    return deco


def _fresh():
    """SymPy's cache cleared, as the harness clears it before each query."""
    try:
        _sys.modules['sympy'].core.cache.clear_cache()
    except (KeyError, AttributeError):
        pass


# setup 1 (the harness's warm-up, version capture and cache clearing left out)
_SETUP1 = _Setup(r'''from sympy import *
import sympy
''', ('sympy', '1.14.0'))

# comments that the cases' code repeats, shown once here (left out below):
# true iff the result is 0; false only if it is a definite nonzero number


# ---- case sp-acj4-0-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_0_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-115-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_115_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -4)))
    Residual = log(x) / -4 - log(real_root(x, -4))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-116-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_116_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -6)))
    Residual = log(x) / -6 - log(real_root(x, -6))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_130_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_151_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_154_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-156-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_156_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = acos(sin(acos(x))) - Abs(asin(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_180_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_183_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_189_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_190_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_191_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_203_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-229-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered true (solved)
@_in(_SETUP1)
def sp_acj4_229_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(Pow(pi, x)))
    Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_234_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-241-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_241_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 3)), ~Q.zero(x))
    Residual = log(real_root(x, 3)) - (log(x) / 3)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-247-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_247_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 9)), ~Q.zero(x))
    Residual = log(real_root(x, 9)) - (log(x) / 9)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_260_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_261_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_266_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_267_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-29-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_29_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
    Residual = 3 * log(x) - log(Pow(x, 3))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-3-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_3_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = asinh(sinh(x)) - x
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered true (solved)
@_in(_SETUP1)
def sp_acj4_343_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_344_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-378-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered true (solved)
@_in(_SETUP1)
def sp_acj4_378_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -5) - exp(x / -5)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-380-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered true (solved)
@_in(_SETUP1)
def sp_acj4_380_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -7) - exp(x / -7)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-392-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_392_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_403_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-410-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered true (solved)
@_in(_SETUP1)
def sp_acj4_410_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(sinh(x)))
    Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-416-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_416_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
    Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_420_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_430_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_433_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_442_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-449-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_449_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cosh(-log(x))), ~Q.zero(1 / x), ~Q.zero(cosh(log(1 / x))))
    Residual = tanh(-log(x)) - tanh(log(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered true (solved)
@_in(_SETUP1)
def sp_acj4_450_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = x / x - 1
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered true (solved)
@_in(_SETUP1)
def sp_acj4_451_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_50_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_55_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_56_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_6_real__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-806-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered true (solved)
@_in(_SETUP1)
def sp_acj4_806_ground__sympy_refine():
    Assum = And()
    Residual = cosh(0) - 1
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-813-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered true (solved)
@_in(_SETUP1)
def sp_acj4_813_ground__sympy_refine():
    Assum = And()
    Residual = sinh(0) - 0
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-816-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261017-044751 answered true (solved)
@_in(_SETUP1)
def sp_acj4_816_ground__sympy_refine():
    Assum = And()
    Residual = tanh(0) - 0
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# (case, system, expected, the stored run's answer, that run, its function)
CASES = [
    ('sp-acj4-0-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261017-044751', sp_acj4_0_real__sympy_refine),
    ('sp-acj4-115-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261017-044751', sp_acj4_115_real__sympy_refine),
    ('sp-acj4-116-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261017-044751', sp_acj4_116_real__sympy_refine),
    ('sp-acj4-130-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_130_real__sympy_refine),
    ('sp-acj4-151-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_151_real__sympy_refine),
    ('sp-acj4-154-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261017-044751', sp_acj4_154_real__sympy_refine),
    ('sp-acj4-156-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_156_real__sympy_refine),
    ('sp-acj4-180-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_180_real__sympy_refine),
    ('sp-acj4-183-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_183_real__sympy_refine),
    ('sp-acj4-189-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261017-044751', sp_acj4_189_real__sympy_refine),
    ('sp-acj4-190-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261017-044751', sp_acj4_190_real__sympy_refine),
    ('sp-acj4-191-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261017-044751', sp_acj4_191_real__sympy_refine),
    ('sp-acj4-203-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_203_real__sympy_refine),
    ('sp-acj4-229-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261017-044751', sp_acj4_229_real__sympy_refine),
    ('sp-acj4-234-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_234_real__sympy_refine),
    ('sp-acj4-241-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_241_real__sympy_refine),
    ('sp-acj4-247-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_247_real__sympy_refine),
    ('sp-acj4-260-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_260_real__sympy_refine),
    ('sp-acj4-261-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261017-044751', sp_acj4_261_real__sympy_refine),
    ('sp-acj4-266-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_266_real__sympy_refine),
    ('sp-acj4-267-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_267_real__sympy_refine),
    ('sp-acj4-29-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_29_real__sympy_refine),
    ('sp-acj4-3-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261017-044751', sp_acj4_3_real__sympy_refine),
    ('sp-acj4-343-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261017-044751', sp_acj4_343_real__sympy_refine),
    ('sp-acj4-344-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_344_real__sympy_refine),
    ('sp-acj4-378-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261017-044751', sp_acj4_378_real__sympy_refine),
    ('sp-acj4-380-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261017-044751', sp_acj4_380_real__sympy_refine),
    ('sp-acj4-392-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_392_real__sympy_refine),
    ('sp-acj4-403-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_403_real__sympy_refine),
    ('sp-acj4-410-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261017-044751', sp_acj4_410_real__sympy_refine),
    ('sp-acj4-416-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_416_real__sympy_refine),
    ('sp-acj4-420-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_420_real__sympy_refine),
    ('sp-acj4-430-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_430_real__sympy_refine),
    ('sp-acj4-433-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_433_real__sympy_refine),
    ('sp-acj4-442-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_442_real__sympy_refine),
    ('sp-acj4-449-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261017-044751', sp_acj4_449_real__sympy_refine),
    ('sp-acj4-450-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261017-044751', sp_acj4_450_real__sympy_refine),
    ('sp-acj4-451-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261017-044751', sp_acj4_451_real__sympy_refine),
    ('sp-acj4-50-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261017-044751', sp_acj4_50_real__sympy_refine),
    ('sp-acj4-55-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_55_real__sympy_refine),
    ('sp-acj4-56-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261017-044751', sp_acj4_56_real__sympy_refine),
    ('sp-acj4-6-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261017-044751', sp_acj4_6_real__sympy_refine),
    ('sp-acj4-806-ground', 'sympy-refine', 'true', 'true', 'sympy-refine-20261017-044751', sp_acj4_806_ground__sympy_refine),
    ('sp-acj4-813-ground', 'sympy-refine', 'true', 'true', 'sympy-refine-20261017-044751', sp_acj4_813_ground__sympy_refine),
    ('sp-acj4-816-ground', 'sympy-refine', 'true', 'true', 'sympy-refine-20261017-044751', sp_acj4_816_ground__sympy_refine),
]


def main(only):
    """Run CASES (of the case ids `only`, if any); the exit status."""
    unknown = set(only) - {c[0] for c in CASES}
    if unknown:
        print(f"no such case in this script: {', '.join(sorted(unknown))} (exit 128: git bisect run stops)")
        return 128
    rows = [c for c in CASES if not only or c[0] in only]
    try:
        for setup in dict.fromkeys(fn.setup for *_, fn in rows):
            setup()
    except _SetupFailed:
        print('SETUP FAILED: nothing to test (exit 125: git bisect run skips this commit)')
        return 125
    outcomes, changed, errors = [], [], 0
    for case, system, expected, stored, run, fn in rows:
        print(f'== {case} | {system} | expected {expected}')
        _fresh()
        try:
            answer = fn()
        except (Exception, SystemExit):
            _sys.stdout.flush()
            _traceback.print_exc()
            errors += 1
            answer = None
        outcome, change = _verdict(answer, expected, stored, run)
        outcomes.append(outcome)
        if change:
            changed.append(f'{case} | {system}: {change}')
    kinds = ['solved', 'wrong', 'no verdict', 'declined correctly'] + ['ungraded'] * ('ungraded' in outcomes)
    print(f"done: {len(outcomes)} case run(s): {', '.join(f'{outcomes.count(k)} {k}' for k in kinds)}"
          + (f' ({errors} error(s))' if errors else '') + f'; {len(changed)} changed vs the stored runs')
    for c in changed:
        print(f'CHANGED: {c}')
    return 1 if changed else 0


_exit(main(_sys.argv[1:] if _as_script() else []))
