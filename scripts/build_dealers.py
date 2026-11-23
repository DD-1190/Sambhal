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
  title="More Buyers & Site Visits for Property Dealers — Ads + WhatsApp | Sambhal",
  desc="Get new buyers from local Instagram and Facebook ads, answer every lead on WhatsApp in under a minute and book more site visits. For Indian property dealers. From ₹15,000/month.",
  crumb="Property dealers", home="Home",
  pill="More buyers for property dealers",
  h1='More site visits every week — <span class="hl">from new buyers</span> and the leads you already pay for.',
  h1_plain="More site visits every week — from new buyers and the leads you already pay for.",
  lead="We turn every new listing into local ads and posts, bring buyers straight to your WhatsApp, and your digital secretary replies in under a minute and books the visit.",
  cta="Get more site visits", price_link="Plans from ₹15,000/month",
  salary="Ads in your name. Leads in your own sheet. Stop anytime.",
  wa="Hi, I'm a property dealer. I want more buyers and site visits with Sambhal.",
  note="Naya buyer, seedha WhatsApp pe ✓",
  chat=dict(name="Amit · Instagram ad", status="online", me="Sharma Properties",
    m1="3BHK chahiye Indirapuram mein, budget 1.2 Cr tak", t1="11:04 pm",
    m2="Namaste Amit ji! Aapke budget mein 3 options hain. Pehla yeh raha 👇", t2="11:04 pm",
    card_t="3BHK builder floor · Niti Khand", card_s="₹1.15 Cr · 1,650 sq ft · park facing",
    m3="Kal shaam 5 baje dekh sakte hain?", t3="11:06 pm",
    m4="Done ✓ Kal 5 baje, Niti Khand. Location bhej raha hoon.", t4="11:06 pm"),
  lcard=("₹1.15 Cr", "3BHK builder floor · Indirapuram", ["1,650 sq ft", "Park facing", "Ready to move"]),
  sponsored="Sponsored · Instagram",
  toast=("Site visit booked", "Tomorrow, 5:00 pm · Niti Khand"),
  works="Buyers from — and leads into —",
  q_eyebrow="Sound familiar?",
  quote="“Portal pe har mahine paisa daalo — aur wahi lead paanch aur dealers ke paas bhi jaati hai.”",
  q_note="Shared portal leads mean you compete on speed and price from the first message. Your own buyers, from your own ads, are worth far more.",
  pains=["Shared portal leads — five dealers call the same buyer", "Leads pile up while you’re out on a site visit — and go cold by morning", "Last month’s leads never get a second call"],
  n_eyebrow="Step one: new buyers", n_h2="How we bring you new buyers",
  new=[("Every listing becomes an ad", "A new flat comes in? It turns into an Instagram and Facebook post, a short reel, a WhatsApp status and portal-ready text — the same day.", "Same day"),
       ("Local ads that open WhatsApp", "Small ads in your area — “3BHK Indirapuram under 1.2 Cr” — that open a WhatsApp chat with you, not a form. Your secretary replies in seconds.", "1–2 weeks"),
       ("Your old contacts, woken up", "Thousands of saved numbers and past enquiries get a well-matched message when something they wanted comes in — only people who agreed to hear from you.", "Within days"),
       ("Found on Google", "Weekly posts on your Google Business Profile and a review request after every deal, so “property dealer near me” finds you.", "1–3 months")],
  seller=("Sellers and landlords too.", "Campaigns asking owners to list with you — more inventory means more to sell."),
  res_label="Results in",
  f_eyebrow2="The full journey", f_h22="From an ad to a booked visit — without you lifting the phone",
  funnel=[("Ad or post", "Instagram, Facebook, Google"), ("WhatsApp chat", "Buyer taps, chat opens"), ("Reply in &lt; 1 min", "Budget, area, BHK"), ("Visit booked", "Slot, location, reminder"), ("Follow-up", "Old leads re-matched")],
  funnel_mark="Your digital secretary takes over here",
  b_eyebrow="Step two: nobody goes cold", b_h2="Then your digital secretary handles every lead",
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
  roi_h="Two extra deals a quarter pay for all of it — ads included.",
  roi_p="On a ₹1 Cr flat, a 1% commission to you is ₹1 lakh. Lead Engine plus a ₹15,000 monthly ad budget comes to about ₹1.5 lakh a quarter.",
  s_eyebrow="How it works", s_h2="Live in about a week",
  steps=[("Share your listings", "Excel, a Google Sheet or just photos on WhatsApp. We turn them into listing cards and ads."),
         ("Set your ad budget", "You choose how much to spend. It’s paid from your own ad account, in your name."),
         ("Ads run, secretary replies", "New buyers come to your WhatsApp, along with your portal leads. Every one gets a reply in under a minute."),
         ("Weekly visits report", "Every Monday: leads, visits booked and what your ads brought in. A real expert tunes it with you.")],
  own_eyebrow="Aapke leads, aapke paas", own_h2="Your leads stay yours.",
  own=[("Your number, your name", "Buyers only ever see your business on WhatsApp — never Sambhal."),
       ("Your ad account", "Ads run from an account in your name. You own it and its data, even if you stop."),
       ("Saved in your own sheet", "Every lead goes into your Google Sheet. Take it with you anytime."),
       ("Never shared", "Not with portals, not with other dealers. Not ever.")],
  p_eyebrow="Pricing", p_h2="Two plans for dealers. No commission, no contract.",
  plan=("Secretary", "For dealers who already get enough leads", "₹15,000", "/month",
        ["Digital secretary on your WhatsApp number", "Replies to portal and WhatsApp leads, 24×7", "Listing cards from your inventory",
         "Site-visit booking and reminders", "Old-lead re-match and 9 pm daily summary", "8 expert hours a month"],
        "Choose Secretary"),
  plan_wa="Hi, I'm a property dealer. I want to know more about the Sambhal Secretary plan (₹15,000/month).",
  plan2=("Secretary + Lead Engine", "For dealers who want more buyers", "₹35,000", "/month + ad budget",
        ["Everything in Secretary", "Every listing turned into posts, reels and ads", "Local click-to-WhatsApp ads, tuned weekly",
         "Old-contact campaigns and Google profile posts", "Seller and landlord campaigns", "Weekly visits report · 20 expert hours a month"],
        "Get more site visits", "We suggest"),
  plan2_wa="Hi, I'm a property dealer. I want to know more about the Sambhal Secretary + Lead Engine plan (₹35,000/month + ad budget).",
  chk=("Not sure yet?", "Start with a ₹999 check", "30 minutes on your leads and listings, plus a one-page plan. Full refund if it isn’t useful.", "₹999", "Book the check"),
  chk_wa="Hi, I'm a property dealer. I want to book the ₹999 business AI check.",
  fine="Stop any month — or stop the ads and keep the secretary. Ad spend goes straight to Meta from your account; we suggest at least ₹15,000–20,000 a month. WhatsApp message charges are billed at actual cost.",
  f_eyebrow="FAQ", f_h2="Questions dealers ask",
  faq=[
       ("How many leads will I get?", "We won’t promise a number — it depends on your area, your listings and your ad budget. You’ll see leads, visits and cost per visit every week, and you can change the budget or stop anytime."),
       ("Who pays for the ads?", "You do, directly to Meta from an ad account in your name. Our fee covers making the ads, running them and tuning them every week."),
       ("Can I stop the ads and keep the secretary?", "Yes. Drop back to the ₹15,000 Secretary plan any month."),
       ("Will buyers know it’s not me?", "Messages go from your number, in your name and your tone. Anything serious — negotiation, a hot buyer, a complaint — comes straight to you."),
       ("Where does my lead data go?", "Into your own Google Sheet. It is never shared with portals or other dealers, and you can take it with you anytime."),
       ("Will it quote the wrong price?", "It only shares prices from your listing sheet. Discounts and negotiation always come to you."),
       ("Does it work with 99acres, MagicBricks and Housing.com?", "Yes. We connect the lead alerts you already get from them, plus your WhatsApp and Facebook leads."),
       ("Can it talk in Hindi?", "Yes — Hindi, English or Hinglish, whichever the buyer writes in."),
       ("What about RERA?", "Your RERA registration number appears on every listing card. It doesn’t give legal advice — those questions come to you.")],
  final_h2="Batao kaunsa area — hum dikhayenge kitne buyers wahan dhoondh rahe hain.",
  final_lead="Send us a voice note on WhatsApp with your area and the kind of property you sell. We’ll show you what your ads and your digital secretary would look like.",
  pricing_anchor="pricing",
 ),
 "hi": dict(
  title="प्रॉपर्टी डीलर के लिए नए खरीदार और ज़्यादा साइट विज़िट — ऐड + WhatsApp | सँभाल",
  desc="लोकल Instagram और Facebook ऐड से नए खरीदार, हर लीड को WhatsApp पर 1 मिनट में जवाब और ज़्यादा साइट विज़िट। भारत के प्रॉपर्टी डीलरों के लिए। ₹15,000/महीना से।",
  crumb="प्रॉपर्टी डीलर", home="होम",
  pill="प्रॉपर्टी डीलर के लिए नए खरीदार",
  h1='हर हफ़्ते ज़्यादा साइट विज़िट — <span class="hl">नए खरीदार भी,</span> पुरानी लीड भी।',
  h1_plain="हर हफ़्ते ज़्यादा साइट विज़िट — नए खरीदार भी, पुरानी लीड भी।",
  lead="हर नई लिस्टिंग को लोकल ऐड और पोस्ट में बदलते हैं, खरीदार सीधे आपके WhatsApp पर आते हैं, और आपका डिजिटल सेक्रेटरी 1 मिनट में जवाब देकर विज़िट बुक करता है।",
  cta="ज़्यादा साइट विज़िट पाएँ", price_link="प्लान ₹15,000/महीना से",
  salary="ऐड आपके नाम से। लीड आपकी अपनी शीट में। जब चाहें बंद करें।",
  wa="नमस्ते, मैं प्रॉपर्टी डीलर हूँ। मुझे सँभाल से नए खरीदार और ज़्यादा साइट विज़िट चाहिए।",
  note="नया खरीदार, सीधे WhatsApp पर ✓",
  chat=dict(name="अमित · Instagram ऐड", status="ऑनलाइन", me="शर्मा प्रॉपर्टीज़",
    m1="इंदिरापुरम में 3BHK चाहिए, बजट 1.2 करोड़ तक", t1="11:04 pm",
    m2="नमस्ते अमित जी! आपके बजट में 3 ऑप्शन हैं। पहला यह रहा 👇", t2="11:04 pm",
    card_t="3BHK बिल्डर फ़्लोर · नीति खंड", card_s="₹1.15 करोड़ · 1,650 वर्ग फ़ुट · पार्क फ़ेसिंग",
    m3="कल शाम 5 बजे देख सकते हैं?", t3="11:06 pm",
    m4="हो गया ✓ कल 5 बजे, नीति खंड। लोकेशन भेज रहा हूँ।", t4="11:06 pm"),
  lcard=("₹1.15 करोड़", "3BHK बिल्डर फ़्लोर · इंदिरापुरम", ["1,650 वर्ग फ़ुट", "पार्क फ़ेसिंग", "रेडी टू मूव"]),
  sponsored="स्पॉन्सर्ड · Instagram",
  toast=("साइट विज़िट बुक", "कल, शाम 5 बजे · नीति खंड"),
  works="खरीदार यहाँ से — और लीड यहाँ से —",
  q_eyebrow="क्या आपके साथ भी होता है?",
  quote="“पोर्टल पर हर महीने पैसा डालो — और वही लीड पाँच और डीलरों के पास भी जाती है।”",
  q_note="शेयर की हुई पोर्टल लीड में पहले मैसेज से ही रफ़्तार और दाम की होड़ होती है। अपने ऐड से आए अपने खरीदार कहीं ज़्यादा कीमती हैं।",
  pains=["शेयर की हुई पोर्टल लीड — पाँच डीलर एक ही खरीदार को फ़ोन करते हैं", "आप साइट विज़िट पर होते हैं, लीड जमा होती हैं — और सुबह तक ठंडी", "पिछले महीने की लीड को दोबारा कोई फ़ोन नहीं करता"],
  n_eyebrow="पहला कदम: नए खरीदार", n_h2="हम आपके लिए नए खरीदार कैसे लाते हैं",
  new=[("हर लिस्टिंग बनती है ऐड", "नया फ़्लैट आया? उसी दिन वह Instagram और Facebook पोस्ट, छोटी रील, WhatsApp स्टेटस और पोर्टल के लिए तैयार टेक्स्ट बन जाता है।", "उसी दिन"),
       ("लोकल ऐड जो WhatsApp खोलें", "आपके इलाके में छोटे ऐड — “इंदिरापुरम में 1.2 करोड़ तक 3BHK” — जो फ़ॉर्म नहीं, सीधे आपसे WhatsApp चैट खोलते हैं। सेक्रेटरी सेकंडों में जवाब देता है।", "1–2 हफ़्ते"),
       ("पुराने कॉन्टैक्ट फिर से जागें", "हज़ारों सेव नंबर और पुरानी पूछताछ — जब उनकी पसंद की प्रॉपर्टी आए, उन्हें सही मैसेज जाता है। सिर्फ़ उन्हें जिन्होंने हाँ कहा हो।", "कुछ ही दिन"),
       ("Google पर दिखें", "आपकी Google Business Profile पर हर हफ़्ते पोस्ट और हर डील के बाद रिव्यू की गुज़ारिश, ताकि “पास में प्रॉपर्टी डीलर” में आप दिखें।", "1–3 महीने")],
  seller=("बेचने वाले और मकान-मालिक भी।", "मालिकों से आपके पास प्रॉपर्टी लिस्ट कराने के कैंपेन — ज़्यादा इन्वेंटरी, ज़्यादा बिक्री।"),
  res_label="नतीजे",
  f_eyebrow2="पूरा सफ़र", f_h22="ऐड से बुक हुई विज़िट तक — आपके फ़ोन उठाए बिना",
  funnel=[("ऐड या पोस्ट", "Instagram, Facebook, Google"), ("WhatsApp चैट", "खरीदार टैप करे, चैट खुले"), ("&lt; 1 मिनट में जवाब", "बजट, इलाका, BHK"), ("विज़िट बुक", "टाइम, लोकेशन, रिमाइंडर"), ("फ़ॉलो-अप", "पुरानी लीड से मिलान")],
  funnel_mark="यहाँ से आपका डिजिटल सेक्रेटरी सँभालता है",
  b_eyebrow="दूसरा कदम: कोई लीड ठंडी नहीं", b_h2="फिर आपका डिजिटल सेक्रेटरी हर लीड सँभालता है",
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
  roi_h="तिमाही में दो डील ज़्यादा — और पूरा ख़र्च वसूल, ऐड समेत।",
  roi_p="₹1 करोड़ के फ़्लैट पर आपका 1% कमीशन ₹1 लाख होता है। लीड इंजन और ₹15,000 महीने का ऐड बजट मिलाकर तिमाही में लगभग ₹1.5 लाख।",
  s_eyebrow="कैसे काम करता है", s_h2="लगभग एक हफ़्ते में चालू",
  steps=[("अपनी लिस्टिंग भेजें", "Excel, Google Sheet या WhatsApp पर बस फ़ोटो। हम उन्हें लिस्टिंग कार्ड और ऐड बना देते हैं।"),
         ("ऐड बजट तय करें", "कितना ख़र्च करना है, आप तय करें। पैसा आपके नाम के ऐड अकाउंट से जाता है।"),
         ("ऐड चलें, सेक्रेटरी जवाब दे", "नए खरीदार आपके WhatsApp पर आते हैं, साथ में पोर्टल की लीड भी। हर एक को 1 मिनट में जवाब।"),
         ("हर हफ़्ते विज़िट रिपोर्ट", "हर सोमवार: लीड, बुक हुई विज़िट और ऐड से क्या मिला। एक असली एक्सपर्ट आपके साथ सुधारता है।")],
  own_eyebrow="भरोसा", own_h2="आपके लीड, आपके पास।",
  own=[("आपका नंबर, आपका नाम", "खरीदार को WhatsApp पर सिर्फ़ आपका बिज़नेस दिखता है — सँभाल नहीं।"),
       ("आपका ऐड अकाउंट", "ऐड आपके नाम के अकाउंट से चलते हैं। अकाउंट और उसका डेटा आपका, बंद करने के बाद भी।"),
       ("आपकी अपनी शीट में", "हर लीड आपकी Google Sheet में सेव होती है। जब चाहें ले जाइए।"),
       ("कभी शेयर नहीं", "न पोर्टल से, न दूसरे डीलरों से। कभी नहीं।")],
  p_eyebrow="दाम", p_h2="डीलरों के लिए दो प्लान। न कमीशन, न कॉन्ट्रैक्ट।",
  plan=("सेक्रेटरी", "जिन डीलरों के पास लीड पहले से काफ़ी हैं", "₹15,000", "/महीना",
        ["आपके WhatsApp नंबर पर डिजिटल सेक्रेटरी", "पोर्टल और WhatsApp लीड को 24×7 जवाब", "आपकी इन्वेंटरी से लिस्टिंग कार्ड",
         "साइट विज़िट बुकिंग और रिमाइंडर", "पुरानी लीड से मिलान और रात 9 बजे का सारांश", "हर महीने 8 घंटे एक्सपर्ट का समय"],
        "सेक्रेटरी चुनें"),
  plan_wa="नमस्ते, मैं प्रॉपर्टी डीलर हूँ। मुझे सँभाल के सेक्रेटरी प्लान (₹15,000/महीना) के बारे में जानना है।",
  plan2=("सेक्रेटरी + लीड इंजन", "जिन डीलरों को नए खरीदार चाहिए", "₹35,000", "/महीना + ऐड बजट",
        ["सेक्रेटरी प्लान का सब कुछ", "हर लिस्टिंग से पोस्ट, रील और ऐड", "लोकल WhatsApp ऐड, हर हफ़्ते सुधार के साथ",
         "पुराने कॉन्टैक्ट के कैंपेन और Google प्रोफ़ाइल पोस्ट", "बेचने वालों और मकान-मालिकों के कैंपेन", "हर हफ़्ते विज़िट रिपोर्ट · महीने में 20 घंटे एक्सपर्ट"],
        "ज़्यादा साइट विज़िट पाएँ", "हमारी सलाह"),
  plan2_wa="नमस्ते, मैं प्रॉपर्टी डीलर हूँ। मुझे सँभाल के सेक्रेटरी + लीड इंजन प्लान (₹35,000/महीना + ऐड बजट) के बारे में जानना है।",
  chk=("अभी पक्का नहीं?", "₹999 की जाँच से शुरू करें", "आपकी लीड और लिस्टिंग पर 30 मिनट की बात, और एक पन्ने का प्लान। काम का न लगे तो पूरा पैसा वापस।", "₹999", "जाँच बुक करें"),
  chk_wa="नमस्ते, मैं प्रॉपर्टी डीलर हूँ। मुझे ₹999 की बिज़नेस AI जाँच बुक करनी है।",
  fine="किसी भी महीने बंद करें — या ऐड बंद करके सेक्रेटरी रखें। ऐड का पैसा आपके अकाउंट से सीधे Meta को जाता है; हम कम से कम ₹15,000–20,000 महीना सुझाते हैं। WhatsApp मैसेज का ख़र्च असल दाम पर अलग से।",
  f_eyebrow="सवाल-जवाब", f_h2="डीलर अक्सर पूछते हैं",
  faq=[
       ("मुझे कितनी लीड मिलेंगी?", "हम कोई गिनती का वादा नहीं करते — यह आपके इलाके, लिस्टिंग और ऐड बजट पर निर्भर है। हर हफ़्ते आपको लीड, विज़िट और हर विज़िट का ख़र्च दिखेगा, और बजट कभी भी बदलें या बंद करें।"),
       ("ऐड का पैसा कौन देता है?", "आप, अपने नाम के ऐड अकाउंट से सीधे Meta को। हमारी फ़ीस ऐड बनाने, चलाने और हर हफ़्ते सुधारने की है।"),
       ("क्या ऐड बंद करके सेक्रेटरी रख सकता हूँ?", "हाँ। किसी भी महीने ₹15,000 के सेक्रेटरी प्लान पर लौट आइए।"),
       ("क्या खरीदार को पता चलेगा कि यह मैं नहीं हूँ?", "मैसेज आपके नंबर से, आपके नाम और आपके अंदाज़ में जाते हैं। कोई भी ज़रूरी बात — मोलभाव, गर्म खरीदार, शिकायत — सीधे आपके पास आती है।"),
       ("मेरी लीड का डेटा कहाँ जाता है?", "आपकी अपनी Google Sheet में। यह कभी पोर्टल या दूसरे डीलरों से शेयर नहीं होता, और आप इसे जब चाहें ले जा सकते हैं।"),
       ("कहीं गलत दाम तो नहीं बता देगा?", "यह सिर्फ़ आपकी लिस्टिंग शीट के दाम बताता है। छूट और मोलभाव हमेशा आपके पास आते हैं।"),
       ("क्या यह 99acres, MagicBricks और Housing.com के साथ चलता है?", "हाँ। उनसे जो लीड अलर्ट आपको पहले से आते हैं, उन्हें हम जोड़ देते हैं — साथ में WhatsApp और Facebook की लीड भी।"),
       ("क्या यह हिंदी में बात करता है?", "हाँ — हिंदी, अंग्रेज़ी या हिंग्लिश, जिसमें खरीदार लिखे।"),
       ("RERA का क्या?", "हर लिस्टिंग कार्ड पर आपका RERA रजिस्ट्रेशन नंबर दिखता है। यह कानूनी सलाह नहीं देता — ऐसे सवाल आपके पास आते हैं।")],
  final_h2="बताइए कौन-सा इलाका — हम दिखाएँगे वहाँ कितने खरीदार ढूँढ रहे हैं।",
  final_lead="WhatsApp पर एक वॉइस नोट भेजिए — आपका इलाका और आप कैसी प्रॉपर्टी बेचते हैं। हम दिखाएँगे कि आपके ऐड और डिजिटल सेक्रेटरी कैसे दिखेंगे।",
  pricing_anchor="daam",
 ),
}

