#!/usr/bin/env python3
"""Scarica da Wikimedia Commons una foto con licenza libera per un ritratto (gira nella GitHub Action «Foto ritratto»).

Uso: python3 ritratti/scarica_foto.py ritratti/foto/<AAAA-MM-GG>.json
Il lavoro:
  {"name": "Tina Anselmi",          # nome e cognome
   "wikidata": "",                  # facoltativo: Q-id della persona su Wikidata
   "file": "",                      # facoltativo: nome esatto del file su Commons (es. "File:Tina Anselmi.jpg")
   "output": "posts/ritratti/2026-10-19/foto"}
Scrive fino a 4 candidate <output>-1.jpg ... <output>-4.jpg (lato lungo 1600 px al massimo, lato corto almeno 600 px)
e <output>.json con, per ciascuna, file, pagina, autore, licenza e la riga di credito da pubblicare. Accetta solo pubblico dominio, CC0, CC BY e CC BY-SA: mai NC, ND o «fair use».
Se non trova una foto utilizzabile scrive solo <output>.json con "error", così l'automazione lo sa.
"""
import html
import io
import json
import re
import sys
import urllib.parse
import urllib.request

from PIL import Image

UA = "TheLobbyRitratti/1.0 (https://thelobbyitalia.it)"
OK_LICENSE = re.compile(r"^(pd|pd-.*|cc0|cc-zero|cc-by-\d.*|cc-by-sa-\d.*|attribution|public domain)$", re.I)
OK_SHORT = re.compile(r"^(public domain|pubblico dominio|cc0|cc by( \d.*)?|cc by-sa( \d.*)?|attribution)", re.I)
BAD = re.compile(r"(\bnc\b|non-?commercial|\bnd\b|no-?deriv|fair use|non-free)", re.I)


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read()


def api(base, **params):
    params["format"] = "json"
    return json.loads(get(base + "?" + urllib.parse.urlencode(params)))


