"""Practice exercises for Track 1, chapters 6 to 11: functions and classes written to a CS50-style specification."""
SOLUTIONS, SPECS, BAD, META = {}, {}, {}, {}


def ex(lid, title, prompt, solution, cases, bad, hints, explain, starter, main=False):
    eid = lid + ("d" if lid == "6.6" else "c")
    SOLUTIONS[eid] = solution
    SPECS[eid] = {"main": main, "starter": starter, "cases": [{"name": n, "check": c} if isinstance(c, str) else dict(c, name=n) for n, c in cases]}
    BAD[eid] = bad
    META[eid] = {"lesson": lid, "title": "Practice: " + title, "prompt": prompt, "hints": hints, "explain": explain}


# ---------------------------------------------------------------- chapter 6
ex("6.1", "Initials",
   "Write initials(full_name) that returns the initials of a name, each in upper case and followed by a full stop.\n\n"
   "Specification:\n- Words are separated by any amount of whitespace.\n- Each word contributes its first letter, upper-cased, then a full stop.\n- An empty or blank name returns an empty string.\n\n"
   "Examples:\n- initials(\"ada king lovelace\") returns \"A.K.L.\"\n- initials(\"Grace Hopper\") returns \"G.H.\"\n\n"
   "Edge cases: initials(\"  alan   turing \") returns \"A.T.\"; initials(\"\") returns \"\".",
   'def initials(full_name):\n    """Return the initials of full_name, like A.K.L."""\n    return "".join(word[0].upper() + "." for word in full_name.split())\n',
   [("Three words", "assert initials('ada king lovelace') == 'A.K.L.', 'initials(\"ada king lovelace\") should be \"A.K.L.\"'"),
    ("Already capitalised", "assert initials('Grace Hopper') == 'G.H.'"),
    ("Extra spaces", "assert initials('  alan   turing ') == 'A.T.', 'Extra spaces should be ignored'"),
    ("Empty name", "assert initials('') == '' and initials('   ') == '', 'An empty or blank name returns an empty string'")],
   ['def initials(full_name):\n    return "".join(w[0].upper() + "." for w in full_name.split(" "))\n',
    'def initials(full_name):\n    return "".join(w[0] + "." for w in full_name.split())\n'],
   ["split() with no argument handles any amount of whitespace and returns [] for a blank string.", "For each word take word[0].upper() and add a full stop.", "\"\".join(...) glues the pieces together; join of nothing is \"\"."],
   "split() without an argument never produces empty words, so the blank and extra-space cases need no special code. Returning the result (rather than printing it) is what makes the function testable and reusable.",
   'def initials(full_name):\n    """Return the initials of full_name, like A.K.L."""\n    pass\n')

ex("6.2", "Prices with tax, without side effects",
   "Write with_tax(prices, rate) that returns a new list with each price increased by rate percent and rounded to 2 decimals. The original list must not change.\n\n"
   "Specification:\n- rate is a percentage, such as 15 for 15%.\n- Each new price is round(price * (1 + rate / 100), 2).\n- Return a new list; never modify prices.\n\n"
   "Examples:\n- with_tax([10, 20], 15) returns [11.5, 23.0]\n- with_tax([4.99], 0) returns [4.99]\n\n"
   "Edge cases: an empty list returns []; after the call, the caller's list is exactly as before.",
   'def with_tax(prices, rate):\n    """Return a new list of prices increased by rate percent."""\n    return [round(p * (1 + rate / 100), 2) for p in prices]\n',
   [("Adds 15%", "assert with_tax([10, 20], 15) == [11.5, 23.0], 'with_tax([10, 20], 15) should be [11.5, 23.0]'"),
    ("Zero rate", "assert with_tax([4.99], 0) == [4.99]"),
    ("Empty list", "assert with_tax([], 10) == []"),
    ("Original list unchanged", "prices = [10, 20, 30]\nresult = with_tax(prices, 10)\nassert prices == [10, 20, 30], 'with_tax must not change the list it was given'\nassert result is not prices, 'Return a new list, not the same one'")],
   ['def with_tax(prices, rate):\n    for i, p in enumerate(prices):\n        prices[i] = round(p * (1 + rate / 100), 2)\n    return prices\n',
    'def with_tax(prices, rate):\n    return [round(p * rate / 100, 2) for p in prices]\n'],
   ["A list comprehension builds a new list and leaves the original alone.", "15% means multiplying by 1.15, which is 1 + rate / 100.", "Round each price with round(value, 2)."],
   "Changing a list passed in as an argument changes the caller's list too, because both names refer to the same object. Returning a new list avoids that surprise, which is why the test checks both the result and the original.",
   'def with_tax(prices, rate):\n    """Return a new list of prices increased by rate percent."""\n    pass\n')

ex("6.3", "Formatting money with defaults",
   "Write money(amount, currency=\"$\", decimals=2, suffix=\"\") that formats an amount as text.\n\n"
   "Specification:\n- The result is the currency symbol, the amount with thousands separators and exactly decimals decimal places, then the suffix.\n- If suffix is not empty, put one space before it.\n\n"
   "Examples:\n- money(1234.5) returns \"$1,234.50\"\n- money(12, currency=\"€\", decimals=0) returns \"€12\"\n- money(15, suffix=\"per month\") returns \"$15.00 per month\"\n\n"
   "Edge cases: money(0) returns \"$0.00\"; keyword arguments may come in any order.",
   'def money(amount, currency="$", decimals=2, suffix=""):\n    """Format an amount of money."""\n    text = f"{currency}{amount:,.{decimals}f}"\n    return text + " " + suffix if suffix else text\n',
   [("Defaults", "assert money(1234.5) == '$1,234.50', 'money(1234.5) should be \"$1,234.50\"'"),
    ("Currency and decimals", "assert money(12, currency='€', decimals=0) == '€12'"),
    ("Suffix", "assert money(15, suffix='per month') == '$15.00 per month', 'Put one space before the suffix'"),
    ("Zero and keyword order", "assert money(0) == '$0.00'\nassert money(9.999, suffix='each', decimals=1, currency='£') == '£10.0 each'")],
   ['def money(amount, currency="$", decimals=2, suffix=""):\n    return f"{currency}{amount:,.{decimals}f}{suffix}"\n',
    'def money(amount, currency="$", decimals=2, suffix=""):\n    t = f"{currency}{amount:.{decimals}f}"\n    return t + " " + suffix if suffix else t\n'],
   ["Give each optional parameter its default in the def line.", "A format spec can contain a nested field: {amount:,.{decimals}f}.", "Only add the space and suffix when suffix is not empty."],
   "Defaults make the common call short, and keyword arguments let callers change just one option in any order. Nested fields in format specs let the number of decimals come from a variable.",
   'def money(amount, currency="$", decimals=2, suffix=""):\n    """Format an amount of money."""\n    pass\n')

ex("6.4", "An average of any number of values",
   "Write average(*values, ndigits=None) that returns the mean of any number of values.\n\n"
   "Specification:\n- With no values, return None.\n- Otherwise return the sum divided by the count.\n- If ndigits is given, round the result to that many decimals.\n\n"
   "Examples:\n- average(1, 2, 3, 4) returns 2.5\n- average(1, 2, 2, ndigits=2) returns 1.67\n- average() returns None\n\n"
   "Edge cases: ndigits=0 still rounds (average(1, 2, ndigits=0) returns 2.0); a list can be spread in with average(*scores).",
   'def average(*values, ndigits=None):\n    """Return the mean of values, or None when there are none."""\n    if not values:\n        return None\n    mean = sum(values) / len(values)\n    return mean if ndigits is None else round(mean, ndigits)\n',
   [("Four values", "assert average(1, 2, 3, 4) == 2.5"),
    ("Rounding", "assert average(1, 2, 2, ndigits=2) == 1.67, 'average(1, 2, 2, ndigits=2) should be 1.67'"),
    ("No values", "assert average() is None, 'With no values, return None'"),
    ("ndigits=0 still rounds", "assert average(1, 2, ndigits=0) == 2.0, 'ndigits=0 means round to 0 decimals, not no rounding'"),
    ("Spreading a list", "scores = [10, 20, 30]\nassert average(*scores) == 20")],
   ['def average(*values, ndigits=None):\n    if not values:\n        return None\n    m = sum(values) / len(values)\n    return round(m, ndigits) if ndigits else m\n',
    'def average(*values, ndigits=None):\n    m = sum(values) / max(1, len(values))\n    return m if ndigits is None else round(m, ndigits)\n'],
   ["*values collects every positional argument into a tuple.", "Parameters after *values can only be given by name, which is what ndigits needs.", "Compare ndigits with None explicitly: 0 is a valid number of digits but is falsy."],
   "*values accepts any number of arguments, and a parameter after it is keyword-only. Testing ndigits is None rather than just ndigits matters, because 0 is falsy yet still means \"round\".",
   'def average(*values, ndigits=None):\n    """Return the mean of values, or None when there are none."""\n    pass\n')

ex("6.5", "Counters that remember",
   "Write make_counter(start=0, step=1) that returns a function. Each call of the returned function returns the next value: start + step, then start + 2 * step, and so on.\n\n"
   "Specification:\n- Use a closure with nonlocal, not a global variable.\n- Each counter made by make_counter keeps its own count.\n\n"
   "Examples:\n- c = make_counter(); c(), c(), c() return 1, 2, 3\n- d = make_counter(10, 5); d(), d() return 15, 20\n\n"
   "Edge cases: two counters do not affect each other; a negative step counts down.",
   'def make_counter(start=0, step=1):\n    """Return a function that counts from start in steps of step."""\n    value = start\n\n    def counter():\n        nonlocal value\n        value += step\n        return value\n\n    return counter\n',
   [("Counts 1, 2, 3", "c = make_counter()\nassert [c(), c(), c()] == [1, 2, 3], 'A new counter should give 1, 2, 3'"),
    ("Start and step", "d = make_counter(10, 5)\nassert [d(), d()] == [15, 20]"),
    ("Independent counters", "a = make_counter()\nb = make_counter()\na(); a(); a()\nassert b() == 1, 'Each counter keeps its own count'"),
    ("Counting down", "c = make_counter(3, -1)\nassert [c(), c(), c()] == [2, 1, 0]")],
   ['count = 0\ndef make_counter(start=0, step=1):\n    def counter():\n        global count\n        count += step\n        return start + count\n    return counter\n',
    'def make_counter(start=0, step=1):\n    value = start\n    def counter():\n        return value + step\n    return counter\n'],
   ["Store the current value in a variable inside make_counter.", "The inner function needs nonlocal value to change it.", "Return the inner function itself, without calling it."],
   "A closure remembers the variables of the function that created it, so each call to make_counter creates a fresh, private count. A global would be shared by every counter, which the independence test catches.",
   'def make_counter(start=0, step=1):\n    """Return a function that counts from start in steps of step."""\n    pass\n')

