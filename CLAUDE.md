# iApp Technologies – Case Studies site

Static site, hosted on Vercel (project `iapp-case-studies`, team "Aziz").
Live: https://iapp-case-studies.vercel.app — every push to `main` deploys automatically.

## How the site is built
- **Never hand-edit the `.html` files in the root.** They are generated.
- `_src/data.py` – all content: one `dict` per case study (text, stats, colours, image paths, links). Order in the list = order on the site.
- `_src/build.py` – page templates, CSS and JS. Run `python3 _src/build.py` to regenerate every page.
- `_src/imgproc.py` – helpers for preparing images (crop, round corners, save as WebP).
- `assets/<slug>/` – images. `vercel.json` gives clean URLs (`/transwayz` not `/transwayz.html`).

## Workflow for any change
1. Edit `_src/data.py` (content) or `_src/build.py` (design).
2. `python3 _src/build.py`
3. Check the result: open the pages locally (`python3 -m http.server` in the repo root), at desktop and phone widths.
4. Commit and push to `main`, then confirm the Vercel deployment is READY and the page loads.

## Case study fields (see existing entries in data.py)
`slug, name, color, kind, category, platform, oneliner, summary, stats (4 × (value,label)), card_stat, brief, client, hard, built, how, outcome, platforms, links`
Optional: `icon` (256px WebP), `shots` (phone screenshots), `hero` (single image + alt + w + h), `wide` (full-width images), `flow` + `flow_title` + `flow_caption` (numbered step cards), `card_img` (image for the listing card).

## Image rules
- Phone screenshots: crop the grey border, normalise to **535×1160**, round corners, save WebP (`imgproc.crop_card`, `norm`, `save_shot`). Keep all shots in one project the same size.
- App icons: square crop of the tile, 256×256 WebP with rounded corners (`save_icon`).
- Wide images: pad 24px white, resize to 1600px wide, WebP quality ~88.
- Remove anything in a screenshot that contradicts the page (e.g. an old download count or a rating that differs from the store).

## Content rules (important – this site goes to clients)
- Only use numbers that can be verified: App Store / Google Play listings, the client's own site, or figures the owner confirms. Never invent results, percentages or testimonials.
- Check store listings for current ratings before changing stats; write in plain, client-ready English.
- Drawn/illustrative UI must be labelled "Illustrative interface".
- Project colours must stay distinct on the landing page. In use: Transwayz #1A30D2, Baridata #0F766E, BeatStars #161616, PDF Converter #C2261C, Screen Recorder #C2410C, Poster Maker #AE1757, Singles Connect #6D2FD6.

## Contact details used on the site
aziz.k@iapptechnologiesllp.com · +91 70095 92313 · Offices: USA, India, Canada, Australia.

## Open items
- Baridata: need a larger logo (500px+) to replace the pulse placeholder icon.
- Singles Connect: need the real app icon to replace the heart placeholder.
- Singles Connect App Store notes (v1.5) expose a test login – make sure that account is disabled.
