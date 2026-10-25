#!/usr/bin/env python3
"""THE LOBBY - contatti pubblici dei moltiplicatori (decisione di Andrea del 25/10/2026).

Raccoglie SOLO indirizzi email pubblicati dagli enti stessi sulle loro pagine ufficiali (mai indirizzi indovinati):
- punti locali Eurodesk (www.eurodesk.it/rete/punti-locali/<regione>/ITxxx);
- scuole secondarie di secondo grado statali della città metropolitana di Milano (open data del Ministero
  dell'istruzione, campo email istituzionale della scuola capofila);
- poche redazioni e organismi giovanili nazionali, dalle loro pagine di contatto.
Gira nella GitHub Action «Contatti pubblici» (lì c'è internet) e scrive outreach/contatti-*.csv con la pagina di origine.
"""
import csv, html, io, json, os, re, sys, time, urllib.request, urllib.error, zipfile

UA = {"User-Agent": "Mozilla/5.0 (compatible; THE-LOBBY-contatti/1.0; +https://thelobbyitalia.it)"}
OUT = os.path.dirname(os.path.abspath(__file__))
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def get(url, binary=False, tries=2):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                b = r.read()
                return b if binary else b.decode(r.headers.get_content_charset() or "utf-8", "replace")
        except Exception as e:  # noqa
            err = e
            time.sleep(2)
    print("ERRORE", url, err, file=sys.stderr)
    return None


def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def mails(page):
    found = set(m.lower() for m in re.findall(r'mailto:([^"\'?>\s]+)', page or "", re.I))
    found |= set(m.lower() for m in EMAIL.findall(text(page or "")))
    return sorted(e.strip(".,;") for e in found if not e.endswith((".png", ".jpg", ".gif", ".webp", ".svg")))


