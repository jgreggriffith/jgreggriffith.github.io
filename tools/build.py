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
import html
import json
import math
import re
import sys
from datetime import date
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://greggriffith.com"
AUTHOR_LINE = ("Greg Griffith is co-founder and Chief Product Officer of EdgeTheory, a narrative intelligence "
               "company that helps government and commercial organizations understand how narratives form, "
               "how they spread, and how they shape the decisions that matter most.")
HOME_COUNT = 4


PULL = re.compile(r"^\{pull\}[ \t]+(.+)$", re.M)


def render_body(body_md):
    """Markdown to HTML, with pull quotes.

    A line of the form  {pull} Text of the quote  becomes a pull quote that floats
    beside the paragraph that follows it. Sides alternate, starting on the right.
    Pull quotes are hidden from screen readers, since they repeat the essay's text.
    """
    quotes = []

    def stash(m):
        quotes.append(m.group(1).strip())
        return f"PULLQUOTE{len(quotes) - 1}"

    html_out = markdown.markdown(PULL.sub(stash, body_md), extensions=["smarty", "sane_lists"])
    for i, q in enumerate(quotes):
        inner = markdown.markdown(q, extensions=["smarty"])
        side = "r" if i % 2 == 0 else "l"
        html_out = html_out.replace(f"<p>PULLQUOTE{i}</p>",
                                    f'<aside class="pull {side}" aria-hidden="true">{inner}</aside>')
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
    meta["html"] = render_body(body_md)
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
    ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "@id": url + "#post",
        "headline": p["title"],
        "description": p["description"],
        "url": url,
        "mainEntityOfPage": url,
        "datePublished": p["date"],
        "dateModified": p["updated"],
        "wordCount": p["words"],
        "inLanguage": "en-US",
        "image": image,
        "author": {"@type": "Person", "@id": f"{SITE}/#person", "name": "Greg Griffith", "url": f"{SITE}/"},
        "publisher": {"@type": "Person", "@id": f"{SITE}/#person", "name": "Greg Griffith"},
        "isPartOf": {"@id": f"{SITE}/blog/#blog"},
    }
    t, d = esc(p["title"]), esc(p["description"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{t} – Greg Griffith</title>
  <meta name="description" content="{d}">
  <link rel="canonical" href="{url}">
  <link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Greg Griffith">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{d}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="article:published_time" content="{p['date']}">
  <meta property="article:modified_time" content="{p['updated']}">
  <meta property="article:author" content="{SITE}/">
  <meta name="author" content="Greg Griffith">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{t}">
  <meta name="twitter:description" content="{d}">
  <meta name="twitter:image" content="{image}">
  <script type="application/ld+json">
{json.dumps(ld, indent=2, ensure_ascii=False)}
  </script>
{HEAD_COMMON}
</head>
<body>
  <div class="wrap">
{MAST}
    <article class="post">
      <p class="meta"><time datetime="{p['date']}">{nice(p['d'])}</time> · {p['minutes']} min read</p>
      <h1 class="page-title">{t}</h1>
      <div class="post-body">
{p['html']}
      </div>
      <aside class="author">
        <p>{esc(AUTHOR_LINE)}</p>
      </aside>
    </article>
    <footer>
      <p><a href="/blog/">All writing</a> · <a href="/">Home</a> · <a href="https://www.linkedin.com/in/greg-griffith-06b9541b/" rel="me">LinkedIn</a></p>
      <p>© {p['d'].year} Greg Griffith</p>
    </footer>
  </div>
</body>
</html>
"""


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
    latest = max([p["updated"] for p in posts], default=date.today().isoformat())
    urls = [(f"{SITE}/", latest), (f"{SITE}/blog/", latest)] + [(f"{SITE}/blog/{p['slug']}/", p["updated"]) for p in posts]
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{d}</lastmod>\n  </url>\n" for u, d in urls)
        + "</urlset>\n", encoding="utf-8")
    print(f"Built {len(posts)} post(s): " + ", ".join(p["slug"] for p in posts))


if __name__ == "__main__":
    main()
