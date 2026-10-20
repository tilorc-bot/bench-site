# assume-eval: a runnable script from the results browser
# Run: python3 this-file.py (or paste it into python or Jupyter).
# suite simplipy · case sp-acj4-260-complex · all Python systems
# 12 case run(s), a function each (listed in CASES).  Each runs in a fresh copy of
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
# dropped (not a unary fact about one symbol): ~Q.zero(cos(x))
# dropped (not a unary fact about one symbol): ~Q.zero(1 / cos(x))
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False


# ---- case sp-acj4-260-complex · expected contingent · system satassume-ask (satassume 0.0.1)
# the run satassume-ask-20261020-065124 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_260_complex__satassume_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Answer = satassume.sympy_api.ask(Q.zero(Residual), Assum, strict=True)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-complex · expected contingent · system satrefine-refine (satsimp 0.1.0)
# the run satrefine-refine-20261020-064814 answered null (declined correctly)
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
# the run satsimp-trigsimp-20261020-065212 answered null (declined correctly)
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
# the run satrefine-simplify-20261020-065134 answered null (declined correctly)
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
# the run sympy-auto-20261020-064252 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_260_complex__sympy_auto():
    x = Symbol('x', complex=True)
    Residual = -log(cos(x)) - log(1 / cos(x))
    # automatic evaluation only: no simplify, refine or other function
    Result = Residual
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_260_complex__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-complex · expected contingent · system sympy-satask (sympy 1.14.0)
# the run sympy-satask-20261020-072057 answered null (declined correctly)
@_in(_SETUP4)
def sp_acj4_260_complex__sympy_satask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Answer = satask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-complex · expected contingent · system sympy-refine (sympy 1.14.0)
# the run sympy-refine-20261020-064447 answered null (declined correctly)
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
# the run sympy-simplify-20261020-064757 answered null (declined correctly)
@_in(_SETUP3)
def sp_acj4_260_complex__sympy_simplify():
    x = Symbol('x', complex=True)
    Residual = -log(cos(x)) - log(1 / cos(x))
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-complex · expected contingent · system sympy-extras-ask (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-ask-20261020-065223 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_260_complex__sympy_extras_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    # the claim as a relation, sympy-extras' statement form (not Q.zero: see the adapter)
    Answer = sympy_extras.assumptions.ask(Eq(Residual, 0), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-complex · expected contingent · system sympy-extras-refine (sympy-extras 0.0.3 (commit 2d60199620ac))
# the run sympy-extras-refine-20261020-065818 answered null (declined correctly)
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
# the run sympy-extras-simplify-20261020-070552 answered null (declined correctly)
@_in(_SETUP5)
def sp_acj4_260_complex__sympy_extras_simplify():
    x = Symbol('x')
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Result = sympy_extras.assumptions.simplify(Residual, Assum)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# (case, system, expected, the stored run's answer, that run, its function)
CASES = [
    ('sp-acj4-260-complex', 'satassume-ask', 'contingent', 'null', 'satassume-ask-20261020-065124', sp_acj4_260_complex__satassume_ask),
    ('sp-acj4-260-complex', 'satrefine-refine', 'contingent', 'null', 'satrefine-refine-20261020-064814', sp_acj4_260_complex__satrefine_refine),
    ('sp-acj4-260-complex', 'satsimp-trigsimp', 'contingent', 'null', 'satsimp-trigsimp-20261020-065212', sp_acj4_260_complex__satsimp_trigsimp),
    ('sp-acj4-260-complex', 'satrefine-simplify', 'contingent', 'null', 'satrefine-simplify-20261020-065134', sp_acj4_260_complex__satrefine_simplify),
    ('sp-acj4-260-complex', 'sympy-auto', 'contingent', 'null', 'sympy-auto-20261020-064252', sp_acj4_260_complex__sympy_auto),
    ('sp-acj4-260-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_260_complex__sympy_ask),
    ('sp-acj4-260-complex', 'sympy-satask', 'contingent', 'null', 'sympy-satask-20261020-072057', sp_acj4_260_complex__sympy_satask),
    ('sp-acj4-260-complex', 'sympy-refine', 'contingent', 'null', 'sympy-refine-20261020-064447', sp_acj4_260_complex__sympy_refine),
    ('sp-acj4-260-complex', 'sympy-simplify', 'contingent', 'null', 'sympy-simplify-20261020-064757', sp_acj4_260_complex__sympy_simplify),
    ('sp-acj4-260-complex', 'sympy-extras-ask', 'contingent', 'null', 'sympy-extras-ask-20261020-065223', sp_acj4_260_complex__sympy_extras_ask),
    ('sp-acj4-260-complex', 'sympy-extras-refine', 'contingent', 'null', 'sympy-extras-refine-20261020-065818', sp_acj4_260_complex__sympy_extras_refine),
    ('sp-acj4-260-complex', 'sympy-extras-simplify', 'contingent', 'null', 'sympy-extras-simplify-20261020-070552', sp_acj4_260_complex__sympy_extras_simplify),
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
