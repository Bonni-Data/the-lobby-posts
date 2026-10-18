#!/usr/bin/env python3
"""THE LOBBY - prepara le grafiche di un reel cinematografico (testi, logo, chiusura, musica).
Uso: python3 render_assets.py job.json cartella/
job.json: {"scenes":[{"text":"Oggi studi.","sub":"Domani tocca a te.","lines":["A) ...","B) ..."]}, ...5],
           ("lines" è facoltativo: fino a 4 risposte di un quiz, ciascuna in una pillola)
           "end":{"title":"Formati gratis.","text":"...","pill":"thelobbyitalia.it · link in bio"}}
Scrive overlay_N.png (RGBA 1080x1920), base.png (sfumature + logo), endcard.mp4 (5 s) e music.m4a."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from PIL import Image, ImageDraw
from make_pill import NAVY, CORAL, IVORY, NAVY_SOFT, BOLD, MED, font, tw, fit_block, draw_arch, draw_logo, PROMISE

W, H, FPS = 1080, 1920, 30
X0 = 80
job = json.load(open(sys.argv[1], encoding="utf-8"))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)

# base layer: legibility gradients + logo watermark
base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
px = base.load()
g = Image.new("L", (1, H))
for y in range(H):
    a = 0
    if y > 900: a = int(min(1, (y - 900) / 700) ** 1.4 * 215)
    if y < 330: a = max(a, int((1 - y / 330) ** 1.6 * 150))
    g.putpixel((0, y), a)
grad = Image.new("RGBA", (W, H), (10, 16, 34, 255)); grad.putalpha(g.resize((W, H)))
base = Image.alpha_composite(base, grad)
draw_logo(base, 70, 110, 0.85)
base.save(os.path.join(out, "base.png"))

for i, s in enumerate(job["scenes"], 1):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    tf, tl, ts = fit_block(d, s["text"], BOLD, W - 2 * X0 - 40, 3, 112, 72)
    sub = s.get("sub", "")
    sf, sl, ss = fit_block(d, sub, MED, W - 2 * X0 - 60, 2, 46, 34) if sub else (None, [], 0)
    opts = s.get("lines", [])[:4]          # risposte del quiz: una pillola per riga
    of = font(MED, 42)
    opt_lines = []
    for o in opts:
        ln = o
        while tw(d, ln, of) > W - 2 * X0 - 60 and len(ln) > 4:
            ln = ln[:-2].rstrip() + "…"
        opt_lines.append(ln)
    block = len(tl) * int(ts * 1.08) + (24 + len(sl) * int(ss * 1.3) if sl else 0) + (24 + len(opt_lines) * 86 if opt_lines else 0)
    y = 1440 - block
    d.rounded_rectangle((X0, y - 44, X0 + 120, y - 32), radius=6, fill=CORAL)
    for ln in tl:
        d.text((X0 + 3, y + 3), ln, font=tf, fill=(0, 0, 0, 120))
        d.text((X0, y), ln, font=tf, fill=IVORY)
        y += int(ts * 1.08)
    if sl:
        y += 24
        for ln in sl:
            d.text((X0, y), ln, font=sf, fill=CORAL)
            y += int(ss * 1.3)
    if opt_lines:
        y += 24
        for ln in opt_lines:
            w = tw(d, ln, of) + 52
            d.rounded_rectangle((X0, y, X0 + w, y + 70), radius=35, fill=(17, 28, 53, 215), outline=CORAL, width=3)
            d.text((X0 + 26, y + 10), ln, font=of, fill=IVORY)
            y += 86
    im.save(os.path.join(out, f"overlay_{i}.png"))

# end card: 5 s, animated
end = job["end"]
def ease(t):
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3
p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                      "-i", "-", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", os.path.join(out, "endcard.mp4")],
                     stdin=subprocess.PIPE)
for k in range(5 * FPS):
    t = k / FPS
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    a = ease(t / 0.9)
    draw_arch(d, 190, int(330 + 60 * (1 - a)), 700, 1300, NAVY_SOFT, 22)
    sc = 0.7 + 0.3 * ease(t / 0.7)
    aw, ah = int(200 * sc), int(266 * sc)
    x, y = (W - aw) // 2, 360 + (266 - ah) // 2
    draw_arch(d, x, y, aw, ah, CORAL, max(8, int(24 * sc)))
    cx, cy, r = W / 2, y + ah * 0.55, int(22 * sc)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=IVORY)
    f = font(BOLD, 104); t1 = "THE LOBBY"
    d.text(((W - tw(d, t1, f)) / 2, 670), t1, font=f, fill=IVORY)
    f2 = font(MED, 32); t2 = "WHERE INFLUENCE BEGINS."
    d.text(((W - tw(d, t2, f2)) / 2, 800), t2, font=f2, fill=CORAL)
    # le tre promesse di THE LOBBY (decisione di Andrea del 18 ottobre 2026)
    if t > 0.3:
        e = ease((t - 0.3) / 0.5)
        pf = font(BOLD, 42)
        widest = max(tw(d, s, pf) for s in PROMISE)
        px = (W - widest - 42) / 2
        _, bt, _, bb = d.textbbox((0, 0), "x", font=pf)
        for k, s in enumerate(PROMISE):
            ek = ease((t - 0.3 - 0.15 * k) / 0.45)
            py = 900 + k * 62 + int(24 * (1 - ek))
            col = tuple(int(NAVY[c] + (IVORY[c] - NAVY[c]) * ek) for c in range(3))
            dc = tuple(int(NAVY[c] + (CORAL[c] - NAVY[c]) * ek) for c in range(3))
            ccy = py + (bt + bb) / 2
            d.ellipse([px, ccy - 7, px + 14, ccy + 7], fill=dc)
            d.text((px + 42, py), s, font=pf, fill=col)
    if t > 0.9:
        b = ease((t - 0.9) / 0.5)
        tf, tl, ts = fit_block(d, end["title"], BOLD, W - 160, 2, 70, 52)
        yy = int(1130 + 40 * (1 - b))
        for ln in tl:
            col = tuple(int(NAVY[c] + (IVORY[c] - NAVY[c]) * b) for c in range(3))
            d.text(((W - tw(d, ln, tf)) / 2, yy), ln, font=tf, fill=col); yy += int(ts * 1.1)
        if end.get("text"):
            sf, sl, ss = fit_block(d, end["text"], MED, W - 220, 2, 34, 26)
            yy += 10
            for ln in sl:
                col = tuple(int(NAVY[c] + (IVORY[c] - NAVY[c]) * b * 0.9) for c in range(3))
                d.text(((W - tw(d, ln, sf)) / 2, yy), ln, font=sf, fill=col); yy += int(ss * 1.35)
    if t > 1.2:
        c = ease((t - 1.2) / 0.45)
        f3 = font(BOLD, 36); lab = end.get("pill", "thelobbyitalia.it · link in bio")
        w = tw(d, lab, f3) + 76; px0 = (W - w) / 2; py0 = 1340 + int(30 * (1 - c))
        d.rounded_rectangle((px0, py0, px0 + w, py0 + 82), radius=41, fill=tuple(int(NAVY[i] + (CORAL[i] - NAVY[i]) * c) for i in range(3)))
        d.text((px0 + 38, py0 + 17), lab, font=f3, fill=NAVY)
    p.stdin.write(img.tobytes())
p.stdin.close(); p.wait()

# music
here = os.path.dirname(os.path.abspath(__file__))
wav = os.path.join(out, "music.wav")
subprocess.run([sys.executable, os.path.join(here, "music_epic.py"), wav, str(job.get("duration", 25))], check=True)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-c:a", "aac", "-b:a", "192k", os.path.join(out, "music.m4a")], check=True)
os.remove(wav)
print("ok", out)
