#!/usr/bin/env python3
"""Build the writing section of greggriffith.com.

Source of truth: one Markdown file per post in content/posts/<slug>.md, with a
front-matter block (title, slug, date, description, optional updated).

This script writes:
  blog/<slug>/index.html   each post page
  blog/index.html          the full list of posts (between the posts markers)
  index.html               the latest posts on the home page (between the writing markers)
  sitemap.xml              every page, with lastmod dates

A post's permanent address is /blog/<slug>/. Never change a slug once published.

Usage: python3 tools/build.py   (requires the "markdown" package)
"""
import hashlib
import html
import json
import math
import re
import sys
from urllib.parse import quote, urlencode
from datetime import date
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://greggriffith.com"
AUTHOR_LINE = ("Greg Griffith is co-founder and Chief Product Officer of EdgeTheory, a narrative intelligence "
               "company that helps government and commercial organizations understand how narratives form, "
               "how they spread, and how they shape the decisions that matter most.")
HOME_COUNT = 4
LINKEDIN = "https://www.linkedin.com/in/greg-griffith-06b9541b/"
PERSON = {
    "@type": "Person",
    "@id": f"{SITE}/#person",
    "name": "Greg Griffith",
    "url": f"{SITE}/",
    "jobTitle": "Chief Product Officer",
    "description": AUTHOR_LINE,
    "worksFor": {"@type": "Organization", "@id": "https://edgetheory.com/", "name": "EdgeTheory", "url": "https://edgetheory.com/"},
    "knowsAbout": ["Narrative intelligence", "Cognitive warfare", "Information operations", "Product strategy",
                   "Product design and user experience"],
    "sameAs": [LINKEDIN],
}


PULL = re.compile(r"^\{pull\}[ \t]+(.+)$", re.M)


def linkedin_text_url(text):
    return "https://www.linkedin.com/feed/?" + urlencode({"shareActive": "true", "text": text}, quote_via=quote)


def render_body(body_md, url=""):
    """Markdown to HTML, with pull quotes.

    A line of the form  {pull} Text of the quote  becomes a pull quote that floats
    beside the paragraph that follows it. Sides alternate, starting on the right.
    The quote text is hidden from screen readers, since it repeats the essay's text; each
    quote carries a link to share it on LinkedIn.
    """
    quotes = []

    def stash(m):
        quotes.append(m.group(1).strip())
        return f"PULLQUOTE{len(quotes) - 1}"

    html_out = markdown.markdown(PULL.sub(stash, body_md), extensions=["smarty", "sane_lists"])
    for i, q in enumerate(quotes):
        inner = markdown.markdown(q, extensions=["smarty"])
        side = "r" if i % 2 == 0 else "l"
        plain = html.unescape(re.sub(r"<[^>]+>", "", inner)).strip()
        share = linkedin_text_url(f"\u201c{plain}\u201d\n\u2014 Greg Griffith\n\n{url}")
        inner = inner.replace("<p>", '<p aria-hidden="true">', 1)
        html_out = html_out.replace(f"<p>PULLQUOTE{i}</p>", f"""<aside class="pull {side}">{inner}
<div class="pull-foot"><span class="pull-rule"></span><a class="pull-share share-popup" href="{esc(share)}" target="_blank" rel="noopener" aria-label="Share this quote on LinkedIn">Share</a></div></aside>""")
    return html_out


