#!/usr/bin/env python3
"""Add module A13, Career toolkit, to the Python Course: lessons, exercises, specs, checklists and quiz.
Idempotent: removes any earlier A13 data first. Lesson example outputs are produced by running the code.
usage: python3 career_add.py   (then deep_build.py, checks_build.py, deep_merge.py as usual)"""
import importlib.util, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("b3", os.path.join(HERE, "specs/b3_career.py"))
b3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b3)

MODULE = {
    "id": "a13", "n": "A13", "t": "Career toolkit: Git, portfolio and QA interviews",
    "goal": "Present your work the way hiring teams read it: a clean Git history, READMEs that get read, and confident answers in QA automation and QA leadership interviews.",
    "res": [["Conventional Commits", "https://www.conventionalcommits.org/en/v1.0.0/"],
            ["GitHub Docs: about READMEs", "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes"],
            ["GitHub Docs: your profile README", "https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme"],
            ["pytest documentation", "https://docs.pytest.org/en/stable/"],
            ["Playwright: auto-waiting", "https://playwright.dev/python/docs/actionability"]],
    "items": [],
}

SPEC_NOTE = "Specification first, as in a real ticket: read every rule and edge case before writing code."

LESSONS = [
 {"id": "A13.1", "t": "Git and GitHub for portfolio work", "min": 90,
  "learn": "Commits that tell a story, feature branches and pull requests, .gitignore, tags and releases, and Conventional Commit messages that tools and reviewers can read.",
  "ex": [
   ["Commit message checker",
    "Write check_commit(message) that returns a list of problem codes for a commit message, in this exact order: type, length, period, case, blank-line. Return [] when the message is fine.\n\n"
    "Specification:\n"
    "- The header is the first line. It must look like type(scope)!: summary, where the scope in brackets and the ! are optional, and there is exactly one space after the colon.\n"
    "- An empty message (or only whitespace) returns [\"empty\"]. A header that does not have that shape returns [\"format\"]. In both cases, return straight away.\n"
    "- type: the type is not one of feat, fix, docs, test, refactor, perf, build, ci, chore, style, revert.\n"
    "- length: the header is longer than 72 characters.\n"
    "- period: the summary ends with a full stop.\n"
    "- case: the summary starts with a capital letter.\n"
    "- blank-line: there is a body, but the second line is not blank.\n\n"
    "Examples:\n"
    "- check_commit(\"feat(api): add shift endpoint\") returns []\n"
    "- check_commit(\"fix: Correct rounding.\") returns [\"period\", \"case\"]\n"
    "- check_commit(\"wip\") returns [\"format\"]\n\n"
    "Edge cases: types are lower case (Fix: is a format problem); exactly 72 characters is fine; feat!: marks a breaking change and is allowed."],
   ["Put one project on GitHub properly",
    "Pick one of your course projects and publish it the way a reviewer expects: a .gitignore that keeps caches, virtual environments and secrets out; a README; work done on a feature branch and merged through a pull request with a description; and a tag v0.1.0 with a GitHub release. Write the repository link and what each step taught you in your notes."],
  ]},
 {"id": "A13.2", "t": "A portfolio that gets read", "min": 90,
  "learn": "How reviewers skim a repository in under a minute, the anatomy of a README that answers their questions, results tables and screenshots, pinned repositories and a short GitHub profile README.",
  "ex": [
   ["README checker",
    "Write readme_report(text) that returns a dictionary with five keys: title, missing, code_blocks, todos and score.\n\n"
    "Specification:\n"
    "- title is True when the first non-empty line, outside code blocks, starts with \"# \" (one hash and a space).\n"
    "- missing lists the required sections that have no heading, in this order: install, usage, tests. A heading is a line starting with \"## \" or \"### \". It covers install if its text contains install, usage if it contains usage, example or quick start, and tests if it contains test (case-insensitive).\n"
    "- Lines inside fenced code blocks (between lines starting with ```) never count as headings or as the title.\n"
    "- code_blocks is the number of complete fenced blocks (fence lines divided by 2, rounded down).\n"
    "- todos is the number of lines containing TODO, anywhere.\n"
    "- score is 100, minus 20 per missing section, minus 20 without a title, minus 10 with no code block, minus 5 per TODO line, and never below 0.\n\n"
    "Example: a README with # tool, ## Install, ## Usage, ## Running the tests and two code blocks gives {\"title\": True, \"missing\": [], \"code_blocks\": 2, \"todos\": 0, \"score\": 100}.\n\n"
    "Edge cases: blank lines before the title are fine; ## Usage inside a code block does not count; an Examples heading counts as usage."],
   ["Write your GitHub profile README",
    "Write the README.md for your GitHub profile repository (the repository named after your username). In under 150 words: who you are and the roles you are aiming for, three pinned projects with one line each on the problem and the result, the tools you use daily, and how to contact you. Then choose which six repositories to pin and in what order."],
  ]},
 {"id": "A13.3", "t": "Interview drills: test design with pytest", "min": 120,
  "learn": "Answer the test-design questions QA automation interviews ask: equivalence classes and boundaries, fixtures, parametrize, fakes versus mocks, and proving that your tests would catch real bugs.",
  "ex": [
   ["Tests that catch bugs",
    "The module shipping provides shipping_cost(weight_kg, express=False), which returns a price in cents. Write pytest-style test functions (names starting with test_) that pass on the correct code and catch the bugs hidden in five broken versions.\n\n"
    "Specification of shipping_cost:\n"
    "- A weight must be more than 0 and at most 30 kg; anything else raises ValueError.\n"
    "- Up to and including 1 kg costs 500.\n"
    "- Every started kilogram above 1 kg adds 200 (1.2 kg costs 700, 2 kg costs 700, 2.01 kg costs 900).\n"
    "- express=True doubles the total.\n\n"
    "Grading: your tests run against the correct function, where every test must pass, then against five versions that each break one rule, where at least one test must fail. Write at least four tests.\n\n"
    "Edge cases to think about: the exact limits 0 and 30, just past them, partial kilograms, and express on a parcel heavier than 1 kg. Use pytest.raises(ValueError) for the errors (a small stand-in for pytest is available here)."],
   ["Answer six classic test-design questions",
    "Write a short spoken-style answer (three to five sentences, with one example from your own work) to each: 1. How do you decide what to automate and what to keep manual? 2. What is the difference between a fixture and setup code in each test? 3. When do you use a fake, a stub or a mock? 4. What makes a test flaky, and what do you do when you find one? 5. How would you test a REST endpoint that creates a resource? 6. How do you know your test suite is good, beyond coverage?"],
  ]},
 {"id": "A13.4", "t": "Interview drills: APIs, browsers and flaky tests", "min": 120,
  "learn": "Explain waiting strategies and why fixed sleeps cause flakiness, write a polling helper you can test deterministically, check API responses against a contract, and diagnose flaky tests methodically.",
  "ex": [
   ["A testable wait_until",
    "Write wait_until(condition, timeout=5.0, interval=0.5, clock=time.monotonic, sleep=time.sleep), the polling helper behind every auto-waiting test tool.\n\n"
    "Specification:\n"
    "- Call condition(). If it returns something truthy, return that value itself (not True).\n"
    "- Otherwise, if clock() minus the start time is at least timeout, raise TimeoutError with a message containing \"after X s\", where X is the timeout as given (for example \"condition not met after 2 s\").\n"
    "- Otherwise call sleep(interval) and try again.\n"
    "- Always use the clock and sleep you were given, never time.sleep directly, so tests can run with a fake clock in no time.\n"
    "- If condition() raises an exception, let it propagate: hiding it would turn a bug into a mysterious timeout.\n\n"
    "Example with a fake clock: a condition that becomes true at 1.2 s, with interval 0.5, is checked at 0, 0.5, 1.0 and 1.5 s, so sleep is called three times.\n\n"
    "Edge cases: with timeout=2 and interval=0.5, a condition that is never true is tried exactly 5 times (at 0, 0.5, 1, 1.5 and 2 s) before the TimeoutError."],
   ["Diagnose five flaky tests",
    "For each scenario, name the most likely cause, how you would prove it, and the fix: 1. A Playwright test fails about 1 run in 20 on CI, never locally, at a click right after navigation. 2. A test passes alone but fails when the whole suite runs. 3. A date test fails every night between 19:00 and midnight local time. 4. An API test fails when a teammate's test runs at the same moment on the shared staging environment. 5. A test that checks search results fails when new data is added to the test database."],
  ]},
 {"id": "A13.5", "t": "Interviews for QA leadership: strategy, metrics and your stories", "min": 90,
  "learn": "Present a test strategy on one page, choose quality metrics that drive decisions rather than vanity numbers, and turn your projects and experience into short STAR stories.",
  "ex": [
   ["A one-page test strategy",
    "Write a one-page test strategy for a product you know (or the shift-planning app from module A12): what is in and out of scope, the risks you test first and why, the test levels and roughly how many tests at each, what runs on every pull request versus nightly, the environments and test data, the quality metrics you would report, and what would make you stop a release."],
   ["Three STAR stories",
    "Write three STAR stories (Situation, Task, Action, Result), each under 150 words and with a number in the result: one about improving quality or speed with automation, one about a hard bug or incident you led to resolution, and one about leading or growing people. Practise telling each out loud in under two minutes, then ask the TA to play the interviewer and push back on one of them."],
  ]},
]

