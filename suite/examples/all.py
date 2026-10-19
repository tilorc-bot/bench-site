# assume-eval: a runnable script from the results browser
# Run: python3 this-file.py (or paste it into python or Jupyter).
# suite examples · every case · all Python systems (27 cases listed)
# 270 case run(s), a function each (listed in CASES).  Each runs in a fresh copy of
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
# dropped (not a unary fact about one symbol): p > 2


# ---- case demo-atan2-01 · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (no verdict)
@_in(_SETUP1)
def demo_atan2_01__satassume_ask():
    x = Symbol('x')
    y = Symbol('y')
    Assum = And(Q.real(x), Q.real(y), Q.positive(x))
    Residual = atan2(y, x) - atan(y / x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-atan2-01 · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered true (solved)
@_in(_SETUP2)
def demo_atan2_01__satrefine_refine():
    x = Symbol('x')
    y = Symbol('y')
    Assum = And(Q.real(x), Q.real(y), Q.positive(x))
    Residual = atan2(y, x) - atan(y / x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-atan2-01 · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered true (solved)
@_in(_SETUP2)
def demo_atan2_01__satrefine_simplify():
    x = Symbol('x')
    y = Symbol('y')
    Assum = And(Q.real(x), Q.real(y), Q.positive(x))
    Residual = atan2(y, x) - atan(y / x)
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-atan2-01 · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered true (solved)
@_in(_SETUP3)
def demo_atan2_01__sympy_auto():
    x = Symbol('x', real=True, positive=True)
    y = Symbol('y', real=True)
    Residual = atan2(y, x) - atan(y / x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-atan2-01 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered null (no verdict)
@_in(_SETUP3)
def demo_atan2_01__sympy_ask():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    Assum = And(Q.real(x), Q.real(y), Q.positive(x))
    Residual = atan2(y, x) - atan(y / x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-atan2-01 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered true (solved)
@_in(_SETUP3)
def demo_atan2_01__sympy_refine():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    Assum = And(Q.real(x), Q.real(y), Q.positive(x))
    Residual = atan2(y, x) - atan(y / x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-atan2-01 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered true (solved)
@_in(_SETUP3)
def demo_atan2_01__sympy_simplify():
    x = Symbol('x', real=True, positive=True)
    y = Symbol('y', real=True)
    Residual = atan2(y, x) - atan(y / x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-atan2-01 · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered null (no verdict)
@_in(_SETUP4)
def demo_atan2_01__sympy_extras_ask():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    Assum = And(Q.real(x), Q.real(y), Q.positive(x))
    Residual = atan2(y, x) - atan(y / x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-atan2-01 · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered true (solved)
@_in(_SETUP4)
def demo_atan2_01__sympy_extras_refine():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    Assum = And(Q.real(x), Q.real(y), Q.positive(x))
    Residual = atan2(y, x) - atan(y / x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-atan2-01 · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered true (solved)
@_in(_SETUP4)
def demo_atan2_01__sympy_extras_simplify():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    Assum = And(Q.real(x), Q.real(y), Q.positive(x))
    Residual = atan2(y, x) - atan(y / x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-atan2-02 · expected false · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (no verdict)
@_in(_SETUP1)
def demo_atan2_02__satassume_ask():
    x = Symbol('x')
    y = Symbol('y')
    Assum = And(Q.real(x), Q.real(y), Q.negative(x), Q.positive(y))
    Residual = atan2(y, x) - atan(y / x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-atan2-02 · expected false · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered false (solved)
@_in(_SETUP2)
def demo_atan2_02__satrefine_refine():
    x = Symbol('x')
    y = Symbol('y')
    Assum = And(Q.real(x), Q.real(y), Q.negative(x), Q.positive(y))
    Residual = atan2(y, x) - atan(y / x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-atan2-02 · expected false · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered false (solved)
@_in(_SETUP2)
def demo_atan2_02__satrefine_simplify():
    x = Symbol('x')
    y = Symbol('y')
    Assum = And(Q.real(x), Q.real(y), Q.negative(x), Q.positive(y))
    Residual = atan2(y, x) - atan(y / x)
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-atan2-02 · expected false · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered false (solved)
@_in(_SETUP3)
def demo_atan2_02__sympy_auto():
    x = Symbol('x', real=True, negative=True)
    y = Symbol('y', real=True, positive=True)
    Residual = atan2(y, x) - atan(y / x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-atan2-02 · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered null (no verdict)
@_in(_SETUP3)
def demo_atan2_02__sympy_ask():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    Assum = And(Q.real(x), Q.real(y), Q.negative(x), Q.positive(y))
    Residual = atan2(y, x) - atan(y / x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-atan2-02 · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered false (solved)
@_in(_SETUP3)
def demo_atan2_02__sympy_refine():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    Assum = And(Q.real(x), Q.real(y), Q.negative(x), Q.positive(y))
    Residual = atan2(y, x) - atan(y / x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-atan2-02 · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered false (solved)
@_in(_SETUP3)
def demo_atan2_02__sympy_simplify():
    x = Symbol('x', real=True, negative=True)
    y = Symbol('y', real=True, positive=True)
    Residual = atan2(y, x) - atan(y / x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-atan2-02 · expected false · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered null (no verdict)
@_in(_SETUP4)
def demo_atan2_02__sympy_extras_ask():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    Assum = And(Q.real(x), Q.real(y), Q.negative(x), Q.positive(y))
    Residual = atan2(y, x) - atan(y / x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-atan2-02 · expected false · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered false (solved)
@_in(_SETUP4)
def demo_atan2_02__sympy_extras_refine():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    Assum = And(Q.real(x), Q.real(y), Q.negative(x), Q.positive(y))
    Residual = atan2(y, x) - atan(y / x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-atan2-02 · expected false · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered false (solved)
@_in(_SETUP4)
def demo_atan2_02__sympy_extras_simplify():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    Assum = And(Q.real(x), Q.real(y), Q.negative(x), Q.positive(y))
    Residual = atan2(y, x) - atan(y / x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-abs-01 · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (no verdict)
@_in(_SETUP1)
def demo_eq_abs_01__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.negative(x))
    Residual = Abs(x) - (-x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-abs-01 · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered true (solved)
@_in(_SETUP2)
def demo_eq_abs_01__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.negative(x))
    Residual = Abs(x) - (-x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-abs-01 · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered true (solved)
@_in(_SETUP2)
def demo_eq_abs_01__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.negative(x))
    Residual = Abs(x) - (-x)
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-abs-01 · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered true (solved)
@_in(_SETUP3)
def demo_eq_abs_01__sympy_auto():
    x = Symbol('x', real=True, negative=True)
    Residual = Abs(x) - (-x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-abs-01 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered null (no verdict)
@_in(_SETUP3)
def demo_eq_abs_01__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x))
    Residual = Abs(x) - (-x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-abs-01 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered true (solved)
@_in(_SETUP3)
def demo_eq_abs_01__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x))
    Residual = Abs(x) - (-x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-abs-01 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered true (solved)
@_in(_SETUP3)
def demo_eq_abs_01__sympy_simplify():
    x = Symbol('x', real=True, negative=True)
    Residual = Abs(x) - (-x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-abs-01 · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered true (solved)
@_in(_SETUP4)
def demo_eq_abs_01__sympy_extras_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x))
    Residual = Abs(x) - (-x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-abs-01 · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered true (solved)
@_in(_SETUP4)
def demo_eq_abs_01__sympy_extras_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x))
    Residual = Abs(x) - (-x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-abs-01 · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered true (solved)
@_in(_SETUP4)
def demo_eq_abs_01__sympy_extras_simplify():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x))
    Residual = Abs(x) - (-x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-abs-02 · expected false · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered false (solved)
@_in(_SETUP1)
def demo_eq_abs_02__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.negative(x))
    Residual = Abs(x) - x
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-abs-02 · expected false · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered null (no verdict)
@_in(_SETUP2)
def demo_eq_abs_02__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.negative(x))
    Residual = Abs(x) - x
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-abs-02 · expected false · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered null (no verdict)
@_in(_SETUP2)
def demo_eq_abs_02__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.negative(x))
    Residual = Abs(x) - x
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-abs-02 · expected false · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered null (no verdict)
@_in(_SETUP3)
def demo_eq_abs_02__sympy_auto():
    x = Symbol('x', real=True, negative=True)
    Residual = Abs(x) - x
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-abs-02 · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered false (solved)
@_in(_SETUP3)
def demo_eq_abs_02__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x))
    Residual = Abs(x) - x
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-abs-02 · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered null (no verdict)
@_in(_SETUP3)
def demo_eq_abs_02__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x))
    Residual = Abs(x) - x
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-abs-02 · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered null (no verdict)
@_in(_SETUP3)
def demo_eq_abs_02__sympy_simplify():
    x = Symbol('x', real=True, negative=True)
    Residual = Abs(x) - x
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-abs-02 · expected false · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered false (solved)
@_in(_SETUP4)
def demo_eq_abs_02__sympy_extras_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x))
    Residual = Abs(x) - x
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-abs-02 · expected false · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered null (no verdict)
@_in(_SETUP4)
def demo_eq_abs_02__sympy_extras_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x))
    Residual = Abs(x) - x
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-abs-02 · expected false · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered null (no verdict)
@_in(_SETUP4)
def demo_eq_abs_02__sympy_extras_simplify():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x))
    Residual = Abs(x) - x
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-log-01 · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (no verdict)
@_in(_SETUP1)
def demo_eq_log_01__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.positive(x))
    Residual = log(exp(x)) - x
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-log-01 · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered true (solved)
@_in(_SETUP2)
def demo_eq_log_01__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.positive(x))
    Residual = log(exp(x)) - x
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-log-01 · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered true (solved)
@_in(_SETUP2)
def demo_eq_log_01__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.positive(x))
    Residual = log(exp(x)) - x
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-log-01 · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered true (solved)
@_in(_SETUP3)
def demo_eq_log_01__sympy_auto():
    x = Symbol('x', real=True, positive=True)
    Residual = log(exp(x)) - x
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-log-01 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered true (solved)
@_in(_SETUP3)
def demo_eq_log_01__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.positive(x))
    Residual = log(exp(x)) - x
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-log-01 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered true (solved)
@_in(_SETUP3)
def demo_eq_log_01__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.positive(x))
    Residual = log(exp(x)) - x
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-log-01 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered true (solved)
@_in(_SETUP3)
def demo_eq_log_01__sympy_simplify():
    x = Symbol('x', real=True, positive=True)
    Residual = log(exp(x)) - x
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-log-01 · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered true (solved)
@_in(_SETUP4)
def demo_eq_log_01__sympy_extras_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.positive(x))
    Residual = log(exp(x)) - x
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-log-01 · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered true (solved)
@_in(_SETUP4)
def demo_eq_log_01__sympy_extras_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.positive(x))
    Residual = log(exp(x)) - x
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-log-01 · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered true (solved)
@_in(_SETUP4)
def demo_eq_log_01__sympy_extras_simplify():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.positive(x))
    Residual = log(exp(x)) - x
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-pow-01 · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (no verdict)
@_in(_SETUP1)
def demo_eq_pow_01__satassume_ask():
    n = Symbol('n')
    Assum = And(Q.integer(n))
    Residual = Pow(-1, 2 * n) - 1
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-pow-01 · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered true (solved)
@_in(_SETUP2)
def demo_eq_pow_01__satrefine_refine():
    n = Symbol('n')
    Assum = And(Q.integer(n))
    Residual = Pow(-1, 2 * n) - 1
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-pow-01 · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered true (solved)
@_in(_SETUP2)
def demo_eq_pow_01__satrefine_simplify():
    n = Symbol('n')
    Assum = And(Q.integer(n))
    Residual = Pow(-1, 2 * n) - 1
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-pow-01 · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered true (solved)
@_in(_SETUP3)
def demo_eq_pow_01__sympy_auto():
    n = Symbol('n', integer=True)
    Residual = Pow(-1, 2 * n) - 1
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-pow-01 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered true (solved)
@_in(_SETUP3)
def demo_eq_pow_01__sympy_ask():
    n = Symbol('n', integer=True)
    Assum = And(Q.integer(n))
    Residual = Pow(-1, 2 * n) - 1
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-pow-01 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered true (solved)
@_in(_SETUP3)
def demo_eq_pow_01__sympy_refine():
    n = Symbol('n', integer=True)
    Assum = And(Q.integer(n))
    Residual = Pow(-1, 2 * n) - 1
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-pow-01 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered true (solved)
@_in(_SETUP3)
def demo_eq_pow_01__sympy_simplify():
    n = Symbol('n', integer=True)
    Residual = Pow(-1, 2 * n) - 1
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-pow-01 · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered true (solved)
@_in(_SETUP4)
def demo_eq_pow_01__sympy_extras_ask():
    n = Symbol('n', integer=True)
    Assum = And(Q.integer(n))
    Residual = Pow(-1, 2 * n) - 1
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-pow-01 · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered true (solved)
@_in(_SETUP4)
def demo_eq_pow_01__sympy_extras_refine():
    n = Symbol('n', integer=True)
    Assum = And(Q.integer(n))
    Residual = Pow(-1, 2 * n) - 1
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-pow-01 · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered true (solved)
@_in(_SETUP4)
def demo_eq_pow_01__sympy_extras_simplify():
    n = Symbol('n', integer=True)
    Assum = And(Q.integer(n))
    Residual = Pow(-1, 2 * n) - 1
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-01 · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (no verdict)
@_in(_SETUP1)
def demo_eq_sqrt_01__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.positive(x))
    Residual = sqrt(Pow(x, 2)) - x
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-01 · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered true (solved)
@_in(_SETUP2)
def demo_eq_sqrt_01__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.positive(x))
    Residual = sqrt(Pow(x, 2)) - x
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-01 · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered true (solved)
@_in(_SETUP2)
def demo_eq_sqrt_01__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.positive(x))
    Residual = sqrt(Pow(x, 2)) - x
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-01 · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered true (solved)
@_in(_SETUP3)
def demo_eq_sqrt_01__sympy_auto():
    x = Symbol('x', real=True, positive=True)
    Residual = sqrt(Pow(x, 2)) - x
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-01 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered null (no verdict)
@_in(_SETUP3)
def demo_eq_sqrt_01__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.positive(x))
    Residual = sqrt(Pow(x, 2)) - x
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-01 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered true (solved)
@_in(_SETUP3)
def demo_eq_sqrt_01__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.positive(x))
    Residual = sqrt(Pow(x, 2)) - x
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-01 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered true (solved)
@_in(_SETUP3)
def demo_eq_sqrt_01__sympy_simplify():
    x = Symbol('x', real=True, positive=True)
    Residual = sqrt(Pow(x, 2)) - x
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-01 · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered true (solved)
@_in(_SETUP4)
def demo_eq_sqrt_01__sympy_extras_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.positive(x))
    Residual = sqrt(Pow(x, 2)) - x
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-01 · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered true (solved)
@_in(_SETUP4)
def demo_eq_sqrt_01__sympy_extras_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.positive(x))
    Residual = sqrt(Pow(x, 2)) - x
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-01 · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered true (solved)
@_in(_SETUP4)
def demo_eq_sqrt_01__sympy_extras_simplify():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.positive(x))
    Residual = sqrt(Pow(x, 2)) - x
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-02 · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (no verdict)
@_in(_SETUP1)
def demo_eq_sqrt_02__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sqrt(Pow(x, 2)) - Abs(x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-02 · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered true (solved)
@_in(_SETUP2)
def demo_eq_sqrt_02__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sqrt(Pow(x, 2)) - Abs(x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-02 · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered true (solved)
@_in(_SETUP2)
def demo_eq_sqrt_02__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sqrt(Pow(x, 2)) - Abs(x)
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-02 · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered true (solved)
@_in(_SETUP3)
def demo_eq_sqrt_02__sympy_auto():
    x = Symbol('x', real=True)
    Residual = sqrt(Pow(x, 2)) - Abs(x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-02 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered true (solved)
@_in(_SETUP3)
def demo_eq_sqrt_02__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = sqrt(Pow(x, 2)) - Abs(x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-02 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered true (solved)
@_in(_SETUP3)
def demo_eq_sqrt_02__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = sqrt(Pow(x, 2)) - Abs(x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-02 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered true (solved)
@_in(_SETUP3)
def demo_eq_sqrt_02__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = sqrt(Pow(x, 2)) - Abs(x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-02 · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered true (solved)
@_in(_SETUP4)
def demo_eq_sqrt_02__sympy_extras_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = sqrt(Pow(x, 2)) - Abs(x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-02 · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered true (solved)
@_in(_SETUP4)
def demo_eq_sqrt_02__sympy_extras_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = sqrt(Pow(x, 2)) - Abs(x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-02 · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered true (solved)
@_in(_SETUP4)
def demo_eq_sqrt_02__sympy_extras_simplify():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = sqrt(Pow(x, 2)) - Abs(x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-03 · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (declined correctly)
@_in(_SETUP1)
def demo_eq_sqrt_03__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sqrt(Pow(x, 2)) - x
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-03 · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered null (declined correctly)
@_in(_SETUP2)
def demo_eq_sqrt_03__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sqrt(Pow(x, 2)) - x
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-03 · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered null (declined correctly)
@_in(_SETUP2)
def demo_eq_sqrt_03__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x))
    Residual = sqrt(Pow(x, 2)) - x
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-03 · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered null (declined correctly)
@_in(_SETUP3)
def demo_eq_sqrt_03__sympy_auto():
    x = Symbol('x', real=True)
    Residual = sqrt(Pow(x, 2)) - x
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-03 · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered null (declined correctly)
@_in(_SETUP3)
def demo_eq_sqrt_03__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = sqrt(Pow(x, 2)) - x
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-03 · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered null (declined correctly)
@_in(_SETUP3)
def demo_eq_sqrt_03__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = sqrt(Pow(x, 2)) - x
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-03 · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered null (declined correctly)
@_in(_SETUP3)
def demo_eq_sqrt_03__sympy_simplify():
    x = Symbol('x', real=True)
    Residual = sqrt(Pow(x, 2)) - x
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-03 · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered null (declined correctly)
@_in(_SETUP4)
def demo_eq_sqrt_03__sympy_extras_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = sqrt(Pow(x, 2)) - x
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-03 · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered null (declined correctly)
@_in(_SETUP4)
def demo_eq_sqrt_03__sympy_extras_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = sqrt(Pow(x, 2)) - x
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-03 · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered null (declined correctly)
@_in(_SETUP4)
def demo_eq_sqrt_03__sympy_extras_simplify():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = sqrt(Pow(x, 2)) - x
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-04 · expected false · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (no verdict)
@_in(_SETUP1)
def demo_eq_sqrt_04__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.positive(x))
    Residual = sqrt(Pow(x, 2)) + 1 - x
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-04 · expected false · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered false (solved)
@_in(_SETUP2)
def demo_eq_sqrt_04__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.positive(x))
    Residual = sqrt(Pow(x, 2)) + 1 - x
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-04 · expected false · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered false (solved)
@_in(_SETUP2)
def demo_eq_sqrt_04__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.positive(x))
    Residual = sqrt(Pow(x, 2)) + 1 - x
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-04 · expected false · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered false (solved)
@_in(_SETUP3)
def demo_eq_sqrt_04__sympy_auto():
    x = Symbol('x', real=True, positive=True)
    Residual = sqrt(Pow(x, 2)) + 1 - x
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-04 · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered null (no verdict)
@_in(_SETUP3)
def demo_eq_sqrt_04__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.positive(x))
    Residual = sqrt(Pow(x, 2)) + 1 - x
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-04 · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered false (solved)
@_in(_SETUP3)
def demo_eq_sqrt_04__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.positive(x))
    Residual = sqrt(Pow(x, 2)) + 1 - x
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-04 · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered false (solved)
@_in(_SETUP3)
def demo_eq_sqrt_04__sympy_simplify():
    x = Symbol('x', real=True, positive=True)
    Residual = sqrt(Pow(x, 2)) + 1 - x
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-04 · expected false · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered false (solved)
@_in(_SETUP4)
def demo_eq_sqrt_04__sympy_extras_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.positive(x))
    Residual = sqrt(Pow(x, 2)) + 1 - x
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-04 · expected false · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered false (solved)
@_in(_SETUP4)
def demo_eq_sqrt_04__sympy_extras_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.positive(x))
    Residual = sqrt(Pow(x, 2)) + 1 - x
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-sqrt-04 · expected false · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered false (solved)
@_in(_SETUP4)
def demo_eq_sqrt_04__sympy_extras_simplify():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.positive(x))
    Residual = sqrt(Pow(x, 2)) + 1 - x
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-trig-01 · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (no verdict)
@_in(_SETUP1)
def demo_eq_trig_01__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(sin(x), 2) + Pow(cos(x), 2) - 1
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-trig-01 · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered null (no verdict)
@_in(_SETUP2)
def demo_eq_trig_01__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(sin(x), 2) + Pow(cos(x), 2) - 1
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-trig-01 · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered true (solved)
@_in(_SETUP2)
def demo_eq_trig_01__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = Pow(sin(x), 2) + Pow(cos(x), 2) - 1
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-trig-01 · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered null (no verdict)
@_in(_SETUP3)
def demo_eq_trig_01__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = Pow(sin(x), 2) + Pow(cos(x), 2) - 1
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-trig-01 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered null (no verdict)
@_in(_SETUP3)
def demo_eq_trig_01__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = Pow(sin(x), 2) + Pow(cos(x), 2) - 1
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-trig-01 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered null (no verdict)
@_in(_SETUP3)
def demo_eq_trig_01__sympy_refine():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = Pow(sin(x), 2) + Pow(cos(x), 2) - 1
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-trig-01 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered true (solved)
@_in(_SETUP3)
def demo_eq_trig_01__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = Pow(sin(x), 2) + Pow(cos(x), 2) - 1
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-trig-01 · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered true (solved)
@_in(_SETUP4)
def demo_eq_trig_01__sympy_extras_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = Pow(sin(x), 2) + Pow(cos(x), 2) - 1
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-trig-01 · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered null (no verdict)
@_in(_SETUP4)
def demo_eq_trig_01__sympy_extras_refine():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = Pow(sin(x), 2) + Pow(cos(x), 2) - 1
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-trig-01 · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered true (solved)
@_in(_SETUP4)
def demo_eq_trig_01__sympy_extras_simplify():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = Pow(sin(x), 2) + Pow(cos(x), 2) - 1
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-trig-02 · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (no verdict)
@_in(_SETUP1)
def demo_eq_trig_02__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = 2 * sin(x) * cos(x) - sin(2 * x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-trig-02 · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered null (no verdict)
@_in(_SETUP2)
def demo_eq_trig_02__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = 2 * sin(x) * cos(x) - sin(2 * x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-trig-02 · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered true (solved)
@_in(_SETUP2)
def demo_eq_trig_02__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x))
    Residual = 2 * sin(x) * cos(x) - sin(2 * x)
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-trig-02 · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered null (no verdict)
@_in(_SETUP3)
def demo_eq_trig_02__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = 2 * sin(x) * cos(x) - sin(2 * x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-trig-02 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered null (no verdict)
@_in(_SETUP3)
def demo_eq_trig_02__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = 2 * sin(x) * cos(x) - sin(2 * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-trig-02 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered null (no verdict)
@_in(_SETUP3)
def demo_eq_trig_02__sympy_refine():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = 2 * sin(x) * cos(x) - sin(2 * x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-trig-02 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered true (solved)
@_in(_SETUP3)
def demo_eq_trig_02__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = 2 * sin(x) * cos(x) - sin(2 * x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-trig-02 · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered true (solved)
@_in(_SETUP4)
def demo_eq_trig_02__sympy_extras_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = 2 * sin(x) * cos(x) - sin(2 * x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-eq-trig-02 · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered null (no verdict)
@_in(_SETUP4)
def demo_eq_trig_02__sympy_extras_refine():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = 2 * sin(x) * cos(x) - sin(2 * x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-eq-trig-02 · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered true (solved)
@_in(_SETUP4)
def demo_eq_trig_02__sympy_extras_simplify():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = 2 * sin(x) * cos(x) - sin(2 * x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-01 · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (no verdict)
@_in(_SETUP1)
def demo_log_01__satassume_ask():
    x = Symbol('x')
    y = Symbol('y')
    Assum = And(Q.real(x), Q.real(y), Q.positive(x), Q.positive(y))
    Residual = log(x * y) - (log(x) + log(y))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-log-01 · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered true (solved)
@_in(_SETUP2)
def demo_log_01__satrefine_refine():
    x = Symbol('x')
    y = Symbol('y')
    Assum = And(Q.real(x), Q.real(y), Q.positive(x), Q.positive(y))
    Residual = log(x * y) - (log(x) + log(y))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-01 · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered true (solved)
@_in(_SETUP2)
def demo_log_01__satrefine_simplify():
    x = Symbol('x')
    y = Symbol('y')
    Assum = And(Q.real(x), Q.real(y), Q.positive(x), Q.positive(y))
    Residual = log(x * y) - (log(x) + log(y))
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-01 · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered null (no verdict)
@_in(_SETUP3)
def demo_log_01__sympy_auto():
    x = Symbol('x', real=True, positive=True)
    y = Symbol('y', real=True, positive=True)
    Residual = log(x * y) - (log(x) + log(y))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-01 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered null (no verdict)
@_in(_SETUP3)
def demo_log_01__sympy_ask():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    Assum = And(Q.real(x), Q.real(y), Q.positive(x), Q.positive(y))
    Residual = log(x * y) - (log(x) + log(y))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-log-01 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered null (no verdict)
@_in(_SETUP3)
def demo_log_01__sympy_refine():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    Assum = And(Q.real(x), Q.real(y), Q.positive(x), Q.positive(y))
    Residual = log(x * y) - (log(x) + log(y))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-01 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered true (solved)
@_in(_SETUP3)
def demo_log_01__sympy_simplify():
    x = Symbol('x', real=True, positive=True)
    y = Symbol('y', real=True, positive=True)
    Residual = log(x * y) - (log(x) + log(y))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-01 · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered true (solved)
@_in(_SETUP4)
def demo_log_01__sympy_extras_ask():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    Assum = And(Q.real(x), Q.real(y), Q.positive(x), Q.positive(y))
    Residual = log(x * y) - (log(x) + log(y))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-log-01 · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered null (no verdict)
@_in(_SETUP4)
def demo_log_01__sympy_extras_refine():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    Assum = And(Q.real(x), Q.real(y), Q.positive(x), Q.positive(y))
    Residual = log(x * y) - (log(x) + log(y))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-01 · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered true (solved)
@_in(_SETUP4)
def demo_log_01__sympy_extras_simplify():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    Assum = And(Q.real(x), Q.real(y), Q.positive(x), Q.positive(y))
    Residual = log(x * y) - (log(x) + log(y))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-02 · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (declined correctly)
@_in(_SETUP1)
def demo_log_02__satassume_ask():
    z = Symbol('z')
    w = Symbol('w')
    Assum = And(Q.complex(z), Q.complex(w), ~Q.zero(z), ~Q.zero(w))
    Residual = log(z * w) - (log(z) + log(w))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-log-02 · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered null (declined correctly)
@_in(_SETUP2)
def demo_log_02__satrefine_refine():
    z = Symbol('z')
    w = Symbol('w')
    Assum = And(Q.complex(z), Q.complex(w), ~Q.zero(z), ~Q.zero(w))
    Residual = log(z * w) - (log(z) + log(w))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-02 · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered null (declined correctly)
@_in(_SETUP2)
def demo_log_02__satrefine_simplify():
    z = Symbol('z')
    w = Symbol('w')
    Assum = And(Q.complex(z), Q.complex(w), ~Q.zero(z), ~Q.zero(w))
    Residual = log(z * w) - (log(z) + log(w))
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-02 · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered null (declined correctly)
@_in(_SETUP3)
def demo_log_02__sympy_auto():
    z = Symbol('z', complex=True, zero=False)
    w = Symbol('w', complex=True, zero=False)
    Residual = log(z * w) - (log(z) + log(w))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-02 · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered null (declined correctly)
@_in(_SETUP3)
def demo_log_02__sympy_ask():
    z = Symbol('z', complex=True)
    w = Symbol('w', complex=True)
    Assum = And(Q.complex(z), Q.complex(w), ~Q.zero(z), ~Q.zero(w))
    Residual = log(z * w) - (log(z) + log(w))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-log-02 · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered null (declined correctly)
@_in(_SETUP3)
def demo_log_02__sympy_refine():
    z = Symbol('z', complex=True)
    w = Symbol('w', complex=True)
    Assum = And(Q.complex(z), Q.complex(w), ~Q.zero(z), ~Q.zero(w))
    Residual = log(z * w) - (log(z) + log(w))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-02 · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered null (declined correctly)
@_in(_SETUP3)
def demo_log_02__sympy_simplify():
    z = Symbol('z', complex=True, zero=False)
    w = Symbol('w', complex=True, zero=False)
    Residual = log(z * w) - (log(z) + log(w))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-02 · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered null (declined correctly)
@_in(_SETUP4)
def demo_log_02__sympy_extras_ask():
    z = Symbol('z', complex=True)
    w = Symbol('w', complex=True)
    Assum = And(Q.complex(z), Q.complex(w), ~Q.zero(z), ~Q.zero(w))
    Residual = log(z * w) - (log(z) + log(w))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-log-02 · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered null (declined correctly)
@_in(_SETUP4)
def demo_log_02__sympy_extras_refine():
    z = Symbol('z', complex=True)
    w = Symbol('w', complex=True)
    Assum = And(Q.complex(z), Q.complex(w), ~Q.zero(z), ~Q.zero(w))
    Residual = log(z * w) - (log(z) + log(w))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-02 · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered null (declined correctly)
@_in(_SETUP4)
def demo_log_02__sympy_extras_simplify():
    z = Symbol('z', complex=True)
    w = Symbol('w', complex=True)
    Assum = And(Q.complex(z), Q.complex(w), ~Q.zero(z), ~Q.zero(w))
    Residual = log(z * w) - (log(z) + log(w))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-03 · expected false · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered false (solved)
@_in(_SETUP1)
def demo_log_03__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.negative(x))
    Residual = log(x) - log(-x)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-log-03 · expected false · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered false (solved)
@_in(_SETUP2)
def demo_log_03__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.negative(x))
    Residual = log(x) - log(-x)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-03 · expected false · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered false (solved)
@_in(_SETUP2)
def demo_log_03__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.negative(x))
    Residual = log(x) - log(-x)
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-03 · expected false · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered null (no verdict)
@_in(_SETUP3)
def demo_log_03__sympy_auto():
    x = Symbol('x', real=True, negative=True)
    Residual = log(x) - log(-x)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-03 · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered false (solved)
@_in(_SETUP3)
def demo_log_03__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x))
    Residual = log(x) - log(-x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-log-03 · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered null (no verdict)
@_in(_SETUP3)
def demo_log_03__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x))
    Residual = log(x) - log(-x)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-03 · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered false (solved)
@_in(_SETUP3)
def demo_log_03__sympy_simplify():
    x = Symbol('x', real=True, negative=True)
    Residual = log(x) - log(-x)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-03 · expected false · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered null (no verdict)
@_in(_SETUP4)
def demo_log_03__sympy_extras_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x))
    Residual = log(x) - log(-x)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-log-03 · expected false · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered null (no verdict)
