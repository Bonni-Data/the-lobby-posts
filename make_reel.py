#!/usr/bin/env python3
"""THE LOBBY - reel Instagram/Facebook (video 1080x1920, 30 fps, H.264 + AAC) con copertina.

Uso: python3 make_reel.py data.json uscita.mp4
Scrive anche uscita-cover.jpg (copertina per Instagram, testo al centro così regge il ritaglio 4:5 della griglia).

La musica è generata qui dentro (accordi, cassa e charleston sintetizzati): nessun brano di terzi, nessun diritto da pagare.

data.json, tre formati:
1) "fact"  (Lo sapevi?) e 3) "news" (Attualità in 30 secondi):
{
  "format": "fact",
  "kicker": "LO SAPEVI?",                         # max ~22 caratteri
  "hook": "Il sindaco non firma i permessi.",      # 1a scena, max ~60 caratteri: deve fermare il pollice
  "points": [                                      # da 2 a 4 scene
    {"title": "Chi firma, allora?", "text": "Gli uffici comunali: dirigenti e funzionari."}
  ],
  "payoff": "La politica dà la direzione, gli uffici gestiscono.",   # facoltativa, max ~80
  "cta": "La lezione completa è gratis"            # facoltativa
}
2) "quiz" (Quiz lampo):
{
  "format": "quiz",
  "kicker": "QUIZ LAMPO",
  "hook": "Solo 3 persone su 10 lo sanno",          # facoltativo, deve essere vero o generico (niente statistiche inventate)
  "question": "Chi approva il bilancio del Comune?",
  "options": ["Il sindaco", "Il consiglio comunale", "Il prefetto"],
  "correct": 1,
  "explain": "Lo approva il consiglio comunale, su proposta della giunta.",
  "cta": "Mettiti alla prova con il quiz completo"
}
Durata: 18-30 secondi. Testi brevi: una scena si legge in 2-3 secondi.
"""
import json
import math
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw

from make_pill import NAVY, CORAL, IVORY, NAVY_SOFT, BOLD, MED, REG, font, tw, wrap, fit_block, draw_arch, draw_logo, promise_list

RW, RH, FPS = 1080, 1920, 30
SR = 44100
X0, X1 = 80, 940          # safe area: Instagram covers the right edge (buttons) and the bottom (caption)
TOP, BOTTOM = 420, 1440
MUTE = (170, 178, 196)
FFMPEG = "ffmpeg"


# ---------------------------------------------------------------- drawing helpers

def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def layer():
    return Image.new("RGBA", (RW, RH), (0, 0, 0, 0))


def text_block(d, text, path, start, minimum, max_lines, width, y, color, center=False, lh=1.15):
    f, lines, size = fit_block(d, text, path, width, max_lines, start, minimum)
    for ln in lines:
        x = (X0 + (X1 - X0 - tw(d, ln, f)) / 2) if center else X0
        d.text((x, y), ln, font=f, fill=color)
        y += int(size * lh)
    return y


