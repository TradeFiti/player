"""Structural acceptance tests for the Joseph Ojwang profile site.

Dependency-free: run with `python3 -m unittest discover -s tests -v`.
"""

import hashlib
import json
import re
import struct
import subprocess
import sys
import unittest
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
VARIANTS = [str(n) for n in range(1, 11)]
PROFILE_ROUTES = {n: ROOT / n / "index.html" for n in VARIANTS}
HUB = ROOT / "index.html"
NOT_FOUND = ROOT / "404.html"
ALL_PAGES = [HUB, NOT_FOUND, *PROFILE_ROUTES.values()]
REQUIRED_ANCHORS = ["overview", "footage", "profile", "trial", "data", "gallery", "contact", "provenance"]
NEW_MATCH_IMAGES = [
    "joseph-match-action",
    "joseph-match-carry",
    "joseph-match-dribble-1",
    "joseph-match-dribble-2",
    "joseph-team-photo",
]
VIDEO_FILES = sorted(p.name for p in (ROOT / "assets" / "videos").glob("*.mp4"))
PROFILE_DATA = json.loads((ROOT / "shared" / "data" / "profile.json").read_text(encoding="utf-8"))
PROFILE_IMAGE_STEMS = [item["stem"] for item in PROFILE_DATA["images"]]
LAST_UPDATED = date(2026, 11, 14)
DOB = date(2010, 9, 13)
FORMSUBMIT = "https://formsubmit.co/"


def expected_age():
    return LAST_UPDATED.year - DOB.year - ((LAST_UPDATED.month, LAST_UPDATED.day) < (DOB.month, DOB.day))


class Node:
    def __init__(self, tag, attrs, parent):
        self.tag = tag
        self.attrs = dict(attrs)
        self.parent = parent
        self.children = []
        self.text = []


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Doc(HTMLParser):
    """Tiny tolerant DOM: enough to query tags, attributes and visible text."""

    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", [], None)
        self.cur = self.root
        self.all = []
        self.text_parts = []
        self._skip = 0
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.cur)
        self.cur.children.append(node)
        self.all.append(node)
        if tag in ("script", "style"):
            self._skip += 1
        if tag not in VOID:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        node = Node(tag, attrs, self.cur)
        self.cur.children.append(node)
        self.all.append(node)

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip = max(0, self._skip - 1)
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        if self._skip:
            return
        self.cur.text.append(data)
        self.text_parts.append(data)

    def find(self, tag=None, **attrs):
        out = []
        for n in self.all:
            if tag and n.tag != tag:
                continue
            if all(n.attrs.get(k.rstrip("_").replace("_", "-")) == v if v is not True else k.rstrip("_").replace("_", "-") in n.attrs for k, v in attrs.items()):
                out.append(n)
        return out

    @property
    def text(self):
        return re.sub(r"\s+", " ", " ".join(self.text_parts))


def node_text(node):
    parts = list(node.text)
    for c in node.children:
        parts.append(node_text(c))
    return re.sub(r"\s+", " ", " ".join(parts)).strip()


_cache = {}


def load(path):
    if path not in _cache:
        raw = path.read_text(encoding="utf-8")
        _cache[path] = (raw, Doc(raw))
    return _cache[path]


def resolve_local(url):
    """Map a root-relative URL to a file in the repo (None if external/anchor)."""
    if not url or url.startswith(("#", "mailto:", "tel:", "data:")):
        return None
    parts = urlsplit(url)
    if parts.scheme or parts.netloc:
        return None
    path = parts.path
    if not path:
        return None
    if path.endswith("/"):
        path += "index.html"
    return ROOT / path.lstrip("/")