@_in(_SETUP4)
def demo_log_03__sympy_extras_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x))
    Residual = log(x) - log(-x)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-log-03 · expected false · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered false (solved)
@_in(_SETUP4)
def demo_log_03__sympy_extras_simplify():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x))
    Residual = log(x) - log(-x)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-nonzero-01 · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (no verdict)
@_in(_SETUP1)
def demo_nonzero_01__satassume_ask():
    z = Symbol('z')
    Assum = And(Q.complex(z), Q.imaginary(z))
    Residual = Abs(sign(z)) - 1
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-nonzero-01 · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered true (solved)
@_in(_SETUP2)
def demo_nonzero_01__satrefine_refine():
    z = Symbol('z')
    Assum = And(Q.complex(z), Q.imaginary(z))
    Residual = Abs(sign(z)) - 1
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-nonzero-01 · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered true (solved)
@_in(_SETUP2)
def demo_nonzero_01__satrefine_simplify():
    z = Symbol('z')
    Assum = And(Q.complex(z), Q.imaginary(z))
    Residual = Abs(sign(z)) - 1
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-nonzero-01 · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered true (solved)
@_in(_SETUP3)
def demo_nonzero_01__sympy_auto():
    z = Symbol('z', complex=True, imaginary=True)
    Residual = Abs(sign(z)) - 1
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-nonzero-01 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered null (no verdict)
@_in(_SETUP3)
def demo_nonzero_01__sympy_ask():
    z = Symbol('z', complex=True)
    Assum = And(Q.complex(z), Q.imaginary(z))
    Residual = Abs(sign(z)) - 1
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-nonzero-01 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered null (no verdict)
@_in(_SETUP3)
def demo_nonzero_01__sympy_refine():
    z = Symbol('z', complex=True)
    Assum = And(Q.complex(z), Q.imaginary(z))
    Residual = Abs(sign(z)) - 1
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-nonzero-01 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered true (solved)
@_in(_SETUP3)
def demo_nonzero_01__sympy_simplify():
    z = Symbol('z', complex=True, imaginary=True)
    Residual = Abs(sign(z)) - 1
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-nonzero-01 · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered null (no verdict)
@_in(_SETUP4)
def demo_nonzero_01__sympy_extras_ask():
    z = Symbol('z', complex=True)
    Assum = And(Q.complex(z), Q.imaginary(z))
    Residual = Abs(sign(z)) - 1
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-nonzero-01 · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered null (no verdict)
@_in(_SETUP4)
def demo_nonzero_01__sympy_extras_refine():
    z = Symbol('z', complex=True)
    Assum = And(Q.complex(z), Q.imaginary(z))
    Residual = Abs(sign(z)) - 1
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-nonzero-01 · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered null (no verdict)
@_in(_SETUP4)
def demo_nonzero_01__sympy_extras_simplify():
    z = Symbol('z', complex=True)
    Assum = And(Q.complex(z), Q.imaginary(z))
    Residual = Abs(sign(z)) - 1
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-01 · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (no verdict)
@_in(_SETUP1)
def demo_parity_01__satassume_ask():
    n = Symbol('n')
    Assum = And(Q.integer(n), Q.odd(n))
    Residual = Pow(-1, n + 1) - 1
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-parity-01 · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered true (solved)
@_in(_SETUP2)
def demo_parity_01__satrefine_refine():
    n = Symbol('n')
    Assum = And(Q.integer(n), Q.odd(n))
    Residual = Pow(-1, n + 1) - 1
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-01 · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered true (solved)
@_in(_SETUP2)
def demo_parity_01__satrefine_simplify():
    n = Symbol('n')
    Assum = And(Q.integer(n), Q.odd(n))
    Residual = Pow(-1, n + 1) - 1
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-01 · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered true (solved)
@_in(_SETUP3)
def demo_parity_01__sympy_auto():
    n = Symbol('n', integer=True, odd=True)
    Residual = Pow(-1, n + 1) - 1
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-01 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered null (no verdict)
@_in(_SETUP3)
def demo_parity_01__sympy_ask():
    n = Symbol('n', integer=True)
    Assum = And(Q.integer(n), Q.odd(n))
    Residual = Pow(-1, n + 1) - 1
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-parity-01 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered true (solved)
@_in(_SETUP3)
def demo_parity_01__sympy_refine():
    n = Symbol('n', integer=True)
    Assum = And(Q.integer(n), Q.odd(n))
    Residual = Pow(-1, n + 1) - 1
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-01 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered true (solved)
@_in(_SETUP3)
def demo_parity_01__sympy_simplify():
    n = Symbol('n', integer=True, odd=True)
    Residual = Pow(-1, n + 1) - 1
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-01 · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered null (no verdict)
@_in(_SETUP4)
def demo_parity_01__sympy_extras_ask():
    n = Symbol('n', integer=True)
    Assum = And(Q.integer(n), Q.odd(n))
    Residual = Pow(-1, n + 1) - 1
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-parity-01 · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered true (solved)
@_in(_SETUP4)
def demo_parity_01__sympy_extras_refine():
    n = Symbol('n', integer=True)
    Assum = And(Q.integer(n), Q.odd(n))
    Residual = Pow(-1, n + 1) - 1
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-01 · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered true (solved)
@_in(_SETUP4)
def demo_parity_01__sympy_extras_simplify():
    n = Symbol('n', integer=True)
    Assum = And(Q.integer(n), Q.odd(n))
    Residual = Pow(-1, n + 1) - 1
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-02 · expected false · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered false (solved)
@_in(_SETUP1)
def demo_parity_02__satassume_ask():
    n = Symbol('n')
    m = Symbol('m')
    Assum = And(Q.integer(n), Q.integer(m), Q.odd(n), Q.odd(m))
    Residual = Pow(-1, n * m) - 1
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-parity-02 · expected false · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered false (solved)
@_in(_SETUP2)
def demo_parity_02__satrefine_refine():
    n = Symbol('n')
    m = Symbol('m')
    Assum = And(Q.integer(n), Q.integer(m), Q.odd(n), Q.odd(m))
    Residual = Pow(-1, n * m) - 1
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-02 · expected false · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered false (solved)
@_in(_SETUP2)
def demo_parity_02__satrefine_simplify():
    n = Symbol('n')
    m = Symbol('m')
    Assum = And(Q.integer(n), Q.integer(m), Q.odd(n), Q.odd(m))
    Residual = Pow(-1, n * m) - 1
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-02 · expected false · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered false (solved)
@_in(_SETUP3)
def demo_parity_02__sympy_auto():
    n = Symbol('n', integer=True, odd=True)
    m = Symbol('m', integer=True, odd=True)
    Residual = Pow(-1, n * m) - 1
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-02 · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered false (solved)
@_in(_SETUP3)
def demo_parity_02__sympy_ask():
    n = Symbol('n', integer=True)
    m = Symbol('m', integer=True)
    Assum = And(Q.integer(n), Q.integer(m), Q.odd(n), Q.odd(m))
    Residual = Pow(-1, n * m) - 1
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-parity-02 · expected false · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered false (solved)
@_in(_SETUP3)
def demo_parity_02__sympy_refine():
    n = Symbol('n', integer=True)
    m = Symbol('m', integer=True)
    Assum = And(Q.integer(n), Q.integer(m), Q.odd(n), Q.odd(m))
    Residual = Pow(-1, n * m) - 1
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-02 · expected false · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered false (solved)
@_in(_SETUP3)
def demo_parity_02__sympy_simplify():
    n = Symbol('n', integer=True, odd=True)
    m = Symbol('m', integer=True, odd=True)
    Residual = Pow(-1, n * m) - 1
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-02 · expected false · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered false (solved)
@_in(_SETUP4)
def demo_parity_02__sympy_extras_ask():
    n = Symbol('n', integer=True)
    m = Symbol('m', integer=True)
    Assum = And(Q.integer(n), Q.integer(m), Q.odd(n), Q.odd(m))
    Residual = Pow(-1, n * m) - 1
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-parity-02 · expected false · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered false (solved)
@_in(_SETUP4)
def demo_parity_02__sympy_extras_refine():
    n = Symbol('n', integer=True)
    m = Symbol('m', integer=True)
    Assum = And(Q.integer(n), Q.integer(m), Q.odd(n), Q.odd(m))
    Residual = Pow(-1, n * m) - 1
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-02 · expected false · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered false (solved)
@_in(_SETUP4)
def demo_parity_02__sympy_extras_simplify():
    n = Symbol('n', integer=True)
    m = Symbol('m', integer=True)
    Assum = And(Q.integer(n), Q.integer(m), Q.odd(n), Q.odd(m))
    Residual = Pow(-1, n * m) - 1
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-03 · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (no verdict)
@_in(_SETUP1)
def demo_parity_03__satassume_ask():
    n = Symbol('n')
    Assum = And(Q.integer(n))
    Residual = Pow(-1, n * (n + 1)) - 1
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-parity-03 · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered true (solved)
@_in(_SETUP2)
def demo_parity_03__satrefine_refine():
    n = Symbol('n')
    Assum = And(Q.integer(n))
    Residual = Pow(-1, n * (n + 1)) - 1
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-03 · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered true (solved)
@_in(_SETUP2)
def demo_parity_03__satrefine_simplify():
    n = Symbol('n')
    Assum = And(Q.integer(n))
    Residual = Pow(-1, n * (n + 1)) - 1
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-03 · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered true (solved)
@_in(_SETUP3)
def demo_parity_03__sympy_auto():
    n = Symbol('n', integer=True)
    Residual = Pow(-1, n * (n + 1)) - 1
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-03 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered true (solved)
@_in(_SETUP3)
def demo_parity_03__sympy_ask():
    n = Symbol('n', integer=True)
    Assum = And(Q.integer(n))
    Residual = Pow(-1, n * (n + 1)) - 1
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-parity-03 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered true (solved)
@_in(_SETUP3)
def demo_parity_03__sympy_refine():
    n = Symbol('n', integer=True)
    Assum = And(Q.integer(n))
    Residual = Pow(-1, n * (n + 1)) - 1
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-03 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered true (solved)
@_in(_SETUP3)
def demo_parity_03__sympy_simplify():
    n = Symbol('n', integer=True)
    Residual = Pow(-1, n * (n + 1)) - 1
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-03 · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered true (solved)
@_in(_SETUP4)
def demo_parity_03__sympy_extras_ask():
    n = Symbol('n', integer=True)
    Assum = And(Q.integer(n))
    Residual = Pow(-1, n * (n + 1)) - 1
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-parity-03 · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered true (solved)
@_in(_SETUP4)
def demo_parity_03__sympy_extras_refine():
    n = Symbol('n', integer=True)
    Assum = And(Q.integer(n))
    Residual = Pow(-1, n * (n + 1)) - 1
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-03 · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered true (solved)
@_in(_SETUP4)
def demo_parity_03__sympy_extras_simplify():
    n = Symbol('n', integer=True)
    Assum = And(Q.integer(n))
    Residual = Pow(-1, n * (n + 1)) - 1
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-04 · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (declined correctly)
@_in(_SETUP1)
def demo_parity_04__satassume_ask():
    n = Symbol('n')
    Assum = And(Q.integer(n), Q.even(n))
    Residual = Pow(I, n) - 1
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-parity-04 · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered null (declined correctly)
@_in(_SETUP2)
def demo_parity_04__satrefine_refine():
    n = Symbol('n')
    Assum = And(Q.integer(n), Q.even(n))
    Residual = Pow(I, n) - 1
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-04 · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered null (declined correctly)
@_in(_SETUP2)
def demo_parity_04__satrefine_simplify():
    n = Symbol('n')
    Assum = And(Q.integer(n), Q.even(n))
    Residual = Pow(I, n) - 1
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-04 · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered null (declined correctly)
@_in(_SETUP3)
def demo_parity_04__sympy_auto():
    n = Symbol('n', integer=True, even=True)
    Residual = Pow(I, n) - 1
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-04 · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered null (declined correctly)
@_in(_SETUP3)
def demo_parity_04__sympy_ask():
    n = Symbol('n', integer=True)
    Assum = And(Q.integer(n), Q.even(n))
    Residual = Pow(I, n) - 1
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-parity-04 · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered null (declined correctly)
@_in(_SETUP3)
def demo_parity_04__sympy_refine():
    n = Symbol('n', integer=True)
    Assum = And(Q.integer(n), Q.even(n))
    Residual = Pow(I, n) - 1
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-04 · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered null (declined correctly)
@_in(_SETUP3)
def demo_parity_04__sympy_simplify():
    n = Symbol('n', integer=True, even=True)
    Residual = Pow(I, n) - 1
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-04 · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered null (declined correctly)
@_in(_SETUP4)
def demo_parity_04__sympy_extras_ask():
    n = Symbol('n', integer=True)
    Assum = And(Q.integer(n), Q.even(n))
    Residual = Pow(I, n) - 1
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-parity-04 · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered null (declined correctly)
@_in(_SETUP4)
def demo_parity_04__sympy_extras_refine():
    n = Symbol('n', integer=True)
    Assum = And(Q.integer(n), Q.even(n))
    Residual = Pow(I, n) - 1
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-04 · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered null (declined correctly)
@_in(_SETUP4)
def demo_parity_04__sympy_extras_simplify():
    n = Symbol('n', integer=True)
    Assum = And(Q.integer(n), Q.even(n))
    Residual = Pow(I, n) - 1
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-05 · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (no verdict)
@_in(_SETUP1)
def demo_parity_05__satassume_ask():
    n = Symbol('n')
    m = Symbol('m')
    Assum = And(Q.integer(n), Q.integer(m), Q.odd(n), Q.odd(m))
    Residual = Pow(-1, n * m) - (-1)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-parity-05 · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered true (solved)
