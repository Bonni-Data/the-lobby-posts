#!/usr/bin/env python3
"""THE LOBBY - fotogrammi di controllo di un video (per le automazioni, che li aprono con Read).

Uso: python3 estrai_fotogrammi.py video.mp4 cartella t1 [t2 ...]
I tempi sono in secondi; un tempo negativo conta dalla fine (-1 = un secondo prima della fine).
Scrive cartella/f_<t>.jpg (540 px di larghezza) e cartella/foglio.jpg con tutti i fotogrammi affiancati.
"""
import json
import os
import subprocess
import sys

from PIL import Image


def main(video, out, *times):
    os.makedirs(out, exist_ok=True)
    d = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", video],
                                  capture_output=True, text=True).stdout or "{}")
    dur = float(d.get("format", {}).get("duration", 0))
    files = []
    for t in times or ("1", "-1"):
        s = float(t)
        s = max(0.0, dur + s if s < 0 else s)
        f = os.path.join(out, f"f_{t}.jpg")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{s:.2f}", "-i", video, "-frames:v", "1",
                        "-vf", "scale=540:-1", f], check=True)
        files.append(f)
    ims = [Image.open(f) for f in files]
    sheet = Image.new("RGB", (sum(i.width for i in ims), max(i.height for i in ims)), (255, 255, 255))
    x = 0
    for i in ims:
        sheet.paste(i, (x, 0))
        x += i.width
    sheet.save(os.path.join(out, "foglio.jpg"), quality=85)
    print("ok", out, f"durata {dur:.1f} s", ", ".join(os.path.basename(f) for f in files))


if __name__ == "__main__":
    main(*sys.argv[1:])
