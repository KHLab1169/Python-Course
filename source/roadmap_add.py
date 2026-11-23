#!/usr/bin/env python3
"""Add module A14, The wider ecosystem: roadmap extras, to the Python Course.

Closes the gaps found by comparing the course with roadmap.sh/python: sorting and searching
algorithms with Big-O, binary search trees and heaps, processes versus threads and the GIL,
the packaging tool landscape (pip, uv, Poetry, PDM, Pipenv, conda, pyenv), documentation and
type-checker tooling (Sphinx, MkDocs, doctest, pyright, tox and nox, formatters), and a tour
of web frameworks (Django, Pyramid, Tornado, Sanic, aiohttp, gevent), plus what Python 3.12 to 3.14 added.
Run it with Python 3.14 (uv python install 3.14): the A14.7 examples use t-strings.
Idempotent: removes any earlier A14 data first. Example outputs come from running the code.
usage: python3 roadmap_add.py   (then deep_build.py, checks_build.py, deep_merge.py as usual)"""
import importlib.util, json, os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a147

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("b6", os.path.join(HERE, "specs/b6_roadmap.py"))
b6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b6)

MODULE = {
    "id": "a14", "n": "A14", "t": "The wider ecosystem: roadmap extras",
    "goal": "Fill the gaps a Python roadmap expects: classic algorithms and their cost, trees and heaps, processes versus threads, the packaging tools you will meet in other teams, documentation and type-checking tools, the web frameworks beyond Flask and FastAPI, and what Python 3.12 to 3.14 added.",
    "res": [["roadmap.sh: Python developer roadmap", "https://roadmap.sh/python"],
            ["Python docs: concurrent.futures", "https://docs.python.org/3/library/concurrent.futures.html"],
            ["Python Packaging User Guide", "https://packaging.python.org/en/latest/"],
            ["Sphinx documentation", "https://www.sphinx-doc.org/en/master/"],
            ["Django documentation: URL dispatcher", "https://docs.djangoproject.com/en/stable/topics/http/urls/"],
            ["What's new in Python 3.14", "https://docs.python.org/3/whatsnew/3.14.html"],
            ["PEP 750: template strings", "https://peps.python.org/pep-0750/"]],
    "items": [],
}