@_in(_SETUP2)
def demo_parity_05__satrefine_refine():
    n = Symbol('n')
    m = Symbol('m')
    Assum = And(Q.integer(n), Q.integer(m), Q.odd(n), Q.odd(m))
    Residual = Pow(-1, n * m) - (-1)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-05 · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered true (solved)
@_in(_SETUP2)
def demo_parity_05__satrefine_simplify():
    n = Symbol('n')
    m = Symbol('m')
    Assum = And(Q.integer(n), Q.integer(m), Q.odd(n), Q.odd(m))
    Residual = Pow(-1, n * m) - (-1)
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-05 · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered true (solved)
@_in(_SETUP3)
def demo_parity_05__sympy_auto():
    n = Symbol('n', integer=True, odd=True)
    m = Symbol('m', integer=True, odd=True)
    Residual = Pow(-1, n * m) - (-1)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-05 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered null (no verdict)
@_in(_SETUP3)
def demo_parity_05__sympy_ask():
    n = Symbol('n', integer=True)
    m = Symbol('m', integer=True)
    Assum = And(Q.integer(n), Q.integer(m), Q.odd(n), Q.odd(m))
    Residual = Pow(-1, n * m) - (-1)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-parity-05 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered true (solved)
@_in(_SETUP3)
def demo_parity_05__sympy_refine():
    n = Symbol('n', integer=True)
    m = Symbol('m', integer=True)
    Assum = And(Q.integer(n), Q.integer(m), Q.odd(n), Q.odd(m))
    Residual = Pow(-1, n * m) - (-1)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-05 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered true (solved)
