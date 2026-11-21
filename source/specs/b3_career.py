"""Autograder specs for module A13, Career toolkit (Python Course, Track 2)."""
SOLUTIONS = {}
SPECS = {}
BAD = {}

# ------------------------------------------------------------------ A13.1a  commit message checker
SOLUTIONS["A13.1a"] = '''import re

TYPES = {"feat", "fix", "docs", "test", "refactor", "perf", "build", "ci", "chore", "style", "revert"}
HEADER = re.compile(r"^(?P<type>[a-z]+)(?:\\((?P<scope>[a-z0-9-]+)\\))?(?P<bang>!)?: (?P<summary>\\S.*)$")


def check_commit(message):
    """Return the problems with a commit message, as codes in a fixed order ([] when it is fine)."""
    if not message.strip():
        return ["empty"]
    lines = message.split("\\n")
    header = lines[0]
    match = HEADER.match(header)
    if not match:
        return ["format"]
    problems = []
    if match["type"] not in TYPES:
        problems.append("type")
    if len(header) > 72:
        problems.append("length")
    summary = match["summary"]
    if summary.endswith("."):
        problems.append("period")
    if summary[0].isupper():
        problems.append("case")
    if len(lines) > 1 and lines[1].strip():
        problems.append("blank-line")
    return problems


if __name__ == "__main__":
    for msg in ["feat(api): add shift endpoint", "Fix: Correct rounding.", "fix: Correct rounding.", "wip"]:
        print(repr(msg), check_commit(msg))
'''
_C = "from solution import check_commit\n" if False else ""
SPECS["A13.1a"] = {
    "main": False,
    "starter": "import re\n\n\ndef check_commit(message):\n    \"\"\"Return the problems with a commit message, as codes in a fixed order ([] when it is fine).\"\"\"\n    return []\n",
    "cases": [
        {"name": "A good header has no problems", "check": "assert check_commit('feat(api): add shift endpoint') == [], 'feat(api): add shift endpoint follows every rule'\nassert check_commit('fix: handle empty input') == [], 'The scope is optional: fix: handle empty input is fine'\nassert check_commit('feat!: drop Python 3.9 support') == [], 'A ! before the colon marks a breaking change and is allowed'"},
        {"name": "Empty and malformed messages", "check": "assert check_commit('') == ['empty'], 'An empty message gives [\"empty\"]'\nassert check_commit('   \\n') == ['empty'], 'A message of only whitespace counts as empty'\nassert check_commit('wip') == ['format'], 'A header without type: summary gives [\"format\"]'\nassert check_commit('fix:no space') == ['format'], 'There must be exactly one space after the colon'\nassert check_commit('Fix: something') == ['format'], 'Types are lower case, so Fix: is a format problem'"},
        {"name": "Unknown type", "check": "assert check_commit('feature: add login') == ['type'], 'feature is not one of the allowed types (feat is)'"},
        {"name": "Summary rules: period and capital letter", "check": "assert check_commit('fix: correct rounding.') == ['period'], 'The summary must not end with a period'\nassert check_commit('fix: Correct rounding') == ['case'], 'The summary starts with a lower-case letter'\nassert check_commit('fix: Correct rounding.') == ['period', 'case'], 'Report period before case'"},
        {"name": "Header longer than 72 characters", "check": "h = 'docs: ' + 'x' * 67\nassert len(h) == 73\nassert check_commit(h) == ['length'], 'A 73-character header is too long'\nassert check_commit(h[:-1]) == [], 'Exactly 72 characters is still fine'"},
        {"name": "Blank line before the body", "check": "assert check_commit('fix: handle empty input\\n\\nThe parser crashed on an empty file.') == [], 'Header, blank line, body is the right shape'\nassert check_commit('fix: handle empty input\\nThe parser crashed.') == ['blank-line'], 'The second line must be blank when there is a body'"},
        {"name": "Several problems in the documented order", "check": "assert check_commit('feature: Add logins everywhere so that every user of the system can sign in.\\nbody') == ['type', 'length', 'period', 'case', 'blank-line'], 'Order: type, length, period, case, blank-line'"},
    ],
}
BAD["A13.1a"] = [
    SOLUTIONS["A13.1a"].replace('(?:\\((?P<scope>[a-z0-9-]+)\\))?', '\\((?P<scope>[a-z0-9-]+)\\)'),   # scope required
    SOLUTIONS["A13.1a"].replace('    if len(lines) > 1 and lines[1].strip():\n        problems.append("blank-line")\n', ''),  # no body check
    SOLUTIONS["A13.1a"].replace('len(header) > 72', 'len(header) >= 72'),                                    # off by one
    SOLUTIONS["A13.1a"].replace('''    if summary.endswith("."):
        problems.append("period")
    if summary[0].isupper():
        problems.append("case")''', '''    if summary[0].isupper():
        problems.append("case")
    if summary.endswith("."):
        problems.append("period")'''),                                                                       # wrong order
]

