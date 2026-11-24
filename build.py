#!/usr/bin/env python3
"""Assemble final static pages from shared partials + per-page body content.
Usage: python3 build.py
Reads partials/{header,footer,overlays}.html and pages_src/<slug>.html (body
content only) and PAGES config below, writes final <slug>.html into the
project root, ready to open or deploy.
"""
import os, re

ROOT = "/home/claude/asha-sweet-center"
PARTIALS = os.path.join(ROOT, "partials")
SRC = os.path.join(ROOT, "pages_src")

with open(os.path.join(PARTIALS, "header.html")) as f: HEADER = f.read()
with open(os.path.join(PARTIALS, "footer.html")) as f: FOOTER = f.read()
with open(os.path.join(PARTIALS, "overlays.html")) as f: OVERLAYS = f.read()

NAV_KEYS = ["SHOP", "SWEETS", "NAMKEEN", "DRYFRUITS", "CORPORATE", "FESTIVALS", "SEASONAL", "BLOG", "MORE"]
# Pages whose "active" nav key sits inside the "More" dropdown should also
# highlight the "More" toggle itself, so the top-level nav still shows state.
MORE_CHILDREN = {"BLOG", "SEASONAL"}

PAGES = [
    {
        "slug": "index",
        "title": "Asha Sweet Center | Premium Indian Sweets &amp; Gifting Since 1951 — Bengaluru",
        "description": "Shop authentic Indian sweets, namkeen, dry fruits and premium gift boxes from Asha Sweet Center, Bengaluru's trusted sweet maker since 1951. Free delivery across India.",
        "active": None,
        "body_class": "page-home",
    },
    {
        "slug": "collections",
        "title": "Shop All Collections | Asha Sweet Center",
        "description": "Browse all Asha Sweet Center collections — traditional sweets, namkeen, dry fruits, gift boxes, corporate gifting and seasonal specials.",
        "active": "SHOP",
        "body_class": "page-collections",
    },
    {
        "slug": "collection-detail",
        "title": "Traditional Indian Sweets | Asha Sweet Center",
        "description": "Shop traditional Indian sweets including Mysore Pak, Kaju Burfi, Motichur Laddu and more, freshly prepared by Asha Sweet Center since 1951.",
        "active": "SWEETS",
        "body_class": "page-collection-detail",
    },
    {
        "slug": "product",
        "title": "Luxurious Mysore Pak — Premium Tin Box | Asha Sweet Center",
        "description": "Buy Luxurious Mysore Pak in a premium gifting tin from Asha Sweet Center. Made fresh with pure ghee. Order online with PIN-code delivery check.",
        "active": "SWEETS",
        "body_class": "page-product",
    },
    {
        "slug": "corporate-gifting",
        "title": "Corporate Gifting | Premium Sweet Boxes for Business | Asha Sweet Center",
        "description": "Celebrate employees and clients with premium corporate gift boxes from Asha Sweet Center. Custom branding, bulk pricing and festival gifting available.",
        "active": "CORPORATE",
        "body_class": "page-corporate",
    },
    {
        "slug": "festivals",
        "title": "Festival Sweets &amp; Gift Boxes | Asha Sweet Center",
        "description": "Shop festive sweets and gift boxes for Diwali, Raksha Bandhan, Pongal, Ugadi and more from Asha Sweet Center, Bengaluru.",
        "active": "FESTIVALS",
        "body_class": "page-festivals",
    },
    {
        "slug": "seasonal",
        "title": "Seasonal Collections | Asha Sweet Center",
        "description": "Discover limited-time seasonal sweets, snacks and gift boxes from Asha Sweet Center.",
        "active": "SEASONAL",
        "body_class": "page-seasonal",
    },
    {
        "slug": "blog",
        "title": "The Sweet Journal — Blog | Asha Sweet Center",
        "description": "Stories, traditions, gifting ideas and guides from Asha Sweet Center — Bengaluru's sweet makers since 1951.",
        "active": "BLOG",
        "body_class": "page-blog",
    },
    {
        "slug": "blog-detail",
        "title": "The History of Mysore Pak: Karnataka's Beloved Sweet | Asha Sweet Center",
        "description": "Discover the fascinating history of Mysore Pak, from the royal kitchens of Mysore to Asha Sweet Center's stores across Bengaluru.",
        "active": "BLOG",
        "body_class": "page-blog-detail",
    },
]

HEAD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="https://www.ashasweetcenter.com/{slug_url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Asha Sweet Center">
<meta property="og:url" content="https://www.ashasweetcenter.com/{slug_url}">
<meta property="og:image" content="https://www.ashasweetcenter.com/assets/images/placeholders/hero-home-desktop.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22><circle cx=%2212%22 cy=%2212%22 r=%2210%22 fill=%22%23D31E43%22/></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Cormorant+Garamond:wght@600;700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
<link rel="stylesheet" href="assets/css/pages.css">
{extra_head}
</head>
<body class="{body_class}">
"""

FOOT_TEMPLATE = """
<script src="assets/js/main.js"></script>
{extra_script}
</body>
</html>
"""

def build_header(active):
    html = HEADER
    for key in NAV_KEYS:
        is_active = (key == active) or (key == "MORE" and active in MORE_CHILDREN)
        html = html.replace("__ACTIVE_%s__" % key, "active" if is_active else "")
    return html

def main():
    for page in PAGES:
        src_path = os.path.join(SRC, page["slug"] + ".html")
        if not os.path.exists(src_path):
            print("MISSING body source for", page["slug"], "- skipping")
            continue
        with open(src_path) as f:
            body = f.read()

        extra_head = page.get("extra_head", "")
        extra_script = page.get("extra_script", "")

        out = HEAD_TEMPLATE.format(
            title=page["title"], description=page["description"],
            slug_url=("" if page["slug"] == "index" else page["slug"] + ".html"),
            body_class=page["body_class"], extra_head=extra_head
        )
        out += '<div id="main-content">\n'
        out += build_header(page["active"])
        out += "\n" + body + "\n"
        out += FOOTER
        out += "</div>\n"
        out += OVERLAYS
        out += FOOT_TEMPLATE.format(extra_script=extra_script)

        out_path = os.path.join(ROOT, page["slug"] + ".html")
        with open(out_path, "w") as f:
            f.write(out)
        print("Built", out_path)

if __name__ == "__main__":
    main()
