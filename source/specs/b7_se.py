"""Autograder specs for module A15, Software engineering practice (Python Course, Track 2)."""
SOLUTIONS = {}
SPECS = {}
BAD = {}

# ------------------------------------------------------------------ A15.1a  joins, grouping and a transaction
SOLUTIONS["A15.1a"] = '''def top_customers(conn, n):
    """Return (name, order_count, total_cents) for the n biggest spenders, biggest first."""
    return conn.execute(
        """
        SELECT c.name, COUNT(o.id), COALESCE(SUM(o.total_cents), 0) AS spent
        FROM customers AS c
        LEFT JOIN orders AS o ON o.customer_id = c.id
        GROUP BY c.id
        ORDER BY spent DESC, c.name
        LIMIT ?
        """,
        (n,),
    ).fetchall()


def transfer(conn, src, dst, cents):
    """Move cents between two accounts, all or nothing."""
    if cents <= 0:
        raise ValueError("cents must be positive")
    with conn:   # commits at the end, rolls back if anything raises
        row = conn.execute("SELECT balance FROM accounts WHERE id = ?", (src,)).fetchone()
        if row is None or conn.execute("SELECT 1 FROM accounts WHERE id = ?", (dst,)).fetchone() is None:
            raise LookupError("no such account")
        if row[0] < cents:
            raise ValueError("not enough money")
        conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (cents, src))
        conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (cents, dst))
'''
_DB = '''import sqlite3
conn = sqlite3.connect(":memory:")
conn.executescript("""
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, total_cents INTEGER);
CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance INTEGER);
INSERT INTO customers VALUES (1, 'Ada'), (2, 'Grace'), (3, 'Linus'), (4, 'Zed');
INSERT INTO orders VALUES (1, 1, 500), (2, 1, 700), (3, 2, 2000), (4, 3, 1200);
INSERT INTO accounts VALUES (1, 1000), (2, 50);
""")
conn.commit()
'''
SPECS["A15.1a"] = {
    "main": False,
    "starter": "def top_customers(conn, n):\n    \"\"\"Return (name, order_count, total_cents) for the n biggest spenders, biggest first.\"\"\"\n    pass\n\n\ndef transfer(conn, src, dst, cents):\n    \"\"\"Move cents between two accounts, all or nothing.\"\"\"\n    pass\n",
    "cases": [
        {"name": "top spenders, biggest first", "check": _DB + "got = [tuple(r) for r in top_customers(conn, 2)]\nassert got == [('Grace', 1, 2000), ('Ada', 2, 1200)], 'Expected Grace (1 order, 2000) then Ada (2 orders, 1200); got ' + repr(got)"},
        {"name": "ties go by name, and customers without orders count", "check": _DB + "got = [tuple(r) for r in top_customers(conn, 10)]\nassert got == [('Grace', 1, 2000), ('Ada', 2, 1200), ('Linus', 1, 1200), ('Zed', 0, 0)], 'Ada and Linus tie on 1200, so the name decides; Zed has no orders and shows 0 and 0 (use a LEFT JOIN); got ' + repr(got)"},
        {"name": "transfer moves the money", "check": _DB + "transfer(conn, 1, 2, 300)\nassert conn.execute('SELECT balance FROM accounts ORDER BY id').fetchall() == [(700,), (350,)], 'After moving 300 the balances should be 700 and 350'"},
        {"name": "not enough money changes nothing", "check": _DB + "try:\n    transfer(conn, 2, 1, 80)\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('Moving more than the balance raises ValueError')\nassert conn.execute('SELECT balance FROM accounts ORDER BY id').fetchall() == [(1000,), (50,)], 'A failed transfer must leave both balances as they were'"},
        {"name": "unknown account and bad amount", "check": _DB + "for args, exc in (((1, 99, 10), LookupError), ((99, 1, 10), LookupError), ((1, 2, 0), ValueError), ((1, 2, -5), ValueError)):\n    try:\n        transfer(conn, *args)\n    except exc:\n        pass\n    else:\n        raise AssertionError(f'transfer{args} should raise {exc.__name__}')\nconn.rollback()\nassert conn.execute('SELECT balance FROM accounts ORDER BY id').fetchall() == [(1000,), (50,)], 'Nothing may change when a transfer is refused (check both accounts before updating)'"},
        {"name": "values are passed as parameters", "static": True, "check": "import re\nassert not re.search(r'execute\\(\\s*f[\\'\\\"]', code) and '.format(' not in code and '%s' not in code, 'Pass values with ? placeholders and a tuple, never by building the SQL string'"},
    ],
}
BAD["A15.1a"] = [
    SOLUTIONS["A15.1a"].replace("LEFT JOIN orders", "JOIN orders"),
    SOLUTIONS["A15.1a"].replace("ORDER BY spent DESC, c.name", "ORDER BY spent DESC, c.id DESC"),
    SOLUTIONS["A15.1a"].replace('''        if row[0] < cents:
            raise ValueError("not enough money")
        conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (cents, src))''', '''        conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (cents, src))
        conn.commit()
        if row[0] < cents:
            raise ValueError("not enough money")'''),
    SOLUTIONS["A15.1a"].replace(''' or conn.execute("SELECT 1 FROM accounts WHERE id = ?", (dst,)).fetchone() is None''', ""),
    SOLUTIONS["A15.1a"].replace('''    if cents <= 0:
        raise ValueError("cents must be positive")
''', ""),
]