LESSONS = [
 {"id": "A14.1", "t": "Sorting, searching and Big-O", "min": 90,
  "learn": "Read code for its cost in Big-O terms, write merge sort and binary search yourself, and know when the built-in sorted() and the bisect module already do the job.",
  "ex": [
   ["Merge sort and binary search",
    "Write two functions without sorted(), list.sort(), heapq or bisect.\n\n"
    "merge_sort(items, key=None) returns a new sorted list:\n"
    "- Split the list in half, sort each half the same way, then merge the two sorted halves.\n"
    "- key works like sorted()'s key: compare key(item), or the item itself when key is None.\n"
    "- The sort is stable: items with equal keys keep their original order.\n"
    "- The input list is never changed, and even a one-item list comes back as a new list.\n\n"
    "binary_search(items, target) takes a sorted sequence and returns the index of the first item equal to target, or -1:\n"
    "- Keep a range [lo, hi) and halve it each step, so a million items need about 20 looks.\n"
    "- With duplicates, return the first one: binary_search([1, 2, 2, 2, 3], 2) is 1.\n"
    "- It must work on any sequence with len() and indexing, not only lists, and must not slice it.\n\n"
    "Examples: merge_sort([5, 2, 9, 1, 5, 6]) gives [1, 2, 5, 5, 6, 9]; binary_search([1, 3, 5, 7], 4) gives -1."]]},
 {"id": "A14.2", "t": "Trees and heaps", "min": 90,
  "learn": "Build a binary search tree with insert, lookup and in-order iteration, see why its shape decides its speed, and use heapq for priority queues and top-k problems.",
  "ex": [
   ["A binary search tree",
    "Complete the class BST (a Node class with value, left and right is given).\n\n"
    "Specification:\n"
    "- BST(values=()) starts empty (root is None) and inserts each of values in order.\n"
    "- insert(value) adds a new Node: smaller values go to the left, larger to the right. It returns True when the value was added and False when it was already there (duplicates are ignored).\n"
    "- value in tree (__contains__) walks down from the root; len(tree) is the number of values.\n"
    "- Iterating gives the values in sorted order (left subtree, node, right subtree).\n"
    "- height() is the number of nodes on the longest path from the root: 0 when empty, 1 for a single node.\n"
    "- min() and max() return the smallest and largest value and raise ValueError on an empty tree.\n\n"
    "Example: BST([5, 3, 8, 1, 4]) iterates as [1, 3, 4, 5, 8], has height 3, and tree.root.left.value is 3.\n\n"
    "Edge case: inserting 1, 2, 3, 4, 5 in order makes a chain of height 5, which is why balanced trees exist."]]},
 {"id": "A14.3", "t": "Processes, threads and the GIL", "min": 90,
  "learn": "Why the GIL means threads help with waiting but not with computing, how multiprocessing and ProcessPoolExecutor run Python on several cores, and how to split work into chunks for a pool.",
  "ex": [
   ["Split work for a process pool",
    "Write two functions. The pool is passed in, so the same code runs with a real ProcessPoolExecutor on your computer and with a stand-in pool in the tests.\n\n"
    "chunks(items, workers):\n"
    "- Split items (any iterable) into at most workers contiguous chunks, as lists, keeping the order.\n"
    "- Chunk sizes differ by at most one, with the bigger chunks first: 10 items for 3 workers gives sizes 4, 3, 3.\n"
    "- Never return an empty chunk: 2 items for 5 workers gives [[a], [b]], and no items gives [].\n"
    "- workers below 1 raises ValueError.\n\n"
    "parallel_sum(numbers, workers, executor):\n"
    "- Call executor.map exactly once, with the built-in sum and the list of chunks, so each worker adds up one chunk.\n"
    "- Return the sum of the partial sums.\n\n"
    "Example: chunks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3) gives [[1, 2, 3, 4], [5, 6, 7], [8, 9, 10]], and parallel_sum(range(1, 101), 4, pool) is 5050.\n\n"
    "The browser runs Python in a single thread, so the starter's ProcessPoolExecutor demo only runs on your computer (under if __name__ == \"__main__\":, which protects it on Windows and macOS too, with the import inside it so the page can still load your code)."]]},
 {"id": "A14.4", "t": "The packaging tool landscape", "min": 75,
  "learn": "What pip, venv, uv, Poetry, PDM, Pipenv, conda and pyenv each solve, how pyproject.toml and lock files fit together, and how to read a project's dependencies with tomllib.",
  "ex": [
   ["Dependency names from pyproject.toml",
    "Write normalize(name) and dependency_names(toml_text, extras=False).\n\n"
    "normalize(name) follows PEP 503: lower case, and every run of -, _ and . becomes a single -. normalize(\"Django.REST-framework\") is \"django-rest-framework\".\n\n"
    "dependency_names(toml_text, extras=False):\n"
    "- Parse the text with tomllib.loads.\n"
    "- Read the list [project].dependencies; with extras=True also every list in [project.optional-dependencies].\n"
    "- Each entry is a requirement string such as \"Requests[socks]>=2.31\", \"typing_extensions; python_version < '3.11'\" or \"mypkg @ git+https://...\". Keep only the name at the start (letters, digits, ., _ and -), drop extras, versions, markers and URLs, and normalise it.\n"
    "- Return the names sorted, each once.\n"
    "- A file without a [project] table or without dependencies gives []. Invalid TOML raises ValueError (tomllib.TOMLDecodeError already is one).\n\n"
    "Example: dependencies [\"Requests[socks]>=2.31\", \"requests>=2.0\", \"typing_extensions\"] give [\"requests\", \"typing-extensions\"]."],
   ["Set up one project three ways",
    "On your computer, create the same small project (one dependency, such as requests, and pytest for development) with three tools: pip with venv and a requirements file, uv (uv init, uv add, uv run pytest), and either Poetry or PDM. For each, note the files it creates, the command that installs everything on a fresh machine, and how it pins exact versions. Finish with three sentences on which you would pick for a new team project and why."]]},
 {"id": "A14.5", "t": "Documentation, type checkers and project tooling", "min": 90,
  "learn": "Docstrings that tools can read, Sphinx and MkDocs sites, doctest, the type checkers mypy, pyright and pyre, the formatters black, yapf and ruff format, and running checks on several Python versions with tox or nox.",
  "ex": [
   ["Docstring checker",
    "Write doc_report(source), which reads Python source with the ast module and returns a list of problems as strings, ordered by the line of the definition.\n\n"
    "Specification:\n"
    "- Check top-level functions (def and async def) and classes whose names do not start with _, and the methods of those classes whose names do not start with _ (so __init__ and other dunders are skipped). Nested functions are not checked.\n"
    "- No docstring: \"name: missing docstring\", where a method's name is written Class.method.\n"
    "- A function with a docstring must mention each parameter as a whole word: positional, *args, keyword-only and **kwargs names, but not self or cls. For each missing one, in parameter order: \"name: parameter p not documented\".\n"
    "- Classes only need a docstring; their parameters come from __init__, which is skipped.\n\n"
    "Example: for def move(shift, *, hours, **opts): with the docstring \"Move it by some hours.\", the result is [\"move: parameter shift not documented\", \"move: parameter opts not documented\"].\n\n"
    "Edge cases: the n inside \"number\" does not count as documenting n; a function in the result twice keeps parameter order."]]},
 {"id": "A14.6", "t": "A tour of web frameworks", "min": 90,
  "learn": "Where Django, Flask, FastAPI, Pyramid, Tornado, Sanic and aiohttp fit, WSGI versus ASGI, what gevent does, and how Django's URL dispatcher turns paths into views with typed arguments.",
  "ex": [
   ["Django-style URL routes",
    "Write resolve(patterns, path). patterns is a list of (route, view_name) pairs in Django's path() syntax; return (view_name, kwargs) for the first route that matches the whole path, or None.\n\n"
    "Specification:\n"
    "- One leading / is removed from path before matching. Routes have no leading /.\n"
    "- Text outside angle brackets must match exactly. <conv:name> captures a part with a converter; <name> alone means <str:name>.\n"
    "- Converters: str is one or more characters except /; int is one or more digits, returned as an int; slug is letters, digits, - and _; path is one or more of any character, / included.\n"
    "- The whole path must match: a missing trailing / or extra text means no match.\n"
    "- Routes are tried in order and the first match wins.\n"
    "- An unknown converter such as <float:v> raises ValueError.\n\n"
    "Example: resolve([(\"articles/<int:year>/<slug:title>/\", \"article\")], \"/articles/2024/tip-split/\") gives (\"article\", {\"year\": 2024, \"title\": \"tip-split\"})."],
   ["Pick a framework for three projects",
    "For each project, choose a framework (Django, Flask, FastAPI, Pyramid, Tornado, Sanic or aiohttp) and justify it in three or four sentences, naming one thing you would give up: 1. a staff scheduling app with logins, an admin screen and a relational database; 2. a JSON API that a mobile app calls, with request validation and generated documentation; 3. a service holding 10,000 open WebSocket connections for live updates."]]},
]