def mp4_is_landscape(path):
    """Read the video track header (tkhd) and account for its rotation matrix."""
    data = path.read_bytes()

    def atoms(buf, start, end):
        i = start
        while i + 8 <= end:
            size, kind = struct.unpack(">I4s", buf[i:i + 8])
            header = 8
            if size == 1:
                size = struct.unpack(">Q", buf[i + 8:i + 16])[0]
                header = 16
            elif size == 0:
                size = end - i
            yield kind.decode("latin-1"), i + header, i + size
            i += size

    for kind, s, e in atoms(data, 0, len(data)):
        if kind != "moov":
            continue
        for k2, s2, e2 in atoms(data, s, e):
            if k2 != "trak":
                continue
            for k3, s3, e3 in atoms(data, s2, e2):
                if k3 != "tkhd":
                    continue
                version = data[s3]
                off = s3 + 4 + (32 if version == 1 else 20) + 8 + 8
                a, b = struct.unpack(">ii", data[off:off + 8])
                w, h = struct.unpack(">II", data[off + 36:off + 44])
                w, h = w >> 16, h >> 16
                if w and h:
                    if b != 0 and a == 0:
                        w, h = h, w
                    return w > h
    raise AssertionError(f"no video track in {path}")


class RouteTests(unittest.TestCase):
    def test_routes_exist(self):
        for page in ALL_PAGES:
            self.assertTrue(page.is_file(), f"missing {page.relative_to(ROOT)}")

    def test_vercel_config(self):
        cfg = json.loads((ROOT / "vercel.json").read_text())
        self.assertIs(cfg.get("trailingSlash"), True)
        for rule in cfg.get("rewrites", []):
            self.assertNotIn(rule.get("destination"), ("/", "/index.html"), "no SPA catch-all")

    def test_aura_inspiration_doc(self):
        doc = (ROOT / "docs" / "AURA-INSPIRATION.md").read_text()
        for needle in [
            "https://www.aura.build/templates/kaltgrat-abfahrt-95",
            "https://www.aura.build/templates/massif",
            "https://www.aura.build/templates/marcus-thorne",
            "https://www.aura.build/templates/ateevibes-own-98",
            "https://www.aura.build/editor/d4270c68-1879-41a9-a0ad-c1dc884ad758",
            "https://www.aura.build/component/7B0754E",
            "https://www.aura.build/component/FD742C",
            "https://www.aura.build/component/AADF2A",
            "https://www.aura.build/component/1077BC",
            "https://www.aura.build/component/EDCC99",
            "Vannarot Roeung", "Sourasith Phomhome", "Meng To",
        ]:
            self.assertIn(needle, doc)
        self.assertRegex(doc.lower(), r"private")
        self.assertRegex(doc.lower(), r"not redistributed")


