#!/usr/bin/env python3
"""Build expanded lessons from deep/py/*.txt into deep.json, running every example for its real output.

Authoring format (one file per module, any number of lessons):

    === 1.2
    @idea
    Paragraphs in plain text. `code` and **bold** are allowed. Blank line = new paragraph.
    @how
    - one rule or step per bullet
    @example pycon: Title
    >>> 17 / 5            (only the input lines: results are filled in by running them)
    @note
    What to notice.
    @example python: Title
    print("a program")    (output is filled in by running it; @stdin gives typed input)
    @stdin
    Ada
    @note
    ...
    @example python norun: Title      (cannot run here: needs a package, a window or a network)
    @output
    sample output written by hand (shown as "Sample output")
    @mistakes
    - **The trap.** What goes wrong and the fix.
    @keys
    - one key point per bullet
"""
import ast, builtins, contextlib, glob, importlib, io, json, os, re, signal, sys, tempfile, traceback, warnings

HERE = os.path.dirname(os.path.abspath(__file__))


class Timeout(BaseException):
    pass


def _alarm(*a):
    raise Timeout()


signal.signal(signal.SIGALRM, _alarm)


def short_exc(e):
    name = type(e).__name__
    msg = str(e)
    return "Traceback (most recent call last):\n  ...\n" + (f"{name}: {msg}" if msg else name)


def run_pycon(code):
    stmts, cur = [], None
    for line in code.split("\n"):
        if line.startswith(">>> "):
            if cur is not None:
                stmts.append(cur)
            cur = line[4:]
        elif line.rstrip() == "...":
            continue                      # the closing empty line is added when the block is shown
        elif line.startswith("... "):
            cur += "\n" + line[4:]
        elif line.strip() == "":
            continue
        else:
            raise ValueError(f"pycon examples hold only >>> and ... lines, got: {line!r}")
    if cur is not None:
        stmts.append(cur)
    ns = {"__name__": "__main__"}
    out = []
    tmp = tempfile.mkdtemp()
    old = os.getcwd()
    os.chdir(tmp)
    try:
        for st in stmts:
            src_lines = st.split("\n")
            out.append(">>> " + src_lines[0])
            out += ["... " + l for l in src_lines[1:]]
            if len(src_lines) > 1 and src_lines[0].rstrip().endswith(":"):
                out.append("...")          # a block (for, def, if ...) ends with an empty line
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    signal.alarm(5)
                    exec(compile(st + "\n", "<stdin>", "single"), ns)
                    signal.alarm(0)
                text = buf.getvalue().rstrip("\n")
            except Timeout:
                raise
            except BaseException as e:  # noqa: BLE001
                signal.alarm(0)
                text = (buf.getvalue() + short_exc(e)).rstrip("\n")
            if text:
                out.append(text)
    finally:
        signal.alarm(0)
        os.chdir(old)
    return "\n".join(out)


def run_python(code, stdin):
    feed = io.StringIO(stdin)
    buf = io.StringIO()
    real_input = builtins.input

    def fake_input(prompt=""):
        buf.write(str(prompt))
        line = feed.readline()
        if not line:
            raise EOFError("EOF when reading a line")
        buf.write(line if line.endswith("\n") else line + "\n")
        return line.rstrip("\n")

    tmp = tempfile.mkdtemp()
    old = os.getcwd()
    os.chdir(tmp)
    builtins.input = fake_input
    saved_argv = sys.argv
    saved_path = list(sys.path)
    sys.argv = ["example.py"]
    mods = set(sys.modules)
    sys.path_importer_cache.clear()          # each example has its own folder
    importlib.invalidate_caches()
    saved_show = warnings.showwarning
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf), warnings.catch_warnings():
            signal.alarm(8)
            try:
                exec(compile(code, "example.py", "exec"), {"__name__": "__main__", "__file__": os.path.join(tmp, "example.py")})
            except SystemExit:
                pass
            finally:
                signal.alarm(0)
    except Timeout:
        raise
    except BaseException as e:  # noqa: BLE001
        buf.write(("\n" if buf.getvalue() and not buf.getvalue().endswith("\n") else "") + short_exc(e))
    finally:
        builtins.input = real_input
        warnings.showwarning = saved_show
        sys.argv = saved_argv
        sys.path[:] = saved_path
        os.chdir(old)
        for m in set(sys.modules) - mods:          # forget modules the example created in its folder
            f = getattr(sys.modules.get(m), "__file__", "") or ""
            if f.startswith(tmp):
                sys.modules.pop(m, None)
        import logging
        logging.getLogger().handlers.clear()
    return buf.getvalue().rstrip("\n")


