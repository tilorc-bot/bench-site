# assume-eval: a runnable script from the results browser
# Run: python3 this-file.py (or paste it into python or Jupyter).
# suite simplipy · category simplipy-complex-branch · all Python systems (80 cases listed)
# 960 case run(s), a function each (listed in CASES).  Each runs in a fresh copy of
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
# dropped (not a unary fact about one symbol): ~Q.zero(Abs(x))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(sin(x))
# dropped (not a unary fact about one symbol): ~Q.zero(tanh(x))
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(asinh(x)))
# dropped (not a unary fact about one symbol): Ne(1 / x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(1 / x, -I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -I, evaluate=False)
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
# dropped (not a unary fact about one symbol): ~Q.zero(-10 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(-4 / x)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, x))
# dropped (not a unary fact about one symbol): Or(~Q.zero(1 / x), re(x) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(log(1 / x)))
# dropped (not a unary fact about one symbol): Or(~Q.zero(exp(x)), re(exp(1)) > 0)
# dropped (not a unary fact about one symbol): Or(~Q.zero(exp(x)), re(pi) > 0)
# dropped (not a unary fact about one symbol): Or(~Q.zero(exp(x)), re(x) > 0)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(-x) > 0)
# dropped (not a unary fact about one symbol): Q.real(acos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(acos(x))
# dropped (not a unary fact about one symbol): Q.real(acosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(acosh(x))
# dropped (not a unary fact about one symbol): Q.real(cosh(x))
# dropped (not a unary fact about one symbol): Q.real(exp(x))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(sin(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(sin(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(tanh(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(-log(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(Abs(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(acosh(Abs(x))))
# dropped (not a unary fact about one symbol): Ne(-log(x), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(-log(x), -I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(log(1 / x), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(log(1 / x), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(log(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / log(x))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(atan(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(6, x))
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(7, x))
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(exp(1)) > 0)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, exp(1)))
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, pi))
# dropped (not a unary fact about one symbol): Ne(tanh(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(tanh(x), -1, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(exp(x))