EXAMPLES = {
 "A14.1": {"title": "Counting the steps: linear search, binary search and sorting",
  "code": '''import bisect, math

def linear_steps(items, target):
    for steps, x in enumerate(items, 1):
        if x == target:
            return steps
    return len(items)

def binary_steps(items, target):
    lo, hi, steps = 0, len(items), 0
    while lo < hi:
        steps += 1
        mid = (lo + hi) // 2
        if items[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return steps

for n in (1_000, 1_000_000):
    data = list(range(n))
    target = n - 1
    print(f"n={n:>9,}: linear {linear_steps(data, target):>9,} steps, binary {binary_steps(data, target):>2} steps, "
          f"log2(n) = {math.log2(n):.1f}")
print("bisect agrees:", bisect.bisect_left(data, 765_432))
print("sorting a million items costs about n*log2(n) =", f"{int(1_000_000 * math.log2(1_000_000)):,}", "comparisons")
''',
  "note": "Linear search grows with n, so a thousand times more data means a thousand times more steps (O(n)). Binary search halves the range every step, so a million items need only 20 looks (O(log n)), but it needs sorted data, and sorting costs O(n log n). Sort once and search many times, and use bisect, which does the halving in C."},
 "A14.2": {"title": "heapq: a priority queue and the top three",
  "code": '''import heapq

tasks = []
heapq.heappush(tasks, (2, "write tests"))
heapq.heappush(tasks, (1, "fix the outage"))
heapq.heappush(tasks, (3, "update the README"))
heapq.heappush(tasks, (1, "answer the on-call page"))
while tasks:
    priority, name = heapq.heappop(tasks)
    print(priority, name)

response_ms = [120, 85, 940, 230, 60, 1210, 310, 75, 880]
print("slowest three:", heapq.nlargest(3, response_ms))
print("fastest two:", heapq.nsmallest(2, response_ms))
''',
  "note": "A heap keeps the smallest item at index 0, and push and pop each cost O(log n), so it is the standard priority queue. Tuples compare item by item, so (priority, name) pops by priority and breaks ties by name. nlargest and nsmallest find the top k without sorting everything."},
 "A14.3": {"title": "The GIL in numbers: threads for waiting, processes for computing",
  "code": '''import time
from concurrent.futures import ThreadPoolExecutor

def wait_for_io(_):
    time.sleep(0.2)          # like a network call: the GIL is released while waiting

def compute(_):
    return sum(i * i for i in range(300_000))   # pure Python: holds the GIL

for name, fn in [("waiting", wait_for_io), ("computing", compute)]:
    start = time.perf_counter()
    for i in range(4):
        fn(i)
    one_by_one = time.perf_counter() - start
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(fn, range(4)))
    threaded = time.perf_counter() - start
    print(f"{name:9}: one by one {one_by_one:.2f} s, four threads {threaded:.2f} s, speed-up x{one_by_one / threaded:.1f}")
''',
  "sample": True,
  "output": "waiting  : one by one 0.80 s, four threads 0.20 s, speed-up x4.0\ncomputing: one by one 0.11 s, four threads 0.11 s, speed-up x1.0",
  "note": "While a thread waits (sleep, network, disk), it releases the GIL and the others run, so four waits overlap. Pure-Python computing holds the GIL, so four threads take as long as one. For computing, use ProcessPoolExecutor or multiprocessing: each process has its own interpreter and its own GIL. Your timings will differ; the browser runs Python in one thread, so run this one on your computer."},
 "A14.4": {"title": "Reading pyproject.toml with tomllib",
  "code": '''import tomllib

text = """
[project]
name = "shiftboard"
version = "0.3.0"
requires-python = ">=3.11"
dependencies = ["requests>=2.31", "pydantic>=2,<3"]

[project.optional-dependencies]
test = ["pytest>=8"]

[project.scripts]
shiftboard = "shiftboard.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
"""
data = tomllib.loads(text)
project = data["project"]
print(project["name"], project["version"], "needs Python", project["requires-python"])
print("runtime:", project["dependencies"])
print("test extra:", project["optional-dependencies"]["test"])
print("command:", list(project["scripts"]))
print("built with:", data["build-system"]["build-backend"])
''',
  "note": "pyproject.toml is the one file every modern tool reads: pip, uv, Poetry, PDM and Hatch all take the [project] table (the standard from PEP 621), and [build-system] says which backend builds the wheel. tomllib (Python 3.11+) reads it; it is read-only, so tools that edit the file use tomli-w or tomlkit."},
 "A14.5": {"title": "doctest: examples in the docstring that are also tests",
  "code": '''import doctest

def split_tips(total_cents, hours):
    """Split tips by hours worked; leftover cents go to the longest shifts.

    Args:
        total_cents: the tips to share, in cents.
        hours: hours worked by each person.

    Returns:
        A list of cents per person that adds up to total_cents.

    >>> split_tips(1000, [4, 4, 2])
    [400, 400, 200]
    >>> split_tips(100, [1, 1, 1])
    [34, 33, 33]
    >>> sum(split_tips(997, [3, 5, 8]))
    997
    """
    shares = [total_cents * h // sum(hours) for h in hours]
    order = sorted(range(len(hours)), key=lambda i: -hours[i])
    for i in order[: total_cents - sum(shares)]:
        shares[i] += 1
    return shares

result = doctest.testmod(verbose=False)
print(f"doctest ran {result.attempted} examples, {result.failed} failed")
print(split_tips.__doc__.splitlines()[0])
''',
  "note": "The docstring follows the Google style (Args, Returns), which Sphinx's napoleon extension and MkDocs' mkdocstrings turn into reference pages, and its examples are run by doctest, so the documentation cannot drift from the code. In a project, pytest --doctest-modules runs them with the rest of your tests."},
 "A14.6": {"title": "WSGI underneath every synchronous framework",
  "code": '''from wsgiref.util import setup_testing_defaults

def app(environ, start_response):
    """The whole WSGI contract: a callable that takes the request and returns the body."""
    path = environ["PATH_INFO"]
    if path == "/health":
        status, body = "200 OK", b"ok"
    else:
        status, body = "404 Not Found", b"no route for " + path.encode()
    start_response(status, [("Content-Type", "text/plain"), ("Content-Length", str(len(body)))])
    return [body]

def call(path):
    environ = {}
    setup_testing_defaults(environ)
    environ["PATH_INFO"] = path
    seen = {}
    body = b"".join(app(environ, lambda status, headers: seen.update(status=status)))
    return seen["status"], body.decode()

print(call("/health"))
print(call("/shifts/42"))
''',
  "note": "Django, Flask and Pyramid are WSGI applications: one callable that a server such as Gunicorn calls once per request. FastAPI, Starlette, Sanic and aiohttp use ASGI, the async version, which can also hold WebSocket connections open. Frameworks add routing, templates, ORMs and middleware on top of this small contract."},
}