def entity(qid):
    ent = json.loads(get(f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"))["entities"][qid]
    claims = ent.get("claims", {})
    def vals(prop):
        return [c["mainsnak"].get("datavalue", {}).get("value") for c in claims.get(prop, [])
                if c.get("rank") != "deprecated" and c["mainsnak"].get("datavalue")]
    human = any(isinstance(v, dict) and v.get("id") == "Q5" for v in vals("P31"))
    return human, [v for v in vals("P18") if isinstance(v, str)], [v for v in vals("P373") if isinstance(v, str)]


def candidates(job):
    """Titoli di file su Commons, in ordine di affidabilità: file indicato, foto ufficiale Wikidata (P18),
    file della categoria Commons della persona (P373), ricerca per nome."""
    out, p18 = [], set()
    def add(t, star=False):
        t = t if t.startswith("File:") else "File:" + t
        if t not in out:
            out.append(t)
        if star:
            p18.add(t)
    if job.get("file"):
        add(job["file"], True)
    qids = [job["wikidata"]] if job.get("wikidata") else []
    if not qids:
        for lang in ("it", "en"):
            res = api("https://www.wikidata.org/w/api.php", action="wbsearchentities", search=job["name"],
                      language=lang, uselang=lang, type="item", limit=5)
            qids += [r["id"] for r in res.get("search", []) if r["id"] not in qids]
    for q in qids:
        human, imgs, cats = entity(q)
        if not human:
            continue
        for i in imgs:
            add(i, True)
        for c in cats[:1]:
            res = api("https://commons.wikimedia.org/w/api.php", action="query", list="categorymembers",
                      cmtitle="Category:" + c, cmtype="file", cmlimit=60)
            for m in res.get("query", {}).get("categorymembers", []):
                add(m["title"])
        break
    res = api("https://commons.wikimedia.org/w/api.php", action="query", list="search", srsearch=job["name"],
              srnamespace=6, srlimit=20)
    for m in res.get("query", {}).get("search", []):
        add(m["title"])
    return out, p18


def strip(s):
    s = re.sub(r"<[^>]+>", " ", str(s) if s is not None else "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


SKIP = re.compile(r"(stemma|logo|firma|signature|autograph|tomba|grave|targa|plaque|lapide|map|mappa|francobollo|"
                  r"stamp|\.svg$|\.pdf$|\.ogg$|\.webm$|street|via |piazza|scuola|school)", re.I)


def main(path):
    job = json.load(open(path, encoding="utf-8"))
    out = job["output"]
    titles, p18 = candidates(job)
    titles = [t for t in titles if not SKIP.search(t)][:80]
    found, tried = [], []
    for k in range(0, len(titles), 40):
        chunk = titles[k:k + 40]
        info = api("https://commons.wikimedia.org/w/api.php", action="query", titles="|".join(chunk),
                   prop="imageinfo", iiprop="url|extmetadata|size|mime", iiurlwidth=1600)
        for page in info.get("query", {}).get("pages", {}).values():
            t = page.get("title")
            if "imageinfo" not in page:
                continue
            ii = page["imageinfo"][0]
            meta = {kk: strip(v.get("value", "")) for kk, v in ii.get("extmetadata", {}).items()}
            lic, short = meta.get("License", ""), meta.get("LicenseShortName", "")
            if BAD.search(lic + " " + short + " " + meta.get("UsageTerms", "")) or not (OK_LICENSE.match(lic) or OK_SHORT.match(short)):
                tried.append(f"{t}: licenza {short or lic}")
                continue
            if ii.get("mime") not in ("image/jpeg", "image/png", "image/tiff", "image/webp"):
                continue
            w, h = ii.get("width", 0), ii.get("height", 0)
            if min(w, h) < 600:
                tried.append(f"{t}: troppo piccola {w}x{h}")
                continue
            score = (2.0 if t in p18 else 1.0) * (1.25 if h >= w else 1.0) * min(w * h, 4_000_000)
            found.append((score, t, ii, meta, short or lic))
    found.sort(key=lambda x: -x[0])
    cands = []
    for n, (score, t, ii, meta, lic) in enumerate(found[:4], 1):
        im = Image.open(io.BytesIO(get(ii.get("thumburl") or ii["url"]))).convert("RGB")
        im.thumbnail((1600, 1600))
        fn = f"{out}-{n}.jpg"
        im.save(fn, "JPEG", quality=90)
        artist = meta.get("Artist") or "autore sconosciuto"
        if len(artist) > 60:
            artist = artist[:57].rstrip() + "…"
        cands.append({"n": n, "jpg": fn, "file": t, "page": ii.get("descriptionurl"), "author": artist,
                      "license": lic, "license_url": meta.get("LicenseUrl", ""),
                      "credit": f"Foto: {artist} · {lic} · Wikimedia Commons",
                      "description": meta.get("ImageDescription", "")[:300], "date": meta.get("DateTimeOriginal", ""),
                      "restrictions": meta.get("Restrictions", ""), "size": [im.width, im.height], "wikidata_p18": t in p18})
    if not cands:
        json.dump({"name": job["name"], "error": "nessuna foto con licenza libera e risoluzione sufficiente", "tried": tried[:30]},
                  open(out + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("nessuna foto", len(tried))
        return
    json.dump({"name": job["name"], "candidates": cands,
               "nota": "Apri le candidate con Read e scegli quella in cui la persona è riconoscibile; usa il suo credit."},
              open(out + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ok", [(c["file"], c["license"], c["size"]) for c in cands])


if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except Exception as e:  # lascia traccia leggibile all'automazione
        import traceback
        job = json.load(open(sys.argv[1], encoding="utf-8"))
        json.dump({"name": job.get("name"), "error": f"{type(e).__name__}: {e}", "trace": traceback.format_exc()[-1500:]},
                  open(job["output"] + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("errore", e)
