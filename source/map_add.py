"""Add a Map tab to the course engine: a roadmap.sh-style tree of every module and lesson,
coloured by the learner's progress, with each node linking to its lesson in the curriculum.

usage: python3 map_add.py course.html   (idempotent)
"""
import sys

CSS = r"""/* MAP:BEGIN */
.mapv{max-width:1080px;margin:0 auto}
.map-top{display:flex;flex-wrap:wrap;gap:12px 20px;align-items:flex-end;justify-content:space-between;margin:4px 0 18px}
.map-top h1{margin:0 0 4px}
.map-tracks{display:flex;flex-wrap:wrap;gap:6px}
.map-tracks button{font:inherit;font-size:.85rem;padding:6px 12px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--ink);cursor:pointer}
.map-tracks button[aria-pressed="true"]{background:var(--ink);color:var(--surface);border-color:var(--ink)}
.map-prog{display:flex;align-items:center;gap:10px;font-size:.85rem;color:var(--muted);margin:0 0 6px}
.map-prog .bar{flex:1;max-width:320px;height:8px;border-radius:99px;background:var(--raised);overflow:hidden}
.map-prog .bar i{display:block;height:100%;background:var(--good)}
.map-legend{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:.8rem;color:var(--muted);margin:0 0 22px}
.map-legend span{display:inline-flex;align-items:center;gap:6px}
.map-legend i{width:14px;height:14px;border-radius:4px;border:2px solid var(--line);background:var(--surface)}
.map-legend .l-done{background:var(--good-soft);border-color:var(--good)}
.map-legend .l-next{border-color:var(--blue);box-shadow:0 0 0 3px var(--blue-soft)}
.map-legend .l-rev{background:var(--warn-soft);border-color:var(--warn)}
.map-legend .l-mod{background:var(--yellow);border-color:var(--yellow-ink)}
.maptree{position:relative;padding:6px 0 30px}
.maptree::before{content:"";position:absolute;left:50%;top:0;bottom:0;width:3px;margin-left:-1.5px;background:var(--blue);opacity:.55;border-radius:2px}
.mrow{position:relative;display:grid;grid-template-columns:1fr minmax(180px,250px) 1fr;align-items:center;column-gap:0;margin:0 0 26px}
.mnode{position:relative;z-index:1;grid-column:2;display:block;width:100%;text-align:center;font:inherit;cursor:pointer;
  background:var(--yellow);color:var(--yellow-ink);border:2px solid var(--yellow-ink);border-radius:8px;padding:9px 12px;box-shadow:0 2px 0 var(--yellow-ink)}
.mnode:hover{transform:translateY(-1px)}
.mnode .mn{display:block;font-family:var(--font-mono);font-size:.72rem;opacity:.8}
.mnode .mt{display:block;font-weight:700;line-height:1.25}
.mnode .mc{display:block;font-size:.75rem;margin-top:3px}
.mnode.done{background:var(--good);color:#fff;border-color:var(--good);box-shadow:0 2px 0 rgba(0,0,0,.25)}
.mnode.part::after{content:"";position:absolute;left:8px;right:8px;bottom:4px;height:3px;border-radius:2px;background:linear-gradient(90deg,var(--good) var(--p),transparent var(--p));opacity:.9}
.mside{display:flex;flex-direction:column;gap:6px;position:relative;padding:6px 0}
.mside.l{grid-column:1;grid-row:1;align-items:flex-end;padding-right:26px;margin-right:0;border-right:2px dashed var(--line)}
.mside.r{grid-column:3;grid-row:1;align-items:flex-start;padding-left:26px;border-left:2px dashed var(--line)}
.mside.l::after,.mside.r::after{content:"";position:absolute;top:50%;width:0;border-top:2px dashed var(--line)}
.mside.l::after{right:-2px}
.mside.r::after{left:-2px}
.mrow .mside.l{margin-right:18px}
.mrow .mside.r{margin-left:18px}
.mrow .mside.l::before,.mrow .mside.r::before{content:"";position:absolute;top:50%;width:18px;border-top:2px dashed var(--line)}
.mrow .mside.l::before{right:-20px}
.mrow .mside.r::before{left:-20px}
.leaf{position:relative;display:inline-flex;align-items:center;gap:7px;max-width:100%;font:inherit;font-size:.86rem;text-align:left;cursor:pointer;
  background:var(--surface);color:var(--ink);border:2px solid var(--line);border-radius:6px;padding:6px 10px;line-height:1.25}
.leaf:hover{border-color:var(--blue)}
.leaf .li{font-family:var(--font-mono);font-size:.72rem;color:var(--muted);flex:none}
.leaf .lt{min-width:0}
.leaf .lx{font-size:.7rem;color:var(--muted);flex:none}
.leaf .ck{flex:none;width:16px;height:16px;border-radius:50%;border:2px solid var(--line);display:inline-grid;place-items:center;font-size:.65rem;line-height:1}
.mside.l .leaf::after,.mside.r .leaf::after{content:"";position:absolute;top:50%;width:24px;border-top:2px dashed var(--line)}
.mside.l .leaf::after{right:-28px}
.mside.r .leaf::after{left:-28px}
.leaf.done{background:var(--good-soft);border-color:var(--good)}
.leaf.done .ck{background:var(--good);border-color:var(--good);color:#fff}
.leaf.done .lt{text-decoration:line-through;text-decoration-color:color-mix(in srgb,var(--good) 60%,transparent)}
.leaf.rev{background:var(--warn-soft);border-color:var(--warn)}
.leaf.next{border-color:var(--blue);box-shadow:0 0 0 3px var(--blue-soft)}
.leaf .here{flex:none;font-size:.68rem;font-weight:700;color:var(--surface);background:var(--blue);border-radius:99px;padding:1px 7px}
.leaf.proj .li::before{content:"\2605 ";color:var(--warn)}
.map-end{position:relative;z-index:1;margin:0 auto;width:max-content;max-width:100%;text-align:center;font-size:.85rem;color:var(--muted);background:var(--bg);padding:6px 12px;border:2px dashed var(--line);border-radius:8px}
@media (max-width:720px){
  .maptree::before{left:14px}
  .mrow{grid-template-columns:1fr;margin-bottom:20px;padding-left:32px}
  .mnode{grid-column:1;text-align:left}
  .mside.l,.mside.r{grid-column:1;grid-row:auto;align-items:stretch;border:0;border-left:2px dashed var(--line);margin:6px 0 0 10px!important;padding:2px 0 2px 18px}
  .mside.r{margin-top:0!important}
  .mside.l::after,.mside.r::after,.mrow .mside.l::before,.mrow .mside.r::before{display:none}
  .mside.l .leaf::after,.mside.r .leaf::after{left:-20px;right:auto;width:16px}
  .leaf{width:100%}
}
/* MAP:END */
"""

