#!/usr/bin/env python3
"""THE LOBBY - grafiche "Scopri THE LOBBY" (1080x1350, IG/FB).

Uso: python3 make_story.py data.json output.png

Due impaginazioni:
- "brand": presenta THE LOBBY o una sua parte (percorso, opportunità, corsi, Premium).
  {"layout": "brand", "kicker": "NASCE THE LOBBY", "title": "Capisci le regole. Cambia le cose.",
   "points": ["...", "...", "...", "..."], "cta": "Gratis · thelobbyitalia.it · link in bio"}
- "founder": racconta il fondatore, con la sua foto scontornata (assets/andrea-cut.png).
  {"layout": "founder", "kicker": "CHI C'È DIETRO", "title": "Frase o citazione, max ~90 caratteri",
   "points": ["...", "..."], "cta": "La sua storia nella web app · link in bio"}
Testi: kicker max ~28 caratteri, title max ~70 (brand) o ~90 (founder), 2-4 punti max ~70 caratteri.
"""
import json
import os
import sys
from PIL import Image, ImageDraw

from make_pill import (W, H, NAVY, CORAL, IVORY, NAVY_SOFT, BOLD, MED, font, tw, wrap, fit_block, draw_arch, draw_logo,
                       BAND, promise_band)

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTO = os.path.join(HERE, "assets", "andrea-cut.png")


def pill(d, x, y, text):
    f = font(BOLD, 28)
    w = tw(d, text, f) + 44
    d.rounded_rectangle((x, y, x + w, y + 52), radius=26, fill=CORAL)
    d.text((x + 22, y + 6), text, font=f, fill=NAVY)


def footer(d):
    fy = H - 90 - BAND
    d.line([70, fy, W - 70, fy], fill=CORAL, width=3)
    d.text((70, fy + 18), "Andrea Bonazzi", font=font(BOLD, 36), fill=IVORY)
    s = "Salva · Condividi"
    sf = font(MED, 24)
    d.text((W - 70 - tw(d, s, sf), fy + 28), s, font=sf, fill=CORAL)


def brand(data, img):
    d = ImageDraw.Draw(img)
    draw_arch(d, 600, 60, 560, 1180, NAVY_SOFT, 26)
    draw_logo(img, 70, 62, 1.0)
    d = ImageDraw.Draw(img)
    pill(d, 70, 200, data.get("kicker", "THE LOBBY").upper())

    tf, tl, ts = fit_block(d, data["title"], BOLD, W - 140, 3, 92, 60)
    y = 290
    for ln in tl:
        d.text((70, y), ln, font=tf, fill=IVORY)
        y += int(ts * 1.16)
    if data.get("subtitle"):
        sf, sl, ss = fit_block(d, data["subtitle"], MED, W - 160, 2, 32, 24)
        y += 14
        for ln in sl:
            d.text((70, y), ln, font=sf, fill=IVORY)
            y += int(ss * 1.35)

    card_top = max(y + 40, 600)
    card_bot = H - 250 - BAND
    d.rounded_rectangle((60, card_top, W - 60, card_bot), radius=34, fill=IVORY)
    pts = data["points"][:4]
    px, pmax = 132, W - 60 - 44 - 132
    pf, _, ps = fit_block(d, max(pts, key=len), MED, pmax, 2, 34, 24)
    blocks = [wrap(d, p, pf, pmax) for p in pts]
    plh = int(ps * 1.3)
    gap = 30
    total = sum(len(b) * plh for b in blocks) + gap * (len(blocks) - 1)
    yy = card_top + (card_bot - card_top - total) / 2
    for i, b in enumerate(blocks, 1):
        cy = yy + plh / 2
        d.ellipse([74, cy - 22, 118, cy + 22], fill=NAVY)
        nf = font(BOLD, 26)
        n = str(i)
        d.text((96 - tw(d, n, nf) / 2, cy - 18), n, font=nf, fill=CORAL)
        for ln in b:
            d.text((px, yy), ln, font=pf, fill=NAVY)
            yy += plh
        yy += gap

    cta = data.get("cta", "Gratis · thelobbyitalia.it · link in bio")
    cf = fit_block(d, cta, BOLD, W - 140, 1, 36, 24)[0]
    d.text((70, card_bot + 40), cta, font=cf, fill=CORAL)
    footer(d)


def founder(data, img):
    d = ImageDraw.Draw(img)
    # foto nell'arco, in basso a destra
    aw, ah = 440, 680
    ax = W - 60 - aw
    atop = H - 110 - BAND - ah
    d.rounded_rectangle((ax, atop, ax + aw, atop + ah), radius=aw // 2, fill=NAVY_SOFT)
    if os.path.exists(PHOTO):
        ph = Image.open(PHOTO).convert("RGBA")
        scale = (aw - 20) / ph.width
        ph = ph.resize((int(ph.width * scale), int(ph.height * scale)), Image.LANCZOS)
        # maschera ad arco, così la foto resta dentro la sagoma
        mask = Image.new("L", (aw, ah), 0)
        md = ImageDraw.Draw(mask)
        md.rounded_rectangle((0, 0, aw, ah + aw), radius=aw // 2, fill=255)
        layer = Image.new("RGBA", (aw, ah), (0, 0, 0, 0))
        layer.paste(ph, ((aw - ph.width) // 2, ah - ph.height), ph)
        alpha = Image.composite(layer.getchannel("A"), Image.new("L", (aw, ah), 0), mask)
        layer.putalpha(alpha)
        img.paste(layer, (ax, atop), layer)
    d = ImageDraw.Draw(img)
    draw_arch(d, ax - 14, atop - 14, aw + 28, ah + 14, CORAL, 8)
    draw_logo(img, 70, 62, 1.0)
    d = ImageDraw.Draw(img)
    pill(d, 70, 200, data.get("kicker", "CHI C'È DIETRO").upper())

    tf, tl, ts = fit_block(d, data["title"], BOLD, ax - 110, 5, 56, 36)
    y = 290
    for ln in tl:
        d.text((70, y), ln, font=tf, fill=IVORY)
        y += int(ts * 1.2)

    y += 30
    pf = font(MED, 28)
    for p in data.get("points", [])[:3]:
        lines = wrap(d, p, pf, ax - 140)
        d.rectangle((70, y + 12, 82, y + 24), fill=CORAL)
        for ln in lines:
            d.text((100, y), ln, font=pf, fill=IVORY)
            y += 38
        y += 14

    cta = data.get("cta", "La sua storia nella web app · link in bio")
    cf = fit_block(d, cta, BOLD, ax - 110, 2, 30, 22)
    cy = H - 250 - BAND
    for ln in cf[1]:
        d.text((70, cy), ln, font=cf[0], fill=CORAL)
        cy += int(cf[2] * 1.25)
    footer(d)


def make(data, out):
    img = Image.new("RGB", (W, H), NAVY)
    (founder if data.get("layout") == "founder" else brand)(data, img)
    promise_band(ImageDraw.Draw(img), W, H)
    img.save(out, "PNG", optimize=True)


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as fh:
        make(json.load(fh), sys.argv[2])
    print("ok", sys.argv[2])