PORTALS = ["Instagram", "Facebook", "Google", "99acres", "MagicBricks", "Housing.com", "WhatsApp"]
PAIN_ICO = [ic('<path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.4 8.4 0 1 1 21 11.5z"/><path d="M12 8v4l2.5 1.5"/>'),
            ic('<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><path d="M14 17.5h7M17.5 14v7"/>'),
            ic('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/><path d="M16 2l6 6M22 2l-6 6"/>')]
STEP_ICO = [ICON["link"], ic('<circle cx="12" cy="12" r="9"/><path d="M14.8 9.2a3 3 0 0 0-2.8-1.7c-1.7 0-2.8.9-2.8 2.2 0 3 5.6 1.6 5.6 4.6 0 1.3-1.2 2.2-2.8 2.2a3 3 0 0 1-2.9-1.8M12 6v1.5M12 16.5V18"/>', 24), ICON["send"], ICON["check"]]
NEW_ICO = [ic('<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/>'),
           ic('<path d="M3 11v2a1 1 0 0 0 1 1h2l5 4V6L6 10H4a1 1 0 0 0-1 1z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M18.5 5.5a9 9 0 0 1 0 13"/>'),
           ic('<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M17 11l2 2 3.5-3.5"/>'),
           ic('<path d="M12 21s-7-6.1-7-11.5a7 7 0 0 1 14 0C19 14.9 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>')]
