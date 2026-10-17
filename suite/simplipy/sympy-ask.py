# assume-eval: a runnable script from the results browser
# Run: python3 this-file.py (or paste it into python or Jupyter).
# suite simplipy · every case · system sympy-ask (307 cases listed)
# 307 case run(s), a function each (listed in CASES).  Each runs in a fresh copy of
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
# not Q.eq: in SymPy 1.14 ask(Q.eq(x**2, x), Q.real(x)) is wrongly False


# ---- case sp-acj4-0-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_0_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-0-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_0_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = acosh(cosh(x)) - Abs(x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_1_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Abs(x) <= 1)
    Residual = asin(Abs(x)) - Abs(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_1_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = asin(Abs(x)) - Abs(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1007-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1007_ground__sympy_ask():
    Assum = And()
    Residual = 0 / sin(5) - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_102_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-102-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_102_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = Abs(x) / 6 - Abs(x / -6)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_108_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_108_condf__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-108-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_108_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Abs(x)))
    Residual = Abs(x) / x - (x / Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1107-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1107_ground__sympy_ask():
    Assum = And()
    Residual = asin(sin(Integer(1) / 10)) - Rational(1, 10)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1148-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_1148_ground__sympy_ask():
    Assum = And()
    Residual = cosh(log(Integer(1) / 4)) - Rational(17, 8)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1149-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1149_ground__sympy_ask():
    Assum = And()
    Residual = exp(Abs(log(2))) - 2
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-115-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_115_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -4)))
    Residual = log(x) / -4 - log(real_root(x, -4))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-116-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_116_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), x > 0, ~Q.zero(real_root(x, -6)))
    Residual = log(x) / -6 - log(real_root(x, -6))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1177-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1177_ground__sympy_ask():
    Assum = And()
    Residual = Pow(0, asinh(10)) - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1195-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1195_ground__sympy_ask():
    Assum = And()
    Residual = Pow(0, atan(7)) - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_120_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-120-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_120_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = pi / Abs(x) - Abs(pi / x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1217-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1217_ground__sympy_ask():
    Assum = And()
    Residual = Pow(0, exp(-1)) - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1238-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1238_ground__sympy_ask():
    Assum = And()
    Residual = Pow(0, 1 / pi) - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-124-condf · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_124_condf__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)))
    Residual = Abs(asin(tanh(x))) - acos(1 / cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1247-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1247_ground__sympy_ask():
    Assum = And()
    Residual = Pow(0, log(9)) - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1254-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1254_ground__sympy_ask():
    Assum = And()
    Residual = Pow(0, sin(2)) - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-1258-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_1258_ground__sympy_ask():
    Assum = And()
    Residual = Pow(0, sin(9)) - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-127-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_127_condf__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), re(x) >= 0, Ne(exp(x), 1, evaluate=False), Ne(exp(x), -1, evaluate=False))
    Residual = Abs(atanh(exp(x))) - atanh(exp(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-127-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_127_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Ne(exp(x), 1, evaluate=False), Ne(exp(x), -1, evaluate=False))
    Residual = Abs(atanh(exp(x))) - atanh(exp(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-128-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_128_cond2__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Abs(x) <= 1)
    Residual = Abs(cos(asin(x))) - cos(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-128-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_128_condf__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), x > 1)
    Residual = Abs(cos(asin(x))) - cos(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-128-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_128_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = Abs(cos(asin(x))) - cos(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-129-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_129_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False))
    Residual = Abs(cos(atan(x))) - cos(atan(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_130_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_130_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Abs(x) < pi / 2, ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-130-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_130_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = Abs(log(cos(x))) - log(1 / cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_131_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-condf · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_131_condf__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-131-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_131_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = Abs(log(cosh(x))) - log(cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_132_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_132_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), x >= 0, x <= pi, ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-132-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_132_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(sin(x)))
    Residual = Abs(log(sin(x))) - (-log(sin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_133_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_133_condf__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-133-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_133_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(tanh(x)))
    Residual = Abs(log(tanh(x))) - (-log(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-136-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_136_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.nonnegative(x), Or(~Q.zero(x), re(exp(1)) > 0))
    Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-136-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_136_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Or(~Q.zero(x), re(exp(1)) > 0))
    Residual = Abs(Pow(x, exp(1))) - Pow(x, exp(1))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_137_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_137_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.nonnegative(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-137-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_137_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0))
    Residual = Abs(Pow(x, pi)) - Pow(x, pi)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-14-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_14_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = -sin(x) - sin(-x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-145-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_145_cond2__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Abs(x) <= 1)
    Residual = Abs(sin(acos(x))) - cos(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-145-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_145_condf__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), x > 1)
    Residual = Abs(sin(acos(x))) - cos(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-145-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_145_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = Abs(sin(acos(x))) - cos(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-147-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_147_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(cosh(asinh(x))), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-147-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_147_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(asinh(x))), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = Abs(tanh(asinh(x))) - cos(atan(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_151_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_151_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Abs(x) <= 1)
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-151-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_151_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = acos(cos(asin(x))) - Abs(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-153-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_153_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = acos(cos(cos(x))) - Abs(cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_154_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-154-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_154_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = acos(cos(sin(x))) - Abs(sin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-156-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_156_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Abs(x) <= 1)
    Residual = acos(sin(acos(x))) - Abs(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-156-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_156_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = acos(sin(acos(x))) - Abs(asin(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-159-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_159_cond2__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), x <= 1, ~Q.zero(cosh(x)))
    Residual = acos(tanh(Abs(x))) - asin(1 / cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-159-cond3 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_159_cond3__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Abs(x) <= pi / 2, ~Q.zero(cosh(x)))
    Residual = acos(tanh(Abs(x))) - asin(1 / cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-162-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_162_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), re(x) >= 0, Q.real(x))
    Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-162-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_162_condf__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x))
    Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-162-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_162_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = acosh(real_root(x, 5)) - acosh(Pow(x, Rational(1, 5)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-165-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_165_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = asin(cos(atan(x))) - Abs(atan(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-171-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_171_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Abs(im(x)) < pi, ~Q.zero(cosh(x)))
    Residual = asin(sin(tanh(x))) - tanh(x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-171-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_171_cond2__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)))
    Residual = asin(sin(tanh(x))) - tanh(x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-173-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_173_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = asin(tanh(Abs(x))) - acos(1 / cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-176-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_176_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = atan(Abs(sinh(x))) - acos(1 / cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-177-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_177_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(cos(x)))
    Residual = atan(Abs(tan(x))) - Abs(asin(sin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-179-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_179_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Abs(x) <= pi / 2, Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
    Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-179-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_179_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Ne(sinh(acos(x)), I, evaluate=False), Ne(sinh(acos(x)), -I, evaluate=False), ~Q.zero(cosh(acos(x))))
    Residual = atan(sinh(acos(x))) - asin(tanh(acos(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_180_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_180_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), re(x) > 0, Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-180-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_180_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Ne(sinh(acosh(x)), I, evaluate=False), Ne(sinh(acosh(x)), -I, evaluate=False), ~Q.zero(cosh(acosh(x))))
    Residual = atan(sinh(acosh(x))) - asin(tanh(acosh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-181-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_181_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Abs(x) <= pi / 2, Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
    Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-181-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_181_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Ne(sinh(asin(x)), I, evaluate=False), Ne(sinh(asin(x)), -I, evaluate=False), ~Q.zero(cosh(asin(x))))
    Residual = atan(sinh(asin(x))) - asin(tanh(asin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_183_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_183_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), re(x) > 0, ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-183-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_183_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), Ne(sinh(log(x)), I, evaluate=False), Ne(sinh(log(x)), -I, evaluate=False), ~Q.zero(cosh(log(x))))
    Residual = atan(sinh(log(x))) - asin(tanh(log(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-185-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_185_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(cos(cos(x))), Ne(tan(cos(x)), I, evaluate=False), Ne(tan(cos(x)), -I, evaluate=False))
    Residual = atan(tan(cos(x))) - cos(x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-186-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_186_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cos(sin(x))), Ne(tan(sin(x)), I, evaluate=False), Ne(tan(sin(x)), -I, evaluate=False))
    Residual = atan(tan(sin(x))) - sin(x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-187-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_187_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)), ~Q.zero(cos(tanh(x))), Ne(tan(tanh(x)), I, evaluate=False), Ne(tan(tanh(x)), -I, evaluate=False))
    Residual = atan(tan(tanh(x))) - tanh(x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_189_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-189-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_189_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Ne(cos(asin(x)), 1, evaluate=False), Ne(cos(asin(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(asin(x))) - acosh(Abs(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_190_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_190_condf__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-190-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_190_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Ne(cos(atan(x)), 1, evaluate=False), Ne(cos(atan(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(cos(atan(x))) - Abs(asinh(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_191_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_191_condf__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-191-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_191_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Ne(sin(acos(x)), 1, evaluate=False), Ne(sin(acos(x)), -1, evaluate=False), ~Q.zero(x))
    Residual = atanh(sin(acos(x))) - acosh(Abs(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-194-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_194_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Ne(sin(cos(x)), 1, evaluate=False), Ne(sin(cos(x)), -1, evaluate=False), ~Q.zero(cos(cos(x))))
    Residual = atanh(sin(cos(x))) - asinh(tan(cos(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-195-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_195_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Ne(sin(sin(x)), 1, evaluate=False), Ne(sin(sin(x)), -1, evaluate=False), ~Q.zero(cos(sin(x))))
    Residual = atanh(sin(sin(x))) - asinh(tan(sin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-196-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_196_cond2__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cosh(x)), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
    Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-196-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_196_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Ne(sin(tanh(x)), 1, evaluate=False), Ne(sin(tanh(x)), -1, evaluate=False), ~Q.zero(cos(tanh(x))))
    Residual = atanh(sin(tanh(x))) - asinh(tan(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-20-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_20_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = sinh(Abs(x)) - Abs(sinh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-20-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_20_condf__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x))
    Residual = sinh(Abs(x)) - Abs(sinh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-200-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_200_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x))
    Residual = cos(asin(sin(x))) - Abs(cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-202-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_202_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cos(x)), Ne(tan(x), I, evaluate=False), Ne(tan(x), -I, evaluate=False))
    Residual = cos(atan(tan(x))) - Abs(cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_203_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_203_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-203-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_203_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = cos(log(1 / x)) - cos(log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-205-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_205_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(cos(x)))
    Residual = cosh(asinh(tan(x))) - Abs(1 / cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-213-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_213_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-10 / x))
    Residual = 1 / (-10 / x) - (x / -10)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-216-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_216_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(-4 / x))
    Residual = 1 / (-4 / x) - (x / -4)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-218-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_218_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-6 / x))
    Residual = 1 / (-6 / x) - (x / -6)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_22_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-22-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_22_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = tanh(Abs(x)) - Abs(tanh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-220-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_220_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(-8 / x))
    Residual = 1 / (-8 / x) - (x / -8)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-229-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_229_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(Pow(pi, x)))
    Residual = 1 / Pow(pi, x) - Pow(1 / pi, x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-233-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_233_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)), Or(~Q.zero(x), re(-pi) > 0))
    Residual = 1 / Pow(x, pi) - Pow(x, -pi)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_234_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_234_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), re(x) >= 0, Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_234_cond2__sympy_ask():
    x = Symbol('x', integer=True)
    Assum = And(Q.integer(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-234-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_234_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0))
    Residual = 1 / Pow(x, x) - Pow(1 / x, x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-241-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_241_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 3)), ~Q.zero(x))
    Residual = log(real_root(x, 3)) - (log(x) / 3)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-243-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_243_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), re(x) > 0, Q.real(x), ~Q.zero(real_root(x, 5)), ~Q.zero(x))
    Residual = log(real_root(x, 5)) - (log(x) / 5)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-245-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_245_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), re(x) > 0, Q.real(x), ~Q.zero(real_root(x, 7)), ~Q.zero(x))
    Residual = log(real_root(x, 7)) - (log(x) / 7)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-247-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_247_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(real_root(x, 9)), ~Q.zero(x))
    Residual = log(real_root(x, 9)) - (log(x) / 9)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-248-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_248_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Abs(x) <= 1)
    Residual = -Abs(asin(x)) - asin(-Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-248-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_248_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = -Abs(asin(x)) - asin(-Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-249-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_249_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = -Abs(asinh(x)) - asinh(-Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-251-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_251_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Abs(x) < 1, Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
    Residual = -Abs(atanh(x)) - atanh(-Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-251-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_251_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False), Ne(-Abs(x), 1, evaluate=False), Ne(-Abs(x), -1, evaluate=False))
    Residual = -Abs(atanh(x)) - atanh(-Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_252_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-252-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_252_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = -Abs(sinh(x)) - sinh(-Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_253_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-253-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_253_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = -Abs(tanh(x)) - tanh(-Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-256-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_256_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(-exp(x)))
    Residual = -exp(-x) - (1 / -exp(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_260_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_260_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Abs(re(x)) < pi / 2, ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-260-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_260_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(1 / cos(x)))
    Residual = -log(cos(x)) - log(1 / cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_261_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_261_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), re(x) > 0, ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-261-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_261_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(cosh(x)), ~Q.zero(1 / cosh(x)))
    Residual = -log(cosh(x)) - log(1 / cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_266_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_266_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-condf · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_266_condf__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-266-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_266_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = -sin(log(x)) - sin(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_267_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_267_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_267_condf__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-267-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_267_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = -tan(log(x)) - tan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-274-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_274_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -2) - Pow(x, -2)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-275-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_275_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -3) - Abs(Pow(x, -3))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-276-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_276_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -4) - Pow(x, -4)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-278-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_278_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = Pow(Abs(x), -6) - Pow(x, -6)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_283_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_283_condf__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-283-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_283_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 2) - (x * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-284-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_284_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 3) - Abs(Pow(x, 3))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-286-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_286_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 5) - Abs(Pow(x, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-287-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_287_condf__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x))
    Residual = Pow(Abs(x), 6) - Pow(x, 6)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-288-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_288_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = Pow(Abs(x), 7) - Abs(Pow(x, 7))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-289-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_289_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x))
    Residual = Pow(Abs(x), 8) - Pow(x, 8)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-289-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_289_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = Pow(Abs(x), 8) - Pow(x, 8)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-29-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_29_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
    Residual = 3 * log(x) - log(Pow(x, 3))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-29-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_29_condf__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
    Residual = 3 * log(x) - log(Pow(x, 3))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-29-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_29_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 3)))
    Residual = 3 * log(x) - log(Pow(x, 3))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-3-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_3_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = asinh(sinh(x)) - x
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-30-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_30_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = 4 * Abs(x) - Abs(-4 * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-31-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_31_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = 5 * Abs(x) - Abs(-5 * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-326-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_326_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = Pow(exp(x), 2) - exp(2 * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-33-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_33_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = 6 * Abs(x) - Abs(-6 * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-334-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_334_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(exp(1)) > 0))
    Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-334-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_334_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), Or(~Q.zero(exp(x)), re(exp(1)) > 0))
    Residual = Pow(exp(x), exp(1)) - exp(exp(1) * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-335-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_335_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(pi) > 0))
    Residual = Pow(exp(x), pi) - exp(pi * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-335-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_335_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), Or(~Q.zero(exp(x)), re(pi) > 0))
    Residual = Pow(exp(x), pi) - exp(pi * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-336-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_336_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Or(~Q.zero(exp(x)), re(x) > 0))
    Residual = Pow(exp(x), x) - exp(x * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-336-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_336_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), Or(~Q.zero(exp(x)), re(x) > 0))
    Residual = Pow(exp(x), x) - exp(x * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_343_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-343-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_343_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = Pow(1 / pi, x) - Pow(pi, -x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_344_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_344_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_344_cond2__sympy_ask():
    x = Symbol('x', integer=True)
    Assum = And(Q.integer(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-344-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_344_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(1 / x), re(x) > 0), Or(~Q.zero(x), re(-x) > 0))
    Residual = Pow(1 / x, x) - Pow(x, -x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-35-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_35_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 7)))
    Residual = 7 * log(x) - log(Pow(x, 7))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-354-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_354_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(5)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(5)) - Pow(5, log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-356-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_356_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(7)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(7)) - Pow(7, log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-359-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_359_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Or(~Q.zero(x), re(log(pi)) > 0), ~Q.zero(x))
    Residual = Pow(x, log(pi)) - Pow(pi, log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-364-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_364_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 3) - Abs(real_root(x, 3))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-367-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_367_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = real_root(Abs(x), 9) - Abs(real_root(x, 9))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_368_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-368-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_368_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.real(acos(x)), ~Q.zero(acos(x)))
    Residual = real_root(acos(x), -5) - Pow(acos(x), Rational(-1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_369_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-369-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_369_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.real(acos(x)))
    Residual = real_root(acos(x), 5) - Pow(acos(x), Rational(1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_370_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-370-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_370_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.real(acosh(x)), ~Q.zero(acosh(x)))
    Residual = real_root(acosh(x), -5) - Pow(acosh(x), Rational(-1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_371_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-371-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_371_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.real(acosh(x)))
    Residual = real_root(acosh(x), 5) - Pow(acosh(x), Rational(1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_372_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.real(cosh(x)), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_372_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), re(x) > 0, Q.real(cosh(x)), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-372-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_372_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(cosh(x)))
    Residual = real_root(cosh(x), -5) - Pow(cosh(x), Rational(-1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_373_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.real(cosh(x)))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_373_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), re(x) > 0, Q.real(cosh(x)))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-373-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_373_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = real_root(cosh(x), 5) - Pow(cosh(x), Rational(1, 5))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-376-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_376_cond2__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Abs(im(x)) < pi, Q.real(exp(x)), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -3) - exp(x / -3)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-378-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_378_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -5) - exp(x / -5)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-38-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_38_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(Pow(x, 9)))
    Residual = 9 * log(x) - log(Pow(x, 9))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-380-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_380_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(exp(x)))
    Residual = real_root(exp(x), -7) - exp(x / -7)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-385-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_385_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), re(x) > 0, Q.real(exp(x)))
    Residual = real_root(exp(x), 3) - exp(x / 3)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-387-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_387_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 5) - exp(x / 5)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-389-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_389_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.real(exp(x)))
    Residual = real_root(exp(x), 7) - exp(x / 7)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-392-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_392_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Abs(x) <= 1)
    Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-392-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_392_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = sin(Abs(asin(x))) - Abs(cos(acos(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-394-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_394_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Abs(x) < 1, Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-394-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_394_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(Abs(atanh(x))) - Abs(sin(atanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-395-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_395_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = sin(Abs(cos(x))) - Abs(sin(cos(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_396_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-396-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_396_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = sin(Abs(sin(x))) - Abs(sin(sin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-397-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_397_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = sin(Abs(tanh(x))) - Abs(sin(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-399-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_399_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x))
    Residual = sin(acos(sin(x))) - Abs(cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-40-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_40_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = Abs(x) * pi - Abs(pi * x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-402-cond · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_402_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Abs(x) < 1, Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-402-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_402_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = sin(atanh(Abs(x))) - Abs(sin(atanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_403_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_403_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-condf · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_403_condf__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-403-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_403_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(1 / x))
    Residual = sin(-log(x)) - sin(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_404_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-404-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_404_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = sin(tanh(Abs(x))) - Abs(sin(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-410-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_410_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(sinh(x)))
    Residual = sinh(exp(log(x))) - exp(log(sinh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-412-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_412_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Abs(x) < 1, ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-412-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_412_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(asin(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(Abs(asin(x))) - Abs(tan(asin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-413-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_413_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(cos(x)))), ~Q.zero(cos(cos(x))))
    Residual = tan(Abs(cos(x))) - Abs(tan(cos(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_414_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-414-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_414_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(sin(x)))), ~Q.zero(cos(sin(x))))
    Residual = tan(Abs(sin(x))) - Abs(tan(sin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_415_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-415-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_415_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(cos(Abs(tanh(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(Abs(tanh(x))) - Abs(tan(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-416-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_416_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Abs(x) <= 1, ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
    Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-416-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_416_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(cos(acos(Abs(x)))), ~Q.zero(cos(acos(x))))
    Residual = tan(acos(Abs(x))) - Abs(tan(acos(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-417-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_417_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Abs(x) < 1, ~Q.zero(cos(asin(Abs(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-417-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_417_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(cos(asin(Abs(x)))), ~Q.zero(cos(asin(x))))
    Residual = tan(asin(Abs(x))) - Abs(tan(asin(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_420_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_420_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_420_condf__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-420-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_420_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cos(-log(x))), ~Q.zero(1 / x), ~Q.zero(cos(log(1 / x))))
    Residual = tan(-log(x)) - tan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_421_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cosh(x)), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-421-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_421_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(cos(tanh(Abs(x)))), ~Q.zero(cos(tanh(x))))
    Residual = tan(tanh(Abs(x))) - Abs(tan(tanh(x)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-422-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_422_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-422-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_422_condf__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(Abs(asinh(x))) - cos(atan(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-423-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_423_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(cosh(acosh(Abs(x)))), ~Q.zero(x))
    Residual = tanh(acosh(Abs(x))) - cos(asin(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-424-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_424_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-424-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_424_condf__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), Ne(1 / x, I, evaluate=False), Ne(1 / x, -I, evaluate=False))
    Residual = tanh(asinh(Abs(x))) - cos(atan(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-428-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_428_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), x <= 1)
    Residual = atan(sinh(x)) - asin(tanh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-428-cond3 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_428_cond3__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), x >= 0, x <= pi)
    Residual = atan(sinh(x)) - asin(tanh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_430_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_430_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-cond2 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_430_cond2__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Abs(x) < 1, ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-430-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_430_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(x) > 0), ~Q.zero(Pow(x, x)))
    Residual = log(x) * x - log(Pow(x, x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-432-cond3 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_432_cond3__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Abs(x) <= pi / 2, ~Q.zero(cosh(x)))
    Residual = acos(Abs(tanh(x))) - asin(1 / cosh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_433_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_433_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), re(x) >= 0, ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_433_condf__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.negative(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-433-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_433_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), Ne(-log(x), I, evaluate=False), Ne(-log(x), -I, evaluate=False), ~Q.zero(1 / x), Ne(log(1 / x), I, evaluate=False), Ne(log(1 / x), -I, evaluate=False))
    Residual = atan(-log(x)) - atan(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_442_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_442_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-cond4 · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_442_cond4__sympy_ask():
    x = Symbol('x', integer=True)
    Assum = And(Q.integer(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-442-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_442_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(1 / log(x)))
    Residual = -log(log(x)) - log(1 / log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-446-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_446_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Ne(x, I, evaluate=False), Ne(x, -I, evaluate=False), ~Q.zero(cos(Abs(atan(x)))))
    Residual = tan(Abs(atan(x))) - Abs(x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-449-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_449_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(cosh(-log(x))), ~Q.zero(1 / x), ~Q.zero(cosh(log(1 / x))))
    Residual = tanh(-log(x)) - tanh(log(1 / x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_450_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = x / x - 1
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-450-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_450_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = x / x - 1
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_451_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-451-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_451_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x))
    Residual = 0 / x - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-46-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_46_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), ~Q.zero(Pow(2, x)))
    Residual = log(2) * x - log(Pow(2, x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_5_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Abs(x) < 1, Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = atanh(Abs(x)) - Abs(atanh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_5_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Ne(Abs(x), 1, evaluate=False), Ne(x, 1, evaluate=False), Ne(x, -1, evaluate=False))
    Residual = atanh(Abs(x)) - Abs(atanh(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_50_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-50-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_50_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(Pow(6, x)))
    Residual = log(6) * x - log(Pow(6, x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-51-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_51_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(Pow(7, x)))
    Residual = log(7) * x - log(Pow(7, x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5372-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_5372_ground__sympy_ask():
    Assum = And()
    Residual = sin(asin(Integer(1) / -4)) - Rational(-1, 4)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5382-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_5382_ground__sympy_ask():
    Assum = And()
    Residual = sinh(log(Integer(1) / 4)) - Rational(-15, 8)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-5385-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_5385_ground__sympy_ask():
    Assum = And()
    Residual = sinh(-log(4)) - Rational(-15, 8)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_55_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_55_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-55-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_55_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(exp(1)) > 0), ~Q.zero(Pow(x, exp(1))))
    Residual = log(x) * exp(1) - log(Pow(x, exp(1)))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_56_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_56_cond__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Q.positive(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-condf · expected false · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_56_condf__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), Q.imaginary(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-56-real · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_56_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), Or(~Q.zero(x), re(pi) > 0), ~Q.zero(Pow(x, pi)))
    Residual = log(x) * pi - log(Pow(x, pi))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_6_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(cosh(x)), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-6-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_6_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), Ne(tanh(x), 1, evaluate=False), Ne(tanh(x), -1, evaluate=False))
    Residual = atanh(tanh(x)) - x
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-7-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_7_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 1 / Abs(x) - Abs(1 / x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-73-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_73_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(-Abs(x)))
    Residual = -1 / Abs(x) - (1 / -Abs(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-80-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_80_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(-cos(x)))
    Residual = -1 / cos(x) - (1 / -cos(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-806-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_806_ground__sympy_ask():
    Assum = And()
    Residual = cosh(0) - 1
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-813-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_813_ground__sympy_ask():
    Assum = And()
    Residual = sinh(0) - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-816-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_816_ground__sympy_ask():
    Assum = And()
    Residual = tanh(0) - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-819-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_819_ground__sympy_ask():
    Assum = And()
    Residual = 0 / pi - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-83-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_83_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(x), ~Q.zero(log(x)), ~Q.zero(-log(x)))
    Residual = -1 / log(x) - (1 / -log(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-837-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_837_ground__sympy_ask():
    Assum = And()
    Residual = Pow(0, pi) - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-848-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_848_ground__sympy_ask():
    Assum = And()
    Residual = sinh(log(4)) - Rational(15, 8)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-86-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_86_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(cos(x)), ~Q.zero(tan(x)), ~Q.zero(-tan(x)))
    Residual = -1 / tan(x) - (1 / -tan(x))
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-868-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_868_ground__sympy_ask():
    Assum = And()
    Residual = 0 * acosh(7) - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-9-complex · expected contingent · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (declined correctly)
@_in(_SETUP1)
def sp_acj4_9_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(exp(x)))
    Residual = log(exp(x)) - x
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-9-cond · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered null (no verdict)
@_in(_SETUP1)
def sp_acj4_9_cond__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), And(im(x) > -pi, im(x) <= pi), ~Q.zero(exp(x)))
    Residual = log(exp(x)) - x
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_90_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-90-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_90_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 3 / Abs(x) - Abs(-3 / x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-911-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_911_ground__sympy_ask():
    Assum = And()
    Residual = 0 / asin(-1) - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-927-ground · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_927_ground__sympy_ask():
    Assum = And()
    Residual = 0 / asinh(4) - 0
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-94-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_94_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x), ~Q.zero(Abs(x)), ~Q.zero(x))
    Residual = 7 / Abs(x) - Abs(-7 / x)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-complex · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_99_complex__sympy_ask():
    x = Symbol('x', complex=True)
    Assum = And(Q.complex(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# ---- case sp-acj4-99-real · expected true · system sympy-ask (sympy 1.14.0)
# the run sympy-ask-20261015-024703 answered true (solved)
@_in(_SETUP1)
def sp_acj4_99_real__sympy_ask():
    x = Symbol('x', real=True)
    Assum = And(Q.real(x))
    Residual = Abs(x) / 3 - Abs(x / -3)
    Answer = ask(Q.zero(Residual), Assum)
    print(Residual, Answer, sep='\n')
    return Answer


# (case, system, expected, the stored run's answer, that run, its function)
CASES = [
    ('sp-acj4-0-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_0_complex__sympy_ask),
    ('sp-acj4-0-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_0_real__sympy_ask),
    ('sp-acj4-1-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_1_cond__sympy_ask),
    ('sp-acj4-1-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_1_real__sympy_ask),
    ('sp-acj4-1007-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_1007_ground__sympy_ask),
    ('sp-acj4-102-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_102_complex__sympy_ask),
    ('sp-acj4-102-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_102_real__sympy_ask),
    ('sp-acj4-108-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_108_complex__sympy_ask),
    ('sp-acj4-108-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261015-024703', sp_acj4_108_condf__sympy_ask),
    ('sp-acj4-108-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_108_real__sympy_ask),
    ('sp-acj4-1107-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_1107_ground__sympy_ask),
    ('sp-acj4-1148-ground', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_1148_ground__sympy_ask),
    ('sp-acj4-1149-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_1149_ground__sympy_ask),
    ('sp-acj4-115-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_115_real__sympy_ask),
    ('sp-acj4-116-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_116_real__sympy_ask),
    ('sp-acj4-1177-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_1177_ground__sympy_ask),
    ('sp-acj4-1195-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_1195_ground__sympy_ask),
    ('sp-acj4-120-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_120_complex__sympy_ask),
    ('sp-acj4-120-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_120_real__sympy_ask),
    ('sp-acj4-1217-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_1217_ground__sympy_ask),
    ('sp-acj4-1238-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_1238_ground__sympy_ask),
    ('sp-acj4-124-condf', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_124_condf__sympy_ask),
    ('sp-acj4-1247-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_1247_ground__sympy_ask),
    ('sp-acj4-1254-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_1254_ground__sympy_ask),
    ('sp-acj4-1258-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_1258_ground__sympy_ask),
    ('sp-acj4-127-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261015-024703', sp_acj4_127_condf__sympy_ask),
    ('sp-acj4-127-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_127_real__sympy_ask),
    ('sp-acj4-128-cond2', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_128_cond2__sympy_ask),
    ('sp-acj4-128-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261015-024703', sp_acj4_128_condf__sympy_ask),
    ('sp-acj4-128-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_128_real__sympy_ask),
    ('sp-acj4-129-cond', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_129_cond__sympy_ask),
    ('sp-acj4-130-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_130_complex__sympy_ask),
    ('sp-acj4-130-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_130_cond__sympy_ask),
    ('sp-acj4-130-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_130_real__sympy_ask),
    ('sp-acj4-131-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_131_complex__sympy_ask),
    ('sp-acj4-131-condf', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_131_condf__sympy_ask),
    ('sp-acj4-131-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_131_real__sympy_ask),
    ('sp-acj4-132-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_132_complex__sympy_ask),
    ('sp-acj4-132-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_132_cond__sympy_ask),
    ('sp-acj4-132-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_132_real__sympy_ask),
    ('sp-acj4-133-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_133_complex__sympy_ask),
    ('sp-acj4-133-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261015-024703', sp_acj4_133_condf__sympy_ask),
    ('sp-acj4-133-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_133_real__sympy_ask),
    ('sp-acj4-136-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_136_cond__sympy_ask),
    ('sp-acj4-136-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_136_real__sympy_ask),
    ('sp-acj4-137-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_137_complex__sympy_ask),
    ('sp-acj4-137-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_137_cond__sympy_ask),
    ('sp-acj4-137-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_137_real__sympy_ask),
    ('sp-acj4-14-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_14_real__sympy_ask),
    ('sp-acj4-145-cond2', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_145_cond2__sympy_ask),
    ('sp-acj4-145-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261015-024703', sp_acj4_145_condf__sympy_ask),
    ('sp-acj4-145-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_145_real__sympy_ask),
    ('sp-acj4-147-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_147_complex__sympy_ask),
    ('sp-acj4-147-cond', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_147_cond__sympy_ask),
    ('sp-acj4-151-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_151_complex__sympy_ask),
    ('sp-acj4-151-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_151_cond__sympy_ask),
    ('sp-acj4-151-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_151_real__sympy_ask),
    ('sp-acj4-153-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_153_complex__sympy_ask),
    ('sp-acj4-154-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_154_complex__sympy_ask),
    ('sp-acj4-154-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_154_real__sympy_ask),
    ('sp-acj4-156-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_156_cond__sympy_ask),
    ('sp-acj4-156-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_156_real__sympy_ask),
    ('sp-acj4-159-cond2', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_159_cond2__sympy_ask),
    ('sp-acj4-159-cond3', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_159_cond3__sympy_ask),
    ('sp-acj4-162-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_162_cond__sympy_ask),
    ('sp-acj4-162-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261015-024703', sp_acj4_162_condf__sympy_ask),
    ('sp-acj4-162-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_162_real__sympy_ask),
    ('sp-acj4-165-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_165_complex__sympy_ask),
    ('sp-acj4-171-cond', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_171_cond__sympy_ask),
    ('sp-acj4-171-cond2', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_171_cond2__sympy_ask),
    ('sp-acj4-173-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_173_complex__sympy_ask),
    ('sp-acj4-176-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_176_complex__sympy_ask),
    ('sp-acj4-177-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_177_complex__sympy_ask),
    ('sp-acj4-179-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_179_cond__sympy_ask),
    ('sp-acj4-179-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_179_real__sympy_ask),
    ('sp-acj4-180-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_180_complex__sympy_ask),
    ('sp-acj4-180-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_180_cond__sympy_ask),
    ('sp-acj4-180-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_180_real__sympy_ask),
    ('sp-acj4-181-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_181_cond__sympy_ask),
    ('sp-acj4-181-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_181_real__sympy_ask),
    ('sp-acj4-183-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_183_complex__sympy_ask),
    ('sp-acj4-183-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_183_cond__sympy_ask),
    ('sp-acj4-183-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_183_real__sympy_ask),
    ('sp-acj4-185-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_185_real__sympy_ask),
    ('sp-acj4-186-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_186_cond__sympy_ask),
    ('sp-acj4-187-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_187_cond__sympy_ask),
    ('sp-acj4-189-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_189_complex__sympy_ask),
    ('sp-acj4-189-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_189_real__sympy_ask),
    ('sp-acj4-190-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_190_complex__sympy_ask),
    ('sp-acj4-190-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261015-024703', sp_acj4_190_condf__sympy_ask),
    ('sp-acj4-190-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_190_real__sympy_ask),
    ('sp-acj4-191-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_191_complex__sympy_ask),
    ('sp-acj4-191-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261015-024703', sp_acj4_191_condf__sympy_ask),
    ('sp-acj4-191-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_191_real__sympy_ask),
    ('sp-acj4-194-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_194_real__sympy_ask),
    ('sp-acj4-195-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_195_real__sympy_ask),
    ('sp-acj4-196-cond2', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_196_cond2__sympy_ask),
    ('sp-acj4-196-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_196_real__sympy_ask),
    ('sp-acj4-20-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_20_complex__sympy_ask),
    ('sp-acj4-20-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261015-024703', sp_acj4_20_condf__sympy_ask),
    ('sp-acj4-200-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_200_cond__sympy_ask),
    ('sp-acj4-202-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_202_cond__sympy_ask),
    ('sp-acj4-203-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_203_complex__sympy_ask),
    ('sp-acj4-203-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_203_cond__sympy_ask),
    ('sp-acj4-203-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_203_real__sympy_ask),
    ('sp-acj4-205-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_205_cond__sympy_ask),
    ('sp-acj4-213-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_213_complex__sympy_ask),
    ('sp-acj4-216-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_216_complex__sympy_ask),
    ('sp-acj4-218-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_218_real__sympy_ask),
    ('sp-acj4-22-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_22_complex__sympy_ask),
    ('sp-acj4-22-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_22_real__sympy_ask),
    ('sp-acj4-220-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_220_real__sympy_ask),
    ('sp-acj4-229-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_229_real__sympy_ask),
    ('sp-acj4-233-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_233_real__sympy_ask),
    ('sp-acj4-234-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_234_complex__sympy_ask),
    ('sp-acj4-234-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_234_cond__sympy_ask),
    ('sp-acj4-234-cond2', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_234_cond2__sympy_ask),
    ('sp-acj4-234-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_234_real__sympy_ask),
    ('sp-acj4-241-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_241_real__sympy_ask),
    ('sp-acj4-243-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_243_cond__sympy_ask),
    ('sp-acj4-245-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_245_cond__sympy_ask),
    ('sp-acj4-247-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_247_real__sympy_ask),
    ('sp-acj4-248-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_248_cond__sympy_ask),
    ('sp-acj4-248-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_248_real__sympy_ask),
    ('sp-acj4-249-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_249_real__sympy_ask),
    ('sp-acj4-251-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_251_cond__sympy_ask),
    ('sp-acj4-251-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_251_real__sympy_ask),
    ('sp-acj4-252-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_252_complex__sympy_ask),
    ('sp-acj4-252-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_252_real__sympy_ask),
    ('sp-acj4-253-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_253_complex__sympy_ask),
    ('sp-acj4-253-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_253_real__sympy_ask),
    ('sp-acj4-256-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_256_real__sympy_ask),
    ('sp-acj4-260-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_260_complex__sympy_ask),
    ('sp-acj4-260-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_260_cond__sympy_ask),
    ('sp-acj4-260-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_260_real__sympy_ask),
    ('sp-acj4-261-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_261_complex__sympy_ask),
    ('sp-acj4-261-cond', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_261_cond__sympy_ask),
    ('sp-acj4-261-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_261_real__sympy_ask),
    ('sp-acj4-266-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_266_complex__sympy_ask),
    ('sp-acj4-266-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_266_cond__sympy_ask),
    ('sp-acj4-266-condf', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_266_condf__sympy_ask),
    ('sp-acj4-266-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_266_real__sympy_ask),
    ('sp-acj4-267-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_267_complex__sympy_ask),
    ('sp-acj4-267-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_267_cond__sympy_ask),
    ('sp-acj4-267-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261015-024703', sp_acj4_267_condf__sympy_ask),
    ('sp-acj4-267-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_267_real__sympy_ask),
    ('sp-acj4-274-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_274_complex__sympy_ask),
    ('sp-acj4-275-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_275_real__sympy_ask),
    ('sp-acj4-276-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_276_real__sympy_ask),
    ('sp-acj4-278-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_278_complex__sympy_ask),
    ('sp-acj4-283-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_283_complex__sympy_ask),
    ('sp-acj4-283-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261015-024703', sp_acj4_283_condf__sympy_ask),
    ('sp-acj4-283-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_283_real__sympy_ask),
    ('sp-acj4-284-complex', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_284_complex__sympy_ask),
    ('sp-acj4-286-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_286_real__sympy_ask),
    ('sp-acj4-287-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261015-024703', sp_acj4_287_condf__sympy_ask),
    ('sp-acj4-288-complex', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_288_complex__sympy_ask),
    ('sp-acj4-289-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_289_cond__sympy_ask),
    ('sp-acj4-289-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_289_real__sympy_ask),
    ('sp-acj4-29-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_29_cond__sympy_ask),
    ('sp-acj4-29-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261015-024703', sp_acj4_29_condf__sympy_ask),
    ('sp-acj4-29-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_29_real__sympy_ask),
    ('sp-acj4-3-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_3_real__sympy_ask),
    ('sp-acj4-30-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_30_complex__sympy_ask),
    ('sp-acj4-31-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_31_real__sympy_ask),
    ('sp-acj4-326-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_326_real__sympy_ask),
    ('sp-acj4-33-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_33_real__sympy_ask),
    ('sp-acj4-334-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_334_complex__sympy_ask),
    ('sp-acj4-334-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_334_cond__sympy_ask),
    ('sp-acj4-335-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_335_complex__sympy_ask),
    ('sp-acj4-335-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_335_cond__sympy_ask),
    ('sp-acj4-336-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_336_complex__sympy_ask),
    ('sp-acj4-336-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_336_cond__sympy_ask),
    ('sp-acj4-343-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_343_complex__sympy_ask),
    ('sp-acj4-343-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_343_real__sympy_ask),
    ('sp-acj4-344-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_344_complex__sympy_ask),
    ('sp-acj4-344-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_344_cond__sympy_ask),
    ('sp-acj4-344-cond2', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_344_cond2__sympy_ask),
    ('sp-acj4-344-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_344_real__sympy_ask),
    ('sp-acj4-35-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_35_real__sympy_ask),
    ('sp-acj4-354-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_354_real__sympy_ask),
    ('sp-acj4-356-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_356_real__sympy_ask),
    ('sp-acj4-359-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_359_real__sympy_ask),
    ('sp-acj4-364-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_364_real__sympy_ask),
    ('sp-acj4-367-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_367_real__sympy_ask),
    ('sp-acj4-368-complex', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_368_complex__sympy_ask),
    ('sp-acj4-368-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_368_real__sympy_ask),
    ('sp-acj4-369-complex', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_369_complex__sympy_ask),
    ('sp-acj4-369-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_369_real__sympy_ask),
    ('sp-acj4-370-complex', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_370_complex__sympy_ask),
    ('sp-acj4-370-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_370_real__sympy_ask),
    ('sp-acj4-371-complex', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_371_complex__sympy_ask),
    ('sp-acj4-371-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_371_real__sympy_ask),
    ('sp-acj4-372-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_372_complex__sympy_ask),
    ('sp-acj4-372-cond', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_372_cond__sympy_ask),
    ('sp-acj4-372-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_372_real__sympy_ask),
    ('sp-acj4-373-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_373_complex__sympy_ask),
    ('sp-acj4-373-cond', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_373_cond__sympy_ask),
    ('sp-acj4-373-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_373_real__sympy_ask),
    ('sp-acj4-376-cond2', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_376_cond2__sympy_ask),
    ('sp-acj4-378-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_378_real__sympy_ask),
    ('sp-acj4-38-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_38_real__sympy_ask),
    ('sp-acj4-380-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_380_real__sympy_ask),
    ('sp-acj4-385-cond', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_385_cond__sympy_ask),
    ('sp-acj4-387-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_387_complex__sympy_ask),
    ('sp-acj4-389-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_389_complex__sympy_ask),
    ('sp-acj4-392-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_392_cond__sympy_ask),
    ('sp-acj4-392-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_392_real__sympy_ask),
    ('sp-acj4-394-cond', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_394_cond__sympy_ask),
    ('sp-acj4-394-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_394_real__sympy_ask),
    ('sp-acj4-395-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_395_real__sympy_ask),
    ('sp-acj4-396-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_396_complex__sympy_ask),
    ('sp-acj4-396-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_396_real__sympy_ask),
    ('sp-acj4-397-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_397_real__sympy_ask),
    ('sp-acj4-399-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_399_cond__sympy_ask),
    ('sp-acj4-40-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_40_complex__sympy_ask),
    ('sp-acj4-402-cond', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_402_cond__sympy_ask),
    ('sp-acj4-402-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_402_real__sympy_ask),
    ('sp-acj4-403-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_403_complex__sympy_ask),
    ('sp-acj4-403-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_403_cond__sympy_ask),
    ('sp-acj4-403-condf', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_403_condf__sympy_ask),
    ('sp-acj4-403-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_403_real__sympy_ask),
    ('sp-acj4-404-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_404_complex__sympy_ask),
    ('sp-acj4-404-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_404_real__sympy_ask),
    ('sp-acj4-410-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_410_real__sympy_ask),
    ('sp-acj4-412-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_412_cond__sympy_ask),
    ('sp-acj4-412-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_412_real__sympy_ask),
    ('sp-acj4-413-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_413_real__sympy_ask),
    ('sp-acj4-414-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_414_complex__sympy_ask),
    ('sp-acj4-414-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_414_real__sympy_ask),
    ('sp-acj4-415-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_415_complex__sympy_ask),
    ('sp-acj4-415-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_415_real__sympy_ask),
    ('sp-acj4-416-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_416_cond__sympy_ask),
    ('sp-acj4-416-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_416_real__sympy_ask),
    ('sp-acj4-417-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_417_cond__sympy_ask),
    ('sp-acj4-417-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_417_real__sympy_ask),
    ('sp-acj4-420-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_420_complex__sympy_ask),
    ('sp-acj4-420-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_420_cond__sympy_ask),
    ('sp-acj4-420-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261015-024703', sp_acj4_420_condf__sympy_ask),
    ('sp-acj4-420-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_420_real__sympy_ask),
    ('sp-acj4-421-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_421_complex__sympy_ask),
    ('sp-acj4-421-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_421_real__sympy_ask),
    ('sp-acj4-422-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_422_complex__sympy_ask),
    ('sp-acj4-422-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261015-024703', sp_acj4_422_condf__sympy_ask),
    ('sp-acj4-423-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_423_complex__sympy_ask),
    ('sp-acj4-424-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_424_complex__sympy_ask),
    ('sp-acj4-424-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261015-024703', sp_acj4_424_condf__sympy_ask),
    ('sp-acj4-428-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_428_cond__sympy_ask),
    ('sp-acj4-428-cond3', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_428_cond3__sympy_ask),
    ('sp-acj4-430-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_430_complex__sympy_ask),
    ('sp-acj4-430-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_430_cond__sympy_ask),
    ('sp-acj4-430-cond2', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_430_cond2__sympy_ask),
    ('sp-acj4-430-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_430_real__sympy_ask),
    ('sp-acj4-432-cond3', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_432_cond3__sympy_ask),
    ('sp-acj4-433-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_433_complex__sympy_ask),
    ('sp-acj4-433-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_433_cond__sympy_ask),
    ('sp-acj4-433-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261015-024703', sp_acj4_433_condf__sympy_ask),
    ('sp-acj4-433-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_433_real__sympy_ask),
    ('sp-acj4-442-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_442_complex__sympy_ask),
    ('sp-acj4-442-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_442_cond__sympy_ask),
    ('sp-acj4-442-cond4', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_442_cond4__sympy_ask),
    ('sp-acj4-442-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_442_real__sympy_ask),
    ('sp-acj4-446-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_446_complex__sympy_ask),
    ('sp-acj4-449-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_449_real__sympy_ask),
    ('sp-acj4-450-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_450_complex__sympy_ask),
    ('sp-acj4-450-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_450_real__sympy_ask),
    ('sp-acj4-451-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_451_complex__sympy_ask),
    ('sp-acj4-451-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_451_real__sympy_ask),
    ('sp-acj4-46-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_46_cond__sympy_ask),
    ('sp-acj4-5-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_5_cond__sympy_ask),
    ('sp-acj4-5-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_5_real__sympy_ask),
    ('sp-acj4-50-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_50_complex__sympy_ask),
    ('sp-acj4-50-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_50_real__sympy_ask),
    ('sp-acj4-51-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_51_complex__sympy_ask),
    ('sp-acj4-5372-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_5372_ground__sympy_ask),
    ('sp-acj4-5382-ground', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_5382_ground__sympy_ask),
    ('sp-acj4-5385-ground', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_5385_ground__sympy_ask),
    ('sp-acj4-55-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_55_complex__sympy_ask),
    ('sp-acj4-55-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_55_cond__sympy_ask),
    ('sp-acj4-55-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_55_real__sympy_ask),
    ('sp-acj4-56-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_56_complex__sympy_ask),
    ('sp-acj4-56-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_56_cond__sympy_ask),
    ('sp-acj4-56-condf', 'sympy-ask', 'false', 'null', 'sympy-ask-20261015-024703', sp_acj4_56_condf__sympy_ask),
    ('sp-acj4-56-real', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_56_real__sympy_ask),
    ('sp-acj4-6-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_6_complex__sympy_ask),
    ('sp-acj4-6-real', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_6_real__sympy_ask),
    ('sp-acj4-7-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_7_complex__sympy_ask),
    ('sp-acj4-73-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_73_real__sympy_ask),
    ('sp-acj4-80-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_80_real__sympy_ask),
    ('sp-acj4-806-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_806_ground__sympy_ask),
    ('sp-acj4-813-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_813_ground__sympy_ask),
    ('sp-acj4-816-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_816_ground__sympy_ask),
    ('sp-acj4-819-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_819_ground__sympy_ask),
    ('sp-acj4-83-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_83_real__sympy_ask),
    ('sp-acj4-837-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_837_ground__sympy_ask),
    ('sp-acj4-848-ground', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_848_ground__sympy_ask),
    ('sp-acj4-86-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_86_real__sympy_ask),
    ('sp-acj4-868-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_868_ground__sympy_ask),
    ('sp-acj4-9-complex', 'sympy-ask', 'contingent', 'null', 'sympy-ask-20261015-024703', sp_acj4_9_complex__sympy_ask),
    ('sp-acj4-9-cond', 'sympy-ask', 'true', 'null', 'sympy-ask-20261015-024703', sp_acj4_9_cond__sympy_ask),
    ('sp-acj4-90-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_90_complex__sympy_ask),
    ('sp-acj4-90-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_90_real__sympy_ask),
    ('sp-acj4-911-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_911_ground__sympy_ask),
    ('sp-acj4-927-ground', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_927_ground__sympy_ask),
    ('sp-acj4-94-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_94_complex__sympy_ask),
    ('sp-acj4-99-complex', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_99_complex__sympy_ask),
    ('sp-acj4-99-real', 'sympy-ask', 'true', 'true', 'sympy-ask-20261015-024703', sp_acj4_99_real__sympy_ask),
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
