# assume-eval: a runnable script from the results browser
# Run: python3 this-file.py (or paste it into python or Jupyter).
# suite simplipy · category simplipy-conditional · system sympy-ask (92 cases listed)
# 92 case run(s), a function each (listed in CASES).  Each runs in a fresh copy of
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
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False


# ---- case sp-acj4-1-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_1_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Abs(x) <= 1)
    Residual = asin(Abs(x)) - Abs(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_108_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-124-condf · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_124_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)))
    Residual = Abs(asin(tanh(x))) - acos(1 / cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-127-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_127_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), re(x) >= 0, Ne(exp(x), 1, evaluate=False), Ne(exp(x), -1, evaluate=False))
    Residual = Abs(atanh(exp(x))) - atanh(exp(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-128-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_128_cond2__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Abs(x) <= 1)
    Residual = Abs(cos(asin(x))) - cos(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-128-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_128_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), x > 1)
    Residual = Abs(cos(asin(x))) - cos(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-129-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_129_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False))
    Residual = Abs(cos(atan(x))) - cos(atan(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_130_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Abs(x) < pi / 2, ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-condf · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_131_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_132_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), x >= 0, x <= pi, ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_133_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-136-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_136_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.nonnegative(x), Or(~Q.zero(x), re(exp(1)) > 0))
    Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_137_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.nonnegative(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-145-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_145_cond2__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Abs(x) <= 1)
    Residual = Abs(sin(acos(x))) - cos(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-145-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_145_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), x > 1)
    Residual = Abs(sin(acos(x))) - cos(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-147-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_147_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(asinh(x))), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_151_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Abs(x) <= 1)
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-156-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_156_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Abs(x) <= 1)
    Residual = acos(sin(acos(x))) - Abs(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-159-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_159_cond2__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), x <= 1, ~Q.zero(cosh(x)))
    Residual = acos(tanh(Abs(x))) - asin(1 / cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-159-cond3 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_159_cond3__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Abs(x) <= pi / 2, ~Q.zero(cosh(x)))
    Residual = acos(tanh(Abs(x))) - asin(1 / cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-162-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_162_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), re(x) >= 0, Q.real(x))
    Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-162-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_162_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.negative(x))
    Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-171-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_171_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Abs(im(x)) < pi, ~Q.zero(cosh(x)))
    Residual = asin(sin(tanh(x))) - tanh(x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-171-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_171_cond2__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)))
    Residual = asin(sin(tanh(x))) - tanh(x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-179-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_179_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Abs(x) <= pi / 2, Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
    Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_180_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), re(x) > 0, Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-181-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_181_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Abs(x) <= pi / 2, Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
    Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_183_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), re(x) > 0, ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-186-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_186_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cos(sin(x))), Ne(tan(sin(x)), I, evaluate=False), Ne(tan(sin(x)), -I, evaluate=False))
    Residual = atan(tan(sin(x))) - sin(x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-187-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_187_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)), ~Q.zero(cos(tanh(x))), Ne(tan(tanh(x)), I, evaluate=False), Ne(tan(tanh(x)), -I, evaluate=False))
    Residual = atan(tan(tanh(x))) - tanh(x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_190_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_191_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-196-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_196_cond2__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
    Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-20-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_20_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x))
    Residual = sinh(Abs(x)) - Abs(sinh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-200-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_200_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x))
    Residual = cos(asin(sin(x))) - Abs(cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-202-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_202_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cos(x)), Ne(tan(x), I, evaluate=False), Ne(tan(x), -I, evaluate=False))
    Residual = cos(atan(tan(x))) - Abs(cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_203_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-205-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_205_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cos(x)))
    Residual = cosh(asinh(tan(x))) - Abs(1 / cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_234_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), re(x) >= 0, Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_234_cond2__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.integer(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-243-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_243_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), re(x) > 0, Q.real(x), ~Q.zero(real_root(x, 5)), ~Q.zero(x))
    Residual = log(real_root(x, 5)) - (log(x) / 5)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-245-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_245_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), re(x) > 0, Q.real(x), ~Q.zero(real_root(x, 7)), ~Q.zero(x))
    Residual = log(real_root(x, 7)) - (log(x) / 7)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-248-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_248_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Abs(x) <= 1)
    Residual = -Abs(asin(x)) - asin(-Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-251-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_251_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Abs(x) < 1, Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
    Residual = -Abs(atanh(x)) - atanh(-Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_260_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Abs(re(x)) < pi / 2, ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_261_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), re(x) > 0, ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_266_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-condf · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_266_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_267_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_267_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_283_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-287-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_287_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x))
    Residual = Pow(Abs(x), 6) - Pow(x, 6)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-289-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_289_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x))
    Residual = Pow(Abs(x), 8) - Pow(x, 8)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-29-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_29_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
    Residual = 3 * log(x) - log(Pow(x, 3))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-29-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_29_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
    Residual = 3 * log(x) - log(Pow(x, 3))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-334-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_334_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), Or(~Q.zero(exp(x)), re(exp(1)) > 0))
    Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-335-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_335_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), Or(~Q.zero(exp(x)), re(pi) > 0))
    Residual = Pow(exp(x), pi) - exp(pi * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-336-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_336_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), Or(~Q.zero(exp(x)), re(x) > 0))
    Residual = Pow(exp(x), x) - exp(x * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_344_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_344_cond2__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.integer(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_372_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), re(x) > 0, Q.real(cosh(x)), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_373_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), re(x) > 0, Q.real(cosh(x)))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-376-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_376_cond2__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Abs(im(x)) < pi, Q.real(exp(x)), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -3) - exp(x / -3)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-385-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_385_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), re(x) > 0, Q.real(exp(x)))
    Residual = real_root(exp(x), 3) - exp(x / 3)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-392-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_392_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Abs(x) <= 1)
    Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-394-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_394_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Abs(x) < 1, Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-399-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_399_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x))
    Residual = sin(acos(sin(x))) - Abs(cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-402-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_402_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Abs(x) < 1, Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_403_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-condf · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_403_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-412-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_412_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Abs(x) < 1, ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-416-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_416_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Abs(x) <= 1, ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
    Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-417-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_417_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Abs(x) < 1, ~Q.zero(cos(asin(Abs(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_420_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_420_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-422-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_422_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-424-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_424_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-428-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_428_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), x <= 1)
    Residual = atan(sinh(x)) - asin(tanh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-428-cond3 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_428_cond3__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), x >= 0, x <= pi)
    Residual = atan(sinh(x)) - asin(tanh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_430_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_430_cond2__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Abs(x) < 1, ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-432-cond3 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_432_cond3__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Abs(x) <= pi / 2, ~Q.zero(cosh(x)))
    Residual = acos(Abs(tanh(x))) - asin(1 / cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_433_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_433_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_442_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-cond4 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_442_cond4__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.integer(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-46-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_46_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), ~Q.zero(Pow(2, x)))
    Residual = log(2) * x - log(Pow(2, x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_5_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Abs(x) < 1, Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = atanh(Abs(x)) - Abs(atanh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_55_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_56_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_56_condf__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-9-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261020-064258 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_9_cond__sympy_ask():
    x = Symbol('x')
    Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), ~Q.zero(exp(x)))
    Residual = log(exp(x)) - x
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# (case, system, expected, the stored run's answer, that run, its function)
CASES = [
    ('sp-acj4-1-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_1_cond__sympy_ask),
    ('sp-acj4-108-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261020-064258', sp_acj4_108_condf__sympy_ask),
    ('sp-acj4-124-condf', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_124_condf__sympy_ask),
    ('sp-acj4-127-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261020-064258', sp_acj4_127_condf__sympy_ask),
    ('sp-acj4-128-cond2', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_128_cond2__sympy_ask),
    ('sp-acj4-128-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261020-064258', sp_acj4_128_condf__sympy_ask),
    ('sp-acj4-129-cond', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_129_cond__sympy_ask),
    ('sp-acj4-130-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_130_cond__sympy_ask),
    ('sp-acj4-131-condf', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_131_condf__sympy_ask),
    ('sp-acj4-132-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_132_cond__sympy_ask),
    ('sp-acj4-133-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261020-064258', sp_acj4_133_condf__sympy_ask),
    ('sp-acj4-136-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_136_cond__sympy_ask),
    ('sp-acj4-137-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_137_cond__sympy_ask),
    ('sp-acj4-145-cond2', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_145_cond2__sympy_ask),
    ('sp-acj4-145-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261020-064258', sp_acj4_145_condf__sympy_ask),
    ('sp-acj4-147-cond', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_147_cond__sympy_ask),
    ('sp-acj4-151-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_151_cond__sympy_ask),
    ('sp-acj4-156-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_156_cond__sympy_ask),
    ('sp-acj4-159-cond2', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_159_cond2__sympy_ask),
    ('sp-acj4-159-cond3', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_159_cond3__sympy_ask),
    ('sp-acj4-162-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_162_cond__sympy_ask),
    ('sp-acj4-162-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261020-064258', sp_acj4_162_condf__sympy_ask),
    ('sp-acj4-171-cond', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_171_cond__sympy_ask),
    ('sp-acj4-171-cond2', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_171_cond2__sympy_ask),
    ('sp-acj4-179-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_179_cond__sympy_ask),
    ('sp-acj4-180-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_180_cond__sympy_ask),
    ('sp-acj4-181-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_181_cond__sympy_ask),
    ('sp-acj4-183-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_183_cond__sympy_ask),
    ('sp-acj4-186-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_186_cond__sympy_ask),
    ('sp-acj4-187-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_187_cond__sympy_ask),
    ('sp-acj4-190-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261020-064258', sp_acj4_190_condf__sympy_ask),
    ('sp-acj4-191-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261020-064258', sp_acj4_191_condf__sympy_ask),
    ('sp-acj4-196-cond2', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_196_cond2__sympy_ask),
    ('sp-acj4-20-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261020-064258', sp_acj4_20_condf__sympy_ask),
    ('sp-acj4-200-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_200_cond__sympy_ask),
    ('sp-acj4-202-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_202_cond__sympy_ask),
    ('sp-acj4-203-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_203_cond__sympy_ask),
    ('sp-acj4-205-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_205_cond__sympy_ask),
    ('sp-acj4-234-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_234_cond__sympy_ask),
    ('sp-acj4-234-cond2', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_234_cond2__sympy_ask),
    ('sp-acj4-243-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_243_cond__sympy_ask),
    ('sp-acj4-245-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_245_cond__sympy_ask),
    ('sp-acj4-248-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_248_cond__sympy_ask),
    ('sp-acj4-251-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_251_cond__sympy_ask),
    ('sp-acj4-260-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_260_cond__sympy_ask),
    ('sp-acj4-261-cond', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_261_cond__sympy_ask),
    ('sp-acj4-266-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_266_cond__sympy_ask),
    ('sp-acj4-266-condf', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_266_condf__sympy_ask),
    ('sp-acj4-267-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_267_cond__sympy_ask),
    ('sp-acj4-267-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261020-064258', sp_acj4_267_condf__sympy_ask),
    ('sp-acj4-283-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261020-064258', sp_acj4_283_condf__sympy_ask),
    ('sp-acj4-287-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261020-064258', sp_acj4_287_condf__sympy_ask),
    ('sp-acj4-289-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_289_cond__sympy_ask),
    ('sp-acj4-29-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_29_cond__sympy_ask),
    ('sp-acj4-29-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261020-064258', sp_acj4_29_condf__sympy_ask),
    ('sp-acj4-334-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_334_cond__sympy_ask),
    ('sp-acj4-335-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_335_cond__sympy_ask),
    ('sp-acj4-336-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_336_cond__sympy_ask),
    ('sp-acj4-344-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_344_cond__sympy_ask),
    ('sp-acj4-344-cond2', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_344_cond2__sympy_ask),
    ('sp-acj4-372-cond', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_372_cond__sympy_ask),
    ('sp-acj4-373-cond', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_373_cond__sympy_ask),
    ('sp-acj4-376-cond2', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_376_cond2__sympy_ask),
    ('sp-acj4-385-cond', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_385_cond__sympy_ask),
    ('sp-acj4-392-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_392_cond__sympy_ask),
    ('sp-acj4-394-cond', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_394_cond__sympy_ask),
    ('sp-acj4-399-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_399_cond__sympy_ask),
    ('sp-acj4-402-cond', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_402_cond__sympy_ask),
    ('sp-acj4-403-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_403_cond__sympy_ask),
    ('sp-acj4-403-condf', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261020-064258', sp_acj4_403_condf__sympy_ask),
    ('sp-acj4-412-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_412_cond__sympy_ask),
    ('sp-acj4-416-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_416_cond__sympy_ask),
    ('sp-acj4-417-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_417_cond__sympy_ask),
    ('sp-acj4-420-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_420_cond__sympy_ask),
    ('sp-acj4-420-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261020-064258', sp_acj4_420_condf__sympy_ask),
    ('sp-acj4-422-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261020-064258', sp_acj4_422_condf__sympy_ask),
    ('sp-acj4-424-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261020-064258', sp_acj4_424_condf__sympy_ask),
    ('sp-acj4-428-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_428_cond__sympy_ask),
    ('sp-acj4-428-cond3', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_428_cond3__sympy_ask),
    ('sp-acj4-430-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_430_cond__sympy_ask),
    ('sp-acj4-430-cond2', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_430_cond2__sympy_ask),
    ('sp-acj4-432-cond3', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_432_cond3__sympy_ask),
    ('sp-acj4-433-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_433_cond__sympy_ask),
    ('sp-acj4-433-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261020-064258', sp_acj4_433_condf__sympy_ask),
    ('sp-acj4-442-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_442_cond__sympy_ask),
    ('sp-acj4-442-cond4', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_442_cond4__sympy_ask),
    ('sp-acj4-46-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_46_cond__sympy_ask),
    ('sp-acj4-5-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_5_cond__sympy_ask),
    ('sp-acj4-55-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_55_cond__sympy_ask),
    ('sp-acj4-56-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_56_cond__sympy_ask),
    ('sp-acj4-56-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261020-064258', sp_acj4_56_condf__sympy_ask),
    ('sp-acj4-9-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261020-064258', sp_acj4_9_cond__sympy_ask),
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
