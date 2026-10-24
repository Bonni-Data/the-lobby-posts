#!/usr/bin/env python3
"""THE LOBBY - copertina «faccia + 2 parole» (decisione di Andrea del 24 ottobre 2026).

Ogni contenuto deve mostrare il volto di Andrea con una o due parole grandi accanto che richiamano il concetto;
la spiegazione viene dopo (slide del carosello, didascalia o video).

Uso: python3 make_face.py data.json uscita.png
data.json:
{
  "format": "post",                 # "post" 1080x1350 (post e copertina carosello) o "reel" 1080x1920 (cover reel e storie)
  "face": "volto/libreria/indica.png",   # PNG scontornato con volto/scontorna.py (accanto c'è il .json con il riquadro del viso)
  "words": ["VIAGGI", "GRATIS"],    # 1 o 2 parole (max ~10 lettere l'una); la seconda va nel riquadro corallo
  "kicker": "OPPORTUNITÀ",          # facoltativo, etichetta piccola in alto (max ~22 caratteri)
  "sub": "3 bandi con spese pagate dagli enti",   # facoltativo, una riga sotto le parole (max ~45 caratteri)
  "side": "right",                  # dove sta Andrea: "right" (default) o "left"
  "theme": "navy",                  # "navy" (default) o "ivory"
  "swipe": true,                    # facoltativo: freccia «Scorri» per i caroselli
  "card": {"photo": "posts/ritratti/.../foto-2.jpg", "label": "Tina Anselmi",   # facoltativo (ritratti):
           "credit": "Foto: autore · licenza · Wikimedia Commons (ritagliata)",   # la foto del personaggio in una
           "focus_x": 0.3, "focus_y": 0.1, "zoom": 1.2}                          # cornice che Andrea presenta
}
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

from make_pill import (BAND, BOLD, CORAL, IVORY, MED, NAVY, NAVY_SOFT, draw_arch, draw_logo, fit_block, font,
                       promise_band, tw)

SIZES = {"post": (1080, 1350), "reel": (1080, 1920)}


def sticker(face, stroke=10, color=IVORY):
    """Bordo pieno attorno alla sagoma (effetto adesivo) e ombra morbida: stacca il volto dallo sfondo."""
    a = face.split()[-1]
    pad = stroke * 3
    big = Image.new("L", (face.width + pad * 2, face.height + pad * 2), 0)
    big.paste(a, (pad, pad))
    grown = big.filter(ImageFilter.MaxFilter(stroke * 2 + 1)).filter(ImageFilter.GaussianBlur(1.2))
    out = Image.new("RGBA", big.size, (0, 0, 0, 0))
    shadow = Image.new("RGBA", big.size, (5, 10, 25, 0))
    sh = Image.new("L", big.size, 0)
    sh.paste(grown.crop((0, 0, big.width, big.height - stroke)), (0, stroke))  # ombra spostata in basso, senza riavvolgere
    shadow.putalpha(sh.filter(ImageFilter.GaussianBlur(stroke * 1.6)).point(lambda v: int(v * 0.55)))
    out = Image.alpha_composite(out, shadow)
    rim = Image.new("RGBA", big.size, color + (0,))
    rim.putalpha(grown)
    out = Image.alpha_composite(out, rim)
    body = Image.new("RGBA", big.size, (0, 0, 0, 0))
    body.paste(face, (pad, pad), face)
    return Image.alpha_composite(out, body), pad


def load_face(path):
    face = Image.open(path).convert("RGBA")
    meta_path = os.path.splitext(path)[0] + ".json"
    box = None
    if os.path.exists(meta_path):
        box = json.load(open(meta_path)).get("face")
    if not box:  # senza riquadro: si assume il volto in alto al centro della sagoma
        w = face.width * 0.36
        box = [face.width / 2 - w / 2, face.height * 0.06, w, w * 1.15]
    return face, box


def place_face(img, path, side, top, bottom, face_h, face_x=None, shift=0):
    """Scala la sagoma perché il viso sia alto face_h px e la appoggia sul fondo (bottom); restituisce il riquadro del viso."""
    W, H = img.size
    face, (fx, fy, fw, fh) = load_face(path)
    s = face_h / fh
    # la sagoma deve arrivare fino in fondo: se è corta la ingrandisco
    need = (bottom - top) / face.height
    s = max(s, need * 0.92)
    face = face.resize((int(face.width * s), int(face.height * s)), Image.LANCZOS)
    fx, fy, fw, fh = fx * s, fy * s, fw * s, fh * s
    cx = W * (face_x if face_x else (0.68 if side == "right" else 0.32))
    x = int(cx - (fx + fw / 2))
    y = int(bottom - face.height * 0.94) + int(shift)  # il fondo della sagoma (spesso irregolare) finisce sotto la fascia
    st, pad = sticker(face)
    img.alpha_composite(st, (x - pad, y - pad))
    global LAST_MASK
    LAST_MASK = Image.new("L", img.size, 0)
    LAST_MASK.paste(st.split()[-1], (x - pad, y - pad))
    return [x + fx, y + fy, fw, fh]


LAST_MASK = None


def free_x(side, y0, y1, fallback, margin=34):
    """Fin dove può arrivare il testo tra y0 e y1 senza finire sopra Andrea (mani e braccia comprese)."""
    if LAST_MASK is None:
        return fallback
    W = LAST_MASK.width
    band = LAST_MASK.crop((0, max(0, int(y0)), W, min(LAST_MASK.height, int(y1)))).point(lambda v: 255 if v > 60 else 0)
    bb = band.getbbox()
    if not bb:
        return fallback
    import numpy as np
    a = np.array(band) > 0
    cols = np.where(a.any(axis=0))[0]
    if side == "right":
        return min(fallback, int(cols[0]) - margin)
    return max(fallback, int(cols[-1]) + margin)


def words_block(d, words, x0, x1, y, align, max_size):
    """Le parole grandi: la prima in avorio, la seconda dentro un riquadro corallo. Restituisce la y finale."""
    col = x1 - x0
    size = max_size
    while size > 60:
        f = font(BOLD, size)
        if all(tw(d, w, f) + (48 if i == 1 else 0) <= col for i, w in enumerate(words)):
            break
        size -= 4
    f = font(BOLD, size)
    for i, w in enumerate(words):
        l, t, r, b = d.textbbox((0, 0), w, font=f)
        wd = r - l
        x = x0 if align == "left" else x1 - wd - (48 if i == 1 else 0)
        if i == 1:
            pad = 24
            d.rounded_rectangle((x, y + t - 14, x + wd + pad * 2, y + b + 16), radius=18, fill=CORAL)
            d.text((x + pad - l, y), w, font=f, fill=NAVY)
            y += int((b - t) + 52)
        else:
            d.text((x - l, y), w, font=f, fill=IVORY, stroke_width=7, stroke_fill=NAVY)
            y += int((b - t) + 40)
    return y


def photo_card(img, card, x, y, w, h, angle=-4):
    """Cornice chiara con la foto del personaggio, il nome sotto e il credito della licenza in piccolo."""
    ph = Image.open(card["photo"]).convert("RGB")
    s = max(w / ph.width, h / ph.height) * float(card.get("zoom", 1.0))
    ph = ph.resize((int(ph.width * s) + 1, int(ph.height * s) + 1), Image.LANCZOS)
    left = min(max(int(float(card.get("focus_x", 0.5)) * ph.width - w / 2), 0), ph.width - w)
    top = min(max(int(float(card.get("focus_y", 0.2)) * ph.height - h / 3), 0), ph.height - h)
    ph = ph.crop((left, top, left + w, top + h))
    m, lab_h = 18, 92
    fr = Image.new("RGBA", (w + 2 * m, h + m + lab_h), IVORY + (255,))
    fr.paste(ph, (m, m))
    fd = ImageDraw.Draw(fr)
    lf, ll, ls = fit_block(fd, card.get("label", ""), BOLD, w, 1, 40, 26)
    fd.text((m, h + m + 12), ll[0] if ll else "", font=lf, fill=NAVY)
    if card.get("credit"):
        cf, cl, cs = fit_block(fd, card["credit"], MED, w, 1, 15, 11)
        fd.text((m, h + m + 62), cl[0], font=cf, fill=(91, 98, 117))
    rot = fr.rotate(angle, resample=Image.BICUBIC, expand=True)
    sh = Image.new("RGBA", rot.size, (5, 10, 25, 0))
    sh.putalpha(rot.split()[-1].filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.5)))
    img.alpha_composite(sh, (x + 8, y + 14))
    img.alpha_composite(rot, (x, y))
    return y + rot.height


def make(data, out):
    fmt = data.get("format", "post")
    W, H = SIZES[fmt]
    side = data.get("side", "right")
    ivory = data.get("theme") == "ivory"
    bg = IVORY if ivory else NAVY
    img = Image.new("RGBA", (W, H), bg + (255,))
    d = ImageDraw.Draw(img)

    band_y = H - BAND if fmt == "post" else 1560
    # l'arco di THE LOBBY fa da «porta» dietro Andrea
    ax = int(W * (0.68 if side == "right" else 0.32))
    aw = 560 if fmt == "post" else 700
    atop = 300 if fmt == "post" else 470
    draw_arch(d, ax - aw // 2, atop, aw, band_y - atop + 40, NAVY_SOFT if not ivory else (232, 225, 211), 30)
    draw_arch(d, ax - aw // 2 + 70, atop + 90, aw - 140, band_y - atop, CORAL, 12)

    # volto
    if fmt == "post":
        top, bottom, face_h = 330, band_y, 300
    else:
        top, bottom, face_h = 600, band_y + 140, 380
    face_h = int(data.get("face_h", face_h))
    face_box = place_face(img, data["face"], side, top, bottom, face_h, data.get("face_x"), data.get("face_shift", 0))
    d = ImageDraw.Draw(img)

    # logo e kicker
    logo_x = 70 if side == "right" else W - 70 - 380
    draw_logo(img, logo_x, 62 if fmt == "post" else 150, 0.82)
    d = ImageDraw.Draw(img)

    # colonna delle parole, dal lato opposto ad Andrea, all'altezza del viso
    fx, fy, fw, fh = face_box
    if side == "right":
        x0, x1, align = 64, int(fx - 44), "left"
    else:
        x0, x1, align = int(fx + fw + 44), W - 64, "right"
    # il testo non va sopra Andrea: si ferma dove inizia la sagoma (anche un braccio o una mano alzata)
    yt0 = (220 if fmt == "post" else 330) if data.get("card") else (data.get("words_y") or max(fy - 40, 230 if fmt == "post" else 330))
    words_h = 380 if data.get("kicker") else 300   # quanto sono alte etichetta + parole
    if side == "right":
        x1 = free_x("right", yt0, yt0 + words_h, x1)
    else:
        x0 = free_x("left", yt0, yt0 + words_h, x0)
    x1 = max(x1, x0 + 400) if side == "right" else x1
    if side == "left":
        x0 = min(x0, x1 - 400)
    card = data.get("card")
    if card:  # ritratto: le parole stanno sopra la cornice, che occupa il centro della colonna
        y = 220 if fmt == "post" else 330
        cw = min(x1 - x0 - 50, 430)
    elif data.get("words_y"):   # posizione fissa delle parole (es. foto in cui Andrea indica in alto)
        y = int(data["words_y"])
    else:
        y = int(max(fy - 40, 230 if fmt == "post" else 330))
    if data.get("kicker"):
        kf = font(BOLD, 26)
        kw = tw(d, data["kicker"].upper(), kf) + 40
        kx = x0 if align == "left" else x1 - kw
        d.rounded_rectangle((kx, y, kx + kw, y + 48), radius=24, fill=CORAL if not ivory else NAVY)
        d.text((kx + 20, y + 7), data["kicker"].upper(), font=kf, fill=NAVY if not ivory else IVORY)
        y += 80
    words = [w.upper() for w in data["words"][:2]]
    y = words_block(d, words, x0, x1, y, align, 150 if fmt == "post" else 170)
    if card:
        cx = x0 + 6 if align == "left" else x1 - cw - 42
        y = photo_card(img, card, cx, y + 4, cw, int(cw * 1.08)) + 6
        d = ImageDraw.Draw(img)
    if data.get("sub"):
        if side == "right":   # la riga sotto ha il suo spazio libero: può essere più stretto (mani, braccia)
            sx1 = max(free_x("right", y, y + 130, x1), x0 + 300)
            sx0 = x0
        else:
            sx0 = min(free_x("left", y, y + 130, x0), x1 - 300)
            sx1 = x1
        x0, x1 = sx0, sx1
        sf, sl, ss = fit_block(d, data["sub"], MED, x1 - x0, 3, 34, 24)
        y += 6
        for ln in sl:
            lx = x0 if align == "left" else x1 - tw(d, ln, sf)
            d.text((lx, y), ln, font=sf, fill=IVORY if not ivory else NAVY, stroke_width=5, stroke_fill=bg)
            y += int(ss * 1.3)

    # firma e promesse
    name_y = band_y - 64
    nf = font(BOLD, 30)
    nx = 64 if side == "right" else W - 64 - tw(d, "Andrea Bonazzi", nf)
    d.rounded_rectangle((nx - 18, name_y - 8, nx + tw(d, "Andrea Bonazzi", nf) + 18, name_y + 46), radius=27, fill=NAVY)
    d.text((nx, name_y - 2), "Andrea Bonazzi", font=nf, fill=IVORY)  # firma: il volto ha sempre un nome
    if data.get("swipe"):
        sw = "Scorri"
        sf = font(BOLD, 28)
        sx = W - 64 - tw(d, sw, sf) - 44 if side == "left" else 64
        sy = name_y - 62
        d.text((sx, sy), sw, font=sf, fill=CORAL)
        ax0 = sx + tw(d, sw, sf) + 12
        d.line([ax0, sy + 21, ax0 + 30, sy + 21], fill=CORAL, width=4)
        d.line([ax0 + 18, sy + 9, ax0 + 30, sy + 21], fill=CORAL, width=4)
        d.line([ax0 + 18, sy + 33, ax0 + 30, sy + 21], fill=CORAL, width=4)
    if fmt == "post":
        promise_band(d, W, H)
    else:
        sub = Image.new("RGBA", (W, BAND), (0, 0, 0, 0))
        promise_band(ImageDraw.Draw(sub), W, BAND)
        img.alpha_composite(sub, (0, band_y))
        d = ImageDraw.Draw(img)
        d.rectangle((0, band_y + BAND, W, H), fill=bg)
        tf = font(BOLD, 34)
        t = "thelobbyitalia.it · link in bio"
        d.text(((W - tw(d, t, tf)) / 2, band_y + BAND + 40), t, font=tf, fill=CORAL)
    img.convert("RGB").save(out, "PNG", optimize=True)
    return out


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as fh:
        print("ok", make(json.load(fh), sys.argv[2]))