# ------------------------------------------------------------------ A15.2a  password hashes and signed tokens
SOLUTIONS["A15.2a"] = '''import base64
import hashlib
import hmac
import json
import os


def hash_password(password, salt=None):
    """Return 'salt_hex$hash_hex' using PBKDF2-HMAC-SHA256 with 100,000 rounds."""
    salt = salt if salt is not None else os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return salt.hex() + "$" + digest.hex()


def verify_password(password, stored):
    """True when password matches a value made by hash_password."""
    try:
        salt_hex, digest_hex = stored.split("$")
        salt = bytes.fromhex(salt_hex)
    except ValueError:
        return False
    return hmac.compare_digest(hash_password(password, salt), stored)


def _b64(data):
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def _sign(body, secret):
    return _b64(hmac.new(secret.encode(), body.encode(), hashlib.sha256).digest())


def make_token(payload, secret, now, ttl=3600):
    """Return 'body.signature': the payload plus an expiry time, signed with the secret."""
    body = _b64(json.dumps({**payload, "exp": now + ttl}, sort_keys=True).encode())
    return body + "." + _sign(body, secret)


def read_token(token, secret, now):
    """Return the payload of a valid, unexpired token; raise ValueError otherwise."""
    try:
        body, signature = token.split(".")
    except ValueError:
        raise ValueError("malformed token") from None
    if not hmac.compare_digest(signature, _sign(body, secret)):
        raise ValueError("bad signature")
    payload = json.loads(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)))
    if now >= payload["exp"]:
        raise ValueError("token expired")
    return payload
'''
SPECS["A15.2a"] = {
    "main": False,
    "starter": "import base64\nimport hashlib\nimport hmac\nimport json\nimport os\n\n\ndef hash_password(password, salt=None):\n    \"\"\"Return 'salt_hex$hash_hex' using PBKDF2-HMAC-SHA256 with 100,000 rounds.\"\"\"\n    pass\n\n\ndef verify_password(password, stored):\n    \"\"\"True when password matches a value made by hash_password.\"\"\"\n    pass\n\n\ndef make_token(payload, secret, now, ttl=3600):\n    \"\"\"Return 'body.signature': the payload plus an expiry time, signed with the secret.\"\"\"\n    pass\n\n\ndef read_token(token, secret, now):\n    \"\"\"Return the payload of a valid, unexpired token; raise ValueError otherwise.\"\"\"\n    pass\n",
    "cases": [
        {"name": "hash format and a known value", "check": "import hashlib\nh = hash_password('tea-time', bytes(range(16)))\nsalt, _, digest = h.partition('$')\nassert salt == bytes(range(16)).hex(), 'The part before $ is the salt in hex'\nassert digest == hashlib.pbkdf2_hmac('sha256', b'tea-time', bytes(range(16)), 100_000).hex(), 'The part after $ is PBKDF2-HMAC-SHA256 of the password with that salt and 100,000 rounds, in hex'"},
        {"name": "every hash gets its own salt", "check": "a, b = hash_password('same'), hash_password('same')\nassert a != b, 'Without a salt argument, use 16 fresh random bytes (os.urandom) so equal passwords hash differently'\nassert len(a.split('$')[0]) == 32, 'The random salt is 16 bytes (32 hex characters)'\nassert 'same' not in a, 'Never store the password itself'"},
        {"name": "verify_password", "check": "stored = hash_password('correct horse')\nassert verify_password('correct horse', stored) is True, 'The right password verifies'\nassert verify_password('Correct horse', stored) is False, 'A wrong password does not'\nassert verify_password('x', 'not-a-hash') is False and verify_password('x', 'zz$zz') is False, 'A malformed stored value gives False, not an error'"},
        {"name": "token round trip", "check": "t = make_token({'user': 'ada', 'role': 'lead'}, 's3cret', now=1000, ttl=60)\nassert t.count('.') == 1, 'A token is body.signature'\nassert read_token(t, 's3cret', now=1030) == {'user': 'ada', 'role': 'lead', 'exp': 1060}, 'read_token returns the payload with exp = now + ttl'\nassert make_token({'a': 1}, 'k', 5) == make_token({'a': 1}, 'k', 5), 'The same input gives the same token'"},
        {"name": "tampering is detected", "check": "import base64, json\nt = make_token({'user': 'ada', 'admin': False}, 's3cret', now=1000)\nbody, sig = t.split('.')\nforged = base64.urlsafe_b64encode(json.dumps({'user': 'ada', 'admin': True, 'exp': 99999}).encode()).decode().rstrip('=')\nfor bad in (forged + '.' + sig, body + '.' + sig[:-2] + 'AA', t + 'x', 'nonsense', body):\n    try:\n        read_token(bad, 's3cret', now=1001)\n    except ValueError:\n        pass\n    else:\n        raise AssertionError('A changed or malformed token must raise ValueError: ' + bad[:30])\ntry:\n    read_token(t, 'other-secret', now=1001)\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('A token signed with a different secret must be refused')"},
        {"name": "tokens expire", "check": "t = make_token({'user': 'ada'}, 'k', now=1000, ttl=60)\nassert read_token(t, 'k', now=1059)['user'] == 'ada', 'One second before the expiry the token is still good'\nfor late in (1060, 5000):\n    try:\n        read_token(t, 'k', now=late)\n    except ValueError:\n        pass\n    else:\n        raise AssertionError(f'At now={late} the token (exp 1060) has expired')"},
        {"name": "constant-time comparison", "static": True, "check": "assert 'compare_digest' in code, 'Compare hashes and signatures with hmac.compare_digest, which takes the same time wherever the first difference is'"},
    ],
}
BAD["A15.2a"] = [
    SOLUTIONS["A15.2a"].replace("salt = salt if salt is not None else os.urandom(16)", "salt = salt if salt is not None else b'0123456789abcdef'"),
    SOLUTIONS["A15.2a"].replace('''    if not hmac.compare_digest(signature, _sign(body, secret)):
        raise ValueError("bad signature")
''', ""),
    SOLUTIONS["A15.2a"].replace('''    if now >= payload["exp"]:''', '''    if now > payload["exp"]:'''),
    SOLUTIONS["A15.2a"].replace('''    except ValueError:
        return False
    return hmac''', '''    except KeyError:
        return False
    return hmac'''),
    SOLUTIONS["A15.2a"].replace('hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)', 'hashlib.sha256(salt + password.encode()).digest()'),
]

