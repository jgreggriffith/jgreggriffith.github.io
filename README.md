# greggriffith.com

Source for the personal website of Greg Griffith, served by GitHub Pages.

## How posts work

Every post has one permanent identifier: its **slug**, the short name in its address.
"Your Brain on MCP" lives at `/blog/your-brain-on-mcp/`, and that address never changes.

- **Write:** each post is one Markdown file, `content/posts/<slug>.md`, starting with:

  ```
  ---
  title: "The post title"
  slug: the-post-title        # must match the file name; never change it once published
  date: 2026-12-14            # publication date
  description: "One or two sentences for search results, link previews, and the post lists."
  updated: 2026-12-20         # optional: last substantive revision
  keywords: "Topic one, Topic two, Topic three"   # optional: 4–8 topics; feed search data and tags
  section: Essays             # optional: Essays (default), Narrative reads, or a series name
  ---
  ```

- **Pull quotes:** put a line like `{pull} The words to feature.` on its own, just before the
  paragraph it should sit beside. Sides alternate automatically; aim for about one per 500 words.
- **Build:** `python3 tools/build.py` (needs the `markdown` package). It writes
  `blog/<slug>/index.html` for every post, refreshes the lists on the home page and
  `/blog/`, and rewrites `sitemap.xml` and the RSS feed `feed.xml`. It warns when a title runs past
  about 60 characters or a description past about 155, the lengths search results display. It plays the role of WordPress's database.
- **Featured image and share card (optional):** put the original image at `content/images/<slug>.jpg`
  (or .png/.webp) and add `image_alt: "…"` to the front matter. The build makes the web-sized copies
  (`blog/<slug>/feature-1200/2400`, .jpg and .webp, metadata stripped) and the 1200 × 630 share card
  `blog/<slug>/og.jpg`: the photo with the title and byline over a darkened left side, no label above the
  title. It re-renders the card whenever the image or the title changes. `card_text: right` in the front
  matter moves the type to the right for images whose subject is on the left. See `tools/images.py`.
  Without an image, the site's share image is used.

Never rename a published slug. If one ever must change, keep the old folder with a page that
redirects to the new address, so existing links keep working.

## Other files

- `index.html`: Home page, including the structured data (JSON-LD) that identifies Greg to search engines.
  When it changes, update its "Last updated" stamp and `dateModified`.
- `assets/`: Shared stylesheet and the color switch. `fonts/`: Instrument Sans (OFL).
- `robots.txt`, `sitemap.xml`: Search engine files (the sitemap is generated).

Changes go through pull requests.
