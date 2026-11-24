#!/usr/bin/env python3
"""Generate consistent, on-brand SVG placeholder imagery for the Asha Sweet
Center redesign. These stand in for real product/lifestyle photography
(which must be supplied by the client before launch) while keeping every
page visually finished and on-brand.
"""
import os, math, random

OUT = "/home/claude/asha-sweet-center/assets/images/placeholders"
os.makedirs(OUT, exist_ok=True)

MAROON = "#D31E43"
GOLD = "#C49A49"
IVORY = "#F7F0E4"
WHITE = "#FFFFFF"
CHARCOAL = "#292421"
GREEN = "#314B39"

def mandala_border(w, h, color, opacity=0.18):
    """Decorative repeating arc border, Indian-motif flavored."""
    arcs = []
    step = 28
    n = int((2*(w+h)) / step)
    for i in range(n):
        cx = (i * step) % w
        arcs.append(f'<circle cx="{cx}" cy="6" r="4" fill="none" stroke="{color}" stroke-width="1.5" opacity="{opacity}"/>')
        arcs.append(f'<circle cx="{cx}" cy="{h-6}" r="4" fill="none" stroke="{color}" stroke-width="1.5" opacity="{opacity}"/>')
    return "\n".join(arcs)

def icon_paths(kind, cx, cy, scale, color):
    """Very simple line-icon glyphs per category, centered at cx,cy."""
    s = scale
    icons = {
        "laddu": f'<circle cx="{cx}" cy="{cy}" r="{28*s}" fill="none" stroke="{color}" stroke-width="{2.5*s}"/><circle cx="{cx}" cy="{cy}" r="{3*s}" fill="{color}"/>' +
                 "".join(f'<circle cx="{cx+22*s*math.cos(a)}" cy="{cy+22*s*math.sin(a)}" r="{2.2*s}" fill="{color}"/>' for a in [i*math.pi/4 for i in range(8)]),
        "barfi": f'<rect x="{cx-26*s}" y="{cy-18*s}" width="{52*s}" height="{36*s}" rx="{3*s}" fill="none" stroke="{color}" stroke-width="{2.5*s}"/><line x1="{cx-26*s}" y1="{cy}" x2="{cx+26*s}" y2="{cy}" stroke="{color}" stroke-width="{1.5*s}"/><line x1="{cx-8.6*s}" y1="{cy-18*s}" x2="{cx-8.6*s}" y2="{cy+18*s}" stroke="{color}" stroke-width="{1.5*s}"/><line x1="{cx+8.6*s}" y1="{cy-18*s}" x2="{cx+8.6*s}" y2="{cy+18*s}" stroke="{color}" stroke-width="{1.5*s}"/>',
        "giftbox": f'<rect x="{cx-26*s}" y="{cy-14*s}" width="{52*s}" height="{40*s}" rx="{2*s}" fill="none" stroke="{color}" stroke-width="{2.5*s}"/><line x1="{cx-26*s}" y1="{cy-14*s}" x2="{cx+26*s}" y2="{cy-14*s}" stroke="{color}" stroke-width="{2.5*s}"/><line x1="{cx}" y1="{cy-26*s}" x2="{cx}" y2="{cy+26*s}" stroke="{color}" stroke-width="{2.5*s}"/><path d="M {cx-10*s} {cy-26*s} Q {cx-20*s} {cy-40*s} {cx} {cy-26*s} Q {cx+20*s} {cy-40*s} {cx+10*s} {cy-26*s}" fill="none" stroke="{color}" stroke-width="{2*s}"/>',
        "dryfruit": f'<ellipse cx="{cx-14*s}" cy="{cy}" rx="{14*s}" ry="{20*s}" fill="none" stroke="{color}" stroke-width="{2.5*s}"/><ellipse cx="{cx+14*s}" cy="{cy+6*s}" rx="{12*s}" ry="{17*s}" fill="none" stroke="{color}" stroke-width="{2.5*s}"/><line x1="{cx-14*s}" y1="{cy-20*s}" x2="{cx-10*s}" y2="{cy-28*s}" stroke="{color}" stroke-width="{2*s}"/>',
        "namkeen": f'<path d="M {cx-26*s} {cy+16*s} Q {cx-20*s} {cy-20*s} {cx} {cy-10*s} Q {cx+20*s} {cy-26*s} {cx+26*s} {cy+16*s} Z" fill="none" stroke="{color}" stroke-width="{2.5*s}"/>' + "".join(f'<circle cx="{cx+random.uniform(-16,16)*s:.1f}" cy="{cy+random.uniform(-6,10)*s:.1f}" r="{1.8*s}" fill="{color}"/>' for _ in range(10)),
        "cookie": f'<circle cx="{cx}" cy="{cy}" r="{26*s}" fill="none" stroke="{color}" stroke-width="{2.5*s}"/>' + "".join(f'<circle cx="{cx+13*s*math.cos(a)}" cy="{cy+13*s*math.sin(a)}" r="{2.4*s}" fill="{color}"/>' for a in [i*math.pi/3 for i in range(6)]),
        "mix": f'<rect x="{cx-24*s}" y="{cy-24*s}" width="{48*s}" height="{48*s}" rx="{6*s}" fill="none" stroke="{color}" stroke-width="{2.5*s}"/><path d="M {cx-24*s} {cy} L {cx+24*s} {cy} M {cx} {cy-24*s} L {cx} {cy+24*s}" stroke="{color}" stroke-width="{1.5*s}"/>',
        "diya": f'<path d="M {cx-28*s} {cy+6*s} Q {cx} {cy+28*s} {cx+28*s} {cy+6*s} Q {cx+14*s} {cy-4*s} {cx} {cy+2*s} Q {cx-14*s} {cy-4*s} {cx-28*s} {cy+6*s} Z" fill="none" stroke="{color}" stroke-width="{2.5*s}"/><path d="M {cx} {cy-6*s} Q {cx-6*s} {cy-22*s} {cx} {cy-32*s} Q {cx+6*s} {cy-22*s} {cx} {cy-6*s} Z" fill="{color}" opacity="0.85"/>',
        "rakhi": f'<circle cx="{cx}" cy="{cy}" r="{16*s}" fill="none" stroke="{color}" stroke-width="{2.5*s}"/>' + "".join(f'<line x1="{cx+16*s*math.cos(a)}" y1="{cy+16*s*math.sin(a)}" x2="{cx+28*s*math.cos(a)}" y2="{cy+28*s*math.sin(a)}" stroke="{color}" stroke-width="{2*s}"/>' for a in [i*math.pi/6 for i in range(12)]),
        "ganesh": f'<circle cx="{cx}" cy="{cy-6*s}" r="{14*s}" fill="none" stroke="{color}" stroke-width="{2.5*s}"/><path d="M {cx-14*s} {cy-2*s} Q {cx-22*s} {cy+10*s} {cx-10*s} {cy+14*s}" fill="none" stroke="{color}" stroke-width="{2.2*s}"/><path d="M {cx-10*s} {cy+10*s} Q {cx} {cy+30*s} {cx+10*s} {cy+10*s} Q {cx+20*s} {cy+22*s} {cx+14*s} {cy+30*s}" fill="none" stroke="{color}" stroke-width="{2.2*s}"/>',
        "kolam": f'<circle cx="{cx}" cy="{cy}" r="{24*s}" fill="none" stroke="{color}" stroke-width="{2*s}"/>' + "".join(f'<circle cx="{cx+24*s*math.cos(a)}" cy="{cy+24*s*math.sin(a)}" r="{3*s}" fill="{color}"/>' for a in [i*math.pi/4 for i in range(8)]),
        "umbrella": f'<path d="M {cx-26*s} {cy} Q {cx} {cy-30*s} {cx+26*s} {cy} Z" fill="none" stroke="{color}" stroke-width="{2.5*s}"/><line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy+28*s}" stroke="{color}" stroke-width="{2.2*s}"/>',
        "leaf-swirl": f'<path d="M {cx-24*s} {cy+16*s} Q {cx-10*s} {cy-26*s} {cx+24*s} {cy-16*s} Q {cx+10*s} {cy+26*s} {cx-24*s} {cy+16*s} Z" fill="none" stroke="{color}" stroke-width="{2.5*s}"/><line x1="{cx-20*s}" y1="{cy+10*s}" x2="{cx+20*s}" y2="{cy-10*s}" stroke="{color}" stroke-width="{1.5*s}"/>',
        "book": f'<path d="M {cx-24*s} {cy-18*s} L {cx} {cy-12*s} L {cx+24*s} {cy-18*s} L {cx+24*s} {cy+18*s} L {cx} {cy+12*s} L {cx-24*s} {cy+18*s} Z" fill="none" stroke="{color}" stroke-width="{2.3*s}"/><line x1="{cx}" y1="{cy-12*s}" x2="{cx}" y2="{cy+12*s}" stroke="{color}" stroke-width="{2*s}"/>',
        "briefcase": f'<rect x="{cx-26*s}" y="{cy-12*s}" width="{52*s}" height="{34*s}" rx="{3*s}" fill="none" stroke="{color}" stroke-width="{2.5*s}"/><path d="M {cx-12*s} {cy-12*s} L {cx-12*s} {cy-20*s} Q {cx-12*s} {cy-24*s} {cx-8*s} {cy-24*s} L {cx+8*s} {cy-24*s} Q {cx+12*s} {cy-24*s} {cx+12*s} {cy-20*s} L {cx+12*s} {cy-12*s}" fill="none" stroke="{color}" stroke-width="{2.3*s}"/>',
        # distinct sweet/snack glyphs added for a richer, less-repetitive image set
        "soan-papdi": f'<rect x="{cx-26*s}" y="{cy-20*s}" width="{52*s}" height="{40*s}" rx="{2*s}" fill="none" stroke="{color}" stroke-width="{2.5*s}"/>' +
                      "".join(f'<path d="M {cx-24*s} {cy-20*s+i*8*s} Q {cx} {cy-14*s+i*8*s} {cx+24*s} {cy-20*s+i*8*s}" fill="none" stroke="{color}" stroke-width="1.3" opacity="0.8"/>' for i in range(6)),
        "baklava": f'<path d="M {cx} {cy-26*s} L {cx+26*s} {cy} L {cx} {cy+26*s} L {cx-26*s} {cy} Z" fill="none" stroke="{color}" stroke-width="{2.5*s}"/>' +
                   f'<line x1="{cx-13*s}" y1="{cy-13*s}" x2="{cx+13*s}" y2="{cy+13*s}" stroke="{color}" stroke-width="1.3" opacity="0.8"/>' +
                   f'<line x1="{cx+13*s}" y1="{cy-13*s}" x2="{cx-13*s}" y2="{cy+13*s}" stroke="{color}" stroke-width="1.3" opacity="0.8"/>' +
                   f'<circle cx="{cx}" cy="{cy}" r="{3*s}" fill="{color}"/>',
        "murukku": f'<path d="M {cx-20*s} {cy} a {10*s} {10*s} 0 1 1 {20*s} 0 a {10*s} {10*s} 0 1 1 {-20*s} 0" fill="none" stroke="{color}" stroke-width="{2.3*s}"/>' +
                   f'<path d="M {cx-8*s} {cy-20*s} a {10*s} {10*s} 0 1 1 {20*s} 0 a {10*s} {10*s} 0 1 1 {-20*s} 0" fill="none" stroke="{color}" stroke-width="{2.3*s}"/>' +
                   f'<path d="M {cx-4*s} {cy+18*s} a {9*s} {9*s} 0 1 1 {18*s} 0 a {9*s} {9*s} 0 1 1 {-18*s} 0" fill="none" stroke="{color}" stroke-width="{2.3*s}"/>',
        "milk-sweet": f'<path d="M {cx-22*s} {cy+14*s} Q {cx-22*s} {cy-18*s} {cx} {cy-20*s} Q {cx+22*s} {cy-18*s} {cx+22*s} {cy+14*s} Q {cx+22*s} {cy+24*s} {cx} {cy+24*s} Q {cx-22*s} {cy+24*s} {cx-22*s} {cy+14*s} Z" fill="none" stroke="{color}" stroke-width="{2.5*s}"/>' +
                      f'<path d="M {cx-10*s} {cy-20*s} Q {cx} {cy-30*s} {cx+10*s} {cy-20*s}" fill="none" stroke="{color}" stroke-width="{2*s}"/>' +
                      f'<circle cx="{cx}" cy="{cy+2*s}" r="{3*s}" fill="{color}"/>',
        "almond": f'<path d="M {cx} {cy-26*s} Q {cx+16*s} {cy-10*s} {cx+13*s} {cy+12*s} Q {cx+8*s} {cy+28*s} {cx} {cy+28*s} Q {cx-8*s} {cy+28*s} {cx-13*s} {cy+12*s} Q {cx-16*s} {cy-10*s} {cx} {cy-26*s} Z" fill="none" stroke="{color}" stroke-width="{2.5*s}"/>' +
                  f'<line x1="{cx}" y1="{cy-14*s}" x2="{cx}" y2="{cy+18*s}" stroke="{color}" stroke-width="1.3" opacity="0.7"/>',
        "cashew": f'<path d="M {cx-14*s} {cy+16*s} Q {cx-26*s} {cy+4*s} {cx-18*s} {cy-12*s} Q {cx-10*s} {cy-28*s} {cx+6*s} {cy-20*s} Q {cx+22*s} {cy-12*s} {cx+14*s} {cy+4*s} Q {cx+8*s} {cy+16*s} {cx-14*s} {cy+16*s} Z" fill="none" stroke="{color}" stroke-width="{2.5*s}"/>',
        "nut-mix": f'<ellipse cx="{cx-16*s}" cy="{cy+4*s}" rx="{11*s}" ry="{15*s}" fill="none" stroke="{color}" stroke-width="{2.3*s}"/>' +
                   f'<path d="M {cx+2*s} {cy+14*s} Q {cx-6*s} {cy+4*s} {cx} {cy-8*s} Q {cx+6*s} {cy-18*s} {cx+16*s} {cy-12*s} Q {cx+24*s} {cy-6*s} {cx+18*s} {cy+4*s} Q {cx+14*s} {cy+14*s} {cx+2*s} {cy+14*s} Z" fill="none" stroke="{color}" stroke-width="{2.3*s}"/>',
    }
    return icons.get(kind, icons["mix"])

