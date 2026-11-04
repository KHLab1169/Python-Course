# Python Course

Python curriculum style application for studying. Runs as a standalone app on my own computer.

- **Track 1** follows *Beginning Python* by Magnus Lie Hetland
- **Track 2** follows [roadmap.sh/python](https://roadmap.sh/python)
- **Track 3** is portfolio projects

Includes worked examples, hints, solutions, an in-browser Python editor with autograded
tests (Pyodide, works offline), chapter quizzes, course exams, and PCEP / PCAP practice exams.

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

## What's different from the online version

- No cloud sync: progress lives in the browser on this computer (use Export/Import).
- The "Ask the TA" feedback panel needs Claude, so it only appears in the online version.