class CommonPageTests(unittest.TestCase):
    def test_landmarks_and_single_h1(self):
        for page in ALL_PAGES:
            raw, doc = load(page)
            with self.subTest(page=page.relative_to(ROOT)):
                self.assertEqual(len(doc.find("h1")), 1)
                self.assertEqual(len(doc.find("main")), 1)
                main = doc.find("main")[0]
                self.assertEqual(main.attrs.get("id"), "main")
                skips = [a for a in doc.find("a") if a.attrs.get("href") == "#main" and "skip-link" in a.attrs.get("class", "")]
                self.assertEqual(len(skips), 1)
                self.assertTrue(doc.find("html")[0].attrs.get("lang"))
                self.assertTrue(doc.find("meta", name="viewport"))
                self.assertTrue(doc.find("meta", name="description"))

    def test_heading_order_is_logical(self):
        for page in ALL_PAGES:
            _, doc = load(page)
            levels = [int(n.tag[1]) for n in doc.all if re.fullmatch(r"h[1-6]", n.tag)]
            with self.subTest(page=page.relative_to(ROOT)):
                self.assertEqual(levels[0], 1)
                for prev, cur in zip(levels, levels[1:]):
                    self.assertLessEqual(cur, prev + 1, f"heading jump h{prev}->h{cur}")

    def test_unique_ids(self):
        for page in ALL_PAGES:
            _, doc = load(page)
            ids = [n.attrs["id"] for n in doc.all if "id" in n.attrs]
            with self.subTest(page=page.relative_to(ROOT)):
                self.assertEqual(len(ids), len(set(ids)), [i for i in ids if ids.count(i) > 1])

    def test_images_have_alt_and_dimensions(self):
        for page in ALL_PAGES:
            _, doc = load(page)
            for img in doc.find("img"):
                with self.subTest(page=page.relative_to(ROOT), src=img.attrs.get("src")):
                    self.assertIn("alt", img.attrs)
                    self.assertIn("width", img.attrs)
                    self.assertIn("height", img.attrs)

    def test_local_references_resolve(self):
        missing = []
        for page in ALL_PAGES:
            _, doc = load(page)
            for n in doc.all:
                urls = [n.attrs.get(k) for k in ("src", "href", "poster", "data-full", "data-src")]
                if n.attrs.get("srcset"):
                    urls += [c.strip().split(" ")[0] for c in n.attrs["srcset"].split(",")]
                for u in urls:
                    if u and not u.startswith(("/", "#", "mailto:", "https://", "tel:")):
                        missing.append((page.relative_to(ROOT), u, "not root-relative"))
                    target = resolve_local(u)
                    if target is not None and not target.exists():
                        missing.append((page.relative_to(ROOT), u))
                    if u and u.startswith("#") and len(u) > 1:
                        if not doc.find(id=u[1:]):
                            missing.append((page.relative_to(ROOT), u, "missing anchor"))
        for css in list((ROOT / "shared").rglob("*.css")) + list((ROOT / "variations").rglob("*.css")):
            for u in re.findall(r"url\(\s*['\"]?([^'\")]+)", css.read_text()):
                if u.startswith("data:"):
                    continue
                target = resolve_local(u)
                if target is None or not target.exists():
                    missing.append((css.relative_to(ROOT), u))
        self.assertEqual(missing, [])

    def test_no_remote_runtime_dependencies(self):
        files = ALL_PAGES + list((ROOT / "shared").rglob("*.css")) + list((ROOT / "shared").rglob("*.js")) + list((ROOT / "variations").rglob("*.*"))
        for f in files:
            raw = f.read_text(encoding="utf-8")
            with self.subTest(file=f.relative_to(ROOT)):
                for url in re.findall(r"(?:https?:)?//[A-Za-z0-9.-]+\.[a-z]{2,}[^\s\"'<>)]*", raw):
                    if url.startswith("//") and f.suffix == ".js":
                        continue  # JS line comments
                    self.assertTrue(url.startswith(FORMSUBMIT) or url.startswith("http://www.w3.org/"), url)
                low = raw.lower()
                for banned in ["tailwind", "googleapis", "gstatic", "unpkg", "jsdelivr", "cdnjs", "aos.js", "aos.css", "glightbox", "iconify", "gsap", "three.module", "three.min"]:
                    self.assertNotIn(banned, low)

    def test_no_rotated_video_controls(self):
        files = ALL_PAGES + list((ROOT / "shared").rglob("*.css")) + list((ROOT / "shared").rglob("*.js")) + list((ROOT / "variations").rglob("*.*"))
        for f in files:
            raw = f.read_text(encoding="utf-8").replace(" ", "")
            self.assertNotIn("rotate(-90deg)", raw, f)
            self.assertNotIn("rotate(90deg)", raw, f)


class HubTests(unittest.TestCase):
    def test_hub_selection_room(self):
        raw, doc = load(HUB)
        self.assertIn("The Selection Room", doc.text)
        cards = doc.find("a", **{"data-card": True})
        self.assertEqual(sorted(a.attrs["href"] for a in cards), sorted(f"/{n}/" for n in VARIANTS))
        hrefs = {a.attrs.get("href") for a in doc.find("a")}
        for n in VARIANTS:
            self.assertIn(f"/{n}/#footage", hrefs)
            self.assertIn(f"/{n}/#contact", hrefs)
        self.assertIn("Joseph Omondi Ojwang", doc.text)
        self.assertIn("14 November 2026", doc.text)

    def test_404(self):
        _, doc = load(NOT_FOUND)
        hrefs = {a.attrs.get("href") for a in doc.find("a")}
        self.assertIn("/", hrefs)