TEXT_SOLUTIONS = {
 "A14.4b": ("text", [
   "Run each tool in its own empty folder so the files it creates are easy to see.",
   "Look for three things: where dependencies are declared (pyproject.toml or requirements.txt), where exact versions are pinned (a lock file), and the one command a teammate runs on a fresh clone.",
   "Time a fresh install with each tool; uv is usually several times faster than pip."],
   "Every team picks a different tool, so being able to read and run any of them on day one matters more than having a favourite.",
   "1. pip + venv: python -m venv .venv; pip install requests pytest; pip freeze > requirements.txt. Files: .venv/, requirements.txt (exact pins, but dev and runtime mixed). Fresh machine: python -m venv .venv && pip install -r requirements.txt.\n"
   "2. uv: uv init; uv add requests; uv add --dev pytest; uv run pytest. Files: pyproject.toml, uv.lock, .python-version, .venv/. Fresh machine: uv sync. Pins every version in uv.lock, including hashes.\n"
   "3. Poetry: poetry new; poetry add requests; poetry add --group dev pytest. Files: pyproject.toml, poetry.lock. Fresh machine: poetry install.\n\n"
   "Choice: uv for a new team project. It uses the standard [project] table, so the project is not locked into one tool, it manages Python versions too (replacing pyenv), and installs are fast enough that CI caches matter less. Poetry is a fine choice where a team already uses it.",
   ["The same project was set up with pip and venv, uv, and Poetry or PDM", "For each tool: the files it creates and the fresh-machine install command", "Explains where exact versions are pinned (requirements file or lock file)", "A justified choice for a new team project"]),
 "A14.6b": ("text", [
   "Start from what each project needs most: built-in features (logins, admin, ORM), request validation and docs, or many long-lived connections.",
   "Batteries included versus micro-framework is the main trade-off: Django gives you a lot and decides a lot; Flask and FastAPI let you choose.",
   "Long-lived connections need an async (ASGI) framework, or the server runs out of threads."],
   "Framework choice is a common interview and design question. A good answer names the project's main need and what you give up.",
   "1. Django: logins, an admin screen and an ORM with migrations come built in, which is most of a scheduling app. I give up some flexibility, since Django has its own way of doing everything.\n"
   "2. FastAPI: validation and OpenAPI documentation come from type hints with Pydantic, and it is async if the API calls other services. I give up Django's admin and ORM, so I pick SQLAlchemy and an auth library myself.\n"
   "3. aiohttp or Starlette/FastAPI on an ASGI server: one event loop holds thousands of idle WebSocket connections cheaply, where a thread per connection would not scale. I give up the simplicity of synchronous code and must keep every handler non-blocking.",
   ["Each project has a named framework", "Each choice is tied to the project's main need", "Each answer names something given up", "The WebSocket answer uses an async (ASGI) framework and says why"]),
}

