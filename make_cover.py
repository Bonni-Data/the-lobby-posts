#!/usr/bin/env python3
"""THE LOBBY - immagine di copertina della Pagina Facebook.

Uso: python3 make_cover.py output.png

Misure: 1640 x 624 px (il doppio di 820 x 312, la copertina su computer).
Da telefono Facebook taglia i lati: testi e logo stanno nella fascia centrale
(x da 180 a 1460), e l'angolo in basso a sinistra resta libero per la foto profilo.
"""
import sys
from PIL import Image, ImageDraw

from make_pill import NAVY, CORAL, IVORY, NAVY_SOFT, BOLD, MED, font, tw, draw_arch, draw_logo

CW, CH = 1640, 624


def make(out):
    img = Image.new("RGB", (CW, CH), NAVY)
    d = ImageDraw.Draw(img)

    # archi di sfondo, come nei post (sui lati: su telefono vengono tagliati, non importa)
    draw_arch(d, -150, 150, 430, 640, NAVY_SOFT, 24)
    draw_arch(d, 1380, 70, 420, 700, NAVY_SOFT, 24)
    draw_arch(d, 1450, 230, 260, 540, NAVY_SOFT, 14)

    # logo centrato
    scale = 1.15
    aw = int(64 * scale)
    logo_w = aw + int(26 * scale) + tw(d, "THE LOBBY", font(BOLD, int(46 * scale)))
    draw_logo(img, (CW - logo_w) // 2, 62, scale)
    d = ImageDraw.Draw(img)

    # titolo su due righe
    tf = font(BOLD, 84)
    y = 196
    for line in ("Capisci le regole.", "Cambia le cose."):
        d.text(((CW - tw(d, line, tf)) / 2, y), line, font=tf, fill=IVORY)
        y += 96

    # sottotitolo
    sf = font(MED, 33)
    sub = "L'academy gratuita su Comune, Parlamento ed Europa"
    d.text(((CW - tw(d, sub, sf)) / 2, y + 18), sub, font=sf, fill=IVORY)

    # pillola corallo con l'indirizzo
    pf = font(BOLD, 30)
    pill = "Tutto gratis · thelobbyitalia.it"
    pw = tw(d, pill, pf) + 64
    px, py = (CW - pw) // 2, y + 88
    d.rounded_rectangle((px, py, px + pw, py + 60), radius=30, fill=CORAL)
    d.text((px + 32, py + 9), pill, font=pf, fill=NAVY)

    img.save(out, "PNG", optimize=True)


if __name__ == "__main__":
    make(sys.argv[1])
    print("ok", sys.argv[1])
