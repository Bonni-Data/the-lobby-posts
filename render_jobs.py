#!/usr/bin/env python3
"""THE LOBBY - esegue su GitHub Actions i generatori di grafiche e video (decisione del 5 novembre 2026).

Perché: nelle sessioni automatiche il controllo dei permessi non lascia più eseguire gli script del repository
(«codice da repo esterno»). Le automazioni quindi non eseguono più python3 make_*.py: scrivono un lavoro in
jobs/render/<AAAA-MM-GG>-<rubrica>-<n>.json, fanno push su main e la GitHub Action «Render grafiche» lo esegue qui,
salva i file prodotti e scrive accanto il risultato <nome>.result.json.

Formato del lavoro:
{
  "steps": [
    ["make_carousel.py", "data/notizia-2026-11-06.json", "posts/notizie/2026-11-06/"],
    ["faccia.py", "data/faccia-2026-11-06-notizia.json"],
    ["make_storia.py", "posts/notizie/2026-11-06/01.png", "posts/storie/2026-11-06-notizia.png", "--hint", "Scorri il carosello sul profilo"]
  ]
}
Si eseguono solo gli script dell'elenco SCRIPTS, senza shell, con percorsi relativi dentro il repository. Un passo
che fallisce non ferma i successivi: l'esito di ognuno finisce nel result.json.
"""
import glob
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = {
    "make_carousel.py", "faccia.py", "make_storia.py", "make_story.py", "make_pill.py", "make_post.py",
    "make_reel.py", "make_face.py", "estrai_fotogrammi.py", "cinema/render_assets.py",
}
# make_slideshow.py tolto il 10/11/2026: Andrea non vuole reel montati dalle immagini dei post (un solo post per contenuto).


def safe(arg):
    a = str(arg)
    if a.startswith("--"):
        return True
    return not (a.startswith("/") or ".." in a.split("/") or "\x00" in a)


def probe(path):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,codec_name,width,height",
                              "-of", "json", path], capture_output=True, text=True, timeout=60)
        d = json.loads(out.stdout or "{}")
        streams = [{k: s.get(k) for k in ("codec_type", "codec_name", "width", "height") if s.get(k) is not None} for s in d.get("streams", [])]
        return {"file": path, "duration": round(float(d.get("format", {}).get("duration", 0)), 2), "streams": streams}
    except Exception as e:  # noqa: BLE001
        return {"file": path, "error": str(e)}


def run_job(path):
    job = json.load(open(path, encoding="utf-8"))
    res = {"job": os.path.relpath(path, HERE), "steps": [], "probe": []}
    for step in job.get("steps", []):
        t0 = time.time()
        item = {"step": step}
        if not step or step[0] not in SCRIPTS or not all(safe(a) for a in step):
            item.update(exit=None, error="passo non ammesso (script fuori elenco o percorso non valido)")
        else:
            try:
                p = subprocess.run([sys.executable, step[0], *map(str, step[1:])], cwd=HERE, capture_output=True,
                                   text=True, timeout=900)
                item.update(exit=p.returncode, output="\n".join((p.stdout + p.stderr).strip().splitlines()[-25:]))
            except subprocess.TimeoutExpired:
                item.update(exit=None, error="timeout di 15 minuti")
        item["seconds"] = round(time.time() - t0, 1)
        res["steps"].append(item)
        print(json.dumps(item, ensure_ascii=False)[:600], flush=True)
    for v in job.get("probe", []):
        if safe(v):
            res["probe"].append(probe(os.path.join(HERE, v)) | {"file": v})
    res["ok"] = all(s.get("exit") == 0 for s in res["steps"])
    out = path[:-5] + ".result.json"
    json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return out


def main():
    todo = sys.argv[1:] or sorted(glob.glob(os.path.join(HERE, "jobs/render/*.json")))
    for j in todo:
        if j.endswith(".result.json") or os.path.exists(j[:-5] + ".result.json"):
            continue
        print("lavoro", j, flush=True)
        print("risultato", run_job(j), flush=True)


if __name__ == "__main__":
    main()