JS = r"""/* MAP:BEGIN */
function mapLeaf(i,next){
  var done=!!S.done[i.id],rv=S.rev[i.id],due=!done?false:!!(rv&&rv.due<=today());
  var exs=i.ex||[],exd=exs.filter(function(e){return S.ex[e.id];}).length;
  var cls="leaf"+(done?" done":"")+(due?" rev":"")+(next?" next":"")+(i.kind==="project"?" proj":"");
  var tip=i.id+" "+i.t+(done?" (complete"+(due?", review due":"")+")":next?" (next up)":"")+(exs.length?". Exercises "+exd+"/"+exs.length:"");
  return "<button type=\"button\" class=\""+cls+"\" data-act=\"open\" data-id=\""+esc(i.id)+"\" title=\""+esc(tip)+"\" aria-label=\""+esc(tip)+"\">"+
    "<span class=\"ck\" aria-hidden=\"true\">"+(done?"✓":"")+"</span><span class=\"li\">"+esc(i.id)+"</span><span class=\"lt\">"+esc(i.t)+"</span>"+
    (exs.length?"<span class=\"lx\">"+exd+"/"+exs.length+"</span>":"")+(next?"<span class=\"here\">Next</span>":"")+"</button>";
}
function viewMap(){
  var tr=S.mapTrack||S.track||"F",mods=M.filter(function(m){return m.track===tr;});
  var nx=nextItem(),all=[],done=0;
  mods.forEach(function(m){m.items.forEach(function(i){all.push(i);if(S.done[i.id])done++;});});
  var pct=all.length?Math.round(done/all.length*100):0;
  var trk=["F","A","P"].filter(function(t){return M.some(function(m){return m.track===t;});}).map(function(t){return [t,trackName(t)];});
  var h="<div class=\"mapv\"><div class=\"map-top\"><div><h1>Map</h1><p class=\"muted\" style=\"margin:0\">Every module and lesson as one tree. Click any box to open it in the curriculum; it fills in as you finish lessons.</p></div>"+
    "<div class=\"map-tracks\" role=\"group\" aria-label=\"Track\">"+trk.map(function(t){return "<button type=\"button\" data-act=\"maptrack\" data-v=\""+t[0]+"\" aria-pressed=\""+(tr===t[0])+"\">"+t[1]+"</button>";}).join("")+"</div></div>"+
    "<div class=\"map-prog\"><span>"+done+" of "+all.length+" lessons complete</span><span class=\"bar\"><i style=\"width:"+pct+"%\"></i></span><b>"+pct+"%</b></div>"+
    "<div class=\"map-legend\"><span><i class=\"l-mod\"></i>Module</span><span><i></i>Not started</span><span><i class=\"l-next\"></i>Next lesson</span><span><i class=\"l-done\"></i>Complete</span><span><i class=\"l-rev\"></i>Review due</span></div>"+
    "<div class=\"maptree\">";
  mods.forEach(function(m){
    var n=m.items.length,d=m.items.filter(function(i){return S.done[i.id];}).length;
    var first=m.items.find(function(i){return !S.done[i.id];})||m.items[0];
    var half=Math.ceil(n/2),L=m.items.slice(0,half),R=m.items.slice(half);
    var side=function(list,c){return list.length?"<div class=\"mside "+c+"\">"+list.map(function(i){return mapLeaf(i,nx&&nx.id===i.id);}).join("")+"</div>":"";};
    h+="<div class=\"mrow\" id=\"map-"+m.id+"\">"+side(L,"l")+
      "<button type=\"button\" class=\"mnode"+(d===n&&n?" done":d?" part":"")+"\" style=\"--p:"+(n?Math.round(d/n*100):0)+"%\" data-act=\"open\" data-id=\""+esc(first.id)+"\" title=\""+esc(m.n+" "+m.t+": "+d+" of "+n+" lessons complete")+"\">"+
      "<span class=\"mn\">"+esc(m.n)+"</span><span class=\"mt\">"+esc(m.t)+"</span><span class=\"mc\">"+(d===n&&n?"✓ Complete":d+" / "+n+" lessons")+"</span></button>"+side(R,"r")+"</div>";
  });
  h+="<div class=\"map-end\">"+(done===all.length&&all.length?"Track complete. Well done.":"Keep going: the next lesson is highlighted.")+"</div></div></div>";
  return h;
}
document.addEventListener("click",function(ev){
  var b=ev.target.closest&&ev.target.closest("[data-act=\"maptrack\"]");if(!b)return;
  S.mapTrack=b.dataset.v;save();render();
});
/* MAP:END */
"""


