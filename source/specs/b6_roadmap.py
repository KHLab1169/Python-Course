"""Autograder specs for module A14, The wider ecosystem: roadmap extras (Python Course, Track 2)."""
SOLUTIONS = {}
SPECS = {}
BAD = {}

# ------------------------------------------------------------------ A14.1a  merge sort and binary search
SOLUTIONS["A14.1a"] = '''def merge_sort(items, key=None):
    """Return a new sorted list (stable), without sorted() or list.sort()."""
    key = key or (lambda x: x)
    items = list(items)
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    left, right = merge_sort(items[:mid], key), merge_sort(items[mid:], key)
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):   # <= keeps equal items in their original order
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    return out + left[i:] + right[j:]


def binary_search(items, target):
    """Return the index of the first occurrence of target in sorted items, or -1."""
    lo, hi = 0, len(items)
    while lo < hi:
        mid = (lo + hi) // 2
        if items[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo if lo < len(items) and items[lo] == target else -1


if __name__ == "__main__":
    data = [5, 2, 9, 1, 5, 6]
    print(merge_sort(data), binary_search(merge_sort(data), 5))
'''
_SEQ = '''class Seq:
    """A read-only sequence that counts how many items are looked at."""
    def __init__(self, n):
        self.n, self.reads = n, 0
    def __len__(self):
        return self.n
    def __getitem__(self, i):
        if isinstance(i, slice):
            raise TypeError("slicing copies the data; look at single items instead")
        if i < 0:
            i += self.n
        if not 0 <= i < self.n:
            raise IndexError(i)
        self.reads += 1
        return i * 2
'''
SPECS["A14.1a"] = {
    "main": False,
    "starter": "def merge_sort(items, key=None):\n    \"\"\"Return a new sorted list (stable), without sorted() or list.sort().\"\"\"\n    pass\n\n\ndef binary_search(items, target):\n    \"\"\"Return the index of the first occurrence of target in sorted items, or -1.\"\"\"\n    pass\n",
    "cases": [
        {"name": "merge_sort sorts numbers", "check": "assert merge_sort([5, 2, 9, 1, 5, 6]) == [1, 2, 5, 5, 6, 9], 'merge_sort([5, 2, 9, 1, 5, 6]) should be [1, 2, 5, 5, 6, 9]'\nassert merge_sort([]) == [] and merge_sort([7]) == [7], 'An empty list and a single item are already sorted'\nimport random\nrng = random.Random(4)\ndata = [rng.randint(-1000, 1000) for _ in range(500)]\nassert merge_sort(data) == sorted(data), 'merge_sort gives the wrong order for 500 random numbers'"},
        {"name": "merge_sort returns a new list", "check": "data = [3, 1, 2]\nresult = merge_sort(data)\nassert data == [3, 1, 2], 'merge_sort must not change the list it was given'\nassert result == [1, 2, 3] and result is not data, 'Return a new list'\none = [7]\nassert merge_sort(one) is not one, 'Even a one-item list comes back as a new list'"},
        {"name": "key and stability", "check": "rows = [('b', 2), ('a', 1), ('c', 2), ('d', 1)]\nassert merge_sort(rows, key=lambda r: r[1]) == [('a', 1), ('d', 1), ('b', 2), ('c', 2)], 'Items with equal keys must keep their original order (a stable sort): expected a, d, b, c'\nassert merge_sort(['pear', 'Fig', 'apple'], key=str.lower) == ['apple', 'Fig', 'pear'], 'Sort by key(item), not by the item itself'"},
        {"name": "no built-in sorting", "static": True, "check": "import ast\ntree = ast.parse(code)\ncalls = [n.func for n in ast.walk(tree) if isinstance(n, ast.Call)]\nassert not any(isinstance(f, ast.Name) and f.id == 'sorted' for f in calls), 'Write the merge yourself: no sorted()'\nassert not any(isinstance(f, ast.Attribute) and f.attr == 'sort' for f in calls), 'Write the merge yourself: no list.sort()'\nassert not any(isinstance(n, (ast.Import, ast.ImportFrom)) and any(a.name in ('heapq', 'bisect') for a in n.names) or (isinstance(n, ast.ImportFrom) and n.module in ('heapq', 'bisect')) for n in ast.walk(tree)), 'Write both algorithms yourself, without heapq or bisect'"},
        {"name": "binary_search finds the first match", "check": "assert binary_search([1, 3, 5, 7], 5) == 2, 'binary_search([1, 3, 5, 7], 5) should be 2'\nassert binary_search([1, 3, 5, 7], 1) == 0 and binary_search([1, 3, 5, 7], 7) == 3, 'Check the first and last positions'\nassert binary_search([1, 2, 2, 2, 3], 2) == 1, 'With duplicates, return the index of the first one (1)'"},
        {"name": "binary_search reports missing values", "check": "assert binary_search([1, 3, 5, 7], 4) == -1, 'A missing value gives -1'\nassert binary_search([1, 3, 5, 7], 9) == -1 and binary_search([1, 3, 5, 7], 0) == -1, 'Values past either end give -1'\nassert binary_search([], 3) == -1, 'An empty list gives -1'"},
        {"name": "binary_search looks at few items", "check": _SEQ + "s = Seq(1_000_000)\nassert binary_search(s, 1_530_864) == 765_432, 'binary_search on a sorted sequence of a million even numbers should find 1530864 at 765432'\nassert s.reads <= 25, f'binary_search looked at {s.reads} items; halving the range each time needs about 20'\ns2 = Seq(1_000_000)\nassert binary_search(s2, 7) == -1 and s2.reads <= 25, 'A missing value should also take about 20 looks'"},
    ],
}
BAD["A14.1a"] = [
    SOLUTIONS["A14.1a"].replace("if key(left[i]) <= key(right[j]):", "if key(left[i]) < key(right[j]):"),   # unstable
    SOLUTIONS["A14.1a"].replace('''        if items[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo if lo < len(items) and items[lo] == target else -1''', '''        if items[mid] == target:
            return mid
        if items[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return -1'''),   # any occurrence, not the first
    SOLUTIONS["A14.1a"].replace('''    lo, hi = 0, len(items)
    while lo < hi:''', '''    for i in range(len(items)):
        if items[i] == target:
            return i
    return -1
    lo, hi = 0, len(items)
    while lo < hi:'''),   # linear search
    SOLUTIONS["A14.1a"].replace('''    key = key or (lambda x: x)
    items = list(items)''', '''    key = key or (lambda x: x)'''),  # returns the same list for length 1
]

