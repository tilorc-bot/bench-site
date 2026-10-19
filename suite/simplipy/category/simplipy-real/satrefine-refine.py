# assume-eval: a runnable script from the results browser
# Run: python3 this-file.py (or paste it into python or Jupyter).
# suite simplipy · category simplipy-real · system satrefine-refine (70 cases listed)
# 70 case run(s), a function each (listed in CASES).  Each runs in a fresh copy of
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
    """SymPy's cache cleared, as the harness clears it before each query (an
    error doing so is no answer, so bisect never counts it bad: a one-line
    warning on stderr, and the case runs with the cache as it is)."""
    try:
        _sys.modules['sympy'].core.cache.clear_cache()
    except Exception as e:
        print(f'warning: clearing the SymPy cache failed ({type(e).__name__}: {e}); '
              'this case runs with a warm cache', file=_sys.stderr)


# setup 1 (the harness's warm-up, version capture and cache clearing left out)
_SETUP1 = _Setup(r'''from sympy import *
import sympy
import satsimp
''', ('satsimp', '0.1.0'))

# comments that the cases' code repeats, shown once here (left out below):
# true iff the result is 0; false only if it is a definite nonzero number


# ---- case sp-acj4-1-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_1_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asin(Abs(x)) - Abs(asin(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_102_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_108_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_120_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-127-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_127_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(exp(x), 1, evaluate=False), Ne(exp(x), -1, evaluate=False))
    Residual = Abs(atanh(exp(x))) - atanh(exp(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-128-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_128_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(cos(asin(x))) - cos(asin(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_131_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_132_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_133_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-136-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_136_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(exp(1)) > 0))
    Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_137_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-14-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_14_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -sin(x) - sin(-x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-145-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_145_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(sin(acos(x))) - cos(asin(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-162-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_162_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-179-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_179_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
    Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-181-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_181_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
    Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-185-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_185_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(cos(x))), Ne(tan(cos(x)), I, evaluate=False), Ne(tan(cos(x)), -I, evaluate=False))
    Residual = atan(tan(cos(x))) - cos(x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-194-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_194_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(cos(x)), 1, evaluate=False), Ne(sin(cos(x)), -1, evaluate=False), ~Q.zero(cos(cos(x))))
    Residual = atanh(sin(cos(x))) - asinh(tan(cos(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-195-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_195_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(sin(x)), 1, evaluate=False), Ne(sin(sin(x)), -1, evaluate=False), ~Q.zero(cos(sin(x))))
    Residual = atanh(sin(sin(x))) - asinh(tan(sin(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-196-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_196_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
    Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-218-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_218_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-6 / x))
    Residual = 1 / (-6 / x) - (x / -6)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_22_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-220-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_220_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-8 / x))
    Residual = 1 / (-8 / x) - (x / -8)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-233-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_233_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)), Or(~Q.zero(x), re(-pi) > 0))
    Residual = 1 / Pow(x, pi) - Pow(x, -pi)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-248-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_248_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asin(x)) - asin(-Abs(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-249-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_249_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asinh(x)) - asinh(-Abs(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-251-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_251_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
    Residual = -Abs(atanh(x)) - atanh(-Abs(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_252_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_253_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-256-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_256_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(-exp(x)))
    Residual = -exp(-x) - (1 / -exp(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-275-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_275_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -3) - Abs(Pow(x, -3))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-276-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_276_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -4) - Pow(x, -4)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_283_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-286-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_286_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 5) - Abs(Pow(x, 5))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-289-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_289_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 8) - Pow(x, 8)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-31-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_31_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 5 * Abs(x) - Abs(-5 * x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-326-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_326_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(exp(x), 2) - exp(2 * x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-33-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_33_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 6 * Abs(x) - Abs(-6 * x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-35-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_35_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 7)))
    Residual = 7 * log(x) - log(Pow(x, 7))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-354-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_354_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(5)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(5)) - Pow(5, log(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-356-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_356_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(7)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(7)) - Pow(7, log(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-359-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_359_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(pi)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(pi)) - Pow(pi, log(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-364-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_364_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 3) - Abs(real_root(x, 3))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-367-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_367_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 9) - Abs(real_root(x, 9))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_368_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_369_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_370_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_371_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_372_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_373_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-38-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_38_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 9)))
    Residual = 9 * log(x) - log(Pow(x, 9))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-394-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_394_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-395-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_395_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_396_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-397-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_397_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(tanh(x))) - Abs(sin(tanh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-402-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_402_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_404_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-412-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_412_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-413-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_413_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(cos(x)))), ~Q.zero(cos(cos(x))))
    Residual = tan(Abs(cos(x))) - Abs(tan(cos(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_414_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_415_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-417-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_417_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(asin(Abs(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_421_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_5_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = atanh(Abs(x)) - Abs(atanh(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-73-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_73_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(-Abs(x)))
    Residual = -1 / Abs(x) - (1 / -Abs(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-80-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_80_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(-cos(x)))
    Residual = -1 / cos(x) - (1 / -cos(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-83-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_83_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(-log(x)))
    Residual = -1 / log(x) - (1 / -log(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-86-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_86_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(tan(x)), ~Q.zero(-tan(x)))
    Residual = -1 / tan(x) - (1 / -tan(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_90_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-214620 answered true (solved)
@_in(_SETUP1)
def sp_acj4_99_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# (case, system, expected, the stored run's answer, that run, its function)
CASES = [
    ('sp-acj4-1-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-214620', sp_acj4_1_real__satrefine_refine),
    ('sp-acj4-102-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_102_real__satrefine_refine),
    ('sp-acj4-108-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_108_real__satrefine_refine),
    ('sp-acj4-120-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_120_real__satrefine_refine),
    ('sp-acj4-127-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-214620', sp_acj4_127_real__satrefine_refine),
    ('sp-acj4-128-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-214620', sp_acj4_128_real__satrefine_refine),
    ('sp-acj4-131-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_131_real__satrefine_refine),
    ('sp-acj4-132-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-214620', sp_acj4_132_real__satrefine_refine),
    ('sp-acj4-133-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-214620', sp_acj4_133_real__satrefine_refine),
    ('sp-acj4-136-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-214620', sp_acj4_136_real__satrefine_refine),
    ('sp-acj4-137-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-214620', sp_acj4_137_real__satrefine_refine),
    ('sp-acj4-14-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_14_real__satrefine_refine),
    ('sp-acj4-145-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-214620', sp_acj4_145_real__satrefine_refine),
    ('sp-acj4-162-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-214620', sp_acj4_162_real__satrefine_refine),
    ('sp-acj4-179-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-214620', sp_acj4_179_real__satrefine_refine),
    ('sp-acj4-181-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-214620', sp_acj4_181_real__satrefine_refine),
    ('sp-acj4-185-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_185_real__satrefine_refine),
    ('sp-acj4-194-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_194_real__satrefine_refine),
    ('sp-acj4-195-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_195_real__satrefine_refine),
    ('sp-acj4-196-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_196_real__satrefine_refine),
    ('sp-acj4-218-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_218_real__satrefine_refine),
    ('sp-acj4-22-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_22_real__satrefine_refine),
    ('sp-acj4-220-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_220_real__satrefine_refine),
    ('sp-acj4-233-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_233_real__satrefine_refine),
    ('sp-acj4-248-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-214620', sp_acj4_248_real__satrefine_refine),
    ('sp-acj4-249-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_249_real__satrefine_refine),
    ('sp-acj4-251-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-214620', sp_acj4_251_real__satrefine_refine),
    ('sp-acj4-252-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_252_real__satrefine_refine),
    ('sp-acj4-253-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_253_real__satrefine_refine),
    ('sp-acj4-256-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_256_real__satrefine_refine),
    ('sp-acj4-275-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_275_real__satrefine_refine),
    ('sp-acj4-276-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_276_real__satrefine_refine),
    ('sp-acj4-283-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_283_real__satrefine_refine),
    ('sp-acj4-286-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_286_real__satrefine_refine),
    ('sp-acj4-289-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_289_real__satrefine_refine),
    ('sp-acj4-31-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_31_real__satrefine_refine),
    ('sp-acj4-326-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_326_real__satrefine_refine),
    ('sp-acj4-33-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_33_real__satrefine_refine),
    ('sp-acj4-35-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-214620', sp_acj4_35_real__satrefine_refine),
    ('sp-acj4-354-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_354_real__satrefine_refine),
    ('sp-acj4-356-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_356_real__satrefine_refine),
    ('sp-acj4-359-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_359_real__satrefine_refine),
    ('sp-acj4-364-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_364_real__satrefine_refine),
    ('sp-acj4-367-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_367_real__satrefine_refine),
    ('sp-acj4-368-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_368_real__satrefine_refine),
    ('sp-acj4-369-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_369_real__satrefine_refine),
    ('sp-acj4-370-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_370_real__satrefine_refine),
    ('sp-acj4-371-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_371_real__satrefine_refine),
    ('sp-acj4-372-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_372_real__satrefine_refine),
    ('sp-acj4-373-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_373_real__satrefine_refine),
    ('sp-acj4-38-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-214620', sp_acj4_38_real__satrefine_refine),
    ('sp-acj4-394-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-214620', sp_acj4_394_real__satrefine_refine),
    ('sp-acj4-395-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_395_real__satrefine_refine),
    ('sp-acj4-396-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_396_real__satrefine_refine),
    ('sp-acj4-397-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_397_real__satrefine_refine),
    ('sp-acj4-402-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-214620', sp_acj4_402_real__satrefine_refine),
    ('sp-acj4-404-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_404_real__satrefine_refine),
    ('sp-acj4-412-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-214620', sp_acj4_412_real__satrefine_refine),
    ('sp-acj4-413-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_413_real__satrefine_refine),
    ('sp-acj4-414-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_414_real__satrefine_refine),
    ('sp-acj4-415-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_415_real__satrefine_refine),
    ('sp-acj4-417-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-214620', sp_acj4_417_real__satrefine_refine),
    ('sp-acj4-421-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-214620', sp_acj4_421_real__satrefine_refine),
    ('sp-acj4-5-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-214620', sp_acj4_5_real__satrefine_refine),
    ('sp-acj4-73-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_73_real__satrefine_refine),
    ('sp-acj4-80-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_80_real__satrefine_refine),
    ('sp-acj4-83-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_83_real__satrefine_refine),
    ('sp-acj4-86-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_86_real__satrefine_refine),
    ('sp-acj4-90-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_90_real__satrefine_refine),
    ('sp-acj4-99-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-214620', sp_acj4_99_real__satrefine_refine),
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