def main(path):
    s = open(path, encoding="utf-8").read()

    def cut(text):
        while "/* MAP:BEGIN */" in text:
            a = text.index("/* MAP:BEGIN */")
            b = text.index("/* MAP:END */", a) + len("/* MAP:END */\n")
            text = text[:a] + text[b:]
        return text

    s = cut(s)

    def rep(a, b):
        nonlocal s
        if b in s:
            return
        assert s.count(a) == 1, (a[:70], s.count(a))
        s = s.replace(a, b)

    i = s.index("</style>")
    s = s[:i] + CSS + s[i:]
    rep('      <a href="#curriculum" data-tab="curriculum">Curriculum</a>\n',
        '      <a href="#curriculum" data-tab="curriculum">Curriculum</a>\n      <a href="#map" data-tab="map">Map</a>\n')
    rep('return h==="curriculum"||h==="grades"?h:"control";}', 'return h==="curriculum"||h==="grades"||h==="map"?h:"control";}')
    rep('el.innerHTML=v==="curriculum"?viewCurriculum():v==="grades"?viewGrades():viewControl();',
        'el.innerHTML=v==="curriculum"?viewCurriculum():v==="grades"?viewGrades():v==="map"?viewMap():viewControl();')
    j = s.index("function render(){")
    s = s[:j] + JS + s[j:]
    open(path, "w", encoding="utf-8").write(s)
    print("map added to", path)


if __name__ == "__main__":
    main(sys.argv[1])
