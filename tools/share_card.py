"""Render a post's 1200x630 share card: the featured photo with the title and byline on the left.

Usage: python3 tools/share_card.py <slug> "<title>"
Reads blog/<slug>/feature-2400.jpg and writes blog/<slug>/og.jpg. Needs Playwright and Chrome.
No kicker above the title (Greg, 2026-11-24).
"""
import sys, html
from pathlib import Path
from playwright.sync_api import sync_playwright
repo = str(Path(__file__).resolve().parent.parent)
slug, title = sys.argv[1:3]
photo = f"{repo}/blog/{slug}/feature-2400.jpg"
f4 = f"file://{repo}/fonts/instrument-sans-latin-400-normal.woff2"
f5 = f"file://{repo}/fonts/instrument-sans-latin-500-normal.woff2"
doc = f"""<html><head><style>
@font-face{{font-family:I;font-weight:400;src:url('{f4}')}}@font-face{{font-family:I;font-weight:500;src:url('{f5}')}}
*{{margin:0;box-sizing:border-box}}
.c{{width:1200px;height:630px;position:relative;overflow:hidden;font-family:I;color:#f2f3f5;
   background:url('file://{photo}') center/cover no-repeat}}
.c::before{{content:"";position:absolute;inset:0;
   background:linear-gradient(90deg, rgba(14,16,19,.92) 0%, rgba(14,16,19,.8) 36%, rgba(14,16,19,.3) 50%, rgba(14,16,19,0) 60%)}}
.t{{position:absolute;left:72px;top:0;bottom:0;width:500px;display:flex;flex-direction:column;justify-content:center}}
.k{{font-size:24px;letter-spacing:.02em;color:#aeb4bc}}
.h{{font-size:60px;line-height:1.08;letter-spacing:-1.4px;margin:22px 0 34px;font-weight:400}}
.u{{font-size:26px;color:#aeb4bc}} .u b{{font-weight:500;color:#f2f3f5}}
.bar{{width:48px;height:3px;background:#7fb0ff;margin-bottom:26px}}
</style></head><body><div class=c><div class=t>
<div class=h>{html.escape(title)}</div>
<div class=bar></div><div class=u><b>Greg Griffith</b> · greggriffith.com</div></div></div></body></html>"""
open("/tmp/og-photo.html","w").write(doc)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox","--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width":1200,"height":630}); pg.goto("file:///tmp/og-photo.html"); pg.wait_for_timeout(700)
    pg.screenshot(path=f"{repo}/blog/{slug}/og.jpg", type="jpeg", quality=88); b.close()