ex("6.6", "Flatten any nesting",
   "Write flatten(items) that takes a list which may contain other lists, nested to any depth, and returns one flat list of all the non-list values in order. Use recursion.\n\n"
   "Specification:\n- Only lists count as nesting; strings, tuples and numbers are values.\n- Return a new list.\n\n"
   "Examples:\n- flatten([1, [2, [3, 4]], 5]) returns [1, 2, 3, 4, 5]\n- flatten([[], [[]]]) returns []\n\n"
   "Edge cases: flatten([\"ab\", (1, 2)]) returns [\"ab\", (1, 2)]; flatten([]) returns [].",
   'def flatten(items):\n    """Return the non-list values of a nested list, in order."""\n    flat = []\n    for item in items:\n        if isinstance(item, list):\n            flat.extend(flatten(item))\n        else:\n            flat.append(item)\n    return flat\n',
   [("Nested numbers", "assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]"),
    ("Empty lists vanish", "assert flatten([[], [[]]]) == [] and flatten([]) == []"),
    ("Strings and tuples are values", "assert flatten(['ab', (1, 2)]) == ['ab', (1, 2)], 'Only lists are flattened; strings and tuples stay as values'"),
    ("Deep nesting", "assert flatten([[[[[7]]]], 8]) == [7, 8]")],
   ['def flatten(items):\n    flat = []\n    for item in items:\n        if isinstance(item, list):\n            flat.extend(item)\n        else:\n            flat.append(item)\n    return flat\n',
    'def flatten(items):\n    flat = []\n    for item in items:\n        if hasattr(item, "__iter__"):\n            flat.extend(flatten(list(item)))\n        else:\n            flat.append(item)\n    return flat\n'],
   ["The base case is a value that is not a list: append it.", "For a list, call flatten on it and extend with the result.", "Check with isinstance(item, list), so strings and tuples are not taken apart."],
   "Recursion matches the shape of the data: a nested list is a list of values and smaller nested lists. Checking specifically for lists keeps strings intact; treating anything iterable as nesting would split \"ab\" into letters.",
   'def flatten(items):\n    """Return the non-list values of a nested list, in order."""\n    pass\n')

# ---------------------------------------------------------------- chapter 7
ex("7.1", "Sizes of anything",
   "Write sizes(things) that returns a list of strings describing each object's type name and length, using duck typing.\n\n"
   "Specification:\n- For each object, if len() works on it, produce \"typename: length\" (for example \"list: 3\").\n- If len() raises a TypeError, produce \"typename: no length\".\n- Use type(obj).__name__ for the type name.\n\n"
   "Examples:\n- sizes([\"abc\", [1, 2], {\"a\": 1}]) returns [\"str: 3\", \"list: 2\", \"dict: 1\"]\n- sizes([42]) returns [\"int: no length\"]\n\n"
   "Edge cases: objects of your own classes with __len__ work too.",
   'def sizes(things):\n    """Describe each object as \'typename: length\'."""\n    result = []\n    for thing in things:\n        name = type(thing).__name__\n        try:\n            result.append(f"{name}: {len(thing)}")\n        except TypeError:\n            result.append(f"{name}: no length")\n    return result\n',
   [("Built-in types", "assert sizes(['abc', [1, 2], {'a': 1}]) == ['str: 3', 'list: 2', 'dict: 1']"),
    ("No length", "assert sizes([42, None]) == ['int: no length', 'NoneType: no length']"),
    ("Your own class", "class Box:\n    def __len__(self):\n        return 7\nassert sizes([Box(), range(4)]) == ['Box: 7', 'range: 4'], 'Any object with __len__ works'")],
   ['def sizes(things):\n    out = []\n    for t in things:\n        if isinstance(t, (str, list, dict)):\n            out.append(f"{type(t).__name__}: {len(t)}")\n        else:\n            out.append(f"{type(t).__name__}: no length")\n    return out\n',
    'def sizes(things):\n    return [f"{type(t).__name__}: {len(t)}" if hasattr(t, "__len__") else "no length" for t in things]\n'],
   ["Duck typing means trying len() rather than checking the type first.", "Catch TypeError, which is what len() raises for objects without a length.", "type(thing).__name__ gives names like str, list and Box."],
   "Trying the operation and handling the failure works for every type, including ones written later, while a list of known types misses them. That is duck typing: it matters what an object can do, not what it is.",
   'def sizes(things):\n    """Describe each object as \'typename: length\'."""\n    pass\n')

ex("7.2", "A tally counter class",
   "Write a class Tally that counts things.\n\n"
   "Specification:\n- Tally() starts at 0; Tally(5) starts at 5.\n- add(n=1) adds n and returns the new value. A negative n raises ValueError.\n- reset() sets the value back to 0.\n- The current count is in the attribute value.\n\n"
   "Examples:\n- t = Tally(); t.add(); t.add(3) leaves t.value at 4\n- Tally(5).add(2) returns 7\n\n"
   "Edge cases: each Tally keeps its own value; add(0) is allowed.",
   'class Tally:\n    """A counter that only goes up, until it is reset."""\n\n    def __init__(self, start=0):\n        self.value = start\n\n    def add(self, n=1):\n        if n < 0:\n            raise ValueError("cannot add a negative amount")\n        self.value += n\n        return self.value\n\n    def reset(self):\n        self.value = 0\n',
   [("Counts up", "t = Tally()\nt.add()\nassert t.add(3) == 4 and t.value == 4, 'After add() and add(3) the value should be 4'"),
    ("Starting value", "assert Tally(5).add(2) == 7"),
    ("Reset", "t = Tally(9)\nt.reset()\nassert t.value == 0"),
    ("Negative raises", "t = Tally()\ntry:\n    t.add(-1)\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('add(-1) should raise ValueError')\nassert t.value == 0, 'A refused add must not change the value'"),
    ("Independent objects", "a, b = Tally(), Tally()\na.add(5)\nassert b.value == 0, 'Each Tally has its own value'")],
   ['class Tally:\n    value = 0\n    def __init__(self, start=0):\n        Tally.value = start\n    def add(self, n=1):\n        if n < 0:\n            raise ValueError\n        Tally.value += n\n        return Tally.value\n    def reset(self):\n        Tally.value = 0\n',
    'class Tally:\n    def __init__(self, start=0):\n        self.value = start\n    def add(self, n=1):\n        self.value += n\n        return self.value\n    def reset(self):\n        self.value = 0\n'],
   ["Store the count on self in __init__: self.value = start.", "Check for a negative n before changing anything.", "Methods change self.value; using the class name instead would share one value between all tallies."],
   "Attributes set on self belong to each object, so two tallies count independently. Validating before changing state means a refused call leaves the object exactly as it was.",
   'class Tally:\n    """A counter that only goes up, until it is reset."""\n\n    def __init__(self, start=0):\n        pass\n')

ex("7.3", "A wallet that protects its balance",
   "Write a class Wallet that keeps its balance in a private attribute _balance.\n\n"
   "Specification:\n- Wallet(owner) starts with a balance of 0; the owner is stored in the attribute owner.\n- deposit(amount) adds money; withdraw(amount) removes it. Both raise ValueError if amount is not positive.\n- withdraw raises ValueError if the amount is more than the balance, and leaves the balance unchanged.\n- balance() returns the current balance.\n\n"
   "Examples:\n- w = Wallet(\"Ada\"); w.deposit(50); w.withdraw(20); w.balance() returns 30\n\n"
   "Edge cases: withdrawing exactly the balance is allowed and leaves 0.",
   'class Wallet:\n    """Money in, money out, never below zero."""\n\n    def __init__(self, owner):\n        self.owner = owner\n        self._balance = 0\n\n    def deposit(self, amount):\n        if amount <= 0:\n            raise ValueError("amount must be positive")\n        self._balance += amount\n\n    def withdraw(self, amount):\n        if amount <= 0:\n            raise ValueError("amount must be positive")\n        if amount > self._balance:\n            raise ValueError("not enough money")\n        self._balance -= amount\n\n    def balance(self):\n        return self._balance\n',
   [("Deposit and withdraw", "w = Wallet('Ada')\nw.deposit(50)\nw.withdraw(20)\nassert w.balance() == 30 and w.owner == 'Ada'"),
    ("Cannot overdraw", "w = Wallet('Ben')\nw.deposit(10)\ntry:\n    w.withdraw(11)\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('Withdrawing more than the balance should raise ValueError')\nassert w.balance() == 10, 'A refused withdrawal leaves the balance unchanged'"),
    ("Exact balance", "w = Wallet('Cy')\nw.deposit(10)\nw.withdraw(10)\nassert w.balance() == 0"),
    ("Positive amounts only", "w = Wallet('Dee')\nfor bad in (0, -5):\n    for method in (w.deposit, w.withdraw):\n        try:\n            method(bad)\n        except ValueError:\n            continue\n        raise AssertionError(f'{method.__name__}({bad}) should raise ValueError')"),
    ("Private attribute", "w = Wallet('Eve')\nw.deposit(5)\nassert w._balance == 5, 'Keep the balance in self._balance'")],
   ['class Wallet:\n    def __init__(self, owner):\n        self.owner = owner\n        self._balance = 0\n    def deposit(self, amount):\n        self._balance += amount\n    def withdraw(self, amount):\n        if amount > self._balance:\n            raise ValueError\n        self._balance -= amount\n    def balance(self):\n        return self._balance\n',
    'class Wallet:\n    def __init__(self, owner):\n        self.owner = owner\n        self._balance = 0\n    def deposit(self, amount):\n        if amount <= 0:\n            raise ValueError\n        self._balance += amount\n    def withdraw(self, amount):\n        if amount <= 0:\n            raise ValueError\n        self._balance -= amount\n        if self._balance < 0:\n            raise ValueError\n    def balance(self):\n        return self._balance\n'],
   ["The leading underscore says \"internal: use the methods\".", "Validate first, then change _balance, so a refused call changes nothing.", "balance() is a method that simply returns self._balance."],
   "Keeping the balance behind methods means every change goes through the same checks. The order matters: subtracting first and checking afterwards would leave a negative balance behind when the error is raised.",
   'class Wallet:\n    """Money in, money out, never below zero."""\n\n    def __init__(self, owner):\n        pass\n')

