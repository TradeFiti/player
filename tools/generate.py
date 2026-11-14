#!/usr/bin/env python3
"""Generate the selector hub, ten profile designs and 404 page from one content model.

    python3 tools/generate.py           write index.html, 1/..10/index.html, 404.html
    python3 tools/generate.py --check   exit 1 if any generated file is out of date

Everything a scout needs is in the HTML; JavaScript only enhances it.
Output is deterministic: same inputs, byte-identical files.
"""

import json
import struct
import sys
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "shared" / "data" / "profile.json").read_text(encoding="utf-8"))
P = DATA["player"]
REP = DATA["representative"]
UPDATED = date.fromisoformat(DATA["updated"])
DOB = date.fromisoformat(P["dob"])
VARIANTS = DATA["variants"]
IMAGES = {i["stem"]: i for i in DATA["images"]}
SECTIONS = ["overview", "footage", "profile", "trial", "data", "gallery", "contact", "provenance"]
FORMSUBMIT = "https://formsubmit.co/" + REP["email"]


def e(text):
    return escape(str(text), quote=True)


def long_date(d):
    return f"{d.day} {d.strftime('%B')} {d.year}"


AGE = UPDATED.year - DOB.year - ((UPDATED.month, UPDATED.day) < (DOB.month, DOB.day))
UPDATED_TEXT = f"Last updated {long_date(UPDATED)}"
DOB_TEXT = long_date(DOB)


# ---------------------------------------------------------------- media helpers

def jpeg_size(path):
    data = path.read_bytes()
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        length = struct.unpack(">H", data[i + 2:i + 4])[0]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        i += 2 + length
    raise ValueError(f"no SOF marker in {path}")


def thumb_url(stem):
    t = ROOT / "assets" / "images" / "thumbs" / f"{stem}.jpg"
    if t.exists():
        return f"/assets/images/thumbs/{stem}.jpg"
    return f"/assets/images/{IMAGES[stem]['file']}"


def full_url(stem):
    img = IMAGES[stem]
    return f"/assets/images/{img.get('web', img['file'])}"


def size_of(url):
    return jpeg_size(ROOT / url.lstrip("/"))


def img(stem, cls="", eager=False, alt=None, sizes="(max-width: 920px) 50vw, 25vw"):
    url = thumb_url(stem)
    w, h = size_of(url)
    attrs = [f'src="{url}"', f'width="{w}"', f'height="{h}"', f'alt="{e(IMAGES[stem]["alt"] if alt is None else alt)}"']
    if cls:
        attrs.insert(0, f'class="{cls}"')
    attrs.append('loading="eager"' if eager else 'loading="lazy"')
    attrs.append('decoding="async"')
    return f"<img {' '.join(attrs)}>"


def portrait(cls="hero-img", stem="hero-portrait"):
    web = full_url(stem)
    thumb = thumb_url(stem)
    w, h = size_of(web)
    tw = size_of(thumb)[0]
    return (
        f'<img class="{cls}" src="{web}" srcset="{thumb} {tw}w, {web} {w}w" '
        f'sizes="(max-width: 920px) 90vw, 40vw" width="{w}" height="{h}" '
        f'alt="{e(IMAGES[stem]["alt"])}" loading="eager" fetchpriority="high" decoding="async">'
    )


def lightbox_link(stem, group, inner, cls="lb-link"):
    return (
        f'<a class="{cls}" href="{full_url(stem)}" data-lightbox="{group}" '
        f'data-caption="{e(IMAGES[stem]["alt"])}">{inner}</a>'
    )


def roman(n):
    return ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"][n]


# ---------------------------------------------------------------- shared pieces

def idline():
    return (
        f'<p class="idline"><span>{e(P["position"])}</span> <span>{e(P["number"])}</span> '
        f'<span>Age {AGE}</span> <span>{e(P["nationality"])}</span> '
        f'<span>{e(P["school"])}, {e(P["school_year"])}</span></p>'
    )


def ctas(extra=""):
    return (
        f'<div class="cta-row{extra}"><a class="btn btn--primary" href="#footage">Watch Footage</a>'
        f'<a class="btn btn--ghost" href="#contact">Contact Representative</a></div>'
    )


def stamp():
    return f'<p class="stamp"><time datetime="{UPDATED.isoformat()}">{UPDATED_TEXT}</time></p>'


def name_h1(cls="", parts=None):
    parts = parts or (P["first"], P["middle"], P["last"])
    c = f' class="{cls}"' if cls else ""
    return (
        f'<h1 id="hero-title"{c}><span class="n-first">{e(parts[0])}</span> '
        f'<span class="n-middle">{e(parts[1])}</span> <span class="n-last">{e(parts[2])}</span></h1>'
    )


