"""Featured images and share cards for posts.

Drop the original image for a post at content/images/<slug>.jpg (or .jpeg, .png, .webp).
tools/build.py then, whenever the image, the title, or the card design changes:

  1. writes blog/<slug>/feature-1200 and feature-2400 as .jpg and .webp, converted to sRGB
     with all metadata (camera, location, editing history) removed; and
  2. renders the 1200x630 share card blog/<slug>/og.jpg: the photo, darkened on one side,
     with the title and "Greg Griffith · greggriffith.com" set over it.

Card rules (Greg, 2026-11-24): type over the image, no kicker above the title.
Front matter `card_text: right` puts the type on the right for images whose subject is on the left.

Needs Pillow; the card also needs Playwright and Chrome. If Playwright is missing, the build
keeps the existing card and prints a note.
"""
import hashlib
import html
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARD_VERSION = 2  # bump to re-render every card after a design change
SOURCE_TYPES = (".jpg", ".jpeg", ".png", ".webp")
CHROME = "/usr/bin/google-chrome"


def source_for(slug):
    for ext in SOURCE_TYPES:
        f = ROOT / "content" / "images" / f"{slug}{ext}"
        if f.exists():
            return f
    return None


def sha(path):
    return hashlib.sha1(path.read_bytes()).hexdigest()


def prepare_feature(src, out_dir):
    from PIL import Image, ImageCms
    with Image.open(src) as raw:
        icc = raw.info.get("icc_profile")
        im = raw.convert("RGB")
    if icc:
        try:
            im = ImageCms.profileToProfile(im, ImageCms.ImageCmsProfile(io.BytesIO(icc)),
                                           ImageCms.createProfile("sRGB"), outputMode="RGB")
        except Exception:
            pass
    out_dir.mkdir(parents=True, exist_ok=True)
    for w in (1200, 2400):
        r = im if im.width <= w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        r.save(out_dir / f"feature-{w}.jpg", "JPEG", quality=82, optimize=True, progressive=True)
        r.save(out_dir / f"feature-{w}.webp", "WEBP", quality=80, method=6)


def card_html(photo, title, side):
    f4 = (ROOT / "fonts" / "instrument-sans-latin-400-normal.woff2").as_uri()
    f5 = (ROOT / "fonts" / "instrument-sans-latin-500-normal.woff2").as_uri()
    direction = "90deg" if side == "left" else "270deg"
    pos = "left:72px" if side == "left" else "right:72px"
    return f"""<html><head><style>
@font-face{{font-family:I;font-weight:400;src:url('{f4}')}}@font-face{{font-family:I;font-weight:500;src:url('{f5}')}}
*{{margin:0;box-sizing:border-box}}
.c{{width:1200px;height:630px;position:relative;overflow:hidden;font-family:I;color:#f2f3f5;
   background:url('{photo.as_uri()}') center/cover no-repeat}}
.c::before{{content:"";position:absolute;inset:0;background:linear-gradient({direction},
   rgba(14,16,19,.92) 0%, rgba(14,16,19,.8) 36%, rgba(14,16,19,.3) 50%, rgba(14,16,19,0) 60%)}}
.t{{position:absolute;{pos};top:0;bottom:0;width:500px;display:flex;flex-direction:column;justify-content:center}}
.h{{font-size:60px;line-height:1.08;letter-spacing:-1.4px;margin:0 0 34px;font-weight:400}}
.u{{font-size:26px;color:#aeb4bc}} .u b{{font-weight:500;color:#f2f3f5}}
.bar{{width:48px;height:3px;background:#7fb0ff;margin-bottom:26px}}
</style></head><body><div class=c><div class=t>
<div class=h>{html.escape(title)}</div>
<div class=bar></div><div class=u><b>Greg Griffith</b> · greggriffith.com</div></div></div></body></html>"""


def render_card(slug, title, side="left"):
    from playwright.sync_api import sync_playwright
    out = ROOT / "blog" / slug
    page_file = out / ".card.html"
    page_file.write_text(card_html(out / "feature-2400.jpg", title, side), encoding="utf-8")
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--allow-file-access-from-files"])
            pg = b.new_page(viewport={"width": 1200, "height": 630})
            pg.goto(page_file.as_uri())
            pg.wait_for_timeout(500)
            # long titles: shrink the type until the title fits in about five lines
            pg.evaluate("""() => { const h = document.querySelector('.h'); let s = 60;
                while (h.offsetHeight > 330 && s > 36) { s -= 2; h.style.fontSize = s + 'px'; } }""")
            pg.screenshot(path=str(out / "og.jpg"), type="jpeg", quality=88)
            b.close()
    finally:
        page_file.unlink(missing_ok=True)


def update(post):
    """Bring a post's featured image and share card up to date. Returns a list of what changed."""
    slug = post["slug"]
    src = source_for(slug)
    if not src:
        return []
    out = ROOT / "blog" / slug
    stamp_file = out / ".images.json"
    old = json.loads(stamp_file.read_text()) if stamp_file.exists() else {}
    side = "right" if post.get("card_text", "left").strip().lower() == "right" else "left"
    new = {"source": sha(src), "title": post["title"], "side": side, "card": CARD_VERSION}
    changed = []
    if old.get("source") != new["source"] or not (out / "feature-2400.jpg").exists():
        prepare_feature(src, out)
        changed.append("featured image")
    if changed or any(old.get(k) != new[k] for k in ("title", "side", "card")) or not (out / "og.jpg").exists():
        try:
            render_card(slug, post["title"], side)
            changed.append("share card")
        except ImportError:
            print(f"  note: {slug}: Playwright isn't installed; share card not updated")
            new["card"] = old.get("card")
            new["title"] = old.get("title")
    stamp_file.write_text(json.dumps(new, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed
