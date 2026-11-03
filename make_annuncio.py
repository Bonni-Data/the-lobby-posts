#!/usr/bin/env python3
"""THE LOBBY - storia 1080x1920 «Settimana prossima»: radio, giornali, tour.

Uso: python3 make_annuncio.py uscita.png
"""
import sys

from PIL import Image, ImageDraw, ImageFilter

from make_pill import (BOLD, CORAL, IVORY, MED, NAVY, NAVY_SOFT, PROMISE_LINE, draw_arch, draw_logo, fit_block,
                       font, tw)

W, H = 1080, 1920
PHOTO = "volto/libreria/sorriso-2.png"
DEEP = (10, 17, 36)


def glow(img, cx, cy, r, color, alpha):
    g = Image.new("L", (W, H), 0)
    ImageDraw.Draw(g).ellipse((cx - r, cy - r, cx + r, cy + r), fill=alpha)
    g = g.filter(ImageFilter.GaussianBlur(r * 0.45))
    layer = Image.new("RGBA", (W, H), color + (0,))
    layer.putalpha(g)
    img.alpha_composite(layer)


def mic(d, cx, cy, s, col):
    d.rounded_rectangle((cx - 9 * s, cy - 22 * s, cx + 9 * s, cy + 6 * s), radius=9 * s, fill=col)
    d.arc((cx - 16 * s, cy - 12 * s, cx + 16 * s, cy + 14 * s), 0, 180, fill=col, width=int(4 * s))
    d.line((cx, cy + 14 * s, cx, cy + 22 * s), fill=col, width=int(4 * s))
    d.line((cx - 10 * s, cy + 22 * s, cx + 10 * s, cy + 22 * s), fill=col, width=int(4 * s))


def paper(d, cx, cy, s, col):
    d.rounded_rectangle((cx - 20 * s, cy - 20 * s, cx + 20 * s, cy + 20 * s), radius=4 * s, outline=col, width=int(4 * s))
    d.rectangle((cx - 13 * s, cy - 13 * s, cx - 1 * s, cy - 1 * s), fill=col)
    for i, yy in enumerate((-12, -4, 6, 13)):
        x0 = cx + 4 * s if i < 2 else cx - 13 * s
        d.line((x0, cy + yy * s, cx + 13 * s, cy + yy * s), fill=col, width=int(3 * s))


def pin(d, cx, cy, s, col):
    d.ellipse((cx - 15 * s, cy - 24 * s, cx + 15 * s, cy + 6 * s), fill=col)
    d.polygon([(cx - 13 * s, cy - 3 * s), (cx + 13 * s, cy - 3 * s), (cx, cy + 22 * s)], fill=col)
    d.ellipse((cx - 6 * s, cy - 15 * s, cx + 6 * s, cy - 3 * s), fill=NAVY)