def parse(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        sys.exit(f"{path}: missing front matter")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    for key in ("title", "slug", "date", "description"):
        if not meta.get(key):
            sys.exit(f"{path}: front matter needs '{key}'")
    if meta["slug"] != path.stem:
        sys.exit(f"{path}: slug must match the file name")
    for key in ("title", "description"):  # typographic apostrophes, to match the body
        meta[key] = re.sub(r"(\w)'(\w)", "\\1\u2019\\2", meta[key])
    body_md = m.group(2)
    words = len(re.findall(r"\b\w+\b", PULL.sub("", body_md)))
    meta["words"] = words
    meta["minutes"] = max(1, math.ceil(words / 230))
    meta["html"] = render_body(body_md, f"{SITE}/blog/{meta['slug']}/")
    meta["keywords"] = [k.strip() for k in meta.get("keywords", "").split(",") if k.strip()]
    meta["section"] = meta.get("section") or "Essays"
    if len(meta["description"]) > 160:
        print(f"  note: {path.name}: description is {len(meta['description'])} characters; "
              "search results show about 155", file=sys.stderr)
    if len(meta["title"]) > 60:
        print(f"  note: {path.name}: title is {len(meta['title'])} characters; search results show about 60",
              file=sys.stderr)
    meta["d"] = date.fromisoformat(meta["date"])
    meta["updated"] = meta.get("updated") or meta["date"]
    return meta


def nice(d):
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def esc(s):
    return html.escape(s, quote=True)


HEAD_COMMON = """  <script>try{if(localStorage.getItem("theme")==="light")document.documentElement.setAttribute("data-theme","light")}catch(e){}</script>
  <meta name="color-scheme" content="dark light">
  <link rel="preload" href="/fonts/instrument-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/site.css">
  <script src="/assets/theme.js" defer></script>"""

MAST = """    <header class="mast">
      <a class="word" href="/">Greg Griffith</a>
      <nav aria-label="Site">
        <a href="/#about">About</a>
        <a href="/blog/">Writing</a>
        <a href="/#press">Press kit</a>
        <button class="theme-toggle" type="button" aria-label="Invert colors" title="Invert" hidden><span class="dot" aria-hidden="true"></span></button>
      </nav>
    </header>"""


def post_page(p):
    url = f"{SITE}/blog/{p['slug']}/"
    image = f"{SITE}/blog/{p['slug']}/og.png" if (ROOT / "blog" / p["slug"] / "og.png").exists() else f"{SITE}/og-image.png"
    post = {
        "@type": "BlogPosting",
        "@id": url + "#post",
        "headline": p["title"],
        "description": p["description"],
        "url": url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "datePublished": p["date"],
        "dateModified": p["updated"],
        "wordCount": p["words"],
        "timeRequired": f"PT{p['minutes']}M",
        "inLanguage": "en-US",
        "articleSection": p["section"],
        "image": {"@type": "ImageObject", "url": image, "width": 1200, "height": 630},
        "author": PERSON,
        "publisher": {"@id": f"{SITE}/#person"},
        "isPartOf": {"@type": "Blog", "@id": f"{SITE}/blog/#blog", "name": "Writing – Greg Griffith", "url": f"{SITE}/blog/"},
    }
    if p["keywords"]:
        post["keywords"] = p["keywords"]
        post["about"] = [{"@type": "Thing", "name": k} for k in p["keywords"]]
    crumbs = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Greg Griffith", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Writing", "item": f"{SITE}/blog/"},
            {"@type": "ListItem", "position": 3, "name": p["title"], "item": url},
        ],
    }
    ld = {"@context": "https://schema.org", "@graph": [post, crumbs]}
    tags = "".join(f'\n  <meta property="article:tag" content="{esc(k)}">' for k in p["keywords"])
    kw = f'\n  <meta name="keywords" content="{esc(", ".join(p["keywords"]))}">' if p["keywords"] else ""
    alt = esc(f"{p['title']} – an essay by Greg Griffith")
    t, d = esc(p["title"]), esc(p["description"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{t} – Greg Griffith</title>
  <meta name="description" content="{d}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
  <meta name="author" content="Greg Griffith">{kw}
  <link rel="canonical" href="{url}">
  <link rel="alternate" type="application/rss+xml" title="Greg Griffith – Writing" href="{SITE}/feed.xml">
  <link rel="author" href="{SITE}/">
  <link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Greg Griffith">
  <meta property="og:locale" content="en_US">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{d}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{alt}">
  <meta property="article:published_time" content="{p['date']}">
  <meta property="article:modified_time" content="{p['updated']}">
  <meta property="article:author" content="{SITE}/">
  <meta property="article:section" content="{esc(p['section'])}">{tags}
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{t}">
  <meta name="twitter:description" content="{d}">
  <meta name="twitter:image" content="{image}">
  <meta name="twitter:image:alt" content="{alt}">
  <script type="application/ld+json">
{json.dumps(ld, indent=2, ensure_ascii=False)}
  </script>
{HEAD_COMMON}
</head>
<body>
  <div class="wrap">
{MAST}
    <article class="post">
      <p class="meta"><time datetime="{p['date']}">{nice(p['d'])}</time> · {p['minutes']} min read · <a href="#share">Share</a></p>
      <h1 class="page-title">{t}</h1>
      <div class="post-body">
{p['html']}
      </div>
{share_row(p, url)}
      <aside class="author">
        <p>{esc(AUTHOR_LINE)}</p>
      </aside>
    </article>
    <footer>
      <p><a href="/blog/">All writing</a> · <a href="/">Home</a> · <a href="https://www.linkedin.com/in/greg-griffith-06b9541b/" rel="me">LinkedIn</a> · <a href="/feed.xml" type="application/rss+xml">RSS</a></p>
      <p>© {p['d'].year} Greg Griffith</p>
    </footer>
  </div>
</body>
</html>
"""


def share_row(p, url):
    li = "https://www.linkedin.com/sharing/share-offsite/?" + urlencode({"url": url})
    x = "https://x.com/intent/post?" + urlencode({"text": p["title"], "url": url}, quote_via=quote)
    fb = "https://www.facebook.com/sharer/sharer.php?" + urlencode({"u": url})
    mail = "mailto:?" + urlencode({"subject": p["title"], "body": f"{p['description']}\n\n{url}"}, quote_via=quote)
    return f"""      <div class="share" id="share">
        <p class="label">Share</p>
        <ul>
          <li><a class="share-popup" href="{esc(li)}" target="_blank" rel="noopener">LinkedIn</a></li>
          <li><a class="share-popup" href="{esc(x)}" target="_blank" rel="noopener">X</a></li>
          <li><a class="share-popup" href="{esc(fb)}" target="_blank" rel="noopener">Facebook</a></li>
          <li><a href="{esc(mail)}" target="_blank" rel="noopener">Email</a></li>
          <li hidden><button type="button" class="copy-link" data-url="{url}">Copy link</button></li>
          <li hidden><button type="button" class="native-share" data-url="{url}" data-title="{esc(p['title'])}">Share…</button></li>
        </ul>
        <p class="share-status" role="status" aria-live="polite"></p>
      </div>"""


def list_items(posts, tag):
    out = [f'<ol class="posts">']
    for p in posts:
        out.append(f"""  <li>
    <p class="meta"><time datetime="{p['date']}">{nice(p['d'])}</time> · {p['minutes']} min read</p>
    <{tag}><a href="/blog/{p['slug']}/">{esc(p['title'])}</a></{tag}>
    <p class="blurb">{esc(p['description'])}</p>
  </li>""")
    out.append("</ol>")
    return "\n".join(out)


def replace_between(path, start, end, new):
    s = path.read_text(encoding="utf-8")
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if not pat.search(s):
        sys.exit(f"{path}: markers {start} / {end} not found")
    path.write_text(pat.sub(lambda _: f"{start}\n{new}\n{end}", s), encoding="utf-8")


def rfc822(d):
    return d.strftime("%a, %d %b %Y 12:00:00 -0600")


def write_feed(posts):
    items = []
    for p in posts:
        url = f"{SITE}/blog/{p['slug']}/"
        cats = "".join(f"\n      <category>{esc(k)}</category>" for k in p["keywords"])
        items.append(f"""    <item>
      <title>{esc(p['title'])}</title>
      <link>{url}</link>
      <guid isPermaLink="true">{url}</guid>
      <pubDate>{rfc822(p['d'])}</pubDate>
      <dc:creator>Greg Griffith</dc:creator>
      <description>{esc(p['description'])}</description>{cats}
      <content:encoded><![CDATA[{re.sub(r'<div class="pull-foot">.*?</div>', '', p['html'], flags=re.S)}]]></content:encoded>
    </item>""")
    built = rfc822(posts[0]["d"]) if posts else rfc822(date.today())
    (ROOT / "feed.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>Greg Griffith – Writing</title>
    <link>{SITE}/blog/</link>
    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>
    <description>Essays on narrative intelligence, cognitive warfare, and human nature.</description>
    <language>en-us</language>
    <lastBuildDate>{built}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
""", encoding="utf-8")


def blog_ld(posts):
    ld = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "@id": f"{SITE}/blog/#blog",
        "url": f"{SITE}/blog/",
        "name": "Writing – Greg Griffith",
        "description": "Essays on narrative intelligence, cognitive warfare, and human nature.",
        "inLanguage": "en-US",
        "isPartOf": {"@id": f"{SITE}/#website"},
        "author": PERSON,
        "publisher": {"@id": f"{SITE}/#person"},
        "blogPost": [{"@type": "BlogPosting", "@id": f"{SITE}/blog/{p['slug']}/#post", "headline": p["title"],
                      "url": f"{SITE}/blog/{p['slug']}/", "datePublished": p["date"], "dateModified": p["updated"]}
                     for p in posts],
    }
    return '  <script type="application/ld+json">\n' + json.dumps(ld, indent=2, ensure_ascii=False) + "\n  </script>"