class ProfileTests(unittest.TestCase):
    def each(self):
        for n, page in PROFILE_ROUTES.items():
            raw, doc = load(page)
            yield n, raw, doc

    def test_required_anchors(self):
        for n, raw, doc in self.each():
            for anchor in REQUIRED_ANCHORS:
                with self.subTest(route=n, anchor=anchor):
                    self.assertEqual(len(doc.find(id=anchor)), 1)

    def test_navigation_contract(self):
        for n, raw, doc in self.each():
            with self.subTest(route=n):
                links = doc.find("a")
                texts = {node_text(a): a.attrs.get("href") for a in links}
                self.assertEqual(texts.get("All Designs"), "/")
                prev = doc.find("a", rel="prev")
                nxt = doc.find("a", rel="next")
                self.assertEqual(len(prev), 1)
                self.assertEqual(len(nxt), 1)
                i = int(n)
                self.assertEqual(prev[0].attrs["href"], f"/{(i - 2) % 10 + 1}/")
                self.assertEqual(nxt[0].attrs["href"], f"/{i % 10 + 1}/")
                toggles = doc.find("button", **{"data-switcher-toggle": True})
                self.assertEqual(len(toggles), 1)
                t = toggles[0]
                self.assertEqual(t.attrs.get("aria-expanded"), "false")
                panel = doc.find(id=t.attrs.get("aria-controls"))
                self.assertEqual(len(panel), 1)
                options = [a for a in links if "data-variant-link" in a.attrs]
                self.assertEqual(sorted(a.attrs["href"] for a in options), sorted(f"/{v}/" for v in VARIANTS))
                current = [a for a in options if a.attrs.get("aria-current") == "page"]
                self.assertEqual([a.attrs["href"] for a in current], [f"/{n}/"])

    def test_above_fold_ctas(self):
        for n, raw, doc in self.each():
            with self.subTest(route=n):
                overview = doc.find(id="overview")[0]
                text = node_text(overview)
                self.assertIn("Watch Footage", text)
                self.assertIn("Contact Representative", text)
                self.assertIn("Last updated 14 November 2026", text)
                self.assertIn("Joseph", text)
                imgs = [c for c in walk(overview) if c.tag == "img"]
                self.assertTrue(any("Joseph" in i.attrs.get("alt", "") for i in imgs), "hero includes a player-identifying image")
                hrefs = [a.attrs.get("href") for a in walk(overview) if a.tag == "a"]
                self.assertIn("#footage", hrefs)
                self.assertIn("#contact", hrefs)
                h1 = doc.find("h1")[0]
                self.assertTrue(any(c is h1 for c in walk(overview)), "h1 lives in the hero")

    def test_canonical_facts(self):
        age = expected_age()
        for n, raw, doc in self.each():
            t = doc.text
            with self.subTest(route=n):
                for fact in [
                    "Joseph Omondi Ojwang", "13 September 2010", f"Age {age}", "Kenyan",
                    "Attacking Midfielder", "#10", "Kitengela International School", "Year 10",
                    "Martin Lugendo", "oluwamartin@gmail.com", "Representative", "Cambrils UCF",
                    "149-minute",
                ]:
                    self.assertIn(fact, t)
                self.assertIn("mailto:oluwamartin@gmail.com", raw)

    def test_session_caveat_near_data(self):
        for n, raw, doc in self.each():
            data = node_text(doc.find(id="data")[0])
            with self.subTest(route=n):
                self.assertIn("one 149-minute technical session", data)
                self.assertRegex(data, r"not (a )?match")

    def test_identical_canonical_module(self):
        """Every route carries the same canonical facts block (data-canonical)."""
        blocks = set()
        for n, raw, doc in self.each():
            nodes = doc.find(**{"data-canonical": "facts"})
            self.assertEqual(len(nodes), 1, n)
            blocks.add(node_text(nodes[0]))
        self.assertEqual(len(blocks), 1)

    def test_video_library(self):
        self.assertEqual(len(VIDEO_FILES), 12)
        for n, raw, doc in self.each():
            footage = doc.find(id="footage")[0]
            videos = [c for c in walk(footage) if c.tag == "video"]
            with self.subTest(route=n):
                srcs = set()
                for v in videos:
                    self.assertEqual(v.attrs.get("preload"), "none")
                    self.assertIn("controls", v.attrs)
                    self.assertNotIn("autoplay", v.attrs)
                    self.assertTrue(v.attrs.get("poster", "").startswith("/assets/posters/"))
                    for c in walk(v):
                        if c.tag == "source":
                            srcs.add(Path(c.attrs["src"]).name)
                    if v.attrs.get("src"):
                        srcs.add(Path(v.attrs["src"]).name)
                self.assertEqual(sorted(srcs), VIDEO_FILES)
                default = [v for v in videos if "data-default" in v.attrs]
                self.assertEqual(len(default), 1)
                name = next(Path(c.attrs["src"]).name for c in walk(default[0]) if c.tag == "source")
                self.assertTrue(mp4_is_landscape(ROOT / "assets" / "videos" / name), f"default {name} not landscape")
                labels = [node_text(c) for c in walk(footage) if "data-clip-label" in c.attrs]
                self.assertGreaterEqual(len(labels), 12)
                self.assertTrue(all(" · " in label for label in labels), "every clip has a useful title and metadata")
                self.assertIn("Start here: player introduction", node_text(footage))

    def test_gallery_media(self):
        for n, raw, doc in self.each():
            gallery = doc.find(id="gallery")[0]
            refs = " ".join(" ".join(filter(None, [c.attrs.get("src"), c.attrs.get("href"), c.attrs.get("data-full")])) for c in walk(gallery))
            with self.subTest(route=n):
                for stem in NEW_MATCH_IMAGES:
                    self.assertIn(stem, refs)
                site_refs = raw
                for stem in PROFILE_IMAGE_STEMS:
                    self.assertIn(f"/assets/images/{stem}", site_refs.replace("/thumbs/", "/").replace("/web/", "/"), stem)
                self.assertNotIn("cambrils-instagram", site_refs)
                self.assertNotIn("trial-certificate-2", site_refs)
                self.assertNotIn(">New<", raw)
                dialogs = doc.find("dialog")
                self.assertEqual(len(dialogs), 1)
                self.assertTrue(dialogs[0].attrs.get("aria-labelledby") or dialogs[0].attrs.get("aria-label"))

    def test_contact_form(self):
        for n, raw, doc in self.each():
            contact = doc.find(id="contact")[0]
            nodes = list(walk(contact))
            forms = [c for c in nodes if c.tag == "form"]
            with self.subTest(route=n):
                self.assertEqual(len(forms), 1)
                f = forms[0]
                self.assertEqual(f.attrs.get("action"), "https://formsubmit.co/oluwamartin@gmail.com")
                self.assertEqual(f.attrs.get("method", "").upper(), "POST")
                fields = [c for c in walk(f) if c.tag in ("input", "textarea", "select") and c.attrs.get("type") not in ("hidden", "submit")]
                label_for = {c.attrs.get("for") for c in walk(f) if c.tag == "label"}
                for fld in fields:
                    if fld.attrs.get("name") == "_honey":
                        continue
                    self.assertIn(fld.attrs.get("id"), label_for, fld.attrs)
                self.assertTrue(any(c.attrs.get("name") == "_honey" for c in walk(f)))
                self.assertTrue(any(c.attrs.get("aria-live") for c in walk(f)))
                self.assertRegex(node_text(contact).lower(), r"privacy")
                self.assertIn("external form processor", node_text(contact).lower())
                self.assertIn("email the representative directly", node_text(contact).lower())
                self.assertNotIn("Contact Agent", node_text(contact))

    def test_contact_ajax_rejects_processor_failures(self):
        app = (ROOT / "shared" / "js" / "app.js").read_text(encoding="utf-8")
        self.assertIn("data.success !== true", app)
        self.assertIn("Form processor rejected the enquiry", app)

    def test_motion_controls(self):
        for n, raw, doc in self.each():
            with self.subTest(route=n):
                b = doc.find("button", **{"data-motion-toggle": True})
                self.assertEqual(len(b), 1)
                self.assertIn(b[0].attrs.get("aria-pressed"), ("false", "true"))
                html = doc.find("html")[0]
                self.assertNotIn("motion-ready", html.attrs.get("class", ""), "motion-ready must only be added by JS")

    def test_variant_assets_and_distinctness(self):
        hero_hashes = set()
        css_hashes = set()
        section_orders = set()
        for n, raw, doc in self.each():
            nn = n.zfill(2)
            with self.subTest(route=n):
                self.assertIn(f"/variations/{nn}/variant.css", raw)
                self.assertEqual(doc.find("body")[0].attrs.get("data-variant"), nn)
                css = (ROOT / "variations" / nn / "variant.css").read_text()
                self.assertGreater(len(css), 3000, "variant needs a real design")
                css_hashes.add(hashlib.sha1(css.encode()).hexdigest())
                hero = doc.find(id="overview")[0]
                hero_hashes.add(hashlib.sha1(repr(structure(hero)).encode()).hexdigest())
                main = doc.find("main")[0]
                section_orders.add(tuple(c.attrs.get("id") for c in walk(main) if c.tag == "section" and c.attrs.get("id") in REQUIRED_ANCHORS))
        self.assertEqual(len(css_hashes), 10)
        self.assertEqual(len(hero_hashes), 10, "each hero must have distinct markup")
        self.assertGreaterEqual(len(section_orders), 8, "designs must present meaningfully different scouting workflows")

    def test_sticky_anchor_offset_and_skip_order(self):
        for n, raw, doc in self.each():
            first_link = doc.find("a")[0]
            self.assertIn("skip-link", first_link.attrs.get("class", ""), n)


