"""Autograder used by the Python Course page. Runs inside Pyodide (and CPython for checks).

grade(code, spec_json) -> JSON list of case results.
spec = {"main": bool, "cases": [{"name", "stdin"?, "argv"?, "setup"?, "check"}]}
- The learner's code runs fresh for every case, in its own empty folder.
- main=True runs it as a script (__name__ == "__main__"); otherwise as a module
  named "solution", so demo code under `if __name__ == "__main__":` is skipped.
- `check` is Python run afterwards with the learner's names in scope, plus:
    out           everything the program printed (input() prompts included, typed text not echoed)
    ns            the learner's namespace as a dict
    capture(f, *a, stdin="", **kw) -> (return_value, printed_text)
    rerun(stdin="", argv=None, source=None) -> printed text of a fresh run (of `source` if given)
    code          the learner's source text
- `static`: true checks the source text only (no run).
- `setup` runs first in the case folder; it may append callables to `undo`, which run after the case.
- Several files go in one box, each after a marker line such as  # --- greetings.py ---
  Every section is written to disk; the last .py section is the program that runs.
  A failing `assert cond, "message"` shows the message to the learner.
"""
import builtins
import importlib
import io
import json
import os
import re
import sys
import tempfile
import traceback
import types

_MAX_OUT = 20000
_ECHO = [False]  # Run button: echo typed answers so the console reads like a terminal


class _Out(io.StringIO):
    def write(self, s):
        if self.tell() > _MAX_OUT:
            raise RuntimeError("The program printed too much output (possible infinite loop)")
        return super().write(s)


def _with_io(stdin, fn):
    out = _Out()
    saved = sys.stdout, sys.stderr, sys.stdin, builtins.input
    sys.stdin = io.StringIO(stdin or "")

    def _input(prompt=""):
        out.write(str(prompt))
        line = sys.stdin.readline()
        if line == "":
            raise EOFError("The program asked for more input than this test provides")
        if _ECHO[0]:
            out.write(line if line.endswith("\n") else line + "\n")
        return line.rstrip("\n")

    sys.stdout = sys.stderr = out
    builtins.input = _input
    try:
        result = fn()
    except BaseException as e:
        e.printed = out.getvalue()  # keep what was printed before the error
        raise
    finally:
        sys.stdout, sys.stderr, sys.stdin, builtins.input = saved
    return result, out.getvalue()


_FILE_MARK = re.compile(r"^#\s*-{2,}\s*([\w./-]+\.(?:py|ini|cfg|txt|json|csv|toml|c|h|md))\s*-{2,}\s*$", re.M)


def _split_files(code):
    """Split '# --- name.py ---' sections into files; the last section is the program."""
    marks = list(_FILE_MARK.finditer(code))
    if not marks:
        return {}, code, "solution.py"
    files = {}
    for i, mk in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(code)
        files[mk.group(1)] = code[mk.end():end].lstrip("\n")
    py = [n for n in files if n.endswith(".py")]
    if not py:
        return files, "", "solution.py"
    main_name = py[-1]
    return {n: b for n, b in files.items() if n != main_name}, files[main_name], main_name


def _write_files(files):
    for name, body in files.items():
        d = os.path.dirname(name)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(name, "w", encoding="utf-8") as fh:
            fh.write(body)
        if not name.endswith(".py"):
            continue
        mod = name[:-3].replace("/", ".")
        if mod.endswith(".__init__"):
            mod = mod[: -len(".__init__")]
        for key in list(sys.modules):
            if key == mod or key.startswith(mod + ".") or key == mod.split(".")[0]:
                sys.modules.pop(key, None)


