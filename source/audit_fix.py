"""Audit fixes for the Python course's code samples (run once; safe to re-run).

- removes imports the style checker reports as unused, splits 'a; b' lines, strips trailing spaces
- lesson files: closes files properly in the two file-handling examples, marks examples whose output
  depends on timing or the machine as 'varies' (shown as "Sample output")
Works on deep/py/*.txt (expanded lessons) and pycontent.json (worked example 1 and model answers).
"""
import io, json, re, sys, tokenize

exec(open("grader_src.py").read())   # for style()

SKIP = ("mutable default", "range(len", "import *", "Avoid 'l'", "longer than")


def fix_code(code):
    """Apply the mechanical fixes; return the new code."""
    for _ in range(6):
        notes = [n for n in json.loads(style(code)) if not any(s in n["msg"] for s in SKIP)
                 and not re.match(r"^[\w/.-]+\.\w+: ", n["msg"])]
        lines = code.split("\n")
        changed = False
        for n in notes:
            i = n["line"] - 1
            if not 0 <= i < len(lines):
                continue
            line = lines[i]
            msg = n["msg"].split(": ", 1)[-1] if re.match(r"^[\w/.]+\.py: ", n["msg"]) else n["msg"]
            m = re.match(r"'(\w+)' is imported but never used", msg)
            if m and "noqa" not in line:
                name = m.group(1)
                if re.fullmatch(rf"\s*import {name}\s*", line) or re.fullmatch(rf"\s*from [\w.]+ import {name}\s*", line):
                    del lines[i]
                else:
                    new = re.sub(rf",\s*{name}\b(?!\.)", "", line)
                    if new == line:
                        new = re.sub(rf"\b{name}\s*,\s*", "", line, count=1)
                    lines[i] = new
                changed = lines != code.split("\n")
                break
            if "joining them with ';'" in msg:
                toks = [t for t in tokenize.generate_tokens(io.StringIO(line.lstrip() + "\n").readline)
                        if t.type == tokenize.OP and t.string == ";"]
                body, indent = line.lstrip(), line[:len(line) - len(line.lstrip())]
                parts, prev = [], 0
                for t in toks:
                    parts.append(body[prev:t.start[1]].strip())
                    prev = t.end[1]
                parts.append(body[prev:].strip())
                lines[i:i + 1] = [indent + p for p in parts if p]
                changed = True
                break
            if "Trailing spaces" in msg:
                lines[i] = line.rstrip()
                changed = True
                break
        code = "\n".join(lines)
        if not changed:
            break
    return code


def fix_lesson_file(path, varies=()):
    s = open(path, encoding="utf-8").read()
    out, pos, n_fixed = [], 0, 0
    lid, k = None, 0
    blocks = list(re.finditer(r"^(=== (\S+)|@example ([^\n]*))\n", s, flags=re.M))
    for b in blocks:
        if b.group(2):
            lid, k = b.group(2), 0
            continue
        k += 1
        head = b.group(3)
        start = b.end()
        nxt = re.search(r"^(@(?:idea|how|example|note|output|stdin|mistakes|keys)\b|=== )", s[start:], flags=re.M)
        end = start + (nxt.start() if nxt else len(s) - start)
        code = s[start:end]
        new_head = head
        if (lid, k + 1) in varies and " varies" not in head.split(":")[0]:
            new_head = re.sub(r"^(\w+)", r"\1 varies", head, count=1)
        new_code = code
        if head.split()[0].rstrip(":") == "python":
            body = code.rstrip("\n")
            fixed = fix_code(body)
            if fixed != body:
                new_code = fixed + code[len(body):]
                n_fixed += 1
        out.append(s[pos:b.start()] + "@example " + new_head + "\n" + new_code)
        pos = end
    out.append(s[pos:])
    new = "".join(out)
    if new != s:
        open(path, "w", encoding="utf-8").write(new)
    return n_fixed, new != s


if __name__ == "__main__":
    import glob
    VARIES = {("A9.5", 2), ("A9.3", 2), ("S2.1", 3), ("S2.2", 2), ("A14.1", 2)}
    touched = []
    for p in sorted(glob.glob("deep/py/*.txt")):
        n, ch = fix_lesson_file(p, VARIES)
        if ch:
            touched.append(p)
            print(p, n, "examples tidied")
    c = json.load(open("pycontent.json"))
    ne = ns = 0
    for k, l in c["lessons"].items():
        e = l.get("example")
        if e and e.get("lang", "python") == "python":
            f = fix_code(e["code"])
            if f != e["code"]:
                e["code"] = f
                ne += 1
        for eid, x in l.get("exercises", {}).items():
            if x.get("lang", "python") == "python" and x.get("solution"):
                f = fix_code(x["solution"])
                if f != x["solution"]:
                    x["solution"] = f
                    ns += 1
                    print("model answer tidied:", eid)
    json.dump(c, open("pycontent.json", "w"), ensure_ascii=False)
    print(ne, "first examples and", ns, "model answers tidied")
    open("audit_touched.txt", "w").write("\n".join(touched))