class ContentSafetyTests(unittest.TestCase):
    BANNED = [
        r"\bage\s*:?\s*15\b", r"\b15\s*(years?|yrs)\b", r"summer 2026", r"successful(ly)? trial",
        r"fully certified", r"ready for (the )?next level", r"\belite\b", r"top \d+\s*%", r"percentile",
        r"better than (most|\d)", r"weak[- ]foot.*(population|average)", r"\bagent\b", r"lorem", r"ipsum",
        r"\btodo\b", r"\bfixme\b", r"john doe", r"jane doe", r"scout said", r"kaltgrat", r"massif",
        r"marcus thorne", r"veloce", r"ateevibes", r"aura\.build", r"\bacademy benchmark",
        r"\bsigned\b", r"contract offer", r"full[- ]length footage", r"tracker export", r"verified facts",
        r"every statement on this page points to",
    ]

    def test_banned_phrases(self):
        for page in ALL_PAGES:
            raw, doc = load(page)
            low = doc.text.lower()
            for pat in self.BANNED:
                with self.subTest(page=page.relative_to(ROOT), pattern=pat):
                    self.assertIsNone(re.search(pat, low), pat)
            self.assertNotRegex(raw, r"[“\"][^”\"]{10,}[”\"]\s*[—-]\s*(scout|coach)", "no unattributed scout quotes")


