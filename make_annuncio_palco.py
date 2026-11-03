#!/usr/bin/env python3
"""THE LOBBY - storia 1080x1920 «Settimana prossima», versione con Andrea in primo piano che parla.

Uso: python3 make_annuncio_palco.py uscita.png
Foto: volto/libreria/mani-aperte-1.png (fotogramma reale, già scontornato). Niente pubblico o scene inventate.
"""
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from make_annuncio import mic, paper, pin
from make_pill import (BOLD, CORAL, IVORY, MED, NAVY, NAVY_SOFT, PROMISE_LINE, draw_arch, draw_logo, fit_block,
                       font, tw)

W, H = 1080, 1920
PHOTO = "volto/libreria/mani-aperte-1.png"
DEEP = (8, 13, 30)


def blurred_shape(draw_fn, blur, color, alpha):
    m = Image.new("L", (W, H), 0)
    draw_fn(ImageDraw.Draw(m), alpha)
    m = m.filter(ImageFilter.GaussianBlur(blur))
    layer = Image.new("RGBA", (W, H), color + (0,))
    layer.putalpha(m)
    return layer


def make(out):
    img = Image.new("RGBA", (W, H), DEEP + (255,))
    # luce da palco: due fasci dall'alto che si incrociano su Andrea + alone corallo
    img.alpha_composite(blurred_shape(lambda d, a: d.polygon([(-40, 0), (230, 0), (700, 1500), (330, 1500)], fill=a),
                                      40, (255, 236, 214), 46))
    img.alpha_composite(blurred_shape(lambda d, a: d.polygon([(850, 0), (1120, 0), (750, 1500), (380, 1500)], fill=a),
                                      40, (255, 236, 214), 46))
    img.alpha_composite(blurred_shape(lambda d, a: d.ellipse((150, 520, 930, 1300), fill=a), 150, CORAL, 150))
    img.alpha_composite(blurred_shape(lambda d, a: d.ellipse((200, 1380, 880, 1560), fill=a), 50, (255, 236, 214), 60))

    d = ImageDraw.Draw(img)
    draw_arch(d, 170, 560, 740, 1000, NAVY_SOFT, 22)
    draw_arch(d, 250, 640, 580, 920, CORAL, 12)

    # Andrea in primo piano
    p = Image.open(PHOTO).convert("RGBA")
    sc = 0.76
    pw, ph = int(p.width * sc), int(p.height * sc)
    p = p.resize((pw, ph), Image.LANCZOS)
    a = p.getchannel("A")
    rim = Image.new("RGBA", (pw, ph), IVORY + (0,))
    rim.putalpha(a.filter(ImageFilter.MaxFilter(11)))
    shadow = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    shadow.putalpha(a.filter(ImageFilter.GaussianBlur(26)).point(lambda v: int(v * 0.6)))
    px, py = (W - pw) // 2, 476
    img.alpha_composite(shadow, (px + 14, py + 22))
    img.alpha_composite(rim, (px, py))
    img.alpha_composite(p, (px, py))

    d = ImageDraw.Draw(img)
    draw_logo(img, 64, 104, 0.72)
    d = ImageDraw.Draw(img)
    lf = font(BOLD, 26)
    ln = "@thelobbyitalia"
    d.text((W - 64 - tw(d, ln, lf), 128), ln, font=lf, fill=IVORY)

    # etichetta + titolo
    kf = font(BOLD, 32)
    k = "SETTIMANA PROSSIMA"
    kw = tw(d, k, kf) + 70
    kx = (W - kw) / 2
    d.rounded_rectangle((kx, 236, kx + kw, 298), radius=31, fill=CORAL)
    d.ellipse((kx + 26, 258, kx + 44, 276), fill=NAVY)
    d.text((kx + 56, 246), k, font=kf, fill=NAVY)

    tf = font(BOLD, 116)
    a1, a2 = "SI FA", "SENTIRE"
    w1, w2 = tw(d, a1, tf), tw(d, a2, tf)
    gap, padx = 28, 26
    total = w1 + gap + w2 + 2 * padx
    x0 = (W - total) / 2
    ty = 320
    d.text((x0, ty), a1, font=tf, fill=IVORY)
    bx = x0 + w1 + gap
    d.rounded_rectangle((bx, ty + 14, bx + w2 + 2 * padx, ty + 150), radius=20, fill=CORAL)
    d.text((bx + padx, ty), a2, font=tf, fill=NAVY)

    # tre schede in fila, sopra le mani
    items = [
        (mic, "IN ONDA", ["La mia intervista", "su Radio Canale", "Italia e Radio Marconi"]),
        (paper, "SUI GIORNALI", ["I primi articoli", "di giornale", "su THE LOBBY"]),
        (pin, "IN TOUR", ["Nelle giovanili", "e nelle scuole"]),
    ]
    tile_y, tile_h, g = 1468, 236, 18
    tile_w = (W - 2 * 48 - 2 * g) // 3
    for i, (icon, tag, lines) in enumerate(items):
        x = 48 + i * (tile_w + g)
        d.rounded_rectangle((x, tile_y, x + tile_w, tile_y + tile_h), radius=26, fill=IVORY)
        cx, cy = x + 52, tile_y + 50
        d.ellipse((cx - 32, cy - 32, cx + 32, cy + 32), fill=NAVY)
        icon(d, cx, cy + 1, 0.72, CORAL)
        d.text((x + 96, tile_y + 34), tag, font=font(BOLD, 24 if len(tag) < 10 else 21), fill=CORAL)
        bf = font(BOLD, 25)
        for j, t in enumerate(lines):
            d.text((x + 22, tile_y + 100 + j * 34), t, font=bf, fill=NAVY)

    # promesse
    by, bh = 1726, 58
    d.rectangle((0, by, W, by + bh), fill=CORAL)
    f = fit_block(d, PROMISE_LINE, BOLD, W - 100, 1, 26, 16)[0]
    l, t, r, b = d.textbbox((0, 0), PROMISE_LINE, font=f)
    d.text(((W - (r - l)) / 2 - l, by + (bh - (b - t)) / 2 - t), PROMISE_LINE, font=f, fill=NAVY)

    img.convert("RGB").save(out, "PNG", optimize=True)
    return out


if __name__ == "__main__":
    print("ok", make(sys.argv[1]))