@_in(_SETUP3)
def demo_parity_05__sympy_simplify():
    n = Symbol('n', integer=True, odd=True)
    m = Symbol('m', integer=True, odd=True)
    Residual = Pow(-1, n * m) - (-1)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-05 · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered null (no verdict)
@_in(_SETUP4)
def demo_parity_05__sympy_extras_ask():
    n = Symbol('n', integer=True)
    m = Symbol('m', integer=True)
    Assum = And(Q.integer(n), Q.integer(m), Q.odd(n), Q.odd(m))
    Residual = Pow(-1, n * m) - (-1)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-parity-05 · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered true (solved)
@_in(_SETUP4)
def demo_parity_05__sympy_extras_refine():
    n = Symbol('n', integer=True)
    m = Symbol('m', integer=True)
    Assum = And(Q.integer(n), Q.integer(m), Q.odd(n), Q.odd(m))
    Residual = Pow(-1, n * m) - (-1)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-parity-05 · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered true (solved)
@_in(_SETUP4)
def demo_parity_05__sympy_extras_simplify():
    n = Symbol('n', integer=True)
    m = Symbol('m', integer=True)
    Assum = And(Q.integer(n), Q.integer(m), Q.odd(n), Q.odd(m))
    Residual = Pow(-1, n * m) - (-1)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-prime-01 · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (no verdict)
