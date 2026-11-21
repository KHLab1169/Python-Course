"""Practice exercises for Track 1, chapters 1 to 5: small programs written to a CS50-style specification.
Each entry: lesson, title, prompt (spec), starter, solution, cases, wrong answers, hints, explanation."""
SOLUTIONS, SPECS, BAD, META = {}, {}, {}, {}


def TAIL(stdin, *want):
    """Check the last printed lines exactly. The program is rerun with each input() prompt on its own line,
    so prompts never get mixed into the answer lines."""
    return ("WRAP = 'import builtins as _bi\\n_real_input = _bi.input\\ndef input(prompt=\\'\\'):\\n    return _real_input(str(prompt) + \\'\\\\n\\' if prompt else \\'\\')\\n'\n"
            f"want = {list(want)!r}\n"
            f"clean = rerun(stdin={stdin!r}, source=WRAP + code)\n"
            "lines = [l.rstrip() for l in clean.rstrip().split('\\n')] if clean.strip() else []\n"
            "last_lines = lines[-len(want):]\n"
            "assert last_lines == want, 'The last line' + ('s' if len(want) > 1 else '') + ' printed should be: ' + ' / '.join(want)\n")


def ex(lid, title, prompt, solution, cases, bad, hints, explain, main=True, starter=""):
    eid = lid + ("d" if lid == "6.6" else "c")
    SOLUTIONS[eid] = solution
    SPECS[eid] = {"main": main, "starter": starter, "cases": [dict(c) for c in cases]}
    BAD[eid] = bad
    META[eid] = {"lesson": lid, "title": "Practice: " + title, "prompt": prompt, "hints": hints, "explain": explain}


def case(name, stdin, *want, argv=None):
    c = {"name": name, "stdin": stdin, "check": TAIL(stdin, *want)}
    if argv is not None:
        c["argv"] = argv
    return c


# ---------------------------------------------------------------- chapter 1
ex("1.1", "Minutes in some days",
   "Write a program that reads a whole number of days and prints how many minutes that is.\n\n"
   "Input: one line with a whole number of days.\n\n"
   "Output: the number of minutes, alone on the last line.\n\n"
   "Examples:\n- 365 prints 525600\n- 1 prints 1440\n\n"
   "Edge cases: 0 days prints 0.",
   'days = int(input("Days: "))\nprint(days * 24 * 60)\n',
   [case("365 days", "365\n", "525600"), case("1 day", "1\n", "1440"), case("0 days", "0\n", "0")],
   ['days = input("Days: ")\nprint(days * 24 * 60)\n', 'days = int(input("Days: "))\nprint(days * 24)\n'],
   ["input() gives text: convert it with int() before doing arithmetic.", "A day has 24 hours and an hour has 60 minutes.", "Print only the number, so it ends up on the last line."],
   "int() turns the typed text into a number, then one multiplication does the work. Forgetting int() is the classic mistake: \"365\" * 1440 repeats the text instead of multiplying.")

ex("1.2", "Pack the eggs",
   "Write a program that reads a number of eggs and a box size, then prints how many full boxes you can fill and how many eggs are left over.\n\n"
   "Input: two lines, the number of eggs and then the box size, both whole numbers.\n\n"
   "Output: one line in exactly this form: 4 boxes, 2 left over\n\n"
   "Examples:\n- 50 and 12 print 4 boxes, 2 left over\n- 24 and 6 print 4 boxes, 0 left over\n\n"
   "Edge cases: fewer eggs than one box (5 and 12) prints 0 boxes, 5 left over.",
   'eggs = int(input("Eggs: "))\nsize = int(input("Box size: "))\nprint(eggs // size, "boxes,", eggs % size, "left over")\n',
   [case("50 eggs in 12s", "50\n12\n", "4 boxes, 2 left over"), case("24 eggs in 6s", "24\n6\n", "4 boxes, 0 left over"), case("Fewer than one box", "5\n12\n", "0 boxes, 5 left over")],
   ['eggs = int(input())\nsize = int(input())\nprint(eggs / size, "boxes,", eggs % size, "left over")\n',
    'eggs = int(input())\nsize = int(input())\nprint(eggs // size, "boxes,", size % eggs, "left over")\n'],
   ["// gives the number of whole boxes; % gives what is left.", "print() with several values puts a space between them, which matches the format.", "Check 5 eggs and boxes of 12: 5 // 12 is 0 and 5 % 12 is 5."],
   "Floor division and remainder are a pair: (eggs // size) * size + eggs % size always gives back the eggs you started with. Using / would print 4.166666 boxes, which you cannot fill.")