EXAMPLES = {
 "A13.1": {"title": "A commit-msg hook in Python",
  "code": '''import re
import sys

PATTERN = re.compile(r"^(feat|fix|docs|test|refactor|perf|build|ci|chore|style|revert)(\\([a-z0-9-]+\\))?!?: \\S")


def check(message):
    header = message.split("\\n")[0]
    if not PATTERN.match(header):
        return "header must look like 'type(scope): summary', e.g. 'fix(api): handle empty body'"
    if len(header) > 72:
        return f"header is {len(header)} characters; keep it to 72"
    return None


# Git runs .git/hooks/commit-msg with the path of the message file; here we feed messages directly.
for message in ["fix(api): handle empty body", "Fixed stuff", "feat: " + "very long summary " * 5]:
    problem = check(message)
    print(f"{message[:40]!r:44} {'ok' if problem is None else 'REJECTED: ' + problem}")
# In the real hook: sys.exit(1) on a problem, so git refuses the commit and shows the message.
''',
  "note": "Git runs the commit-msg hook with the path of the message file and refuses the commit if the hook exits with a non-zero status. A few lines of Python enforce the convention for every commit, so the history stays readable and release notes can be generated from it."},
 "A13.2": {"title": "A results table generated for the README",
  "code": '''results = {
    "pricing (pure functions)": {"coverage": 100, "mutation": 0.92, "seconds": 1.8},
    "csv parser": {"coverage": 94, "mutation": 0.81, "seconds": 3.1},
    "scheduler (time and I/O)": {"coverage": 72, "mutation": 0.55, "seconds": 6.4},
}

lines = ["| module | coverage % | mutation score | run time |", "|---|---:|---:|---:|"]
for name, r in sorted(results.items(), key=lambda kv: -kv[1]["mutation"]):
    lines.append(f"| {name} | {r['coverage']} | {r['mutation']:.2f} | {r['seconds']:.1f} s |")
print("\\n".join(lines))
weakest = min(results, key=lambda n: results[n]["mutation"])
print(f"\\nLimitation to state in the README: {weakest} is the weakest area.")
''',
  "note": "Generating the table from real results keeps the README honest and easy to update after every run. Stating the weakest area as a limitation is a strength in a portfolio: it shows you measure your own work and know where it falls short."},
 "A13.3": {"title": "Proving a test would catch a bug",
  "code": '''def discount(total):
    """10% off orders of 100 or more."""
    return round(total * 0.9, 2) if total >= 100 else total


def mutant(total):                      # the bug a careless edit might introduce
    return round(total * 0.9, 2) if total > 100 else total


weak_tests = [(50, 50), (200, 180.0)]
strong_tests = weak_tests + [(100, 90.0), (99.99, 99.99)]

for name, tests in [("weak", weak_tests), ("strong", strong_tests)]:
    passes_real = all(discount(x) == want for x, want in tests)
    catches_bug = any(mutant(x) != want for x, want in tests)
    print(f"{name:6} suite: passes on the real code {passes_real}, catches the >= bug {catches_bug}")
''',
  "note": "Both suites pass on the real code, but only the one that tests the boundary values 100 and 99.99 notices the off-by-one bug. That is the answer interviewers want to \"how do you know your tests are good?\": think in boundaries, and check that a deliberately broken version fails."},
 "A13.4": {"title": "Why fixed sleeps make tests flaky",
  "code": '''import random

random.seed(7)
latencies = [random.lognormvariate(-0.9, 0.6) for _ in range(200)]   # seconds until the page is ready

fixed_wait = 0.5
flaky = sum(1 for t in latencies if t > fixed_wait)
print(f"sleep(0.5) then click: fails {flaky} of {len(latencies)} runs")

polling_timeout = 5.0
failed = sum(1 for t in latencies if t > polling_timeout)
average_wait = sum(min(t, polling_timeout) for t in latencies) / len(latencies)
print(f"poll every 0.1 s up to 5 s: fails {failed} of {len(latencies)} runs, waits {average_wait:.2f} s on average")
''',
  "note": "The fixed half-second sleep is both too short (it fails whenever the page is slow) and too long (it wastes time when the page is fast). Polling until the condition holds, with a generous timeout, removes the flakiness and is faster on average. That is what Playwright's auto-waiting does for you."},
 "A13.5": {"title": "Quality metrics that drive decisions",
  "code": '''releases = [
    {"name": "2.3", "found_before": 41, "found_after": 3, "hours_to_fix_after": [6, 30, 4]},
    {"name": "2.4", "found_before": 35, "found_after": 7, "hours_to_fix_after": [48, 12, 3, 72, 5, 9, 26]},
    {"name": "2.5", "found_before": 52, "found_after": 2, "hours_to_fix_after": [2, 8]},
]
runs, flaky_runs = 1240, 37

for r in releases:
    escape = r["found_after"] / (r["found_before"] + r["found_after"])
    mttr = sum(r["hours_to_fix_after"]) / len(r["hours_to_fix_after"])
    print(f"release {r['name']}: defect escape rate {escape:5.1%}, mean time to fix escapes {mttr:5.1f} h")
print(f"flaky test runs: {flaky_runs / runs:.1%} of CI runs (target: under 1%)")
worst = max(releases, key=lambda r: r["found_after"])
print(f"talking point: release {worst['name']} let the most defects escape; what changed in testing after it?")
''',
  "note": "Escape rate and time to fix escaped defects measure what users feel, and the flaky-run rate measures how much the team can trust its pipeline. Each number leads to a decision or a question, which is the difference between a metric and a vanity statistic, and the kind of answer a QA leadership interview looks for."},
}

