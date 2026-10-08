/* "Meet our AI" chat: the mascot asks for a name, then a number, so the iApp sales team can call back.
   Copied to /assets/ai-chat.js by build.py. Leads are POSTed to /api/lead (see api/lead.js). */
(function () {
  var sec = document.querySelector(".meet"), box = document.getElementById("aic");
  if (!sec || !box) return;
  var log = box.querySelector(".aic-log"), form = box.querySelector(".aic-form"), input = box.querySelector(".aic-in"),
      hp = box.querySelector(".aic-hp"), chips = box.querySelector(".aic-chips"), legal = box.querySelector(".aic-legal"),
      launch = document.querySelector(".aic-launch"), status = box.querySelector(".aic-st");
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var WA = "917009592313", MAIL = "aziz.k@iapptechnologiesllp.com";
  var st = { step: "idle", name: "", phone: "", location: "", email: "", interest: "", t0: 0, opened: false };
  var tz = ""; try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ""; } catch (e) {}
  var saved = {};
  try { saved = JSON.parse(localStorage.getItem("iappLead") || "{}"); } catch (e) {}

  var meet = function () { return window.iappMeet || { look: function () {}, setText: function () {}, model: function () { return ""; } }; };
  var pick = function (a) { return a[Math.floor(Math.random() * a.length)]; };
  var wait = function (ms) { return new Promise(function (r) { setTimeout(r, reduce ? 0 : ms); }); };
  var scrollLog = function () { log.scrollTop = log.scrollHeight; };

  function bubble(who, text) {
    var b = document.createElement("div");
    b.className = "aic-msg " + who;
    b.textContent = text;
    log.appendChild(b); scrollLog();
    return b;
  }
  // AI message: typing dots, then the words appear a few characters at a time
  function say(text, pause) {
    meet().look(0.72, -0.12);
    status.textContent = "typing…";
    var dots = document.createElement("div");
    dots.className = "aic-msg ai typing"; dots.innerHTML = "<i></i><i></i><i></i>";
    log.appendChild(dots); scrollLog();
    return wait(pause != null ? pause : Math.min(1500, 450 + text.length * 14)).then(function () {
      dots.remove();
      var b = bubble("ai", reduce ? text : "");
      if (reduce) { status.textContent = "online"; return; }
      return new Promise(function (done) {
        var i = 0, id = setInterval(function () {
          i = Math.min(text.length, i + 3); b.textContent = text.slice(0, i); scrollLog();
          if (i >= text.length) { clearInterval(id); status.textContent = "online"; done(); }
        }, 16);
      });
    });
  }
  function ask(type, placeholder, auto, skip) {
    input.type = type; input.placeholder = placeholder; input.value = "";
    input.setAttribute("autocomplete", auto); input.setAttribute("inputmode", type === "tel" ? "tel" : "text");
    input.maxLength = type === "tel" ? 20 : type === "email" ? 80 : 60;
    form.hidden = false; chips.innerHTML = "";
    if (skip) { var c = document.createElement("button"); c.type = "button"; c.className = "aic-chip"; c.textContent = skip.label; c.addEventListener("click", skip.fn); chips.appendChild(c); }
    if (st.opened && matchMedia("(hover: hover)").matches) input.focus({ preventScroll: true });
  }
  function offer(list, onPick) {
    form.hidden = true; chips.innerHTML = "";
    list.forEach(function (label) {
      var c = document.createElement("button"); c.type = "button"; c.className = "aic-chip"; c.textContent = label;
      c.addEventListener("click", function () { chips.innerHTML = ""; onPick(label); });
      chips.appendChild(c);
    });
    scrollLog();
  }
  function links(name) {
    chips.innerHTML = ""; form.hidden = true;
    var msg = "Hi iApp team, I'm " + name + (st.location ? " from " + st.location : "") + ". Please call me on " + st.phone + (st.email ? " or email " + st.email : "") + " about " + (st.interest || "a project") + ".";
    [["Send on WhatsApp", "https://wa.me/" + WA + "?text=" + encodeURIComponent(msg)],
     ["Send by email", "mailto:" + MAIL + "?subject=" + encodeURIComponent("Call me back: " + name) + "&body=" + encodeURIComponent(msg)]]
      .forEach(function (l) { var a = document.createElement("a"); a.className = "aic-chip"; a.href = l[1]; a.target = "_blank"; a.rel = "noopener"; a.textContent = l[0]; chips.appendChild(a); });
  }
  var cap = function (s) { return s.replace(/\s+/g, " ").trim().replace(/(^|\s)\S/g, function (m) { return m.toUpperCase(); }); };

  function start() {
    if (st.step !== "idle") return;
    st.t0 = Date.now();
    if (saved.sent && saved.name) {
      st.step = "done"; st.name = saved.name; meet().setText("Hi, " + st.name);
      return say("Welcome back, " + st.name + " 👋 The team already has your number, so expect a human to call. Anything else? I'm all goggles.").then(function () {
        offer(["Change my number", "Just browsing"], function (l) { if (l === "Just browsing") { bubble("me", l); say("Enjoy the tour. I'll keep my visor warm for you."); } else { bubble("me", l); st.step = "phone"; askPhone(); } });
      });
    }
    if (saved.name) {
      st.name = saved.name; meet().setText("Hi, " + st.name);
      return say("Welcome back, " + st.name + ". I may be made of polygons, but I never forget a name.").then(askPhone);
    }
    st.step = "name";
    return say(pick(["Psst. Over here. 👀 I'm the iApp AI, and you've been staring at my goggles for a while.", "Hey you. 👋 Yes, you with the excellent cursor control. I'm the iApp AI."]), 700)
      .then(function () { return say("Before you scroll off and break my circuits: what should I call you?"); })
      .then(function () { ask("text", "Your first name", "given-name"); });
  }
  function askPhone() {
    st.step = "phone";
    return say("So, " + st.name + ", I'll be bold. Can I have your number? 📱")
      .then(function () { return say("Strictly professional, I promise. A real human from the iApp team will call you about what you're building. I'd call you myself, but… no hands. Just goggles."); })
      .then(function () {
        legal.hidden = false;
        ask("tel", "+91 98765 43210", "tel");
      });
  }
  function askLocation() {
    st.step = "location";
    return say(pick(["Smooth. 😏 Saved somewhere safer than my own memory.", "Got it. I'd wink, but my visor only does text."]))
      .then(function () { return say("Where in the world are you, " + st.name + "? City and country, so my humans don't ring you at 3 a.m. They need their beauty sleep too."); })
      .then(function () { ask("text", "e.g. Pune, India", "off"); });
  }
  function askEmail() {
    st.step = "email";
    return say("Want to drop your email too? Totally optional. I promise not to send you 47 newsletters.")
      .then(function () { ask("email", "you@company.com", "email", { label: "Skip", fn: function () { bubble("me", "Skip"); st.email = ""; askInterest(true); } }); });
  }
  function askInterest(skipped) {
    st.step = "interest";
    return say(skipped ? "No problem. A phone call it is. 📞" : pick(["Noted. Your inbox is in safe hands.", "Perfect. I'll make sure it doesn't end up in a spam folder of shame."]))
      .then(function () { return say("Last one, " + st.name + ": what are you dreaming up?"); })
      .then(function () {
        offer(["An AI agent", "A mobile app", "A web platform", "Just exploring"], function (l) { bubble("me", l); st.interest = l; send(); });
      });
  }
  function send() {
    st.step = "sending";
    status.textContent = "thinking…";
    return say(pick(["Beaming this to my humans… ✨", "Encrypting your number with my finest neural network…"]), 500).then(function () {
      return fetch("/api/lead", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: st.name, phone: st.phone, location: st.location, email: st.email, tz: tz, interest: st.interest, model: meet().model(), page: location.pathname, company_site: hp.value, elapsed: Date.now() - st.t0 }),
      }).then(function (r) { return r.ok; }, function () { return false; });
    }).then(function (ok) {
      if (ok) {
        st.step = "done";
        try { localStorage.setItem("iappLead", JSON.stringify({ name: st.name, sent: true })); } catch (e) {}
        meet().setText("See you soon, " + st.name);
        sec.classList.add("aic-sent");
        return say("Done, " + st.name + ". A real iApp human will call you within one business day. Fair warning: they're almost as charming as me. ✨")
          .then(function () { offer(["Keep exploring"], function () { minimise(); }); });
      }
      st.step = "fallback";
      return say("Hmm, my line to the team is having a moment, " + st.name + ". Tap one of these and your message goes straight to them:").then(function () { links(st.name); });
    });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var v = input.value.trim();
    if (!v) return;
    if (st.step === "name") {
      var name = cap(v.replace(/[^\p{L}\p{M}\s'.-]/gu, "")).slice(0, 30);
      if (!name) return say("That's a very modern name. Got one with letters in it?");
      bubble("me", name); st.name = name; form.hidden = true;
      try { localStorage.setItem("iappLead", JSON.stringify({ name: name })); } catch (e) {}
      meet().setText("Hi, " + name);
      say(pick([name + ". Lovely. My neural nets just did a little happy dance.", "Nice to meet you, " + name + ". I'd blush, but I'm mostly aluminium.", name + "! Saved to memory. Permanently. Well, until the next deploy."]))
        .then(function () { return say("Look at my goggles, " + name + ". 😉"); }).then(askPhone);
    } else if (st.step === "phone") {
      var digits = v.replace(/\D/g, "");
      if (digits.length < 7 || digits.length > 15 || !/^[+\d\s().-]+$/.test(v)) { say("That doesn't look like a number I can pass on. Mind checking it? I'm not judging the area code."); return; }
      bubble("me", v); st.phone = v; form.hidden = true; legal.hidden = true;
      askLocation();
    } else if (st.step === "location") {
      var loc = v.replace(/[^\p{L}\p{M}\s,.'()-]/gu, "").replace(/\s+/g, " ").trim().slice(0, 60);
      if (loc.replace(/[^\p{L}]/gu, "").length < 2) { say("I couldn't find that on my map. City and country, please, like \"Dubai, UAE\"."); return; }
      if (loc === loc.toLowerCase()) {
        // "dubai, uae" -> "Dubai, UAE": title-case, and short country codes after the comma in capitals
        loc = cap(loc);
        var parts = loc.split(",");
        if (parts.length > 1) parts.push(parts.pop().replace(/\b\p{L}{2,3}\b/gu, function (w) { return w.toUpperCase(); }));
        loc = parts.join(",");
      }
      bubble("me", loc); st.location = loc; form.hidden = true;
      var city = loc.split(",")[0].trim();
      say(pick([city + "! Great choice. I've only ever been inside a GPU, so I'm a little jealous.", city + ", noted. My humans will call at a civilised hour, promise."])).then(askEmail);
    } else if (st.step === "email") {
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) || v.length > 80) { say("Hmm, that email looks like it took a wrong turn. Try again, or tap Skip."); return; }
      bubble("me", v); st.email = v; form.hidden = true; chips.innerHTML = "";
      askInterest(false);
    }
  });

  function open(byUser) {
    if (box.classList.contains("on")) return;
    box.classList.add("on"); sec.classList.add("chatting"); if (launch) launch.hidden = true;
    st.opened = !!byUser;
    start();
    if (byUser && !form.hidden && matchMedia("(hover: hover)").matches) input.focus({ preventScroll: true });
  }
  function minimise() { box.classList.remove("on"); sec.classList.remove("chatting"); if (launch) launch.hidden = false; }
  box.querySelector(".aic-x").addEventListener("click", minimise);
  if (launch) launch.addEventListener("click", function () { open(true); });
  [].forEach.call(document.querySelectorAll("[data-aic-open]"), function (b) { b.addEventListener("click", function (e) { e.preventDefault(); open(true); }); });
  box.addEventListener("pointerdown", function () { st.opened = true; });

  // open by itself once the visitor has spent a moment in the section
  var timer = 0;
  new IntersectionObserver(function (es) {
    if (es[0].isIntersecting) { if (!timer && st.step === "idle") timer = setTimeout(function () { open(false); }, 2600); }
    else if (timer) { clearTimeout(timer); timer = 0; }
  }, { threshold: 0.55 }).observe(sec);
})();