def eurodesk():
    regions = ["abruzzo", "basilicata", "calabria", "campania", "emilia-romagna", "friuli-venezia-giulia", "lazio", "liguria",
               "lombardia", "marche", "molise", "piemonte", "puglia", "sardegna", "sicilia", "toscana", "trentino-alto-adige",
               "umbria", "valle-daosta", "veneto"]
    points = []
    for reg in regions:
        page = get(f"https://www.eurodesk.it/rete/punti-locali/{reg}")
        if not page:
            continue
        links = sorted(set(re.findall(r'href="(/rete/punti-locali/[^"/]+/IT\d+)"', page, re.I)))
        print(reg, len(links), "punti")
        for link in links:
            url = "https://www.eurodesk.it" + link
            p = get(url)
            if not p:
                continue
            h1 = text((re.search(r"<h1[^>]*>(.*?)</h1>", p, re.S) or [None, ""])[1])
            title = text((re.search(r"<title>(.*?)</title>", p, re.S) or [None, ""])[1])
            main = p.split("<footer")[0]
            points.append({"regione": reg, "codice": link.rsplit("/", 1)[1], "url": url, "nome": h1 or title,
                           "testo": text(re.sub(r"<(script|style|nav|header)[^>]*>.*?</\1>", " ", main, flags=re.S))[:600],
                           "email": mails(main)})
            time.sleep(0.5)
    # gli indirizzi che compaiono su quasi tutte le pagine sono quelli del sito nazionale, non del punto locale
    count = {}
    for pt in points:
        for e in pt["email"]:
            count[e] = count.get(e, 0) + 1
    common = {e for e, n in count.items() if n > max(5, len(points) // 4)}
    with open(os.path.join(OUT, "contatti-eurodesk.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["regione", "codice", "nome", "email", "pagina", "testo"])
        for pt in points:
            em = [e for e in pt["email"] if e not in common]
            w.writerow([pt["regione"], pt["codice"], pt["nome"], " ".join(em), pt["url"], pt["testo"]])
    print("eurodesk:", len(points), "punti; esclusi gli indirizzi comuni", sorted(common))


def scuole():
    cat = get("https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Scuole") or ""
    names = sorted(set(re.findall(r"(SCUANAGRAFESTAT\d{16}\.csv)", cat)), reverse=True)
    if not names:
        names = ["SCUANAGRAFESTAT20252620250901.csv", "SCUANAGRAFESTAT20242520240901.csv"]
    data = None
    for n in names:
        data = get(f"https://dati.istruzione.it/opendata/opendata/catalogo/elements1/{n}")
        if data and "CODICESCUOLA" in data[:2000]:
            print("anagrafe scuole:", n)
            break
        data = None
    if not data:
        print("anagrafe scuole non trovata", file=sys.stderr)
        return
    rows = list(csv.DictReader(io.StringIO(data)))
    seen = {}
    for r in rows:
        if (r.get("PROVINCIA") or "").upper() != "MILANO":
            continue
        grado = (r.get("DESCRIZIONETIPOLOGIAGRADOISTRUZIONESCUOLA") or "").upper()
        if not any(k in grado for k in ("LICEO", "ISTITUTO TECNICO", "ISTITUTO PROFESSIONALE", "ISTITUTO SUPERIORE", "ISTITUTO D'ARTE", "SECONDARIA DI II", "IST PROF", "IST TEC")):
            continue
        email = (r.get("INDIRIZZOEMAILSCUOLA") or "").strip().lower()
        if not EMAIL.fullmatch(email):
            continue
        capofila = r.get("CODICEISTITUTORIFERIMENTO") or r.get("CODICESCUOLA")
        key = email
        if key not in seen:
            seen[key] = {"codice_istituto": capofila, "istituto": r.get("DENOMINAZIONEISTITUTORIFERIMENTO") or r.get("DENOMINAZIONESCUOLA"),
                         "scuola": r.get("DENOMINAZIONESCUOLA"), "tipo": grado.title(), "comune": (r.get("DESCRIZIONECOMUNE") or "").title(),
                         "email": email, "sito": r.get("SITOWEBSCUOLA") or ""}
    with open(os.path.join(OUT, "contatti-scuole-milano.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["codice_istituto", "istituto", "scuola", "tipo", "comune", "email", "sito"])
        w.writeheader()
        for v in sorted(seen.values(), key=lambda x: (x["comune"] != "Milano", x["comune"], x["istituto"] or "")):
            w.writerow(v)
    print("scuole Milano:", len(seen))


def vari():
    pages = {
        "Studenti.it": ["https://www.studenti.it/chi-siamo.html"],
        "Skuola.net": ["https://www.skuola.net/contatti.html", "https://www.skuola.net/info/contatti.html", "https://www.skuola.net/chi-siamo.html"],
        "ScuolaZoo": ["https://www.scuolazoo.com/contatti/", "https://www.scuolazoo.com/contatti", "https://www.scuolazoo.com/chi-siamo/"],
        "Orizzonte Scuola": ["https://www.orizzontescuola.it/contatti/", "https://www.orizzontescuola.it/redazione/"],
        "Tecnica della Scuola": ["https://www.tecnicadellascuola.it/contatti", "https://www.tecnicadellascuola.it/redazione"],
        "Consiglio Nazionale dei Giovani": ["https://consiglionazionaledeigiovani.it/contatti/", "https://www.consiglionazionaledeigiovani.it/contatti/"],
        "Agenzia Italiana per la Gioventù": ["https://agenziagioventu.gov.it/contatti/", "https://www.agenziagioventu.gov.it/contatti/"],
        "Eurodesk Italy": ["https://www.eurodesk.it/contatti"],
    }
    with open(os.path.join(OUT, "contatti-vari.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["ente", "email", "pagina"])
        for ente, urls in pages.items():
            for u in urls:
                p = get(u, tries=1)
                if not p:
                    continue
                em = mails(p)
                print(ente, u, em)
                w.writerow([ente, " ".join(em), u])


if __name__ == "__main__":
    what = sys.argv[1:] or ["eurodesk", "scuole", "vari"]
    for fn in what:
        globals()[fn]()