TEXT_SOLUTIONS = {
 "A13.1b": ("text", [
   "Start with a .gitignore from GitHub's Python template, then add anything specific: .env, data folders, editor settings.",
   "Do the work on a branch (git switch -c feature/readme), push it, and open the pull request on GitHub with a description of what, why and how it was tested.",
   "After merging, tag the merge commit (git tag -a v0.1.0 -m \"First release\"; git push --tags) and create a release from the tag with short notes."],
   "A clean history is part of the portfolio: reviewers open the commits and pull requests, not just the code.",
   "Checklist I followed for teatime (example):\n\n1. .gitignore: __pycache__/, .venv/, .pytest_cache/, .env, dist/, .coverage\n2. README.md with install, usage and tests sections\n3. git switch -c feature/cli-help; two commits: \"feat(cli): add --help text\" and \"test(cli): cover unknown tea names\"\n4. Pull request #1: What (help text), Why (users guessed the options), How tested (2 new tests, CI green); merged with a merge commit\n5. git tag -a v0.1.0 -m \"First release\"; git push --tags; GitHub release v0.1.0 with notes generated from the pull requests\n\nWhat I learned: the pull request description is the place to explain decisions; the tag gives reviewers a stable version to try.",
   ["The repository has a .gitignore and no caches, virtual environments or secrets are committed", "Work happened on a branch and was merged through a pull request with a description", "A tag v0.1.0 exists with a GitHub release and short notes", "Commit messages follow type: summary and explain why where it is not obvious"]),
 "A13.2b": ("text", [
   "Lead with the roles you want, not your life story: one line that a recruiter can match to a job description.",
   "For each pinned project: the problem it solves and one result with a number (time saved, defects caught, coverage).",
   "Pin the projects that match the jobs you apply for, best first; archive or unpin exercises and forks."],
   "The profile README is the first thing a recruiter sees after clicking the link on your CV, so it should answer \"what do you do and can I see proof?\" in ten seconds.",
   "# Hi, I'm Alex\n\nQA lead and test automation engineer. I build test suites, CI quality gates and tools that make releases safer.\n\n**Featured projects**\n- **testpilot**: an AI agent that writes pytest tests until coverage and mutation targets are met (92% mutation score on pure modules)\n- **intrusion-watch**: detects brute-force logins from server logs; 3 scenarios tested end to end\n- **shiftboard**: shift planning API with Playwright and API tests running in GitHub Actions\n\n**Daily tools**: Python, pytest, Playwright, GitHub Actions, Docker, SQL, Jira\n\n**Contact**: LinkedIn (link) · email (link)\n\nPinned, in order: testpilot, shiftboard, intrusion-watch, integrity-guard, secret-auditor, Python-Course.",
   ["Under 150 words, with the target roles in the first line", "Three projects, each with a problem and a measurable result", "Pinned repositories match the jobs you apply for, best first", "Contact details are present"]),
 "A13.3b": ("text", [
   "Use one structure for every answer: a one-sentence answer, the reason, then a short example from your own work.",
   "For flaky tests, show a process: measure (rerun to confirm), isolate (run alone and in order), find the cause (timing, shared state, environment, data), fix it or quarantine it with an owner.",
   "For \"is the suite good?\", go beyond coverage: escaped defects, mutation testing, time to feedback and how often tests fail for the wrong reason."],
   "Interviewers listen for judgement and examples more than definitions. Practising out loud turns knowledge into fluent answers.",
   "1. Automate what is repeated, stable and high-risk (regression, smoke, API contracts, data checks); keep exploratory testing, usability and one-off checks manual. I start from risk and frequency, not from the UI.\n2. A fixture is reusable setup that pytest injects by name, with its own scope and cleanup after yield; setup copied into each test drifts and hides intent.\n3. Fake: a working lightweight version (an in-memory repository). Stub: returns canned answers. Mock: records calls so the test can assert how it was used. I prefer fakes and check outcomes; mocks only for interactions that are the point, like sending an email.\n4. Flaky means the result changes without a code change: timing, shared state, order dependence, environment, data. Confirm by rerunning, isolate, fix the cause; quarantine with an owner and a ticket if it cannot be fixed at once, never retry silently.\n5. POST with valid data and check 201, the response body against the schema and the Location header; then GET it back; then invalid input (400 or 422), duplicates (409), no auth (401), wrong user (403 or 404), and idempotency where it matters.\n6. Coverage shows what ran, not what was checked. I look at mutation score on critical code, defects that escaped to production, how fast the suite gives feedback, and the rate of false failures.",
   ["Each answer has a direct one-line answer first", "Each answer includes a concrete example", "The flaky-test answer describes a process, not just \"add retries\"", "The \"good suite\" answer goes beyond coverage"]),
 "A13.4b": ("text", [
   "Ask what is different about the failing runs: timing (CI is slower), order (suite versus alone), time of day, shared environments, data.",
   "Prove a cause before fixing it: rerun 50 times, run in a different order, freeze the clock, use a fresh database.",
   "The fix removes the cause: wait for a state instead of sleeping, isolate state per test, use UTC and fixed clocks, unique test data per run."],
   "Methodical diagnosis is what separates a senior tester from someone who adds retries until the build goes green.",
   "1. The click races the page: the element is not ready on slower CI machines. Prove with tracing or by slowing the network; fix with a web-first assertion or locator action that auto-waits (expect(...).to_be_visible()), never sleep.\n2. Order dependence through shared state (a global, a database row, a file left behind). Prove by running the suite in random order (pytest-randomly) and bisecting; fix with per-test fixtures and cleanup.\n3. Time zones: local evening is already tomorrow in UTC. Prove by freezing the clock at 23:30 local; fix by using UTC everywhere and injecting the clock.\n4. Shared staging environment: tests collide on the same records. Prove from logs and timestamps; fix with unique data per run (prefixes or UUIDs), or ephemeral environments.\n5. The test depends on the database contents. Prove by adding a record and rerunning; fix by seeding the data the test needs and asserting on that, not on the whole result set.",
   ["Each scenario names a likely cause", "Each scenario says how to prove the cause before fixing it", "No fix relies on longer sleeps or blind retries"]),
 "A13.5a": ("text", [
   "Start from risk: what would hurt users or the business most if it broke? Test that first and deepest.",
   "Use the test pyramid as a budget: many fast unit tests, fewer API tests, a handful of end-to-end journeys.",
   "End with explicit release criteria, so \"can we ship?\" has an agreed answer before the pressure starts."],
   "A one-page strategy shows you can make trade-offs, which is the core of QA leadership.",
   "Test strategy: Shiftboard v1\n\nScope: shift creation, overlap rules, tip split, schedule page. Out: accounts, PDF export, mobile.\nRisks first: money (tip split must sum exactly), overlapping shifts, time zones and daylight saving, concurrent edits.\nLevels: about 120 unit tests (rules, tip split with property tests), 30 API tests (every status code in the contract), 6 Playwright journeys (add, refuse overlap, split tips, schedule view, error messages, mobile width).\nPipeline: on every pull request lint, types, unit and API tests (under 4 minutes); nightly browser tests on three browsers plus a 20-minute load smoke test.\nEnvironments and data: ephemeral database per run, seeded factories, UTC clock injected.\nMetrics: escaped defects per release, flaky-run rate (under 1%), pull request feedback time (under 10 minutes), mutation score on the rules module.\nStop the release if: any money or overlap test fails, a P1 bug is open, or the flaky rate is above 3% (results cannot be trusted).",
   ["Scope and out-of-scope are explicit", "Risks are prioritised with a reason", "Test levels have rough numbers and a pipeline split", "Metrics and stop-the-release criteria are stated"]),
 "A13.5b": ("text", [
   "Situation and task in two sentences; spend most of the time on your actions; end with a measurable result.",
   "Use \"I\" for what you did, even in team work, and say what you would do differently next time.",
   "Prepare one story for each common theme (automation, incident, people, conflict, failure); many questions can be answered with one of them."],
   "STAR stories turn experience into evidence. Numbers in the result make them memorable and believable.",
   "Story 1, automation. Situation: the regression pass before each release took two testers three days. Task: shorten it without losing coverage of the riskiest flows. Action: I ranked the test cases by risk and frequency, automated the top 40 as API and browser tests in CI, and kept exploratory sessions for new features. Result: the regression pass dropped to half a day, and releases moved from monthly to every two weeks.\n\nStory 2, incident. Situation: customers reported duplicate charges after a release. Task: stop the damage and find the cause. Action: I reproduced it with a retried payment request, showed the endpoint was not idempotent, coordinated a hotfix and added an idempotency test to the suite. Result: fixed within six hours, refunds issued the same day, and the class of bug covered by an automated check.\n\nStory 3, people. Situation: a new team needed testers fast. Task: hire and onboard them without slowing the release. Action: I wrote the role profile, ran the interviews, created an onboarding checklist and paired with each new tester for their first week. Result: three testers productive within a month, and the checklist reused for every later hire.",
   ["Three stories: automation, incident, people", "Each result contains a number", "Each story is under 150 words and uses \"I\" for your actions"]),
}

