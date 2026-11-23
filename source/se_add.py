#!/usr/bin/env python3
"""Add module A15, Software engineering practice, to the Python Course.

The general engineering skills the audit found missing: SQL beyond the basics, logins and tokens,
debugging, configuration and Docker, code review on a shared repository, and a system design primer.
Idempotent. Run with Python 3.14 (the page's version), then deep_partial.sh, checks_build.py, deep_merge.py."""
import importlib.util, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("b7", os.path.join(HERE, "specs/b7_se.py"))
b7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b7)

MODULE = {
    "id": "a15", "n": "A15", "t": "Software engineering practice",
    "goal": "The skills every software team expects beyond the language itself: querying a real database, handling logins safely, finding bugs methodically, configuring and shipping a service, working through code review, and reasoning about a system's design.",
    "res": [["SQLite: query language", "https://www.sqlite.org/lang.html"],
            ["OWASP Password Storage Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"],
            ["Python docs: pdb, the debugger", "https://docs.python.org/3/library/pdb.html"],
            ["The Twelve-Factor App", "https://12factor.net/"],
            ["Conventional Commits", "https://www.conventionalcommits.org/"],
            ["Google Engineering Practices: code review", "https://google.github.io/eng-practices/review/"]],
    "items": [],
}

LESSONS = [
 {"id": "A15.1", "t": "SQL beyond the basics: joins, grouping, indexes, transactions", "min": 110,
  "learn": "Combine tables with JOIN, summarise with GROUP BY, make queries fast with indexes, and keep data consistent with transactions, using sqlite3 and skills that carry over to PostgreSQL.",
  "ex": [["Top customers and a safe transfer",
    "Two functions over an open sqlite3 connection.\n\n"
    "Tables: customers(id, name), orders(id, customer_id, total_cents), accounts(id, balance).\n\n"
    "top_customers(conn, n) returns the n biggest spenders as rows of (name, order_count, total_cents):\n"
    "- Biggest total first; equal totals are ordered by name.\n"
    "- Customers with no orders are included, with 0 orders and a total of 0 (LEFT JOIN, and COALESCE for the sum).\n"
    "- Pass n as a query parameter.\n\n"
    "transfer(conn, src, dst, cents) moves money between two accounts in one transaction:\n"
    "- cents of 0 or less raises ValueError.\n"
    "- An account id that does not exist (either one) raises LookupError.\n"
    "- A balance smaller than cents raises ValueError.\n"
    "- On success both updates are committed together; on any error nothing changes.\n\n"
    "Use ? placeholders for every value; never build SQL with f-strings or format.\n\n"
    "Example: with Ada's orders 500 and 700, Grace's 2000, top_customers(conn, 2) is [(\"Grace\", 1, 2000), (\"Ada\", 2, 1200)]."]]},
 {"id": "A15.2", "t": "Logins done safely: password hashes, sessions and tokens", "min": 100,
  "learn": "Store passwords as salted, slow hashes, compare secrets in constant time, and understand how signed tokens (the idea behind JWT) and sessions keep a user logged in.",
  "ex": [["Password hashes and signed tokens",
    "Write four functions with the standard library (hashlib, hmac, os, json, base64).\n\n"
    "hash_password(password, salt=None):\n"
    "- Uses hashlib.pbkdf2_hmac(\"sha256\", password bytes, salt, 100_000).\n"
    "- With salt=None, makes 16 random bytes with os.urandom.\n"
    "- Returns salt and hash in hex, joined by $: \"salt_hex$hash_hex\".\n\n"
    "verify_password(password, stored) returns True only for the right password. A malformed stored value returns False. Compare with hmac.compare_digest.\n\n"
    "make_token(payload, secret, now, ttl=3600):\n"
    "- Adds \"exp\": now + ttl to a copy of the payload dictionary.\n"
    "- body = URL-safe base64 of the JSON (sort_keys=True), without = padding.\n"
    "- signature = URL-safe base64 (no padding) of HMAC-SHA256 of body with the secret.\n"
    "- Returns body + \".\" + signature.\n\n"
    "read_token(token, secret, now) returns the payload dictionary (including exp). It raises ValueError when the token is malformed, when the signature does not match (check this before decoding the body), or when now >= exp.\n\n"
    "now is passed in as a number of seconds so the tests can control time."]]},
 {"id": "A15.3", "t": "Debugging methodically: tracebacks, pdb, logging and bisecting", "min": 90,
  "learn": "Read a traceback from the bottom up, step through code with breakpoint() and pdb, leave useful logging behind, and find the commit that broke something with git bisect.",
  "ex": [["Find the first bad version",
    "git bisect finds the commit that introduced a bug by testing the middle of the range again and again. Write the same search.\n\n"
    "first_bad(versions, is_bad):\n"
    "- versions is a sequence ordered from oldest to newest (it has len() and indexing).\n"
    "- is_bad(version) returns True for a broken version. Once a version is bad, every later one is bad too.\n"
    "- Return the first bad version, or None when none is bad (or the sequence is empty).\n"
    "- Testing a version is slow (think: build and run the test suite), so call is_bad as few times as possible: about log2(n) calls, never the same version twice.\n\n"
    "Example: first_bad([\"v1\", \"v2\", \"v3\", \"v4\"], lambda v: v >= \"v3\") is \"v3\".\n\n"
    "Edge cases: everything bad gives the first version; a million versions need at most 20 calls."]]},
 {"id": "A15.4", "t": "Configuration, Docker and deployment", "min": 100,
  "learn": "Read settings from the environment and validate them at start-up, package a service in a small Docker image, and know what a health check, a rollout and a rollback are.",
  "ex": [["Configuration from the environment",
    "Complete load_config(env), which turns a mapping of environment variables (such as os.environ) into the frozen Config dataclass given in the starter.\n\n"
    "Rules, checked in this order:\n"
    "- DATABASE_URL is required; surrounding spaces are stripped. Missing or blank: \"DATABASE_URL is required\".\n"
    "- PORT (default 8000) must be a whole number from 1 to 65535.\n"
    "- WORKERS (default 2) must be a whole number from 1 to 64.\n"
    "- For both: not a number gives \"PORT must be a whole number, got 'http'\"; out of range gives \"PORT must be between 1 and 65535, got 70000\".\n"
    "- DEBUG (default False) accepts 1, true, yes, on and 0, false, no, off in any letter case. Anything else: \"DEBUG must be true or false, got 'maybe'\".\n"
    "- Other variables are ignored.\n\n"
    "Collect every problem and raise ConfigError(problems) once, so an operator can fix them all in one go. With no problems, return the Config.\n\n"
    "Example: load_config({\"DATABASE_URL\": \"postgres://db/app\", \"PORT\": \"9090\"}) gives Config(\"postgres://db/app\", 9090, False, 2)."],
   ["Containerise a small service",
    "On your computer, take any small web app from this course (the FastAPI or Flask one). Write a Dockerfile that uses a slim Python base image, installs dependencies before copying the code (so the layer is cached), runs as a non-root user and starts the server. Add a /health route, build the image, run it with settings passed by -e or --env-file, and check the health route with curl. Note the image size and one thing you would change before running it in production."]]},
 {"id": "A15.5", "t": "Working in a shared repository: branches, pull requests and code review", "min": 90,
  "learn": "Work in short-lived branches, write commit messages and pull requests other people can review, give and receive review comments well, and resolve a merge conflict.",
  "ex": [["Commit message checker",
    "Teams often enforce the Conventional Commits format in CI. Write check_commit(message), which returns a list of problems (an empty list for a good message). The first line is the subject.\n\n"
    "Rules, reported in this order:\n"
    "1. The subject matches type(scope): summary. The scope in brackets is optional and uses lower-case letters, digits and hyphens; a ! may follow for a breaking change; then a colon, one space and a non-empty summary. If not: \"subject must look like 'type(scope): summary'\". If it matches but the type is not in TYPES: \"unknown type 'update'\".\n"
    "2. More than 72 characters: \"subject is 75 characters; keep it to 72\".\n"
    "3. The subject ends with a full stop: \"subject must not end with a full stop\".\n"
    "4. The summary starts with a capital letter (only checked when rule 1 matched): \"summary starts with a lower-case letter\".\n"
    "5. A second line that is not blank: \"leave the second line blank\".\n"
    "6. A ! without a body line starting with \"BREAKING CHANGE: \": \"a breaking change (!) needs a 'BREAKING CHANGE: ' line in the body\".\n\n"
    "Example: check_commit(\"fix: stop tips being split twice\") is []; check_commit(\"feature: Add it.\") reports the unknown type, the full stop and the capital letter."],
   ["Review a pull request",
    "Open a pull request on one of your own repositories (a real change, 50 to 200 lines), then review it as if a colleague wrote it. Write at least five review comments: one about correctness, one about tests, one about naming or readability, one question, and one thing done well. Mark which comments would block the merge and which are suggestions. Then address them and merge."]]},
 {"id": "A15.6", "t": "A system design primer: caches, queues and rough numbers", "min": 100,
  "learn": "Sketch how a web service fits together (load balancer, app servers, database, cache, queue), estimate load with rough numbers, and reason about the trade-offs interviewers ask about.",
  "ex": [["An LRU cache with expiry",
    "Complete the class LRUCache, the cache behind functools.lru_cache and most in-memory caches.\n\n"
    "Specification:\n"
    "- LRUCache(capacity, ttl=None); capacity below 1 raises ValueError.\n"
    "- put(key, value, now=0) stores the value with the time it was stored. If the cache then holds more than capacity items, the least recently used one is dropped.\n"
    "- get(key, now=0) returns the value, or None when the key is missing or expired. Both get and put count as using a key.\n"
    "- With a ttl, an item expires when now - time stored >= ttl; an expired item is removed when it is asked for. Reading does not restart the clock.\n"
    "- hits and misses count the get calls that found or did not find a value; hit_rate() is hits / (hits + misses), or 0.0 before any lookup.\n"
    "- len(cache) is the number of stored items.\n\n"
    "now is passed in so the tests can control time.\n\n"
    "Example: with capacity 2, after put a, put b, get a, put c, the cache holds a and c: b was used least recently.\n\n"
    "Hint: collections.OrderedDict has move_to_end(key) and popitem(last=False)."]]},
]

