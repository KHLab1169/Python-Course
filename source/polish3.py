"""Page code for expanded lessons: The idea, How it works, more worked examples, Common mistakes, Key points."""
import shutil
SRC = "course.html"
shutil.copy(SRC, "course.pre-polish3.html")
s = open(SRC, encoding="utf-8").read()


def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, f"expected {count} of {old[:80]!r}, found {n}"
    s = s.replace(old, new)


rep('''  return "<section class=\\"eg\\"><h4>Worked example</h4>"''',
    '''  return "<section class=\\"eg\\"><h4>Worked example"+(DEEP[i.id]?" 1":"")+"</h4>"''')
rep('''"</span><button type=\\"button\\" class=\\"linkbtn focusbtn\\" data-act=\\"focus\\" data-id=\\""+i.id+"\\">"+(FOCUS===i.id?"Leave focus mode":"Focus mode")+"</button></div><p class=\\"muted\\">"+esc(i.learn)+"</p>"+exampleBlock(i)+quickChecks(i)+''',
    '''"</span><button type=\\"button\\" class=\\"linkbtn focusbtn\\" data-act=\\"focus\\" data-id=\\""+i.id+"\\">"+(FOCUS===i.id?"Leave focus mode":"Focus mode")+"</button></div><p class=\\"muted\\">"+esc(i.learn)+"</p>"+deepIntro(i)+exampleBlock(i)+quickChecks(i)+deepExamples(i)+deepOutro(i)+''')
rep('''IDX.push({k:"Lesson",id:i.id,lid:i.id,t:i.t,sub:trackName(i.mod.track)+" · "+i.mod.n+" "+i.mod.t,tt:(i.id+" "+i.t).toLowerCase(),txt:(i.learn+" "+i.mod.t).toLowerCase()});''',
    '''var dp=DEEP[i.id];
    IDX.push({k:"Lesson",id:i.id,lid:i.id,t:i.t,sub:trackName(i.mod.track)+" · "+i.mod.n+" "+i.mod.t,tt:(i.id+" "+i.t).toLowerCase(),txt:(i.learn+" "+i.mod.t+(dp?" "+dp.idea.join(" ")+" "+dp.keys.join(" "):"")).toLowerCase()});''')

JS = r'''
/* ================= expanded lessons ================= */
var DEEP=(window.PYCC_CONTENT||{}).deep||{};
function md(t){
  var codes=[];
  var s=esc(String(t).replace(/`([^`]+)`/g,function(_,c){codes.push(c);return "\u0000"+(codes.length-1)+"\u0000";}));
  s=s.replace(/\*\*(.+?)\*\*/g,"<b>$1</b>");
  return s.replace(/\u0000(\d+)\u0000/g,function(_,n){return "<code>"+esc(codes[+n])+"</code>";});
}
function deepIntro(i){
  var d=DEEP[i.id];if(!d)return "";
  return "<section class=\"deep\"><h4 class=\"lbl\">The idea</h4>"+d.idea.map(function(p){return "<p>"+md(p)+"</p>";}).join("")+
    (d.how&&d.how.length?"<h4 class=\"lbl\">How it works</h4><ul class=\"how\">"+d.how.map(function(h){return "<li>"+md(h)+"</li>";}).join("")+"</ul>":"")+"</section>";
}
function deepExamples(i){
  var d=DEEP[i.id];if(!d||!d.examples)return "";
  return d.examples.map(function(x,k){
    return "<section class=\"eg\"><h4>Worked example "+(k+2)+"</h4>"+(x.title?"<p class=\"egt\">"+esc(x.title)+"</p>":"")+codeBlock(x.code,x.lang,"dx|"+i.id+"|"+k,x.lang)+
      (x.output?"<div class=\"out\"><h4 style=\"margin-bottom:4px\">"+(x.label||(x.sample?"Sample output":"Output"))+"</h4><pre>"+esc(x.output)+"</pre></div>":"")+
      (x.note?"<p class=\"note\">"+md(x.note)+"</p>":"")+"</section>";
  }).join("");
}
function deepOutro(i){
  var d=DEEP[i.id];if(!d)return "";
  return (d.mistakes&&d.mistakes.length?"<section class=\"deep traps\"><h4 class=\"lbl\">Common mistakes</h4><ul>"+d.mistakes.map(function(m){return "<li>"+md(m)+"</li>";}).join("")+"</ul></section>":"")+
    (d.keys&&d.keys.length?"<section class=\"keys\"><h4 class=\"lbl\">Key points</h4><ul>"+d.keys.map(function(k){return "<li>"+md(k)+"</li>";}).join("")+"</ul></section>":"");
}
'''
rep('''
render();
initCloud();
})();''', JS + '''
render();
initCloud();
})();''')

CSS = r'''
/* ===== expanded lessons ===== */
.deep{display:flex;flex-direction:column;gap:10px;max-width:72ch}
.deep h4.lbl{margin:6px 0 0}
.deep p{line-height:1.65}
.deep code,.keys code,.eg .note code{font-family:var(--font-mono);font-size:.86em;background:var(--raised);padding:1px 5px;border-radius:4px}
.deep ul{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:6px;line-height:1.55}
.deep ul.how li::marker{color:var(--blue)}
.traps ul{list-style:none;padding-left:0}
.traps li{padding-left:22px;position:relative}
.traps li::before{content:"!";position:absolute;left:0;top:1px;width:15px;height:15px;border-radius:50%;background:var(--warn-soft);color:var(--warn);font:700 .7rem/15px var(--font-mono);text-align:center}
.keys{border-radius:8px;background:var(--blue-soft);padding:12px 16px;max-width:72ch}
.keys h4.lbl{margin:0 0 6px}
.keys ul{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:5px;line-height:1.5}
'''
rep('''/* ===== polish layer 2 ===== */''', CSS + '''/* ===== polish layer 2 ===== */''')
open(SRC, "w", encoding="utf-8").write(s)
print("expanded-lesson rendering added")
