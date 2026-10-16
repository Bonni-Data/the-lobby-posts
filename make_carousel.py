#!/usr/bin/env python3
"""THE LOBBY - carosello Instagram/Facebook (slide 1080x1350).

Uso: python3 make_carousel.py data.json cartella_uscita/
Scrive 01.png, 02.png, ... nella cartella (da 4 a 9 slide in tutto).

data.json:
{
  "kicker": "LEZIONE IN 6 SLIDE",                   # max ~26 caratteri
  "title": "Chi decide davvero nel tuo Comune?",     # copertina, max ~60 caratteri
  "subtitle": "Sindaco, giunta e consiglio in 2 minuti",   # facoltativo, max ~70
  "slides": [                                        # da 2 a 7 slide di contenuto
    {"title": "Il consiglio", "text": "Approva bilancio e regolamenti. ...", "tag": "facoltativo, max ~22"}
  ],
  "cta": {"title": "Il corso completo è gratis", "text": "5 lezioni da 5 minuti, quiz e certificato."},
  "source": "Fonte: TUEL, d.lgs. 267/2000"           # facoltativo, in piccolo sull'ultima slide di contenuto
}
Testi: titolo di slide max ~50 caratteri, testo max ~260 caratteri.
"""
import json
import os
import sys
from PIL import Image, ImageDraw

from make_pill import W, H, NAVY, CORAL, IVORY, NAVY_SOFT, BOLD, MED, REG, font, tw, wrap, fit_block, draw_arch, draw_logo

PAPER = (251, 249, 245)
MUTED = (91, 98, 117)
LINE = (227, 221, 209)