# ---- case sp-acj4-0-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_0_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_0_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_0_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_0_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_0_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = acosh(cosh(x)) - Abs(x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_0_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_0_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_0_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_0_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = acosh(cosh(x)) - Abs(x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_0_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_0_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_0_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-complex · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered true (solved)
@_in(_SETUP1)
def sp_acj4_102_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-complex · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered true (solved)
@_in(_SETUP2)
def sp_acj4_102_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-complex · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered true (solved)
@_in(_SETUP2)
def sp_acj4_102_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-complex · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered true (solved)
@_in(_SETUP2)
def sp_acj4_102_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-complex · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered true (solved)
@_in(_SETUP3)
def sp_acj4_102_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = Abs(x) / 6 - Abs(x / -6)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered true (solved)
@_in(_SETUP3)
def sp_acj4_102_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-complex · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered true (solved)
@_in(_SETUP4)
def sp_acj4_102_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered true (solved)
@_in(_SETUP3)
def sp_acj4_102_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered true (solved)
@_in(_SETUP3)
def sp_acj4_102_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = Abs(x) / 6 - Abs(x / -6)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-complex · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered true (solved)
@_in(_SETUP5)
def sp_acj4_102_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-complex · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered true (solved)
@_in(_SETUP5)
def sp_acj4_102_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-complex · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered true (solved)
@_in(_SETUP5)
def sp_acj4_102_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_108_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_108_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_108_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_108_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_108_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = Abs(x) / x - (x / Abs(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_108_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_108_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_108_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_108_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = Abs(x) / x - (x / Abs(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_108_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_108_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_108_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-complex · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered true (solved)
@_in(_SETUP1)
def sp_acj4_120_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-complex · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered true (solved)
@_in(_SETUP2)
def sp_acj4_120_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-complex · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered true (solved)
@_in(_SETUP2)
def sp_acj4_120_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-complex · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered true (solved)
@_in(_SETUP2)
def sp_acj4_120_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-complex · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered true (solved)
@_in(_SETUP3)
def sp_acj4_120_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = pi / Abs(x) - Abs(pi / x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered true (solved)
@_in(_SETUP3)
def sp_acj4_120_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-complex · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered true (solved)
@_in(_SETUP4)
def sp_acj4_120_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered true (solved)
@_in(_SETUP3)
def sp_acj4_120_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered true (solved)
@_in(_SETUP3)
def sp_acj4_120_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = pi / Abs(x) - Abs(pi / x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-complex · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered true (solved)
@_in(_SETUP5)
def sp_acj4_120_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-complex · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered true (solved)
@_in(_SETUP5)
def sp_acj4_120_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-complex · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered true (solved)
@_in(_SETUP5)
def sp_acj4_120_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_130_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_130_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_130_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_130_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_130_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_130_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_130_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_130_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_130_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_130_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_130_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_130_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_131_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_131_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_131_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_131_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_131_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_131_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_131_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_131_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_131_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_131_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_131_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_131_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_132_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_132_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_132_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_132_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_132_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_132_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_132_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_132_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_132_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_132_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_132_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_132_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_133_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_133_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_133_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_133_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_133_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_133_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_133_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_133_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_133_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_133_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_133_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_133_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_137_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_137_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_137_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_137_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_137_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_137_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_137_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_137_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_137_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_137_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_137_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_137_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-147-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_147_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(asinh(x))), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-147-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_147_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(asinh(x))), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-147-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_147_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(asinh(x))), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-147-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_147_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(asinh(x))), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-147-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_147_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-147-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_147_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(asinh(x))), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-147-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_147_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(asinh(x))), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-147-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_147_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(asinh(x))), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-147-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_147_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-147-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_147_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(asinh(x))), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-147-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_147_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(asinh(x))), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-147-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_147_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(asinh(x))), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_151_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_151_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_151_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_151_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_151_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_151_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_151_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_151_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_151_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_151_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_151_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_151_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-153-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_153_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(cos(x))) - Abs(cos(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-153-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_153_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(cos(x))) - Abs(cos(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-153-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_153_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(cos(x))) - Abs(cos(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-153-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_153_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(cos(x))) - Abs(cos(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-153-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_153_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = acos(cos(cos(x))) - Abs(cos(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-153-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_153_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(cos(x))) - Abs(cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-153-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_153_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(cos(x))) - Abs(cos(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-153-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_153_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(cos(x))) - Abs(cos(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-153-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_153_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = acos(cos(cos(x))) - Abs(cos(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-153-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_153_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(cos(x))) - Abs(cos(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-153-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_153_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(cos(x))) - Abs(cos(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-153-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_153_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(cos(x))) - Abs(cos(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_154_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_154_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_154_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_154_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_154_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_154_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_154_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_154_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_154_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_154_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_154_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_154_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-165-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_165_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = asin(cos(atan(x))) - Abs(atan(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-165-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_165_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = asin(cos(atan(x))) - Abs(atan(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-165-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_165_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = asin(cos(atan(x))) - Abs(atan(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-165-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_165_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = asin(cos(atan(x))) - Abs(atan(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-165-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_165_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = asin(cos(atan(x))) - Abs(atan(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-165-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_165_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = asin(cos(atan(x))) - Abs(atan(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-165-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_165_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = asin(cos(atan(x))) - Abs(atan(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-165-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_165_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = asin(cos(atan(x))) - Abs(atan(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-165-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_165_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = asin(cos(atan(x))) - Abs(atan(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-165-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_165_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = asin(cos(atan(x))) - Abs(atan(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-165-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_165_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = asin(cos(atan(x))) - Abs(atan(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-165-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_165_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = asin(cos(atan(x))) - Abs(atan(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-173-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_173_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = asin(tanh(Abs(x))) - acos(1 / cosh(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-173-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_173_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = asin(tanh(Abs(x))) - acos(1 / cosh(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-173-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_173_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = asin(tanh(Abs(x))) - acos(1 / cosh(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-173-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_173_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = asin(tanh(Abs(x))) - acos(1 / cosh(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-173-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_173_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = asin(tanh(Abs(x))) - acos(1 / cosh(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-173-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_173_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = asin(tanh(Abs(x))) - acos(1 / cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-173-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_173_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = asin(tanh(Abs(x))) - acos(1 / cosh(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-173-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_173_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = asin(tanh(Abs(x))) - acos(1 / cosh(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-173-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_173_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = asin(tanh(Abs(x))) - acos(1 / cosh(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-173-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_173_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = asin(tanh(Abs(x))) - acos(1 / cosh(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-173-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_173_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = asin(tanh(Abs(x))) - acos(1 / cosh(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-173-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_173_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = asin(tanh(Abs(x))) - acos(1 / cosh(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-176-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_176_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = atan(Abs(sinh(x))) - acos(1 / cosh(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-176-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_176_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = atan(Abs(sinh(x))) - acos(1 / cosh(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-176-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_176_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = atan(Abs(sinh(x))) - acos(1 / cosh(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-176-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_176_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = atan(Abs(sinh(x))) - acos(1 / cosh(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-176-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_176_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = atan(Abs(sinh(x))) - acos(1 / cosh(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-176-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_176_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = atan(Abs(sinh(x))) - acos(1 / cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-176-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_176_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = atan(Abs(sinh(x))) - acos(1 / cosh(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-176-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_176_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = atan(Abs(sinh(x))) - acos(1 / cosh(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-176-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_176_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = atan(Abs(sinh(x))) - acos(1 / cosh(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-176-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_176_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = atan(Abs(sinh(x))) - acos(1 / cosh(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-176-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_176_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = atan(Abs(sinh(x))) - acos(1 / cosh(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-176-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_176_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = atan(Abs(sinh(x))) - acos(1 / cosh(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-177-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_177_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)))
    Residual = atan(Abs(tan(x))) - Abs(asin(sin(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-177-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_177_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)))
    Residual = atan(Abs(tan(x))) - Abs(asin(sin(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-177-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_177_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)))
    Residual = atan(Abs(tan(x))) - Abs(asin(sin(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-177-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_177_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)))
    Residual = atan(Abs(tan(x))) - Abs(asin(sin(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-177-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_177_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = atan(Abs(tan(x))) - Abs(asin(sin(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-177-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_177_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)))
    Residual = atan(Abs(tan(x))) - Abs(asin(sin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-177-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_177_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)))
    Residual = atan(Abs(tan(x))) - Abs(asin(sin(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-177-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_177_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)))
    Residual = atan(Abs(tan(x))) - Abs(asin(sin(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-177-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_177_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = atan(Abs(tan(x))) - Abs(asin(sin(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-177-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_177_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)))
    Residual = atan(Abs(tan(x))) - Abs(asin(sin(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-177-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_177_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)))
    Residual = atan(Abs(tan(x))) - Abs(asin(sin(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-177-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_177_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)))
    Residual = atan(Abs(tan(x))) - Abs(asin(sin(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_180_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_180_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_180_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_180_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_180_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_180_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_180_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_180_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_180_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_180_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_180_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_180_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_183_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_183_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_183_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_183_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_183_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_183_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_183_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_183_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_183_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_183_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_183_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_183_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_189_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_189_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_189_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_189_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_189_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_189_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_189_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_189_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_189_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_189_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_189_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_189_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_190_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_190_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_190_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_190_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_190_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_190_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_190_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_190_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_190_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_190_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_190_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_190_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_191_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_191_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_191_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_191_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_191_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_191_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_191_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_191_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_191_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_191_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_191_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_191_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-20-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_20_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = sinh(Abs(x)) - Abs(sinh(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-20-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_20_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = sinh(Abs(x)) - Abs(sinh(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-20-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_20_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = sinh(Abs(x)) - Abs(sinh(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-20-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_20_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = sinh(Abs(x)) - Abs(sinh(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-20-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_20_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = sinh(Abs(x)) - Abs(sinh(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-20-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_20_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = sinh(Abs(x)) - Abs(sinh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-20-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_20_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = sinh(Abs(x)) - Abs(sinh(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-20-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_20_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = sinh(Abs(x)) - Abs(sinh(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-20-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_20_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = sinh(Abs(x)) - Abs(sinh(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-20-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_20_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = sinh(Abs(x)) - Abs(sinh(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-20-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_20_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = sinh(Abs(x)) - Abs(sinh(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-20-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_20_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = sinh(Abs(x)) - Abs(sinh(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_203_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_203_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_203_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_203_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_203_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = cos(log(1 / x)) - cos(log(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_203_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_203_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_203_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_203_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = cos(log(1 / x)) - cos(log(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_203_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_203_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_203_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-213-complex · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered true (solved)
@_in(_SETUP1)
def sp_acj4_213_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-10 / x))
    Residual = 1 / (-10 / x) - (x / -10)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-213-complex · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered true (solved)
@_in(_SETUP2)
def sp_acj4_213_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-10 / x))
    Residual = 1 / (-10 / x) - (x / -10)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-213-complex · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered true (solved)
@_in(_SETUP2)
def sp_acj4_213_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-10 / x))
    Residual = 1 / (-10 / x) - (x / -10)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-213-complex · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered true (solved)
@_in(_SETUP2)
def sp_acj4_213_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-10 / x))
    Residual = 1 / (-10 / x) - (x / -10)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-213-complex · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered true (solved)
@_in(_SETUP3)
def sp_acj4_213_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = 1 / (-10 / x) - (x / -10)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-213-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered true (solved)
@_in(_SETUP3)
def sp_acj4_213_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-10 / x))
    Residual = 1 / (-10 / x) - (x / -10)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-213-complex · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered true (solved)
@_in(_SETUP4)
def sp_acj4_213_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-10 / x))
    Residual = 1 / (-10 / x) - (x / -10)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-213-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered true (solved)
@_in(_SETUP3)
def sp_acj4_213_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-10 / x))
    Residual = 1 / (-10 / x) - (x / -10)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-213-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered true (solved)
@_in(_SETUP3)
def sp_acj4_213_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = 1 / (-10 / x) - (x / -10)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-213-complex · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered true (solved)
@_in(_SETUP5)
def sp_acj4_213_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-10 / x))
    Residual = 1 / (-10 / x) - (x / -10)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-213-complex · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered true (solved)
@_in(_SETUP5)
def sp_acj4_213_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-10 / x))
    Residual = 1 / (-10 / x) - (x / -10)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-213-complex · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered true (solved)
@_in(_SETUP5)
def sp_acj4_213_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-10 / x))
    Residual = 1 / (-10 / x) - (x / -10)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-216-complex · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered true (solved)
@_in(_SETUP1)
def sp_acj4_216_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-4 / x))
    Residual = 1 / (-4 / x) - (x / -4)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-216-complex · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered true (solved)
@_in(_SETUP2)
def sp_acj4_216_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-4 / x))
    Residual = 1 / (-4 / x) - (x / -4)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-216-complex · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered true (solved)
@_in(_SETUP2)
def sp_acj4_216_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-4 / x))
    Residual = 1 / (-4 / x) - (x / -4)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-216-complex · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered true (solved)
@_in(_SETUP2)
def sp_acj4_216_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-4 / x))
    Residual = 1 / (-4 / x) - (x / -4)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-216-complex · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered true (solved)
@_in(_SETUP3)
def sp_acj4_216_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = 1 / (-4 / x) - (x / -4)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-216-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered true (solved)
@_in(_SETUP3)
def sp_acj4_216_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-4 / x))
    Residual = 1 / (-4 / x) - (x / -4)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-216-complex · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered true (solved)
@_in(_SETUP4)
def sp_acj4_216_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-4 / x))
    Residual = 1 / (-4 / x) - (x / -4)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-216-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered true (solved)
@_in(_SETUP3)
def sp_acj4_216_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-4 / x))
    Residual = 1 / (-4 / x) - (x / -4)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-216-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered true (solved)
@_in(_SETUP3)
def sp_acj4_216_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = 1 / (-4 / x) - (x / -4)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-216-complex · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered true (solved)
@_in(_SETUP5)
def sp_acj4_216_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-4 / x))
    Residual = 1 / (-4 / x) - (x / -4)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-216-complex · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered true (solved)
@_in(_SETUP5)
def sp_acj4_216_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-4 / x))
    Residual = 1 / (-4 / x) - (x / -4)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-216-complex · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered true (solved)
@_in(_SETUP5)
def sp_acj4_216_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-4 / x))
    Residual = 1 / (-4 / x) - (x / -4)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_22_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_22_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_22_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_22_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_22_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_22_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_22_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_22_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_22_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_22_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_22_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_22_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_234_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_234_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_234_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_234_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_234_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_234_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_234_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_234_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_234_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_234_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_234_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_234_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_252_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_252_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_252_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_252_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_252_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_252_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_252_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_252_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_252_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_252_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_252_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_252_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_253_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_253_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_253_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_253_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_253_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_253_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_253_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_253_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_253_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_253_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_253_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_253_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_260_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_260_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_260_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_260_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_260_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = -log(cos(x)) - log(1 / cos(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_260_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_260_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_260_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_260_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = -log(cos(x)) - log(1 / cos(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_260_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_260_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_260_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_261_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_261_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_261_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_261_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_261_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_261_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_261_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_261_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_261_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_261_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_261_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_261_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_266_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_266_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_266_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_266_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_266_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = -sin(log(x)) - sin(log(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_266_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_266_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_266_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_266_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = -sin(log(x)) - sin(log(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_266_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_266_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_266_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_267_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_267_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_267_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_267_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_267_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = -tan(log(x)) - tan(log(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_267_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_267_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_267_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_267_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = -tan(log(x)) - tan(log(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_267_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_267_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_267_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-274-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_274_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -2) - Pow(x, -2)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-274-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_274_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -2) - Pow(x, -2)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-274-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_274_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -2) - Pow(x, -2)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-274-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_274_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -2) - Pow(x, -2)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-274-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_274_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = Pow(Abs(x), -2) - Pow(x, -2)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-274-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_274_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -2) - Pow(x, -2)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-274-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_274_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -2) - Pow(x, -2)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-274-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_274_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -2) - Pow(x, -2)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-274-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_274_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = Pow(Abs(x), -2) - Pow(x, -2)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-274-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_274_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -2) - Pow(x, -2)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-274-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_274_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -2) - Pow(x, -2)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-274-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_274_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -2) - Pow(x, -2)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-278-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_278_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -6) - Pow(x, -6)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-278-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_278_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -6) - Pow(x, -6)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-278-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_278_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -6) - Pow(x, -6)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-278-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_278_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -6) - Pow(x, -6)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-278-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_278_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = Pow(Abs(x), -6) - Pow(x, -6)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-278-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_278_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -6) - Pow(x, -6)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-278-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_278_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -6) - Pow(x, -6)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-278-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_278_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -6) - Pow(x, -6)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-278-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_278_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = Pow(Abs(x), -6) - Pow(x, -6)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-278-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_278_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -6) - Pow(x, -6)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-278-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_278_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -6) - Pow(x, -6)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-278-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_278_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -6) - Pow(x, -6)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_283_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_283_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_283_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_283_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_283_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = Pow(Abs(x), 2) - (x * x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_283_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_283_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_283_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_283_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = Pow(Abs(x), 2) - (x * x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_283_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_283_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_283_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-284-complex · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_284_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 3) - Abs(Pow(x, 3))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-284-complex · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered true (solved)
@_in(_SETUP2)
def sp_acj4_284_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 3) - Abs(Pow(x, 3))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-284-complex · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_284_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 3) - Abs(Pow(x, 3))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-284-complex · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered true (solved)
@_in(_SETUP2)
def sp_acj4_284_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 3) - Abs(Pow(x, 3))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-284-complex · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_284_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = Pow(Abs(x), 3) - Abs(Pow(x, 3))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-284-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_284_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 3) - Abs(Pow(x, 3))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-284-complex · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_284_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 3) - Abs(Pow(x, 3))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-284-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_284_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 3) - Abs(Pow(x, 3))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-284-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_284_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = Pow(Abs(x), 3) - Abs(Pow(x, 3))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-284-complex · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_284_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 3) - Abs(Pow(x, 3))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-284-complex · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_284_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 3) - Abs(Pow(x, 3))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-284-complex · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_284_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 3) - Abs(Pow(x, 3))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-288-complex · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_288_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 7) - Abs(Pow(x, 7))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-288-complex · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered true (solved)
@_in(_SETUP2)
def sp_acj4_288_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 7) - Abs(Pow(x, 7))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-288-complex · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_288_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 7) - Abs(Pow(x, 7))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-288-complex · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered true (solved)
@_in(_SETUP2)
def sp_acj4_288_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 7) - Abs(Pow(x, 7))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-288-complex · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_288_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = Pow(Abs(x), 7) - Abs(Pow(x, 7))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-288-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_288_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 7) - Abs(Pow(x, 7))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-288-complex · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_288_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 7) - Abs(Pow(x, 7))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-288-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_288_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 7) - Abs(Pow(x, 7))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-288-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_288_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = Pow(Abs(x), 7) - Abs(Pow(x, 7))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-288-complex · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_288_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 7) - Abs(Pow(x, 7))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-288-complex · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_288_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 7) - Abs(Pow(x, 7))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-288-complex · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_288_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 7) - Abs(Pow(x, 7))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-30-complex · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered true (solved)
@_in(_SETUP1)
def sp_acj4_30_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = 4 * Abs(x) - Abs(-4 * x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-30-complex · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered true (solved)
@_in(_SETUP2)
def sp_acj4_30_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = 4 * Abs(x) - Abs(-4 * x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-30-complex · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered true (solved)
@_in(_SETUP2)
def sp_acj4_30_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = 4 * Abs(x) - Abs(-4 * x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-30-complex · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered true (solved)
@_in(_SETUP2)
def sp_acj4_30_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = 4 * Abs(x) - Abs(-4 * x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-30-complex · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered true (solved)
@_in(_SETUP3)
def sp_acj4_30_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = 4 * Abs(x) - Abs(-4 * x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-30-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered true (solved)
@_in(_SETUP3)
def sp_acj4_30_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = 4 * Abs(x) - Abs(-4 * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-30-complex · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered true (solved)
@_in(_SETUP4)
def sp_acj4_30_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = 4 * Abs(x) - Abs(-4 * x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-30-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered true (solved)
@_in(_SETUP3)
def sp_acj4_30_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = 4 * Abs(x) - Abs(-4 * x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-30-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered true (solved)
@_in(_SETUP3)
def sp_acj4_30_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = 4 * Abs(x) - Abs(-4 * x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-30-complex · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered true (solved)
@_in(_SETUP5)
def sp_acj4_30_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = 4 * Abs(x) - Abs(-4 * x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-30-complex · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered true (solved)
@_in(_SETUP5)
def sp_acj4_30_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = 4 * Abs(x) - Abs(-4 * x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-30-complex · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered true (solved)
@_in(_SETUP5)
def sp_acj4_30_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = 4 * Abs(x) - Abs(-4 * x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-334-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_334_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(exp(1)) > 0))
    Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-334-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_334_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(exp(1)) > 0))
    Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-334-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_334_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(exp(1)) > 0))
    Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-334-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_334_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(exp(1)) > 0))
    Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-334-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_334_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-334-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_334_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(exp(1)) > 0))
    Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-334-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_334_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(exp(1)) > 0))
    Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-334-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_334_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(exp(1)) > 0))
    Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-334-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_334_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-334-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_334_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(exp(1)) > 0))
    Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-334-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_334_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(exp(1)) > 0))
    Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-334-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_334_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(exp(1)) > 0))
    Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-335-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_335_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(pi) > 0))
    Residual = Pow(exp(x), pi) - exp(pi * x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-335-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_335_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(pi) > 0))
    Residual = Pow(exp(x), pi) - exp(pi * x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-335-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_335_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(pi) > 0))
    Residual = Pow(exp(x), pi) - exp(pi * x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-335-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_335_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(pi) > 0))
    Residual = Pow(exp(x), pi) - exp(pi * x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-335-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_335_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = Pow(exp(x), pi) - exp(pi * x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-335-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_335_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(pi) > 0))
    Residual = Pow(exp(x), pi) - exp(pi * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-335-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_335_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(pi) > 0))
    Residual = Pow(exp(x), pi) - exp(pi * x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-335-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_335_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(pi) > 0))
    Residual = Pow(exp(x), pi) - exp(pi * x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-335-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_335_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = Pow(exp(x), pi) - exp(pi * x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-335-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_335_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(pi) > 0))
    Residual = Pow(exp(x), pi) - exp(pi * x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-335-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_335_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(pi) > 0))
    Residual = Pow(exp(x), pi) - exp(pi * x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-335-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_335_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(pi) > 0))
    Residual = Pow(exp(x), pi) - exp(pi * x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-336-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_336_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(x) > 0))
    Residual = Pow(exp(x), x) - exp(x * x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-336-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_336_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(x) > 0))
    Residual = Pow(exp(x), x) - exp(x * x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-336-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_336_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(x) > 0))
    Residual = Pow(exp(x), x) - exp(x * x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-336-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_336_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(x) > 0))
    Residual = Pow(exp(x), x) - exp(x * x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-336-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_336_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = Pow(exp(x), x) - exp(x * x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-336-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_336_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(x) > 0))
    Residual = Pow(exp(x), x) - exp(x * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-336-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_336_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(x) > 0))
    Residual = Pow(exp(x), x) - exp(x * x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-336-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_336_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(x) > 0))
    Residual = Pow(exp(x), x) - exp(x * x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-336-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_336_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = Pow(exp(x), x) - exp(x * x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-336-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_336_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(x) > 0))
    Residual = Pow(exp(x), x) - exp(x * x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-336-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_336_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(x) > 0))
    Residual = Pow(exp(x), x) - exp(x * x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-336-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_336_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(x) > 0))
    Residual = Pow(exp(x), x) - exp(x * x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-complex · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered true (solved)
@_in(_SETUP1)
def sp_acj4_343_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-complex · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered true (solved)
@_in(_SETUP2)
def sp_acj4_343_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-complex · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered true (solved)
@_in(_SETUP2)
def sp_acj4_343_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-complex · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered true (solved)
@_in(_SETUP2)
def sp_acj4_343_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-complex · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered true (solved)
@_in(_SETUP3)
def sp_acj4_343_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered true (solved)
@_in(_SETUP3)
def sp_acj4_343_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-complex · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered true (solved)
@_in(_SETUP4)
def sp_acj4_343_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered true (solved)
@_in(_SETUP3)
def sp_acj4_343_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered true (solved)
@_in(_SETUP3)
def sp_acj4_343_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-complex · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered true (solved)
@_in(_SETUP5)
def sp_acj4_343_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-complex · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered true (solved)
@_in(_SETUP5)
def sp_acj4_343_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-complex · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered true (solved)
@_in(_SETUP5)
def sp_acj4_343_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_344_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_344_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_344_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_344_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_344_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_344_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_344_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_344_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_344_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_344_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_344_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_344_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-complex · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_368_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-complex · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered true (solved)
@_in(_SETUP2)
def sp_acj4_368_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-complex · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_368_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-complex · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered true (solved)
@_in(_SETUP2)
def sp_acj4_368_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-complex · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_368_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_368_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-complex · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_368_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_368_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_368_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-complex · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_368_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-complex · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_368_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-complex · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_368_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-complex · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_369_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-complex · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_369_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-complex · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_369_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-complex · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_369_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-complex · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_369_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_369_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-complex · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_369_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_369_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_369_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-complex · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_369_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-complex · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_369_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-complex · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_369_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-complex · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_370_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-complex · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_370_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-complex · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_370_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-complex · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_370_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-complex · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_370_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_370_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-complex · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_370_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_370_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_370_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-complex · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_370_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-complex · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_370_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-complex · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_370_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-complex · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_371_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-complex · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_371_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-complex · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_371_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-complex · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_371_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-complex · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_371_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_371_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-complex · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_371_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_371_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_371_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-complex · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_371_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-complex · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_371_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-complex · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_371_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_372_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(cosh(x)), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_372_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(cosh(x)), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_372_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(cosh(x)), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_372_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(cosh(x)), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_372_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_372_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(cosh(x)), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_372_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(cosh(x)), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_372_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(cosh(x)), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_372_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_372_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(cosh(x)), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_372_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(cosh(x)), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_372_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(cosh(x)), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_373_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(cosh(x)))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_373_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(cosh(x)))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_373_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(cosh(x)))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_373_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(cosh(x)))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_373_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_373_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(cosh(x)))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_373_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(cosh(x)))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_373_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(cosh(x)))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_373_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_373_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(cosh(x)))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_373_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(cosh(x)))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_373_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(cosh(x)))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-387-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_387_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 5) - exp(x / 5)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-387-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_387_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 5) - exp(x / 5)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-387-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_387_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 5) - exp(x / 5)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-387-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_387_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 5) - exp(x / 5)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-387-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_387_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = real_root(exp(x), 5) - exp(x / 5)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-387-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_387_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 5) - exp(x / 5)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-387-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_387_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 5) - exp(x / 5)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-387-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_387_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 5) - exp(x / 5)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-387-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_387_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = real_root(exp(x), 5) - exp(x / 5)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-387-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_387_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 5) - exp(x / 5)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-387-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_387_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 5) - exp(x / 5)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-387-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_387_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 5) - exp(x / 5)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-389-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_389_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 7) - exp(x / 7)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-389-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_389_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 7) - exp(x / 7)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-389-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_389_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 7) - exp(x / 7)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-389-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_389_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 7) - exp(x / 7)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-389-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_389_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = real_root(exp(x), 7) - exp(x / 7)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-389-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_389_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 7) - exp(x / 7)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-389-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_389_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 7) - exp(x / 7)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-389-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_389_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 7) - exp(x / 7)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-389-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_389_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = real_root(exp(x), 7) - exp(x / 7)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-389-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_389_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 7) - exp(x / 7)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-389-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_389_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 7) - exp(x / 7)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-389-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_389_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 7) - exp(x / 7)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_396_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_396_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_396_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_396_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_396_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_396_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_396_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_396_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_396_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_396_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_396_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_396_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-40-complex · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered true (solved)
@_in(_SETUP1)
def sp_acj4_40_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) * pi - Abs(pi * x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-40-complex · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered true (solved)
@_in(_SETUP2)
def sp_acj4_40_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) * pi - Abs(pi * x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-40-complex · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered true (solved)
@_in(_SETUP2)
def sp_acj4_40_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) * pi - Abs(pi * x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-40-complex · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered true (solved)
@_in(_SETUP2)
def sp_acj4_40_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) * pi - Abs(pi * x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-40-complex · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered true (solved)
@_in(_SETUP3)
def sp_acj4_40_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = Abs(x) * pi - Abs(pi * x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-40-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered true (solved)
@_in(_SETUP3)
def sp_acj4_40_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) * pi - Abs(pi * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-40-complex · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered true (solved)
@_in(_SETUP4)
def sp_acj4_40_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) * pi - Abs(pi * x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-40-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered true (solved)
@_in(_SETUP3)
def sp_acj4_40_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) * pi - Abs(pi * x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-40-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered true (solved)
@_in(_SETUP3)
def sp_acj4_40_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = Abs(x) * pi - Abs(pi * x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-40-complex · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered true (solved)
@_in(_SETUP5)
def sp_acj4_40_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) * pi - Abs(pi * x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-40-complex · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered true (solved)
@_in(_SETUP5)
def sp_acj4_40_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) * pi - Abs(pi * x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-40-complex · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered true (solved)
@_in(_SETUP5)
def sp_acj4_40_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) * pi - Abs(pi * x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_403_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_403_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_403_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_403_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_403_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = sin(-log(x)) - sin(log(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_403_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_403_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_403_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_403_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = sin(-log(x)) - sin(log(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_403_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_403_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_403_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_404_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_404_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_404_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_404_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_404_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_404_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_404_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_404_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_404_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_404_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_404_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_404_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_414_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_414_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_414_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_414_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_414_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_414_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_414_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_414_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_414_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_414_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_414_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_414_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_415_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_415_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_415_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_415_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_415_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_415_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_415_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_415_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_415_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_415_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_415_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_415_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_420_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_420_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_420_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_420_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_420_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = tan(-log(x)) - tan(log(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_420_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_420_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_420_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_420_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = tan(-log(x)) - tan(log(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_420_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_420_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_420_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_421_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cosh(x)), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_421_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cosh(x)), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_421_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cosh(x)), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_421_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cosh(x)), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_421_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_421_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cosh(x)), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_421_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cosh(x)), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_421_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cosh(x)), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_421_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_421_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cosh(x)), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_421_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cosh(x)), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_421_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cosh(x)), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-422-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_422_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-422-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_422_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-422-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_422_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-422-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_422_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-422-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_422_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-422-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_422_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-422-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_422_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-422-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_422_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-422-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_422_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-422-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_422_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-422-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_422_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-422-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_422_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-423-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_423_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(acosh(Abs(x)))), ~Q.zero(x))
    Residual = tanh(acosh(Abs(x))) - cos(asin(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-423-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_423_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(acosh(Abs(x)))), ~Q.zero(x))
    Residual = tanh(acosh(Abs(x))) - cos(asin(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-423-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_423_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(acosh(Abs(x)))), ~Q.zero(x))
    Residual = tanh(acosh(Abs(x))) - cos(asin(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-423-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_423_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(acosh(Abs(x)))), ~Q.zero(x))
    Residual = tanh(acosh(Abs(x))) - cos(asin(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-423-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_423_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = tanh(acosh(Abs(x))) - cos(asin(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-423-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_423_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(acosh(Abs(x)))), ~Q.zero(x))
    Residual = tanh(acosh(Abs(x))) - cos(asin(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-423-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_423_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(acosh(Abs(x)))), ~Q.zero(x))
    Residual = tanh(acosh(Abs(x))) - cos(asin(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-423-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_423_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(acosh(Abs(x)))), ~Q.zero(x))
    Residual = tanh(acosh(Abs(x))) - cos(asin(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-423-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_423_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = tanh(acosh(Abs(x))) - cos(asin(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-423-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_423_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(acosh(Abs(x)))), ~Q.zero(x))
    Residual = tanh(acosh(Abs(x))) - cos(asin(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-423-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_423_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(acosh(Abs(x)))), ~Q.zero(x))
    Residual = tanh(acosh(Abs(x))) - cos(asin(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-423-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_423_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(acosh(Abs(x)))), ~Q.zero(x))
    Residual = tanh(acosh(Abs(x))) - cos(asin(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-424-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_424_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-424-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_424_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-424-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_424_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-424-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_424_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-424-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_424_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-424-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_424_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-424-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_424_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-424-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_424_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-424-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_424_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-424-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_424_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-424-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_424_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-424-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_424_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_430_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_430_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_430_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_430_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_430_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = log(x) * x - log(Pow(x, x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_430_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_430_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_430_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_430_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = log(x) * x - log(Pow(x, x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_430_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_430_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_430_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_433_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_433_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_433_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_433_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_433_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = atan(-log(x)) - atan(log(1 / x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_433_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_433_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_433_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_433_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = atan(-log(x)) - atan(log(1 / x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_433_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_433_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_433_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_442_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_442_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_442_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_442_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_442_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = -log(log(x)) - log(1 / log(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_442_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_442_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_442_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_442_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = -log(log(x)) - log(1 / log(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_442_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_442_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_442_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-446-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_446_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(cos(Abs(atan(x)))))
    Residual = tan(Abs(atan(x))) - Abs(x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-446-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_446_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(cos(Abs(atan(x)))))
    Residual = tan(Abs(atan(x))) - Abs(x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-446-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_446_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(cos(Abs(atan(x)))))
    Residual = tan(Abs(atan(x))) - Abs(x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-446-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_446_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(cos(Abs(atan(x)))))
    Residual = tan(Abs(atan(x))) - Abs(x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-446-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_446_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = tan(Abs(atan(x))) - Abs(x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-446-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_446_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(cos(Abs(atan(x)))))
    Residual = tan(Abs(atan(x))) - Abs(x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-446-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_446_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(cos(Abs(atan(x)))))
    Residual = tan(Abs(atan(x))) - Abs(x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-446-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_446_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(cos(Abs(atan(x)))))
    Residual = tan(Abs(atan(x))) - Abs(x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-446-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_446_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = tan(Abs(atan(x))) - Abs(x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-446-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_446_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(cos(Abs(atan(x)))))
    Residual = tan(Abs(atan(x))) - Abs(x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-446-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_446_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(cos(Abs(atan(x)))))
    Residual = tan(Abs(atan(x))) - Abs(x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-446-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_446_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(cos(Abs(atan(x)))))
    Residual = tan(Abs(atan(x))) - Abs(x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-complex · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered true (solved)
@_in(_SETUP1)
def sp_acj4_450_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = x / x - 1
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-complex · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered true (solved)
@_in(_SETUP2)
def sp_acj4_450_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = x / x - 1
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-complex · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered true (solved)
@_in(_SETUP2)
def sp_acj4_450_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = x / x - 1
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-complex · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered true (solved)
@_in(_SETUP2)
def sp_acj4_450_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = x / x - 1
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-complex · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered true (solved)
@_in(_SETUP3)
def sp_acj4_450_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = x / x - 1
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered true (solved)
@_in(_SETUP3)
def sp_acj4_450_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = x / x - 1
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-complex · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered true (solved)
@_in(_SETUP4)
def sp_acj4_450_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = x / x - 1
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered true (solved)
@_in(_SETUP3)
def sp_acj4_450_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = x / x - 1
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered true (solved)
@_in(_SETUP3)
def sp_acj4_450_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = x / x - 1
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-complex · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered true (solved)
@_in(_SETUP5)
def sp_acj4_450_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = x / x - 1
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-complex · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered true (solved)
@_in(_SETUP5)
def sp_acj4_450_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = x / x - 1
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-complex · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered true (solved)
@_in(_SETUP5)
def sp_acj4_450_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = x / x - 1
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-complex · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered true (solved)
@_in(_SETUP1)
def sp_acj4_451_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-complex · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered true (solved)
@_in(_SETUP2)
def sp_acj4_451_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-complex · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered true (solved)
@_in(_SETUP2)
def sp_acj4_451_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-complex · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered true (solved)
@_in(_SETUP2)
def sp_acj4_451_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-complex · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered true (solved)
@_in(_SETUP3)
def sp_acj4_451_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = 0 / x - 0
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered true (solved)
@_in(_SETUP3)
def sp_acj4_451_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-complex · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered true (solved)
@_in(_SETUP4)
def sp_acj4_451_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered true (solved)
@_in(_SETUP3)
def sp_acj4_451_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered true (solved)
@_in(_SETUP3)
def sp_acj4_451_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = 0 / x - 0
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-complex · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered true (solved)
@_in(_SETUP5)
def sp_acj4_451_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-complex · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered true (solved)
@_in(_SETUP5)
def sp_acj4_451_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-complex · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered true (solved)
@_in(_SETUP5)
def sp_acj4_451_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_50_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_50_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_50_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_50_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_50_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = log(6) * x - log(Pow(6, x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_50_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_50_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_50_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_50_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = log(6) * x - log(Pow(6, x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_50_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_50_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_50_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-51-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_51_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Pow(7, x)))
    Residual = log(7) * x - log(Pow(7, x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-51-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_51_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Pow(7, x)))
    Residual = log(7) * x - log(Pow(7, x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-51-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_51_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Pow(7, x)))
    Residual = log(7) * x - log(Pow(7, x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-51-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_51_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Pow(7, x)))
    Residual = log(7) * x - log(Pow(7, x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-51-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_51_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = log(7) * x - log(Pow(7, x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-51-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_51_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Pow(7, x)))
    Residual = log(7) * x - log(Pow(7, x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-51-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_51_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Pow(7, x)))
    Residual = log(7) * x - log(Pow(7, x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-51-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_51_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Pow(7, x)))
    Residual = log(7) * x - log(Pow(7, x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-51-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_51_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = log(7) * x - log(Pow(7, x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-51-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_51_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Pow(7, x)))
    Residual = log(7) * x - log(Pow(7, x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-51-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_51_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Pow(7, x)))
    Residual = log(7) * x - log(Pow(7, x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-51-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_51_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Pow(7, x)))
    Residual = log(7) * x - log(Pow(7, x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_55_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_55_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_55_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_55_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_55_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_55_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_55_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_55_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_55_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_55_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_55_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_55_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_56_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_56_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_56_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_56_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_56_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = log(x) * pi - log(Pow(x, pi))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_56_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_56_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_56_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_56_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = log(x) * pi - log(Pow(x, pi))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_56_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_56_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_56_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_6_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_6_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_6_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_6_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_6_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = atanh(tanh(x)) - x
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_6_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_6_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_6_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_6_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = atanh(tanh(x)) - x
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_6_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_6_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_6_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-7-complex · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered true (solved)
@_in(_SETUP1)
def sp_acj4_7_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 1 / Abs(x) - Abs(1 / x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-7-complex · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered true (solved)
@_in(_SETUP2)
def sp_acj4_7_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 1 / Abs(x) - Abs(1 / x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-7-complex · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered true (solved)
@_in(_SETUP2)
def sp_acj4_7_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 1 / Abs(x) - Abs(1 / x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-7-complex · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered true (solved)
@_in(_SETUP2)
def sp_acj4_7_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 1 / Abs(x) - Abs(1 / x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-7-complex · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered true (solved)
@_in(_SETUP3)
def sp_acj4_7_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = 1 / Abs(x) - Abs(1 / x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-7-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered true (solved)
@_in(_SETUP3)
def sp_acj4_7_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 1 / Abs(x) - Abs(1 / x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-7-complex · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered true (solved)
@_in(_SETUP4)
def sp_acj4_7_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 1 / Abs(x) - Abs(1 / x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-7-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered true (solved)
@_in(_SETUP3)
def sp_acj4_7_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 1 / Abs(x) - Abs(1 / x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-7-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered true (solved)
@_in(_SETUP3)
def sp_acj4_7_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = 1 / Abs(x) - Abs(1 / x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-7-complex · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered true (solved)
@_in(_SETUP5)
def sp_acj4_7_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 1 / Abs(x) - Abs(1 / x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-7-complex · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered true (solved)
@_in(_SETUP5)
def sp_acj4_7_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 1 / Abs(x) - Abs(1 / x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-7-complex · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered true (solved)
@_in(_SETUP5)
def sp_acj4_7_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 1 / Abs(x) - Abs(1 / x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-9-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_9_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(exp(x)))
    Residual = log(exp(x)) - x
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-9-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_9_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(exp(x)))
    Residual = log(exp(x)) - x
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-9-complex · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_9_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(exp(x)))
    Residual = log(exp(x)) - x
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-9-complex · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_9_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(exp(x)))
    Residual = log(exp(x)) - x
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-9-complex · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_9_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = log(exp(x)) - x
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-9-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_9_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(exp(x)))
    Residual = log(exp(x)) - x
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-9-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_9_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(exp(x)))
    Residual = log(exp(x)) - x
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-9-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_9_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(exp(x)))
    Residual = log(exp(x)) - x
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-9-complex · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_9_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = log(exp(x)) - x
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-9-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_9_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(exp(x)))
    Residual = log(exp(x)) - x
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-9-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_9_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(exp(x)))
    Residual = log(exp(x)) - x
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-9-complex · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_9_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(exp(x)))
    Residual = log(exp(x)) - x
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-complex · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered true (solved)
@_in(_SETUP1)
def sp_acj4_90_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-complex · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered true (solved)
@_in(_SETUP2)
def sp_acj4_90_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-complex · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered true (solved)
@_in(_SETUP2)
def sp_acj4_90_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-complex · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered true (solved)
@_in(_SETUP2)
def sp_acj4_90_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-complex · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered true (solved)
@_in(_SETUP3)
def sp_acj4_90_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered true (solved)
@_in(_SETUP3)
def sp_acj4_90_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-complex · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered true (solved)
@_in(_SETUP4)
def sp_acj4_90_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered true (solved)
@_in(_SETUP3)
def sp_acj4_90_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered true (solved)
@_in(_SETUP3)
def sp_acj4_90_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-complex · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered true (solved)
@_in(_SETUP5)
def sp_acj4_90_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-complex · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered true (solved)
@_in(_SETUP5)
def sp_acj4_90_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-complex · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered true (solved)
@_in(_SETUP5)
def sp_acj4_90_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-94-complex · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered true (solved)
@_in(_SETUP1)
def sp_acj4_94_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 7 / Abs(x) - Abs(-7 / x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-94-complex · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered true (solved)
@_in(_SETUP2)
def sp_acj4_94_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 7 / Abs(x) - Abs(-7 / x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-94-complex · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered true (solved)
@_in(_SETUP2)
def sp_acj4_94_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 7 / Abs(x) - Abs(-7 / x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-94-complex · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered true (solved)
@_in(_SETUP2)
def sp_acj4_94_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 7 / Abs(x) - Abs(-7 / x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-94-complex · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered true (solved)
@_in(_SETUP3)
def sp_acj4_94_complex__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = 7 / Abs(x) - Abs(-7 / x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-94-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered true (solved)
@_in(_SETUP3)
def sp_acj4_94_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 7 / Abs(x) - Abs(-7 / x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-94-complex · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered true (solved)
@_in(_SETUP4)
def sp_acj4_94_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 7 / Abs(x) - Abs(-7 / x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-94-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered true (solved)
@_in(_SETUP3)
def sp_acj4_94_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 7 / Abs(x) - Abs(-7 / x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-94-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered true (solved)
@_in(_SETUP3)
def sp_acj4_94_complex__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = 7 / Abs(x) - Abs(-7 / x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-94-complex · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered true (solved)
@_in(_SETUP5)
def sp_acj4_94_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 7 / Abs(x) - Abs(-7 / x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-94-complex · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered true (solved)
@_in(_SETUP5)
def sp_acj4_94_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 7 / Abs(x) - Abs(-7 / x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-94-complex · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered true (solved)
@_in(_SETUP5)
def sp_acj4_94_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 7 / Abs(x) - Abs(-7 / x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-complex · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261028-185930 answered true (solved)
@_in(_SETUP1)
def sp_acj4_99_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-complex · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261028-185603 answered true (solved)
@_in(_SETUP2)
def sp_acj4_99_complex__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-complex · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261028-190021 answered true (solved)
@_in(_SETUP2)
def sp_acj4_99_complex__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-complex · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261028-185941 answered true (solved)
@_in(_SETUP2)
def sp_acj4_99_complex__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-complex · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261028-185041 answered true (solved)
@_in(_SETUP3)
def sp_acj4_99_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = Abs(x) / 3 - Abs(x / -3)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261028-185047 answered true (solved)
@_in(_SETUP3)
def sp_acj4_99_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-complex · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261028-193021 answered true (solved)
@_in(_SETUP4)
def sp_acj4_99_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-complex · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261028-185236 answered true (solved)
@_in(_SETUP3)
def sp_acj4_99_complex__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-complex · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261028-185545 answered true (solved)
@_in(_SETUP3)
def sp_acj4_99_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = Abs(x) / 3 - Abs(x / -3)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-complex · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261028-190032 answered true (solved)
@_in(_SETUP5)
def sp_acj4_99_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-complex · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261028-190628 answered true (solved)
@_in(_SETUP5)
def sp_acj4_99_complex__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-complex · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261028-191418 answered true (solved)
@_in(_SETUP5)
def sp_acj4_99_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# (case, system, expected, the stored run's answer, that run, its function)
CASES = [
    ('sp-acj4-0-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_0_complex__satassume_ask),
    ('sp-acj4-0-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_0_complex__satrefine_refine),
    ('sp-acj4-0-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_0_complex__satsimp_trigsimp),
    ('sp-acj4-0-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_0_complex__satrefine_simplify),
    ('sp-acj4-0-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_0_complex__sympy_auto),
    ('sp-acj4-0-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_0_complex__sympy_ask),
    ('sp-acj4-0-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_0_complex__sympy_satask),
    ('sp-acj4-0-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_0_complex__sympy_refine),
    ('sp-acj4-0-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_0_complex__sympy_simplify),
    ('sp-acj4-0-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_0_complex__sympy_extras_ask),
    ('sp-acj4-0-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_0_complex__sympy_extras_refine),
    ('sp-acj4-0-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_0_complex__sympy_extras_simplify),
    ('sp-acj4-102-complex', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-185930', sp_acj4_102_complex__satassume_ask),
    ('sp-acj4-102-complex', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-185603', sp_acj4_102_complex__satrefine_refine),
    ('sp-acj4-102-complex', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-190021', sp_acj4_102_complex__satsimp_trigsimp),
    ('sp-acj4-102-complex', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-185941', sp_acj4_102_complex__satrefine_simplify),
    ('sp-acj4-102-complex', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-185041', sp_acj4_102_complex__sympy_auto),
    ('sp-acj4-102-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-185047', sp_acj4_102_complex__sympy_ask),
    ('sp-acj4-102-complex', 'sympy-satask', 'true', 'true', 'sympy-satask-20261028-193021', sp_acj4_102_complex__sympy_satask),
    ('sp-acj4-102-complex', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-185236', sp_acj4_102_complex__sympy_refine),
    ('sp-acj4-102-complex', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-185545', sp_acj4_102_complex__sympy_simplify),
    ('sp-acj4-102-complex', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-190032', sp_acj4_102_complex__sympy_extras_ask),
    ('sp-acj4-102-complex', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-190628', sp_acj4_102_complex__sympy_extras_refine),
    ('sp-acj4-102-complex', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-191418', sp_acj4_102_complex__sympy_extras_simplify),
    ('sp-acj4-108-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_108_complex__satassume_ask),
    ('sp-acj4-108-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_108_complex__satrefine_refine),
    ('sp-acj4-108-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_108_complex__satsimp_trigsimp),
    ('sp-acj4-108-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_108_complex__satrefine_simplify),
    ('sp-acj4-108-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_108_complex__sympy_auto),
    ('sp-acj4-108-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_108_complex__sympy_ask),
    ('sp-acj4-108-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_108_complex__sympy_satask),
    ('sp-acj4-108-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_108_complex__sympy_refine),
    ('sp-acj4-108-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_108_complex__sympy_simplify),
    ('sp-acj4-108-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_108_complex__sympy_extras_ask),
    ('sp-acj4-108-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_108_complex__sympy_extras_refine),
    ('sp-acj4-108-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_108_complex__sympy_extras_simplify),
    ('sp-acj4-120-complex', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-185930', sp_acj4_120_complex__satassume_ask),
    ('sp-acj4-120-complex', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-185603', sp_acj4_120_complex__satrefine_refine),
    ('sp-acj4-120-complex', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-190021', sp_acj4_120_complex__satsimp_trigsimp),
    ('sp-acj4-120-complex', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-185941', sp_acj4_120_complex__satrefine_simplify),
    ('sp-acj4-120-complex', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-185041', sp_acj4_120_complex__sympy_auto),
    ('sp-acj4-120-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-185047', sp_acj4_120_complex__sympy_ask),
    ('sp-acj4-120-complex', 'sympy-satask', 'true', 'true', 'sympy-satask-20261028-193021', sp_acj4_120_complex__sympy_satask),
    ('sp-acj4-120-complex', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-185236', sp_acj4_120_complex__sympy_refine),
    ('sp-acj4-120-complex', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-185545', sp_acj4_120_complex__sympy_simplify),
    ('sp-acj4-120-complex', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-190032', sp_acj4_120_complex__sympy_extras_ask),
    ('sp-acj4-120-complex', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-190628', sp_acj4_120_complex__sympy_extras_refine),
    ('sp-acj4-120-complex', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-191418', sp_acj4_120_complex__sympy_extras_simplify),
    ('sp-acj4-130-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_130_complex__satassume_ask),
    ('sp-acj4-130-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_130_complex__satrefine_refine),
    ('sp-acj4-130-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_130_complex__satsimp_trigsimp),
    ('sp-acj4-130-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_130_complex__satrefine_simplify),
    ('sp-acj4-130-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_130_complex__sympy_auto),
    ('sp-acj4-130-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_130_complex__sympy_ask),
    ('sp-acj4-130-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_130_complex__sympy_satask),
    ('sp-acj4-130-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_130_complex__sympy_refine),
    ('sp-acj4-130-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_130_complex__sympy_simplify),
    ('sp-acj4-130-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_130_complex__sympy_extras_ask),
    ('sp-acj4-130-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_130_complex__sympy_extras_refine),
    ('sp-acj4-130-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_130_complex__sympy_extras_simplify),
    ('sp-acj4-131-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_131_complex__satassume_ask),
    ('sp-acj4-131-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_131_complex__satrefine_refine),
    ('sp-acj4-131-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_131_complex__satsimp_trigsimp),
    ('sp-acj4-131-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_131_complex__satrefine_simplify),
    ('sp-acj4-131-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_131_complex__sympy_auto),
    ('sp-acj4-131-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_131_complex__sympy_ask),
    ('sp-acj4-131-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_131_complex__sympy_satask),
    ('sp-acj4-131-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_131_complex__sympy_refine),
    ('sp-acj4-131-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_131_complex__sympy_simplify),
    ('sp-acj4-131-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_131_complex__sympy_extras_ask),
    ('sp-acj4-131-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_131_complex__sympy_extras_refine),
    ('sp-acj4-131-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_131_complex__sympy_extras_simplify),
    ('sp-acj4-132-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_132_complex__satassume_ask),
    ('sp-acj4-132-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_132_complex__satrefine_refine),
    ('sp-acj4-132-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_132_complex__satsimp_trigsimp),
    ('sp-acj4-132-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_132_complex__satrefine_simplify),
    ('sp-acj4-132-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_132_complex__sympy_auto),
    ('sp-acj4-132-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_132_complex__sympy_ask),
    ('sp-acj4-132-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_132_complex__sympy_satask),
    ('sp-acj4-132-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_132_complex__sympy_refine),
    ('sp-acj4-132-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_132_complex__sympy_simplify),
    ('sp-acj4-132-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_132_complex__sympy_extras_ask),
    ('sp-acj4-132-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_132_complex__sympy_extras_refine),
    ('sp-acj4-132-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_132_complex__sympy_extras_simplify),
    ('sp-acj4-133-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_133_complex__satassume_ask),
    ('sp-acj4-133-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_133_complex__satrefine_refine),
    ('sp-acj4-133-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_133_complex__satsimp_trigsimp),
    ('sp-acj4-133-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_133_complex__satrefine_simplify),
    ('sp-acj4-133-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_133_complex__sympy_auto),
    ('sp-acj4-133-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_133_complex__sympy_ask),
    ('sp-acj4-133-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_133_complex__sympy_satask),
    ('sp-acj4-133-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_133_complex__sympy_refine),
    ('sp-acj4-133-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_133_complex__sympy_simplify),
    ('sp-acj4-133-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_133_complex__sympy_extras_ask),
    ('sp-acj4-133-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_133_complex__sympy_extras_refine),
    ('sp-acj4-133-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_133_complex__sympy_extras_simplify),
    ('sp-acj4-137-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_137_complex__satassume_ask),
    ('sp-acj4-137-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_137_complex__satrefine_refine),
    ('sp-acj4-137-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_137_complex__satsimp_trigsimp),
    ('sp-acj4-137-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_137_complex__satrefine_simplify),
    ('sp-acj4-137-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_137_complex__sympy_auto),
    ('sp-acj4-137-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_137_complex__sympy_ask),
    ('sp-acj4-137-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_137_complex__sympy_satask),
    ('sp-acj4-137-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_137_complex__sympy_refine),
    ('sp-acj4-137-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_137_complex__sympy_simplify),
    ('sp-acj4-137-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_137_complex__sympy_extras_ask),
    ('sp-acj4-137-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_137_complex__sympy_extras_refine),
    ('sp-acj4-137-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_137_complex__sympy_extras_simplify),
    ('sp-acj4-147-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_147_complex__satassume_ask),
    ('sp-acj4-147-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_147_complex__satrefine_refine),
    ('sp-acj4-147-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_147_complex__satsimp_trigsimp),
    ('sp-acj4-147-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_147_complex__satrefine_simplify),
    ('sp-acj4-147-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_147_complex__sympy_auto),
    ('sp-acj4-147-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_147_complex__sympy_ask),
    ('sp-acj4-147-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_147_complex__sympy_satask),
    ('sp-acj4-147-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_147_complex__sympy_refine),
    ('sp-acj4-147-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_147_complex__sympy_simplify),
    ('sp-acj4-147-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_147_complex__sympy_extras_ask),
    ('sp-acj4-147-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_147_complex__sympy_extras_refine),
    ('sp-acj4-147-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_147_complex__sympy_extras_simplify),
    ('sp-acj4-151-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_151_complex__satassume_ask),
    ('sp-acj4-151-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_151_complex__satrefine_refine),
    ('sp-acj4-151-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_151_complex__satsimp_trigsimp),
    ('sp-acj4-151-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_151_complex__satrefine_simplify),
    ('sp-acj4-151-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_151_complex__sympy_auto),
    ('sp-acj4-151-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_151_complex__sympy_ask),
    ('sp-acj4-151-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_151_complex__sympy_satask),
    ('sp-acj4-151-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_151_complex__sympy_refine),
    ('sp-acj4-151-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_151_complex__sympy_simplify),
    ('sp-acj4-151-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_151_complex__sympy_extras_ask),
    ('sp-acj4-151-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_151_complex__sympy_extras_refine),
    ('sp-acj4-151-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_151_complex__sympy_extras_simplify),
    ('sp-acj4-153-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_153_complex__satassume_ask),
    ('sp-acj4-153-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_153_complex__satrefine_refine),
    ('sp-acj4-153-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_153_complex__satsimp_trigsimp),
    ('sp-acj4-153-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_153_complex__satrefine_simplify),
    ('sp-acj4-153-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_153_complex__sympy_auto),
    ('sp-acj4-153-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_153_complex__sympy_ask),
    ('sp-acj4-153-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_153_complex__sympy_satask),
    ('sp-acj4-153-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_153_complex__sympy_refine),
    ('sp-acj4-153-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_153_complex__sympy_simplify),
    ('sp-acj4-153-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_153_complex__sympy_extras_ask),
    ('sp-acj4-153-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_153_complex__sympy_extras_refine),
    ('sp-acj4-153-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_153_complex__sympy_extras_simplify),
    ('sp-acj4-154-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_154_complex__satassume_ask),
    ('sp-acj4-154-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_154_complex__satrefine_refine),
    ('sp-acj4-154-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_154_complex__satsimp_trigsimp),
    ('sp-acj4-154-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_154_complex__satrefine_simplify),
    ('sp-acj4-154-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_154_complex__sympy_auto),
    ('sp-acj4-154-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_154_complex__sympy_ask),
    ('sp-acj4-154-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_154_complex__sympy_satask),
    ('sp-acj4-154-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_154_complex__sympy_refine),
    ('sp-acj4-154-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_154_complex__sympy_simplify),
    ('sp-acj4-154-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_154_complex__sympy_extras_ask),
    ('sp-acj4-154-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_154_complex__sympy_extras_refine),
    ('sp-acj4-154-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_154_complex__sympy_extras_simplify),
    ('sp-acj4-165-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_165_complex__satassume_ask),
    ('sp-acj4-165-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_165_complex__satrefine_refine),
    ('sp-acj4-165-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_165_complex__satsimp_trigsimp),
    ('sp-acj4-165-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_165_complex__satrefine_simplify),
    ('sp-acj4-165-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_165_complex__sympy_auto),
    ('sp-acj4-165-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_165_complex__sympy_ask),
    ('sp-acj4-165-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_165_complex__sympy_satask),
    ('sp-acj4-165-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_165_complex__sympy_refine),
    ('sp-acj4-165-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_165_complex__sympy_simplify),
    ('sp-acj4-165-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_165_complex__sympy_extras_ask),
    ('sp-acj4-165-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_165_complex__sympy_extras_refine),
    ('sp-acj4-165-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_165_complex__sympy_extras_simplify),
    ('sp-acj4-173-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_173_complex__satassume_ask),
    ('sp-acj4-173-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_173_complex__satrefine_refine),
    ('sp-acj4-173-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_173_complex__satsimp_trigsimp),
    ('sp-acj4-173-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_173_complex__satrefine_simplify),
    ('sp-acj4-173-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_173_complex__sympy_auto),
    ('sp-acj4-173-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_173_complex__sympy_ask),
    ('sp-acj4-173-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_173_complex__sympy_satask),
    ('sp-acj4-173-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_173_complex__sympy_refine),
    ('sp-acj4-173-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_173_complex__sympy_simplify),
    ('sp-acj4-173-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_173_complex__sympy_extras_ask),
    ('sp-acj4-173-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_173_complex__sympy_extras_refine),
    ('sp-acj4-173-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_173_complex__sympy_extras_simplify),
    ('sp-acj4-176-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_176_complex__satassume_ask),
    ('sp-acj4-176-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_176_complex__satrefine_refine),
    ('sp-acj4-176-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_176_complex__satsimp_trigsimp),
    ('sp-acj4-176-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_176_complex__satrefine_simplify),
    ('sp-acj4-176-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_176_complex__sympy_auto),
    ('sp-acj4-176-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_176_complex__sympy_ask),
    ('sp-acj4-176-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_176_complex__sympy_satask),
    ('sp-acj4-176-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_176_complex__sympy_refine),
    ('sp-acj4-176-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_176_complex__sympy_simplify),
    ('sp-acj4-176-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_176_complex__sympy_extras_ask),
    ('sp-acj4-176-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_176_complex__sympy_extras_refine),
    ('sp-acj4-176-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_176_complex__sympy_extras_simplify),
    ('sp-acj4-177-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_177_complex__satassume_ask),
    ('sp-acj4-177-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_177_complex__satrefine_refine),
    ('sp-acj4-177-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_177_complex__satsimp_trigsimp),
    ('sp-acj4-177-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_177_complex__satrefine_simplify),
    ('sp-acj4-177-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_177_complex__sympy_auto),
    ('sp-acj4-177-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_177_complex__sympy_ask),
    ('sp-acj4-177-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_177_complex__sympy_satask),
    ('sp-acj4-177-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_177_complex__sympy_refine),
    ('sp-acj4-177-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_177_complex__sympy_simplify),
    ('sp-acj4-177-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_177_complex__sympy_extras_ask),
    ('sp-acj4-177-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_177_complex__sympy_extras_refine),
    ('sp-acj4-177-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_177_complex__sympy_extras_simplify),
    ('sp-acj4-180-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_180_complex__satassume_ask),
    ('sp-acj4-180-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_180_complex__satrefine_refine),
    ('sp-acj4-180-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_180_complex__satsimp_trigsimp),
    ('sp-acj4-180-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_180_complex__satrefine_simplify),
    ('sp-acj4-180-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_180_complex__sympy_auto),
    ('sp-acj4-180-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_180_complex__sympy_ask),
    ('sp-acj4-180-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_180_complex__sympy_satask),
    ('sp-acj4-180-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_180_complex__sympy_refine),
    ('sp-acj4-180-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_180_complex__sympy_simplify),
    ('sp-acj4-180-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_180_complex__sympy_extras_ask),
    ('sp-acj4-180-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_180_complex__sympy_extras_refine),
    ('sp-acj4-180-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_180_complex__sympy_extras_simplify),
    ('sp-acj4-183-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_183_complex__satassume_ask),
    ('sp-acj4-183-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_183_complex__satrefine_refine),
    ('sp-acj4-183-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_183_complex__satsimp_trigsimp),
    ('sp-acj4-183-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_183_complex__satrefine_simplify),
    ('sp-acj4-183-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_183_complex__sympy_auto),
    ('sp-acj4-183-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_183_complex__sympy_ask),
    ('sp-acj4-183-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_183_complex__sympy_satask),
    ('sp-acj4-183-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_183_complex__sympy_refine),
    ('sp-acj4-183-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_183_complex__sympy_simplify),
    ('sp-acj4-183-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_183_complex__sympy_extras_ask),
    ('sp-acj4-183-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_183_complex__sympy_extras_refine),
    ('sp-acj4-183-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_183_complex__sympy_extras_simplify),
    ('sp-acj4-189-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_189_complex__satassume_ask),
    ('sp-acj4-189-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_189_complex__satrefine_refine),
    ('sp-acj4-189-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_189_complex__satsimp_trigsimp),
    ('sp-acj4-189-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_189_complex__satrefine_simplify),
    ('sp-acj4-189-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_189_complex__sympy_auto),
    ('sp-acj4-189-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_189_complex__sympy_ask),
    ('sp-acj4-189-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_189_complex__sympy_satask),
    ('sp-acj4-189-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_189_complex__sympy_refine),
    ('sp-acj4-189-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_189_complex__sympy_simplify),
    ('sp-acj4-189-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_189_complex__sympy_extras_ask),
    ('sp-acj4-189-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_189_complex__sympy_extras_refine),
    ('sp-acj4-189-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_189_complex__sympy_extras_simplify),
    ('sp-acj4-190-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_190_complex__satassume_ask),
    ('sp-acj4-190-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_190_complex__satrefine_refine),
    ('sp-acj4-190-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_190_complex__satsimp_trigsimp),
    ('sp-acj4-190-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_190_complex__satrefine_simplify),
    ('sp-acj4-190-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_190_complex__sympy_auto),
    ('sp-acj4-190-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_190_complex__sympy_ask),
    ('sp-acj4-190-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_190_complex__sympy_satask),
    ('sp-acj4-190-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_190_complex__sympy_refine),
    ('sp-acj4-190-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_190_complex__sympy_simplify),
    ('sp-acj4-190-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_190_complex__sympy_extras_ask),
    ('sp-acj4-190-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_190_complex__sympy_extras_refine),
    ('sp-acj4-190-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_190_complex__sympy_extras_simplify),
    ('sp-acj4-191-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_191_complex__satassume_ask),
    ('sp-acj4-191-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_191_complex__satrefine_refine),
    ('sp-acj4-191-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_191_complex__satsimp_trigsimp),
    ('sp-acj4-191-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_191_complex__satrefine_simplify),
    ('sp-acj4-191-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_191_complex__sympy_auto),
    ('sp-acj4-191-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_191_complex__sympy_ask),
    ('sp-acj4-191-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_191_complex__sympy_satask),
    ('sp-acj4-191-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_191_complex__sympy_refine),
    ('sp-acj4-191-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_191_complex__sympy_simplify),
    ('sp-acj4-191-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_191_complex__sympy_extras_ask),
    ('sp-acj4-191-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_191_complex__sympy_extras_refine),
    ('sp-acj4-191-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_191_complex__sympy_extras_simplify),
    ('sp-acj4-20-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_20_complex__satassume_ask),
    ('sp-acj4-20-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_20_complex__satrefine_refine),
    ('sp-acj4-20-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_20_complex__satsimp_trigsimp),
    ('sp-acj4-20-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_20_complex__satrefine_simplify),
    ('sp-acj4-20-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_20_complex__sympy_auto),
    ('sp-acj4-20-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_20_complex__sympy_ask),
    ('sp-acj4-20-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_20_complex__sympy_satask),
    ('sp-acj4-20-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_20_complex__sympy_refine),
    ('sp-acj4-20-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_20_complex__sympy_simplify),
    ('sp-acj4-20-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_20_complex__sympy_extras_ask),
    ('sp-acj4-20-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_20_complex__sympy_extras_refine),
    ('sp-acj4-20-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_20_complex__sympy_extras_simplify),
    ('sp-acj4-203-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_203_complex__satassume_ask),
    ('sp-acj4-203-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_203_complex__satrefine_refine),
    ('sp-acj4-203-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_203_complex__satsimp_trigsimp),
    ('sp-acj4-203-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_203_complex__satrefine_simplify),
    ('sp-acj4-203-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_203_complex__sympy_auto),
    ('sp-acj4-203-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_203_complex__sympy_ask),
    ('sp-acj4-203-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_203_complex__sympy_satask),
    ('sp-acj4-203-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_203_complex__sympy_refine),
    ('sp-acj4-203-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_203_complex__sympy_simplify),
    ('sp-acj4-203-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_203_complex__sympy_extras_ask),
    ('sp-acj4-203-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_203_complex__sympy_extras_refine),
    ('sp-acj4-203-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_203_complex__sympy_extras_simplify),
    ('sp-acj4-213-complex', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-185930', sp_acj4_213_complex__satassume_ask),
    ('sp-acj4-213-complex', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-185603', sp_acj4_213_complex__satrefine_refine),
    ('sp-acj4-213-complex', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-190021', sp_acj4_213_complex__satsimp_trigsimp),
    ('sp-acj4-213-complex', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-185941', sp_acj4_213_complex__satrefine_simplify),
    ('sp-acj4-213-complex', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-185041', sp_acj4_213_complex__sympy_auto),
    ('sp-acj4-213-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-185047', sp_acj4_213_complex__sympy_ask),
    ('sp-acj4-213-complex', 'sympy-satask', 'true', 'true', 'sympy-satask-20261028-193021', sp_acj4_213_complex__sympy_satask),
    ('sp-acj4-213-complex', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-185236', sp_acj4_213_complex__sympy_refine),
    ('sp-acj4-213-complex', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-185545', sp_acj4_213_complex__sympy_simplify),
    ('sp-acj4-213-complex', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-190032', sp_acj4_213_complex__sympy_extras_ask),
    ('sp-acj4-213-complex', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-190628', sp_acj4_213_complex__sympy_extras_refine),
    ('sp-acj4-213-complex', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-191418', sp_acj4_213_complex__sympy_extras_simplify),
    ('sp-acj4-216-complex', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-185930', sp_acj4_216_complex__satassume_ask),
    ('sp-acj4-216-complex', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-185603', sp_acj4_216_complex__satrefine_refine),
    ('sp-acj4-216-complex', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-190021', sp_acj4_216_complex__satsimp_trigsimp),
    ('sp-acj4-216-complex', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-185941', sp_acj4_216_complex__satrefine_simplify),
    ('sp-acj4-216-complex', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-185041', sp_acj4_216_complex__sympy_auto),
    ('sp-acj4-216-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-185047', sp_acj4_216_complex__sympy_ask),
    ('sp-acj4-216-complex', 'sympy-satask', 'true', 'true', 'sympy-satask-20261028-193021', sp_acj4_216_complex__sympy_satask),
    ('sp-acj4-216-complex', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-185236', sp_acj4_216_complex__sympy_refine),
    ('sp-acj4-216-complex', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-185545', sp_acj4_216_complex__sympy_simplify),
    ('sp-acj4-216-complex', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-190032', sp_acj4_216_complex__sympy_extras_ask),
    ('sp-acj4-216-complex', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-190628', sp_acj4_216_complex__sympy_extras_refine),
    ('sp-acj4-216-complex', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-191418', sp_acj4_216_complex__sympy_extras_simplify),
    ('sp-acj4-22-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_22_complex__satassume_ask),
    ('sp-acj4-22-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_22_complex__satrefine_refine),
    ('sp-acj4-22-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_22_complex__satsimp_trigsimp),
    ('sp-acj4-22-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_22_complex__satrefine_simplify),
    ('sp-acj4-22-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_22_complex__sympy_auto),
    ('sp-acj4-22-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_22_complex__sympy_ask),
    ('sp-acj4-22-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_22_complex__sympy_satask),
    ('sp-acj4-22-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_22_complex__sympy_refine),
    ('sp-acj4-22-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_22_complex__sympy_simplify),
    ('sp-acj4-22-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_22_complex__sympy_extras_ask),
    ('sp-acj4-22-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_22_complex__sympy_extras_refine),
    ('sp-acj4-22-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_22_complex__sympy_extras_simplify),
    ('sp-acj4-234-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_234_complex__satassume_ask),
    ('sp-acj4-234-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_234_complex__satrefine_refine),
    ('sp-acj4-234-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_234_complex__satsimp_trigsimp),
    ('sp-acj4-234-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_234_complex__satrefine_simplify),
    ('sp-acj4-234-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_234_complex__sympy_auto),
    ('sp-acj4-234-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_234_complex__sympy_ask),
    ('sp-acj4-234-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_234_complex__sympy_satask),
    ('sp-acj4-234-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_234_complex__sympy_refine),
    ('sp-acj4-234-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_234_complex__sympy_simplify),
    ('sp-acj4-234-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_234_complex__sympy_extras_ask),
    ('sp-acj4-234-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_234_complex__sympy_extras_refine),
    ('sp-acj4-234-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_234_complex__sympy_extras_simplify),
    ('sp-acj4-252-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_252_complex__satassume_ask),
    ('sp-acj4-252-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_252_complex__satrefine_refine),
    ('sp-acj4-252-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_252_complex__satsimp_trigsimp),
    ('sp-acj4-252-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_252_complex__satrefine_simplify),
    ('sp-acj4-252-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_252_complex__sympy_auto),
    ('sp-acj4-252-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_252_complex__sympy_ask),
    ('sp-acj4-252-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_252_complex__sympy_satask),
    ('sp-acj4-252-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_252_complex__sympy_refine),
    ('sp-acj4-252-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_252_complex__sympy_simplify),
    ('sp-acj4-252-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_252_complex__sympy_extras_ask),
    ('sp-acj4-252-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_252_complex__sympy_extras_refine),
    ('sp-acj4-252-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_252_complex__sympy_extras_simplify),
    ('sp-acj4-253-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_253_complex__satassume_ask),
    ('sp-acj4-253-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_253_complex__satrefine_refine),
    ('sp-acj4-253-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_253_complex__satsimp_trigsimp),
    ('sp-acj4-253-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_253_complex__satrefine_simplify),
    ('sp-acj4-253-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_253_complex__sympy_auto),
    ('sp-acj4-253-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_253_complex__sympy_ask),
    ('sp-acj4-253-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_253_complex__sympy_satask),
    ('sp-acj4-253-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_253_complex__sympy_refine),
    ('sp-acj4-253-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_253_complex__sympy_simplify),
    ('sp-acj4-253-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_253_complex__sympy_extras_ask),
    ('sp-acj4-253-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_253_complex__sympy_extras_refine),
    ('sp-acj4-253-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_253_complex__sympy_extras_simplify),
    ('sp-acj4-260-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_260_complex__satassume_ask),
    ('sp-acj4-260-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_260_complex__satrefine_refine),
    ('sp-acj4-260-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_260_complex__satsimp_trigsimp),
    ('sp-acj4-260-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_260_complex__satrefine_simplify),
    ('sp-acj4-260-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_260_complex__sympy_auto),
    ('sp-acj4-260-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_260_complex__sympy_ask),
    ('sp-acj4-260-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_260_complex__sympy_satask),
    ('sp-acj4-260-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_260_complex__sympy_refine),
    ('sp-acj4-260-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_260_complex__sympy_simplify),
    ('sp-acj4-260-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_260_complex__sympy_extras_ask),
    ('sp-acj4-260-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_260_complex__sympy_extras_refine),
    ('sp-acj4-260-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_260_complex__sympy_extras_simplify),
    ('sp-acj4-261-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_261_complex__satassume_ask),
    ('sp-acj4-261-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_261_complex__satrefine_refine),
    ('sp-acj4-261-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_261_complex__satsimp_trigsimp),
    ('sp-acj4-261-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_261_complex__satrefine_simplify),
    ('sp-acj4-261-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_261_complex__sympy_auto),
    ('sp-acj4-261-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_261_complex__sympy_ask),
    ('sp-acj4-261-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_261_complex__sympy_satask),
    ('sp-acj4-261-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_261_complex__sympy_refine),
    ('sp-acj4-261-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_261_complex__sympy_simplify),
    ('sp-acj4-261-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_261_complex__sympy_extras_ask),
    ('sp-acj4-261-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_261_complex__sympy_extras_refine),
    ('sp-acj4-261-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_261_complex__sympy_extras_simplify),
    ('sp-acj4-266-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_266_complex__satassume_ask),
    ('sp-acj4-266-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_266_complex__satrefine_refine),
    ('sp-acj4-266-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_266_complex__satsimp_trigsimp),
    ('sp-acj4-266-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_266_complex__satrefine_simplify),
    ('sp-acj4-266-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_266_complex__sympy_auto),
    ('sp-acj4-266-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_266_complex__sympy_ask),
    ('sp-acj4-266-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_266_complex__sympy_satask),
    ('sp-acj4-266-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_266_complex__sympy_refine),
    ('sp-acj4-266-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_266_complex__sympy_simplify),
    ('sp-acj4-266-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_266_complex__sympy_extras_ask),
    ('sp-acj4-266-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_266_complex__sympy_extras_refine),
    ('sp-acj4-266-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_266_complex__sympy_extras_simplify),
    ('sp-acj4-267-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_267_complex__satassume_ask),
    ('sp-acj4-267-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_267_complex__satrefine_refine),
    ('sp-acj4-267-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_267_complex__satsimp_trigsimp),
    ('sp-acj4-267-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_267_complex__satrefine_simplify),
    ('sp-acj4-267-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_267_complex__sympy_auto),
    ('sp-acj4-267-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_267_complex__sympy_ask),
    ('sp-acj4-267-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_267_complex__sympy_satask),
    ('sp-acj4-267-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_267_complex__sympy_refine),
    ('sp-acj4-267-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_267_complex__sympy_simplify),
    ('sp-acj4-267-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_267_complex__sympy_extras_ask),
    ('sp-acj4-267-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_267_complex__sympy_extras_refine),
    ('sp-acj4-267-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_267_complex__sympy_extras_simplify),
    ('sp-acj4-274-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_274_complex__satassume_ask),
    ('sp-acj4-274-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_274_complex__satrefine_refine),
    ('sp-acj4-274-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_274_complex__satsimp_trigsimp),
    ('sp-acj4-274-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_274_complex__satrefine_simplify),
    ('sp-acj4-274-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_274_complex__sympy_auto),
    ('sp-acj4-274-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_274_complex__sympy_ask),
    ('sp-acj4-274-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_274_complex__sympy_satask),
    ('sp-acj4-274-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_274_complex__sympy_refine),
    ('sp-acj4-274-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_274_complex__sympy_simplify),
    ('sp-acj4-274-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_274_complex__sympy_extras_ask),
    ('sp-acj4-274-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_274_complex__sympy_extras_refine),
    ('sp-acj4-274-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_274_complex__sympy_extras_simplify),
    ('sp-acj4-278-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_278_complex__satassume_ask),
    ('sp-acj4-278-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_278_complex__satrefine_refine),
    ('sp-acj4-278-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_278_complex__satsimp_trigsimp),
    ('sp-acj4-278-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_278_complex__satrefine_simplify),
    ('sp-acj4-278-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_278_complex__sympy_auto),
    ('sp-acj4-278-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_278_complex__sympy_ask),
    ('sp-acj4-278-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_278_complex__sympy_satask),
    ('sp-acj4-278-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_278_complex__sympy_refine),
    ('sp-acj4-278-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_278_complex__sympy_simplify),
    ('sp-acj4-278-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_278_complex__sympy_extras_ask),
    ('sp-acj4-278-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_278_complex__sympy_extras_refine),
    ('sp-acj4-278-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_278_complex__sympy_extras_simplify),
    ('sp-acj4-283-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_283_complex__satassume_ask),
    ('sp-acj4-283-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_283_complex__satrefine_refine),
    ('sp-acj4-283-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_283_complex__satsimp_trigsimp),
    ('sp-acj4-283-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_283_complex__satrefine_simplify),
    ('sp-acj4-283-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_283_complex__sympy_auto),
    ('sp-acj4-283-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_283_complex__sympy_ask),
    ('sp-acj4-283-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_283_complex__sympy_satask),
    ('sp-acj4-283-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_283_complex__sympy_refine),
    ('sp-acj4-283-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_283_complex__sympy_simplify),
    ('sp-acj4-283-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_283_complex__sympy_extras_ask),
    ('sp-acj4-283-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_283_complex__sympy_extras_refine),
    ('sp-acj4-283-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_283_complex__sympy_extras_simplify),
    ('sp-acj4-284-complex', 'satassume-ask', 'true', 'null', 'satassume-ask-20261028-185930', sp_acj4_284_complex__satassume_ask),
    ('sp-acj4-284-complex', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-185603', sp_acj4_284_complex__satrefine_refine),
    ('sp-acj4-284-complex', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_284_complex__satsimp_trigsimp),
    ('sp-acj4-284-complex', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-185941', sp_acj4_284_complex__satrefine_simplify),
    ('sp-acj4-284-complex', 'sympy-auto', 'true', 'null', 'sympy-auto-20261028-185041', sp_acj4_284_complex__sympy_auto),
    ('sp-acj4-284-complex', 'sympy-ask', 'true', 'null', 'sympy-ask-20261028-185047', sp_acj4_284_complex__sympy_ask),
    ('sp-acj4-284-complex', 'sympy-satask', 'true', 'null', 'sympy-satask-20261028-193021', sp_acj4_284_complex__sympy_satask),
    ('sp-acj4-284-complex', 'sympy-refine', 'true', 'null', 'sympy-refine-20261028-185236', sp_acj4_284_complex__sympy_refine),
    ('sp-acj4-284-complex', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261028-185545', sp_acj4_284_complex__sympy_simplify),
    ('sp-acj4-284-complex', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_284_complex__sympy_extras_ask),
    ('sp-acj4-284-complex', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_284_complex__sympy_extras_refine),
    ('sp-acj4-284-complex', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_284_complex__sympy_extras_simplify),
    ('sp-acj4-288-complex', 'satassume-ask', 'true', 'null', 'satassume-ask-20261028-185930', sp_acj4_288_complex__satassume_ask),
    ('sp-acj4-288-complex', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-185603', sp_acj4_288_complex__satrefine_refine),
    ('sp-acj4-288-complex', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_288_complex__satsimp_trigsimp),
    ('sp-acj4-288-complex', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-185941', sp_acj4_288_complex__satrefine_simplify),
    ('sp-acj4-288-complex', 'sympy-auto', 'true', 'null', 'sympy-auto-20261028-185041', sp_acj4_288_complex__sympy_auto),
    ('sp-acj4-288-complex', 'sympy-ask', 'true', 'null', 'sympy-ask-20261028-185047', sp_acj4_288_complex__sympy_ask),
    ('sp-acj4-288-complex', 'sympy-satask', 'true', 'null', 'sympy-satask-20261028-193021', sp_acj4_288_complex__sympy_satask),
    ('sp-acj4-288-complex', 'sympy-refine', 'true', 'null', 'sympy-refine-20261028-185236', sp_acj4_288_complex__sympy_refine),
    ('sp-acj4-288-complex', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261028-185545', sp_acj4_288_complex__sympy_simplify),
    ('sp-acj4-288-complex', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_288_complex__sympy_extras_ask),
    ('sp-acj4-288-complex', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_288_complex__sympy_extras_refine),
    ('sp-acj4-288-complex', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_288_complex__sympy_extras_simplify),
    ('sp-acj4-30-complex', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-185930', sp_acj4_30_complex__satassume_ask),
    ('sp-acj4-30-complex', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-185603', sp_acj4_30_complex__satrefine_refine),
    ('sp-acj4-30-complex', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-190021', sp_acj4_30_complex__satsimp_trigsimp),
    ('sp-acj4-30-complex', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-185941', sp_acj4_30_complex__satrefine_simplify),
    ('sp-acj4-30-complex', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-185041', sp_acj4_30_complex__sympy_auto),
    ('sp-acj4-30-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-185047', sp_acj4_30_complex__sympy_ask),
    ('sp-acj4-30-complex', 'sympy-satask', 'true', 'true', 'sympy-satask-20261028-193021', sp_acj4_30_complex__sympy_satask),
    ('sp-acj4-30-complex', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-185236', sp_acj4_30_complex__sympy_refine),
    ('sp-acj4-30-complex', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-185545', sp_acj4_30_complex__sympy_simplify),
    ('sp-acj4-30-complex', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-190032', sp_acj4_30_complex__sympy_extras_ask),
    ('sp-acj4-30-complex', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-190628', sp_acj4_30_complex__sympy_extras_refine),
    ('sp-acj4-30-complex', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-191418', sp_acj4_30_complex__sympy_extras_simplify),
    ('sp-acj4-334-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_334_complex__satassume_ask),
    ('sp-acj4-334-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_334_complex__satrefine_refine),
    ('sp-acj4-334-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_334_complex__satsimp_trigsimp),
    ('sp-acj4-334-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_334_complex__satrefine_simplify),
    ('sp-acj4-334-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_334_complex__sympy_auto),
    ('sp-acj4-334-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_334_complex__sympy_ask),
    ('sp-acj4-334-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_334_complex__sympy_satask),
    ('sp-acj4-334-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_334_complex__sympy_refine),
    ('sp-acj4-334-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_334_complex__sympy_simplify),
    ('sp-acj4-334-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_334_complex__sympy_extras_ask),
    ('sp-acj4-334-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_334_complex__sympy_extras_refine),
    ('sp-acj4-334-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_334_complex__sympy_extras_simplify),
    ('sp-acj4-335-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_335_complex__satassume_ask),
    ('sp-acj4-335-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_335_complex__satrefine_refine),
    ('sp-acj4-335-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_335_complex__satsimp_trigsimp),
    ('sp-acj4-335-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_335_complex__satrefine_simplify),
    ('sp-acj4-335-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_335_complex__sympy_auto),
    ('sp-acj4-335-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_335_complex__sympy_ask),
    ('sp-acj4-335-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_335_complex__sympy_satask),
    ('sp-acj4-335-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_335_complex__sympy_refine),
    ('sp-acj4-335-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_335_complex__sympy_simplify),
    ('sp-acj4-335-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_335_complex__sympy_extras_ask),
    ('sp-acj4-335-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_335_complex__sympy_extras_refine),
    ('sp-acj4-335-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_335_complex__sympy_extras_simplify),
    ('sp-acj4-336-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_336_complex__satassume_ask),
    ('sp-acj4-336-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_336_complex__satrefine_refine),
    ('sp-acj4-336-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_336_complex__satsimp_trigsimp),
    ('sp-acj4-336-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_336_complex__satrefine_simplify),
    ('sp-acj4-336-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_336_complex__sympy_auto),
    ('sp-acj4-336-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_336_complex__sympy_ask),
    ('sp-acj4-336-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_336_complex__sympy_satask),
    ('sp-acj4-336-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_336_complex__sympy_refine),
    ('sp-acj4-336-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_336_complex__sympy_simplify),
    ('sp-acj4-336-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_336_complex__sympy_extras_ask),
    ('sp-acj4-336-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_336_complex__sympy_extras_refine),
    ('sp-acj4-336-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_336_complex__sympy_extras_simplify),
    ('sp-acj4-343-complex', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-185930', sp_acj4_343_complex__satassume_ask),
    ('sp-acj4-343-complex', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-185603', sp_acj4_343_complex__satrefine_refine),
    ('sp-acj4-343-complex', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-190021', sp_acj4_343_complex__satsimp_trigsimp),
    ('sp-acj4-343-complex', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-185941', sp_acj4_343_complex__satrefine_simplify),
    ('sp-acj4-343-complex', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-185041', sp_acj4_343_complex__sympy_auto),
    ('sp-acj4-343-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-185047', sp_acj4_343_complex__sympy_ask),
    ('sp-acj4-343-complex', 'sympy-satask', 'true', 'true', 'sympy-satask-20261028-193021', sp_acj4_343_complex__sympy_satask),
    ('sp-acj4-343-complex', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-185236', sp_acj4_343_complex__sympy_refine),
    ('sp-acj4-343-complex', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-185545', sp_acj4_343_complex__sympy_simplify),
    ('sp-acj4-343-complex', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-190032', sp_acj4_343_complex__sympy_extras_ask),
    ('sp-acj4-343-complex', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-190628', sp_acj4_343_complex__sympy_extras_refine),
    ('sp-acj4-343-complex', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-191418', sp_acj4_343_complex__sympy_extras_simplify),
    ('sp-acj4-344-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_344_complex__satassume_ask),
    ('sp-acj4-344-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_344_complex__satrefine_refine),
    ('sp-acj4-344-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_344_complex__satsimp_trigsimp),
    ('sp-acj4-344-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_344_complex__satrefine_simplify),
    ('sp-acj4-344-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_344_complex__sympy_auto),
    ('sp-acj4-344-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_344_complex__sympy_ask),
    ('sp-acj4-344-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_344_complex__sympy_satask),
    ('sp-acj4-344-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_344_complex__sympy_refine),
    ('sp-acj4-344-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_344_complex__sympy_simplify),
    ('sp-acj4-344-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_344_complex__sympy_extras_ask),
    ('sp-acj4-344-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_344_complex__sympy_extras_refine),
    ('sp-acj4-344-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_344_complex__sympy_extras_simplify),
    ('sp-acj4-368-complex', 'satassume-ask', 'true', 'null', 'satassume-ask-20261028-185930', sp_acj4_368_complex__satassume_ask),
    ('sp-acj4-368-complex', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-185603', sp_acj4_368_complex__satrefine_refine),
    ('sp-acj4-368-complex', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_368_complex__satsimp_trigsimp),
    ('sp-acj4-368-complex', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-185941', sp_acj4_368_complex__satrefine_simplify),
    ('sp-acj4-368-complex', 'sympy-auto', 'true', 'null', 'sympy-auto-20261028-185041', sp_acj4_368_complex__sympy_auto),
    ('sp-acj4-368-complex', 'sympy-ask', 'true', 'null', 'sympy-ask-20261028-185047', sp_acj4_368_complex__sympy_ask),
    ('sp-acj4-368-complex', 'sympy-satask', 'true', 'null', 'sympy-satask-20261028-193021', sp_acj4_368_complex__sympy_satask),
    ('sp-acj4-368-complex', 'sympy-refine', 'true', 'null', 'sympy-refine-20261028-185236', sp_acj4_368_complex__sympy_refine),
    ('sp-acj4-368-complex', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261028-185545', sp_acj4_368_complex__sympy_simplify),
    ('sp-acj4-368-complex', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_368_complex__sympy_extras_ask),
    ('sp-acj4-368-complex', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_368_complex__sympy_extras_refine),
    ('sp-acj4-368-complex', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_368_complex__sympy_extras_simplify),
    ('sp-acj4-369-complex', 'satassume-ask', 'true', 'null', 'satassume-ask-20261028-185930', sp_acj4_369_complex__satassume_ask),
    ('sp-acj4-369-complex', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261028-185603', sp_acj4_369_complex__satrefine_refine),
    ('sp-acj4-369-complex', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_369_complex__satsimp_trigsimp),
    ('sp-acj4-369-complex', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_369_complex__satrefine_simplify),
    ('sp-acj4-369-complex', 'sympy-auto', 'true', 'null', 'sympy-auto-20261028-185041', sp_acj4_369_complex__sympy_auto),
    ('sp-acj4-369-complex', 'sympy-ask', 'true', 'null', 'sympy-ask-20261028-185047', sp_acj4_369_complex__sympy_ask),
    ('sp-acj4-369-complex', 'sympy-satask', 'true', 'null', 'sympy-satask-20261028-193021', sp_acj4_369_complex__sympy_satask),
    ('sp-acj4-369-complex', 'sympy-refine', 'true', 'null', 'sympy-refine-20261028-185236', sp_acj4_369_complex__sympy_refine),
    ('sp-acj4-369-complex', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261028-185545', sp_acj4_369_complex__sympy_simplify),
    ('sp-acj4-369-complex', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_369_complex__sympy_extras_ask),
    ('sp-acj4-369-complex', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_369_complex__sympy_extras_refine),
    ('sp-acj4-369-complex', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_369_complex__sympy_extras_simplify),
    ('sp-acj4-370-complex', 'satassume-ask', 'true', 'null', 'satassume-ask-20261028-185930', sp_acj4_370_complex__satassume_ask),
    ('sp-acj4-370-complex', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261028-185603', sp_acj4_370_complex__satrefine_refine),
    ('sp-acj4-370-complex', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_370_complex__satsimp_trigsimp),
    ('sp-acj4-370-complex', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_370_complex__satrefine_simplify),
    ('sp-acj4-370-complex', 'sympy-auto', 'true', 'null', 'sympy-auto-20261028-185041', sp_acj4_370_complex__sympy_auto),
    ('sp-acj4-370-complex', 'sympy-ask', 'true', 'null', 'sympy-ask-20261028-185047', sp_acj4_370_complex__sympy_ask),
    ('sp-acj4-370-complex', 'sympy-satask', 'true', 'null', 'sympy-satask-20261028-193021', sp_acj4_370_complex__sympy_satask),
    ('sp-acj4-370-complex', 'sympy-refine', 'true', 'null', 'sympy-refine-20261028-185236', sp_acj4_370_complex__sympy_refine),
    ('sp-acj4-370-complex', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261028-185545', sp_acj4_370_complex__sympy_simplify),
    ('sp-acj4-370-complex', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_370_complex__sympy_extras_ask),
    ('sp-acj4-370-complex', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_370_complex__sympy_extras_refine),
    ('sp-acj4-370-complex', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_370_complex__sympy_extras_simplify),
    ('sp-acj4-371-complex', 'satassume-ask', 'true', 'null', 'satassume-ask-20261028-185930', sp_acj4_371_complex__satassume_ask),
    ('sp-acj4-371-complex', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261028-185603', sp_acj4_371_complex__satrefine_refine),
    ('sp-acj4-371-complex', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_371_complex__satsimp_trigsimp),
    ('sp-acj4-371-complex', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_371_complex__satrefine_simplify),
    ('sp-acj4-371-complex', 'sympy-auto', 'true', 'null', 'sympy-auto-20261028-185041', sp_acj4_371_complex__sympy_auto),
    ('sp-acj4-371-complex', 'sympy-ask', 'true', 'null', 'sympy-ask-20261028-185047', sp_acj4_371_complex__sympy_ask),
    ('sp-acj4-371-complex', 'sympy-satask', 'true', 'null', 'sympy-satask-20261028-193021', sp_acj4_371_complex__sympy_satask),
    ('sp-acj4-371-complex', 'sympy-refine', 'true', 'null', 'sympy-refine-20261028-185236', sp_acj4_371_complex__sympy_refine),
    ('sp-acj4-371-complex', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261028-185545', sp_acj4_371_complex__sympy_simplify),
    ('sp-acj4-371-complex', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_371_complex__sympy_extras_ask),
    ('sp-acj4-371-complex', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_371_complex__sympy_extras_refine),
    ('sp-acj4-371-complex', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_371_complex__sympy_extras_simplify),
    ('sp-acj4-372-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_372_complex__satassume_ask),
    ('sp-acj4-372-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_372_complex__satrefine_refine),
    ('sp-acj4-372-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_372_complex__satsimp_trigsimp),
    ('sp-acj4-372-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_372_complex__satrefine_simplify),
    ('sp-acj4-372-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_372_complex__sympy_auto),
    ('sp-acj4-372-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_372_complex__sympy_ask),
    ('sp-acj4-372-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_372_complex__sympy_satask),
    ('sp-acj4-372-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_372_complex__sympy_refine),
    ('sp-acj4-372-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_372_complex__sympy_simplify),
    ('sp-acj4-372-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_372_complex__sympy_extras_ask),
    ('sp-acj4-372-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_372_complex__sympy_extras_refine),
    ('sp-acj4-372-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_372_complex__sympy_extras_simplify),
    ('sp-acj4-373-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_373_complex__satassume_ask),
    ('sp-acj4-373-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_373_complex__satrefine_refine),
    ('sp-acj4-373-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_373_complex__satsimp_trigsimp),
    ('sp-acj4-373-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_373_complex__satrefine_simplify),
    ('sp-acj4-373-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_373_complex__sympy_auto),
    ('sp-acj4-373-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_373_complex__sympy_ask),
    ('sp-acj4-373-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_373_complex__sympy_satask),
    ('sp-acj4-373-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_373_complex__sympy_refine),
    ('sp-acj4-373-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_373_complex__sympy_simplify),
    ('sp-acj4-373-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_373_complex__sympy_extras_ask),
    ('sp-acj4-373-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_373_complex__sympy_extras_refine),
    ('sp-acj4-373-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_373_complex__sympy_extras_simplify),
    ('sp-acj4-387-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_387_complex__satassume_ask),
    ('sp-acj4-387-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_387_complex__satrefine_refine),
    ('sp-acj4-387-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_387_complex__satsimp_trigsimp),
    ('sp-acj4-387-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_387_complex__satrefine_simplify),
    ('sp-acj4-387-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_387_complex__sympy_auto),
    ('sp-acj4-387-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_387_complex__sympy_ask),
    ('sp-acj4-387-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_387_complex__sympy_satask),
    ('sp-acj4-387-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_387_complex__sympy_refine),
    ('sp-acj4-387-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_387_complex__sympy_simplify),
    ('sp-acj4-387-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_387_complex__sympy_extras_ask),
    ('sp-acj4-387-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_387_complex__sympy_extras_refine),
    ('sp-acj4-387-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_387_complex__sympy_extras_simplify),
    ('sp-acj4-389-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_389_complex__satassume_ask),
    ('sp-acj4-389-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_389_complex__satrefine_refine),
    ('sp-acj4-389-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_389_complex__satsimp_trigsimp),
    ('sp-acj4-389-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_389_complex__satrefine_simplify),
    ('sp-acj4-389-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_389_complex__sympy_auto),
    ('sp-acj4-389-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_389_complex__sympy_ask),
    ('sp-acj4-389-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_389_complex__sympy_satask),
    ('sp-acj4-389-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_389_complex__sympy_refine),
    ('sp-acj4-389-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_389_complex__sympy_simplify),
    ('sp-acj4-389-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_389_complex__sympy_extras_ask),
    ('sp-acj4-389-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_389_complex__sympy_extras_refine),
    ('sp-acj4-389-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_389_complex__sympy_extras_simplify),
    ('sp-acj4-396-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_396_complex__satassume_ask),
    ('sp-acj4-396-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_396_complex__satrefine_refine),
    ('sp-acj4-396-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_396_complex__satsimp_trigsimp),
    ('sp-acj4-396-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_396_complex__satrefine_simplify),
    ('sp-acj4-396-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_396_complex__sympy_auto),
    ('sp-acj4-396-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_396_complex__sympy_ask),
    ('sp-acj4-396-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_396_complex__sympy_satask),
    ('sp-acj4-396-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_396_complex__sympy_refine),
    ('sp-acj4-396-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_396_complex__sympy_simplify),
    ('sp-acj4-396-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_396_complex__sympy_extras_ask),
    ('sp-acj4-396-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_396_complex__sympy_extras_refine),
    ('sp-acj4-396-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_396_complex__sympy_extras_simplify),
    ('sp-acj4-40-complex', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-185930', sp_acj4_40_complex__satassume_ask),
    ('sp-acj4-40-complex', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-185603', sp_acj4_40_complex__satrefine_refine),
    ('sp-acj4-40-complex', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-190021', sp_acj4_40_complex__satsimp_trigsimp),
    ('sp-acj4-40-complex', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-185941', sp_acj4_40_complex__satrefine_simplify),
    ('sp-acj4-40-complex', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-185041', sp_acj4_40_complex__sympy_auto),
    ('sp-acj4-40-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-185047', sp_acj4_40_complex__sympy_ask),
    ('sp-acj4-40-complex', 'sympy-satask', 'true', 'true', 'sympy-satask-20261028-193021', sp_acj4_40_complex__sympy_satask),
    ('sp-acj4-40-complex', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-185236', sp_acj4_40_complex__sympy_refine),
    ('sp-acj4-40-complex', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-185545', sp_acj4_40_complex__sympy_simplify),
    ('sp-acj4-40-complex', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-190032', sp_acj4_40_complex__sympy_extras_ask),
    ('sp-acj4-40-complex', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-190628', sp_acj4_40_complex__sympy_extras_refine),
    ('sp-acj4-40-complex', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-191418', sp_acj4_40_complex__sympy_extras_simplify),
    ('sp-acj4-403-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_403_complex__satassume_ask),
    ('sp-acj4-403-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_403_complex__satrefine_refine),
    ('sp-acj4-403-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_403_complex__satsimp_trigsimp),
    ('sp-acj4-403-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_403_complex__satrefine_simplify),
    ('sp-acj4-403-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_403_complex__sympy_auto),
    ('sp-acj4-403-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_403_complex__sympy_ask),
    ('sp-acj4-403-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_403_complex__sympy_satask),
    ('sp-acj4-403-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_403_complex__sympy_refine),
    ('sp-acj4-403-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_403_complex__sympy_simplify),
    ('sp-acj4-403-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_403_complex__sympy_extras_ask),
    ('sp-acj4-403-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_403_complex__sympy_extras_refine),
    ('sp-acj4-403-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_403_complex__sympy_extras_simplify),
    ('sp-acj4-404-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_404_complex__satassume_ask),
    ('sp-acj4-404-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_404_complex__satrefine_refine),
    ('sp-acj4-404-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_404_complex__satsimp_trigsimp),
    ('sp-acj4-404-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_404_complex__satrefine_simplify),
    ('sp-acj4-404-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_404_complex__sympy_auto),
    ('sp-acj4-404-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_404_complex__sympy_ask),
    ('sp-acj4-404-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_404_complex__sympy_satask),
    ('sp-acj4-404-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_404_complex__sympy_refine),
    ('sp-acj4-404-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_404_complex__sympy_simplify),
    ('sp-acj4-404-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_404_complex__sympy_extras_ask),
    ('sp-acj4-404-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_404_complex__sympy_extras_refine),
    ('sp-acj4-404-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_404_complex__sympy_extras_simplify),
    ('sp-acj4-414-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_414_complex__satassume_ask),
    ('sp-acj4-414-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_414_complex__satrefine_refine),
    ('sp-acj4-414-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_414_complex__satsimp_trigsimp),
    ('sp-acj4-414-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_414_complex__satrefine_simplify),
    ('sp-acj4-414-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_414_complex__sympy_auto),
    ('sp-acj4-414-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_414_complex__sympy_ask),
    ('sp-acj4-414-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_414_complex__sympy_satask),
    ('sp-acj4-414-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_414_complex__sympy_refine),
    ('sp-acj4-414-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_414_complex__sympy_simplify),
    ('sp-acj4-414-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_414_complex__sympy_extras_ask),
    ('sp-acj4-414-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_414_complex__sympy_extras_refine),
    ('sp-acj4-414-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_414_complex__sympy_extras_simplify),
    ('sp-acj4-415-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_415_complex__satassume_ask),
    ('sp-acj4-415-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_415_complex__satrefine_refine),
    ('sp-acj4-415-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_415_complex__satsimp_trigsimp),
    ('sp-acj4-415-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_415_complex__satrefine_simplify),
    ('sp-acj4-415-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_415_complex__sympy_auto),
    ('sp-acj4-415-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_415_complex__sympy_ask),
    ('sp-acj4-415-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_415_complex__sympy_satask),
    ('sp-acj4-415-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_415_complex__sympy_refine),
    ('sp-acj4-415-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_415_complex__sympy_simplify),
    ('sp-acj4-415-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_415_complex__sympy_extras_ask),
    ('sp-acj4-415-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_415_complex__sympy_extras_refine),
    ('sp-acj4-415-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_415_complex__sympy_extras_simplify),
    ('sp-acj4-420-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_420_complex__satassume_ask),
    ('sp-acj4-420-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_420_complex__satrefine_refine),
    ('sp-acj4-420-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_420_complex__satsimp_trigsimp),
    ('sp-acj4-420-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_420_complex__satrefine_simplify),
    ('sp-acj4-420-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_420_complex__sympy_auto),
    ('sp-acj4-420-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_420_complex__sympy_ask),
    ('sp-acj4-420-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_420_complex__sympy_satask),
    ('sp-acj4-420-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_420_complex__sympy_refine),
    ('sp-acj4-420-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_420_complex__sympy_simplify),
    ('sp-acj4-420-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_420_complex__sympy_extras_ask),
    ('sp-acj4-420-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_420_complex__sympy_extras_refine),
    ('sp-acj4-420-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_420_complex__sympy_extras_simplify),
    ('sp-acj4-421-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_421_complex__satassume_ask),
    ('sp-acj4-421-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_421_complex__satrefine_refine),
    ('sp-acj4-421-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_421_complex__satsimp_trigsimp),
    ('sp-acj4-421-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_421_complex__satrefine_simplify),
    ('sp-acj4-421-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_421_complex__sympy_auto),
    ('sp-acj4-421-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_421_complex__sympy_ask),
    ('sp-acj4-421-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_421_complex__sympy_satask),
    ('sp-acj4-421-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_421_complex__sympy_refine),
    ('sp-acj4-421-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_421_complex__sympy_simplify),
    ('sp-acj4-421-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_421_complex__sympy_extras_ask),
    ('sp-acj4-421-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_421_complex__sympy_extras_refine),
    ('sp-acj4-421-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_421_complex__sympy_extras_simplify),
    ('sp-acj4-422-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_422_complex__satassume_ask),
    ('sp-acj4-422-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_422_complex__satrefine_refine),
    ('sp-acj4-422-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_422_complex__satsimp_trigsimp),
    ('sp-acj4-422-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_422_complex__satrefine_simplify),
    ('sp-acj4-422-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_422_complex__sympy_auto),
    ('sp-acj4-422-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_422_complex__sympy_ask),
    ('sp-acj4-422-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_422_complex__sympy_satask),
    ('sp-acj4-422-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_422_complex__sympy_refine),
    ('sp-acj4-422-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_422_complex__sympy_simplify),
    ('sp-acj4-422-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_422_complex__sympy_extras_ask),
    ('sp-acj4-422-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_422_complex__sympy_extras_refine),
    ('sp-acj4-422-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_422_complex__sympy_extras_simplify),
    ('sp-acj4-423-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_423_complex__satassume_ask),
    ('sp-acj4-423-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_423_complex__satrefine_refine),
    ('sp-acj4-423-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_423_complex__satsimp_trigsimp),
    ('sp-acj4-423-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_423_complex__satrefine_simplify),
    ('sp-acj4-423-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_423_complex__sympy_auto),
    ('sp-acj4-423-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_423_complex__sympy_ask),
    ('sp-acj4-423-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_423_complex__sympy_satask),
    ('sp-acj4-423-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_423_complex__sympy_refine),
    ('sp-acj4-423-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_423_complex__sympy_simplify),
    ('sp-acj4-423-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_423_complex__sympy_extras_ask),
    ('sp-acj4-423-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_423_complex__sympy_extras_refine),
    ('sp-acj4-423-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_423_complex__sympy_extras_simplify),
    ('sp-acj4-424-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_424_complex__satassume_ask),
    ('sp-acj4-424-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_424_complex__satrefine_refine),
    ('sp-acj4-424-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_424_complex__satsimp_trigsimp),
    ('sp-acj4-424-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_424_complex__satrefine_simplify),
    ('sp-acj4-424-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_424_complex__sympy_auto),
    ('sp-acj4-424-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_424_complex__sympy_ask),
    ('sp-acj4-424-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_424_complex__sympy_satask),
    ('sp-acj4-424-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_424_complex__sympy_refine),
    ('sp-acj4-424-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_424_complex__sympy_simplify),
    ('sp-acj4-424-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_424_complex__sympy_extras_ask),
    ('sp-acj4-424-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_424_complex__sympy_extras_refine),
    ('sp-acj4-424-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_424_complex__sympy_extras_simplify),
    ('sp-acj4-430-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_430_complex__satassume_ask),
    ('sp-acj4-430-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_430_complex__satrefine_refine),
    ('sp-acj4-430-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_430_complex__satsimp_trigsimp),
    ('sp-acj4-430-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_430_complex__satrefine_simplify),
    ('sp-acj4-430-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_430_complex__sympy_auto),
    ('sp-acj4-430-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_430_complex__sympy_ask),
    ('sp-acj4-430-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_430_complex__sympy_satask),
    ('sp-acj4-430-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_430_complex__sympy_refine),
    ('sp-acj4-430-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_430_complex__sympy_simplify),
    ('sp-acj4-430-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_430_complex__sympy_extras_ask),
    ('sp-acj4-430-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_430_complex__sympy_extras_refine),
    ('sp-acj4-430-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_430_complex__sympy_extras_simplify),
    ('sp-acj4-433-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_433_complex__satassume_ask),
    ('sp-acj4-433-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_433_complex__satrefine_refine),
    ('sp-acj4-433-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_433_complex__satsimp_trigsimp),
    ('sp-acj4-433-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_433_complex__satrefine_simplify),
    ('sp-acj4-433-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_433_complex__sympy_auto),
    ('sp-acj4-433-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_433_complex__sympy_ask),
    ('sp-acj4-433-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_433_complex__sympy_satask),
    ('sp-acj4-433-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_433_complex__sympy_refine),
    ('sp-acj4-433-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_433_complex__sympy_simplify),
    ('sp-acj4-433-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_433_complex__sympy_extras_ask),
    ('sp-acj4-433-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_433_complex__sympy_extras_refine),
    ('sp-acj4-433-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_433_complex__sympy_extras_simplify),
    ('sp-acj4-442-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_442_complex__satassume_ask),
    ('sp-acj4-442-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_442_complex__satrefine_refine),
    ('sp-acj4-442-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_442_complex__satsimp_trigsimp),
    ('sp-acj4-442-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_442_complex__satrefine_simplify),
    ('sp-acj4-442-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_442_complex__sympy_auto),
    ('sp-acj4-442-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_442_complex__sympy_ask),
    ('sp-acj4-442-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_442_complex__sympy_satask),
    ('sp-acj4-442-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_442_complex__sympy_refine),
    ('sp-acj4-442-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_442_complex__sympy_simplify),
    ('sp-acj4-442-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_442_complex__sympy_extras_ask),
    ('sp-acj4-442-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_442_complex__sympy_extras_refine),
    ('sp-acj4-442-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_442_complex__sympy_extras_simplify),
    ('sp-acj4-446-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_446_complex__satassume_ask),
    ('sp-acj4-446-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_446_complex__satrefine_refine),
    ('sp-acj4-446-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_446_complex__satsimp_trigsimp),
    ('sp-acj4-446-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_446_complex__satrefine_simplify),
    ('sp-acj4-446-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_446_complex__sympy_auto),
    ('sp-acj4-446-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_446_complex__sympy_ask),
    ('sp-acj4-446-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_446_complex__sympy_satask),
    ('sp-acj4-446-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_446_complex__sympy_refine),
    ('sp-acj4-446-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_446_complex__sympy_simplify),
    ('sp-acj4-446-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_446_complex__sympy_extras_ask),
    ('sp-acj4-446-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_446_complex__sympy_extras_refine),
    ('sp-acj4-446-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_446_complex__sympy_extras_simplify),
    ('sp-acj4-450-complex', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-185930', sp_acj4_450_complex__satassume_ask),
    ('sp-acj4-450-complex', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-185603', sp_acj4_450_complex__satrefine_refine),
    ('sp-acj4-450-complex', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-190021', sp_acj4_450_complex__satsimp_trigsimp),
    ('sp-acj4-450-complex', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-185941', sp_acj4_450_complex__satrefine_simplify),
    ('sp-acj4-450-complex', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-185041', sp_acj4_450_complex__sympy_auto),
    ('sp-acj4-450-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-185047', sp_acj4_450_complex__sympy_ask),
    ('sp-acj4-450-complex', 'sympy-satask', 'true', 'true', 'sympy-satask-20261028-193021', sp_acj4_450_complex__sympy_satask),
    ('sp-acj4-450-complex', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-185236', sp_acj4_450_complex__sympy_refine),
    ('sp-acj4-450-complex', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-185545', sp_acj4_450_complex__sympy_simplify),
    ('sp-acj4-450-complex', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-190032', sp_acj4_450_complex__sympy_extras_ask),
    ('sp-acj4-450-complex', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-190628', sp_acj4_450_complex__sympy_extras_refine),
    ('sp-acj4-450-complex', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-191418', sp_acj4_450_complex__sympy_extras_simplify),
    ('sp-acj4-451-complex', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-185930', sp_acj4_451_complex__satassume_ask),
    ('sp-acj4-451-complex', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-185603', sp_acj4_451_complex__satrefine_refine),
    ('sp-acj4-451-complex', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-190021', sp_acj4_451_complex__satsimp_trigsimp),
    ('sp-acj4-451-complex', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-185941', sp_acj4_451_complex__satrefine_simplify),
    ('sp-acj4-451-complex', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-185041', sp_acj4_451_complex__sympy_auto),
    ('sp-acj4-451-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-185047', sp_acj4_451_complex__sympy_ask),
    ('sp-acj4-451-complex', 'sympy-satask', 'true', 'true', 'sympy-satask-20261028-193021', sp_acj4_451_complex__sympy_satask),
    ('sp-acj4-451-complex', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-185236', sp_acj4_451_complex__sympy_refine),
    ('sp-acj4-451-complex', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-185545', sp_acj4_451_complex__sympy_simplify),
    ('sp-acj4-451-complex', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-190032', sp_acj4_451_complex__sympy_extras_ask),
    ('sp-acj4-451-complex', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-190628', sp_acj4_451_complex__sympy_extras_refine),
    ('sp-acj4-451-complex', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-191418', sp_acj4_451_complex__sympy_extras_simplify),
    ('sp-acj4-50-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_50_complex__satassume_ask),
    ('sp-acj4-50-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_50_complex__satrefine_refine),
    ('sp-acj4-50-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_50_complex__satsimp_trigsimp),
    ('sp-acj4-50-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_50_complex__satrefine_simplify),
    ('sp-acj4-50-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_50_complex__sympy_auto),
    ('sp-acj4-50-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_50_complex__sympy_ask),
    ('sp-acj4-50-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_50_complex__sympy_satask),
    ('sp-acj4-50-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_50_complex__sympy_refine),
    ('sp-acj4-50-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_50_complex__sympy_simplify),
    ('sp-acj4-50-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_50_complex__sympy_extras_ask),
    ('sp-acj4-50-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_50_complex__sympy_extras_refine),
    ('sp-acj4-50-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_50_complex__sympy_extras_simplify),
    ('sp-acj4-51-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_51_complex__satassume_ask),
    ('sp-acj4-51-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_51_complex__satrefine_refine),
    ('sp-acj4-51-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_51_complex__satsimp_trigsimp),
    ('sp-acj4-51-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_51_complex__satrefine_simplify),
    ('sp-acj4-51-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_51_complex__sympy_auto),
    ('sp-acj4-51-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_51_complex__sympy_ask),
    ('sp-acj4-51-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_51_complex__sympy_satask),
    ('sp-acj4-51-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_51_complex__sympy_refine),
    ('sp-acj4-51-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_51_complex__sympy_simplify),
    ('sp-acj4-51-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_51_complex__sympy_extras_ask),
    ('sp-acj4-51-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_51_complex__sympy_extras_refine),
    ('sp-acj4-51-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_51_complex__sympy_extras_simplify),
    ('sp-acj4-55-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_55_complex__satassume_ask),
    ('sp-acj4-55-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_55_complex__satrefine_refine),
    ('sp-acj4-55-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_55_complex__satsimp_trigsimp),
    ('sp-acj4-55-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_55_complex__satrefine_simplify),
    ('sp-acj4-55-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_55_complex__sympy_auto),
    ('sp-acj4-55-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_55_complex__sympy_ask),
    ('sp-acj4-55-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_55_complex__sympy_satask),
    ('sp-acj4-55-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_55_complex__sympy_refine),
    ('sp-acj4-55-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_55_complex__sympy_simplify),
    ('sp-acj4-55-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_55_complex__sympy_extras_ask),
    ('sp-acj4-55-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_55_complex__sympy_extras_refine),
    ('sp-acj4-55-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_55_complex__sympy_extras_simplify),
    ('sp-acj4-56-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_56_complex__satassume_ask),
    ('sp-acj4-56-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_56_complex__satrefine_refine),
    ('sp-acj4-56-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_56_complex__satsimp_trigsimp),
    ('sp-acj4-56-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_56_complex__satrefine_simplify),
    ('sp-acj4-56-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_56_complex__sympy_auto),
    ('sp-acj4-56-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_56_complex__sympy_ask),
    ('sp-acj4-56-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_56_complex__sympy_satask),
    ('sp-acj4-56-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_56_complex__sympy_refine),
    ('sp-acj4-56-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_56_complex__sympy_simplify),
    ('sp-acj4-56-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_56_complex__sympy_extras_ask),
    ('sp-acj4-56-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_56_complex__sympy_extras_refine),
    ('sp-acj4-56-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_56_complex__sympy_extras_simplify),
    ('sp-acj4-6-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_6_complex__satassume_ask),
    ('sp-acj4-6-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_6_complex__satrefine_refine),
    ('sp-acj4-6-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_6_complex__satsimp_trigsimp),
    ('sp-acj4-6-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_6_complex__satrefine_simplify),
    ('sp-acj4-6-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_6_complex__sympy_auto),
    ('sp-acj4-6-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_6_complex__sympy_ask),
    ('sp-acj4-6-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_6_complex__sympy_satask),
    ('sp-acj4-6-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_6_complex__sympy_refine),
    ('sp-acj4-6-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_6_complex__sympy_simplify),
    ('sp-acj4-6-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_6_complex__sympy_extras_ask),
    ('sp-acj4-6-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_6_complex__sympy_extras_refine),
    ('sp-acj4-6-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_6_complex__sympy_extras_simplify),
    ('sp-acj4-7-complex', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-185930', sp_acj4_7_complex__satassume_ask),
    ('sp-acj4-7-complex', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-185603', sp_acj4_7_complex__satrefine_refine),
    ('sp-acj4-7-complex', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-190021', sp_acj4_7_complex__satsimp_trigsimp),
    ('sp-acj4-7-complex', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-185941', sp_acj4_7_complex__satrefine_simplify),
    ('sp-acj4-7-complex', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-185041', sp_acj4_7_complex__sympy_auto),
    ('sp-acj4-7-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-185047', sp_acj4_7_complex__sympy_ask),
    ('sp-acj4-7-complex', 'sympy-satask', 'true', 'true', 'sympy-satask-20261028-193021', sp_acj4_7_complex__sympy_satask),
    ('sp-acj4-7-complex', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-185236', sp_acj4_7_complex__sympy_refine),
    ('sp-acj4-7-complex', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-185545', sp_acj4_7_complex__sympy_simplify),
    ('sp-acj4-7-complex', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-190032', sp_acj4_7_complex__sympy_extras_ask),
    ('sp-acj4-7-complex', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-190628', sp_acj4_7_complex__sympy_extras_refine),
    ('sp-acj4-7-complex', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-191418', sp_acj4_7_complex__sympy_extras_simplify),
    ('sp-acj4-9-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261028-185930', sp_acj4_9_complex__satassume_ask),
    ('sp-acj4-9-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261028-185603', sp_acj4_9_complex__satrefine_refine),
    ('sp-acj4-9-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261028-190021', sp_acj4_9_complex__satsimp_trigsimp),
    ('sp-acj4-9-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261028-185941', sp_acj4_9_complex__satrefine_simplify),
    ('sp-acj4-9-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261028-185041', sp_acj4_9_complex__sympy_auto),
    ('sp-acj4-9-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261028-185047', sp_acj4_9_complex__sympy_ask),
    ('sp-acj4-9-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261028-193021', sp_acj4_9_complex__sympy_satask),
    ('sp-acj4-9-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261028-185236', sp_acj4_9_complex__sympy_refine),
    ('sp-acj4-9-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261028-185545', sp_acj4_9_complex__sympy_simplify),
    ('sp-acj4-9-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261028-190032', sp_acj4_9_complex__sympy_extras_ask),
    ('sp-acj4-9-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261028-190628', sp_acj4_9_complex__sympy_extras_refine),
    ('sp-acj4-9-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261028-191418', sp_acj4_9_complex__sympy_extras_simplify),
    ('sp-acj4-90-complex', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-185930', sp_acj4_90_complex__satassume_ask),
    ('sp-acj4-90-complex', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-185603', sp_acj4_90_complex__satrefine_refine),
    ('sp-acj4-90-complex', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-190021', sp_acj4_90_complex__satsimp_trigsimp),
    ('sp-acj4-90-complex', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-185941', sp_acj4_90_complex__satrefine_simplify),
    ('sp-acj4-90-complex', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-185041', sp_acj4_90_complex__sympy_auto),
    ('sp-acj4-90-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-185047', sp_acj4_90_complex__sympy_ask),
    ('sp-acj4-90-complex', 'sympy-satask', 'true', 'true', 'sympy-satask-20261028-193021', sp_acj4_90_complex__sympy_satask),
    ('sp-acj4-90-complex', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-185236', sp_acj4_90_complex__sympy_refine),
    ('sp-acj4-90-complex', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-185545', sp_acj4_90_complex__sympy_simplify),
    ('sp-acj4-90-complex', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-190032', sp_acj4_90_complex__sympy_extras_ask),
    ('sp-acj4-90-complex', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-190628', sp_acj4_90_complex__sympy_extras_refine),
    ('sp-acj4-90-complex', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-191418', sp_acj4_90_complex__sympy_extras_simplify),
    ('sp-acj4-94-complex', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-185930', sp_acj4_94_complex__satassume_ask),
    ('sp-acj4-94-complex', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-185603', sp_acj4_94_complex__satrefine_refine),
    ('sp-acj4-94-complex', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-190021', sp_acj4_94_complex__satsimp_trigsimp),
    ('sp-acj4-94-complex', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-185941', sp_acj4_94_complex__satrefine_simplify),
    ('sp-acj4-94-complex', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-185041', sp_acj4_94_complex__sympy_auto),
    ('sp-acj4-94-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-185047', sp_acj4_94_complex__sympy_ask),
    ('sp-acj4-94-complex', 'sympy-satask', 'true', 'true', 'sympy-satask-20261028-193021', sp_acj4_94_complex__sympy_satask),
    ('sp-acj4-94-complex', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-185236', sp_acj4_94_complex__sympy_refine),
    ('sp-acj4-94-complex', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-185545', sp_acj4_94_complex__sympy_simplify),
    ('sp-acj4-94-complex', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-190032', sp_acj4_94_complex__sympy_extras_ask),
    ('sp-acj4-94-complex', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-190628', sp_acj4_94_complex__sympy_extras_refine),
    ('sp-acj4-94-complex', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-191418', sp_acj4_94_complex__sympy_extras_simplify),
    ('sp-acj4-99-complex', 'satassume-ask', 'true', 'true', 'satassume-ask-20261028-185930', sp_acj4_99_complex__satassume_ask),
    ('sp-acj4-99-complex', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261028-185603', sp_acj4_99_complex__satrefine_refine),
    ('sp-acj4-99-complex', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261028-190021', sp_acj4_99_complex__satsimp_trigsimp),
    ('sp-acj4-99-complex', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261028-185941', sp_acj4_99_complex__satrefine_simplify),
    ('sp-acj4-99-complex', 'sympy-auto', 'true', 'true', 'sympy-auto-20261028-185041', sp_acj4_99_complex__sympy_auto),
    ('sp-acj4-99-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261028-185047', sp_acj4_99_complex__sympy_ask),
    ('sp-acj4-99-complex', 'sympy-satask', 'true', 'true', 'sympy-satask-20261028-193021', sp_acj4_99_complex__sympy_satask),
    ('sp-acj4-99-complex', 'sympy-refine', 'true', 'true', 'sympy-refine-20261028-185236', sp_acj4_99_complex__sympy_refine),
    ('sp-acj4-99-complex', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261028-185545', sp_acj4_99_complex__sympy_simplify),
    ('sp-acj4-99-complex', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261028-190032', sp_acj4_99_complex__sympy_extras_ask),
    ('sp-acj4-99-complex', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261028-190628', sp_acj4_99_complex__sympy_extras_refine),
    ('sp-acj4-99-complex', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261028-191418', sp_acj4_99_complex__sympy_extras_simplify),
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