# ------------------------------------------------------------------ A14.2a  binary search tree
SOLUTIONS["A14.2a"] = '''class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:
    """A binary search tree of unique values."""

    def __init__(self, values=()):
        self.root = None
        self.size = 0
        for v in values:
            self.insert(v)

    def insert(self, value):
        """Add value; return False if it was already there."""
        if self.root is None:
            self.root = Node(value)
            self.size = 1
            return True
        node = self.root
        while True:
            if value == node.value:
                return False
            side = "left" if value < node.value else "right"
            child = getattr(node, side)
            if child is None:
                setattr(node, side, Node(value))
                self.size += 1
                return True
            node = child

    def __contains__(self, value):
        node = self.root
        while node is not None:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False

    def __len__(self):
        return self.size

    def __iter__(self):
        stack, node = [], self.root
        while stack or node is not None:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            yield node.value
            node = node.right

    def height(self):
        def h(node):
            return 0 if node is None else 1 + max(h(node.left), h(node.right))
        return h(self.root)

    def min(self):
        if self.root is None:
            raise ValueError("min() of an empty tree")
        node = self.root
        while node.left is not None:
            node = node.left
        return node.value

    def max(self):
        if self.root is None:
            raise ValueError("max() of an empty tree")
        node = self.root
        while node.right is not None:
            node = node.right
        return node.value


if __name__ == "__main__":
    t = BST([5, 3, 8, 1, 4])
    print(list(t), len(t), t.height(), 4 in t)
'''
SPECS["A14.2a"] = {
    "main": False,
    "starter": "class Node:\n    def __init__(self, value):\n        self.value = value\n        self.left = None\n        self.right = None\n\n\nclass BST:\n    \"\"\"A binary search tree of unique values.\"\"\"\n\n    def __init__(self, values=()):\n        self.root = None\n\n    def insert(self, value):\n        \"\"\"Add value; return False if it was already there.\"\"\"\n        pass\n",
    "cases": [
        {"name": "insert, len and in", "check": "t = BST()\nassert len(t) == 0 and 3 not in t, 'A new tree is empty'\nassert t.insert(5) is True and t.insert(3) is True and t.insert(8) is True, 'insert returns True for a new value'\nassert len(t) == 3, 'len() counts the values'\nassert 3 in t and 8 in t and 4 not in t, 'in (__contains__) should find 3 and 8 but not 4'"},
        {"name": "duplicates are ignored", "check": "t = BST([5, 3])\nassert t.insert(3) is False, 'Inserting a value that is already there returns False'\nassert len(t) == 2, 'A duplicate does not change the size'"},
        {"name": "it is really a tree", "check": "t = BST([5, 3, 8, 4])\nr = t.root\nassert r is not None and r.value == 5, 'The first value becomes the root'\nassert r.left is not None and r.left.value == 3 and r.right is not None and r.right.value == 8, 'Smaller values go left, larger go right'\nassert r.left.right is not None and r.left.right.value == 4, '4 is smaller than 5 but larger than 3, so it goes left then right'"},
        {"name": "iteration is in order", "check": "t = BST([50, 30, 70, 20, 40, 60, 80, 35])\nassert list(t) == [20, 30, 35, 40, 50, 60, 70, 80], 'Iterating gives the values in sorted order (left, node, right)'\nassert list(BST()) == [], 'An empty tree iterates to nothing'"},
        {"name": "height", "check": "assert BST().height() == 0, 'An empty tree has height 0'\nassert BST([1]).height() == 1, 'One node has height 1'\nassert BST([5, 3, 8, 1, 4]).height() == 3, 'BST([5, 3, 8, 1, 4]) has height 3'\nassert BST([1, 2, 3, 4, 5]).height() == 5, 'Sorted inserts make a chain: height 5'"},
        {"name": "min and max", "check": "t = BST([5, 3, 8, 1, 9])\nassert t.min() == 1 and t.max() == 9, 'min() and max() follow the left and right edges'\ntry:\n    BST().min()\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('min() of an empty tree raises ValueError')\ntry:\n    BST().max()\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('max() of an empty tree raises ValueError')"},
    ],
}
BAD["A14.2a"] = [
    SOLUTIONS["A14.2a"].replace('''            if value == node.value:
                return False
            side''', '''            side'''),                         # duplicates inserted
    SOLUTIONS["A14.2a"].replace('''            node = stack.pop()
            yield node.value
            node = node.right''', '''            node = stack.pop()
            node = node.right'''),            # iteration yields nothing
    SOLUTIONS["A14.2a"].replace("return 0 if node is None else 1 + max", "return -1 if node is None else 1 + max"),   # edges not nodes
    SOLUTIONS["A14.2a"].replace('''        if self.root is None:
            raise ValueError("min() of an empty tree")
''', '''        if self.root is None:
            return None
'''),
]

