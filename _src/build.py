"""Builds the case studies site. Run from anywhere:  python3 _src/build.py
Edits go in _src/data.py (content) or here (layout and styles). Output: the .html files in the repo root."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import os, json, shutil
from data import PROJECTS

FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..900&family=Space+Mono:wght@400;700&family=Anton+SC&display=swap" rel="stylesheet">'

CSS = r"""
:root{--paper:#EDEFEA;--paper2:#F7F8F4;--ink:#1A1F2B;--muted:#4F5663;--rule:#C7CCC4;--onc:#fff;
--f:'Archivo',ui-sans-serif,system-ui,-apple-system,'Segoe UI',sans-serif;box-sizing:border-box;
padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#14171D;--paper2:#1B1F27;--ink:#E8EBE4;--muted:#A9B0BA;--rule:#323844}}
:root[data-theme="dark"]{--paper:#14171D;--paper2:#1B1F27;--ink:#E8EBE4;--muted:#A9B0BA;--rule:#323844}
html{scroll-padding-top:env(safe-area-inset-top,0px)}
*,*::before,*::after{box-sizing:inherit}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--f);font-size:18px;line-height:1.6;font-variation-settings:'wdth' 100;-webkit-font-smoothing:antialiased}
a{color:inherit}
img{max-width:100%}
:focus-visible{outline:3px solid var(--ink);outline-offset:3px;border-radius:4px}
.wrap{max-width:1200px;margin:0 auto;padding:0 clamp(20px,5vw,56px)}
/* top bar */
.bar{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;padding:20px 0}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;font-weight:800;font-variation-settings:'wdth' 112;font-size:19px;letter-spacing:-.01em}
.brand i{width:30px;height:30px;border-radius:9px;background:var(--ink);display:grid;place-items:center;color:var(--paper);font-style:normal;font-size:15px}
.bar nav{display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.lnk{text-decoration:none;padding:10px 14px;border-radius:999px;font-size:16px;font-weight:500}
.lnk:hover{background:rgba(127,127,127,.14)}
.btn{display:inline-flex;align-items:center;min-height:46px;text-decoration:none;padding:10px 20px;border-radius:999px;background:var(--ink);color:var(--paper);font-weight:600;font-size:16px}
.btn:hover{opacity:.88}
.on-color .btn{background:#fff;color:#14171D}
.on-color .lnk:hover{background:rgba(255,255,255,.16)}
.on-color .brand i{background:#fff;color:var(--c)}
/* index hero */
.ihero{padding:clamp(40px,8vw,96px) 0 40px}
.ihero h1{font-size:clamp(46px,8.4vw,124px);line-height:.9;letter-spacing:-.035em;font-weight:850;font-variation-settings:'wdth' 125;margin:0 0 28px;max-width:11ch}
.ihero p{font-size:clamp(18px,2vw,22px);color:var(--muted);max-width:56ch;margin:0}
/* home screen */
.home{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:clamp(20px,3vw,40px);padding:48px 0 64px}
.app{text-decoration:none;display:flex;flex-direction:column;align-items:flex-start;gap:12px}
.icon{width:100%;aspect-ratio:1;border-radius:24%;background:var(--c);display:grid;place-items:center;color:#fff;transition:transform .2s ease}
.icon svg{width:44%;height:44%}
.app:hover .icon{translate:0 -4px}
.app b{font-size:18px;font-weight:700;line-height:1.2}
.app span{font-size:15px;color:var(--muted);line-height:1.3;margin-top:-8px}
.tally{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));border-top:2px solid var(--ink);border-bottom:1px solid var(--rule)}
.tally div{padding:22px 0 24px;border-right:1px solid var(--rule);padding-right:20px}
.tally div:last-child{border-right:0}
.tally strong{display:block;font-size:clamp(36px,4.6vw,60px);line-height:1;font-weight:800;font-variation-settings:'wdth' 118;letter-spacing:-.03em}
.tally span{color:var(--muted);font-size:16px}
/* list */
.list{padding-top:72px;padding-bottom:40px}
.list h2,.sec h2{font-size:clamp(28px,3.4vw,40px);line-height:1.05;letter-spacing:-.02em;font-weight:800;font-variation-settings:'wdth' 115;margin:0 0 24px}
.cards{display:grid;gap:22px;perspective:1400px}
.row{--rx:0deg;--ry:0deg;--lift:0px;display:grid;grid-template-columns:96px minmax(0,1fr) auto;gap:28px;align-items:center;padding:26px 28px;text-decoration:none;
background:var(--paper2);border:1px solid var(--rule);border-radius:26px;position:relative;transform-style:preserve-3d;
transform:translateY(var(--lift)) rotateX(var(--rx)) rotateY(var(--ry));
box-shadow:0 1px 0 rgba(255,255,255,.6) inset,0 6px 0 -1px color-mix(in srgb,var(--c) 22%,var(--rule)),0 14px 28px -14px rgba(20,25,35,.28);
transition:transform .25s cubic-bezier(.2,.8,.2,1),box-shadow .25s ease,border-color .25s ease}
.row::after{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;
background:radial-gradient(420px circle at var(--mx,50%) var(--my,0%),rgba(255,255,255,.35),transparent 60%);opacity:0;transition:opacity .25s}
.row:hover,.row:focus-visible{--lift:-6px;border-color:color-mix(in srgb,var(--c) 45%,var(--rule));
box-shadow:0 1px 0 rgba(255,255,255,.6) inset,0 10px 0 -1px color-mix(in srgb,var(--c) 38%,var(--rule)),0 30px 50px -18px color-mix(in srgb,var(--c) 45%,rgba(20,25,35,.5))}
.row:hover::after{opacity:1}
.row:active{--lift:2px;box-shadow:0 1px 0 rgba(255,255,255,.6) inset,0 2px 0 -1px color-mix(in srgb,var(--c) 30%,var(--rule)),0 6px 12px -8px rgba(20,25,35,.3);transition-duration:.08s}
.row .icon{width:96px;border-radius:24px;transform:translateZ(30px);
box-shadow:inset 0 2px 0 rgba(255,255,255,.28),inset 0 -4px 0 rgba(0,0,0,.18),0 6px 0 color-mix(in srgb,var(--c) 65%,#000),0 16px 24px -10px color-mix(in srgb,var(--c) 70%,transparent);transition:transform .25s cubic-bezier(.2,.8,.2,1)}
.row:hover .icon{transform:translateZ(46px) translateY(-3px) rotate(-3deg)}
.row h3{margin:0;font-size:clamp(24px,2.6vw,32px);line-height:1.1;font-weight:800;font-variation-settings:'wdth' 112;letter-spacing:-.015em;transform:translateZ(18px)}
.row p{margin:6px 0 0;color:var(--muted);max-width:60ch}
.row .kpi{text-align:right;white-space:nowrap;display:grid;justify-items:end;gap:2px;transform:translateZ(22px)}
.row .kpi b{display:block;font-size:20px}
.row .kpi span{font-size:15px;color:var(--muted)}
.open{display:inline-flex;align-items:center;gap:8px;margin-top:12px;min-height:40px;padding:8px 14px 8px 16px;border-radius:999px;border:1.5px solid var(--ink);font-weight:650;font-size:15px;transition:background .2s,color .2s,border-color .2s,gap .2s}
.open svg{width:16px;height:16px;transition:transform .2s}
.row:hover .open,.row:focus-visible .open{background:var(--c);border-color:var(--c);color:#fff}
.row:hover .open svg{transform:translateX(3px)}
@media (max-width:720px){.row{grid-template-columns:64px minmax(0,1fr);gap:18px;padding:20px}.row .icon{width:64px;border-radius:17px}.row .kpi{grid-column:1/-1;justify-items:start;text-align:left}}
@media (prefers-reduced-motion:reduce){.row,.row .icon,.open svg{transition:none}.row:hover .icon{transform:translateZ(30px)}}
/* case hero */
.chero{background:var(--c);color:#fff;--onc:#fff}
.chero .inner{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:clamp(28px,5vw,72px);align-items:center;padding:clamp(28px,5vw,64px) 0 clamp(36px,5vw,56px)}
@media (max-width:900px){.chero .inner{grid-template-columns:1fr}}
.crumb{display:flex;align-items:center;gap:14px;margin-bottom:28px}
.crumb .icon{width:64px;border-radius:16px;background:rgba(255,255,255,.16);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.4)}
.crumb div{font-size:16px;line-height:1.35}
.crumb b{display:block;font-size:18px}
.chero h1{font-size:clamp(44px,7.2vw,104px);line-height:.92;letter-spacing:-.035em;font-weight:850;font-variation-settings:'wdth' 125;margin:0 0 24px}
.chero .lede{font-size:clamp(18px,1.9vw,22px);max-width:46ch;margin:0;opacity:.94}
.storerow{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:1px solid rgba(255,255,255,.35)}
@media (max-width:640px){.storerow{grid-template-columns:repeat(2,minmax(0,1fr))}}
.storerow div{padding:20px 16px 26px 0;border-right:1px solid rgba(255,255,255,.25)}
.storerow div:last-child{border-right:0}
.storerow strong{display:block;font-size:clamp(30px,3.6vw,48px);line-height:1;font-weight:800;font-variation-settings:'wdth' 118;letter-spacing:-.025em}
.storerow span{font-size:15px;opacity:.9}
/* sections */
.sec{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,2.4fr);gap:clamp(20px,4vw,64px);padding:clamp(48px,6vw,80px) 0;border-bottom:1px solid var(--rule)}
@media (max-width:820px){.sec{grid-template-columns:1fr}}
.sec h2{position:sticky;top:24px;align-self:start;margin:0}
@media (max-width:820px){.sec h2{position:static}}
.prose p{margin:0 0 18px;max-width:64ch}
.prose .big{font-size:clamp(21px,2.2vw,27px);line-height:1.42;font-weight:500;letter-spacing:-.008em}
.prose .who{color:var(--muted)}
.hard{display:grid;gap:0}
.hard div{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.6fr);gap:24px;padding:20px 0;border-top:1px solid var(--rule)}
.hard div:first-child{border-top:0;padding-top:0}
@media (max-width:640px){.hard div{grid-template-columns:1fr;gap:6px}}
.hard h3,.feat h3{margin:0;font-size:20px;line-height:1.3;font-weight:700}
.hard p,.feat p{margin:0;color:var(--muted)}
.feat{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:32px 40px}
.feat div{border-top:3px solid var(--c);padding-top:16px}
.feat h3{margin-bottom:6px}
.steps{list-style:none;margin:0;padding:0;counter-reset:s;display:grid;gap:0}
.steps li{counter-increment:s;display:grid;grid-template-columns:64px minmax(0,1fr);gap:16px;padding:20px 0;border-top:1px solid var(--rule)}
.steps li:first-child{border-top:0;padding-top:0}
.steps li::before{content:counter(s);width:44px;height:44px;border-radius:50%;border:2px solid var(--c);display:grid;place-items:center;font-weight:800;color:var(--ink)}
.steps h3{margin:0 0 4px;font-size:20px;font-weight:700}
.steps p{margin:0;color:var(--muted);max-width:60ch}
.chips{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 28px;padding:0;list-style:none}
.chips li{padding:8px 16px;border-radius:999px;border:1.5px solid var(--rule);font-size:16px;font-weight:500}
.links{display:flex;flex-wrap:wrap;gap:12px}
.ghost{display:inline-flex;align-items:center;min-height:46px;padding:10px 20px;border-radius:999px;border:2px solid var(--ink);text-decoration:none;font-weight:600;font-size:16px}
.ghost:hover{background:var(--ink);color:var(--paper)}
.outcome{font-size:clamp(26px,3.2vw,40px);line-height:1.15;letter-spacing:-.02em;font-weight:750;font-variation-settings:'wdth' 108;margin:0;max-width:26ch}
/* next + cta */
.next{display:block;text-decoration:none;background:var(--c);color:#fff;border-radius:28px;padding:clamp(28px,4vw,48px);margin:clamp(48px,6vw,80px) 0 0}
.next span{font-size:16px;opacity:.9}
.next b{display:block;font-size:clamp(36px,6vw,80px);line-height:.95;letter-spacing:-.03em;font-weight:850;font-variation-settings:'wdth' 125;margin-top:8px}
.next:hover b{text-decoration:underline;text-decoration-thickness:3px;text-underline-offset:8px}
.cta{padding:clamp(56px,8vw,104px) 0;display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr);gap:32px;align-items:end}
@media (max-width:820px){.cta{grid-template-columns:1fr}}
.cta h2{font-size:clamp(36px,5vw,64px);line-height:.98;letter-spacing:-.03em;font-weight:850;font-variation-settings:'wdth' 120;margin:0}
.cta p{margin:0 0 20px;color:var(--muted)}
footer{border-top:1px solid var(--rule);padding:32px 0 48px;font-size:15px;color:var(--muted)}
footer .wrap{display:flex;flex-wrap:wrap;gap:12px 32px;justify-content:space-between}
footer a{text-decoration:none}footer a:hover{text-decoration:underline}
/* device mocks */
.mock{justify-self:center;width:min(100%,300px)}
.mock.web{width:100%;max-width:520px}
.phone{background:#0E1015;border-radius:44px;padding:12px;box-shadow:0 30px 60px -20px rgba(0,0,0,.45)}
.screen{background:#fff;color:#1A1F2B;border-radius:33px;overflow:hidden;aspect-ratio:9/19;display:flex;flex-direction:column;font-size:12px;line-height:1.3}
.island{width:84px;height:24px;background:#0E1015;border-radius:999px;margin:8px auto 6px}
.sc{padding:8px 16px;flex:1;display:flex;flex-direction:column;gap:10px;min-height:0}
.sc h4{margin:0;font-size:18px;font-weight:800;font-variation-settings:'wdth' 110}
.mute{color:#5d6470}
.caption{font-size:13px;opacity:.85;text-align:center;margin-top:12px}
.tools{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.tools div{background:#F3F1EF;border-radius:12px;padding:10px 6px;text-align:center;font-weight:600}
.tools i{display:block;width:22px;height:22px;border-radius:7px;background:var(--c);margin:0 auto 6px;opacity:.9}
.file{display:flex;gap:10px;align-items:center;padding:8px 0;border-top:1px solid #ECEAE6}
.file i{width:28px;height:34px;border-radius:5px;background:#F4DAD7;border:1.5px solid var(--c)}
.file b{display:block;font-size:12px}
.rec{flex:1;display:grid;place-items:center}
.recbtn{width:120px;height:120px;border-radius:50%;border:6px solid #E7E2DE;display:grid;place-items:center}
.recbtn i{width:74px;height:74px;border-radius:50%;background:var(--c)}
.timer{font-size:34px;font-weight:800;text-align:center;font-variant-numeric:tabular-nums;font-variation-settings:'wdth' 110}
.toggles{display:grid;gap:8px}
.toggles div{display:flex;justify-content:space-between;align-items:center;background:#F4F1EE;border-radius:12px;padding:10px 12px;font-weight:600}
.sw{width:34px;height:20px;border-radius:999px;background:var(--c);position:relative}
.sw::after{content:"";position:absolute;right:2px;top:2px;width:16px;height:16px;border-radius:50%;background:#fff}
.sw.off{background:#CFCAC4}.sw.off::after{right:auto;left:2px}
.canvas{flex:1;border-radius:14px;background:#1E1638;color:#fff;padding:16px;display:flex;flex-direction:column;justify-content:space-between;position:relative;overflow:hidden}
.canvas .blob{position:absolute;width:150px;height:150px;border-radius:50%;background:#FF6B4A;right:-40px;top:-30px}
.canvas .blob2{position:absolute;width:90px;height:90px;border-radius:24px;background:#F5D547;left:-20px;bottom:60px;transform:rotate(18deg)}
.canvas b{position:relative;font-size:30px;line-height:.95;font-weight:900;font-variation-settings:'wdth' 125;letter-spacing:-.02em}
.canvas span{position:relative;font-weight:600}
.strip{display:flex;gap:8px}
.strip i{flex:1;aspect-ratio:3/4;border-radius:8px;background:#EEE9F8;border:1.5px solid #DCD3F2}
.strip i:first-child{border-color:var(--c);border-width:2px}
.prompt{display:flex;justify-content:space-between;align-items:center;background:#F2EFF9;border-radius:999px;padding:8px 8px 8px 14px;font-weight:500}
.prompt i{width:26px;height:26px;border-radius:50%;background:var(--c)}
.art{aspect-ratio:1;border-radius:14px;background:linear-gradient(135deg,#2340C9,#0E1A63);display:grid;place-items:center}
.art svg{width:40%;color:#fff}
.wave{display:flex;align-items:center;gap:3px;height:40px}
.wave i{flex:1;background:#CBD3F4;border-radius:2px}
.wave i.p{background:var(--c)}
.ctrls{display:flex;justify-content:center;align-items:center;gap:28px}
.ctrls i{width:20px;height:20px;border-radius:4px;background:#D9DDEA}
.ctrls .play{width:56px;height:56px;border-radius:50%;background:var(--c)}
.lic{display:flex;justify-content:space-between;align-items:center;border:1.5px solid #E1E4EE;border-radius:12px;padding:10px 12px;font-weight:600}
.lic em{font-style:normal;background:var(--c);color:#fff;border-radius:999px;padding:4px 10px}
.browser{background:#0E1015;border-radius:16px;padding:10px;box-shadow:0 30px 60px -20px rgba(0,0,0,.45)}
.bdots{display:flex;gap:6px;padding:2px 4px 10px}.bdots i{width:9px;height:9px;border-radius:50%;background:#3A3F4B}
.dash{background:#F6F7F5;color:#1A1F2B;border-radius:8px;display:grid;grid-template-columns:96px 1fr;min-height:300px;font-size:11px;overflow:hidden}
.side{background:#fff;border-right:1px solid #E6E8E3;padding:12px 10px;display:flex;flex-direction:column;gap:7px}
.side b{font-size:12px;margin-bottom:6px}
.side span{padding:4px 6px;border-radius:6px}.side span.on{background:var(--c);color:#fff}
.main{padding:12px;display:grid;gap:10px;align-content:start}
.kp{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.kp div{background:#fff;border:1px solid #E6E8E3;border-radius:8px;padding:8px}
.kp b{display:block;font-size:16px}
.cols{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.col{background:#EDEFEB;border-radius:8px;padding:6px;display:grid;gap:6px;align-content:start}
.col>span{font-weight:700}
.trip{background:#fff;border-radius:6px;padding:6px;border-left:0;box-shadow:inset 0 2px 0 var(--c)}
.mapbox{height:70px;border-radius:8px;background:repeating-linear-gradient(0deg,#E4E8E1 0 1px,transparent 1px 18px),repeating-linear-gradient(90deg,#E4E8E1 0 1px,#F1F3EF 1px 18px);position:relative}
.mapbox i{position:absolute;width:10px;height:10px;border-radius:50%;background:var(--c);box-shadow:0 0 0 4px rgba(15,107,92,.2)}
/* entrance: one orchestrated moment */
@media (prefers-reduced-motion:no-preference){
.chero .inner>*{animation:rise .7s cubic-bezier(.2,.7,.2,1) both}
.chero .inner>.mock{animation-delay:.12s}
.home .app{animation:pop .5s cubic-bezier(.2,.8,.3,1.2) both}
.home .app:nth-child(2){animation-delay:.06s}.home .app:nth-child(3){animation-delay:.12s}.home .app:nth-child(4){animation-delay:.18s}.home .app:nth-child(5){animation-delay:.24s}
}
@keyframes rise{from{opacity:0;translate:0 18px}to{opacity:1;translate:none}}
@keyframes pop{from{opacity:0;scale:.85}to{opacity:1;scale:1}}
.ihero h1{max-width:13ch}
.company{padding:clamp(64px,8vw,104px) 0 0}
.cohead{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:clamp(20px,4vw,64px);align-items:end;margin-bottom:40px}
@media (max-width:820px){.cohead{grid-template-columns:1fr}}
.cohead h2{font-size:clamp(34px,4.6vw,60px);line-height:.98;letter-spacing:-.03em;font-weight:850;font-variation-settings:'wdth' 120;margin:0}
.cohead p{margin:0;color:var(--muted);max-width:52ch}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:0;border-top:2px solid var(--ink);margin-bottom:48px}
.facts div{padding:20px 20px 22px 0}
.facts strong{display:block;font-size:clamp(32px,3.8vw,48px);line-height:1;font-weight:800;font-variation-settings:'wdth' 118;letter-spacing:-.03em}
.facts span{color:var(--muted);font-size:16px}
.svc{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px}
.svc>div{background:var(--paper2);border:1px solid var(--rule);border-radius:20px;padding:24px}
.svc h3{margin:0 0 8px;font-size:21px;line-height:1.25;font-weight:750}
.svc p{margin:0;color:var(--muted);font-size:17px}
.svc .ai{grid-column:1/-1;background:var(--ink);color:var(--paper);border-color:var(--ink);padding:clamp(24px,3.5vw,40px)}
.svc .ai h3{font-size:clamp(26px,3vw,36px);font-weight:850;font-variation-settings:'wdth' 118;letter-spacing:-.02em}
.svc .ai p{color:var(--paper);opacity:.85;max-width:64ch;font-size:18px}
.svc .ai ul{display:flex;flex-wrap:wrap;gap:10px;list-style:none;padding:0;margin:20px 0 0}
.svc .ai li{border:1.5px solid currentColor;border-radius:999px;padding:6px 14px;font-size:15px;font-weight:600;opacity:.95}
.live{display:flex;flex-wrap:wrap;gap:10px;margin-top:28px}
.livebtn{display:inline-flex;align-items:center;min-height:46px;padding:10px 20px;border-radius:999px;background:#fff;color:#14171D;text-decoration:none;font-weight:650;font-size:16px}
.livebtn:hover{opacity:.9}
.seelive{font-size:18px;margin:0 0 12px}
.icon.has-img{background:none;overflow:hidden}
.icon.has-img img{width:100%;height:100%;display:block;object-fit:cover}
.crumb .icon.has-img{box-shadow:0 0 0 2px rgba(255,255,255,.55)}
.fan{position:relative;width:min(100%,460px);aspect-ratio:1/1.12;justify-self:center;perspective:1200px}
.fan img{position:absolute;top:50%;left:50%;width:50%;height:auto;border-radius:22px;box-shadow:0 30px 60px -20px rgba(0,0,0,.55),0 0 0 1px rgba(255,255,255,.18);transition:transform .45s cubic-bezier(.2,.8,.2,1)}
.fan .f0{z-index:3;transform:translate(-50%,-50%)}
.fan .f1{z-index:2;transform:translate(-100%,-46%) rotate(-9deg) scale(.88)}
.fan .f2{z-index:1;transform:translate(0%,-46%) rotate(9deg) scale(.88)}
.fan:hover .f1{transform:translate(-112%,-47%) rotate(-12deg) scale(.9)}
.fan:hover .f2{transform:translate(12%,-47%) rotate(12deg) scale(.9)}
.fan:hover .f0{transform:translate(-50%,-53%)}
.gallery{padding:clamp(48px,6vw,80px) 0;border-bottom:1px solid var(--rule)}
.gallery h2{font-size:clamp(28px,3.4vw,40px);line-height:1.05;letter-spacing:-.02em;font-weight:800;font-variation-settings:'wdth' 115;margin:0 0 32px}
.shots{display:grid;grid-template-columns:repeat(var(--n,3),minmax(0,1fr));gap:clamp(16px,3vw,40px)}
@media (max-width:760px){.shots{grid-template-columns:none;grid-auto-flow:column;grid-auto-columns:72%;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:12px}.shots figure{scroll-snap-align:start}}
.shots figure{margin:0}
.shots img{width:100%;height:auto;display:block;border-radius:26px;background:var(--paper2);box-shadow:0 0 0 1px var(--rule),0 24px 40px -24px rgba(20,25,35,.35)}
.shots figcaption{margin-top:14px;font-weight:650;font-size:17px;line-height:1.35}
@media (prefers-reduced-motion:reduce){.fan img{transition:none}}
.single{perspective:1400px;width:100%;max-width:500px;justify-self:center}
.single img{width:100%;height:auto;display:block;border-radius:18px;transform:rotateY(-9deg) rotateX(4deg);box-shadow:0 0 0 1px rgba(255,255,255,.2),-30px 40px 70px -30px rgba(0,0,0,.6);transition:transform .5s cubic-bezier(.2,.8,.2,1)}
.single:hover img{transform:none}
.widefig{margin:0 0 40px}
.widefig:last-child{margin-bottom:0}
.widefig>img{width:100%;height:auto;display:block;border-radius:22px;background:#fff;box-shadow:0 0 0 1px var(--rule),0 24px 40px -24px rgba(20,25,35,.3)}
.widefig figcaption{margin-top:14px;font-weight:650;font-size:17px;line-height:1.35}
.flow{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px}
.flow li{background:#fff;color:#1A1F2B;border-radius:22px;padding:24px;box-shadow:0 0 0 1px var(--rule),0 18px 30px -22px rgba(20,25,35,.3)}
.fi{width:48px;height:48px;border-radius:14px;display:grid;place-items:center;color:#fff;margin-bottom:18px}
.fi svg{width:24px;height:24px}
.flow small{display:block;font-size:14px;color:#5d6470;font-variant-numeric:tabular-nums;letter-spacing:.04em}
.flow h3{margin:4px 0 8px;font-size:21px;font-weight:750}
.flow p{margin:0;color:#4F5663;font-size:16px;line-height:1.55}
@media (prefers-reduced-motion:reduce){.single img{transition:none}}
.chero{overflow-x:clip}
@media (max-width:520px){.bar nav .lnk{display:none}}
/* case study listing */
.cs-head{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:20px 32px;margin-bottom:32px}
.cs-head h2{margin:0 0 8px}
.cs-head p{margin:0;color:var(--muted);max-width:52ch}
.cs-filter{display:flex;flex-wrap:nowrap;max-width:100%;overflow-x:auto;scrollbar-width:none;gap:8px;padding:6px;border-radius:999px;background:var(--paper2);border:1px solid var(--rule)}
.cs-filter button{flex:none;white-space:nowrap;font:inherit;font-size:16px;font-weight:600;min-height:44px;padding:8px 16px;border-radius:999px;border:0;background:transparent;color:var(--ink);cursor:pointer;display:inline-flex;align-items:center;gap:8px;transition:background .2s,color .2s}
.cs-filter button span{font-size:13px;min-width:24px;padding:2px 7px;border-radius:999px;background:rgba(127,127,127,.16);font-variant-numeric:tabular-nums}
.cs-filter button[aria-pressed="true"]{background:var(--ink);color:var(--paper)}
.cs-filter button[aria-pressed="true"] span{background:rgba(255,255,255,.2)}
.cs-filter button:not([aria-pressed="true"]):hover{background:rgba(127,127,127,.12)}
.cs-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px;perspective:1600px}
@media (max-width:860px){.cs-grid{grid-template-columns:1fr}}
.cs-card{--rx:0deg;--ry:0deg;--lift:0px;--ty:0px;position:relative;display:flex;flex-direction:column;text-decoration:none;border-radius:30px;overflow:hidden;background:var(--paper2);border:1px solid var(--rule);
transform:translateY(calc(var(--ty) + var(--lift))) rotateX(var(--rx)) rotateY(var(--ry));
box-shadow:0 1px 0 rgba(255,255,255,.5) inset,0 18px 36px -22px rgba(20,25,35,.35);
transition:transform .5s cubic-bezier(.2,.8,.2,1),box-shadow .35s ease,opacity .5s ease,border-color .3s}
.cs-card::after{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;background:radial-gradient(500px circle at var(--mx,50%) var(--my,0%),rgba(255,255,255,.22),transparent 60%);opacity:0;transition:opacity .3s}
.cs-card:hover,.cs-card:focus-visible{--lift:-8px;border-color:color-mix(in srgb,var(--c) 40%,var(--rule));box-shadow:0 1px 0 rgba(255,255,255,.5) inset,0 40px 60px -28px color-mix(in srgb,var(--c) 55%,rgba(20,25,35,.6))}
.cs-card:hover::after{opacity:1}
.cs-card:active{--lift:-2px;transition-duration:.12s}
.js .cs-card{--ty:36px;opacity:0;transition-delay:var(--d,0ms)}
.js .cs-card.in{--ty:0px;opacity:1}
.js .cs-card.in:hover{transition-delay:0ms}
.cs-card.out{opacity:0!important;--ty:16px;transition-delay:0ms}
.cs-media{position:relative;height:300px;overflow:hidden;background:radial-gradient(120% 90% at 20% 0%,rgba(255,255,255,.22),transparent 55%),var(--c)}
.cs-media::before{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.16) 1px,transparent 1px);background-size:18px 18px;mask-image:linear-gradient(to bottom,#000,transparent 80%);-webkit-mask-image:linear-gradient(to bottom,#000,transparent 80%)}
.cs-ic{position:absolute;top:20px;left:20px;width:56px;border-radius:15px;z-index:5;box-shadow:0 10px 24px -8px rgba(0,0,0,.45),0 0 0 1.5px rgba(255,255,255,.35);background:rgba(255,255,255,.16)}
.cs-ic svg{width:50%;height:50%}
.cs-media img{position:absolute;display:block;transition:transform .6s cubic-bezier(.2,.8,.2,1)}
.cs-media .p{width:27%;height:auto;bottom:-46%;border-radius:16px;box-shadow:0 24px 40px -14px rgba(0,0,0,.55),0 0 0 1px rgba(255,255,255,.15)}
.cs-media .p0{left:36.5%;z-index:3;transform:translateY(-8%)}
.cs-media .p1{left:14%;z-index:2;transform:translateY(6%) rotate(-9deg)}
.cs-media .p2{left:59%;z-index:1;transform:translateY(6%) rotate(9deg)}
.cs-card:hover .p0{transform:translateY(-20%)}
.cs-card:hover .p1{transform:translate(-10%,-2%) rotate(-13deg)}
.cs-card:hover .p2{transform:translate(10%,-2%) rotate(13deg)}
.cs-media .w{width:94%;height:auto;right:-12%;top:96px;border-radius:16px;transform:rotate(-5deg);box-shadow:0 30px 50px -16px rgba(0,0,0,.55),0 0 0 1px rgba(255,255,255,.18)}
.cs-card:hover .w{transform:translateY(-18px) rotate(-2deg)}
.cs-body{position:relative;z-index:1;background:var(--paper2);padding:26px 28px 28px;display:flex;flex-direction:column;gap:10px;flex:1}
.cs-cat{font-size:15px;font-weight:600;color:var(--muted)}
.cs-body h3{margin:0;font-size:clamp(26px,2.6vw,34px);line-height:1.05;letter-spacing:-.02em;font-weight:850;font-variation-settings:'wdth' 118}
.cs-body p{margin:0;color:var(--muted);max-width:52ch}
.cs-stats{display:flex;flex-wrap:wrap;gap:8px;list-style:none;margin:6px 0 0;padding:0}
.cs-stats li{font-size:15px;padding:6px 12px;border-radius:999px;background:color-mix(in srgb,var(--c) 10%,transparent);border:1px solid color-mix(in srgb,var(--c) 25%,var(--rule))}
.cs-stats b{font-weight:800}
.cs-go{margin-top:auto;padding-top:14px;display:inline-flex;align-items:center;gap:12px;font-weight:700;font-size:16px}
.cs-go i{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;border:1.5px solid var(--ink);transition:background .25s,color .25s,border-color .25s,transform .25s}
.cs-go svg{width:16px;height:16px}
.cs-card:hover .cs-go i{background:var(--c);border-color:var(--c);color:#fff;transform:translateX(4px)}
@media (min-width:861px){.cs-card.cs-feat:not(.solo){grid-column:1/-1;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr)}
.cs-card.cs-feat:not(.solo) .cs-media{order:2;height:auto;min-height:400px}
.cs-card.cs-feat:not(.solo) .cs-body{padding:40px;justify-content:center}
.cs-card.cs-feat:not(.solo) .w{width:86%;right:-6%;top:64px;bottom:auto;transform:rotate(-4deg)}
.cs-card.cs-feat:not(.solo):hover .w{transform:translateY(-14px) rotate(-2deg)}
.cs-card.cs-feat:not(.solo) h3{font-size:clamp(34px,4vw,52px)}}
@media (max-width:600px){.cs-media{height:240px}.cs-body{padding:22px}.cs-filter{flex-wrap:wrap;overflow:visible;background:none;border:0;padding:0}.cs-filter button{padding:8px 12px;font-size:15px;border:1px solid var(--rule);background:var(--paper2)}}
@media (prefers-reduced-motion:reduce){.cs-card,.cs-media img,.cs-go i{transition:none}.js .cs-card{opacity:1;--ty:0px}}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
/* AI tool badges */
.ai-tag{display:inline-flex;align-items:center;gap:6px;padding:4px 11px 4px 8px;border-radius:999px;font-size:13px;font-weight:750;letter-spacing:.02em;line-height:1.2;color:#fff;background:linear-gradient(135deg,#6D28D9,#BE185D);vertical-align:middle;white-space:nowrap}
.ai-tag svg{width:14px;height:14px;flex:none}
.on-color .ai-tag{background:#fff;color:#14171D}
.cs-meta{display:flex;align-items:center;flex-wrap:wrap;gap:8px 10px}
.ai-mini{font-style:normal;font-size:11px;font-weight:800;letter-spacing:.04em;padding:2px 7px;border-radius:999px;color:#fff;background:linear-gradient(135deg,#6D28D9,#BE185D);vertical-align:middle;margin-left:6px;position:relative;top:-1px}
.crumb .tags{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
/* 3D niche label */
.niche{display:inline-flex;align-items:center;padding:5px 12px 6px;border-radius:10px;font-size:13px;font-weight:800;letter-spacing:.03em;text-transform:uppercase;line-height:1.15;color:#fff;white-space:nowrap;
background:linear-gradient(180deg,color-mix(in srgb,var(--c) 78%,#fff),var(--c) 55%,color-mix(in srgb,var(--c) 88%,#000));
box-shadow:inset 0 1px 0 rgba(255,255,255,.45),inset 0 -2px 0 rgba(0,0,0,.18),0 3px 0 color-mix(in srgb,var(--c) 55%,#000),0 8px 14px -6px color-mix(in srgb,var(--c) 70%,rgba(0,0,0,.5));
text-shadow:0 1px 0 rgba(0,0,0,.25);transform:translateY(-1px);transition:transform .2s ease,box-shadow .2s ease}
.cs-card:hover .niche{transform:translateY(-3px);box-shadow:inset 0 1px 0 rgba(255,255,255,.45),inset 0 -2px 0 rgba(0,0,0,.18),0 5px 0 color-mix(in srgb,var(--c) 55%,#000),0 12px 18px -6px color-mix(in srgb,var(--c) 70%,rgba(0,0,0,.5))}
.on-color .niche{color:#14171D;text-shadow:none;background:linear-gradient(180deg,#fff,#E9ECEF);box-shadow:inset 0 1px 0 #fff,inset 0 -2px 0 rgba(0,0,0,.08),0 3px 0 rgba(0,0,0,.28),0 8px 14px -6px rgba(0,0,0,.45)}
@media (prefers-reduced-motion:reduce){.niche{transition:none}}
.demo-tag{display:inline-flex;align-items:center;padding:3px 10px;border-radius:999px;font-size:12px;font-weight:700;letter-spacing:.02em;border:1.5px dashed currentColor;color:var(--muted);white-space:nowrap}
.on-color .demo-tag{color:#fff}
/* scroll progress */
.fx-bar{position:fixed;left:0;top:0;height:3px;width:100%;z-index:60;transform-origin:0 50%;transform:scaleX(0);background:linear-gradient(90deg,#6D28D9,#BE185D,#F59E0B);pointer-events:none}
/* rise into view */
.fx .rise{opacity:0;translate:0 36px;transition:opacity .9s cubic-bezier(.2,.7,.2,1),translate .9s cubic-bezier(.2,.7,.2,1)}
.fx .rise.risen{opacity:1;translate:none}
.fx .svc>div.rise:nth-child(2),.fx .steps li.rise:nth-child(2),.fx .feat>div.rise:nth-child(2),.fx .hard>div.rise:nth-child(2){transition-delay:.08s}
.fx .svc>div.rise:nth-child(3),.fx .steps li.rise:nth-child(3),.fx .feat>div.rise:nth-child(3),.fx .hard>div.rise:nth-child(3){transition-delay:.16s}
.fx .svc>div.rise:nth-child(4),.fx .steps li.rise:nth-child(4),.fx .feat>div.rise:nth-child(4),.fx .hard>div.rise:nth-child(4){transition-delay:.24s}
.fx .svc>div.rise:nth-child(n+5),.fx .feat>div.rise:nth-child(n+5){transition-delay:.32s}
[data-words] .w{transition:opacity .25s linear}
/* hero: metallic title and floating 3D glass objects */
.ihero{position:relative}
.ihero>*:not(.fx-stage){position:relative;z-index:1}
.ihero h1{background:linear-gradient(180deg,var(--ink) 38%,color-mix(in srgb,var(--ink) 45%,#7C3AED));-webkit-background-clip:text;background-clip:text;color:transparent;transform-origin:20% 50%;will-change:transform}
.fx-stage{position:absolute;inset:0;pointer-events:none;perspective:1000px;z-index:0}
.fx-obj{position:absolute;transform-style:preserve-3d;will-change:transform}
.bob{animation:bob 7s ease-in-out infinite;transform-style:preserve-3d}.b2{animation-duration:9s;animation-delay:-2s}.b3{animation-duration:11s;animation-delay:-4s}.b4{animation-duration:8s;animation-delay:-1s}
@keyframes bob{0%,100%{translate:0 0;rotate:0deg}50%{translate:0 -16px;rotate:6deg}}
.o1{right:5%;top:8%}.o2{right:27%;top:50%}.o3{right:1%;top:58%}.o4{right:31%;top:4%}.o5{right:19%;top:33%}
.orb{display:block;width:150px;height:150px;border-radius:50%;
background:radial-gradient(circle at 32% 26%,rgba(255,255,255,.95) 0 5%,rgba(255,255,255,.35) 11%,transparent 30%),radial-gradient(circle at 72% 78%,rgba(244,114,182,.85),transparent 50%),radial-gradient(circle at 45% 45%,#8B5CF6,#3B0764 75%);
box-shadow:inset -14px -20px 34px rgba(0,0,0,.35),inset 12px 12px 30px rgba(255,255,255,.25),0 34px 60px -22px rgba(109,40,217,.65)}
.orb.sm{width:52px;height:52px}
.cube{--s:92px;width:var(--s);height:var(--s);position:relative;transform-style:preserve-3d;animation:spin 16s linear infinite}
.cube i{position:absolute;inset:0;border-radius:14px;border:1.5px solid rgba(255,255,255,.6);background:linear-gradient(135deg,rgba(167,139,250,.55),rgba(236,72,153,.3));box-shadow:inset 0 0 22px rgba(255,255,255,.35)}
.cube i:nth-child(1){transform:translateZ(calc(var(--s)/2))}.cube i:nth-child(2){transform:rotateY(180deg) translateZ(calc(var(--s)/2))}
.cube i:nth-child(3){transform:rotateY(90deg) translateZ(calc(var(--s)/2))}.cube i:nth-child(4){transform:rotateY(-90deg) translateZ(calc(var(--s)/2))}
.cube i:nth-child(5){transform:rotateX(90deg) translateZ(calc(var(--s)/2))}.cube i:nth-child(6){transform:rotateX(-90deg) translateZ(calc(var(--s)/2))}
@keyframes spin{from{transform:rotateX(-22deg) rotateY(0deg)}to{transform:rotateX(-22deg) rotateY(360deg)}}
.ring{display:block;width:140px;height:140px;border-radius:50%;transform:rotateX(64deg) rotateZ(20deg);
background:conic-gradient(from 90deg,#F59E0B,#EC4899,#8B5CF6,#3B82F6,#F59E0B);-webkit-mask:radial-gradient(circle,transparent 46%,#000 47.5%);mask:radial-gradient(circle,transparent 46%,#000 47.5%);filter:drop-shadow(0 20px 18px rgba(109,40,217,.45))}
.pill{display:block;width:120px;height:44px;border-radius:999px;transform:rotate(-24deg);
background:linear-gradient(180deg,rgba(255,255,255,.85),rgba(255,255,255,0) 45%),linear-gradient(90deg,#F59E0B,#EC4899);box-shadow:inset 0 -6px 12px rgba(0,0,0,.18),0 20px 30px -14px rgba(236,72,153,.6)}
main{overflow-x:clip}
@media (max-width:900px){.o1{right:-2%;top:-1%;scale:.42;transform-origin:100% 0}.o5{right:30%;top:-1%;scale:.6}.o2,.o3,.o4{display:none}.ihero h1{padding-top:44px}}
/* icons follow the cursor in 3D */
.home{transform-style:preserve-3d;will-change:transform}
.home .app{transform-style:preserve-3d}
.home .icon{transform:translateZ(26px);box-shadow:0 18px 30px -18px color-mix(in srgb,var(--c) 80%,transparent)}
/* tilted screen wall that slides with scroll */
.fx-wall{overflow:hidden;padding:56px 0 24px;perspective:1600px;-webkit-mask:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);mask:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.fx-plane{transform:rotateX(18deg) rotateZ(-4deg) scale(1.06);transform-style:preserve-3d}
.fx-row{display:flex;gap:18px;width:max-content;margin-bottom:18px;will-change:transform}
.fx-row img{height:200px;width:auto;border-radius:16px;background:#fff;box-shadow:0 0 0 1px var(--rule),0 24px 40px -22px rgba(20,25,35,.45)}
.fx-row[data-dir="1"]{transform:translate3d(-30%,0,0)}
@media (max-width:700px){.fx-row img{height:130px;border-radius:12px}.fx-row{gap:12px;margin-bottom:12px}}
/* AI spotlight: cards that pin and stack */
.spot{padding-top:88px}
.spot-head{max-width:720px;margin-bottom:36px}
.spot-head h2{font-size:clamp(34px,5vw,64px);line-height:.98;letter-spacing:-.03em;font-weight:850;font-variation-settings:'wdth' 120;margin:16px 0 14px}
.spot-head p{margin:0;color:var(--muted);max-width:56ch}
.stack{display:grid;gap:44px;padding-bottom:6vh}
.sc{position:sticky;top:calc(84px + var(--i)*26px);display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:clamp(20px,3vw,44px);align-items:center;min-height:440px;padding:clamp(24px,3.6vw,44px);border-radius:32px;color:#fff;transform-origin:50% 0;will-change:transform,filter;
background:radial-gradient(90% 120% at 100% 0%,color-mix(in srgb,var(--c) 75%,transparent),transparent 62%),linear-gradient(160deg,color-mix(in srgb,var(--c) 40%,#0B0D12),#0B0D12 70%);
box-shadow:0 -1px 0 rgba(255,255,255,.12) inset,0 40px 80px -40px rgba(10,12,20,.7)}
.sc-n{display:block;font-size:clamp(56px,7vw,96px);line-height:.85;font-weight:900;font-variation-settings:'wdth' 125;letter-spacing:-.04em;background:linear-gradient(180deg,#fff,rgba(255,255,255,.25));-webkit-background-clip:text;background-clip:text;color:transparent;margin-bottom:14px}
.sc h3{font-size:clamp(30px,3.6vw,48px);line-height:1;letter-spacing:-.025em;font-weight:850;font-variation-settings:'wdth' 118;margin:14px 0 12px}
.sc p{margin:0;color:rgba(255,255,255,.8);max-width:46ch}
.sc-stats{list-style:none;padding:0;margin:20px 0 24px;display:flex;flex-wrap:wrap;gap:8px}
.sc-stats li{font-size:14px;padding:6px 12px;border-radius:999px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18)}
.sc-stats b{margin-right:5px}
.sc .btn{background:#fff;color:#14171D}
.sc .ghost{border-color:rgba(255,255,255,.7);color:#fff}.sc .ghost:hover{background:#fff;color:#14171D}
.sc .niche{box-shadow:inset 0 1px 0 rgba(255,255,255,.45),inset 0 -2px 0 rgba(0,0,0,.18),0 3px 0 rgba(0,0,0,.45)}
.sc-vis{position:relative;height:100%;min-height:340px;border-radius:22px;overflow:hidden;background:rgba(255,255,255,.06);box-shadow:inset 0 0 0 1px rgba(255,255,255,.12)}
.sv-img{position:absolute;left:8%;top:12%;width:110%;max-width:none;height:auto;border-radius:16px;transform:rotate(-4deg);box-shadow:0 30px 60px -20px rgba(0,0,0,.7)}
.sv-fan img{position:absolute;bottom:-28%;width:34%;height:auto;border-radius:16px;box-shadow:0 30px 50px -18px rgba(0,0,0,.7)}
.sv-fan img:nth-child(1){left:33%;z-index:3;transform:translateY(-12%)}.sv-fan img:nth-child(2){left:6%;transform:rotate(-10deg)}.sv-fan img:nth-child(3){left:60%;transform:rotate(10deg)}
.sv-mock{position:absolute;left:7%;top:12%;width:540px;transform:scale(.82) rotate(-3deg);transform-origin:top left}
.sv-mock .browser{box-shadow:0 30px 60px -20px rgba(0,0,0,.7)}
@media (max-width:860px){.sc{grid-template-columns:1fr;min-height:0;top:calc(70px + var(--i)*18px)}.sc-vis{min-height:220px}.sv-mock{transform:scale(.55) rotate(-3deg)}.sc-n{margin-bottom:6px}}
/* tap feedback */
.fx-rhost{overflow:hidden;isolation:isolate}
.fx-ripple{position:absolute;border-radius:50%;pointer-events:none;z-index:6;background:radial-gradient(circle,rgba(255,255,255,.75),color-mix(in srgb,var(--c,#BE185D) 45%,transparent) 42%,transparent 70%);transform:scale(0);opacity:1;animation:fxRipple .65s cubic-bezier(.2,.7,.2,1) forwards}
@keyframes fxRipple{to{transform:scale(1);opacity:0}}
.cs-card:active,.app:active .icon,.sc:active{scale:.97;transition:scale .08s}
.btn:active,.ghost:active,.livebtn:active,.meet-btn:active,.cs-filter button:active{scale:.95}
.fx-chosen.cs-card,.fx-chosen .icon,.fx-chosen.btn{outline:3px solid color-mix(in srgb,var(--c,#7C3AED) 70%,#fff);outline-offset:4px;animation:fxPick .45s ease}
@keyframes fxPick{0%{scale:1}35%{scale:.96}100%{scale:1.01}}
.fx-curtain{position:fixed;inset:0;z-index:200;display:grid;place-items:center;align-content:center;gap:22px;background:radial-gradient(120% 90% at 50% 120%,color-mix(in srgb,var(--fc) 60%,#fff 0%),var(--fc) 60%);color:#fff;clip-path:circle(0% at 50% 100%);transition:clip-path .46s cubic-bezier(.7,0,.2,1)}
.fx-curtain.on{clip-path:circle(150% at 50% 100%)}
.fx-cname{font-size:clamp(34px,6vw,84px);font-weight:850;font-variation-settings:'wdth' 120;letter-spacing:-.03em;opacity:0;translate:0 20px;transition:opacity .3s .15s,translate .3s .15s}
.fx-curtain.on .fx-cname{opacity:1;translate:none}
.fx-load{display:block;width:120px;height:3px;border-radius:3px;background:rgba(255,255,255,.25);overflow:hidden;position:relative}
.fx-load::after{content:"";position:absolute;inset:0;background:#fff;transform-origin:0 50%;animation:fxLoad .9s ease-in-out infinite}
@keyframes fxLoad{0%{transform:scaleX(0)}60%{transform:scaleX(1)}100%{transform:scaleX(1);opacity:0}}
html.fx-arrive::after{content:"";position:fixed;inset:0;z-index:200;background:var(--fc);pointer-events:none;animation:fxArrive .6s cubic-bezier(.7,0,.2,1) forwards}
@keyframes fxArrive{from{clip-path:inset(0 0 0 0)}to{clip-path:inset(0 0 100% 0)}}
/* Meet our AI: full-screen 3D mascot */
.meet{display:block;width:100%;position:relative;height:100vh;height:100svh;min-height:640px;margin-top:72px;background:#000;color:#fff;overflow:hidden}
.meet-stage{position:absolute;inset:0;background:#000 url(/assets/mascot-poster.webp) 50% 100%/cover no-repeat}
.meet-stage canvas{position:absolute;inset:0;width:100%;height:100%;display:block;opacity:0;transition:opacity 1.2s ease}
.meet.live .meet-stage canvas{opacity:1}
.meet-stage::after{content:"";position:absolute;left:0;right:0;bottom:0;height:22%;background:linear-gradient(transparent,#000);pointer-events:none}
.meet-ui{position:relative;z-index:1;width:100%;height:100%;display:flex;flex-direction:column;justify-content:space-between;padding:clamp(24px,4vw,52px);pointer-events:none;font-family:"Space Mono",ui-monospace,monospace}
.meet-ui a{pointer-events:auto}
.meet-tag{align-self:flex-start;padding:7px 14px;border-radius:999px;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.07);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:rgba(255,255,255,.75)}
.meet-row{display:flex;justify-content:space-between;align-items:flex-end;gap:28px}
.meet h2,.meet .big{font-family:inherit;font-weight:400;font-size:clamp(40px,7.4vw,100px);line-height:.95;letter-spacing:-.03em;margin:0;color:#fff}
.meet .r .big{text-align:right}
.meet .l p{max-width:390px;margin:20px 0 24px;font-size:14px;line-height:1.7;color:rgba(255,255,255,.62)}
.meet-btn{display:inline-flex;align-items:center;min-height:48px;padding:0 24px;border-radius:999px;background:#fff;color:#000;font-weight:700;font-size:14px;text-decoration:none;transition:transform .2s ease,background .2s ease}
.meet-btn:hover{background:#e6e6ea;transform:scale(1.03)}
.meet.v2 .meet-stage{background-image:url(/assets/mascot-v2-poster.webp)}
.meet-ver{position:absolute;top:clamp(24px,4vw,52px);right:clamp(24px,4vw,52px);display:flex;gap:4px;padding:4px;border-radius:999px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);pointer-events:auto}
.meet-ver button{font:inherit;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:rgba(255,255,255,.7);background:none;border:0;border-radius:999px;padding:8px 14px;cursor:pointer}
.meet-ver button[aria-pressed="true"]{background:#fff;color:#000}
.meet-hint{position:absolute;left:50%;bottom:18px;transform:translateX(-50%);font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:rgba(255,255,255,.38)}
@media (max-width:760px){.meet{height:auto;min-height:0}.meet-stage{position:relative;inset:auto;width:100%;height:68svh;min-height:420px;background-size:cover}
.meet-ui{position:static;height:auto;padding:0 20px 44px;margin-top:-56px}.meet-tag{position:absolute;top:20px;left:20px;z-index:2}.meet-ver{top:16px;right:16px}.meet-row{position:relative;z-index:1;flex-direction:column;align-items:flex-start;gap:18px}.meet .r{display:none}.meet-hint{display:none}}
@media (prefers-reduced-motion:reduce){.bob,.cube{animation:none}.sc{position:relative;top:auto}}
/* results panel */
.tally{position:relative;overflow:hidden;border:0;border-radius:28px;gap:0;color:#fff;
background:radial-gradient(90% 140% at 0% 0%,rgba(124,58,237,.45),transparent 55%),radial-gradient(80% 140% at 100% 100%,rgba(190,24,93,.4),transparent 55%),#14171F;
box-shadow:0 30px 60px -30px rgba(20,25,35,.55),inset 0 0 0 1px rgba(255,255,255,.08)}
.tally::before{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.09) 1px,transparent 1px);background-size:20px 20px;pointer-events:none}
.tally div{position:relative;padding:32px 32px 34px;border-right:1px solid rgba(255,255,255,.1)}
.tally div:last-child{border-right:0}
.tally strong{font-size:clamp(44px,5.4vw,72px);margin-top:16px;background:linear-gradient(180deg,#fff 30%,#D9C6FF);-webkit-background-clip:text;background-clip:text;color:transparent;font-variant-numeric:tabular-nums}
.tally span{display:block;margin-top:8px;color:rgba(255,255,255,.75);font-size:17px}
.ti{display:grid;place-items:center;width:46px;height:46px;border-radius:14px;color:#fff;background:linear-gradient(135deg,#6D28D9,#BE185D);box-shadow:inset 0 1px 0 rgba(255,255,255,.3),0 10px 20px -8px rgba(190,24,93,.7)}
.ti svg{width:22px;height:22px}
.stars{display:block;position:relative;width:110px;height:20px;margin-top:12px;background:linear-gradient(90deg,rgba(255,255,255,.22) 0 100%);-webkit-mask:var(--st);mask:var(--st);
--st:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 110 20'%3E%3Cg fill='%23000'%3E%3Cpath id='s' d='M10 1.5l2.6 5.3 5.8.8-4.2 4.1 1 5.8L10 14.8l-5.2 2.7 1-5.8L1.6 7.6l5.8-.8z'/%3E%3Cuse href='%23s' x='22'/%3E%3Cuse href='%23s' x='44'/%3E%3Cuse href='%23s' x='66'/%3E%3Cuse href='%23s' x='88'/%3E%3C/g%3E%3C/svg%3E") 0 0/110px 20px no-repeat}
.stars b{position:absolute;inset:0 auto 0 0;background:#FBBF24}
@media (max-width:700px){.tally div{border-right:0;border-bottom:1px solid rgba(255,255,255,.1);padding:26px 24px}.tally div:last-child{border-bottom:0}}
/* compact case study grid */
.cs-grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
@media (max-width:1060px){.cs-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:680px){.cs-grid{grid-template-columns:1fr}}
.cs-card{border-radius:22px}
.cs-media{height:200px}
.cs-ic{top:14px;left:14px;width:44px;border-radius:12px}
.cs-media .p{width:30%;border-radius:12px;bottom:-62%}
.cs-media .w{width:96%;right:-14%;top:58px;border-radius:12px}
.cs-media .cm{position:absolute;width:520px;left:22%;top:40px;transform:scale(.6) rotate(-4deg);transform-origin:top left;transition:transform .6s cubic-bezier(.2,.8,.2,1)}
.cs-card:hover .cm{transform:translateY(-10px) scale(.6) rotate(-2deg)}
.cs-media .cm .browser{box-shadow:0 30px 50px -16px rgba(0,0,0,.55),0 0 0 1px rgba(255,255,255,.18)}
.cs-body{padding:20px 22px 22px;gap:8px}
.cs-body h3{font-size:clamp(22px,1.9vw,26px)}
.cs-body p{font-size:16px;line-height:1.5;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.cs-meta{gap:6px 8px;min-height:24px}
.cs-meta .niche{font-size:11px;padding:4px 9px 5px;border-radius:8px}
.cs-meta .ai-tag{font-size:11.5px;padding:3px 9px 3px 7px}.cs-meta .ai-tag svg{width:12px;height:12px}
.cs-cat{font-size:14px}
.cs-stats{gap:6px;margin-top:4px}
.cs-stats li{font-size:13px;padding:4px 10px}
.cs-go{font-size:15px;padding-top:12px}
.cs-go i{width:34px;height:34px}
@media (max-width:600px){.cs-media{height:190px}}
@media (min-width:1061px){.cs-card.cs-top:not(.solo){grid-column:1/-1;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.25fr)}
.cs-card.cs-top:not(.solo) .cs-media{order:2;height:auto;min-height:300px}
.cs-card.cs-top:not(.solo) .cs-body{padding:32px 36px;justify-content:center}
.cs-card.cs-top:not(.solo) h3{font-size:34px}
.cs-card.cs-top:not(.solo) .w{width:88%;right:-8%;top:52px}
.cs-card.cs-top:not(.solo) .cs-go{margin-top:8px}}
/* GhostAI illustrative call */
.call{position:relative;background:#1B1F27;border-radius:8px;min-height:300px;padding:10px;overflow:hidden}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.tiles i{background:#2B313D;border-radius:8px;height:136px;display:grid;place-items:center}
.tiles i::before{content:"";width:44px;height:44px;border-radius:50%;background:#3A4252}
.ghostp{position:absolute;right:12px;bottom:12px;width:64%;background:rgba(255,255,255,.95);color:#1A1F2B;border-radius:12px;padding:12px 14px;font-size:12px;line-height:1.45;box-shadow:0 18px 40px -12px rgba(0,0,0,.6)}
.ghostp .gq{display:block;color:#5d6470;margin-bottom:6px}
.ghostp b{display:block;color:var(--c);font-size:12px;margin-bottom:2px}
.ghostp p{margin:0 0 8px}
.cs-media .cm .browser{padding:8px;border-radius:14px}.cs-media .cm .call{min-height:0}
.gk{display:flex;gap:6px}
/* GenZpark illustrative workspace */
.gz{background:#0B0D10;color:#E8EBE4;border-radius:8px;display:grid;grid-template-columns:92px 1fr;min-height:300px;font-size:11px;overflow:hidden}
.gz .side{background:#12151A;border-right:1px solid #22262E;color:#C9CEC4}
.gz .side b{color:#D4F85A}
.gz .side span.on{background:#D4F85A;color:#14171D}
.gz .main{padding:12px}
.gzp{display:flex;justify-content:space-between;align-items:center;background:#1A1E25;border:1px solid #2A2F38;border-radius:999px;padding:6px 6px 6px 12px}
.gzp em{font-style:normal;background:#D4F85A;color:#14171D;border-radius:999px;padding:4px 10px;font-weight:700}
.gzg{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.gzg i{aspect-ratio:1;border-radius:8px;background:linear-gradient(135deg,#2E4A12,#0E2A33)}
.gzg i:nth-child(2){background:linear-gradient(135deg,#D4F85A,#3F8F5A)}.gzg i:nth-child(4){background:linear-gradient(135deg,#1B3B5A,#58C4A8)}.gzg i:nth-child(6){background:linear-gradient(135deg,#3F6212,#D4F85A)}
.gzc{display:flex;justify-content:space-between;color:#9AA196}.gk span{background:#EEF0F8;border-radius:999px;padding:3px 9px;font-weight:600}
"""

GLYPH = {
 "transwayz":'<rect x="7" y="2" width="10" height="20" rx="5"/><path d="M9.6 7.6h4.8M10.3 7.6 9.3 17.6M13.7 7.6l1 10M12 10v.9M12 12.6v.9M12 15.2v.9"/>',
 "beatstars":'<path d="M4 10v4M8 6.5v11M12 3.5v17M16 7.5v9M20 10v4"/>',
 "pdf-converter":'<path d="M6 2.5h8.5l4.5 4.5v14.5H6z"/><path d="M14.5 2.5V7H19"/><path d="M9 13h7M9 16.5h5"/>',
 "screen-recorder":'<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="3.6" fill="currentColor"/>',
 "singles-connect":'<path d="M12 20s-7-4.4-7-9.6A3.9 3.9 0 0 1 12 8a3.9 3.9 0 0 1 7 2.4C19 15.6 12 20 12 20z"/><path d="M17.5 3.5c.6-.7 1.9-.5 2.1.5.3 1.2-1.6 2.5-2.1 2.8-.5-.3-2.4-1.6-2.1-2.8.2-1 1.5-1.2 2.1-.5z" fill="currentColor"/>',
 "baridata":'<path d="M3 12.5h4l2-5 4 10 2-5h6"/>',
 "code-claw":'<g fill="currentColor" stroke="none"><ellipse cx="5.6" cy="10.2" rx="1.9" ry="2.4"/><ellipse cx="9.6" cy="5.9" rx="2" ry="2.6"/><ellipse cx="14.4" cy="5.9" rx="2" ry="2.6"/><ellipse cx="18.4" cy="10.2" rx="1.9" ry="2.4"/><path d="M12 11.3c-2.7 0-5.6 3.7-5.6 6.4 0 1.6 1.2 2.4 2.7 2.4 1.2 0 1.9-.6 2.9-.6s1.7.6 2.9.6c1.5 0 2.7-.8 2.7-2.4 0-2.7-2.9-6.4-5.6-6.4z"/></g>',
 "ghostai":'<path d="M6 20.5V10a6 6 0 0 1 12 0v10.5l-2-1.6-2 1.6-2-1.6-2 1.6-2-1.6z"/><circle cx="9.8" cy="10.6" r="1.1" fill="currentColor"/><circle cx="14.2" cy="10.6" r="1.1" fill="currentColor"/>',
 "genzpark":'<rect x="3.5" y="3.5" width="7" height="7" rx="2"/><rect x="13.5" y="3.5" width="7" height="7" rx="2"/><rect x="3.5" y="13.5" width="7" height="7" rx="2"/><path d="M17 13.2l1 2.8 2.8 1-2.8 1-1 2.8-1-2.8-2.8-1 2.8-1z" fill="currentColor"/>',
 "3d-demo":'<path d="M12 2.8 20 7.3v9.4l-8 4.5-8-4.5V7.3z"/><path d="M4 7.3l8 4.6 8-4.6M12 11.9v9.3"/>',
 "poster-maker":'<rect x="4" y="3" width="16" height="18" rx="2"/><circle cx="9.5" cy="8.5" r="1.8"/><path d="M4 17l5-5 4 4 2.5-2.5L20 18"/>',
}
import base64
SPARK='<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.2 6.3 6.3 2.2-6.3 2.2L12 19.5l-2.2-6.3L3.5 11l6.3-2.2z"/><path d="M19 15.5l.9 2.6 2.6.9-2.6.9-.9 2.6-.9-2.6-2.6-.9 2.6-.9z"/></svg>'
def niche_tag(p): return f'<span class="niche">{p["niche"]}</span>' if p.get("niche") else ''
def demo_tag(p): return '<span class="demo-tag">Concept demo</span>' if p.get("demo") else ''
def ai_tag(p): return f'<span class="ai-tag">{SPARK}AI tool</span>' if p.get("ai") else ''
ASSET=lambda path: "/"+path
def data_uri(path):
    return "data:image/webp;base64,"+base64.b64encode(open(path,"rb").read()).decode()
def icon_inner(p):
    if p.get("icon"): return f'<img src="{ASSET(p["icon"])}" alt="" width="256" height="256" loading="lazy">'
    return glyph(p["slug"])
def glyph(slug):
    vb="4.5 1 15 22" if slug=="transwayz" else "0 0 24 24"
    return f'<svg viewBox="{vb}" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{GLYPH[slug]}</svg>'

GZ_DASH='''<div class="gz"><div class="side"><b>GenZpark</b><span>Chat</span><span class="on">Images</span><span>Video</span><span>Docs</span><span>Slides</span><span>Music</span><span>PDF chat</span><span>Design</span></div>
<div class="main"><div class="gzp">Neon city skyline at dusk, poster style<em>Generate</em></div><div class="gzc"><span>Images</span><span>Credit cost shown first</span></div><div class="gzg"><i></i><i></i><i></i><i></i><i></i><i></i></div></div></div>'''
GHOST_CALL='''<div class="call">
<div class="tiles"><i></i><i></i><i></i><i></i></div>
<div class="ghostp"><span class="gq">Question heard: "When can we go live?"</span><b>Suggested answer</b><p>Beta in two weeks, full launch after the security review.</p><div class="gk"><span>Notes</span><span>Action items</span></div></div></div>'''

def mock(p):
    if p.get("hero"):
        src,alt,w,h=p["hero"]
        return f'<div class="mock single"><img src="{ASSET(src)}" alt="{alt}" width="{w}" height="{h}"></div>'
    if p.get("shots"):
        imgs="".join(f'<img class="f{i}" src="{ASSET(src)}" alt="{alt}" width="535" height="1160">' for i,(src,cap,alt) in enumerate(p["shots"][:3]))
        return f'<div class="mock fan">{imgs}</div>'
    k=p["kind"]
    if k=="web":
        return '''<figure class="mock web" style="margin:0"><div class="browser" role="img" aria-label="Illustration of the Transwayz dispatch dashboard"><div class="bdots"><i></i><i></i><i></i></div><div class="dash">
<div class="side"><b>Transwayz</b><span>Dashboard</span><span>Orders</span><span class="on">Trips</span><span>Accounting</span><span>IFTA</span><span>Reports</span></div>
<div class="main"><div class="kp"><div><span>In transit</span><b>24</b></div><div><span>At pickup</span><b>9</b></div><div><span>Delivered today</span><b>31</b></div></div>
<div class="cols"><div class="col"><span>Dispatched</span><div class="trip">Order 4812<br>Dallas to Tulsa</div><div class="trip">Order 4815<br>Reno to Boise</div></div>
<div class="col"><span>In transit</span><div class="trip">Order 4799<br>HOS left 6h 10m</div><div class="trip">Order 4803<br>HOS left 2h 45m</div></div>
<div class="col"><span>Delivered</span><div class="trip">Order 4790<br>POD uploaded</div></div></div>
<div class="mapbox"><i style="left:22%;top:30%"></i><i style="left:58%;top:55%"></i><i style="left:80%;top:22%"></i></div></div></div></div>
<figcaption class="caption">Illustrative interface</figcaption></figure>'''
    if k=="registry":
        pts="10,80 50,70 90,58 130,50 170,40 210,34 250,30 290,27"
        return '''<figure class="mock web" style="margin:0"><div class="browser" role="img" aria-label="Illustration of the Baridata outcomes dashboard"><div class="bdots"><i></i><i></i><i></i></div><div class="dash">
<div class="side"><b>Baridata</b><span class="on">Outcomes</span><span>Surgeries</span><span>Follow-ups</span><span>Patients</span><span>Benchmarks</span><span>Export</span></div>
<div class="main"><div class="kp"><div><span>%TWL 12 mo</span><b>31.4%</b></div><div><span>Diabetes remission</span><b>68%</b></div><div><span>Follow-up rate</span><b>87%</b></div></div>
<div style="background:#fff;border:1px solid #E6E8E3;border-radius:8px;padding:8px"><span style="font-weight:700">Weight loss over time</span>
<svg viewBox="0 0 300 90" style="width:100%;height:auto;display:block;margin-top:4px"><path d="M10 85H290" stroke="#E6E8E3"/><polyline points="'''+pts+'''" fill="none" stroke="var(--c)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
<div class="cols" style="grid-template-columns:1fr 1fr"><div class="col"><span>Due this week</span><div class="trip">Patient 1042<br>6-month review</div><div class="trip">Patient 0987<br>12-month review</div></div>
<div class="col"><span>Missed visits</span><div class="trip">Patient 0911<br>Reminder sent</div></div></div></div></div></div>
<figcaption class="caption">Illustrative interface</figcaption></figure>'''
    if k=="workspace":
        return '''<figure class="mock web" style="margin:0"><div class="browser" role="img" aria-label="Illustration of the GenZpark dashboard generating images from a prompt"><div class="bdots"><i></i><i></i><i></i></div>'''+GZ_DASH+'''</div>
<figcaption class="caption">Illustrative interface</figcaption></figure>'''
    if k=="ghost":
        return '''<figure class="mock web" style="margin:0"><div class="browser" role="img" aria-label="Illustration of GhostAI suggesting an answer during a video call"><div class="bdots"><i></i><i></i><i></i></div>'''+GHOST_CALL+'''</div>
<figcaption class="caption">Illustrative interface</figcaption></figure>'''
    head='<figure class="mock" style="margin:0"><div class="phone" role="img" aria-label="Illustration of the '+p["name"]+' app"><div class="screen"><div class="island"></div><div class="sc">'
    tail='</div></div></div><figcaption class="caption">Illustrative interface</figcaption></figure>'
    if k=="pdf":
        body='''<h4>Tools</h4><div class="tools"><div><i></i>Convert</div><div><i></i>Merge</div><div><i></i>Split</div><div><i></i>Compress</div><div><i></i>Sign</div><div><i></i>Edit</div></div>
<div style="display:flex;justify-content:space-between;align-items:center;margin-top:4px"><b>Recent</b><span class="mute">See all</span></div>
<div class="file"><i></i><div><b>Lease agreement.pdf</b><span class="mute">Signed, 2.1 MB</span></div></div>
<div class="file"><i></i><div><b>Q3 report.pdf</b><span class="mute">From Word, 840 KB</span></div></div>
<div class="file"><i></i><div><b>Receipts merged.pdf</b><span class="mute">12 pages</span></div></div>'''
    elif k=="rec":
        body='''<h4>Record</h4><div class="rec"><div style="display:grid;gap:14px;justify-items:center"><div class="recbtn"><i></i></div><div class="timer">00:42</div></div></div>
<div class="toggles"><div>Face cam<span class="sw"></span></div><div>Microphone<span class="sw"></span></div><div>Live stream<span class="sw off"></span></div></div>'''
    elif k=="poster":
        body='''<div class="prompt">Neon party flyer<i></i></div><div class="canvas"><div class="blob"></div><div class="blob2"></div><b>Friday<br>night<br>lights</b><span>Rooftop, 9 pm</span></div>
<div class="strip"><i></i><i></i><i></i><i></i></div>'''
    else:
        body='''<div class="art">'''+'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 10v4M8 6.5v11M12 3.5v17M16 7.5v9M20 10v4"/></svg>'+'''</div>
<div><b style="font-size:15px">Midnight drive</b><br><span class="mute">Trap, 140 BPM</span></div>
<div class="wave">'''+''.join(f'<i class="{"p" if i<11 else ""}" style="height:{h}%"></i>' for i,h in enumerate([30,55,80,45,90,65,40,70,95,60,35,75,50,85,40,65,30,55,80,45]))+'''</div>
<div class="ctrls"><i></i><span class="play"></span><i></i></div>
<div class="lic">Basic licence<em>Add to cart</em></div>'''
    return head+body+tail

def topbar(home_href, on_color=False):
    return f'''<div class="wrap"><header class="bar"><a class="brand" href="{home_href}"><i>i</i>iApp Technologies</a>
<nav aria-label="Main"><a class="lnk" href="{home_href}">Case studies</a><a class="lnk" href="https://iapptechnologies.com/about">About</a><a class="btn" href="https://iapptechnologies.com/business-enquiry">Start a project</a></nav></header></div>'''

FOOT='''<footer><div class="wrap"><span>© 2012–2026 iApp Technologies LLP</span>
<span><a href="mailto:aziz.k@iapptechnologiesllp.com">aziz.k@iapptechnologiesllp.com</a></span>
<span><a href="tel:+917009592313">+91 70095 92313</a></span>
<span>Offices in the USA, India, Canada and Australia</span></div></footer>'''

def cta():
    return '''<section class="wrap cta"><h2>Have a product that needs to reach millions?</h2>
<div><p>Tell us what you are building. We will come back with a plan, a team and a realistic timeline.</p><div class="links"><a class="btn" href="mailto:aziz.k@iapptechnologiesllp.com">Email us</a><a class="ghost" href="tel:+917009592313">+91 70095 92313</a></div></div></section>'''

FX_JS=r'''/* Cursor and scroll effects for the case studies site. Everything is skipped for reduced motion. */
(function(){
var d=document,root=d.documentElement,W=window;
var reduce=matchMedia("(prefers-reduced-motion: reduce)").matches,fine=matchMedia("(hover: hover) and (pointer: fine)").matches;
root.classList.add("fx");
var clamp=function(v,a,b){return Math.max(a,Math.min(b,v))};
var $$=function(q){return [].slice.call(d.querySelectorAll(q))};

/* scroll progress bar */
var bar=d.createElement("div");bar.className="fx-bar";bar.setAttribute("aria-hidden","true");d.body.appendChild(bar);

/* sections rise into view */
var rise=$$(".list .cs-head,.cohead,.facts,.svc>div,.sec,.gallery,.next,.cta,.spot-head,.tally,.steps li,.feat>div,.hard>div");
rise.forEach(function(e){e.classList.add("rise")});
if(reduce||!("IntersectionObserver" in W)){rise.forEach(function(e){e.classList.add("risen")})}
else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("risen");io.unobserve(e.target)}})},{rootMargin:"0px 0px -8% 0px"});rise.forEach(function(e){io.observe(e)})}

/* paragraphs that light up word by word */
var esc=function(t){return t.replace(/&/g,"&amp;").replace(/</g,"&lt;")};
var words=reduce?[]:$$("[data-words]").map(function(el){var t=el.textContent.trim().split(/\s+/);el.innerHTML=t.map(function(w){return '<span class="w">'+esc(w)+'</span>'}).join(" ");return {el:el,ws:[].slice.call(el.querySelectorAll(".w"))}});

/* click feedback: ripple, press and a page transition so every tap visibly registers */
var TAP="a,button,.cs-card,.app,.sc";
d.addEventListener("pointerdown",function(e){var el=e.target.closest(TAP);if(!el||e.button>0)return;
  var host=el.classList.contains("app")?el.querySelector(".icon"):el;if(!host)return;
  var r=host.getBoundingClientRect(),s=Math.max(r.width,r.height)*2.2,rp=d.createElement("span");rp.className="fx-ripple";
  rp.style.cssText="width:"+s+"px;height:"+s+"px;left:"+(e.clientX-r.left-s/2)+"px;top:"+(e.clientY-r.top-s/2)+"px";
  if(getComputedStyle(host).position==="static")host.style.position="relative";host.classList.add("fx-rhost");host.appendChild(rp);
  setTimeout(function(){rp.remove()},700)},{passive:true});
d.addEventListener("click",function(e){var a=e.target.closest("a[href]");if(!a||e.defaultPrevented||e.button>0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;
  if(a.target==="_blank"||a.hasAttribute("download"))return;var u;try{u=new URL(a.href,location.href)}catch(x){return}
  if(u.origin!==location.origin||(u.pathname===location.pathname&&u.hash))return;
  e.preventDefault();var card=a.closest("[style*='--c']")||a,col=getComputedStyle(card).getPropertyValue("--c").trim()||"#14171D";
  var name=(a.querySelector("h3,b")||{}).textContent||"";name=name.replace(/AI$/,"").trim();
  a.classList.add("fx-chosen");try{sessionStorage.setItem("fxNav",col)}catch(x){}
  if(reduce){location.href=u.href;return}
  var c=d.createElement("div");c.className="fx-curtain";c.style.setProperty("--fc",col);c.innerHTML='<span class="fx-cname"></span><i class="fx-load"></i>';c.firstChild.textContent=name;d.body.appendChild(c);
  requestAnimationFrame(function(){c.classList.add("on")});setTimeout(function(){location.href=u.href},460)});
W.addEventListener("pageshow",function(e){if(e.persisted){$$(".fx-curtain").forEach(function(c){c.remove()});$$(".fx-chosen").forEach(function(a){a.classList.remove("fx-chosen")})}});

var objs=$$(".fx-obj").map(function(e){return {el:e,k:parseFloat(e.getAttribute("data-depth"))||1}});
var h1=d.querySelector(".ihero h1"),home=d.querySelector(".home"),mock=d.querySelector(".chero .mock");
var wall=d.querySelector(".fx-wall"),rows=$$(".fx-row"),cards=$$(".stack .sc");
if(reduce){return}

var tx=0,ty=0,cx=0,cy=0,hx=0,hy=0,hcx=0,hcy=0,sy=W.scrollY,vh=W.innerHeight,raf=0;
function kick(){if(!raf)raf=requestAnimationFrame(frame)}
function frame(){
  raf=0;
  cx+=(tx-cx)*.08;cy+=(ty-cy)*.08;hcx+=(hx-hcx)*.1;hcy+=(hy-hcy)*.1;
  objs.forEach(function(o){var k=o.k;o.el.style.transform="translate3d("+(cx*k*26).toFixed(1)+"px,"+(cy*k*22-sy*k*.18).toFixed(1)+"px,0) rotateX("+(-cy*k*9).toFixed(2)+"deg) rotateY("+(cx*k*12).toFixed(2)+"deg)"});
  if(h1)h1.style.transform="perspective(900px) rotateX("+(-cy*4).toFixed(2)+"deg) rotateY("+(cx*6).toFixed(2)+"deg)";
  if(home)home.style.transform="perspective(1100px) rotateX("+(-hcy*7).toFixed(2)+"deg) rotateY("+(hcx*9).toFixed(2)+"deg)";
  if(mock)mock.style.transform="perspective(1200px) rotateX("+(-cy*6).toFixed(2)+"deg) rotateY("+(cx*8).toFixed(2)+"deg) translateY("+(sy*.06).toFixed(1)+"px)";
  if(Math.abs(tx-cx)+Math.abs(ty-cy)+Math.abs(hx-hcx)+Math.abs(hy-hcy)>.002)kick();
}
function onScroll(){
  sy=W.scrollY;
  var max=root.scrollHeight-vh;bar.style.transform="scaleX("+(max>0?sy/max:0).toFixed(4)+")";
  words.forEach(function(o){var r=o.el.getBoundingClientRect();if(r.bottom<-50||r.top>vh+50)return;
    var p=clamp((vh*.9-r.top)/(vh*.55+r.height*.5),0,1),n=o.ws.length;
    o.ws.forEach(function(w,i){w.style.opacity=(.18+.82*clamp(p*n*1.15-i,0,1)).toFixed(2)})});
  if(wall){var r=wall.getBoundingClientRect();if(r.bottom>0&&r.top<vh){var p=clamp((vh-r.top)/(vh+r.height),0,1);
    rows.forEach(function(row){var dir=+row.getAttribute("data-dir"),extra=Math.max(0,row.scrollWidth/2);var x=dir<0?-p*extra*.55:-(1-p)*extra*.55;row.style.transform="translate3d("+x.toFixed(1)+"px,0,0)"})}}
  for(var i=0;i<cards.length-1;i++){var a=cards[i].getBoundingClientRect(),b=cards[i+1].getBoundingClientRect();
    var t=clamp((a.bottom-b.top)/a.height,0,1);cards[i].style.transform="scale("+(1-.06*t).toFixed(3)+")";cards[i].style.filter="brightness("+(1-.4*t).toFixed(2)+")"}
  kick();
}
W.addEventListener("scroll",onScroll,{passive:true});
W.addEventListener("resize",function(){vh=W.innerHeight;onScroll()});
if(fine){W.addEventListener("pointermove",function(e){tx=e.clientX/W.innerWidth*2-1;ty=e.clientY/vh*2-1;
  if(home){var r=home.getBoundingClientRect();var inside=e.clientX>r.left-80&&e.clientX<r.right+80&&e.clientY>r.top-80&&e.clientY<r.bottom+80;
    hx=inside?clamp((e.clientX-r.left)/r.width*2-1,-1,1):0;hy=inside?clamp((e.clientY-r.top)/r.height*2-1,-1,1):0}
  kick()},{passive:true});
  d.addEventListener("pointerleave",function(){tx=ty=hx=hy=0;kick()})}
onScroll();
})();
'''

TILT='''<script>(function(){
var cards=[].slice.call(document.querySelectorAll(".cs-card"));
var reduce=matchMedia("(prefers-reduced-motion: reduce)").matches;
document.documentElement.classList.add("js");
if(!reduce&&"IntersectionObserver" in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{rootMargin:"0px 0px -8% 0px"});cards.forEach(function(c){io.observe(c)})}else{cards.forEach(function(c){c.classList.add("in")})}
if(!reduce)cards.forEach(function(c){c.addEventListener("pointermove",function(e){if(e.pointerType!=="mouse")return;var r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width,y=(e.clientY-r.top)/r.height;c.style.setProperty("--ry",((x-.5)*4).toFixed(2)+"deg");c.style.setProperty("--rx",((.5-y)*4).toFixed(2)+"deg");c.style.setProperty("--mx",(x*100)+"%");c.style.setProperty("--my",(y*100)+"%")});c.addEventListener("pointerleave",function(){c.style.setProperty("--rx","0deg");c.style.setProperty("--ry","0deg")})});
var btns=[].slice.call(document.querySelectorAll(".cs-filter button"));
btns.forEach(function(b){b.addEventListener("click",function(){var f=b.getAttribute("data-f");btns.forEach(function(x){x.setAttribute("aria-pressed",x===b?"true":"false")});
cards.forEach(function(c,i){var show=f==="all"||(" "+c.getAttribute("data-groups")+" ").indexOf(" "+f+" ")>-1;
if(show){if(c.hidden){c.hidden=false;c.classList.add("out");c.classList.remove("feat-off");void c.offsetWidth;}c.style.setProperty("--d",(i%2)*60+"ms");c.classList.remove("out");c.classList.add("in")}
else if(!c.hidden){c.classList.add("out");setTimeout(function(){if(c.classList.contains("out"))c.hidden=true},reduce?0:260)}
c.classList.toggle("solo",f!=="all")})})});
var nums=[].slice.call(document.querySelectorAll(".tally strong[data-to]"));
if(!reduce&&"IntersectionObserver" in window&&nums.length){var done=false,t=new IntersectionObserver(function(es){if(done||!es.some(function(e){return e.isIntersecting}))return;done=true;t.disconnect();
var t0=performance.now();nums.forEach(function(n){n.dataset.final=n.textContent});
(function step(now){var k=Math.min(1,(now-t0)/1400),e=1-Math.pow(1-k,3);nums.forEach(function(n){var v=parseFloat(n.dataset.to)*e;n.textContent=(k<1?v.toFixed(+n.dataset.dec):n.dataset.final.replace(n.dataset.suf,""))+n.dataset.suf;if(k===1)n.textContent=n.dataset.final});if(k<1)requestAnimationFrame(step)})(t0)},{threshold:.4});t.observe(document.querySelector(".tally"))}
})();</script>'''

WALL_A=["code-claw/features.webp","transwayz/integrations.webp","3d-demo/about.webp","baridata/dashboard.webp","beatstars/web.webp","3d-demo/projects.webp"]
WALL_B=["poster-maker/screen-1.webp","singles-connect/screen-1.webp","pdf-converter/screen-1.webp","3d-demo/hero.webp","screen-recorder/screen-2.webp","beatstars/screen-1.webp","transwayz/dispatch.webp","poster-maker/screen-2.webp","singles-connect/screen-2.webp","code-claw/hero.webp"]
def wall():
    row=lambda L,d: f'<div class="fx-row" data-dir="{d}">'+''.join(f'<img src="/assets/{f}" alt="" loading="lazy" decoding="async">' for f in L+L)+'</div>'
    return f'<section class="fx-wall" aria-hidden="true"><div class="fx-plane">{row(WALL_A,-1)}{row(WALL_B,1)}</div></section>'

def meet():
    return '''<section class="meet" id="meet" aria-labelledby="meet-h"><div class="meet-stage" aria-hidden="true"><canvas></canvas></div>
<div class="meet-ui"><span class="meet-tag">Meet our AI</span>
<div class="meet-row"><div class="l"><h2 id="meet-h"><span data-s="Built to">Built to</span><br><span data-s="Think">Think</span></h2>
<p>We design AI that listens, reasons and acts: agents that run real workflows, assistants that answer from your own data, and apps that get smarter with every user.</p>
<a class="meet-btn" href="mailto:aziz.k@iapptechnologiesllp.com">Talk to our AI team</a></div>
<div class="r"><p class="big" aria-hidden="true"><span data-s="Built by">Built by</span><br><span data-s="iApp">iApp</span></p></div></div>
<span class="meet-hint" aria-hidden="true">Move your cursor</span>
<div class="meet-ver" role="group" aria-label="Choose mascot version"><button type="button" data-v="1">V1 Headset</button><button type="button" data-v="2">V2 Giraffe</button></div></div></section>
<script>(function(){var s=document.getElementById("meet");if(!s)return;var reduce=matchMedia("(prefers-reduced-motion: reduce)").matches;
var CH="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+~|}{[]:;?><";
function scr(el,delay){var t=el.getAttribute("data-s");el.innerHTML="&nbsp;";setTimeout(function(){var p=0,id=setInterval(function(){p+=.5;var o="";for(var i=0;i<t.length;i++){if(t[i]===" "){o+=" ";continue}if(i<p)o+=t[i];else if(i<p+3)o+=CH[Math.random()*CH.length|0]}el.textContent=o||"\u00a0";if(p>=t.length){clearInterval(id);el.textContent=t}},25)},delay)}
var ver="2";try{ver=new URLSearchParams(location.search).get("mascot")||localStorage.getItem("mascotV")||"2"}catch(e){}
if(ver==="2")s.classList.add("v2");
[].forEach.call(s.querySelectorAll(".meet-ver button"),function(b){b.setAttribute("aria-pressed",b.getAttribute("data-v")===ver?"true":"false");
  b.addEventListener("click",function(){try{localStorage.setItem("mascotV",b.getAttribute("data-v"))}catch(e){}var u=new URL(location.href);u.searchParams.set("mascot",b.getAttribute("data-v"));u.hash="meet";location.replace(u.href)})});
var load=function(){import(ver==="2"?"/assets/mascot-v2.js":"/assets/mascot.js").then(function(m){m.mount(s)}).catch(function(){s.classList.add("no-webgl")})};
if(!("IntersectionObserver" in window)){load();return}
var a=new IntersectionObserver(function(e){if(e[0].isIntersecting){a.disconnect();load()}},{rootMargin:"700px 0px"});a.observe(s);
if(!reduce){var b=new IntersectionObserver(function(e){if(e[0].isIntersecting){b.disconnect();[].forEach.call(s.querySelectorAll("[data-s]"),function(el,i){scr(el,150+i*260)})}},{threshold:.35});b.observe(s)}
})();</script>'''

def spot_visual(p):
    if p.get("shots"):
        return '<div class="sv-fan">'+''.join(f'<img src="{ASSET(src)}" alt="" width="535" height="1160" loading="lazy">' for src,cap,alt in p["shots"][:3])+'</div>'
    if p.get("card_img") or p.get("hero"):
        src,alt,w,h=p.get("card_img") or p["hero"]; return f'<img class="sv-img" src="{ASSET(src)}" alt="" width="{w}" height="{h}" loading="lazy">'
    inner=GZ_DASH if p["kind"]=="workspace" else GHOST_CALL
    return f'<div class="sv-mock"><div class="browser"><div class="bdots"><i></i><i></i><i></i></div>{inner}</div></div>'

def spotlight(href):
    ai=[p for p in PROJECTS if p.get("ai")]
    cards=''
    for i,p in enumerate(ai):
        st=''.join(f'<li><b>{v}</b>{l}</li>' for v,l in p["stats"][:2])
        live=f'<a class="ghost" href="{p["links"][0][1]}" target="_blank" rel="noopener">{p["links"][0][0]}</a>' if p.get("links") else ''
        cards+=f'''<article class="sc" style="--c:{p["color"]};--i:{i}"><div class="sc-txt"><span class="sc-n" aria-hidden="true">0{i+1}</span><div class="cs-meta">{niche_tag(p)}{ai_tag(p)}</div>
<h3>{p["name"]}</h3><p>{p["oneliner"]}</p><ul class="sc-stats">{st}</ul><div class="links"><a class="btn" href="{href(p["slug"])}">View case study</a>{live}</div></div>
<div class="sc-vis" aria-hidden="true">{spot_visual(p)}</div></article>'''
    return f'''<section class="wrap spot" aria-labelledby="spot-h"><div class="spot-head"><span class="ai-tag">{SPARK}Built in-house</span><h2 id="spot-h">AI products we built</h2>
<p>Our own AI tools, designed, engineered and shipped by the same team that builds for our clients.</p></div><div class="stack">{cards}</div></section>'''

def index_body(href):
    total="11.8M+"
    apps=''.join(f'<a class="app" href="{href(p["slug"])}" style="--c:{p["color"]}"><div class="icon{" has-img" if p.get("icon") else ""}">{icon_inner(p)}</div><b>{p["name"]}{'<em class="ai-mini">AI</em>' if p.get("ai") else ''}</b><span>{p["card_stat"][0]}</span></a>' for p in PROJECTS)
    ARROW='<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'
    def media(p):
        ic=f'<div class="cs-ic icon{" has-img" if p.get("icon") else ""}">{icon_inner(p)}</div>'
        if p.get("shots"):
            im=''.join(f'<img class="p p{i}" src="{ASSET(src)}" alt="" width="535" height="1160" loading="lazy">' for i,(src,cap,alt) in enumerate(p["shots"][:3]))
        elif p.get("card_img") or p.get("hero"):
            src,alt,w,h=p.get("card_img") or p["hero"]; im=f'<img class="w" src="{ASSET(src)}" alt="" width="{w}" height="{h}" loading="lazy">'
        elif p["kind"]=="workspace": im=f'<div class="cm"><div class="browser"><div class="bdots"><i></i><i></i><i></i></div>{GZ_DASH}</div></div>'
        elif p["kind"]=="ghost": im=f'<div class="cm"><div class="browser"><div class="bdots"><i></i><i></i><i></i></div>{GHOST_CALL}</div></div>'
        else: im=''
        return f'<div class="cs-media" aria-hidden="true">{ic}{im}</div>'
    def group(p): return "web" if p["kind"] in ("web","registry") else "desktop" if p["kind"]=="desktop" else "mobile"
    def groups(p): return group(p)+(" ai" if p.get("ai") else "")
    cards=''
    for i,p in enumerate(PROJECTS):
        chips=''.join(f'<li><b>{v}</b> {l}</li>' for v,l in p["stats"][:2])
        cards+=f'''<a class="cs-card" href="{href(p["slug"])}" data-groups="{groups(p)}" style="--c:{p["color"]};--d:{(i%2)*90}ms">{media(p)}
<div class="cs-body"><div class="cs-meta">{niche_tag(p) or f'<span class="cs-cat">{p["category"]}</span>'}{ai_tag(p)}{demo_tag(p)}</div><h3>{p["name"]}</h3><p>{p["oneliner"]}</p><ul class="cs-stats">{chips}</ul>
<span class="cs-go">View case study<i>{ARROW}</i></span></div></a>'''
    n=lambda g: sum(g in groups(p).split() for p in PROJECTS)
    btn=lambda f,label,c,on=False: f'<button type="button" aria-pressed="{"true" if on else "false"}" data-f="{f}">{label} <span>{c}</span></button>' if c else ''
    filt=('<div class="cs-filter" role="group" aria-label="Filter case studies">'+btn("all","All",len(PROJECTS),True)+btn("ai","AI tools",n("ai"))
          +btn("mobile","Mobile apps",n("mobile"))+btn("web","Web platforms",n("web"))+btn("desktop","Desktop apps",n("desktop"))+'</div>')
    return f'''{topbar(href(None))}<main>
<section class="wrap ihero"><div class="fx-stage" aria-hidden="true">
<div class="fx-obj o1" data-depth="1.2"><div class="bob"><i class="orb"></i></div></div>
<div class="fx-obj o2" data-depth=".8"><div class="bob b2"><div class="cube"><i></i><i></i><i></i><i></i><i></i><i></i></div></div></div>
<div class="fx-obj o3" data-depth="1.7"><div class="bob b3"><i class="ring"></i></div></div>
<div class="fx-obj o4" data-depth=".5"><div class="bob b4"><i class="pill"></i></div></div>
<div class="fx-obj o5" data-depth="2.2"><div class="bob b2"><i class="orb sm"></i></div></div></div><h1>Ideas, engineered into intelligent products.</h1>
<p>iApp Technologies is a leading AI development company. Since 2012, our team of 100+ designers, engineers and marketers has taken products from first sketch to millions of users. Today we build AI agents, RAG systems and intelligent apps for businesses around the world.</p>
<div class="links" style="margin-top:32px"><a class="btn" href="#work">See our work</a><a class="ghost" href="mailto:aziz.k@iapptechnologiesllp.com">Talk to our team</a></div></section>
<section class="wrap" aria-label="Products"><div class="home">{apps}</div>
<div class="tally" aria-label="Results across our consumer apps">
<div><i class="ti" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v11M7.5 10.5 12 15l4.5-4.5M5 19.5h14"/></svg></i><strong data-to="11.8" data-suf="M+" data-dec="1">{total}</strong><span>downloads across our four consumer apps</span></div>
<div><i class="ti" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5h16v11H9l-5 4z"/><path d="M8.5 9.5h7M8.5 12.5h4"/></svg></i><strong data-to="108" data-suf="K+" data-dec="0">108K+</strong><span>ratings on the US App Store</span></div>
<div><i class="ti" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 3.2l2.7 5.6 6.1.8-4.5 4.2 1.1 6.1L12 17l-5.4 2.9 1.1-6.1-4.5-4.2 6.1-.8z"/></svg></i><strong data-to="4.6" data-suf="" data-dec="1">4.6</strong><span>median App Store rating</span><em class="stars" aria-hidden="true"><b style="width:92%"></b></em></div></div></section>
{wall()}{meet()}{spotlight(href)}<section class="wrap list" id="work"><div class="cs-head"><div><h2>Case studies</h2><p>Products we have designed, built and kept shipping, from freight and healthcare platforms to apps with millions of installs.</p></div>{filt}</div><div class="cs-grid">{cards}</div></section>
<section class="wrap company"><div class="cohead"><h2>One team. Every stage. Under one roof.</h2><p data-words>Most products stall in the hand-offs between agencies. We keep strategy, design, engineering, AI, QA and growth inside one accountable team, so your product moves from idea to launch to scale without changing hands.</p></div>
<div class="facts"><div><strong>100+</strong><span>people on staff</span></div><div><strong>2012</strong><span>building since</span></div><div><strong>4</strong><span>offices: USA, India, Canada, Australia</span></div></div>
<div class="svc">
<div class="ai"><h3>AI and agentic solutions</h3><p data-words>Autonomous AI agents that run real workflows, RAG systems that answer from your own documents and data, LLM features inside your apps, and chatbots connected to your CRM and ERP.</p><ul><li>AI agents</li><li>RAG</li><li>LLM integration</li><li>Chatbots</li><li>Generative AI</li></ul></div>
<div><h3>Product design</h3><p>Research, user journeys, wireframes, prototypes and design systems that make complex products simple to use.</p></div>
<div><h3>Development</h3><p>iOS, Android, Flutter, web apps, SaaS platforms and cloud back ends built to handle millions of users.</p></div>
<div><h3>Testing and QA</h3><p>Manual and automated testing across devices, so every release ships stable.</p></div>
<div><h3>Maintenance and support</h3><p>Ongoing updates, monitoring, OS compatibility and performance work long after launch.</p></div>
<div><h3>SEO and marketing</h3><p>App store optimisation, SEO and performance marketing that bring users in and keep them.</p></div>
</div></section>
{cta()}</main>{FOOT}'''+TILT

def case_body(p, href, nxt):
    st=''.join(f'<div><strong>{v}</strong><span>{l}</span></div>' for v,l in p["stats"])
    hard=''.join(f'<div><h3>{a}</h3><p>{b}</p></div>' for a,b in p["hard"])
    feat=''.join(f'<div><h3>{a}</h3><p>{b}</p></div>' for a,b in p["built"])
    how=''.join(f'<li><div><h3>{a}</h3><p>{b}</p></div></li>' for a,b in p["how"])
    gallery=''
    if p.get("shots"):
        g=''.join(f'<figure><img src="{ASSET(src)}" alt="{alt}" width="535" height="1160" loading="lazy"><figcaption>{cap}</figcaption></figure>' for src,cap,alt in p["shots"])
        gallery=f'<section class="gallery"><h2>Inside the app</h2><div class="shots" style="--n:{len(p["shots"])}">{g}</div></section>'
    if p.get("wide") or p.get("flow"):
        FI={"box":'<path d="M12 3 4 7v10l8 4 8-4V7z"/><path d="M4 7l8 4 8-4M12 11v10"/>',
            "truck":'<path d="M2 6.5h11v9H2z"/><path d="M13 9.5h4l3 3.2v2.8h-7"/><circle cx="6" cy="17.5" r="1.7"/><circle cx="16.5" cy="17.5" r="1.7"/>',
            "pin":'<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0C18.5 15.4 12 21 12 21z"/><circle cx="12" cy="10" r="2.4"/>',
            "clipboard":'<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v1M9 10h6M9 14h6M9 18h3"/>',
            "calendar":'<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 9.5h17M8 3v4M16 3v4M8 14l2 2 4-4"/>',
            "pulse":'<path d="M3 12.5h4l2-5 4 10 2-5h6"/>',
            "chart":'<path d="M4 20V4M4 20h16"/><path d="M7 15l4-4 3 3 5-6"/>',
            "bars":'<path d="M6 20V11M12 20V5M18 20v-7M3 20h18"/>',
            "download":'<path d="M12 4v11M7.5 10.5 12 15l4.5-4.5M5 19.5h14"/>',
            "receipt":'<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M14 8.5c-.6-.7-1.3-1-2.2-1-1.2 0-2 .6-2 1.5 0 2 4.4 1.2 4.4 3.3 0 .9-.9 1.6-2.2 1.6-1 0-1.8-.4-2.4-1.1M12 6.5v1M12 14v1"/>'}
        w=''.join(f'<figure class="widefig"><img src="{ASSET(src)}" alt="{alt}" width="{iw}" height="{ih}" loading="lazy"><figcaption>{cap}</figcaption></figure>' for src,cap,alt,iw,ih in p.get("wide",[]))
        fl=''
        if p.get("flow"):
            cards=''.join(f'<li><span class="fi" style="background:{col}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{FI[ic]}</svg></span><small>0{i+1}</small><h3>{t}</h3><p>{tx}</p></li>' for i,(t,tx,col,ic) in enumerate(p["flow"]))
            fl=f'<figure class="widefig"><ol class="flow" style="grid-template-columns:repeat(auto-fit,minmax({300 if len(p["flow"])>4 else 230}px,1fr))">{cards}</ol><figcaption>{p.get("flow_caption","The life of a load in Transwayz, from first order to settled pay")}</figcaption></figure>'
        sh=''
        if p.get("shots"):
            sh='<div class="shots" style="margin-bottom:40px">'+''.join(f'<figure><img src="{ASSET(src)}" alt="{alt}" width="535" height="1160" loading="lazy"><figcaption>{cap}</figcaption></figure>' for src,cap,alt in p["shots"])+'</div>'
        gallery=f'<section class="gallery"><h2>{p.get("flow_title","Inside the product")}</h2>{sh}{w}{fl}</section>'
    chips=''.join(f'<li>{c}</li>' for c in p["platforms"])
    live=''.join(f'<a class="livebtn" href="{u}" target="_blank" rel="noopener">{t}</a>' for t,u in p["links"])
    links=''.join(f'<a class="ghost" href="{u}" target="_blank" rel="noopener">{t}</a>' for t,u in p["links"])
    return f'''<div style="--c:{p["color"]}"><div class="chero on-color">{topbar(href(None),True)}
<div class="wrap"><div class="inner"><div><div class="crumb"><div class="icon{" has-img" if p.get("icon") else ""}">{icon_inner(p)}</div><div><b>Case study</b>{p["category"]}, {p["platform"]}{('<span class="tags">'+niche_tag(p)+ai_tag(p)+demo_tag(p)+'</span>') if (p.get("niche") or p.get("ai") or p.get("demo")) else ''}</div></div>
<h1>{p["name"]}</h1><p class="lede">{p["oneliner"]}</p>{('<div class="live">'+live+'</div>') if live else ''}</div>{mock(p)}</div>
<div class="storerow">{st}</div></div></div>
<main class="wrap">
<section class="sec"><h2>The brief</h2><div class="prose"><p class="big" data-words>{p["summary"]}</p><p>{p["brief"]}</p><p class="who">Who it serves: {p["client"]}</p></div></section>
{gallery}<section class="sec"><h2>What made it hard</h2><div class="hard">{hard}</div></section>
<section class="sec"><h2>What we built</h2><div class="feat">{feat}</div></section>
<section class="sec"><h2>How we worked</h2><ol class="steps">{how}</ol></section>
<section class="sec" style="border-bottom:0"><h2>Where it landed</h2><div><p class="outcome">{p["outcome"]}</p><div style="height:28px"></div><ul class="chips" aria-label="Platforms">{chips}</ul>{('<h3 class="seelive">See it live</h3><div class="links">'+links+'</div>') if links else ''}</div></section>
<a class="next" href="{href(nxt["slug"])}" style="--c:{nxt["color"]}"><span>Next case study</span><b>{nxt["name"]}</b></a>
</main>{cta()}{FOOT}</div>'''

def page(title, desc, body, extra_head=""):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2224%22 fill=%22%231A1F2B%22/><text x=%2250%22 y=%2270%22 font-size=%2260%22 text-anchor=%22middle%22 fill=%22white%22 font-family=%22Arial%22 font-weight=%22bold%22>i</text></svg>">
{FONT}<script>try{{var c=sessionStorage.getItem("fxNav");if(c&&!matchMedia("(prefers-reduced-motion: reduce)").matches){{document.documentElement.classList.add("fx-arrive");document.documentElement.style.setProperty("--fc",c)}}sessionStorage.removeItem("fxNav")}}catch(e){{}}</script><style>{CSS}</style>{extra_head}<script src="/fx.js" defer></script></head><body>{body}</body></html>'''

# ---- multi-page site for Vercel
out=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(out)  # asset paths in data.py are relative to the repo root
href_site=lambda s: "/" if s is None else f"/{s}"
open(f"{out}/index.html","w").write(page("Case studies | iApp Technologies","Products iApp Technologies designed and built, including AI tools: "+", ".join(p["name"] for p in PROJECTS)+".",index_body(href_site)))
for i,p in enumerate(PROJECTS):
    nxt=PROJECTS[(i+1)%len(PROJECTS)]
    open(f"{out}/{p['slug']}.html","w").write(page(f"{p['name']} case study | iApp Technologies",p["oneliner"],case_body(p,href_site,nxt)))
open(f"{out}/fx.js","w").write(FX_JS)
json.dump({"cleanUrls":True,"trailingSlash":False},open(f"{out}/vercel.json","w"),indent=2)
print("Built", len(PROJECTS), "case studies + index into", out)