AUTO = {
 "A13.1a": {"hints": ["Split off the header with message.split(\"\\n\")[0], and handle the empty message first.",
                       "One regular expression can check the whole header shape: ^([a-z]+)(\\([a-z0-9-]+\\))?(!)?: (\\S.*)$ with named groups.",
                       "Collect problems in a list in the documented order; return early only for empty and format."],
            "explain": "Validating the header shape first means the later rules can trust the named groups. Each remaining rule appends its code in the documented order, so the result is predictable and easy to test. Typical slips: making the scope required, checking 72 with >= instead of >, and forgetting that a body needs a blank line after the header."},
 "A13.2a": {"hints": ["Walk the lines once, flipping an in_code flag on every line that starts with ```; skip lines while it is set.",
                       "Keep the first non-empty line outside code for the title check, and collect the lower-cased text of ## and ### headings.",
                       "Compute the score from the parts, then clamp with max(0, score)."],
            "explain": "One pass with an in-code flag handles the trickiest rule: headings inside fenced examples must not count. Matching keywords rather than exact headings accepts the many ways people name sections (Installation, Quick start, Running the tests). Clamping the score keeps it meaningful for very poor READMEs."},
 "A13.3a": {"hints": ["Test the exact boundaries: 1 kg costs 500, 30 kg is accepted, 0 and just over 30 raise ValueError.",
                       "Partial kilograms round up: test 1.2 kg and a value just over a whole kilogram like 2.01.",
                       "Express must double the price; with 1 kg doubling and adding 500 give the same answer, so test express on a heavier parcel."],
            "explain": "Each broken version breaks one rule at a boundary or in a specific case, which is exactly where good tests look. The express mutant is the instructive one: a test with a 1 kg parcel cannot tell doubling from adding 500, so you need a case where the two differ. This way of checking tests against deliberate bugs is mutation testing, and it is a strong answer to \"how do you know your tests are good?\"."},
 "A13.4a": {"hints": ["Record start = clock() once, then loop: call the condition, return its value if truthy.",
                       "Check the deadline after a failed attempt, not before the first one, so a 2 s timeout with 0.5 s interval gives 5 attempts.",
                       "Call the sleep parameter, never time.sleep, and do not wrap condition() in try/except."],
            "explain": "Injecting the clock and sleep functions makes time controllable, so the tests run instantly and deterministically, which is the same reason Playwright and other tools are testable. Returning the condition's value lets callers use the result (the element, the rows) directly. Letting exceptions propagate keeps real bugs visible instead of turning them into timeouts."},
}