# ------------------------------------------------------------------ A14.3a  splitting work for a pool
SOLUTIONS["A14.3a"] = '''def chunks(items, workers):
    """Split items into at most `workers` contiguous chunks whose sizes differ by at most one."""
    if workers < 1:
        raise ValueError("workers must be at least 1")
    items = list(items)
    n = min(workers, len(items))
    if n == 0:
        return []
    size, extra = divmod(len(items), n)
    out, start = [], 0
    for k in range(n):
        end = start + size + (1 if k < extra else 0)
        out.append(items[start:end])
        start = end
    return out


def parallel_sum(numbers, workers, executor):
    """Sum numbers by giving one chunk to each worker through executor.map."""
    return sum(executor.map(sum, chunks(numbers, workers)))


if __name__ == "__main__":
    # Imported here: the browser's Python cannot start processes, but your computer can.
    from concurrent.futures import ProcessPoolExecutor

    with ProcessPoolExecutor(max_workers=4) as pool:
        print(parallel_sum(range(1, 1_000_001), 4, pool))
'''
_FAKE = '''class FakePool:
    """Runs everything in this process and records what it was asked to do."""
    def __init__(self):
        self.calls = []
    def map(self, fn, *iterables):
        jobs = list(iterables[0])
        self.calls.append((fn, jobs))
        return [fn(j) for j in jobs]
    def submit(self, fn, *a, **kw):
        raise AssertionError("Use executor.map for this exercise, not submit")
'''
SPECS["A14.3a"] = {
    "main": False,
    "starter": "def chunks(items, workers):\n    \"\"\"Split items into at most `workers` contiguous chunks whose sizes differ by at most one.\"\"\"\n    pass\n\n\ndef parallel_sum(numbers, workers, executor):\n    \"\"\"Sum numbers by giving one chunk to each worker through executor.map.\"\"\"\n    pass\n\n\nif __name__ == \"__main__\":\n    # Imported here: the browser's Python cannot start processes, but your computer can.\n    from concurrent.futures import ProcessPoolExecutor\n\n    with ProcessPoolExecutor(max_workers=4) as pool:\n        print(parallel_sum(range(1, 1_000_001), 4, pool))\n",
    "cases": [
        {"name": "even split", "check": "assert chunks(list(range(1, 10)), 3) == [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 'chunks(1..9, 3) gives three chunks of three'"},
        {"name": "larger chunks first", "check": "assert chunks(list(range(1, 11)), 3) == [[1, 2, 3, 4], [5, 6, 7], [8, 9, 10]], 'chunks(1..10, 3): sizes 4, 3, 3, with the bigger chunk first'\nassert chunks('abcdefg', 4) == [['a', 'b'], ['c', 'd'], ['e', 'f'], ['g']], 'Any iterable works; sizes differ by at most one'"},
        {"name": "never an empty chunk", "check": "assert chunks([1, 2], 5) == [[1], [2]], 'With more workers than items, each item gets its own chunk (no empty chunks)'\nassert chunks([], 3) == [], 'Nothing to split gives []'"},
        {"name": "workers must be at least 1", "check": "try:\n    chunks([1, 2, 3], 0)\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('chunks(items, 0) should raise ValueError')"},
        {"name": "parallel_sum uses the pool once", "check": _FAKE + "pool = FakePool()\nassert parallel_sum(range(1, 101), 4, pool) == 5050, 'parallel_sum(1..100) should be 5050'\nassert len(pool.calls) == 1, 'Call executor.map exactly once'\nfn, jobs = pool.calls[0]\nassert jobs == chunks(range(1, 101), 4), 'Hand executor.map the chunks, one job per worker'\nassert fn is sum, 'Each worker sums its own chunk with the built-in sum'"},
        {"name": "parallel_sum with one worker and none to do", "check": _FAKE + "pool = FakePool()\nassert parallel_sum([7, 8], 1, pool) == 15, 'One worker gets one chunk'\npool2 = FakePool()\nassert parallel_sum([], 3, pool2) == 0, 'An empty list sums to 0'"},
    ],
}
BAD["A14.3a"] = [
    SOLUTIONS["A14.3a"].replace("end = start + size + (1 if k < extra else 0)", "end = start + size + (1 if k >= n - extra else 0)"),   # small chunks first
    SOLUTIONS["A14.3a"].replace("    n = min(workers, len(items))\n    if n == 0:\n        return []\n", "    n = workers\n"),  # empty chunks
    SOLUTIONS["A14.3a"].replace("    return sum(executor.map(sum, chunks(numbers, workers)))", "    return sum(numbers)"),
    SOLUTIONS["A14.3a"].replace('''    if workers < 1:
        raise ValueError("workers must be at least 1")
''', '''    workers = max(workers, 1)
'''),
]