EXAMPLES = {
 "A15.1": {"title": "JOIN, GROUP BY and what an index changes",
  "code": '''import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE staff (id INTEGER PRIMARY KEY, name TEXT, team TEXT);
CREATE TABLE shifts (id INTEGER PRIMARY KEY, staff_id INTEGER REFERENCES staff(id), hours INTEGER);
INSERT INTO staff VALUES (1, 'Ada', 'kitchen'), (2, 'Grace', 'floor'), (3, 'Linus', 'floor');
INSERT INTO shifts (staff_id, hours) VALUES (1, 6), (1, 8), (2, 4), (2, 4), (2, 5);
""")

print("hours per person (LEFT JOIN keeps Linus, who has no shifts):")
for row in db.execute("""
    SELECT s.name, COUNT(sh.id), COALESCE(SUM(sh.hours), 0)
    FROM staff AS s LEFT JOIN shifts AS sh ON sh.staff_id = s.id
    GROUP BY s.id ORDER BY 3 DESC"""):
    print(" ", row)

print("teams with more than 10 hours (HAVING filters groups):")
print(" ", db.execute("""
    SELECT s.team, SUM(sh.hours) FROM staff AS s JOIN shifts AS sh ON sh.staff_id = s.id
    GROUP BY s.team HAVING SUM(sh.hours) > 10 ORDER BY s.team""").fetchall())

query = "SELECT * FROM shifts WHERE staff_id = ?"
print("before index:", db.execute("EXPLAIN QUERY PLAN " + query, (2,)).fetchone()[3])
db.execute("CREATE INDEX idx_shifts_staff ON shifts(staff_id)")
print("after index: ", db.execute("EXPLAIN QUERY PLAN " + query, (2,)).fetchone()[3])
''',
  "note": "JOIN matches rows from two tables; LEFT JOIN also keeps rows with no match, filling the gaps with NULL, which COALESCE turns into 0. GROUP BY makes one row per group, WHERE filters rows before grouping and HAVING filters groups after. EXPLAIN QUERY PLAN shows the difference an index makes: SCAN reads every row, SEARCH jumps straight to the matching ones."},
 "A15.2": {"title": "Why passwords are salted and hashed slowly",
  "code": '''import hashlib, hmac, os, time

password = "correct horse"
print("plain sha256, same every time:", hashlib.sha256(password.encode()).hexdigest()[:16],
      hashlib.sha256(password.encode()).hexdigest()[:16])

salt_a, salt_b = os.urandom(16), os.urandom(16)
a = hashlib.pbkdf2_hmac("sha256", password.encode(), salt_a, 100_000)
b = hashlib.pbkdf2_hmac("sha256", password.encode(), salt_b, 100_000)
print("salted: two users with the same password get equal hashes?", a == b)

start = time.perf_counter()
hashlib.sha256(password.encode()).digest()
fast = time.perf_counter() - start
start = time.perf_counter()
hashlib.pbkdf2_hmac("sha256", password.encode(), salt_a, 100_000)
slow = time.perf_counter() - start
print("one slow hash costs an attacker far more per guess:", slow > fast * 100)

again = hashlib.pbkdf2_hmac("sha256", b"correct horse", salt_a, 100_000)
print("login check:", hmac.compare_digest(a, again), hmac.compare_digest(a, b))
''',
  "note": "A fast, unsalted hash lets an attacker who steals the table try billions of guesses a second and crack every copy of a common password at once. A random salt per user makes equal passwords look different, and a deliberately slow function (PBKDF2 here; Argon2 or scrypt in new systems) makes each guess expensive. compare_digest avoids leaking where two values differ through timing."},
 "A15.3": {"title": "Reading a traceback and leaving a log behind",
  "code": '''import logging, sys, traceback

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s", stream=sys.stdout)
log = logging.getLogger("payroll")

def hourly_rate(staff):
    return staff["pay"] / staff["hours"]

def payroll(team):
    rates = {}
    for person in team:
        try:
            rates[person["name"]] = round(hourly_rate(person), 2)
        except ZeroDivisionError:
            log.warning("skipping %s: no hours recorded", person["name"])
    log.info("computed %d of %d rates", len(rates), len(team))
    return rates

team = [{"name": "Ada", "pay": 900, "hours": 30}, {"name": "Grace", "pay": 0, "hours": 0}]
print(payroll(team))

try:
    payroll([{"name": "Linus", "pay": 500}])
except KeyError:
    last = traceback.extract_tb(sys.exc_info()[2])[-1]
    print(f"KeyError raised in {last.name}(), on the line: {last.line}")
''',
  "note": "Read a traceback from the bottom: the last line names the error, and the frame just above it is where it happened (hourly_rate, not payroll). Log messages with %s arguments instead of f-strings so the text is only built when the level is enabled, and log what you would want to know at 3 a.m.: which record, and what was skipped. In an editor or terminal, breakpoint() at that line drops you into pdb to inspect the values."},
 "A15.4": {"title": "Settings from the environment, checked at start-up",
  "code": '''from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    database_url: str
    port: int
    debug: bool

def from_env(env):
    missing = [k for k in ("DATABASE_URL",) if not env.get(k)]
    if missing:
        raise SystemExit("missing settings: " + ", ".join(missing))
    return Settings(env["DATABASE_URL"], int(env.get("PORT", "8000")), env.get("DEBUG", "").lower() in {"1", "true"})

print(from_env({"DATABASE_URL": "postgres://db/app", "PORT": "9090", "DEBUG": "true"}))
print(from_env({"DATABASE_URL": "sqlite:///dev.db"}))
try:
    from_env({"PORT": "9090"})
except SystemExit as stop:
    print("refused to start:", stop)
''',
  "note": "The same code runs on a laptop, in CI and in production; only the environment differs, so settings such as database addresses and secrets come from environment variables, not from the code (the 'config' rule of the Twelve-Factor App). Reading them once at start-up into a frozen object, and refusing to start when something is missing (a real program passes os.environ), turns a confusing failure at 3 a.m. into a clear message at deploy time."},
 "A15.5": {"title": "A three-way merge and where conflicts come from",
  "code": '''def merge(base, ours, theirs):
    """Merge two edits of the same lines, the way git does, line by line."""
    out = []
    for b, o, t in zip(base, ours, theirs):
        if o == t:
            out.append(o)              # same on both sides (or nobody changed it)
        elif o == b:
            out.append(t)              # only they changed it
        elif t == b:
            out.append(o)              # only we changed it
        else:
            out += ["<<<<<<< ours", o, "=======", t, ">>>>>>> theirs"]
    return out

base   = ["PORT = 8000", "DEBUG = False", "WORKERS = 2"]
ours   = ["PORT = 8000", "DEBUG = True",  "WORKERS = 4"]
theirs = ["PORT = 9090", "DEBUG = False", "WORKERS = 8"]
print("\\n".join(merge(base, ours, theirs)))
''',
  "note": "Git compares both branches with their common ancestor. A line changed on one side only is taken automatically; a line changed differently on both sides is a conflict, and git writes both versions between markers for a person to resolve. Short-lived branches and small pull requests keep the two sides close, which is the practical way to have fewer conflicts."},
 "A15.6": {"title": "Back-of-the-envelope numbers for a service",
  "code": '''users = 200_000
requests_per_user_per_day = 40
peak_factor = 5                      # the busiest minute is about 5x the average
average_rps = users * requests_per_user_per_day / 86_400
peak_rps = average_rps * peak_factor
print(f"average {average_rps:.0f} requests/s, peak about {peak_rps:.0f} requests/s")

one_server_rps = 150                 # measured with a load test
servers = -(-peak_rps // one_server_rps) + 1      # round up, plus one spare
print(f"app servers needed: {servers:.0f}")

db_ms, cache_ms, hit_rate = 40, 1, 0.9
with_cache = hit_rate * cache_ms + (1 - hit_rate) * (cache_ms + db_ms)
print(f"average read: {db_ms} ms without a cache, {with_cache:.1f} ms with a 90% hit rate")
print(f"database load falls to {(1 - hit_rate) * 100:.0f}% of the reads")

row_bytes, rows_per_day = 300, users * 3
print(f"storage: about {row_bytes * rows_per_day * 365 / 1e9:.0f} GB a year")
''',
  "note": "System design starts with rough numbers: 8 million requests a day sounds huge but averages under 100 a second, and a peak factor and one measured number per server tell you how many machines that is. The cache sum shows why a 90% hit rate matters twice: reads get about eight times faster and the database sees a tenth of the traffic. Being roughly right quickly is the skill; precision comes from load tests."},
}

