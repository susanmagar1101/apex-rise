"""Builds the Apex Rise site pages with one shared head, top bar and footer.

Run from anywhere:  python _build/build.py
It writes the plain static HTML pages, sitemap.xml and vercel.json into the site folder.
Projects for the Our Work page come from _build/projects.json (see _build/README.md).
Needs Python 3 only (no extra packages)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent  # the site folder (one level above _build)
BASE = "https://apexriseits.vercel.app"
NAME = "Apex Rise IT Solution"

NAV = [("/", "Home"), ("/services", "Services"), ("/work", "Our Work"), ("/about", "About Us")]


def head(title, desc, path, extra=""):
    url = BASE + (path if path != "/" else "/")
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#17191B">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Apex Rise IT Solution logo with the tagline Rise Beyond Limits">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{BASE}/assets/og-image.jpg">
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<script src="/assets/tailwind-config.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
{extra}</head>
"""


def logo_block(dark=False, size="w-10 h-10", name_cls="text-label-md", sub_cls="text-caption"):
    sub_col = "text-white" if dark else "text-[#17191B]"
    return (f'<span class="flex items-center gap-stack-sm"><span class="{size} rounded-full bg-[#17191B] border border-outline-variant/30 overflow-hidden flex items-center justify-center shrink-0">'
            f'<img alt="" class="w-full h-full object-contain" src="/assets/logo-icon-160.png" width="160" height="160"></span>'
            f'<span class="flex flex-col leading-none"><span class="custom-gold-text font-bold {name_cls}">Apex Rise</span>'
            f'<span class="{sub_col} {sub_cls} font-medium">IT Solution</span></span></span>')


