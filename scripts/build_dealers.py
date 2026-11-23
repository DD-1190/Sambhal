"""Generate the property-dealer landing page (English /property-dealers, Hindi /hi/property-dealers).

Run:  python3 scripts/build_dealers.py && python3 scripts/stamp_assets.py
Header and final call-to-action come from the home pages so the page matches the site.
English page: any Hindi is written in Hinglish (Roman script). Hindi page: Devanagari.
"""
import json, pathlib, re, sys, urllib.parse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_usecases import ROOT, D, WA, ICON, ic, esc, url, path, grab  # noqa: E402

SLUG = "property-dealers"
TICK = ic('<path d="M5 12.5l4.5 4.5L19 7"/>', 16, 2.6)
IMG = "/assets/dealer/"


def pic(name, alt, sizes, cls="", eager=False, w=1200, h=800):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img class="{cls}" src="{IMG}{name}-1200.webp" srcset="{IMG}{name}-640.webp 640w, {IMG}{name}-1200.webp 1200w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{alt}" {load} decoding="async">')


C = {
 "en": dict(
  title="WhatsApp Digital Secretary for Property Dealers | Sambhal",
  desc="Reply to every 99acres, MagicBricks and WhatsApp lead in under a minute — even at 11 pm. Listing cards, site-visit booking and old-lead follow-ups for Indian property dealers. ₹15,000/month.",
  crumb="Property dealers", home="Home",
  pill="Digital secretary for property dealers",
  h1='Every lead answered in&nbsp;1&nbsp;minute — <span class="hl">even at 11 pm.</span>',
  h1_plain="Every lead answered in 1 minute — even at 11 pm.",
  lead="Enquiries from 99acres, MagicBricks and WhatsApp get a reply, matching listings and a site-visit slot — in your name, on your number. You just show up for the visit.",
  cta="See it on WhatsApp", price_link="₹15,000/month — see what’s included",
  salary="Less than an office assistant’s salary — and it never takes a day off.",
  wa="Hi, I'm a property dealer. I want to see the Sambhal digital secretary for my leads.",
  note="Jawab 38 second mein ✓",
  chat=dict(name="Amit · 99acres lead", status="online", me="Sharma Properties",
    m1="3BHK chahiye Indirapuram mein, budget 1.2 Cr tak", t1="11:04 pm",
    m2="Namaste Amit ji! Aapke budget mein 3 options hain. Pehla yeh raha 👇", t2="11:04 pm",
    card_t="3BHK builder floor · Niti Khand", card_s="₹1.15 Cr · 1,650 sq ft · park facing",
    m3="Kal shaam 5 baje dekh sakte hain?", t3="11:06 pm",
    m4="Done ✓ Kal 5 baje, Niti Khand. Location bhej raha hoon.", t4="11:06 pm"),
  lcard=("₹1.15 Cr", "3BHK builder floor · Indirapuram", ["1,650 sq ft", "Park facing", "Ready to move"]),
  toast=("Site visit booked", "Tomorrow, 5:00 pm · Niti Khand"),
  works="Works with the leads you already get",
  q_eyebrow="Sound familiar?",
  quote="“Lead raat 11 baje aayi. Humne subah 10 baje call kiya. Tab tak client teen aur dealers se baat kar chuka tha.”",
  q_note="Buyers enquire on four or five listings at once. The dealer who replies first usually gets the site visit.",
  pains=["Portal leads pile up while you’re out on a site visit", "The same flat goes out with ten different photos and prices", "Last month’s leads never get a second call"],
  b_eyebrow="Every day, without being told", b_h2="What your digital secretary does",
  b1=("No lead waits", "Every portal and WhatsApp enquiry gets a reply in under a minute, day or night. It asks budget, area and BHK — the questions you would ask.",
      [("11:04 pm", "99acres", "38 sec"), ("6:52 am", "MagicBricks", "41 sec"), ("1:15 pm", "WhatsApp", "22 sec")], "replied in"),
  stat=("&lt; 1 min", "average first reply, 24×7"),
  b2=("Listing cards, not messy forwards", "Your inventory becomes clean cards with photos, price, size and your RERA number — sent only to buyers it fits."),
  b3=("Old leads come back", "A new 200-gaj plot comes in? It finds everyone who asked for a plot in the last six months and messages them for you.",
      "Sir, aapne plot ke baare mein poocha tha — Sector 12 mein naya 200 gaj aaya hai. Dekhna chahenge?"),
  b4=("Your day, in one message", "Every night at 9 pm: new leads, tomorrow’s visits, and who needs a call from you.",
      "Today at Sharma Properties", [("New leads", "14"), ("Site visits tomorrow", "5"), ("Hot buyers — call them", "3")]),
  ba_eyebrow="Same flat, better first impression", ba_h2="From a forward to a listing buyers trust.",
  before_tag="Before", after_tag="After",
  before_msg="3bhk avlbl indirapuram 1.15cr park fcng ready call 98XXXXXXXX", fwd="Forwarded many times",
  after=("₹1.15 Cr", "3BHK builder floor · Niti Khand, Indirapuram", ["1,650 sq ft", "Park facing", "Ready to move"], "RERA no. on every card", "Book a site visit"),
  roi_h="One extra deal a quarter pays for Sambhal — many times over.",
  roi_p="On a ₹1 Cr flat, a 1% commission to you is ₹1 lakh. Sambhal costs ₹45,000 a quarter.",
  s_eyebrow="How it works", s_h2="Live in about a week",
  steps=[("Share your listings", "Excel, a Google Sheet or just photos on WhatsApp. We turn them into listing cards."),
         ("Connect your lead alerts", "The 99acres, MagicBricks and Housing.com alerts you already get, plus your WhatsApp Business number."),
         ("Your secretary starts replying", "A real expert checks it every week and tunes it with you. You handle the visits and the deals.")],
  own_eyebrow="Aapke leads, aapke paas", own_h2="Your leads stay yours.",
  own=[("Your number, your name", "Buyers only ever see your business on WhatsApp — never Sambhal."),
       ("Saved in your own sheet", "Every lead goes into your Google Sheet. Take it with you anytime."),
       ("Never shared", "Not with portals, not with other dealers. Not ever.")],
  p_eyebrow="Pricing", p_h2="One plan for dealers. No commission, no contract.",
  plan=("Dealer plan", "For individual dealers and small agencies", "₹15,000", "/month",
        ["Digital secretary on your WhatsApp number", "Replies to portal and WhatsApp leads, 24×7", "Listing cards from your inventory",
         "Site-visit booking and reminders", "Old-lead re-match and 9 pm daily summary", "8 expert hours a month"],
        "Start on WhatsApp"),
  plan_wa="Hi, I'm a property dealer. I want to know more about the Sambhal dealer plan (₹15,000/month).",
  chk=("Not sure yet?", "Start with a ₹999 check", "30 minutes on your leads and listings, plus a one-page plan. Full refund if it isn’t useful.", "₹999", "Book the check"),
  chk_wa="Hi, I'm a property dealer. I want to book the ₹999 business AI check.",
  fine="Stop any month. WhatsApp message charges are billed at actual cost.",
  f_eyebrow="FAQ", f_h2="Questions dealers ask",
  faq=[("Will buyers know it’s not me?", "Messages go from your number, in your name and your tone. Anything serious — negotiation, a hot buyer, a complaint — comes straight to you."),
       ("Where does my lead data go?", "Into your own Google Sheet. It is never shared with portals or other dealers, and you can take it with you anytime."),
       ("Will it quote the wrong price?", "It only shares prices from your listing sheet. Discounts and negotiation always come to you."),
       ("Does it work with 99acres, MagicBricks and Housing.com?", "Yes. We connect the lead alerts you already get from them, plus your WhatsApp and Facebook leads."),
       ("Can it talk in Hindi?", "Yes — Hindi, English or Hinglish, whichever the buyer writes in."),
       ("What about RERA?", "Your RERA registration number appears on every listing card. It doesn’t give legal advice — those questions come to you.")],
  final_h2="Let your phone work the night shift.",
  final_lead="Send us a voice note on WhatsApp — your area and how many leads you get. We’ll show you how your digital secretary would reply.",
  pricing_anchor="pricing",
 ),
 "hi": dict(
  title="प्रॉपर्टी डीलर के लिए WhatsApp डिजिटल सेक्रेटरी | सँभाल",
  desc="99acres, MagicBricks और WhatsApp की हर लीड का जवाब 1 मिनट में — रात 11 बजे भी। लिस्टिंग कार्ड, साइट विज़िट बुकिंग और पुरानी लीड से दोबारा बात। ₹15,000/महीना।",
  crumb="प्रॉपर्टी डीलर", home="होम",
  pill="प्रॉपर्टी डीलर का डिजिटल सेक्रेटरी",
  h1='हर लीड का जवाब 1&nbsp;मिनट में — <span class="hl">रात 11 बजे भी।</span>',
  h1_plain="हर लीड का जवाब 1 मिनट में — रात 11 बजे भी।",
  lead="99acres, MagicBricks और WhatsApp की हर पूछताछ को जवाब, सही प्रॉपर्टी और साइट विज़िट का टाइम — आपके नाम से, आपके नंबर से। आपको बस विज़िट पर पहुँचना है।",
  cta="WhatsApp पर देखें", price_link="₹15,000/महीना — क्या-क्या मिलता है",
  salary="एक ऑफ़िस असिस्टेंट की सैलरी से भी कम — और यह कभी छुट्टी नहीं लेता।",
  wa="नमस्ते, मैं प्रॉपर्टी डीलर हूँ। मुझे अपनी लीड के लिए सँभाल का डिजिटल सेक्रेटरी देखना है।",
  note="जवाब 38 सेकंड में ✓",
  chat=dict(name="अमित · 99acres लीड", status="ऑनलाइन", me="शर्मा प्रॉपर्टीज़",
    m1="इंदिरापुरम में 3BHK चाहिए, बजट 1.2 करोड़ तक", t1="11:04 pm",
    m2="नमस्ते अमित जी! आपके बजट में 3 ऑप्शन हैं। पहला यह रहा 👇", t2="11:04 pm",
    card_t="3BHK बिल्डर फ़्लोर · नीति खंड", card_s="₹1.15 करोड़ · 1,650 वर्ग फ़ुट · पार्क फ़ेसिंग",
    m3="कल शाम 5 बजे देख सकते हैं?", t3="11:06 pm",
    m4="हो गया ✓ कल 5 बजे, नीति खंड। लोकेशन भेज रहा हूँ।", t4="11:06 pm"),
  lcard=("₹1.15 करोड़", "3BHK बिल्डर फ़्लोर · इंदिरापुरम", ["1,650 वर्ग फ़ुट", "पार्क फ़ेसिंग", "रेडी टू मूव"]),
  toast=("साइट विज़िट बुक", "कल, शाम 5 बजे · नीति खंड"),
  works="उन्हीं लीड के साथ काम करता है जो आपको पहले से मिलती हैं",
  q_eyebrow="क्या आपके साथ भी होता है?",
  quote="“लीड रात 11 बजे आई। हमने सुबह 10 बजे फ़ोन किया। तब तक क्लाइंट तीन और डीलरों से बात कर चुका था।”",
  q_note="खरीदार एक साथ चार-पाँच लिस्टिंग पर पूछताछ करता है। जो डीलर पहले जवाब देता है, अक्सर साइट विज़िट उसी को मिलती है।",
  pains=["आप साइट विज़िट पर होते हैं और पोर्टल की लीड जमा होती रहती हैं", "एक ही फ़्लैट दस अलग फ़ोटो और दाम के साथ घूमता है", "पिछले महीने की लीड को दोबारा कोई फ़ोन नहीं करता"],
  b_eyebrow="रोज़, बिना कहे", b_h2="आपका डिजिटल सेक्रेटरी क्या करता है",
  b1=("कोई लीड इंतज़ार नहीं करती", "पोर्टल और WhatsApp की हर पूछताछ का जवाब 1 मिनट के अंदर, दिन हो या रात। बजट, इलाका और BHK पूछता है — वही सवाल जो आप पूछते।",
      [("11:04 pm", "99acres", "38 सेकंड"), ("6:52 am", "MagicBricks", "41 सेकंड"), ("1:15 pm", "WhatsApp", "22 सेकंड")], "जवाब"),
  stat=("&lt; 1 मिनट", "औसत पहला जवाब, 24×7"),
  b2=("गंदे फ़ॉरवर्ड नहीं, साफ़ लिस्टिंग कार्ड", "आपकी इन्वेंटरी फ़ोटो, दाम, साइज़ और RERA नंबर वाले कार्ड में बदलती है — और सिर्फ़ सही खरीदार को जाती है।"),
  b3=("पुरानी लीड लौट आती हैं", "नया 200 गज़ का प्लॉट आया? पिछले छह महीने में जिसने भी प्लॉट पूछा था, उसे यह खुद मैसेज कर देता है।",
      "सर, आपने प्लॉट के बारे में पूछा था — सेक्टर 12 में नया 200 गज़ आया है। देखना चाहेंगे?"),
  b4=("पूरा दिन, एक मैसेज में", "हर रात 9 बजे: नई लीड, कल की विज़िट, और किसे आपका फ़ोन चाहिए।",
      "आज शर्मा प्रॉपर्टीज़ में", [("नई लीड", "14"), ("कल की साइट विज़िट", "5"), ("गर्म खरीदार — फ़ोन करें", "3")]),
  ba_eyebrow="वही फ़्लैट, बेहतर पहली छाप", ba_h2="फ़ॉरवर्ड से ऐसी लिस्टिंग तक, जिस पर खरीदार भरोसा करे।",
  before_tag="पहले", after_tag="अब",
  before_msg="3bhk avlbl indirapuram 1.15cr park fcng ready call 98XXXXXXXX", fwd="कई बार फ़ॉरवर्ड किया गया",
  after=("₹1.15 करोड़", "3BHK बिल्डर फ़्लोर · नीति खंड, इंदिरापुरम", ["1,650 वर्ग फ़ुट", "पार्क फ़ेसिंग", "रेडी टू मूव"], "हर कार्ड पर RERA नंबर", "साइट विज़िट बुक करें"),
  roi_h="तिमाही में एक डील ज़्यादा — और सँभाल का ख़र्च कई गुना वसूल।",
  roi_p="₹1 करोड़ के फ़्लैट पर आपका 1% कमीशन ₹1 लाख होता है। सँभाल का ख़र्च तिमाही में ₹45,000 है।",
  s_eyebrow="कैसे काम करता है", s_h2="लगभग एक हफ़्ते में चालू",
  steps=[("अपनी लिस्टिंग भेजें", "Excel, Google Sheet या WhatsApp पर बस फ़ोटो। हम उन्हें लिस्टिंग कार्ड बना देते हैं।"),
         ("लीड अलर्ट जोड़ें", "99acres, MagicBricks और Housing.com के जो अलर्ट आपको आते हैं, और आपका WhatsApp Business नंबर।"),
         ("सेक्रेटरी जवाब देने लगता है", "एक असली एक्सपर्ट हर हफ़्ते जाँचता है और आपके साथ सुधारता है। आप विज़िट और डील सँभालिए।")],
  own_eyebrow="भरोसा", own_h2="आपके लीड, आपके पास।",
  own=[("आपका नंबर, आपका नाम", "खरीदार को WhatsApp पर सिर्फ़ आपका बिज़नेस दिखता है — सँभाल नहीं।"),
       ("आपकी अपनी शीट में", "हर लीड आपकी Google Sheet में सेव होती है। जब चाहें ले जाइए।"),
       ("कभी शेयर नहीं", "न पोर्टल से, न दूसरे डीलरों से। कभी नहीं।")],
  p_eyebrow="दाम", p_h2="डीलरों के लिए एक प्लान। न कमीशन, न कॉन्ट्रैक्ट।",
  plan=("डीलर प्लान", "अकेले डीलर और छोटी एजेंसियों के लिए", "₹15,000", "/महीना",
        ["आपके WhatsApp नंबर पर डिजिटल सेक्रेटरी", "पोर्टल और WhatsApp लीड को 24×7 जवाब", "आपकी इन्वेंटरी से लिस्टिंग कार्ड",
         "साइट विज़िट बुकिंग और रिमाइंडर", "पुरानी लीड से मिलान और रात 9 बजे का सारांश", "हर महीने 8 घंटे एक्सपर्ट का समय"],
        "WhatsApp पर शुरू करें"),
  plan_wa="नमस्ते, मैं प्रॉपर्टी डीलर हूँ। मुझे सँभाल के डीलर प्लान (₹15,000/महीना) के बारे में जानना है।",
  chk=("अभी पक्का नहीं?", "₹999 की जाँच से शुरू करें", "आपकी लीड और लिस्टिंग पर 30 मिनट की बात, और एक पन्ने का प्लान। काम का न लगे तो पूरा पैसा वापस।", "₹999", "जाँच बुक करें"),
  chk_wa="नमस्ते, मैं प्रॉपर्टी डीलर हूँ। मुझे ₹999 की बिज़नेस AI जाँच बुक करनी है।",
  fine="किसी भी महीने बंद करें। WhatsApp मैसेज का ख़र्च असल दाम पर बिल में अलग से।",
  f_eyebrow="सवाल-जवाब", f_h2="डीलर अक्सर पूछते हैं",
  faq=[("क्या खरीदार को पता चलेगा कि यह मैं नहीं हूँ?", "मैसेज आपके नंबर से, आपके नाम और आपके अंदाज़ में जाते हैं। कोई भी ज़रूरी बात — मोलभाव, गर्म खरीदार, शिकायत — सीधे आपके पास आती है।"),
       ("मेरी लीड का डेटा कहाँ जाता है?", "आपकी अपनी Google Sheet में। यह कभी पोर्टल या दूसरे डीलरों से शेयर नहीं होता, और आप इसे जब चाहें ले जा सकते हैं।"),
       ("कहीं गलत दाम तो नहीं बता देगा?", "यह सिर्फ़ आपकी लिस्टिंग शीट के दाम बताता है। छूट और मोलभाव हमेशा आपके पास आते हैं।"),
       ("क्या यह 99acres, MagicBricks और Housing.com के साथ चलता है?", "हाँ। उनसे जो लीड अलर्ट आपको पहले से आते हैं, उन्हें हम जोड़ देते हैं — साथ में WhatsApp और Facebook की लीड भी।"),
       ("क्या यह हिंदी में बात करता है?", "हाँ — हिंदी, अंग्रेज़ी या हिंग्लिश, जिसमें खरीदार लिखे।"),
       ("RERA का क्या?", "हर लिस्टिंग कार्ड पर आपका RERA रजिस्ट्रेशन नंबर दिखता है। यह कानूनी सलाह नहीं देता — ऐसे सवाल आपके पास आते हैं।")],
  final_h2="रात की शिफ़्ट आपका फ़ोन सँभाले।",
  final_lead="WhatsApp पर एक वॉइस नोट भेजिए — आपका इलाका और रोज़ कितनी लीड आती हैं। हम दिखाएँगे कि आपका डिजिटल सेक्रेटरी कैसे जवाब देगा।",
  pricing_anchor="daam",
 ),
}

