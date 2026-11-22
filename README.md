# Python Course

Python curriculum style application for studying. Runs as a standalone app on my own computer.

- **Track 1** follows *Beginning Python* by Magnus Lie Hetland
- **Track 2** follows [roadmap.sh/python](https://roadmap.sh/python)
- **Track 3** is portfolio projects
- **PY295 Career toolkit**: Git and pull requests, portfolio READMEs, and QA automation
  interview drills (pytest fixtures, waits instead of sleeps, flaky-test diagnosis, STAR answers)

Includes worked examples, hints, solutions, an in-browser Python editor with autograded
tests (Pyodide, works offline), chapter quizzes, course exams, and PCEP / PCAP practice exams.

## Features

- **Modern design** throughout: soft cards, gradient accents, pill navigation, and matching light and dark themes.
- **Map** (the first tab): a modern dashboard-poster of your progress (stats, a module donut,
  ringed module badges) and a roadmap timeline of every module and lesson, per track. Each box opens that lesson in the
  curriculum and fills in as you complete lessons (next lesson highlighted, reviews due marked).
- **Code editor**: syntax colours, line numbers, auto-indent, Tab / Shift+Tab, Ctrl+/ to comment,
  adjustable text size, drag the corner to resize. Ctrl+Enter runs, Ctrl+Shift+Enter submits.
- **Errors point to the line**: after a failed run or submission the line is marked in red,
  with a *Go to line* button (also for answers split into several files).
- **Compare with model answer**: side-by-side view once you pass or open the solution.
- **Failure details**: a failed test shows what was typed, what your code gave, and what was
  expected, instead of just "failed".
- **Style notes** (not graded) beside the test results: unused imports, `== None`, shadowed
  built-ins, mutable defaults, very long functions and similar.
- **Points** per module: one per test passed, two per finished exercise without tests, one per
  quick check answered correctly.
- **Practice problem sets**: an extra autograded exercise in every Track 1 lesson, written as a
  specification with examples and edge cases.
- **Quick checks**: short questions after many worked examples; the example's output stays hidden
  until you answer.
- **Checklists and basic checks** for projects and other exercises without full tests.
- **Reviews with tests**: a due review asks you to solve a past exercise again from the starter
  code; passing the tests completes it.
- **Weekly report** on the Overview, **search** (Ctrl+K or /), **focus mode** in each lesson,
  and **Grades → Download my answers (.zip)** to keep all your code as `.py` files.
- Answers can hold several files, each after a marker line such as `# --- greetings.py ---`.

## Run it

You need Python 3 installed (nothing else, and no internet once downloaded).

| System | Do this |
|---|---|
| Windows | Double-click `start-windows.bat` |
| macOS / Linux | Double-click `start-mac-linux.command` (or run `python3 start.py`) |

Your browser opens at **http://127.0.0.1:8765**. Keep the small window open while you study.

> Opening `index.html` directly by double-clicking won't work: browsers block the Python
> engine from loading off `file://`. Always use a start script.

## Progress

- Progress saves in your browser automatically.
- On first launch the app loads `progress.json` (a snapshot of my progress from the online version).
- **Grades → Back up your progress** exports or imports a progress file. Use it to move
  between computers or browsers, or between this app and the online page.
- To back up progress to GitHub: export, save the file over `progress.json`, commit and push.

## Source

The expanded lessons (the idea, worked examples 2 and 3, common mistakes, key points) are in
`source/lessons/*.txt`, and the quick check for each new example is in `source/checks/*.txt`.
`deep_build.py` runs every example for its real output, `checks_build.py` attaches the quick
checks (failing if a "predict" answer isn't really in the output, or if a `RUN:` line gives a
different result), and `deep_merge.py` puts both into the page:

    python3 deep_build.py                            # writes deep.json
    python3 checks_build.py checks deep.json         # adds the quick checks
    python3 deep_merge.py ../index.html deep.json    # updates the app

The autograder's Python side is `grader_src.py` (embedded in `py-worker.js`). The practice
problem sets and the career module's tests are in `specs/`, each with model solutions and wrong
answers that must fail; `harness.py specs/<file>.py` checks both. `practice_add.py` and
`career_add.py` merge them into the course. These are authoring scripts: they expect the
course page (`course.html`) and its content file (`pycontent.json`) next to them.

## What's different from the online version

- No cloud sync: progress lives in the browser on this computer (use Export/Import).
- The "Ask the TA" feedback panel needs Claude, so it only appears in the online version.
  Here each lesson shows a *Stuck?* panel with next steps and related lessons instead.
- Programs that need packages (Flask, requests, tkinter...) can be graded here but not tried
  out with Run: use your own Python for those.
