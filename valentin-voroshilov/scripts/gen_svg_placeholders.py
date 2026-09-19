#!/usr/bin/env python3
"""
Generates elegant, clearly-marked SVG placeholder images for the
Valentin Voroshilov website. These are abstract tonal placeholders
(NOT stock photography, NOT a likeness of any real person) meant to
hold layout/aspect-ratio until real photography/video is supplied.
"""
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "src", "assets", "images", "ph")
os.makedirs(OUT, exist_ok=True)

# Charcoal/ivory tonal palette used across all placeholders
DARK_STOPS = [("#1c1b17", 0), ("#0a0a09", 100)]
LIGHT_STOPS = [("#efeadf", 0), ("#ddd6c4", 100)]

def svg_template(width, height, label, sublabel, dark=True, seed=0):
    grad_id = f"g{seed}"
    stops = DARK_STOPS if dark else LIGHT_STOPS
    text_color = "#efeadf" if dark else "#0a0a09"
    muted = "#9c9686" if dark else "#726e63"
    line_color = "rgba(239,234,223,0.18)" if dark else "rgba(10,10,9,0.14)"
    cx, cy = width / 2, height / 2

    # subtle abstract arcs (evoke a scroll/instrument curve without being a literal music-note cliche)
    arcs = ""
    for i in range(3):
        r = min(width, height) * (0.28 + i * 0.16)
        arcs += (
            f'<circle cx="{cx + width*0.18}" cy="{cy - height*0.12}" r="{r:.1f}" '
            f'fill="none" stroke="{line_color}" stroke-width="1" />'
        )

    fs_label = max(12, min(width, height) * 0.032)
    fs_sub = fs_label * 0.62

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="{label} placeholder image">
  <defs>
    <linearGradient id="{grad_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="{stops[0][1]}%" stop-color="{stops[0][0]}"/>
      <stop offset="{stops[1][1]}%" stop-color="{stops[1][0]}"/>
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" fill="url(#{grad_id})"/>
  {arcs}
  <rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" fill="none" stroke="{line_color}" stroke-width="1"/>
  <g font-family="Georgia, 'DejaVu Serif', serif" text-anchor="middle">
    <text x="{cx}" y="{cy - fs_label*0.2}" font-size="{fs_label:.1f}" fill="{text_color}" letter-spacing="1">{label}</text>
    <text x="{cx}" y="{cy + fs_sub*1.9}" font-size="{fs_sub:.1f}" fill="{muted}" font-family="Helvetica, Arial, 'DejaVu Sans', sans-serif" letter-spacing="2.5">{sublabel}</text>
  </g>
</svg>'''
    return svg


def svg_hero_template(width, height, sublabel, seed=0):
    """Full-bleed hero/header placeholder with the marker tucked in a corner
    so it never collides with real heading text overlaid by the page."""
    grad_id = f"h{seed}"
    line_color = "rgba(239,234,223,0.14)"
    muted = "#8a8578"

    # subtle abstract arcs, pushed to the top-right so the bottom-left
    # (where page headlines sit) stays clean
    arcs = ""
    for i in range(3):
        r = min(width, height) * (0.32 + i * 0.22)
        arcs += (
            f'<circle cx="{width*0.82}" cy="{height*0.1}" r="{r:.1f}" '
            f'fill="none" stroke="{line_color}" stroke-width="1" />'
        )

    fs = max(11, min(width, height) * 0.02)
    pad = min(width, height) * 0.045

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="Photography placeholder image">
  <defs>
    <linearGradient id="{grad_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1c1b17"/>
      <stop offset="100%" stop-color="#0a0a09"/>
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" fill="url(#{grad_id})"/>
  {arcs}
  <rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" fill="none" stroke="{line_color}" stroke-width="1"/>
  <text x="{width - pad}" y="{height - pad}" font-size="{fs:.1f}" fill="{muted}" text-anchor="end" font-family="Helvetica, Arial, 'DejaVu Sans', sans-serif" letter-spacing="2.5">{sublabel}</text>
</svg>'''
    return svg

# Hero / page-header images: full-bleed banners with real heading text
# overlaid by the page, so these use a corner marker instead of centered text.
HERO_IMAGES = [
    ("hero-home", 1920, 1080, "PHOTOGRAPHY / VIDEO PLACEHOLDER — HERO"),
    ("about-header", 1920, 700, "PHOTOGRAPHY PLACEHOLDER — HEADER"),
    ("performances-header", 1920, 700, "PHOTOGRAPHY PLACEHOLDER — HEADER"),
    ("gallery-header", 1920, 700, "PHOTOGRAPHY PLACEHOLDER — HEADER"),
    ("previous-work-header", 1920, 700, "PHOTOGRAPHY PLACEHOLDER — HEADER"),
    ("testimonials-header", 1920, 700, "PHOTOGRAPHY PLACEHOLDER — HEADER"),
    ("contact-header", 1920, 700, "PHOTOGRAPHY PLACEHOLDER — HEADER"),
]

for name, w, h, sub in HERO_IMAGES:
    content = svg_hero_template(w, h, sub, seed=abs(hash(name)) % 999)
    with open(os.path.join(OUT, f"{name}.svg"), "w") as f:
        f.write(content)

# name, width, height, label, sublabel
IMAGES = [
    ("about-portrait", 1200, 1500, "PORTRAIT", "PHOTOGRAPHY PLACEHOLDER — REPLACE WITH FINAL PORTRAIT"),
    ("about-secondary", 1200, 1500, "IN PERFORMANCE", "PHOTOGRAPHY PLACEHOLDER"),
    ("category-weddings", 1000, 1300, "WEDDINGS", "PHOTOGRAPHY PLACEHOLDER"),
    ("category-corporate", 1000, 1300, "CORPORATE EVENTS", "PHOTOGRAPHY PLACEHOLDER"),
    ("category-private", 1000, 1300, "PRIVATE EVENTS", "PHOTOGRAPHY PLACEHOLDER"),
    ("category-collab", 1000, 1300, "LIVE COLLABORATIONS", "PHOTOGRAPHY PLACEHOLDER"),
    ("selected-1", 1400, 1000, "SELECTED PERFORMANCE", "PHOTOGRAPHY / VIDEO PLACEHOLDER"),
    ("selected-2", 1400, 1000, "SELECTED PERFORMANCE", "PHOTOGRAPHY / VIDEO PLACEHOLDER"),
    ("selected-3", 1400, 1000, "SELECTED PERFORMANCE", "PHOTOGRAPHY / VIDEO PLACEHOLDER"),
    ("event-lepas-l6", 1400, 900, "LEPAS L6 PRESENTATION", "PHOTOGRAPHY / VIDEO PLACEHOLDER"),
    ("event-future", 1400, 900, "YOUR NEXT EVENT", "ADD PHOTOGRAPHY WHEN AVAILABLE"),
    ("testimonial-avatar", 300, 300, "", "PHOTO"),
]

# Gallery grid — categories: weddings, corporate, concerts, events, behind-the-scenes
GALLERY_CATS = [
    ("weddings", 4), ("corporate", 3), ("concerts", 3), ("events", 3), ("bts", 3),
]

for i in range(1, 20):
    IMAGES.append((f"gallery-{i:02d}", 1200, 1500, "GALLERY", f"IMAGE {i:02d} PLACEHOLDER"))

for name, w, h, label, sub in IMAGES:
    dark = not name.startswith("testimonial-avatar")
    content = svg_template(w, h, label, sub, dark=dark, seed=abs(hash(name)) % 999)
    with open(os.path.join(OUT, f"{name}.svg"), "w") as f:
        f.write(content)

print(f"Generated {len(IMAGES) + len(HERO_IMAGES)} placeholder SVGs in {OUT}")
