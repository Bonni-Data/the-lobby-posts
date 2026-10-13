#!/usr/bin/env python3
"""THE LOBBY - generatore grafica settimanale (1080x1350, IG/FB).

Uso: python3 make_post.py data.json output.png
data.json:
{
  "week_label": "Settimana del 13 ottobre 2026",
  "items": [
    {"title": "...", "desc": "...", "deadline": "15 ott"},   # esattamente 3
    ...
  ]
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

FD = "/usr/share/fonts/truetype/google-fonts/"
BOLD = FD + "Poppins-Bold.ttf"
MED = FD + "Poppins-Medium.ttf"
REG = FD + "Poppins-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(d, t, f):
    return d.textlength(t, font=f)


def fit(d, t, path, size, max_w, min_size=24):
    while size > min_size and text_w(d, t, font(path, size)) > max_w:
        size -= 2
    return font(path, size)


def draw_arch(d, x, y, w, h, color, thick):
    """Arco 'Atrio/Soglia': montanti + semicerchio, contorno."""
    r = w / 2
    d.arc([x, y, x + w, y + w], 180, 360, fill=color, width=thick)
    d.line([x + thick / 2 - 1, y + r, x + thick / 2 - 1, y + h], fill=color, width=thick)
    d.line([x + w - thick / 2, y + r, x + w - thick / 2, y + h], fill=color, width=thick)
    # soglia
    d.line([x - thick, y + h, x + w + thick, y + h], fill=color, width=thick)


def draw_logo(img, x, y, scale=1.0):
    d = ImageDraw.Draw(img)
    aw, ah = int(64 * scale), int(86 * scale)
    draw_arch(d, x, y, aw, ah, CORAL, max(6, int(8 * scale)))
    # punto centrale sotto l'arco (la "persona" nell'atrio)
    cx = x + aw / 2
    rr = int(7 * scale)
    d.ellipse([cx - rr, y + ah * 0.55 - rr, cx + rr, y + ah * 0.55 + rr], fill=IVORY)
    f = font(BOLD, int(46 * scale))
    # Wordmark: THE LOBBY, O ben leggibile (nessuna sostituzione grafica sulla O)
    d.text((x + aw + int(26 * scale), y + int(8 * scale)), "THE LOBBY", font=f, fill=IVORY)
    f2 = font(MED, int(17 * scale))
    d.text((x + aw + int(28 * scale), y + int(62 * scale)), "WHERE INFLUENCE BEGINS.", font=f2, fill=CORAL)


def rounded(d, box, r, fill):
    d.rounded_rectangle(box, radius=r, fill=fill)


def make(data, out):
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # grande arco decorativo di sfondo
    deco = Image.new("RGB", (W, H), NAVY)
    dd = ImageDraw.Draw(deco)
    draw_arch(dd, 640, 40, 520, 1200, NAVY_SOFT, 26)
    img.paste(deco)
    d = ImageDraw.Draw(img)

    # logo in alto
    draw_logo(img, 70, 62, 1.0)

    # titolo
    d.text((70, 215), "3 OPPORTUNITÀ", font=font(BOLD, 84), fill=IVORY)
    d.text((70, 312), "da cogliere adesso", font=font(BOLD, 84), fill=CORAL)
    d.text((72, 424), data.get("week_label", ""), font=font(MED, 28), fill=IVORY)

    # card
    items = data["items"][:3]
    top = 490
    card_h = 218
    gap = 24
    for i, it in enumerate(items):
        y0 = top + i * (card_h + gap)
        rounded(d, (60, y0, W - 60, y0 + card_h), 34, IVORY)
        # numero
        cx, cy = 130, y0 + card_h // 2
        d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=CORAL)
        nf = font(BOLD, 44)
        nt = str(i + 1)
        d.text((cx - text_w(d, nt, nf) / 2, cy - 33), nt, font=nf, fill=NAVY)

        tx = 200
        max_w = W - 60 - 30 - tx
        tag = it.get("tag")
        title_max = max_w
        if tag:
            tgf = font(BOLD, 20)
            tgw = text_w(d, tag.upper(), tgf) + 32
            tgx = W - 60 - 28 - tgw
            title_max = tgx - 16 - tx
            rounded(d, (tgx, y0 + 26, tgx + tgw, y0 + 62), 18, CORAL)
            d.text((tgx + 16, y0 + 31), tag.upper(), font=tgf, fill=NAVY)
        tf = fit(d, it["title"], BOLD, 42, title_max, 28)
        d.text((tx, y0 + 28), it["title"], font=tf, fill=NAVY)
        df = fit(d, it["desc"], REG, 28, max_w, 20)
        d.text((tx, y0 + 88), it["desc"], font=df, fill=(60, 68, 92))
        # pill scadenza
        label = "SCADENZA  " + it["deadline"].upper()
        pf = font(BOLD, 26)
        pw = text_w(d, label, pf) + 44
        px, py = tx, y0 + 144
        rounded(d, (px, py, px + pw, py + 48), 24, NAVY)
        d.text((px + 22, py + 7), label, font=pf, fill=CORAL)

    # footer con nome
    fy = H - 108
    d.line([70, fy, W - 70, fy], fill=CORAL, width=3)
    d.text((70, fy + 24), "Andrea Bonazzi", font=font(BOLD, 40), fill=IVORY)
    cta = "Salva il post · Condividilo"
    cf = font(MED, 26)
    d.text((W - 70 - text_w(d, cta, cf), fy + 34), cta, font=cf, fill=CORAL)

    img.save(out, "PNG", optimize=True)


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as fh:
        make(json.load(fh), sys.argv[2])
    print("ok", sys.argv[2])