ex("1.3", "An 18% tip",
   "Write a program that reads a restaurant bill and prints an 18% tip, rounded to 2 decimal places with round().\n\n"
   "Input: one line with the bill, which may have decimals.\n\n"
   "Output: the tip, printed with print(round(tip, 2)), on the last line.\n\n"
   "Examples:\n- 42.50 prints 7.65\n- 50 prints 9.0\n\n"
   "Edge cases: a bill of 0 prints 0.0.",
   'bill = float(input("Bill: "))\ntip = bill * 0.18\nprint(round(tip, 2))\n',
   [case("Bill of 42.50", "42.50\n", "7.65"), case("Bill of 50", "50\n", "9.0"), case("Bill of 0", "0\n", "0.0")],
   ['bill = float(input())\nprint(round(bill * 18, 2))\n', 'bill = int(float(input()))\nprint(round(bill * 0.18, 2))\n'],
   ["Use float() because bills have cents.", "18% is 0.18 as a number.", "round(value, 2) keeps two decimals; Python prints 9.0, not 9.00, and that is what the tests expect."],
   "float() accepts decimals, which int() would refuse. Rounding only at the end keeps full precision during the calculation. Formatting such as 9.00 comes in chapter 3.")

ex("1.4", "Area of a circle",
   "Write a program that reads a radius and prints the area of a circle with that radius, using math.pi, rounded to 2 decimal places.\n\n"
   "Input: one line with the radius (it may have decimals).\n\n"
   "Output: the area, printed with print(round(area, 2)).\n\n"
   "Examples:\n- 3 prints 28.27\n- 0.5 prints 0.79\n\n"
   "Edge cases: a radius of 0 prints 0.0.",
   'import math\n\nradius = float(input("Radius: "))\narea = math.pi * radius ** 2\nprint(round(area, 2))\n',
   [case("Radius 3", "3\n", "28.27"), case("Radius 0.5", "0.5\n", "0.79"), case("Radius 0", "0\n", "0.0")],
   ['import math\nr = float(input())\nprint(round(math.pi * r * 2, 2))\n', 'r = float(input())\nprint(round(3.14 * r ** 2, 2))\n'],
   ["import math at the top gives you math.pi.", "The area is pi times the radius squared: radius ** 2.", "Use math.pi, not 3.14: the tests expect the exact value rounded."],
   "math.pi is far more precise than 3.14, which would give 28.26 instead of 28.27 for a radius of 3. ** 2 squares the radius; * 2 would compute part of the circumference instead.")

ex("1.5", "Seconds to hours, minutes and seconds",
   "Write a program that reads a number of seconds and prints it as hours, minutes and seconds.\n\n"
   "Input: one line with a whole number of seconds.\n\n"
   "Output: one line in exactly this form: 1 h 1 min 1 s\n\n"
   "Examples:\n- 3661 prints 1 h 1 min 1 s\n- 59 prints 0 h 0 min 59 s\n\n"
   "Edge cases: 86399 prints 23 h 59 min 59 s; 0 prints 0 h 0 min 0 s.",
   'total = int(input("Seconds: "))\nhours = total // 3600\nminutes = total % 3600 // 60\nseconds = total % 60\nprint(hours, "h", minutes, "min", seconds, "s")\n',
   [case("3661 seconds", "3661\n", "1 h 1 min 1 s"), case("59 seconds", "59\n", "0 h 0 min 59 s"), case("Just under a day", "86399\n", "23 h 59 min 59 s"), case("Zero", "0\n", "0 h 0 min 0 s")],
   ['total = int(input())\nprint(total // 3600, "h", total // 60, "min", total % 60, "s")\n', 'total = int(input())\nprint(total // 3600, "h", total % 60 // 60, "min", total % 60, "s")\n'],
   ["An hour is 3600 seconds: total // 3600 gives the hours.", "What is left after the hours is total % 3600; divide that by 60 for the minutes.", "The seconds are simply total % 60."],
   "Each unit comes from the remainder of the bigger one. The common mistake is total // 60 for the minutes, which counts all the minutes (61) instead of the minutes after the last full hour (1).")

ex("1.6", "A framed word",
   "Write a program that reads a word and prints it inside a frame, then prints its length.\n\n"
   "Input: one line of text.\n\n"
   "Output: two lines. First the text between *** and ***, with one space on each side; then the number of characters in the text.\n\n"
   "Examples:\n- Ada prints *** Ada *** and then 3\n- hello world prints *** hello world *** and then 11\n\n"
   "Edge cases: spaces count as characters.",
   'word = input("Word: ")\nprint("*** " + word + " ***")\nprint(len(word))\n',
   [case("Ada", "Ada\n", "*** Ada ***", "3"), case("Two words", "hello world\n", "*** hello world ***", "11"), case("Spaces count", "a b\n", "*** a b ***", "3")],
   ['word = input()\nprint("***" + word + "***")\nprint(len(word))\n', 'word = input()\nprint("*** " + word + " ***")\nprint(len(word.split()))\n'],
   ["Join strings with +, remembering the spaces inside the quotes.", "len() counts every character, spaces included.", "Two print() calls give two lines."],
   "+ joins strings exactly as written, so the spaces must be part of the literal \"*** \". len() counts characters, not words.")