# ------------------------------------------------------------------ A13.2a  README checker
SOLUTIONS["A13.2a"] = '''SECTIONS = [("install", ("install",)), ("usage", ("usage", "example", "quick start")), ("tests", ("test",))]


def readme_report(text):
    """Check a README for the parts a reviewer looks for first."""
    lines = text.split("\\n")
    in_code = False
    headings = []
    code_fences = 0
    first = None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            code_fences += 1
            in_code = not in_code
            continue
        if in_code:
            continue
        if first is None and stripped:
            first = stripped
        if stripped.startswith(("## ", "### ")):
            headings.append(stripped.lstrip("#").strip().lower())
    missing = [name for name, words in SECTIONS
               if not any(word in heading for heading in headings for word in words)]
    title = first is not None and first.startswith("# ")
    todos = sum("TODO" in line for line in lines)
    blocks = code_fences // 2
    score = 100 - 20 * len(missing) - (0 if title else 20) - (10 if blocks == 0 else 0) - 5 * todos
    return {"title": title, "missing": missing, "code_blocks": blocks, "todos": todos, "score": max(0, score)}


if __name__ == "__main__":
    print(readme_report("# shiftboard\\n\\n## Install\\n\\n```\\npip install .\\n```\\n\\n## Usage\\n\\n## Running the tests\\n"))
'''
GOOD_README = "# shiftboard\\n\\nPlan shifts.\\n\\n## Install\\n\\n```bash\\npip install shiftboard\\n```\\n\\n## Usage\\n\\nRun it.\\n\\n## Running the tests\\n\\n```bash\\npytest\\n```\\n"
SPECS["A13.2a"] = {
    "main": False,
    "starter": "def readme_report(text):\n    \"\"\"Check a README for the parts a reviewer looks for first.\"\"\"\n    return {\"title\": False, \"missing\": [], \"code_blocks\": 0, \"todos\": 0, \"score\": 0}\n",
    "cases": [
        {"name": "A complete README scores 100", "check": f"r = readme_report('{GOOD_README}')\nassert r == {{'title': True, 'missing': [], 'code_blocks': 2, 'todos': 0, 'score': 100}}, 'The complete example README should give title True, nothing missing, 2 code blocks, 0 TODOs and score 100'"},
        {"name": "Missing sections, in install/usage/tests order", "check": "r = readme_report('# tool\\n\\n## Install\\n\\n```\\npip install tool\\n```\\n')\nassert r['missing'] == ['usage', 'tests'], 'Without usage and test sections, missing should be [\"usage\", \"tests\"]'\nassert r['score'] == 60, '100 - 2 x 20 = 60'"},
        {"name": "Usage also counts Example or Quick start headings", "check": "r = readme_report('# t\\n\\n## Installation\\n\\n### Quick start\\n\\n## Testing\\n\\n```\\nx\\n```\\n')\nassert r['missing'] == [], 'Installation, Quick start and Testing cover all three sections'\nr2 = readme_report('# t\\n\\n## Install\\n\\n## Examples\\n\\n## Tests\\n\\n```\\nx\\n```\\n')\nassert r2['missing'] == [], 'An Examples heading counts as usage'"},
        {"name": "Title must be the first non-empty line, as an H1", "check": "assert readme_report('\\n\\n# Good title\\n## Install\\n## Usage\\n## Tests\\n```\\n```\\n')['title'] is True, 'Blank lines before the H1 are fine'\nr = readme_report('Some intro\\n# Late title\\n## Install\\n## Usage\\n## Tests\\n```\\n```\\n')\nassert r['title'] is False and r['score'] == 80, 'A title that is not the first line does not count: score 80'\nassert readme_report('## Install\\n## Usage\\n## Tests\\n```\\n```\\n')['title'] is False, 'A ## heading is not a title'"},
        {"name": "Headings inside code blocks do not count", "check": "r = readme_report('# t\\n\\n```markdown\\n## Install\\n## Usage\\n## Tests\\n```\\n')\nassert r['missing'] == ['install', 'usage', 'tests'], 'The headings are inside a fenced code block, so all three sections are still missing'\nassert r['code_blocks'] == 1"},
        {"name": "TODOs and no code blocks", "check": "r = readme_report('# t\\n## Install\\nTODO\\n## Usage\\nTODO: write\\n## Tests\\n')\nassert r['todos'] == 2 and r['code_blocks'] == 0, 'Two TODO lines and no fenced blocks'\nassert r['score'] == 80, '100 - 10 (no code block) - 2 x 5 (TODOs) = 80'"},
        {"name": "The score never goes below 0", "check": "r = readme_report('\\n'.join(['TODO'] * 30))\nassert r['score'] == 0, 'With 30 TODOs and nothing else the score is clamped at 0'"},
    ],
}
BAD["A13.2a"] = [
    SOLUTIONS["A13.2a"].replace("        if in_code:\n            continue\n", ""),                    # counts headings inside code
    SOLUTIONS["A13.2a"].replace('"score": max(0, score)', '"score": score'),                         # not clamped
    SOLUTIONS["A13.2a"].replace('("usage", "example", "quick start")', '("usage",)'),                # misses Example / Quick start
    SOLUTIONS["A13.2a"].replace('        if first is None and stripped:\n            first = stripped\n', '        if stripped.startswith("# "):\n            first = stripped\n'),  # title anywhere
]