TEXT_SOLUTIONS = {
 "A15.4b": ("text", [
   "Order the Dockerfile so things that change rarely come first: base image, dependencies, then your code.",
   "Create a user with RUN useradd and switch with USER before CMD; pass settings with -e NAME=value.",
   "docker build -t app . then docker run -p 8000:8000 -e DATABASE_URL=... app, and curl localhost:8000/health."],
   "A container image is how most teams ship Python services, and the Dockerfile is often part of a take-home task.",
   "FROM python:3.14-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nRUN useradd --create-home app\nUSER app\nEXPOSE 8000\nHEALTHCHECK CMD python -c \"import urllib.request; urllib.request.urlopen('http://localhost:8000/health')\"\nCMD [\"uvicorn\", \"main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n\n"
   "Notes: dependencies are installed before COPY . . so editing code does not reinstall them. The image is about 200 MB with the slim base. Before production: pin dependency versions with a lock file, add a .dockerignore (no .git, .venv or .env in the image), and never bake secrets into the image.",
   ["A Dockerfile with a slim base image and dependencies installed before the code is copied", "The container runs as a non-root user", "Settings are passed in from the environment, not written in the image", "A /health route answers inside the running container", "One production improvement is named"]),
 "A15.5b": ("text", [
   "Review the diff, not the person: say what the code does and what you would expect instead.",
   "Prefix comments so the author knows their weight: 'blocking:', 'suggestion:', 'question:', 'nit:'.",
   "Check the tests first: do they fail without the change, and do they cover the edge cases?"],
   "Code review is a daily activity on every team, and your QA background is a strength here: you already look for the cases the author did not think of.",
   "Example comments:\n- blocking (correctness): split_tips() divides by sum(hours); a team with no hours raises ZeroDivisionError. Return [] or raise a clear error.\n- blocking (tests): there is no test for an odd number of cents; add one that checks the shares still add up.\n- suggestion (naming): h and t would read better as hours and total_cents.\n- question: is rounding down intended, with the remainder going to the longest shift? A comment or docstring would help.\n- praise: nice that the function is pure, with no file or network access; it made it easy to review and test.\n\nThen: push follow-up commits, reply to each comment, and merge once the blocking ones are resolved.",
   ["A real pull request of 50 to 200 lines", "At least five comments: correctness, tests, readability, a question, and something done well", "Comments are marked as blocking or suggestions", "The comments were addressed and the pull request merged"]),
}

