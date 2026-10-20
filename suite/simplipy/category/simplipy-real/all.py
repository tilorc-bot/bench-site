# assume-eval: a runnable script from the results browser
# Run: python3 this-file.py (or paste it into python or Jupyter).
# suite simplipy · category simplipy-real · all Python systems (70 cases listed)
# 836 case run(s), a function each (listed in CASES).  Each runs in a fresh copy of
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
# dropped (not a unary fact about one symbol): Ne(exp(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(exp(x), -1, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(sin(x))
# dropped (not a unary fact about one symbol): ~Q.zero(tanh(x))
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(exp(1)) > 0)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(pi) > 0)
# dropped (not a unary fact about one symbol): Ne(sinh(acos(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(acos(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(acos(x)))
# dropped (not a unary fact about one symbol): Ne(sinh(asin(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sinh(asin(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cosh(asin(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(cos(x)))
# dropped (not a unary fact about one symbol): Ne(tan(cos(x)), I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(tan(cos(x)), -I, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(cos(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(cos(x)), -1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(sin(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(sin(x)), -1, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(sin(x)))
# dropped (not a unary fact about one symbol): Ne(sin(tanh(x)), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(sin(tanh(x)), -1, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(-6 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(-8 / x)
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, pi))
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(-pi) > 0)
# dropped (not a unary fact about one symbol): Ne(x, 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(x, -1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(-Abs(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): Ne(-Abs(x), -1, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(-exp(x))
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, 7))
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(log(5)) > 0)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(log(7)) > 0)
# dropped (not a unary fact about one symbol): Or(~Q.zero(x), re(log(pi)) > 0)
# dropped (not a unary fact about one symbol): Q.real(acos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(acos(x))
# dropped (not a unary fact about one symbol): Q.real(acosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(acosh(x))
# dropped (not a unary fact about one symbol): ~Q.zero(Pow(x, 9))
# dropped (not a unary fact about one symbol): Ne(Abs(x), 1, evaluate=False)
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(asin(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(asin(x)))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(cos(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(sin(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(Abs(tanh(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(asin(Abs(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(tanh(Abs(x))))
# dropped (not a unary fact about one symbol): ~Q.zero(-Abs(x))
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(-cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(log(x))
# dropped (not a unary fact about one symbol): ~Q.zero(-log(x))
# dropped (not a unary fact about one symbol): ~Q.zero(tan(x))
# dropped (not a unary fact about one symbol): ~Q.zero(-tan(x))


# ---- case sp-acj4-1-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_1_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asin(Abs(x)) - Abs(asin(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_1_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asin(Abs(x)) - Abs(asin(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_1_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asin(Abs(x)) - Abs(asin(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_1_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asin(Abs(x)) - Abs(asin(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_1_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = asin(Abs(x)) - Abs(asin(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_1_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asin(Abs(x)) - Abs(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_1_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asin(Abs(x)) - Abs(asin(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_1_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asin(Abs(x)) - Abs(asin(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_1_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = asin(Abs(x)) - Abs(asin(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_1_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asin(Abs(x)) - Abs(asin(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_1_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asin(Abs(x)) - Abs(asin(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_1_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = asin(Abs(x)) - Abs(asin(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered true (solved)
@_in(_SETUP1)
def sp_acj4_102_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_102_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered true (solved)
@_in(_SETUP2)
def sp_acj4_102_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_102_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_102_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = Abs(x) / 6 - Abs(x / -6)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered true (solved)
@_in(_SETUP3)
def sp_acj4_102_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered true (solved)
@_in(_SETUP4)
def sp_acj4_102_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered true (solved)
@_in(_SETUP3)
def sp_acj4_102_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_102_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = Abs(x) / 6 - Abs(x / -6)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_102_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_102_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_102_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_108_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_108_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_108_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_108_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_108_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = Abs(x) / x - (x / Abs(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_108_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_108_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_108_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_108_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = Abs(x) / x - (x / Abs(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_108_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_108_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_108_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered true (solved)
@_in(_SETUP1)
def sp_acj4_120_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_120_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered true (solved)
@_in(_SETUP2)
def sp_acj4_120_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_120_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_120_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = pi / Abs(x) - Abs(pi / x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered true (solved)
@_in(_SETUP3)
def sp_acj4_120_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered true (solved)
@_in(_SETUP4)
def sp_acj4_120_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered true (solved)
@_in(_SETUP3)
def sp_acj4_120_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_120_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = pi / Abs(x) - Abs(pi / x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_120_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_120_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_120_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-127-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_127_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(exp(x), 1, evaluate=False), Ne(exp(x), -1, evaluate=False))
    Residual = Abs(atanh(exp(x))) - atanh(exp(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-127-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_127_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(exp(x), 1, evaluate=False), Ne(exp(x), -1, evaluate=False))
    Residual = Abs(atanh(exp(x))) - atanh(exp(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-127-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_127_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(exp(x), 1, evaluate=False), Ne(exp(x), -1, evaluate=False))
    Residual = Abs(atanh(exp(x))) - atanh(exp(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-127-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_127_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(exp(x), 1, evaluate=False), Ne(exp(x), -1, evaluate=False))
    Residual = Abs(atanh(exp(x))) - atanh(exp(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-127-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_127_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = Abs(atanh(exp(x))) - atanh(exp(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-127-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_127_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(exp(x), 1, evaluate=False), Ne(exp(x), -1, evaluate=False))
    Residual = Abs(atanh(exp(x))) - atanh(exp(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-127-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_127_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(exp(x), 1, evaluate=False), Ne(exp(x), -1, evaluate=False))
    Residual = Abs(atanh(exp(x))) - atanh(exp(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-127-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_127_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(exp(x), 1, evaluate=False), Ne(exp(x), -1, evaluate=False))
    Residual = Abs(atanh(exp(x))) - atanh(exp(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-127-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_127_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = Abs(atanh(exp(x))) - atanh(exp(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-127-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_127_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(exp(x), 1, evaluate=False), Ne(exp(x), -1, evaluate=False))
    Residual = Abs(atanh(exp(x))) - atanh(exp(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-128-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_128_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(cos(asin(x))) - cos(asin(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-128-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_128_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(cos(asin(x))) - cos(asin(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-128-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_128_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(cos(asin(x))) - cos(asin(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-128-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_128_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(cos(asin(x))) - cos(asin(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-128-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_128_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = Abs(cos(asin(x))) - cos(asin(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-128-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_128_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(cos(asin(x))) - cos(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-128-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_128_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(cos(asin(x))) - cos(asin(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-128-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_128_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(cos(asin(x))) - cos(asin(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-128-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_128_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = Abs(cos(asin(x))) - cos(asin(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-128-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_128_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(cos(asin(x))) - cos(asin(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-128-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_128_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(cos(asin(x))) - cos(asin(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-128-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_128_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(cos(asin(x))) - cos(asin(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_131_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_131_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_131_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_131_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_131_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_131_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_131_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_131_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_131_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_131_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_131_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_131_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_132_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_132_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_132_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_132_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_132_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_132_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_132_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_132_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_132_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_132_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_132_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_132_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_133_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_133_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_133_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_133_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_133_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_133_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_133_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_133_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_133_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_133_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_133_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_133_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-136-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_136_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(exp(1)) > 0))
    Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-136-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_136_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(exp(1)) > 0))
    Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-136-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_136_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(exp(1)) > 0))
    Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-136-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_136_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(exp(1)) > 0))
    Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-136-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_136_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-136-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_136_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(exp(1)) > 0))
    Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-136-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_136_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(exp(1)) > 0))
    Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-136-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_136_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(exp(1)) > 0))
    Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-136-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_136_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-136-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_136_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(exp(1)) > 0))
    Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-136-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_136_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(exp(1)) > 0))
    Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-136-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_136_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(exp(1)) > 0))
    Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_137_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_137_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_137_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_137_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_137_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_137_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_137_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_137_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_137_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_137_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_137_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_137_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-14-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered true (solved)
@_in(_SETUP1)
def sp_acj4_14_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -sin(x) - sin(-x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-14-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_14_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -sin(x) - sin(-x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-14-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered true (solved)
@_in(_SETUP2)
def sp_acj4_14_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -sin(x) - sin(-x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-14-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_14_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -sin(x) - sin(-x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-14-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_14_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = -sin(x) - sin(-x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-14-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered true (solved)
@_in(_SETUP3)
def sp_acj4_14_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -sin(x) - sin(-x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-14-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered true (solved)
@_in(_SETUP4)
def sp_acj4_14_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -sin(x) - sin(-x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-14-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered true (solved)
@_in(_SETUP3)
def sp_acj4_14_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -sin(x) - sin(-x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-14-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_14_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = -sin(x) - sin(-x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-14-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_14_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -sin(x) - sin(-x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-14-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_14_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -sin(x) - sin(-x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-14-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_14_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -sin(x) - sin(-x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-145-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_145_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(sin(acos(x))) - cos(asin(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-145-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_145_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(sin(acos(x))) - cos(asin(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-145-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_145_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(sin(acos(x))) - cos(asin(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-145-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_145_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(sin(acos(x))) - cos(asin(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-145-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_145_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = Abs(sin(acos(x))) - cos(asin(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-145-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_145_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(sin(acos(x))) - cos(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-145-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_145_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(sin(acos(x))) - cos(asin(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-145-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_145_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(sin(acos(x))) - cos(asin(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-145-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_145_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = Abs(sin(acos(x))) - cos(asin(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-145-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_145_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(sin(acos(x))) - cos(asin(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-145-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_145_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(sin(acos(x))) - cos(asin(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-145-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_145_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(sin(acos(x))) - cos(asin(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-162-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_162_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-162-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_162_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-162-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_162_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-162-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_162_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-162-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_162_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-162-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_162_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-162-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_162_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-162-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_162_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-162-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_162_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-162-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_162_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-162-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_162_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-162-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_162_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-179-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_179_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
    Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-179-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_179_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
    Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-179-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_179_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
    Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-179-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_179_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
    Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-179-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_179_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-179-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_179_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
    Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-179-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_179_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
    Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-179-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_179_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
    Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-179-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_179_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-179-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_179_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
    Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-179-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_179_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
    Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-179-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_179_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
    Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-181-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_181_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
    Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-181-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_181_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
    Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-181-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_181_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
    Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-181-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_181_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
    Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-181-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_181_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-181-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_181_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
    Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-181-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_181_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
    Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-181-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_181_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
    Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-181-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_181_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-181-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_181_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
    Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-181-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_181_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
    Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-181-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_181_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
    Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-185-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_185_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(cos(x))), Ne(tan(cos(x)), I, evaluate=False), Ne(tan(cos(x)), -I, evaluate=False))
    Residual = atan(tan(cos(x))) - cos(x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-185-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_185_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(cos(x))), Ne(tan(cos(x)), I, evaluate=False), Ne(tan(cos(x)), -I, evaluate=False))
    Residual = atan(tan(cos(x))) - cos(x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-185-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered true (solved)
@_in(_SETUP2)
def sp_acj4_185_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(cos(x))), Ne(tan(cos(x)), I, evaluate=False), Ne(tan(cos(x)), -I, evaluate=False))
    Residual = atan(tan(cos(x))) - cos(x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-185-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_185_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(cos(x))), Ne(tan(cos(x)), I, evaluate=False), Ne(tan(cos(x)), -I, evaluate=False))
    Residual = atan(tan(cos(x))) - cos(x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-185-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_185_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = atan(tan(cos(x))) - cos(x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-185-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_185_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(cos(x))), Ne(tan(cos(x)), I, evaluate=False), Ne(tan(cos(x)), -I, evaluate=False))
    Residual = atan(tan(cos(x))) - cos(x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-185-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_185_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(cos(x))), Ne(tan(cos(x)), I, evaluate=False), Ne(tan(cos(x)), -I, evaluate=False))
    Residual = atan(tan(cos(x))) - cos(x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-185-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_185_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(cos(x))), Ne(tan(cos(x)), I, evaluate=False), Ne(tan(cos(x)), -I, evaluate=False))
    Residual = atan(tan(cos(x))) - cos(x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-185-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_185_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = atan(tan(cos(x))) - cos(x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-185-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_185_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(cos(x))), Ne(tan(cos(x)), I, evaluate=False), Ne(tan(cos(x)), -I, evaluate=False))
    Residual = atan(tan(cos(x))) - cos(x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-185-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_185_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(cos(x))), Ne(tan(cos(x)), I, evaluate=False), Ne(tan(cos(x)), -I, evaluate=False))
    Residual = atan(tan(cos(x))) - cos(x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-185-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_185_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(cos(x))), Ne(tan(cos(x)), I, evaluate=False), Ne(tan(cos(x)), -I, evaluate=False))
    Residual = atan(tan(cos(x))) - cos(x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-194-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_194_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(cos(x)), 1, evaluate=False), Ne(sin(cos(x)), -1, evaluate=False), ~Q.zero(cos(cos(x))))
    Residual = atanh(sin(cos(x))) - asinh(tan(cos(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-194-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_194_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(cos(x)), 1, evaluate=False), Ne(sin(cos(x)), -1, evaluate=False), ~Q.zero(cos(cos(x))))
    Residual = atanh(sin(cos(x))) - asinh(tan(cos(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-194-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_194_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(cos(x)), 1, evaluate=False), Ne(sin(cos(x)), -1, evaluate=False), ~Q.zero(cos(cos(x))))
    Residual = atanh(sin(cos(x))) - asinh(tan(cos(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-194-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_194_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(cos(x)), 1, evaluate=False), Ne(sin(cos(x)), -1, evaluate=False), ~Q.zero(cos(cos(x))))
    Residual = atanh(sin(cos(x))) - asinh(tan(cos(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-194-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_194_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = atanh(sin(cos(x))) - asinh(tan(cos(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-194-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_194_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(cos(x)), 1, evaluate=False), Ne(sin(cos(x)), -1, evaluate=False), ~Q.zero(cos(cos(x))))
    Residual = atanh(sin(cos(x))) - asinh(tan(cos(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-194-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_194_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(cos(x)), 1, evaluate=False), Ne(sin(cos(x)), -1, evaluate=False), ~Q.zero(cos(cos(x))))
    Residual = atanh(sin(cos(x))) - asinh(tan(cos(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-194-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_194_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(cos(x)), 1, evaluate=False), Ne(sin(cos(x)), -1, evaluate=False), ~Q.zero(cos(cos(x))))
    Residual = atanh(sin(cos(x))) - asinh(tan(cos(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-194-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_194_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = atanh(sin(cos(x))) - asinh(tan(cos(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-194-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_194_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(cos(x)), 1, evaluate=False), Ne(sin(cos(x)), -1, evaluate=False), ~Q.zero(cos(cos(x))))
    Residual = atanh(sin(cos(x))) - asinh(tan(cos(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-194-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_194_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(cos(x)), 1, evaluate=False), Ne(sin(cos(x)), -1, evaluate=False), ~Q.zero(cos(cos(x))))
    Residual = atanh(sin(cos(x))) - asinh(tan(cos(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-194-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_194_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(cos(x)), 1, evaluate=False), Ne(sin(cos(x)), -1, evaluate=False), ~Q.zero(cos(cos(x))))
    Residual = atanh(sin(cos(x))) - asinh(tan(cos(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-195-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_195_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(sin(x)), 1, evaluate=False), Ne(sin(sin(x)), -1, evaluate=False), ~Q.zero(cos(sin(x))))
    Residual = atanh(sin(sin(x))) - asinh(tan(sin(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-195-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_195_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(sin(x)), 1, evaluate=False), Ne(sin(sin(x)), -1, evaluate=False), ~Q.zero(cos(sin(x))))
    Residual = atanh(sin(sin(x))) - asinh(tan(sin(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-195-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_195_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(sin(x)), 1, evaluate=False), Ne(sin(sin(x)), -1, evaluate=False), ~Q.zero(cos(sin(x))))
    Residual = atanh(sin(sin(x))) - asinh(tan(sin(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-195-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_195_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(sin(x)), 1, evaluate=False), Ne(sin(sin(x)), -1, evaluate=False), ~Q.zero(cos(sin(x))))
    Residual = atanh(sin(sin(x))) - asinh(tan(sin(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-195-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_195_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = atanh(sin(sin(x))) - asinh(tan(sin(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-195-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_195_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(sin(x)), 1, evaluate=False), Ne(sin(sin(x)), -1, evaluate=False), ~Q.zero(cos(sin(x))))
    Residual = atanh(sin(sin(x))) - asinh(tan(sin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-195-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_195_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(sin(x)), 1, evaluate=False), Ne(sin(sin(x)), -1, evaluate=False), ~Q.zero(cos(sin(x))))
    Residual = atanh(sin(sin(x))) - asinh(tan(sin(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-195-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_195_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(sin(x)), 1, evaluate=False), Ne(sin(sin(x)), -1, evaluate=False), ~Q.zero(cos(sin(x))))
    Residual = atanh(sin(sin(x))) - asinh(tan(sin(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-195-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_195_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = atanh(sin(sin(x))) - asinh(tan(sin(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-195-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_195_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(sin(x)), 1, evaluate=False), Ne(sin(sin(x)), -1, evaluate=False), ~Q.zero(cos(sin(x))))
    Residual = atanh(sin(sin(x))) - asinh(tan(sin(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-195-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_195_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(sin(x)), 1, evaluate=False), Ne(sin(sin(x)), -1, evaluate=False), ~Q.zero(cos(sin(x))))
    Residual = atanh(sin(sin(x))) - asinh(tan(sin(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-195-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_195_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(sin(x)), 1, evaluate=False), Ne(sin(sin(x)), -1, evaluate=False), ~Q.zero(cos(sin(x))))
    Residual = atanh(sin(sin(x))) - asinh(tan(sin(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-196-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_196_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
    Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-196-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_196_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
    Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-196-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_196_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
    Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-196-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_196_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
    Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-196-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_196_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-196-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_196_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
    Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-196-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_196_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
    Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-196-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_196_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
    Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-196-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_196_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-196-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_196_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
    Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-196-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_196_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
    Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-196-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_196_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
    Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-218-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered true (solved)
@_in(_SETUP1)
def sp_acj4_218_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-6 / x))
    Residual = 1 / (-6 / x) - (x / -6)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-218-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_218_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-6 / x))
    Residual = 1 / (-6 / x) - (x / -6)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-218-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered true (solved)
@_in(_SETUP2)
def sp_acj4_218_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-6 / x))
    Residual = 1 / (-6 / x) - (x / -6)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-218-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_218_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-6 / x))
    Residual = 1 / (-6 / x) - (x / -6)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-218-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_218_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = 1 / (-6 / x) - (x / -6)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-218-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered true (solved)
@_in(_SETUP3)
def sp_acj4_218_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-6 / x))
    Residual = 1 / (-6 / x) - (x / -6)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-218-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered true (solved)
@_in(_SETUP4)
def sp_acj4_218_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-6 / x))
    Residual = 1 / (-6 / x) - (x / -6)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-218-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered true (solved)
@_in(_SETUP3)
def sp_acj4_218_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-6 / x))
    Residual = 1 / (-6 / x) - (x / -6)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-218-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_218_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = 1 / (-6 / x) - (x / -6)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-218-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_218_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-6 / x))
    Residual = 1 / (-6 / x) - (x / -6)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-218-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_218_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-6 / x))
    Residual = 1 / (-6 / x) - (x / -6)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-218-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_218_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-6 / x))
    Residual = 1 / (-6 / x) - (x / -6)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_22_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_22_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_22_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_22_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_22_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_22_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_22_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_22_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_22_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_22_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_22_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_22_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-220-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered true (solved)
@_in(_SETUP1)
def sp_acj4_220_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-8 / x))
    Residual = 1 / (-8 / x) - (x / -8)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-220-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_220_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-8 / x))
    Residual = 1 / (-8 / x) - (x / -8)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-220-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered true (solved)
@_in(_SETUP2)
def sp_acj4_220_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-8 / x))
    Residual = 1 / (-8 / x) - (x / -8)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-220-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_220_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-8 / x))
    Residual = 1 / (-8 / x) - (x / -8)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-220-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_220_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = 1 / (-8 / x) - (x / -8)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-220-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered true (solved)
@_in(_SETUP3)
def sp_acj4_220_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-8 / x))
    Residual = 1 / (-8 / x) - (x / -8)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-220-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered true (solved)
@_in(_SETUP4)
def sp_acj4_220_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-8 / x))
    Residual = 1 / (-8 / x) - (x / -8)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-220-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered true (solved)
@_in(_SETUP3)
def sp_acj4_220_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-8 / x))
    Residual = 1 / (-8 / x) - (x / -8)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-220-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_220_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = 1 / (-8 / x) - (x / -8)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-220-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_220_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-8 / x))
    Residual = 1 / (-8 / x) - (x / -8)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-220-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_220_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-8 / x))
    Residual = 1 / (-8 / x) - (x / -8)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-220-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_220_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-8 / x))
    Residual = 1 / (-8 / x) - (x / -8)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-233-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered true (solved)
@_in(_SETUP1)
def sp_acj4_233_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)), Or(~Q.zero(x), re(-pi) > 0))
    Residual = 1 / Pow(x, pi) - Pow(x, -pi)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-233-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_233_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)), Or(~Q.zero(x), re(-pi) > 0))
    Residual = 1 / Pow(x, pi) - Pow(x, -pi)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-233-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered true (solved)
@_in(_SETUP2)
def sp_acj4_233_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)), Or(~Q.zero(x), re(-pi) > 0))
    Residual = 1 / Pow(x, pi) - Pow(x, -pi)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-233-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_233_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)), Or(~Q.zero(x), re(-pi) > 0))
    Residual = 1 / Pow(x, pi) - Pow(x, -pi)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-233-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_233_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = 1 / Pow(x, pi) - Pow(x, -pi)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-233-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered true (solved)
@_in(_SETUP3)
def sp_acj4_233_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)), Or(~Q.zero(x), re(-pi) > 0))
    Residual = 1 / Pow(x, pi) - Pow(x, -pi)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-233-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered true (solved)
@_in(_SETUP4)
def sp_acj4_233_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)), Or(~Q.zero(x), re(-pi) > 0))
    Residual = 1 / Pow(x, pi) - Pow(x, -pi)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-233-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered true (solved)
@_in(_SETUP3)
def sp_acj4_233_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)), Or(~Q.zero(x), re(-pi) > 0))
    Residual = 1 / Pow(x, pi) - Pow(x, -pi)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-233-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_233_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = 1 / Pow(x, pi) - Pow(x, -pi)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-233-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_233_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)), Or(~Q.zero(x), re(-pi) > 0))
    Residual = 1 / Pow(x, pi) - Pow(x, -pi)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-233-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_233_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)), Or(~Q.zero(x), re(-pi) > 0))
    Residual = 1 / Pow(x, pi) - Pow(x, -pi)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-233-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_233_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)), Or(~Q.zero(x), re(-pi) > 0))
    Residual = 1 / Pow(x, pi) - Pow(x, -pi)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-248-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_248_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asin(x)) - asin(-Abs(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-248-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_248_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asin(x)) - asin(-Abs(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-248-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_248_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asin(x)) - asin(-Abs(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-248-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_248_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asin(x)) - asin(-Abs(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-248-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_248_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = -Abs(asin(x)) - asin(-Abs(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-248-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_248_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asin(x)) - asin(-Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-248-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_248_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asin(x)) - asin(-Abs(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-248-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_248_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asin(x)) - asin(-Abs(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-248-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_248_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = -Abs(asin(x)) - asin(-Abs(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-248-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_248_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asin(x)) - asin(-Abs(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-248-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_248_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asin(x)) - asin(-Abs(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-248-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_248_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asin(x)) - asin(-Abs(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-249-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_249_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asinh(x)) - asinh(-Abs(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-249-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_249_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asinh(x)) - asinh(-Abs(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-249-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_249_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asinh(x)) - asinh(-Abs(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-249-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_249_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asinh(x)) - asinh(-Abs(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-249-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_249_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = -Abs(asinh(x)) - asinh(-Abs(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-249-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_249_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asinh(x)) - asinh(-Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-249-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_249_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asinh(x)) - asinh(-Abs(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-249-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_249_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asinh(x)) - asinh(-Abs(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-249-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_249_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = -Abs(asinh(x)) - asinh(-Abs(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-249-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_249_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asinh(x)) - asinh(-Abs(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-249-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_249_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asinh(x)) - asinh(-Abs(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-249-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_249_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(asinh(x)) - asinh(-Abs(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-251-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_251_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
    Residual = -Abs(atanh(x)) - atanh(-Abs(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-251-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_251_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
    Residual = -Abs(atanh(x)) - atanh(-Abs(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-251-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_251_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
    Residual = -Abs(atanh(x)) - atanh(-Abs(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-251-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_251_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
    Residual = -Abs(atanh(x)) - atanh(-Abs(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-251-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_251_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = -Abs(atanh(x)) - atanh(-Abs(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-251-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_251_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
    Residual = -Abs(atanh(x)) - atanh(-Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-251-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_251_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
    Residual = -Abs(atanh(x)) - atanh(-Abs(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-251-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_251_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
    Residual = -Abs(atanh(x)) - atanh(-Abs(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-251-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_251_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = -Abs(atanh(x)) - atanh(-Abs(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-251-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_251_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
    Residual = -Abs(atanh(x)) - atanh(-Abs(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-251-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_251_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
    Residual = -Abs(atanh(x)) - atanh(-Abs(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-251-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_251_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
    Residual = -Abs(atanh(x)) - atanh(-Abs(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_252_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_252_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_252_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_252_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_252_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_252_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_252_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_252_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_252_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_252_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_252_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_252_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_253_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_253_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_253_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_253_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_253_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_253_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_253_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_253_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_253_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_253_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_253_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_253_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-256-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered true (solved)
@_in(_SETUP1)
def sp_acj4_256_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(-exp(x)))
    Residual = -exp(-x) - (1 / -exp(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-256-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_256_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(-exp(x)))
    Residual = -exp(-x) - (1 / -exp(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-256-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered true (solved)
@_in(_SETUP2)
def sp_acj4_256_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(-exp(x)))
    Residual = -exp(-x) - (1 / -exp(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-256-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_256_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(-exp(x)))
    Residual = -exp(-x) - (1 / -exp(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-256-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_256_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = -exp(-x) - (1 / -exp(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-256-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered true (solved)
@_in(_SETUP3)
def sp_acj4_256_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(-exp(x)))
    Residual = -exp(-x) - (1 / -exp(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-256-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered true (solved)
@_in(_SETUP4)
def sp_acj4_256_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(-exp(x)))
    Residual = -exp(-x) - (1 / -exp(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-256-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered true (solved)
@_in(_SETUP3)
def sp_acj4_256_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(-exp(x)))
    Residual = -exp(-x) - (1 / -exp(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-256-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_256_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = -exp(-x) - (1 / -exp(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-256-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_256_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(-exp(x)))
    Residual = -exp(-x) - (1 / -exp(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-256-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_256_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(-exp(x)))
    Residual = -exp(-x) - (1 / -exp(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-256-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_256_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(-exp(x)))
    Residual = -exp(-x) - (1 / -exp(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-275-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_275_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -3) - Abs(Pow(x, -3))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-275-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_275_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -3) - Abs(Pow(x, -3))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-275-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_275_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -3) - Abs(Pow(x, -3))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-275-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_275_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -3) - Abs(Pow(x, -3))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-275-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_275_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = Pow(Abs(x), -3) - Abs(Pow(x, -3))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-275-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_275_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -3) - Abs(Pow(x, -3))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-275-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_275_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -3) - Abs(Pow(x, -3))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-275-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_275_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -3) - Abs(Pow(x, -3))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-275-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_275_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = Pow(Abs(x), -3) - Abs(Pow(x, -3))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-275-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_275_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -3) - Abs(Pow(x, -3))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-275-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_275_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -3) - Abs(Pow(x, -3))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-275-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_275_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -3) - Abs(Pow(x, -3))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-276-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_276_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -4) - Pow(x, -4)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-276-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_276_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -4) - Pow(x, -4)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-276-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_276_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -4) - Pow(x, -4)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-276-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_276_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -4) - Pow(x, -4)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-276-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_276_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = Pow(Abs(x), -4) - Pow(x, -4)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-276-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_276_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -4) - Pow(x, -4)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-276-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_276_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -4) - Pow(x, -4)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-276-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered true (solved)
@_in(_SETUP3)
def sp_acj4_276_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -4) - Pow(x, -4)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-276-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_276_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = Pow(Abs(x), -4) - Pow(x, -4)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-276-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_276_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -4) - Pow(x, -4)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-276-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_276_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -4) - Pow(x, -4)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-276-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_276_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -4) - Pow(x, -4)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_283_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_283_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_283_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_283_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_283_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = Pow(Abs(x), 2) - (x * x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_283_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_283_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered true (solved)
@_in(_SETUP3)
def sp_acj4_283_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_283_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = Pow(Abs(x), 2) - (x * x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_283_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_283_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_283_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-286-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_286_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 5) - Abs(Pow(x, 5))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-286-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_286_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 5) - Abs(Pow(x, 5))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-286-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_286_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 5) - Abs(Pow(x, 5))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-286-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_286_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 5) - Abs(Pow(x, 5))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-286-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_286_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = Pow(Abs(x), 5) - Abs(Pow(x, 5))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-286-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_286_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 5) - Abs(Pow(x, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-286-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_286_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 5) - Abs(Pow(x, 5))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-286-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_286_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 5) - Abs(Pow(x, 5))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-286-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_286_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = Pow(Abs(x), 5) - Abs(Pow(x, 5))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-286-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_286_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 5) - Abs(Pow(x, 5))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-286-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_286_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 5) - Abs(Pow(x, 5))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-286-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_286_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 5) - Abs(Pow(x, 5))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-289-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_289_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 8) - Pow(x, 8)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-289-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_289_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 8) - Pow(x, 8)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-289-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_289_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 8) - Pow(x, 8)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-289-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_289_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 8) - Pow(x, 8)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-289-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_289_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = Pow(Abs(x), 8) - Pow(x, 8)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-289-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_289_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 8) - Pow(x, 8)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-289-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_289_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 8) - Pow(x, 8)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-289-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered true (solved)
@_in(_SETUP3)
def sp_acj4_289_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 8) - Pow(x, 8)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-289-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_289_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = Pow(Abs(x), 8) - Pow(x, 8)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-289-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_289_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 8) - Pow(x, 8)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-289-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_289_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 8) - Pow(x, 8)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-289-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_289_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 8) - Pow(x, 8)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-31-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered true (solved)
@_in(_SETUP1)
def sp_acj4_31_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 5 * Abs(x) - Abs(-5 * x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-31-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_31_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 5 * Abs(x) - Abs(-5 * x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-31-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered true (solved)
@_in(_SETUP2)
def sp_acj4_31_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 5 * Abs(x) - Abs(-5 * x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-31-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_31_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 5 * Abs(x) - Abs(-5 * x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-31-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_31_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = 5 * Abs(x) - Abs(-5 * x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-31-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered true (solved)
@_in(_SETUP3)
def sp_acj4_31_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 5 * Abs(x) - Abs(-5 * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-31-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered true (solved)
@_in(_SETUP4)
def sp_acj4_31_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 5 * Abs(x) - Abs(-5 * x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-31-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered true (solved)
@_in(_SETUP3)
def sp_acj4_31_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 5 * Abs(x) - Abs(-5 * x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-31-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_31_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = 5 * Abs(x) - Abs(-5 * x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-31-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_31_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 5 * Abs(x) - Abs(-5 * x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-31-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_31_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 5 * Abs(x) - Abs(-5 * x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-31-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_31_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 5 * Abs(x) - Abs(-5 * x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-326-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered true (solved)
@_in(_SETUP1)
def sp_acj4_326_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(exp(x), 2) - exp(2 * x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-326-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_326_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(exp(x), 2) - exp(2 * x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-326-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered true (solved)
@_in(_SETUP2)
def sp_acj4_326_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(exp(x), 2) - exp(2 * x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-326-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_326_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(exp(x), 2) - exp(2 * x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-326-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_326_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = Pow(exp(x), 2) - exp(2 * x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-326-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered true (solved)
@_in(_SETUP3)
def sp_acj4_326_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(exp(x), 2) - exp(2 * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-326-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered true (solved)
@_in(_SETUP4)
def sp_acj4_326_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(exp(x), 2) - exp(2 * x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-326-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered true (solved)
@_in(_SETUP3)
def sp_acj4_326_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(exp(x), 2) - exp(2 * x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-326-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_326_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = Pow(exp(x), 2) - exp(2 * x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-326-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_326_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(exp(x), 2) - exp(2 * x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-326-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_326_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(exp(x), 2) - exp(2 * x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-326-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_326_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Pow(exp(x), 2) - exp(2 * x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-33-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered true (solved)
@_in(_SETUP1)
def sp_acj4_33_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 6 * Abs(x) - Abs(-6 * x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-33-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_33_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 6 * Abs(x) - Abs(-6 * x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-33-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered true (solved)
@_in(_SETUP2)
def sp_acj4_33_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 6 * Abs(x) - Abs(-6 * x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-33-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_33_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 6 * Abs(x) - Abs(-6 * x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-33-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_33_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = 6 * Abs(x) - Abs(-6 * x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-33-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered true (solved)
@_in(_SETUP3)
def sp_acj4_33_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 6 * Abs(x) - Abs(-6 * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-33-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered true (solved)
@_in(_SETUP4)
def sp_acj4_33_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 6 * Abs(x) - Abs(-6 * x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-33-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered true (solved)
@_in(_SETUP3)
def sp_acj4_33_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 6 * Abs(x) - Abs(-6 * x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-33-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_33_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = 6 * Abs(x) - Abs(-6 * x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-33-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_33_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 6 * Abs(x) - Abs(-6 * x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-33-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_33_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 6 * Abs(x) - Abs(-6 * x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-33-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_33_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = 6 * Abs(x) - Abs(-6 * x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-35-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_35_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 7)))
    Residual = 7 * log(x) - log(Pow(x, 7))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-35-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_35_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 7)))
    Residual = 7 * log(x) - log(Pow(x, 7))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-35-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_35_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 7)))
    Residual = 7 * log(x) - log(Pow(x, 7))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-35-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_35_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 7)))
    Residual = 7 * log(x) - log(Pow(x, 7))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-35-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_35_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = 7 * log(x) - log(Pow(x, 7))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-35-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_35_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 7)))
    Residual = 7 * log(x) - log(Pow(x, 7))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-35-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_35_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 7)))
    Residual = 7 * log(x) - log(Pow(x, 7))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-35-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_35_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 7)))
    Residual = 7 * log(x) - log(Pow(x, 7))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-35-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_35_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = 7 * log(x) - log(Pow(x, 7))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-35-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_35_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 7)))
    Residual = 7 * log(x) - log(Pow(x, 7))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-35-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_35_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 7)))
    Residual = 7 * log(x) - log(Pow(x, 7))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-35-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_35_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 7)))
    Residual = 7 * log(x) - log(Pow(x, 7))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-354-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_354_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(5)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(5)) - Pow(5, log(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-354-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_354_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(5)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(5)) - Pow(5, log(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-354-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_354_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(5)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(5)) - Pow(5, log(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-354-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_354_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(5)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(5)) - Pow(5, log(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-354-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_354_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = Pow(x, log(5)) - Pow(5, log(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-354-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_354_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(5)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(5)) - Pow(5, log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-354-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_354_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(5)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(5)) - Pow(5, log(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-354-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_354_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(5)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(5)) - Pow(5, log(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-354-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_354_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = Pow(x, log(5)) - Pow(5, log(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-354-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_354_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(5)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(5)) - Pow(5, log(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-354-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_354_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(5)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(5)) - Pow(5, log(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-354-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_354_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(5)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(5)) - Pow(5, log(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-356-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_356_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(7)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(7)) - Pow(7, log(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-356-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_356_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(7)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(7)) - Pow(7, log(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-356-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_356_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(7)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(7)) - Pow(7, log(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-356-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_356_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(7)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(7)) - Pow(7, log(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-356-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_356_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = Pow(x, log(7)) - Pow(7, log(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-356-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_356_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(7)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(7)) - Pow(7, log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-356-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_356_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(7)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(7)) - Pow(7, log(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-356-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_356_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(7)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(7)) - Pow(7, log(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-356-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_356_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = Pow(x, log(7)) - Pow(7, log(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-356-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_356_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(7)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(7)) - Pow(7, log(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-356-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_356_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(7)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(7)) - Pow(7, log(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-356-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_356_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(7)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(7)) - Pow(7, log(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-359-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_359_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(pi)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(pi)) - Pow(pi, log(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-359-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_359_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(pi)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(pi)) - Pow(pi, log(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-359-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_359_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(pi)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(pi)) - Pow(pi, log(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-359-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_359_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(pi)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(pi)) - Pow(pi, log(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-359-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_359_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = Pow(x, log(pi)) - Pow(pi, log(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-359-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_359_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(pi)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(pi)) - Pow(pi, log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-359-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_359_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(pi)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(pi)) - Pow(pi, log(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-359-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_359_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(pi)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(pi)) - Pow(pi, log(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-359-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_359_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = Pow(x, log(pi)) - Pow(pi, log(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-359-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_359_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(pi)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(pi)) - Pow(pi, log(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-359-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_359_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(pi)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(pi)) - Pow(pi, log(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-359-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_359_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(pi)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(pi)) - Pow(pi, log(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-364-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_364_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 3) - Abs(real_root(x, 3))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-364-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_364_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 3) - Abs(real_root(x, 3))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-364-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_364_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 3) - Abs(real_root(x, 3))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-364-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_364_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 3) - Abs(real_root(x, 3))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-364-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_364_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = real_root(Abs(x), 3) - Abs(real_root(x, 3))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-364-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_364_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 3) - Abs(real_root(x, 3))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-364-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_364_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 3) - Abs(real_root(x, 3))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-364-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_364_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 3) - Abs(real_root(x, 3))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-364-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_364_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = real_root(Abs(x), 3) - Abs(real_root(x, 3))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-364-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_364_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 3) - Abs(real_root(x, 3))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-364-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_364_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 3) - Abs(real_root(x, 3))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-364-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_364_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 3) - Abs(real_root(x, 3))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-367-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_367_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 9) - Abs(real_root(x, 9))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-367-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_367_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 9) - Abs(real_root(x, 9))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-367-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_367_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 9) - Abs(real_root(x, 9))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-367-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_367_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 9) - Abs(real_root(x, 9))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-367-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_367_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = real_root(Abs(x), 9) - Abs(real_root(x, 9))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-367-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_367_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 9) - Abs(real_root(x, 9))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-367-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_367_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 9) - Abs(real_root(x, 9))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-367-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_367_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 9) - Abs(real_root(x, 9))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-367-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_367_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = real_root(Abs(x), 9) - Abs(real_root(x, 9))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-367-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_367_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 9) - Abs(real_root(x, 9))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-367-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_367_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 9) - Abs(real_root(x, 9))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-367-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_367_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 9) - Abs(real_root(x, 9))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_368_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_368_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_368_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_368_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_368_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_368_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_368_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_368_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_368_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_368_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_368_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_368_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_369_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_369_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_369_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_369_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_369_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_369_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_369_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_369_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_369_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_369_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_369_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_369_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_370_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_370_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_370_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_370_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_370_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_370_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_370_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_370_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_370_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_370_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_370_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_370_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_371_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_371_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_371_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_371_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_371_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_371_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_371_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_371_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_371_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_371_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_371_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_371_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_372_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_372_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_372_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_372_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_372_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_372_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_372_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_372_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_372_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_372_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_372_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_372_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_373_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_373_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_373_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_373_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_373_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_373_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_373_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_373_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_373_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_373_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_373_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_373_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-38-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_38_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 9)))
    Residual = 9 * log(x) - log(Pow(x, 9))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-38-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_38_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 9)))
    Residual = 9 * log(x) - log(Pow(x, 9))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-38-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_38_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 9)))
    Residual = 9 * log(x) - log(Pow(x, 9))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-38-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_38_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 9)))
    Residual = 9 * log(x) - log(Pow(x, 9))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-38-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_38_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = 9 * log(x) - log(Pow(x, 9))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-38-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_38_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 9)))
    Residual = 9 * log(x) - log(Pow(x, 9))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-38-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_38_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 9)))
    Residual = 9 * log(x) - log(Pow(x, 9))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-38-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_38_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 9)))
    Residual = 9 * log(x) - log(Pow(x, 9))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-38-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_38_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = 9 * log(x) - log(Pow(x, 9))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-38-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_38_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 9)))
    Residual = 9 * log(x) - log(Pow(x, 9))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-38-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_38_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 9)))
    Residual = 9 * log(x) - log(Pow(x, 9))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-38-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_38_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 9)))
    Residual = 9 * log(x) - log(Pow(x, 9))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-394-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_394_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-394-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_394_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-394-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_394_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-394-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_394_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-394-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_394_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-394-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_394_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-394-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_394_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-394-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_394_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-394-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_394_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-394-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_394_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-394-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_394_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-394-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_394_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-395-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_395_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-395-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_395_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-395-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_395_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-395-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_395_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-395-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_395_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-395-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_395_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-395-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_395_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-395-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_395_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-395-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_395_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-395-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_395_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-395-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_395_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-395-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_395_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_396_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_396_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_396_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_396_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_396_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_396_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_396_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_396_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_396_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_396_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_396_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_396_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-397-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_397_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(tanh(x))) - Abs(sin(tanh(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-397-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_397_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(tanh(x))) - Abs(sin(tanh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-397-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_397_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(tanh(x))) - Abs(sin(tanh(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-397-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_397_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(tanh(x))) - Abs(sin(tanh(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-397-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_397_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = sin(Abs(tanh(x))) - Abs(sin(tanh(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-397-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_397_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(tanh(x))) - Abs(sin(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-397-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_397_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(tanh(x))) - Abs(sin(tanh(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-397-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_397_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(tanh(x))) - Abs(sin(tanh(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-397-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_397_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = sin(Abs(tanh(x))) - Abs(sin(tanh(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-397-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_397_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(tanh(x))) - Abs(sin(tanh(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-397-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_397_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(tanh(x))) - Abs(sin(tanh(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-397-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_397_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(Abs(tanh(x))) - Abs(sin(tanh(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-402-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_402_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-402-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_402_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-402-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_402_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-402-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_402_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-402-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_402_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-402-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_402_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-402-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_402_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-402-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_402_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-402-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_402_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-402-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_402_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-402-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_402_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-402-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_402_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_404_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_404_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_404_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_404_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_404_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_404_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_404_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_404_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_404_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_404_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_404_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_404_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-412-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_412_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-412-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_412_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-412-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_412_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-412-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_412_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-412-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_412_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-412-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_412_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-412-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_412_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-412-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_412_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-412-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_412_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-412-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_412_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-412-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_412_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-412-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_412_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-413-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_413_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(cos(x)))), ~Q.zero(cos(cos(x))))
    Residual = tan(Abs(cos(x))) - Abs(tan(cos(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-413-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_413_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(cos(x)))), ~Q.zero(cos(cos(x))))
    Residual = tan(Abs(cos(x))) - Abs(tan(cos(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-413-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_413_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(cos(x)))), ~Q.zero(cos(cos(x))))
    Residual = tan(Abs(cos(x))) - Abs(tan(cos(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-413-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_413_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(cos(x)))), ~Q.zero(cos(cos(x))))
    Residual = tan(Abs(cos(x))) - Abs(tan(cos(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-413-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_413_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = tan(Abs(cos(x))) - Abs(tan(cos(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-413-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_413_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(cos(x)))), ~Q.zero(cos(cos(x))))
    Residual = tan(Abs(cos(x))) - Abs(tan(cos(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-413-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_413_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(cos(x)))), ~Q.zero(cos(cos(x))))
    Residual = tan(Abs(cos(x))) - Abs(tan(cos(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-413-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_413_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(cos(x)))), ~Q.zero(cos(cos(x))))
    Residual = tan(Abs(cos(x))) - Abs(tan(cos(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-413-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_413_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = tan(Abs(cos(x))) - Abs(tan(cos(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-413-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_413_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(cos(x)))), ~Q.zero(cos(cos(x))))
    Residual = tan(Abs(cos(x))) - Abs(tan(cos(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-413-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_413_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(cos(x)))), ~Q.zero(cos(cos(x))))
    Residual = tan(Abs(cos(x))) - Abs(tan(cos(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-413-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_413_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(cos(x)))), ~Q.zero(cos(cos(x))))
    Residual = tan(Abs(cos(x))) - Abs(tan(cos(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_414_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_414_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_414_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_414_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_414_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_414_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_414_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_414_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_414_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_414_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_414_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_414_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_415_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_415_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_415_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_415_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_415_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_415_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_415_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_415_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_415_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_415_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_415_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_415_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-417-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_417_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(asin(Abs(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-417-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_417_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(asin(Abs(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-417-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_417_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(asin(Abs(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-417-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_417_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(asin(Abs(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-417-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_417_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-417-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_417_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(asin(Abs(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-417-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_417_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(asin(Abs(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-417-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_417_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(asin(Abs(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-417-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_417_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-417-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_417_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(asin(Abs(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_421_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_421_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_421_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (no verdict)
@_in(_SETUP2)
def sp_acj4_421_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_421_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_421_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (no verdict)
@_in(_SETUP4)
def sp_acj4_421_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_421_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (no verdict)
@_in(_SETUP3)
def sp_acj4_421_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_421_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_421_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (no verdict)
@_in(_SETUP5)
def sp_acj4_421_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5-real · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_5_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = atanh(Abs(x)) - Abs(atanh(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5-real · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_5_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = atanh(Abs(x)) - Abs(atanh(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5-real · expected contingent · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_5_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = atanh(Abs(x)) - Abs(atanh(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5-real · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
@_in(_SETUP2)
def sp_acj4_5_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = atanh(Abs(x)) - Abs(atanh(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5-real · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_5_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = atanh(Abs(x)) - Abs(atanh(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_5_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = atanh(Abs(x)) - Abs(atanh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5-real · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_5_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = atanh(Abs(x)) - Abs(atanh(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5-real · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_5_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = atanh(Abs(x)) - Abs(atanh(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5-real · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_5_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = atanh(Abs(x)) - Abs(atanh(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5-real · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_5_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = atanh(Abs(x)) - Abs(atanh(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5-real · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_5_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = atanh(Abs(x)) - Abs(atanh(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5-real · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_5_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = atanh(Abs(x)) - Abs(atanh(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-73-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered true (solved)
@_in(_SETUP1)
def sp_acj4_73_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(-Abs(x)))
    Residual = -1 / Abs(x) - (1 / -Abs(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-73-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_73_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(-Abs(x)))
    Residual = -1 / Abs(x) - (1 / -Abs(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-73-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered true (solved)
@_in(_SETUP2)
def sp_acj4_73_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(-Abs(x)))
    Residual = -1 / Abs(x) - (1 / -Abs(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-73-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_73_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(-Abs(x)))
    Residual = -1 / Abs(x) - (1 / -Abs(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-73-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_73_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = -1 / Abs(x) - (1 / -Abs(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-73-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered true (solved)
@_in(_SETUP3)
def sp_acj4_73_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(-Abs(x)))
    Residual = -1 / Abs(x) - (1 / -Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-73-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered true (solved)
@_in(_SETUP4)
def sp_acj4_73_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(-Abs(x)))
    Residual = -1 / Abs(x) - (1 / -Abs(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-73-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered true (solved)
@_in(_SETUP3)
def sp_acj4_73_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(-Abs(x)))
    Residual = -1 / Abs(x) - (1 / -Abs(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-73-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_73_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = -1 / Abs(x) - (1 / -Abs(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-73-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_73_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(-Abs(x)))
    Residual = -1 / Abs(x) - (1 / -Abs(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-73-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_73_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(-Abs(x)))
    Residual = -1 / Abs(x) - (1 / -Abs(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-73-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_73_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(-Abs(x)))
    Residual = -1 / Abs(x) - (1 / -Abs(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-80-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered true (solved)
@_in(_SETUP1)
def sp_acj4_80_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(-cos(x)))
    Residual = -1 / cos(x) - (1 / -cos(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-80-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_80_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(-cos(x)))
    Residual = -1 / cos(x) - (1 / -cos(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-80-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered true (solved)
@_in(_SETUP2)
def sp_acj4_80_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(-cos(x)))
    Residual = -1 / cos(x) - (1 / -cos(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-80-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_80_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(-cos(x)))
    Residual = -1 / cos(x) - (1 / -cos(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-80-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_80_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = -1 / cos(x) - (1 / -cos(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-80-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered true (solved)
@_in(_SETUP3)
def sp_acj4_80_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(-cos(x)))
    Residual = -1 / cos(x) - (1 / -cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-80-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered true (solved)
@_in(_SETUP4)
def sp_acj4_80_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(-cos(x)))
    Residual = -1 / cos(x) - (1 / -cos(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-80-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered true (solved)
@_in(_SETUP3)
def sp_acj4_80_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(-cos(x)))
    Residual = -1 / cos(x) - (1 / -cos(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-80-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_80_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = -1 / cos(x) - (1 / -cos(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-80-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_80_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(-cos(x)))
    Residual = -1 / cos(x) - (1 / -cos(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-80-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_80_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(-cos(x)))
    Residual = -1 / cos(x) - (1 / -cos(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-80-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_80_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(-cos(x)))
    Residual = -1 / cos(x) - (1 / -cos(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-83-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered true (solved)
@_in(_SETUP1)
def sp_acj4_83_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(-log(x)))
    Residual = -1 / log(x) - (1 / -log(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-83-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_83_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(-log(x)))
    Residual = -1 / log(x) - (1 / -log(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-83-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered true (solved)
@_in(_SETUP2)
def sp_acj4_83_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(-log(x)))
    Residual = -1 / log(x) - (1 / -log(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-83-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_83_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(-log(x)))
    Residual = -1 / log(x) - (1 / -log(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-83-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_83_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = -1 / log(x) - (1 / -log(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-83-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered true (solved)
@_in(_SETUP3)
def sp_acj4_83_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(-log(x)))
    Residual = -1 / log(x) - (1 / -log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-83-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered true (solved)
@_in(_SETUP4)
def sp_acj4_83_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(-log(x)))
    Residual = -1 / log(x) - (1 / -log(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-83-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered true (solved)
@_in(_SETUP3)
def sp_acj4_83_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(-log(x)))
    Residual = -1 / log(x) - (1 / -log(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-83-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_83_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = -1 / log(x) - (1 / -log(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-83-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_83_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(-log(x)))
    Residual = -1 / log(x) - (1 / -log(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-83-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_83_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(-log(x)))
    Residual = -1 / log(x) - (1 / -log(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-83-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_83_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(-log(x)))
    Residual = -1 / log(x) - (1 / -log(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-86-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered true (solved)
@_in(_SETUP1)
def sp_acj4_86_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(tan(x)), ~Q.zero(-tan(x)))
    Residual = -1 / tan(x) - (1 / -tan(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-86-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_86_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(tan(x)), ~Q.zero(-tan(x)))
    Residual = -1 / tan(x) - (1 / -tan(x))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-86-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered true (solved)
@_in(_SETUP2)
def sp_acj4_86_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(tan(x)), ~Q.zero(-tan(x)))
    Residual = -1 / tan(x) - (1 / -tan(x))
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-86-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_86_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(tan(x)), ~Q.zero(-tan(x)))
    Residual = -1 / tan(x) - (1 / -tan(x))
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-86-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_86_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = -1 / tan(x) - (1 / -tan(x))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-86-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered true (solved)
@_in(_SETUP3)
def sp_acj4_86_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(tan(x)), ~Q.zero(-tan(x)))
    Residual = -1 / tan(x) - (1 / -tan(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-86-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered true (solved)
@_in(_SETUP4)
def sp_acj4_86_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(tan(x)), ~Q.zero(-tan(x)))
    Residual = -1 / tan(x) - (1 / -tan(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-86-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered true (solved)
@_in(_SETUP3)
def sp_acj4_86_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(tan(x)), ~Q.zero(-tan(x)))
    Residual = -1 / tan(x) - (1 / -tan(x))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-86-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_86_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = -1 / tan(x) - (1 / -tan(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-86-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_86_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(tan(x)), ~Q.zero(-tan(x)))
    Residual = -1 / tan(x) - (1 / -tan(x))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-86-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_86_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(tan(x)), ~Q.zero(-tan(x)))
    Residual = -1 / tan(x) - (1 / -tan(x))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-86-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_86_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(tan(x)), ~Q.zero(-tan(x)))
    Residual = -1 / tan(x) - (1 / -tan(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered true (solved)
@_in(_SETUP1)
def sp_acj4_90_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_90_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered true (solved)
@_in(_SETUP2)
def sp_acj4_90_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_90_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_90_real__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered true (solved)
@_in(_SETUP3)
def sp_acj4_90_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered true (solved)
@_in(_SETUP4)
def sp_acj4_90_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered true (solved)
@_in(_SETUP3)
def sp_acj4_90_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_90_real__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_90_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_90_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_90_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-real · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered true (solved)
@_in(_SETUP1)
def sp_acj4_99_real__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-real · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered true (solved)
@_in(_SETUP2)
def sp_acj4_99_real__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-real · expected true · system satsimp-trigsimp (satsimp 0.1.0)
# the run satsimp-trigsimp-20261020-065212 answered true (solved)
@_in(_SETUP2)
def sp_acj4_99_real__satsimp_trigsimp():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Result = satsimp.trigsimp(Residual, Assum, strict=True)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-real · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261020-065134 answered true (solved)
@_in(_SETUP2)
def sp_acj4_99_real__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Result = simplify(satsimp.refine(Residual, Assum, strict=True))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-real · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261020-064252 answered true (solved)
@_in(_SETUP3)
def sp_acj4_99_real__sympy_auto():
    x = Symbol('x', real=True)
    Residual = Abs(x) / 3 - Abs(x / -3)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered true (solved)
@_in(_SETUP3)
def sp_acj4_99_real__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-real · expected true · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261019-221849 answered true (solved)
@_in(_SETUP4)
def sp_acj4_99_real__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-real · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered true (solved)
@_in(_SETUP3)
def sp_acj4_99_real__sympy_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-real · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261020-064757 answered true (solved)
@_in(_SETUP3)
def sp_acj4_99_real__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = Abs(x) / 3 - Abs(x / -3)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-real · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered true (solved)
@_in(_SETUP5)
def sp_acj4_99_real__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-real · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered true (solved)
@_in(_SETUP5)
def sp_acj4_99_real__sympy_extras_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-real · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261020-070552 answered true (solved)
@_in(_SETUP5)
def sp_acj4_99_real__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# (case, system, expected, the stored run's answer, that run, its function)
CASES = [
    ('sp-acj4-1-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_1_real__satassume_ask),
    ('sp-acj4-1-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_1_real__satrefine_refine),
    ('sp-acj4-1-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_1_real__satsimp_trigsimp),
    ('sp-acj4-1-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_1_real__satrefine_simplify),
    ('sp-acj4-1-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_1_real__sympy_auto),
    ('sp-acj4-1-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_1_real__sympy_ask),
    ('sp-acj4-1-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261019-221849', sp_acj4_1_real__sympy_satask),
    ('sp-acj4-1-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_1_real__sympy_refine),
    ('sp-acj4-1-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_1_real__sympy_simplify),
    ('sp-acj4-1-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_1_real__sympy_extras_ask),
    ('sp-acj4-1-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_1_real__sympy_extras_refine),
    ('sp-acj4-1-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_1_real__sympy_extras_simplify),
    ('sp-acj4-102-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261020-065124', sp_acj4_102_real__satassume_ask),
    ('sp-acj4-102-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_102_real__satrefine_refine),
    ('sp-acj4-102-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261020-065212', sp_acj4_102_real__satsimp_trigsimp),
    ('sp-acj4-102-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_102_real__satrefine_simplify),
    ('sp-acj4-102-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_102_real__sympy_auto),
    ('sp-acj4-102-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261020-064258', sp_acj4_102_real__sympy_ask),
    ('sp-acj4-102-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261019-221849', sp_acj4_102_real__sympy_satask),
    ('sp-acj4-102-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261020-064447', sp_acj4_102_real__sympy_refine),
    ('sp-acj4-102-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_102_real__sympy_simplify),
    ('sp-acj4-102-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_102_real__sympy_extras_ask),
    ('sp-acj4-102-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_102_real__sympy_extras_refine),
    ('sp-acj4-102-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_102_real__sympy_extras_simplify),
    ('sp-acj4-108-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_108_real__satassume_ask),
    ('sp-acj4-108-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_108_real__satrefine_refine),
    ('sp-acj4-108-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_108_real__satsimp_trigsimp),
    ('sp-acj4-108-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_108_real__satrefine_simplify),
    ('sp-acj4-108-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_108_real__sympy_auto),
    ('sp-acj4-108-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_108_real__sympy_ask),
    ('sp-acj4-108-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_108_real__sympy_satask),
    ('sp-acj4-108-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_108_real__sympy_refine),
    ('sp-acj4-108-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_108_real__sympy_simplify),
    ('sp-acj4-108-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_108_real__sympy_extras_ask),
    ('sp-acj4-108-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_108_real__sympy_extras_refine),
    ('sp-acj4-108-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_108_real__sympy_extras_simplify),
    ('sp-acj4-120-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261020-065124', sp_acj4_120_real__satassume_ask),
    ('sp-acj4-120-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_120_real__satrefine_refine),
    ('sp-acj4-120-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261020-065212', sp_acj4_120_real__satsimp_trigsimp),
    ('sp-acj4-120-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_120_real__satrefine_simplify),
    ('sp-acj4-120-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_120_real__sympy_auto),
    ('sp-acj4-120-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261020-064258', sp_acj4_120_real__sympy_ask),
    ('sp-acj4-120-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261019-221849', sp_acj4_120_real__sympy_satask),
    ('sp-acj4-120-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261020-064447', sp_acj4_120_real__sympy_refine),
    ('sp-acj4-120-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_120_real__sympy_simplify),
    ('sp-acj4-120-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_120_real__sympy_extras_ask),
    ('sp-acj4-120-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_120_real__sympy_extras_refine),
    ('sp-acj4-120-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_120_real__sympy_extras_simplify),
    ('sp-acj4-127-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_127_real__satassume_ask),
    ('sp-acj4-127-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_127_real__satrefine_refine),
    ('sp-acj4-127-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_127_real__satsimp_trigsimp),
    ('sp-acj4-127-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_127_real__satrefine_simplify),
    ('sp-acj4-127-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_127_real__sympy_auto),
    ('sp-acj4-127-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_127_real__sympy_ask),
    ('sp-acj4-127-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261019-221849', sp_acj4_127_real__sympy_satask),
    ('sp-acj4-127-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_127_real__sympy_refine),
    ('sp-acj4-127-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_127_real__sympy_simplify),
    ('sp-acj4-127-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_127_real__sympy_extras_ask),
    ('sp-acj4-128-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_128_real__satassume_ask),
    ('sp-acj4-128-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_128_real__satrefine_refine),
    ('sp-acj4-128-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_128_real__satsimp_trigsimp),
    ('sp-acj4-128-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_128_real__satrefine_simplify),
    ('sp-acj4-128-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_128_real__sympy_auto),
    ('sp-acj4-128-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_128_real__sympy_ask),
    ('sp-acj4-128-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261019-221849', sp_acj4_128_real__sympy_satask),
    ('sp-acj4-128-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_128_real__sympy_refine),
    ('sp-acj4-128-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_128_real__sympy_simplify),
    ('sp-acj4-128-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_128_real__sympy_extras_ask),
    ('sp-acj4-128-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_128_real__sympy_extras_refine),
    ('sp-acj4-128-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_128_real__sympy_extras_simplify),
    ('sp-acj4-131-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_131_real__satassume_ask),
    ('sp-acj4-131-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_131_real__satrefine_refine),
    ('sp-acj4-131-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_131_real__satsimp_trigsimp),
    ('sp-acj4-131-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_131_real__satrefine_simplify),
    ('sp-acj4-131-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_131_real__sympy_auto),
    ('sp-acj4-131-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_131_real__sympy_ask),
    ('sp-acj4-131-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_131_real__sympy_satask),
    ('sp-acj4-131-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_131_real__sympy_refine),
    ('sp-acj4-131-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_131_real__sympy_simplify),
    ('sp-acj4-131-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_131_real__sympy_extras_ask),
    ('sp-acj4-131-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_131_real__sympy_extras_refine),
    ('sp-acj4-131-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_131_real__sympy_extras_simplify),
    ('sp-acj4-132-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_132_real__satassume_ask),
    ('sp-acj4-132-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_132_real__satrefine_refine),
    ('sp-acj4-132-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_132_real__satsimp_trigsimp),
    ('sp-acj4-132-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_132_real__satrefine_simplify),
    ('sp-acj4-132-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_132_real__sympy_auto),
    ('sp-acj4-132-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_132_real__sympy_ask),
    ('sp-acj4-132-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261019-221849', sp_acj4_132_real__sympy_satask),
    ('sp-acj4-132-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_132_real__sympy_refine),
    ('sp-acj4-132-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_132_real__sympy_simplify),
    ('sp-acj4-132-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_132_real__sympy_extras_ask),
    ('sp-acj4-132-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_132_real__sympy_extras_refine),
    ('sp-acj4-132-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_132_real__sympy_extras_simplify),
    ('sp-acj4-133-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_133_real__satassume_ask),
    ('sp-acj4-133-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_133_real__satrefine_refine),
    ('sp-acj4-133-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_133_real__satsimp_trigsimp),
    ('sp-acj4-133-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_133_real__satrefine_simplify),
    ('sp-acj4-133-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_133_real__sympy_auto),
    ('sp-acj4-133-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_133_real__sympy_ask),
    ('sp-acj4-133-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261019-221849', sp_acj4_133_real__sympy_satask),
    ('sp-acj4-133-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_133_real__sympy_refine),
    ('sp-acj4-133-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_133_real__sympy_simplify),
    ('sp-acj4-133-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_133_real__sympy_extras_ask),
    ('sp-acj4-133-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_133_real__sympy_extras_refine),
    ('sp-acj4-133-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_133_real__sympy_extras_simplify),
    ('sp-acj4-136-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_136_real__satassume_ask),
    ('sp-acj4-136-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_136_real__satrefine_refine),
    ('sp-acj4-136-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_136_real__satsimp_trigsimp),
    ('sp-acj4-136-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_136_real__satrefine_simplify),
    ('sp-acj4-136-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_136_real__sympy_auto),
    ('sp-acj4-136-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_136_real__sympy_ask),
    ('sp-acj4-136-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261019-221849', sp_acj4_136_real__sympy_satask),
    ('sp-acj4-136-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_136_real__sympy_refine),
    ('sp-acj4-136-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_136_real__sympy_simplify),
    ('sp-acj4-136-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_136_real__sympy_extras_ask),
    ('sp-acj4-136-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_136_real__sympy_extras_refine),
    ('sp-acj4-136-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_136_real__sympy_extras_simplify),
    ('sp-acj4-137-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_137_real__satassume_ask),
    ('sp-acj4-137-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_137_real__satrefine_refine),
    ('sp-acj4-137-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_137_real__satsimp_trigsimp),
    ('sp-acj4-137-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_137_real__satrefine_simplify),
    ('sp-acj4-137-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_137_real__sympy_auto),
    ('sp-acj4-137-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_137_real__sympy_ask),
    ('sp-acj4-137-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261019-221849', sp_acj4_137_real__sympy_satask),
    ('sp-acj4-137-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_137_real__sympy_refine),
    ('sp-acj4-137-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_137_real__sympy_simplify),
    ('sp-acj4-137-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_137_real__sympy_extras_ask),
    ('sp-acj4-137-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_137_real__sympy_extras_refine),
    ('sp-acj4-137-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_137_real__sympy_extras_simplify),
    ('sp-acj4-14-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261020-065124', sp_acj4_14_real__satassume_ask),
    ('sp-acj4-14-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_14_real__satrefine_refine),
    ('sp-acj4-14-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261020-065212', sp_acj4_14_real__satsimp_trigsimp),
    ('sp-acj4-14-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_14_real__satrefine_simplify),
    ('sp-acj4-14-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_14_real__sympy_auto),
    ('sp-acj4-14-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261020-064258', sp_acj4_14_real__sympy_ask),
    ('sp-acj4-14-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261019-221849', sp_acj4_14_real__sympy_satask),
    ('sp-acj4-14-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261020-064447', sp_acj4_14_real__sympy_refine),
    ('sp-acj4-14-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_14_real__sympy_simplify),
    ('sp-acj4-14-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_14_real__sympy_extras_ask),
    ('sp-acj4-14-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_14_real__sympy_extras_refine),
    ('sp-acj4-14-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_14_real__sympy_extras_simplify),
    ('sp-acj4-145-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_145_real__satassume_ask),
    ('sp-acj4-145-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_145_real__satrefine_refine),
    ('sp-acj4-145-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_145_real__satsimp_trigsimp),
    ('sp-acj4-145-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_145_real__satrefine_simplify),
    ('sp-acj4-145-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_145_real__sympy_auto),
    ('sp-acj4-145-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_145_real__sympy_ask),
    ('sp-acj4-145-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261019-221849', sp_acj4_145_real__sympy_satask),
    ('sp-acj4-145-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_145_real__sympy_refine),
    ('sp-acj4-145-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_145_real__sympy_simplify),
    ('sp-acj4-145-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_145_real__sympy_extras_ask),
    ('sp-acj4-145-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_145_real__sympy_extras_refine),
    ('sp-acj4-145-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_145_real__sympy_extras_simplify),
    ('sp-acj4-162-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_162_real__satassume_ask),
    ('sp-acj4-162-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_162_real__satrefine_refine),
    ('sp-acj4-162-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_162_real__satsimp_trigsimp),
    ('sp-acj4-162-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_162_real__satrefine_simplify),
    ('sp-acj4-162-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_162_real__sympy_auto),
    ('sp-acj4-162-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_162_real__sympy_ask),
    ('sp-acj4-162-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261019-221849', sp_acj4_162_real__sympy_satask),
    ('sp-acj4-162-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_162_real__sympy_refine),
    ('sp-acj4-162-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_162_real__sympy_simplify),
    ('sp-acj4-162-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_162_real__sympy_extras_ask),
    ('sp-acj4-162-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_162_real__sympy_extras_refine),
    ('sp-acj4-162-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_162_real__sympy_extras_simplify),
    ('sp-acj4-179-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_179_real__satassume_ask),
    ('sp-acj4-179-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_179_real__satrefine_refine),
    ('sp-acj4-179-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_179_real__satsimp_trigsimp),
    ('sp-acj4-179-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_179_real__satrefine_simplify),
    ('sp-acj4-179-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_179_real__sympy_auto),
    ('sp-acj4-179-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_179_real__sympy_ask),
    ('sp-acj4-179-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261019-221849', sp_acj4_179_real__sympy_satask),
    ('sp-acj4-179-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_179_real__sympy_refine),
    ('sp-acj4-179-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_179_real__sympy_simplify),
    ('sp-acj4-179-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_179_real__sympy_extras_ask),
    ('sp-acj4-179-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_179_real__sympy_extras_refine),
    ('sp-acj4-179-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_179_real__sympy_extras_simplify),
    ('sp-acj4-181-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_181_real__satassume_ask),
    ('sp-acj4-181-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_181_real__satrefine_refine),
    ('sp-acj4-181-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_181_real__satsimp_trigsimp),
    ('sp-acj4-181-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_181_real__satrefine_simplify),
    ('sp-acj4-181-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_181_real__sympy_auto),
    ('sp-acj4-181-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_181_real__sympy_ask),
    ('sp-acj4-181-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261019-221849', sp_acj4_181_real__sympy_satask),
    ('sp-acj4-181-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_181_real__sympy_refine),
    ('sp-acj4-181-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_181_real__sympy_simplify),
    ('sp-acj4-181-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_181_real__sympy_extras_ask),
    ('sp-acj4-181-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_181_real__sympy_extras_refine),
    ('sp-acj4-181-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_181_real__sympy_extras_simplify),
    ('sp-acj4-185-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_185_real__satassume_ask),
    ('sp-acj4-185-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_185_real__satrefine_refine),
    ('sp-acj4-185-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261020-065212', sp_acj4_185_real__satsimp_trigsimp),
    ('sp-acj4-185-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_185_real__satrefine_simplify),
    ('sp-acj4-185-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_185_real__sympy_auto),
    ('sp-acj4-185-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_185_real__sympy_ask),
    ('sp-acj4-185-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_185_real__sympy_satask),
    ('sp-acj4-185-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_185_real__sympy_refine),
    ('sp-acj4-185-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_185_real__sympy_simplify),
    ('sp-acj4-185-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_185_real__sympy_extras_ask),
    ('sp-acj4-185-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_185_real__sympy_extras_refine),
    ('sp-acj4-185-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_185_real__sympy_extras_simplify),
    ('sp-acj4-194-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_194_real__satassume_ask),
    ('sp-acj4-194-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_194_real__satrefine_refine),
    ('sp-acj4-194-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_194_real__satsimp_trigsimp),
    ('sp-acj4-194-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_194_real__satrefine_simplify),
    ('sp-acj4-194-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_194_real__sympy_auto),
    ('sp-acj4-194-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_194_real__sympy_ask),
    ('sp-acj4-194-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_194_real__sympy_satask),
    ('sp-acj4-194-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_194_real__sympy_refine),
    ('sp-acj4-194-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_194_real__sympy_simplify),
    ('sp-acj4-194-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_194_real__sympy_extras_ask),
    ('sp-acj4-194-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_194_real__sympy_extras_refine),
    ('sp-acj4-194-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_194_real__sympy_extras_simplify),
    ('sp-acj4-195-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_195_real__satassume_ask),
    ('sp-acj4-195-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_195_real__satrefine_refine),
    ('sp-acj4-195-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_195_real__satsimp_trigsimp),
    ('sp-acj4-195-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_195_real__satrefine_simplify),
    ('sp-acj4-195-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_195_real__sympy_auto),
    ('sp-acj4-195-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_195_real__sympy_ask),
    ('sp-acj4-195-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_195_real__sympy_satask),
    ('sp-acj4-195-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_195_real__sympy_refine),
    ('sp-acj4-195-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_195_real__sympy_simplify),
    ('sp-acj4-195-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_195_real__sympy_extras_ask),
    ('sp-acj4-195-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_195_real__sympy_extras_refine),
    ('sp-acj4-195-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_195_real__sympy_extras_simplify),
    ('sp-acj4-196-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_196_real__satassume_ask),
    ('sp-acj4-196-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_196_real__satrefine_refine),
    ('sp-acj4-196-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_196_real__satsimp_trigsimp),
    ('sp-acj4-196-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_196_real__satrefine_simplify),
    ('sp-acj4-196-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_196_real__sympy_auto),
    ('sp-acj4-196-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_196_real__sympy_ask),
    ('sp-acj4-196-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_196_real__sympy_satask),
    ('sp-acj4-196-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_196_real__sympy_refine),
    ('sp-acj4-196-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_196_real__sympy_simplify),
    ('sp-acj4-196-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_196_real__sympy_extras_ask),
    ('sp-acj4-196-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_196_real__sympy_extras_refine),
    ('sp-acj4-196-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_196_real__sympy_extras_simplify),
    ('sp-acj4-218-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261020-065124', sp_acj4_218_real__satassume_ask),
    ('sp-acj4-218-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_218_real__satrefine_refine),
    ('sp-acj4-218-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261020-065212', sp_acj4_218_real__satsimp_trigsimp),
    ('sp-acj4-218-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_218_real__satrefine_simplify),
    ('sp-acj4-218-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_218_real__sympy_auto),
    ('sp-acj4-218-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261020-064258', sp_acj4_218_real__sympy_ask),
    ('sp-acj4-218-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261019-221849', sp_acj4_218_real__sympy_satask),
    ('sp-acj4-218-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261020-064447', sp_acj4_218_real__sympy_refine),
    ('sp-acj4-218-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_218_real__sympy_simplify),
    ('sp-acj4-218-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_218_real__sympy_extras_ask),
    ('sp-acj4-218-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_218_real__sympy_extras_refine),
    ('sp-acj4-218-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_218_real__sympy_extras_simplify),
    ('sp-acj4-22-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_22_real__satassume_ask),
    ('sp-acj4-22-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_22_real__satrefine_refine),
    ('sp-acj4-22-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_22_real__satsimp_trigsimp),
    ('sp-acj4-22-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_22_real__satrefine_simplify),
    ('sp-acj4-22-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_22_real__sympy_auto),
    ('sp-acj4-22-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_22_real__sympy_ask),
    ('sp-acj4-22-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_22_real__sympy_satask),
    ('sp-acj4-22-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_22_real__sympy_refine),
    ('sp-acj4-22-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_22_real__sympy_simplify),
    ('sp-acj4-22-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_22_real__sympy_extras_ask),
    ('sp-acj4-22-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_22_real__sympy_extras_refine),
    ('sp-acj4-22-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_22_real__sympy_extras_simplify),
    ('sp-acj4-220-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261020-065124', sp_acj4_220_real__satassume_ask),
    ('sp-acj4-220-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_220_real__satrefine_refine),
    ('sp-acj4-220-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261020-065212', sp_acj4_220_real__satsimp_trigsimp),
    ('sp-acj4-220-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_220_real__satrefine_simplify),
    ('sp-acj4-220-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_220_real__sympy_auto),
    ('sp-acj4-220-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261020-064258', sp_acj4_220_real__sympy_ask),
    ('sp-acj4-220-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261019-221849', sp_acj4_220_real__sympy_satask),
    ('sp-acj4-220-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261020-064447', sp_acj4_220_real__sympy_refine),
    ('sp-acj4-220-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_220_real__sympy_simplify),
    ('sp-acj4-220-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_220_real__sympy_extras_ask),
    ('sp-acj4-220-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_220_real__sympy_extras_refine),
    ('sp-acj4-220-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_220_real__sympy_extras_simplify),
    ('sp-acj4-233-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261020-065124', sp_acj4_233_real__satassume_ask),
    ('sp-acj4-233-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_233_real__satrefine_refine),
    ('sp-acj4-233-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261020-065212', sp_acj4_233_real__satsimp_trigsimp),
    ('sp-acj4-233-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_233_real__satrefine_simplify),
    ('sp-acj4-233-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_233_real__sympy_auto),
    ('sp-acj4-233-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261020-064258', sp_acj4_233_real__sympy_ask),
    ('sp-acj4-233-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261019-221849', sp_acj4_233_real__sympy_satask),
    ('sp-acj4-233-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261020-064447', sp_acj4_233_real__sympy_refine),
    ('sp-acj4-233-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_233_real__sympy_simplify),
    ('sp-acj4-233-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_233_real__sympy_extras_ask),
    ('sp-acj4-233-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_233_real__sympy_extras_refine),
    ('sp-acj4-233-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_233_real__sympy_extras_simplify),
    ('sp-acj4-248-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_248_real__satassume_ask),
    ('sp-acj4-248-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_248_real__satrefine_refine),
    ('sp-acj4-248-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_248_real__satsimp_trigsimp),
    ('sp-acj4-248-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_248_real__satrefine_simplify),
    ('sp-acj4-248-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_248_real__sympy_auto),
    ('sp-acj4-248-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_248_real__sympy_ask),
    ('sp-acj4-248-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261019-221849', sp_acj4_248_real__sympy_satask),
    ('sp-acj4-248-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_248_real__sympy_refine),
    ('sp-acj4-248-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_248_real__sympy_simplify),
    ('sp-acj4-248-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_248_real__sympy_extras_ask),
    ('sp-acj4-248-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_248_real__sympy_extras_refine),
    ('sp-acj4-248-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_248_real__sympy_extras_simplify),
    ('sp-acj4-249-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_249_real__satassume_ask),
    ('sp-acj4-249-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_249_real__satrefine_refine),
    ('sp-acj4-249-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_249_real__satsimp_trigsimp),
    ('sp-acj4-249-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_249_real__satrefine_simplify),
    ('sp-acj4-249-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_249_real__sympy_auto),
    ('sp-acj4-249-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_249_real__sympy_ask),
    ('sp-acj4-249-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_249_real__sympy_satask),
    ('sp-acj4-249-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_249_real__sympy_refine),
    ('sp-acj4-249-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_249_real__sympy_simplify),
    ('sp-acj4-249-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_249_real__sympy_extras_ask),
    ('sp-acj4-249-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_249_real__sympy_extras_refine),
    ('sp-acj4-249-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_249_real__sympy_extras_simplify),
    ('sp-acj4-251-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_251_real__satassume_ask),
    ('sp-acj4-251-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_251_real__satrefine_refine),
    ('sp-acj4-251-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_251_real__satsimp_trigsimp),
    ('sp-acj4-251-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_251_real__satrefine_simplify),
    ('sp-acj4-251-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_251_real__sympy_auto),
    ('sp-acj4-251-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_251_real__sympy_ask),
    ('sp-acj4-251-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261019-221849', sp_acj4_251_real__sympy_satask),
    ('sp-acj4-251-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_251_real__sympy_refine),
    ('sp-acj4-251-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_251_real__sympy_simplify),
    ('sp-acj4-251-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_251_real__sympy_extras_ask),
    ('sp-acj4-251-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_251_real__sympy_extras_refine),
    ('sp-acj4-251-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_251_real__sympy_extras_simplify),
    ('sp-acj4-252-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_252_real__satassume_ask),
    ('sp-acj4-252-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_252_real__satrefine_refine),
    ('sp-acj4-252-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_252_real__satsimp_trigsimp),
    ('sp-acj4-252-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_252_real__satrefine_simplify),
    ('sp-acj4-252-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_252_real__sympy_auto),
    ('sp-acj4-252-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_252_real__sympy_ask),
    ('sp-acj4-252-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_252_real__sympy_satask),
    ('sp-acj4-252-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_252_real__sympy_refine),
    ('sp-acj4-252-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_252_real__sympy_simplify),
    ('sp-acj4-252-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_252_real__sympy_extras_ask),
    ('sp-acj4-252-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_252_real__sympy_extras_refine),
    ('sp-acj4-252-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_252_real__sympy_extras_simplify),
    ('sp-acj4-253-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_253_real__satassume_ask),
    ('sp-acj4-253-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_253_real__satrefine_refine),
    ('sp-acj4-253-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_253_real__satsimp_trigsimp),
    ('sp-acj4-253-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_253_real__satrefine_simplify),
    ('sp-acj4-253-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_253_real__sympy_auto),
    ('sp-acj4-253-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_253_real__sympy_ask),
    ('sp-acj4-253-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_253_real__sympy_satask),
    ('sp-acj4-253-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_253_real__sympy_refine),
    ('sp-acj4-253-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_253_real__sympy_simplify),
    ('sp-acj4-253-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_253_real__sympy_extras_ask),
    ('sp-acj4-253-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_253_real__sympy_extras_refine),
    ('sp-acj4-253-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_253_real__sympy_extras_simplify),
    ('sp-acj4-256-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261020-065124', sp_acj4_256_real__satassume_ask),
    ('sp-acj4-256-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_256_real__satrefine_refine),
    ('sp-acj4-256-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261020-065212', sp_acj4_256_real__satsimp_trigsimp),
    ('sp-acj4-256-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_256_real__satrefine_simplify),
    ('sp-acj4-256-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_256_real__sympy_auto),
    ('sp-acj4-256-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261020-064258', sp_acj4_256_real__sympy_ask),
    ('sp-acj4-256-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261019-221849', sp_acj4_256_real__sympy_satask),
    ('sp-acj4-256-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261020-064447', sp_acj4_256_real__sympy_refine),
    ('sp-acj4-256-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_256_real__sympy_simplify),
    ('sp-acj4-256-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_256_real__sympy_extras_ask),
    ('sp-acj4-256-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_256_real__sympy_extras_refine),
    ('sp-acj4-256-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_256_real__sympy_extras_simplify),
    ('sp-acj4-275-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_275_real__satassume_ask),
    ('sp-acj4-275-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_275_real__satrefine_refine),
    ('sp-acj4-275-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_275_real__satsimp_trigsimp),
    ('sp-acj4-275-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_275_real__satrefine_simplify),
    ('sp-acj4-275-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_275_real__sympy_auto),
    ('sp-acj4-275-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_275_real__sympy_ask),
    ('sp-acj4-275-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_275_real__sympy_satask),
    ('sp-acj4-275-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_275_real__sympy_refine),
    ('sp-acj4-275-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_275_real__sympy_simplify),
    ('sp-acj4-275-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_275_real__sympy_extras_ask),
    ('sp-acj4-275-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_275_real__sympy_extras_refine),
    ('sp-acj4-275-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_275_real__sympy_extras_simplify),
    ('sp-acj4-276-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_276_real__satassume_ask),
    ('sp-acj4-276-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_276_real__satrefine_refine),
    ('sp-acj4-276-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_276_real__satsimp_trigsimp),
    ('sp-acj4-276-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_276_real__satrefine_simplify),
    ('sp-acj4-276-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_276_real__sympy_auto),
    ('sp-acj4-276-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_276_real__sympy_ask),
    ('sp-acj4-276-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_276_real__sympy_satask),
    ('sp-acj4-276-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261020-064447', sp_acj4_276_real__sympy_refine),
    ('sp-acj4-276-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_276_real__sympy_simplify),
    ('sp-acj4-276-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_276_real__sympy_extras_ask),
    ('sp-acj4-276-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_276_real__sympy_extras_refine),
    ('sp-acj4-276-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_276_real__sympy_extras_simplify),
    ('sp-acj4-283-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_283_real__satassume_ask),
    ('sp-acj4-283-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_283_real__satrefine_refine),
    ('sp-acj4-283-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_283_real__satsimp_trigsimp),
    ('sp-acj4-283-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_283_real__satrefine_simplify),
    ('sp-acj4-283-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_283_real__sympy_auto),
    ('sp-acj4-283-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_283_real__sympy_ask),
    ('sp-acj4-283-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_283_real__sympy_satask),
    ('sp-acj4-283-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261020-064447', sp_acj4_283_real__sympy_refine),
    ('sp-acj4-283-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_283_real__sympy_simplify),
    ('sp-acj4-283-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_283_real__sympy_extras_ask),
    ('sp-acj4-283-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_283_real__sympy_extras_refine),
    ('sp-acj4-283-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_283_real__sympy_extras_simplify),
    ('sp-acj4-286-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_286_real__satassume_ask),
    ('sp-acj4-286-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_286_real__satrefine_refine),
    ('sp-acj4-286-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_286_real__satsimp_trigsimp),
    ('sp-acj4-286-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_286_real__satrefine_simplify),
    ('sp-acj4-286-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_286_real__sympy_auto),
    ('sp-acj4-286-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_286_real__sympy_ask),
    ('sp-acj4-286-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_286_real__sympy_satask),
    ('sp-acj4-286-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_286_real__sympy_refine),
    ('sp-acj4-286-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_286_real__sympy_simplify),
    ('sp-acj4-286-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_286_real__sympy_extras_ask),
    ('sp-acj4-286-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_286_real__sympy_extras_refine),
    ('sp-acj4-286-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_286_real__sympy_extras_simplify),
    ('sp-acj4-289-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_289_real__satassume_ask),
    ('sp-acj4-289-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_289_real__satrefine_refine),
    ('sp-acj4-289-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_289_real__satsimp_trigsimp),
    ('sp-acj4-289-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_289_real__satrefine_simplify),
    ('sp-acj4-289-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_289_real__sympy_auto),
    ('sp-acj4-289-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_289_real__sympy_ask),
    ('sp-acj4-289-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_289_real__sympy_satask),
    ('sp-acj4-289-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261020-064447', sp_acj4_289_real__sympy_refine),
    ('sp-acj4-289-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_289_real__sympy_simplify),
    ('sp-acj4-289-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_289_real__sympy_extras_ask),
    ('sp-acj4-289-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_289_real__sympy_extras_refine),
    ('sp-acj4-289-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_289_real__sympy_extras_simplify),
    ('sp-acj4-31-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261020-065124', sp_acj4_31_real__satassume_ask),
    ('sp-acj4-31-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_31_real__satrefine_refine),
    ('sp-acj4-31-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261020-065212', sp_acj4_31_real__satsimp_trigsimp),
    ('sp-acj4-31-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_31_real__satrefine_simplify),
    ('sp-acj4-31-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_31_real__sympy_auto),
    ('sp-acj4-31-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261020-064258', sp_acj4_31_real__sympy_ask),
    ('sp-acj4-31-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261019-221849', sp_acj4_31_real__sympy_satask),
    ('sp-acj4-31-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261020-064447', sp_acj4_31_real__sympy_refine),
    ('sp-acj4-31-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_31_real__sympy_simplify),
    ('sp-acj4-31-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_31_real__sympy_extras_ask),
    ('sp-acj4-31-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_31_real__sympy_extras_refine),
    ('sp-acj4-31-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_31_real__sympy_extras_simplify),
    ('sp-acj4-326-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261020-065124', sp_acj4_326_real__satassume_ask),
    ('sp-acj4-326-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_326_real__satrefine_refine),
    ('sp-acj4-326-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261020-065212', sp_acj4_326_real__satsimp_trigsimp),
    ('sp-acj4-326-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_326_real__satrefine_simplify),
    ('sp-acj4-326-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_326_real__sympy_auto),
    ('sp-acj4-326-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261020-064258', sp_acj4_326_real__sympy_ask),
    ('sp-acj4-326-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261019-221849', sp_acj4_326_real__sympy_satask),
    ('sp-acj4-326-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261020-064447', sp_acj4_326_real__sympy_refine),
    ('sp-acj4-326-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_326_real__sympy_simplify),
    ('sp-acj4-326-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_326_real__sympy_extras_ask),
    ('sp-acj4-326-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_326_real__sympy_extras_refine),
    ('sp-acj4-326-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_326_real__sympy_extras_simplify),
    ('sp-acj4-33-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261020-065124', sp_acj4_33_real__satassume_ask),
    ('sp-acj4-33-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_33_real__satrefine_refine),
    ('sp-acj4-33-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261020-065212', sp_acj4_33_real__satsimp_trigsimp),
    ('sp-acj4-33-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_33_real__satrefine_simplify),
    ('sp-acj4-33-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_33_real__sympy_auto),
    ('sp-acj4-33-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261020-064258', sp_acj4_33_real__sympy_ask),
    ('sp-acj4-33-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261019-221849', sp_acj4_33_real__sympy_satask),
    ('sp-acj4-33-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261020-064447', sp_acj4_33_real__sympy_refine),
    ('sp-acj4-33-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_33_real__sympy_simplify),
    ('sp-acj4-33-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_33_real__sympy_extras_ask),
    ('sp-acj4-33-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_33_real__sympy_extras_refine),
    ('sp-acj4-33-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_33_real__sympy_extras_simplify),
    ('sp-acj4-35-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_35_real__satassume_ask),
    ('sp-acj4-35-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_35_real__satrefine_refine),
    ('sp-acj4-35-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_35_real__satsimp_trigsimp),
    ('sp-acj4-35-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_35_real__satrefine_simplify),
    ('sp-acj4-35-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_35_real__sympy_auto),
    ('sp-acj4-35-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_35_real__sympy_ask),
    ('sp-acj4-35-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261019-221849', sp_acj4_35_real__sympy_satask),
    ('sp-acj4-35-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_35_real__sympy_refine),
    ('sp-acj4-35-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_35_real__sympy_simplify),
    ('sp-acj4-35-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_35_real__sympy_extras_ask),
    ('sp-acj4-35-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_35_real__sympy_extras_refine),
    ('sp-acj4-35-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_35_real__sympy_extras_simplify),
    ('sp-acj4-354-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_354_real__satassume_ask),
    ('sp-acj4-354-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_354_real__satrefine_refine),
    ('sp-acj4-354-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_354_real__satsimp_trigsimp),
    ('sp-acj4-354-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_354_real__satrefine_simplify),
    ('sp-acj4-354-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_354_real__sympy_auto),
    ('sp-acj4-354-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_354_real__sympy_ask),
    ('sp-acj4-354-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_354_real__sympy_satask),
    ('sp-acj4-354-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_354_real__sympy_refine),
    ('sp-acj4-354-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_354_real__sympy_simplify),
    ('sp-acj4-354-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_354_real__sympy_extras_ask),
    ('sp-acj4-354-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_354_real__sympy_extras_refine),
    ('sp-acj4-354-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_354_real__sympy_extras_simplify),
    ('sp-acj4-356-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_356_real__satassume_ask),
    ('sp-acj4-356-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_356_real__satrefine_refine),
    ('sp-acj4-356-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_356_real__satsimp_trigsimp),
    ('sp-acj4-356-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_356_real__satrefine_simplify),
    ('sp-acj4-356-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_356_real__sympy_auto),
    ('sp-acj4-356-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_356_real__sympy_ask),
    ('sp-acj4-356-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_356_real__sympy_satask),
    ('sp-acj4-356-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_356_real__sympy_refine),
    ('sp-acj4-356-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_356_real__sympy_simplify),
    ('sp-acj4-356-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_356_real__sympy_extras_ask),
    ('sp-acj4-356-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_356_real__sympy_extras_refine),
    ('sp-acj4-356-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_356_real__sympy_extras_simplify),
    ('sp-acj4-359-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_359_real__satassume_ask),
    ('sp-acj4-359-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_359_real__satrefine_refine),
    ('sp-acj4-359-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_359_real__satsimp_trigsimp),
    ('sp-acj4-359-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_359_real__satrefine_simplify),
    ('sp-acj4-359-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_359_real__sympy_auto),
    ('sp-acj4-359-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_359_real__sympy_ask),
    ('sp-acj4-359-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_359_real__sympy_satask),
    ('sp-acj4-359-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_359_real__sympy_refine),
    ('sp-acj4-359-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_359_real__sympy_simplify),
    ('sp-acj4-359-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_359_real__sympy_extras_ask),
    ('sp-acj4-359-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_359_real__sympy_extras_refine),
    ('sp-acj4-359-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_359_real__sympy_extras_simplify),
    ('sp-acj4-364-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_364_real__satassume_ask),
    ('sp-acj4-364-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_364_real__satrefine_refine),
    ('sp-acj4-364-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_364_real__satsimp_trigsimp),
    ('sp-acj4-364-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_364_real__satrefine_simplify),
    ('sp-acj4-364-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_364_real__sympy_auto),
    ('sp-acj4-364-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_364_real__sympy_ask),
    ('sp-acj4-364-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_364_real__sympy_satask),
    ('sp-acj4-364-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_364_real__sympy_refine),
    ('sp-acj4-364-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_364_real__sympy_simplify),
    ('sp-acj4-364-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_364_real__sympy_extras_ask),
    ('sp-acj4-364-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_364_real__sympy_extras_refine),
    ('sp-acj4-364-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_364_real__sympy_extras_simplify),
    ('sp-acj4-367-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_367_real__satassume_ask),
    ('sp-acj4-367-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_367_real__satrefine_refine),
    ('sp-acj4-367-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_367_real__satsimp_trigsimp),
    ('sp-acj4-367-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_367_real__satrefine_simplify),
    ('sp-acj4-367-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_367_real__sympy_auto),
    ('sp-acj4-367-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_367_real__sympy_ask),
    ('sp-acj4-367-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_367_real__sympy_satask),
    ('sp-acj4-367-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_367_real__sympy_refine),
    ('sp-acj4-367-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_367_real__sympy_simplify),
    ('sp-acj4-367-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_367_real__sympy_extras_ask),
    ('sp-acj4-367-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_367_real__sympy_extras_refine),
    ('sp-acj4-367-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_367_real__sympy_extras_simplify),
    ('sp-acj4-368-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_368_real__satassume_ask),
    ('sp-acj4-368-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_368_real__satrefine_refine),
    ('sp-acj4-368-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_368_real__satsimp_trigsimp),
    ('sp-acj4-368-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_368_real__satrefine_simplify),
    ('sp-acj4-368-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_368_real__sympy_auto),
    ('sp-acj4-368-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_368_real__sympy_ask),
    ('sp-acj4-368-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_368_real__sympy_satask),
    ('sp-acj4-368-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_368_real__sympy_refine),
    ('sp-acj4-368-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_368_real__sympy_simplify),
    ('sp-acj4-368-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_368_real__sympy_extras_ask),
    ('sp-acj4-368-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_368_real__sympy_extras_refine),
    ('sp-acj4-368-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_368_real__sympy_extras_simplify),
    ('sp-acj4-369-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_369_real__satassume_ask),
    ('sp-acj4-369-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_369_real__satrefine_refine),
    ('sp-acj4-369-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_369_real__satsimp_trigsimp),
    ('sp-acj4-369-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_369_real__satrefine_simplify),
    ('sp-acj4-369-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_369_real__sympy_auto),
    ('sp-acj4-369-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_369_real__sympy_ask),
    ('sp-acj4-369-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_369_real__sympy_satask),
    ('sp-acj4-369-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_369_real__sympy_refine),
    ('sp-acj4-369-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_369_real__sympy_simplify),
    ('sp-acj4-369-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_369_real__sympy_extras_ask),
    ('sp-acj4-369-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_369_real__sympy_extras_refine),
    ('sp-acj4-369-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_369_real__sympy_extras_simplify),
    ('sp-acj4-370-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_370_real__satassume_ask),
    ('sp-acj4-370-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_370_real__satrefine_refine),
    ('sp-acj4-370-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_370_real__satsimp_trigsimp),
    ('sp-acj4-370-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_370_real__satrefine_simplify),
    ('sp-acj4-370-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_370_real__sympy_auto),
    ('sp-acj4-370-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_370_real__sympy_ask),
    ('sp-acj4-370-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_370_real__sympy_satask),
    ('sp-acj4-370-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_370_real__sympy_refine),
    ('sp-acj4-370-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_370_real__sympy_simplify),
    ('sp-acj4-370-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_370_real__sympy_extras_ask),
    ('sp-acj4-370-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_370_real__sympy_extras_refine),
    ('sp-acj4-370-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_370_real__sympy_extras_simplify),
    ('sp-acj4-371-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_371_real__satassume_ask),
    ('sp-acj4-371-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_371_real__satrefine_refine),
    ('sp-acj4-371-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_371_real__satsimp_trigsimp),
    ('sp-acj4-371-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_371_real__satrefine_simplify),
    ('sp-acj4-371-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_371_real__sympy_auto),
    ('sp-acj4-371-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_371_real__sympy_ask),
    ('sp-acj4-371-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_371_real__sympy_satask),
    ('sp-acj4-371-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_371_real__sympy_refine),
    ('sp-acj4-371-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_371_real__sympy_simplify),
    ('sp-acj4-371-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_371_real__sympy_extras_ask),
    ('sp-acj4-371-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_371_real__sympy_extras_refine),
    ('sp-acj4-371-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_371_real__sympy_extras_simplify),
    ('sp-acj4-372-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_372_real__satassume_ask),
    ('sp-acj4-372-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_372_real__satrefine_refine),
    ('sp-acj4-372-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_372_real__satsimp_trigsimp),
    ('sp-acj4-372-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_372_real__satrefine_simplify),
    ('sp-acj4-372-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_372_real__sympy_auto),
    ('sp-acj4-372-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_372_real__sympy_ask),
    ('sp-acj4-372-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_372_real__sympy_satask),
    ('sp-acj4-372-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_372_real__sympy_refine),
    ('sp-acj4-372-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_372_real__sympy_simplify),
    ('sp-acj4-372-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_372_real__sympy_extras_ask),
    ('sp-acj4-372-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_372_real__sympy_extras_refine),
    ('sp-acj4-372-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_372_real__sympy_extras_simplify),
    ('sp-acj4-373-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_373_real__satassume_ask),
    ('sp-acj4-373-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_373_real__satrefine_refine),
    ('sp-acj4-373-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_373_real__satsimp_trigsimp),
    ('sp-acj4-373-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_373_real__satrefine_simplify),
    ('sp-acj4-373-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_373_real__sympy_auto),
    ('sp-acj4-373-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_373_real__sympy_ask),
    ('sp-acj4-373-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_373_real__sympy_satask),
    ('sp-acj4-373-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_373_real__sympy_refine),
    ('sp-acj4-373-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_373_real__sympy_simplify),
    ('sp-acj4-373-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_373_real__sympy_extras_ask),
    ('sp-acj4-373-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_373_real__sympy_extras_refine),
    ('sp-acj4-373-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_373_real__sympy_extras_simplify),
    ('sp-acj4-38-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_38_real__satassume_ask),
    ('sp-acj4-38-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_38_real__satrefine_refine),
    ('sp-acj4-38-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_38_real__satsimp_trigsimp),
    ('sp-acj4-38-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_38_real__satrefine_simplify),
    ('sp-acj4-38-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_38_real__sympy_auto),
    ('sp-acj4-38-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_38_real__sympy_ask),
    ('sp-acj4-38-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261019-221849', sp_acj4_38_real__sympy_satask),
    ('sp-acj4-38-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_38_real__sympy_refine),
    ('sp-acj4-38-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_38_real__sympy_simplify),
    ('sp-acj4-38-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_38_real__sympy_extras_ask),
    ('sp-acj4-38-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_38_real__sympy_extras_refine),
    ('sp-acj4-38-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_38_real__sympy_extras_simplify),
    ('sp-acj4-394-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_394_real__satassume_ask),
    ('sp-acj4-394-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_394_real__satrefine_refine),
    ('sp-acj4-394-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_394_real__satsimp_trigsimp),
    ('sp-acj4-394-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_394_real__satrefine_simplify),
    ('sp-acj4-394-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_394_real__sympy_auto),
    ('sp-acj4-394-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_394_real__sympy_ask),
    ('sp-acj4-394-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261019-221849', sp_acj4_394_real__sympy_satask),
    ('sp-acj4-394-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_394_real__sympy_refine),
    ('sp-acj4-394-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_394_real__sympy_simplify),
    ('sp-acj4-394-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_394_real__sympy_extras_ask),
    ('sp-acj4-394-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_394_real__sympy_extras_refine),
    ('sp-acj4-394-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_394_real__sympy_extras_simplify),
    ('sp-acj4-395-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_395_real__satassume_ask),
    ('sp-acj4-395-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_395_real__satrefine_refine),
    ('sp-acj4-395-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_395_real__satsimp_trigsimp),
    ('sp-acj4-395-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_395_real__satrefine_simplify),
    ('sp-acj4-395-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_395_real__sympy_auto),
    ('sp-acj4-395-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_395_real__sympy_ask),
    ('sp-acj4-395-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_395_real__sympy_satask),
    ('sp-acj4-395-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_395_real__sympy_refine),
    ('sp-acj4-395-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_395_real__sympy_simplify),
    ('sp-acj4-395-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_395_real__sympy_extras_ask),
    ('sp-acj4-395-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_395_real__sympy_extras_refine),
    ('sp-acj4-395-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_395_real__sympy_extras_simplify),
    ('sp-acj4-396-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_396_real__satassume_ask),
    ('sp-acj4-396-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_396_real__satrefine_refine),
    ('sp-acj4-396-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_396_real__satsimp_trigsimp),
    ('sp-acj4-396-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_396_real__satrefine_simplify),
    ('sp-acj4-396-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_396_real__sympy_auto),
    ('sp-acj4-396-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_396_real__sympy_ask),
    ('sp-acj4-396-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_396_real__sympy_satask),
    ('sp-acj4-396-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_396_real__sympy_refine),
    ('sp-acj4-396-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_396_real__sympy_simplify),
    ('sp-acj4-396-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_396_real__sympy_extras_ask),
    ('sp-acj4-396-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_396_real__sympy_extras_refine),
    ('sp-acj4-396-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_396_real__sympy_extras_simplify),
    ('sp-acj4-397-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_397_real__satassume_ask),
    ('sp-acj4-397-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_397_real__satrefine_refine),
    ('sp-acj4-397-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_397_real__satsimp_trigsimp),
    ('sp-acj4-397-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_397_real__satrefine_simplify),
    ('sp-acj4-397-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_397_real__sympy_auto),
    ('sp-acj4-397-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_397_real__sympy_ask),
    ('sp-acj4-397-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_397_real__sympy_satask),
    ('sp-acj4-397-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_397_real__sympy_refine),
    ('sp-acj4-397-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_397_real__sympy_simplify),
    ('sp-acj4-397-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_397_real__sympy_extras_ask),
    ('sp-acj4-397-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_397_real__sympy_extras_refine),
    ('sp-acj4-397-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_397_real__sympy_extras_simplify),
    ('sp-acj4-402-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_402_real__satassume_ask),
    ('sp-acj4-402-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_402_real__satrefine_refine),
    ('sp-acj4-402-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_402_real__satsimp_trigsimp),
    ('sp-acj4-402-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_402_real__satrefine_simplify),
    ('sp-acj4-402-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_402_real__sympy_auto),
    ('sp-acj4-402-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_402_real__sympy_ask),
    ('sp-acj4-402-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261019-221849', sp_acj4_402_real__sympy_satask),
    ('sp-acj4-402-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_402_real__sympy_refine),
    ('sp-acj4-402-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_402_real__sympy_simplify),
    ('sp-acj4-402-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_402_real__sympy_extras_ask),
    ('sp-acj4-402-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_402_real__sympy_extras_refine),
    ('sp-acj4-402-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_402_real__sympy_extras_simplify),
    ('sp-acj4-404-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_404_real__satassume_ask),
    ('sp-acj4-404-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_404_real__satrefine_refine),
    ('sp-acj4-404-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_404_real__satsimp_trigsimp),
    ('sp-acj4-404-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_404_real__satrefine_simplify),
    ('sp-acj4-404-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_404_real__sympy_auto),
    ('sp-acj4-404-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_404_real__sympy_ask),
    ('sp-acj4-404-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_404_real__sympy_satask),
    ('sp-acj4-404-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_404_real__sympy_refine),
    ('sp-acj4-404-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_404_real__sympy_simplify),
    ('sp-acj4-404-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_404_real__sympy_extras_ask),
    ('sp-acj4-404-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_404_real__sympy_extras_refine),
    ('sp-acj4-404-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_404_real__sympy_extras_simplify),
    ('sp-acj4-412-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_412_real__satassume_ask),
    ('sp-acj4-412-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_412_real__satrefine_refine),
    ('sp-acj4-412-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_412_real__satsimp_trigsimp),
    ('sp-acj4-412-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_412_real__satrefine_simplify),
    ('sp-acj4-412-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_412_real__sympy_auto),
    ('sp-acj4-412-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_412_real__sympy_ask),
    ('sp-acj4-412-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261019-221849', sp_acj4_412_real__sympy_satask),
    ('sp-acj4-412-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_412_real__sympy_refine),
    ('sp-acj4-412-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_412_real__sympy_simplify),
    ('sp-acj4-412-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_412_real__sympy_extras_ask),
    ('sp-acj4-412-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_412_real__sympy_extras_refine),
    ('sp-acj4-412-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_412_real__sympy_extras_simplify),
    ('sp-acj4-413-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_413_real__satassume_ask),
    ('sp-acj4-413-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_413_real__satrefine_refine),
    ('sp-acj4-413-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_413_real__satsimp_trigsimp),
    ('sp-acj4-413-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_413_real__satrefine_simplify),
    ('sp-acj4-413-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_413_real__sympy_auto),
    ('sp-acj4-413-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_413_real__sympy_ask),
    ('sp-acj4-413-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_413_real__sympy_satask),
    ('sp-acj4-413-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_413_real__sympy_refine),
    ('sp-acj4-413-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_413_real__sympy_simplify),
    ('sp-acj4-413-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_413_real__sympy_extras_ask),
    ('sp-acj4-413-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_413_real__sympy_extras_refine),
    ('sp-acj4-413-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_413_real__sympy_extras_simplify),
    ('sp-acj4-414-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_414_real__satassume_ask),
    ('sp-acj4-414-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_414_real__satrefine_refine),
    ('sp-acj4-414-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_414_real__satsimp_trigsimp),
    ('sp-acj4-414-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_414_real__satrefine_simplify),
    ('sp-acj4-414-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_414_real__sympy_auto),
    ('sp-acj4-414-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_414_real__sympy_ask),
    ('sp-acj4-414-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_414_real__sympy_satask),
    ('sp-acj4-414-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_414_real__sympy_refine),
    ('sp-acj4-414-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_414_real__sympy_simplify),
    ('sp-acj4-414-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_414_real__sympy_extras_ask),
    ('sp-acj4-414-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_414_real__sympy_extras_refine),
    ('sp-acj4-414-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_414_real__sympy_extras_simplify),
    ('sp-acj4-415-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_415_real__satassume_ask),
    ('sp-acj4-415-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_415_real__satrefine_refine),
    ('sp-acj4-415-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_415_real__satsimp_trigsimp),
    ('sp-acj4-415-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_415_real__satrefine_simplify),
    ('sp-acj4-415-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_415_real__sympy_auto),
    ('sp-acj4-415-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_415_real__sympy_ask),
    ('sp-acj4-415-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_415_real__sympy_satask),
    ('sp-acj4-415-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_415_real__sympy_refine),
    ('sp-acj4-415-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_415_real__sympy_simplify),
    ('sp-acj4-415-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_415_real__sympy_extras_ask),
    ('sp-acj4-415-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_415_real__sympy_extras_refine),
    ('sp-acj4-415-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_415_real__sympy_extras_simplify),
    ('sp-acj4-417-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_417_real__satassume_ask),
    ('sp-acj4-417-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_417_real__satrefine_refine),
    ('sp-acj4-417-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_417_real__satsimp_trigsimp),
    ('sp-acj4-417-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_417_real__satrefine_simplify),
    ('sp-acj4-417-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_417_real__sympy_auto),
    ('sp-acj4-417-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_417_real__sympy_ask),
    ('sp-acj4-417-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261019-221849', sp_acj4_417_real__sympy_satask),
    ('sp-acj4-417-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_417_real__sympy_refine),
    ('sp-acj4-417-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_417_real__sympy_simplify),
    ('sp-acj4-417-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_417_real__sympy_extras_ask),
    ('sp-acj4-421-real', 'satassume-ask', 'true', 'null', 'satassume-ask-20261020-065124', sp_acj4_421_real__satassume_ask),
    ('sp-acj4-421-real', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261020-064814', sp_acj4_421_real__satrefine_refine),
    ('sp-acj4-421-real', 'satsimp-trigsimp', 'true', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_421_real__satsimp_trigsimp),
    ('sp-acj4-421-real', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_421_real__satrefine_simplify),
    ('sp-acj4-421-real', 'sympy-auto', 'true', 'null', 'sympy-auto-20261020-064252', sp_acj4_421_real__sympy_auto),
    ('sp-acj4-421-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_421_real__sympy_ask),
    ('sp-acj4-421-real', 'sympy-satask', 'true', 'null', 'sympy-satask-20261019-221849', sp_acj4_421_real__sympy_satask),
    ('sp-acj4-421-real', 'sympy-refine', 'true', 'null', 'sympy-refine-20261020-064447', sp_acj4_421_real__sympy_refine),
    ('sp-acj4-421-real', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261020-064757', sp_acj4_421_real__sympy_simplify),
    ('sp-acj4-421-real', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_421_real__sympy_extras_ask),
    ('sp-acj4-421-real', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_421_real__sympy_extras_refine),
    ('sp-acj4-421-real', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_421_real__sympy_extras_simplify),
    ('sp-acj4-5-real', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_5_real__satassume_ask),
    ('sp-acj4-5-real', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_5_real__satrefine_refine),
    ('sp-acj4-5-real', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_5_real__satsimp_trigsimp),
    ('sp-acj4-5-real', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_5_real__satrefine_simplify),
    ('sp-acj4-5-real', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_5_real__sympy_auto),
    ('sp-acj4-5-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_5_real__sympy_ask),
    ('sp-acj4-5-real', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261019-221849', sp_acj4_5_real__sympy_satask),
    ('sp-acj4-5-real', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_5_real__sympy_refine),
    ('sp-acj4-5-real', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_5_real__sympy_simplify),
    ('sp-acj4-5-real', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_5_real__sympy_extras_ask),
    ('sp-acj4-5-real', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_5_real__sympy_extras_refine),
    ('sp-acj4-5-real', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_5_real__sympy_extras_simplify),
    ('sp-acj4-73-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261020-065124', sp_acj4_73_real__satassume_ask),
    ('sp-acj4-73-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_73_real__satrefine_refine),
    ('sp-acj4-73-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261020-065212', sp_acj4_73_real__satsimp_trigsimp),
    ('sp-acj4-73-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_73_real__satrefine_simplify),
    ('sp-acj4-73-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_73_real__sympy_auto),
    ('sp-acj4-73-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261020-064258', sp_acj4_73_real__sympy_ask),
    ('sp-acj4-73-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261019-221849', sp_acj4_73_real__sympy_satask),
    ('sp-acj4-73-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261020-064447', sp_acj4_73_real__sympy_refine),
    ('sp-acj4-73-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_73_real__sympy_simplify),
    ('sp-acj4-73-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_73_real__sympy_extras_ask),
    ('sp-acj4-73-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_73_real__sympy_extras_refine),
    ('sp-acj4-73-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_73_real__sympy_extras_simplify),
    ('sp-acj4-80-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261020-065124', sp_acj4_80_real__satassume_ask),
    ('sp-acj4-80-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_80_real__satrefine_refine),
    ('sp-acj4-80-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261020-065212', sp_acj4_80_real__satsimp_trigsimp),
    ('sp-acj4-80-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_80_real__satrefine_simplify),
    ('sp-acj4-80-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_80_real__sympy_auto),
    ('sp-acj4-80-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261020-064258', sp_acj4_80_real__sympy_ask),
    ('sp-acj4-80-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261019-221849', sp_acj4_80_real__sympy_satask),
    ('sp-acj4-80-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261020-064447', sp_acj4_80_real__sympy_refine),
    ('sp-acj4-80-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_80_real__sympy_simplify),
    ('sp-acj4-80-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_80_real__sympy_extras_ask),
    ('sp-acj4-80-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_80_real__sympy_extras_refine),
    ('sp-acj4-80-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_80_real__sympy_extras_simplify),
    ('sp-acj4-83-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261020-065124', sp_acj4_83_real__satassume_ask),
    ('sp-acj4-83-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_83_real__satrefine_refine),
    ('sp-acj4-83-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261020-065212', sp_acj4_83_real__satsimp_trigsimp),
    ('sp-acj4-83-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_83_real__satrefine_simplify),
    ('sp-acj4-83-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_83_real__sympy_auto),
    ('sp-acj4-83-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261020-064258', sp_acj4_83_real__sympy_ask),
    ('sp-acj4-83-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261019-221849', sp_acj4_83_real__sympy_satask),
    ('sp-acj4-83-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261020-064447', sp_acj4_83_real__sympy_refine),
    ('sp-acj4-83-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_83_real__sympy_simplify),
    ('sp-acj4-83-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_83_real__sympy_extras_ask),
    ('sp-acj4-83-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_83_real__sympy_extras_refine),
    ('sp-acj4-83-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_83_real__sympy_extras_simplify),
    ('sp-acj4-86-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261020-065124', sp_acj4_86_real__satassume_ask),
    ('sp-acj4-86-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_86_real__satrefine_refine),
    ('sp-acj4-86-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261020-065212', sp_acj4_86_real__satsimp_trigsimp),
    ('sp-acj4-86-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_86_real__satrefine_simplify),
    ('sp-acj4-86-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_86_real__sympy_auto),
    ('sp-acj4-86-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261020-064258', sp_acj4_86_real__sympy_ask),
    ('sp-acj4-86-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261019-221849', sp_acj4_86_real__sympy_satask),
    ('sp-acj4-86-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261020-064447', sp_acj4_86_real__sympy_refine),
    ('sp-acj4-86-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_86_real__sympy_simplify),
    ('sp-acj4-86-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_86_real__sympy_extras_ask),
    ('sp-acj4-86-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_86_real__sympy_extras_refine),
    ('sp-acj4-86-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_86_real__sympy_extras_simplify),
    ('sp-acj4-90-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261020-065124', sp_acj4_90_real__satassume_ask),
    ('sp-acj4-90-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_90_real__satrefine_refine),
    ('sp-acj4-90-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261020-065212', sp_acj4_90_real__satsimp_trigsimp),
    ('sp-acj4-90-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_90_real__satrefine_simplify),
    ('sp-acj4-90-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_90_real__sympy_auto),
    ('sp-acj4-90-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261020-064258', sp_acj4_90_real__sympy_ask),
    ('sp-acj4-90-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261019-221849', sp_acj4_90_real__sympy_satask),
    ('sp-acj4-90-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261020-064447', sp_acj4_90_real__sympy_refine),
    ('sp-acj4-90-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_90_real__sympy_simplify),
    ('sp-acj4-90-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_90_real__sympy_extras_ask),
    ('sp-acj4-90-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_90_real__sympy_extras_refine),
    ('sp-acj4-90-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_90_real__sympy_extras_simplify),
    ('sp-acj4-99-real', 'satassume-ask', 'true', 'true', 'satassume-ask-20261020-065124', sp_acj4_99_real__satassume_ask),
    ('sp-acj4-99-real', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261020-064814', sp_acj4_99_real__satrefine_refine),
    ('sp-acj4-99-real', 'satsimp-trigsimp', 'true', 'true', 'satsimp-trigsimp-20261020-065212', sp_acj4_99_real__satsimp_trigsimp),
    ('sp-acj4-99-real', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261020-065134', sp_acj4_99_real__satrefine_simplify),
    ('sp-acj4-99-real', 'sympy-auto', 'true', 'true', 'sympy-auto-20261020-064252', sp_acj4_99_real__sympy_auto),
    ('sp-acj4-99-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261020-064258', sp_acj4_99_real__sympy_ask),
    ('sp-acj4-99-real', 'sympy-satask', 'true', 'true', 'sympy-satask-20261019-221849', sp_acj4_99_real__sympy_satask),
    ('sp-acj4-99-real', 'sympy-refine', 'true', 'true', 'sympy-refine-20261020-064447', sp_acj4_99_real__sympy_refine),
    ('sp-acj4-99-real', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261020-064757', sp_acj4_99_real__sympy_simplify),
    ('sp-acj4-99-real', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261020-065223', sp_acj4_99_real__sympy_extras_ask),
    ('sp-acj4-99-real', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261020-065818', sp_acj4_99_real__sympy_extras_refine),
    ('sp-acj4-99-real', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261020-070552', sp_acj4_99_real__sympy_extras_simplify),
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
