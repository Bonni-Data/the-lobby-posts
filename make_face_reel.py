#!/usr/bin/env python3
"""THE LOBBY - reel «faccia prima» (decisione di Andrea del 24 ottobre 2026), 1080x1920, 30 fps, H.264 + AAC.

Due modi:
- "video": il video verticale registrato da Andrea; sopra: le 1-2 parole del gancio nei primi 3 secondi, logo,
  nome, sottotitoli, fascia con le tre promesse; in fondo 2,5 s di chiusura. Audio: la voce di Andrea.
- "photo": quando il video non c'è. La foto scontornata di Andrea con zoom lento, le parole che entrano,
  il testo a schermo a blocchi e la stessa chiusura. Audio: musica sintetizzata (cinema/music_epic.py), nessun diritto.

Uso: python3 make_face_reel.py data.json uscita.mp4      (scrive anche uscita-cover.jpg)
data.json:
{
  "video": "volto/video/2026-10-28-mercoledi.mp4",   # se c'è, modo video; altrimenti serve "face"
  "face": "volto/libreria/sorpreso-1.png",          # foto scontornata (modo photo, e copertina)
  "words": ["NON LO", "SAPEVI"],                    # il gancio: 1-2 parole
  "kicker": "LO SAPEVI?",
  "captions": [{"t": 0.0, "e": 1.6, "text": "Il sindaco non firma"}],   # facoltativo: sottotitoli con i tempi
  "script": "testo detto nel video",               # in alternativa: sottotitoli a blocchi di 3-5 parole,
                                                    # distribuiti sulla durata (tempi approssimati)
  "duration": 14                                    # solo modo photo: secondi prima della chiusura
}
"""
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter

from make_face import load_face, sticker, words_block
from make_pill import BAND, BOLD, CORAL, IVORY, MED, NAVY, NAVY_SOFT, PROMISE, draw_arch, draw_logo, fit_block, font, promise_band, promise_list, tw

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
END = 2.5
STRIP_Y = 1480          # fascia promesse: sopra la zona coperta dall'interfaccia di Instagram
CAP_Y = 1180            # sottotitoli


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def chunks_from_script(script, dur, start=0.4):
    words = script.split()
    out, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= 4 or w.endswith((".", ",", "?", "!", ":")) and len(cur) >= 2:
            out.append(" ".join(cur))
            cur = []
    if cur:
        out.append(" ".join(cur))
    total = sum(len(c) for c in out) or 1
    t, caps = start, []
    span = max(dur - start - 0.2, 1)
    for c in out:
        d = span * len(c) / total
        caps.append({"t": t, "e": t + d, "text": c})
        t += d
    return caps