# ------------------------------------------------------------------ A15.3a  bisecting to the first bad version
SOLUTIONS["A15.3a"] = '''def first_bad(versions, is_bad):
    """Return the first version for which is_bad(version) is True, or None.

    versions go from oldest to newest; once one is bad, every later one is bad too.
    """
    lo, hi = 0, len(versions)
    while lo < hi:
        mid = (lo + hi) // 2
        if is_bad(versions[mid]):
            hi = mid
        else:
            lo = mid + 1
    return versions[lo] if lo < len(versions) else None
'''
_CNT = '''class Probe:
    def __init__(self, first):
        self.first, self.calls = first, []
    def __call__(self, v):
        self.calls.append(v)
        return v >= self.first
'''
SPECS["A15.3a"] = {
    "main": False,
    "starter": "def first_bad(versions, is_bad):\n    \"\"\"Return the first version for which is_bad(version) is True, or None.\n\n    versions go from oldest to newest; once one is bad, every later one is bad too.\n    \"\"\"\n    pass\n",
    "cases": [
        {"name": "finds the first bad version", "check": "versions = ['v1', 'v2', 'v3', 'v4', 'v5', 'v6']\nassert first_bad(versions, lambda v: v >= 'v4') == 'v4', 'With v4, v5 and v6 bad, the first bad one is v4'\nassert first_bad(versions, lambda v: True) == 'v1', 'If everything is bad, the first version is the answer'\nassert first_bad(versions, lambda v: v == 'v6') == 'v6', 'Only the newest is bad'"},
        {"name": "nothing bad, nothing to check", "check": "assert first_bad([1, 2, 3], lambda v: False) is None, 'No bad version gives None'\nassert first_bad([], lambda v: True) is None, 'An empty list gives None'"},
        {"name": "every position works", "check": "for n in range(1, 40):\n    for k in range(n + 1):\n        got = first_bad(list(range(n)), lambda v: v >= k)\n        assert got == (k if k < n else None), f'{n} versions with the first bad one at index {k}: got {got!r}'"},
        {"name": "asks about few versions", "check": _CNT + "p = Probe(700_000)\nassert first_bad(range(1_000_000), p) == 700_000, 'A million versions, first bad one is 700000'\nassert len(p.calls) <= 20, f'is_bad was called {len(p.calls)} times; halving the range needs at most 20 for a million versions'\nassert len(set(p.calls)) == len(p.calls), 'Never test the same version twice'"},
    ],
}
BAD["A15.3a"] = [
    '''def first_bad(versions, is_bad):
    for v in versions:
        if is_bad(v):
            return v
    return None
''',
    SOLUTIONS["A15.3a"].replace("return versions[lo] if lo < len(versions) else None", "return versions[lo - 1] if lo else None"),
    SOLUTIONS["A15.3a"].replace("lo, hi = 0, len(versions)", "lo, hi = 0, len(versions) - 1"),
    SOLUTIONS["A15.3a"].replace("            hi = mid\n", "            hi = mid\n            if mid and not is_bad(versions[mid - 1]):\n                return versions[mid]\n"),
]