class MotionAndTouchContracts(unittest.TestCase):
    def css_files(self):
        return sorted((ROOT / "shared" / "css").glob("*.css")) + sorted((ROOT / "variations").rglob("*.css"))

    def test_shared_css_files_exist(self):
        for name in ["tokens", "base", "components", "motion"]:
            self.assertTrue((ROOT / "shared" / "css" / f"{name}.css").is_file(), name)
        self.assertTrue((ROOT / "shared" / "js" / "app.js").is_file())
        for nn in [str(i).zfill(2) for i in range(1, 11)]:
            self.assertTrue((ROOT / "variations" / nn / "variant.css").is_file(), nn)

    def test_reduced_motion_contract(self):
        motion = (ROOT / "shared" / "css" / "motion.css").read_text()
        self.assertIn("prefers-reduced-motion: reduce", motion)
        self.assertIn(".motion-paused", motion)
        self.assertIn("scroll-behavior: auto", motion)
        js = (ROOT / "shared" / "js" / "app.js").read_text()
        self.assertIn("prefers-reduced-motion: reduce", js)
        self.assertIn("saveData", js)
        self.assertIn("visibilitychange", js)
        self.assertIn("IntersectionObserver", js)
        self.assertIn("motion-ready", js)

    def test_hidden_states_only_under_motion_ready(self):
        """Content may only start invisible when JS has opted into motion."""
        offenders = []
        for css in self.css_files():
            text = re.sub(r"/\*.*?\*/", "", css.read_text(), flags=re.S)
            text = re.sub(r"@keyframes[^{]+\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", "", text)
            for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", text):
                if re.search(r"(^|;)\s*opacity\s*:\s*0(\.0+)?\s*(;|$|!)", body.strip()) or re.search(r"visibility\s*:\s*hidden", body):
                    sel = sel.strip()
                    if "motion-ready" in sel or any(ok in sel for ok in ("[hidden]", "::backdrop", ".skip-link", ":not(:focus", ".sr-only", "_honey", ".hp")):
                        continue
                    offenders.append((css.name, sel))
        self.assertEqual(offenders, [])

    def test_touch_targets_and_scroll_margin(self):
        css = "\n".join(f.read_text() for f in (ROOT / "shared" / "css").glob("*.css"))
        blocks = re.findall(r"@media\s*\(max-width:\s*920px\)\s*\{(.*?)\n\}", css, re.S)
        self.assertTrue(any("min-height: 44px" in b and "min-width: 44px" in b for b in blocks), "needs a <=920px touch block")
        self.assertIn("scroll-margin-top", css)
        self.assertIn(":focus-visible", css)

    def test_fonts_are_local(self):
        for css in self.css_files():
            for u in re.findall(r"@font-face[^}]*url\(['\"]?([^'\")]+)", css.read_text()):
                self.assertTrue(u.startswith("/shared/fonts/"), u)


