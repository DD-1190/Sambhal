# Sambhal — landing page (Hindi + English)

A plain HTML/CSS static site with no build step and no dependencies. It loads fast on slow 4G.

```
/index.html          Hindi (default, served at /)
/en/index.html       English (served at /en)
/assets/styles.css   shared styles
/assets/favicon.svg
/assets/logo-mark.svg  Sambhal logo mark
/assets/main.js      use-case phone carousel (no dependencies)
/assets/founder.svg  placeholder photo, replace with yours
/vercel.json         clean URLs + asset caching
/brand/              logo pack v2 — two palms holding a marigold (SVG + PNG, Hindi + English, reverse, mono, app icon)
```

## Brand

Colours, fonts, logo rules and tone of voice follow the Sambhal brand guideline: Neel `#232E66`, Genda `#F2A43A`, Kagaz `#F7F3EA`, Syahi `#15161D`; Bricolage Grotesque + Anek Devanagari for headlines, Inter + Noto Sans Devanagari for text.

## Before you go live

- WhatsApp and phone are set to **+91 98734 70074** on every button. Each button sends its own pre-filled message, so you can tell which one a lead tapped.
- Founder photo: `/assets/founder.jpg` (square, 320×320). To change it, replace the file and run the stamp script.
- The chat examples in the phone use sample names, amounts and items. Adjust them to match your first target business type.

## Updating the site (no stale cache)

Browsers check for a fresh copy of every page and file on each visit (`vercel.json`), and each `/assets/` link carries a content-hash version. After changing anything in `/assets`, run:

```bash
python3 scripts/stamp_assets.py
```

then commit. Visitors get the new version on their next load — no hard refresh needed.

## Run locally

```bash
npx serve .
# or
python3 -m http.server 8000
```

## Deploy to Vercel

1. Push this folder to a new GitHub repository.
2. In Vercel: **Add New → Project**, import the repo.
3. Framework preset: **Other**. Leave the build command and output directory empty.
4. Deploy.

## Measuring the test

- In the Vercel project, go to **Analytics** and enable **Web Analytics**. The script tag is already on both pages.
- Every call-to-action link has a `data-cta` attribute (`whatsapp-hero`, `whatsapp-check`, `whatsapp-final`, `call-header`, `call-final`) so you can add click tracking later.
- Simplest signal: the WhatsApp prefill text tells you which button someone used. The ₹999 button sends a different message from the general ones.
- Use a separate link per traffic source, e.g. `yoursite.com/?src=ca-referral` or `/en?src=meta-ad`, and ask new leads where they found you.