def make(out):
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    # fondo: sfumatura verso il basso + bagliori corallo
    grad = Image.new("L", (1, H))
    for y in range(H):
        grad.putpixel((0, y), int(255 * max(0, (y - 900) / 1020) ** 1.3))
    deep = Image.new("RGBA", (W, H), DEEP + (255,))
    deep.putalpha(grad.resize((W, H)))
    img.alpha_composite(deep)
    glow(img, 760, 640, 360, CORAL, 120)
    glow(img, 120, 1500, 300, (60, 90, 170), 70)

    d = ImageDraw.Draw(img)
    # archi del marchio dietro ad Andrea
    draw_arch(d, 470, 330, 560, 652, NAVY_SOFT, 22)
    draw_arch(d, 548, 420, 404, 560, CORAL, 12)

    # Andrea
    p = Image.open(PHOTO).convert("RGBA")
    ph = 840
    pw = int(p.width * ph / p.height)
    p = p.resize((pw, ph), Image.LANCZOS)
    a = p.getchannel("A")
    # bordo avorio attorno alla sagoma (stile del profilo) e dissolvenza in basso
    rim = a.filter(ImageFilter.MaxFilter(13))
    fade = Image.new("L", (1, ph))
    for y in range(ph):
        fade.putpixel((0, y), 255)
    fade = fade.resize((pw, ph))
    from PIL import ImageChops
    rim = ImageChops.multiply(rim, fade)
    a2 = ImageChops.multiply(a, fade)
    p.putalpha(a2)
    rl = Image.new("RGBA", (pw, ph), IVORY + (0,))
    rl.putalpha(rim)
    px, py = W - pw + 120, 250
    cut = 1001 - py  # la foto finisce sotto la prima scheda
    img.alpha_composite(rl.crop((0, 0, pw, cut)), (px, py))
    img.alpha_composite(p.crop((0, 0, pw, cut)), (px, py))

    d = ImageDraw.Draw(img)
    draw_logo(img, 64, 110, 0.78)
    d = ImageDraw.Draw(img)

    # etichetta
    kf = font(BOLD, 34)
    k = "SETTIMANA PROSSIMA"
    kw = tw(d, k, kf) + 64
    d.rounded_rectangle((64, 300, 64 + kw, 366), radius=33, fill=CORAL)
    d.ellipse((90, 324, 108, 342), fill=NAVY)
    d.text((120, 311), k, font=kf, fill=NAVY)

    # titolo
    tf = font(BOLD, 150)
    d.text((58, 420), "SI FA", font=tf, fill=IVORY)
    w2 = tw(d, "SENTIRE", tf)
    d.rounded_rectangle((52, 600, 52 + w2 + 40, 772), radius=22, fill=CORAL)
    d.text((72, 588), "SENTIRE", font=tf, fill=NAVY)
    sf = font(MED, 34)
    for i, ln in enumerate(("THE LOBBY arriva in radio,", "sui giornali e nelle scuole.")):
        d.text((64, 816 + i * 48), ln, font=sf, fill=IVORY)

    # tre schede
    items = [
        (mic, "IN ONDA", "La mia intervista su", "Radio Canale Italia e Radio Marconi"),
        (paper, "SUI GIORNALI", "I primi articoli", "di giornale su THE LOBBY"),
        (pin, "IN TOUR", "Nelle giovanili", "e nelle scuole"),
    ]
    y = 1000
    ch, gap = 164, 24
    for icon, tag, l1, l2 in items:
        card = Image.new("RGBA", (W - 128, ch), (0, 0, 0, 0))
        cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((0, 0, W - 129, ch - 1), radius=30, fill=(244, 240, 232, 255))
        img.alpha_composite(card, (64, y))
        d = ImageDraw.Draw(img)
        cx, cy = 64 + 92, y + ch / 2
        d.ellipse((cx - 56, cy - 56, cx + 56, cy + 56), fill=NAVY)
        icon(d, cx, cy + 1, 1.25, CORAL)
        tx = 64 + 180
        d.text((tx, y + 22), tag, font=font(BOLD, 26), fill=CORAL)
        lf = fit_block(d, l2, BOLD, W - 128 - 180 - 30, 1, 36, 26)[0]
        d.text((tx, y + 56), l1, font=font(MED, 34), fill=NAVY)
        d.text((tx, y + 100), l2, font=lf, fill=NAVY)
        y += ch + gap

    # chiusura
    cf = font(BOLD, 44)
    c = "Questo è solo l'inizio."
    d.text(((W - tw(d, c, cf)) / 2, y + 14), c, font=cf, fill=IVORY)
    hf = font(MED, 32)
    h = "thelobbyitalia.it · link in bio"
    d.text(((W - tw(d, h, hf)) / 2, y + 76), h, font=hf, fill=CORAL)

    # promesse
    by, bh = 1736, 60
    d.rectangle((0, by, W, by + bh), fill=CORAL)
    f = fit_block(d, PROMISE_LINE, BOLD, W - 100, 1, 26, 16)[0]
    l, t, r, b = d.textbbox((0, 0), PROMISE_LINE, font=f)
    d.text(((W - (r - l)) / 2 - l, by + (bh - (b - t)) / 2 - t), PROMISE_LINE, font=f, fill=NAVY)

    img.convert("RGB").save(out, "PNG", optimize=True)
    return out


if __name__ == "__main__":
    print("ok", make(sys.argv[1]))
