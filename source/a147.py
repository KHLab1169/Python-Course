LESSON = {"id": "A14.7", "t": "Modern Python: what 3.12, 3.13 and 3.14 added", "min": 90,
  "learn": "Template strings (t-strings) for safe HTML and SQL, deferred annotations, except without brackets, copy.replace, itertools.batched, the type statement, TypeIs and @deprecated, and the free-threaded build. The course editor runs Python 3.14.",
  "ex": [
   ["Safe HTML and SQL with t-strings",
    "Python 3.14 adds template strings: t\"Hi {name}\" looks like an f-string, but instead of a str it gives a string.templatelib.Template that keeps the text and the values apart. Iterating a Template yields its parts in order: str for the text and Interpolation objects (with value, conversion and format_spec) for each {...}. Write two functions.\n\n"
    "html(template):\n"
    "- Keep the text parts as they are.\n"
    "- For each interpolation, apply its conversion (!r, !s or !a) and format spec the way an f-string would, then escape the result with html.escape(..., quote=True).\n"
    "- If an interpolation's value is itself a Template, render it with html() instead of escaping it, so fragments can be nested.\n"
    "- A plain str raises TypeError: an f-string has already mixed markup and values together.\n\n"
    "sql(template) returns (query, params):\n"
    "- Text parts go into the query; each value becomes a ? placeholder and is added to params, in order.\n"
    "- A nested Template adds its own text to the query and its values to params.\n"
    "- A plain str raises TypeError.\n\n"
    "Examples: html(t\"<p>{name}</p>\") with name = \"<b>\" gives \"<p>&lt;b&gt;</p>\"; sql(t\"SELECT * FROM staff WHERE name = {name}\") gives (\"SELECT * FROM staff WHERE name = ?\", [name]).\n\n"
    "Edge cases: {price:,.2f} formats before escaping; html(t\"\") is \"\"; the query from sql() runs safely with sqlite3 even when a value contains quotes."]]}
EXAMPLE = {"title": "f-strings versus t-strings",
  "code": '''from string.templatelib import Interpolation, Template

name = "<img src=x onerror=alert(1)>"
f = f"<p>Hello {name}!</p>"
t = t"<p>Hello {name}!</p>"

print(type(f).__name__, "->", f)
print(type(t).__name__, "->", t.strings, "values:", t.values)
for part in t:
    kind = "text " if isinstance(part, str) else "value"
    print(" ", kind, repr(part if isinstance(part, str) else part.value))
''',
  "note": "The f-string has already glued the dangerous value into the markup, so nothing downstream can tell them apart. The t-string keeps the text parts and the values separate, so a function such as html() or sql() can escape or parameterise the values and leave the template text alone. That separation is the whole point of PEP 750."}
AUTO = {"hints": ["Check isinstance(template, Template) first and raise TypeError otherwise; then loop with for part in template.",
                   "A part is either a str (keep it) or an Interpolation: look at part.value, part.conversion (\"r\", \"s\", \"a\" or None) and part.format_spec, and finish with format(value, part.format_spec).",
                   "For a nested Template call the same function recursively; in sql(), extend the outer params with the inner ones."],
        "explain": "A t-string gives the function receiving it both halves of the string: the trusted text written by the programmer and the untrusted values. Escaping only the values (html) or replacing them with placeholders (sql) is exactly what template engines and database drivers do, now with a language feature behind it, which is why PEP 750 calls out HTML, SQL, logging and shell commands as the main uses. Refusing plain str matters: once an f-string has run, the boundary is gone and no function can recover it."}
QUIZ = [
 ("What does t\"Hello {name}\" evaluate to in Python 3.14?", ["A string.templatelib.Template that keeps the text and the value of name separate", "A str, exactly like an f-string", "A function that formats later", "A SyntaxError"], 0,
  "t-strings (PEP 750) produce a Template; code that receives it decides how to combine the parts, for example by escaping the values."),
 ("Which line is valid in Python 3.14 but a syntax error in 3.13?", ["except ValueError, TypeError:", "match command:", "type Pair[T] = tuple[T, T]", "print(f\"{x=}\")"], 0,
  "PEP 758 allows several exception types without brackets when there is no as clause. The type statement arrived in 3.12 and match in 3.10."),
]