def _exec_program(code, stdin, argv, main):
    files, main_code, main_name = _split_files(code)
    _write_files(files)
    module = types.ModuleType("__main__" if main else "solution")
    ns = module.__dict__
    ns.update({"__builtins__": builtins, "__file__": os.path.join(os.getcwd(), main_name)})
    saved_argv, saved_path = sys.argv, list(sys.path)
    saved_main = sys.modules.get("__main__")
    sys.argv = [main_name] + list(argv or [])
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())
    importlib.invalidate_caches()
    if main:
        sys.modules["__main__"] = module  # so doctest.testmod() and unittest.main() find the code
    try:
        _, printed = _with_io(stdin, lambda: exec(compile(main_code, main_name, "exec"), ns))
    except SystemExit as e:  # sys.exit() or unittest.main(): keep what ran and what was printed
        printed = getattr(e, "printed", "")
    finally:
        sys.argv = saved_argv
        sys.path[:] = saved_path
        if saved_main is not None:
            sys.modules["__main__"] = saved_main
    return ns, printed


def _tidy(work):
    """Forget modules loaded from the case folder, and logging set up by the program."""
    for key, mod in list(sys.modules.items()):
        f = getattr(mod, "__file__", None) or ""
        if (work and f.startswith(work)) or getattr(mod, "__fake__", False):
            sys.modules.pop(key, None)
    if "logging" in sys.modules:
        import logging
        root = logging.getLogger()
        for h in list(root.handlers):
            root.removeHandler(h)
            try:
                h.close()
            except Exception:  # noqa: BLE001
                pass
        root.setLevel(logging.WARNING)
        for lg in list(logging.Logger.manager.loggerDict.values()):
            if isinstance(lg, logging.Logger):
                lg.handlers[:] = []
                lg.setLevel(logging.NOTSET)


def _short_tb(exc):
    lines = traceback.format_exception(type(exc), exc, exc.__traceback__)
    keep = [l for l in lines if 'File "<' not in l and "grader.py" not in l and "importlib" not in l]
    return "".join(keep[-4:]).strip()


# ---------- failure details: what the learner's code gave versus what the test wanted ----------
import ast as _ast
import operator as _op

_OPS = {_ast.Eq: ("==", _op.eq), _ast.NotEq: ("!=", _op.ne), _ast.Lt: ("<", _op.lt), _ast.LtE: ("<=", _op.le),
        _ast.Gt: (">", _op.gt), _ast.GtE: (">=", _op.ge), _ast.In: ("in", lambda a, b: a in b),
        _ast.NotIn: ("not in", lambda a, b: a not in b), _ast.Is: ("is", _op.is_), _ast.IsNot: ("is not", _op.is_not)}
_HELPERS = {"capture", "rerun"}


class _Probe:
    """Records learner calls and comparisons while an assert is evaluated (each value computed once)."""

    def __init__(self):
        self.trace = []

    def reset(self):
        self.trace = []

    def rec(self, src, value):
        self.trace.append(("call", src, value))
        return value

    def cmp(self, src, left, opname, right, side):
        fn = {v[0]: v[1] for v in _OPS.values()}[opname]
        result = fn(left, right)
        self.trace.append(("cmp", src, left, opname, right, side, bool(result)))
        return result


def _mentions(node, names):
    return any(isinstance(n, _ast.Name) and n.id in names for n in _ast.walk(node))


def _root_name(func):
    while isinstance(func, _ast.Attribute):
        func = func.value
    return func.id if isinstance(func, _ast.Name) else None


class _Instrument(_ast.NodeTransformer):
    def __init__(self, learner):
        self.learner = learner | {"out"}
        self.callers = (learner | _HELPERS)

    def _src(self, node):
        try:
            s = _ast.unparse(node)
        except Exception:  # noqa: BLE001
            return "?"
        return s if len(s) <= 90 else s[:87] + "..."

    def visit_Assert(self, node):
        node.test = _InstrumentExpr(self).visit(node.test)
        reset = _ast.Expr(_ast.Call(_ast.Attribute(_ast.Name("__dx", _ast.Load()), "reset", _ast.Load()), [], []))
        return [reset, node]


