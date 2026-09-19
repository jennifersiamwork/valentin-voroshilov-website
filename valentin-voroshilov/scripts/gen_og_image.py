#!/usr/bin/env python3
"""Generate a default Open Graph share image (1200x630 JPG)."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "src", "assets", "images")
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1200, 630
img = Image.new("RGB", (W, H), "#0a0a09")
draw = ImageDraw.Draw(img)

# Subtle vertical gradient charcoal -> black
top = (28, 27, 23)
bottom = (10, 10, 9)
for y in range(H):
    t = y / H
    r = int(top[0] + (bottom[0] - top[0]) * t)
    g = int(top[1] + (bottom[1] - top[1]) * t)
    b = int(top[2] + (bottom[2] - top[2]) * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# thin frame
draw.rectangle([16, 16, W - 17, H - 17], outline=(239, 234, 223, 60), width=1)

serif_path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
sans_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

title_font = ImageFont.truetype(serif_path, 74)
role_font = ImageFont.truetype(serif_path, 34)
label_font = ImageFont.truetype(sans_path, 20)

ivory = (239, 234, 223)
mist = (199, 195, 184)
muted = (156, 150, 134)

def center_text(y, text, font, fill, spacing=0):
    if spacing:
        text = (" " * 0).join(list(text))
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text(((W - w) / 2, y), text, font=font, fill=fill)

center_text(255, "VALENTIN VOROSHILOV", title_font, ivory)
center_text(345, "Violinist", role_font, mist)
center_text(410, "KOH SAMUI · WORLDWIDE", label_font, muted)

img.save(os.path.join(OUT_DIR, "og-default.jpg"), quality=90)
print("Wrote og-default.jpg")
