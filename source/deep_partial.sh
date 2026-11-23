#!/bin/sh
# Rebuild some lesson files with a given Python and merge them into deep.json (the rest is kept).
# usage: ./deep_partial.sh /path/to/python deep/py/a.txt deep/py/b.txt ...
cd "$(dirname "$0")"; PY="$1"; shift
cp deep.json deep.keep.json
"$PY" deep_build.py "$@" | grep -i 'problem\|built'
python3 - <<'PY'
import json
full=json.load(open('deep.keep.json'));part=json.load(open('deep.json'))
keep_checks={(k,i):x.get('check') for k,v in full.items() for i,x in enumerate(v['examples'])}
full.update(part)
json.dump(full,open('deep.json','w'),ensure_ascii=False)
print(len(part),'lessons rebuilt,',len(full),'in total')
PY