AUTO = {
 "A15.1a": {"hints": ["Start from customers and LEFT JOIN orders ON orders.customer_id = customers.id, then GROUP BY the customer id.",
                       "COUNT(o.id) counts only real orders (NULLs are skipped), and COALESCE(SUM(o.total_cents), 0) turns a missing total into 0. ORDER BY the total DESC, then the name, and LIMIT ?.",
                       "For transfer, do the checks and both UPDATE statements inside 'with conn:': it commits if the block finishes and rolls back if anything raises."],
            "explain": "The LEFT JOIN keeps customers without orders, which an inner JOIN silently drops; that is one of the most common reporting bugs. A transaction makes the two updates atomic: either both happen or neither does, so money can never leave one account without arriving in the other, even if the program crashes in between. Checking everything before the first UPDATE, inside the same transaction, keeps a refused transfer from leaving partial changes. Parameters (?) keep data out of the SQL text, which prevents SQL injection."},
 "A15.2a": {"hints": ["hash_password: salt = salt or os.urandom(16) is nearly right, but use 'is not None' so an explicit salt always wins; return salt.hex() + \"$\" + digest.hex().",
                       "verify_password: split the stored value at $, rebuild the hash with the same salt and compare the two strings with hmac.compare_digest; catch ValueError for malformed input.",
                       "Tokens: body = base64.urlsafe_b64encode(json bytes).decode().rstrip(\"=\"); signature = the same encoding of hmac.new(secret.encode(), body.encode(), hashlib.sha256).digest(). To decode, add the padding back: body + \"=\" * (-len(body) % 4)."],
            "explain": "Hashing with a per-user salt and many rounds is what turns a stolen password table from a disaster into a slow, expensive problem for the attacker. The token is the core of a JWT: the server signs the payload with a secret only it knows, so it can trust the payload later without storing anything, and any change to the body breaks the signature. Check the signature before reading the body, and always include an expiry. In real projects use a maintained library (argon2-cffi, PyJWT) rather than your own code, but knowing what is inside makes you able to use and review them."},
 "A15.3a": {"hints": ["This is binary search for the boundary between good and bad: keep lo = 0 and hi = len(versions).",
                       "Test the middle version. If it is bad, the first bad one is at mid or earlier (hi = mid); if it is good, it is later (lo = mid + 1).",
                       "When lo reaches hi, that index is the first bad version, unless it equals len(versions), which means nothing was bad."],
            "explain": "Because every version after the first bad one is also bad, each test rules out half of the remaining range, so a thousand commits need about ten tests and a million about twenty. That is exactly what git bisect start, git bisect bad, git bisect good do, and git bisect run automates it with a script. The half-open range [lo, hi) avoids the off-by-one mistakes that make hand-written binary searches return the neighbour of the right answer."},
 "A15.4a": {"hints": ["Keep a list of problems and a dictionary of values, and only raise at the end.",
                       "PORT and WORKERS follow the same rule with different limits, so loop over (name, low, high) tuples; int() raises ValueError for text that is not a number.",
                       "For DEBUG, lower-case the stripped text and test membership in two sets of accepted words."],
            "explain": "Validating all settings at start-up and reporting every problem together respects the operator's time: one failed deploy shows the whole list. A frozen dataclass gives the rest of the program typed, read-only settings instead of string lookups scattered through the code. Libraries such as pydantic-settings do the same job with less code, and the rules here (required, ranges, booleans from words) are the ones they implement."},
 "A15.5a": {"hints": ["Split the message into lines; the subject is lines[0]. One regular expression can capture type, optional (scope), optional ! and the summary.",
                       "Check the rules in the listed order and append to a list; some rules only apply when the subject matched.",
                       "For the breaking-change rule, look at the lines after the blank second line for one that starts with \"BREAKING CHANGE: \"."],
            "explain": "A consistent subject line makes history searchable and lets tools build changelogs and choose version numbers: fix means a patch release, feat a minor one, and ! or BREAKING CHANGE a major one. Returning every problem in a fixed order makes the checker predictable in CI output. Real projects use commitlint or a pre-commit hook for this; writing one shows you exactly what those tools check."},
 "A15.6a": {"hints": ["Store key -> (value, time stored) in an OrderedDict; the order of the dictionary is the order of use.",
                       "On every successful get and every put, call move_to_end(key); when there are too many items, popitem(last=False) removes the oldest.",
                       "In get, check expiry first: if now - stored >= ttl, delete the item and treat it as a miss."],
            "explain": "An LRU cache bets that what was used recently will be used again, which holds for most web traffic, and a time limit bounds how stale an answer can be. Both operations are O(1) because an OrderedDict is a hash table plus a linked list. The hit rate is the number to watch: a cache with a low hit rate adds complexity without saving work. Typical slips: forgetting that a read counts as a use, and letting reads extend the expiry so stale data never leaves."},
}