ex("7.4", "Shapes with inheritance",
   "Write a base class Shape and two subclasses, Rectangle and Square.\n\n"
   "Specification:\n- Shape has a method describe() that returns f\"{name} with area {area}\", where name is the class name and area comes from self.area(), rounded to 2 decimals.\n- Rectangle(width, height) defines area().\n- Square(side) is a Rectangle whose width and height are both side; call super().__init__ instead of repeating code.\n\n"
   "Examples:\n- Rectangle(3, 4).describe() returns \"Rectangle with area 12\"\n- Square(2.5).describe() returns \"Square with area 6.25\"\n\n"
   "Edge cases: isinstance(Square(1), Rectangle) and isinstance(Square(1), Shape) are both True.",
   'class Shape:\n    def area(self):\n        raise NotImplementedError\n\n    def describe(self):\n        return f"{type(self).__name__} with area {round(self.area(), 2)}"\n\n\nclass Rectangle(Shape):\n    def __init__(self, width, height):\n        self.width = width\n        self.height = height\n\n    def area(self):\n        return self.width * self.height\n\n\nclass Square(Rectangle):\n    def __init__(self, side):\n        super().__init__(side, side)\n',
   [("Rectangle", "assert Rectangle(3, 4).describe() == 'Rectangle with area 12'"),
    ("Square", "assert Square(2.5).describe() == 'Square with area 6.25', 'The name comes from the class: Square'"),
    ("Inheritance", "s = Square(1)\nassert isinstance(s, Rectangle) and isinstance(s, Shape), 'A Square is a Rectangle, which is a Shape'\nassert s.width == 1 and s.height == 1"),
    ("Uses super()", "import re\nassert re.search(r'super\\(\\)\\.__init__', code), 'Square should call super().__init__(side, side)'")],
   ['class Shape:\n    def describe(self):\n        return f"Shape with area {round(self.area(), 2)}"\nclass Rectangle(Shape):\n    def __init__(self, w, h):\n        self.width, self.height = w, h\n    def area(self):\n        return self.width * self.height\nclass Square(Rectangle):\n    def __init__(self, side):\n        super().__init__(side, side)\n',
    'class Shape:\n    def describe(self):\n        return f"{type(self).__name__} with area {round(self.area(), 2)}"\nclass Rectangle(Shape):\n    def __init__(self, w, h):\n        self.width, self.height = w, h\n    def area(self):\n        return self.width * self.height\nclass Square(Shape):\n    def __init__(self, side):\n        self.width = self.height = side\n    def area(self):\n        return self.width ** 2\n'],
   ["describe lives in Shape and calls self.area(), which each subclass provides.", "type(self).__name__ gives the real class name of the object.", "Square inherits from Rectangle and calls super().__init__(side, side)."],
   "Writing describe once in the base class and letting it call self.area() means every subclass gets it for free. Square reuses Rectangle's setup through super(), so a change to Rectangle applies to squares too.",
   'class Shape:\n    def describe(self):\n        pass\n\n\nclass Rectangle(Shape):\n    pass\n\n\nclass Square(Rectangle):\n    pass\n')

ex("7.5", "An exporter contract with abc",
   "Write an abstract class Exporter and two concrete exporters.\n\n"
   "Specification:\n- Exporter inherits from ABC and has an abstract method export(rows), where rows is a list of dictionaries with the same keys.\n- CsvExporter.export(rows) returns the rows as CSV text: a header line with the keys, then one line per row, values joined with commas, lines joined with \\n.\n- LinesExporter.export(rows) returns one line per row in the form key=value;key=value, lines joined with \\n.\n- Creating Exporter() directly must raise TypeError.\n\n"
   "Examples:\n- CsvExporter().export([{\"item\": \"tea\", \"qty\": 2}]) returns \"item,qty\\ntea,2\"\n- LinesExporter().export([{\"item\": \"tea\", \"qty\": 2}]) returns \"item=tea;qty=2\"\n\n"
   "Edge cases: an empty list exports as an empty string with both exporters.",
   'from abc import ABC, abstractmethod\n\n\nclass Exporter(ABC):\n    @abstractmethod\n    def export(self, rows):\n        """Return rows (a list of dicts) as text."""\n\n\nclass CsvExporter(Exporter):\n    def export(self, rows):\n        if not rows:\n            return ""\n        keys = list(rows[0])\n        lines = [",".join(keys)] + [",".join(str(r[k]) for k in keys) for r in rows]\n        return "\\n".join(lines)\n\n\nclass LinesExporter(Exporter):\n    def export(self, rows):\n        return "\\n".join(";".join(f"{k}={v}" for k, v in r.items()) for r in rows)\n',
   [("CSV", "rows = [{'item': 'tea', 'qty': 2}, {'item': 'cake', 'qty': 1}]\nassert CsvExporter().export(rows) == 'item,qty\\ntea,2\\ncake,1'"),
    ("Lines", "assert LinesExporter().export([{'item': 'tea', 'qty': 2}]) == 'item=tea;qty=2'"),
    ("Empty input", "assert CsvExporter().export([]) == '' and LinesExporter().export([]) == ''"),
    ("Abstract base", "try:\n    Exporter()\nexcept TypeError:\n    pass\nelse:\n    raise AssertionError('Exporter() should raise TypeError: make export an @abstractmethod of an ABC')\nassert issubclass(CsvExporter, Exporter) and issubclass(LinesExporter, Exporter)")],
   ['class Exporter:\n    def export(self, rows):\n        raise NotImplementedError\nclass CsvExporter(Exporter):\n    def export(self, rows):\n        if not rows:\n            return ""\n        keys = list(rows[0])\n        return "\\n".join([",".join(keys)] + [",".join(str(r[k]) for k in keys) for r in rows])\nclass LinesExporter(Exporter):\n    def export(self, rows):\n        return "\\n".join(";".join(f"{k}={v}" for k, v in r.items()) for r in rows)\n',
    'from abc import ABC, abstractmethod\nclass Exporter(ABC):\n    @abstractmethod\n    def export(self, rows):\n        pass\nclass CsvExporter(Exporter):\n    def export(self, rows):\n        keys = list(rows[0])\n        return "\\n".join([",".join(keys)] + [",".join(str(r[k]) for k in keys) for r in rows])\nclass LinesExporter(Exporter):\n    def export(self, rows):\n        return "\\n".join(";".join(f"{k}={v}" for k, v in r.items()) for r in rows)\n'],
   ["from abc import ABC, abstractmethod; mark export with @abstractmethod.", "The CSV header is the keys of the first row; str() each value before joining.", "Handle the empty list before reading rows[0]."],
   "An abstract base class turns \"every exporter must have export\" into a rule Python enforces when an object is created. Each concrete class only supplies the format, and new formats can be added without touching code that uses an Exporter.",
   'from abc import ABC, abstractmethod\n\n\nclass Exporter(ABC):\n    pass\n')

# ---------------------------------------------------------------- chapter 8
ex("8.1", "Parse an age, or raise",
   "Write parse_age(text) that turns text into an age, raising ValueError with a clear message when that is impossible.\n\n"
   "Specification:\n- Surrounding spaces are ignored.\n- If the text is not a whole number, raise ValueError with a message containing \"whole number\".\n- If the number is below 0 or above 150, raise ValueError with a message containing \"between 0 and 150\".\n- Otherwise return the age as an int.\n\n"
   "Examples:\n- parse_age(\"42\") returns 42\n- parse_age(\" 7 \") returns 7\n- parse_age(\"forty\") raises ValueError(\"... whole number ...\")\n\n"
   "Edge cases: 0 and 150 are valid; -1 and 151 are not; 12.5 is not a whole number.",
   'def parse_age(text):\n    """Return text as an age from 0 to 150, or raise ValueError."""\n    text = text.strip()\n    if not text.lstrip("-").isdigit():\n        raise ValueError(f"age must be a whole number, got {text!r}")\n    age = int(text)\n    if not 0 <= age <= 150:\n        raise ValueError(f"age must be between 0 and 150, got {age}")\n    return age\n',
   [("Valid ages", "assert parse_age('42') == 42 and parse_age(' 7 ') == 7\nassert parse_age('0') == 0 and parse_age('150') == 150, '0 and 150 are both valid'"),
    ("Not a number", "for bad in ('forty', '12.5', ''):\n    try:\n        parse_age(bad)\n    except ValueError as e:\n        assert 'whole number' in str(e), f'The message for {bad!r} should mention a whole number, got: {e}'\n    else:\n        raise AssertionError(f'parse_age({bad!r}) should raise ValueError')"),
    ("Out of range", "for bad in ('-1', '151'):\n    try:\n        parse_age(bad)\n    except ValueError as e:\n        assert 'between 0 and 150' in str(e), f'The message for {bad!r} should say between 0 and 150, got: {e}'\n    else:\n        raise AssertionError(f'parse_age({bad!r}) should raise ValueError')")],
   ['def parse_age(text):\n    return int(text)\n',
    'def parse_age(text):\n    text = text.strip()\n    if not text.isdigit():\n        raise ValueError("age must be a whole number")\n    age = int(text)\n    if age > 150:\n        raise ValueError("age must be between 0 and 150")\n    return age\n'],
   ["Strip the spaces first, then check the text before converting.", "A leading minus sign is allowed in the text, so check text.lstrip(\"-\").isdigit().", "Check the range after converting, with 0 <= age <= 150."],
   "Raising ValueError with a message that says what was expected turns bad input into a helpful error. The minus sign case is subtle: \"-1\" is a whole number but out of range, so it must reach the range check and get the right message.",
   'def parse_age(text):\n    """Return text as an age from 0 to 150, or raise ValueError."""\n    pass\n')

