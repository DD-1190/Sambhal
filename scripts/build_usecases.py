"""Generate the use-case landing pages (English at /<slug>, Hindi at /hi/<slug>).

Run:  python3 scripts/build_usecases.py && python3 scripts/stamp_assets.py
Header, phone chat and final call-to-action are taken from the two home pages,
so the use-case pages always match the main site.
"""
import json, pathlib, re, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = "https://www.sambhalhub.in"
WA = "https://wa.me/919873470074?text="


def ic(d, w=22, sw=2):
    return (f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>')

ICON = {
    "msg": ic('<path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.4 8.4 0 1 1 21 11.5z"/><path d="M12 8v4l2.5 1.5"/>'),
    "table": ic('<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M3 15h18M9 4v16"/>'),
    "bell": ic('<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.9 1.9 0 0 0 3.4 0"/>'),
    "link": ic('<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>', 24),
    "send": ic('<path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4z"/>', 24),
    "check": ic('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>', 24),
    "chat": ic('<path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.4 8.4 0 1 1 21 11.5z"/>', 22),
    "plus": ic('<path d="M12 5v14M5 12h14"/>', 18),
    "arrow": ic('<path d="M5 12h14M13 6l6 6-6 6"/>', 18),
}
PAIN_ICONS = ["msg", "table", "bell"]
STEP_ICONS = ["link", "send", "check"]

UI = {
    "en": dict(home="Home", pains="Sound familiar?", how="How it works", who="Who it's for",
               faq="Questions", more="Other jobs Sambhal handles", cta="Chat on WhatsApp",
               check="See the ₹999 business check →", step="STEP", eyebrow_pains="EVERYDAY PROBLEMS",
               eyebrow_how="HOW IT WORKS", eyebrow_faq="FAQ", learn="See how it works"),
    "hi": dict(home="होम", pains="क्या आपके साथ भी होता है?", how="कैसे काम करता है", who="किसके लिए है",
               faq="सवाल-जवाब", more="सँभाल और क्या-क्या सँभालता है", cta="WhatsApp पर बात करें",
               check="₹999 की बिज़नेस जाँच देखें →", step="कदम", eyebrow_pains="रोज़ की परेशानी",
               eyebrow_how="कैसे काम करता है", eyebrow_faq="सवाल-जवाब", learn="कैसे काम करता है, देखें"),
}

PAGES = [
  {
    "slug": "whatsapp-payment-reminders", "slide": "uc-2",
    "en": dict(
      title="Automatic Payment Reminders on WhatsApp for Small Businesses | Sambhal",
      desc="Send polite payment reminders on WhatsApp automatically, with a UPI pay link and receipt. Set up and looked after by Sambhal. Start with a ₹999 check.",
      eyebrow="Payment reminders", card="Payment reminders on WhatsApp",
      h1="Payment reminders on WhatsApp — sent on time, every time.",
      lead="Sambhal reads your pending bills from Tally or Excel and sends each customer a polite WhatsApp reminder with a UPI link. When they pay, the receipt goes out on its own — and you stop chasing.",
      wa="Hi, I want automatic payment reminders on WhatsApp for my business.",
      pains=["You call the same customers again and again for payment", "Staff forget which bills are due this week", "Awkward follow-ups strain good relationships"],
      steps=[("We connect your bills", "From Tally, Busy, Excel or Google Sheets. Nothing new for your staff to learn."),
             ("Reminders go out on schedule", "A polite message before the due date, on the day and after — in Hindi or English, with a UPI pay link."),
             ("Payment in, receipt out", "Paid bills are marked on their own, and every evening you get a list of what's still pending.")],
      who=["Traders", "Distributors", "Wholesalers", "Factories", "CA firms", "Coaching institutes"],
      faq=[("Will my customers feel harassed?", "No. You choose the tone and how often. Messages are polite and stop as soon as the bill is paid."),
           ("Do I need to set up anything technical?", "No. We handle the setup. Reminders go from your business number, and we explain any WhatsApp charges upfront."),
           ("Does it work with Tally?", "Yes. We can read pending bills from Tally, Busy, Excel or Google Sheets.")]),
    "hi": dict(
      title="WhatsApp पर अपने आप पेमेंट रिमाइंडर — छोटे बिज़नेस के लिए | सँभाल",
      desc="बकाया बिलों के लिए WhatsApp पर विनम्र पेमेंट रिमाइंडर, UPI लिंक और रसीद — अपने आप। सेटअप और देखभाल सँभाल की। ₹999 की जाँच से शुरुआत करें।",
      eyebrow="पेमेंट रिमाइंडर", card="WhatsApp पर पेमेंट रिमाइंडर",
      h1="WhatsApp पर पेमेंट रिमाइंडर — समय पर, हर बार।",
      lead="सँभाल आपके Tally या Excel से बकाया बिल पढ़ता है और हर ग्राहक को UPI लिंक के साथ विनम्र WhatsApp रिमाइंडर भेजता है। पेमेंट आते ही रसीद अपने आप चली जाती है — और आपको फ़ोन नहीं करने पड़ते।",
      wa="नमस्ते, मुझे अपने बिज़नेस के लिए WhatsApp पर अपने आप पेमेंट रिमाइंडर चाहिए।",
      pains=["एक ही ग्राहक को पेमेंट के लिए बार-बार फ़ोन करना पड़ता है", "स्टाफ़ भूल जाता है कि इस हफ़्ते कौन से बिल ड्यू हैं", "बार-बार माँगने से अच्छे रिश्ते ख़राब होते हैं"],
      steps=[("हम आपके बिल जोड़ते हैं", "Tally, Busy, Excel या Google Sheets से। स्टाफ़ को कुछ नया नहीं सीखना।"),
             ("रिमाइंडर समय पर जाते हैं", "ड्यू डेट से पहले, उस दिन और बाद में — हिंदी या इंग्लिश में, UPI लिंक के साथ।"),
             ("पेमेंट आया, रसीद गई", "भरे गए बिल अपने आप मार्क होते हैं, और हर शाम आपको बचे हुए बकाये की लिस्ट मिलती है।")],
      who=["ट्रेडर", "डिस्ट्रीब्यूटर", "होलसेलर", "फ़ैक्ट्री", "CA फ़र्म", "कोचिंग"],
      faq=[("क्या ग्राहक परेशान तो नहीं होंगे?", "नहीं। लहजा और कितनी बार भेजना है, यह आप तय करते हैं। पेमेंट होते ही मैसेज बंद।"),
           ("क्या मुझे कुछ टेक्निकल सेट करना होगा?", "नहीं। सेटअप हम करते हैं। रिमाइंडर आपके बिज़नेस नंबर से जाते हैं, और WhatsApp का ख़र्च हम पहले ही बता देते हैं।"),
           ("क्या यह Tally के साथ चलेगा?", "हाँ। Tally, Busy, Excel या Google Sheets — कहीं से भी बकाया बिल पढ़ सकते हैं।")]),
  },
  {
    "slug": "whatsapp-quotations", "slide": "uc-1",
    "en": dict(
      title="Send Quotations on WhatsApp Automatically | Sambhal",
      desc="Reply to every enquiry in minutes with a quotation PDF built from your own price list — even at 11 pm. WhatsApp quotations for Indian businesses.",
      eyebrow="Quotations", card="Quotations on WhatsApp",
      h1="Every enquiry gets a quotation in minutes — even at 11 pm.",
      lead="Sambhal answers rate enquiries on your WhatsApp, builds a quotation PDF from your own price list and sends it while the customer is still interested. You review big orders; the rest runs on its own.",
      wa="Hi, I want to send quotations on WhatsApp automatically.",
      pains=["Leads ask for rates and go cold before anyone replies", "Quotations take hours to make by hand", "Prices and discounts change depending on who replies"],
      steps=[("Share your price list", "Excel, PDF or even a photo. We set up your products, rates, discounts and GST."),
             ("Enquiries get instant replies", "The AI asks for quantity and delivery details, then sends a quotation PDF with your name on it."),
             ("You close the deal", "Hot leads and big orders come to you with the full chat, so you step in at the right moment.")],
      who=["Distributors", "Manufacturers", "Wholesalers", "Printing & packaging", "Building materials", "Event suppliers"],
      faq=[("Can I check quotations before they go?", "Yes. Approve every quotation, only big orders, or let routine ones go straight out — your choice."),
           ("Will it quote the wrong price?", "It only uses your price list and your discount rules. Anything outside them comes to you."),
           ("Can it reply in Hindi?", "Yes — in Hindi, English or Hinglish, whichever the customer writes in.")]),
    "hi": dict(
      title="WhatsApp पर अपने आप कोटेशन भेजें | सँभाल",
      desc="हर पूछताछ का जवाब मिनटों में, आपकी प्राइस लिस्ट से बना कोटेशन PDF — रात 11 बजे भी। भारतीय बिज़नेस के लिए WhatsApp कोटेशन, सँभाल के साथ।",
      eyebrow="कोटेशन", card="WhatsApp पर कोटेशन",
      h1="हर पूछताछ को मिनटों में कोटेशन — रात 11 बजे भी।",
      lead="सँभाल आपके WhatsApp पर रेट की पूछताछ का जवाब देता है, आपकी अपनी प्राइस लिस्ट से कोटेशन PDF बनाता है और ग्राहक की दिलचस्पी रहते ही भेज देता है। बड़े ऑर्डर आप देखते हैं, बाक़ी अपने आप।",
      wa="नमस्ते, मुझे WhatsApp पर अपने आप कोटेशन भेजने हैं।",
      pains=["रेट पूछकर ग्राहक जवाब आने से पहले ठंडा पड़ जाता है", "कोटेशन हाथ से बनाने में घंटों लगते हैं", "कौन जवाब दे रहा है, उसके हिसाब से रेट और डिस्काउंट बदल जाते हैं"],
      steps=[("प्राइस लिस्ट भेजिए", "Excel, PDF या फ़ोटो भी। प्रोडक्ट, रेट, डिस्काउंट और GST हम सेट करते हैं।"),
             ("पूछताछ का तुरंत जवाब", "AI मात्रा और डिलीवरी पूछता है, फिर आपके नाम का कोटेशन PDF भेजता है।"),
             ("डील आप पक्की करें", "गर्म लीड और बड़े ऑर्डर पूरी चैट के साथ आपके पास आते हैं, ताकि आप सही समय पर बात करें।")],
      who=["डिस्ट्रीब्यूटर", "मैन्युफ़ैक्चरर", "होलसेलर", "प्रिंटिंग और पैकेजिंग", "बिल्डिंग मटीरियल", "इवेंट सप्लायर"],
      faq=[("क्या कोटेशन जाने से पहले मैं देख सकता हूँ?", "हाँ। हर कोटेशन, सिर्फ़ बड़े ऑर्डर, या रूटीन वाले सीधे — जैसा आप चाहें।"),
           ("कहीं ग़लत रेट तो नहीं बता देगा?", "यह सिर्फ़ आपकी प्राइस लिस्ट और डिस्काउंट के नियम इस्तेमाल करता है। उसके बाहर की बात आपके पास आती है।"),
           ("क्या यह हिंदी में जवाब देगा?", "हाँ — हिंदी, इंग्लिश या हिंग्लिश, ग्राहक जिसमें लिखे।")]),
  },
  {
    "slug": "daily-sales-report-whatsapp", "slide": "uc-3",
    "en": dict(
      title="Daily Sales Report on WhatsApp from Tally or Excel | Sambhal",
      desc="Get today's sales, new orders, pending payments and low stock on WhatsApp every evening — straight from Tally or Excel. No dashboards to learn.",
      eyebrow="Daily report", card="Daily sales report on WhatsApp",
      h1="Your whole day's numbers on WhatsApp, every evening at 7.",
      lead="Sambhal pulls sales, orders, pending payments and stock from Tally or Excel and sends you a short report on WhatsApp. Ask a follow-up question in plain Hindi or English and get the answer in seconds.",
      wa="Hi, I want a daily sales report on WhatsApp for my business.",
      pains=["You ask staff for the numbers every evening", "Getting reports out of Tally needs someone who knows Tally", "Low stock is noticed only when a customer asks"],
      steps=[("We connect your data", "Tally, Busy, Excel or Google Sheets — wherever your numbers already live."),
             ("You choose what matters", "Sales, collections, pending payments, stock — by staff member or by branch."),
             ("The report arrives on WhatsApp", "Every evening, or weekly. Ask “which items are low?” and get the answer straight away.")],
      who=["Shop owners", "Distributors", "Factories", "Multi-branch businesses", "Restaurants"],
      faq=[("Do I need to change my software?", "No. We work with what you already use."),
           ("Is my data safe?", "Your data is used only for your reports. Access is limited and ends when you stop."),
           ("Can my partner get the report too?", "Yes. It can go to you, partners or managers — each sees only what you allow.")]),
    "hi": dict(
      title="Tally या Excel से रोज़ की सेल्स रिपोर्ट WhatsApp पर | सँभाल",
      desc="आज की बिक्री, नए ऑर्डर, बकाया पेमेंट और कम स्टॉक — हर शाम आपके WhatsApp पर, सीधे Tally या Excel से। कोई डैशबोर्ड सीखना नहीं।",
      eyebrow="रोज़ की रिपोर्ट", card="WhatsApp पर रोज़ की रिपोर्ट",
      h1="दिन का पूरा हिसाब, हर शाम 7 बजे आपके WhatsApp पर।",
      lead="सँभाल Tally या Excel से बिक्री, ऑर्डर, बकाया और स्टॉक निकालकर आपको WhatsApp पर छोटी-सी रिपोर्ट भेजता है। आगे कुछ पूछना हो तो सीधे हिंदी या इंग्लिश में पूछिए — जवाब सेकंडों में।",
      wa="नमस्ते, मुझे अपने बिज़नेस की रोज़ की सेल्स रिपोर्ट WhatsApp पर चाहिए।",
      pains=["हर शाम स्टाफ़ से हिसाब पूछना पड़ता है", "Tally से रिपोर्ट निकालने के लिए Tally जानने वाला चाहिए", "स्टॉक कम है, यह तब पता चलता है जब ग्राहक माँगता है"],
      steps=[("हम आपका डेटा जोड़ते हैं", "Tally, Busy, Excel या Google Sheets — जहाँ आपके आँकड़े पहले से हैं।"),
             ("आप तय करें क्या देखना है", "बिक्री, वसूली, बकाया, स्टॉक — स्टाफ़ या ब्रांच के हिसाब से।"),
             ("रिपोर्ट WhatsApp पर आती है", "हर शाम या हफ़्ते में। “कौन सा माल कम है?” पूछिए, जवाब तुरंत।")],
      who=["दुकानदार", "डिस्ट्रीब्यूटर", "फ़ैक्ट्री", "कई ब्रांच वाले बिज़नेस", "रेस्टोरेंट"],
      faq=[("क्या सॉफ़्टवेयर बदलना पड़ेगा?", "नहीं। आप जो इस्तेमाल करते हैं, हम उसी के साथ काम करते हैं।"),
           ("क्या मेरा डेटा सुरक्षित है?", "आपका डेटा सिर्फ़ आपकी रिपोर्ट के लिए इस्तेमाल होता है। एक्सेस सीमित है और काम बंद होते ही ख़त्म।"),
           ("क्या मेरे पार्टनर को भी रिपोर्ट मिल सकती है?", "हाँ। आपको, पार्टनर या मैनेजर को — हर किसी को उतना ही दिखेगा जितना आप चाहें।")]),
  },
  {
    "slug": "whatsapp-appointment-booking", "slide": "uc-4",
    "en": dict(
      title="WhatsApp Appointment Booking & Reminders for Clinics | Sambhal",
      desc="Let patients and students book slots on WhatsApp, get a reminder before the visit and reschedule on their own. Fewer no-shows, fewer phone calls.",
      eyebrow="Appointments", card="Appointments on WhatsApp",
      h1="Bookings and reminders on WhatsApp — without a single phone call.",
      lead="Patients, students and buyers pick a free slot on WhatsApp. Sambhal confirms it, reminds them an hour before and handles rescheduling — so your front desk can focus on the people in front of them.",
      wa="Hi, I want appointment booking and reminders on WhatsApp.",
      pains=["The phone rings all day for appointments", "No-shows waste doctors' and teachers' time", "Double bookings happen when two people share one diary"],
      steps=[("Set your timings", "Working hours, slot length, breaks and holidays — we set it up with you."),
             ("Customers book on WhatsApp", "They see free slots, pick one and get a confirmation instantly."),
             ("Reminders do the rest", "A reminder before the visit, easy rescheduling, and a daily list for your front desk.")],
      who=["Clinics", "Diagnostic centres", "Coaching institutes", "Salons", "Property site visits", "Service centres"],
      faq=[("Can it use my existing calendar?", "Yes. We can connect Google Calendar or keep a simple shared sheet."),
           ("What if a patient wants to talk to someone?", "They can ask for a person any time, and your staff take over the chat."),
           ("Does it work in Hindi?", "Yes — in Hindi, English or Hinglish.")]),
    "hi": dict(
      title="WhatsApp पर अपॉइंटमेंट बुकिंग और रिमाइंडर — क्लिनिक के लिए | सँभाल",
      desc="मरीज़ और स्टूडेंट WhatsApp पर ख़ुद स्लॉट बुक करें, आने से पहले रिमाइंडर पाएँ और समय बदलें। कम नो-शो, कम फ़ोन कॉल।",
      eyebrow="अपॉइंटमेंट", card="WhatsApp पर अपॉइंटमेंट",
      h1="बुकिंग और रिमाइंडर WhatsApp पर — बिना एक भी फ़ोन कॉल के।",
      lead="मरीज़, स्टूडेंट या ख़रीदार WhatsApp पर ख़ाली स्लॉट चुनते हैं। सँभाल बुकिंग कन्फ़र्म करता है, एक घंटा पहले याद दिलाता है और समय बदलना भी सँभालता है — ताकि आपका रिसेप्शन सामने वाले लोगों पर ध्यान दे सके।",
      wa="नमस्ते, मुझे WhatsApp पर अपॉइंटमेंट बुकिंग और रिमाइंडर चाहिए।",
      pains=["अपॉइंटमेंट के लिए दिन भर फ़ोन बजता रहता है", "नो-शो से डॉक्टर और टीचर का समय बर्बाद होता है", "दो लोग एक डायरी सँभालें तो डबल बुकिंग हो जाती है"],
      steps=[("अपना समय बताइए", "काम के घंटे, स्लॉट कितनी देर का, ब्रेक और छुट्टियाँ — हम आपके साथ सेट करते हैं।"),
             ("ग्राहक WhatsApp पर बुक करें", "ख़ाली स्लॉट देखें, एक चुनें और तुरंत कन्फ़र्मेशन पाएँ।"),
             ("बाक़ी काम रिमाइंडर का", "आने से पहले याद-दिहानी, आसानी से समय बदलना, और रिसेप्शन के लिए रोज़ की लिस्ट।")],
      who=["क्लिनिक", "डायग्नोस्टिक सेंटर", "कोचिंग", "सैलून", "प्रॉपर्टी साइट विज़िट", "सर्विस सेंटर"],
      faq=[("क्या यह मेरे मौजूदा कैलेंडर से जुड़ेगा?", "हाँ। Google Calendar से जोड़ सकते हैं या एक आसान शेयर्ड शीट रख सकते हैं।"),
           ("अगर मरीज़ किसी इंसान से बात करना चाहे?", "वे कभी भी इंसान से बात माँग सकते हैं, और आपका स्टाफ़ चैट सँभाल लेता है।"),
           ("क्या यह हिंदी में चलेगा?", "हाँ — हिंदी, इंग्लिश या हिंग्लिश में।")]),
  },
]


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def url(lang, slug=""):
    if lang == "en":
        return f"{D}/{slug}" if slug else f"{D}/"
    return f"{D}/hi/{slug}" if slug else f"{D}/hi"


def path(lang, slug=""):
    if lang == "en":
        return f"/{slug}" if slug else "/"
    return f"/hi/{slug}" if slug else "/hi"


def grab(html, pattern):
    m = re.search(pattern, html, re.S)
    assert m, pattern
    return m.group(0)


def build(page, lang, home_html):
    c, ui, slug = page[lang], UI[lang], page["slug"]
    other = "hi" if lang == "en" else "en"
    org = '{"@id":"' + D + '/#org"}'

    # pieces shared with the home page
    header = grab(home_html, r'<header class="site-header">.*?</header>')
    header = header.replace(f'class="lang" href="{path(other)}"', f'class="lang" href="{path(other, slug)}"')
    final = grab(home_html, r'<section class="final">.*?</section>')
    final = re.sub(r'href="https://wa\.me/919873470074\?text=[^"]*"',
                   f'href="{WA}{urllib.parse.quote(c["wa"])}"', final, count=1)
    final = final.replace('href="/" aria-label', f'href="{path(lang)}" aria-label')
    phone = grab(home_html, r'<div class="phone">.*?</div>\n          </div>\n        </div>')
    # keep only this page's chat, shown
    slides = re.findall(r'<article class="slide[^"]*" id="(uc-\d)".*?</article>', phone, re.S)
    for sid in slides:
        art = re.search(rf'<article class="slide[^"]*" id="{sid}".*?</article>', phone, re.S).group(0)
        if sid == page["slide"]:
            new = re.sub(r'<article class="slide[^"]*" id="uc-\d"[^>]*>', '<article class="slide is-active">', art, count=1)
            phone = phone.replace(art, new)
        else:
            phone = phone.replace(art, "")
    phone = re.sub(r'\n\s*\n+', '\n', phone).replace(' aria-live="polite"', '')

    head_home = grab(home_html, r'<head>.*?</head>')
    fonts = grab(head_home, r'  <link rel="preconnect" href="https://fonts.googleapis.com">.*?</head>').replace("</head>", "")

    pains = "\n".join(f'        <li class="pain"><span class="ico">{ICON[PAIN_ICONS[i]]}</span><p>{p}</p></li>' for i, p in enumerate(c["pains"]))
    steps = "\n".join(
        f'        <li class="step">\n          <span class="step-ico">{ICON[STEP_ICONS[i]]}</span>\n'
        f'          <div><p class="step-num">{ui["step"]} {i + 1}</p><h3>{t}</h3><p>{d}</p></div>\n        </li>'
        for i, (t, d) in enumerate(c["steps"]))
    who = "".join(f"<li>{w}</li>" for w in c["who"])
    faqs = "\n".join(f'        <details>\n          <summary>{q}{ICON["plus"]}</summary>\n          <p>{a}</p>\n        </details>' for q, a in c["faq"])
    others = "\n".join(
        f'        <a class="uc-card" href="{path(lang, p["slug"])}"><span class="eyebrow">{p[lang]["eyebrow"]}</span>'
        f'<strong>{p[lang]["card"]}</strong>{ICON["arrow"]}</a>'
        for p in PAGES if p["slug"] != slug)

    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url(lang, slug) + "#webpage", "url": url(lang, slug), "name": c["title"],
         "description": c["desc"], "inLanguage": "en-IN" if lang == "en" else "hi-IN",
         "isPartOf": {"@id": D + "/#website"}, "breadcrumb": {"@id": url(lang, slug) + "#breadcrumb"}},
        {"@type": "Service", "name": c["card"], "serviceType": c["eyebrow"], "description": c["lead"],
         "provider": {"@type": "Organization", "@id": D + "/#org", "name": "Sambhal", "url": D + "/", "telephone": "+91-9873470074"},
         "areaServed": {"@type": "Country", "name": "India"},
         "offers": {"@type": "Offer", "name": "Business AI check" if lang == "en" else "बिज़नेस AI जाँच", "price": "999", "priceCurrency": "INR"}},
        {"@type": "BreadcrumbList", "@id": url(lang, slug) + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": ui["home"], "item": url(lang)},
            {"@type": "ListItem", "position": 2, "name": c["eyebrow"], "item": url(lang, slug)}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c["faq"]]},
    ]}
    ld = json.dumps(graph, ensure_ascii=False, indent=1).replace("</", "<\\/")
    og = f"{D}/assets/og-image{'-hi' if lang == 'hi' else ''}.png"

    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(c["title"])}</title>
  <meta name="description" content="{esc(c["desc"])}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="#232E66">
  <link rel="canonical" href="{url(lang, slug)}">
  <link rel="alternate" hreflang="en-IN" href="{url("en", slug)}">
  <link rel="alternate" hreflang="hi-IN" href="{url("hi", slug)}">
  <link rel="alternate" hreflang="x-default" href="{url("en", slug)}">

  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/assets/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Sambhal">
  <meta property="og:url" content="{url(lang, slug)}">
  <meta property="og:title" content="{esc(c["h1"])}">
  <meta property="og:description" content="{esc(c["desc"])}">
  <meta property="og:image" content="{og}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(c["h1"])}">
  <meta name="twitter:description" content="{esc(c["desc"])}">
  <meta name="twitter:image" content="{og}">

  <script type="application/ld+json">
{ld}
  </script>

