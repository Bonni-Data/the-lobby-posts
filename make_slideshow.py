#!/usr/bin/env python3
"""THE LOBBY - da carosello a reel verticale (decisione del 3 novembre 2026, piano di crescita).

Perché: su Facebook i caroselli (album) della pagina arrivano a 1-9 persone, i reel a circa 200 visualizzazioni
l'uno (dati Metricool 13/10-3/11/2026). Su Instagram il reel è l'unico formato che viene proposto a chi non ci
segue. Questo script prende le slide già pronte di un carosello (01.png = copertina con il volto di Andrea) e le
monta in un reel 1080x1920 di 12-22 secondi: la copertina con il volto per prima (faccia prima), poi le slide che
entrano da destra come quando si scorre un carosello, uno zoom lento, la musica sintetizzata di THE LOBBY
(cinema/music_epic.py, nessun brano di terzi) e una barra di avanzamento. Nessuna immagine generata con l'IA.

Uso: python3 make_slideshow.py <cartella o PNG in ordine...> uscita.mp4 [--per 3.4] [--cover 2.2] [--max 8]
Esempio: python3 make_slideshow.py posts/notizie/2026-11-04/ reels/notizia-2026-11-04.mp4
Scrive anche uscita-cover.jpg (copertina 1080x1920 per videoThumbnailUrl). Stampa la durata.
Controlla SEMPRE il risultato: ffprobe (1080x1920, h264, aac) e 3 fotogrammi con Read (-ss 1, a metà, 1 s prima della fine).
"""
import glob
import os
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from make_pill import BOLD, CORAL, IVORY, NAVY, NAVY_SOFT, font, tw  # noqa: E402

W, H, FPS = 1080, 1920, 30
SY = 190            # le slide 1080x1350 stanno tra y=190 e y=1540: sopra e sotto c'è l'interfaccia di Instagram
PUSH = 0.28         # secondi del passaggio da una slide all'altra


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def canvas():
    bg = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(bg)
    f = font(BOLD, 34)
    t = "thelobbyitalia.it · link in bio"
    d.text(((W - tw(d, t, f)) / 2, SY + 1350 + 70), t, font=f, fill=CORAL)
    f2 = font(BOLD, 30)
    t2 = "Segui @thelobbyitalia"
    d.text(((W - tw(d, t2, f2)) / 2, SY + 1350 + 125), t2, font=f2, fill=IVORY)
    return bg


def fit(img):
    img = img.convert("RGB")
    if img.size != (1080, 1350):
        r = min(1080 / img.width, 1350 / img.height)
        img = img.resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
        pad = Image.new("RGB", (1080, 1350), NAVY)
        pad.paste(img, ((1080 - img.width) // 2, (1350 - img.height) // 2))
        img = pad
    return img


def zoomed(img, z):
    if z <= 1.0005:
        return img
    w, h = int(1080 * z), int(1350 * z)
    big = img.resize((w, h), Image.BILINEAR)
    x, y = (w - 1080) // 2, (h - 1350) // 2
    return big.crop((x, y, x + 1080, y + 1350))


def progress(d, idx, n, a):
    """Barra in alto: un segmento per slide, come le storie."""
    gap, x0, x1, y = 10, 60, W - 60, SY - 46
    seg = (x1 - x0 - gap * (n - 1)) / n
    for i in range(n):
        sx = x0 + i * (seg + gap)
        d.rounded_rectangle((sx, y, sx + seg, y + 8), radius=4, fill=NAVY_SOFT)
        fill = 1.0 if i < idx else (a if i == idx else 0.0)
        if fill > 0:
            d.rounded_rectangle((sx, y, sx + max(8, seg * fill), y + 8), radius=4, fill=CORAL)


def main(argv):
    opts, clean, it = {}, [], iter(argv)
    for a in it:
        if a.startswith("--"):
            opts[a[2:]] = float(next(it))
        else:
            clean.append(a)
    *inputs, out = clean
    files = []
    for p in inputs:
        files += sorted(glob.glob(os.path.join(p, "*.png"))) if os.path.isdir(p) else [p]
    files = [f for f in files if os.path.basename(f)[0].isdigit()] or files
    mx = int(opts.get("max", 8))
    if len(files) > mx:   # si tengono la copertina e l'ultima slide (le tre promesse e l'invito)
        files = files[: mx - 1] + files[-1:]
    if not files:
        sys.exit("nessuna slide trovata")
    slides = [fit(Image.open(f)) for f in files]
    # con poche slide ognuna resta di più (una grafica con 3 opportunità va letta): 2 slide -> 6 s, 6 slide -> 3,4 s
    per = opts.get("per", max(3.4, min(6.0, 12.0 / max(1, len(slides) - 1))))
    cover_t = opts.get("cover", 2.2)
    times = [cover_t] + [per] * (len(slides) - 1)
    total = sum(times) + 0.6     # piccola coda sull'ultima slide
    base = canvas()
    tmp = out[:-4] + ".noaudio.mp4"
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                            "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    starts = [sum(times[:i]) for i in range(len(times))]
    cover = None
    for f in range(int(total * FPS)):
        t = f / FPS
        idx = max(i for i, s in enumerate(starts) if s <= t)
        lt = t - starts[idx]
        dur = times[idx] if idx < len(times) - 1 else times[idx] + 0.6
        frame = base.copy()
        cur = zoomed(slides[idx], 1.0 + 0.035 * (lt / dur))
        if idx > 0 and lt < PUSH:
            # la slide nuova entra da destra e spinge fuori la precedente (come scorrere un carosello)
            a = ease(lt / PUSH)
            prev = zoomed(slides[idx - 1], 1.035)
            frame.paste(prev, (int(-W * a), SY))
            frame.paste(cur, (int(W * (1 - a)), SY))
        else:
            frame.paste(cur, (0, SY))
        progress(ImageDraw.Draw(frame), idx, len(slides), min(1.0, lt / dur))
        if cover is None and t >= 0.5:
            cover = frame.copy()
        enc.stdin.write(frame.tobytes())
    enc.stdin.close()
    enc.wait()
    wav = out[:-4] + ".wav"
    subprocess.run([sys.executable, os.path.join(HERE, "cinema", "music_epic.py"), wav, str(int(total) + 1)], check=True,
                   stdout=subprocess.DEVNULL)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-af", f"afade=t=out:st={total - 1.2:.2f}:d=1.2",
                    "-t", f"{total:.2f}", "-movflags", "+faststart", out], check=True)
    os.remove(wav)
    os.remove(tmp)
    (cover or base).save(out[:-4] + "-cover.jpg", "JPEG", quality=92)
    print(f"ok {out} ({len(slides)} slide, {total:.1f} s) copertina {out[:-4]}-cover.jpg")


if __name__ == "__main__":
    main(sys.argv[1:])