def make_svg(path, w, h, label, sub, bg, accent, icon, pattern=True, text_color=None, show_text=True, icon_x_frac=0.5, corner_icon=None):
    text_color = text_color or CHARCOAL
    pat = mandala_border(w, h, accent, 0.22) if pattern else ""
    icon_cy = h*0.5 if not show_text else h*0.40
    icon_scale = (min(w, h)/220) * (1.5 if not show_text else 1.0)
    badge_svg = ""
    if icon and show_text:
        # soft premium "badge" plate behind product/blog icons so they read as
        # a designed tile rather than a bare line-icon floating on gradient
        br = min(w, h) * 0.20
        badge_svg = (f'<circle cx="{w*icon_x_frac}" cy="{icon_cy}" r="{br}" fill="{WHITE}" opacity="0.6"/>'
                     f'<circle cx="{w*icon_x_frac}" cy="{icon_cy}" r="{br}" fill="none" stroke="{accent}" stroke-width="1.2" opacity="0.4"/>'
                     f'<circle cx="{w*icon_x_frac}" cy="{icon_cy}" r="{br+6}" fill="none" stroke="{accent}" stroke-width="1" opacity="0.18"/>')
    icon_svg = icon_paths(icon, w*icon_x_frac, icon_cy, icon_scale, accent) if icon else ""
    corner_svg = ""
    if corner_icon:
        ccx, ccy = w*0.90, h*0.78
        cscale = (min(w, h)/220) * 0.85
        corner_svg = f'<g opacity="0.5">{icon_paths(corner_icon, ccx, ccy, cscale, accent)}</g>'
        corner_svg += f'<circle cx="{ccx}" cy="{ccy}" r="{cscale*44}" fill="none" stroke="{accent}" stroke-width="1" opacity="0.25"/>'
    label_esc = label.replace("&", "&amp;")
    sub_esc = (sub or "").replace("&", "&amp;")
    text_block = ""
    if show_text:
        text_block = f'<text x="50%" y="{h*0.40+ min(w,h)*0.22}" text-anchor="middle" font-family="Georgia, \'Playfair Display\', serif" font-size="{max(13, min(w,h)*0.052)}" fill="{text_color}" font-weight="600">{label_esc}</text>'
        if sub:
            text_block += f'<text x="50%" y="{h*0.40+ min(w,h)*0.22+22}" text-anchor="middle" font-family="Arial, sans-serif" font-size="{max(10, min(w,h)*0.032)}" fill="{accent}" letter-spacing="1">{sub_esc}</text>'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label_esc}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{bg}"/>
      <stop offset="1" stop-color="{WHITE}"/>
    </linearGradient>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#g)"/>
  <rect x="10" y="10" width="{w-20}" height="{h-20}" fill="none" stroke="{accent}" stroke-width="1" opacity="0.35"/>
  {pat}
  {corner_svg}
  {badge_svg}
  {icon_svg}
  {text_block}
