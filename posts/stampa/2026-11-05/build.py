import sys
sys.path.insert(0, '/home/claude/the-lobby-posts')
from PIL import Image, ImageDraw, ImageFilter
from make_pill import BOLD, MED, REG, CORAL, IVORY, NAVY, NAVY_SOFT, font, tw, wrap, draw_arch, draw_logo, promise_band
A = '/mnt/user-data/attachments/dfe1d4e0-496e-5631-b96b-85b7e15b38f2/'
W, H = 1080, 1350

# ---------- 1. copertina: foto con lo schermo pulito ----------
ph = Image.open(A + 'bc109736-image.jpg').convert('RGB')
# schermo nuovo (al posto del testo illeggibile)
SW, SH = 1092, 712
scr = Image.new('RGB', (SW, SH), NAVY)
d = ImageDraw.Draw(scr)
draw_arch(d, SW // 2 - 70, 40, 140, 190, CORAL, 7)
f = font(BOLD, 52); t = 'THE LOBBY'
d.text(((SW - tw(d, t, f)) / 2, 250), t, font=f, fill=IVORY)
fq = font(BOLD, 74)
lines = wrap(d, '«Proviamo a cambiare le regole del gioco»', fq, SW - 120)
y = 340
for ln in lines:
    d.text(((SW - tw(d, ln, fq)) / 2, y), ln, font=fq, fill=IVORY); y += 90
fb = font(BOLD, 40); t = 'thelobbyitalia.it'
bw = tw(d, t, fb) + 80
d.rounded_rectangle(((SW - bw) / 2, y + 30, (SW + bw) / 2, y + 110), radius=40, fill=CORAL)
d.text(((SW - tw(d, t, fb)) / 2, y + 45), t, font=fb, fill=NAVY)
# angoli dello schermo nella foto originale (alto-sx, basso-sx, basso-dx, alto-dx)
quad = (299, 659, 300, 891, 659, 891, 659, 658)
x0, y0, x1, y1 = 299, 658, 660, 892
warped = scr.transform((x1 - x0, y1 - y0), Image.QUAD,
                       tuple(v for i, v in enumerate(quad)), Image.BICUBIC) if False else None
# lo schermo è quasi frontale: basta ridimensionare e incollare nell'area interna
ph.paste(scr.resize((x1 - x0, y1 - y0), Image.LANCZOS), (x0, y0))

s = W / ph.width
big = ph.resize((W, int(ph.height * s)), Image.LANCZOS)
OFF = 215
cov = Image.new('RGB', (W, H))
# parete estesa verso l'alto: colore della prima riga, colonna per colonna
top = big.crop((0, 0, W, 6)).resize((W, 1)).resize((W, OFF))
cov.paste(top.filter(ImageFilter.GaussianBlur(4)), (0, 0))
cov.paste(big, (0, OFF))
d = ImageDraw.Draw(cov)
fk = font(BOLD, 30); t = 'RASSEGNA STAMPA · GIOVEDÌ 5 NOVEMBRE'
d.text(((W - tw(d, t, fk)) / 2, 62), t, font=fk, fill=(214, 82, 60))
fh = font(BOLD, 88); t = 'Ne parla Il Giorno'
d.text(((W - tw(d, t, fh)) / 2, 100), t, font=fh, fill=NAVY)
# «Scorri»
fs = font(BOLD, 34); t = 'Scorri'
tl = tw(d, t, fs); tx, ty = W - tl - 56 - 50, H - 64 - 70
d.rounded_rectangle((tx - 24, ty - 10, tx + tl + 74, ty + 50), radius=30, fill=NAVY)
d.text((tx, ty), t, font=fs, fill=IVORY)
ax, ay = tx + tl + 16, ty + 22
d.line((ax, ay, ax + 34, ay), fill=CORAL, width=5)
d.polygon([(ax + 40, ay), (ax + 26, ay - 11), (ax + 26, ay + 11)], fill=CORAL)
promise_band(d, W, H)
cov.save('01.png')

# ---------- 2. l'articolo ----------
img = Image.new('RGB', (W, H), NAVY)
d = ImageDraw.Draw(img)
draw_arch(d, 120, 180, 840, 1000, NAVY_SOFT, 26)
draw_logo(img, 64, 60, 0.62)
d = ImageDraw.Draw(img)
fk = font(BOLD, 30); t = 'IL GIORNO · 5 NOVEMBRE 2026'
d.text((W - 64 - tw(d, t, fk), 78), t, font=fk, fill=CORAL)
sc = Image.open(A + 'a3dfed10-image.png').convert('RGB')
r = sc.width / 924
sc = sc.crop((0, int(285 * r), sc.width, int(955 * r)))
cw = 900; ch = int(sc.height * cw / sc.width)
sc = sc.resize((cw, ch), Image.LANCZOS)
cx, cy = (W - cw) // 2, 215
sh = Image.new('L', (cw + 80, ch + 80), 0)
ImageDraw.Draw(sh).rounded_rectangle((40, 40, cw + 40, ch + 40), radius=28, fill=170)
sh = sh.filter(ImageFilter.GaussianBlur(20))
img.paste((0, 0, 0), (cx - 40, cy - 25), sh)
m = Image.new('L', (cw, ch), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, cw - 1, ch - 1), radius=28, fill=255)
img.paste(sc, (cx, cy), m)
d = ImageDraw.Draw(img)
y = cy + ch + 60
fq = font(BOLD, 50)
for ln in wrap(d, '«La politica non è una cosa per pochi: è un mestiere che si impara.»', fq, W - 160):
    d.text((80, y), ln, font=fq, fill=IVORY); y += 66
d.text((80, y + 14), 'Andrea Bonazzi, founder di THE LOBBY', font=font(MED, 30), fill=CORAL)
promise_band(d, W, H)
img.save('02.png')
print('ok', cov.size, img.size, 'fine testo slide 2 a y', y + 50)