def caption_layer(text):
    layer = Image.new("RGBA", (W, 260), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f, lines, s = fit_block(d, text.upper(), BOLD, W - 160, 2, 64, 44)
    y = 10
    for ln in lines:
        x = (W - tw(d, ln, f)) / 2
        d.text((x, y), ln, font=f, fill=IVORY, stroke_width=8, stroke_fill=NAVY)
        y += int(s * 1.15)
    return layer


def hook_layer(data, x0=64, x1=W - 64, y=300, align="left"):
    layer = Image.new("RGBA", (W, 700), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    yy = 0
    if data.get("kicker"):
        kf = font(BOLD, 28)
        k = data["kicker"].upper()
        kw = tw(d, k, kf) + 40
        d.rounded_rectangle((x0, yy, x0 + kw, yy + 52), radius=26, fill=CORAL)
        d.text((x0 + 20, yy + 8), k, font=kf, fill=NAVY)
        yy += 84
    words_block(d, [w.upper() for w in data["words"][:2]], x0, x1, yy, align, 170)
    return layer


def chrome_layer(name=True):
    """Logo in alto, nome, fascia delle promesse: restano per tutto il video."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_logo(layer, 64, 150, 0.72)
    d = ImageDraw.Draw(layer)
    sub = Image.new("RGBA", (W, BAND), (0, 0, 0, 0))
    promise_band(ImageDraw.Draw(sub), W, BAND)
    layer.alpha_composite(sub, (0, STRIP_Y))
    if name:
        nf = font(BOLD, 30)
        nw = tw(d, "Andrea Bonazzi", nf)
        d.rounded_rectangle((46, STRIP_Y - 72, 46 + nw + 36, STRIP_Y - 18), radius=27, fill=NAVY)
        d.text((64, STRIP_Y - 70), "Andrea Bonazzi", font=nf, fill=IVORY)
    return layer


def endcard():
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    d = ImageDraw.Draw(img)
    draw_arch(d, 375, 330, 330, 430, NAVY_SOFT, 22)
    draw_arch(d, 470, 430, 140, 270, CORAL, 10)
    d.ellipse([528, 590, 552, 614], fill=IVORY)
    f = font(BOLD, 86)
    d.text(((W - tw(d, "THE LOBBY", f)) / 2, 820), "THE LOBBY", font=f, fill=IVORY)
    y = promise_list(d, W, 980, W - 160, size=42, min_size=30)
    lf = font(BOLD, 36)
    label = "thelobbyitalia.it · link in bio"
    lw = tw(d, label, lf) + 70
    d.rounded_rectangle(((W - lw) / 2, y + 50, (W + lw) / 2, y + 132), radius=41, fill=CORAL)
    d.text(((W - lw) / 2 + 35, y + 66), label, font=lf, fill=NAVY)
    g = font(MED, 30)
    t = "È tutto gratis"
    d.text(((W - tw(d, t, g)) / 2, y + 170), t, font=g, fill=IVORY)
    return img


def photo_scene(face_path):
    """Sfondo con arco + Andrea scontornato, a grandezza piena: lo zoom lo fa il montaggio."""
    bg = Image.new("RGBA", (W, H), NAVY + (255,))
    d = ImageDraw.Draw(bg)
    draw_arch(d, 260, 640, 760, 1000, NAVY_SOFT, 34)
    draw_arch(d, 340, 740, 600, 900, CORAL, 12)
    face, (fx, fy, fw, fh) = load_face(face_path)
    s = 420 / fh
    s = max(s, (H - 700) / face.height)
    face = face.resize((int(face.width * s), int(face.height * s)), Image.LANCZOS)
    fx, fy, fw, fh = fx * s, fy * s, fw * s, fh * s
    x = int(W * 0.62 - (fx + fw / 2))
    y = int(800 - fy)              # il viso sotto le parole del gancio; il busto può uscire dal fondo
    st, pad = sticker(face, 12)
    bg.alpha_composite(st, (x - pad, y - pad))
    return bg


def run(data, out):
    video = data.get("video")
    chrome = chrome_layer()
    hook = hook_layer(data)
    end = endcard().convert("RGB")
    if video:
        probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                               capture_output=True, text=True, check=True)
        dur = float(probe.stdout.strip())
    else:
        dur = float(data.get("duration", 12))
        scene = photo_scene(data["face"])
    caps = data.get("captions") or (chunks_from_script(data["script"], dur) if data.get("script") else [])
    cap_layers = [(c["t"], c["e"], caption_layer(c["text"])) for c in caps]
    total = dur + END
    n = int(total * FPS)
    tmp = out[:-4] + ".noaudio.mp4"
    enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                            "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    dec = None
    if video:
        dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", video, "-vf",
                                f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
                                "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    last = None
    cover = None
    for i in range(n):
        t = i / FPS
        if t >= dur:
            # chiusura: dissolvenza veloce dall'ultimo fotogramma
            a = ease((t - dur) / 0.35)
            frame = Image.blend(last, end, a) if last is not None and a < 1 else end
            enc.stdin.write(frame.tobytes())
            continue
        if dec:
            raw = dec.stdout.read(W * H * 3)
            if len(raw) < W * H * 3:
                raw = last.tobytes() if last is not None else bytes(W * H * 3)
            base = Image.frombytes("RGB", (W, H), raw).convert("RGBA")
            # velo scuro in alto e in basso per leggere i testi
            base.alpha_composite(veil())
        else:
            z = 1.08 - 0.08 * ease(t / 1.2) + 0.03 * (t / dur)   # entra con uno zoom, poi si avvicina piano
            sw, sh = int(W * z), int(H * z)
            sc = scene.resize((sw, sh), Image.BILINEAR)
            base = sc.crop(((sw - W) // 2, (sh - H) // 2 + int((sh - H) * 0.2), (sw - W) // 2 + W, (sh - H) // 2 + int((sh - H) * 0.2) + H))
        base.alpha_composite(chrome)
        # gancio: entra da sinistra nei primi 0,4 s; nel video resta 3 s, nella foto per tutto il tempo
        keep = 3.0 if video else dur
        if t < keep:
            a = ease(t / 0.4)
            hx = int(-80 * (1 - a))
            fade = 1.0 if t < keep - 0.3 else max(0.0, (keep - t) / 0.3)
            h2 = hook.copy()
            if a < 1 or fade < 1:
                h2.putalpha(h2.split()[-1].point(lambda v: int(v * min(a, fade))))
            base.alpha_composite(h2, (hx, 300))
        for (t0, t1, lay) in cap_layers:
            if t0 <= t < t1:
                base.alpha_composite(lay, (0, CAP_Y))
                break
        frame = base.convert("RGB")
        if cover is None and t >= (0.6 if video else 1.3):
            cover = frame.copy()
        last = frame
        enc.stdin.write(frame.tobytes())
    enc.stdin.close()
    enc.wait()
    if dec:
        dec.stdout.close()
        dec.wait()
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-i", video, "-map", "0:v", "-map", "1:a?",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-af", f"apad=pad_dur={END}", "-t", f"{total:.2f}", out], check=True)
    else:
        wav = out[:-4] + ".wav"
        subprocess.run([sys.executable, os.path.join(HERE, "cinema", "music_epic.py"), wav, str(int(total) + 1)], check=True)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-i", wav, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-t", f"{total:.2f}", out], check=True)
        os.remove(wav)
    os.remove(tmp)
    (cover or end).save(out[:-4] + "-cover.jpg", "JPEG", quality=92)
    return out


_VEIL = None


def veil():
    global _VEIL
    if _VEIL is None:
        v = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(v)
        for y in range(H):
            if y < 820:
                a = int(150 * (1 - y / 820) ** 1.2)
            elif y > 1100:
                a = int(170 * ((y - 1100) / (H - 1100)) ** 1.3)
            else:
                a = 0
            d.line([(0, y), (W, y)], fill=a)
        _VEIL = Image.new("RGBA", (W, H), NAVY + (0,))
        _VEIL.putalpha(v)
    return _VEIL


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as fh:
        print("ok", run(json.load(fh), sys.argv[2]))
