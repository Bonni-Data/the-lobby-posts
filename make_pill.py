#!/usr/bin/env python3
"""THE LOBBY - generatore grafica 'Pillola' (1080x1350, IG/FB).

Uso: python3 make_pill.py data.json output.png
data.json:
{
  "number": 1,
  "course": "Il Comune, senza segreti",
  "title": "Chi nomina gli assessori? (non il consiglio)",   # gancio, max ~70 caratteri
  "points": ["frase breve", "frase breve", "frase breve"],     # 3 punti, max ~85 caratteri ciascuno
  "takeaway": "frase finale breve"                              # opzionale, max ~60 caratteri
}
"""
import json
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
NAVY = (17, 28, 53)
CORAL = (255, 112, 88)
IVORY = (244, 240, 232)
NAVY_SOFT = (28, 42, 74)
INK = (60, 68, 92)

FD = "/usr/share/fonts/truetype/google-fonts/"
BOLD = FD + "Poppins-Bold.ttf"
MED = FD + "Poppins-Medium.ttf"
REG = FD + "Poppins-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def tw(d, t, f):
    return d.textlength(t, font=f)


def wrap(d, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(d, t, f) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_block(d, text, path, max_w, max_lines, start, min_size):
    size = start
    while True:
        f = font(path, size)
        lines = wrap(d, text, f, max_w)
        if len(lines) <= max_lines or size <= min_size:
            return f, lines, size
        size -= 2


def draw_arch(d, x, y, w, h, color, thick):
    r = w / 2
    d.arc([x, y, x + w, y + w], 180, 360, fill=color, width=thick)
    d.line([x + thick / 2 - 1, y + r, x + thick / 2 - 1, y + h], fill=color, width=thick)
    d.line([x + w - thick / 2, y + r, x + w - thick / 2, y + h], fill=color, width=thick)
    d.line([x - thick, y + h, x + w + thick, y + h], fill=color, width=thick)


def draw_logo(img, x, y, scale=1.0):
    d = ImageDraw.Draw(img)
    aw, ah = int(64 * scale), int(86 * scale)
    draw_arch(d, x, y, aw, ah, CORAL, max(6, int(8 * scale)))
    cx = x + aw / 2
    rr = int(7 * scale)
    d.ellipse([cx - rr, y + ah * 0.55 - rr, cx + rr, y + ah * 0.55 + rr], fill=IVORY)
    d.text((x + aw + int(26 * scale), y + int(8 * scale)), "THE LOBBY", font=font(BOLD, int(46 * scale)), fill=IVORY)
    d.text((x + aw + int(28 * scale), y + int(62 * scale)), "WHERE INFLUENCE BEGINS.", font=font(MED, int(17 * scale)), fill=CORAL)


def make(data, out):
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    draw_arch(d, 640, 40, 520, 1200, NAVY_SOFT, 26)
    d = ImageDraw.Draw(img)
    draw_logo(img, 70, 62, 1.0)

    # etichetta pillola
    label = "PILLOLA #%s" % data.get("number", "")
    lf = font(BOLD, 28)
    lw = tw(d, label, lf) + 44
    d.rounded_rectangle((70, 200, 70 + lw, 252), radius=26, fill=CORAL)
    d.text((92, 206), label, font=lf, fill=NAVY)
    d.text((70 + lw + 22, 210), data.get("course", "").upper(), font=font(MED, 24), fill=IVORY)

    # gancio (titolo)
    tf, tl, ts = fit_block(d, data["title"], BOLD, W - 70 - 110, 4, 78, 52)
    y = 290
    lh = int(ts * 1.22)
    for ln in tl:
        d.text((70, y), ln, font=tf, fill=IVORY)
        y += lh

    # card con i punti
    card_top = max(y + 30, 640)
    card_bot = H - 270
    d.rounded_rectangle((60, card_top, W - 60, card_bot), radius=34, fill=IVORY)
    px = 120
    pmax = W - 60 - 40 - px
    pts = data["points"][:3]
    pf, _, ps = fit_block(d, max(pts, key=len), MED, pmax, 3, 34, 24)
    # calcola altezza totale per centrare verticalmente
    blocks = [wrap(d, p, pf, pmax) for p in pts]
    plh = int(ps * 1.32)
    gap = 34
    total = sum(len(b) * plh for b in blocks) + gap * (len(blocks) - 1)
    yy = card_top + (card_bot - card_top - total) / 2
    for b in blocks:
        d.ellipse([72, yy + plh / 2 - 14 - 0, 100, yy + plh / 2 + 14], fill=CORAL)
        for ln in b:
            d.text((px, yy), ln, font=pf, fill=NAVY)
            yy += plh
        yy += gap

    # chiusura + CTA
    ty = card_bot + 26
    tk = data.get("takeaway")
    if tk:
        kf, kl, ks = fit_block(d, tk, BOLD, W - 140, 1, 36, 26)
        d.text((70, ty), kl[0], font=kf, fill=CORAL)
    cta = "Altre pillole così nella web app · link in bio"
    cf = fit_block(d, cta, MED, W - 140, 1, 28, 20)[0]
    d.text((70, ty + 56), cta, font=cf, fill=IVORY)

    # footer
    fy = H - 90
    d.line([70, fy, W - 70, fy], fill=CORAL, width=3)
    d.text((70, fy + 18), "Andrea Bonazzi", font=font(BOLD, 36), fill=IVORY)
    s = "Salva · Condividi"
    sf = font(MED, 24)
    d.text((W - 70 - tw(d, s, sf), fy + 28), s, font=sf, fill=CORAL)

    img.save(out, "PNG", optimize=True)


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as fh:
        make(json.load(fh), sys.argv[2])
    print("ok", sys.argv[2])