def ensure_feed_link(path):
    s = path.read_text(encoding="utf-8")
    if "application/rss+xml" not in s:
        s = s.replace("</head>", f'  <link rel="alternate" type="application/rss+xml" title="Greg Griffith – Writing" href="{SITE}/feed.xml">\n</head>', 1)
        path.write_text(s, encoding="utf-8")


def stamp_assets():
    """Add a content fingerprint to the stylesheet and script links on every page, so
    browsers fetch the new file as soon as it changes instead of using a cached copy."""
    stamps = {}
    for name in ("site.css", "theme.js"):
        digest = hashlib.sha1((ROOT / "assets" / name).read_bytes()).hexdigest()[:8]
        stamps[name] = digest
    pages = [ROOT / "index.html", ROOT / "404.html", ROOT / "blog" / "index.html"] + list((ROOT / "blog").glob("*/index.html"))
    for page in pages:
        s = page.read_text(encoding="utf-8")
        for name, digest in stamps.items():
            s = re.sub(r"/assets/" + re.escape(name) + r'(\?v=[0-9a-f]+)?"', f'/assets/{name}?v={digest}"', s)
        page.write_text(s, encoding="utf-8")


def main():
    posts = sorted((parse(f) for f in (ROOT / "content" / "posts").glob("*.md")), key=lambda p: p["d"], reverse=True)
    for p in posts:
        out = ROOT / "blog" / p["slug"]
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(post_page(p), encoding="utf-8")
    empty = '<p class="empty">The first essays are on their way.</p>'
    replace_between(ROOT / "blog" / "index.html", "<!-- posts:start -->", "<!-- posts:end -->",
                    list_items(posts, "h2") if posts else empty)
    replace_between(ROOT / "index.html", "<!-- writing:start -->", "<!-- writing:end -->",
                    list_items(posts[:HOME_COUNT], "h3") if posts else empty)
    bi = ROOT / "blog" / "index.html"
    b = bi.read_text(encoding="utf-8")
    b = re.sub(r'  <script type="application/ld\+json">.*?</script>', lambda _: blog_ld(posts), b, count=1, flags=re.S)
    bi.write_text(b, encoding="utf-8")
    for f in (ROOT / "index.html", bi):
        ensure_feed_link(f)
    write_feed(posts)
    latest = max([p["updated"] for p in posts], default=date.today().isoformat())
    urls = [(f"{SITE}/", latest), (f"{SITE}/blog/", latest)] + [(f"{SITE}/blog/{p['slug']}/", p["updated"]) for p in posts]
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{d}</lastmod>\n  </url>\n" for u, d in urls)
        + "</urlset>\n", encoding="utf-8")
    stamp_assets()
    print(f"Built {len(posts)} post(s): " + ", ".join(p["slug"] for p in posts))


if __name__ == "__main__":
    main()