{fonts}</head>
<body>

{header}

<main>

  <section class="hero hero--uc">
    <div class="wrap hero-grid">
      <div class="hero-copy">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="{path(lang)}">{ui["home"]}</a><span aria-hidden="true">/</span><span>{c["eyebrow"]}</span></nav>
        <p class="pill">{c["eyebrow"]}</p>
        <h1>{c["h1"]}</h1>
        <p class="lead">{c["lead"]}</p>
        <div class="hero-actions">
          <a class="btn btn-primary" data-cta="whatsapp-{slug}" href="{WA}{urllib.parse.quote(c["wa"])}">
            {ICON["chat"]}
            {ui["cta"]}
          </a>
          <a class="link-arrow" href="{path(lang)}#{'daam' if lang == 'hi' else 'pricing'}">{ui["check"]}</a>
        </div>
      </div>

      <div class="showcase">
        {phone}
      </div>
    </div>
  </section>

  <section class="pains">
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow">{ui["eyebrow_pains"]}</span>
        <h2>{ui["pains"]}</h2>
      </div>
      <ul class="pain-grid">
{pains}
      </ul>
      <div class="uc-who">
        <p class="uc-who-label">{ui["who"]}</p>
        <ul class="uc-who-chips">{who}</ul>
      </div>
    </div>
  </section>

  <section class="steps">
    <div class="wrap">
      <div class="section-head center">
        <span class="eyebrow">{ui["eyebrow_how"]}</span>
        <h2>{ui["how"]}</h2>
      </div>
      <ol class="step-grid">
{steps}
      </ol>
    </div>
  </section>

  <section class="faq faq--uc">
    <div class="wrap faq-grid">
      <div>
        <span class="eyebrow">{ui["eyebrow_faq"]}</span>
        <h2>{ui["faq"]}</h2>
      </div>
      <div>
{faqs}
      </div>
    </div>
  </section>

  <section class="uc-more">
    <div class="wrap">
      <h2>{ui["more"]}</h2>
      <div class="uc-cards">
{others}
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
    homes = {"en": (ROOT / "index.html").read_text(encoding="utf-8"),
             "hi": (ROOT / "hi" / "index.html").read_text(encoding="utf-8")}
    for page in PAGES:
        for lang in ("en", "hi"):
            out = ROOT / (page["slug"] if lang == "en" else f"hi/{page['slug']}") / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(build(page, lang, homes[lang]), encoding="utf-8")
            print("built", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