ex("8.2", "Text to a number, with a default",
   "Write to_number(text, default=None) that converts text to an int if possible, otherwise to a float, otherwise returns default.\n\n"
   "Specification:\n- Try int first, then float, catching ValueError each time.\n- Surrounding spaces are fine (int and float accept them).\n- Never let the ValueError escape.\n\n"
   "Examples:\n- to_number(\"42\") returns 42\n- to_number(\"3.5\") returns 3.5\n- to_number(\"abc\") returns None\n- to_number(\"abc\", 0) returns 0\n\n"
   "Edge cases: to_number(\" 7 \") returns 7 (an int); to_number(\"1e3\") returns 1000.0.",
   'def to_number(text, default=None):\n    """Return text as an int, else a float, else default."""\n    try:\n        return int(text)\n    except ValueError:\n        pass\n    try:\n        return float(text)\n    except ValueError:\n        return default\n',
   [("Whole number", "r = to_number('42')\nassert r == 42 and isinstance(r, int), 'to_number(\"42\") should return the int 42'"),
    ("Decimal", "r = to_number('3.5')\nassert r == 3.5 and isinstance(r, float)"),
    ("Not a number", "assert to_number('abc') is None and to_number('abc', 0) == 0, 'Return the default when neither works'"),
    ("Spaces and exponents", "r = to_number(' 7 ')\nassert r == 7 and isinstance(r, int)\nassert to_number('1e3') == 1000.0")],
   ['def to_number(text, default=None):\n    try:\n        return float(text)\n    except ValueError:\n        return default\n',
    'def to_number(text, default=None):\n    try:\n        return int(text)\n    except ValueError:\n        return default\n'],
   ["Use two try/except blocks, one for int and one for float.", "Catch ValueError specifically, not every exception.", "Order matters: try int first, so \"42\" stays an int."],
   "Trying the stricter conversion first keeps whole numbers as ints, and catching only ValueError means real bugs (such as passing a list) still show up as errors.",
   'def to_number(text, default=None):\n    """Return text as an int, else a float, else default."""\n    pass\n')

ex("8.3", "Always log the end",
   "Write process(items, log) that adds up a list of numbers while recording what happens in the list log.\n\n"
   "Specification:\n- First append \"start\" to log.\n- Add up the items and return the total.\n- If an item is not a number, the resulting TypeError must reach the caller (do not catch it).\n- Whatever happens, append \"end\" to log as the last thing, using finally.\n- On success only, append f\"total {total}\" just before \"end\", using else.\n\n"
   "Examples:\n- process([1, 2, 3], log) returns 6 and log becomes [\"start\", \"total 6\", \"end\"]\n- process([1, \"x\"], log) raises TypeError and log becomes [\"start\", \"end\"]\n\n"
   "Edge cases: an empty list returns 0 and logs total 0.",
   'def process(items, log):\n    """Sum items, logging start, the total on success, and always end."""\n    log.append("start")\n    try:\n        total = 0\n        for item in items:\n            total += item\n    except TypeError:\n        raise\n    else:\n        log.append(f"total {total}")\n        return total\n    finally:\n        log.append("end")\n',
   [("Success", "log = []\nassert process([1, 2, 3], log) == 6\nassert log == ['start', 'total 6', 'end'], f'log should be [\"start\", \"total 6\", \"end\"], got {log}'"),
    ("Error reaches the caller", "log = []\ntry:\n    process([1, 'x'], log)\nexcept TypeError:\n    pass\nelse:\n    raise AssertionError('A non-number should raise TypeError to the caller')\nassert log == ['start', 'end'], f'After an error log should be [\"start\", \"end\"], got {log}'"),
    ("Empty list", "log = []\nassert process([], log) == 0 and log == ['start', 'total 0', 'end']")],
   ['def process(items, log):\n    log.append("start")\n    total = sum(items)\n    log.append(f"total {total}")\n    log.append("end")\n    return total\n',
    'def process(items, log):\n    log.append("start")\n    try:\n        total = sum(items)\n    except TypeError:\n        log.append("end")\n        return None\n    log.append(f"total {total}")\n    log.append("end")\n    return total\n'],
   ["Put the work in try; the success-only line goes in else; \"end\" goes in finally.", "finally runs even when the exception continues to the caller.", "You do not need an except clause at all if you only want cleanup."],
   "finally guarantees cleanup whether the block succeeds, fails or returns, which is exactly what logging, closing files and releasing locks need. else keeps the success-only step out of the try block, so it cannot accidentally hide errors.",
   'def process(items, log):\n    """Sum items, logging start, the total on success, and always end."""\n    pass\n')

ex("8.4", "Safe nested lookups",
   "Write get_path(data, path, default=None) that follows a dotted path through nested dictionaries and lists, asking forgiveness rather than permission.\n\n"
   "Specification:\n- path is a string like \"user.emails.0\": keys separated by dots.\n- A part made only of digits is used as a list index (convert it with int); other parts are dictionary keys.\n- If any step fails with KeyError, IndexError or TypeError, return default.\n\n"
   "Examples:\n- get_path({\"user\": {\"name\": \"Ada\"}}, \"user.name\") returns \"Ada\"\n- get_path({\"user\": {\"emails\": [\"a@x.org\"]}}, \"user.emails.0\") returns \"a@x.org\"\n- get_path({\"user\": {}}, \"user.name\", \"?\") returns \"?\"\n\n"
   "Edge cases: an index past the end, or indexing into a number, returns default.",
   'def get_path(data, path, default=None):\n    """Follow a dotted path through nested dicts and lists, or return default."""\n    current = data\n    try:\n        for part in path.split("."):\n            current = current[int(part)] if part.isdigit() else current[part]\n    except (KeyError, IndexError, TypeError):\n        return default\n    return current\n',
   [("Nested key", "assert get_path({'user': {'name': 'Ada'}}, 'user.name') == 'Ada'"),
    ("List index", "assert get_path({'user': {'emails': ['a@x.org', 'b@x.org']}}, 'user.emails.1') == 'b@x.org'"),
    ("Missing key", "assert get_path({'user': {}}, 'user.name', '?') == '?' and get_path({}, 'a.b') is None"),
    ("Bad index and wrong type", "d = {'items': [1, 2], 'n': 5}\nassert get_path(d, 'items.9', 'none') == 'none', 'An index past the end returns default'\nassert get_path(d, 'n.x', 'none') == 'none', 'Looking inside a number returns default'")],
   ['def get_path(data, path, default=None):\n    cur = data\n    for part in path.split("."):\n        if isinstance(cur, dict) and part in cur:\n            cur = cur[part]\n        else:\n            return default\n    return cur\n',
    'def get_path(data, path, default=None):\n    cur = data\n    try:\n        for part in path.split("."):\n            cur = cur[int(part)] if part.isdigit() else cur[part]\n    except KeyError:\n        return default\n    return cur\n'],
   ["Split the path on dots and walk through it, replacing current at each step.", "Use int(part) when part.isdigit(), so list indexes work.", "Wrap the whole loop in one try and catch the three exception types together."],
   "Asking forgiveness keeps the happy path short: walk the structure and handle any failure in one place. Checking every step first (is it a dict? is the key there? is it a list? is the index in range?) takes far more code and still misses cases.",
   'def get_path(data, path, default=None):\n    """Follow a dotted path through nested dicts and lists, or return default."""\n    pass\n')

# ---------------------------------------------------------------- chapter 9
ex("9.1", "A discounted product",
   "Write a class Product and a subclass DiscountedProduct.\n\n"
   "Specification:\n- Product(name, price) stores both; price() returns the price; __repr__ returns f\"{ClassName}({name!r}, {price})\", using the actual class name.\n- DiscountedProduct(name, price, percent) calls super().__init__ for the name and price, stores percent, and overrides price() to return the price reduced by percent, rounded to 2 decimals.\n\n"
   "Examples:\n- Product(\"tea\", 4.0).price() returns 4.0\n- DiscountedProduct(\"tea\", 4.0, 25).price() returns 3.0\n- repr(Product(\"tea\", 4.0)) returns \"Product('tea', 4.0)\"\n\n"
   "Edge cases: repr of a DiscountedProduct starts with DiscountedProduct(.",
   'class Product:\n    def __init__(self, name, price):\n        self.name = name\n        self._price = price\n\n    def price(self):\n        return self._price\n\n    def __repr__(self):\n        return f"{type(self).__name__}({self.name!r}, {self._price})"\n\n\nclass DiscountedProduct(Product):\n    def __init__(self, name, price, percent):\n        super().__init__(name, price)\n        self.percent = percent\n\n    def price(self):\n        return round(super().price() * (1 - self.percent / 100), 2)\n',
   [("Product", "p = Product('tea', 4.0)\nassert p.price() == 4.0 and p.name == 'tea'"),
    ("Discount", "assert DiscountedProduct('tea', 4.0, 25).price() == 3.0\nassert DiscountedProduct('cake', 9.99, 10).price() == 8.99"),
    ("repr uses the class name", "assert repr(Product('tea', 4.0)) == \"Product('tea', 4.0)\"\nassert repr(DiscountedProduct('tea', 4.0, 25)).startswith('DiscountedProduct('), 'Use type(self).__name__ so subclasses show their own name'"),
    ("Calls super().__init__", "import re\nassert re.search(r'super\\(\\)\\.__init__', code), 'DiscountedProduct should call super().__init__(name, price)'")],
   ['class Product:\n    def __init__(self, name, price):\n        self.name = name\n        self._price = price\n    def price(self):\n        return self._price\n    def __repr__(self):\n        return f"Product({self.name!r}, {self._price})"\nclass DiscountedProduct(Product):\n    def __init__(self, name, price, percent):\n        super().__init__(name, price)\n        self.percent = percent\n    def price(self):\n        return round(self._price * (1 - self.percent / 100), 2)\n',
    'class Product:\n    def __init__(self, name, price):\n        self.name = name\n        self._price = price\n    def price(self):\n        return self._price\n    def __repr__(self):\n        return f"{type(self).__name__}({self.name!r}, {self._price})"\nclass DiscountedProduct(Product):\n    def __init__(self, name, price, percent):\n        super().__init__(name, price)\n        self.percent = percent\n    def price(self):\n        return round(self._price * self.percent / 100, 2)\n'],
   ["Call super().__init__(name, price) first, then store percent.", "Override price() and reuse the parent's value with super().price().", "type(self).__name__ makes __repr__ correct for subclasses."],
   "super() reuses the parent's setup and behaviour instead of copying it, so a change in Product (say, validation) applies to discounted products too. A __repr__ built from type(self).__name__ stays correct in every subclass.",
   'class Product:\n    def __init__(self, name, price):\n        pass\n\n\nclass DiscountedProduct(Product):\n    pass\n')