# ------------------------------------------------------------------ A14.4a  dependency names from pyproject.toml
SOLUTIONS["A14.4a"] = '''import re
import tomllib

NAME = re.compile(r"^\\s*([A-Za-z0-9][A-Za-z0-9._-]*)")


def normalize(name):
    """PEP 503: lower case, and every run of -, _ and . becomes one -."""
    return re.sub(r"[-_.]+", "-", name).lower()


def dependency_names(toml_text, extras=False):
    """Return the sorted, normalised names of a project's dependencies."""
    data = tomllib.loads(toml_text)
    project = data.get("project", {})
    reqs = list(project.get("dependencies", []))
    if extras:
        for group in project.get("optional-dependencies", {}).values():
            reqs.extend(group)
    names = set()
    for req in reqs:
        m = NAME.match(req)
        if m:
            names.add(normalize(m.group(1)))
    return sorted(names)
'''
_TOML = '''TOML = """
[project]
name = "shiftboard"
version = "0.3.0"
requires-python = ">=3.11"
dependencies = [
    "Requests[socks]>=2.31",
    "typing_extensions; python_version < '3.11'",
    "Django.REST-framework~=3.15",
    "mypkg @ git+https://example.com/mypkg.git",
    "requests>=2.0",
]

[project.optional-dependencies]
test = ["pytest>=8", "pytest-cov"]
docs = ["Sphinx", "furo"]
"""
'''
SPECS["A14.4a"] = {
    "main": False,
    "starter": "import re\nimport tomllib\n\n\ndef normalize(name):\n    \"\"\"PEP 503: lower case, and every run of -, _ and . becomes one -.\"\"\"\n    pass\n\n\ndef dependency_names(toml_text, extras=False):\n    \"\"\"Return the sorted, normalised names of a project's dependencies.\"\"\"\n    pass\n",
    "cases": [
        {"name": "normalize follows PEP 503", "check": "assert normalize('Django.REST-framework') == 'django-rest-framework', 'normalize(\"Django.REST-framework\") should be \"django-rest-framework\"'\nassert normalize('typing_extensions') == 'typing-extensions', 'Underscores become -'\nassert normalize('a__b--c..d') == 'a-b-c-d', 'A run of separators becomes a single -'"},
        {"name": "names without versions, extras or markers", "check": _TOML + "assert dependency_names(TOML) == ['django-rest-framework', 'mypkg', 'requests', 'typing-extensions'], 'Expected the four normalised names, sorted, each once; got ' + repr(dependency_names(TOML))"},
        {"name": "optional dependencies only when asked", "check": _TOML + "got = dependency_names(TOML, extras=True)\nassert got == ['django-rest-framework', 'furo', 'mypkg', 'pytest', 'pytest-cov', 'requests', 'sphinx', 'typing-extensions'], 'extras=True adds every optional group; got ' + repr(got)"},
        {"name": "projects without dependencies", "check": "assert dependency_names('[project]\\nname = \"x\"\\n') == [], 'No dependencies key gives []'\nassert dependency_names('[tool.ruff]\\nline-length = 100\\n') == [], 'No [project] table gives []'"},
        {"name": "invalid TOML raises ValueError", "check": "try:\n    dependency_names('[project\\nname = ')\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('Invalid TOML should raise an error (tomllib.TOMLDecodeError is a ValueError)')"},
    ],
}
BAD["A14.4a"] = [
    SOLUTIONS["A14.4a"].replace('re.sub(r"[-_.]+", "-", name).lower()', 're.sub(r"[-_]+", "-", name).lower()'),
    SOLUTIONS["A14.4a"].replace("    if extras:\n        for group", "    if True:\n        for group"),
    SOLUTIONS["A14.4a"].replace("    names = set()\n", "    names = []\n").replace("names.add(normalize(m.group(1)))", "names.append(normalize(m.group(1)))"),
    SOLUTIONS["A14.4a"].replace("        m = NAME.match(req)\n        if m:\n            names.add(normalize(m.group(1)))", "        names.add(normalize(req.split('>')[0].split('=')[0].split('~')[0].strip()))"),
]

