# assume-eval: a runnable script from the results browser
# Run: python3 this-file.py (or paste it into python or Jupyter).
# suite simplipy · category simplipy-ground · system sympy-simplify (20 cases listed)
# 20 case run(s), a function each (listed in CASES).  Each runs in a fresh copy of
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
''', ('sympy', '1.14.0'))

# comments that the cases' code repeats, shown once here (left out below):
# true iff the result is 0; false only if it is a definite nonzero number


# ---- case sp-acj4-1007-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-110207 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1007_ground__sympy_simplify():
    Residual = 0 / sin(5) - 0
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1107-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-110207 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1107_ground__sympy_simplify():
    Residual = asin(sin(Integer(1) / 10)) - Rational(1, 10)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1148-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-110207 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1148_ground__sympy_simplify():
    Residual = cosh(log(Integer(1) / 4)) - Rational(17, 8)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1149-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-110207 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1149_ground__sympy_simplify():
    Residual = exp(Abs(log(2))) - 2
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1177-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-110207 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1177_ground__sympy_simplify():
    Residual = Pow(0, asinh(10)) - 0
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1195-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-110207 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1195_ground__sympy_simplify():
    Residual = Pow(0, atan(7)) - 0
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1217-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-110207 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1217_ground__sympy_simplify():
    Residual = Pow(0, exp(-1)) - 0
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1238-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-110207 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1238_ground__sympy_simplify():
    Residual = Pow(0, 1 / pi) - 0
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1247-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-110207 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1247_ground__sympy_simplify():
    Residual = Pow(0, log(9)) - 0
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1254-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-110207 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1254_ground__sympy_simplify():
    Residual = Pow(0, sin(2)) - 0
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1258-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-110207 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1258_ground__sympy_simplify():
    Residual = Pow(0, sin(9)) - 0
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5372-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-110207 answered true (solved)
@_in(_SETUP1)
def sp_acj4_5372_ground__sympy_simplify():
    Residual = sin(asin(Integer(1) / -4)) - Rational(-1, 4)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5382-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-110207 answered true (solved)
@_in(_SETUP1)
def sp_acj4_5382_ground__sympy_simplify():
    Residual = sinh(log(Integer(1) / 4)) - Rational(-15, 8)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5385-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-110207 answered true (solved)
@_in(_SETUP1)
def sp_acj4_5385_ground__sympy_simplify():
    Residual = sinh(-log(4)) - Rational(-15, 8)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-819-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-110207 answered true (solved)
@_in(_SETUP1)
def sp_acj4_819_ground__sympy_simplify():
    Residual = 0 / pi - 0
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-837-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-110207 answered true (solved)
@_in(_SETUP1)
def sp_acj4_837_ground__sympy_simplify():
    Residual = Pow(0, pi) - 0
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-848-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-110207 answered true (solved)
@_in(_SETUP1)
def sp_acj4_848_ground__sympy_simplify():
    Residual = sinh(log(4)) - Rational(15, 8)
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-868-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-110207 answered true (solved)
@_in(_SETUP1)
def sp_acj4_868_ground__sympy_simplify():
    Residual = 0 * acosh(7) - 0
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-911-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-110207 answered true (solved)
@_in(_SETUP1)
def sp_acj4_911_ground__sympy_simplify():
    Residual = 0 / asin(-1) - 0
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-927-ground · expected true · system sympy-simplify (sympy 1.14.0)
# the run sympy-simplify-20261019-110207 answered true (solved)
@_in(_SETUP1)
def sp_acj4_927_ground__sympy_simplify():
    Residual = 0 / asinh(4) - 0
    Result = simplify(Residual)
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
    return Answer


# (case, system, expected, the stored run's answer, that run, its function)
CASES = [
    ('sp-acj4-1007-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-110207', sp_acj4_1007_ground__sympy_simplify),
    ('sp-acj4-1107-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-110207', sp_acj4_1107_ground__sympy_simplify),
    ('sp-acj4-1148-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-110207', sp_acj4_1148_ground__sympy_simplify),
    ('sp-acj4-1149-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-110207', sp_acj4_1149_ground__sympy_simplify),
    ('sp-acj4-1177-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-110207', sp_acj4_1177_ground__sympy_simplify),
    ('sp-acj4-1195-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-110207', sp_acj4_1195_ground__sympy_simplify),
    ('sp-acj4-1217-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-110207', sp_acj4_1217_ground__sympy_simplify),
    ('sp-acj4-1238-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-110207', sp_acj4_1238_ground__sympy_simplify),
    ('sp-acj4-1247-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-110207', sp_acj4_1247_ground__sympy_simplify),
    ('sp-acj4-1254-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-110207', sp_acj4_1254_ground__sympy_simplify),
    ('sp-acj4-1258-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-110207', sp_acj4_1258_ground__sympy_simplify),
    ('sp-acj4-5372-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-110207', sp_acj4_5372_ground__sympy_simplify),
    ('sp-acj4-5382-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-110207', sp_acj4_5382_ground__sympy_simplify),
    ('sp-acj4-5385-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-110207', sp_acj4_5385_ground__sympy_simplify),
    ('sp-acj4-819-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-110207', sp_acj4_819_ground__sympy_simplify),
    ('sp-acj4-837-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-110207', sp_acj4_837_ground__sympy_simplify),
    ('sp-acj4-848-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-110207', sp_acj4_848_ground__sympy_simplify),
    ('sp-acj4-868-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-110207', sp_acj4_868_ground__sympy_simplify),
    ('sp-acj4-911-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-110207', sp_acj4_911_ground__sympy_simplify),
    ('sp-acj4-927-ground', 'sympy-simplify', 'true', 'true', 'sympy-simplify-20261019-110207', sp_acj4_927_ground__sympy_simplify),
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