ex("9.2", "A playlist with item access",
   "Write a class Playlist that behaves like a sequence of song titles.\n\n"
   "Specification:\n- Playlist(titles) copies the list it is given.\n- len(p) gives the number of songs; p[i] gives a title (negative indexes and slices work like a list; a slice returns a list).\n- p[i] = title replaces a song, but raises TypeError if title is not a str.\n- del p[i] removes a song.\n\n"
   "Examples:\n- p = Playlist([\"Halo\", \"Hey Jude\"]); len(p) is 2; p[-1] is \"Hey Jude\"\n- p[0] = \"Imagine\" replaces Halo\n\n"
   "Edge cases: changing the playlist never changes the list that was passed in; p[0] = 42 raises TypeError.",
   'class Playlist:\n    """A list of song titles with list-like access."""\n\n    def __init__(self, titles):\n        self._titles = list(titles)\n\n    def __len__(self):\n        return len(self._titles)\n\n    def __getitem__(self, index):\n        return self._titles[index]\n\n    def __setitem__(self, index, title):\n        if not isinstance(title, str):\n            raise TypeError("titles must be strings")\n        self._titles[index] = title\n\n    def __delitem__(self, index):\n        del self._titles[index]\n',
   [("len and indexing", "p = Playlist(['Halo', 'Hey Jude', 'Imagine'])\nassert len(p) == 3 and p[0] == 'Halo' and p[-1] == 'Imagine'\nassert p[0:2] == ['Halo', 'Hey Jude'], 'A slice should return a list'"),
    ("Replace and delete", "p = Playlist(['Halo', 'Hey Jude'])\np[0] = 'Imagine'\ndel p[1]\nassert len(p) == 1 and p[0] == 'Imagine'"),
    ("Only strings", "p = Playlist(['Halo'])\ntry:\n    p[0] = 42\nexcept TypeError:\n    pass\nelse:\n    raise AssertionError('Assigning a non-string should raise TypeError')\nassert p[0] == 'Halo'"),
    ("Copies its input", "songs = ['Halo']\np = Playlist(songs)\np[0] = 'Imagine'\nassert songs == ['Halo'], 'Changing the playlist must not change the original list'"),
    ("Works in for loops and in", "p = Playlist(['a', 'b'])\nassert list(p) == ['a', 'b'] and 'b' in p")],
   ['class Playlist:\n    def __init__(self, titles):\n        self._titles = titles\n    def __len__(self):\n        return len(self._titles)\n    def __getitem__(self, i):\n        return self._titles[i]\n    def __setitem__(self, i, t):\n        if not isinstance(t, str):\n            raise TypeError\n        self._titles[i] = t\n    def __delitem__(self, i):\n        del self._titles[i]\n',
    'class Playlist:\n    def __init__(self, titles):\n        self._titles = list(titles)\n    def __len__(self):\n        return len(self._titles)\n    def __getitem__(self, i):\n        return self._titles[i]\n    def __setitem__(self, i, t):\n        self._titles[i] = t\n    def __delitem__(self, i):\n        del self._titles[i]\n'],
   ["Store a copy: self._titles = list(titles).", "Pass the index straight to the inner list in __getitem__, so negatives and slices work for free.", "Check isinstance(title, str) in __setitem__ before changing anything."],
   "Each piece of familiar syntax calls one special method, and delegating to an inner list gives negative indexes, slices, for loops and in without extra code. Copying the input protects the caller's list.",
   'class Playlist:\n    """A list of song titles with list-like access."""\n\n    def __init__(self, titles):\n        pass\n')

ex("9.3", "A temperature with properties",
   "Write a class Temperature with checked and computed attributes.\n\n"
   "Specification:\n- Temperature(celsius) stores the temperature.\n- celsius is a property; setting it below -273.15 raises ValueError (also in __init__).\n- fahrenheit is a property computed from celsius (celsius * 9 / 5 + 32); setting it updates celsius.\n- Temperature.from_fahrenheit(f) is a classmethod that creates a Temperature.\n\n"
   "Examples:\n- Temperature(100).fahrenheit is 212.0\n- t = Temperature(0); t.fahrenheit = 212 makes t.celsius 100.0\n- Temperature.from_fahrenheit(32).celsius is 0.0\n\n"
   "Edge cases: Temperature(-300) raises ValueError; -273.15 itself is allowed.",
   'class Temperature:\n    """A temperature that can never go below absolute zero."""\n\n    def __init__(self, celsius):\n        self.celsius = celsius\n\n    @property\n    def celsius(self):\n        return self._celsius\n\n    @celsius.setter\n    def celsius(self, value):\n        if value < -273.15:\n            raise ValueError("below absolute zero")\n        self._celsius = value\n\n    @property\n    def fahrenheit(self):\n        return self._celsius * 9 / 5 + 32\n\n    @fahrenheit.setter\n    def fahrenheit(self, value):\n        self.celsius = (value - 32) * 5 / 9\n\n    @classmethod\n    def from_fahrenheit(cls, f):\n        return cls((f - 32) * 5 / 9)\n',
   [("Computed fahrenheit", "assert Temperature(100).fahrenheit == 212.0 and Temperature(0).fahrenheit == 32.0"),
    ("Setting fahrenheit", "t = Temperature(0)\nt.fahrenheit = 212\nassert t.celsius == 100.0"),
    ("Class method", "t = Temperature.from_fahrenheit(32)\nassert isinstance(t, Temperature) and t.celsius == 0.0"),
    ("Absolute zero", "assert Temperature(-273.15).celsius == -273.15\nfor make in (lambda: Temperature(-300), lambda: setattr(Temperature(0), 'celsius', -274)):\n    try:\n        make()\n    except ValueError:\n        continue\n    raise AssertionError('Temperatures below -273.15 must raise ValueError, in __init__ and when setting celsius')")],
   ['class Temperature:\n    def __init__(self, celsius):\n        self._celsius = celsius\n    @property\n    def celsius(self):\n        return self._celsius\n    @celsius.setter\n    def celsius(self, v):\n        if v < -273.15:\n            raise ValueError\n        self._celsius = v\n    @property\n    def fahrenheit(self):\n        return self._celsius * 9 / 5 + 32\n    @fahrenheit.setter\n    def fahrenheit(self, v):\n        self.celsius = (v - 32) * 5 / 9\n    @classmethod\n    def from_fahrenheit(cls, f):\n        return cls((f - 32) * 5 / 9)\n',
    'class Temperature:\n    def __init__(self, celsius):\n        self.celsius = celsius\n        self.fahrenheit = celsius * 9 / 5 + 32\n    @classmethod\n    def from_fahrenheit(cls, f):\n        return cls((f - 32) * 5 / 9)\n'],
   ["In __init__, assign self.celsius = celsius so the setter's check runs there too.", "Store the real value in self._celsius and expose it through @property.", "The fahrenheit setter can simply set self.celsius, reusing the check."],
   "Properties let callers use plain attribute syntax while the class keeps control: the setter validates every change, including the one in __init__, and fahrenheit is always computed, so it can never go out of date.",
   'class Temperature:\n    """A temperature that can never go below absolute zero."""\n\n    def __init__(self, celsius):\n        pass\n')

ex("9.4", "A countdown iterator",
   "Write a class Countdown that is its own iterator.\n\n"
   "Specification:\n- Countdown(n) produces n, n - 1, ..., 1 when iterated.\n- __iter__ returns self; __next__ returns the next number or raises StopIteration when done.\n- Once used up, it stays used up.\n\n"
   "Examples:\n- list(Countdown(3)) returns [3, 2, 1]\n- c = Countdown(2); next(c) is 2; next(c) is 1; next(c) raises StopIteration\n\n"
   "Edge cases: Countdown(0) produces nothing.",
   'class Countdown:\n    """Counts down from n to 1."""\n\n    def __init__(self, n):\n        self.current = n\n\n    def __iter__(self):\n        return self\n\n    def __next__(self):\n        if self.current <= 0:\n            raise StopIteration\n        value = self.current\n        self.current -= 1\n        return value\n',
   [("Counts down", "assert list(Countdown(3)) == [3, 2, 1]"),
    ("next() by hand", "c = Countdown(2)\nassert next(c) == 2 and next(c) == 1\ntry:\n    next(c)\nexcept StopIteration:\n    pass\nelse:\n    raise AssertionError('After the last number, next() should raise StopIteration')"),
    ("Zero", "assert list(Countdown(0)) == []"),
    ("Its own iterator, used once", "c = Countdown(3)\nassert iter(c) is c, '__iter__ should return self'\nlist(c)\nassert list(c) == [], 'Once used up it stays used up'")],
   ['class Countdown:\n    def __init__(self, n):\n        self.n = n\n    def __iter__(self):\n        return iter(range(self.n, 0, -1))\n',
    'class Countdown:\n    def __init__(self, n):\n        self.current = n\n    def __iter__(self):\n        return self\n    def __next__(self):\n        if self.current < 0:\n            raise StopIteration\n        v = self.current\n        self.current -= 1\n        return v\n'],
   ["Keep the next number to return in an attribute.", "__next__ raises StopIteration when the number reaches 0.", "__iter__ just returns self."],
   "An iterator remembers where it is, which is why it can only be used once: the for loop calls __next__ until StopIteration. Getting the stop condition right (<= 0) is the usual off-by-one trap.",
   'class Countdown:\n    """Counts down from n to 1."""\n\n    def __init__(self, n):\n        pass\n')

