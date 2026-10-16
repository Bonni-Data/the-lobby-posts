#!/usr/bin/env python3
"""THE LOBBY - copertina 1080x1920 con il solo logo (per i reel). Uso: python3 make_logo_cover.py uscita.jpg"""
import sys
from PIL import Image, ImageDraw
from make_pill import NAVY, CORAL, IVORY, NAVY_SOFT, BOLD, MED, font, tw, draw_arch

W, H = 1080, 1920
img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)
draw_arch(d, 190, 330, 700, 1300, NAVY_SOFT, 22)
aw, ah = 300, 400
x, y = (W - aw) // 2, 560
draw_arch(d, x, y, aw, ah, CORAL, 34)
cx, cy, r = W / 2, y + ah * 0.55, 32
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=IVORY)
f = font(BOLD, 128)
t = "THE LOBBY"
d.text(((W - tw(d, t, f)) / 2, 1030), t, font=f, fill=IVORY)
f2 = font(MED, 40)
t2 = "WHERE INFLUENCE BEGINS."
d.text(((W - tw(d, t2, f2)) / 2, 1190), t2, font=f2, fill=CORAL)
img.save(sys.argv[1], "JPEG", quality=92)
print("ok", sys.argv[1])
