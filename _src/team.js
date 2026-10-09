/* "Our Team" 3D carousel. Copied to /assets/team.js by build.py; markup comes from team() in build.py.
   Cards sit on a shallow arc: the centre person is large and in colour, neighbours step back, tilt and turn grey. */
(function () {
  var sec = document.getElementById("team");
  if (!sec) return;
  var stage = sec.querySelector(".tm-stage"), cards = [].slice.call(sec.querySelectorAll(".tm-card")),
      dashes = [].slice.call(sec.querySelectorAll(".tm-dash")), num = sec.querySelector(".tm-now"), live = sec.querySelector(".tm-live");
  var n = cards.length, cur = 0, pos = 0, raf = 0, drag = null;
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = matchMedia("(hover: hover) and (pointer: fine)").matches;
  var tiltX = 0, tiltY = 0, tiltRaf = 0;

  function wrap(d) { d = ((d % n) + n) % n; return d > n / 2 ? d - n : d; }
  function spacing() { return Math.min(260, Math.max(120, stage.clientWidth * 0.2)); }

  function layout(p) {
    var sp = spacing();
    cards.forEach(function (c, i) {
      var d = wrap(i - p), a = Math.abs(d);
      var x = d * sp * (1 - Math.min(a, 3) * 0.08), z = -Math.min(a, 4) * 150, ry = -Math.max(-1, Math.min(1, d)) * Math.min(a, 1) * 16 - (a > 1 ? Math.sign(d) * 6 : 0);
      var s = 1 - Math.min(a, 3) * 0.06, centre = Math.max(0, 1 - a);
      var tilt = centre > 0.5 ? " rotateX(" + (tiltY * centre).toFixed(2) + "deg) rotateY(" + (tiltX * centre).toFixed(2) + "deg)" : "";
      c.style.transform = "translate(-50%,-50%) translateX(" + x.toFixed(1) + "px) translateZ(" + z.toFixed(1) + "px) rotateY(" + ry.toFixed(2) + "deg) scale(" + s.toFixed(3) + ")" + tilt;
      c.style.zIndex = String(100 - Math.round(a * 10));
      c.style.opacity = a > 3.6 ? "0" : String(Math.min(1, 4 - a));
      c.classList.toggle("on", a < 0.5);
    });
  }
  function select(i, opts) {
    cur = ((i % n) + n) % n;
    var c = cards[cur];
    sec.style.setProperty("--tc", c.getAttribute("data-accent"));
    num.textContent = String(cur + 1).padStart(2, "0");
    dashes.forEach(function (d, k) { d.setAttribute("aria-current", k === cur ? "true" : "false"); });
    cards.forEach(function (k, j) { k.setAttribute("aria-hidden", j === cur ? "false" : "true"); k.tabIndex = j === cur ? 0 : -1; });
    if (live && !(opts && opts.quiet)) live.textContent = c.getAttribute("data-name") + ", " + c.getAttribute("data-role");
    animateTo(cur);
  }
  function animateTo(target) {
    var t = pos + wrap(target - pos);
    if (reduce) { pos = t; layout(pos); return; }
    cancelAnimationFrame(raf);
    var from = pos, t0 = performance.now(), dur = 760;
    (function step(now) {
      var k = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - k, 4);
      pos = from + (t - from) * e; layout(pos);
      if (k < 1) raf = requestAnimationFrame(step); else { pos = ((t % n) + n) % n; layout(pos); }
    })(t0);
  }

  sec.querySelector(".tm-prev").addEventListener("click", function () { select(cur - 1); });
  sec.querySelector(".tm-next").addEventListener("click", function () { select(cur + 1); });
  dashes.forEach(function (d, k) { d.addEventListener("click", function () { select(k); }); });
  cards.forEach(function (c, k) { c.addEventListener("click", function () { if (!drag || !drag.moved) { if (k !== cur) select(k); } }); });

  // keyboard: arrows while the section has focus or is mostly on screen
  var inView = false;
  new IntersectionObserver(function (e) { inView = e[0].intersectionRatio > 0.6; }, { threshold: [0, 0.6, 1] }).observe(sec);
  document.addEventListener("keydown", function (e) {
    if (e.target.closest && e.target.closest("input,textarea,select,.aic")) return;
    if (!(inView || sec.contains(document.activeElement))) return;
    if (e.key === "ArrowRight") { select(cur + 1); e.preventDefault(); }
    else if (e.key === "ArrowLeft") { select(cur - 1); e.preventDefault(); }
  });

  // drag / swipe: the row follows the finger, then settles on the nearest person
  stage.addEventListener("pointerdown", function (e) {
    if (e.button > 0) return;
    cancelAnimationFrame(raf);
    drag = { x: e.clientX, y: e.clientY, p: pos, moved: false, id: e.pointerId, v: 0, lx: e.clientX, lt: performance.now() };
  });
  window.addEventListener("pointermove", function (e) {
    if (fine && !drag) {
      var r = stage.getBoundingClientRect();
      if (e.clientY > r.top && e.clientY < r.bottom) {
        tiltX = ((e.clientX - r.left) / r.width - 0.5) * 10; tiltY = -((e.clientY - r.top) / r.height - 0.5) * 8;
        if (!raf && !tiltRaf) tiltRaf = requestAnimationFrame(function () { tiltRaf = 0; if (!raf) layout(pos); });
      }
    }
    if (!drag || e.pointerId !== drag.id) return;
    var dx = e.clientX - drag.x, dy = e.clientY - drag.y;
    if (!drag.moved) {
      if (Math.abs(dx) < 8) return;
      if (Math.abs(dy) > Math.abs(dx)) { drag = null; return; } // vertical swipe: let the page scroll
      drag.moved = true; stage.classList.add("dragging");
      try { stage.setPointerCapture(e.pointerId); } catch (x) {}
    }
    var now = performance.now(); drag.v = (e.clientX - drag.lx) / Math.max(1, now - drag.lt); drag.lx = e.clientX; drag.lt = now;
    pos = drag.p - dx / spacing(); layout(pos);
  }, { passive: true });
  function endDrag() {
    if (!drag) return;
    var d = drag; stage.classList.remove("dragging");
    if (d.moved) { var fling = Math.max(-1.5, Math.min(1.5, -d.v * 0.9)); select(Math.round(pos + fling)); }
    setTimeout(function () { drag = null; }, 0);
  }
  window.addEventListener("pointerup", endDrag);
  window.addEventListener("pointercancel", endDrag);

  // horizontal trackpad / shift+wheel moves one person at a time (vertical scrolling is left to the page)
  var wheelLock = 0;
  stage.addEventListener("wheel", function (e) {
    var dx = Math.abs(e.deltaX) > Math.abs(e.deltaY) * 1.2 ? e.deltaX : (e.shiftKey ? e.deltaY : 0);
    if (!dx) return;
    var now = performance.now();
    if (now < wheelLock || Math.abs(dx) < 4) return;
    wheelLock = now + 520; select(cur + (dx > 0 ? 1 : -1));
  }, { passive: true });

  // centre photo zooms in as the section reaches the middle of the screen, and out as it leaves;
  // when the visitor comes back to the section, Jagwinder (the first card) is back in the middle
  var zoom = 1, zoomGoal = 1, zRaf = 0, wasAway = false, HOME = 0;
  function zoomFrame() {
    zRaf = 0; zoom += (zoomGoal - zoom) * 0.12;
    sec.style.setProperty("--zoom", zoom.toFixed(4));
    if (Math.abs(zoomGoal - zoom) > 0.0005) zRaf = requestAnimationFrame(zoomFrame);
  }
  function onScroll() {
    var r = sec.getBoundingClientRect(), vh = window.innerHeight;
    if (r.bottom < 0 || r.top > vh) { if (!wasAway) wasAway = true; return; }
    if (wasAway) { wasAway = false; if (cur !== HOME && !drag) select(HOME, { quiet: true }); }
    var p = (r.top + r.height / 2 - vh / 2) / (vh / 2 + r.height / 2);   // -1 .. 1, 0 = centred
    zoomGoal = reduce ? 1 : 1 + 0.14 * Math.max(0, 1 - Math.abs(p) * 1.25);
    if (!zRaf) zRaf = requestAnimationFrame(zoomFrame);
  }
  var sTick = 0;
  window.addEventListener("scroll", function () { if (!sTick) { sTick = 1; requestAnimationFrame(function () { sTick = 0; onScroll(); }); } }, { passive: true });
  onScroll();

  window.addEventListener("resize", function () { layout(pos); });
  sec.classList.add("ready");
  select(0, { quiet: true });
})();