AUTO = {
 "A14.1a": {"hints": ["merge_sort: a list of 0 or 1 items is already sorted (return a copy); otherwise sort items[:mid] and items[mid:] recursively.",
                       "Merge with two indexes i and j, taking from the left half while key(left[i]) <= key(right[j]); the <= keeps the sort stable. Add whatever is left over at the end.",
                       "binary_search: keep lo = 0, hi = len(items); while lo < hi, look at mid = (lo + hi) // 2, then move lo past mid when items[mid] < target, otherwise set hi = mid. At the end, check items[lo] == target."],
            "explain": "Merge sort does O(n log n) work at every size because each level of splitting does n comparisons and there are log n levels; taking from the left half on ties is what makes it stable, which is why Python's own sort (Timsort) is stable too. The binary search form that moves hi down on equality finds the first occurrence instead of any occurrence, the same rule as bisect_left. Typical slips: using < in the merge (unstable), returning mid as soon as it matches (not the first duplicate), and slicing the sequence in binary search (which copies data and costs O(n))."},
 "A14.2a": {"hints": ["insert: if the tree is empty, the new Node is the root. Otherwise walk down from the root, going left when value < node.value and right when it is larger, until the child on that side is None.",
                       "Return False as soon as you meet an equal value, and keep a counter for len().",
                       "Iterate in order with a recursive generator (yield from the left subtree, yield the value, yield from the right) or with an explicit stack; height is 0 for None and 1 + max(left height, right height) otherwise."],
            "explain": "Every comparison sends the search to one side, so lookup and insert cost O(height): about log2(n) for a balanced tree, but n for a chain built from sorted input. That is why real libraries use self-balancing trees (red-black, AVL) or a different structure: Python's dict and set are hash tables, and the sortedcontainers package uses sorted lists. In-order traversal visits left, node, right, so it gives sorted output for free."},
 "A14.3a": {"hints": ["Turn items into a list first, then n = min(workers, len(items)) is the number of chunks; return [] when it is 0.",
                       "divmod(len(items), n) gives the base size and how many chunks get one extra item; give the extras to the first chunks.",
                       "parallel_sum is one line: sum(executor.map(sum, chunks(numbers, workers)))."],
            "explain": "Sending work to another process costs time (the data is pickled and copied), so pools work best with a few large chunks rather than one task per item, which is what chunks does and what executor.map's chunksize argument does for you. Passing the executor in keeps the function testable and lets the caller choose threads for waiting or processes for computing. Typical slips: empty chunks when there are more workers than items, and summing in the main process without using the pool at all."},
 "A14.4a": {"hints": ["normalize is one re.sub: replace the pattern [-_.]+ with \"-\", then lower-case the result.",
                       "tomllib.loads(text) gives nested dictionaries; use .get(\"project\", {}) and .get(\"dependencies\", []) so missing tables are fine.",
                       "A regular expression anchored at the start, ^\\s*([A-Za-z0-9][A-Za-z0-9._-]*), picks the name out of every requirement form; collect into a set, then return sorted(names)."],
            "explain": "Requirement strings (PEP 508) can carry extras, version specifiers, environment markers and direct URLs, but the name always comes first, so matching the name at the start is more robust than splitting on every possible operator. Normalising names matters because PyPI treats Django_Rest.Framework and django-rest-framework as the same project; tools such as pip, uv and pip-audit compare normalised names. This is the first step of a dependency audit: compare the names with an allow-list, a lock file or a vulnerability database."},
 "A14.5a": {"hints": ["Loop over ast.parse(source).body for top-level nodes, and over a class's body for its methods; ast.get_docstring(node) returns None when there is no docstring.",
                       "Collect parameter names from node.args: posonlyargs, args, vararg, kwonlyargs and kwarg (the last two may be None), then drop self and cls.",
                       "Use re.search(rf\"\\b{re.escape(p)}\\b\", doc) for a whole-word match, keep (lineno, message) pairs, and sort by line number at the end."],
            "explain": "Working on the syntax tree, not on text, means comments, strings and odd formatting cannot fool the checker, and the same approach powers real tools: pydocstyle and ruff's D rules check docstrings, and interrogate measures documentation coverage. Whole-word matching avoids false passes such as n inside number. Typical slips: forgetting keyword-only and **kwargs parameters, reporting self, and checking private helpers that do not need public documentation."},
 "A14.6a": {"hints": ["Turn each route into a regular expression: escape the plain text with re.escape, and replace each <conv:name> with a named group such as (?P<year>[0-9]+).",
                       "Keep a dictionary from group name to a conversion function (int for int, str for the others) and apply it to m.groupdict() after a match.",
                       "Anchor the pattern with ^ and $ (or use fullmatch) so extra text fails, strip one leading / from the path, and return on the first matching route."],
            "explain": "This is how Django's path() works inside: each route compiles to a regular expression with named groups, and converters both restrict what matches and convert the captured text, so views receive an int year instead of a string. Trying routes in order makes the first match win, which is why specific routes go before general ones. Typical slips: forgetting the $ anchor (articles/2024/x/ would match articles/2024/), letting str match a slash, and returning strings for int parts."},
}