# ---------------------------------------------------------------- chapter 2
ex("2.1", "First and last letters",
   "Write a program that reads a word and prints its first and last characters, separated by a space.\n\n"
   "Input: one line with at least one character.\n\n"
   "Output: one line with the first character, a space and the last character.\n\n"
   "Examples:\n- Python prints P n\n- racecar prints r r\n\n"
   "Edge cases: a single character prints it twice: x prints x x.",
   'word = input("Word: ")\nprint(word[0], word[-1])\n',
   [case("Python", "Python\n", "P n"), case("racecar", "racecar\n", "r r"), case("One character", "x\n", "x x")],
   ['word = input()\nprint(word[0], word[len(word)])\n', 'word = input()\nprint(word[1], word[-1])\n'],
   ["Positions start at 0, so the first character is word[0].", "word[-1] is the last character, whatever the length.", "print() with two values puts one space between them."],
   "Negative indices count from the end, so word[-1] works for any length. word[len(word)] would be one past the end and raise an IndexError.")

ex("2.2", "Reformat a date",
   "Write a program that reads a date written as YYYY-MM-DD and prints it as DD/MM/YYYY, using slices.\n\n"
   "Input: one line such as 2026-11-20.\n\n"
   "Output: the same date as 20/11/2026.\n\n"
   "Examples:\n- 2026-11-20 prints 20/11/2026\n- 1999-01-05 prints 05/01/1999\n\n"
   "Edge cases: keep leading zeros exactly as typed.",
   'date = input("Date: ")\nprint(date[8:] + "/" + date[5:7] + "/" + date[:4])\n',
   [case("2026-11-20", "2026-11-20\n", "20/11/2026"), case("1999-01-05", "1999-01-05\n", "05/01/1999"), case("2000-12-31", "2000-12-31\n", "31/12/2000")],
   ['d = input()\nprint(d[8:] + "/" + d[4:7] + "/" + d[:4])\n', 'd = input()\nprint(d[8:] + "/" + d[5:7] + "/" + d[:3])\n'],
   ["Positions 0 to 3 hold the year, 4 is a dash, 5 and 6 the month, 7 a dash, 8 and 9 the day.", "A slice [start:end] stops before end, so the year is date[:4].", "Join the parts with + and \"/\"."],
   "Slices take a range that stops before the end index, so date[5:7] is the two month characters. Working with the fixed positions of a known format is a quick, reliable technique.")

ex("2.3", "Underlined names",
   "Write a program that reads a first name and a last name, then prints the full name between two lines of dashes exactly as long as the full name.\n\n"
   "Input: two lines, the first name and the last name.\n\n"
   "Output: three lines: dashes, the full name (first and last separated by one space), dashes again.\n\n"
   "Examples:\n- Ada and Lovelace print ------------, Ada Lovelace, ------------\n- Al and Gore print ------, Al Gore, ------\n\n"
   "Edge cases: the dashes count the space between the names.",
   'first = input("First name: ")\nlast = input("Last name: ")\nfull = first + " " + last\nprint("-" * len(full))\nprint(full)\nprint("-" * len(full))\n',
   [case("Ada Lovelace", "Ada\nLovelace\n", "------------", "Ada Lovelace", "------------"), case("Al Gore", "Al\nGore\n", "-------", "Al Gore", "-------")],
   ['f = input()\nl = input()\nfull = f + " " + l\nprint("-" * len(f + l))\nprint(full)\nprint("-" * len(f + l))\n', 'f = input()\nl = input()\nprint("-" * 10)\nprint(f + " " + l)\nprint("-" * 10)\n'],
   ["Build the full name first, with a space in the middle.", "\"-\" * n repeats the dash n times.", "Use len() of the full name, so the space counts."],
   "Multiplying a string repeats it, and len() of the joined name includes the space, so the dashes line up exactly. Measuring the two names separately would be one dash short.")

ex("2.4", "Swap the ends",
   "Write a program that reads four lines into a list, swaps the first and last items by assigning to their indices, and prints the list.\n\n"
   "Input: four lines of text.\n\n"
   "Output: the changed list, printed with print(items).\n\n"
   "Examples:\n- a, b, c, d print ['d', 'b', 'c', 'a']\n- tea, cake, soup, jam print ['jam', 'cake', 'soup', 'tea']\n\n"
   "Edge cases: identical first and last items stay the same.",
   'items = [input(), input(), input(), input()]\nfirst = items[0]\nitems[0] = items[-1]\nitems[-1] = first\nprint(items)\n',
   [case("a b c d", "a\nb\nc\nd\n", "['d', 'b', 'c', 'a']"), case("Food", "tea\ncake\nsoup\njam\n", "['jam', 'cake', 'soup', 'tea']"), case("Same ends", "x\ny\nz\nx\n", "['x', 'y', 'z', 'x']")],
   ['items = [input(), input(), input(), input()]\nitems[0] = items[-1]\nitems[-1] = items[0]\nprint(items)\n', 'items = [input(), input(), input(), input()]\nprint(items)\n'],
   ["Build the list with four input() calls inside square brackets.", "Save the first item in a variable before overwriting it.", "Then assign items[0] and items[-1]."],
   "Lists can be changed in place by index. Without the temporary variable, the first assignment overwrites the value you still need, and both ends end up the same.")