@_in(_SETUP1)
def demo_prime_01__satassume_ask():
    p = Symbol('p')
    Assum = And(Q.integer(p), Q.prime(p), p > 2)
    Residual = Pow(-1, p) - (-1)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-prime-01 · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered null (no verdict)
@_in(_SETUP2)
def demo_prime_01__satrefine_refine():
    p = Symbol('p')
    Assum = And(Q.integer(p), Q.prime(p), p > 2)
    Residual = Pow(-1, p) - (-1)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-prime-01 · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered null (no verdict)
@_in(_SETUP2)
def demo_prime_01__satrefine_simplify():
    p = Symbol('p')
    Assum = And(Q.integer(p), Q.prime(p), p > 2)
    Residual = Pow(-1, p) - (-1)
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-prime-01 · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered null (no verdict)
@_in(_SETUP3)
def demo_prime_01__sympy_auto():
    p = Symbol('p', integer=True, prime=True)
    Residual = Pow(-1, p) - (-1)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-prime-01 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered null (no verdict)
@_in(_SETUP3)
def demo_prime_01__sympy_ask():
    p = Symbol('p', integer=True)
    Assum = And(Q.integer(p), Q.prime(p), p > 2)
    Residual = Pow(-1, p) - (-1)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-prime-01 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered null (no verdict)
@_in(_SETUP3)
def demo_prime_01__sympy_refine():
    p = Symbol('p', integer=True)
    Assum = And(Q.integer(p), Q.prime(p), p > 2)
    Residual = Pow(-1, p) - (-1)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-prime-01 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered null (no verdict)
@_in(_SETUP3)
def demo_prime_01__sympy_simplify():
    p = Symbol('p', integer=True, prime=True)
    Residual = Pow(-1, p) - (-1)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-prime-01 · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered null (no verdict)
@_in(_SETUP4)
def demo_prime_01__sympy_extras_ask():
    p = Symbol('p', integer=True)
    Assum = And(Q.integer(p), Q.prime(p), p > 2)
    Residual = Pow(-1, p) - (-1)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-prime-01 · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered null (no verdict)
@_in(_SETUP4)
def demo_prime_01__sympy_extras_refine():
    p = Symbol('p', integer=True)
    Assum = And(Q.integer(p), Q.prime(p), p > 2)
    Residual = Pow(-1, p) - (-1)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-prime-01 · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered null (no verdict)
@_in(_SETUP4)
def demo_prime_01__sympy_extras_simplify():
    p = Symbol('p', integer=True)
    Assum = And(Q.integer(p), Q.prime(p), p > 2)
    Residual = Pow(-1, p) - (-1)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-prime-02 · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (declined correctly)
@_in(_SETUP1)
def demo_prime_02__satassume_ask():
    p = Symbol('p')
    Assum = And(Q.integer(p), Q.prime(p))
    Residual = Pow(-1, p) - (-1)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-prime-02 · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered null (declined correctly)
@_in(_SETUP2)
def demo_prime_02__satrefine_refine():
    p = Symbol('p')
    Assum = And(Q.integer(p), Q.prime(p))
    Residual = Pow(-1, p) - (-1)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-prime-02 · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered null (declined correctly)
@_in(_SETUP2)
def demo_prime_02__satrefine_simplify():
    p = Symbol('p')
    Assum = And(Q.integer(p), Q.prime(p))
    Residual = Pow(-1, p) - (-1)
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-prime-02 · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered null (declined correctly)
@_in(_SETUP3)
def demo_prime_02__sympy_auto():
    p = Symbol('p', integer=True, prime=True)
    Residual = Pow(-1, p) - (-1)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-prime-02 · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered null (declined correctly)
@_in(_SETUP3)
def demo_prime_02__sympy_ask():
    p = Symbol('p', integer=True)
    Assum = And(Q.integer(p), Q.prime(p))
    Residual = Pow(-1, p) - (-1)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-prime-02 · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered null (declined correctly)
@_in(_SETUP3)
def demo_prime_02__sympy_refine():
    p = Symbol('p', integer=True)
    Assum = And(Q.integer(p), Q.prime(p))
    Residual = Pow(-1, p) - (-1)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-prime-02 · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered null (declined correctly)
@_in(_SETUP3)
def demo_prime_02__sympy_simplify():
    p = Symbol('p', integer=True, prime=True)
    Residual = Pow(-1, p) - (-1)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-prime-02 · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered null (declined correctly)
@_in(_SETUP4)
def demo_prime_02__sympy_extras_ask():
    p = Symbol('p', integer=True)
    Assum = And(Q.integer(p), Q.prime(p))
    Residual = Pow(-1, p) - (-1)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-prime-02 · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered null (declined correctly)
@_in(_SETUP4)
def demo_prime_02__sympy_extras_refine():
    p = Symbol('p', integer=True)
    Assum = And(Q.integer(p), Q.prime(p))
    Residual = Pow(-1, p) - (-1)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-prime-02 · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered null (declined correctly)
@_in(_SETUP4)
def demo_prime_02__sympy_extras_simplify():
    p = Symbol('p', integer=True)
    Assum = And(Q.integer(p), Q.prime(p))
    Residual = Pow(-1, p) - (-1)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-02 · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (no verdict)
@_in(_SETUP1)
def demo_sign_02__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = sign(Pow(x, 2)) - 1
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-sign-02 · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered true (solved)
@_in(_SETUP2)
def demo_sign_02__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = sign(Pow(x, 2)) - 1
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-02 · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered true (solved)
@_in(_SETUP2)
def demo_sign_02__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = sign(Pow(x, 2)) - 1
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-02 · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered true (solved)
@_in(_SETUP3)
def demo_sign_02__sympy_auto():
    x = Symbol('x', real=True, zero=False)
    Residual = sign(Pow(x, 2)) - 1
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-02 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered null (no verdict)
@_in(_SETUP3)
def demo_sign_02__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = sign(Pow(x, 2)) - 1
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-sign-02 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered true (solved)
@_in(_SETUP3)
def demo_sign_02__sympy_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = sign(Pow(x, 2)) - 1
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-02 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered true (solved)
@_in(_SETUP3)
def demo_sign_02__sympy_simplify():
    x = Symbol('x', real=True, zero=False)
    Residual = sign(Pow(x, 2)) - 1
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-02 · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered null (no verdict)
@_in(_SETUP4)
def demo_sign_02__sympy_extras_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = sign(Pow(x, 2)) - 1
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-sign-02 · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered true (solved)
@_in(_SETUP4)
def demo_sign_02__sympy_extras_refine():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = sign(Pow(x, 2)) - 1
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-02 · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered true (solved)
@_in(_SETUP4)
def demo_sign_02__sympy_extras_simplify():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = sign(Pow(x, 2)) - 1
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-03 · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (declined correctly)
@_in(_SETUP1)
def demo_sign_03__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = sign(Pow(x, 2)) - 1
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-sign-03 · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered null (declined correctly)
@_in(_SETUP2)
def demo_sign_03__satrefine_refine():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = sign(Pow(x, 2)) - 1
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-03 · expected contingent · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered null (declined correctly)
@_in(_SETUP2)
def demo_sign_03__satrefine_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = sign(Pow(x, 2)) - 1
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-03 · expected contingent · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered null (declined correctly)
@_in(_SETUP3)
def demo_sign_03__sympy_auto():
    x = Symbol('x', complex=True, zero=False)
    Residual = sign(Pow(x, 2)) - 1
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-03 · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered null (declined correctly)
@_in(_SETUP3)
def demo_sign_03__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = sign(Pow(x, 2)) - 1
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-sign-03 · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered null (declined correctly)
@_in(_SETUP3)
def demo_sign_03__sympy_refine():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = sign(Pow(x, 2)) - 1
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-03 · expected contingent · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered null (declined correctly)
@_in(_SETUP3)
def demo_sign_03__sympy_simplify():
    x = Symbol('x', complex=True, zero=False)
    Residual = sign(Pow(x, 2)) - 1
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-03 · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered null (declined correctly)
@_in(_SETUP4)
def demo_sign_03__sympy_extras_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = sign(Pow(x, 2)) - 1
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-sign-03 · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered null (declined correctly)
@_in(_SETUP4)
def demo_sign_03__sympy_extras_refine():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = sign(Pow(x, 2)) - 1
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-03 · expected contingent · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered null (declined correctly)
@_in(_SETUP4)
def demo_sign_03__sympy_extras_simplify():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = sign(Pow(x, 2)) - 1
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-04 · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (no verdict)
@_in(_SETUP1)
def demo_sign_04__satassume_ask():
    z = Symbol('z')
    Assum = And(Q.complex(z))
    Residual = Abs(z * conjugate(z)) - (z * conjugate(z))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-sign-04 · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered true (solved)
@_in(_SETUP2)
def demo_sign_04__satrefine_refine():
    z = Symbol('z')
    Assum = And(Q.complex(z))
    Residual = Abs(z * conjugate(z)) - (z * conjugate(z))
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-04 · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered true (solved)
@_in(_SETUP2)
def demo_sign_04__satrefine_simplify():
    z = Symbol('z')
    Assum = And(Q.complex(z))
    Residual = Abs(z * conjugate(z)) - (z * conjugate(z))
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-04 · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered null (no verdict)
@_in(_SETUP3)
def demo_sign_04__sympy_auto():
    z = Symbol('z', complex=True)
    Residual = Abs(z * conjugate(z)) - (z * conjugate(z))
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-04 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered null (no verdict)
@_in(_SETUP3)
def demo_sign_04__sympy_ask():
    z = Symbol('z', complex=True)
    Assum = And(Q.complex(z))
    Residual = Abs(z * conjugate(z)) - (z * conjugate(z))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-sign-04 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered null (no verdict)
@_in(_SETUP3)
def demo_sign_04__sympy_refine():
    z = Symbol('z', complex=True)
    Assum = And(Q.complex(z))
    Residual = Abs(z * conjugate(z)) - (z * conjugate(z))
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-04 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered null (no verdict)
@_in(_SETUP3)
def demo_sign_04__sympy_simplify():
    z = Symbol('z', complex=True)
    Residual = Abs(z * conjugate(z)) - (z * conjugate(z))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-04 · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered null (no verdict)
@_in(_SETUP4)
def demo_sign_04__sympy_extras_ask():
    z = Symbol('z', complex=True)
    Assum = And(Q.complex(z))
    Residual = Abs(z * conjugate(z)) - (z * conjugate(z))
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-sign-04 · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered null (no verdict)
@_in(_SETUP4)
def demo_sign_04__sympy_extras_refine():
    z = Symbol('z', complex=True)
    Assum = And(Q.complex(z))
    Residual = Abs(z * conjugate(z)) - (z * conjugate(z))
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-04 · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered null (no verdict)
@_in(_SETUP4)
def demo_sign_04__sympy_extras_simplify():
    z = Symbol('z', complex=True)
    Assum = And(Q.complex(z))
    Residual = Abs(z * conjugate(z)) - (z * conjugate(z))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-05 · expected true · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261019-041805 answered null (no verdict)
@_in(_SETUP1)
def demo_sign_05__satassume_ask():
    x = Symbol('x')
    y = Symbol('y')
    Assum = And(Q.real(x), Q.real(y), Q.positive(x), Q.negative(y))
    Residual = Abs(x - y) - (x - y)
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-sign-05 · expected true · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261019-074829 answered true (solved)
@_in(_SETUP2)
def demo_sign_05__satrefine_refine():
    x = Symbol('x')
    y = Symbol('y')
    Assum = And(Q.real(x), Q.real(y), Q.positive(x), Q.negative(y))
    Residual = Abs(x - y) - (x - y)
    Result = satsimp.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-05 · expected true · system satrefine-simplify (satsimp 0.1.0)