# ------------------------------------------------------------------ A15.4a  configuration from the environment
SOLUTIONS["A15.4a"] = '''from dataclasses import dataclass


class ConfigError(Exception):
    """Raised with every problem found, one per line."""

    def __init__(self, problems):
        super().__init__("\\n".join(problems))
        self.problems = problems


@dataclass(frozen=True)
class Config:
    database_url: str
    port: int = 8000
    debug: bool = False
    workers: int = 2


TRUE, FALSE = {"1", "true", "yes", "on"}, {"0", "false", "no", "off"}


def load_config(env):
    """Build a Config from a mapping of environment variables, reporting every problem at once."""
    problems, values = [], {}
    url = env.get("DATABASE_URL", "").strip()
    if not url:
        problems.append("DATABASE_URL is required")
    values["database_url"] = url
    for key, low, high in (("PORT", 1, 65535), ("WORKERS", 1, 64)):
        if key in env:
            try:
                number = int(env[key])
            except ValueError:
                problems.append(f"{key} must be a whole number, got {env[key]!r}")
                continue
            if not low <= number <= high:
                problems.append(f"{key} must be between {low} and {high}, got {number}")
            values[key.lower()] = number
    if "DEBUG" in env:
        text = env["DEBUG"].strip().lower()
        if text in TRUE | FALSE:
            values["debug"] = text in TRUE
        else:
            problems.append(f"DEBUG must be true or false, got {env['DEBUG']!r}")
    if problems:
        raise ConfigError(problems)
    return Config(**values)
'''
SPECS["A15.4a"] = {
    "main": False,
    "starter": "from dataclasses import dataclass\n\n\nclass ConfigError(Exception):\n    \"\"\"Raised with every problem found, one per line.\"\"\"\n\n    def __init__(self, problems):\n        super().__init__(\"\\n\".join(problems))\n        self.problems = problems\n\n\n@dataclass(frozen=True)\nclass Config:\n    database_url: str\n    port: int = 8000\n    debug: bool = False\n    workers: int = 2\n\n\ndef load_config(env):\n    \"\"\"Build a Config from a mapping of environment variables, reporting every problem at once.\"\"\"\n    pass\n",
    "cases": [
        {"name": "defaults", "check": "c = load_config({'DATABASE_URL': 'postgres://db/app'})\nassert (c.database_url, c.port, c.debug, c.workers) == ('postgres://db/app', 8000, False, 2), 'Only DATABASE_URL is required; the rest default to port 8000, debug False, workers 2; got ' + repr(c)"},
        {"name": "values are converted", "check": "c = load_config({'DATABASE_URL': ' sqlite:///x.db ', 'PORT': '9090', 'DEBUG': 'Yes', 'WORKERS': '8', 'HOME': '/root'})\nassert c == Config('sqlite:///x.db', 9090, True, 8), 'PORT and WORKERS become ints, DEBUG a bool, the URL is stripped and other variables are ignored; got ' + repr(c)\nassert load_config({'DATABASE_URL': 'x', 'DEBUG': 'off'}).debug is False and load_config({'DATABASE_URL': 'x', 'DEBUG': '1'}).debug is True, 'DEBUG accepts 1/true/yes/on and 0/false/no/off in any case'"},
        {"name": "the config cannot be changed", "check": "c = load_config({'DATABASE_URL': 'x'})\ntry:\n    c.port = 1\nexcept Exception:\n    pass\nelse:\n    raise AssertionError('Config is frozen: settings are read once at start-up')"},
        {"name": "every problem is reported at once", "check": "try:\n    load_config({'PORT': 'http', 'DEBUG': 'maybe', 'WORKERS': '0'})\nexcept ConfigError as e:\n    assert e.problems == ['DATABASE_URL is required', \"PORT must be a whole number, got 'http'\", 'WORKERS must be between 1 and 64, got 0', \"DEBUG must be true or false, got 'maybe'\"], 'Expected four problems in this order (URL, PORT, WORKERS, DEBUG); got ' + repr(e.problems)\n    assert str(e).count('\\n') == 3, 'str(error) lists one problem per line'\nelse:\n    raise AssertionError('Bad settings raise ConfigError')"},
        {"name": "ranges and blank values", "check": "c = load_config({'DATABASE_URL': 'x', 'PORT': '65535', 'WORKERS': '64'})\nassert (c.port, c.workers) == (65535, 64), 'The top of each range is allowed: port 65535 and 64 workers'\nfor env, text in (({'DATABASE_URL': 'x', 'PORT': '70000'}, 'PORT must be between 1 and 65535, got 70000'), ({'DATABASE_URL': '   '}, 'DATABASE_URL is required'), ({'DATABASE_URL': 'x', 'WORKERS': '65'}, 'WORKERS must be between 1 and 64, got 65')):\n    try:\n        load_config(env)\n    except ConfigError as e:\n        assert e.problems == [text], f'For {env} expected [{text!r}]; got {e.problems!r}'\n    else:\n        raise AssertionError(f'{env} should raise ConfigError')"},
    ],
}
BAD["A15.4a"] = [
    SOLUTIONS["A15.4a"].replace('''                problems.append(f"{key} must be a whole number, got {env[key]!r}")
                continue''', '''                raise ConfigError([f"{key} must be a whole number, got {env[key]!r}"])'''),
    SOLUTIONS["A15.4a"].replace('url = env.get("DATABASE_URL", "").strip()', 'url = env.get("DATABASE_URL", "")'),
    SOLUTIONS["A15.4a"].replace("        text = env[\"DEBUG\"].strip().lower()", "        text = env[\"DEBUG\"].strip()"),
    SOLUTIONS["A15.4a"].replace("            if not low <= number <= high:", "            if not low <= number < high:"),
    SOLUTIONS["A15.4a"].replace("@dataclass(frozen=True)", "@dataclass"),
]

