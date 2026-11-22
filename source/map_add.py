"""Add a Map tab to the course engine, styled as a graphic-syllabus poster: a flat light-blue
page with navy section tabs, icon tiles, a module donut, ringed module badges and a vertical
roadmap timeline. Every lesson box links to its lesson, and the whole poster reflects progress.

The roadmap's connectors are drawn as an SVG overlay after layout, so they follow the boxes
at any width. The tab sits first, before Overview.

usage: python3 map_add.py course.html   (idempotent)
"""
import sys

FONT = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" data-map-font>'

CSS = r"""/* MAP:BEGIN */
.pz{--pz-bg1:#EEF4FF;--pz-bg2:#F5F0FF;--pz-navy:#1D4ED8;--pz-deep:#0F1F3D;--pz-yel:#F59E0B;--pz-org:#F97316;--pz-sky:#0EA5E9;--pz-mid:#6366F1;--pz-green:#10B981;
  --pz-ink:#0F1F3D;--pz-sub:#5B6B82;--pz-card:#FFFFFF;--pz-pale:#F1F5FB;--pz-line:#DCE4F0;--pz-shadow:0 1px 2px rgba(15,31,61,.04),0 8px 24px -12px rgba(15,31,61,.18);
  --pz-grad:linear-gradient(135deg,#2563EB 0%,#7C3AED 100%);--pz-grad2:linear-gradient(90deg,#10B981,#0EA5E9);
  font-family:'Plus Jakarta Sans','Inter',var(--font-body),system-ui,sans-serif;color:var(--pz-ink);
  background:radial-gradient(1200px 500px at 0% 0%,color-mix(in srgb,#60A5FA 22%,transparent),transparent 60%),radial-gradient(900px 500px at 100% 10%,color-mix(in srgb,#A78BFA 20%,transparent),transparent 60%),linear-gradient(180deg,var(--pz-bg1),var(--pz-bg2));
  max-width:1160px;margin:0 auto 16px;border-radius:24px;padding:clamp(18px,3.4vw,40px) clamp(14px,3.4vw,40px) 36px;position:relative;overflow:hidden;border:1px solid var(--pz-line)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .pz{--pz-bg1:#0B1222;--pz-bg2:#120E24;--pz-navy:#60A5FA;--pz-deep:#E6EEFB;--pz-ink:#E6EEFB;--pz-sub:#94A3B8;--pz-card:#131C30;--pz-pale:#1A2540;--pz-line:#24314D;--pz-shadow:0 1px 2px rgba(0,0,0,.3),0 10px 30px -14px rgba(0,0,0,.7)}}
:root[data-theme="dark"] .pz{--pz-bg1:#0B1222;--pz-bg2:#120E24;--pz-navy:#60A5FA;--pz-deep:#E6EEFB;--pz-ink:#E6EEFB;--pz-sub:#94A3B8;--pz-card:#131C30;--pz-pale:#1A2540;--pz-line:#24314D;--pz-shadow:0 1px 2px rgba(0,0,0,.3),0 10px 30px -14px rgba(0,0,0,.7)}
.pz *{box-sizing:border-box}
.pz button{font:inherit;color:inherit}
.pz .sc{font-variant:normal}
/* header */
.pz-head{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:22px 30px;align-items:center;margin-bottom:18px}
.pz-title{font-weight:800;font-size:clamp(2rem,4.6vw,3.2rem);line-height:1.02;letter-spacing:-.035em;background:var(--pz-grad);-webkit-background-clip:text;background-clip:text;color:transparent;padding:2px 0}
.pz-sub{display:inline-flex;align-items:center;gap:8px;font-size:.92rem;font-weight:600;color:var(--pz-sub);margin:10px 0 0}
.pz-sub::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--pz-green);box-shadow:0 0 0 4px color-mix(in srgb,var(--pz-green) 22%,transparent)}
.pz-facts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.pz-fact{display:flex;align-items:center;gap:12px;min-width:0;background:var(--pz-card);border:1px solid var(--pz-line);border-radius:16px;padding:12px 14px;box-shadow:var(--pz-shadow)}
.pz-ico{flex:none;width:40px;height:40px;border-radius:12px;background:var(--pz-grad);color:#fff;display:grid;place-items:center;box-shadow:0 6px 14px -6px rgba(37,99,235,.6)}
.pz-fact:nth-child(2) .pz-ico{background:linear-gradient(135deg,#0EA5E9,#10B981)}
.pz-fact:nth-child(3) .pz-ico{background:linear-gradient(135deg,#F59E0B,#F97316)}
.pz-fact:nth-child(4) .pz-ico{background:linear-gradient(135deg,#EC4899,#8B5CF6)}
.pz-ico svg{width:20px;height:20px}
.pz-fact>div{min-width:0;display:flex;flex-direction:column;line-height:1.15}
.pz-fact b{font-weight:800;font-size:1.3rem;letter-spacing:-.02em}
.pz-fact div span{color:var(--pz-sub);font-size:.8rem;font-weight:500}
.pz-tracks{display:inline-flex;flex-wrap:wrap;align-items:center;gap:4px;margin:0 0 26px;padding:5px;border-radius:999px;background:color-mix(in srgb,var(--pz-card) 70%,transparent);border:1px solid var(--pz-line);backdrop-filter:blur(8px);font-size:.9rem;max-width:100%}
.pz-tracks .pz-ico,.pz-tracks>b{display:none}
.pz-tracks button{background:none;border:0;padding:8px 14px;cursor:pointer;border-radius:999px;font-weight:600;color:var(--pz-sub);transition:background .2s,color .2s}
.pz-tracks button:hover{color:var(--pz-ink)}
.pz-tracks button[aria-pressed="true"]{background:var(--pz-card);color:var(--pz-ink);box-shadow:var(--pz-shadow)}
.pz-tracks button small{font-weight:700;margin-left:4px;color:var(--pz-navy)}
/* section cards */
.pz-sec{margin:0 0 20px;background:var(--pz-card);border:1px solid var(--pz-line);border-radius:20px;padding:20px 22px;box-shadow:var(--pz-shadow);min-width:0}
.pz-tab{display:flex;align-items:center;gap:10px;margin:0 0 16px}
.pz-tab b{font-size:.74rem;font-weight:800;text-transform:uppercase;letter-spacing:.12em;color:var(--pz-sub)}
.pz-tab::before{content:"";width:6px;height:18px;border-radius:4px;background:var(--pz-grad)}
.pz-grid2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0 20px;align-items:stretch}
/* you are here */
.pz-here{display:flex;gap:22px;align-items:center}
.pz-ring{flex:none;width:150px;height:150px;border-radius:50%;background:conic-gradient(from 200deg,#F59E0B,#F97316,#EC4899,#8B5CF6,#2563EB,#F59E0B);display:grid;place-items:center;padding:8px;box-shadow:0 14px 30px -14px rgba(249,115,22,.55)}
.pz-ring>div{width:100%;height:100%;border-radius:50%;background:var(--pz-card);display:grid;place-content:center;text-align:center;color:var(--pz-ink);font-weight:800;font-size:1.9rem;letter-spacing:-.03em;line-height:1}
.pz-ring small{display:block;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--pz-sub);margin-top:6px}
.pz-here h3{margin:0 0 3px;font-size:.72rem;font-weight:800;text-transform:uppercase;letter-spacing:.12em;color:var(--pz-sub)}
.pz-here p{margin:0 0 12px;line-height:1.45;font-weight:600}
.pz-btn{display:inline-flex;align-items:center;gap:8px;background:var(--pz-grad);color:#fff!important;border:0;border-radius:12px;padding:10px 16px;font-weight:700;cursor:pointer;box-shadow:0 8px 18px -8px rgba(37,99,235,.7);transition:transform .15s}
.pz-btn:hover{transform:translateY(-1px)}
/* donut */
.pz-donut-wrap{display:flex;gap:20px;align-items:center;flex-wrap:wrap}
.pz-donut{flex:none;position:relative;width:200px;height:200px}
.pz-donut svg{width:100%;height:100%;transform:rotate(-90deg);filter:drop-shadow(0 8px 14px rgba(15,31,61,.12))}
.pz-donut path{cursor:pointer;transition:opacity .15s}
.pz-donut path:hover{opacity:.75}
.pz-donut .mid{position:absolute;inset:0;display:grid;place-content:center;text-align:center;pointer-events:none}
.pz-donut .mid b{font-size:2.2rem;font-weight:800;line-height:1;letter-spacing:-.04em}
.pz-donut .mid span{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--pz-sub);margin-top:4px}
.pz-keys{display:grid;gap:8px;min-width:0}
.pz-key{display:flex;align-items:center;gap:10px}
.pz-key i{display:none}
.pz-key span{font-size:.9rem;font-weight:600;white-space:nowrap;display:inline-flex;align-items:center}
.pz-key em{display:inline-block;width:12px;height:12px;border-radius:4px;margin-right:9px;font-style:normal}
/* module badges */
.pz-badges{display:grid;grid-template-columns:repeat(auto-fill,minmax(118px,1fr));gap:12px}
.pz-badge{background:var(--pz-pale);border:1px solid transparent;border-radius:16px;padding:14px 8px 12px;cursor:pointer;text-align:center;display:grid;justify-items:center;gap:8px;transition:transform .15s,border-color .15s,background .15s}
.pz-badge:hover{transform:translateY(-2px);border-color:var(--pz-line);background:var(--pz-card);box-shadow:var(--pz-shadow)}
.pz-badge .rg{width:74px;height:74px;border-radius:50%;padding:6px;background:conic-gradient(var(--c) var(--p),color-mix(in srgb,var(--c) 16%,var(--pz-card)) 0)}
.pz-badge .rg>span{width:100%;height:100%;border-radius:50%;background:var(--pz-card);display:grid;place-content:center;line-height:1.05}
.pz-badge .rg b{font-weight:800;font-size:1.05rem;letter-spacing:-.02em}
.pz-badge .rg small{font-size:.66rem;color:var(--pz-sub);font-weight:600}
.pz-badge.done .rg{background:var(--pz-grad2)}
.pz-badge.done .rg>span{background:var(--pz-card);color:var(--pz-green)}
.pz-badge .cap{font-size:.74rem;font-weight:600;line-height:1.25;color:var(--pz-sub);max-width:112px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.pz-badge.cur{border-color:color-mix(in srgb,var(--pz-org) 60%,transparent);background:color-mix(in srgb,var(--pz-org) 8%,var(--pz-card))}
/* roadmap */
.pz-legend{display:flex;flex-wrap:wrap;gap:8px 18px;margin:-4px 0 18px;font-size:.82rem;font-weight:600;color:var(--pz-sub)}
.pz-legend span{display:inline-flex;align-items:center;gap:7px}
.pz-legend i{display:block;width:10px;height:10px;border-radius:50%}
.pz-road{position:relative;padding:0 0 4px}
.pz-lines{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible}
.pz-lines .sp{stroke:url(#pzspine);stroke-width:4;fill:none;stroke-linecap:round}
.pz-lines .br{fill:none;stroke:var(--pz-line);stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.pz-lines .br.done{stroke:color-mix(in srgb,var(--pz-green) 70%,transparent)}
.pz-lines .br.next{stroke:var(--pz-org);stroke-width:2.2}
.pz-cap{position:relative;z-index:1;margin:0 auto 26px;width:104px;height:104px;border-radius:50%;background:var(--pz-card);border:0;display:grid;place-content:center;text-align:center;line-height:1;box-shadow:0 0 0 6px color-mix(in srgb,var(--pz-navy) 14%,transparent),var(--pz-shadow)}
.pz-cap b{font-size:1.6rem;font-weight:800;letter-spacing:-.04em;background:var(--pz-grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.pz-cap small{font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--pz-sub);margin-top:4px}
.pz-cap.end{width:78px;height:78px;margin:4px auto 0}
.pz-cap.end b{font-size:1.05rem}
.pz-row{position:relative;display:grid;grid-template-columns:1fr minmax(210px,260px) 1fr;column-gap:52px;align-items:center;margin:0 0 26px}
.pz .pz-node{position:relative;z-index:1;grid-column:2;display:flex;align-items:center;gap:12px;background:var(--pz-card);color:var(--pz-ink);border:1px solid var(--pz-line);border-radius:16px;padding:10px 14px 10px 10px;cursor:pointer;text-align:left;width:100%;box-shadow:var(--pz-shadow);transition:transform .15s}
.pz .pz-node:hover{transform:translateY(-2px)}
.pz-node .dot{flex:none;width:40px;height:40px;border-radius:12px;background:color-mix(in srgb,var(--c) 16%,var(--pz-card));color:var(--c);display:grid;place-items:center;font-weight:800;font-size:.82rem;border:0}
.pz-node .nt{display:block;font-weight:700;line-height:1.2;font-size:.95rem}
.pz-node .nc{display:block;font-size:.74rem;color:var(--pz-sub);margin-top:2px}
.pz-node .nb{display:block;height:5px;margin-top:7px;border-radius:9px;background:var(--pz-pale);overflow:hidden}
.pz-node .nb i{display:block;height:100%;border-radius:9px;background:var(--pz-grad2)}
.pz .pz-node.done{background:linear-gradient(135deg,color-mix(in srgb,var(--pz-green) 14%,var(--pz-card)),var(--pz-card));border-color:color-mix(in srgb,var(--pz-green) 40%,transparent)}
.pz .pz-node.done .dot{background:var(--pz-green);color:#fff}
.pz .pz-node.cur{border-color:var(--pz-org);box-shadow:0 0 0 4px color-mix(in srgb,var(--pz-org) 18%,transparent),var(--pz-shadow);outline:0}
.pz-side{display:flex;flex-direction:column;gap:7px;min-width:0}
.pz-side.l{grid-column:1;grid-row:1;align-items:flex-end}
.pz-side.r{grid-column:3;grid-row:1;align-items:flex-start}
.pz-leaf{position:relative;z-index:1;display:inline-flex;align-items:center;max-width:100%;background:var(--pz-card);border:1px solid var(--pz-line);border-radius:12px;padding:0;cursor:pointer;text-align:left;transition:border-color .15s,transform .15s,box-shadow .15s}
.pz-leaf:hover{border-color:color-mix(in srgb,var(--pz-navy) 50%,transparent);transform:translateY(-1px);box-shadow:var(--pz-shadow)}
.pz-leaf .mk{flex:none;width:10px;height:10px;border-radius:50%;margin:0 0 0 11px;background:transparent;box-shadow:inset 0 0 0 2px color-mix(in srgb,var(--pz-sub) 55%,transparent);outline:0}
.pz-leaf .bx{display:flex;align-items:center;gap:8px;min-width:0;background:none;padding:7px 12px 7px 9px;font-size:.86rem;line-height:1.25}
.pz-leaf .id{flex:none;color:var(--pz-sub);font-weight:600;font-size:.75rem;font-variant-numeric:tabular-nums}
.pz-leaf .tt{min-width:0;font-weight:500}
.pz-leaf .ex{flex:none;display:inline-flex;gap:3px}
.pz-leaf .ex i{width:5px;height:5px;border-radius:50%;background:var(--pz-line)}
.pz-leaf .ex i.on{background:var(--pz-navy)}
.pz-leaf .tag{flex:none;font-size:.64rem;font-weight:800;color:#fff;background:var(--pz-org);padding:2px 8px;border-radius:999px;text-transform:uppercase;letter-spacing:.06em}
.pz-leaf.done{background:color-mix(in srgb,var(--pz-green) 7%,var(--pz-card));border-color:color-mix(in srgb,var(--pz-green) 30%,transparent)}
.pz-leaf.done .mk{background:var(--pz-green);box-shadow:none}
.pz-leaf.done .tt{color:color-mix(in srgb,var(--pz-ink) 75%,transparent)}
.pz-leaf.next{border-color:var(--pz-org);box-shadow:0 0 0 3px color-mix(in srgb,var(--pz-org) 16%,transparent)}
.pz-leaf.next .mk{background:var(--pz-org);box-shadow:0 0 0 0 color-mix(in srgb,var(--pz-org) 60%,transparent);animation:pzpulse 1.8s infinite}
@keyframes pzpulse{70%{box-shadow:0 0 0 7px transparent}100%{box-shadow:0 0 0 0 transparent}}
.pz-leaf.rev .mk{background:var(--pz-yel);box-shadow:none}
.pz-leaf.rev{border-color:color-mix(in srgb,var(--pz-yel) 60%,transparent)}
.pz-leaf.proj .id::before{content:"\2605 ";color:var(--pz-yel)}
.pz-side.l .pz-leaf{flex-direction:row-reverse}
.pz-side.l .pz-leaf .mk{margin:0 11px 0 0}
.pz-side.l .pz-leaf .bx{padding:7px 9px 7px 12px}
@media (max-width:900px){.pz-head{grid-template-columns:1fr}.pz-grid2{grid-template-columns:1fr}}
@media (max-width:720px){
  .pz{border-radius:18px}
  .pz-facts{grid-template-columns:1fr 1fr;gap:8px}
  .pz-fact{padding:10px;gap:9px}
  .pz-fact b{font-size:1.1rem}
  .pz-tracks{display:flex;border-radius:16px}
  .pz-tracks button{flex:1 1 auto;padding:7px 10px}
  .pz-sec{padding:16px 14px;border-radius:16px}
  .pz-here{flex-direction:column;align-items:flex-start}
  .pz-ring{width:124px;height:124px}
  .pz-badges{grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:8px}
  .pz-badge .rg{width:62px;height:62px}
  .pz-row{grid-template-columns:1fr;column-gap:0;row-gap:7px;padding-left:28px;margin-bottom:22px}
  .pz .pz-node{grid-column:1;order:-1}
  .pz-side.l,.pz-side.r{grid-column:1;grid-row:auto;align-items:stretch;padding-left:20px}
  .pz-side.l .pz-leaf{flex-direction:row}
  .pz-side.l .pz-leaf .mk{margin:0 0 0 11px}
  .pz-side.l .pz-leaf .bx{padding:7px 12px 7px 9px}
  .pz-leaf{width:100%}.pz-leaf .bx{flex:1}
  .pz-cap{margin-left:0}
  .pz-cap.end{margin-left:13px}
}
@media (max-width:340px){.pz-facts{grid-template-columns:1fr}}
@media (prefers-reduced-motion:no-preference){.pz-row{animation:pzin .45s both}@keyframes pzin{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}}
@media (prefers-reduced-motion:reduce){.pz-leaf.next .mk{animation:none}}
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
var PZ_RINGS=["#6366F1","#0EA5E9","#F59E0B","#EC4899","#10B981","#8B5CF6"];
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
    var col=d===n?"var(--pz-green)":d?"var(--pz-sky)":"var(--pz-line)";
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
      "<div class=\"pz-keys\"><div class=\"pz-key\"><i aria-hidden=\"true\">"+PZ_ICON.check+"</i><span><em style=\"background:var(--pz-green)\"></em>"+st.modsDone+(st.modsDone===1?" module":" modules")+" complete</span></div>"+
      "<div class=\"pz-key\"><i aria-hidden=\"true\">"+PZ_ICON.half+"</i><span><em style=\"background:var(--pz-sky)\"></em>"+started+" in progress</span></div>"+
      "<div class=\"pz-key\"><i aria-hidden=\"true\">"+PZ_ICON.ring+"</i><span><em style=\"background:var(--pz-line)\"></em>"+(mods.length-st.modsDone-started)+" not started</span></div></div></div></section></div>"+
    "<section class=\"pz-sec\"><div class=\"pz-tab\"><b>Modules</b></div><div class=\"pz-badges\">"+mods.map(function(m,k){
      var n=m.items.length,d=m.items.filter(function(i){return S.done[i.id];}).length,p=n?Math.round(d/n*100):0;
      var cur=trackNext&&m.items.indexOf(trackNext)>=0;
      return "<button type=\"button\" class=\"pz-badge"+(d===n&&n?" done":"")+(cur?" cur":"")+"\" data-act=\"mapjump\" data-v=\""+m.id+"\" style=\"--c:"+PZ_RINGS[k%PZ_RINGS.length]+";--p:"+p+"%\" title=\""+esc(m.n+" "+m.t+": "+d+" of "+n+" lessons")+"\"><span class=\"rg\"><span><b>"+esc(m.n)+"</b><small>"+d+"/"+n+"</small></span></span><span class=\"cap\">"+esc(m.t)+"</span></button>";
    }).join("")+"</div></section>"+
    "<section class=\"pz-sec\" style=\"margin-bottom:0\"><div class=\"pz-tab\"><b>Roadmap</b></div>"+
    "<div class=\"pz-legend\"><span><i style=\"background:var(--pz-green)\"></i>Complete</span><span><i style=\"background:var(--pz-org)\"></i>Next lesson</span><span><i style=\"background:var(--pz-yel)\"></i>Review due</span><span><i style=\"background:transparent;box-shadow:inset 0 0 0 2px var(--pz-sub)\"></i>Not started</span></div>"+
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
      var elbow=function(x1,y1,xm,y2,x2){var dy=y2-y1,r=Math.min(10,Math.abs(dy)/2,Math.abs(xm-x1),Math.abs(x2-xm));if(Math.abs(dy)<1)return "M"+x1+" "+y1+" H"+x2;var sx=xm>x1?1:-1,sy=dy>0?1:-1,ex=x2>xm?1:-1;
        return "M"+x1+" "+y1+" H"+(xm-sx*r)+" Q"+xm+" "+y1+" "+xm+" "+(y1+sy*r)+" V"+(y2-sy*r)+" Q"+xm+" "+y2+" "+(xm+ex*r)+" "+y2+" H"+x2;};
      if(narrow){var x0=n.l+18,r0=Math.min(10,Math.abs(f.cy-n.b));d="M"+x0+" "+n.b+" V"+(f.cy-r0)+" Q"+x0+" "+f.cy+" "+(x0+r0)+" "+f.cy+" H"+f.l;}
      else if(f.r<=n.l){d=elbow(n.l,n.cy,(n.l+f.r)/2,f.cy,f.r);}
      else{d=elbow(n.r,n.cy,(n.r+f.l)/2,f.cy,f.l);}
      out.push("<path class=\""+cls+"\" d=\""+d+"\"/>");
    });
  });
  svg.innerHTML="<defs><linearGradient id=\"pzspine\" gradientUnits=\"userSpaceOnUse\" x1=\""+spineX+"\" y1=\""+cap.cy+"\" x2=\""+spineX+"\" y2=\""+end.cy+"\"><stop offset=\"0\" style=\"stop-color:#2563EB\"/><stop offset=\".5\" style=\"stop-color:#7C3AED\"/><stop offset=\"1\" style=\"stop-color:#0EA5E9\"/></linearGradient></defs><path class=\"sp\" d=\"M"+spineX+" "+cap.cy+" V"+end.cy+"\"/>"+out.join("");
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