QUIZ = [
 ("Which commit message follows Conventional Commits?", ["fix(api): handle empty request body", "Fixed the API bug.", "FIX: api empty body", "fix - handle empty body"], 0,
  "type(scope): summary in lower case, with no full stop, is the convention tools parse for changelogs and version bumps."),
 ("Why tag a release (for example v0.1.0) instead of telling people to use the latest main branch?", ["A tag points at one exact commit, so everyone tests and installs the same version", "Tags make the repository smaller", "GitHub deletes untagged commits", "Tags run the tests automatically"], 0,
  "A tag is a stable, named reference; main keeps moving."),
 ("What should the first lines of a project README answer?", ["What the project does and why someone would use it", "The full history of the project", "Every function's parameters", "The licence text"], 0,
  "Reviewers decide in seconds; install, usage and details come after the pitch."),
 ("Which line belongs in a .gitignore for a Python project?", [".venv/", "README.md", "pyproject.toml", "tests/"], 0,
  "Virtual environments, caches and secrets stay out of version control; project files go in."),
 ("A test for a discount that starts at 100 uses only the totals 50 and 200. What is the main risk?", ["It cannot tell >= from >, so an off-by-one bug at 100 goes unnoticed", "It runs too slowly", "It is too hard to read", "It will fail on correct code"], 0,
  "Boundary values (100 and just below) are where off-by-one bugs hide."),
 ("What is mutation testing?", ["Running your tests against deliberately broken versions of the code to check they fail", "Changing tests randomly to find bugs", "Testing code that changes at run time", "Measuring how many lines ran"], 0,
  "If a broken version still passes, your tests are missing a case."),
 ("Why does page.wait_for_timeout(500) before a click make a test flaky?", ["The page is sometimes slower than 500 ms on CI, and the wait wastes time when it is faster", "Playwright forbids waiting", "It clicks twice", "It only works in headed mode"], 0,
  "Wait for a condition (auto-waiting locators and web-first assertions), not for a fixed time."),
 ("A test passes alone but fails in the full suite. What is the most likely cause?", ["Shared state left by another test (order dependence)", "The test is too short", "The CPU is too fast", "pytest is out of date"], 0,
  "Run in random order and bisect to find the test that leaks state, then isolate with fixtures."),
 ("Which metric best reflects quality as users experience it?", ["Defect escape rate (bugs found after release versus before)", "Number of test cases written", "Lines of test code", "Hours spent testing"], 0,
  "Counts of tests or hours are activity; escaped defects are outcomes."),
 ("In a STAR story, where should most of the time go?", ["Action: what you did and why", "Situation: the company background", "Task: the job description", "Result: the team's achievements without your part"], 0,
  "Keep situation and task short, spend the time on your actions, and end with a measurable result."),
]