class _InstrumentExpr(_ast.NodeTransformer):
    def __init__(self, outer):
        self.o = outer

    def visit_Lambda(self, node):  # leave function bodies alone
        return node

    def visit_Call(self, node):
        self.generic_visit(node)
        root = _root_name(node.func)
        if root in self.o.callers:
            return _ast.Call(_ast.Attribute(_ast.Name("__dx", _ast.Load()), "rec", _ast.Load()),
                             [_ast.Constant(self.o._src(node)), node], [])
        return node

    def visit_Compare(self, node):
        src = self.o._src(node)
        if len(node.ops) != 1 or type(node.ops[0]) not in _OPS:
            self.generic_visit(node)
            return node
        left_l = _mentions(node.left, self.o.learner)
        right_l = _mentions(node.comparators[0], self.o.learner)
        side = "L" if left_l and not right_l else "R" if right_l and not left_l else ""
        self.generic_visit(node)
        return _ast.Call(_ast.Attribute(_ast.Name("__dx", _ast.Load()), "cmp", _ast.Load()),
                         [_ast.Constant(src), node.left, _ast.Constant(_OPS[type(node.ops[0])][0]),
                          node.comparators[0], _ast.Constant(side)], [])


def _instrument(check, learner):
    try:
        tree = _Instrument(set(learner)).visit(_ast.parse(check))
        _ast.fix_missing_locations(tree)
        return compile(tree, "<check>", "exec")
    except Exception:  # noqa: BLE001 - fall back to the plain check
        return None


def _short(v, n=160):
    try:
        s = repr(v)
    except Exception:  # noqa: BLE001
        s = "<" + type(v).__name__ + ">"
    return s if len(s) <= n else s[: n - 3] + "..."


def _detail(trace, case, printed):
    lines = []
    if case.get("stdin"):
        lines.append("Input typed:    " + " | ".join(case["stdin"].rstrip("\n").split("\n")))
    if case.get("argv") is not None and case.get("argv") != []:
        lines.append("Arguments:      " + " ".join(case["argv"]))
    seen = {}
    for t in trace:
        if t[0] == "call":
            seen[t[1]] = t[2]
    shown_out = False
    for src, val in list(seen.items())[-3:]:
        if src.startswith("rerun("):
            lines.append("Program printed: " + _short(val, 300))
            shown_out = True
        elif src.startswith("capture(") and isinstance(val, tuple) and len(val) == 2:
            lines.append(f"{src[8:-1].split(',')[0]}(...) returned {_short(val[0])} and printed {_short(val[1], 200)}")
        else:
            lines.append(f"{src} gave {_short(val)}")
    fails = [t for t in trace if t[0] == "cmp" and not t[6]]
    if fails:
        _, src, left, op, right, side, _r = fails[-1]
        uses_out = "out" in src.split("(")[0] or src.endswith(" out") or " out " in src or src.startswith("out")
        if op in ("==", "!=") and side:
            got, exp = (left, right) if side == "L" else (right, left)
            lines.append(("Expected:       " if op == "==" else "Should differ from: ") + _short(exp))
            lines.append("Got:            " + _short(got))
        elif op in ("in", "not in") and isinstance(right, str):
            what = "the output" if uses_out else _short(right, 120)
            lines.append(("Looked for " if op == "in" else "Did not expect ") + _short(left, 120) + " in " + what)
        elif op in ("in", "not in") and side == "L":
            lines.append("Got " + _short(left) + (", which is not one of " if op == "in" else ", which should not be in ") + _short(right, 120))
        elif op in ("<", "<=", ">", ">="):
            lines.append(f"Check failed:   {src}   (left side was {_short(left)}, right side {_short(right)})")
        if uses_out and not shown_out:
            lines.append("Your output:    " + (_short(printed, 300) if printed else "(nothing was printed)"))
            shown_out = True
    if not shown_out and not seen:
        lines.append("Your output:    " + (_short(printed, 300) if printed else "(nothing was printed)"))
    return lines[:8]