# ------------------------------------------------------------------ A14.5a  docstring checker
SOLUTIONS["A14.5a"] = '''import ast
import re


def _params(fn):
    a = fn.args
    names = [p.arg for p in a.posonlyargs + a.args]
    if a.vararg:
        names.append(a.vararg.arg)
    names += [p.arg for p in a.kwonlyargs]
    if a.kwarg:
        names.append(a.kwarg.arg)
    return [n for n in names if n not in ("self", "cls")]


def _check(fn, qualname, problems):
    doc = ast.get_docstring(fn)
    if doc is None:
        problems.append((fn.lineno, f"{qualname}: missing docstring"))
        return
    if isinstance(fn, ast.ClassDef):
        return
    for p in _params(fn):
        if not re.search(rf"\\b{re.escape(p)}\\b", doc):
            problems.append((fn.lineno, f"{qualname}: parameter {p} not documented"))


def doc_report(source):
    """Return the documentation problems in source, in line order."""
    problems = []
    funcs = (ast.FunctionDef, ast.AsyncFunctionDef)
    for node in ast.parse(source).body:
        if isinstance(node, funcs + (ast.ClassDef,)) and not node.name.startswith("_"):
            _check(node, node.name, problems)
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, funcs) and not item.name.startswith("_"):
                        _check(item, f"{node.name}.{item.name}", problems)
    return [msg for _, msg in sorted(problems, key=lambda p: p[0])]
'''
SPECS["A14.5a"] = {
    "main": False,
    "starter": "import ast\nimport re\n\n\ndef doc_report(source):\n    \"\"\"Return the documentation problems in source, in line order.\"\"\"\n    return []\n",
    "cases": [
        {"name": "missing docstrings", "check": "src = 'def total(prices):\\n    return sum(prices)\\n\\nclass Cart:\\n    pass\\n'\nassert doc_report(src) == ['total: missing docstring', 'Cart: missing docstring'], 'A public function and a public class without docstrings; got ' + repr(doc_report(src))"},
        {"name": "fully documented code is clean", "check": "src = 'def total(prices, tax=0.0):\\n    \"\"\"Add up prices.\\n\\n    Args:\\n        prices: amounts in cents.\\n        tax: rate to add.\\n    \"\"\"\\n    return sum(prices)\\n'\nassert doc_report(src) == [], 'Every parameter is named in the docstring, so there is nothing to report'"},
        {"name": "undocumented parameters", "check": "src = 'def move(shift, *, hours, **opts):\\n    \"\"\"Move it by some hours.\"\"\"\\n'\nassert doc_report(src) == ['move: parameter shift not documented', 'move: parameter opts not documented'], 'hours appears in the docstring but shift and opts do not (report them in parameter order); got ' + repr(doc_report(src))"},
        {"name": "whole words only", "check": "src = 'def repeat(n, text):\\n    \"\"\"Return the text a number of times.\"\"\"\\n'\nassert doc_report(src) == ['repeat: parameter n not documented'], 'The n inside \"number\" does not count: match whole words'"},
        {"name": "methods, self and private names", "check": "src = '''class Board:\\n    \"\"\"Shift board.\"\"\"\\n\\n    def __init__(self, name):\\n        self.name = name\\n\\n    def add(self, shift):\\n        \"\"\"Add one shift.\"\"\"\\n\\n    def _tidy(self):\\n        pass\\n\\n    async def sync(self, url):\\n        pass\\n\\ndef _helper(x):\\n    pass\\n'''\nassert doc_report(src) == ['Board.sync: missing docstring'], 'Check public methods (Class.method), skip self, dunder and private names; got ' + repr(doc_report(src))"},
        {"name": "nested functions are not reported", "check": "src = 'def outer():\\n    \"\"\"Do it.\"\"\"\\n    def inner(y):\\n        return y\\n    return inner\\n'\nassert doc_report(src) == [], 'Only top-level functions and classes, and methods of top-level classes, are checked'"},
    ],
}
BAD["A14.5a"] = [
    SOLUTIONS["A14.5a"].replace('if isinstance(node, funcs + (ast.ClassDef,)) and not node.name.startswith("_"):', 'if isinstance(node, funcs + (ast.ClassDef,)):'),
    SOLUTIONS["A14.5a"].replace('if not re.search(rf"\\b{re.escape(p)}\\b", doc):', 'if p not in doc:'),
    SOLUTIONS["A14.5a"].replace('    return [n for n in names if n not in ("self", "cls")]', '    return names'),
    SOLUTIONS["A14.5a"].replace("    if a.kwarg:\n        names.append(a.kwarg.arg)\n", ""),
    SOLUTIONS["A14.5a"].replace("    funcs = (ast.FunctionDef, ast.AsyncFunctionDef)", "    funcs = (ast.FunctionDef,)"),
]