# the run satrefine-simplify-20261019-041807 answered true (solved)
@_in(_SETUP2)
def demo_sign_05__satrefine_simplify():
    x = Symbol('x')
    y = Symbol('y')
    Assum = And(Q.real(x), Q.real(y), Q.positive(x), Q.negative(y))
    Residual = Abs(x - y) - (x - y)
    Result = simplify(satsimp.refine(Residual, Assum))
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-05 · expected true · system sympy-auto (sympy 1.14.0)
# the run sympy-auto-20261019-040938 answered true (solved)
@_in(_SETUP3)
def demo_sign_05__sympy_auto():
    x = Symbol('x', real=True, positive=True)
    y = Symbol('y', real=True, negative=True)
    Residual = Abs(x - y) - (x - y)
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-05 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261019-040940 answered null (no verdict)
@_in(_SETUP3)
def demo_sign_05__sympy_ask():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    Assum = And(Q.real(x), Q.real(y), Q.positive(x), Q.negative(y))
    Residual = Abs(x - y) - (x - y)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-sign-05 · expected true · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261019-040943 answered true (solved)
@_in(_SETUP3)
def demo_sign_05__sympy_refine():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    Assum = And(Q.real(x), Q.real(y), Q.positive(x), Q.negative(y))
    Residual = Abs(x - y) - (x - y)
    Result = refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-05 · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-040945 answered true (solved)
@_in(_SETUP3)
def demo_sign_05__sympy_simplify():
    x = Symbol('x', real=True, positive=True)
    y = Symbol('y', real=True, negative=True)
    Residual = Abs(x - y) - (x - y)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-05 · expected true · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261019-041809 answered true (solved)
@_in(_SETUP4)
def demo_sign_05__sympy_extras_ask():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    Assum = And(Q.real(x), Q.real(y), Q.positive(x), Q.negative(y))
    Residual = Abs(x - y) - (x - y)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case demo-sign-05 · expected true · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261019-041814 answered true (solved)
