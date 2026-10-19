#!/usr/bin/env python3
"""Scarica da Wikimedia Commons una foto con licenza libera per un ritratto (gira nella GitHub Action «Foto ritratto»).

Uso: python3 ritratti/scarica_foto.py ritratti/foto/<AAAA-MM-GG>.json
Il lavoro:
  {"name": "Tina Anselmi",          # nome e cognome
   "wikidata": "",                  # facoltativo: Q-id della persona su Wikidata
   "file": "",                      # facoltativo: nome esatto del file su Commons (es. "File:Tina Anselmi.jpg")
   "output": "posts/ritratti/2026-10-19/foto"}
Scrive <output>.jpg (lato lungo 1600 px al massimo) e <output>.json con file, pagina, autore, licenza e la riga
di credito da pubblicare. Accetta solo pubblico dominio, CC0, CC BY e CC BY-SA: mai NC, ND o «fair use».
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


def p18(qid):
    ent = json.loads(get(f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"))["entities"][qid]
    claims = ent.get("claims", {})
    humans = [c["mainsnak"].get("datavalue", {}).get("value", {}).get("id") for c in claims.get("P31", [])]
    imgs = [c["mainsnak"].get("datavalue", {}).get("value") for c in claims.get("P18", [])
            if c.get("rank") != "deprecated"]
    return ("Q5" in humans), [i for i in imgs if i]


def candidates(job):
    if job.get("file"):
        yield job["file"]
    qids = [job["wikidata"]] if job.get("wikidata") else []
    if not qids:
        for lang in ("it", "en"):
            res = api("https://www.wikidata.org/w/api.php", action="wbsearchentities", search=job["name"],
                      language=lang, uselang=lang, type="item", limit=5)
            qids += [r["id"] for r in res.get("search", []) if r["id"] not in qids]
    for q in qids:
        human, imgs = p18(q)
        if human:
            for i in imgs:
                yield "File:" + i
            if imgs:
                return


def strip(s):
    s = re.sub(r"<[^>]+>", " ", str(s) if s is not None else "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def main(path):
    job = json.load(open(path, encoding="utf-8"))
    out = job["output"]
    tried = []
    for title in candidates(job):
        title = title if title.startswith("File:") else "File:" + title
        info = api("https://commons.wikimedia.org/w/api.php", action="query", titles=title, prop="imageinfo",
                   iiprop="url|extmetadata|size|mime", iiurlwidth=1600)
        page = next(iter(info["query"]["pages"].values()))
        if "imageinfo" not in page:
            tried.append(f"{title}: non trovato")
            continue
        ii = page["imageinfo"][0]
        meta = {k: strip(v.get("value", "")) for k, v in ii.get("extmetadata", {}).items()}
        lic, short = meta.get("License", ""), meta.get("LicenseShortName", "")
        if BAD.search(lic + " " + short + " " + meta.get("UsageTerms", "")) or not (OK_LICENSE.match(lic) or OK_SHORT.match(short)):
            tried.append(f"{title}: licenza non adatta ({short or lic})")
            continue
        if ii.get("mime") not in ("image/jpeg", "image/png", "image/tiff", "image/webp"):
            tried.append(f"{title}: formato {ii.get('mime')}")
            continue
        im = Image.open(io.BytesIO(get(ii.get("thumburl") or ii["url"]))).convert("RGB")
        im.thumbnail((1600, 1600))
        im.save(out + ".jpg", "JPEG", quality=90)
        artist = meta.get("Artist") or "autore sconosciuto"
        if len(artist) > 60:
            artist = artist[:57].rstrip() + "…"
        credit = f"Foto: {artist} · {short or lic} · Wikimedia Commons"
        json.dump({"name": job["name"], "file": title, "page": ii.get("descriptionurl"), "author": artist,
                   "license": short or lic, "license_url": meta.get("LicenseUrl", ""), "credit": credit,
                   "restrictions": meta.get("Restrictions", ""), "size": [im.width, im.height]},
                  open(out + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("ok", title, short, im.size)
        return
    json.dump({"name": job["name"], "error": "nessuna foto con licenza libera trovata", "tried": tried},
              open(out + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("nessuna foto", tried)


if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except Exception as e:  # lascia traccia leggibile all'automazione
        import traceback
        job = json.load(open(sys.argv[1], encoding="utf-8"))
        json.dump({"name": job.get("name"), "error": f"{type(e).__name__}: {e}", "trace": traceback.format_exc()[-1500:]},
                  open(job["output"] + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("errore", e)