# ------------------------------------------------------------------ A15.5a  commit message checker
SOLUTIONS["A15.5a"] = '''import re

TYPES = ("feat", "fix", "docs", "test", "refactor", "chore", "perf", "ci")
SUBJECT = re.compile(r"^(?P<type>[a-z]+)(\\((?P<scope>[a-z0-9-]+)\\))?(?P<bang>!)?: (?P<text>.+)$")


def check_commit(message):
    """Return the problems with a commit message, in the order of the rules."""
    problems = []
    lines = message.rstrip("\\n").split("\\n")
    subject = lines[0]
    m = SUBJECT.match(subject)
    if not m:
        problems.append("subject must look like 'type(scope): summary'")
    elif m["type"] not in TYPES:
        problems.append(f"unknown type {m['type']!r}")
    if len(subject) > 72:
        problems.append(f"subject is {len(subject)} characters; keep it to 72")
    text = m["text"] if m else subject
    if text.endswith("."):
        problems.append("subject must not end with a full stop")
    if m and text[:1].isupper():
        problems.append("summary starts with a lower-case letter")
    if len(lines) > 1 and lines[1].strip():
        problems.append("leave the second line blank")
    if m and m["bang"] and not any(l.startswith("BREAKING CHANGE: ") for l in lines[2:]):
        problems.append("a breaking change (!) needs a 'BREAKING CHANGE: ' line in the body")
    return problems
'''
SPECS["A15.5a"] = {
    "main": False,
    "starter": "import re\n\nTYPES = (\"feat\", \"fix\", \"docs\", \"test\", \"refactor\", \"chore\", \"perf\", \"ci\")\n\n\ndef check_commit(message):\n    \"\"\"Return the problems with a commit message, in the order of the rules.\"\"\"\n    return []\n",
    "cases": [
        {"name": "good messages pass", "check": "for msg in ('fix: stop tips being split twice', 'feat(api): add shift swap endpoint\\n\\nStaff can now trade shifts.\\nCloses #42', 'docs(read-me2): explain setup\\n', 'feat!: drop Python 3.9\\n\\nBREAKING CHANGE: needs 3.10 or newer'):\n    assert check_commit(msg) == [], f'{msg!r} follows every rule; got {check_commit(msg)!r}'"},
        {"name": "the subject shape", "check": "want = [\"subject must look like 'type(scope): summary'\"]\nfor msg in ('Fixed the bug', 'fix:no space', 'fix(API): caps scope', 'fix(): empty scope', 'fix: '):\n    assert check_commit(msg) == want, f'{msg!r} does not match type(scope): summary; got {check_commit(msg)!r}'\nassert check_commit('update: bump deps') == [\"unknown type 'update'\"], 'The type must be one of TYPES'"},
        {"name": "length, full stop and capital", "check": "long = 'fix: ' + 'x' * 70\nassert check_commit(long) == ['subject is 75 characters; keep it to 72'], 'A 75-character subject is too long; got ' + repr(check_commit(long))\nassert check_commit('fix: ' + 'x' * 67) == [], '72 characters is allowed'\nassert check_commit('fix: stop the crash.') == ['subject must not end with a full stop'], 'No full stop at the end'\nassert check_commit('fix: Stop the crash') == ['summary starts with a lower-case letter'], 'The summary starts in lower case'"},
        {"name": "blank second line and breaking changes", "check": "assert check_commit('fix: one\\nmore detail') == ['leave the second line blank'], 'The body starts on line 3'\nassert check_commit('feat(api)!: remove v1') == [\"a breaking change (!) needs a 'BREAKING CHANGE: ' line in the body\"], 'A ! needs a BREAKING CHANGE: line'\nassert check_commit('feat!: remove v1\\n\\nbreaking change: v1 is gone') == [\"a breaking change (!) needs a 'BREAKING CHANGE: ' line in the body\"], 'The marker is upper case and starts a line'"},
        {"name": "several problems, in rule order", "check": "got = check_commit('Fixed the login page and the logout page and three other things on the way.\\nalso tests')\nassert got == [\"subject must look like 'type(scope): summary'\", 'subject is 75 characters; keep it to 72', 'subject must not end with a full stop', 'leave the second line blank'], 'Report every broken rule in order; got ' + repr(got)\ngot = check_commit('feature: Add it.')\nassert got == [\"unknown type 'feature'\", 'subject must not end with a full stop', 'summary starts with a lower-case letter'], 'got ' + repr(got)"},
    ],
}
BAD["A15.5a"] = [
    SOLUTIONS["A15.5a"].replace("    if len(subject) > 72:", "    if len(subject) >= 72:"),
    SOLUTIONS["A15.5a"].replace('(?P<scope>[a-z0-9-]+)', '(?P<scope>[^)]*)'),
    SOLUTIONS["A15.5a"].replace("    if len(lines) > 1 and lines[1].strip():", "    if len(lines) > 1 and not lines[1].strip():"),
    SOLUTIONS["A15.5a"].replace('    elif m["type"] not in TYPES:\n        problems.append(f"unknown type {m[\'type\']!r}")\n', ""),
    SOLUTIONS["A15.5a"].replace('any(l.startswith("BREAKING CHANGE: ") for l in lines[2:])', 'any("breaking change" in l.lower() for l in lines[2:])'),
]