# ------------------------------------------------------------------ A14.6a  Django-style URL routes
SOLUTIONS["A14.6a"] = '''import re

CONVERTERS = {
    "str": (r"[^/]+", str),
    "int": (r"[0-9]+", int),
    "slug": (r"[-a-zA-Z0-9_]+", str),
    "path": (r".+", str),
}
PART = re.compile(r"<(?:(?P<conv>[a-z]+):)?(?P<name>[A-Za-z_][A-Za-z0-9_]*)>")


def compile_route(route):
    """Turn a route like 'articles/<int:year>/' into a regex and the converters it uses."""
    regex, conv, pos = "^", {}, 0
    for m in PART.finditer(route):
        kind = m["conv"] or "str"
        if kind not in CONVERTERS:
            raise ValueError(f"unknown converter {kind!r} in {route!r}")
        regex += re.escape(route[pos:m.start()]) + f"(?P<{m['name']}>{CONVERTERS[kind][0]})"
        conv[m["name"]] = CONVERTERS[kind][1]
        pos = m.end()
    return re.compile(regex + re.escape(route[pos:]) + "$"), conv


def resolve(patterns, path):
    """Return (view_name, kwargs) for the first route that matches path, or None."""
    if path.startswith("/"):
        path = path[1:]
    for route, name in patterns:
        regex, conv = compile_route(route)
        m = regex.match(path)
        if m:
            return name, {k: conv[k](v) for k, v in m.groupdict().items()}
    return None
'''
_ROUTES = '''ROUTES = [
    ("", "home"),
    ("articles/<int:year>/", "year_archive"),
    ("articles/<int:year>/<slug:title>/", "article"),
    ("users/<name>/", "profile"),
    ("files/<path:rest>", "file"),
]
'''
SPECS["A14.6a"] = {
    "main": False,
    "starter": "import re\n\n\ndef resolve(patterns, path):\n    \"\"\"Return (view_name, kwargs) for the first route that matches path, or None.\"\"\"\n    return None\n",
    "cases": [
        {"name": "plain routes and the leading slash", "check": _ROUTES + "assert resolve(ROUTES, '') == ('home', {}), 'The empty route matches the empty path'\nassert resolve(ROUTES, '/') == ('home', {}), 'One leading / is ignored'"},
        {"name": "int converts to a number", "check": _ROUTES + "got = resolve(ROUTES, 'articles/2024/')\nassert got == ('year_archive', {'year': 2024}), 'articles/2024/ gives year_archive with year as the int 2024; got ' + repr(got)\nassert resolve(ROUTES, 'articles/twenty/') is None, 'int only matches digits'"},
        {"name": "slug and several converters", "check": _ROUTES + "got = resolve(ROUTES, '/articles/2024/tip-split_v2/')\nassert got == ('article', {'year': 2024, 'title': 'tip-split_v2'}), 'Expected article with year 2024 and title tip-split_v2; got ' + repr(got)\nassert resolve(ROUTES, 'articles/2024/tip split/') is None, 'A slug has no spaces'"},
        {"name": "str stops at a slash, path does not", "check": _ROUTES + "assert resolve(ROUTES, 'users/ada/') == ('profile', {'name': 'ada'}), '<name> with no converter is a str'\nassert resolve(ROUTES, 'users/ada/extra/') is None, 'str never matches a /'\nassert resolve(ROUTES, 'files/docs/2024/plan.pdf') == ('file', {'rest': 'docs/2024/plan.pdf'}), 'path matches the rest, slashes included'"},
        {"name": "the whole path must match", "check": _ROUTES + "assert resolve(ROUTES, 'articles/2024') is None, 'The trailing / in the route is required'\nassert resolve(ROUTES, 'articles/2024/x/y/') is None, 'Extra text after a route means no match'\nassert resolve(ROUTES, 'nope/') is None, 'No route gives None'"},
        {"name": "first match wins", "check": "routes = [('items/<int:n>/', 'by_number'), ('items/<slug:s>/', 'by_slug')]\nassert resolve(routes, 'items/7/') == ('by_number', {'n': 7}), 'Routes are tried in order: the int route comes first'\nassert resolve(routes, 'items/seven/') == ('by_slug', {'s': 'seven'}), 'If the first does not match, try the next'"},
        {"name": "unknown converters are an error", "check": "try:\n    resolve([('x/<float:v>/', 'x')], 'x/1.5/')\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('An unknown converter like <float:v> raises ValueError')"},
    ],
}
BAD["A14.6a"] = [
    SOLUTIONS["A14.6a"].replace('    "int": (r"[0-9]+", int),', '    "int": (r"[0-9]+", str),'),
    SOLUTIONS["A14.6a"].replace('return re.compile(regex + re.escape(route[pos:]) + "$"), conv', 'return re.compile(regex + re.escape(route[pos:])), conv'),
    SOLUTIONS["A14.6a"].replace('    "str": (r"[^/]+", str),', '    "str": (r".+", str),'),
    SOLUTIONS["A14.6a"].replace("    for route, name in patterns:", "    for route, name in reversed(patterns):"),
    SOLUTIONS["A14.6a"].replace('''        if kind not in CONVERTERS:
            raise ValueError(f"unknown converter {kind!r} in {route!r}")
''', '''        if kind not in CONVERTERS:
            kind = "str"
'''),
]