def facts_block():
    rows = [
        ("Full name", P["full_name"]),
        ("Date of birth", DOB_TEXT),
        ("Age", str(AGE)),
        ("Nationality", P["nationality"]),
        ("Position", f'{P["position"]} ({P["number"]})'),
        ("Feet", P["foot"]),
        ("School", f'{P["school"]}, {P["school_year"]}'),
        ("Documented trial", f'{DATA["trial"]["club"]}, participation'),
        ("Representative", f'{REP["name"]}'),
    ]
    items = "".join(f'<div class="fact"><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in rows)
    items += (
        f'<div class="fact"><dt>Email</dt><dd><a href="mailto:{REP["email"]}">{REP["email"]}</a></dd></div>'
    )
    return f'<dl class="facts" data-canonical="facts">{items}</dl>'


KICKERS = {
    1: lambda n: f"§ {n:02d}",
    2: lambda n: f"Segment {n:02d}",
    3: lambda n: f"p. {n * 4:02d}",
    4: lambda n: f"Phase {n}",
    5: lambda n: f"Exhibit {chr(64 + n)}",
    6: lambda n: f"{n:02d} / 08",
    7: lambda n: f"Chapter {roman(n)}",
    8: lambda n: f"Stop {n:02d}",
    9: lambda n: f"Frame {n:02d}",
    10: lambda n: f"{n:02d}",
}

TITLES = {
    "footage": "Footage",
    "profile": "Player profile",
    "trial": "Cambrils UCF trial",
    "data": "Session data",
    "gallery": "Gallery",
    "contact": "Contact the representative",
    "provenance": "Sources and provenance",
}
TITLE_OVERRIDES = {
    2: {"footage": "The footage queue", "data": "Session readout"},
    3: {"footage": "On the ball", "profile": "The player", "gallery": "Picture spread"},
    4: {"profile": "Role and traits", "data": "Session numbers"},
    5: {"trial": "Trial documents", "gallery": "Contact sheets", "provenance": "Chain of evidence"},
    6: {"data": "Left and right, measured"},
    7: {"footage": "See him play", "profile": "The player"},
    8: {"trial": "Catalonia: the Cambrils UCF trial", "profile": "Where it starts"},
    9: {"gallery": "Every frame"},
    10: {"footage": "Watch", "profile": "Profile", "trial": "Trial", "data": "Data", "contact": "Contact"},
}
LEDES = {
    "footage": "Twelve clips supplied by the family. Start with Joseph's introduction, then use the conservative visual descriptions to review the football sequences. Dates, opponents and outcomes are not asserted.",
    "profile": "",
    "trial": "",
    "data": "",
    "gallery": "Photographs from matches, training, the Cambrils UCF trial and portraits. Select any image to enlarge it.",
    "contact": f"Joseph is under 18. Please direct all enquiries to his representative, {REP['name']}.",
    "provenance": "Where each part of this profile comes from.",
}


def section(v, sid, body, cls=""):
    n = SECTIONS.index(sid) + 1
    title = TITLE_OVERRIDES.get(v, {}).get(sid, TITLES[sid])
    lede = LEDES.get(sid, "")
    lede_html = f'<p class="lede">{e(lede)}</p>' if lede else ""
    return (
        f'<section id="{sid}" class="sec sec--{sid}{(" " + cls) if cls else ""}" aria-labelledby="{sid}-title">'
        f'<div class="sec-inner">'
        f'<header class="sec-head" data-reveal><p class="sec-kicker">{e(KICKERS[v](n))}</p>'
        f'<h2 id="{sid}-title">{e(title)}</h2>{lede_html}</header>'
        f"{body}</div></section>"
    )


# ---------------------------------------------------------------- modules

def footage(v):
    items = []
    for i, clip in enumerate(DATA["videos"]):
        cid = clip["id"]
        poster = f"/assets/posters/highlight-{cid}.jpg"
        w, h = size_of(poster)
        default = " data-default" if cid == "02" else ""
        featured = " clip--featured" if i == 0 else ""
        orient = clip["orientation"]
        items.append(
            f'<li class="clip clip--{orient}{featured}" id="clip-{cid}" data-orientation="{orient}" data-reveal>'
            f'<figure class="clip-fig"><div class="clip-frame">'
            f'<video controls preload="none" playsinline poster="{poster}" width="{w}" height="{h}"{default} '
            f'aria-describedby="clip-{cid}-label">'
            f'<source src="/assets/videos/highlight-{cid}.mp4" type="video/mp4">'
            f'<a href="/assets/videos/highlight-{cid}.mp4">Download clip {cid}</a></video></div>'
            f'<figcaption class="clip-cap" id="clip-{cid}-label" data-clip-label>'
            f'<span class="clip-no">Clip {cid} · {e(clip["title"])}</span> '
            f'<span class="clip-meta">{orient.capitalize()} · {clip["duration"]}</span>'
            f'<span class="clip-desc">{e(clip["description"])}</span>'
            f"</figcaption></figure></li>"
        )
    filters = (
        '<div class="chip-row" data-clip-filters role="group" aria-label="Filter clips by orientation" hidden>'
        '<button type="button" class="chip" data-clip-filter="all" aria-pressed="true">All 12</button>'
        '<button type="button" class="chip" data-clip-filter="landscape" aria-pressed="false">Landscape</button>'
        '<button type="button" class="chip" data-clip-filter="portrait" aria-pressed="false">Portrait</button></div>'
    )
    note = ('<p class="fine"><strong>Viewing note:</strong> Native player controls; nothing plays automatically and only one clip plays at a time. '
            'The text under each clip provides a visual description. Kit colours and shirt numbers are only stated when visible; no unverified opponent, date or outcome is assigned.</p>')
    return section(v, "footage", f'{filters}<ol class="clip-list">{"".join(items)}</ol>{note}')


def traits():
    out = []
    for t in DATA["traits"]:
        ev = "".join(f'<li><a href="{e(x["href"])}">{e(x["label"])}</a></li>' for x in t["evidence"])
        out.append(
            f'<li class="trait" data-trait="{t["id"]}" data-reveal><h4>{e(t["title"])}</h4>'
            f'<p>{e(t["prompt"])}</p><ul class="evidence" aria-label="Evidence for {e(t["title"].lower())}">{ev}</ul></li>'
        )
    return (
        '<div class="traits-wrap"><h3>What to look for</h3>'
        '<p class="fine">Viewing prompts linked to evidence on this page. They are not assessments.</p>'
        f'<ol class="traits" data-traits>{"".join(out)}</ol></div>'
    )


def profile(v):
    copy = "".join(f"<p>{e(p)}</p>" for p in DATA["summary"])
    extra = pathway() if v == 8 else ""
    body = (
        f'<div class="profile-grid"><div class="profile-copy" data-reveal>{copy}</div>'
        f'<div class="profile-facts" data-reveal><h3>Key facts</h3>{facts_block()}</div></div>{extra}{traits()}'
    )
    return section(v, "profile", body)


def pathway():
    stops = [
        ("Kitengela, Kenya", "1.47° S, 36.96° E", f'Home and school: {P["school"]}, {P["school_year"]}.', "team-local"),
        ("Cambrils, Catalonia, Spain", "41.07° N, 1.06° E", "Trial participation with Cambrils UCF, documented by certificate.", "trial-pitch"),
        ("Barcelona, Spain", "41.38° N, 2.12° E", "Visit to the FC Barcelona museum at Camp Nou.", "campnou"),
    ]
    items = "".join(
        f'<li class="stop" data-reveal><div class="stop-media">{img(s)}</div><div class="stop-copy">'
        f'<h4>{e(place)}</h4><p class="stop-coord">{e(coord)}</p><p>{e(text)}</p></div></li>'
        for place, coord, text, s in stops
    )
    return (
        '<div class="pathway"><h3>Places on the record</h3>'
        '<p class="fine">Ordered by geography. This is not a career path and does not imply any club registration.</p>'
        f'<ol class="stops">{items}</ol></div>'
    )


def timeline():
    dated = [
        (DOB.isoformat(), DOB_TEXT, "Born", "Identity details supplied by family."),
        ("2025-08-20", DATA["session"]["date"], "Technical session recorded", "One 149-minute session on a wearable tracker. Screenshots in Session data."),
        (UPDATED.isoformat(), long_date(UPDATED), "Profile updated", "Current version of this page."),
    ]
    rows = "".join(
        f'<li class="tl-item" data-reveal><time datetime="{iso}">{e(label)}</time><h4>{e(title)}</h4><p>{e(text)}</p></li>'
        for iso, label, title, text in dated
    )
    return (
        '<div class="timeline-wrap"><h3>Evidence timeline</h3>'
        f'<ol class="timeline">{rows}</ol>'
        '<p class="fine">Undated: the Cambrils UCF trial certificate and photographs. Their date is not stated on this page.</p></div>'
    )


def trial(v):
    t = DATA["trial"]
    stems = ["trial-certificate", "trial-action-1", "trial-team", "trial-huddle", "trial-pitch", "trial-gear"]
    media_items = []
    for s in stems:
        caption = f'<span class="cap">{e(IMAGES[s]["alt"])}</span>'
        media_items.append(
            f'<li class="trial-item" data-reveal>{lightbox_link(s, "trial", img(s) + caption)}</li>'
        )
    media = "".join(media_items)
    extra = timeline() if v == 5 else ""
    body = (
        f'<div class="trial-grid"><div class="trial-copy" data-reveal><p class="trial-club">{e(t["club"])}'
        f' <span>{e(t["place"])}</span></p><p>{e(t["summary"])}</p><p class="note">{e(t["note"])}</p></div>'
        f'<ul class="trial-media">{media}</ul></div>{extra}'
    )
    return section(v, "trial", body)


def fmt(x):
    return f"{x:g}"


def data_section(v):
    s = DATA["session"]
    stat_items = []
    for h in s["headline"]:
        unit = f'<span class="unit"> {e(h["unit"])}</span>' if h["unit"] else ""
        stat_items.append(
            f'<li class="stat" data-reveal><span class="stat-value">{e(h["value"])}{unit}</span>'
            f'<span class="stat-label">{e(h["label"])}</span></li>'
        )
    stats = "".join(stat_items)
    pairs = []
    for p in s["pairs"]:
        top = max(p["left"], p["right"])
        lw = round(p["left"] / top * 100, 1)
        rw = round(p["right"] / top * 100, 1)
        unit = f' {p["unit"]}' if p["unit"] else ""
        pairs.append(
            f'<li class="pair" data-reveal><span class="pair-label">{e(p["label"])}</span>'
            f'<span class="pair-val pair-val--l">{fmt(p["left"])}{unit} <small>left</small></span>'
            f'<span class="pair-bars" aria-hidden="true"><span class="bar bar--l" style="--w: {lw}%"><span class="bar-fill"></span></span>'
            f'<span class="bar bar--r" style="--w: {rw}%"><span class="bar-fill"></span></span></span>'
            f'<span class="pair-val pair-val--r">{fmt(p["right"])}{unit} <small>right</small></span></li>'
        )
    turns = "".join(f'<div class="turn"><dt>{e(t["label"])}</dt><dd>{e(t["value"])}</dd></div>' for t in s["turns"])
    screens = "".join(
        f'<li data-reveal>{lightbox_link(st, "data", img(st, sizes="(max-width: 920px) 33vw, 12vw"))}</li>' for st in s["screens"]
    )
    body = (
        f'<p class="caveat" role="note"><strong>Session caveat.</strong> {e(s["caveat"])}</p>'
        f'<ul class="stat-grid">{"".join(stats)}</ul>'
        f'<div class="data-split"><div class="pairs-wrap"><h3>Left and right foot</h3>'
        f'<ul class="pairs" data-pairs>{"".join(pairs)}</ul>'
        '<p class="fine">Bars compare each foot with the other within this session only.</p></div>'
        f'<div class="turns-wrap"><h3>Turning and agility</h3><dl class="turns">{turns}</dl></div></div>'
        f'<h3>Tracker screenshots</h3><ul class="screens">{screens}</ul>'
    )
    return section(v, "data", body)


def gallery(v):
    order = [i for i in DATA["images"]]
    filters = "".join(
        f'<button type="button" class="chip" data-gallery-filter="{f["key"]}" aria-pressed="{"true" if f["key"] == "all" else "false"}">{e(f["label"])}</button>'
        for f in DATA["gallery_filters"]
    )
    items = []
    for i, im in enumerate(order, 1):
        inner = img(im["stem"]) + f'<span class="g-cap"><span class="g-no">{i:02d}</span> {e(im["alt"])}</span>'
        items.append(
            f'<li class="g-item g-item--{im["cat"]}" id="photo-{im["stem"]}" data-cat="{im["cat"]}"'
            f' data-reveal>{lightbox_link(im["stem"], "gallery", inner, "g-link")}</li>'
        )
    body = (
        f'<div class="chip-row" data-gallery-filters role="group" aria-label="Filter photographs" hidden>{filters}</div>'
        '<p class="fine" data-gallery-count aria-live="polite"></p>'
        f'<ul class="gallery-grid">{"".join(items)}</ul>'
    )
    return section(v, "gallery", body)


def contact(v):
    nn = f"{v:02d}"
    form = (
        f'<form class="contact-form" action="{FORMSUBMIT}" method="POST" data-contact-form aria-describedby="cf-privacy" data-reveal>'
        f'<input type="hidden" name="_subject" value="Enquiry about Joseph Ojwang (design {nn})">'
        '<input type="hidden" name="_template" value="table">'
        '<div class="hp" aria-hidden="true"><label>Leave this field empty <input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>'
        '<div class="field"><label for="cf-name">Your name</label><input id="cf-name" name="name" type="text" autocomplete="name" required></div>'
        '<div class="field"><label for="cf-email">Email address</label><input id="cf-email" name="email" type="email" autocomplete="email" required></div>'
        '<div class="field"><label for="cf-org">Club or organisation <span class="opt">(optional)</span></label><input id="cf-org" name="organisation" type="text" autocomplete="organization"></div>'
        '<div class="field"><label for="cf-message">Message</label><textarea id="cf-message" name="message" rows="5" required></textarea></div>'
        '<p class="privacy" id="cf-privacy"><strong>Privacy:</strong> this form sends your name, email, organisation and message through FormSubmit, an external form processor, to Joseph\'s representative. '
        f'Do not include sensitive personal information or details about other young people. You can instead <a href="mailto:{REP["email"]}">email the representative directly</a>.</p>'
        '<button class="btn btn--primary" type="submit">Send enquiry</button>'
        '<p class="form-status" data-form-status role="status" aria-live="polite"></p></form>'
    )
    card = (
        f'<div class="rep-card" data-reveal><h3>{e(REP["role"])}</h3><p class="rep-name">{e(REP["name"])}</p>'
        f'<p><a class="rep-mail" href="mailto:{REP["email"]}">{REP["email"]}</a></p>'
        '<h4>Evidence in this profile</h4><ul class="ticks"><li>Twelve labelled short clips</li>'
        '<li>Wearable-session screenshots</li><li>Cambrils UCF trial certificate and photographs</li>'
        '<li>School details supplied by the representative</li></ul></div>'
    )
    return section(v, "contact", f'<div class="contact-grid">{card}{form}</div>')


def provenance(v):
    rows = [
        ("Identity and school", "Supplied by Joseph's family and representative."),
        ("Footage", "Twelve clips supplied by the family. Titles and descriptions state only what is visible; dates, opponents and outcomes are not assigned."),
        ("Photographs", "Local profile media supplied for Joseph's page. Captions describe only what is visible."),
        ("Session data", f'Screenshots from a wearable tracker app for one session on {DATA["session"]["date"]}.'),
        ("Trial", "Participation certificate and photographs from the Cambrils UCF trial."),
        ("Last updated", long_date(UPDATED)),
        ("Design", "Original code. Aura design references are documented in the project repository; no Aura source code, fonts or media is redistributed."),
    ]
    body = "".join(f'<div class="prov"><dt>{e(k)}</dt><dd>{e(val)}</dd></div>' for k, val in rows)
    return section(v, "provenance", f'<dl class="prov-list" data-reveal>{body}</dl>')


# ---------------------------------------------------------------- heroes

def hero_open(cls, extra=""):
    return f'<section id="overview" class="hero {cls}" aria-labelledby="hero-title"{extra}>'


def hero1():
    rows = [
        ("Born", f"{DOB_TEXT} · Age {AGE}"),
        ("Nationality", P["nationality"]),
        ("Position", f'{P["position"]} · {P["number"]}'),
        ("School", f'{P["school"]}, {P["school_year"]}'),
        ("Feet", "Both used; right dominant in session"),
        ("Trial", "Cambrils UCF · participation documented"),
    ]
    table = "".join(f'<tr><th scope="row">{e(k)}</th><td>{e(val)}</td></tr>' for k, val in rows)
    return (
        hero_open("hero--dossier")
        + '<div class="dossier-sheet">'
        '<div class="dossier-head"><p class="dossier-file">Player file <strong>JO-10</strong></p>'
        '<p class="dossier-class">For scouts and coaches</p></div>'
        '<div class="dossier-grid">'
        f'<figure class="dossier-photo" data-reveal>{portrait()}<figcaption>Fig. 1 · Joseph Ojwang</figcaption></figure>'
        '<div class="dossier-main" data-reveal>'
        f'<p class="kicker">Recruitment dossier · {e(P["position"])}</p>{name_h1()}{idline()}'
        f"{ctas()}{stamp()}"
        f'<table class="dossier-table"><caption class="sr-only">Key details</caption><tbody>{table}</tbody></table>'
        "</div></div></div></section>"
    )


def queue(limit=3):
    out = []
    for clip in DATA["videos"][:limit]:
        cid = clip["id"]
        poster = f"/assets/posters/highlight-{cid}.jpg"
        w, h = size_of(poster)
        out.append(
            f'<li><a href="#clip-{cid}"><img src="{poster}" width="{w}" height="{h}" alt="" loading="lazy" decoding="async">'
            f'<span>{e(clip["title"])}</span> <span class="q-meta">Clip {cid} · {clip["orientation"].capitalize()} · {clip["duration"]}</span></a></li>'
        )
    return "".join(out)


def hero2():
    return (
        hero_open("hero--broadcast", " data-pointer-light")
        + '<div class="bc-frame">'
        f'<figure class="bc-photo">{portrait(stem="joseph-match-carry")}</figure>'
        '<div class="bc-copy">'
        '<p class="bc-tag"><span class="bc-dot" aria-hidden="true"></span> Player feature</p>'
        f"{name_h1('bc-name')}"
        '<div class="lower-third" data-reveal><span class="lt-num" aria-hidden="true">10</span>'
        f'<div class="lt-text"><p class="lt-role">{e(P["position"])} · {e(P["number"])}</p>'
        f'<p class="lt-meta">Age {AGE} · {e(P["nationality"])} · {e(P["school"])}, {e(P["school_year"])}</p></div></div>'
        f"{ctas()}{stamp()}</div>"
        f'<aside class="bc-queue" aria-label="Up next"><p class="bc-queue-title">Up next</p><ol>{queue()}</ol></aside>'
        "</div></section>"
    )


def hero3():
    return (
        hero_open("hero--programme")
        + '<div class="prog-mast"><span>Matchday programme</span><span>Player feature · No. 10</span>'
        '<span class="folio">p. 01</span></div>'
        '<div class="prog-spread">'
        '<div class="prog-cover" data-reveal><p class="prog-kicker">In focus</p>'
        f"{name_h1('prog-name')}"
        f'<p class="prog-standfirst">An attacking midfielder from {e(P["location"])}. Footage, documented trial participation and one recorded training session, gathered in one place.</p>'
        f"{idline()}{ctas()}{stamp()}</div>"
        f'<figure class="prog-photo" data-parallax="0.05">{portrait(stem="joseph-match-dribble-1")}<figcaption>Joseph Ojwang in match action. Photograph supplied for the profile.</figcaption></figure>'
        "</div></section>"
    )


PITCH_SVG = (
    '<svg class="pitch" viewBox="0 0 680 440" role="img" aria-labelledby="pitch-title">'
    '<title id="pitch-title">Diagram of the attacking half of a pitch. The two half-space channels are shaded and a #10 marker sits between them.</title>'
    '<g class="pitch-lines" fill="none" stroke="currentColor" stroke-width="2">'
    '<rect class="draw" x="10" y="10" width="660" height="420" pathLength="1"/>'
    '<path class="draw" d="M10 220 H90 M590 10 V430" pathLength="1"/>'
    '<rect class="draw" x="510" y="110" width="160" height="220" pathLength="1"/>'
    '<rect class="draw" x="620" y="170" width="50" height="100" pathLength="1"/>'
    '<path class="draw" d="M10 150 A70 70 0 0 1 10 290" pathLength="1"/>'
    '<path class="draw" d="M510 175 A55 55 0 0 0 510 265" pathLength="1"/></g>'
    '<g class="zones"><rect x="250" y="80" width="340" height="80" class="zone"/><rect x="250" y="280" width="340" height="80" class="zone"/></g>'
    '<path class="run draw" d="M250 230 C330 230 360 170 440 150" fill="none" pathLength="1"/>'
    '<g class="marker"><circle cx="250" cy="230" r="26"/><text x="250" y="238" text-anchor="middle">10</text></g>'
    '<text class="zone-label" x="560" y="128" text-anchor="end">Half-space</text>'
    '<text class="zone-label" x="560" y="328" text-anchor="end">Half-space</text></svg>'
)


def hero4():
    return (
        hero_open("hero--board", " data-pointer-light")
        + '<div class="board">'
        f'<div class="board-copy" data-reveal><p class="kicker">Tactical board · Role</p>{name_h1()}{idline()}{ctas()}{stamp()}</div>'
        f'<figure class="board-pitch" data-reveal>{PITCH_SVG}<figcaption>Illustrative zones for the position, not tracking data. <a href="#footage">Use the footage for player evidence.</a></figcaption></figure>'
        f'<figure class="board-photo">{portrait(stem="joseph-match-action")}</figure>'
        "</div></section>"
    )


def hero5():
    frames = [
        ("A", "Match photograph", portrait("strip-img", "joseph-match-carry")),
        ("B", "Trial certificate", img("trial-certificate", eager=True)),
        ("C", "Player portrait", img("hero-portrait", eager=True)),
        ("D", "Session tracker", img("stats-overview", eager=True)),
    ]
    strip = "".join(
        f'<li class="strip-frame" data-reveal><figure>{im}<figcaption><span>Exhibit {k}</span> {e(lbl)}</figcaption></figure></li>'
        for k, lbl, im in frames
    )
    return (
        hero_open("hero--archive")
        + '<div class="archive-head"><p>Evidence file · J. O. Ojwang</p>'
        f'<p>12 clips · {len(IMAGES)} images · 1 recorded session</p></div>'
        '<div class="archive-grid">'
        f'<div class="archive-copy" data-reveal><p class="kicker">Documented record</p>{name_h1()}{idline()}'
        f"{ctas()}{stamp()}"
        '<p class="archive-lede">Footage, photographs and documents are labelled by source and shown without unsupported match claims.</p></div>'
        f'<ol class="contact-strip">{strip}</ol></div></section>'
    )


def hero6():
    return (
        hero_open("hero--split")
        + '<div class="split-bg" aria-hidden="true"><span class="split-l">Left</span><span class="split-r">Right</span></div>'
        f'<figure class="split-photo">{portrait(stem="joseph-match-dribble-2")}</figure>'
        f'<div class="split-copy" data-reveal><p class="kicker">Single-session foot-use record</p>{name_h1()}{idline()}'
        '<p class="split-caveat"><strong>Context first.</strong> The figures below are from one technical session, not match data or a player benchmark.</p>'
        '<div class="split-meter" role="img" aria-label="Recorded session touches: 117 with the left foot, 235 with the right foot">'
        '<span class="sm-l" style="--w: 33%">117 L</span><span class="sm-r" style="--w: 67%">235 R</span></div>'
        '<p class="split-note">Touches in one 149-minute technical session. <a href="#data">Read the caveat</a></p>'
        f"{ctas()}{stamp()}</div></section>"
    )


def hero7():
    chapters = "".join(
        f'<li><a href="#{sid}"><span>{roman(SECTIONS.index(sid) + 1)}</span> {e(TITLE_OVERRIDES[7].get(sid, TITLES[sid]))}</a></li>'
        for sid in SECTIONS[1:]
    )
    return (
        hero_open("hero--ten", " data-pointer-light")
        + '<p class="ten-numeral" aria-hidden="true" data-parallax="-0.08">10</p>'
        f'<figure class="ten-photo" data-parallax="0.04">{portrait(stem="joseph-match-carry")}</figure>'
        f'<div class="ten-copy" data-reveal><p class="kicker">The Number Ten</p>{name_h1()}{idline()}{ctas()}{stamp()}</div>'
        f'<nav class="ten-chapters" aria-label="Chapters"><ol>{chapters}</ol></nav></section>'
    )


ROUTE_SVG = (
    '<svg class="route" viewBox="0 0 600 420" role="img" aria-labelledby="route-title route-desc">'
    '<title id="route-title">Route from Kitengela, Kenya to Cambrils, Catalonia</title>'
    '<desc id="route-desc">A stylised line, not to scale, joining Kitengela in Kenya with Cambrils and Barcelona in Spain.</desc>'
    '<g class="graticule" fill="none" stroke="currentColor" stroke-width="1">'
    '<path d="M0 105 H600 M0 210 H600 M0 315 H600 M150 0 V420 M300 0 V420 M450 0 V420"/></g>'
    '<path class="route-line draw" d="M470 360 C430 250 330 210 250 160 S150 90 130 80" fill="none" pathLength="1"/>'
    '<g class="route-stop"><circle cx="470" cy="360" r="8"/><text x="486" y="366">Kitengela</text></g>'
    '<g class="route-stop"><circle cx="130" cy="80" r="8"/><text x="112" y="66" text-anchor="end">Cambrils</text></g>'
    '<g class="route-stop route-stop--minor"><circle cx="165" cy="64" r="5"/><text x="178" y="56">Barcelona</text></g></svg>'
)


def hero8():
    return (
        hero_open("hero--route")
        + '<div class="route-wrap">'
        f'<div class="route-copy" data-reveal><p class="kicker">Kitengela to Cambrils</p>{name_h1()}{idline()}{ctas()}{stamp()}</div>'
        f'<figure class="route-map" data-reveal>{ROUTE_SVG}<figcaption>Not to scale. Shows where Joseph has studied and trained; it does not indicate a club registration.</figcaption></figure>'
        f'<figure class="route-photo">{portrait(stem="trial-action-1")}</figure></div></section>'
    )


def hero9():
    others = ["joseph-match-carry", "joseph-match-dribble-2", "action-kick", "trial-action-1", "joseph-team-photo"]
    frames = "".join(
        f'<li class="sheet-frame" data-reveal><a href="#photo-{s}">{img(s, eager=True)}<span class="frame-no">{i:02d}A</span></a></li>'
        for i, s in enumerate(others, 2)
    )
    return (
        hero_open("hero--sheet")
        + f'<div class="sheet-head"><p>Contact sheet 01</p><p>Joseph Ojwang · 12 clips · {len(IMAGES)} images</p></div>'
        '<div class="sheet-grid">'
        f'<figure class="sheet-key">{portrait(stem="joseph-match-action")}<figcaption><span class="frame-no">01A</span> Match frame</figcaption></figure>'
        f'<div class="sheet-copy" data-reveal><p class="kicker">Frame by frame</p>{name_h1()}{idline()}{ctas()}{stamp()}</div>'
        f'<ul class="sheet-frames" aria-label="More frames">{frames}</ul></div></section>'
    )


def hero10():
    s = DATA["session"]
    steps = [
        ("Who", f'{P["nationality"]} attacking midfielder wearing {P["number"]}. Age {AGE}. {P["school_year"]} at {P["school"]}.', "#profile", "Full profile"),
        ("Watch", "Start with Clip 13 to identify Joseph, then follow the labelled football sequences. Twelve clips in total; none autoplay.", "#clip-13", "Start with Clip 13"),
        ("Role", f'{P["position"]}. {P["foot"]}.', "#profile", "Viewing prompts"),
        ("Trial", f'Documented trial participation with {DATA["trial"]["club"]} in {DATA["trial"]["place"]}.', "#trial", "Trial documents"),
        ("Data", "One 149-minute technical session: 352 touches, 4.9 km, top speed 24.5 kph. Not match data.", "#data", "Session data and caveat"),
        ("Contact", f'{REP["name"]}, representative: {REP["email"]}.', "#contact", "Contact form"),
    ]
    items = "".join(
        f'<li class="step" id="step-{i}" data-step><p class="step-no">{i:02d} / 06</p><h2>{e(t)}</h2><p>{e(body)}</p>'
        f'<p><a class="step-link" href="{href}">{e(link)}</a></p></li>'
        for i, (t, body, href, link) in enumerate(steps, 1)
    )
    return (
        hero_open("hero--brief")
        + f'<div class="brief-top"><p class="kicker">60-second scout briefing</p>{stamp()}</div>'
        '<div class="brief-grid">'
        f'<div class="brief-id"><figure class="brief-photo">{portrait()}</figure>{name_h1()}{idline()}{ctas()}</div>'
        '<div class="brief-steps" data-stepper>'
        '<div class="step-nav" data-step-nav hidden><button type="button" class="step-btn" data-step-prev>Previous</button>'
        '<p class="step-count" data-step-count aria-live="polite">Step 1 of 6</p>'
        '<button type="button" class="step-btn" data-step-next>Next step</button></div>'
        f'<ol class="steps">{items}</ol>'
        '<p class="fine">You control the pace. There is no timer.</p></div></div></section>'
    )


HEROES = {1: hero1, 2: hero2, 3: hero3, 4: hero4, 5: hero5, 6: hero6, 7: hero7, 8: hero8, 9: hero9, 10: hero10}


# ---------------------------------------------------------------- page shell

FONT_PRELOADS = {
    1: ["newsreader-var.woff2", "geist-var.woff2"],
    2: ["big-shoulders-display-var.woff2", "geist-var.woff2"],
    3: ["instrument-serif.woff2", "big-shoulders-display-var.woff2"],
    4: ["archivo-var.woff2"],
    5: ["newsreader-var.woff2", "ibm-plex-mono-400.woff2"],
    6: ["geist-var.woff2", "archivo-var.woff2"],
    7: ["fraunces-var.woff2", "geist-var.woff2"],
    8: ["bricolage-grotesque-var.woff2", "newsreader-var.woff2"],
    9: ["instrument-serif.woff2", "ibm-plex-mono-400.woff2"],
    10: ["geist-var.woff2"],
}
VARIANT_JS = {4, 10}


def head(title, desc, css, preloads, theme):
    links = "".join(f'<link rel="preload" href="/shared/fonts/{f}" as="font" type="font/woff2" crossorigin>' for f in preloads)
    sheets = "".join(f'<link rel="stylesheet" href="{c}">' for c in css)
    return (
        '<!doctype html>\n<html lang="en" class="no-js">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{e(title)}</title>\n<meta name=\"description\" content=\"{e(desc)}\">\n"
        f'<meta name="theme-color" content="{theme}">\n<meta property="og:title" content="{e(title)}">\n'
        f'<meta property="og:description" content="{e(desc)}">\n'
        '<link rel="icon" href="/shared/favicon.svg" type="image/svg+xml">\n'
        f"{links}\n{sheets}\n"
        "<script>document.documentElement.classList.replace('no-js','js')</script>\n"
        '<script src="/shared/js/app.js" defer></script>\n'
    )


BASE_CSS = ["/shared/css/tokens.css", "/shared/css/base.css", "/shared/css/components.css", "/shared/css/motion.css"]
DESC = (
    f'{P["full_name"]}, {P["nationality"]} {P["position"].lower()} ({P["number"]}), age {AGE}. '
    f"Footage, documented Cambrils UCF trial participation, session data and representative contact."
)


def design_bar(v):
    meta = VARIANTS[v - 1]
    prev = VARIANTS[(v - 2) % 10]
    nxt = VARIANTS[v % 10]
    opt_items = []
    for x in VARIANTS:
        current = ' aria-current="page"' if x["n"] == v else ""
        opt_items.append(
            f'<li><a data-variant-link href="/{x["n"]}/"{current}>'
            f'<span class="sw-n">{x["n"]:02d}</span> <span class="sw-t">{e(x["name"])}</span> <small>{e(x["line"])}</small></a></li>'
        )
    opts = "".join(opt_items)
    return (
        '<nav class="design-bar" aria-label="Design variations">'
        '<a class="db-all" href="/">All Designs</a>'
        f'<a class="db-step" rel="prev" href="/{prev["n"]}/" aria-label="Previous design: {e(prev["name"])}"><span aria-hidden="true">←</span> <span class="db-step-t">Prev</span></a>'
        '<div class="switcher"><button type="button" class="switcher-toggle" data-switcher-toggle aria-expanded="false" aria-controls="switcher-panel">'
        f'<span class="sw-cur">Design {v:02d}/10</span> <span class="sw-curname">{e(meta["name"])}</span> <span class="sw-short" aria-hidden="true">{v:02d}/10</span> <span class="sw-caret" aria-hidden="true">▾</span></button>'
        f'<div class="switcher-panel" id="switcher-panel" hidden><p class="sw-head">Switch design · keeps your place</p><ul>{opts}</ul></div></div>'
        f'<a class="db-step" rel="next" href="/{nxt["n"]}/" aria-label="Next design: {e(nxt["name"])}"><span class="db-step-t">Next</span> <span aria-hidden="true">→</span></a>'
        '<button type="button" class="motion-toggle" data-motion-toggle aria-pressed="false"><span class="mt-icon" aria-hidden="true"></span><span class="mt-label">Pause motion</span></button>'
        "</nav>"
    )


def site_header(v):
    links = "".join(
        f'<li><a href="#{sid}">{e(TITLES[sid].replace("Contact the representative", "Contact").replace("Sources and provenance", "Sources").replace("Cambrils UCF trial", "Trial").replace("Player profile", "Profile"))}</a></li>'
        for sid in SECTION_ORDERS[v]
    )
    return (
        '<header class="site-header"><a class="brand" href="#overview">J. Ojwang <span>#10</span></a>'
        '<button type="button" class="menu-toggle" data-menu-toggle aria-expanded="false" aria-controls="site-nav">Menu</button>'
        f'<nav class="site-nav" id="site-nav" aria-label="Sections"><ul>{links}</ul></nav></header>'
    )


def lightbox():
    hp = thumb_url("hero-portrait")
    w, h = size_of(hp)
    return (
        '<dialog class="lightbox" id="lightbox" aria-labelledby="lightbox-title">'
        '<div class="lb-inner"><h2 class="sr-only" id="lightbox-title">Image viewer</h2>'
        f'<figure class="lb-figure"><img class="lb-img" src="{hp}" width="{w}" height="{h}" alt="" loading="lazy" decoding="async">'
        '<figcaption class="lb-caption" data-lb-caption></figcaption></figure>'
        '<div class="lb-controls"><button type="button" class="lb-btn" data-lb-prev>Previous image</button>'
        '<p class="lb-count" data-lb-count aria-live="polite"></p>'
        '<button type="button" class="lb-btn" data-lb-next>Next image</button>'
        '<button type="button" class="lb-btn lb-close" data-lb-close>Close</button></div></div></dialog>'
    )


def footer():
    return (
        '<footer class="site-footer"><div class="foot-inner">'
        f'<p class="foot-name">{e(P["full_name"])} · {e(P["position"])} {e(P["number"])}</p>'
        f'<p>Representative: {e(REP["name"])} · <a href="mailto:{REP["email"]}">{REP["email"]}</a></p>'
        f'<p>{UPDATED_TEXT} · <a href="/">All Designs</a> · <a href="#overview">Back to top</a></p>'
        "</div></footer>"
    )


SECTION_BUILDERS = {
    "footage": footage,
    "profile": profile,
    "trial": trial,
    "data": data_section,
    "gallery": gallery,
    "contact": contact,
    "provenance": provenance,
}

# Each design keeps the same evidence but presents a different scouting workflow.
# The switcher preserves stable anchors, so routes remain directly comparable.
SECTION_ORDERS = {
    1: ["profile", "footage", "trial", "data", "gallery", "contact", "provenance"],
    2: ["footage", "profile", "data", "trial", "gallery", "contact", "provenance"],
    3: ["profile", "gallery", "footage", "trial", "data", "contact", "provenance"],
    4: ["footage", "profile", "data", "gallery", "trial", "contact", "provenance"],
    5: ["trial", "gallery", "footage", "profile", "data", "contact", "provenance"],
    6: ["footage", "data", "profile", "gallery", "trial", "contact", "provenance"],
    7: ["footage", "gallery", "profile", "trial", "data", "contact", "provenance"],
    8: ["profile", "trial", "gallery", "footage", "data", "contact", "provenance"],
    9: ["gallery", "footage", "profile", "trial", "data", "contact", "provenance"],
    10: ["profile", "footage", "trial", "data", "gallery", "contact", "provenance"],
}


def profile_page(v):
    meta = VARIANTS[v - 1]
    nn = f"{v:02d}"
    css = BASE_CSS + [f"/variations/{nn}/variant.css"]
    out = head(f'{P["full_name"]} · {P["position"]} {P["number"]} · Design {nn} {meta["name"]}', DESC, css, FONT_PRELOADS[v], meta["palette"][0])
    if v in VARIANT_JS:
        out += f'<script src="/variations/{nn}/variant.js" defer></script>\n'
    out += "</head>\n"
    out += f'<body class="profile v{nn}" data-variant="{nn}">\n'
    out += '<a class="skip-link" href="#main">Skip to main content</a>\n'
    out += '<div class="progress" aria-hidden="true"><span></span></div>\n'
    out += design_bar(v) + "\n" + site_header(v) + "\n"
    out += '<main id="main" tabindex="-1">\n' + HEROES[v]() + "\n"
    rest = "\n".join(SECTION_BUILDERS[sid](v) for sid in SECTION_ORDERS[v])
    if v == 1:
        idx = "".join(
            f'<li><a href="#{sid}"><span>§ {SECTIONS.index(sid) + 1:02d}</span> {e(TITLES[sid])}</a></li>' for sid in SECTION_ORDERS[v]
        )
        rest = (
            f'<div class="dossier-body"><nav class="dossier-index" aria-label="Dossier index"><p>Index</p><ol>{idx}</ol></nav>'
            f'<div class="dossier-pages">\n{rest}\n</div></div>'
        )
    out += rest + "\n</main>\n" + footer() + "\n" + lightbox() + "\n</body>\n</html>\n"
    return out


HUB_THUMBS = ["hero-portrait", "joseph-match-action", "portrait-1", "joseph-match-carry", "trial-certificate",
              "joseph-match-dribble-2", "portrait-2", "trial-pitch", "joseph-match-dribble-1", "action-kick"]


def hub_page():
    out = head(
        f'The Selection Room · {P["full_name"]} profile designs',
        f'Ten profile designs for {P["full_name"]}, {P["nationality"]} {P["position"].lower()} {P["number"]}. Choose a design, watch footage or contact his representative.',
        BASE_CSS + ["/shared/css/hub.css"],
        ["big-shoulders-display-var.woff2", "geist-var.woff2"],
        "#0c0d0c",
    )
    cards = []
    for x, stem in zip(VARIANTS, HUB_THUMBS):
        c1, c2, c3 = x["palette"]
        cards.append(
            f'<li class="card" style="--c1: {c1}; --c2: {c2}; --c3: {c3}" data-pointer-light data-reveal>'
            f'<div class="card-preview" aria-hidden="true">{img(stem, alt="")}<span class="card-num">{x["n"]:02d}</span>'
            '<span class="card-swatches"><i></i><i></i><i></i></span></div>'
            f'<div class="card-body"><h3><a class="card-link" data-card href="/{x["n"]}/">{e(x["name"])}</a></h3>'
            f'<p>{e(x["line"])}</p>'
            f'<ul class="card-shortcuts"><li><a href="/{x["n"]}/#footage">Watch<span class="sr-only"> footage in {e(x["name"])}</span></a></li>'
            f'<li><a href="/{x["n"]}/#contact">Contact<span class="sr-only"> the representative via {e(x["name"])}</span></a></li></ul></div></li>'
        )
    out += "</head>\n<body class=\"hub\">\n"
    out += '<a class="skip-link" href="#main">Skip to main content</a>\n'
    out += (
        '<header class="hub-header"><p class="hub-brand">J. Ojwang <span>#10</span></p>'
        '<nav aria-label="Shortcuts"><ul><li><a href="#designs">Designs</a></li><li><a href="/1/#footage">Footage</a></li>'
        '<li><a href="/1/#contact">Contact</a></li></ul></nav>'
        '<button type="button" class="motion-toggle" data-motion-toggle aria-pressed="false"><span class="mt-icon" aria-hidden="true"></span><span class="mt-label">Pause motion</span></button></header>\n'
    )
    out += (
        '<main id="main" tabindex="-1">\n<section class="hub-hero" aria-labelledby="hub-title" data-pointer-light>'
        f'<div class="hub-copy" data-reveal><p class="kicker">Ten profile designs · {e(P["full_name"])}</p>'
        '<h1 id="hub-title">The Selection Room</h1>'
        f'<p class="hub-lede">Every design carries the same documented profile facts, all 12 clips, the full gallery and a direct line to Joseph\'s representative. Pick the presentation that suits how you scout.</p>'
        f"{idline()}"
        '<div class="cta-row"><a class="btn btn--primary" href="/1/#footage">Watch Footage</a>'
        '<a class="btn btn--ghost" href="/1/#contact">Contact Representative</a></div>'
        f"{stamp()}</div>"
        f'<figure class="hub-photo">{portrait(stem="joseph-match-carry")}<figcaption>{e(P["full_name"])} in match action</figcaption></figure></section>\n'
        '<section id="designs" class="hub-designs" aria-labelledby="designs-title"><div class="hub-designs-head">'
        '<h2 id="designs-title">Choose a design</h2><p>Each card opens the full profile. Shortcuts jump straight to footage or contact.</p></div>'
        f'<ol class="cards">{"".join(cards)}</ol></section>\n'
        '<section class="hub-facts" aria-labelledby="facts-title"><h2 id="facts-title">The facts every design shares</h2>'
        f"{facts_block()}"
        f'<p class="fine">Session figures come from one 149-minute technical session and are not match data. {UPDATED_TEXT}.</p></section>\n'
        "</main>\n"
    )
    out += (
        f'<footer class="site-footer"><div class="foot-inner"><p class="foot-name">{e(P["full_name"])}</p>'
        f'<p>Representative: {e(REP["name"])} · <a href="mailto:{REP["email"]}">{REP["email"]}</a></p></div></footer>\n'
        "</body>\n</html>\n"
    )
    return out


def not_found_page():
    out = head(f'Page not found · {P["full_name"]}', "This page does not exist. Return to the profile designs.", BASE_CSS + ["/shared/css/hub.css"], [], "#0c0d0c")
    out += "</head>\n<body class=\"hub hub--404\">\n"
    out += '<a class="skip-link" href="#main">Skip to main content</a>\n'
    out += (
        '<main id="main" tabindex="-1"><section class="nf" aria-labelledby="nf-title">'
        '<p class="kicker">404</p><h1 id="nf-title">This page is offside</h1>'
        '<p>The address does not match any page. The profile is still one step away.</p>'
        '<div class="cta-row"><a class="btn btn--primary" href="/">All Designs</a>'
        '<a class="btn btn--ghost" href="/1/#footage">Watch Footage</a>'
        '<a class="btn btn--ghost" href="/1/#contact">Contact Representative</a></div></section></main>\n'
        "</body>\n</html>\n"
    )
    return out


def outputs():
    files = {"index.html": hub_page(), "404.html": not_found_page()}
    for x in VARIANTS:
        files[f'{x["n"]}/index.html'] = profile_page(x["n"])
    return files


def main(argv):
    check = "--check" in argv
    stale = []
    for rel, html in outputs().items():
        path = ROOT / rel
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != html:
                stale.append(rel)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(html, encoding="utf-8")
    if check and stale:
        print("Out of date (run python3 tools/generate.py):", ", ".join(stale))
        return 1
    if not check:
        print(f"Generated {len(outputs())} pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
