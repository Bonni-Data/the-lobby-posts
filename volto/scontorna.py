#!/usr/bin/env python3
"""Scontorna una foto di Andrea: toglie lo sfondo e salva un PNG trasparente ritagliato sulla persona.

Uso: python3 volto/scontorna.py foto.jpg uscita.png [--modello isnet|human|mix]
Modelli ONNX in ~/.u2net (scaricati da github.com/danielgatis/rembg/releases/v0.0.0):
  isnet-general-use.onnx (bordi più precisi), u2net_human_seg.onnx (specifico per persone).
Di default usa «mix»: la media dei due, che tiene bene capelli e spalle.
Stampa anche dove sta il volto (riquadro del viso, se lo trova) per impaginare: viene salvato in uscita.json.
"""
import json
import os
import sys

import cv2
import numpy as np
import onnxruntime as ort
from PIL import Image, ImageFilter, ImageOps

DIR = os.path.expanduser("~/.u2net")
_sess = {}


def session(name):
    if name not in _sess:
        _sess[name] = ort.InferenceSession(os.path.join(DIR, name + ".onnx"), providers=["CPUExecutionProvider"])
    return _sess[name]


def predict(img, name, size, mean, std):
    s = session(name)
    im = img.convert("RGB").resize((size, size), Image.LANCZOS)
    a = np.array(im).astype(np.float32)
    a = a / max(np.max(a), 1e-6)
    a = (a - np.array(mean, dtype=np.float32)) / np.array(std, dtype=np.float32)
    a = a.transpose(2, 0, 1)[None]
    out = s.run(None, {s.get_inputs()[0].name: a})[0][0, 0]
    out = (out - out.min()) / max(out.max() - out.min(), 1e-6)
    m = Image.fromarray((out * 255).astype(np.uint8)).resize(img.size, Image.LANCZOS)
    return np.array(m).astype(np.float32) / 255


def mask_for(img, mode="mix"):
    masks = []
    if mode in ("isnet", "mix"):
        masks.append(predict(img, "isnet-general-use", 1024, (0.5, 0.5, 0.5), (1.0, 1.0, 1.0)))
    if mode in ("human", "mix"):
        masks.append(predict(img, "u2net_human_seg", 320, (0.485, 0.456, 0.406), (0.229, 0.224, 0.225)))
    m = np.mean(masks, axis=0)
    # contrasto sul bordo: toglie l'alone senza tagliare i capelli
    m = np.clip((m - 0.18) / 0.64, 0, 1)
    # tiene solo la figura più grande (via macchie isolate dello sfondo)
    b = (m > 0.5).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(b, 8)
    if n > 2:
        keep = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        big = (lab == keep).astype(np.uint8)
        big = cv2.dilate(big, np.ones((25, 25), np.uint8))
        m = m * big
    return m


def face_box(img, alpha=None):
    """Riquadro del viso (x, y, w, h in pixel), stimato dalla sagoma: la testa è la parte sopra il collo,
    cioè sopra la riga più stretta tra la fronte e le spalle. Senza modelli esterni, regge su foto a mezzo busto."""
    a = np.array(alpha if alpha is not None else img.split()[-1]) > 128
    rows = np.where(a.any(axis=1))[0]
    if len(rows) < 20:
        return None
    top, bot = rows[0], rows[-1]
    widths = a.sum(axis=1)
    h = bot - top
    # il collo: riga più stretta tra il 18% e il 55% dell'altezza, dopo la parte più larga della testa
    lo, hi = top + int(h * 0.18), top + int(h * 0.55)
    neck = lo + int(np.argmin(widths[lo:hi]))
    head = a[top:neck]
    cols = np.where(head.any(axis=0))[0]
    if len(cols) == 0:
        return None
    # centro della testa: media delle colonne piene nella parte alta
    x0, x1 = cols[0], cols[-1]
    hw = x1 - x0
    hh = neck - top
    # il viso occupa la testa tolti i capelli in alto (~18%) e le orecchie ai lati (~8%)
    return [int(x0 + hw * 0.08), int(top + hh * 0.18), int(hw * 0.84), int(hh * 0.82)]


def main(src, out, mode="mix"):
    img = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    img.thumbnail((2200, 2200), Image.LANCZOS)
    m = mask_for(img, mode)
    alpha = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    rgba = img.copy()
    rgba.putalpha(alpha)
    bbox = alpha.point(lambda v: 255 if v > 24 else 0).getbbox()
    face = face_box(img, alpha)
    if bbox:
        rgba = rgba.crop(bbox)
        if face:
            face = [face[0] - bbox[0], face[1] - bbox[1], face[2], face[3]]
    rgba.save(out, "PNG", optimize=True)
    info = {"src": os.path.basename(src), "size": list(rgba.size), "face": face}
    json.dump(info, open(os.path.splitext(out)[0] + ".json", "w"), indent=1)
    print("ok", out, info)


if __name__ == "__main__":
    a = sys.argv[1:]
    mode = "mix"
    if "--modello" in a:
        i = a.index("--modello")
        mode = a[i + 1]
        del a[i:i + 2]
    main(a[0], a[1], mode)
