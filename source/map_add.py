"""Add a Map tab to the course engine: an infographic of the learner's progress and a
roadmap.sh-style tree of every module and lesson, with each node linking to its lesson.

The tree's connectors are drawn as an SVG overlay after layout, so they follow the real
positions of the boxes at any width. The tab sits first, before Overview.

usage: python3 map_add.py course.html   (idempotent)
"""
import sys

CSS = r"""/* MAP:BEGIN */
.mapv{max-width:1120px;margin:0 auto;--m-line:color-mix(in srgb,var(--muted) 38%,transparent);--m-done:var(--good);--m-accent:var(--blue)}
.mapv *{box-sizing:border-box}
.map-hero{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:18px;margin:6px 0 22px}
.mh-card{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:20px 22px;min-width:0}
.mh-main{display:flex;gap:22px;align-items:center;background:linear-gradient(135deg,var(--surface) 0%,var(--surface) 55%,color-mix(in srgb,var(--blue-soft) 70%,var(--surface)) 100%)}
.mh-ring{flex:none;position:relative;width:132px;height:132px}
.mh-ring svg{width:100%;height:100%;transform:rotate(-90deg)}
.mh-ring .bg{stroke:var(--raised)}
.mh-ring .fg{stroke:var(--m-done);transition:stroke-dashoffset .9s cubic-bezier(.2,.8,.2,1)}
.mh-ring .pc{position:absolute;inset:0;display:grid;place-content:center;text-align:center}
.mh-ring .pc b{font-family:var(--font-display);font-size:2.1rem;line-height:1;letter-spacing:-.02em}
.mh-ring .pc span{font-size:.72rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-top:4px}
.mh-txt{min-width:0}
.mh-txt h1{margin:0 0 4px;font-family:var(--font-display);font-size:1.9rem;letter-spacing:-.02em}
.mh-txt p{margin:0 0 12px;color:var(--muted)}
.map-tracks{display:flex;flex-wrap:wrap;gap:6px}
.map-tracks button{font:inherit;font-size:.8rem;display:inline-flex;align-items:center;gap:8px;padding:6px 10px 6px 12px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--ink);cursor:pointer}
.map-tracks button i{display:inline-block;width:34px;height:5px;border-radius:9px;background:var(--raised);overflow:hidden;position:relative}
.map-tracks button i::after{content:"";position:absolute;inset:0 auto 0 0;width:var(--w);background:var(--m-done)}
.map-tracks button[aria-pressed="true"]{background:var(--ink);color:var(--surface);border-color:var(--ink)}
.mh-stats{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.mh-stat{border-radius:12px;padding:12px 14px;background:var(--bg);min-width:0}
.mh-stat b{display:block;font-family:var(--font-display);font-size:1.5rem;line-height:1.1}
.mh-stat span{font-size:.78rem;color:var(--muted)}
.mh-stat .sbar{display:block;height:4px;border-radius:4px;background:var(--raised);margin-top:8px;overflow:hidden}
.mh-stat .sbar i{display:block;height:100%;background:var(--sc,var(--m-done))}
.mh-next{grid-column:1/-1;display:flex;align-items:center;gap:12px;border-radius:12px;padding:12px 14px;background:var(--blue-soft);color:var(--ink);border:0;font:inherit;text-align:left;cursor:pointer;width:100%}
.mh-next:hover{filter:brightness(.98)}
.mh-next .lbl{font-size:.7rem;text-transform:uppercase;letter-spacing:.08em;color:var(--blue);font-weight:700}
.mh-next b{display:block;font-weight:600}
.mh-next .go{margin-left:auto;flex:none;width:32px;height:32px;border-radius:50%;background:var(--blue);color:#fff;display:grid;place-items:center;font-size:1rem}
.map-strip{display:flex;gap:3px;margin:0 0 8px;padding:0}
.map-strip button{flex:1;min-width:0;height:26px;border:0;border-radius:5px;cursor:pointer;background:var(--raised);position:relative;overflow:hidden;padding:0;font:inherit}
.map-strip button::before{content:"";position:absolute;inset:0 auto 0 0;width:var(--p);background:var(--m-done);opacity:.9}
.map-strip button span{position:relative;font-family:var(--font-mono);font-size:.62rem;color:var(--ink);opacity:.75}
.map-strip button.cur{outline:2px solid var(--blue);outline-offset:1px}
.map-strip button:hover{filter:brightness(.95)}
.map-legend{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:.78rem;color:var(--muted);margin:10px 0 18px}
.map-legend span{display:inline-flex;align-items:center;gap:6px}
.map-legend i{width:12px;height:12px;border-radius:50%;border:2px solid var(--line);background:var(--surface)}
.map-legend .l-done{background:var(--m-done);border-color:var(--m-done)}
.map-legend .l-next{border-color:var(--blue);box-shadow:0 0 0 3px var(--blue-soft)}
.map-legend .l-rev{background:var(--warn);border-color:var(--warn)}
.map-legend .l-mod{border-radius:3px;background:var(--yellow);border-color:var(--yellow)}
.maptree{position:relative;padding:8px 0 10px}
.maplines{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible}
.maplines .spine{stroke:var(--m-line);stroke-width:4;fill:none;stroke-linecap:round}
.maplines .spine-done{stroke:url(#mapgrad);stroke-width:4;fill:none;stroke-linecap:round}
.maplines .br{fill:none;stroke:var(--m-line);stroke-width:1.6;stroke-dasharray:4 4}
.maplines .br.done{stroke:var(--m-done);stroke-width:2;stroke-dasharray:none;opacity:.75}
.maplines .br.next{stroke:var(--blue);stroke-width:2;stroke-dasharray:none}
.mrow{position:relative;display:grid;grid-template-columns:1fr minmax(210px,270px) 1fr;align-items:center;column-gap:56px;margin:0 0 30px;animation:mapin .5s both}
.mrow:nth-child(n+3){animation-delay:.05s}
@keyframes mapin{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){.mrow{animation:none}.mh-ring .fg{transition:none}}
.mnode{position:relative;z-index:1;grid-column:2;display:flex;align-items:center;gap:12px;width:100%;text-align:left;font:inherit;cursor:pointer;
  background:var(--surface);color:var(--ink);border:2px solid var(--line);border-radius:14px;padding:10px 14px 10px 10px;box-shadow:0 6px 18px -12px rgba(0,0,0,.35)}
.mnode:hover{border-color:var(--blue);transform:translateY(-1px)}
.mnode .mring{flex:none;position:relative;width:46px;height:46px}
.mnode .mring svg{width:100%;height:100%;transform:rotate(-90deg)}
.mnode .mring .bg{stroke:var(--raised)}
.mnode .mring .fg{stroke:var(--m-done)}
.mnode .mring b{position:absolute;inset:0;display:grid;place-items:center;font-family:var(--font-mono);font-size:.78rem}
.mnode .mtx{min-width:0}
.mnode .mt{display:block;font-weight:700;line-height:1.2}
.mnode .mc{display:block;font-size:.74rem;color:var(--muted);margin-top:2px}
.mnode.todo{background:var(--yellow);border-color:var(--yellow);color:var(--yellow-ink)}
.mnode.todo .mc{color:inherit;opacity:.75}
.mnode.todo .mring .bg{stroke:color-mix(in srgb,var(--yellow-ink) 18%,transparent)}
.mnode.part{border-color:var(--blue);background:linear-gradient(90deg,var(--blue-soft) var(--p),var(--surface) var(--p))}
.mnode.done{background:var(--m-done);border-color:var(--m-done);color:#fff}
.mnode.done .mc{color:#fff;opacity:.85}
.mnode.done .mring .bg{stroke:rgba(255,255,255,.3)}
.mnode.done .mring .fg{stroke:#fff}
.mnode.cur{box-shadow:0 0 0 4px var(--blue-soft),0 6px 18px -10px rgba(0,0,0,.4)}
.mside{display:flex;flex-direction:column;gap:7px;min-width:0}
.mside.l{grid-column:1;grid-row:1;align-items:flex-end}
.mside.r{grid-column:3;grid-row:1;align-items:flex-start}
.leaf{position:relative;z-index:1;display:inline-flex;align-items:center;gap:8px;max-width:100%;font:inherit;font-size:.84rem;text-align:left;cursor:pointer;
  background:var(--surface);color:var(--ink);border:1.5px solid var(--line);border-radius:999px;padding:5px 12px 5px 6px;line-height:1.25}
.leaf:hover{border-color:var(--blue);background:var(--blue-soft)}
.leaf .ck{flex:none;width:20px;height:20px;border-radius:50%;border:2px solid var(--line);display:inline-grid;place-items:center;font-size:.68rem;line-height:1;color:#fff;background:var(--surface)}
.leaf .li{font-family:var(--font-mono);font-size:.7rem;color:var(--muted);flex:none}
.leaf .lt{min-width:0}
.leaf .lx{flex:none;display:inline-flex;gap:2px}
.leaf .lx i{width:6px;height:6px;border-radius:50%;background:var(--raised)}
.leaf .lx i.on{background:var(--m-done)}
.leaf.done{border-color:color-mix(in srgb,var(--m-done) 55%,transparent);background:var(--good-soft)}
.leaf.done .ck{background:var(--m-done);border-color:var(--m-done)}
.leaf.rev .ck{background:var(--warn);border-color:var(--warn)}
.leaf.rev{border-color:var(--warn);background:var(--warn-soft)}
.leaf.next{border-color:var(--blue);box-shadow:0 0 0 3px var(--blue-soft)}
.leaf.next .ck{border-color:var(--blue);animation:mappulse 1.8s infinite}
@keyframes mappulse{0%{box-shadow:0 0 0 0 color-mix(in srgb,var(--blue) 55%,transparent)}70%{box-shadow:0 0 0 7px transparent}100%{box-shadow:0 0 0 0 transparent}}
@media (prefers-reduced-motion:reduce){.leaf.next .ck{animation:none}}
.leaf .here{flex:none;font-size:.66rem;font-weight:700;color:#fff;background:var(--blue);border-radius:99px;padding:1px 7px}
.leaf.proj .li::before{content:"\2605 ";color:var(--warn)}
.map-end{position:relative;z-index:1;margin:6px auto 0;width:max-content;max-width:100%;text-align:center;font-size:.85rem;color:var(--muted);background:var(--surface);padding:8px 14px;border:1.5px solid var(--line);border-radius:999px}
.map-end.won{background:var(--m-done);color:#fff;border-color:var(--m-done)}
@media (max-width:860px){.map-hero{grid-template-columns:1fr}}
@media (max-width:720px){
  .mh-main{flex-direction:column;align-items:flex-start;gap:14px}
  .mh-ring{width:112px;height:112px}
  .map-strip button span{display:none}
  .mrow{grid-template-columns:1fr;column-gap:0;row-gap:7px;margin-bottom:24px;padding-left:30px}
  .mnode{grid-column:1;order:-1}
  .mside.l,.mside.r{grid-column:1;grid-row:auto;align-items:stretch;padding-left:26px}
  .leaf{width:100%;border-radius:12px}
}
/* MAP:END */
"""