def _run_case(code, case, main):
    start = os.getcwd()
    work = tempfile.mkdtemp(prefix="case_")
    os.chdir(work)
    printed = ""
    undo = []
    try:
        if case.get("setup"):
            exec(case["setup"], {"__builtins__": builtins, "undo": undo})
        try:
            if case.get("static"):  # reads the code without running it
                ns, printed = {}, ""
            else:
                ns, printed = _exec_program(code, case.get("stdin", ""), case.get("argv"), main)
        except BaseException as e:  # noqa: BLE001 - report learner errors
            return {"ok": False, "msg": "Your program raised an error:\n" + _short_tb(e), "out": getattr(e, "printed", "")}

        def capture(f, *a, stdin="", **kw):
            return _with_io(stdin, lambda: f(*a, **kw))

        def rerun(stdin="", argv=None, source=None):
            return _exec_program(code if source is None else source, stdin, argv, main)[1]

        scope = dict(ns)
        probe = _Probe()
        scope.update({"out": printed, "ns": ns, "code": code, "capture": capture, "rerun": rerun, "__builtins__": builtins, "__dx": probe})
        sys.path.insert(0, work)
        importlib.invalidate_caches()
        learner = {k for k in ns if not k.startswith("__")}
        compiled = _instrument(case["check"], learner)
        try:
            exec(compiled if compiled is not None else case["check"], scope)
        except AssertionError as e:
            try:
                detail = _detail(probe.trace, case, printed)
            except Exception:  # noqa: BLE001
                detail = []
            return {"ok": False, "msg": str(e) or "The result was not what this test expects.", "out": printed, "detail": detail}
        except NameError as e:
            return {"ok": False, "msg": f"Something this test needs is missing: {e}", "out": printed}
        except BaseException as e:  # noqa: BLE001
            return {"ok": False, "msg": "Calling your code raised an error:\n" + _short_tb(e), "out": printed}
        return {"ok": True, "msg": "", "out": printed}
    finally:
        for fn in reversed(undo):
            try:
                fn()
            except Exception:  # noqa: BLE001
                pass
        while work in sys.path:
            sys.path.remove(work)
        _tidy(work)
        os.chdir(start)


def grade(code, spec_json):
    spec = json.loads(spec_json) if isinstance(spec_json, str) else spec_json
    results = []
    for case in spec.get("cases", []):
        r = _run_case(code, case, bool(spec.get("main")))
        r["name"] = case.get("name", "")
        r["out"] = r["out"][-1500:]
        results.append(r)
    return json.dumps(results)


def run(code, stdin=""):
    """Plain run for the Run button: returns printed output and any error."""
    start = os.getcwd()
    os.makedirs("/tmp/playground", exist_ok=True)
    os.chdir("/tmp/playground")
    _ECHO[0] = True
    try:
        try:
            _, printed = _exec_program(code, stdin, [], True)
            return json.dumps({"out": printed, "err": ""})
        except BaseException as e:  # noqa: BLE001
            err = _short_tb(e)
            err += _page_limit_note(e)
            return json.dumps({"out": getattr(e, "printed", ""), "err": err})
    finally:
        _ECHO[0] = False
        _tidy("/tmp/playground")
        os.chdir(start)


_DESKTOP_ONLY = {"tkinter", "flask", "requests", "markupsafe", "turtle", "pygame", "numpy", "pandas"}


def _page_limit_note(e):
    """A plain-words note when a program hits a limit of the in-page Python (not a bug in the program)."""
    own = "Run it in your own Python on your computer to try it out; Submit answer still grades it here."
    text = str(e)
    if isinstance(e, ImportError):
        top = (getattr(e, "name", "") or "").split(".")[0]
        if top in _DESKTOP_ONLY:
            return "\n\nThis program needs " + top + ", which the in-page Python does not have. " + own
        if top and isinstance(e, ModuleNotFoundError) and not os.path.exists(top + ".py") and not os.path.isdir(top):
            return ("\n\nIf " + top + " is a library you install with pip, the in-page Python does not have it "
                    "(it has the standard library only). " + own + " If it is a module of your own, check its name.")
        return ""
    if isinstance(e, RuntimeError) and "start new thread" in text:
        return "\n\nThe in-page Python has a single thread, so it cannot start threads. " + own
    if "stack switching" in text or "run_until_complete" in text:
        return ("\n\nasyncio.run() needs a browser feature this browser does not offer to the page. " + own)
    if (isinstance(e, (OSError, NotImplementedError))
            and ("does not support processes" in text or "multiprocessing" in text)):
        return "\n\nThe in-page Python cannot start other programs or processes. " + own
    return ""