# ------------------------------------------------------------------ A13.3a  tests that catch bugs
SHIPPING = '''import math


def shipping_cost(weight_kg, express=False):
    """Cost in cents for one parcel."""
    if weight_kg <= 0 or weight_kg > 30:
        raise ValueError("weight must be more than 0 and at most 30 kg")
    cost = 500 + 200 * max(0, math.ceil(weight_kg - 1))
    return cost * 2 if express else cost
'''
MUTANTS = {
    "30 kg is refused": SHIPPING.replace("weight_kg > 30", "weight_kg >= 30"),
    "0 kg is accepted": SHIPPING.replace("weight_kg <= 0", "weight_kg < 0"),
    "partial kilograms are rounded down": SHIPPING.replace("math.ceil(weight_kg - 1)", "math.floor(weight_kg - 1)"),
    "express adds 500 instead of doubling": SHIPPING.replace("cost * 2 if express else cost", "cost + 500 if express else cost"),
    "there is no upper weight limit": SHIPPING.replace(" or weight_kg > 30", ""),
}
FAKE_PYTEST = '''import contextlib


class _Raised:
    value = None


@contextlib.contextmanager
def raises(exc_type, match=None):
    info = _Raised()
    try:
        yield info
    except exc_type as e:
        info.value = e
        if match is not None:
            import re
            assert re.search(match, str(e)), f"exception message {str(e)!r} does not match {match!r}"
        return
    raise AssertionError(f"DID NOT RAISE {exc_type.__name__}")


def approx(x, rel=1e-6, abs=1e-12):
    class _A:
        def __eq__(self, other):
            return __builtins__["abs"](other - x) <= max(rel * __builtins__["abs"](x), abs) if isinstance(__builtins__, dict) else other == x
    return _A()
'''
SETUP_33 = ("open('shipping.py', 'w').write(" + repr(SHIPPING) + ")\nopen('pytest.py', 'w').write(" + repr(FAKE_PYTEST) + ")\n")
RUN_TESTS = '''
import sys, types
def run_suite(impl_src):
    mod = types.ModuleType("shipping")
    exec(impl_src, mod.__dict__)
    saved = sys.modules.get("shipping")
    sys.modules["shipping"] = mod
    try:
        g = {"__name__": "learner_tests", "__builtins__": __builtins__}
        exec(code, g)
        tests = {n: f for n, f in g.items() if n.startswith("test") and callable(f)}
        failed = []
        for name, fn in sorted(tests.items()):
            try:
                fn()
            except Exception as e:
                failed.append(name)
        return tests, failed
    finally:
        if saved is not None:
            sys.modules["shipping"] = saved
'''
SOLUTIONS["A13.3a"] = '''import pytest

from shipping import shipping_cost


def test_one_kilogram_is_the_base_price():
    assert shipping_cost(1) == 500


def test_each_started_kilogram_above_one_adds_200():
    assert shipping_cost(1.2) == 700
    assert shipping_cost(2) == 700
    assert shipping_cost(2.01) == 900


def test_express_doubles_the_total():
    assert shipping_cost(3, express=True) == 1800


def test_thirty_kilograms_is_the_maximum():
    assert shipping_cost(30) == 6300
    with pytest.raises(ValueError):
        shipping_cost(30.5)


def test_zero_and_negative_weights_are_refused():
    with pytest.raises(ValueError):
        shipping_cost(0)
    with pytest.raises(ValueError):
        shipping_cost(-1)
'''
cases = [{"name": "At least four tests, all passing on the correct code", "setup": SETUP_33, "check": RUN_TESTS + '''
tests, failed = run_suite(open("shipping.py").read())
assert len(tests) >= 4, f"Write at least four test functions whose names start with test_ (found {len(tests)})"
assert not failed, "These tests fail on the correct shipping_cost, so the test itself is wrong: " + ", ".join(failed)
'''}]
for label, src in MUTANTS.items():
    cases.append({"name": "Catches the bug: " + label, "setup": SETUP_33, "check": RUN_TESTS + f'''
tests, failed = run_suite({src!r})
assert failed, "None of your tests fails when {label}. Add a test at that boundary or case."
'''})
SPECS["A13.3a"] = {
    "main": False,
    "starter": "import pytest\n\nfrom shipping import shipping_cost\n\n\ndef test_one_kilogram_is_the_base_price():\n    assert shipping_cost(1) == 500\n",
    "cases": cases,
}
BAD["A13.3a"] = [
    SOLUTIONS["A13.3a"].split("def test_express")[0] + "def test_more():\n    assert shipping_cost(1, express=True) == 1000\n\n\ndef test_again():\n    assert shipping_cost(1) == 500\n",  # misses boundaries
    SOLUTIONS["A13.3a"].replace("assert shipping_cost(1.2) == 700", "assert shipping_cost(1.2) == 500"),  # wrong expectation
    "from shipping import shipping_cost\n",                                                                # no tests
]