ex("2.5", "Sorted, then without the maximum",
   "Write a program that reads five whole numbers, sorts them with the sort method, prints the list, removes the largest with pop(), and prints the list again.\n\n"
   "Input: five lines, each a whole number.\n\n"
   "Output: two lines: the sorted list, then the list without its largest number.\n\n"
   "Examples:\n- 3, 9, 1, 7, 5 print [1, 3, 5, 7, 9] and then [1, 3, 5, 7]\n\n"
   "Edge cases: duplicates stay: 2, 2, 2, 1, 2 print [1, 2, 2, 2, 2] and then [1, 2, 2, 2].",
   'numbers = [int(input()), int(input()), int(input()), int(input()), int(input())]\nnumbers.sort()\nprint(numbers)\nnumbers.pop()\nprint(numbers)\n',
   [case("Five numbers", "3\n9\n1\n7\n5\n", "[1, 3, 5, 7, 9]", "[1, 3, 5, 7]"), case("Duplicates", "2\n2\n2\n1\n2\n", "[1, 2, 2, 2, 2]", "[1, 2, 2, 2]"), case("Negatives", "-1\n0\n-5\n4\n4\n", "[-5, -1, 0, 4, 4]", "[-5, -1, 0, 4]")],
   ['n = [input(), input(), input(), input(), input()]\nn.sort()\nprint(n)\nn.pop()\nprint(n)\n', 'n = [int(input()), int(input()), int(input()), int(input()), int(input())]\nn.sort()\nprint(n)\nn.pop(0)\nprint(n)\n'],
   ["Convert each line with int(), or the numbers sort as text (\"10\" before \"9\").", "numbers.sort() changes the list itself and returns None.", "After sorting, the largest number is last, and pop() removes the last item."],
   "Sorting first puts the maximum at the end, where pop() removes it in one step. Sorting text instead of numbers is the usual trap: as text, \"-5\" and \"10\" sort in surprising places.")

ex("2.6", "A point as a tuple",
   "Write a program that reads x and y, stores them in a tuple, prints the tuple, then prints the distance from (0, 0) rounded to 2 decimals.\n\n"
   "Input: two lines, x and y, both whole numbers.\n\n"
   "Output: two lines: the tuple, then the distance.\n\n"
   "Examples:\n- 3 and 4 print (3, 4) and then 5.0\n- 1 and 1 print (1, 1) and then 1.41\n\n"
   "Edge cases: negative coordinates work: -6 and 8 print (-6, 8) and then 10.0.",
   'point = (int(input("x: ")), int(input("y: ")))\nprint(point)\nprint(round((point[0] ** 2 + point[1] ** 2) ** 0.5, 2))\n',
   [case("3 and 4", "3\n4\n", "(3, 4)", "5.0"), case("1 and 1", "1\n1\n", "(1, 1)", "1.41"), case("Negative x", "-6\n8\n", "(-6, 8)", "10.0")],
   ['p = [int(input()), int(input())]\nprint(p)\nprint(round((p[0] ** 2 + p[1] ** 2) ** 0.5, 2))\n', 'p = (int(input()), int(input()))\nprint(p)\nprint(round((p[0] + p[1]) ** 0.5, 2))\n'],
   ["Parentheses with a comma make a tuple: (x, y).", "The distance is the square root of x squared plus y squared.", "** 0.5 takes a square root."],
   "A tuple fits a point well: two values that belong together and should not change. Squaring before adding matters because negative coordinates would otherwise reduce the distance.")

# ---------------------------------------------------------------- chapter 3
ex("3.1", "Reversed and palindrome",
   "Write a program that reads a word, prints it reversed, then prints whether it reads the same both ways.\n\n"
   "Input: one line of text.\n\n"
   "Output: two lines: the reversed text, then True or False.\n\n"
   "Examples:\n- racecar prints racecar and then True\n- Python prints nohtyP and then False\n\n"
   "Edge cases: the check is exact, so Anna prints annA and then False.",
   'word = input("Word: ")\nprint(word[::-1])\nprint(word == word[::-1])\n',
   [case("racecar", "racecar\n", "racecar", "True"), case("Python", "Python\n", "nohtyP", "False"), case("Case matters", "Anna\n", "annA", "False")],
   ['w = input()\nprint(w[::-1])\nprint(w.lower() == w[::-1].lower())\n', 'w = input()\nprint(w[::1])\nprint(w == w[::-1])\n'],
   ["A slice with step -1 walks backwards: word[::-1].", "Comparing with == gives True or False directly.", "Do not lower-case: the specification asks for an exact comparison."],
   "Strings are sequences, so slicing with a negative step reverses them without a loop. Following the specification exactly (case-sensitive here) is part of the exercise.")

