#!/usr/bin/env python3
"""THE LOBBY - la storia che rilancia ogni post (decisione di Andrea del 24 ottobre 2026: ogni post va anche nella storia).

Uso: python3 make_storia.py copertina.png uscita.png [--label "NUOVO POST"] [--hint "Scorri il carosello sul profilo"]
- copertina.png: la prima immagine del post (1080x1350 o 1080x1080)
- uscita.png: 1080x1920, con la copertina al centro, l'etichetta in alto e il rimando al profilo in basso
Per i reel non serve: la storia è il video del reel stesso (è già verticale).
"""
import sys

from PIL import Image, ImageDraw, ImageFilter

from make_pill import BOLD, CORAL, IVORY, MED, NAVY, NAVY_SOFT, draw_arch, draw_logo, font, tw

W, H = 1080, 1920


def make(src, out, label="NUOVO POST", hint="Lo trovi sul profilo @thelobbyitalia"):
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    d = ImageDraw.Draw(img)
    draw_arch(d, 90, 230, 900, 1500, NAVY_SOFT, 30)
    draw_logo(img, 64, 110, 0.72)
    d = ImageDraw.Draw(img)
    cover = Image.open(src).convert("RGB")
    cw = 900
    ch = int(cover.height * cw / cover.width)
    if ch > 1180:
        ch = 1180
        cw = int(cover.width * ch / cover.height)
    cover = cover.resize((cw, ch), Image.LANCZOS)
    x, y = (W - cw) // 2, 360
    # ombra e angoli arrotondati: sembra il post, appoggiato sulla storia
    sh = Image.new("L", (cw + 80, ch + 80), 0)
    ImageDraw.Draw(sh).rounded_rectangle((40, 40, cw + 40, ch + 40), radius=36, fill=150)
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    shl = Image.new("RGBA", sh.size, (0, 0, 0, 0)); shl.putalpha(sh)
    img.alpha_composite(shl, (x - 40, y - 20))
    m = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, cw - 1, ch - 1), radius=36, fill=255)
    rim = Image.new("RGBA", (cw + 12, ch + 12), (0, 0, 0, 0))
    ImageDraw.Draw(rim).rounded_rectangle((0, 0, cw + 11, ch + 11), radius=42, fill=IVORY + (255,))
    img.alpha_composite(rim, (x - 6, y - 6))
    img.paste(cover, (x, y), m)
    d = ImageDraw.Draw(img)
    kf = font(BOLD, 34)
    kw = tw(d, label, kf) + 56
    d.rounded_rectangle(((W - kw) // 2, 250, (W + kw) // 2, 316), radius=33, fill=CORAL)
    d.text(((W - kw) // 2 + 28, 262), label, font=kf, fill=NAVY)
    hf = font(BOLD, 40)
    yy = y + ch + 70
    d.text(((W - tw(d, hint, hf)) / 2, yy), hint, font=hf, fill=IVORY)
    sf = font(MED, 32)
    t = "thelobbyitalia.it · link in bio"
    d.text(((W - tw(d, t, sf)) / 2, yy + 66), t, font=sf, fill=CORAL)
    img.convert("RGB").save(out, "PNG", optimize=True)
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    kw = {}
    for k in ("--label", "--hint"):
        if k in a:
            i = a.index(k)
            kw[k[2:]] = a[i + 1]
            del a[i:i + 2]
    print("ok", make(a[0], a[1], **kw))
