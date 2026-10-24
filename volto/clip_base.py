#!/usr/bin/env python3
"""THE LOBBY - spezzone «base» per le intro video dei reel (decisione di Andrea del 24 ottobre 2026).

Prende 3 secondi di un video verticale di Andrea, toglie lo sfondo fotogramma per fotogramma e lo mette davanti agli
archi di THE LOBBY, con il bordo avorio delle copertine. Niente testi e niente audio: le parole del gancio, il logo,
il nome, la fascia delle promesse e la musica li aggiunge make_face_reel.clip_intro() a ogni reel.

Uso: python3 volto/clip_base.py video.mov inizio_secondi uscita.mp4 [--hdr]
  --hdr: per i video dell'iPhone in HDR (colori un po' più vivi dopo la conversione)

Regole (vincolanti):
- L'audio del video originale non entra MAI: il file in uscita è muto.
- Sceglie spezzoni in cui Andrea si muove poco: con le mani veloci lo sfondo può restare attaccato alla sagoma.
- Dopo averlo creato, CONTROLLA TUTTI I FOTOGRAMMI (python3 volto/clip_base.py --foglio uscita.mp4 fa i fogli di
  controllo) e scarta lo spezzone se resta anche una sola traccia dello sfondo originale (scritte, simboli, bandiere).
- Mai spezzoni che rivelano cariche politiche, partiti o persone terze riconoscibili.
"""
import os
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
from scontorna import predict, solidify  # noqa: E402
from make_pill import CORAL, IVORY, NAVY, NAVY_SOFT, draw_arch  # noqa: E402
from PIL import ImageDraw  # noqa: E402

W, H, FPS = 1080, 1920, 30
STRIP_Y = 1480
SCALE, PX, PY = 0.80, 290, 220      # Andrea a destra; a sinistra resta la colonna per le parole del gancio
DUR = 3.0


def mask(frame):
    """Serve l'accordo di due modelli: dove solo uno vede la persona (scritte dietro, mani mosse) si toglie."""
    m = predict(frame, "isnet-general-use", 1024, (0.5, 0.5, 0.5), (1.0, 1.0, 1.0))
    m = np.clip((m - 0.18) / 0.64, 0, 1)
    hm = predict(frame, "u2net_human_seg", 320, (0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
    m = m * cv2.dilate((hm > 0.5).astype(np.uint8), np.ones((9, 9), np.uint8))
    m = solidify(m, erode=15)
    m = cv2.erode(m.astype(np.float32), np.ones((3, 3), np.uint8))
    b = (m > 0.5).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(b, 8)
    if n > 2:
        keep = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        m = m * cv2.dilate((lab == keep).astype(np.uint8), np.ones((11, 11), np.uint8))
    return m


def background():
    bg = Image.new("RGBA", (W, H), NAVY + (255,))
    d = ImageDraw.Draw(bg)
    cx = int(W * 0.66)
    draw_arch(d, cx - 330, 470, 660, STRIP_Y - 470 + 40, NAVY_SOFT, 34)
    draw_arch(d, cx - 255, 570, 510, STRIP_Y - 570, CORAL, 12)
    return bg


def make(src, start, out, hdr=False):
    vf = "fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
    if hdr:
        vf += ",eq=saturation=1.1:contrast=1.03"
    dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", f"{start:.2f}", "-t", f"{DUR + 0.2:.2f}", "-i", src,
                            "-an", "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                            "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    bg = background()
    sw, sh = int(W * SCALE), int(H * SCALE)
    for i in range(int(DUR * FPS)):
        raw = dec.stdout.read(W * H * 3)
        if len(raw) < W * H * 3:
            break
        fr = Image.frombytes("RGB", (W, H), raw)
        m = mask(fr)   # ogni fotogramma, senza mescolarlo col precedente: niente aloni di sfondo quando si muove
        person = fr.resize((sw, sh), Image.LANCZOS).convert("RGBA")
        a = Image.fromarray((m * 255).astype("uint8")).resize((sw, sh), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.8))
        person.putalpha(a)
        rim = a.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(1.2))
        shadow = rim.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.45))
        frame = bg.copy()
        sl = Image.new("RGBA", (sw, sh), (0, 0, 0, 0)); sl.putalpha(shadow)
        frame.alpha_composite(sl, (PX + 10, PY + 14))
        rl = Image.new("RGBA", (sw, sh), IVORY + (0,)); rl.putalpha(rim)
        frame.alpha_composite(rl, (PX, PY))
        frame.alpha_composite(person, (PX, PY))
        enc.stdin.write(frame.convert("RGB").tobytes())
    enc.stdin.close(); enc.wait()
    dec.stdout.close(); dec.wait()
    print("ok", out)


def sheets(path):
    """Fogli di controllo: tutti i fotogrammi, ritagliati sulla sagoma, per cercare tracce dello sfondo originale."""
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    fr = []
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        fr.append(Image.frombytes("RGB", (W, H), b).crop((250, 380, 1080, 1560)).resize((360, 512)))
    base = os.path.splitext(path)[0]
    for k in range(0, len(fr), 30):
        part = fr[k:k + 30]
        s = Image.new("RGB", (360 * 6, 512 * ((len(part) + 5) // 6)), "white")
        for i, t in enumerate(part):
            s.paste(t, ((i % 6) * 360, (i // 6) * 512))
        s.save(f"{base}-controllo-{k // 30 + 1}.jpg", quality=85)
        print("foglio", f"{base}-controllo-{k // 30 + 1}.jpg")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--foglio":
        sheets(a[1])
    else:
        hdr = "--hdr" in a
        a = [x for x in a if x != "--hdr"]
        make(a[0], float(a[1]), a[2], hdr)