ex("3.2", "A price label",
   "Write a program that reads an item name and a price, then prints a label with an f-string.\n\n"
   "Input: two lines, the item and the price (which may have decimals).\n\n"
   "Output: one line in exactly this form: tea: $2.50\n\n"
   "Examples:\n- tea and 2.5 print tea: $2.50\n- notebook and 12 print notebook: $12.00\n\n"
   "Edge cases: the price always has two decimals: 3.999 prints $4.00.",
   'item = input("Item: ")\nprice = float(input("Price: "))\nprint(f"{item}: ${price:.2f}")\n',
   [case("Tea", "tea\n2.5\n", "tea: $2.50"), case("Notebook", "notebook\n12\n", "notebook: $12.00"), case("Rounds up", "pen\n3.999\n", "pen: $4.00")],
   ['item = input()\nprice = float(input())\nprint(f"{item}: ${price}")\n', 'item = input()\nprice = float(input())\nprint(f"{item}: ${round(price, 2)}")\n'],
   ["Convert the price with float().", "Inside an f-string, {price:.2f} shows exactly two decimals.", "The $ before the brace is plain text."],
   ":.2f always shows two decimals and rounds, which round(price, 2) cannot do on its own (it gives 2.5, not 2.50). Format specs are the right tool for money.")

ex("3.3", "A right-aligned amount",
   "Write a program that reads a number and prints it right-aligned in a field 15 characters wide, with thousands separators and 2 decimals.\n\n"
   "Input: one line with a number.\n\n"
   "Output: the formatted number, exactly 15 characters wide.\n\n"
   "Examples:\n- 1234567.891 prints    1,234,567.89 (3 spaces in front)\n- 5 prints           5.00 (11 spaces in front)\n\n"
   "Edge cases: negative numbers keep their sign: -9876.5 prints      -9,876.50.",
   'value = float(input("Number: "))\nprint(f"{value:>15,.2f}")\n',
   [case("Millions", "1234567.891\n", "   1,234,567.89"), case("Small number", "5\n", "           5.00"), case("Negative", "-9876.5\n", "      -9,876.50")],
   ['v = float(input())\nprint(f"{v:<15,.2f}")\n', 'v = float(input())\nprint(f"{v:>15.2f}")\n'],
   ["The format spec goes after a colon: {value:...}.", "> aligns right, 15 is the width, a comma adds separators and .2f gives two decimals.", "The order inside the spec is alignment, width, comma, precision: >15,.2f"],
   "One format spec handles alignment, width, grouping and precision together. Right-aligned numbers with the same number of decimals line up in columns, which is why reports use them.")

ex("3.4", "Make a slug",
   "Write a program that reads a title and prints a URL slug: the words in lower case, joined with single dashes.\n\n"
   "Input: one line of text.\n\n"
   "Output: the slug on one line.\n\n"
   "Examples:\n- Hello Big World prints hello-big-world\n- Python  for   Everyone prints python-for-everyone\n\n"
   "Edge cases: extra spaces, including at the ends, never produce empty pieces or double dashes.",
   'title = input("Title: ")\nprint("-".join(title.lower().split()))\n',
   [case("Three words", "Hello Big World\n", "hello-big-world"), case("Extra spaces", "Python  for   Everyone\n", "python-for-everyone"), case("Spaces at the ends", "  Tea Time  \n", "tea-time")],
   ['t = input()\nprint("-".join(t.lower().split(" ")))\n', 't = input()\nprint(t.lower().replace(" ", "-"))\n'],
   ["split() with no argument splits on any run of spaces and ignores spaces at the ends.", "\"-\".join(words) puts a dash between the words.", "lower() can come before or after splitting."],
   "split() without an argument is the robust choice: it never produces empty strings, unlike split(\" \") or replace(), which turn double spaces into double dashes.")

ex("3.5", "A valid phone number?",
   "Write a program that reads a phone number, removes spaces and dashes, and prints True if what remains is exactly 10 digits, otherwise False.\n\n"
   "Input: one line of text.\n\n"
   "Output: True or False.\n\n"
   "Examples:\n- 514-555-0199 prints True\n- 514 555 0199 prints True\n- 555-0199 prints False\n\n"
   "Edge cases: letters make it invalid (514-555-01a9 prints False); spaces around the number are fine.",
   'raw = input("Phone: ")\ndigits = raw.strip().replace(" ", "").replace("-", "")\nprint(digits.isdigit() and len(digits) == 10)\n',
   [case("Dashes", "514-555-0199\n", "True"), case("Spaces", "514 555 0199\n", "True"), case("Too short", "555-0199\n", "False"), case("A letter", "514-555-01a9\n", "False"), case("Padded", "  5145550199  \n", "True")],
   ['r = input()\nd = r.replace(" ", "").replace("-", "")\nprint(len(d) == 10)\n', 'r = input()\nd = r.replace("-", "")\nprint(d.isdigit() and len(d) == 10)\n'],
   ["replace() returns a new string; chain two calls to remove spaces and dashes.", "isdigit() is True only if every character is a digit.", "Combine the two conditions with and."],
   "Cleaning the input first, then checking both the characters and the length, catches every invalid case in the examples. Checking only the length would accept letters.")