# ---------- style notes (not graded): a small, offline checker in the spirit of CS50's style50 ----------
_BUILTIN_NAMES = {"list", "dict", "str", "int", "float", "set", "tuple", "sum", "max", "min", "len", "input",
                  "print", "range", "open", "map", "filter", "sorted", "any", "all", "iter", "zip", "round",
                  "abs", "bool"}
_SNAKE = re.compile(r"^_{0,2}[a-z][a-z0-9_]*$")
_CAPS = re.compile(r"^_{0,2}[A-Z][A-Z0-9_]*$")
_CAPWORDS = re.compile(r"^_{0,2}[A-Z][a-zA-Z0-9]*$")


def _style_notes(code):
    """Style notes for one program; multi-file answers are checked file by file."""
    marks = list(_FILE_MARK.finditer(code))
    if not marks:
        return _style_file(code, "main.py")
    out = []
    for i, mk in enumerate(marks):
        name = mk.group(1)
        if not name.endswith(".py"):
            continue
        start_line = code[: mk.end()].count("\n") + 1
        end = marks[i + 1].start() if i + 1 < len(marks) else len(code)
        for x in _style_file(code[mk.end():end].lstrip("\n").rstrip(), name):
            out.append({"line": x["line"] + start_line, "msg": (name + ": " if len(marks) > 1 else "") + x["msg"]})
    return out[:8]


