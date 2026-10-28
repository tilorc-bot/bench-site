# assume-eval: a runnable script from the results browser
# Run: python3 this-file.py (or paste it into python or Jupyter).
# suite simplipy · category simplipy-f64-edge · all Python systems (45 cases listed)
# 539 case run(s), a function each (listed in CASES).  Each runs in a fresh copy of
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
import satassume.sympy_api
''', ('satassume', '0.0.1'))

# setup 2 (the harness's warm-up, version capture and cache clearing left out)
_SETUP2 = _Setup(r'''from sympy import *
import sympy
import satsimp
''', ('satsimp', '0.1.0'))

# setup 3 (the harness's warm-up, version capture and cache clearing left out)
_SETUP3 = _Setup(r'''from sympy import *
import sympy
''', ('sympy', '1.14.0'))

# setup 4 (the harness's warm-up, version capture and cache clearing left out)
_SETUP4 = _Setup(r'''from sympy import *
import sympy
from sympy.assumptions.satask import satask
''', ('sympy', '1.14.0'))

# setup 5 (the harness's warm-up, version capture and cache clearing left out)
_SETUP5 = _Setup(r'''from sympy import *
import sympy
import sympy_extras.assumptions
import sympy_extras.settings
import importlib.metadata
import json as Json, re as Regex
Source = Json.loads(importlib.metadata.distribution('sympy-extras').read_text('direct_url.json') or '{}')
Archive = Regex.match('https://[^#]*/archive/([0-9a-f]{40})[.](tar[.]gz|zip)(#|$)', Source.get('url', '')) if 'archive_info' in Source else None
Commit = Source.get('vcs_info', {}).get('commit_id') or (Archive and Archive.group(1))
Settings = f'{sympy_extras.settings.settings!r}, time_scale={sympy_extras.settings.settings.time_scale}'
''', ('sympy-extras', '0.0.3 (commit 2d60199620ac)'))

# comments that the cases' code repeats, shown once here (left out below):
# true iff the result is 0; false only if it is a definite nonzero number
# automatic evaluation only: no simplify, refine or other function
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False
# the claim as a relation, sympy-extras' statement form (not Q.zero: see the adapter)
# dropped (not a unary fact about one symbol): x > 0
# dropped (not a unary fact about one symbol): ~Q.zero(real_root(x, -4))
# dropped (not a unary fact about one symbol): ~Q.zero(real_root(x, -6))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cos(x))
# dropped (not a unary fact about one symbol): Ne(sinh(acosh(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(acosh(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(acosh(x)))
# dropped (not a unary fact about one symbol): Ne(sinh(log(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(log(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(log(x)))
# dropped (not a unary fact about one symbol): Ne(cos(asin(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(cos(asin(x)), -1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(cos(atan(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(cos(atan(x)), -1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(acos(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(acos(x)), -1, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(pi, x))
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, x))
# dropped (not a unary fact about one symbol): Or(~Q.zero(1 / x), re(x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(real_root(x, 3))
# dropped (not a unary fact about one symbol): ~Q.zero(real_root(x, 9))
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(1 / x)))
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, 3))
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(-x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(exp(x))
# dropped (not a unary fact about one symbol): ~Q.zero(sinh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(acos(Abs(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(acos(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(-log(x)))
# dropped (not a unary fact about one symbol): Ne(-log(x), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(-log(x), -I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(log(1 / x), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(log(1 / x), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(log(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / log(x))
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(-log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(log(1 / x)))
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(6, x))
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(exp(1)) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, exp(1)))
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, pi))
# dropped (not a unary fact about one symbol): Ne(tanh(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(tanh(x), -1, evaluate=False)


# ---- case sp-acj4-0-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_0_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered true (solved)
@_in(_SETUP2)
def sp_acj4_0_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_0_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered true (solved)
@_in(_SETUP2)
def sp_acj4_0_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_0_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = acosh(cosh(x)) - Abs(x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_0_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_0_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_0_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_0_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = acosh(cosh(x)) - Abs(x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_0_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_0_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_0_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-115-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_115_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -4)))
    Residual = log(x) / -4 - log(real_root(x, -4))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-115-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered true (solved)
@_in(_SETUP2)
def sp_acj4_115_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -4)))
    Residual = log(x) / -4 - log(real_root(x, -4))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-115-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_115_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -4)))
    Residual = log(x) / -4 - log(real_root(x, -4))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-115-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered true (solved)
@_in(_SETUP2)
def sp_acj4_115_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -4)))
    Residual = log(x) / -4 - log(real_root(x, -4))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-115-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_115_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = log(x) / -4 - log(real_root(x, -4))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-115-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_115_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -4)))
    Residual = log(x) / -4 - log(real_root(x, -4))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-115-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_115_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -4)))
    Residual = log(x) / -4 - log(real_root(x, -4))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-115-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_115_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -4)))
    Residual = log(x) / -4 - log(real_root(x, -4))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-115-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered true (solved)
@_in(_SETUP3)
def sp_acj4_115_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = log(x) / -4 - log(real_root(x, -4))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-115-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered true (solved)
@_in(_SETUP5)
def sp_acj4_115_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -4)))
    Residual = log(x) / -4 - log(real_root(x, -4))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-115-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered true (solved)
@_in(_SETUP5)
def sp_acj4_115_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -4)))
    Residual = log(x) / -4 - log(real_root(x, -4))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-115-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered true (solved)
@_in(_SETUP5)
def sp_acj4_115_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -4)))
    Residual = log(x) / -4 - log(real_root(x, -4))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-116-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_116_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -6)))
    Residual = log(x) / -6 - log(real_root(x, -6))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-116-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered true (solved)
@_in(_SETUP2)
def sp_acj4_116_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -6)))
    Residual = log(x) / -6 - log(real_root(x, -6))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-116-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_116_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -6)))
    Residual = log(x) / -6 - log(real_root(x, -6))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-116-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered true (solved)
@_in(_SETUP2)
def sp_acj4_116_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -6)))
    Residual = log(x) / -6 - log(real_root(x, -6))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-116-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_116_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = log(x) / -6 - log(real_root(x, -6))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-116-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_116_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -6)))
    Residual = log(x) / -6 - log(real_root(x, -6))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-116-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_116_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -6)))
    Residual = log(x) / -6 - log(real_root(x, -6))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-116-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_116_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -6)))
    Residual = log(x) / -6 - log(real_root(x, -6))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-116-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered true (solved)
@_in(_SETUP3)
def sp_acj4_116_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = log(x) / -6 - log(real_root(x, -6))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-116-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered true (solved)
@_in(_SETUP5)
def sp_acj4_116_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -6)))
    Residual = log(x) / -6 - log(real_root(x, -6))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-116-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered true (solved)
@_in(_SETUP5)
def sp_acj4_116_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -6)))
    Residual = log(x) / -6 - log(real_root(x, -6))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-116-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered true (solved)
@_in(_SETUP5)
def sp_acj4_116_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -6)))
    Residual = log(x) / -6 - log(real_root(x, -6))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_130_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_130_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_130_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_130_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_130_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_130_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_130_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_130_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_130_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_130_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_130_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_130_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_151_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_151_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_151_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_151_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_151_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_151_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_151_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_151_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_151_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_151_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_151_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_151_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_154_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_154_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_154_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_154_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_154_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_154_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_154_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_154_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_154_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_154_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_154_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-156-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_156_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(sin(acos(x))) - Abs(asin(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-156-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_156_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(sin(acos(x))) - Abs(asin(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-156-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_156_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(sin(acos(x))) - Abs(asin(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-156-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_156_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(sin(acos(x))) - Abs(asin(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-156-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_156_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = acos(sin(acos(x))) - Abs(asin(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-156-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_156_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(sin(acos(x))) - Abs(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-156-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_156_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(sin(acos(x))) - Abs(asin(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-156-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_156_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(sin(acos(x))) - Abs(asin(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-156-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_156_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = acos(sin(acos(x))) - Abs(asin(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-156-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_156_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(sin(acos(x))) - Abs(asin(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-156-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_156_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(sin(acos(x))) - Abs(asin(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-156-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_156_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acos(sin(acos(x))) - Abs(asin(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_180_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_180_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_180_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_180_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_180_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_180_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_180_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_180_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_180_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_180_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_180_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_180_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_183_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_183_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_183_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_183_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_183_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_183_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_183_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_183_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_183_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_183_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_183_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_183_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_189_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_189_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_189_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_189_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_189_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_189_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_189_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_189_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_189_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_189_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_189_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_189_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_190_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_190_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_190_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_190_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_190_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_190_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_190_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_190_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_190_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_190_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_190_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_190_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_191_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_191_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_191_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_191_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_191_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_191_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_191_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_191_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_191_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_191_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_191_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_191_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_203_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_203_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_203_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_203_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_203_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = cos(log(1 / x)) - cos(log(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_203_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_203_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_203_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_203_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = cos(log(1 / x)) - cos(log(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_203_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_203_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_203_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-229-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered true (solved)
@_in(_SETUP1)
def sp_acj4_229_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Pow(pi, x)))
    Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-229-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered true (solved)
@_in(_SETUP2)
def sp_acj4_229_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Pow(pi, x)))
    Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-229-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered true (solved)
@_in(_SETUP2)
def sp_acj4_229_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Pow(pi, x)))
    Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-229-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered true (solved)
@_in(_SETUP2)
def sp_acj4_229_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Pow(pi, x)))
    Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-229-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered true (solved)
@_in(_SETUP3)
def sp_acj4_229_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-229-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered true (solved)
@_in(_SETUP3)
def sp_acj4_229_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Pow(pi, x)))
    Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-229-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered true (solved)
@_in(_SETUP4)
def sp_acj4_229_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Pow(pi, x)))
    Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-229-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered true (solved)
@_in(_SETUP3)
def sp_acj4_229_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Pow(pi, x)))
    Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-229-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered true (solved)
@_in(_SETUP3)
def sp_acj4_229_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-229-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered true (solved)
@_in(_SETUP5)
def sp_acj4_229_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Pow(pi, x)))
    Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-229-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered true (solved)
@_in(_SETUP5)
def sp_acj4_229_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Pow(pi, x)))
    Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-229-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered true (solved)
@_in(_SETUP5)
def sp_acj4_229_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Pow(pi, x)))
    Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_234_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_234_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_234_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_234_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_234_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_234_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_234_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_234_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_234_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_234_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_234_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_234_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-241-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_241_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 3)), ~Q.zero(x))
    Residual = log(real_root(x, 3)) - (log(x) / 3)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-241-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_241_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 3)), ~Q.zero(x))
    Residual = log(real_root(x, 3)) - (log(x) / 3)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-241-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_241_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 3)), ~Q.zero(x))
    Residual = log(real_root(x, 3)) - (log(x) / 3)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-241-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_241_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 3)), ~Q.zero(x))
    Residual = log(real_root(x, 3)) - (log(x) / 3)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-241-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_241_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = log(real_root(x, 3)) - (log(x) / 3)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-241-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_241_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 3)), ~Q.zero(x))
    Residual = log(real_root(x, 3)) - (log(x) / 3)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-241-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_241_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 3)), ~Q.zero(x))
    Residual = log(real_root(x, 3)) - (log(x) / 3)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-241-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_241_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 3)), ~Q.zero(x))
    Residual = log(real_root(x, 3)) - (log(x) / 3)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-241-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_241_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = log(real_root(x, 3)) - (log(x) / 3)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-241-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_241_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 3)), ~Q.zero(x))
    Residual = log(real_root(x, 3)) - (log(x) / 3)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-241-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_241_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 3)), ~Q.zero(x))
    Residual = log(real_root(x, 3)) - (log(x) / 3)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-241-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_241_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 3)), ~Q.zero(x))
    Residual = log(real_root(x, 3)) - (log(x) / 3)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-247-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_247_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 9)), ~Q.zero(x))
    Residual = log(real_root(x, 9)) - (log(x) / 9)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-247-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_247_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 9)), ~Q.zero(x))
    Residual = log(real_root(x, 9)) - (log(x) / 9)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-247-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_247_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 9)), ~Q.zero(x))
    Residual = log(real_root(x, 9)) - (log(x) / 9)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-247-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_247_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 9)), ~Q.zero(x))
    Residual = log(real_root(x, 9)) - (log(x) / 9)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-247-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_247_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = log(real_root(x, 9)) - (log(x) / 9)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-247-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_247_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 9)), ~Q.zero(x))
    Residual = log(real_root(x, 9)) - (log(x) / 9)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-247-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_247_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 9)), ~Q.zero(x))
    Residual = log(real_root(x, 9)) - (log(x) / 9)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-247-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_247_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 9)), ~Q.zero(x))
    Residual = log(real_root(x, 9)) - (log(x) / 9)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-247-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_247_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = log(real_root(x, 9)) - (log(x) / 9)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-247-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_247_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 9)), ~Q.zero(x))
    Residual = log(real_root(x, 9)) - (log(x) / 9)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-247-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_247_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 9)), ~Q.zero(x))
    Residual = log(real_root(x, 9)) - (log(x) / 9)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-247-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_247_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 9)), ~Q.zero(x))
    Residual = log(real_root(x, 9)) - (log(x) / 9)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_260_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_260_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_260_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_260_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_260_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = -log(cos(x)) - log(1 / cos(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_260_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_260_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_260_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_260_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = -log(cos(x)) - log(1 / cos(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_260_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_260_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_260_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_261_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered true (solved)
@_in(_SETUP2)
def sp_acj4_261_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_261_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered true (solved)
@_in(_SETUP2)
def sp_acj4_261_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_261_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_261_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_261_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_261_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered true (solved)
@_in(_SETUP3)
def sp_acj4_261_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered true (solved)
@_in(_SETUP5)
def sp_acj4_261_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered true (solved)
@_in(_SETUP5)
def sp_acj4_261_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered true (solved)
@_in(_SETUP5)
def sp_acj4_261_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_266_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_266_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_266_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_266_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_266_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = -sin(log(x)) - sin(log(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_266_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_266_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_266_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_266_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = -sin(log(x)) - sin(log(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_266_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_266_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_266_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_267_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_267_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_267_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_267_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_267_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = -tan(log(x)) - tan(log(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_267_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_267_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_267_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_267_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = -tan(log(x)) - tan(log(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_267_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_267_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_267_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-29-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_29_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
    Residual = 3 * log(x) - log(Pow(x, 3))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-29-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_29_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
    Residual = 3 * log(x) - log(Pow(x, 3))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-29-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_29_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
    Residual = 3 * log(x) - log(Pow(x, 3))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-29-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_29_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
    Residual = 3 * log(x) - log(Pow(x, 3))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-29-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_29_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = 3 * log(x) - log(Pow(x, 3))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-29-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_29_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
    Residual = 3 * log(x) - log(Pow(x, 3))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-29-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_29_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
    Residual = 3 * log(x) - log(Pow(x, 3))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-29-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_29_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
    Residual = 3 * log(x) - log(Pow(x, 3))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-29-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_29_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = 3 * log(x) - log(Pow(x, 3))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-29-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_29_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
    Residual = 3 * log(x) - log(Pow(x, 3))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-29-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_29_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
    Residual = 3 * log(x) - log(Pow(x, 3))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-29-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_29_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
    Residual = 3 * log(x) - log(Pow(x, 3))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-3-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_3_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asinh(sinh(x)) - x
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-3-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered true (solved)
@_in(_SETUP2)
def sp_acj4_3_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asinh(sinh(x)) - x
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-3-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_3_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asinh(sinh(x)) - x
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-3-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered true (solved)
@_in(_SETUP2)
def sp_acj4_3_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asinh(sinh(x)) - x
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-3-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_3_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = asinh(sinh(x)) - x
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-3-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_3_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asinh(sinh(x)) - x
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-3-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_3_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asinh(sinh(x)) - x
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-3-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_3_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asinh(sinh(x)) - x
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-3-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_3_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = asinh(sinh(x)) - x
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-3-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered true (solved)
@_in(_SETUP5)
def sp_acj4_3_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asinh(sinh(x)) - x
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-3-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_3_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asinh(sinh(x)) - x
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-3-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered true (solved)
@_in(_SETUP5)
def sp_acj4_3_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asinh(sinh(x)) - x
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered true (solved)
@_in(_SETUP1)
def sp_acj4_343_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered true (solved)
@_in(_SETUP2)
def sp_acj4_343_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered true (solved)
@_in(_SETUP2)
def sp_acj4_343_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered true (solved)
@_in(_SETUP2)
def sp_acj4_343_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered true (solved)
@_in(_SETUP3)
def sp_acj4_343_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered true (solved)
@_in(_SETUP3)
def sp_acj4_343_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered true (solved)
@_in(_SETUP4)
def sp_acj4_343_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered true (solved)
@_in(_SETUP3)
def sp_acj4_343_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered true (solved)
@_in(_SETUP3)
def sp_acj4_343_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered true (solved)
@_in(_SETUP5)
def sp_acj4_343_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered true (solved)
@_in(_SETUP5)
def sp_acj4_343_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered true (solved)
@_in(_SETUP5)
def sp_acj4_343_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_344_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_344_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_344_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_344_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_344_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_344_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_344_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_344_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_344_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_344_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_344_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_344_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-378-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_378_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -5) - exp(x / -5)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-378-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered true (solved)
@_in(_SETUP2)
def sp_acj4_378_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -5) - exp(x / -5)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-378-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_378_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -5) - exp(x / -5)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-378-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered true (solved)
@_in(_SETUP2)
def sp_acj4_378_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -5) - exp(x / -5)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-378-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered true (solved)
@_in(_SETUP3)
def sp_acj4_378_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = real_root(exp(x), -5) - exp(x / -5)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-378-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_378_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -5) - exp(x / -5)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-378-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_378_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -5) - exp(x / -5)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-378-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_378_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -5) - exp(x / -5)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-378-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered true (solved)
@_in(_SETUP3)
def sp_acj4_378_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = real_root(exp(x), -5) - exp(x / -5)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-378-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_378_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -5) - exp(x / -5)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-378-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered true (solved)
@_in(_SETUP5)
def sp_acj4_378_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -5) - exp(x / -5)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-378-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered true (solved)
@_in(_SETUP5)
def sp_acj4_378_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -5) - exp(x / -5)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-380-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_380_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -7) - exp(x / -7)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-380-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered true (solved)
@_in(_SETUP2)
def sp_acj4_380_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -7) - exp(x / -7)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-380-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_380_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -7) - exp(x / -7)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-380-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered true (solved)
@_in(_SETUP2)
def sp_acj4_380_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -7) - exp(x / -7)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-380-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered true (solved)
@_in(_SETUP3)
def sp_acj4_380_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = real_root(exp(x), -7) - exp(x / -7)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-380-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_380_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -7) - exp(x / -7)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-380-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_380_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -7) - exp(x / -7)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-380-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_380_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -7) - exp(x / -7)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-380-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered true (solved)
@_in(_SETUP3)
def sp_acj4_380_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = real_root(exp(x), -7) - exp(x / -7)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-380-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_380_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -7) - exp(x / -7)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-380-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered true (solved)
@_in(_SETUP5)
def sp_acj4_380_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -7) - exp(x / -7)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-380-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered true (solved)
@_in(_SETUP5)
def sp_acj4_380_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -7) - exp(x / -7)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-392-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_392_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-392-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_392_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-392-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_392_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-392-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_392_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-392-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_392_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-392-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_392_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-392-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_392_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-392-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_392_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-392-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_392_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-392-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_392_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-392-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_392_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-392-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_392_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_403_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_403_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_403_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_403_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_403_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = sin(-log(x)) - sin(log(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_403_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_403_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_403_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_403_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = sin(-log(x)) - sin(log(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_403_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_403_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_403_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-410-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered true (solved)
@_in(_SETUP1)
def sp_acj4_410_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(sinh(x)))
    Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-410-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered true (solved)
@_in(_SETUP2)
def sp_acj4_410_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(sinh(x)))
    Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-410-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered true (solved)
@_in(_SETUP2)
def sp_acj4_410_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(sinh(x)))
    Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-410-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered true (solved)
@_in(_SETUP2)
def sp_acj4_410_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(sinh(x)))
    Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-410-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered true (solved)
@_in(_SETUP3)
def sp_acj4_410_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-410-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered true (solved)
@_in(_SETUP3)
def sp_acj4_410_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(sinh(x)))
    Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-410-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered true (solved)
@_in(_SETUP4)
def sp_acj4_410_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(sinh(x)))
    Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-410-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered true (solved)
@_in(_SETUP3)
def sp_acj4_410_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(sinh(x)))
    Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-410-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered true (solved)
@_in(_SETUP3)
def sp_acj4_410_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-410-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered true (solved)
@_in(_SETUP5)
def sp_acj4_410_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(sinh(x)))
    Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-410-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered true (solved)
@_in(_SETUP5)
def sp_acj4_410_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(sinh(x)))
    Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-410-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered true (solved)
@_in(_SETUP5)
def sp_acj4_410_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(sinh(x)))
    Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-416-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_416_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
    Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-416-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_416_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
    Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-416-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_416_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
    Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-416-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_416_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
    Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-416-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_416_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-416-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_416_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
    Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-416-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_416_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
    Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-416-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_416_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
    Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-416-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_416_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-416-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_416_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
    Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-416-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_416_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
    Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-416-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_416_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
    Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_420_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_420_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_420_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_420_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_420_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = tan(-log(x)) - tan(log(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_420_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_420_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_420_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_420_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = tan(-log(x)) - tan(log(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_420_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_420_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_420_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_430_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_430_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_430_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_430_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_430_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = log(x) * x - log(Pow(x, x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_430_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_430_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_430_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_430_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = log(x) * x - log(Pow(x, x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_430_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_430_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_430_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_433_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_433_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_433_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_433_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_433_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = atan(-log(x)) - atan(log(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_433_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_433_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_433_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_433_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = atan(-log(x)) - atan(log(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_433_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_433_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_433_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_442_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_442_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_442_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_442_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_442_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = -log(log(x)) - log(1 / log(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_442_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_442_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_442_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_442_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = -log(log(x)) - log(1 / log(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_442_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_442_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_442_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-449-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_449_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cosh(-log(x))), ~Q.zero(1 / x), ~Q.zero(cosh(log(1 / x))))
    Residual = tanh(-log(x)) - tanh(log(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-449-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_449_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cosh(-log(x))), ~Q.zero(1 / x), ~Q.zero(cosh(log(1 / x))))
    Residual = tanh(-log(x)) - tanh(log(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-449-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_449_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cosh(-log(x))), ~Q.zero(1 / x), ~Q.zero(cosh(log(1 / x))))
    Residual = tanh(-log(x)) - tanh(log(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-449-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_449_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cosh(-log(x))), ~Q.zero(1 / x), ~Q.zero(cosh(log(1 / x))))
    Residual = tanh(-log(x)) - tanh(log(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-449-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_449_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = tanh(-log(x)) - tanh(log(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-449-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_449_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cosh(-log(x))), ~Q.zero(1 / x), ~Q.zero(cosh(log(1 / x))))
    Residual = tanh(-log(x)) - tanh(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-449-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_449_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cosh(-log(x))), ~Q.zero(1 / x), ~Q.zero(cosh(log(1 / x))))
    Residual = tanh(-log(x)) - tanh(log(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-449-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_449_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cosh(-log(x))), ~Q.zero(1 / x), ~Q.zero(cosh(log(1 / x))))
    Residual = tanh(-log(x)) - tanh(log(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-449-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_449_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = tanh(-log(x)) - tanh(log(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-449-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered true (solved)
@_in(_SETUP5)
def sp_acj4_449_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cosh(-log(x))), ~Q.zero(1 / x), ~Q.zero(cosh(log(1 / x))))
    Residual = tanh(-log(x)) - tanh(log(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-449-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_449_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cosh(-log(x))), ~Q.zero(1 / x), ~Q.zero(cosh(log(1 / x))))
    Residual = tanh(-log(x)) - tanh(log(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-449-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered true (solved)
@_in(_SETUP5)
def sp_acj4_449_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cosh(-log(x))), ~Q.zero(1 / x), ~Q.zero(cosh(log(1 / x))))
    Residual = tanh(-log(x)) - tanh(log(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered true (solved)
@_in(_SETUP1)
def sp_acj4_450_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = x / x - 1
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered true (solved)
@_in(_SETUP2)
def sp_acj4_450_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = x / x - 1
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered true (solved)
@_in(_SETUP2)
def sp_acj4_450_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = x / x - 1
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered true (solved)
@_in(_SETUP2)
def sp_acj4_450_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = x / x - 1
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered true (solved)
@_in(_SETUP3)
def sp_acj4_450_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = x / x - 1
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered true (solved)
@_in(_SETUP3)
def sp_acj4_450_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = x / x - 1
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered true (solved)
@_in(_SETUP4)
def sp_acj4_450_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = x / x - 1
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered true (solved)
@_in(_SETUP3)
def sp_acj4_450_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = x / x - 1
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered true (solved)
@_in(_SETUP3)
def sp_acj4_450_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = x / x - 1
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered true (solved)
@_in(_SETUP5)
def sp_acj4_450_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = x / x - 1
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered true (solved)
@_in(_SETUP5)
def sp_acj4_450_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = x / x - 1
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered true (solved)
@_in(_SETUP5)
def sp_acj4_450_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = x / x - 1
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered true (solved)
@_in(_SETUP1)
def sp_acj4_451_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered true (solved)
@_in(_SETUP2)
def sp_acj4_451_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered true (solved)
@_in(_SETUP2)
def sp_acj4_451_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered true (solved)
@_in(_SETUP2)
def sp_acj4_451_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered true (solved)
@_in(_SETUP3)
def sp_acj4_451_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = 0 / x - 0
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered true (solved)
@_in(_SETUP3)
def sp_acj4_451_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered true (solved)
@_in(_SETUP4)
def sp_acj4_451_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered true (solved)
@_in(_SETUP3)
def sp_acj4_451_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered true (solved)
@_in(_SETUP3)
def sp_acj4_451_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = 0 / x - 0
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered true (solved)
@_in(_SETUP5)
def sp_acj4_451_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered true (solved)
@_in(_SETUP5)
def sp_acj4_451_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered true (solved)
@_in(_SETUP5)
def sp_acj4_451_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_50_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered true (solved)
@_in(_SETUP2)
def sp_acj4_50_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_50_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered true (solved)
@_in(_SETUP2)
def sp_acj4_50_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_50_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = log(6) * x - log(Pow(6, x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_50_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_50_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_50_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered true (solved)
@_in(_SETUP3)
def sp_acj4_50_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = log(6) * x - log(Pow(6, x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered true (solved)
@_in(_SETUP5)
def sp_acj4_50_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered true (solved)
@_in(_SETUP5)
def sp_acj4_50_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered true (solved)
@_in(_SETUP5)
def sp_acj4_50_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_55_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_55_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_55_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_55_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_55_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_55_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_55_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_55_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_55_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_55_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_55_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_55_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_56_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_56_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_56_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_56_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_56_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = log(x) * pi - log(Pow(x, pi))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_56_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_56_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_56_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_56_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = log(x) * pi - log(Pow(x, pi))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_56_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_56_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_56_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_6_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered true (solved)
@_in(_SETUP2)
def sp_acj4_6_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_6_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered true (solved)
@_in(_SETUP2)
def sp_acj4_6_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_6_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = atanh(tanh(x)) - x
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_6_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_6_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_6_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_6_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = atanh(tanh(x)) - x
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered true (solved)
@_in(_SETUP5)
def sp_acj4_6_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_6_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered true (solved)
@_in(_SETUP5)
def sp_acj4_6_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-806-ground · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered true (solved)
@_in(_SETUP1)
def sp_acj4_806_ground__satassume_ask():
    Assum = And()
    Residual = cosh(0) - 1
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-806-ground · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered true (solved)
@_in(_SETUP2)
def sp_acj4_806_ground__satrefine_refine():
    Assum = And()
    Residual = cosh(0) - 1
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-806-ground · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered true (solved)
@_in(_SETUP2)
def sp_acj4_806_ground__satsimp_trigsimp():
    Assum = And()
    Residual = cosh(0) - 1
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-806-ground · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered true (solved)
@_in(_SETUP2)
def sp_acj4_806_ground__satrefine_simplify():
    Assum = And()
    Residual = cosh(0) - 1
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-806-ground · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered true (solved)
@_in(_SETUP3)
def sp_acj4_806_ground__sympy_auto():
    Residual = cosh(0) - 1
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-806-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered true (solved)
@_in(_SETUP3)
def sp_acj4_806_ground__sympy_ask():
    Assum = And()
    Residual = cosh(0) - 1
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-806-ground · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered true (solved)
@_in(_SETUP4)
def sp_acj4_806_ground__sympy_satask():
    Assum = And()
    Residual = cosh(0) - 1
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-806-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered true (solved)
@_in(_SETUP3)
def sp_acj4_806_ground__sympy_refine():
    Assum = And()
    Residual = cosh(0) - 1
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-806-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered true (solved)
@_in(_SETUP3)
def sp_acj4_806_ground__sympy_simplify():
    Residual = cosh(0) - 1
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-806-ground · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered true (solved)
@_in(_SETUP5)
def sp_acj4_806_ground__sympy_extras_ask():
    Assum = And()
    Residual = cosh(0) - 1
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-806-ground · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered true (solved)
@_in(_SETUP5)
def sp_acj4_806_ground__sympy_extras_refine():
    Assum = And()
    Residual = cosh(0) - 1
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-806-ground · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered true (solved)
@_in(_SETUP5)
def sp_acj4_806_ground__sympy_extras_simplify():
    Assum = And()
    Residual = cosh(0) - 1
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-813-ground · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered true (solved)
@_in(_SETUP1)
def sp_acj4_813_ground__satassume_ask():
    Assum = And()
    Residual = sinh(0) - 0
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-813-ground · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered true (solved)
@_in(_SETUP2)
def sp_acj4_813_ground__satrefine_refine():
    Assum = And()
    Residual = sinh(0) - 0
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-813-ground · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered true (solved)
@_in(_SETUP2)
def sp_acj4_813_ground__satsimp_trigsimp():
    Assum = And()
    Residual = sinh(0) - 0
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-813-ground · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered true (solved)
@_in(_SETUP2)
def sp_acj4_813_ground__satrefine_simplify():
    Assum = And()
    Residual = sinh(0) - 0
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-813-ground · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered true (solved)
@_in(_SETUP3)
def sp_acj4_813_ground__sympy_auto():
    Residual = sinh(0) - 0
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-813-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered true (solved)
@_in(_SETUP3)
def sp_acj4_813_ground__sympy_ask():
    Assum = And()
    Residual = sinh(0) - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-813-ground · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered true (solved)
@_in(_SETUP4)
def sp_acj4_813_ground__sympy_satask():
    Assum = And()
    Residual = sinh(0) - 0
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-813-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered true (solved)
@_in(_SETUP3)
def sp_acj4_813_ground__sympy_refine():
    Assum = And()
    Residual = sinh(0) - 0
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-813-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered true (solved)
@_in(_SETUP3)
def sp_acj4_813_ground__sympy_simplify():
    Residual = sinh(0) - 0
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-813-ground · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered true (solved)
@_in(_SETUP5)
def sp_acj4_813_ground__sympy_extras_ask():
    Assum = And()
    Residual = sinh(0) - 0
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-813-ground · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered true (solved)
@_in(_SETUP5)
def sp_acj4_813_ground__sympy_extras_refine():
    Assum = And()
    Residual = sinh(0) - 0
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-813-ground · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered true (solved)
@_in(_SETUP5)
def sp_acj4_813_ground__sympy_extras_simplify():
    Assum = And()
    Residual = sinh(0) - 0
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-816-ground · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-002222 answered true (solved)
@_in(_SETUP1)
def sp_acj4_816_ground__satassume_ask():
    Assum = And()
    Residual = tanh(0) - 0
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-816-ground · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-001852 answered true (solved)
@_in(_SETUP2)
def sp_acj4_816_ground__satrefine_refine():
    Assum = And()
    Residual = tanh(0) - 0
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-816-ground · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-002313 answered true (solved)
@_in(_SETUP2)
def sp_acj4_816_ground__satsimp_trigsimp():
    Assum = And()
    Residual = tanh(0) - 0
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-816-ground · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-002233 answered true (solved)
@_in(_SETUP2)
def sp_acj4_816_ground__satrefine_simplify():
    Assum = And()
    Residual = tanh(0) - 0
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-816-ground · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-001315 answered true (solved)
@_in(_SETUP3)
def sp_acj4_816_ground__sympy_auto():
    Residual = tanh(0) - 0
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-816-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-001321 answered true (solved)
@_in(_SETUP3)
def sp_acj4_816_ground__sympy_ask():
    Assum = And()
    Residual = tanh(0) - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-816-ground · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered true (solved)
@_in(_SETUP4)
def sp_acj4_816_ground__sympy_satask():
    Assum = And()
    Residual = tanh(0) - 0
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-816-ground · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-001510 answered true (solved)
@_in(_SETUP3)
def sp_acj4_816_ground__sympy_refine():
    Assum = And()
    Residual = tanh(0) - 0
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-816-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-001834 answered true (solved)
@_in(_SETUP3)
def sp_acj4_816_ground__sympy_simplify():
    Residual = tanh(0) - 0
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-816-ground · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-002324 answered true (solved)
@_in(_SETUP5)
def sp_acj4_816_ground__sympy_extras_ask():
    Assum = And()
    Residual = tanh(0) - 0
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-816-ground · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-002919 answered true (solved)
@_in(_SETUP5)
def sp_acj4_816_ground__sympy_extras_refine():
    Assum = And()
    Residual = tanh(0) - 0
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-816-ground · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-003616 answered true (solved)
@_in(_SETUP5)
def sp_acj4_816_ground__sympy_extras_simplify():
    Assum = And()
    Residual = tanh(0) - 0
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# (case, system, expected, the stored run's answer, that run, its function)
CASES = [
    ('sp-acj4-0-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261028-002222', sp_acj4_0_real__satassume_ask),
    ('sp-acj4-0-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-001852', sp_acj4_0_real__satrefine_refine),
    ('sp-acj4-0-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_0_real__satsimp_trigsimp),
    ('sp-acj4-0-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-002233', sp_acj4_0_real__satrefine_simplify),
    ('sp-acj4-0-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261028-001315', sp_acj4_0_real__sympy_auto),
    ('sp-acj4-0-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261028-001321', sp_acj4_0_real__sympy_ask),
    ('sp-acj4-0-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261020-072057', sp_acj4_0_real__sympy_satask),
    ('sp-acj4-0-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261028-001510', sp_acj4_0_real__sympy_refine),
    ('sp-acj4-0-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261028-001834', sp_acj4_0_real__sympy_simplify),
    ('sp-acj4-0-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_0_real__sympy_extras_ask),
    ('sp-acj4-0-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_0_real__sympy_extras_refine),
    ('sp-acj4-0-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_0_real__sympy_extras_simplify),
    ('sp-acj4-115-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261028-002222', sp_acj4_115_real__satassume_ask),
    ('sp-acj4-115-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-001852', sp_acj4_115_real__satrefine_refine),
    ('sp-acj4-115-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_115_real__satsimp_trigsimp),
    ('sp-acj4-115-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-002233', sp_acj4_115_real__satrefine_simplify),
    ('sp-acj4-115-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261028-001315', sp_acj4_115_real__sympy_auto),
    ('sp-acj4-115-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261028-001321', sp_acj4_115_real__sympy_ask),
    ('sp-acj4-115-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261020-072057', sp_acj4_115_real__sympy_satask),
    ('sp-acj4-115-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261028-001510', sp_acj4_115_real__sympy_refine),
    ('sp-acj4-115-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-001834', sp_acj4_115_real__sympy_simplify),
    ('sp-acj4-115-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-002324', sp_acj4_115_real__sympy_extras_ask),
    ('sp-acj4-115-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-002919', sp_acj4_115_real__sympy_extras_refine),
    ('sp-acj4-115-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-003616', sp_acj4_115_real__sympy_extras_simplify),
    ('sp-acj4-116-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261028-002222', sp_acj4_116_real__satassume_ask),
    ('sp-acj4-116-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-001852', sp_acj4_116_real__satrefine_refine),
    ('sp-acj4-116-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_116_real__satsimp_trigsimp),
    ('sp-acj4-116-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-002233', sp_acj4_116_real__satrefine_simplify),
    ('sp-acj4-116-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261028-001315', sp_acj4_116_real__sympy_auto),
    ('sp-acj4-116-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261028-001321', sp_acj4_116_real__sympy_ask),
    ('sp-acj4-116-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261020-072057', sp_acj4_116_real__sympy_satask),
    ('sp-acj4-116-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261028-001510', sp_acj4_116_real__sympy_refine),
    ('sp-acj4-116-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-001834', sp_acj4_116_real__sympy_simplify),
    ('sp-acj4-116-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-002324', sp_acj4_116_real__sympy_extras_ask),
    ('sp-acj4-116-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-002919', sp_acj4_116_real__sympy_extras_refine),
    ('sp-acj4-116-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-003616', sp_acj4_116_real__sympy_extras_simplify),
    ('sp-acj4-130-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_130_real__satassume_ask),
    ('sp-acj4-130-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_130_real__satrefine_refine),
    ('sp-acj4-130-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_130_real__satsimp_trigsimp),
    ('sp-acj4-130-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_130_real__satrefine_simplify),
    ('sp-acj4-130-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_130_real__sympy_auto),
    ('sp-acj4-130-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_130_real__sympy_ask),
    ('sp-acj4-130-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_130_real__sympy_satask),
    ('sp-acj4-130-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_130_real__sympy_refine),
    ('sp-acj4-130-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_130_real__sympy_simplify),
    ('sp-acj4-130-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_130_real__sympy_extras_ask),
    ('sp-acj4-130-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_130_real__sympy_extras_refine),
    ('sp-acj4-130-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_130_real__sympy_extras_simplify),
    ('sp-acj4-151-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_151_real__satassume_ask),
    ('sp-acj4-151-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_151_real__satrefine_refine),
    ('sp-acj4-151-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_151_real__satsimp_trigsimp),
    ('sp-acj4-151-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_151_real__satrefine_simplify),
    ('sp-acj4-151-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_151_real__sympy_auto),
    ('sp-acj4-151-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_151_real__sympy_ask),
    ('sp-acj4-151-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_151_real__sympy_satask),
    ('sp-acj4-151-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_151_real__sympy_refine),
    ('sp-acj4-151-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_151_real__sympy_simplify),
    ('sp-acj4-151-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_151_real__sympy_extras_ask),
    ('sp-acj4-151-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_151_real__sympy_extras_refine),
    ('sp-acj4-151-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_151_real__sympy_extras_simplify),
    ('sp-acj4-154-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261028-002222', sp_acj4_154_real__satassume_ask),
    ('sp-acj4-154-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261028-001852', sp_acj4_154_real__satrefine_refine),
    ('sp-acj4-154-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_154_real__satsimp_trigsimp),
    ('sp-acj4-154-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_154_real__satrefine_simplify),
    ('sp-acj4-154-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261028-001315', sp_acj4_154_real__sympy_auto),
    ('sp-acj4-154-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261028-001321', sp_acj4_154_real__sympy_ask),
    ('sp-acj4-154-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261020-072057', sp_acj4_154_real__sympy_satask),
    ('sp-acj4-154-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261028-001510', sp_acj4_154_real__sympy_refine),
    ('sp-acj4-154-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261028-001834', sp_acj4_154_real__sympy_simplify),
    ('sp-acj4-154-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_154_real__sympy_extras_refine),
    ('sp-acj4-154-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_154_real__sympy_extras_simplify),
    ('sp-acj4-156-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_156_real__satassume_ask),
    ('sp-acj4-156-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_156_real__satrefine_refine),
    ('sp-acj4-156-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_156_real__satsimp_trigsimp),
    ('sp-acj4-156-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_156_real__satrefine_simplify),
    ('sp-acj4-156-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_156_real__sympy_auto),
    ('sp-acj4-156-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_156_real__sympy_ask),
    ('sp-acj4-156-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_156_real__sympy_satask),
    ('sp-acj4-156-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_156_real__sympy_refine),
    ('sp-acj4-156-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_156_real__sympy_simplify),
    ('sp-acj4-156-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_156_real__sympy_extras_ask),
    ('sp-acj4-156-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_156_real__sympy_extras_refine),
    ('sp-acj4-156-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_156_real__sympy_extras_simplify),
    ('sp-acj4-180-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_180_real__satassume_ask),
    ('sp-acj4-180-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_180_real__satrefine_refine),
    ('sp-acj4-180-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_180_real__satsimp_trigsimp),
    ('sp-acj4-180-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_180_real__satrefine_simplify),
    ('sp-acj4-180-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_180_real__sympy_auto),
    ('sp-acj4-180-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_180_real__sympy_ask),
    ('sp-acj4-180-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_180_real__sympy_satask),
    ('sp-acj4-180-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_180_real__sympy_refine),
    ('sp-acj4-180-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_180_real__sympy_simplify),
    ('sp-acj4-180-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_180_real__sympy_extras_ask),
    ('sp-acj4-180-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_180_real__sympy_extras_refine),
    ('sp-acj4-180-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_180_real__sympy_extras_simplify),
    ('sp-acj4-183-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_183_real__satassume_ask),
    ('sp-acj4-183-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_183_real__satrefine_refine),
    ('sp-acj4-183-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_183_real__satsimp_trigsimp),
    ('sp-acj4-183-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_183_real__satrefine_simplify),
    ('sp-acj4-183-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_183_real__sympy_auto),
    ('sp-acj4-183-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_183_real__sympy_ask),
    ('sp-acj4-183-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_183_real__sympy_satask),
    ('sp-acj4-183-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_183_real__sympy_refine),
    ('sp-acj4-183-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_183_real__sympy_simplify),
    ('sp-acj4-183-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_183_real__sympy_extras_ask),
    ('sp-acj4-183-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_183_real__sympy_extras_refine),
    ('sp-acj4-183-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_183_real__sympy_extras_simplify),
    ('sp-acj4-189-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261028-002222', sp_acj4_189_real__satassume_ask),
    ('sp-acj4-189-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261028-001852', sp_acj4_189_real__satrefine_refine),
    ('sp-acj4-189-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_189_real__satsimp_trigsimp),
    ('sp-acj4-189-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_189_real__satrefine_simplify),
    ('sp-acj4-189-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261028-001315', sp_acj4_189_real__sympy_auto),
    ('sp-acj4-189-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261028-001321', sp_acj4_189_real__sympy_ask),
    ('sp-acj4-189-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261020-072057', sp_acj4_189_real__sympy_satask),
    ('sp-acj4-189-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261028-001510', sp_acj4_189_real__sympy_refine),
    ('sp-acj4-189-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261028-001834', sp_acj4_189_real__sympy_simplify),
    ('sp-acj4-189-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_189_real__sympy_extras_ask),
    ('sp-acj4-189-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_189_real__sympy_extras_refine),
    ('sp-acj4-189-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_189_real__sympy_extras_simplify),
    ('sp-acj4-190-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261028-002222', sp_acj4_190_real__satassume_ask),
    ('sp-acj4-190-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261028-001852', sp_acj4_190_real__satrefine_refine),
    ('sp-acj4-190-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_190_real__satsimp_trigsimp),
    ('sp-acj4-190-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_190_real__satrefine_simplify),
    ('sp-acj4-190-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261028-001315', sp_acj4_190_real__sympy_auto),
    ('sp-acj4-190-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261028-001321', sp_acj4_190_real__sympy_ask),
    ('sp-acj4-190-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261020-072057', sp_acj4_190_real__sympy_satask),
    ('sp-acj4-190-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261028-001510', sp_acj4_190_real__sympy_refine),
    ('sp-acj4-190-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261028-001834', sp_acj4_190_real__sympy_simplify),
    ('sp-acj4-190-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_190_real__sympy_extras_ask),
    ('sp-acj4-190-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_190_real__sympy_extras_refine),
    ('sp-acj4-190-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_190_real__sympy_extras_simplify),
    ('sp-acj4-191-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261028-002222', sp_acj4_191_real__satassume_ask),
    ('sp-acj4-191-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261028-001852', sp_acj4_191_real__satrefine_refine),
    ('sp-acj4-191-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_191_real__satsimp_trigsimp),
    ('sp-acj4-191-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_191_real__satrefine_simplify),
    ('sp-acj4-191-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261028-001315', sp_acj4_191_real__sympy_auto),
    ('sp-acj4-191-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261028-001321', sp_acj4_191_real__sympy_ask),
    ('sp-acj4-191-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261020-072057', sp_acj4_191_real__sympy_satask),
    ('sp-acj4-191-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261028-001510', sp_acj4_191_real__sympy_refine),
    ('sp-acj4-191-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261028-001834', sp_acj4_191_real__sympy_simplify),
    ('sp-acj4-191-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_191_real__sympy_extras_ask),
    ('sp-acj4-191-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_191_real__sympy_extras_refine),
    ('sp-acj4-191-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_191_real__sympy_extras_simplify),
    ('sp-acj4-203-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_203_real__satassume_ask),
    ('sp-acj4-203-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_203_real__satrefine_refine),
    ('sp-acj4-203-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_203_real__satsimp_trigsimp),
    ('sp-acj4-203-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_203_real__satrefine_simplify),
    ('sp-acj4-203-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_203_real__sympy_auto),
    ('sp-acj4-203-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_203_real__sympy_ask),
    ('sp-acj4-203-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_203_real__sympy_satask),
    ('sp-acj4-203-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_203_real__sympy_refine),
    ('sp-acj4-203-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_203_real__sympy_simplify),
    ('sp-acj4-203-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_203_real__sympy_extras_ask),
    ('sp-acj4-203-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_203_real__sympy_extras_refine),
    ('sp-acj4-203-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_203_real__sympy_extras_simplify),
    ('sp-acj4-229-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-002222', sp_acj4_229_real__satassume_ask),
    ('sp-acj4-229-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-001852', sp_acj4_229_real__satrefine_refine),
    ('sp-acj4-229-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-002313', sp_acj4_229_real__satsimp_trigsimp),
    ('sp-acj4-229-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-002233', sp_acj4_229_real__satrefine_simplify),
    ('sp-acj4-229-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-001315', sp_acj4_229_real__sympy_auto),
    ('sp-acj4-229-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-001321', sp_acj4_229_real__sympy_ask),
    ('sp-acj4-229-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261020-072057', sp_acj4_229_real__sympy_satask),
    ('sp-acj4-229-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-001510', sp_acj4_229_real__sympy_refine),
    ('sp-acj4-229-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-001834', sp_acj4_229_real__sympy_simplify),
    ('sp-acj4-229-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-002324', sp_acj4_229_real__sympy_extras_ask),
    ('sp-acj4-229-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-002919', sp_acj4_229_real__sympy_extras_refine),
    ('sp-acj4-229-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-003616', sp_acj4_229_real__sympy_extras_simplify),
    ('sp-acj4-234-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_234_real__satassume_ask),
    ('sp-acj4-234-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_234_real__satrefine_refine),
    ('sp-acj4-234-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_234_real__satsimp_trigsimp),
    ('sp-acj4-234-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_234_real__satrefine_simplify),
    ('sp-acj4-234-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_234_real__sympy_auto),
    ('sp-acj4-234-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_234_real__sympy_ask),
    ('sp-acj4-234-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_234_real__sympy_satask),
    ('sp-acj4-234-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_234_real__sympy_refine),
    ('sp-acj4-234-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_234_real__sympy_simplify),
    ('sp-acj4-234-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_234_real__sympy_extras_ask),
    ('sp-acj4-234-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_234_real__sympy_extras_refine),
    ('sp-acj4-234-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_234_real__sympy_extras_simplify),
    ('sp-acj4-241-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_241_real__satassume_ask),
    ('sp-acj4-241-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_241_real__satrefine_refine),
    ('sp-acj4-241-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_241_real__satsimp_trigsimp),
    ('sp-acj4-241-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_241_real__satrefine_simplify),
    ('sp-acj4-241-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_241_real__sympy_auto),
    ('sp-acj4-241-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_241_real__sympy_ask),
    ('sp-acj4-241-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_241_real__sympy_satask),
    ('sp-acj4-241-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_241_real__sympy_refine),
    ('sp-acj4-241-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_241_real__sympy_simplify),
    ('sp-acj4-241-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_241_real__sympy_extras_ask),
    ('sp-acj4-241-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_241_real__sympy_extras_refine),
    ('sp-acj4-241-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_241_real__sympy_extras_simplify),
    ('sp-acj4-247-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_247_real__satassume_ask),
    ('sp-acj4-247-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_247_real__satrefine_refine),
    ('sp-acj4-247-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_247_real__satsimp_trigsimp),
    ('sp-acj4-247-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_247_real__satrefine_simplify),
    ('sp-acj4-247-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_247_real__sympy_auto),
    ('sp-acj4-247-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_247_real__sympy_ask),
    ('sp-acj4-247-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_247_real__sympy_satask),
    ('sp-acj4-247-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_247_real__sympy_refine),
    ('sp-acj4-247-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_247_real__sympy_simplify),
    ('sp-acj4-247-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_247_real__sympy_extras_ask),
    ('sp-acj4-247-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_247_real__sympy_extras_refine),
    ('sp-acj4-247-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_247_real__sympy_extras_simplify),
    ('sp-acj4-260-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_260_real__satassume_ask),
    ('sp-acj4-260-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_260_real__satrefine_refine),
    ('sp-acj4-260-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_260_real__satsimp_trigsimp),
    ('sp-acj4-260-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_260_real__satrefine_simplify),
    ('sp-acj4-260-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_260_real__sympy_auto),
    ('sp-acj4-260-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_260_real__sympy_ask),
    ('sp-acj4-260-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_260_real__sympy_satask),
    ('sp-acj4-260-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_260_real__sympy_refine),
    ('sp-acj4-260-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_260_real__sympy_simplify),
    ('sp-acj4-260-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_260_real__sympy_extras_ask),
    ('sp-acj4-260-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_260_real__sympy_extras_refine),
    ('sp-acj4-260-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_260_real__sympy_extras_simplify),
    ('sp-acj4-261-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261028-002222', sp_acj4_261_real__satassume_ask),
    ('sp-acj4-261-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-001852', sp_acj4_261_real__satrefine_refine),
    ('sp-acj4-261-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_261_real__satsimp_trigsimp),
    ('sp-acj4-261-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-002233', sp_acj4_261_real__satrefine_simplify),
    ('sp-acj4-261-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261028-001315', sp_acj4_261_real__sympy_auto),
    ('sp-acj4-261-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261028-001321', sp_acj4_261_real__sympy_ask),
    ('sp-acj4-261-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261020-072057', sp_acj4_261_real__sympy_satask),
    ('sp-acj4-261-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261028-001510', sp_acj4_261_real__sympy_refine),
    ('sp-acj4-261-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-001834', sp_acj4_261_real__sympy_simplify),
    ('sp-acj4-261-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-002324', sp_acj4_261_real__sympy_extras_ask),
    ('sp-acj4-261-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-002919', sp_acj4_261_real__sympy_extras_refine),
    ('sp-acj4-261-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-003616', sp_acj4_261_real__sympy_extras_simplify),
    ('sp-acj4-266-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_266_real__satassume_ask),
    ('sp-acj4-266-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_266_real__satrefine_refine),
    ('sp-acj4-266-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_266_real__satsimp_trigsimp),
    ('sp-acj4-266-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_266_real__satrefine_simplify),
    ('sp-acj4-266-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_266_real__sympy_auto),
    ('sp-acj4-266-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_266_real__sympy_ask),
    ('sp-acj4-266-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_266_real__sympy_satask),
    ('sp-acj4-266-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_266_real__sympy_refine),
    ('sp-acj4-266-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_266_real__sympy_simplify),
    ('sp-acj4-266-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_266_real__sympy_extras_ask),
    ('sp-acj4-266-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_266_real__sympy_extras_refine),
    ('sp-acj4-266-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_266_real__sympy_extras_simplify),
    ('sp-acj4-267-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_267_real__satassume_ask),
    ('sp-acj4-267-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_267_real__satrefine_refine),
    ('sp-acj4-267-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_267_real__satsimp_trigsimp),
    ('sp-acj4-267-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_267_real__satrefine_simplify),
    ('sp-acj4-267-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_267_real__sympy_auto),
    ('sp-acj4-267-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_267_real__sympy_ask),
    ('sp-acj4-267-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_267_real__sympy_satask),
    ('sp-acj4-267-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_267_real__sympy_refine),
    ('sp-acj4-267-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_267_real__sympy_simplify),
    ('sp-acj4-267-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_267_real__sympy_extras_ask),
    ('sp-acj4-267-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_267_real__sympy_extras_refine),
    ('sp-acj4-267-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_267_real__sympy_extras_simplify),
    ('sp-acj4-29-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_29_real__satassume_ask),
    ('sp-acj4-29-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_29_real__satrefine_refine),
    ('sp-acj4-29-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_29_real__satsimp_trigsimp),
    ('sp-acj4-29-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_29_real__satrefine_simplify),
    ('sp-acj4-29-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_29_real__sympy_auto),
    ('sp-acj4-29-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_29_real__sympy_ask),
    ('sp-acj4-29-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_29_real__sympy_satask),
    ('sp-acj4-29-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_29_real__sympy_refine),
    ('sp-acj4-29-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_29_real__sympy_simplify),
    ('sp-acj4-29-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_29_real__sympy_extras_ask),
    ('sp-acj4-29-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_29_real__sympy_extras_refine),
    ('sp-acj4-29-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_29_real__sympy_extras_simplify),
    ('sp-acj4-3-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261028-002222', sp_acj4_3_real__satassume_ask),
    ('sp-acj4-3-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-001852', sp_acj4_3_real__satrefine_refine),
    ('sp-acj4-3-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_3_real__satsimp_trigsimp),
    ('sp-acj4-3-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-002233', sp_acj4_3_real__satrefine_simplify),
    ('sp-acj4-3-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261028-001315', sp_acj4_3_real__sympy_auto),
    ('sp-acj4-3-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261028-001321', sp_acj4_3_real__sympy_ask),
    ('sp-acj4-3-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261020-072057', sp_acj4_3_real__sympy_satask),
    ('sp-acj4-3-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261028-001510', sp_acj4_3_real__sympy_refine),
    ('sp-acj4-3-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261028-001834', sp_acj4_3_real__sympy_simplify),
    ('sp-acj4-3-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-002324', sp_acj4_3_real__sympy_extras_ask),
    ('sp-acj4-3-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_3_real__sympy_extras_refine),
    ('sp-acj4-3-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-003616', sp_acj4_3_real__sympy_extras_simplify),
    ('sp-acj4-343-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-002222', sp_acj4_343_real__satassume_ask),
    ('sp-acj4-343-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-001852', sp_acj4_343_real__satrefine_refine),
    ('sp-acj4-343-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-002313', sp_acj4_343_real__satsimp_trigsimp),
    ('sp-acj4-343-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-002233', sp_acj4_343_real__satrefine_simplify),
    ('sp-acj4-343-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-001315', sp_acj4_343_real__sympy_auto),
    ('sp-acj4-343-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-001321', sp_acj4_343_real__sympy_ask),
    ('sp-acj4-343-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261020-072057', sp_acj4_343_real__sympy_satask),
    ('sp-acj4-343-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-001510', sp_acj4_343_real__sympy_refine),
    ('sp-acj4-343-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-001834', sp_acj4_343_real__sympy_simplify),
    ('sp-acj4-343-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-002324', sp_acj4_343_real__sympy_extras_ask),
    ('sp-acj4-343-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-002919', sp_acj4_343_real__sympy_extras_refine),
    ('sp-acj4-343-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-003616', sp_acj4_343_real__sympy_extras_simplify),
    ('sp-acj4-344-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_344_real__satassume_ask),
    ('sp-acj4-344-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_344_real__satrefine_refine),
    ('sp-acj4-344-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_344_real__satsimp_trigsimp),
    ('sp-acj4-344-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_344_real__satrefine_simplify),
    ('sp-acj4-344-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_344_real__sympy_auto),
    ('sp-acj4-344-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_344_real__sympy_ask),
    ('sp-acj4-344-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_344_real__sympy_satask),
    ('sp-acj4-344-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_344_real__sympy_refine),
    ('sp-acj4-344-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_344_real__sympy_simplify),
    ('sp-acj4-344-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_344_real__sympy_extras_ask),
    ('sp-acj4-344-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_344_real__sympy_extras_refine),
    ('sp-acj4-344-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_344_real__sympy_extras_simplify),
    ('sp-acj4-378-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261028-002222', sp_acj4_378_real__satassume_ask),
    ('sp-acj4-378-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-001852', sp_acj4_378_real__satrefine_refine),
    ('sp-acj4-378-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_378_real__satsimp_trigsimp),
    ('sp-acj4-378-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-002233', sp_acj4_378_real__satrefine_simplify),
    ('sp-acj4-378-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-001315', sp_acj4_378_real__sympy_auto),
    ('sp-acj4-378-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261028-001321', sp_acj4_378_real__sympy_ask),
    ('sp-acj4-378-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261020-072057', sp_acj4_378_real__sympy_satask),
    ('sp-acj4-378-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261028-001510', sp_acj4_378_real__sympy_refine),
    ('sp-acj4-378-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-001834', sp_acj4_378_real__sympy_simplify),
    ('sp-acj4-378-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_378_real__sympy_extras_ask),
    ('sp-acj4-378-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-002919', sp_acj4_378_real__sympy_extras_refine),
    ('sp-acj4-378-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-003616', sp_acj4_378_real__sympy_extras_simplify),
    ('sp-acj4-380-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261028-002222', sp_acj4_380_real__satassume_ask),
    ('sp-acj4-380-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-001852', sp_acj4_380_real__satrefine_refine),
    ('sp-acj4-380-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_380_real__satsimp_trigsimp),
    ('sp-acj4-380-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-002233', sp_acj4_380_real__satrefine_simplify),
    ('sp-acj4-380-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-001315', sp_acj4_380_real__sympy_auto),
    ('sp-acj4-380-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261028-001321', sp_acj4_380_real__sympy_ask),
    ('sp-acj4-380-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261020-072057', sp_acj4_380_real__sympy_satask),
    ('sp-acj4-380-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261028-001510', sp_acj4_380_real__sympy_refine),
    ('sp-acj4-380-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-001834', sp_acj4_380_real__sympy_simplify),
    ('sp-acj4-380-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_380_real__sympy_extras_ask),
    ('sp-acj4-380-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-002919', sp_acj4_380_real__sympy_extras_refine),
    ('sp-acj4-380-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-003616', sp_acj4_380_real__sympy_extras_simplify),
    ('sp-acj4-392-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_392_real__satassume_ask),
    ('sp-acj4-392-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_392_real__satrefine_refine),
    ('sp-acj4-392-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_392_real__satsimp_trigsimp),
    ('sp-acj4-392-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_392_real__satrefine_simplify),
    ('sp-acj4-392-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_392_real__sympy_auto),
    ('sp-acj4-392-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_392_real__sympy_ask),
    ('sp-acj4-392-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_392_real__sympy_satask),
    ('sp-acj4-392-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_392_real__sympy_refine),
    ('sp-acj4-392-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_392_real__sympy_simplify),
    ('sp-acj4-392-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_392_real__sympy_extras_ask),
    ('sp-acj4-392-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_392_real__sympy_extras_refine),
    ('sp-acj4-392-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_392_real__sympy_extras_simplify),
    ('sp-acj4-403-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_403_real__satassume_ask),
    ('sp-acj4-403-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_403_real__satrefine_refine),
    ('sp-acj4-403-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_403_real__satsimp_trigsimp),
    ('sp-acj4-403-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_403_real__satrefine_simplify),
    ('sp-acj4-403-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_403_real__sympy_auto),
    ('sp-acj4-403-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_403_real__sympy_ask),
    ('sp-acj4-403-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_403_real__sympy_satask),
    ('sp-acj4-403-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_403_real__sympy_refine),
    ('sp-acj4-403-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_403_real__sympy_simplify),
    ('sp-acj4-403-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_403_real__sympy_extras_ask),
    ('sp-acj4-403-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_403_real__sympy_extras_refine),
    ('sp-acj4-403-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_403_real__sympy_extras_simplify),
    ('sp-acj4-410-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-002222', sp_acj4_410_real__satassume_ask),
    ('sp-acj4-410-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-001852', sp_acj4_410_real__satrefine_refine),
    ('sp-acj4-410-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-002313', sp_acj4_410_real__satsimp_trigsimp),
    ('sp-acj4-410-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-002233', sp_acj4_410_real__satrefine_simplify),
    ('sp-acj4-410-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-001315', sp_acj4_410_real__sympy_auto),
    ('sp-acj4-410-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-001321', sp_acj4_410_real__sympy_ask),
    ('sp-acj4-410-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261020-072057', sp_acj4_410_real__sympy_satask),
    ('sp-acj4-410-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-001510', sp_acj4_410_real__sympy_refine),
    ('sp-acj4-410-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-001834', sp_acj4_410_real__sympy_simplify),
    ('sp-acj4-410-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-002324', sp_acj4_410_real__sympy_extras_ask),
    ('sp-acj4-410-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-002919', sp_acj4_410_real__sympy_extras_refine),
    ('sp-acj4-410-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-003616', sp_acj4_410_real__sympy_extras_simplify),
    ('sp-acj4-416-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_416_real__satassume_ask),
    ('sp-acj4-416-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_416_real__satrefine_refine),
    ('sp-acj4-416-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_416_real__satsimp_trigsimp),
    ('sp-acj4-416-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_416_real__satrefine_simplify),
    ('sp-acj4-416-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_416_real__sympy_auto),
    ('sp-acj4-416-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_416_real__sympy_ask),
    ('sp-acj4-416-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_416_real__sympy_satask),
    ('sp-acj4-416-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_416_real__sympy_refine),
    ('sp-acj4-416-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_416_real__sympy_simplify),
    ('sp-acj4-416-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_416_real__sympy_extras_ask),
    ('sp-acj4-416-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_416_real__sympy_extras_refine),
    ('sp-acj4-416-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_416_real__sympy_extras_simplify),
    ('sp-acj4-420-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_420_real__satassume_ask),
    ('sp-acj4-420-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_420_real__satrefine_refine),
    ('sp-acj4-420-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_420_real__satsimp_trigsimp),
    ('sp-acj4-420-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_420_real__satrefine_simplify),
    ('sp-acj4-420-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_420_real__sympy_auto),
    ('sp-acj4-420-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_420_real__sympy_ask),
    ('sp-acj4-420-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_420_real__sympy_satask),
    ('sp-acj4-420-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_420_real__sympy_refine),
    ('sp-acj4-420-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_420_real__sympy_simplify),
    ('sp-acj4-420-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_420_real__sympy_extras_ask),
    ('sp-acj4-420-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_420_real__sympy_extras_refine),
    ('sp-acj4-420-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_420_real__sympy_extras_simplify),
    ('sp-acj4-430-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_430_real__satassume_ask),
    ('sp-acj4-430-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_430_real__satrefine_refine),
    ('sp-acj4-430-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_430_real__satsimp_trigsimp),
    ('sp-acj4-430-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_430_real__satrefine_simplify),
    ('sp-acj4-430-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_430_real__sympy_auto),
    ('sp-acj4-430-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_430_real__sympy_ask),
    ('sp-acj4-430-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_430_real__sympy_satask),
    ('sp-acj4-430-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_430_real__sympy_refine),
    ('sp-acj4-430-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_430_real__sympy_simplify),
    ('sp-acj4-430-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_430_real__sympy_extras_ask),
    ('sp-acj4-430-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_430_real__sympy_extras_refine),
    ('sp-acj4-430-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_430_real__sympy_extras_simplify),
    ('sp-acj4-433-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_433_real__satassume_ask),
    ('sp-acj4-433-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_433_real__satrefine_refine),
    ('sp-acj4-433-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_433_real__satsimp_trigsimp),
    ('sp-acj4-433-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_433_real__satrefine_simplify),
    ('sp-acj4-433-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_433_real__sympy_auto),
    ('sp-acj4-433-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_433_real__sympy_ask),
    ('sp-acj4-433-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_433_real__sympy_satask),
    ('sp-acj4-433-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_433_real__sympy_refine),
    ('sp-acj4-433-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_433_real__sympy_simplify),
    ('sp-acj4-433-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_433_real__sympy_extras_ask),
    ('sp-acj4-433-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_433_real__sympy_extras_refine),
    ('sp-acj4-433-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_433_real__sympy_extras_simplify),
    ('sp-acj4-442-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_442_real__satassume_ask),
    ('sp-acj4-442-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_442_real__satrefine_refine),
    ('sp-acj4-442-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_442_real__satsimp_trigsimp),
    ('sp-acj4-442-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_442_real__satrefine_simplify),
    ('sp-acj4-442-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_442_real__sympy_auto),
    ('sp-acj4-442-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_442_real__sympy_ask),
    ('sp-acj4-442-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_442_real__sympy_satask),
    ('sp-acj4-442-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_442_real__sympy_refine),
    ('sp-acj4-442-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_442_real__sympy_simplify),
    ('sp-acj4-442-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_442_real__sympy_extras_ask),
    ('sp-acj4-442-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_442_real__sympy_extras_refine),
    ('sp-acj4-442-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_442_real__sympy_extras_simplify),
    ('sp-acj4-449-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261028-002222', sp_acj4_449_real__satassume_ask),
    ('sp-acj4-449-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261028-001852', sp_acj4_449_real__satrefine_refine),
    ('sp-acj4-449-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_449_real__satsimp_trigsimp),
    ('sp-acj4-449-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_449_real__satrefine_simplify),
    ('sp-acj4-449-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261028-001315', sp_acj4_449_real__sympy_auto),
    ('sp-acj4-449-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261028-001321', sp_acj4_449_real__sympy_ask),
    ('sp-acj4-449-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261020-072057', sp_acj4_449_real__sympy_satask),
    ('sp-acj4-449-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261028-001510', sp_acj4_449_real__sympy_refine),
    ('sp-acj4-449-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261028-001834', sp_acj4_449_real__sympy_simplify),
    ('sp-acj4-449-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-002324', sp_acj4_449_real__sympy_extras_ask),
    ('sp-acj4-449-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_449_real__sympy_extras_refine),
    ('sp-acj4-449-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-003616', sp_acj4_449_real__sympy_extras_simplify),
    ('sp-acj4-450-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-002222', sp_acj4_450_real__satassume_ask),
    ('sp-acj4-450-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-001852', sp_acj4_450_real__satrefine_refine),
    ('sp-acj4-450-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-002313', sp_acj4_450_real__satsimp_trigsimp),
    ('sp-acj4-450-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-002233', sp_acj4_450_real__satrefine_simplify),
    ('sp-acj4-450-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-001315', sp_acj4_450_real__sympy_auto),
    ('sp-acj4-450-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-001321', sp_acj4_450_real__sympy_ask),
    ('sp-acj4-450-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261020-072057', sp_acj4_450_real__sympy_satask),
    ('sp-acj4-450-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-001510', sp_acj4_450_real__sympy_refine),
    ('sp-acj4-450-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-001834', sp_acj4_450_real__sympy_simplify),
    ('sp-acj4-450-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-002324', sp_acj4_450_real__sympy_extras_ask),
    ('sp-acj4-450-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-002919', sp_acj4_450_real__sympy_extras_refine),
    ('sp-acj4-450-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-003616', sp_acj4_450_real__sympy_extras_simplify),
    ('sp-acj4-451-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-002222', sp_acj4_451_real__satassume_ask),
    ('sp-acj4-451-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-001852', sp_acj4_451_real__satrefine_refine),
    ('sp-acj4-451-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-002313', sp_acj4_451_real__satsimp_trigsimp),
    ('sp-acj4-451-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-002233', sp_acj4_451_real__satrefine_simplify),
    ('sp-acj4-451-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-001315', sp_acj4_451_real__sympy_auto),
    ('sp-acj4-451-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-001321', sp_acj4_451_real__sympy_ask),
    ('sp-acj4-451-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261020-072057', sp_acj4_451_real__sympy_satask),
    ('sp-acj4-451-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-001510', sp_acj4_451_real__sympy_refine),
    ('sp-acj4-451-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-001834', sp_acj4_451_real__sympy_simplify),
    ('sp-acj4-451-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-002324', sp_acj4_451_real__sympy_extras_ask),
    ('sp-acj4-451-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-002919', sp_acj4_451_real__sympy_extras_refine),
    ('sp-acj4-451-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-003616', sp_acj4_451_real__sympy_extras_simplify),
    ('sp-acj4-50-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261028-002222', sp_acj4_50_real__satassume_ask),
    ('sp-acj4-50-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-001852', sp_acj4_50_real__satrefine_refine),
    ('sp-acj4-50-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_50_real__satsimp_trigsimp),
    ('sp-acj4-50-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-002233', sp_acj4_50_real__satrefine_simplify),
    ('sp-acj4-50-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261028-001315', sp_acj4_50_real__sympy_auto),
    ('sp-acj4-50-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261028-001321', sp_acj4_50_real__sympy_ask),
    ('sp-acj4-50-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261020-072057', sp_acj4_50_real__sympy_satask),
    ('sp-acj4-50-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261028-001510', sp_acj4_50_real__sympy_refine),
    ('sp-acj4-50-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-001834', sp_acj4_50_real__sympy_simplify),
    ('sp-acj4-50-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-002324', sp_acj4_50_real__sympy_extras_ask),
    ('sp-acj4-50-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-002919', sp_acj4_50_real__sympy_extras_refine),
    ('sp-acj4-50-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-003616', sp_acj4_50_real__sympy_extras_simplify),
    ('sp-acj4-55-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_55_real__satassume_ask),
    ('sp-acj4-55-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_55_real__satrefine_refine),
    ('sp-acj4-55-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_55_real__satsimp_trigsimp),
    ('sp-acj4-55-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_55_real__satrefine_simplify),
    ('sp-acj4-55-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_55_real__sympy_auto),
    ('sp-acj4-55-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_55_real__sympy_ask),
    ('sp-acj4-55-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_55_real__sympy_satask),
    ('sp-acj4-55-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_55_real__sympy_refine),
    ('sp-acj4-55-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_55_real__sympy_simplify),
    ('sp-acj4-55-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_55_real__sympy_extras_ask),
    ('sp-acj4-55-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_55_real__sympy_extras_refine),
    ('sp-acj4-55-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_55_real__sympy_extras_simplify),
    ('sp-acj4-56-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-002222', sp_acj4_56_real__satassume_ask),
    ('sp-acj4-56-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-001852', sp_acj4_56_real__satrefine_refine),
    ('sp-acj4-56-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_56_real__satsimp_trigsimp),
    ('sp-acj4-56-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-002233', sp_acj4_56_real__satrefine_simplify),
    ('sp-acj4-56-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-001315', sp_acj4_56_real__sympy_auto),
    ('sp-acj4-56-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-001321', sp_acj4_56_real__sympy_ask),
    ('sp-acj4-56-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_56_real__sympy_satask),
    ('sp-acj4-56-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-001510', sp_acj4_56_real__sympy_refine),
    ('sp-acj4-56-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-001834', sp_acj4_56_real__sympy_simplify),
    ('sp-acj4-56-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-002324', sp_acj4_56_real__sympy_extras_ask),
    ('sp-acj4-56-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_56_real__sympy_extras_refine),
    ('sp-acj4-56-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-003616', sp_acj4_56_real__sympy_extras_simplify),
    ('sp-acj4-6-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261028-002222', sp_acj4_6_real__satassume_ask),
    ('sp-acj4-6-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-001852', sp_acj4_6_real__satrefine_refine),
    ('sp-acj4-6-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261028-002313', sp_acj4_6_real__satsimp_trigsimp),
    ('sp-acj4-6-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-002233', sp_acj4_6_real__satrefine_simplify),
    ('sp-acj4-6-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261028-001315', sp_acj4_6_real__sympy_auto),
    ('sp-acj4-6-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261028-001321', sp_acj4_6_real__sympy_ask),
    ('sp-acj4-6-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261020-072057', sp_acj4_6_real__sympy_satask),
    ('sp-acj4-6-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261028-001510', sp_acj4_6_real__sympy_refine),
    ('sp-acj4-6-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261028-001834', sp_acj4_6_real__sympy_simplify),
    ('sp-acj4-6-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-002324', sp_acj4_6_real__sympy_extras_ask),
    ('sp-acj4-6-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261028-002919', sp_acj4_6_real__sympy_extras_refine),
    ('sp-acj4-6-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-003616', sp_acj4_6_real__sympy_extras_simplify),
    ('sp-acj4-806-ground', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-002222', sp_acj4_806_ground__satassume_ask),
    ('sp-acj4-806-ground', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-001852', sp_acj4_806_ground__satrefine_refine),
    ('sp-acj4-806-ground', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-002313', sp_acj4_806_ground__satsimp_trigsimp),
    ('sp-acj4-806-ground', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-002233', sp_acj4_806_ground__satrefine_simplify),
    ('sp-acj4-806-ground', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-001315', sp_acj4_806_ground__sympy_auto),
    ('sp-acj4-806-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-001321', sp_acj4_806_ground__sympy_ask),
    ('sp-acj4-806-ground', 'sympy-satask', 'true', 'true', 'sympy-satask-20261020-072057', sp_acj4_806_ground__sympy_satask),
    ('sp-acj4-806-ground', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-001510', sp_acj4_806_ground__sympy_refine),
    ('sp-acj4-806-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-001834', sp_acj4_806_ground__sympy_simplify),
    ('sp-acj4-806-ground', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-002324', sp_acj4_806_ground__sympy_extras_ask),
    ('sp-acj4-806-ground', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-002919', sp_acj4_806_ground__sympy_extras_refine),
    ('sp-acj4-806-ground', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-003616', sp_acj4_806_ground__sympy_extras_simplify),
    ('sp-acj4-813-ground', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-002222', sp_acj4_813_ground__satassume_ask),
    ('sp-acj4-813-ground', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-001852', sp_acj4_813_ground__satrefine_refine),
    ('sp-acj4-813-ground', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-002313', sp_acj4_813_ground__satsimp_trigsimp),
    ('sp-acj4-813-ground', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-002233', sp_acj4_813_ground__satrefine_simplify),
    ('sp-acj4-813-ground', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-001315', sp_acj4_813_ground__sympy_auto),
    ('sp-acj4-813-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-001321', sp_acj4_813_ground__sympy_ask),
    ('sp-acj4-813-ground', 'sympy-satask', 'true', 'true', 'sympy-satask-20261020-072057', sp_acj4_813_ground__sympy_satask),
    ('sp-acj4-813-ground', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-001510', sp_acj4_813_ground__sympy_refine),
    ('sp-acj4-813-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-001834', sp_acj4_813_ground__sympy_simplify),
    ('sp-acj4-813-ground', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-002324', sp_acj4_813_ground__sympy_extras_ask),
    ('sp-acj4-813-ground', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-002919', sp_acj4_813_ground__sympy_extras_refine),
    ('sp-acj4-813-ground', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-003616', sp_acj4_813_ground__sympy_extras_simplify),
    ('sp-acj4-816-ground', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-002222', sp_acj4_816_ground__satassume_ask),
    ('sp-acj4-816-ground', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-001852', sp_acj4_816_ground__satrefine_refine),
    ('sp-acj4-816-ground', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-002313', sp_acj4_816_ground__satsimp_trigsimp),
    ('sp-acj4-816-ground', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-002233', sp_acj4_816_ground__satrefine_simplify),
    ('sp-acj4-816-ground', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-001315', sp_acj4_816_ground__sympy_auto),
    ('sp-acj4-816-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-001321', sp_acj4_816_ground__sympy_ask),
    ('sp-acj4-816-ground', 'sympy-satask', 'true', 'true', 'sympy-satask-20261020-072057', sp_acj4_816_ground__sympy_satask),
    ('sp-acj4-816-ground', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-001510', sp_acj4_816_ground__sympy_refine),
    ('sp-acj4-816-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-001834', sp_acj4_816_ground__sympy_simplify),
    ('sp-acj4-816-ground', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-002324', sp_acj4_816_ground__sympy_extras_ask),
    ('sp-acj4-816-ground', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-002919', sp_acj4_816_ground__sympy_extras_refine),
    ('sp-acj4-816-ground', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-003616', sp_acj4_816_ground__sympy_extras_simplify),
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