def run_example(code):
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=60, cwd=d)
    if r.returncode != 0:
        raise SystemExit("example failed:\n" + r.stderr)
    return r.stdout.rstrip("\n")


def main():
    d = json.load(open(os.path.join(HERE, "pycontent.json")))
    for k in [k for k in d["lessons"] if k.startswith("A13.")]:
        del d["lessons"][k]
    for coll in ("grade", "chk"):
        for k in [k for k in d[coll] if k.startswith("A13.")]:
            del d[coll][k]
    d["quiz"].pop("a13", None)

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
                lesson["exercises"][eid] = {"hints": AUTO[eid]["hints"], "lang": "python", "solution": b3.SOLUTIONS[eid],
                                            "explain": AUTO[eid]["explain"]}
                sp = dict(b3.SPECS[eid])
                d["grade"][eid] = sp
            else:
                lang, hints, why, sol, chk = TEXT_SOLUTIONS[eid]
                lesson["exercises"][eid] = {"hints": hints, "lang": lang, "solution": sol, "explain": why}
                d["chk"][eid] = chk
        d["lessons"][L["id"]] = lesson
    d["quiz"]["a13"] = [{"id": f"a13-{n + 1:02d}", "type": "single", "pool": "quiz", "prompt": q, "code": "",
                         "options": opts, "answer": [ans], "explain": ex} for n, (q, opts, ans, ex) in enumerate(QUIZ)]
    json.dump(d, open(os.path.join(HERE, "pycontent.json"), "w"), ensure_ascii=False)

    page = open(os.path.join(HERE, "course.html"), encoding="utf-8").read()
    # module list
    m = re.search(r"var MA=(\[.*?\]);\n", page)
    ma = json.loads(m.group(1))
    ma = [x for x in ma if x["id"] != "a13"] + [MODULE]
    page = page[:m.start(1)] + json.dumps(ma, ensure_ascii=False) + page[m.end(1):]
    # course grouping, level, content
    if '"a13"' not in page.split("var COURSES=[")[1].split("];")[0]:
        page = page.replace('  {code:"PY290",t:"Capstone Project",y:2,mods:["a12"],studio:true},',
                            '  {code:"PY290",t:"Capstone Project",y:2,mods:["a12"],studio:true},\n  {code:"PY295",t:"Career Toolkit: Git, Portfolio and QA Interviews",y:2,mods:["a13"]},')
    if "a13:" not in page:
        page = page.replace("a11:4,a12:5};", "a11:4,a12:5,a13:3};")
    i = page.find("window.PYCC_CONTENT=") + len("window.PYCC_CONTENT=")
    j = page.find(";</script>", i)
    c = json.loads(page[i:j].replace("<\\!", "<!"))
    for k in ("lessons", "grade", "chk", "quiz"):
        c[k] = d[k]
    page = page[:i] + json.dumps(c).replace("</", "<\\/").replace("<!", "<\\!") + page[j:]
    open(os.path.join(HERE, "course.html"), "w", encoding="utf-8").write(page)
    print("A13 added:", len(LESSONS), "lessons,", sum(len(L["ex"]) for L in LESSONS), "exercises,", len(QUIZ), "quiz questions")


if __name__ == "__main__":
    main()