# ---------------------------------------------------------------- chapter 4
ex("4.1", "Menu lookup",
   "The menu is {\"tea\": 2.5, \"coffee\": 3.0, \"cake\": 4.25}. Write a program that reads an item and prints its price, or not on the menu if it is missing, using the get method.\n\n"
   "Input: one line with an item name.\n\n"
   "Output: the price, or the text not on the menu.\n\n"
   "Examples:\n- tea prints 2.5\n- cake prints 4.25\n- soup prints not on the menu\n\n"
   "Edge cases: names are matched exactly, so Tea is not on the menu.",
   'menu = {"tea": 2.5, "coffee": 3.0, "cake": 4.25}\nitem = input("Item: ")\nprint(menu.get(item, "not on the menu"))\n',
   [case("Tea", "tea\n", "2.5"), case("Cake", "cake\n", "4.25"), case("Missing", "soup\n", "not on the menu"), case("Capital letter", "Tea\n", "not on the menu")],
   ['menu = {"tea": 2.5, "coffee": 3.0, "cake": 4.25}\nprint(menu[input()])\n', 'menu = {"tea": 2.5, "coffee": 3.0, "cake": 4.25}\nprint(menu.get(input()))\n'],
   ["Copy the menu dictionary into your program.", "menu.get(item, default) returns the default when the key is missing.", "Indexing with menu[item] would crash with a KeyError for soup."],
   "get() handles a missing key without an error, and its second argument chooses what to return instead of None. It is the everyday way to look something up when it might not be there.")

ex("4.2", "An order confirmation",
   "Write a program that reads a name and a number of cups, stores them in a dictionary with the keys name and cups, and prints a confirmation with format_map.\n\n"
   "Input: two lines, the name and the number of cups.\n\n"
   "Output: one line in exactly this form: Ada ordered 3 cups.\n\n"
   "Examples:\n- Ada and 3 print Ada ordered 3 cups.\n- Ben and 12 print Ben ordered 12 cups.\n\n"
   "Edge cases: the number is printed as typed (no conversion needed).",
   'order = {"name": input("Name: "), "cups": input("Cups: ")}\nprint("{name} ordered {cups} cups.".format_map(order))\n',
   [case("Ada", "Ada\n3\n", "Ada ordered 3 cups."), case("Ben", "Ben\n12\n", "Ben ordered 12 cups.")],
   ['o = {"name": input(), "cups": input()}\nprint("{name} ordered {cups} cups".format_map(o))\n', 'o = {"name": input(), "cups": input()}\nprint("{cups} ordered {name} cups.".format_map(o))\n'],
   ["Build the dictionary with the two input() calls as values.", "In the template, {name} and {cups} name the keys.", "Mind the full stop at the end of the sentence."],
   "format_map fills each named placeholder from the dictionary, which keeps templates readable when there are many values. The output must match exactly, full stop included.")

ex("4.3", "Count four fruits",
   "Write a program that reads four fruit names and counts them in a dictionary using get, then prints the dictionary.\n\n"
   "Input: four lines, each a fruit name.\n\n"
   "Output: the dictionary, with keys in the order they first appeared.\n\n"
   "Examples:\n- apple, pear, apple, fig print {'apple': 2, 'pear': 1, 'fig': 1}\n\n"
   "Edge cases: four identical names print {'kiwi': 4}.",
   'counts = {}\nfor _ in range(4):\n    fruit = input("Fruit: ")\n    counts[fruit] = counts.get(fruit, 0) + 1\nprint(counts)\n',
   [case("Mixed", "apple\npear\napple\nfig\n", "{'apple': 2, 'pear': 1, 'fig': 1}"), case("All the same", "kiwi\nkiwi\nkiwi\nkiwi\n", "{'kiwi': 4}"), case("All different", "a\nb\nc\nd\n", "{'a': 1, 'b': 1, 'c': 1, 'd': 1}")],
   ['c = {}\nfor _ in range(4):\n    f = input()\n    c[f] = 1\nprint(c)\n', 'c = {}\nfor _ in range(4):\n    f = input()\n    c[f] = c.get(f, 1) + 1\nprint(c)\n'],
   ["Start with an empty dictionary.", "counts.get(fruit, 0) is the count so far, or 0 the first time.", "You can repeat the same two lines four times, or use a loop if you already know one."],
   "get with a default of 0 makes the first count and every later count the same line of code. Dictionaries keep insertion order, so the printed keys follow the order the fruits were typed.")