</svg>'''
    with open(os.path.join(OUT, path), "w") as f:
        f.write(svg)

# ---- Hero banners (decorative pattern only — page HTML overlays real heading
# text, and a center icon would risk colliding with it at some viewport, so
# these carry no icon, just the brand gradient + mandala border) ----
make_svg("hero-home-desktop.svg", 1440, 640, "Asha Sweet Center hero", "", IVORY, GOLD, None, show_text=False, corner_icon="giftbox")
make_svg("hero-home-mobile.svg", 390, 460, "Asha Sweet Center hero", "", IVORY, GOLD, None, show_text=False, corner_icon="giftbox")
make_svg("hero-corporate-desktop.svg", 1440, 520, "Corporate gifting hero", "", MAROON, GOLD, None, text_color=WHITE, show_text=False, corner_icon="briefcase")
make_svg("hero-corporate-mobile.svg", 390, 420, "Corporate gifting hero", "", MAROON, GOLD, None, text_color=WHITE, show_text=False, corner_icon="briefcase")
make_svg("hero-festivals-desktop.svg", 1440, 560, "Festival collections hero", "", IVORY, MAROON, None, show_text=False, corner_icon="diya")
make_svg("hero-festivals-mobile.svg", 390, 440, "Festival collections hero", "", IVORY, MAROON, None, show_text=False, corner_icon="diya")
make_svg("hero-seasonal-desktop.svg", 1440, 520, "Seasonal collections hero", "", GREEN, GOLD, None, text_color=WHITE, show_text=False, corner_icon="leaf-swirl")
make_svg("hero-seasonal-mobile.svg", 390, 420, "Seasonal collections hero", "", GREEN, GOLD, None, text_color=WHITE, show_text=False, corner_icon="leaf-swirl")
make_svg("hero-blog-desktop.svg", 1440, 420, "The Sweet Journal hero", "", IVORY, MAROON, None, show_text=False, corner_icon="book")
make_svg("hero-blog-mobile.svg", 390, 340, "The Sweet Journal hero", "", IVORY, MAROON, None, show_text=False, corner_icon="book")
make_svg("hero-collections-desktop.svg", 1440, 360, "Our collections hero", "", IVORY, GOLD, None, show_text=False, corner_icon="kolam")
make_svg("hero-bangalore-desktop.svg", 1440, 420, "Bangalore quick delivery hero", "", GREEN, GOLD, None, text_color=WHITE, show_text=False, corner_icon="diya")

# ---- Category tiles (square, home + nav) ----
cats = [
    ("category-sweets.svg", "Traditional Sweets", "laddu", MAROON),
    ("category-namkeen.svg", "Namkeen", "namkeen", GOLD),
    ("category-dryfruits.svg", "Dry Fruits", "dryfruit", GREEN),
    ("category-cookies.svg", "Cookies", "cookie", MAROON),
    ("category-giftboxes.svg", "Gift Boxes", "giftbox", GOLD),
    ("category-instantmix.svg", "Instant Ready Mix", "mix", GREEN),
]
for fn, label, icon, accent in cats:
    make_svg(fn, 560, 560, label, None, IVORY, accent, icon, show_text=False)

# ---- Product card placeholders (square) ----
products = [
    ("product-mysore-pak.svg", "Mysore Pak", "barfi"),
    ("product-kaju-burfi.svg", "Kaju Burfi", "cashew"),
    ("product-motichur-laddu.svg", "Motichur Laddu", "laddu"),
    ("product-soan-papdi.svg", "Soan Papdi", "soan-papdi"),
    ("product-baklava.svg", "Premium Baklava", "baklava"),
    ("product-navarathan-mixture.svg", "Navarathan Mixture", "namkeen"),
    ("product-chow-chow.svg", "Chow Chow", "namkeen"),
    ("product-cashew-burfi.svg", "Cashew Burfi", "nut-mix"),
    ("product-roasted-almonds.svg", "Roasted Almonds", "almond"),
    ("product-roasted-cashews.svg", "Roasted Cashews", "cashew"),
    ("product-dryfruit-giftbox.svg", "Dry Fruit Gift Box", "giftbox"),
    ("product-kaju-badam-mix.svg", "Kaju Badam Mix Sweets", "nut-mix"),
    ("product-milk-sweet.svg", "Milk Sweets", "milk-sweet"),
    ("product-murukku.svg", "Murukku", "murukku"),
]
for fn, label, icon in products:
    make_svg(fn, 640, 640, label, "ASHA SWEET CENTER", IVORY, MAROON, icon)

# ---- Product gallery (PDP) ----
for i in range(1, 5):
    make_svg(f"product-gallery-{i}.svg", 720, 720, "Luxurious Mysore Pak", f"VIEW {i}", IVORY, GOLD, "barfi")

# ---- Gifting / lifestyle collections (text overlaid by page HTML) ----
make_svg("gifting-collection-1.svg", 720, 540, "Premium gift boxes", "", IVORY, GOLD, "giftbox", show_text=False)
make_svg("gifting-collection-2.svg", 720, 540, "Dry fruit hampers", "", IVORY, GREEN, "dryfruit", show_text=False)
make_svg("heritage-image.svg", 720, 820, "Est. 1951", "MALLESHWARAM, BENGALURU", MAROON, GOLD, "giftbox", text_color=WHITE)

# ---- Occasion cards ----
occasions = [
    ("occasion-diwali.svg", "Diwali", "diya", MAROON),
    ("occasion-rakhi.svg", "Raksha Bandhan", "rakhi", GOLD),
    ("occasion-weddings.svg", "Weddings", "giftbox", MAROON),
    ("occasion-housewarming.svg", "Housewarming", "diya", GREEN),
    ("occasion-family.svg", "Family Celebrations", "kolam", GOLD),
    ("occasion-corporate.svg", "Corporate Events", "briefcase", CHARCOAL),
]
for fn, label, icon, accent in occasions:
    make_svg(fn, 480, 360, label, None, IVORY, accent, icon, show_text=False)

# ---- Festival banners ----
fests = [
    ("festival-diwali.svg", "Diwali", "diya", MAROON),
    ("festival-rakhi.svg", "Raksha Bandhan", "rakhi", GOLD),
    ("festival-pongal.svg", "Pongal", "kolam", GREEN),
    ("festival-ugadi.svg", "Ugadi", "leaf-swirl", GOLD),
    ("festival-dussehra.svg", "Dussehra", "diya", MAROON),
    ("festival-ganesh.svg", "Ganesh Chaturthi", "ganesh", GREEN),
    ("festival-holi.svg", "Holi", "kolam", GOLD),
]
for fn, label, icon, accent in fests:
    make_svg(fn, 560, 420, label, "SHOP THE COLLECTION", IVORY, accent, icon, show_text=False)

# ---- Seasonal ----
make_svg("seasonal-collection-1.svg", 640, 480, "Summer Coolers", "SEASONAL FAVOURITES", IVORY, GREEN, "leaf-swirl", show_text=False)
make_svg("seasonal-collection-2.svg", 640, 480, "Winter Dry Fruit Mix", "LIMITED TIME", IVORY, GOLD, "dryfruit", show_text=False)
make_svg("seasonal-collection-3.svg", 640, 480, "Monsoon Snack Box", "LIMITED TIME", IVORY, MAROON, "namkeen", show_text=False)

# ---- Blog ----
make_svg("blog-featured.svg", 960, 540, "The History of Mysore Pak", "FOOD & CULTURE", IVORY, GOLD, "book")
blogs = [
    ("blog-1.svg", "10 Traditional Sweets for Diwali", "diya"),
    ("blog-2.svg", "A Guide to Corporate Festive Gifting", "briefcase"),
    ("blog-3.svg", "How Mysore Pak is Made", "barfi"),
    ("blog-4.svg", "Choosing the Perfect Gift Box", "giftbox"),
    ("blog-5.svg", "Dry Fruits 101: A Buyer's Guide", "dryfruit"),
    ("blog-6.svg", "Festive Traditions of Karnataka", "kolam"),
]
for fn, label, icon in blogs:
    make_svg(fn, 560, 360, label, "ASHA SWEET CENTER", IVORY, MAROON, icon)

# ---- corporate gifting detail ----
make_svg("corporate-giftbox-1.svg", 640, 480, "Executive Assortment Box", "CUSTOM BRANDING AVAILABLE", IVORY, GOLD, "giftbox", show_text=False)
make_svg("corporate-giftbox-2.svg", 640, 480, "Client Celebration Hamper", "BULK PRICING AVAILABLE", IVORY, MAROON, "giftbox", show_text=False)
make_svg("corporate-giftbox-3.svg", 640, 480, "Diwali Corporate Box", "CUSTOM LOGO PACKAGING", IVORY, GREEN, "diya", show_text=False)

# ---- logo (recreation of the real Asha Sweet Center wordmark: bold serif
# "ASHA" over tracked-caps "SWEET CENTER", as used on ashasweetcenter.com) ----
def make_logo(path, w, h, color, transparent=True):
    bg = "" if transparent else f'<rect width="{w}" height="{h}" fill="{WHITE}"/>'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Asha Sweet Center">
  {bg}
  <text x="50%" y="46" text-anchor="middle" font-family="'Playfair Display', Georgia, serif" font-size="46" font-weight="900" letter-spacing="-1" fill="{color}">ASHA</text>
  <text x="50%" y="68" text-anchor="middle" font-family="'Manrope', Arial, sans-serif" font-size="13" font-weight="800" letter-spacing="5" fill="{color}">SWEET CENTER</text>
</svg>'''
    with open(os.path.join(OUT, path), "w") as f:
        f.write(svg)

make_logo("logo.svg", 220, 76, MAROON)
make_logo("logo-white.svg", 220, 76, WHITE)

print("Generated", len(os.listdir(OUT)), "placeholder assets")