def parse_file(path):
    lessons = {}
    text = open(path, encoding="utf-8").read()
    for block in re.split(r"^=== ", text, flags=re.M)[1:]:
        head, _, body = block.partition("\n")
        lid = head.strip()
        secs = re.split(r"^@(\w+)(?:[ \t]+(.*))?$", body, flags=re.M)
        les = {"idea": [], "how": [], "examples": [], "mistakes": [], "keys": []}
        k = 1
        while k < len(secs):
            name, arg, content = secs[k], (secs[k + 1] or "").strip(), secs[k + 2]
            k += 3
            content = content.strip("\n")
            if name == "idea":
                les["idea"] = [re.sub(r"\s*\n\s*", " ", p.strip()) for p in re.split(r"\n\s*\n", content) if p.strip()]
            elif name in ("how", "mistakes", "keys"):
                les[name] = [re.sub(r"\s*\n\s*", " ", b.strip()) for b in re.split(r"^- ", content, flags=re.M) if b.strip()]
            elif name == "example":
                m = re.match(r"(\w+)((?:\s+\w+)*)\s*:\s*(.*)$", arg)
                if not m:
                    raise ValueError(f"{lid}: bad @example header {arg!r}")
                flags = m.group(2).split()
                les["examples"].append({"lang": m.group(1), "title": m.group(3).strip(), "code": content.rstrip(),
                                        "norun": "norun" in flags, "stdin": "", "note": "", "output": ""})
            elif name == "stdin":
                les["examples"][-1]["stdin"] = content + "\n"
            elif name == "output":
                les["examples"][-1]["output"] = content.rstrip()
                les["examples"][-1]["sample"] = True
            elif name == "note":
                les["examples"][-1]["note"] = re.sub(r"\s*\n\s*", " ", content.strip())
            else:
                raise ValueError(f"{lid}: unknown section @{name}")
        lessons[lid] = les
    return lessons


def build(paths, out_path, known_ids=None):
    allles, problems = {}, []
    for p in paths:
        for lid, les in parse_file(p).items():
            if known_ids is not None and lid not in known_ids:
                problems.append(f"{lid}: no such lesson")
            for n, ex in enumerate(les["examples"], 2):
                where = f"{lid} example {n}"
                try:
                    if ex["lang"] == "pycon":
                        ex["code"] = run_pycon(ex["code"])
                        if "Traceback" in ex["code"] and "error" not in (ex["note"] + ex["title"]).lower():
                            problems.append(f"{where}: raised an error but the note does not mention it")
                    elif ex["lang"] == "python" and not ex["norun"]:
                        ex["output"] = run_python(ex["code"], ex["stdin"])
                        if "Traceback" in ex["output"] and "error" not in (ex["note"] + ex["title"]).lower():
                            problems.append(f"{where}: raised an error: {ex['output'].splitlines()[-1]}")
                    elif ex["lang"] == "python":
                        ast.parse(re.sub(r"^#\s*-{2,}.*$", "", ex["code"], flags=re.M))
                except SyntaxError as e:
                    problems.append(f"{where}: syntax error line {e.lineno}: {e.msg}")
                except Timeout:
                    problems.append(f"{where}: took too long (waiting for input or an endless loop?)")
                except Exception as e:  # noqa: BLE001
                    problems.append(f"{where}: {e}")
                for key in ("norun", "stdin"):
                    ex.pop(key, None)
            words = sum(len(x.split()) for part in ("idea", "how", "mistakes", "keys") for x in les[part])
            if not les["idea"] or not les["keys"] or len(les["examples"]) < 2:
                problems.append(f"{lid}: needs @idea, @keys and two examples")
            les["_words"] = words
            allles[lid] = les
    with open(out_path, "w") as fh:
        json.dump(allles, fh, ensure_ascii=False)
    return allles, problems


if __name__ == "__main__":
    d = json.load(open(os.path.join(HERE, "pycontent.json")))
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(HERE, "deep", "py", "*.txt")))
    les, problems = build(files, os.path.join(HERE, "deep.json"), set(d["lessons"]))
    words = [v["_words"] for v in les.values()]
    print(f"{len(les)} lessons built, {sum(words)} words of explanation (avg {sum(words) // max(1, len(words))}),"
          f" {sum(len(v['examples']) for v in les.values())} new examples")
    for p in problems:
        print("PROBLEM", p)