def _style_file(code, filename):
    notes = []

    def add(line, msg):
        notes.append({"line": line, "msg": msg})

    try:
        tree = _ast.parse(code)
    except SyntaxError:
        return []
    # line-based checks
    long_lines = []
    for n, text in enumerate(code.split("\n"), 1):
        if len(text) > 120 and not _in_bracket_line(code, n, strings_only=True):
            long_lines.append(n)
        if text.rstrip() != text and text.strip():
            add(n, "Trailing spaces at the end of the line.")
        indent = len(text) - len(text.lstrip(" \t"))
        if "\t" in text[:indent]:
            add(n, "Indent with spaces, not tabs (PEP 8 uses 4 spaces).")
        elif text.strip() and indent % 4 and not text.lstrip().startswith(("#", ")", "]", "}")) and not _in_bracket_line(code, n):
            add(n, "Indentation is not a multiple of 4 spaces.")
    for n in long_lines[:2]:
        add(n, "Line is longer than 120 characters; split it so it is easy to read (PEP 8 suggests 79, many teams allow 88 to 120).")

    framework = set()  # functions and names inside classes with base classes often follow the base's API
    for node in _ast.walk(tree):
        if isinstance(node, _ast.ClassDef) and node.bases:
            for sub in node.body:
                framework.add(id(sub))
                if isinstance(sub, (_ast.Assign, _ast.AnnAssign)):
                    for nm in _ast.walk(sub):
                        framework.add(id(nm))
    class_body = set()
    for node in _ast.walk(tree):
        if isinstance(node, _ast.ClassDef):
            for sub in node.body:
                if isinstance(sub, (_ast.Assign, _ast.AnnAssign)):
                    class_body.add(id(sub))
    imported, used = {}, set()
    for node in _ast.walk(tree):
        if isinstance(node, _ast.Name) and isinstance(node.ctx, _ast.Load):
            used.add(node.id)
        elif isinstance(node, _ast.Attribute):
            root = node
            while isinstance(root, _ast.Attribute):
                root = root.value
            if isinstance(root, _ast.Name):
                used.add(root.id)
    for node in _ast.walk(tree):
        if isinstance(node, (_ast.Import, _ast.ImportFrom)):
            for a in node.names:
                if a.name == "*":
                    add(node.lineno, "Avoid 'from ... import *': it hides where names come from.")
                    continue
                name = (a.asname or a.name).split(".")[0]
                if not (isinstance(node, _ast.ImportFrom) and node.module == "__future__"):
                    imported.setdefault(name, node.lineno)
        elif isinstance(node, _ast.Compare):
            for op, right in zip(node.ops, node.comparators):
                if isinstance(op, (_ast.Eq, _ast.NotEq)) and isinstance(right, _ast.Constant) and right.value is None:
                    add(node.lineno, "Compare with None using 'is None' / 'is not None', not == or !=.")
                elif isinstance(op, (_ast.Eq, _ast.NotEq)) and isinstance(right, _ast.Constant) and isinstance(right.value, bool):
                    add(node.lineno, "No need to compare with True/False: use 'if x:' or 'if not x:'.")
            if (isinstance(node.left, _ast.Call) and isinstance(node.left.func, _ast.Name) and node.left.func.id == "type"
                    and isinstance(node.ops[0], (_ast.Eq, _ast.Is))):
                add(node.lineno, "Use isinstance(x, T) rather than comparing type(x).")
        elif isinstance(node, _ast.ExceptHandler) and node.type is None:
            add(node.lineno, "A bare 'except:' also catches typos and Ctrl+C; name the exception you expect.")
        elif isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef)):
            if id(node) not in framework and not _SNAKE.match(node.name) and not node.name.startswith("test") and not (node.name.startswith("__") and node.name.endswith("__")) and not node.name.startswith(("visit_", "do_", "setUp", "tearDown")):
                add(node.lineno, f"Function names use snake_case: '{node.name}' could be '{_to_snake(node.name)}'.")
            for d in node.args.defaults + node.args.kw_defaults:
                if isinstance(d, (_ast.List, _ast.Dict, _ast.Set)):
                    add(node.lineno, f"'{node.name}' has a mutable default argument; use None and create the list or dict inside.")
            for a in node.args.args + node.args.kwonlyargs:
                if a.arg in _BUILTIN_NAMES:
                    add(node.lineno, f"Parameter '{a.arg}' hides the built-in {a.arg}(); pick another name.")
            notes.extend(_unused_locals(node))
            body_lines = (getattr(node, "end_lineno", node.lineno) or node.lineno) - node.lineno
            if body_lines > 50:
                add(node.lineno, f"'{node.name}' is {body_lines} lines long; consider splitting it into smaller functions.")
        elif isinstance(node, _ast.ClassDef):
            if not _CAPWORDS.match(node.name):
                add(node.lineno, f"Class names use CapWords: '{node.name}'.")
        elif isinstance(node, (_ast.Assign, _ast.AnnAssign, _ast.AugAssign)) and id(node) not in framework:
            in_class = id(node) in class_body
            targets = node.targets if isinstance(node, _ast.Assign) else [node.target]
            for t in targets:
                for nm in _ast.walk(t):
                    if isinstance(nm, _ast.Name) and isinstance(nm.ctx, _ast.Store):
                        if nm.id in _BUILTIN_NAMES and not in_class:
                            add(node.lineno, f"Variable '{nm.id}' hides the built-in {nm.id}(); pick another name.")
                        elif nm.id in ("l", "O", "I"):
                            add(node.lineno, f"Avoid '{nm.id}' as a name: it looks like 1 or 0 in many fonts.")
                        elif not (_SNAKE.match(nm.id) or _CAPS.match(nm.id) or nm.id == "_" or _CAPWORDS.match(nm.id)):
                            add(node.lineno, f"Variable names use snake_case: '{nm.id}' could be '{_to_snake(nm.id)}'.")
        elif isinstance(node, _ast.For):
            it = node.iter
            if (isinstance(it, _ast.Call) and isinstance(it.func, _ast.Name) and it.func.id == "range" and len(it.args) == 1
                    and isinstance(it.args[0], _ast.Call) and isinstance(it.args[0].func, _ast.Name) and it.args[0].func.id == "len"):
                add(node.lineno, "'for i in range(len(seq))': if you need the items, loop over them directly or use enumerate().")
    all_names = set()
    for node in _ast.walk(tree):
        if isinstance(node, _ast.Assign) and any(isinstance(t, _ast.Name) and t.id == "__all__" for t in node.targets):
            all_names = {e.value for e in getattr(node.value, "elts", []) if isinstance(e, _ast.Constant)}
    for name, line in imported.items():
        if filename.endswith("__init__.py"):
            break  # imports in a package's __init__ are usually re-exports
        if name not in used and name not in all_names:
            add(line, f"'{name}' is imported but never used.")
    if ";" in code:
        import io as _io2
        import tokenize as _tok
        try:   # real ';' tokens only: text inside strings, docstrings and comments does not count
            semi = sorted({t.start[0] for t in _tok.generate_tokens(_io2.StringIO(code).readline)
                           if t.type == _tok.OP and t.string == ";"})
        except Exception:  # noqa: BLE001
            semi = [n for n, text in enumerate(code.split("\n"), 1) if _has_statement_semicolon(text)]
        for n in semi[:1]:
            add(n, "Put each statement on its own line instead of joining them with ';'.")
    seen, out = set(), []
    for x in sorted(notes, key=lambda x: x["line"]):
        key = (x["line"], x["msg"])
        if key not in seen:
            seen.add(key)
            out.append(x)
    return out[:8]