JS = r"""/* MAP:BEGIN */
function mapRing(pct,size,stroke,inner){
  var r=(size-stroke)/2,c=2*Math.PI*r;
  return "<svg viewBox=\"0 0 "+size+" "+size+"\" aria-hidden=\"true\"><circle class=\"bg\" cx=\""+size/2+"\" cy=\""+size/2+"\" r=\""+r+"\" fill=\"none\" stroke-width=\""+stroke+"\"/>"+
    "<circle class=\"fg\" cx=\""+size/2+"\" cy=\""+size/2+"\" r=\""+r+"\" fill=\"none\" stroke-width=\""+stroke+"\" stroke-linecap=\"round\" stroke-dasharray=\""+c.toFixed(1)+"\" stroke-dashoffset=\""+(c*(1-pct/100)).toFixed(1)+"\"/></svg>"+(inner||"");
}
function mapLeaf(i,next){
  var done=!!S.done[i.id],rv=S.rev[i.id],due=done&&!!(rv&&rv.due<=today());
  var exs=i.ex||[],exd=exs.filter(function(e){return S.ex[e.id];}).length;
  var cls="leaf"+(done?" done":"")+(due?" rev":"")+(next?" next":"")+(i.kind==="project"?" proj":"");
  var tip=i.id+" "+i.t+(done?" (complete"+(due?", review due":"")+")":next?" (next up)":"")+(exs.length?". Exercises "+exd+" of "+exs.length:"");
  return "<button type=\"button\" class=\""+cls+"\" data-act=\"open\" data-id=\""+esc(i.id)+"\" data-st=\""+(done?"done":next?"next":"")+"\" title=\""+esc(tip)+"\" aria-label=\""+esc(tip)+"\">"+
    "<span class=\"ck\" aria-hidden=\"true\">"+(due?"↻":done?"✓":"")+"</span><span class=\"li\">"+esc(i.id)+"</span><span class=\"lt\">"+esc(i.t)+"</span>"+
    (exs.length?"<span class=\"lx\" aria-hidden=\"true\">"+exs.map(function(e){return "<i"+(S.ex[e.id]?" class=\"on\"":"")+"></i>";}).join("")+"</span>":"")+
    (next?"<span class=\"here\">Next</span>":"")+"</button>";
}
function viewMap(){
  var tr=S.mapTrack||S.track||"F",mods=M.filter(function(m){return m.track===tr;});
  var nx=nextItem(),all=[],done=0,exT=0,exD=0,modsDone=0,due=0,t=today();
  mods.forEach(function(m){
    var md=0;
    m.items.forEach(function(i){all.push(i);if(S.done[i.id]){done++;md++;if(S.rev[i.id]&&S.rev[i.id].due<=t)due++;}(i.ex||[]).forEach(function(e){exT++;if(S.ex[e.id])exD++;});});
    if(md===m.items.length&&md)modsDone++;
  });
  var pct=all.length?Math.round(done/all.length*100):0;
  var trackNext=all.find(function(i){return !S.done[i.id];});
  var trk=["F","A","P"].filter(function(k){return M.some(function(m){return m.track===k;});}).map(function(k){
    var its=[];M.forEach(function(m){if(m.track===k)its=its.concat(m.items);});
    var d=its.filter(function(i){return S.done[i.id];}).length;
    return "<button type=\"button\" data-act=\"maptrack\" data-v=\""+k+"\" aria-pressed=\""+(tr===k)+"\">"+esc(trackName(k))+"<i style=\"--w:"+(its.length?Math.round(d/its.length*100):0)+"%\"></i></button>";
  }).join("");
  var stat=function(n,label,p,col){return "<div class=\"mh-stat\"><b>"+n+"</b><span>"+label+"</span>"+(p!=null?"<span class=\"sbar\"><i style=\"width:"+p+"%"+(col?";--sc:"+col:"")+"\"></i></span>":"")+"</div>";};
  var h="<div class=\"mapv\"><div class=\"map-hero\">"+
    "<div class=\"mh-card mh-main\"><div class=\"mh-ring\" role=\"img\" aria-label=\""+pct+" percent of this track complete\">"+mapRing(pct,132,12,"<div class=\"pc\"><b>"+pct+"%</b><span>complete</span></div>")+"</div>"+
    "<div class=\"mh-txt\"><h1>Your map</h1><p>Every module and lesson in one tree. Click a box to open it in the curriculum; the map fills in as you go.</p><div class=\"map-tracks\" role=\"group\" aria-label=\"Track\">"+trk+"</div></div></div>"+
    "<div class=\"mh-card mh-stats\">"+
      stat(done+"<small style=\"font-size:.55em;color:var(--muted)\"> / "+all.length+"</small>","lessons complete",pct)+
      stat(exD+"<small style=\"font-size:.55em;color:var(--muted)\"> / "+exT+"</small>","exercises done",exT?Math.round(exD/exT*100):0,"var(--blue)")+
      stat(modsDone+"<small style=\"font-size:.55em;color:var(--muted)\"> / "+mods.length+"</small>","modules complete",mods.length?Math.round(modsDone/mods.length*100):0,"var(--yellow)")+
      stat(due,due===1?"review due today":"reviews due today",null)+
      (trackNext?"<button type=\"button\" class=\"mh-next\" data-act=\"open\" data-id=\""+esc(trackNext.id)+"\"><div><span class=\"lbl\">Next up</span><b>"+esc(trackNext.id+" "+trackNext.t)+"</b></div><span class=\"go\" aria-hidden=\"true\">→</span></button>":"")+
    "</div></div>"+
    "<div class=\"map-strip\" role=\"group\" aria-label=\"Jump to a module\">"+mods.map(function(m){
      var n=m.items.length,d=m.items.filter(function(i){return S.done[i.id];}).length;
      var cur=trackNext&&m.items.indexOf(trackNext)>=0;
      return "<button type=\"button\" data-act=\"mapjump\" data-v=\""+m.id+"\" class=\""+(cur?"cur":"")+"\" style=\"--p:"+(n?Math.round(d/n*100):0)+"%\" title=\""+esc(m.n+" "+m.t+": "+d+" of "+n)+"\"><span>"+esc(m.n)+"</span></button>";
    }).join("")+"</div>"+
    "<div class=\"map-legend\"><span><i class=\"l-mod\"></i>Module</span><span><i></i>Not started</span><span><i class=\"l-next\"></i>Next lesson</span><span><i class=\"l-done\"></i>Complete</span><span><i class=\"l-rev\"></i>Review due</span><span><i style=\"border-radius:3px;width:16px;height:6px;border:0;background:var(--m-done)\"></i>Exercises</span></div>"+
    "<div class=\"maptree\"><svg class=\"maplines\" aria-hidden=\"true\"></svg>";
  mods.forEach(function(m){
    var n=m.items.length,d=m.items.filter(function(i){return S.done[i.id];}).length,p=n?Math.round(d/n*100):0;
    var first=m.items.find(function(i){return !S.done[i.id];})||m.items[0];
    var cur=trackNext&&m.items.indexOf(trackNext)>=0;
    var half=Math.ceil(n/2),L=m.items.slice(0,half),R=m.items.slice(half);
    var side=function(list,c){return list.length?"<div class=\"mside "+c+"\">"+list.map(function(i){return mapLeaf(i,nx&&nx.id===i.id);}).join("")+"</div>":"";};
    var st=d===n&&n?"done":d?"part":"todo";
    h+="<div class=\"mrow\" id=\"map-"+m.id+"\" data-st=\""+st+"\">"+side(L,"l")+
      "<button type=\"button\" class=\"mnode "+st+(cur?" cur":"")+"\" style=\"--p:"+p+"%\" data-act=\"open\" data-id=\""+esc(first.id)+"\" title=\""+esc(m.n+" "+m.t+": "+d+" of "+n+" lessons complete")+"\">"+
      "<span class=\"mring\">"+mapRing(p,46,5,"<b>"+esc(m.n)+"</b>")+"</span><span class=\"mtx\"><span class=\"mt\">"+esc(m.t)+"</span><span class=\"mc\">"+(st==="done"?"✓ Complete":d+" of "+n+" lessons · "+p+"%")+"</span></span></button>"+side(R,"r")+"</div>";
  });
  h+="<div class=\"map-end"+(done===all.length&&all.length?" won":"")+"\">"+(done===all.length&&all.length?"★ Track complete. Well done.":"⚑ Finish line: "+(all.length-done)+" lessons to go")+"</div></div></div>";
  return h;
}
function mapDraw(){
  var tree=document.querySelector(".maptree"),svg=tree&&tree.querySelector(".maplines");if(!svg)return;
  var box=tree.getBoundingClientRect(),W=box.width,H=tree.scrollHeight;
  svg.setAttribute("viewBox","0 0 "+W+" "+H);svg.setAttribute("width",W);svg.setAttribute("height",H);
  var rel=function(el){var r=el.getBoundingClientRect();return {l:r.left-box.left,r:r.right-box.left,t:r.top-box.top,b:r.bottom-box.top,cx:(r.left+r.right)/2-box.left,cy:(r.top+r.bottom)/2-box.top};};
  var rows=[].slice.call(tree.querySelectorAll(".mrow")),narrow=W<700,out=[],spineX=null,firstY=null,lastY=null,doneY=null;
  rows.forEach(function(row){
    var node=row.querySelector(".mnode");if(!node)return;
    var n=rel(node);
    var sx=narrow?n.l-16:n.cx;
    if(spineX===null)spineX=sx;
    if(firstY===null)firstY=n.cy;lastY=n.cy;
    if(node.classList.contains("cur"))doneY=n.cy;
    row.querySelectorAll(".leaf").forEach(function(leaf){
      var f=rel(leaf),cls="br"+(leaf.dataset.st?" "+leaf.dataset.st:""),d;
      if(narrow){var x0=n.l+22,y0=n.b;d="M"+x0+" "+y0+" V"+(f.cy-10)+" Q"+x0+" "+f.cy+" "+(x0+10)+" "+f.cy+" H"+f.l;}
      else if(f.r<=n.l){var x1=n.l,y1=n.cy,x2=f.r,y2=f.cy,k=(x1-x2)*0.55;d="M"+x1+" "+y1+" C"+(x1-k)+" "+y1+" "+(x2+k)+" "+y2+" "+x2+" "+y2;}
      else{var a=n.r,b=n.cy,c=f.l,e=f.cy,q=(c-a)*0.55;d="M"+a+" "+b+" C"+(a+q)+" "+b+" "+(c-q)+" "+e+" "+c+" "+e;}
      out.push("<path class=\""+cls+"\" d=\""+d+"\"/>");
    });
  });
  if(spineX===null){svg.innerHTML="";return;}
  var end=tree.querySelector(".map-end"),endY=end?rel(end).cy:lastY;
  if(doneY===null&&rows.length&&rows.every(function(r){return r.dataset.st==="done";}))doneY=endY;
  var gy1=Math.max(0,firstY-30),gy2=Math.max(gy1+1,doneY||gy1+1);
  var defs="<defs><linearGradient id=\"mapgrad\" gradientUnits=\"userSpaceOnUse\" x1=\""+spineX+"\" y1=\""+gy1+"\" x2=\""+spineX+"\" y2=\""+gy2+"\"><stop offset=\"0\" style=\"stop-color:var(--good)\"/><stop offset=\"1\" style=\"stop-color:var(--blue)\"/></linearGradient></defs>";
  var spine="<path class=\"spine\" d=\"M"+spineX+" "+Math.max(0,firstY-30)+" V"+endY+"\"/>"+(doneY!==null?"<path class=\"spine-done\" d=\"M"+spineX+" "+Math.max(0,firstY-30)+" V"+doneY+"\"/>":"");
  svg.innerHTML=defs+spine+out.join("");
}
var mapResizeT=0;
window.addEventListener("resize",function(){clearTimeout(mapResizeT);mapResizeT=setTimeout(function(){if(currentView()==="map")mapDraw();},120);});
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){if(currentView()==="map")mapDraw();});
document.addEventListener("click",function(ev){
  var b=ev.target.closest&&ev.target.closest("[data-act=\"maptrack\"],[data-act=\"mapjump\"]");if(!b)return;
  if(b.dataset.act==="maptrack"){S.mapTrack=b.dataset.v;save();render();window.scrollTo({top:0});return;}
  var row=document.getElementById("map-"+b.dataset.v);if(row)row.scrollIntoView({behavior:"smooth",block:"center"});
});
/* MAP:END */
"""