QUIZ = [
 ("Binary search on a sorted list of a million items needs about how many comparisons?", ["20", "1,000", "500,000", "1,000,000"], 0,
  "Each comparison halves the range: 2 to the power 20 is about a million, so O(log n) means about 20 looks."),
 ("Which of these is O(n log n)?", ["Sorting with merge sort or sorted()", "Looking up a key in a dict", "Finding an item with a linear scan", "Reading the first item of a list"], 0,
  "Comparison sorts need about n log n comparisons; dict lookup is O(1) on average and a linear scan is O(n)."),
 ("What does a stable sort guarantee?", ["Items with equal keys keep their original order", "The sort never raises an error", "The input list is not changed", "It always takes the same time"], 0,
  "Stability lets you sort by one key, then by another, and keep the first order within ties. Python's sort is stable."),
 ("A binary search tree is built by inserting 1, 2, 3, ..., 1000 in order. What is its height?", ["1000", "10", "500", "2"], 0,
  "Each new value is larger than all the others, so it goes right every time and the tree becomes a chain. Balanced trees avoid this."),
 ("Which structure gives the smallest item in O(1) and removes it in O(log n)?", ["A heap (heapq)", "A sorted list with insert", "A dict", "A set"], 0,
  "heap[0] is always the smallest; heappop restores the heap property in O(log n)."),
 ("Your program spends its time on pure-Python calculations. What speeds it up on a 4-core machine?", ["ProcessPoolExecutor or multiprocessing", "ThreadPoolExecutor", "asyncio", "Adding time.sleep(0)"], 0,
  "The GIL lets only one thread run Python bytecode at a time; separate processes each have their own interpreter and GIL."),
 ("Why must ProcessPoolExecutor code sit under if __name__ == \"__main__\":?", ["Child processes import the main module, and without the guard they would start pools of their own", "It makes the code run faster", "Python forbids pools at module level", "It turns off the GIL"], 0,
  "With the spawn start method (Windows, macOS) each worker imports your module; the guard stops that import from starting new workers."),
 ("What does a lock file (uv.lock, poetry.lock) add on top of pyproject.toml?", ["The exact version of every package, including indirect ones, so installs are reproducible", "The project's licence", "The list of Python files", "A faster Python interpreter"], 0,
  "pyproject.toml states ranges such as requests>=2.31; the lock file records exactly what was resolved."),
 ("Which tool type-checks Python code without running it?", ["pyright", "black", "Sphinx", "tox"], 0,
  "mypy, pyright and pyre are static type checkers; black formats, Sphinx builds docs, tox runs commands in several environments."),
 ("A service must hold thousands of open WebSocket connections. Which kind of framework fits?", ["An ASGI framework on an event loop, such as aiohttp, Starlette or FastAPI", "Any WSGI framework with more threads", "Django's admin", "A static site generator"], 0,
  "WSGI handles one request per thread until it returns; ASGI can keep many idle connections open cheaply in one event loop."),
]