def topbar(active):
    links = "\n".join(
        f'<a class="nav-link" href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    mlinks = "\n".join(
        f'<a class="mobile-link" href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    cta_href = "#enquiry" if active == "/contact" else "/contact"
    return f"""<body class="bg-[#F7F7F5] text-on-background font-body-md antialiased min-h-screen flex flex-col">
<a class="skip-link" href="#main">Skip to content</a>
<header class="bg-[#F7F7F5] sticky top-0 z-50 border-b border-[#E2E2DE]">
<div class="flex justify-between items-center w-full px-margin-mobile lg:px-margin-desktop py-stack-md max-w-container-max mx-auto">
<a class="flex items-center h-10" href="/" aria-label="{NAME} home page">{logo_block()}</a>
<nav class="hidden lg:flex gap-gutter items-center text-label-md font-label-md" aria-label="Main menu">
{links}
</nav>
<a class="hidden lg:inline-flex items-center justify-center bg-[#17191B] text-white px-6 py-3 rounded hover:bg-white hover:text-[#17191B] transition-all duration-200 text-label-md font-label-md font-bold border border-[#17191B]" href="{cta_href}">Let's Talk <span class="material-symbols-outlined ml-2 text-[18px]" aria-hidden="true">arrow_forward</span></a>
<button id="menu-toggle" type="button" class="lg:hidden inline-flex items-center justify-center w-11 h-11 -mr-2 text-[#17191B] rounded" aria-controls="mobile-menu" aria-expanded="false" aria-label="Open menu">
<span class="material-symbols-outlined text-[28px]" aria-hidden="true">menu</span>
</button>
</div>
<div id="mobile-menu" class="hidden lg:hidden border-t border-[#E2E2DE] bg-[#F7F7F5]">
<nav class="px-margin-mobile pb-stack-lg max-w-container-max mx-auto" aria-label="Phone menu">
{mlinks}
<a class="mt-stack-lg flex items-center justify-center bg-[#17191B] text-white px-6 py-4 rounded font-bold text-label-md" href="{cta_href}">Let's Talk <span class="material-symbols-outlined ml-2 text-[18px]" aria-hidden="true">arrow_forward</span></a>
</nav>
</div>
</header>
<main id="main" class="flex-grow">
"""


def footer():
    fl = "text-body-md font-body-md text-outline-variant hover:text-[#C9A227] transition-colors duration-200 w-max"
    co = "\n".join(f'<a class="{fl}" href="{h}">{t}</a>' for h, t in NAV + [("/contact", "Contact Us")])
    sv = "\n".join(f'<a class="{fl}" href="/services#{a}">{t}</a>' for a, t in SERVICES_SHORT)
    return f"""</main>
<footer class="custom-dark-bg text-white border-t border-outline-variant/20">
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-stack-lg lg:gap-gutter px-margin-mobile md:px-margin-desktop py-section-gap max-w-container-max mx-auto">
<div class="flex flex-col gap-stack-md">
<a class="flex items-center" href="/" aria-label="{NAME} home page">{logo_block(dark=True, size="w-12 h-12", name_cls="text-headline-md", sub_cls="text-label-md")}</a>
<p class="text-body-md text-outline-variant mt-2"><span class="custom-gold-text font-semibold">Rise Beyond Limits.</span> Websites, apps and software for small businesses in Pokhara.</p>
</div>
<div class="flex flex-col gap-stack-sm">
<h2 class="text-label-md font-label-md uppercase tracking-wider text-outline-variant mb-2">Company</h2>
{co}
</div>
<div class="flex flex-col gap-stack-sm">
<h2 class="text-label-md font-label-md uppercase tracking-wider text-outline-variant mb-2">Services</h2>
{sv}
</div>
<div class="flex flex-col gap-stack-sm">
<h2 class="text-label-md font-label-md uppercase tracking-wider text-outline-variant mb-2">Contact</h2>
<a class="text-body-md text-outline-variant hover:text-[#C9A227] flex items-center gap-2 w-max" href="mailto:apexrise26@gmail.com"><span class="material-symbols-outlined text-[18px] custom-gold-text" aria-hidden="true">mail</span>apexrise26@gmail.com</a>
<a class="text-body-md text-outline-variant hover:text-[#C9A227] flex items-center gap-2 w-max" href="tel:+9779816636599"><span class="material-symbols-outlined text-[18px] custom-gold-text" aria-hidden="true">call</span>+977-9816636599</a>
<p class="text-body-md text-outline-variant flex items-center gap-2"><span class="material-symbols-outlined text-[18px] custom-gold-text" aria-hidden="true">location_on</span>Pokhara, Nepal</p>
</div>
</div>
<div class="border-t border-outline-variant/20">
<p class="px-margin-mobile md:px-margin-desktop py-stack-md max-w-container-max mx-auto text-center md:text-left text-caption font-caption text-outline-variant">Copyright © 2026 <span class="custom-gold-text">Apex Rise</span> IT Solution. All rights reserved.</p>
</div>
</footer>
<script src="/assets/site.js"></script>
</body>
</html>
"""


SERVICES_SHORT = [("web-development", "Web Development"), ("mobile-apps", "Mobile App Development"),
                  ("seo", "SEO &amp; Digital Growth"), ("software", "Software &amp; IT Solutions"),
                  ("ui-ux-design", "UI/UX Design"), ("graphic-design", "Graphic Design")]

# ---------- shared blocks ----------
EYEBROW = "text-label-md font-label-md uppercase tracking-widest custom-gold-text"
H2 = "text-headline-lg-mobile md:text-headline-lg font-headline-lg-mobile md:font-headline-lg text-[#17191B]"
BODY = "text-body-md font-body-md text-[#666666]"
BTN_DARK = "inline-flex items-center justify-center bg-[#17191B] text-white px-8 py-4 rounded font-label-md text-label-md font-bold hover:bg-[#2f3130] transition-colors"
BTN_LINE = "inline-flex items-center justify-center bg-transparent border border-[#17191B] text-[#17191B] px-8 py-4 rounded font-label-md text-label-md font-bold hover:bg-white transition-colors"
BTN_GOLD = "inline-flex items-center justify-center custom-gold-bg text-[#17191B] px-8 py-4 rounded font-label-md text-label-md hover:opacity-90 transition-opacity font-bold"
ARROW = '<span class="material-symbols-outlined ml-2 text-[18px]" aria-hidden="true">arrow_forward</span>'
EXT = '<span class="material-symbols-outlined ml-2 text-[18px]" aria-hidden="true">open_in_new</span>'
LIVE = "https://warehousingcompany.vercel.app"

PROCESS = [
    ("DISCOVER", "We listen first. We learn about your business, your customers and the tools you already use, then agree what the project needs to do."),
    ("PLAN", "We sketch the pages or screens, agree the features and set a realistic timeline before any code is written."),
    ("BUILD", "We build in short stages and show you progress as we go, so there are no surprises at the end."),
    ("IMPROVE", "We test everything, fix what needs fixing and keep improving the work after launch."),
]


def process_section(title, bg="bg-[#F7F7F5]"):
    steps = "\n".join(f"""<div class="flex flex-col gap-stack-md {bg} pr-4 relative">
<span class="text-[64px] leading-none font-display text-[#C9A227] opacity-60" aria-hidden="true">0{i}</span>
<h3 class="text-headline-md font-headline-md text-[#17191B]">{t}</h3>
<p class="{BODY}">{d}</p>
</div>""" for i, (t, d) in enumerate(PROCESS, 1))
    return f"""<section class="py-section-gap {bg}" aria-labelledby="process-title">
<div class="px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto">
<h2 id="process-title" class="{H2} text-center mb-section-gap">{title}</h2>
<div class="relative">
<div class="hidden md:block absolute top-[50px] left-0 w-full h-[1px] bg-[#E2E2DE] z-0"></div>
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-gutter relative z-10">
{steps}
</div>
</div>
</div>
</section>
"""


def cta(title, text, button="Let's Talk", href="/contact"):
    return f"""<section class="custom-dark-bg py-section-gap">
<div class="px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto text-center flex flex-col items-center gap-stack-md">
<h2 class="text-headline-lg-mobile md:text-headline-lg font-headline-lg text-white">{title}</h2>
<p class="text-body-lg font-body-lg text-outline-variant max-w-2xl mb-stack-sm">{text}</p>
<a class="{BTN_GOLD}" href="{href}">{button}{ARROW}</a>
</div>
</section>
"""


def page_hero(eyebrow, h1, text, crumb=None, buttons=""):
    trail = [("/", "Home")] + (list(crumb[:-1]) if isinstance(crumb, list) else [])
    current = crumb[-1] if isinstance(crumb, list) else crumb
    links = "".join(f'<a class="hover:text-[#17191B] underline-offset-4 hover:underline" href="{h}">{t}</a> / ' for h, t in trail)
    bc = (f'<nav aria-label="Breadcrumb" class="font-caption text-caption text-outline mt-stack-lg">{links}<span class="text-[#17191B] font-medium" aria-current="page">{current}</span></nav>'
          if crumb else "")
    return f"""<section class="py-section-gap px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto text-center flex flex-col items-center">
<p class="text-label-md font-label-md uppercase tracking-widest text-on-surface-variant mb-stack-md flex items-center gap-2"><span class="w-8 h-px bg-[#C9A227]" aria-hidden="true"></span>{eyebrow}<span class="w-8 h-px bg-[#C9A227]" aria-hidden="true"></span></p>
<h1 class="text-[36px] leading-[44px] md:text-display font-display font-bold text-[#17191B] mb-stack-lg max-w-3xl">{h1}</h1>
<p class="text-body-lg font-body-lg text-[#666666] max-w-2xl">{text}</p>
{buttons}
{bc}
</section>
"""


# ---------- HOME ----------
HOME_SERVICES = [
    ("web-development", "Web Development", "Business websites, online shops and web applications that load quickly and work well on any phone, tablet or computer."),
    ("mobile-apps", "Mobile App Development", "Android and iOS apps that let your customers book, buy or get in touch straight from their phone."),
    ("seo", "SEO &amp; Digital Growth", "Clear page titles, helpful content and technical fixes so local customers can find you on Google."),
    ("software", "Software &amp; IT Solutions", "Custom software and business systems that replace paper forms and spreadsheets, plus honest IT advice."),
]

WHY = [
    ("PRACTICAL APPROACH", "We build what your business needs, not technology for its own sake. If a simple fix will do the job, we will tell you."),
    ("CLEAR COMMUNICATION", "No jargon. You will always know what we are doing, why we are doing it and what it means for your business."),
    ("MODERN, RELIABLE TECHNOLOGY", "We use proven tools such as Next.js, TypeScript and Supabase, so your website or system is quick and easy to look after."),
    ("FOCUSED ON GROWTH", "We judge every project by one simple question: does it help your business grow?"),
]


def home():
    jsonld = {
        "@context": "https://schema.org", "@type": "ProfessionalService", "name": NAME, "url": BASE + "/",
        "logo": BASE + "/assets/logo.png", "image": BASE + "/assets/og-image.jpg", "slogan": "Rise Beyond Limits",
        "description": "IT company in Pokhara, Nepal offering web development, mobile apps, SEO, custom software, UI/UX design and graphic design.",
        "email": "apexrise26@gmail.com", "telephone": "+977-9816636599",
        "address": {"@type": "PostalAddress", "addressLocality": "Pokhara", "addressCountry": "NP"},
        "areaServed": "Pokhara, Nepal",
    }
    extra = '<script type="application/ld+json">' + json.dumps(jsonld) + "</script>\n"
    cards = "\n".join(f"""<a class="bg-white border border-[#E2E2DE] rounded-[8px] p-stack-lg flex flex-col gap-stack-md hover:shadow-md transition-shadow duration-200 relative group" href="/services#{a}">
<span class="text-display font-display custom-gold-text opacity-40" aria-hidden="true">0{i}</span>
<h3 class="text-headline-md font-headline-md text-[#17191B] mt-auto">{t}</h3>
<p class="{BODY}">{d}</p>
<span class="material-symbols-outlined absolute bottom-4 right-4 text-[24px] custom-gold-text opacity-0 group-hover:opacity-100 transition-opacity" aria-hidden="true">arrow_forward</span>
</a>""" for i, (a, t, d) in enumerate(HOME_SERVICES, 1))
    why = "\n".join(f"""<div class="flex gap-gutter pt-stack-lg{' first:pt-0' if i == 1 else ''}">
<span class="text-headline-md font-headline-md custom-gold-text w-8 shrink-0" aria-hidden="true">0{i}</span>
<div>
<h3 class="text-headline-md font-headline-md text-[#17191B] mb-stack-sm">{t}</h3>
<p class="{BODY}">{d}</p>
</div>
</div>""" for i, (t, d) in enumerate(WHY, 1))
    stats = "\n".join(f"""<div class="border-l-2 border-[#C9A227] pl-stack-md"><p class="text-headline-md font-headline-md text-[#17191B]">{n}</p><p class="text-caption font-caption text-[#666666] uppercase tracking-wider">{l}</p></div>"""
                      for n, l in (("6", "Training levels"), ("51", "Hazards to find"), ("78", "Safety guides"), ("40 / 40", "System tests passed")))
    body = f"""<section class="py-section-gap px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto">
<div class="flex flex-col gap-stack-lg items-center text-center mx-auto max-w-[900px]">
<p class="text-label-md font-label-md uppercase tracking-widest text-on-surface-variant">Rise Beyond Limits</p>
<h1 class="text-[34px] leading-[42px] sm:text-[40px] sm:leading-[48px] md:text-display font-display font-bold text-[#17191B]">
Bring Your Ideas to Life with the IT Company in Pokhara that is
<span class="rotating-slot"><span class="invisible custom-gold-text" aria-hidden="true">professional</span><span class="absolute left-0 top-0 custom-gold-text transform translate-y-0 opacity-100 transition-all duration-500" id="rotating-text">progressive</span></span>
</h1>
<p class="text-body-lg font-body-lg text-[#666666] max-w-[650px]">
<span class="custom-gold-text font-bold">Apex Rise</span> IT Solution is a four-person IT team in Pokhara. We build websites, mobile apps and business software that do a clear job for your business, and we explain every step in plain language.
</p>
<div class="flex flex-col sm:flex-row gap-stack-md pt-stack-sm justify-center w-full sm:w-auto">
<a class="{BTN_DARK}" href="/services">Explore Our Services{ARROW}</a>
<a class="{BTN_LINE}" href="/contact">Contact Us</a>
</div>
</div>
</section>
<section class="border-y border-[#E2E2DE] bg-[#F7F7F5]" aria-label="Our positioning">
<div class="max-w-container-max mx-auto px-margin-mobile md:px-margin-desktop py-stack-md">
<p class="text-center text-label-md font-label-md tracking-[0.1em] text-on-surface-variant uppercase flex flex-col md:flex-row justify-center items-center gap-stack-sm md:gap-gutter">
<span>Practical Technology</span><span class="hidden md:inline text-outline-variant" aria-hidden="true">|</span><span>Clear Strategy</span><span class="hidden md:inline text-outline-variant" aria-hidden="true">|</span><span>Business-Focused Solutions</span>
</p>
</div>
</section>
<section class="py-section-gap px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto">
<div class="flex flex-col md:flex-row justify-between md:items-end mb-stack-lg gap-stack-md">
<div class="max-w-2xl">
<h2 class="{H2} mb-stack-sm">Solutions Built Around Your Business.</h2>
<p class="{BODY}">Websites, mobile apps, SEO and custom software. Tell us the problem and we will suggest the simplest thing that solves it.</p>
</div>
<a class="text-[#17191B] font-label-md text-label-md hover:text-[#C9A227] transition-colors flex items-center shrink-0" href="/services">View All Six Services <span class="material-symbols-outlined ml-1 text-[18px]" aria-hidden="true">arrow_forward</span></a>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 gap-gutter">
{cards}
</div>
</section>
<section class="bg-white border-y border-[#E2E2DE] py-section-gap" aria-labelledby="work-title">
<div class="px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto grid grid-cols-1 lg:grid-cols-2 gap-stack-lg lg:gap-section-gap items-center">
<div class="flex flex-col gap-stack-md">
<p class="{EYEBROW}">Our Work</p>
<h2 id="work-title" class="{H2}">Hazard Perception Training Simulator</h2>
<p class="{BODY}">For the Logistic &amp; Warehousing Company we built a public website, an employee training portal with a six-level 3D warehouse simulator, and an admin portal that tracks every employee's progress.</p>
<div class="grid grid-cols-2 gap-stack-md my-stack-sm">
{stats}
</div>
<div class="flex flex-col sm:flex-row gap-stack-md">
<a class="{BTN_DARK}" href="{case_url(PROJECTS[0])}">Read the Case Study{ARROW}</a>
<a class="{BTN_LINE}" href="{LIVE}" target="_blank" rel="noopener">Visit the Live System{EXT}</a>
</div>
<a class="text-[#17191B] font-label-md text-label-md hover:text-[#C9A227] transition-colors flex items-center w-max" href="/work">See All Our Projects <span class="material-symbols-outlined ml-1 text-[18px]" aria-hidden="true">arrow_forward</span></a>
</div>
<a href="{case_url(PROJECTS[0])}" class="block rounded-xl overflow-hidden border border-[#E2E2DE] shadow-sm hover:shadow-md transition-shadow">
<img class="w-full h-auto" src="/assets/work/simulator-level-1.jpg" width="1400" height="788" loading="lazy" alt="Level 1 of the hazard perception simulator: a 3D warehouse with racking, a forklift, a spill and cones, with the level, hazards found, time and score shown at the top">
</a>
</div>
</section>
<section class="custom-dark-bg py-section-gap">
<div class="px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto grid grid-cols-1 md:grid-cols-2 gap-stack-lg md:gap-gutter items-center">
<div class="flex flex-col gap-stack-lg">
<p class="{EYEBROW}">About Apex Rise</p>
<h2 class="text-[36px] leading-[44px] md:text-display font-display font-bold text-white">Technology With a Clear Purpose.</h2>
<p class="text-body-lg font-body-lg text-outline-variant max-w-xl"><span class="custom-gold-text font-bold">Our mission</span> is to build technology that people actually use, not just technology that works. If the people it was made for do not use it, it has not solved anything.</p>
<p class="text-body-md text-outline-variant max-w-xl">Our vision is to help businesses rise beyond their digital limits: easier to find online, stronger in their digital presence and ready to grow.</p>
<div class="pt-stack-sm">
<a class="inline-flex items-center text-white font-label-md text-label-md hover:text-[#C9A227] transition-colors" href="/about#mission">Our Mission, Vision and Values <span class="material-symbols-outlined ml-2 text-[18px] custom-gold-text" aria-hidden="true">arrow_forward</span></a>
</div>
</div>
<div class="relative w-full flex md:justify-end">
<img alt="A staircase leading up to an arrow, the Apex Rise symbol of steady progress" class="w-full h-auto object-contain rounded-xl" src="/assets/brand-stairs.jpg" width="512" height="228" loading="lazy">
</div>
</div>
</section>
<section class="bg-[#F7F7F5] border-b border-[#E2E2DE] py-section-gap">
<div class="px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto grid grid-cols-1 gap-stack-lg md:gap-[120px] md:grid-cols-2">
<div>
<p class="{EYEBROW} mb-stack-sm">Why Apex Rise</p>
<h2 class="{H2}">Built for Progress, Not Just Appearance.</h2>
<p class="text-[#666666] text-body-md font-body-md mt-4 max-w-md">We believe technology should solve real problems. These four values shape how we work with every client.</p>
</div>
<div class="flex flex-col gap-stack-lg divide-y divide-[#E2E2DE]">
{why}
</div>
</div>
</section>
{process_section("From Idea to Implementation.")}
{cta("Ready to Move Your Idea Forward?", "Tell us about your project. We will reply with honest advice on what it needs and how we can help.")}"""
    return (head(f"{NAME} | Web, App and Software Development in Pokhara",
                 "Apex Rise IT Solution is a four-person IT team in Pokhara, Nepal. We build websites, mobile apps, SEO and custom business software in plain language.",
                 "/", extra) + topbar("/") + body + footer())


# ---------- SERVICES ----------
SERVICES = [
    ("web-development", "Web Development", "Websites and web applications that look professional, load quickly and work on every screen size.",
     ["Business websites", "E-commerce", "Custom web applications", "Responsive development"]),
    ("mobile-apps", "Mobile App Development", "Android and iOS apps that let your customers book, buy or contact you from their phone.",
     ["Android apps", "iOS apps", "Cross-platform apps", "App maintenance"]),
    ("seo", "SEO &amp; Digital Growth", "Help for local customers to find you on Google, without paying for adverts.",
     ["Technical SEO", "On-page optimisation", "Content strategy", "Digital strategy"]),
    ("software", "Software &amp; IT Solutions", "Software built around the way your business works, and straight answers to your IT questions.",
     ["Custom software", "Business systems", "System integration", "IT consultation"]),
    ("ui-ux-design", "UI/UX Design", "Screens and layouts that are clear, attractive and easy for your customers to use.",
     ["User research", "Wireframing", "Prototyping", "Interface design"]),
    ("graphic-design", "Graphic Design", "Logos, brand colours and marketing material that make your business look the same everywhere it appears.",
     ["Brand identity", "Marketing materials", "Social media graphics", "Print design"]),
]


def services():
    cards = "\n".join(f"""<article id="{a}" class="scroll-mt-28 bg-white border border-[#E2E2DE] rounded-service-card p-stack-lg hover:shadow-lg transition-shadow duration-300 flex flex-col">
<span class="text-display font-display text-brand-gold-light mb-stack-md block" aria-hidden="true">0{i}</span>
<h2 class="text-headline-md font-headline-md text-[#17191B] mb-stack-sm uppercase">{t}</h2>
<p class="{BODY} mb-stack-md">{d}</p>
<ul class="text-body-md font-body-md text-on-surface-variant space-y-stack-sm">
{''.join(f'<li class="flex items-start gap-2"><span class="material-symbols-outlined text-brand-gold text-[20px]" aria-hidden="true">check</span>{x}</li>' for x in items)}
</ul>
</article>""" for i, (a, t, d, items) in enumerate(SERVICES, 1))
    body = page_hero("Our Services", 'Digital <span class="custom-gold-text">Solutions</span> Built Around Your Business.',
                     "From websites and mobile apps to SEO and custom software, we help small and growing businesses get the website, app or software they need.",
                     "Services") + f"""<section class="py-section-gap bg-white border-y border-[#E2E2DE]" aria-label="Our six services">
<div class="px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-gutter">
{cards}
</div>
</section>
<section class="py-stack-lg bg-[#F7F7F5] border-b border-[#E2E2DE]">
<div class="px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto flex flex-col md:flex-row md:items-center justify-between gap-stack-md">
<div>
<p class="{EYEBROW} mb-1">See it in practice</p>
<p class="text-body-lg font-body-lg text-[#17191B] max-w-2xl">Our hazard perception case study brings web development, custom software and UI/UX design together in one live system.</p>
</div>
<a class="{BTN_LINE} shrink-0" href="/work">View Our Work{ARROW}</a>
</div>
</section>
{process_section("The Right Solution Starts With Understanding.")}
{cta("Have an Idea You Want to Build?", "Tell us what you want to achieve and we will suggest the right approach for your business and budget.")}"""
    return (head(f"Services | Websites, Apps, SEO and Software | {NAME}",
                 "Six services from one local team: web development, mobile apps, SEO and digital growth, custom software and IT advice, UI/UX design and graphic design.",
                 "/services") + topbar("/services") + body + footer())


# ---------- OUR WORK ----------
def load_projects():
    """Project cards and case study pages come from projects.json, in the order they appear there."""
    with open(HERE / "projects.json", encoding="utf-8") as f:
        return json.load(f)["projects"]


def case_study(p):
    """One case study page, filled in from a projects.json entry."""
    hero, brief, delivered, worked = p["hero"], p["brief"], p["delivered"], p["how_we_worked"]
    blocks = []
    for i, d in enumerate(delivered["items"]):
        flip = "lg:order-2" if i % 2 else ""
        blocks.append(f"""<div class="grid grid-cols-1 lg:grid-cols-2 gap-stack-lg lg:gap-section-gap items-center">
<div class="{flip}">
<img class="w-full h-auto rounded-xl border border-[#E2E2DE] shadow-sm" src="/assets/work/{d['image']}" width="{d['width']}" height="{d['height']}" loading="lazy" alt="{d['alt']}">
</div>
<div class="flex flex-col gap-stack-sm">
<span class="text-headline-md font-headline-md custom-gold-text" aria-hidden="true">0{i + 1}</span>
<h3 class="text-headline-md font-headline-md text-[#17191B]">{d['title']}</h3>
<p class="{BODY}">{d['text']}</p>
</div>
</div>""")
    facts = "\n".join(f"""<div class="border-t border-[#E2E2DE] pt-stack-md"><dt class="text-caption font-caption uppercase tracking-wider custom-gold-text mb-1">{k}</dt><dd class="text-body-md text-[#17191B]">{v}</dd></div>"""
                      for k, v in p["facts"])
    roles = "\n".join(f"""<div class="bg-white border border-[#E2E2DE] rounded-lg p-stack-lg"><h3 class="font-bold text-[#17191B]">{n}</h3><p class="text-caption custom-gold-text font-semibold uppercase tracking-wider mt-1">{r}</p></div>"""
                      for _, n, r, *_ in TEAM)
    live = (f"""<a class="{BTN_DARK}" href="{hero['live_url']}" target="_blank" rel="noopener">Visit the Live System{EXT}</a>\n"""
            if hero.get("live_url") else "")
    buttons = f"""<div class="flex flex-col sm:flex-row gap-stack-md pt-stack-lg justify-center w-full sm:w-auto">
{live}<a class="{BTN_LINE}" href="/contact">Start a Project Like This</a>
</div>"""
    img = hero["image"]
    paras = "\n".join(f'<p class="text-body-lg font-body-lg text-[#666666]">{t}</p>' for t in brief["paragraphs"])
    body = page_hero("Case Study", hero["title_html"], hero["intro"],
                     [("/work", "Our Work"), p["name"]], buttons) + f"""<section class="px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto pb-section-gap">
<img class="w-full h-auto rounded-xl border border-[#E2E2DE] shadow-md" src="/assets/work/{img['file']}" width="{img['width']}" height="{img['height']}" alt="{img['alt']}">
<dl class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-gutter mt-stack-lg">
{facts}
</dl>
</section>
<section class="bg-white border-y border-[#E2E2DE] py-section-gap" aria-labelledby="brief-title">
<div class="px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto grid grid-cols-1 md:grid-cols-12 gap-gutter">
<div class="md:col-span-5">
<p class="{EYEBROW} mb-stack-sm">The Brief</p>
<h2 id="brief-title" class="{H2}">{brief['heading']}</h2>
</div>
<div class="md:col-span-7 flex flex-col gap-stack-md">
{paras}
</div>
</div>
</section>
<section class="py-section-gap" aria-labelledby="delivered-title">
<div class="px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto flex flex-col gap-section-gap">
<div class="max-w-2xl">
<p class="{EYEBROW} mb-stack-sm">What We Delivered</p>
<h2 id="delivered-title" class="{H2}">{delivered['heading']}</h2>
<p class="{BODY} mt-stack-sm">{delivered['note']}</p>
</div>
{chr(10).join(blocks)}
</div>
</section>
<section class="bg-white border-y border-[#E2E2DE] py-section-gap" aria-labelledby="team-title">
<div class="px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto">
<p class="{EYEBROW} mb-stack-sm">How We Worked</p>
<h2 id="team-title" class="{H2} mb-stack-sm">{worked['heading']}</h2>
<p class="{BODY} max-w-2xl mb-stack-lg">{worked['text']}</p>
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-gutter">
{roles}
</div>
</div>
</section>
<section class="py-stack-lg">
<div class="px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto">
<a class="text-[#17191B] font-label-md text-label-md hover:text-[#C9A227] transition-colors inline-flex items-center" href="/work"><span class="material-symbols-outlined mr-1 text-[18px]" aria-hidden="true">arrow_back</span>Back to All Projects</a>
</div>
</section>
{cta(p["cta"]["title"], p["cta"]["text"])}"""
    return body


PROJECTS = load_projects()


def case_url(p):
    return f"/work/{p['slug']}"


def project_card(p):
    w, h = p["card_image"]["width"], p["card_image"]["height"]
    return f"""<a class="group bg-white border border-[#E2E2DE] rounded-lg overflow-hidden flex flex-col hover:shadow-lg transition-shadow duration-300" href="{case_url(p)}">
<div class="aspect-[16/9] overflow-hidden bg-surface-container">
<img class="w-full h-full object-cover group-hover:scale-[1.02] transition-transform duration-500" src="/assets/work/{p['card_image']['file']}" width="{w}" height="{h}" alt="{p['card_image']['alt']}">
</div>
<div class="p-stack-lg flex flex-col gap-stack-sm flex-grow">
<p class="text-caption font-semibold uppercase tracking-wider custom-gold-text">{p['sector']}</p>
<h2 class="text-headline-md font-headline-md text-[#17191B]">{p['name']}</h2>
<p class="text-caption font-caption text-on-surface-variant">Client: {p['client']}</p>
<p class="{BODY}">{p['summary']}</p>
<span class="mt-auto pt-stack-sm inline-flex items-center font-label-md text-label-md text-[#17191B] group-hover:text-[#C9A227] transition-colors">View Case Study{ARROW}</span>
</div>
</a>"""


def work():
    cards = "\n".join(project_card(p) for p in PROJECTS)
    soon = f"""<div class="border-2 border-dashed border-[#E2E2DE] rounded-lg p-stack-lg flex flex-col justify-center gap-stack-sm min-h-[260px]">
<span class="material-symbols-outlined custom-gold-text text-[32px]" aria-hidden="true">add_circle</span>
<h2 class="text-headline-md font-headline-md text-[#17191B]">More Projects Coming Soon</h2>
<p class="{BODY}">We add a new card here each time we finish a project. Have a project in mind?</p>
<a class="text-[#17191B] font-label-md text-label-md hover:text-[#C9A227] transition-colors inline-flex items-center w-max" href="/contact">Let's Talk <span class="material-symbols-outlined ml-1 text-[18px]" aria-hidden="true">arrow_forward</span></a>
</div>"""
    body = page_hero("Our Work", 'Projects We Have <span class="custom-gold-text">Delivered.</span>',
                     "Real projects that we designed, built and tested. Open a project to read the full case study.",
                     "Our Work") + f"""<section class="px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto pb-section-gap" aria-label="Projects">
<div class="grid grid-cols-1 md:grid-cols-2 gap-gutter">
{cards}
{soon}
</div>
</section>
{process_section("How We Run Every Project.", "bg-white")}
{cta("Have a Project You Want to Build?", "Tell us what you need. We will explain how we would build it and what it would take.")}"""
    return (head(f"Our Work | Projects and Case Studies | {NAME}",
                 "Projects by Apex Rise IT Solution in Pokhara. Read our case study of a 3D hazard perception training simulator built for the Logistic &amp; Warehousing Company.",
                 "/work") + topbar("/work") + body + footer())


def project_page(p):
    return (head(p["page_title"], p["page_description"], case_url(p)) + topbar("/work") + case_study(p) + footer())


# ---------- ABOUT ----------
TEAM = [
    ("susan-rana.jpg", "Susan Rana", "Team Leader &amp; Business Analyst", 600, 600, "object-top"),
    ("swagat-basnet.jpg", "Swagat Basnet", "Development &amp; Deployment", 600, 800, "object-center"),
    ("nathan-sharma-poudel.jpg", "Nathan Sharma Poudel", "Design &amp; Marketing", 600, 800, "object-center"),
    ("awasar-gurung.jpg", "Awasar Gurung", "QA &amp; Documentation", 402, 856, "object-[50%_65%] sm:object-center"),
]

VALUES = [
    ("Practical approach", "We build what your business needs, not technology for its own sake."),
    ("Clear communication", "Plain language, regular updates and no jargon."),
    ("Modern, reliable technology", "Proven tools that keep your website or system quick and easy to look after."),
    ("Focused on growth", "Every project is judged by whether it helps your business move forward."),
]


def about():
    team = "\n".join(f"""<article class="group flex flex-col border border-[#E2E2DE] bg-white rounded-lg overflow-hidden transition-all duration-300 hover:border-outline">
<div class="aspect-square sm:aspect-[3/4] w-full bg-surface-container overflow-hidden">
<img class="w-full h-full object-cover {pos} filter lg:grayscale lg:group-hover:grayscale-0 transition-all duration-500" alt="Photo of {n}, {r.replace('&amp;', 'and')}" src="/assets/team/{img}" width="{w}" height="{h}" loading="lazy">
</div>
<div class="p-stack-md border-t border-[#E2E2DE] flex flex-col gap-1 flex-grow">
<h3 class="text-body-lg font-bold text-[#17191B]">{n}</h3>
<p class="text-caption font-semibold uppercase tracking-wider custom-gold-text">{r}</p>
</div>
</article>""" for img, n, r, w, h, pos in TEAM)
    values = "\n".join(f"""<div class="border-t border-outline-variant/30 pt-stack-md"><span class="custom-gold-text font-bold" aria-hidden="true">0{i}</span><h4 class="text-white font-semibold text-body-lg mt-1">{t}</h4><p class="text-outline-variant text-body-md mt-1">{d}</p></div>"""
                       for i, (t, d) in enumerate(VALUES, 1))
    body = page_hero("About Apex Rise", 'Technology With a Clear <span class="custom-gold-text">Purpose.</span>',
                     "Apex Rise IT Solution is a team of four based in Pokhara, Nepal. We build websites, apps and business software for small and growing businesses.",
                     "About Us") + f"""<section class="w-full bg-white border-y border-[#E2E2DE] py-section-gap">
<div class="max-w-container-max mx-auto px-margin-mobile md:px-margin-desktop grid grid-cols-1 md:grid-cols-12 gap-gutter">
<div class="md:col-span-5">
<p class="text-label-md font-label-md text-on-surface-variant uppercase tracking-widest mb-stack-md">Who We Are</p>
<h2 class="{H2} max-w-md">Building Technology Around Real Business Needs.</h2>
</div>
<div class="md:col-span-7 flex flex-col justify-center">
<p class="text-body-lg font-body-lg text-[#666666] border-l border-[#E2E2DE] pl-gutter">At Apex Rise we believe technology should earn its place. We are not interested in complex systems for the sake of it. We take time to understand the everyday problems our clients face, then build clear, well-tested solutions that deal with them directly and help the business grow.</p>
</div>
</div>
</section>
<section id="mission" class="scroll-mt-24 w-full custom-dark-bg py-section-gap" aria-labelledby="mission-title">
<div class="max-w-container-max mx-auto px-margin-mobile md:px-margin-desktop">
<p class="{EYEBROW} mb-stack-sm">What Drives Us</p>
<h2 id="mission-title" class="text-headline-lg-mobile md:text-headline-lg font-headline-lg text-white mb-stack-lg">Mission, Vision and Values.</h2>
<div class="grid grid-cols-1 md:grid-cols-2 gap-gutter mb-section-gap">
<div class="border border-outline-variant/30 rounded-lg p-stack-lg">
<h3 class="{EYEBROW} mb-stack-md">Our Mission</h3>
<p class="text-body-lg font-body-lg text-white">We build technology that people actually use, not just technology that works. We judge a solution by whether it reaches the people it was made for and changes how they work, because software nobody uses has solved nothing. That is what rising beyond limits means to us.</p>
</div>
<div class="border border-outline-variant/30 rounded-lg p-stack-lg">
<h3 class="{EYEBROW} mb-stack-md">Our Vision</h3>
<p class="text-body-lg font-body-lg text-white">To help businesses rise beyond their digital limits by improving their online visibility, strengthening their digital presence and creating opportunities for lasting growth.</p>
</div>
</div>
<h3 class="{EYEBROW} mb-stack-md">Our Values</h3>
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-gutter">
{values}
</div>
</div>
</section>
<section class="w-full max-w-container-max mx-auto px-margin-mobile md:px-margin-desktop py-section-gap" aria-labelledby="team-title">
<div class="flex flex-col items-center text-center mb-stack-lg">
<p class="text-label-md font-label-md text-on-surface-variant uppercase tracking-widest mb-stack-md">Our Team</p>
<h2 id="team-title" class="{H2}">The People Behind Apex Rise.</h2>
<p class="{BODY} max-w-2xl mt-stack-sm">Each of us has one main role, matched to the skills we bring. On every project we plan, review and test together.</p>
</div>
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-gutter mt-stack-lg">
{team}
</div>
</section>
<section class="w-full bg-white border-y border-[#E2E2DE] py-section-gap" aria-labelledby="logo-title">
<div class="max-w-container-max mx-auto px-margin-mobile md:px-margin-desktop grid grid-cols-1 md:grid-cols-2 gap-stack-lg md:gap-section-gap items-center">
<div>
<p class="{EYEBROW} mb-stack-sm">Our Brand</p>
<h2 id="logo-title" class="{H2} mb-stack-md">Rise Beyond Limits.</h2>
<p class="text-body-lg font-body-lg text-[#666666] mb-stack-md">Our logo is a gold staircase and an upward arrow that together form the letter A. The curly braces around it come from computer code and stand for the software side of our work.</p>
<p class="{BODY}">The steps say what we believe: progress comes one solid step at a time. That idea gives us our tagline, Rise Beyond Limits, and our promise of Practical Technology, Clear Strategy and Business-Focused Solutions.</p>
</div>
<div class="flex justify-center md:justify-end">
<img src="/assets/logo-600.jpg" alt="The Apex Rise IT Solution logo: a gold staircase and white arrow forming the letter A inside curly braces" class="w-64 h-64 md:w-80 md:h-80 object-cover rounded-full border border-[#E2E2DE]" width="600" height="600" loading="lazy">
</div>
</div>
</section>
{cta("Let's Build Something Useful.", "Tell us about your business and what you would like to improve. We will get back to you with honest advice.")}"""
    return (head(f"About Us | Mission, Vision and Team | {NAME}",
                 "Meet the four-person Apex Rise team in Pokhara and read our mission, vision and values.",
                 "/about") + topbar("/about") + body + footer())


# ---------- CONTACT ----------
def contact():
    inp = "border border-outline-variant rounded px-4 py-3 text-body-md focus:border-[#17191B] focus:ring-0 transition-colors bg-white w-full"
    lab = "text-caption font-caption uppercase text-on-surface-variant mb-1"
    body = page_hero("Get in Touch", 'Let\'s Talk About Your Next <span class="custom-gold-text">Idea.</span>',
                     "Have a project in mind, a problem to solve, or just want to know what is possible? We would be happy to hear from you.",
                     "Contact Us") + f"""<section class="max-w-container-max mx-auto px-margin-mobile md:px-margin-desktop pb-section-gap w-full">
<div class="grid grid-cols-1 md:grid-cols-12 gap-gutter">
<div class="md:col-span-4 md:col-start-1 lg:col-start-2 md:border-r border-[#E2E2DE] md:pr-gutter">
<h2 class="text-headline-md font-headline-md text-[#17191B] mb-stack-lg">Let's Start a Conversation.</h2>
<div class="flex flex-col gap-stack-lg">
<div class="border-t border-[#E2E2DE] pt-stack-md">
<span class="text-label-md font-label-md uppercase custom-gold-text block mb-1">Email</span>
<a class="text-body-lg font-body-lg hover:opacity-70 transition-opacity break-all" href="mailto:apexrise26@gmail.com">apexrise26@gmail.com</a>
</div>
<div class="border-t border-[#E2E2DE] pt-stack-md">
<span class="text-label-md font-label-md uppercase custom-gold-text block mb-1">Phone</span>
<a class="text-body-lg font-body-lg hover:opacity-70 transition-opacity" href="tel:+9779816636599">+977-9816636599</a>
</div>
<div class="border-t border-[#E2E2DE] pt-stack-md">
<span class="text-label-md font-label-md uppercase custom-gold-text block mb-1">Location</span>
<p class="text-body-lg font-body-lg">Pokhara, Nepal</p>
</div>
</div>
</div>
<div class="md:col-span-8 lg:col-span-6 lg:col-start-7 mt-12 md:mt-0 scroll-mt-28" id="enquiry">
<span class="text-label-md font-label-md uppercase tracking-widest custom-gold-text block mb-2">Send an Enquiry</span>
<h2 class="text-headline-md font-headline-md text-[#17191B] mb-stack-lg">Tell Us About Your Project.</h2>
<form id="contactForm" action="https://api.web3forms.com/submit" method="POST" class="flex flex-col gap-stack-md bg-white p-6 md:p-8 border border-[#E2E2DE] rounded" novalidate>
<input type="hidden" name="access_key" value="cb35adf1-660c-4e55-ba42-68df8ceb5d56">
<input type="hidden" name="subject" value="New Enquiry from Apex Rise Website">
<input type="hidden" name="from_name" value="Apex Rise Website">
<input type="checkbox" name="botcheck" class="hidden" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="grid grid-cols-1 md:grid-cols-2 gap-stack-md">
<div class="flex flex-col"><label class="{lab}" for="name">Name</label><input class="{inp}" id="name" name="name" required type="text" autocomplete="name"></div>
<div class="flex flex-col"><label class="{lab}" for="email">Email</label><input class="{inp}" id="email" name="email" required type="email" autocomplete="email"></div>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 gap-stack-md">
<div class="flex flex-col"><label class="{lab}" for="phone">Phone (optional)</label><input class="{inp}" id="phone" name="phone" type="tel" autocomplete="tel"></div>
<div class="flex flex-col"><label class="{lab}" for="company">Company (optional)</label><input class="{inp}" id="company" name="company" type="text" autocomplete="organization"></div>
</div>
<div class="flex flex-col">
<label class="{lab}" for="service">Service Needed</label>
<select class="{inp}" id="service" name="service">
<option disabled selected value="">Select a service...</option>
<option value="web">Web Development</option>
<option value="mobile">Mobile App Development</option>
<option value="seo">SEO &amp; Digital Growth</option>
<option value="software">Software &amp; IT Solutions</option>
<option value="uiux">UI/UX Design</option>
<option value="graphic">Graphic Design</option>
<option value="other">Other</option>
</select>
</div>
<div class="flex flex-col"><label class="{lab}" for="message">Message</label><textarea class="{inp} resize-y" id="message" name="message" required rows="5"></textarea></div>
<button class="mt-2 bg-[#17191B] text-white px-8 py-4 rounded hover:opacity-90 transition-opacity text-label-md font-label-md font-bold flex items-center justify-center gap-2 self-stretch sm:self-start disabled:opacity-60" type="submit" id="contactSubmitBtn">
<span id="contactSubmitLabel">Send Enquiry</span> <span class="custom-gold-text" aria-hidden="true">→</span>
</button>
<div id="contactFormStatus" class="hidden" role="status" aria-live="polite"></div>
</form>
</div>
</div>
</section>
<section class="max-w-container-max mx-auto px-margin-mobile md:px-margin-desktop pb-section-gap text-center border-t border-[#E2E2DE] pt-section-gap w-full">
<span class="text-label-md font-label-md uppercase tracking-widest custom-gold-text block mb-2">Our Location</span>
<h2 class="text-headline-md font-headline-md text-[#17191B] mb-stack-sm">Based in Pokhara.</h2>
<p class="{BODY} mb-stack-md">Apex Rise IT Solution is based in Pokhara, Nepal. Call, email or use the form and one of the team will get back to you.</p>
<p class="text-caption font-caption text-on-surface-variant">Want to see what we can do first? <a class="underline underline-offset-4 hover:text-[#C9A227]" href="{case_url(PROJECTS[0])}">Read our case study</a>.</p>
</section>
""" + CONTACT_JS
    return (head(f"Contact Us | {NAME}, Pokhara",
                 "Contact Apex Rise IT Solution in Pokhara, Nepal. Email apexrise26@gmail.com, call +977-9816636599 or send an enquiry through the form.",
                 "/contact") + topbar("/contact") + body + footer())


CONTACT_JS = """<script>
document.getElementById('contactForm').addEventListener('submit', async function (e) {
  e.preventDefault();
  const form = e.target;
  const btn = document.getElementById('contactSubmitBtn');
  const btnLabel = document.getElementById('contactSubmitLabel');
  const status = document.getElementById('contactFormStatus');
  const show = (text, ok) => {
    status.textContent = text;
    status.className = ok
      ? 'block bg-green-50 text-green-700 border border-green-200 px-4 py-3 rounded'
      : 'block bg-red-50 text-red-700 border border-red-200 px-4 py-3 rounded';
  };
  if (!form.checkValidity()) {
    show('Please fill in your name, a valid email address and a message.', false);
    form.reportValidity();
    return;
  }
  btn.disabled = true;
  btnLabel.textContent = 'Sending...';
  status.className = 'hidden';
  try {
    const response = await fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(Object.fromEntries(new FormData(form)))
    });
    const result = await response.json();
    if (result.success) {
      show("Thanks! Your message has been sent. We will get back to you soon.", true);
      form.reset();
    } else {
      show('Something went wrong. Please try again or email us at apexrise26@gmail.com.', false);
      console.error('Web3Forms submission failed:', result);
    }
  } catch (error) {
    show('Something went wrong. Please try again or email us at apexrise26@gmail.com.', false);
    console.error('Web3Forms connection error:', error);
  } finally {
    btn.disabled = false;
    btnLabel.textContent = 'Send Enquiry';
  }
});
</script>
"""


def notfound():
    body = page_hero("Page Not Found", "Sorry, We Could Not Find That Page.",
                     "The link may be old or mistyped. Try one of the pages below.",
                     buttons=f"""<div class="flex flex-col sm:flex-row gap-stack-md pt-stack-lg justify-center w-full sm:w-auto">
<a class="{BTN_DARK}" href="/">Go to the Home Page{ARROW}</a>
<a class="{BTN_LINE}" href="/contact">Contact Us</a>
</div>""")
    return (head(f"Page Not Found | {NAME}", "This page could not be found. Visit the Apex Rise IT Solution home page.", "/404").replace(
        '<meta name="robots" content="index, follow">', '<meta name="robots" content="noindex">').replace(
        f'<link rel="canonical" href="{BASE}/404">\n', '').replace(
        f'<meta property="og:url" content="{BASE}/404">\n', '') + topbar("") + body + footer())


PAGES = {"index.html": home, "services.html": services, "work.html": work, "about.html": about,
         "contact.html": contact, "404.html": notfound}

MAIN_URLS = [("/", "1.0"), ("/services", "0.9"), ("/work", "0.8"), ("/about", "0.8"), ("/contact", "0.7")]


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    print("wrote", path.relative_to(SITE).as_posix(), len(text))


if __name__ == "__main__":
    for fn, f in PAGES.items():
        write(SITE / fn, f())
    for p in PROJECTS:
        write(SITE / "work" / f"{p['slug']}.html", project_page(p))
    urls = MAIN_URLS[:3] + [(case_url(p), "0.8") for p in PROJECTS] + MAIN_URLS[3:]
    write(SITE / "sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{BASE}{u}</loc><lastmod>2026-10-12</lastmod><priority>{pr}</priority></url>\n" for u, pr in urls)
          + "</urlset>\n")
    rewrites = [{"source": u, "destination": u + ".html"} for u in ("/about", "/services", "/work", "/contact")]
    rewrites += [{"source": case_url(p), "destination": case_url(p) + ".html"} for p in PROJECTS]
    write(SITE / "vercel.json", json.dumps({"cleanUrls": True, "trailingSlash": False, "rewrites": rewrites}, indent=2) + "\n")