def pill(d, x, y, text, fill=CORAL, ink=NAVY, size=34, center=False):
    f = font(BOLD, size)
    w = tw(d, text, f) + 52
    if center:
        x = (RW - w) / 2
    d.rounded_rectangle((x, y, x + w, y + size + 30), radius=(size + 30) // 2, fill=fill)
    d.text((x + 26, y + 8), text, font=f, fill=ink)
    return y + size + 30


def background(t):
    img = Image.new("RGB", (RW, RH), NAVY)
    d = ImageDraw.Draw(img)
    drift = math.sin(t * 0.35) * 30
    draw_arch(d, 470 + drift, 980 - drift * 0.5, 760, 1500, NAVY_SOFT, 34)
    draw_arch(d, -260 - drift * 0.6, 1300 + drift * 0.3, 560, 1100, NAVY_SOFT, 22)
    return img


def chrome(img, progress, n_scenes, idx):
    draw_logo(img, X0, 150, 0.85)
    d = ImageDraw.Draw(img)
    # story-style progress: one segment per scene
    gap, y = 10, 290
    seg = (X1 - X0 - gap * (n_scenes - 1)) / n_scenes
    for k in range(n_scenes):
        x = X0 + k * (seg + gap)
        d.rounded_rectangle((x, y, x + seg, y + 8), radius=4, fill=NAVY_SOFT)
        fill = 1.0 if k < idx else (progress if k == idx else 0.0)
        if fill > 0:
            d.rounded_rectangle((x, y, x + max(8, seg * fill), y + 8), radius=4, fill=CORAL)


# ---------------------------------------------------------------- scenes
# Each scene: dict(kind, dur, draw(d, t) -> None on an RGBA layer, sfx)

def scene_hook(kicker, hook, dur=2.6):
    def draw(lay, t):
        d = ImageDraw.Draw(lay)
        f, lines, size = fit_block(d, hook, BOLD, X1 - X0, 5, 112, 64)
        y = 860 - (80 + len(lines) * int(size * 1.1)) // 2
        y = pill(d, X0, y, kicker.upper()) + 50
        text_block(d, hook, BOLD, 112, 64, 5, X1 - X0, y, IVORY, lh=1.1)
    return {"dur": dur, "draw": draw, "sfx": "whoosh"}


def scene_point(i, title, text, dur):
    def draw(lay, t):
        d = ImageDraw.Draw(lay)
        y = 600
        d.text((X0, y), f"{i:02d}", font=font(BOLD, 150), fill=CORAL)
        y += 200
        y = text_block(d, title, BOLD, 80, 52, 3, X1 - X0, y, IVORY, lh=1.12) + 34
        d.line([X0, y, X0 + 120, y], fill=CORAL, width=7)
        y += 46
        text_block(d, text, MED, 56, 38, 6, X1 - X0, y, IVORY, lh=1.36)
    return {"dur": dur, "draw": draw, "sfx": "whoosh"}


def scene_payoff(text, dur=3.0):
    def draw(lay, t):
        d = ImageDraw.Draw(lay)
        f, lines, size = fit_block(d, text, BOLD, X1 - X0, 5, 76, 48)
        y = 900 - len(lines) * int(size * 1.15) // 2
        d.rectangle((X0, y - 10, X0 + 10, y + len(lines) * int(size * 1.15)), fill=CORAL)
        for ln in lines:
            d.text((X0 + 44, y), ln, font=f, fill=IVORY)
            y += int(size * 1.15)
    return {"dur": dur, "draw": draw, "sfx": "whoosh"}


def scene_cta(cta, dur=4.2):
    def draw(lay, t):
        d = ImageDraw.Draw(lay)
        draw_arch(d, 430, 420, 220, 290, CORAL, 12)
        d.ellipse([528, 562, 552, 586], fill=IVORY)
        y = 780
        y = text_block(d, cta, BOLD, 72, 48, 2, X1 - X0, y, IVORY, center=True, lh=1.12) + 44
        # le tre promesse di THE LOBBY (decisione di Andrea del 18 ottobre 2026)
        y = promise_list(d, RW, y, X1 - X0, size=44, min_size=32) + 26
        y = pill(d, 0, y, "Gratis · link in bio", size=40, center=True) + 30
        sf = font(MED, 34)
        u = "thelobbyitalia.it"
        d.text(((RW - tw(d, u, sf)) / 2, y), u, font=sf, fill=IVORY)
    return {"dur": dur, "draw": draw, "sfx": "chime"}


LETTERS = "ABCD"


def quiz_scenes(q):
    opts, correct = q["options"][:4], int(q["correct"])

    def draw_question(d, y):
        return text_block(d, q["question"], BOLD, 78, 50, 4, X1 - X0, y, IVORY, lh=1.12)

    def draw_options(d, y, reveal=False, appear=1.0):
        f = font(MED, 44)
        for k, o in enumerate(opts):
            if not reveal and k / len(opts) > appear:
                break
            box_h = 118
            right = reveal and k == correct
            dim = reveal and k != correct
            fill = CORAL if right else (NAVY_SOFT if not dim else (24, 35, 62))
            d.rounded_rectangle((X0, y, X1, y + box_h), radius=26, fill=fill)
            ink = NAVY if right else (IVORY if not dim else MUTE)
            d.text((X0 + 34, y + 30), LETTERS[k], font=font(BOLD, 46), fill=ink if right else CORAL)
            lines = wrap(d, o, f, X1 - X0 - 150)[:2]
            ly = y + (box_h - len(lines) * 50) / 2
            for ln in lines:
                d.text((X0 + 104, ly), ln, font=f, fill=ink)
                ly += 50
            y += box_h + 22
        return y

    def s_question(lay, t):
        d = ImageDraw.Draw(lay)
        y = pill(d, X0, 600, "DOMANDA") + 44
        y = draw_question(d, y) + 50
        draw_options(d, y, appear=min(1.0, t / 1.6 + 0.01))

    def s_count(lay, t):
        d = ImageDraw.Draw(lay)
        y = pill(d, X0, 600, "DOMANDA") + 44
        y = draw_question(d, y) + 50
        y = draw_options(d, y) + 30
        n = 3 - int(min(2.999, t))
        f = font(BOLD, 120)
        s = str(n)
        cx = RW / 2
        r = 86
        d.ellipse((cx - r, y, cx + r, y + 2 * r), outline=CORAL, width=10)
        d.text((cx - tw(d, s, f) / 2, y + 16), s, font=f, fill=IVORY)

    def s_reveal(lay, t):
        d = ImageDraw.Draw(lay)
        y = pill(d, X0, 560, "RISPOSTA") + 44
        y = draw_question(d, y) + 40
        y = draw_options(d, y, reveal=True) + 30
        if q.get("explain"):
            text_block(d, q["explain"], MED, 46, 32, 4, X1 - X0, y, IVORY, lh=1.36)

    return [
        {"dur": 3.6, "draw": s_question, "sfx": "whoosh"},
        {"dur": 3.0, "draw": s_count, "sfx": "ticks", "static_in": True},
        {"dur": 4.6, "draw": s_reveal, "sfx": "ding"},
    ]


def build(data):
    fmt = data.get("format", "fact")
    kicker = data.get("kicker") or {"fact": "LO SAPEVI?", "quiz": "QUIZ LAMPO", "news": "ATTUALITÀ IN 30 SECONDI"}[fmt]
    scenes = []
    if fmt == "quiz":
        scenes.append(scene_hook(kicker, data.get("hook") or "Lo sai o tiri a indovinare?", 2.4))
        scenes += quiz_scenes(data)
        scenes.append(scene_cta(data.get("cta") or "Mettiti alla prova con il quiz completo"))
    else:
        scenes.append(scene_hook(kicker, data["hook"]))
        for i, p in enumerate(data["points"][:4], 1):
            words = len((p.get("title", "") + " " + p.get("text", "")).split())
            scenes.append(scene_point(i, p["title"], p["text"], max(3.0, min(5.0, 1.4 + words * 0.17))))
        if data.get("payoff"):
            scenes.append(scene_payoff(data["payoff"]))
        scenes.append(scene_cta(data.get("cta") or "La lezione completa è gratis"))
    return scenes


# ---------------------------------------------------------------- audio (synthesised, royalty free)

def synth_music(total, cuts, sfx):
    n = int(total * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    bpm = 96
    beat = 60 / bpm
    # chords: Am - F - C - G, one per bar (4 beats)
    roots = [220.00, 174.61, 261.63, 196.00]
    thirds = [261.63, 220.00, 329.63, 246.94]
    fifths = [329.63, 261.63, 392.00, 293.66]
    bar = 4 * beat
    for b in range(int(total / bar) + 1):
        s0, s1 = int(b * bar * SR), min(n, int((b + 1) * bar * SR))
        if s0 >= n:
            break
        tt = t[s0:s1] - b * bar
        env = np.minimum(1, tt / 0.4) * np.exp(-tt * 0.35)
        k = b % 4
        pad = sum(np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.003 * tt) for f in (roots[k] / 2, thirds[k], fifths[k]))
        out[s0:s1] += 0.06 * env * pad
        # soft pluck on each beat
        for q in range(4):
            p0 = s0 + int(q * beat * SR)
            if p0 >= s1:
                break
            pt = np.arange(min(int(0.5 * SR), s1 - p0)) / SR
            note = [roots[k], thirds[k], fifths[k], thirds[k]][q] * 2
            out[p0:p0 + len(pt)] += 0.05 * np.sin(2 * np.pi * note * pt) * np.exp(-pt * 7)
    # kick on beats 1 and 3, hats on the off-beats
    rng = np.random.default_rng(7)
    for k in range(int(total / beat) + 1):
        s0 = int(k * beat * SR)
        if s0 >= n:
            break
        if k % 2 == 0:
            kt = np.arange(min(int(0.3 * SR), n - s0)) / SR
            freq = 50 + 70 * np.exp(-kt * 30)
            out[s0:s0 + len(kt)] += 0.35 * np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-kt * 9)
        h0 = s0 + int(beat / 2 * SR)
        if h0 < n:
            ht = np.arange(min(int(0.05 * SR), n - h0)) / SR
            noise = np.diff(rng.standard_normal(len(ht) + 1))
            out[h0:h0 + len(ht)] += 0.03 * noise * np.exp(-ht * 60)
    # sound effects at scene starts
    for at, kind in zip(cuts, sfx):
        s0 = int(at * SR)
        if s0 >= n:
            continue
        if kind == "whoosh":
            L = min(int(0.35 * SR), n - s0)
            wt = np.arange(L) / SR
            noise = rng.standard_normal(L)
            noise = np.convolve(noise, np.ones(30) / 30, mode="same")
            out[s0:s0 + L] += 0.25 * noise * np.sin(np.pi * wt / 0.35)
        elif kind == "ticks":
            for j in range(3):
                p0 = s0 + int(j * SR)
                L = min(int(0.06 * SR), n - p0)
                if L <= 0:
                    break
                tt = np.arange(L) / SR
                out[p0:p0 + L] += 0.3 * np.sin(2 * np.pi * 1800 * tt) * np.exp(-tt * 70)
        elif kind in ("ding", "chime"):
            L = min(int(1.2 * SR), n - s0)
            tt = np.arange(L) / SR
            tone = np.sin(2 * np.pi * 880 * tt) + 0.6 * np.sin(2 * np.pi * 1320 * tt) + (0.4 * np.sin(2 * np.pi * 1760 * tt) if kind == "chime" else 0)
            out[s0:s0 + L] += 0.18 * tone * np.exp(-tt * 3.5)
    # fade in/out and normalise
    fade = int(0.6 * SR)
    out[:fade] *= np.linspace(0, 1, fade)
    out[-fade:] *= np.linspace(1, 0, fade)
    out = out / (np.max(np.abs(out)) + 1e-9) * 0.7
    return (out * 32767).astype(np.int16)