QUIZ = [
 ("Which join keeps customers who have no orders?", ["LEFT JOIN from customers to orders", "INNER JOIN", "JOIN with a WHERE clause", "CROSS JOIN"], 0,
  "A LEFT JOIN keeps every row of the left table and fills the missing right-hand columns with NULL."),
 ("What does a transaction guarantee for a money transfer?", ["Both updates happen or neither does", "The transfer is faster", "The tables are backed up", "Nobody else can read the database"], 0,
  "Atomicity: if anything fails before the commit, the database rolls back to how it was."),
 ("A query filters on a column of a table with ten million rows. What usually makes it fast?", ["An index on that column", "SELECT *", "A bigger LIMIT", "Running it twice"], 0,
  "An index lets the database jump to matching rows instead of scanning the whole table, at the cost of slightly slower writes."),
 ("How should a web application store passwords?", ["As a salted hash from a deliberately slow function such as Argon2, scrypt or PBKDF2", "Encrypted, so support can read them", "As plain SHA-256", "In a cookie"], 0,
  "A slow, salted hash makes each guess expensive and stops one cracked password revealing every user who chose it."),
 ("A signed token's payload is changed by the user. What happens when the server reads it?", ["The signature no longer matches, so the server rejects it", "The server accepts the new payload", "The token becomes encrypted", "The expiry is extended"], 0,
  "The signature is computed from the body with a secret only the server knows; any change breaks it."),
 ("Where do you start reading a Python traceback?", ["At the bottom: the error type and message, then the frame just above", "At the top, always", "In the middle", "Only the file names matter"], 0,
  "The last line says what went wrong and the frame above it says where; earlier frames show how the program got there."),
 ("A bug appeared somewhere in the last 1,000 commits. About how many builds does git bisect need?", ["10", "100", "500", "1,000"], 0,
  "Each test halves the range, and 2 to the power 10 is 1,024."),
 ("Why read configuration from environment variables?", ["The same code and image run everywhere; only the settings differ, and secrets stay out of the repository", "They are faster than files", "Python requires it", "They are encrypted automatically"], 0,
  "This is the Twelve-Factor config rule: strict separation of config from code."),
 ("In a Dockerfile, why copy requirements.txt and install before copying the rest of the code?", ["The dependency layer is cached, so code changes rebuild in seconds", "It makes the image smaller", "Docker requires that order", "It hides the code"], 0,
  "Layers are rebuilt from the first changed step onwards, so put what changes least first."),
 ("Which review comment is most useful to the author?", ["blocking: this divides by zero when the team has no hours; return [] or raise a clear error", "This is wrong.", "I would never write it like this.", "LGTM (without reading it)"], 0,
  "Good comments say what happens, why it matters, how serious it is and what would fix it."),
 ("A cache has a 90% hit rate. What share of reads still reach the database?", ["10%", "90%", "50%", "0%"], 0,
  "Only the misses go to the database, which is why hit rate is the number to watch."),
 ("A service gets 8.6 million requests a day. Roughly how many per second on average?", ["100", "10", "1,000", "10,000"], 0,
  "A day has 86,400 seconds, so 8.64 million a day is 100 a second; the peak may be several times higher."),
]


