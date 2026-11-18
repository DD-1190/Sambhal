# Sambhal — landing page (Hindi + English)

A plain HTML/CSS static site with no build step and no dependencies. It loads fast on slow 4G.

```
/index.html          Hindi (default, served at /)
/en/index.html       English (served at /en)
/assets/styles.css   shared styles
/assets/favicon.svg
/assets/logo-mark.svg  Sambhal logo mark
/assets/founder.svg  placeholder photo, replace with yours
/vercel.json         clean URLs + asset caching
/brand/              logo pack (Hindi + English, light + dark, mark SVG + 512px PNG)
```

## Before you go live

Search the project for these and replace them:

| Find | Replace with |
|---|---|
| `910000000000` | Your WhatsApp number: country code + number, no `+` or spaces (e.g. `919812345678`) |
| `+91 00000 00000` | Your phone number as it should appear |
| `[आपका नाम]` / `[Your name]` | Your name |
| `[पता]` / `[address]` / `[Address]` | Your office address |
| `/assets/founder.svg` | Your photo, e.g. `/assets/founder.jpg` (square, at least 160×160) |
| `₹4,250` in the chat example | A realistic price for your first target business type |

Also check the `TODO` comments in both HTML files.

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