@_in(_SETUP4)
def demo_sign_05__sympy_extras_refine():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    Assum = And(Q.real(x), Q.real(y), Q.positive(x), Q.negative(y))
    Residual = Abs(x - y) - (x - y)
    Result = sympy_extras.assumptions.refine(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case demo-sign-05 · expected true · system sympy-extras-simplify (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-simplify-20261019-041817 answered true (solved)
@_in(_SETUP4)
def demo_sign_05__sympy_extras_simplify():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    Assum = And(Q.real(x), Q.real(y), Q.positive(x), Q.negative(y))
    Residual = Abs(x - y) - (x - y)
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# (case, system, expected, the stored run's answer, that run, its function)
CASES = [
    ('demo-atan2-01', 'satassume-ask', 'true', 'null', 'satassume-ask-20261019-041805', demo_atan2_01__satassume_ask),
    ('demo-atan2-01', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-074829', demo_atan2_01__satrefine_refine),
    ('demo-atan2-01', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261019-041807', demo_atan2_01__satrefine_simplify),
    ('demo-atan2-01', 'sympy-auto', 'true', 'true', 'sympy-auto-20261019-040938', demo_atan2_01__sympy_auto),
    ('demo-atan2-01', 'sympy-ask', 'true', 'null', 'sympy-ask-20261019-040940', demo_atan2_01__sympy_ask),
    ('demo-atan2-01', 'sympy-refine', 'true', 'true', 'sympy-refine-20261019-040943', demo_atan2_01__sympy_refine),
    ('demo-atan2-01', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-040945', demo_atan2_01__sympy_simplify),
    ('demo-atan2-01', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261019-041809', demo_atan2_01__sympy_extras_ask),
    ('demo-atan2-01', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261019-041814', demo_atan2_01__sympy_extras_refine),
    ('demo-atan2-01', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261019-041817', demo_atan2_01__sympy_extras_simplify),
    ('demo-atan2-02', 'satassume-ask', 'false', 'null', 'satassume-ask-20261019-041805', demo_atan2_02__satassume_ask),
    ('demo-atan2-02', 'satrefine-refine', 'false', 'false', 'satrefine-refine-20261019-074829', demo_atan2_02__satrefine_refine),
    ('demo-atan2-02', 'satrefine-simplify', 'false', 'false', 'satrefine-simplify-20261019-041807', demo_atan2_02__satrefine_simplify),
    ('demo-atan2-02', 'sympy-auto', 'false', 'false', 'sympy-auto-20261019-040938', demo_atan2_02__sympy_auto),
    ('demo-atan2-02', 'sympy-ask', 'false', 'null', 'sympy-ask-20261019-040940', demo_atan2_02__sympy_ask),
    ('demo-atan2-02', 'sympy-refine', 'false', 'false', 'sympy-refine-20261019-040943', demo_atan2_02__sympy_refine),
    ('demo-atan2-02', 'sympy-simplify', 'false', 'false', 'sympy-simplify-20261019-040945', demo_atan2_02__sympy_simplify),
    ('demo-atan2-02', 'sympy-extras-ask', 'false', 'null', 'sympy-extras-ask-20261019-041809', demo_atan2_02__sympy_extras_ask),
    ('demo-atan2-02', 'sympy-extras-refine', 'false', 'false', 'sympy-extras-refine-20261019-041814', demo_atan2_02__sympy_extras_refine),
    ('demo-atan2-02', 'sympy-extras-simplify', 'false', 'false', 'sympy-extras-simplify-20261019-041817', demo_atan2_02__sympy_extras_simplify),
    ('demo-eq-abs-01', 'satassume-ask', 'true', 'null', 'satassume-ask-20261019-041805', demo_eq_abs_01__satassume_ask),
    ('demo-eq-abs-01', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-074829', demo_eq_abs_01__satrefine_refine),
    ('demo-eq-abs-01', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261019-041807', demo_eq_abs_01__satrefine_simplify),
    ('demo-eq-abs-01', 'sympy-auto', 'true', 'true', 'sympy-auto-20261019-040938', demo_eq_abs_01__sympy_auto),
    ('demo-eq-abs-01', 'sympy-ask', 'true', 'null', 'sympy-ask-20261019-040940', demo_eq_abs_01__sympy_ask),
    ('demo-eq-abs-01', 'sympy-refine', 'true', 'true', 'sympy-refine-20261019-040943', demo_eq_abs_01__sympy_refine),
    ('demo-eq-abs-01', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-040945', demo_eq_abs_01__sympy_simplify),
    ('demo-eq-abs-01', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261019-041809', demo_eq_abs_01__sympy_extras_ask),
    ('demo-eq-abs-01', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261019-041814', demo_eq_abs_01__sympy_extras_refine),
    ('demo-eq-abs-01', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261019-041817', demo_eq_abs_01__sympy_extras_simplify),
    ('demo-eq-abs-02', 'satassume-ask', 'false', 'false', 'satassume-ask-20261019-041805', demo_eq_abs_02__satassume_ask),
    ('demo-eq-abs-02', 'satrefine-refine', 'false', 'null', 'satrefine-refine-20261019-074829', demo_eq_abs_02__satrefine_refine),
    ('demo-eq-abs-02', 'satrefine-simplify', 'false', 'null', 'satrefine-simplify-20261019-041807', demo_eq_abs_02__satrefine_simplify),
    ('demo-eq-abs-02', 'sympy-auto', 'false', 'null', 'sympy-auto-20261019-040938', demo_eq_abs_02__sympy_auto),
    ('demo-eq-abs-02', 'sympy-ask', 'false', 'false', 'sympy-ask-20261019-040940', demo_eq_abs_02__sympy_ask),
    ('demo-eq-abs-02', 'sympy-refine', 'false', 'null', 'sympy-refine-20261019-040943', demo_eq_abs_02__sympy_refine),
    ('demo-eq-abs-02', 'sympy-simplify', 'false', 'null', 'sympy-simplify-20261019-040945', demo_eq_abs_02__sympy_simplify),
    ('demo-eq-abs-02', 'sympy-extras-ask', 'false', 'false', 'sympy-extras-ask-20261019-041809', demo_eq_abs_02__sympy_extras_ask),
    ('demo-eq-abs-02', 'sympy-extras-refine', 'false', 'null', 'sympy-extras-refine-20261019-041814', demo_eq_abs_02__sympy_extras_refine),
    ('demo-eq-abs-02', 'sympy-extras-simplify', 'false', 'null', 'sympy-extras-simplify-20261019-041817', demo_eq_abs_02__sympy_extras_simplify),
    ('demo-eq-log-01', 'satassume-ask', 'true', 'null', 'satassume-ask-20261019-041805', demo_eq_log_01__satassume_ask),
    ('demo-eq-log-01', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-074829', demo_eq_log_01__satrefine_refine),
    ('demo-eq-log-01', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261019-041807', demo_eq_log_01__satrefine_simplify),
    ('demo-eq-log-01', 'sympy-auto', 'true', 'true', 'sympy-auto-20261019-040938', demo_eq_log_01__sympy_auto),
    ('demo-eq-log-01', 'sympy-ask', 'true', 'true', 'sympy-ask-20261019-040940', demo_eq_log_01__sympy_ask),
    ('demo-eq-log-01', 'sympy-refine', 'true', 'true', 'sympy-refine-20261019-040943', demo_eq_log_01__sympy_refine),
    ('demo-eq-log-01', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-040945', demo_eq_log_01__sympy_simplify),
    ('demo-eq-log-01', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261019-041809', demo_eq_log_01__sympy_extras_ask),
    ('demo-eq-log-01', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261019-041814', demo_eq_log_01__sympy_extras_refine),
    ('demo-eq-log-01', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261019-041817', demo_eq_log_01__sympy_extras_simplify),
    ('demo-eq-pow-01', 'satassume-ask', 'true', 'null', 'satassume-ask-20261019-041805', demo_eq_pow_01__satassume_ask),
    ('demo-eq-pow-01', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-074829', demo_eq_pow_01__satrefine_refine),
    ('demo-eq-pow-01', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261019-041807', demo_eq_pow_01__satrefine_simplify),
    ('demo-eq-pow-01', 'sympy-auto', 'true', 'true', 'sympy-auto-20261019-040938', demo_eq_pow_01__sympy_auto),
    ('demo-eq-pow-01', 'sympy-ask', 'true', 'true', 'sympy-ask-20261019-040940', demo_eq_pow_01__sympy_ask),
    ('demo-eq-pow-01', 'sympy-refine', 'true', 'true', 'sympy-refine-20261019-040943', demo_eq_pow_01__sympy_refine),
    ('demo-eq-pow-01', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-040945', demo_eq_pow_01__sympy_simplify),
    ('demo-eq-pow-01', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261019-041809', demo_eq_pow_01__sympy_extras_ask),
    ('demo-eq-pow-01', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261019-041814', demo_eq_pow_01__sympy_extras_refine),
    ('demo-eq-pow-01', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261019-041817', demo_eq_pow_01__sympy_extras_simplify),
    ('demo-eq-sqrt-01', 'satassume-ask', 'true', 'null', 'satassume-ask-20261019-041805', demo_eq_sqrt_01__satassume_ask),
    ('demo-eq-sqrt-01', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-074829', demo_eq_sqrt_01__satrefine_refine),
    ('demo-eq-sqrt-01', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261019-041807', demo_eq_sqrt_01__satrefine_simplify),
    ('demo-eq-sqrt-01', 'sympy-auto', 'true', 'true', 'sympy-auto-20261019-040938', demo_eq_sqrt_01__sympy_auto),
    ('demo-eq-sqrt-01', 'sympy-ask', 'true', 'null', 'sympy-ask-20261019-040940', demo_eq_sqrt_01__sympy_ask),
    ('demo-eq-sqrt-01', 'sympy-refine', 'true', 'true', 'sympy-refine-20261019-040943', demo_eq_sqrt_01__sympy_refine),
    ('demo-eq-sqrt-01', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-040945', demo_eq_sqrt_01__sympy_simplify),
    ('demo-eq-sqrt-01', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261019-041809', demo_eq_sqrt_01__sympy_extras_ask),
    ('demo-eq-sqrt-01', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261019-041814', demo_eq_sqrt_01__sympy_extras_refine),
    ('demo-eq-sqrt-01', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261019-041817', demo_eq_sqrt_01__sympy_extras_simplify),
    ('demo-eq-sqrt-02', 'satassume-ask', 'true', 'null', 'satassume-ask-20261019-041805', demo_eq_sqrt_02__satassume_ask),
    ('demo-eq-sqrt-02', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-074829', demo_eq_sqrt_02__satrefine_refine),
    ('demo-eq-sqrt-02', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261019-041807', demo_eq_sqrt_02__satrefine_simplify),
    ('demo-eq-sqrt-02', 'sympy-auto', 'true', 'true', 'sympy-auto-20261019-040938', demo_eq_sqrt_02__sympy_auto),
    ('demo-eq-sqrt-02', 'sympy-ask', 'true', 'true', 'sympy-ask-20261019-040940', demo_eq_sqrt_02__sympy_ask),
    ('demo-eq-sqrt-02', 'sympy-refine', 'true', 'true', 'sympy-refine-20261019-040943', demo_eq_sqrt_02__sympy_refine),
    ('demo-eq-sqrt-02', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-040945', demo_eq_sqrt_02__sympy_simplify),
    ('demo-eq-sqrt-02', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261019-041809', demo_eq_sqrt_02__sympy_extras_ask),
    ('demo-eq-sqrt-02', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261019-041814', demo_eq_sqrt_02__sympy_extras_refine),
    ('demo-eq-sqrt-02', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261019-041817', demo_eq_sqrt_02__sympy_extras_simplify),
    ('demo-eq-sqrt-03', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261019-041805', demo_eq_sqrt_03__satassume_ask),
    ('demo-eq-sqrt-03', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-074829', demo_eq_sqrt_03__satrefine_refine),
    ('demo-eq-sqrt-03', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261019-041807', demo_eq_sqrt_03__satrefine_simplify),
    ('demo-eq-sqrt-03', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261019-040938', demo_eq_sqrt_03__sympy_auto),
    ('demo-eq-sqrt-03', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261019-040940', demo_eq_sqrt_03__sympy_ask),
    ('demo-eq-sqrt-03', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261019-040943', demo_eq_sqrt_03__sympy_refine),
    ('demo-eq-sqrt-03', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261019-040945', demo_eq_sqrt_03__sympy_simplify),
    ('demo-eq-sqrt-03', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261019-041809', demo_eq_sqrt_03__sympy_extras_ask),
    ('demo-eq-sqrt-03', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261019-041814', demo_eq_sqrt_03__sympy_extras_refine),
    ('demo-eq-sqrt-03', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261019-041817', demo_eq_sqrt_03__sympy_extras_simplify),
    ('demo-eq-sqrt-04', 'satassume-ask', 'false', 'null', 'satassume-ask-20261019-041805', demo_eq_sqrt_04__satassume_ask),
    ('demo-eq-sqrt-04', 'satrefine-refine', 'false', 'false', 'satrefine-refine-20261019-074829', demo_eq_sqrt_04__satrefine_refine),
    ('demo-eq-sqrt-04', 'satrefine-simplify', 'false', 'false', 'satrefine-simplify-20261019-041807', demo_eq_sqrt_04__satrefine_simplify),
    ('demo-eq-sqrt-04', 'sympy-auto', 'false', 'false', 'sympy-auto-20261019-040938', demo_eq_sqrt_04__sympy_auto),
    ('demo-eq-sqrt-04', 'sympy-ask', 'false', 'null', 'sympy-ask-20261019-040940', demo_eq_sqrt_04__sympy_ask),
    ('demo-eq-sqrt-04', 'sympy-refine', 'false', 'false', 'sympy-refine-20261019-040943', demo_eq_sqrt_04__sympy_refine),
    ('demo-eq-sqrt-04', 'sympy-simplify', 'false', 'false', 'sympy-simplify-20261019-040945', demo_eq_sqrt_04__sympy_simplify),
    ('demo-eq-sqrt-04', 'sympy-extras-ask', 'false', 'false', 'sympy-extras-ask-20261019-041809', demo_eq_sqrt_04__sympy_extras_ask),
    ('demo-eq-sqrt-04', 'sympy-extras-refine', 'false', 'false', 'sympy-extras-refine-20261019-041814', demo_eq_sqrt_04__sympy_extras_refine),
    ('demo-eq-sqrt-04', 'sympy-extras-simplify', 'false', 'false', 'sympy-extras-simplify-20261019-041817', demo_eq_sqrt_04__sympy_extras_simplify),
    ('demo-eq-trig-01', 'satassume-ask', 'true', 'null', 'satassume-ask-20261019-041805', demo_eq_trig_01__satassume_ask),
    ('demo-eq-trig-01', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-074829', demo_eq_trig_01__satrefine_refine),
    ('demo-eq-trig-01', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261019-041807', demo_eq_trig_01__satrefine_simplify),
    ('demo-eq-trig-01', 'sympy-auto', 'true', 'null', 'sympy-auto-20261019-040938', demo_eq_trig_01__sympy_auto),
    ('demo-eq-trig-01', 'sympy-ask', 'true', 'null', 'sympy-ask-20261019-040940', demo_eq_trig_01__sympy_ask),
    ('demo-eq-trig-01', 'sympy-refine', 'true', 'null', 'sympy-refine-20261019-040943', demo_eq_trig_01__sympy_refine),
    ('demo-eq-trig-01', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-040945', demo_eq_trig_01__sympy_simplify),
    ('demo-eq-trig-01', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261019-041809', demo_eq_trig_01__sympy_extras_ask),
    ('demo-eq-trig-01', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261019-041814', demo_eq_trig_01__sympy_extras_refine),
    ('demo-eq-trig-01', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261019-041817', demo_eq_trig_01__sympy_extras_simplify),
    ('demo-eq-trig-02', 'satassume-ask', 'true', 'null', 'satassume-ask-20261019-041805', demo_eq_trig_02__satassume_ask),
    ('demo-eq-trig-02', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-074829', demo_eq_trig_02__satrefine_refine),
    ('demo-eq-trig-02', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261019-041807', demo_eq_trig_02__satrefine_simplify),
    ('demo-eq-trig-02', 'sympy-auto', 'true', 'null', 'sympy-auto-20261019-040938', demo_eq_trig_02__sympy_auto),
    ('demo-eq-trig-02', 'sympy-ask', 'true', 'null', 'sympy-ask-20261019-040940', demo_eq_trig_02__sympy_ask),
    ('demo-eq-trig-02', 'sympy-refine', 'true', 'null', 'sympy-refine-20261019-040943', demo_eq_trig_02__sympy_refine),
    ('demo-eq-trig-02', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-040945', demo_eq_trig_02__sympy_simplify),
    ('demo-eq-trig-02', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261019-041809', demo_eq_trig_02__sympy_extras_ask),
    ('demo-eq-trig-02', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261019-041814', demo_eq_trig_02__sympy_extras_refine),
    ('demo-eq-trig-02', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261019-041817', demo_eq_trig_02__sympy_extras_simplify),
    ('demo-log-01', 'satassume-ask', 'true', 'null', 'satassume-ask-20261019-041805', demo_log_01__satassume_ask),
    ('demo-log-01', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-074829', demo_log_01__satrefine_refine),
    ('demo-log-01', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261019-041807', demo_log_01__satrefine_simplify),
    ('demo-log-01', 'sympy-auto', 'true', 'null', 'sympy-auto-20261019-040938', demo_log_01__sympy_auto),
    ('demo-log-01', 'sympy-ask', 'true', 'null', 'sympy-ask-20261019-040940', demo_log_01__sympy_ask),
    ('demo-log-01', 'sympy-refine', 'true', 'null', 'sympy-refine-20261019-040943', demo_log_01__sympy_refine),
    ('demo-log-01', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-040945', demo_log_01__sympy_simplify),
    ('demo-log-01', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261019-041809', demo_log_01__sympy_extras_ask),
    ('demo-log-01', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261019-041814', demo_log_01__sympy_extras_refine),
    ('demo-log-01', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261019-041817', demo_log_01__sympy_extras_simplify),
    ('demo-log-02', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261019-041805', demo_log_02__satassume_ask),
    ('demo-log-02', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-074829', demo_log_02__satrefine_refine),
    ('demo-log-02', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261019-041807', demo_log_02__satrefine_simplify),
    ('demo-log-02', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261019-040938', demo_log_02__sympy_auto),
    ('demo-log-02', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261019-040940', demo_log_02__sympy_ask),
    ('demo-log-02', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261019-040943', demo_log_02__sympy_refine),
    ('demo-log-02', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261019-040945', demo_log_02__sympy_simplify),
    ('demo-log-02', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261019-041809', demo_log_02__sympy_extras_ask),
    ('demo-log-02', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261019-041814', demo_log_02__sympy_extras_refine),
    ('demo-log-02', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261019-041817', demo_log_02__sympy_extras_simplify),
    ('demo-log-03', 'satassume-ask', 'false', 'false', 'satassume-ask-20261019-041805', demo_log_03__satassume_ask),
    ('demo-log-03', 'satrefine-refine', 'false', 'false', 'satrefine-refine-20261019-074829', demo_log_03__satrefine_refine),
    ('demo-log-03', 'satrefine-simplify', 'false', 'false', 'satrefine-simplify-20261019-041807', demo_log_03__satrefine_simplify),
    ('demo-log-03', 'sympy-auto', 'false', 'null', 'sympy-auto-20261019-040938', demo_log_03__sympy_auto),
    ('demo-log-03', 'sympy-ask', 'false', 'false', 'sympy-ask-20261019-040940', demo_log_03__sympy_ask),
    ('demo-log-03', 'sympy-refine', 'false', 'null', 'sympy-refine-20261019-040943', demo_log_03__sympy_refine),
    ('demo-log-03', 'sympy-simplify', 'false', 'false', 'sympy-simplify-20261019-040945', demo_log_03__sympy_simplify),
    ('demo-log-03', 'sympy-extras-ask', 'false', 'null', 'sympy-extras-ask-20261019-041809', demo_log_03__sympy_extras_ask),
    ('demo-log-03', 'sympy-extras-refine', 'false', 'null', 'sympy-extras-refine-20261019-041814', demo_log_03__sympy_extras_refine),
    ('demo-log-03', 'sympy-extras-simplify', 'false', 'false', 'sympy-extras-simplify-20261019-041817', demo_log_03__sympy_extras_simplify),
    ('demo-nonzero-01', 'satassume-ask', 'true', 'null', 'satassume-ask-20261019-041805', demo_nonzero_01__satassume_ask),
    ('demo-nonzero-01', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-074829', demo_nonzero_01__satrefine_refine),
    ('demo-nonzero-01', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261019-041807', demo_nonzero_01__satrefine_simplify),
    ('demo-nonzero-01', 'sympy-auto', 'true', 'true', 'sympy-auto-20261019-040938', demo_nonzero_01__sympy_auto),
    ('demo-nonzero-01', 'sympy-ask', 'true', 'null', 'sympy-ask-20261019-040940', demo_nonzero_01__sympy_ask),
    ('demo-nonzero-01', 'sympy-refine', 'true', 'null', 'sympy-refine-20261019-040943', demo_nonzero_01__sympy_refine),
    ('demo-nonzero-01', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-040945', demo_nonzero_01__sympy_simplify),
    ('demo-nonzero-01', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261019-041809', demo_nonzero_01__sympy_extras_ask),
    ('demo-nonzero-01', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261019-041814', demo_nonzero_01__sympy_extras_refine),
    ('demo-nonzero-01', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261019-041817', demo_nonzero_01__sympy_extras_simplify),
    ('demo-parity-01', 'satassume-ask', 'true', 'null', 'satassume-ask-20261019-041805', demo_parity_01__satassume_ask),
    ('demo-parity-01', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-074829', demo_parity_01__satrefine_refine),
    ('demo-parity-01', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261019-041807', demo_parity_01__satrefine_simplify),
    ('demo-parity-01', 'sympy-auto', 'true', 'true', 'sympy-auto-20261019-040938', demo_parity_01__sympy_auto),
    ('demo-parity-01', 'sympy-ask', 'true', 'null', 'sympy-ask-20261019-040940', demo_parity_01__sympy_ask),
    ('demo-parity-01', 'sympy-refine', 'true', 'true', 'sympy-refine-20261019-040943', demo_parity_01__sympy_refine),
    ('demo-parity-01', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-040945', demo_parity_01__sympy_simplify),
    ('demo-parity-01', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261019-041809', demo_parity_01__sympy_extras_ask),
    ('demo-parity-01', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261019-041814', demo_parity_01__sympy_extras_refine),
    ('demo-parity-01', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261019-041817', demo_parity_01__sympy_extras_simplify),
    ('demo-parity-02', 'satassume-ask', 'false', 'false', 'satassume-ask-20261019-041805', demo_parity_02__satassume_ask),
    ('demo-parity-02', 'satrefine-refine', 'false', 'false', 'satrefine-refine-20261019-074829', demo_parity_02__satrefine_refine),
    ('demo-parity-02', 'satrefine-simplify', 'false', 'false', 'satrefine-simplify-20261019-041807', demo_parity_02__satrefine_simplify),
    ('demo-parity-02', 'sympy-auto', 'false', 'false', 'sympy-auto-20261019-040938', demo_parity_02__sympy_auto),
    ('demo-parity-02', 'sympy-ask', 'false', 'false', 'sympy-ask-20261019-040940', demo_parity_02__sympy_ask),
    ('demo-parity-02', 'sympy-refine', 'false', 'false', 'sympy-refine-20261019-040943', demo_parity_02__sympy_refine),
    ('demo-parity-02', 'sympy-simplify', 'false', 'false', 'sympy-simplify-20261019-040945', demo_parity_02__sympy_simplify),
    ('demo-parity-02', 'sympy-extras-ask', 'false', 'false', 'sympy-extras-ask-20261019-041809', demo_parity_02__sympy_extras_ask),
    ('demo-parity-02', 'sympy-extras-refine', 'false', 'false', 'sympy-extras-refine-20261019-041814', demo_parity_02__sympy_extras_refine),
    ('demo-parity-02', 'sympy-extras-simplify', 'false', 'false', 'sympy-extras-simplify-20261019-041817', demo_parity_02__sympy_extras_simplify),
    ('demo-parity-03', 'satassume-ask', 'true', 'null', 'satassume-ask-20261019-041805', demo_parity_03__satassume_ask),
    ('demo-parity-03', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-074829', demo_parity_03__satrefine_refine),
    ('demo-parity-03', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261019-041807', demo_parity_03__satrefine_simplify),
    ('demo-parity-03', 'sympy-auto', 'true', 'true', 'sympy-auto-20261019-040938', demo_parity_03__sympy_auto),
    ('demo-parity-03', 'sympy-ask', 'true', 'true', 'sympy-ask-20261019-040940', demo_parity_03__sympy_ask),
    ('demo-parity-03', 'sympy-refine', 'true', 'true', 'sympy-refine-20261019-040943', demo_parity_03__sympy_refine),
    ('demo-parity-03', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-040945', demo_parity_03__sympy_simplify),
    ('demo-parity-03', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261019-041809', demo_parity_03__sympy_extras_ask),
    ('demo-parity-03', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261019-041814', demo_parity_03__sympy_extras_refine),
    ('demo-parity-03', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261019-041817', demo_parity_03__sympy_extras_simplify),
    ('demo-parity-04', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261019-041805', demo_parity_04__satassume_ask),
    ('demo-parity-04', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-074829', demo_parity_04__satrefine_refine),
    ('demo-parity-04', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261019-041807', demo_parity_04__satrefine_simplify),
    ('demo-parity-04', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261019-040938', demo_parity_04__sympy_auto),
    ('demo-parity-04', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261019-040940', demo_parity_04__sympy_ask),
    ('demo-parity-04', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261019-040943', demo_parity_04__sympy_refine),
    ('demo-parity-04', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261019-040945', demo_parity_04__sympy_simplify),
    ('demo-parity-04', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261019-041809', demo_parity_04__sympy_extras_ask),
    ('demo-parity-04', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261019-041814', demo_parity_04__sympy_extras_refine),
    ('demo-parity-04', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261019-041817', demo_parity_04__sympy_extras_simplify),
    ('demo-parity-05', 'satassume-ask', 'true', 'null', 'satassume-ask-20261019-041805', demo_parity_05__satassume_ask),
    ('demo-parity-05', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-074829', demo_parity_05__satrefine_refine),
    ('demo-parity-05', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261019-041807', demo_parity_05__satrefine_simplify),
    ('demo-parity-05', 'sympy-auto', 'true', 'true', 'sympy-auto-20261019-040938', demo_parity_05__sympy_auto),
    ('demo-parity-05', 'sympy-ask', 'true', 'null', 'sympy-ask-20261019-040940', demo_parity_05__sympy_ask),
    ('demo-parity-05', 'sympy-refine', 'true', 'true', 'sympy-refine-20261019-040943', demo_parity_05__sympy_refine),
    ('demo-parity-05', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-040945', demo_parity_05__sympy_simplify),
    ('demo-parity-05', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261019-041809', demo_parity_05__sympy_extras_ask),
    ('demo-parity-05', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261019-041814', demo_parity_05__sympy_extras_refine),
    ('demo-parity-05', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261019-041817', demo_parity_05__sympy_extras_simplify),
    ('demo-prime-01', 'satassume-ask', 'true', 'null', 'satassume-ask-20261019-041805', demo_prime_01__satassume_ask),
    ('demo-prime-01', 'satrefine-refine', 'true', 'null', 'satrefine-refine-20261019-074829', demo_prime_01__satrefine_refine),
    ('demo-prime-01', 'satrefine-simplify', 'true', 'null', 'satrefine-simplify-20261019-041807', demo_prime_01__satrefine_simplify),
    ('demo-prime-01', 'sympy-auto', 'true', 'null', 'sympy-auto-20261019-040938', demo_prime_01__sympy_auto),
    ('demo-prime-01', 'sympy-ask', 'true', 'null', 'sympy-ask-20261019-040940', demo_prime_01__sympy_ask),
    ('demo-prime-01', 'sympy-refine', 'true', 'null', 'sympy-refine-20261019-040943', demo_prime_01__sympy_refine),
    ('demo-prime-01', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261019-040945', demo_prime_01__sympy_simplify),
    ('demo-prime-01', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261019-041809', demo_prime_01__sympy_extras_ask),
    ('demo-prime-01', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261019-041814', demo_prime_01__sympy_extras_refine),
    ('demo-prime-01', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261019-041817', demo_prime_01__sympy_extras_simplify),
    ('demo-prime-02', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261019-041805', demo_prime_02__satassume_ask),
    ('demo-prime-02', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-074829', demo_prime_02__satrefine_refine),
    ('demo-prime-02', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261019-041807', demo_prime_02__satrefine_simplify),
    ('demo-prime-02', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261019-040938', demo_prime_02__sympy_auto),
    ('demo-prime-02', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261019-040940', demo_prime_02__sympy_ask),
    ('demo-prime-02', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261019-040943', demo_prime_02__sympy_refine),
    ('demo-prime-02', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261019-040945', demo_prime_02__sympy_simplify),
    ('demo-prime-02', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261019-041809', demo_prime_02__sympy_extras_ask),
    ('demo-prime-02', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261019-041814', demo_prime_02__sympy_extras_refine),
    ('demo-prime-02', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261019-041817', demo_prime_02__sympy_extras_simplify),
    ('demo-sign-02', 'satassume-ask', 'true', 'null', 'satassume-ask-20261019-041805', demo_sign_02__satassume_ask),
    ('demo-sign-02', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-074829', demo_sign_02__satrefine_refine),
    ('demo-sign-02', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261019-041807', demo_sign_02__satrefine_simplify),
    ('demo-sign-02', 'sympy-auto', 'true', 'true', 'sympy-auto-20261019-040938', demo_sign_02__sympy_auto),
    ('demo-sign-02', 'sympy-ask', 'true', 'null', 'sympy-ask-20261019-040940', demo_sign_02__sympy_ask),
    ('demo-sign-02', 'sympy-refine', 'true', 'true', 'sympy-refine-20261019-040943', demo_sign_02__sympy_refine),
    ('demo-sign-02', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-040945', demo_sign_02__sympy_simplify),
    ('demo-sign-02', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261019-041809', demo_sign_02__sympy_extras_ask),
    ('demo-sign-02', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261019-041814', demo_sign_02__sympy_extras_refine),
    ('demo-sign-02', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261019-041817', demo_sign_02__sympy_extras_simplify),
    ('demo-sign-03', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261019-041805', demo_sign_03__satassume_ask),
    ('demo-sign-03', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261019-074829', demo_sign_03__satrefine_refine),
    ('demo-sign-03', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261019-041807', demo_sign_03__satrefine_simplify),
    ('demo-sign-03', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261019-040938', demo_sign_03__sympy_auto),
    ('demo-sign-03', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261019-040940', demo_sign_03__sympy_ask),
    ('demo-sign-03', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261019-040943', demo_sign_03__sympy_refine),
    ('demo-sign-03', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261019-040945', demo_sign_03__sympy_simplify),
    ('demo-sign-03', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261019-041809', demo_sign_03__sympy_extras_ask),
    ('demo-sign-03', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261019-041814', demo_sign_03__sympy_extras_refine),
    ('demo-sign-03', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261019-041817', demo_sign_03__sympy_extras_simplify),
    ('demo-sign-04', 'satassume-ask', 'true', 'null', 'satassume-ask-20261019-041805', demo_sign_04__satassume_ask),
    ('demo-sign-04', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-074829', demo_sign_04__satrefine_refine),
    ('demo-sign-04', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261019-041807', demo_sign_04__satrefine_simplify),
    ('demo-sign-04', 'sympy-auto', 'true', 'null', 'sympy-auto-20261019-040938', demo_sign_04__sympy_auto),
    ('demo-sign-04', 'sympy-ask', 'true', 'null', 'sympy-ask-20261019-040940', demo_sign_04__sympy_ask),
    ('demo-sign-04', 'sympy-refine', 'true', 'null', 'sympy-refine-20261019-040943', demo_sign_04__sympy_refine),
    ('demo-sign-04', 'sympy-simplify', 'true', 'null', 'sympy-simplify-20261019-040945', demo_sign_04__sympy_simplify),
    ('demo-sign-04', 'sympy-extras-ask', 'true', 'null', 'sympy-extras-ask-20261019-041809', demo_sign_04__sympy_extras_ask),
    ('demo-sign-04', 'sympy-extras-refine', 'true', 'null', 'sympy-extras-refine-20261019-041814', demo_sign_04__sympy_extras_refine),
    ('demo-sign-04', 'sympy-extras-simplify', 'true', 'null', 'sympy-extras-simplify-20261019-041817', demo_sign_04__sympy_extras_simplify),
    ('demo-sign-05', 'satassume-ask', 'true', 'null', 'satassume-ask-20261019-041805', demo_sign_05__satassume_ask),
    ('demo-sign-05', 'satrefine-refine', 'true', 'true', 'satrefine-refine-20261019-074829', demo_sign_05__satrefine_refine),
    ('demo-sign-05', 'satrefine-simplify', 'true', 'true', 'satrefine-simplify-20261019-041807', demo_sign_05__satrefine_simplify),
    ('demo-sign-05', 'sympy-auto', 'true', 'true', 'sympy-auto-20261019-040938', demo_sign_05__sympy_auto),
    ('demo-sign-05', 'sympy-ask', 'true', 'null', 'sympy-ask-20261019-040940', demo_sign_05__sympy_ask),
    ('demo-sign-05', 'sympy-refine', 'true', 'true', 'sympy-refine-20261019-040943', demo_sign_05__sympy_refine),
    ('demo-sign-05', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-040945', demo_sign_05__sympy_simplify),
    ('demo-sign-05', 'sympy-extras-ask', 'true', 'true', 'sympy-extras-ask-20261019-041809', demo_sign_05__sympy_extras_ask),
    ('demo-sign-05', 'sympy-extras-refine', 'true', 'true', 'sympy-extras-refine-20261019-041814', demo_sign_05__sympy_extras_refine),
    ('demo-sign-05', 'sympy-extras-simplify', 'true', 'true', 'sympy-extras-simplify-20261019-041817', demo_sign_05__sympy_extras_simplify),
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