def run_example(code):
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=60, cwd=d)
    if r.returncode != 0:
        raise SystemExit("example failed:\n" + r.stderr)
    return r.stdout.rstrip("\n")


def main():
    d = json.load(open(os.path.join(HERE, "pycontent.json")))
    for coll in ("lessons", "grade", "chk"):
        for k in [k for k in d[coll] if k.startswith("A15.")]:
            del d[coll][k]
    d["quiz"].pop("a15", None)
    MODULE["items"] = []
    for L in LESSONS:
        MODULE["items"].append({"id": L["id"], "t": L["t"], "min": L["min"], "learn": L["learn"], "kind": "lesson",
                                "ex": [{"id": L["id"] + "abc"[i], "t": e[0], "p": e[1]} for i, e in enumerate(L["ex"])]})
        ex = EXAMPLES[L["id"]]
        lesson = {"example": {"title": ex["title"], "code": ex["code"], "note": ex["note"], "output": run_example(ex["code"])},
                  "exercises": {}}
        for i, _ in enumerate(L["ex"]):
            eid = L["id"] + "abc"[i]
            if eid in AUTO:
                lesson["exercises"][eid] = {"hints": AUTO[eid]["hints"], "lang": "python", "solution": b7.SOLUTIONS[eid],
                                            "explain": AUTO[eid]["explain"]}
                d["grade"][eid] = dict(b7.SPECS[eid])
            else:
                lang, hints, why, sol, chk = TEXT_SOLUTIONS[eid]
                lesson["exercises"][eid] = {"hints": hints, "lang": lang, "solution": sol, "explain": why}
                d["chk"][eid] = chk
        d["lessons"][L["id"]] = lesson
    d["quiz"]["a15"] = [{"id": f"a15-{n + 1:02d}", "type": "single", "pool": "quiz", "prompt": q, "code": "",
                         "options": opts, "answer": [ans], "explain": ex} for n, (q, opts, ans, ex) in enumerate(QUIZ)]
    json.dump(d, open(os.path.join(HERE, "pycontent.json"), "w"), ensure_ascii=False)

    page = open(os.path.join(HERE, "course.html"), encoding="utf-8").read()
    m = re.search(r"var MA=(\[.*?\]);\n", page)
    ma = [x for x in json.loads(m.group(1)) if x["id"] != "a15"]
    ma.insert(next(i for i, x in enumerate(ma) if x["id"] == "a13"), MODULE)   # before the career toolkit and capstone
    page = page[:m.start(1)] + json.dumps(ma, ensure_ascii=False) + page[m.end(1):]
    if '"a15"' not in page.split("var COURSES=[")[1].split("];")[0]:
        old = '  {code:"PY206",t:"The Wider Ecosystem: Roadmap Extras",y:2,mods:["a14"]},'
        assert old in page
        page = page.replace(old, old + '\n  {code:"PY207",t:"Software Engineering Practice",y:2,mods:["a15"]},')
    if "a15:" not in page:
        page = page.replace("a13:3,a14:3};", "a13:3,a14:3,a15:4};")
    i = page.find("window.PYCC_CONTENT=") + len("window.PYCC_CONTENT=")
    j = page.find(";</script>", i)
    c = json.loads(page[i:j].replace("<\\!", "<!"))
    for k in ("lessons", "grade", "chk", "quiz"):
        c[k] = d[k]
    page = page[:i] + json.dumps(c).replace("</", "<\\/").replace("<!", "<\\!") + page[j:]
    open(os.path.join(HERE, "course.html"), "w", encoding="utf-8").write(page)
    print("A15 added:", len(LESSONS), "lessons,", sum(len(L["ex"]) for L in LESSONS), "exercises,", len(QUIZ), "quiz questions")


if __name__ == "__main__":
    main()