SELLER_ICO = ic('<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>')
OWN_ICO = [ic('<path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.4 8.4 0 1 1 21 11.5z"/>', 22),
           ic('<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/>', 22),
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
    newcards = "\n".join(f'        <article class="dk-new"><span class="ico">{NEW_ICO[i]}</span><h3>{t}</h3><p>{d}</p><span class="dk-when">{c["res_label"]}: <b>{w}</b></span></article>'
                         for i, (t, d, w) in enumerate(c["new"]))
    funnel = "".join(f'<li class="{"dk-sec" if i >= 2 else ""}"><b>{t}</b><span>{d}</span></li>' for i, (t, d) in enumerate(c["funnel"]))
    p2 = c["plan2"]
    plan2_items = "".join(f"<li>{TICK}{x}</li>" for x in p2[4])

    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url(lang, SLUG) + "#webpage", "url": url(lang, SLUG), "name": c["title"],
         "description": c["desc"], "inLanguage": "en-IN" if lang == "en" else "hi-IN",
         "isPartOf": {"@id": D + "/#website"}, "breadcrumb": {"@id": url(lang, SLUG) + "#breadcrumb"}},
        {"@type": "Service", "name": c["pill"], "serviceType": "Lead generation and WhatsApp lead response for real estate agents",
         "description": c["lead"], "audience": {"@type": "BusinessAudience", "audienceType": "Real estate agents and property dealers"},
         "provider": {"@type": "Organization", "@id": D + "/#org", "name": "Sambhal", "url": D + "/", "telephone": "+91-9873470074"},
         "areaServed": {"@type": "Country", "name": "India"},
         "offers": [{"@type": "Offer", "name": pl[0], "price": "15000", "priceCurrency": "INR",
                     "priceSpecification": {"@type": "UnitPriceSpecification", "price": "15000", "priceCurrency": "INR", "unitText": "MONTH"}},
                    {"@type": "Offer", "name": c["plan2"][0], "price": "35000", "priceCurrency": "INR",
                     "priceSpecification": {"@type": "UnitPriceSpecification", "price": "35000", "priceCurrency": "INR", "unitText": "MONTH"}},
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
        <div class="dk-lcard" aria-hidden="true">{pic("floor", "", "260px", "", True, 1200, 800)}<div><small class="dk-spon">{c["sponsored"]}</small><b>{lc[0]}</b><span>{lc[1]}</span><ul class="dk-chips">{chips(lc[2])}</ul></div></div>
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

  <section class="dk-new-sec">
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow">{c["n_eyebrow"]}</span>
        <h2>{c["n_h2"]}</h2>
      </div>
      <div class="dk-new-grid">
{newcards}
      </div>
      <div class="dk-seller"><span class="ico">{SELLER_ICO}</span><p><strong>{c["seller"][0]}</strong> {c["seller"][1]}</p></div>
    </div>
  </section>

  <section class="dk-funnel-sec">
    <div class="wrap">
      <div class="section-head center">
        <span class="eyebrow">{c["f_eyebrow2"]}</span>
        <h2>{c["f_h22"]}</h2>
      </div>
      <ol class="dk-funnel">{funnel}</ol>
      <p class="dk-funnel-mark"><span>{c["funnel_mark"]}</span></p>
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
        <div class="plan">
          <p class="plan-name">{pl[0]}</p>
          <p class="plan-for">{pl[1]}</p>
          <p class="plan-price"><b>{pl[2]}</b><span>{pl[3]}</span></p>
          <ul>{plan_items}</ul>
          <a class="btn btn-outline" data-cta="plan-dealer-secretary" href="{WA}{urllib.parse.quote(c["plan_wa"])}">{pl[5]}</a>
        </div>
        <div class="plan featured">
          <span class="badge">{p2[6]}</span>
          <p class="plan-name">{p2[0]}</p>
          <p class="plan-for">{p2[1]}</p>
          <p class="plan-price"><b>{p2[2]}</b><span>{p2[3]}</span></p>
          <ul>{plan2_items}</ul>
          <a class="btn btn-accent" data-cta="plan-dealer-lead-engine" href="{WA}{urllib.parse.quote(c["plan2_wa"])}">{p2[5]}</a>
        </div>
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
