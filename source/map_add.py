"""Add a Map tab to the course engine, styled as a graphic-syllabus poster: a flat light-blue
page with navy section tabs, icon tiles, a module donut, ringed module badges and a vertical
roadmap timeline. Every lesson box links to its lesson, and the whole poster reflects progress.

The roadmap's connectors are drawn as an SVG overlay after layout, so they follow the boxes
at any width. The tab sits first, before Overview.

usage: python3 map_add.py course.html   (idempotent)
"""
import sys

FONT = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;600;700;800&display=swap" data-map-font>'

CSS = r"""/* MAP:BEGIN */
.pz{--pz-bg:#C9E4FA;--pz-navy:#0B5C91;--pz-deep:#0A2A43;--pz-yel:#FFD60A;--pz-org:#D2602F;--pz-sky:#11ABEC;--pz-mid:#2E7CB8;
  --pz-ink:#0A2A43;--pz-sub:#3D5A73;--pz-card:#FFFFFF;--pz-pale:#E7F2FC;--pz-line:#0B5C91;
  font-family:'Raleway',var(--font-display),system-ui,sans-serif;color:var(--pz-ink);background:var(--pz-bg);
  max-width:1120px;margin:0 auto 12px;border-radius:6px;padding:34px clamp(16px,4vw,48px) 40px;position:relative;overflow:hidden}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .pz{--pz-bg:#0C2338;--pz-navy:#2F86C6;--pz-deep:#E3F0FB;--pz-mid:#5AA3DC;--pz-ink:#E3F0FB;--pz-sub:#A9C3D8;--pz-card:#13324D;--pz-pale:#183A57;--pz-line:#5AA3DC}}
:root[data-theme="dark"] .pz{--pz-bg:#0C2338;--pz-navy:#2F86C6;--pz-deep:#E3F0FB;--pz-mid:#5AA3DC;--pz-ink:#E3F0FB;--pz-sub:#A9C3D8;--pz-card:#13324D;--pz-pale:#183A57;--pz-line:#5AA3DC}
.pz *{box-sizing:border-box}
.pz button{font:inherit;color:inherit}
.pz .sc{font-variant:small-caps;letter-spacing:.02em}
/* header */
.pz-head{display:grid;grid-template-columns:minmax(0,auto) minmax(0,1fr);gap:20px 34px;align-items:start;margin-bottom:26px}
.pz-title{display:inline-block;background:var(--pz-navy);color:#fff;font-weight:800;font-size:clamp(1.9rem,4.6vw,3.3rem);line-height:1;padding:10px 16px 8px;letter-spacing:-.01em;text-transform:uppercase}
.pz-sub{font-variant:small-caps;font-size:clamp(1.1rem,2.2vw,1.55rem);color:var(--pz-navy);margin:8px 0 0 16px;font-weight:600}
.pz-facts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 18px}
.pz-fact{display:flex;align-items:center;gap:10px;min-width:0;font-size:1.02rem}
.pz-ico{flex:none;width:44px;height:44px;background:var(--pz-navy);color:#fff;display:grid;place-items:center}
.pz-ico svg{width:22px;height:22px}
.pz-fact b{font-weight:800;font-size:1.35rem}
.pz-fact div span{color:var(--pz-sub)}
.pz-tracks{display:flex;flex-wrap:wrap;align-items:center;gap:6px 0;margin:0 0 30px;font-size:1.05rem}
.pz-tracks .pz-ico{margin-right:12px}
.pz-tracks button{background:none;border:0;padding:4px 14px;cursor:pointer;border-right:1.5px solid var(--pz-sub);line-height:1.2}
.pz-tracks button:last-child{border-right:0}
.pz-tracks button[aria-pressed="true"]{font-weight:800;text-decoration:underline;text-decoration-color:var(--pz-yel);text-decoration-thickness:4px;text-underline-offset:5px}
.pz-tracks button small{color:var(--pz-sub);font-weight:600}
/* section tabs */
.pz-sec{margin:0 0 30px}
.pz-tab{display:flex;align-items:flex-end;margin:0 0 16px}
.pz-tab b{background:var(--pz-navy);color:#fff;font-weight:800;text-transform:uppercase;font-size:.98rem;letter-spacing:.02em;padding:6px 14px}
.pz-tab::after{content:"";flex:1;border-bottom:1.5px solid var(--pz-line);opacity:.8}
.pz-grid2{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:10px 40px;align-items:start}
/* you are here */
.pz-here{display:flex;gap:22px;align-items:center}
.pz-ring{flex:none;width:170px;height:170px;border-radius:50%;background:var(--pz-yel);display:grid;place-items:center;padding:13px}
.pz-ring>div{width:100%;height:100%;border-radius:50%;background:var(--pz-navy);border:6px solid #fff;display:grid;place-content:center;text-align:center;color:#fff;font-weight:800;font-variant:small-caps;font-size:1.45rem;line-height:1.05}
.pz-ring small{display:block;font-size:.8rem;font-weight:600;font-variant:normal;opacity:.85;margin-top:6px}
.pz-here h3{margin:0 0 2px;font-variant:small-caps;font-weight:800;font-size:1.05rem;letter-spacing:.03em}
.pz-here p{margin:0 0 12px;line-height:1.4}
.pz-btn{display:inline-flex;align-items:center;gap:8px;background:var(--pz-navy);color:#fff!important;border:0;padding:9px 14px;font-weight:700;cursor:pointer}
.pz-btn:hover{filter:brightness(1.1)}
/* donut */
.pz-donut-wrap{display:flex;gap:18px;align-items:center;flex-wrap:wrap}
.pz-donut{flex:none;position:relative;width:210px;height:210px}
.pz-donut svg{width:100%;height:100%;transform:rotate(-90deg)}
.pz-donut path{cursor:pointer}
.pz-donut path:hover{opacity:.8}
.pz-donut .mid{position:absolute;inset:0;display:grid;place-content:center;text-align:center;pointer-events:none}
.pz-donut .mid b{font-size:2.3rem;font-weight:800;line-height:1}
.pz-donut .mid span{font-variant:small-caps;color:var(--pz-sub);font-weight:600}
.pz-keys{display:grid;gap:8px;min-width:0}
.pz-key{display:flex;align-items:center;gap:0}
.pz-key i{flex:none;width:36px;height:36px;display:grid;place-items:center;background:var(--pz-navy);color:#fff}
.pz-key i svg{width:18px;height:18px}
.pz-key span{background:var(--pz-card);padding:6px 10px;font-size:.95rem;white-space:nowrap}
.pz-key em{display:inline-block;width:12px;height:12px;margin-right:6px;vertical-align:-1px;font-style:normal}
/* module badges */
.pz-badges{display:grid;grid-template-columns:repeat(auto-fill,minmax(112px,1fr));gap:18px 10px}
.pz-badge{background:none;border:0;padding:0;cursor:pointer;text-align:center;display:grid;justify-items:center;gap:6px}
.pz-badge .rg{width:104px;height:104px;border-radius:50%;padding:9px;background:conic-gradient(var(--c) var(--p),color-mix(in srgb,var(--c) 38%,var(--pz-card)) 0)}
.pz-badge .rg>span{width:100%;height:100%;border-radius:50%;background:var(--pz-navy);border:5px solid var(--pz-bg);display:grid;place-content:center;color:#fff;line-height:1.05}
.pz-badge .rg b{font-weight:800;font-size:1.3rem}
.pz-badge .rg small{font-size:.72rem;opacity:.85}
.pz-badge.done .rg>span{background:var(--pz-deep);color:var(--pz-bg)}
.pz-badge .cap{font-size:.78rem;font-weight:700;line-height:1.2;max-width:110px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.pz-badge:hover .rg{transform:scale(1.04)}
.pz-badge.cur .rg{box-shadow:0 0 0 4px var(--pz-bg),0 0 0 7px var(--pz-org)}
/* roadmap timeline */
.pz-legend{display:flex;flex-wrap:wrap;gap:6px 22px;margin:-4px 0 18px;font-size:.92rem}
.pz-legend span{display:grid;gap:4px}
.pz-legend i{display:block;width:84px;height:7px}
.pz-road{position:relative;padding:0 0 6px}
.pz-lines{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible}
.pz-lines .sp{stroke:var(--pz-deep);stroke-width:9;fill:none}
.pz-lines .br{fill:none;stroke:var(--pz-navy);stroke-width:2.5;opacity:.55}
.pz-lines .br.done{opacity:1}
.pz-lines .br.next{stroke:var(--pz-org);opacity:1;stroke-width:3}
.pz-cap{position:relative;z-index:1;margin:0 auto 26px;width:118px;height:118px;border-radius:50%;background:var(--pz-card);border:11px solid var(--pz-deep);display:grid;place-content:center;text-align:center;line-height:1}
.pz-cap b{font-size:1.75rem;font-weight:800}
.pz-cap small{font-variant:small-caps;font-weight:700;color:var(--pz-sub);margin-top:3px}
.pz-cap.end{width:84px;height:84px;border-width:9px;margin:4px auto 0}
.pz-cap.end b{font-size:1rem}
.pz-row{position:relative;display:grid;grid-template-columns:1fr minmax(200px,250px) 1fr;column-gap:48px;align-items:center;margin:0 0 30px}
.pz .pz-node{position:relative;z-index:1;grid-column:2;display:flex;align-items:center;gap:10px;background:var(--pz-navy);color:#fff;border:0;padding:8px 12px 8px 8px;cursor:pointer;text-align:left;width:100%}
.pz-node:hover{filter:brightness(1.08)}
.pz-node .dot{flex:none;width:40px;height:40px;border-radius:50%;background:var(--pz-card);color:var(--pz-ink);display:grid;place-items:center;font-weight:800;font-size:.85rem;border:4px solid var(--c)}
.pz-node .nt{display:block;font-weight:800;line-height:1.15}
.pz-node .nc{display:block;font-size:.76rem;opacity:.85;margin-top:2px}
.pz-node .nb{display:block;height:4px;margin-top:6px;background:rgba(255,255,255,.25)}
.pz-node .nb i{display:block;height:100%;background:var(--pz-yel)}
.pz .pz-node.done{background:var(--pz-deep);color:var(--pz-bg)}
.pz-node.done .nb i{background:var(--pz-sky)}
.pz-node.cur{outline:4px solid var(--pz-org);outline-offset:2px}
.pz-side{display:flex;flex-direction:column;gap:8px;min-width:0}
.pz-side.l{grid-column:1;grid-row:1;align-items:flex-end}
.pz-side.r{grid-column:3;grid-row:1;align-items:flex-start}
.pz-leaf{position:relative;z-index:1;display:inline-flex;align-items:stretch;max-width:100%;background:none;border:0;padding:0;cursor:pointer;text-align:left}
.pz-leaf .mk{flex:none;width:9px;background:var(--pz-card);outline:1.5px solid var(--pz-navy);outline-offset:-1.5px}
.pz-leaf .bx{display:flex;align-items:center;gap:8px;min-width:0;background:var(--pz-card);padding:6px 11px;font-size:.93rem;line-height:1.25}
.pz-leaf .id{flex:none;color:var(--pz-sub);font-weight:600;font-size:.84rem}
.pz-leaf .tt{min-width:0}
.pz-leaf .ex{flex:none;display:inline-flex;gap:2px}
.pz-leaf .ex i{width:6px;height:6px;border-radius:50%;background:color-mix(in srgb,var(--pz-navy) 25%,transparent)}
.pz-leaf .ex i.on{background:var(--pz-navy)}
.pz-leaf .tag{flex:none;font-size:.7rem;font-weight:800;color:#fff;background:var(--pz-org);padding:1px 7px;text-transform:uppercase;letter-spacing:.04em}
.pz-leaf.done .mk{background:var(--pz-navy)}
.pz-leaf.done .tt{font-weight:700}
.pz-leaf.next .mk{background:var(--pz-org);outline-color:var(--pz-org)}
.pz-leaf.next .bx{box-shadow:inset 0 0 0 2px var(--pz-org)}
.pz-leaf.rev .mk{background:var(--pz-yel);outline-color:#B89400}
.pz-leaf.proj .id::before{content:"\2605 ";color:var(--pz-org)}
.pz-leaf:hover .bx{background:var(--pz-pale)}
.pz-side.l .pz-leaf{flex-direction:row-reverse}
@media (max-width:860px){.pz-head{grid-template-columns:1fr}.pz-grid2{grid-template-columns:1fr}}
@media (max-width:720px){
  .pz{padding-top:24px}
  .pz-facts{grid-template-columns:1fr 1fr}
  .pz-fact b{font-size:1.1rem}
  .pz-here{flex-direction:column;align-items:flex-start}
  .pz-ring{width:140px;height:140px}
  .pz-row{grid-template-columns:1fr;column-gap:0;row-gap:8px;padding-left:34px;margin-bottom:24px}
  .pz-node{grid-column:1;order:-1}
  .pz-side.l,.pz-side.r{grid-column:1;grid-row:auto;align-items:stretch;padding-left:22px}
  .pz-side.l .pz-leaf{flex-direction:row}
  .pz-leaf{width:100%}.pz-leaf .bx{flex:1}
  .pz-cap{margin-left:0}
  .pz-cap.end{margin-left:6px}
}
@media (max-width:460px){.pz-facts{grid-template-columns:1fr}.pz-tracks button{padding:4px 9px}}
@media (prefers-reduced-motion:no-preference){.pz-row{animation:pzin .45s both}@keyframes pzin{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}}
/* MAP:END */
"""