ex("9.5", "Chunks with a generator",
   "Write a generator function chunks(items, size) that yields lists of size consecutive items.\n\n"
   "Specification:\n- Yield lists of length size, in order; the last one may be shorter.\n- If size is less than 1, raise ValueError (it is fine if the error appears when iteration starts).\n- Work with any iterable, not just lists, and do not build all chunks in advance.\n\n"
   "Examples:\n- list(chunks([1, 2, 3, 4, 5], 2)) returns [[1, 2], [3, 4], [5]]\n- list(chunks(\"abcdef\", 3)) returns [[\"a\", \"b\", \"c\"], [\"d\", \"e\", \"f\"]]\n\n"
   "Edge cases: an empty input yields nothing; getting the first chunk must not read the whole input.",
   'def chunks(items, size):\n    """Yield lists of size consecutive items; the last may be shorter."""\n    if size < 1:\n        raise ValueError("size must be at least 1")\n    chunk = []\n    for item in items:\n        chunk.append(item)\n        if len(chunk) == size:\n            yield chunk\n            chunk = []\n    if chunk:\n        yield chunk\n',
   [("Uneven split", "assert list(chunks([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]"),
    ("Any iterable", "assert list(chunks('abcdef', 3)) == [['a', 'b', 'c'], ['d', 'e', 'f']]"),
    ("Empty input", "assert list(chunks([], 4)) == []"),
    ("Lazy", "import types\npulled = []\ndef source():\n    for i in range(1000):\n        pulled.append(i)\n        yield i\ng = chunks(source(), 3)\nassert isinstance(g, types.GeneratorType), 'chunks should be a generator function (use yield)'\nassert next(g) == [0, 1, 2]\nassert len(pulled) <= 4, f'Getting the first chunk read {len(pulled)} items; read only as many as needed'"),
    ("Invalid size", "try:\n    list(chunks([1], 0))\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError('size 0 should raise ValueError')")],
   ['def chunks(items, size):\n    items = list(items)\n    return [items[i:i + size] for i in range(0, len(items), size)]\n',
    'def chunks(items, size):\n    chunk = []\n    for item in items:\n        chunk.append(item)\n        if len(chunk) == size:\n            yield chunk\n            chunk = []\n'],
   ["Collect items into a list; when it reaches size, yield it and start a new one.", "After the loop, yield what is left if it is not empty.", "Check size before the loop."],
   "A generator produces one chunk at a time, so it works on huge or endless inputs; building a list first would try to hold a billion numbers. Forgetting the final partial chunk is the classic bug the uneven-split test catches.",
   'def chunks(items, size):\n    """Yield lists of size consecutive items; the last may be shorter."""\n    pass\n')

ex("9.6", "Count the queens' solutions",
   "Write count_solutions(n) that returns how many ways n queens can be placed on an n by n board so that no two attack each other, using a recursive generator.\n\n"
   "Specification:\n- A placement is a tuple of column numbers, one per row.\n- Two queens attack each other if they share a column or a diagonal (the column distance equals the row distance).\n- Generate the solutions with a recursive generator and count them.\n\n"
   "Examples:\n- count_solutions(4) returns 2\n- count_solutions(6) returns 4\n- count_solutions(8) returns 92\n\n"
   "Edge cases: count_solutions(1) returns 1; count_solutions(2) and count_solutions(3) return 0.",
   'def conflict(state, col):\n    row = len(state)\n    return any(c == col or abs(c - col) == row - r for r, c in enumerate(state))\n\n\ndef queens(n, state=()):\n    for col in range(n):\n        if not conflict(state, col):\n            if len(state) == n - 1:\n                yield (col,)\n            else:\n                for rest in queens(n, state + (col,)):\n                    yield (col,) + rest\n\n\ndef count_solutions(n):\n    """Return the number of ways to place n non-attacking queens."""\n    return sum(1 for _ in queens(n))\n',
   [("Four queens", "assert count_solutions(4) == 2"),
    ("Six and eight", "assert count_solutions(6) == 4 and count_solutions(8) == 92"),
    ("Small boards", "assert count_solutions(1) == 1 and count_solutions(2) == 0 and count_solutions(3) == 0")],
   ['def count_solutions(n):\n    import itertools\n    return sum(1 for p in itertools.permutations(range(n)))\n',
    'def conflict(state, col):\n    return col in state\ndef queens(n, state=()):\n    for col in range(n):\n        if not conflict(state, col):\n            if len(state) == n - 1:\n                yield (col,)\n            else:\n                for rest in queens(n, state + (col,)):\n                    yield (col,) + rest\ndef count_solutions(n):\n    return sum(1 for _ in queens(n))\n'],
   ["A new queen in row len(state) conflicts if it shares a column or a diagonal with an earlier queen.", "The generator places one queen per row, recursing for the remaining rows.", "sum(1 for _ in queens(n)) counts without storing the solutions."],
   "The diagonal test abs(c - col) == row - r is the heart of the puzzle; checking columns alone counts all permutations. Generating only safe placements prunes most of the search, so even 8 queens is quick.",
   'def count_solutions(n):\n    """Return the number of ways to place n non-attacking queens."""\n    pass\n')

# ---------------------------------------------------------------- chapter 10
ex("10.1", "Your own module",
   "Write a module textstats.py and a main program that uses it, both in this one box.\n\n"
   "Specification:\n- Start the module with the marker line # --- textstats.py --- and the program with # --- main.py --- (the last section is the program that runs).\n- textstats.py defines word_count(text), the number of words (split on whitespace), and longest_word(text), the first of the longest words (\"\" for empty text). Its own test code goes under if __name__ == \"__main__\": so it does not run on import.\n- main.py imports textstats and prints word_count and longest_word for the text \"the quick brown fox jumps\", one per line.\n\n"
   "Examples:\n- word_count(\"the quick brown fox jumps\") is 5\n- longest_word(\"the quick brown fox jumps\") is \"quick\"\n\n"
   "Edge cases: importing textstats prints nothing; longest_word(\"\") is \"\".",
   '# --- textstats.py ---\n"""Small text statistics."""\n\n\ndef word_count(text):\n    return len(text.split())\n\n\ndef longest_word(text):\n    words = text.split()\n    return max(words, key=len) if words else ""\n\n\nif __name__ == "__main__":\n    print(word_count("one two"), longest_word("one three"))\n\n# --- main.py ---\nimport textstats\n\ntext = "the quick brown fox jumps"\nprint(textstats.word_count(text))\nprint(textstats.longest_word(text))\n',
   [("main.py prints the results", "lines = out.strip().split('\\n')\nassert lines == ['5', 'quick'], f'main.py should print 5 and quick on two lines, got {lines}'"),
    ("The module's functions", "import importlib, sys\nsys.modules.pop('textstats', None)\nimport textstats\nassert textstats.word_count('  a  b c ') == 3\nassert textstats.longest_word('hi hello hey') == 'hello' and textstats.longest_word('') == ''"),
    ("Importing prints nothing", "import importlib, sys, io, contextlib\nsys.modules.pop('textstats', None)\nbuf = io.StringIO()\nwith contextlib.redirect_stdout(buf):\n    import textstats\nassert buf.getvalue() == '', 'Put the module\\'s own test code under if __name__ == \"__main__\":'")],
   ['# --- textstats.py ---\ndef word_count(text):\n    return len(text.split())\ndef longest_word(text):\n    words = text.split()\n    return max(words, key=len) if words else ""\nprint(word_count("one two"))\n\n# --- main.py ---\nimport textstats\ntext = "the quick brown fox jumps"\nprint(textstats.word_count(text))\nprint(textstats.longest_word(text))\n',
    '# --- textstats.py ---\ndef word_count(text):\n    return len(text.split(" "))\ndef longest_word(text):\n    return max(text.split(), key=len)\n\n# --- main.py ---\nimport textstats\ntext = "the quick brown fox jumps"\nprint(textstats.word_count(text))\nprint(textstats.longest_word(text))\n'],
   ["Each file starts with its marker line, exactly like # --- textstats.py ---.", "max(words, key=len) returns the first of the longest words; handle the empty list first.", "Code under if __name__ == \"__main__\": runs only when the file itself is run."],
   "A module is just a file of definitions that other files import. The __name__ test lets the same file hold its own quick checks without them running for everyone who imports it.",
   '# --- textstats.py ---\n\n\n# --- main.py ---\nimport textstats\n', main=True)

ex("10.2", "The public names of a module",
   "Write public_names(module) that returns the names a module offers to its users.\n\n"
   "Specification:\n- If the module defines __all__, return a sorted list of the names in it.\n- Otherwise return a sorted list of the names in dir(module) that do not start with an underscore.\n\n"
   "Examples:\n- for a module with names helper, _secret and greet and no __all__, the result is [\"greet\", \"helper\"]\n- with __all__ = [\"greet\"], the result is [\"greet\"]\n\n"
   "Edge cases: works for real modules too: \"sqrt\" is in public_names(math) and no name starts with _.",
   'def public_names(module):\n    """Return the sorted public names of module."""\n    if hasattr(module, "__all__"):\n        return sorted(module.__all__)\n    return sorted(name for name in dir(module) if not name.startswith("_"))\n',
   [("Without __all__", "import types\nm = types.ModuleType('demo')\nm.helper = 1; m._secret = 2; m.greet = 3\nassert public_names(m) == ['greet', 'helper']"),
    ("With __all__", "import types\nm = types.ModuleType('demo')\nm.helper = 1; m.greet = 3; m.__all__ = ['greet']\nassert public_names(m) == ['greet'], 'When __all__ exists, return exactly its names, sorted'"),
    ("A real module", "import math\nnames = public_names(math)\nassert 'sqrt' in names and not any(n.startswith('_') for n in names) and names == sorted(names)")],
   ['def public_names(module):\n    return sorted(n for n in dir(module) if not n.startswith("_"))\n',
    'def public_names(module):\n    if hasattr(module, "__all__"):\n        return module.__all__\n    return [n for n in dir(module) if not n.startswith("__")]\n'],
   ["hasattr(module, \"__all__\") tells you whether the module declares its public names.", "dir(module) lists every name; filter out those starting with _.", "Return sorted lists in both cases."],
   "__all__ is the module author's own statement of what is public, so it wins when present. Otherwise the leading-underscore convention is the best guide; the result matches what from module import * would bring in.",
   'def public_names(module):\n    """Return the sorted public names of module."""\n    pass\n')

