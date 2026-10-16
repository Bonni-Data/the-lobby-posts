#!/usr/bin/env python3
"""THE LOBBY - monta un reel cinematografico: clip video + transizioni + testi animati + chiusura + musica.
Uso: python3 compose.py job.json [cartella_clip]
Se cartella_clip manca, scarica le clip dagli url in job["clips"] (serve internet: gira nella GitHub Action).
Usa le grafiche già pronte in job["assets"] (render_assets.py)."""
import json, math, os, subprocess, sys, urllib.request
import numpy as np
from PIL import Image

W, H, FPS = 1080, 1920, 30
S, O = 120, 12            # 4 s per scena, 0,4 s di transizione
END = 150                 # 5 s di chiusura
try:
    import imageio_ffmpeg
    FF = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FF = "ffmpeg"

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
job_path = sys.argv[1]
job = json.load(open(job_path, encoding="utf-8"))
A = os.path.join(root, job["assets"])
clipdir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(root, "_clips")
os.makedirs(clipdir, exist_ok=True)
clips = []
urls = job["clips"] or [None] * len(job["scenes"])
for i, url in enumerate(urls, 1):
    p = os.path.join(clipdir, f"c{i}.mp4")
    if not os.path.exists(p):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r, open(p, "wb") as f:
            f.write(r.read())
    clips.append(p)
clips.append(os.path.join(A, "endcard.mp4"))
n_sc = len(clips) - 1

def frames(path):
    cmd = [FF, "-loglevel", "error", "-i", path, "-an", "-vf",
           f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    last = None
    while True:
        b = pr.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        last = np.frombuffer(b, np.uint8).reshape(H, W, 3)
        yield last
    while True:           # clip più corta del previsto: tiene l'ultimo fotogramma
        yield last if last is not None else np.zeros((H, W, 3), np.uint8)

def rgba(path):
    a = np.asarray(Image.open(path).convert("RGBA")).astype(np.float32) / 255
    return a[..., :3] * 255, a[..., 3:4]
base_rgb, base_a = rgba(os.path.join(A, "base.png"))
ov = [rgba(os.path.join(A, f"overlay_{i}.png")) for i in range(1, n_sc + 1)]

def ease(t):
    t = min(1.0, max(0.0, t)); return 1 - (1 - t) ** 3

def zoom(img, z, cy=0.5):
    if abs(z - 1) < 1e-3: return img.astype(np.float32)
    im = Image.fromarray(img)
    cw, ch = W / z, H / z
    x0 = (W - cw) / 2; y0 = (H - ch) * cy
    return np.asarray(im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))).astype(np.float32)

def grade(f):
    f = (f - 128) * 1.08 + 128          # un filo di contrasto
    f[..., 0] *= 1.03; f[..., 2] *= 0.97  # caldo
    return f

yy, xx = np.mgrid[0:H, 0:W]
vign = (1 - 0.35 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 2).astype(np.float32)[..., None]

def scene_frame(i, raw, k):
    """clip i (0-based), fotogramma locale k: ken burns + grade + vignetta + base + testo animato"""
    if i == n_sc:
        return raw.astype(np.float32)
    f = grade(zoom(raw, 1.0 + 0.07 * k / (S + O))) * vign
    f = f * (1 - base_a) + base_rgb * base_a
    start = 3 if i == 0 else 8
    a_in = ease((k - start) / 10)
    a_out = 1 - ease((k - (S - 8)) / 7)
    a = max(0.0, min(a_in, a_out))
    if a > 0:
        rgb, al = ov[i]
        dy = int(46 * (1 - a_in))
        if dy:
            rgb = np.roll(rgb, dy, axis=0); al = np.roll(al, dy, axis=0)
        al = al * a
        f = f * (1 - al) + rgb * al
    return f

def transition(kind, A_, B_, t):
    e = ease(t)
    if kind == "slide":
        off = int(H * e)
        out = np.empty_like(A_)
        out[: H - off] = A_[off:]
        out[H - off:] = B_[: off]
        blur = int(60 * math.sin(math.pi * t))
        if blur > 2:
            out = (out + np.roll(out, blur // 2, 0) + np.roll(out, -blur // 2, 0) + np.roll(out, blur, 0)) / 4
        return out
    if kind == "zoom":
        za = 1 + 0.35 * e; zb = 1.35 - 0.35 * e
        a = zoom(np.clip(A_, 0, 255).astype(np.uint8), za); b = zoom(np.clip(B_, 0, 255).astype(np.uint8), zb)
        return a * (1 - e) + b * e
    # flash
    out = A_ * (1 - e) + B_ * e
    fl = math.sin(math.pi * t) ** 1.5 * 0.9
    return out * (1 - fl) + 255 * fl

out_path = os.path.join(root, job["output"])
os.makedirs(os.path.dirname(out_path), exist_ok=True)
total = n_sc * S + END
enc = subprocess.Popen([FF, "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-i", os.path.join(A, "music.m4a"), "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "21",
                        "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", "-movflags", "+faststart", out_path], stdin=subprocess.PIPE)
gens = [frames(c) for c in clips]
local = [0] * len(clips)
trans = job.get("transitions", ["flash"] * n_sc)
for t in range(total):
    i = min(t // S, n_sc)
    k = t - i * S
    cur_raw = next(gens[i]); local[i] += 1
    cur = scene_frame(i, cur_raw, k + (O if i > 0 else 0))
    if i > 0 and k < O:
        prev_raw = next(gens[i - 1]); local[i - 1] += 1
        prev = scene_frame(i - 1, prev_raw, S + k)
        cur = transition(trans[i - 1], prev, cur, (k + 1) / (O + 1))
    enc.stdin.write(np.clip(cur, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait()
# copertina: il logo (stessa immagine del reel di lancio) se esiste, altrimenti un fotogramma
print("ok", out_path, f"{total / FPS:.1f} s")