def _to_snake(name):
    s = re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", name)
    return s.lower()


def _has_statement_semicolon(text):
    code_part = text.split("#")[0]
    depth, q = 0, None
    for ch in code_part:
        if q:
            if ch == q:
                q = None
            continue
        if ch in "'\"":
            q = ch
        elif ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif ch == ";" and depth == 0:
            return True
    return False


def _in_bracket_line(code, n, strings_only=False):
    """True when line n continues an open bracket or string (alignment indents are fine there)."""
    import tokenize
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(code).readline))
    except (tokenize.TokenError, SyntaxError, IndentationError):
        return True
    for t in toks:
        if t.start[0] < n <= t.end[0] and t.type == tokenize.STRING:
            return True
    if strings_only:
        return False
    depth = 0
    for t in toks:
        if t.start[0] >= n:
            break
        if t.type == tokenize.OP and t.string in "([{":
            depth += 1
        elif t.type == tokenize.OP and t.string in ")]}":
            depth -= 1
    return depth > 0


def _unused_locals(fn):
    assigned, loaded = {}, set()
    globals_ = set()
    for node in _ast.walk(fn):
        if isinstance(node, (_ast.Global, _ast.Nonlocal)):
            globals_.update(node.names)
    for node in _ast.walk(fn):
        if node is not fn and isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef, _ast.Lambda, _ast.ClassDef)):
            for sub in _ast.walk(node):
                if isinstance(sub, _ast.Name) and isinstance(sub.ctx, _ast.Load):
                    loaded.add(sub.id)
        if isinstance(node, _ast.Name):
            if isinstance(node.ctx, _ast.Store):
                assigned.setdefault(node.id, node.lineno)
            else:
                loaded.add(node.id)
    for node in _ast.walk(fn):
        if isinstance(node, (_ast.For, _ast.comprehension)):
            for nm in _ast.walk(node.target):
                if isinstance(nm, _ast.Name):
                    assigned.pop(nm.id, None)  # unused loop variables are a separate, softer matter
        if isinstance(node, (_ast.With, _ast.AsyncWith)):
            for item in node.items:
                if item.optional_vars is not None:
                    for nm in _ast.walk(item.optional_vars):
                        if isinstance(nm, _ast.Name):
                            assigned.pop(nm.id, None)
        if isinstance(node, _ast.Tuple) and isinstance(getattr(node, "ctx", None), _ast.Store):
            for nm in node.elts:
                if isinstance(nm, _ast.Name):
                    assigned.pop(nm.id, None)  # unpacking often names parts it does not need
    return [{"line": line, "msg": f"'{name}' is assigned in {fn.name}() but never used."}
            for name, line in assigned.items()
            if name not in loaded and name not in globals_ and not name.startswith("_")]


def style(code):
    """Style notes for the Submit panel: [{line, msg}], at most 8. Never affects grading."""
    try:
        return json.dumps(_style_notes(code))
    except Exception:  # noqa: BLE001
        return "[]"
