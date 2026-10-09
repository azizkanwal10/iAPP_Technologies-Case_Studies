/* Cursor and scroll effects for the case studies site. Everything is skipped for reduced motion. */
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
var sTick=0;W.addEventListener("scroll",function(){if(!sTick){sTick=1;requestAnimationFrame(function(){sTick=0;onScroll()})}},{passive:true});
W.addEventListener("resize",function(){vh=W.innerHeight;onScroll()});
if(fine){W.addEventListener("pointermove",function(e){tx=e.clientX/W.innerWidth*2-1;ty=e.clientY/vh*2-1;
  if(home){var r=home.getBoundingClientRect();var inside=e.clientX>r.left-80&&e.clientX<r.right+80&&e.clientY>r.top-80&&e.clientY<r.bottom+80;
    hx=inside?clamp((e.clientX-r.left)/r.width*2-1,-1,1):0;hy=inside?clamp((e.clientY-r.top)/r.height*2-1,-1,1):0}
  kick()},{passive:true});
  d.addEventListener("pointerleave",function(){tx=ty=hx=hy=0;kick()})}
onScroll();
})();