JS = r"""/* MAP:BEGIN */
var PZ_ICON={
  book:"<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linejoin=\"round\"><path d=\"M3 5c3-1 6-1 9 1 3-2 6-2 9-1v14c-3-1-6-1-9 1-3-2-6-2-9-1z\"/><path d=\"M12 6v14\"/></svg>",
  pen:"<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M4 20l4-1 11-11-3-3L5 16z\"/><path d=\"M14 6l3 3\"/></svg>",
  layers:"<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linejoin=\"round\"><path d=\"M12 3l9 5-9 5-9-5z\"/><path d=\"M3 13l9 5 9-5\"/></svg>",
  redo:"<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M20 12a8 8 0 1 1-2.3-5.7\"/><path d=\"M20 4v5h-5\"/></svg>",
  route:"<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"6\" cy=\"19\" r=\"2\"/><circle cx=\"18\" cy=\"5\" r=\"2\"/><path d=\"M8 19h7a3.5 3.5 0 0 0 0-7H9a3.5 3.5 0 0 1 0-7h7\"/></svg>",
  check:"<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M5 12l5 5 9-10\"/></svg>",
  half:"<svg viewBox=\"0 0 24 24\"><circle cx=\"12\" cy=\"12\" r=\"8\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.5\"/><path d=\"M12 4a8 8 0 0 1 0 16z\" fill=\"currentColor\"/></svg>",
  ring:"<svg viewBox=\"0 0 24 24\"><circle cx=\"12\" cy=\"12\" r=\"8\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.5\"/></svg>"
};
var PZ_RINGS=["var(--pz-org)","var(--pz-mid)","var(--pz-yel)","var(--pz-navy)","var(--pz-sky)"];
function pzStats(mods){
  var r={all:[],done:0,exT:0,exD:0,modsDone:0,due:0},t=today();
  mods.forEach(function(m){var md=0;m.items.forEach(function(i){r.all.push(i);if(S.done[i.id]){r.done++;md++;if(S.rev[i.id]&&S.rev[i.id].due<=t)r.due++;}(i.ex||[]).forEach(function(e){r.exT++;if(S.ex[e.id])r.exD++;});});if(md===m.items.length&&md)r.modsDone++;});
  return r;
}
function pzLeaf(i,next){
  var done=!!S.done[i.id],rv=S.rev[i.id],due=done&&!!(rv&&rv.due<=today());
  var exs=i.ex||[],exd=exs.filter(function(e){return S.ex[e.id];}).length;
  var cls="pz-leaf"+(done?" done":"")+(due?" rev":"")+(next?" next":"")+(i.kind==="project"?" proj":"");
  var tip=i.id+" "+i.t+(done?" (complete"+(due?", review due":"")+")":next?" (next up)":"")+(exs.length?". Exercises "+exd+" of "+exs.length:"");
  return "<button type=\"button\" class=\""+cls+"\" data-act=\"open\" data-id=\""+esc(i.id)+"\" data-st=\""+(done?"done":next?"next":"")+"\" title=\""+esc(tip)+"\" aria-label=\""+esc(tip)+"\">"+
    "<span class=\"mk\" aria-hidden=\"true\"></span><span class=\"bx\"><span class=\"id\">"+esc(i.id)+"</span><span class=\"tt\">"+esc(i.t)+"</span>"+
    (exs.length?"<span class=\"ex\" aria-hidden=\"true\">"+exs.map(function(e){return "<i"+(S.ex[e.id]?" class=\"on\"":"")+"></i>";}).join("")+"</span>":"")+
    (next?"<span class=\"tag\">Next</span>":"")+"</span></button>";
}
function pzDonut(mods){
  var total=0;mods.forEach(function(m){total+=m.items.length;});
  if(!total)return "";
  var R=100,r=62,cx=105,cy=105,a=0,out="",gap=mods.length>12?0.006:0.012;
  var pt=function(rad,ang){return (cx+rad*Math.cos(ang*2*Math.PI)).toFixed(2)+" "+(cy+rad*Math.sin(ang*2*Math.PI)).toFixed(2);};
  mods.forEach(function(m,k){
    var n=m.items.length,d=m.items.filter(function(i){return S.done[i.id];}).length,f=n/total,a0=a+gap/2,a1=a+f-gap/2;a+=f;
    if(a1<=a0)return;
    var col=d===n?"var(--pz-deep)":d?"var(--pz-sky)":"var(--pz-card)";
    var big=(a1-a0)>0.5?1:0;
    out+="<path d=\"M"+pt(R,a0)+" A"+R+" "+R+" 0 "+big+" 1 "+pt(R,a1)+" L"+pt(r,a1)+" A"+r+" "+r+" 0 "+big+" 0 "+pt(r,a0)+"Z\" fill=\""+col+"\" data-act=\"mapjump\" data-v=\""+m.id+"\"><title>"+esc(m.n+" "+m.t+": "+d+" of "+n)+"</title></path>";
  });
  return "<svg viewBox=\"0 0 210 210\" role=\"img\" aria-label=\"Modules by completion\">"+out+"</svg>";
}
function viewMap(){
  var tr=S.mapTrack||S.track||"F",mods=M.filter(function(m){return m.track===tr;});
  var st=pzStats(mods),pct=st.all.length?Math.round(st.done/st.all.length*100):0;
  var nx=nextItem(),trackNext=st.all.find(function(i){return !S.done[i.id];});
  var name=(document.querySelector(".bname")||{}).textContent||"Course";
  var started=mods.filter(function(m){var d=m.items.filter(function(i){return S.done[i.id];}).length;return d&&d<m.items.length;}).length;
  var fact=function(ic,b,s){return "<div class=\"pz-fact\"><span class=\"pz-ico\" aria-hidden=\"true\">"+PZ_ICON[ic]+"</span><div><b>"+b+"</b> <span>"+s+"</span></div></div>";};
  var tracks=["F","A","P"].filter(function(k){return M.some(function(m){return m.track===k;});}).map(function(k){
    var its=[];M.forEach(function(m){if(m.track===k)its=its.concat(m.items);});
    var d=its.filter(function(i){return S.done[i.id];}).length;
    return "<button type=\"button\" data-act=\"maptrack\" data-v=\""+k+"\" aria-pressed=\""+(tr===k)+"\">"+esc(trackName(k).replace(/^Track \d+ · /,""))+" <small>"+(its.length?Math.round(d/its.length*100):0)+"%</small></button>";
  }).join("");
  var h="<div class=\"pz\">"+
    "<div class=\"pz-head\"><div><div class=\"pz-title\">"+esc(name)+"</div><div class=\"pz-sub\">"+esc(trackName(tr))+"</div></div>"+
    "<div class=\"pz-facts\">"+fact("book",st.done+"/"+st.all.length,"lessons complete")+fact("pen",st.exD+"/"+st.exT,"exercises done")+fact("layers",st.modsDone+"/"+mods.length,"modules complete")+fact("redo",st.due,st.due===1?"review due today":"reviews due today")+"</div></div>"+
    "<div class=\"pz-tracks\" role=\"group\" aria-label=\"Track\"><span class=\"pz-ico\" aria-hidden=\"true\">"+PZ_ICON.route+"</span><b style=\"margin-right:4px\">Tracks:</b>"+tracks+"</div>"+
    "<div class=\"pz-grid2\"><section class=\"pz-sec\"><div class=\"pz-tab\"><b>You are here</b></div><div class=\"pz-here\">"+
      "<div class=\"pz-ring\"><div>"+(trackNext?esc(trackNext.id)+"<small>next lesson</small>":"Done!<small>track complete</small>")+"</div></div>"+
      "<div>"+(trackNext?"<h3>Up next</h3><p>"+esc(trackNext.t)+"</p><button type=\"button\" class=\"pz-btn\" data-act=\"open\" data-id=\""+esc(trackNext.id)+"\">Open the lesson →</button>":"<h3>Track complete</h3><p>Every lesson in this track is done. Pick another track above.</p>")+
      "<h3 style=\"margin-top:16px\">Reviews</h3><p>"+(st.due?st.due+" lesson"+(st.due>1?"s":"")+" due for review today: they're marked yellow below.":"Nothing due today. Finished lessons come back for review on a schedule.")+"</p></div>"+
    "</div></section>"+
    "<section class=\"pz-sec\"><div class=\"pz-tab\"><b>Progress</b></div><div class=\"pz-donut-wrap\"><div class=\"pz-donut\">"+pzDonut(mods)+"<div class=\"mid\"><b>"+pct+"%</b><span>complete</span></div></div>"+
      "<div class=\"pz-keys\"><div class=\"pz-key\"><i aria-hidden=\"true\">"+PZ_ICON.check+"</i><span><em style=\"background:var(--pz-deep)\"></em>"+st.modsDone+(st.modsDone===1?" module":" modules")+" complete</span></div>"+
      "<div class=\"pz-key\"><i aria-hidden=\"true\">"+PZ_ICON.half+"</i><span><em style=\"background:var(--pz-sky)\"></em>"+started+" in progress</span></div>"+
      "<div class=\"pz-key\"><i aria-hidden=\"true\">"+PZ_ICON.ring+"</i><span><em style=\"background:var(--pz-card);outline:1px solid var(--pz-sub)\"></em>"+(mods.length-st.modsDone-started)+" not started</span></div></div></div></section></div>"+
    "<section class=\"pz-sec\"><div class=\"pz-tab\"><b>Modules</b></div><div class=\"pz-badges\">"+mods.map(function(m,k){
      var n=m.items.length,d=m.items.filter(function(i){return S.done[i.id];}).length,p=n?Math.round(d/n*100):0;
      var cur=trackNext&&m.items.indexOf(trackNext)>=0;
      return "<button type=\"button\" class=\"pz-badge"+(d===n&&n?" done":"")+(cur?" cur":"")+"\" data-act=\"mapjump\" data-v=\""+m.id+"\" style=\"--c:"+PZ_RINGS[k%PZ_RINGS.length]+";--p:"+p+"%\" title=\""+esc(m.n+" "+m.t+": "+d+" of "+n+" lessons")+"\"><span class=\"rg\"><span><b>"+esc(m.n)+"</b><small>"+d+"/"+n+"</small></span></span><span class=\"cap\">"+esc(m.t)+"</span></button>";
    }).join("")+"</div></section>"+
    "<section class=\"pz-sec\" style=\"margin-bottom:0\"><div class=\"pz-tab\"><b>Roadmap</b></div>"+
    "<div class=\"pz-legend\"><span><i style=\"background:var(--pz-navy)\"></i>Complete</span><span><i style=\"background:var(--pz-org)\"></i>Next lesson</span><span><i style=\"background:var(--pz-yel)\"></i>Review due</span><span><i style=\"background:var(--pz-card)\"></i>Not started</span></div>"+
    "<div class=\"pz-road\"><svg class=\"pz-lines\" aria-hidden=\"true\"></svg><div class=\"pz-cap\"><b>"+pct+"%</b><small>"+esc(trackName(tr).split(" · ")[0])+"</small></div>";
  mods.forEach(function(m,k){
    var n=m.items.length,d=m.items.filter(function(i){return S.done[i.id];}).length,p=n?Math.round(d/n*100):0;
    var first=m.items.find(function(i){return !S.done[i.id];})||m.items[0];
    var cur=trackNext&&m.items.indexOf(trackNext)>=0;
    var half=Math.ceil(n/2),L=m.items.slice(0,half),R=m.items.slice(half);
    var side=function(list,c){return list.length?"<div class=\"pz-side "+c+"\">"+list.map(function(i){return pzLeaf(i,nx&&nx.id===i.id);}).join("")+"</div>":"";};
    var s=d===n&&n?"done":d?"part":"todo";
    h+="<div class=\"pz-row\" id=\"map-"+m.id+"\" data-st=\""+s+"\">"+side(L,"l")+
      "<button type=\"button\" class=\"pz-node "+s+(cur?" cur":"")+"\" style=\"--c:"+PZ_RINGS[k%PZ_RINGS.length]+"\" data-act=\"open\" data-id=\""+esc(first.id)+"\" title=\""+esc(m.n+" "+m.t+": "+d+" of "+n+" lessons complete")+"\">"+
      "<span class=\"dot\">"+esc(m.n)+"</span><span style=\"min-width:0;flex:1\"><span class=\"nt\">"+esc(m.t)+"</span><span class=\"nc\">"+(s==="done"?"✓ Complete":d+" of "+n+" lessons")+"</span><span class=\"nb\"><i style=\"width:"+p+"%\"></i></span></span></button>"+side(R,"r")+"</div>";
  });
  h+="<div class=\"pz-cap end\"><b>"+(st.done===st.all.length&&st.all.length?"★":(st.all.length-st.done))+"</b><small>"+(st.done===st.all.length&&st.all.length?"done":"to go")+"</small></div></div></section></div>";
  return h;
}
function mapDraw(){
  var road=document.querySelector(".pz-road"),svg=road&&road.querySelector(".pz-lines");if(!svg)return;
  var box=road.getBoundingClientRect(),W=box.width,H=road.scrollHeight;
  svg.setAttribute("viewBox","0 0 "+W+" "+H);svg.setAttribute("width",W);svg.setAttribute("height",H);
  var rel=function(el){var r=el.getBoundingClientRect();return {l:r.left-box.left,r:r.right-box.left,t:r.top-box.top,b:r.bottom-box.top,cx:(r.left+r.right)/2-box.left,cy:(r.top+r.bottom)/2-box.top};};
  var narrow=W<700,out=[];
  var cap=rel(road.querySelector(".pz-cap")),end=rel(road.querySelector(".pz-cap.end"));
  var spineX=narrow?cap.cx:W/2;
  road.querySelectorAll(".pz-row").forEach(function(row){
    var node=row.querySelector(".pz-node");if(!node)return;
    var n=rel(node);
    row.querySelectorAll(".pz-leaf").forEach(function(leaf){
      var f=rel(leaf),cls="br"+(leaf.dataset.st?" "+leaf.dataset.st:""),d;
      if(narrow){var x0=n.l+20;d="M"+x0+" "+n.b+" V"+f.cy+" H"+f.l;}
      else if(f.r<=n.l){var xm=(n.l+f.r)/2;d="M"+n.l+" "+n.cy+" H"+xm+" V"+f.cy+" H"+f.r;}
      else{var xn=(n.r+f.l)/2;d="M"+n.r+" "+n.cy+" H"+xn+" V"+f.cy+" H"+f.l;}
      out.push("<path class=\""+cls+"\" d=\""+d+"\"/>");
    });
  });
  svg.innerHTML="<path class=\"sp\" d=\"M"+spineX+" "+cap.cy+" V"+end.cy+"\"/>"+out.join("");
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
    s = s.replace(FONT, "")

    def rep(a, b):
        nonlocal s
        if b in s:
            return
        assert s.count(a) == 1, (a[:70], s.count(a))
        s = s.replace(a, b)

    if "</head>" in s:
        s = s.replace("</head>", FONT + "\n</head>", 1)
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
