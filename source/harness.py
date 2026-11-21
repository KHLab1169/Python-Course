"""Check autograder specs: the official solution must pass every case, each bad answer must fail one.
usage: harness.py specs/batch1.py [specs/batch2.py ...]"""
import importlib.util, json, os, re, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
w = open(os.path.join(HERE, 'python-course/py-worker.js')).read()
G = {}
exec(compile(json.loads(re.search(r'const GRADER = (".*?");\n', w).group(1)), 'grader.py', 'exec'), G)
d = json.load(open(os.path.join(HERE, 'pycontent.json')))
def solution(eid):
    for l in d['lessons'].values():
        if eid in l.get('exercises', {}):
            return l['exercises'][eid]['solution']
ok = True
os.chdir(tempfile.mkdtemp())
for path in sys.argv[1:]:
    spec_mod = importlib.util.spec_from_file_location('m', os.path.join(HERE, path)); m = importlib.util.module_from_spec(spec_mod); spec_mod.loader.exec_module(m)
    for eid, spec in m.SPECS.items():
        sol = m.SOLUTIONS.get(eid) or solution(eid)
        res = json.loads(G['grade'](sol, json.dumps(spec)))
        bad_sol = [r for r in res if not r['ok']]
        line = f"{eid}: solution {len(res)-len(bad_sol)}/{len(res)}"
        if bad_sol:
            ok = False
            line += '  FAIL ' + ' | '.join(f"{r['name']}: {r['msg'][:200]}" for r in bad_sol)
        for i, bad in enumerate(m.BAD.get(eid, [])):
            r2 = json.loads(G['grade'](bad, json.dumps(spec)))
            if all(r['ok'] for r in r2):
                ok = False
                line += f"  BAD#{i} PASSED (should fail)"
            else:
                line += f"  bad#{i} ok"
        if not m.BAD.get(eid):
            line += '  (no bad answers!)'
        print(line)
print('ALL GOOD' if ok else 'PROBLEMS')
