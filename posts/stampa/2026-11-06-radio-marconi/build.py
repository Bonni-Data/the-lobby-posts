"""Post e storia per l'intervista di Andrea a Radio Marconi («Belle Storie», 5 novembre 2026).
python3 build.py  (dalla cartella del post). Foto: volto/libreria/mani-aperte-1.png, foto vera scontornata."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, ROOT)
from PIL import Image, ImageDraw, ImageFilter  # noqa: E402
from make_pill import (BOLD, MED, REG, CORAL, IVORY, NAVY, NAVY_SOFT, font, tw, wrap, fit_block,  # noqa: E402
                       draw_arch, draw_logo, promise_band, promise_list)

T = json.load(open(os.path.join(HERE, 'testi.json'), encoding='utf-8'))
W, H = 1080, 1350
PHOTO = Image.open(os.path.join(ROOT, 'volto/libreria/mani-aperte-1.png')).convert('RGBA')


def person(height):
    s = height / PHOTO.height
    return PHOTO.resize((int(PHOTO.width * s), height), Image.LANCZOS)


def paste_person(img, p, x, y):
    # ombra morbida dietro la persona, poi la persona
    a = p.getchannel('A').filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.55))
    img.paste((5, 10, 25), (x + 10, y + 14), a)
    img.paste(p, (x, y), p)


def waveform(d, x, y, w, h, color, bars=34, seed=7):
    import random
    r = random.Random(seed)
    bw = w / bars
    for i in range(bars):
        k = 0.25 + 0.75 * abs(r.random() * (1 - abs(i - bars / 2) / (bars / 1.6)))
        bh = max(8, h * k)
        cx = x + i * bw + bw / 2
        d.rounded_rectangle((cx - bw * 0.28, y + (h - bh) / 2, cx + bw * 0.28, y + (h + bh) / 2), radius=4, fill=color)


def player(img, x, y, w, title, sub):
    """Riquadro «lettore audio»: tasto play, onda sonora, titolo del programma."""
    h = 190
    d = ImageDraw.Draw(img)
    sh = Image.new('L', (w + 60, h + 60), 0)
    ImageDraw.Draw(sh).rounded_rectangle((30, 30, w + 30, h + 30), radius=34, fill=150)
    img.paste((0, 0, 0), (x - 30, y - 18), sh.filter(ImageFilter.GaussianBlur(16)))
    d.rounded_rectangle((x, y, x + w, y + h), radius=34, fill=IVORY)
    cx, cy, r = x + 30 + 52, y + h / 2, 52
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=CORAL)
    d.polygon([(cx - 16, cy - 26), (cx - 16, cy + 26), (cx + 28, cy)], fill=IVORY)
    tx = cx + r + 28
    d.text((tx, y + 26), title, font=font(BOLD, 34), fill=NAVY)
    d.text((tx, y + 70), sub, font=font(MED, 25), fill=(214, 82, 60))
    waveform(d, tx, y + 112, x + w - 36 - tx, 52, NAVY)
    return y + h


def scorri(d):
    fs = font(BOLD, 34); t = 'Scorri'
    tl = tw(d, t, fs); tx, ty = W - tl - 56 - 50, H - 64 - 70
    d.rounded_rectangle((tx - 24, ty - 10, tx + tl + 74, ty + 50), radius=30, fill=CORAL)
    d.text((tx, ty), t, font=fs, fill=NAVY)
    ax, ay = tx + tl + 16, ty + 22
    d.line((ax, ay, ax + 34, ay), fill=NAVY, width=5)
    d.polygon([(ax + 40, ay), (ax + 26, ay - 11), (ax + 26, ay + 11)], fill=NAVY)


# ---------- 1. copertina ----------
img = Image.new('RGB', (W, H), NAVY)
d = ImageDraw.Draw(img)
draw_arch(d, 250, 300, 760, 1060, NAVY_SOFT, 30)
draw_arch(d, 330, 390, 600, 960, CORAL, 9)
draw_logo(img, 64, 56, 0.62)
d = ImageDraw.Draw(img)
fk = font(BOLD, 28); t = T['kicker']
d.text((W - 64 - tw(d, t, fk), 74), t, font=fk, fill=CORAL)
fh = font(BOLD, 84)
y = 160
for ln in T['cover_title']:
    d.text((64, y), ln, font=fh, fill=IVORY); y += 96
fc = font(BOLD, 74); t = T['cover_pill']
pw = tw(d, t, fc) + 48
d.rounded_rectangle((52, y + 10, 52 + pw, y + 108), radius=22, fill=CORAL)
d.text((76, y + 10), t, font=fc, fill=NAVY)
p = person(1000)
paste_person(img, p, 540, H - 64 - p.height + 30)
d = ImageDraw.Draw(img)
fq = font(BOLD, 36)
qy = y + 160
for ln in wrap(d, T['cover_quote'], fq, 450):
    d.text((64, qy), ln, font=fq, fill=IVORY); qy += 50
d.text((64, qy + 10), '— Andrea Bonazzi', font=font(MED, 28), fill=CORAL)
player(img, 52, 1030, 500, T['programma'], T['data_breve'])
d = ImageDraw.Draw(img)
scorri(d)
promise_band(d, W, H)
img.save(os.path.join(HERE, '01.png'))
print('01 citazione fino a y', qy + 50, '(il lettore parte a 1030)')

# ---------- 2. la citazione ----------
img = Image.new('RGB', (W, H), NAVY)
d = ImageDraw.Draw(img)
draw_arch(d, 120, 200, 840, 1000, NAVY_SOFT, 26)
draw_logo(img, 64, 56, 0.62)
d = ImageDraw.Draw(img)
t = T['kicker']
d.text((W - 64 - tw(d, t, fk), 74), t, font=fk, fill=CORAL)
d.text((64, 160), '«', font=font(BOLD, 260), fill=CORAL)
fqb, lines, size = fit_block(d, T['quote'], BOLD, W - 150, 7, 64, 40)
y = 420
for ln in lines:
    d.text((72, y), ln, font=fqb, fill=IVORY); y += int(size * 1.3)
d.text((72, y + 24), 'Andrea Bonazzi, founder di THE LOBBY', font=font(MED, 32), fill=CORAL)
d.text((72, y + 70), T['fonte'], font=font(REG, 28), fill=(170, 180, 205))
py = player(img, 64, max(y + 150, 960), W - 128, 'Ascolta l\'intervista completa', T['dove_link'])
promise_band(d, W, H)
img.save(os.path.join(HERE, '02.png'))
print('02 fine player a y', py, 'righe citazione', len(lines), size)

# ---------- storia 1080x1920 ----------
SH_ = 1920
st = Image.new('RGB', (W, SH_), NAVY)
d = ImageDraw.Draw(st)
draw_arch(d, 200, 470, 680, 860, NAVY_SOFT, 30)
draw_logo(st, 64, 120, 0.7)
d = ImageDraw.Draw(st)
fp = font(BOLD, 34); t = T['story_pill']
pw = tw(d, t, fp) + 56
d.rounded_rectangle(((W - pw) / 2, 250, (W + pw) / 2, 312), radius=31, fill=CORAL)
d.text(((W - tw(d, t, fp)) / 2, 258), t, font=fp, fill=NAVY)
fh = font(BOLD, 80)
y = 340
for ln in T['story_title']:
    d.text(((W - tw(d, ln, fh)) / 2, y), ln, font=fh, fill=IVORY); y += 94
p = person(700)
paste_person(st, p, (W - p.width) // 2, y + 10)
d = ImageDraw.Draw(st)
# citazione su un cartiglio sotto la foto
qy0 = y + 10 + 700 - 120
fq = font(BOLD, 40)
ql = wrap(d, T['cover_quote'], fq, W - 220)
qh = 50 * len(ql) + 56
d.rounded_rectangle((70, qy0, W - 70, qy0 + qh), radius=30, fill=IVORY)
qy = qy0 + 28
for ln in ql:
    d.text(((W - tw(d, ln, fq)) / 2, qy), ln, font=fq, fill=NAVY); qy += 50
# spazio per lo sticker link
ly = qy0 + qh + 44
fl = font(BOLD, 38); t = 'Ascolta l\'intervista'
d.text(((W - tw(d, t, fl)) / 2 - 24, ly), t, font=fl, fill=IVORY)
ax = (W + tw(d, t, fl)) / 2 - 4; ay = ly + 26
d.line((ax, ay - 14, ax, ay + 14), fill=CORAL, width=5)
d.polygon([(ax - 12, ay + 10), (ax + 12, ay + 10), (ax, ay + 26)], fill=CORAL)
bx0, by0, bx1, by1 = 230, ly + 70, W - 230, ly + 70 + 170
for i in range(int(bx0) + 30, int(bx1) - 30, 34):  # bordo tratteggiato
    d.line((i, by0, i + 18, by0), fill=CORAL, width=4)
    d.line((i, by1, i + 18, by1), fill=CORAL, width=4)
for j in range(int(by0) + 30, int(by1) - 30, 34):
    d.line((bx0, j, bx0, j + 18), fill=CORAL, width=4)
    d.line((bx1, j, bx1, j + 18), fill=CORAL, width=4)
for (cx, cy, a0) in ((bx0 + 30, by0 + 30, 180), (bx1 - 30, by0 + 30, 270), (bx1 - 30, by1 - 30, 0), (bx0 + 30, by1 - 30, 90)):
    d.arc((cx - 30, cy - 30, cx + 30, cy + 30), a0, a0 + 90, fill=CORAL, width=4)
y2 = promise_list(d, W, by1 + 50, W - 160, size=34, min_size=26, row=1.38)
fb = font(BOLD, 32); t = 'thelobbyitalia.it · tutto gratis'
d.text(((W - tw(d, t, fb)) / 2, y2 + 14), t, font=fb, fill=CORAL)
st.save(os.path.join(HERE, 'storia.png'))
print('storia: riquadro link', (bx0, by0, bx1, by1), 'fine testo a y', y2 + 60)