# ---------------------------------------------------------------- chapter 5
ex("5.1", "Join a date with sep",
   "Write a program that reads a day, a month and a year, then prints them as year-month-day using print with sep.\n\n"
   "Input: three lines: day, month, year.\n\n"
   "Output: one line such as 2026-11-20.\n\n"
   "Examples:\n- 20, 11, 2026 print 2026-11-20\n- 05, 01, 1999 print 1999-01-05\n\n"
   "Edge cases: print the parts exactly as typed.",
   'day = input("Day: ")\nmonth = input("Month: ")\nyear = input("Year: ")\nprint(year, month, day, sep="-")\n',
   [case("2026-11-20", "20\n11\n2026\n", "2026-11-20"), case("Leading zeros", "05\n01\n1999\n", "1999-01-05")],
   ['d = input()\nm = input()\ny = input()\nprint(day := d, m, y, sep="-")\n', 'd = input()\nm = input()\ny = input()\nprint(y, m, d)\n'],
   ["print(a, b, c, sep=\"-\") puts a dash between the values instead of a space.", "Mind the order: year first, then month, then day.", "No conversion is needed: printing the text keeps leading zeros."],
   "sep replaces the space print normally puts between values, so one call builds the date. Keeping the values as text preserves the leading zeros that int() would remove.")

ex("5.2", "Swap two values",
   "Write a program that reads two lines into a and b, swaps them with a single tuple assignment, and prints a and b on one line.\n\n"
   "Input: two lines of text.\n\n"
   "Output: one line: the new a, a space, the new b.\n\n"
   "Examples:\n- left and right print right left\n- 1 and 2 print 2 1\n\n"
   "Edge cases: equal values stay the same.",
   'a = input("a: ")\nb = input("b: ")\na, b = b, a\nprint(a, b)\n',
   [case("Words", "left\nright\n", "right left"), case("Numbers", "1\n2\n", "2 1"), case("Equal", "x\nx\n", "x x")],
   ['a = input()\nb = input()\na = b\nb = a\nprint(a, b)\n', 'a = input()\nb = input()\nprint(a, b)\n'],
   ["a, b = b, a evaluates the right side first, then assigns both names.", "No temporary variable is needed.", "print(a, b) separates them with a space."],
   "Tuple assignment builds (b, a) before assigning anything, so neither value is lost. Two separate assignments would copy the same value into both names.")

ex("5.3", "Letter grades",
   "Write a program that reads a score and prints its letter grade: A for 90 to 100, B for 80 to 89, C for 70 to 79, D for 60 to 69 and F below 60. Scores below 0 or above 100 print invalid.\n\n"
   "Input: one line with a whole number.\n\n"
   "Output: one letter, or the word invalid.\n\n"
   "Examples:\n- 95 prints A\n- 80 prints B\n- 59 prints F\n\n"
   "Edge cases: 100 prints A, 0 prints F, 101 and -1 print invalid.",
   'score = int(input("Score: "))\nif score < 0 or score > 100:\n    print("invalid")\nelif score >= 90:\n    print("A")\nelif score >= 80:\n    print("B")\nelif score >= 70:\n    print("C")\nelif score >= 60:\n    print("D")\nelse:\n    print("F")\n',
   [case("95", "95\n", "A"), case("Exactly 80", "80\n", "B"), case("79", "79\n", "C"), case("60", "60\n", "D"), case("59", "59\n", "F"), case("Edges 100 and 0", "100\n", "A"), case("Zero", "0\n", "F"), case("Too high", "101\n", "invalid"), case("Negative", "-1\n", "invalid")],
   ['s = int(input())\nif s >= 90:\n    print("A")\nelif s >= 80:\n    print("B")\nelif s >= 70:\n    print("C")\nelif s >= 60:\n    print("D")\nelse:\n    print("F")\n',
    's = int(input())\nif s < 0 or s > 100:\n    print("invalid")\nelif s > 90:\n    print("A")\nelif s > 80:\n    print("B")\nelif s > 70:\n    print("C")\nelif s > 60:\n    print("D")\nelse:\n    print("F")\n'],
   ["Check the invalid range first, so later branches only see valid scores.", "Then go from the highest grade down with elif, using >=.", "Only the first true branch runs, so 95 stops at A."],
   "Ordering the branches from the most specific (invalid) and then the highest grade down means each condition only needs a lower bound. Using > instead of >= is the off-by-one bug the boundary tests catch.")

ex("5.4", "Leap years",
   "Write a program that reads a year and prints leap if it is a leap year, otherwise not leap. A year is a leap year if it is divisible by 4 but not by 100, unless it is also divisible by 400.\n\n"
   "Input: one line with a whole number.\n\n"
   "Output: leap or not leap.\n\n"
   "Examples:\n- 2024 prints leap\n- 2026 prints not leap\n\n"
   "Edge cases: 1900 prints not leap; 2000 prints leap.",
   'year = int(input("Year: "))\nif (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:\n    print("leap")\nelse:\n    print("not leap")\n',
   [case("2024", "2024\n", "leap"), case("2026", "2026\n", "not leap"), case("1900", "1900\n", "not leap"), case("2000", "2000\n", "leap")],
   ['y = int(input())\nprint("leap" if y % 4 == 0 else "not leap")\n', 'y = int(input())\nif y % 4 == 0 and y % 100 != 0:\n    print("leap")\nelse:\n    print("not leap")\n'],
   ["% gives the remainder: year % 4 == 0 means divisible by 4.", "Combine the rule with and, or, and brackets to make the grouping clear.", "Test 1900 and 2000: they are the cases a simpler rule gets wrong."],
   "The rule has three parts, and the century years are the boundary cases: 1900 is divisible by 4 but not a leap year, and 2000 is, because it is divisible by 400.")