PORTALS = ["99acres", "MagicBricks", "Housing.com", "WhatsApp", "Facebook"]
PAIN_ICO = [ic('<path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.4 8.4 0 1 1 21 11.5z"/><path d="M12 8v4l2.5 1.5"/>'),
            ic('<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><path d="M14 17.5h7M17.5 14v7"/>'),
            ic('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/><path d="M16 2l6 6M22 2l-6 6"/>')]
STEP_ICO = [ICON["link"], ICON["send"], ICON["check"]]
OWN_ICO = [ic('<path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.4 8.4 0 1 1 21 11.5z"/>', 22),
           ic('<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M3 15h18M9 4v16"/>', 22),
           ic('<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>', 22)]


def chips(items):
    return "".join(f"<li>{x}</li>" for x in items)


def build(lang, home):
    c = C[lang]
    other = "hi" if lang == "en" else "en"
    ch = c["chat"]
    wa = WA + urllib.parse.quote(c["wa"])

    header = grab(home, r'<header class="site-header">.*?</header>')
    header = header.replace(f'class="lang" href="{path(other)}"', f'class="lang" href="{path(other, SLUG)}"')
    final = grab(home, r'<section class="final">.*?</section>')
    final = final.replace('<section class="final">', '<section class="final dk-final">', 1)
    final = re.sub(r'href="https://wa\.me/919873470074\?text=[^"]*"', f'href="{wa}"', final, count=1)
    final = re.sub(r'<h2>.*?</h2>', f'<h2>{c["final_h2"]}</h2>', final, count=1, flags=re.S)
    final = re.sub(r'<p class="lead">.*?</p>', f'<p class="lead">{c["final_lead"]}</p>', final, count=1, flags=re.S)
    final = final.replace('<div class="wrap">', '<div class="dk-final-bg" aria-hidden="true">'
                          + pic("colony", "", "100vw", "", False, 1200, 800) + '</div>\n    <div class="wrap">', 1)
    statusbar = grab(home, r'<div class="statusbar".*?</div>')
    fonts = grab(grab(home, r'<head>.*?</head>'), r'  <link rel="preconnect" href="https://fonts.googleapis.com">.*?</head>').replace("</head>", "")
    fonts = fonts.replace("&display=swap", "&family=Kalam&display=swap")
    fonts = fonts.replace('<link rel="stylesheet" href="/assets/styles.css', '<link rel="stylesheet" href="/assets/styles.css') \
                 .rstrip() + '\n  <link rel="stylesheet" href="/assets/dealer.css">\n'

    phone = f'''<div class="phone">
            <span class="ph-btn ph-action" aria-hidden="true"></span><span class="ph-btn ph-vol-up" aria-hidden="true"></span><span class="ph-btn ph-vol-down" aria-hidden="true"></span><span class="ph-btn ph-power" aria-hidden="true"></span>
            <div class="ph-bezel">
            <div class="screen">
              {statusbar}
              <article class="slide is-active">
                <div class="chat-head"><span class="avatar">A</span><span class="who"><strong>{ch["name"]}</strong><span>{ch["status"]}</span></span></div>
                <div class="bubble in">{ch["m1"]}<span class="time">{ch["t1"]}</span></div>
                <div class="bubble out"><small>{ch["me"]}</small>{ch["m2"]}<span class="time">{ch["t2"]}</span></div>
                <div class="dk-mini">{pic("floor", "", "200px", "", True, 1200, 800)}<p><strong>{ch["card_t"]}</strong><span>{ch["card_s"]}</span></p></div>
                <div class="bubble in">{ch["m3"]}<span class="time">{ch["t3"]}</span></div>
                <div class="bubble out">{ch["m4"]}<span class="time">{ch["t4"]}</span></div>
              </article>
            </div>
            </div>
          </div>'''

    lc = c["lcard"]
    b1, b2, b3, b4 = c["b1"], c["b2"], c["b3"], c["b4"]
    log = "".join(f'<li><span>{t}</span><span>{s}</span><b>{b1[3]} {d}</b></li>' for t, s, d in b1[2])
    summary = "".join(f'<li><span>{k}</span><b>{v}</b></li>' for k, v in b4[3])
    af = c["after"]
    pl = c["plan"]
    plan_items = "".join(f"<li>{TICK}{x}</li>" for x in pl[4])
    pains = "".join(f'<li><span class="ico">{PAIN_ICO[i]}</span><p>{p}</p></li>' for i, p in enumerate(c["pains"]))
    steps = "\n".join(f'        <li class="step"><span class="step-ico">{STEP_ICO[i]}</span><div><p class="step-num">{"STEP" if lang == "en" else "कदम"} {i + 1}</p><h3>{t}</h3><p>{d}</p></div></li>'
                      for i, (t, d) in enumerate(c["steps"]))
    own = "".join(f'<li><span class="ico">{OWN_ICO[i]}</span><strong>{t}</strong><span>{d}</span></li>' for i, (t, d) in enumerate(c["own"]))
    faqs = "\n".join(f'        <details>\n          <summary>{q}{ICON["plus"]}</summary>\n          <p>{a}</p>\n        </details>' for q, a in c["faq"])
    portals = "".join(f"<li>{p}</li>" for p in PORTALS)

    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url(lang, SLUG) + "#webpage", "url": url(lang, SLUG), "name": c["title"],
         "description": c["desc"], "inLanguage": "en-IN" if lang == "en" else "hi-IN",
         "isPartOf": {"@id": D + "/#website"}, "breadcrumb": {"@id": url(lang, SLUG) + "#breadcrumb"}},
        {"@type": "Service", "name": c["pill"], "serviceType": "WhatsApp lead response for real estate agents",
         "description": c["lead"], "audience": {"@type": "BusinessAudience", "audienceType": "Real estate agents and property dealers"},
         "provider": {"@type": "Organization", "@id": D + "/#org", "name": "Sambhal", "url": D + "/", "telephone": "+91-9873470074"},
         "areaServed": {"@type": "Country", "name": "India"},
         "offers": [{"@type": "Offer", "name": pl[0], "price": "15000", "priceCurrency": "INR",
                     "priceSpecification": {"@type": "UnitPriceSpecification", "price": "15000", "priceCurrency": "INR", "unitText": "MONTH"}},
                    {"@type": "Offer", "name": c["chk"][1], "price": "999", "priceCurrency": "INR"}]},
        {"@type": "BreadcrumbList", "@id": url(lang, SLUG) + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": c["home"], "item": url(lang)},
            {"@type": "ListItem", "position": 2, "name": c["crumb"], "item": url(lang, SLUG)}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c["faq"]]},
    ]}
    ld = json.dumps(graph, ensure_ascii=False, indent=1).replace("</", "<\\/")
    og = f"{D}/assets/og-dealers{'-hi' if lang == 'hi' else ''}.png"

    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(c["title"])}</title>
  <meta name="description" content="{esc(c["desc"])}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="#232E66">
  <link rel="canonical" href="{url(lang, SLUG)}">
  <link rel="alternate" hreflang="en-IN" href="{url("en", SLUG)}">
  <link rel="alternate" hreflang="hi-IN" href="{url("hi", SLUG)}">
  <link rel="alternate" hreflang="x-default" href="{url("en", SLUG)}">

  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/assets/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="preload" as="image" href="{IMG}desk-640.webp" imagesrcset="{IMG}desk-640.webp 640w, {IMG}desk-1200.webp 1024w" imagesizes="(min-width: 900px) 420px, 74vw">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Sambhal">
  <meta property="og:url" content="{url(lang, SLUG)}">
  <meta property="og:title" content="{esc(c["h1_plain"])}">
  <meta property="og:description" content="{esc(c["desc"])}">
  <meta property="og:image" content="{og}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(c["h1_plain"])}">
  <meta name="twitter:description" content="{esc(c["desc"])}">
  <meta name="twitter:image" content="{og}">

  <script type="application/ld+json">
{ld}
  </script>