class ToolingTests(unittest.TestCase):
    def test_js_syntax(self):
        js = list((ROOT / "shared").rglob("*.js")) + list((ROOT / "variations").rglob("*.js"))
        self.assertTrue(js)
        for f in js:
            r = subprocess.run(["node", "--check", str(f)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, f"{f}: {r.stderr}")

    def test_python_compiles(self):
        for f in list((ROOT / "tools").glob("*.py")) + list((ROOT / "tests").glob("*.py")):
            r = subprocess.run([sys.executable, "-m", "py_compile", str(f)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)

    def test_generator_is_deterministic_and_in_sync(self):
        r = subprocess.run([sys.executable, str(ROOT / "tools" / "generate.py"), "--check"], capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_git_diff_check(self):
        r = subprocess.run(["git", "diff", "--check"], capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(r.returncode, 0, r.stdout)
        # untracked text files too
        bad = []
        for f in [*ALL_PAGES, *(ROOT / "shared").rglob("*.css"), *(ROOT / "shared").rglob("*.js"), *(ROOT / "variations").rglob("*.*"), *(ROOT / "tools").glob("*.py")]:
            if f.exists():
                for i, line in enumerate(f.read_text().splitlines(), 1):
                    if line != line.rstrip():
                        bad.append(f"{f.relative_to(ROOT)}:{i}")
        self.assertEqual(bad[:10], [])


def walk(node):
    for c in node.children:
        yield c
        yield from walk(c)


def structure(node):
    return (node.tag, node.attrs.get("class"), [structure(c) for c in node.children if c.tag not in ("source",)])


if __name__ == "__main__":
    unittest.main()