ex("5.5", "Multiplication table",
   "Write a program that reads a number n and prints its multiplication table from 1 to 10, one line per row.\n\n"
   "Input: one line with a whole number.\n\n"
   "Output: ten lines such as 7 x 1 = 7, ending with 7 x 10 = 70.\n\n"
   "Examples:\n- 7 prints 7 x 1 = 7 up to 7 x 10 = 70\n\n"
   "Edge cases: 0 prints ten lines ending with 0 x 10 = 0.",
   'n = int(input("Number: "))\nfor i in range(1, 11):\n    print(n, "x", i, "=", n * i)\n',
   [case("Table of 7", "7\n", *[f"7 x {i} = {7 * i}" for i in range(1, 11)]), case("Table of 0", "0\n", *[f"0 x {i} = 0" for i in range(1, 11)])],
   ['n = int(input())\nfor i in range(1, 10):\n    print(n, "x", i, "=", n * i)\n', 'n = int(input())\nfor i in range(10):\n    print(n, "x", i, "=", n * i)\n'],
   ["range(1, 11) gives 1 to 10: the end is not included.", "print with several values separates them with spaces, which matches the format.", "Compute n * i inside the loop."],
   "range stops before its end value, so the table needs range(1, 11). Off-by-one ranges are among the most common loop bugs, and the first and last rows are what the tests check.")

ex("5.6", "Total until done",
   "Write a program that reads lines until one of them is done, adds up the lines that are whole numbers, skips any other line with continue, and prints the total.\n\n"
   "Input: any number of lines, then a line done.\n\n"
   "Output: the total, alone on the last line.\n\n"
   "Examples:\n- 3, (empty line), x, 4, done prints 7\n\n"
   "Edge cases: done straight away prints 0; lines after done are never read.",
   'total = 0\nwhile True:\n    line = input("Number or done: ")\n    if line == "done":\n        break\n    if not line.isdigit():\n        continue\n    total += int(line)\nprint(total)\n',
   [case("Skips bad lines", "3\n\nx\n4\ndone\n9\n", "7"), case("Done at once", "done\n", "0"), case("Only numbers", "10\n20\n30\ndone\n", "60")],
   ['t = 0\nwhile True:\n    l = input()\n    if l == "done":\n        break\n    t += int(l)\nprint(t)\n', 't = 0\nfor l in ["3", "4"]:\n    t += int(l)\nprint(t)\n'],
   ["while True with break inside is the natural loop when you do not know how many lines will come.", "Check for done first, then skip anything that is not digits with continue.", "Only add after both checks."],
   "break ends the loop when done arrives, so lines after it are never read. continue skips the empty line and x without crashing on int(). Together they keep the loop body flat and readable.")

ex("5.7", "Squares of even numbers",
   "Write a program that reads a line of whole numbers separated by spaces and prints a list of the squares of the even ones, built with a list comprehension.\n\n"
   "Input: one line of numbers separated by spaces.\n\n"
   "Output: the list.\n\n"
   "Examples:\n- 1 2 3 4 prints [4, 16]\n- 10 7 0 prints [100, 0]\n\n"
   "Edge cases: an empty line prints []; negative even numbers count: -2 prints [4].",
   'numbers = [int(x) for x in input("Numbers: ").split()]\nprint([n * n for n in numbers if n % 2 == 0])\n',
   [case("1 2 3 4", "1 2 3 4\n", "[4, 16]"), case("With zero", "10 7 0\n", "[100, 0]"), case("Empty line", "\n", "[]"), case("Negative", "-2 -3\n", "[4]")],
   ['ns = [int(x) for x in input().split()]\nprint([n * 2 for n in ns if n % 2 == 0])\n', 'ns = [int(x) for x in input().split()]\nprint([n * n for n in ns if n % 2 == 1])\n'],
   ["input().split() gives the pieces; int() turns each into a number.", "The filter goes at the end of the comprehension: if n % 2 == 0.", "n * n (or n ** 2) is the square."],
   "A comprehension with a condition filters and transforms in one readable line. Note that 0 is even, and -2 % 2 is 0 in Python, so both are kept.")

for _eid, _bads in BAD.items():
    for _i, _b in enumerate(_bads):
        assert _b != SOLUTIONS[_eid], f"{_eid} bad#{_i} is identical to the solution"