# ------------------------------------------------------------------ A15.6a  an LRU cache with expiry
SOLUTIONS["A15.6a"] = '''from collections import OrderedDict


class LRUCache:
    """Keeps at most `capacity` items; drops the least recently used, and items older than ttl."""

    def __init__(self, capacity, ttl=None):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity, self.ttl = capacity, ttl
        self.items = OrderedDict()      # key -> (value, time stored)
        self.hits = self.misses = 0

    def get(self, key, now=0):
        entry = self.items.get(key)
        if entry is not None and self.ttl is not None and now - entry[1] >= self.ttl:
            del self.items[key]
            entry = None
        if entry is None:
            self.misses += 1
            return None
        self.items.move_to_end(key)
        self.hits += 1
        return entry[0]

    def put(self, key, value, now=0):
        self.items[key] = (value, now)
        self.items.move_to_end(key)
        if len(self.items) > self.capacity:
            self.items.popitem(last=False)

    def __len__(self):
        return len(self.items)

    def hit_rate(self):
        total = self.hits + self.misses
        return self.hits / total if total else 0.0
'''
SPECS["A15.6a"] = {
    "main": False,
    "starter": "from collections import OrderedDict\n\n\nclass LRUCache:\n    \"\"\"Keeps at most `capacity` items; drops the least recently used, and items older than ttl.\"\"\"\n\n    def __init__(self, capacity, ttl=None):\n        self.capacity, self.ttl = capacity, ttl\n\n    def get(self, key, now=0):\n        pass\n\n    def put(self, key, value, now=0):\n        pass\n",
    "cases": [
        {"name": "get and put", "check": "c = LRUCache(2)\nassert c.get('a') is None, 'A missing key gives None'\nc.put('a', 1)\nc.put('b', 2)\nassert c.get('a') == 1 and c.get('b') == 2 and len(c) == 2, 'Stored values come back'\nc.put('a', 10)\nassert c.get('a') == 10 and len(c) == 2, 'Putting an existing key replaces its value'"},
        {"name": "the least recently used item is dropped", "check": "c = LRUCache(2)\nc.put('a', 1)\nc.put('b', 2)\nc.get('a')\nc.put('c', 3)\nassert c.get('b') is None, 'b was used least recently (a was read after it), so b is dropped'\nassert c.get('a') == 1 and c.get('c') == 3 and len(c) == 2, 'a and c stay'\nc.put('a', 5)\nc.put('d', 4)\nassert c.get('c') is None and c.get('a') == 5, 'put also counts as using a key'"},
        {"name": "items expire after ttl", "check": "c = LRUCache(5, ttl=10)\nc.put('k', 'v', now=100)\nassert c.get('k', now=109) == 'v', 'Younger than ttl: still there'\nassert c.get('k', now=110) is None and len(c) == 0, 'At now - stored >= ttl the item has expired and is removed'\nc.put('k', 'v2', now=200)\nc.get('k', now=205)\nassert c.get('k', now=210) is None, 'Reading does not restart the clock: expiry counts from when it was put'\nc2 = LRUCache(1)\nc2.put('x', 1, now=0)\nassert c2.get('x', now=10**9) == 1, 'With ttl=None nothing expires'"},
        {"name": "hit rate", "check": "c = LRUCache(2, ttl=5)\nassert c.hit_rate() == 0.0, 'No lookups yet: 0.0'\nc.put('a', 1, now=0)\nc.get('a', now=1)\nc.get('zzz', now=1)\nc.get('a', now=2)\nc.get('a', now=9)\nassert (c.hits, c.misses) == (2, 2), 'Two hits, then a miss for zzz and a miss for the expired a; got ' + repr((c.hits, c.misses))\nassert c.hit_rate() == 0.5, 'hit_rate is hits / lookups'"},
        {"name": "capacity must be positive", "check": "try:\n    LRUCache(0)\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('LRUCache(0) raises ValueError')"},
    ],
}
BAD["A15.6a"] = [
    SOLUTIONS["A15.6a"].replace("        self.items.move_to_end(key)\n        self.hits += 1", "        self.hits += 1"),
    SOLUTIONS["A15.6a"].replace("now - entry[1] >= self.ttl", "now - entry[1] > self.ttl"),
    SOLUTIONS["A15.6a"].replace("            self.items.popitem(last=False)", "            self.items.popitem(last=True)"),
    SOLUTIONS["A15.6a"].replace("        self.items.move_to_end(key)\n        self.hits += 1\n        return entry[0]", "        self.items[key] = (entry[0], now)\n        self.items.move_to_end(key)\n        self.hits += 1\n        return entry[0]"),
    SOLUTIONS["A15.6a"].replace("        if entry is None:\n            self.misses += 1\n            return None", "        if entry is None:\n            return None"),
]