# ------------------------------------------------------------------ A14.7a  safe HTML and SQL with t-strings (Python 3.14)
SOLUTIONS["A14.7a"] = '''from html import escape
from string.templatelib import Interpolation, Template


def _convert(part):
    """Apply !r, !s or !a and the format spec, the way an f-string would."""
    value = part.value
    if part.conversion == "r":
        value = repr(value)
    elif part.conversion == "s":
        value = str(value)
    elif part.conversion == "a":
        value = ascii(value)
    return format(value, part.format_spec)


def html(template):
    """Render a t-string as HTML, escaping every interpolated value."""
    if not isinstance(template, Template):
        raise TypeError("html() needs a t-string such as t\\"<p>{name}</p>\\", not a str")
    out = []
    for part in template:
        if isinstance(part, str):
            out.append(part)
        elif isinstance(part.value, Template):
            out.append(html(part.value))        # a nested template is already safe HTML
        else:
            out.append(escape(_convert(part), quote=True))
    return "".join(out)


def sql(template):
    """Turn a t-string into a query with ? placeholders and a list of parameters."""
    if not isinstance(template, Template):
        raise TypeError("sql() needs a t-string such as t\\"SELECT * FROM t WHERE id = {id}\\", not a str")
    query, params = [], []
    for part in template:
        if isinstance(part, str):
            query.append(part)
        elif isinstance(part.value, Template):
            q, p = sql(part.value)
            query.append(q)
            params.extend(p)
        else:
            query.append("?")
            params.append(part.value)
    return "".join(query), params


if __name__ == "__main__":
    name = "<script>alert(1)</script>"
    print(html(t"<p>Hello {name}!</p>"))
    print(sql(t"SELECT * FROM staff WHERE name = {name}"))
'''
SPECS["A14.7a"] = {
    "main": False,
    "starter": "from html import escape\nfrom string.templatelib import Interpolation, Template\n\n\ndef html(template):\n    \"\"\"Render a t-string as HTML, escaping every interpolated value.\"\"\"\n    pass\n\n\ndef sql(template):\n    \"\"\"Turn a t-string into a query with ? placeholders and a list of parameters.\"\"\"\n    pass\n",
    "cases": [
        {"name": "html escapes values, not the markup", "check": "name = '<script>alert(\"x\")</script>'\ngot = html(t'<p class=\"greet\">Hi {name}!</p>')\nassert got == '<p class=\"greet\">Hi &lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;!</p>', 'Escape the interpolated value with html.escape(..., quote=True) and keep the template text as it is; got ' + repr(got)"},
        {"name": "html applies conversions and format specs", "check": "price, item = 1234.5, \"Tom's tea\"\ngot = html(t'<td>{item!r}</td><td>{price:,.2f}</td>')\nassert got == '<td>&quot;Tom&#x27;s tea&quot;</td><td>1,234.50</td>', 'Apply !r and :,.2f as an f-string would, then escape; got ' + repr(got)\nassert html(t'{3}') == '3' and html(t'') == '', 'Numbers become text; an empty template gives an empty string'"},
        {"name": "nested templates are not escaped twice", "check": "user = 'Ada & Grace'\nrow = t'<li>{user}</li>'\ngot = html(t'<ul>{row}</ul>')\nassert got == '<ul><li>Ada &amp; Grace</li></ul>', 'A Template inside a template is rendered with html() itself, so its tags stay tags and its values are escaped once; got ' + repr(got)"},
        {"name": "html refuses plain strings", "check": "name = 'x'\ntry:\n    html(f'<p>{name}</p>')\nexcept TypeError:\n    pass\nelse:\n    raise AssertionError('html() must raise TypeError for a str: an f-string has already lost the difference between markup and values')"},
        {"name": "sql uses placeholders", "check": "name, min_hours = \"O'Brien\", 20\ngot = sql(t'SELECT * FROM staff WHERE name = {name} AND hours >= {min_hours}')\nassert got == ('SELECT * FROM staff WHERE name = ? AND hours >= ?', [\"O'Brien\", 20]), 'Each value becomes ? and goes into the parameter list, in order; got ' + repr(got)\nassert sql(t'SELECT 1') == ('SELECT 1', []), 'No values: no parameters'"},
        {"name": "sql works with sqlite3 and nested templates", "check": "import sqlite3\ndb = sqlite3.connect(':memory:')\ndb.execute('CREATE TABLE staff (name TEXT, hours INT)')\ndb.executemany('INSERT INTO staff VALUES (?, ?)', [('Ada', 30), (\"Robert'); DROP TABLE staff;--\", 5)])\nevil = \"Robert'); DROP TABLE staff;--\"\nwhere = t'name = {evil}'\nq, p = sql(t'SELECT hours FROM staff WHERE {where}')\nassert (q, p) == ('SELECT hours FROM staff WHERE name = ?', [evil]), 'A nested template adds its own text and parameters; got ' + repr((q, p))\nassert db.execute(q, p).fetchall() == [(5,)], 'The query runs safely and finds the row'\nassert db.execute('SELECT COUNT(*) FROM staff').fetchone()[0] == 2, 'The table is still there'"},
        {"name": "sql refuses plain strings", "check": "try:\n    sql('SELECT * FROM staff')\nexcept TypeError:\n    pass\nelse:\n    raise AssertionError('sql() must raise TypeError for a str')"},
    ],
}
BAD["A14.7a"] = [
    SOLUTIONS["A14.7a"].replace("out.append(escape(_convert(part), quote=True))", "out.append(_convert(part))"),
    SOLUTIONS["A14.7a"].replace("            out.append(html(part.value))        # a nested template is already safe HTML\n", "            out.append(escape(html(part.value)))\n"),
    SOLUTIONS["A14.7a"].replace('''    if not isinstance(template, Template):
        raise TypeError("html() needs''', '''    if isinstance(template, str):
        return template
    if not isinstance(template, Template):
        raise TypeError("html() needs'''),
    SOLUTIONS["A14.7a"].replace('''            query.append("?")
            params.append(part.value)''', '''            query.append(repr(part.value))'''),
    SOLUTIONS["A14.7a"].replace("    return format(value, part.format_spec)", "    return str(part.value)"),
    SOLUTIONS["A14.7a"].replace('''            q, p = sql(part.value)
            query.append(q)
            params.extend(p)''', '''            query.append("?")
            params.append(part.value)'''),
]