def pill(d, x, y, text, fill=CORAL, ink=NAVY, size=28):
    f = font(BOLD, size)
    w = tw(d, text, f) + 44
    d.rounded_rectangle((x, y, x + w, y + size + 24), radius=(size + 24) // 2, fill=fill)
    d.text((x + 22, y + 6), text, font=f, fill=ink)
    return w


def dots(d, i, n, y, on, off):
    total = n * 18 + (n - 1) * 10
    x = (W - total) / 2
    for k in range(n):
        d.rounded_rectangle((x, y, x + (34 if k == i else 18), y + 10), radius=5, fill=on if k == i else off)
        x += (34 if k == i else 18) + 10


def swipe(d, color, y=H - 128):
    f = font(MED, 26)
    t = "Scorri"
    x = W - 70 - tw(d, t, f) - 46
    d.text((x, y), t, font=f, fill=color)
    ax = W - 70 - 30
    d.line([ax, y + 18, ax + 28, y + 18], fill=color, width=4)
    d.line([ax + 16, y + 6, ax + 28, y + 18], fill=color, width=4)
    d.line([ax + 16, y + 30, ax + 28, y + 18], fill=color, width=4)


def cover(data, n):
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    draw_arch(d, 560, 220, 600, 1240, NAVY_SOFT, 30)
    draw_arch(d, 690, 420, 340, 1040, NAVY_SOFT, 18)
    draw_logo(img, 70, 62, 1.0)
    d = ImageDraw.Draw(img)
    pill(d, 70, 230, data.get("kicker", "THE LOBBY").upper())
    tf, tl, ts = fit_block(d, data["title"], BOLD, W - 150, 5, 108, 64)
    y = 380
    for ln in tl:
        d.text((70, y), ln, font=tf, fill=IVORY)
        y += int(ts * 1.12)
    if data.get("subtitle"):
        sf, sl, ss = fit_block(d, data["subtitle"], MED, W - 180, 3, 38, 28)
        y += 26
        for ln in sl:
            d.text((70, y), ln, font=sf, fill=CORAL)
            y += int(ss * 1.32)
    dots(d, 0, n, H - 70, CORAL, NAVY_SOFT)
    swipe(d, IVORY)
    return img


def content(data, s, i, n, last_content):
    img = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(img)
    # small arch mark and page number
    draw_arch(d, 70, 70, 44, 58, CORAL, 7)
    d.ellipse([88, 101, 98, 111], fill=NAVY)
    pf = font(MED, 26)
    page = f"{i + 1}/{n}"
    d.text((W - 70 - tw(d, page, pf), 82), page, font=pf, fill=MUTED)
    num = f"{i:02d}"
    d.text((70, 190), num, font=font(BOLD, 150), fill=CORAL)
    y = 390
    if s.get("tag"):
        pill(d, 70, y, s["tag"].upper(), fill=NAVY, ink=IVORY, size=24)
        y += 76
    tf, tl, ts = fit_block(d, s["title"], BOLD, W - 140, 3, 76, 50)
    for ln in tl:
        d.text((70, y), ln, font=tf, fill=NAVY)
        y += int(ts * 1.14)
    y += 30
    d.line([70, y, 190, y], fill=CORAL, width=6)
    y += 44
    bf, bl, bs = fit_block(d, s["text"], REG, W - 150, 10, 50, 32)
    for ln in bl:
        d.text((70, y), ln, font=bf, fill=NAVY)
        y += int(bs * 1.42)
    if last_content and data.get("source"):
        sf = font(REG, 22)
        for k, ln in enumerate(wrap(d, data["source"], sf, W - 140)[:2]):
            d.text((70, H - 200 + k * 30), ln, font=sf, fill=MUTED)
    dots(d, i, n, H - 70, NAVY, LINE)
    if i < n - 1:
        swipe(d, NAVY)
    return img


def final(data, n):
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    draw_arch(d, 330, 120, 420, 560, NAVY_SOFT, 26)
    draw_arch(d, 440, 250, 200, 400, CORAL, 12)
    d.ellipse([528, 478, 552, 502], fill=IVORY)
    cta = data.get("cta", {})
    tf, tl, ts = fit_block(d, cta.get("title", "È tutto gratis"), BOLD, W - 160, 3, 84, 56)
    y = 760
    for ln in tl:
        d.text(((W - tw(d, ln, tf)) / 2, y), ln, font=tf, fill=IVORY)
        y += int(ts * 1.12)
    if cta.get("text"):
        sf, sl, ss = fit_block(d, cta["text"], MED, W - 200, 2, 36, 26)
        y += 14
        for ln in sl:
            d.text(((W - tw(d, ln, sf)) / 2, y), ln, font=sf, fill=IVORY)
            y += int(ss * 1.35)
    f = font(BOLD, 34)
    label = "thelobbyitalia.it · link in bio"
    w = tw(d, label, f) + 70
    x = (W - w) / 2
    y = max(y + 40, 1090)
    d.rounded_rectangle((x, y, x + w, y + 78), radius=39, fill=CORAL)
    d.text((x + 35, y + 16), label, font=f, fill=NAVY)
    sv = "Salva il post · Mandalo a un amico"
    sf = font(MED, 26)
    d.text(((W - tw(d, sv, sf)) / 2, H - 150), sv, font=sf, fill=CORAL)
    dots(d, n - 1, n, H - 70, CORAL, NAVY_SOFT)
    return img


def make(data, outdir):
    slides = data["slides"][:7]
    if len(slides) < 2:
        raise SystemExit("servono almeno 2 slide di contenuto")
    n = len(slides) + 2
    os.makedirs(outdir, exist_ok=True)
    imgs = [cover(data, n)]
    for k, s in enumerate(slides, 1):
        imgs.append(content(data, s, k, n, k == len(slides)))
    imgs.append(final(data, n))
    paths = []
    for k, im in enumerate(imgs, 1):
        p = os.path.join(outdir, f"{k:02d}.png")
        im.save(p, "PNG", optimize=True)
        paths.append(p)
    return paths


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as fh:
        for p in make(json.load(fh), sys.argv[2]):
            print("ok", p)