def write_wav(path, samples):
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(samples.tobytes())


# ---------------------------------------------------------------- render

def render(data, out):
    scenes = build(data)
    total = sum(s["dur"] for s in scenes)
    cuts, acc = [], 0.0
    for s in scenes:
        cuts.append(acc)
        acc += s["dur"]
    wav = out[:-4] + ".wav"
    write_wav(wav, synth_music(total, cuts, [s["sfx"] for s in scenes]))

    cmd = [FFMPEG, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{RW}x{RH}", "-r", str(FPS), "-i", "-",
           "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "24", "-pix_fmt", "yuv420p", "-profile:v", "high",
           "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-shortest", "-movflags", "+faststart", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    frames = int(total * FPS)
    cache = {}
    for fi in range(frames):
        t = fi / FPS
        idx = max(i for i, c in enumerate(cuts) if c <= t + 1e-9)
        s = scenes[idx]
        lt = t - cuts[idx]
        img = background(t)
        chrome(img, lt / s["dur"], len(scenes), idx)
        # scenes that animate inside (quiz) are drawn every frame; the others are drawn once and cached
        animated = idx in (1, 2) and data.get("format") == "quiz"
        if animated:
            lay = layer()
            s["draw"](lay, lt)
        else:
            if idx not in cache:
                lay0 = layer()
                s["draw"](lay0, 0)
                cache[idx] = lay0
            lay = cache[idx]
        a_in = 1.0 if s.get("static_in") else ease(lt / 0.4)
        a_out = 1.0 if idx == len(scenes) - 1 else min(1.0, (s["dur"] - lt) / 0.22)
        alpha = max(0.0, min(a_in, a_out))
        dy = int((1 - a_in) * 70)
        if alpha < 1.0:
            a = lay.getchannel("A").point(lambda v, k=alpha: int(v * k))
            lay = lay.copy()
            lay.putalpha(a)
        base = img.convert("RGBA")
        base.alpha_composite(lay, (0, dy))
        proc.stdin.write(base.convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit("ffmpeg non è riuscito a creare il video")
    os.remove(wav)

    # cover: the hook scene, fully visible
    img = background(0)
    chrome(img, 0, len(scenes), 0)
    lay = layer()
    scenes[0]["draw"](lay, 0)
    base = img.convert("RGBA")
    base.alpha_composite(lay)
    base.convert("RGB").save(out[:-4] + "-cover.jpg", "JPEG", quality=90)
    return total


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as fh:
        secs = render(json.load(fh), sys.argv[2])
    size = os.path.getsize(sys.argv[2]) / 1e6
    print(f"ok {sys.argv[2]} · {secs:.1f} s · {size:.1f} MB")