ex("10.3", "Greet everyone on the command line",
   "Write a program that greets every name given as a command-line argument, using sys.argv.\n\n"
   "Specification:\n- With no arguments, print usage: greet.py NAME... and exit with sys.exit(1).\n- Otherwise print Hello, NAME! for each argument, one per line, then a last line with the count, such as 3 people greeted.\n\n"
   "Examples:\n- greet.py Ada Ben prints Hello, Ada!, Hello, Ben!, 2 people greeted\n\n"
   "Edge cases: one name prints 1 people greeted (keep it simple).",
   'import sys\n\nnames = sys.argv[1:]\nif not names:\n    print("usage: greet.py NAME...")\n    sys.exit(1)\nfor name in names:\n    print(f"Hello, {name}!")\nprint(f"{len(names)} people greeted")\n',
   [("Two names", {"argv": ["Ada", "Ben"], "check": "assert out.strip().split('\\n') == ['Hello, Ada!', 'Hello, Ben!', '2 people greeted']"}),
    ("One name", {"argv": ["Cy"], "check": "assert out.strip().split('\\n') == ['Hello, Cy!', '1 people greeted']"}),
    ("No names", {"argv": [], "check": "assert out.strip() == 'usage: greet.py NAME...', 'With no arguments print the usage line'\nimport re\nassert re.search(r'sys\\.exit\\(\\s*1\\s*\\)', code), 'Exit with sys.exit(1) after the usage line'"})],
   ['import sys\nfor name in sys.argv:\n    print(f"Hello, {name}!")\nprint(f"{len(sys.argv)} people greeted")\n',
    'import sys\nnames = sys.argv[1:]\nfor name in names:\n    print(f"Hello, {name}!")\nprint(f"{len(names)} people greeted")\n'],
   ["sys.argv[0] is the script name; the arguments are sys.argv[1:].", "Check for an empty list first and exit with sys.exit(1).", "An f-string builds each greeting."],
   "sys.argv always starts with the script's own name, so the real arguments are a slice. Exiting with a non-zero status on bad usage lets shells and scripts detect the failure.",
   'import sys\n\n', main=True)

ex("10.4", "Top scores with heapq",
   "Write top_n(scores, n) that returns the names of the n highest scores, highest first, using heapq.\n\n"
   "Specification:\n- scores is a dictionary of name to score.\n- Return a list of names, highest score first; equal scores are ordered alphabetically by name.\n- If n is larger than the number of names, return them all.\n\n"
   "Examples:\n- top_n({\"ada\": 90, \"ben\": 75, \"cy\": 95}, 2) returns [\"cy\", \"ada\"]\n\n"
   "Edge cases: ties: top_n({\"zoe\": 80, \"amy\": 80, \"bo\": 70}, 2) returns [\"amy\", \"zoe\"]; n = 0 returns [].",
   'import heapq\n\n\ndef top_n(scores, n):\n    """Return the names with the n highest scores, ties alphabetical."""\n    best = heapq.nsmallest(n, scores.items(), key=lambda kv: (-kv[1], kv[0]))\n    return [name for name, _ in best]\n',
   [("Top two", "assert top_n({'ada': 90, 'ben': 75, 'cy': 95}, 2) == ['cy', 'ada']"),
    ("Ties are alphabetical", "assert top_n({'zoe': 80, 'amy': 80, 'bo': 70}, 2) == ['amy', 'zoe'], 'Equal scores are ordered by name'"),
    ("n too large or zero", "s = {'a': 1, 'b': 2}\nassert top_n(s, 10) == ['b', 'a'] and top_n(s, 0) == []"),
    ("Uses heapq", "assert 'heapq' in code, 'Use the heapq module (nlargest or nsmallest)'")],
   ['import heapq\ndef top_n(scores, n):\n    return [k for k, v in heapq.nlargest(n, scores.items(), key=lambda kv: kv[1])]\n',
    'import heapq\ndef top_n(scores, n):\n    return sorted(scores, key=lambda k: -scores[k])[:n - 1]\n'],
   ["heapq.nlargest(n, items, key=...) and heapq.nsmallest(n, items, key=...) find the top n without sorting everything.", "A key of (-score, name) puts high scores first and breaks ties alphabetically with nsmallest.", "scores.items() gives (name, score) pairs."],
   "A tuple key handles two ordering rules at once: negating the score makes higher come first, and the name decides ties. heapq finds the top n efficiently, which matters for big inputs.",
   'import heapq\n\n\ndef top_n(scores, n):\n    """Return the names with the n highest scores, ties alphabetical."""\n    pass\n')

ex("10.5", "Save and load scores as JSON",
   "Write save_scores(scores, path) and load_scores(path).\n\n"
   "Specification:\n- save_scores writes the dictionary to path as JSON, with indent=2 and sort_keys=True, using UTF-8.\n- load_scores returns the dictionary read from path, or an empty dictionary if the file does not exist.\n\n"
   "Examples:\n- save_scores({\"ben\": 3, \"ada\": 5}, \"s.json\") writes a file whose text starts with {, then a line with   \"ada\": 5,\n- load_scores(\"s.json\") returns {\"ada\": 5, \"ben\": 3}\n\n"
   "Edge cases: load_scores(\"missing.json\") returns {}; names with accents such as \"Zoé\" survive the round trip.",
   'import json\n\n\ndef save_scores(scores, path):\n    with open(path, "w", encoding="utf-8") as f:\n        json.dump(scores, f, indent=2, sort_keys=True, ensure_ascii=False)\n\n\ndef load_scores(path):\n    try:\n        with open(path, encoding="utf-8") as f:\n            return json.load(f)\n    except FileNotFoundError:\n        return {}\n',
   [("Round trip", "save_scores({'ben': 3, 'ada': 5}, 's.json')\nassert load_scores('s.json') == {'ada': 5, 'ben': 3}"),
    ("Sorted and indented", "save_scores({'ben': 3, 'ada': 5}, 's.json')\ntext = open('s.json', encoding='utf-8').read()\nassert text.splitlines()[:2] == ['{', '  \"ada\": 5,'], 'Use indent=2 and sort_keys=True'"),
    ("Missing file", "assert load_scores('missing.json') == {}, 'A missing file gives an empty dictionary'"),
    ("Accents survive", "save_scores({'Zoé': 1}, 'z.json')\nassert load_scores('z.json') == {'Zoé': 1}")],
   ['import json\ndef save_scores(scores, path):\n    with open(path, "w") as f:\n        json.dump(scores, f)\ndef load_scores(path):\n    with open(path) as f:\n        return json.load(f)\n',
    'import json\ndef save_scores(scores, path):\n    with open(path, "w", encoding="utf-8") as f:\n        json.dump(scores, f, indent=2)\ndef load_scores(path):\n    try:\n        with open(path, encoding="utf-8") as f:\n            return json.load(f)\n    except FileNotFoundError:\n        return {}\n'],
   ["json.dump(obj, file, indent=2, sort_keys=True) writes readable, stable JSON.", "Open files with encoding=\"utf-8\" for both writing and reading.", "Catch FileNotFoundError in load_scores and return {}."],
   "Sorted keys and indentation make the file readable and stable, so it diffs cleanly in version control. Treating a missing file as \"no scores yet\" makes the first run of a program work without setup.",
   'import json\n\n\ndef save_scores(scores, path):\n    pass\n\n\ndef load_scores(path):\n    pass\n')

ex("10.6", "Find the email addresses",
   "Write find_emails(text) that returns every email address in text, in order, using the re module.\n\n"
   "Specification:\n- An address is one or more letters, digits, dots, underscores, plus signs or hyphens, then @, then a domain: letters, digits and hyphens in parts separated by dots, ending with a part of at least 2 letters.\n- A full stop right after an address (end of a sentence) is not part of it.\n\n"
   "Examples:\n- find_emails(\"Write to ada@example.com or ben.ng@mail.example.org.\") returns [\"ada@example.com\", \"ben.ng@mail.example.org\"]\n\n"
   "Edge cases: no addresses returns []; \"name@localhost\" is not an address (no dot in the domain).",
   'import re\n\nEMAIL = re.compile(r"[\\w.+-]+@(?:[A-Za-z0-9-]+\\.)+[A-Za-z]{2,}")\n\n\ndef find_emails(text):\n    """Return the email addresses in text, in order."""\n    return EMAIL.findall(text)\n',
   [("Two addresses", "assert find_emails('Write to ada@example.com or ben.ng@mail.example.org.') == ['ada@example.com', 'ben.ng@mail.example.org'], 'The final full stop is not part of the address'"),
    ("Plus and hyphen", "assert find_emails('cy+news@my-site.co.uk, done') == ['cy+news@my-site.co.uk']"),
    ("None found", "assert find_emails('no addresses here') == [] and find_emails('name@localhost') == []")],
   ['import re\ndef find_emails(text):\n    return re.findall(r"\\S+@\\S+", text)\n',
    'import re\ndef find_emails(text):\n    return re.findall(r"[\\w.+-]+@[\\w.-]+", text)\n'],
   ["Build the pattern in pieces: the name part [\\w.+-]+, the @, then the domain.", "(?:[A-Za-z0-9-]+\\.)+ matches domain parts each followed by a dot; then [A-Za-z]{2,} is the final part.", "re.findall returns all matches in order (with a non-capturing group, it returns the whole match)."],
   "Writing the domain as parts each ending with a dot, then a final part of letters, makes the trailing full stop impossible to swallow. A non-capturing group (?:...) keeps findall returning whole addresses instead of just the group.",
   'import re\n\n\ndef find_emails(text):\n    """Return the email addresses in text, in order."""\n    pass\n')