LESSONS.append(a147.LESSON)
EXAMPLES["A14.7"] = a147.EXAMPLE
AUTO["A14.7a"] = a147.AUTO
QUIZ.extend(a147.QUIZ)


def run_example(code):
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=60, cwd=d)
    if r.returncode != 0:
        raise SystemExit("example failed:\n" + r.stderr)
    return r.stdout.rstrip("\n")


def main():
    d = json.load(open(os.path.join(HERE, "pycontent.json")))
    for k in [k for k in d["lessons"] if k.startswith("A14.")]:
        del d["lessons"][k]
    for coll in ("grade", "chk"):
        for k in [k for k in d[coll] if k.startswith("A14.")]:
            del d[coll][k]
    d["quiz"].pop("a14", None)

    MODULE["items"] = []
    for L in LESSONS:
        MODULE["items"].append({"id": L["id"], "t": L["t"], "min": L["min"], "learn": L["learn"], "kind": "lesson",
                                "ex": [{"id": L["id"] + "abc"[i], "t": e[0], "p": e[1]} for i, e in enumerate(L["ex"])]})
        ex = EXAMPLES[L["id"]]
        example = {"title": ex["title"], "code": ex["code"], "note": ex["note"]}
        if ex.get("sample"):
            example["output"] = ex["output"]
            example["sample"] = True
        else:
            example["output"] = run_example(ex["code"])
        lesson = {"example": example, "exercises": {}}
        for i, _ in enumerate(L["ex"]):
            eid = L["id"] + "abc"[i]
            if eid in AUTO:
                lesson["exercises"][eid] = {"hints": AUTO[eid]["hints"], "lang": "python", "solution": b6.SOLUTIONS[eid],
                                            "explain": AUTO[eid]["explain"]}
                d["grade"][eid] = dict(b6.SPECS[eid])
            else:
                lang, hints, why, sol, chk = TEXT_SOLUTIONS[eid]
                lesson["exercises"][eid] = {"hints": hints, "lang": lang, "solution": sol, "explain": why}
                d["chk"][eid] = chk
        d["lessons"][L["id"]] = lesson
    d["quiz"]["a14"] = [{"id": f"a14-{n + 1:02d}", "type": "single", "pool": "quiz", "prompt": q, "code": "",
                         "options": opts, "answer": [ans], "explain": ex} for n, (q, opts, ans, ex) in enumerate(QUIZ)]
    json.dump(d, open(os.path.join(HERE, "pycontent.json"), "w"), ensure_ascii=False)

    page = open(os.path.join(HERE, "course.html"), encoding="utf-8").read()
    m = re.search(r"var MA=(\[.*?\]);\n", page)
    ma = json.loads(m.group(1))
    ma = [x for x in ma if x["id"] != "a14"]
    at = next(i for i, x in enumerate(ma) if x["id"] == "a12")   # before the capstone
    ma.insert(at, MODULE)
    page = page[:m.start(1)] + json.dumps(ma, ensure_ascii=False) + page[m.end(1):]
    if '"a14"' not in page.split("var COURSES=[")[1].split("];")[0]:
        page = page.replace('  {code:"PY205",t:"Web APIs and Data Analysis",y:2,mods:["a10","a10b","a11"]},',
                            '  {code:"PY205",t:"Web APIs and Data Analysis",y:2,mods:["a10","a10b","a11"]},\n  {code:"PY206",t:"The Wider Ecosystem: Roadmap Extras",y:2,mods:["a14"]},')
    if "a14:" not in page:
        page = page.replace("a11:4,a12:5,a13:3};", "a11:4,a12:5,a13:3,a14:3};")
    i = page.find("window.PYCC_CONTENT=") + len("window.PYCC_CONTENT=")
    j = page.find(";</script>", i)
    c = json.loads(page[i:j].replace("<\\!", "<!"))
    for k in ("lessons", "grade", "chk", "quiz"):
        c[k] = d[k]
    page = page[:i] + json.dumps(c).replace("</", "<\\/").replace("<!", "<\\!") + page[j:]
    open(os.path.join(HERE, "course.html"), "w", encoding="utf-8").write(page)
    print("A14 added:", len(LESSONS), "lessons,", sum(len(L["ex"]) for L in LESSONS), "exercises,", len(QUIZ), "quiz questions")


if __name__ == "__main__":
    main()
