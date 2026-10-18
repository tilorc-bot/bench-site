# assume-eval: a runnable script from the results browser
# Run: python3 this-file.py (or paste it into python or Jupyter).
# case sp-acj4-180-cond · expected true · system satrefine-refine (satrefine 0.1.0)
# the run satrefine-refine-20261018-192437 answered null (no verdict)
# It prints the CAS version that runs (with a warning if the stored run used another), the
# verdict, and CHANGED: <stored> -> <got> if the answer is not the stored run's.
# Exit status: 0 when the answer is the stored run's (a wrong one too; an error answers null,
# as in the harness), 1 when it changed, 125 when the setup fails (SymPy does not import, say).
# So PYTHONPATH=<sympy checkout> git bisect run python3 this-file.py, with this script from a
# run of the good commit, finds the commit that changed the answer (125: skipped).  Pasted into
# python or Jupyter it never exits.

import os as _os
import sys as _sys
import traceback as _traceback


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


def _setup_failed():
    """The setup raised (SymPy does not import, say): exit 125, which git bisect run reads as skip."""
    _traceback.print_exc()
    print('SETUP FAILED: nothing to test (exit 125: git bisect run skips this commit)')
    _exit(125)
    raise


# setup (the harness's warm-up, version capture and cache clearing left out; if it fails: exit 125)
try:
    from sympy import *
    import sympy
    import satrefine
except Exception:
    _setup_failed()

_version('satrefine', '0.1.0')

# the query code, exactly as it ran (an error answers null, as in the harness)
try:
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), re(x) > 0, Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Result = satrefine.refine(Residual, Assum)
    # true iff the result is 0; false only if it is a definite nonzero number
    Answer = True if Result == 0 else False if (Result.is_number and Result.is_finite and Result.is_zero is False) else None
    print(Result, Answer, sep='\n')
except (Exception, SystemExit):
    _traceback.print_exc()
    Answer = None

_outcome, _change = _verdict(globals().get('Answer'), 'true', 'null', 'satrefine-refine-20261018-192437')
_exit(1 if _change else 0)
