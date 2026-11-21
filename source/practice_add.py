"""Add the spec-style practice exercises (specs/b4_practice.py, specs/b5_practice.py) to the Foundations track.

Idempotent: re-running replaces earlier practice exercises.
Each one becomes the next exercise of its lesson (id <lesson>c, or 6.6d), is autograded,
and carries hints, a model solution and an explanation.
"""
import importlib.util
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, "specs", name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    mods = [load("b4_practice"), load("b5_practice")]
    d = json.load(open(os.path.join(HERE, "pycontent.json")))
    practice = {}
    for m in mods:
        for eid, meta in m.META.items():
            lid = meta["lesson"]
            practice.setdefault(lid, []).append([meta["title"], meta["prompt"]])
            d["lessons"][lid]["exercises"][eid] = {"hints": meta["hints"], "lang": "python",
                                                   "solution": m.SOLUTIONS[eid], "explain": meta["explain"]}
            d["grade"][eid] = m.SPECS[eid]
    json.dump(d, open(os.path.join(HERE, "pycontent.json"), "w"), ensure_ascii=False)

    page = open(os.path.join(HERE, "course.html"), encoding="utf-8").read()
    blob = json.dumps(practice, ensure_ascii=False).replace("</", "<\\/")
    line = "var PRACTICE=" + blob + ";\n"
    if "var PRACTICE=" in page:
        page = re.sub(r"var PRACTICE=.*?;\n(?=function L\()", lambda _: line, page, count=1, flags=re.S)
    else:
        page = page.replace("function L(id,t,min,learn,exs,kind){", line + "function L(id,t,min,learn,exs,kind){", 1)
    page = page.replace('ex:exs.map(function(e,i){return {id:id+"abc"[i],t:e[0],p:e[1]};})};',
                        'ex:exs.concat(PRACTICE[id]||[]).map(function(e,i){return {id:id+"abcd"[i],t:e[0],p:e[1]};})};')
    assert 'exs.concat(PRACTICE[id]||[])' in page

    i = page.find("window.PYCC_CONTENT=") + len("window.PYCC_CONTENT=")
    j = page.find(";</script>", i)
    c = json.loads(page[i:j].replace("<\\!", "<!"))
    for k in ("lessons", "grade"):
        c[k] = d[k]
    page = page[:i] + json.dumps(c).replace("</", "<\\/").replace("<!", "<\\!") + page[j:]
    open(os.path.join(HERE, "course.html"), "w", encoding="utf-8").write(page)
    print("practice added:", sum(len(v) for v in practice.values()), "exercises in", len(practice), "lessons")


if __name__ == "__main__":
    main()
