#!/usr/bin/env python3
"""Put deep.json (expanded lessons) into the course page's content. Safe to run again."""
import json, sys
page = sys.argv[1] if len(sys.argv) > 1 else "course.html"
deep = json.load(open(sys.argv[2] if len(sys.argv) > 2 else "deep.json"))
for v in deep.values():
    v.pop("_words", None)
s = open(page, encoding="utf-8").read()
i = s.find("window.PYCC_CONTENT=") + len("window.PYCC_CONTENT=")
j = s.find(";</script>", i)
c = json.loads(s[i:j].replace("<\\!", "<!"))
c["deep"] = deep
s = s[:i] + json.dumps(c).replace("</", "<\\/").replace("<!", "<\\!") + s[j:]
open(page, "w", encoding="utf-8").write(s)
print(f"{len(deep)} expanded lessons in {page}")