# ------------------------------------------------------------------ A13.4a  wait_until with an injected clock
SOLUTIONS["A13.4a"] = '''import time


def wait_until(condition, timeout=5.0, interval=0.5, clock=time.monotonic, sleep=time.sleep):
    """Call condition() until it returns something truthy; return that value or raise TimeoutError."""
    start = clock()
    while True:
        value = condition()
        if value:
            return value
        if clock() - start >= timeout:
            raise TimeoutError(f"condition not met after {timeout} s")
        sleep(interval)
'''
FAKE = '''
class FakeTime:
    def __init__(self):
        self.now = 0.0
        self.sleeps = []
    def clock(self):
        return self.now
    def sleep(self, s):
        self.sleeps.append(s)
        self.now += s
'''
SPECS["A13.4a"] = {
    "main": False,
    "starter": "import time\n\n\ndef wait_until(condition, timeout=5.0, interval=0.5, clock=time.monotonic, sleep=time.sleep):\n    \"\"\"Call condition() until it returns something truthy; return that value or raise TimeoutError.\"\"\"\n    return condition()\n",
    "cases": [
        {"name": "Returns at once when the condition is already true", "check": FAKE + "t = FakeTime()\nassert wait_until(lambda: 'ready', clock=t.clock, sleep=t.sleep) == 'ready', 'Return the value the condition gave'\nassert t.sleeps == [], 'No sleeping when the first check succeeds'"},
        {"name": "Polls until the condition becomes true and returns its value", "check": FAKE + "t = FakeTime()\nr = wait_until(lambda: t.now >= 1.2 and {'rows': 3}, timeout=5, interval=0.5, clock=t.clock, sleep=t.sleep)\nassert r == {'rows': 3}, 'Return the truthy value itself, not True'\nassert t.sleeps == [0.5, 0.5, 0.5], 'Checks at 0, 0.5, 1.0 and 1.5 s: three sleeps of 0.5'"},
        {"name": "Times out with a clear message", "check": FAKE + "t = FakeTime()\ncalls = []\ntry:\n    wait_until(lambda: calls.append(1), timeout=2, interval=0.5, clock=t.clock, sleep=t.sleep)\nexcept TimeoutError as e:\n    assert 'after 2 s' in str(e), 'The message should say how long it waited, e.g. condition not met after 2 s'\nelse:\n    raise AssertionError('wait_until should raise TimeoutError when the condition never becomes true')\nassert len(calls) == 5, f'Check at 0, 0.5, 1, 1.5 and 2 s: 5 attempts (got {len(calls)})'"},
        {"name": "Uses the injected clock and sleep, never the real ones", "check": FAKE + "import time\nreal = time.sleep\ntime.sleep = lambda s: (_ for _ in ()).throw(AssertionError('Call the sleep you were given, not time.sleep'))\ntry:\n    t = FakeTime()\n    wait_until(lambda: t.now >= 1, timeout=3, interval=0.25, clock=t.clock, sleep=t.sleep)\n    assert t.sleeps == [0.25] * 4, 'Four sleeps of 0.25 s before the check at 1.0 s succeeds'\nfinally:\n    time.sleep = real"},
        {"name": "Errors raised by the condition are not hidden", "check": FAKE + "t = FakeTime()\ndef broken():\n    raise KeyError('missing field')\ntry:\n    wait_until(broken, timeout=2, clock=t.clock, sleep=t.sleep)\nexcept KeyError:\n    pass\nelse:\n    raise AssertionError('Let exceptions from the condition propagate: hiding them turns a bug into a timeout')"},
    ],
}
BAD["A13.4a"] = [
    SOLUTIONS["A13.4a"].replace('''        value = condition()
        if value:
            return value
        if clock() - start >= timeout:''', '''        if clock() - start >= timeout:
            raise TimeoutError(f"condition not met after {timeout} s")
        value = condition()
        if value:
            return value
        if False:'''),                                                         # checks the deadline first: one attempt too few
    SOLUTIONS["A13.4a"].replace("        value = condition()\n", "        try:\n            value = condition()\n        except Exception:\n            value = None\n"),  # swallows errors
    SOLUTIONS["A13.4a"].replace("            return value", "            return True"),                                                       # loses the value
]

for _eid, _bads in BAD.items():
    for _i, _b in enumerate(_bads):
        assert _b != SOLUTIONS[_eid], f"{_eid} bad#{_i} is identical to the solution"