ex("10.7", "Group words by first letter",
   "Write group_by_letter(words) that groups words by their first letter, using collections.defaultdict.\n\n"
   "Specification:\n- Keys are lower-case first letters; values are the words with that first letter, sorted case-insensitively.\n- Return a plain dict (convert the defaultdict) with keys in alphabetical order.\n- Empty strings are skipped.\n\n"
   "Examples:\n- group_by_letter([\"banana\", \"Apple\", \"avocado\", \"cherry\"]) returns {\"a\": [\"Apple\", \"avocado\"], \"b\": [\"banana\"], \"c\": [\"cherry\"]}\n\n"
   "Edge cases: an empty list returns {}; the result's type is dict, not defaultdict.",
   'from collections import defaultdict\n\n\ndef group_by_letter(words):\n    """Group words by lower-case first letter, each group sorted case-insensitively."""\n    groups = defaultdict(list)\n    for word in words:\n        if word:\n            groups[word[0].lower()].append(word)\n    return {letter: sorted(groups[letter], key=str.lower) for letter in sorted(groups)}\n',
   [("Groups and sorts", "assert group_by_letter(['banana', 'Apple', 'avocado', 'cherry']) == {'a': ['Apple', 'avocado'], 'b': ['banana'], 'c': ['cherry']}"),
    ("Keys in order, plain dict", "r = group_by_letter(['zeta', 'alpha', 'mu'])\nassert list(r) == ['a', 'm', 'z'] and type(r) is dict, 'Return a plain dict with keys in alphabetical order'"),
    ("Empty input and empty words", "assert group_by_letter([]) == {} and group_by_letter(['', 'x']) == {'x': ['x']}"),
    ("Uses defaultdict", "assert 'defaultdict' in code")],
   ['from collections import defaultdict\ndef group_by_letter(words):\n    g = defaultdict(list)\n    for w in words:\n        g[w[0]].append(w)\n    return dict(g)\n',
    'from collections import defaultdict\ndef group_by_letter(words):\n    g = defaultdict(list)\n    for w in words:\n        if w:\n            g[w[0].lower()].append(w)\n    return g\n'],
   ["defaultdict(list) creates an empty list the first time a key is used.", "Use word[0].lower() as the key and skip empty strings.", "Build the final dict with sorted keys and sorted(group, key=str.lower) for each value."],
   "defaultdict removes the \"is this key there yet?\" check from the loop. Converting to a plain dict at the end hides that detail from callers, and sorting both levels makes the output predictable.",
   'from collections import defaultdict\n\n\ndef group_by_letter(words):\n    """Group words by lower-case first letter, each group sorted case-insensitively."""\n    pass\n')

# ---------------------------------------------------------------- chapter 11
ex("11.1", "Append and count lines",
   "Write append_line(path, text) and count_lines(path).\n\n"
   "Specification:\n- append_line adds text and a newline to the end of the file, creating it if needed, using UTF-8.\n- count_lines returns the number of lines in the file, or 0 if the file does not exist.\n\n"
   "Examples:\n- after append_line(\"log.txt\", \"one\") and append_line(\"log.txt\", \"two\"), count_lines(\"log.txt\") is 2 and the file contains one\\ntwo\\n\n\n"
   "Edge cases: count_lines(\"missing.txt\") is 0; appending never erases earlier lines.",
   'def append_line(path, text):\n    with open(path, "a", encoding="utf-8") as f:\n        f.write(text + "\\n")\n\n\ndef count_lines(path):\n    try:\n        with open(path, encoding="utf-8") as f:\n            return sum(1 for _ in f)\n    except FileNotFoundError:\n        return 0\n',
   [("Appends", "append_line('log.txt', 'one')\nappend_line('log.txt', 'two')\nassert open('log.txt', encoding='utf-8').read() == 'one\\ntwo\\n'\nassert count_lines('log.txt') == 2"),
    ("Missing file", "assert count_lines('missing.txt') == 0"),
    ("Keeps earlier lines", "open('notes.txt', 'w', encoding='utf-8').write('keep me\\n')\nappend_line('notes.txt', 'added ✔')\nassert open('notes.txt', encoding='utf-8').read() == 'keep me\\nadded ✔\\n', 'Open with mode \"a\" so earlier lines stay'")],
   ['def append_line(path, text):\n    with open(path, "w", encoding="utf-8") as f:\n        f.write(text + "\\n")\ndef count_lines(path):\n    try:\n        with open(path, encoding="utf-8") as f:\n            return len(f.readlines())\n    except FileNotFoundError:\n        return 0\n',
    'def append_line(path, text):\n    with open(path, "a", encoding="utf-8") as f:\n        f.write(text)\ndef count_lines(path):\n    with open(path, encoding="utf-8") as f:\n        return len(f.readlines())\n'],
   ["Mode \"a\" appends and creates the file if needed; mode \"w\" would erase it.", "Write text + \"\\n\" so each call adds one line.", "Count lines by looping over the file, and catch FileNotFoundError."],
   "The file mode decides everything here: \"a\" keeps what is there, \"w\" empties the file first. Looping over the file object counts lines without loading the whole file into memory.",
   'def append_line(path, text):\n    pass\n\n\ndef count_lines(path):\n    pass\n')

ex("11.2", "The longest line",
   "Write longest_line(path) that returns the line number and text of the longest line in a file.\n\n"
   "Specification:\n- Return a tuple (line_number, text), counting lines from 1, with the newline removed from text.\n- If several lines tie, return the first.\n- An empty file returns None.\n- Use a with statement so the file is always closed.\n\n"
   "Examples:\n- for a file with the lines \"tea\", \"biscuits\" and \"jam\", the result is (2, \"biscuits\")\n\n"
   "Edge cases: an empty file returns None; ties return the earliest line.",
   'def longest_line(path):\n    """Return (line_number, text) of the longest line, or None for an empty file."""\n    best = None\n    with open(path, encoding="utf-8") as f:\n        for number, line in enumerate(f, start=1):\n            text = line.rstrip("\\n")\n            if best is None or len(text) > len(best[1]):\n                best = (number, text)\n    return best\n',
   [("Longest line", "open('a.txt', 'w', encoding='utf-8').write('tea\\nbiscuits\\njam\\n')\nassert longest_line('a.txt') == (2, 'biscuits')"),
    ("Ties return the first", "open('b.txt', 'w', encoding='utf-8').write('abc\\nxyz\\nab\\n')\nassert longest_line('b.txt') == (1, 'abc'), 'For a tie, return the first line'"),
    ("Empty file", "open('c.txt', 'w', encoding='utf-8').write('')\nassert longest_line('c.txt') is None"),
    ("No newline at the end", "open('d.txt', 'w', encoding='utf-8').write('short\\nthe very last line')\nassert longest_line('d.txt') == (2, 'the very last line')"),
    ("Uses with", "assert 'with open' in code, 'Open the file with a with statement'")],
   ['def longest_line(path):\n    best = None\n    with open(path, encoding="utf-8") as f:\n        for n, line in enumerate(f):\n            t = line.rstrip("\\n")\n            if best is None or len(t) > len(best[1]):\n                best = (n, t)\n    return best\n',
    'def longest_line(path):\n    best = None\n    with open(path, encoding="utf-8") as f:\n        for n, line in enumerate(f, start=1):\n            if best is None or len(line) >= len(best[1]):\n                best = (n, line.rstrip("\\n"))\n    return best\n'],
   ["enumerate(f, start=1) gives line numbers from 1 while looping over the file.", "Strip the newline before comparing lengths, so the last line is not short-changed.", "Only replace the best line when the new one is strictly longer, so ties keep the first."],
   "Looping over the file with enumerate reads one line at a time and numbers it for free. Comparing with > rather than >= keeps the first of equal lines, and stripping the newline first keeps the comparison fair for a last line with no newline.",
   'def longest_line(path):\n    """Return (line_number, text) of the longest line, or None for an empty file."""\n    pass\n')

ex("11.3", "A small grep",
   "Write grep(path, word) that returns the lines of a file containing word, case-insensitively, each prefixed with its line number.\n\n"
   "Specification:\n- Read the file lazily, one line at a time.\n- A line matches if word, lower-cased, appears in the line, lower-cased.\n- Return a list of strings in the form \"3: the matching line\", without the newline.\n\n"
   "Examples:\n- for a file with the lines \"ERROR disk full\", \"ok\" and \"error: timeout\", grep(path, \"error\") returns [\"1: ERROR disk full\", \"3: error: timeout\"]\n\n"
   "Edge cases: no matches returns []; a missing file raises FileNotFoundError (do not hide it).",
   'def grep(path, word):\n    """Return \'n: line\' for each line containing word, case-insensitively."""\n    word = word.lower()\n    matches = []\n    with open(path, encoding="utf-8") as f:\n        for number, line in enumerate(f, start=1):\n            if word in line.lower():\n                matches.append(f"{number}: {line.rstrip(chr(10))}")\n    return matches\n',
   [("Matches", "open('log.txt', 'w', encoding='utf-8').write('ERROR disk full\\nok\\nerror: timeout\\n')\nassert grep('log.txt', 'error') == ['1: ERROR disk full', '3: error: timeout']"),
    ("Case-insensitive word", "open('log.txt', 'w', encoding='utf-8').write('Tea time\\n')\nassert grep('log.txt', 'TEA') == ['1: Tea time']"),
    ("No matches", "open('log.txt', 'w', encoding='utf-8').write('a\\nb\\n')\nassert grep('log.txt', 'zzz') == []"),
    ("Missing file is an error", "try:\n    grep('missing.txt', 'x')\nexcept FileNotFoundError:\n    pass\nelse:\n    raise AssertionError('A missing file should raise FileNotFoundError')")],
   ['def grep(path, word):\n    out = []\n    with open(path, encoding="utf-8") as f:\n        for n, line in enumerate(f, start=1):\n            if word in line:\n                out.append(f"{n}: {line.rstrip()}")\n    return out\n',
    'def grep(path, word):\n    try:\n        with open(path, encoding="utf-8") as f:\n            return [f"{n}: {l.rstrip()}" for n, l in enumerate(f, start=1) if word.lower() in l.lower()]\n    except FileNotFoundError:\n        return []\n'],
   ["Loop over the file object with enumerate(f, start=1).", "Compare lower-cased versions of both the word and the line.", "Do not catch FileNotFoundError: a missing file should be reported."],
   "Iterating over the file reads it lazily, so grep works on logs of any size. Lower-casing both sides makes the match case-insensitive, and letting the missing-file error through tells the caller about a real problem instead of pretending there were no matches.",
   'def grep(path, word):\n    """Return \'n: line\' for each line containing word, case-insensitively."""\n    pass\n')

for _eid, _bads in BAD.items():
    for _i, _b in enumerate(_bads):
        assert _b != SOLUTIONS[_eid], f"{_eid} bad#{_i} is identical to the solution"