def main(path):
    s = open(path, encoding="utf-8").read()
    while "/* MAP:BEGIN */" in s:
        a = s.index("/* MAP:BEGIN */")
        b = s.index("/* MAP:END */", a) + len("/* MAP:END */\n")
        s = s[:a] + s[b:]
    s = s.replace('      <a href="#map" data-tab="map">Map</a>\n', "")
    s = s.replace('if(v==="map")requestAnimationFrame(mapDraw);', "")

    def rep(a, b):
        nonlocal s
        if b in s:
            return
        assert s.count(a) == 1, (a[:70], s.count(a))
        s = s.replace(a, b)

    i = s.index("</style>")
    s = s[:i] + CSS + s[i:]
    rep('      <a href="#control" data-tab="control">Overview</a>\n',
        '      <a href="#map" data-tab="map">Map</a>\n      <a href="#control" data-tab="control">Overview</a>\n')
    rep('return h==="curriculum"||h==="grades"?h:"control";}', 'return h==="curriculum"||h==="grades"||h==="map"?h:"control";}')
    rep('el.innerHTML=v==="curriculum"?viewCurriculum():v==="grades"?viewGrades():viewControl();',
        'el.innerHTML=v==="curriculum"?viewCurriculum():v==="grades"?viewGrades():v==="map"?viewMap():viewControl();')
    a = s.index("function render(){")
    b = s.index("function go(view)", a)
    body = s[a:b]
    assert body.count("highlight(el);") == 1
    s = s[:a] + body.replace("highlight(el);", 'highlight(el);if(v==="map")requestAnimationFrame(mapDraw);') + s[b:]
    j = s.index("function render(){")
    s = s[:j] + JS + s[j:]
    open(path, "w", encoding="utf-8").write(s)
    print("map added to", path)


if __name__ == "__main__":
    main(sys.argv[1])