{fonts}</head>
<body class="dk">

{header}

<main>

  <section class="hero dk-hero">
    <div class="wrap hero-grid">
      <div class="hero-copy">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="{path(lang)}">{c["home"]}</a><span aria-hidden="true">/</span><span>{c["crumb"]}</span></nav>
        <p class="pill dk-pill">{c["pill"]}</p>
        <h1>{c["h1"]}</h1>
        <p class="lead">{c["lead"]}</p>
        <div class="hero-actions">
          <a class="btn btn-accent" data-cta="whatsapp-dealer-hero" href="{wa}">{ICON["chat"]}{c["cta"]}</a>
          <a class="link-arrow" href="#{c["pricing_anchor"]}">{c["price_link"]} →</a>
        </div>
        <p class="dk-salary">{c["salary"]}</p>
      </div>

      <div class="dk-collage">
        <div class="dk-photo">{pic("desk", "", "(min-width: 900px) 420px, 74vw", "", True, 1024, 1280)}</div>
        <p class="dk-note" aria-hidden="true">{c["note"]}</p>
        <div class="dk-phone">{phone}</div>
        <div class="dk-lcard" aria-hidden="true">{pic("floor", "", "260px", "", True, 1200, 800)}<div><b>{lc[0]}</b><span>{lc[1]}</span><ul class="dk-chips">{chips(lc[2])}</ul></div></div>
        <div class="dk-toast" aria-hidden="true"><span class="dk-tick">{TICK}</span><div><strong>{c["toast"][0]}</strong><span>{c["toast"][1]}</span></div></div>
      </div>
    </div>
    <div class="wrap">
      <div class="dk-works"><p>{c["works"]}</p><ul>{portals}</ul></div>
    </div>
  </section>

  <section class="dk-quote">
    <div class="wrap">
      <span class="eyebrow">{c["q_eyebrow"]}</span>
      <blockquote><p>{c["quote"]}</p></blockquote>
      <p class="dk-qnote">{c["q_note"]}</p>
      <ul class="dk-pains">{pains}</ul>
    </div>
  </section>

  <section class="dk-bento-sec">
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow">{c["b_eyebrow"]}</span>
        <h2>{c["b_h2"]}</h2>
      </div>
      <div class="dk-bento">
        <article class="dk-b dk-b1">
          <h3>{b1[0]}</h3><p>{b1[1]}</p>
          <p class="dk-stat"><b>{c["stat"][0]}</b><span>{c["stat"][1]}</span></p>
          <ul class="dk-log">{log}</ul>
        </article>
        <article class="dk-b dk-b2">
          <div class="dk-b-img">{pic("floor", "", "(min-width: 900px) 360px, 90vw", "", False, 1200, 800)}<span class="dk-rera">RERA</span></div>
          <h3>{b2[0]}</h3><p>{b2[1]}</p>
        </article>
        <article class="dk-b dk-b3">
          <div class="dk-b-img">{pic("plot", "", "(min-width: 900px) 360px, 90vw", "", False, 1200, 800)}</div>
          <h3>{b3[0]}</h3><p>{b3[1]}</p>
          <div class="bubble out dk-bubble">{b3[2]}</div>
        </article>
        <article class="dk-b dk-b4">
          <h3>{b4[0]}</h3><p>{b4[1]}</p>
          <div class="dk-summary"><p class="dk-sum-head"><span>9:00 pm</span>{b4[2]}</p><ul>{summary}</ul></div>
        </article>
      </div>
    </div>
  </section>

  <section class="dk-ba-sec">
    <div class="wrap">
      <div class="section-head center">
        <span class="eyebrow">{c["ba_eyebrow"]}</span>
        <h2>{c["ba_h2"]}</h2>
      </div>
      <div class="dk-ba">
        <figure class="dk-before">
          <figcaption>{c["before_tag"]}</figcaption>
          <div class="dk-chatbg"><div class="bubble in"><small class="dk-fwd">↪ {c["fwd"]}</small><span class="dk-blur" aria-hidden="true"></span>{c["before_msg"]}<span class="time">2:17 pm</span></div></div>
        </figure>
        <div class="dk-arrow" aria-hidden="true">{ICON["arrow"]}</div>
        <figure class="dk-after">
          <figcaption>{c["after_tag"]}</figcaption>
          <div class="dk-listing">
            {pic("resale", "", "(min-width: 900px) 420px, 90vw", "", False, 1200, 800)}
            <div class="dk-listing-body">
              <b>{af[0]}</b><span>{af[1]}</span>
              <ul class="dk-chips">{chips(af[2])}</ul>
              <p class="dk-rera-line">{TICK}{af[3]}</p>
              <span class="dk-fake-btn">{af[4]}</span>
            </div>
          </div>
        </figure>
      </div>
    </div>
  </section>

  <section class="dk-roi">
    <div class="wrap">
      <p class="dk-roi-h">{c["roi_h"]}</p>
      <p class="dk-roi-p">{c["roi_p"]}</p>
    </div>
  </section>

  <section class="steps">
    <div class="wrap">
      <div class="section-head center">
        <span class="eyebrow">{c["s_eyebrow"]}</span>
        <h2>{c["s_h2"]}</h2>
      </div>
      <ol class="step-grid">
{steps}
      </ol>
    </div>
  </section>

  <section class="dk-own">
    <div class="wrap">
      <div class="dk-own-grid">
        <div><span class="eyebrow">{c["own_eyebrow"]}</span><h2>{c["own_h2"]}</h2></div>
        <ul>{own}</ul>
      </div>
    </div>
  </section>

  <section class="pricing dk-pricing" id="{c["pricing_anchor"]}">
    <div class="wrap">
      <div class="section-head center">
        <span class="eyebrow">{c["p_eyebrow"]}</span>
        <h2>{c["p_h2"]}</h2>
      </div>
      <div class="dk-price-grid">
        <div class="plan featured">
          <p class="plan-name">{pl[0]}</p>
          <p class="plan-for">{pl[1]}</p>
          <p class="plan-price"><b>{pl[2]}</b><span>{pl[3]}</span></p>
          <ul>{plan_items}</ul>
          <a class="btn btn-accent" data-cta="plan-dealer" href="{WA}{urllib.parse.quote(c["plan_wa"])}">{pl[5]}</a>
        </div>
        <div class="check-strip dk-check">
          <div>
            <span class="tag">{c["chk"][0]}</span>
            <h3>{c["chk"][1]}</h3>
            <p>{c["chk"][2]}</p>
          </div>
          <div class="price-side">
            <span class="big">{c["chk"][3]}</span>
            <a class="btn btn-primary" data-cta="whatsapp-check-dealer" href="{WA}{urllib.parse.quote(c["chk_wa"])}">{c["chk"][4]}</a>
          </div>
        </div>
      </div>
      <p class="fine">{c["fine"]}</p>
    </div>
  </section>

  <section class="faq faq--uc dk-faq">
    <div class="wrap faq-grid">
      <div>
        <span class="eyebrow">{c["f_eyebrow"]}</span>
        <h2>{c["f_h2"]}</h2>
      </div>
      <div>
{faqs}
      </div>
    </div>
  </section>

  {final}

</main>

<script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
'''


def main():
    for lang in ("en", "hi"):
        home = (ROOT / ("index.html" if lang == "en" else "hi/index.html")).read_text(encoding="utf-8")
        out = ROOT / (SLUG if lang == "en" else f"hi/{SLUG}") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build(lang, home), encoding="utf-8")
        print("built", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
