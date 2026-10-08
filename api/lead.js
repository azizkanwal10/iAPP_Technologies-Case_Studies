// Vercel serverless function: receives a lead from the "Meet our AI" chat and emails it to the sales team.
// Needs RESEND_API_KEY in the Vercel project settings. Optional: LEAD_TO (comma-separated) and LEAD_FROM.
const INTERESTS = ["An AI agent", "A mobile app", "A web platform", "Just exploring"];
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

module.exports = async (req, res) => {
  if (req.method !== "POST") { res.setHeader("Allow", "POST"); return res.status(405).json({ ok: false }); }
  let b = req.body || {};
  if (typeof b === "string") { try { b = JSON.parse(b); } catch (e) { b = {}; } }

  // bots: hidden field filled in, or the form was "typed" impossibly fast
  if (b.company_site || (Number(b.elapsed) || 0) < 2500) return res.status(200).json({ ok: true });

  const name = String(b.name || "").trim().replace(/\s+/g, " ").slice(0, 60);
  const phone = String(b.phone || "").trim().slice(0, 30);
  const digits = phone.replace(/\D/g, "");
  const interest = INTERESTS.includes(b.interest) ? b.interest : "Not specified";
  const location = String(b.location || "").trim().replace(/\s+/g, " ").slice(0, 80);
  let email = String(b.email || "").trim().slice(0, 80);
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) email = "";
  // visitor's own time zone (from their browser), so calls land at a sensible hour
  let tz = String(b.tz || "").slice(0, 60), localTime = "";
  try { localTime = new Date().toLocaleString("en-GB", { timeZone: tz, weekday: "short", hour: "numeric", minute: "2-digit", hour12: true }); } catch (e) { tz = ""; }
  const model = String(b.model || "").slice(0, 20);
  const page = String(b.page || "").slice(0, 200);
  if (!name || digits.length < 7 || digits.length > 15 || !/^[+\d\s().-]+$/.test(phone)) return res.status(400).json({ ok: false, error: "invalid" });

  const key = process.env.RESEND_API_KEY;
  if (!key) return res.status(503).json({ ok: false, error: "not_configured" });

  const to = (process.env.LEAD_TO || "aziz.k@iapptechnologiesllp.com").split(",").map((s) => s.trim()).filter(Boolean);
  const when = new Date().toLocaleString("en-GB", { timeZone: "Asia/Kolkata", dateStyle: "medium", timeStyle: "short" });
  const wa = "https://wa.me/" + digits;
  const html = `<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.6;color:#14171d">
<h2 style="margin:0 0 12px">New lead from the iApp AI chat</h2>
<table cellpadding="6" style="border-collapse:collapse">
<tr><td style="color:#667">Name</td><td><b>${esc(name)}</b></td></tr>
<tr><td style="color:#667">Phone</td><td><b><a href="tel:${esc(digits)}">${esc(phone)}</a></b> &middot; <a href="${esc(wa)}">WhatsApp</a></td></tr>
<tr><td style="color:#667">Location</td><td>${esc(location || "-")}</td></tr>
<tr><td style="color:#667">Their local time</td><td>${localTime ? `<b>${esc(localTime)}</b> (${esc(tz)}) when they sent this` : "-"}</td></tr>
<tr><td style="color:#667">Email</td><td>${email ? `<a href="mailto:${esc(email)}">${esc(email)}</a>` : "Not shared"}</td></tr>
<tr><td style="color:#667">Interested in</td><td>${esc(interest)}</td></tr>
<tr><td style="color:#667">Chatted with</td><td>${esc(model || "-")}</td></tr>
<tr><td style="color:#667">Page</td><td>${esc(page || "-")}</td></tr>
<tr><td style="color:#667">Time (IST)</td><td>${esc(when)}</td></tr></table>
<p style="color:#667">The visitor agreed to be contacted by iApp Technologies about their project.</p></div>`;

  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        from: process.env.LEAD_FROM || "iApp AI <onboarding@resend.dev>",
        to,
        subject: `New lead: ${name}${location ? ", " + location : ""} (${interest})`,
        ...(email ? { reply_to: email } : {}),
        html,
        text: `New lead from the iApp AI chat\nName: ${name}\nPhone: ${phone}\nLocation: ${location || "-"}\nTheir local time: ${localTime ? localTime + " (" + tz + ")" : "-"}\nEmail: ${email || "Not shared"}\nInterested in: ${interest}\nPage: ${page}\nTime (IST): ${when}`,
      }),
    });
    if (!r.ok) { console.error("resend", r.status, await r.text()); return res.status(502).json({ ok: false, error: "send_failed" }); }
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error("resend", e);
    return res.status(502).json({ ok: false, error: "send_failed" });
  }
};
