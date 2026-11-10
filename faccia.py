#!/usr/bin/env python3
"""THE LOBBY - «faccia prima» per tutte le rubriche (decisione di Andrea del 24 ottobre 2026).

Ogni contenuto mostra il volto di Andrea con 1-2 parole grandi accanto che richiamano il concetto; la
spiegazione viene dopo (le slide successive, la didascalia o il resto del reel). Questo script sceglie da solo
la foto giusta della libreria (volto/libreria/indice.json) in base alla rubrica, evita di ripetere la stessa foto
dei giorni precedenti, impagina e salva l'uso in volto/uso.json.

Uso: python3 faccia.py lavoro.json
lavoro.json:
{
  "mode": "post",              # "post": immagine 1080x1350 da mettere PRIMA della grafica della rubrica
                               #         (o al posto della copertina 01.png di un carosello)
                               # "reel": 2,5 s con il volto e le parole messi DAVANTI al reel già pronto
                               #         + copertina 1080x1920
  "rubrica": "opportunita",    # opportunita | lezioni | ritratti | lo-sapevi | pillole | quiz | founder |
                               # presentazione | attualita | notizie | premium (cene e lezioni live)
  "words": ["VIAGGI", "GRATIS"],   # 1 o 2 parole, max ~10 lettere l'una, in maiuscolo: il concetto in un colpo d'occhio
  "kicker": "Opportunità",     # facoltativo, etichetta piccola (max ~22 caratteri)
  "sub": "3 bandi con le spese coperte dagli enti",   # facoltativo: post una riga (max ~45 caratteri); reel la frase
                               # del gancio (max ~70 caratteri), scritta sotto le parole. Deve essere SPECIFICA del
                               # contenuto di oggi, mai una formula fissa (piano di crescita del 3/11/2026)
  "swipe": true,               # facoltativo (post): freccia «Scorri» quando dopo ci sono altre immagini
  "tono": "serio",             # facoltativo: "serio" (cronaca, processi, lutti, guerre, disastri: solo foto serie)
                               # o "neutro" (temi seri: niente sorrisi); senza tono vanno bene tutte le foto
  "card": {...},               # facoltativo (ritratti): foto del personaggio, vedi make_face.py
  "video": "reels/2026-10-28.mp4",   # solo mode reel: il reel già pronto (grafico o cinematografico)
                               # Nei reel l'intro è uno spezzone di Andrea in movimento (volto/clip/indice.json,
                               # decisione del 24/10/2026); se non ce n'è uno adatto, o con "tono": "serio",
                               # l'intro è la foto con lo zoom. "clip": false per forzare la foto.
  "out": "posts/2026-10-27-faccia.png" # post: il PNG; reel: l'MP4 finale (scrive anche <out>-cover.jpg)
}
Stampa la foto scelta. Controlla SEMPRE il risultato con Read (e per il reel 2 fotogrammi: -ss 1 e -ss 4).
"""
import datetime
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "volto", "libreria")
CLIP = os.path.join(HERE, "volto", "clip")
USO = os.path.join(HERE, "volto", "uso.json")

# rubrica -> foto preferite, in ordine (se non c'è nulla di adatto si usa la rotazione su tutte le «alta»)
FALLBACK = ["sorriso-2", "sicuro-1", "sorriso-4"]
THEME_BY_RUBRICA = {"notizie": "coral", "opportunita": "ivory", "pillole": "ivory", "founder": "ivory",
                    "lezioni": "navy", "premium": "navy", "ritratti": "navy"}


def load(p, default):
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return default


# "tono" del lavoro -> toni di foto ammessi (una faccia sorridente su una notizia triste non va mai bene)
TONI = {"serio": {"serio"}, "neutro": {"serio", "neutro"}}


def choose(rubrica, tono=None):
    idx = load(os.path.join(LIB, "indice.json"), {}).get("foto", {})
    uso = load(USO, [])
    recent = [u["foto"] for u in uso[-2:]]
    ok = TONI.get(tono)
    if ok:
        idx = {k: v for k, v in idx.items() if v.get("tono") in ok} or idx
    cands = [k for k, v in idx.items() if rubrica in v.get("rubriche", [])]
    if not cands and ok:   # col tono richiesto conta più il tono della rubrica
        cands = list(idx)
    if not cands:
        cands = [k for k, v in idx.items() if v.get("qualita") == "alta"] or FALLBACK
    # la meno usata di recente tra le adatte, mai la stessa delle ultime due uscite se c'è alternativa
    last_use = {k: -1 for k in cands}
    for i, u in enumerate(uso):
        if u["foto"] in last_use:
            last_use[u["foto"]] = i
    order = sorted(cands, key=lambda k: (k in recent, last_use[k]))
    return order[0]


def choose_clip(rubrica, tono=None):
    """Spezzone in movimento per l'intro del reel: il meno usato tra quelli adatti; nessuno per i temi tristi."""
    if tono == "serio":
        return None
    idx = load(os.path.join(CLIP, "indice.json"), {}).get("clip", {})
    cands = [k for k, v in idx.items() if os.path.exists(os.path.join(CLIP, k + ".mp4"))
             and (rubrica in v.get("rubriche", []) or not v.get("rubriche"))]
    if not cands:
        return None
    uso = load(USO, [])
    last = {k: -1 for k in cands}
    for i, u in enumerate(uso):
        if u.get("clip") in last:
            last[u["clip"]] = i
    return sorted(cands, key=lambda k: last[k])[0]


def record(foto, job, clip=None):
    uso = load(USO, [])
    uso.append({"data": datetime.date.today().isoformat(), "rubrica": job.get("rubrica"), "mode": job.get("mode"),
                "foto": foto, "clip": clip, "words": job.get("words"), "out": job.get("out")})
    with open(USO, "w", encoding="utf-8") as fh:
        json.dump(uso[-400:], fh, ensure_ascii=False, indent=1)


def face_data(job, foto, fmt):
    meta = load(os.path.join(LIB, foto + ".json"), {})
    d = {"format": fmt, "face": os.path.join(LIB, foto + ".png"), "words": job["words"][:2]}
    for k in ("kicker", "sub", "swipe", "card"):
        if job.get(k):
            d[k] = job[k]
    d.update(meta.get("layout", {}))
    # 10/11/2026: colore della copertina secondo la rubrica, perché il feed alterni i colori; le notizie tristi
    # (tono «serio») restano sempre su navy
    d["theme"] = job.get("theme") or ("navy" if job.get("tono") == "serio" else THEME_BY_RUBRICA.get(job.get("rubrica", ""), "navy"))
    if job.get("card"):  # con la cornice del ritratto Andrea sta sempre a destra, a grandezza normale
        for k in ("face_h", "face_x", "face_shift", "words_y"):
            d.pop(k, None)
        d["side"] = "right"
    return d


def warn_repeat(job):
    """Copertine tutte uguali fanno scorrere via (piano di crescita del 3/11/2026): avvisa se le parole o la frase
    sono già uscite nelle ultime 20 copertine."""
    uso = load(USO, [])[-20:]
    w = [x.upper() for x in job.get("words", [])]
    for u in uso:
        uw = [x.upper() for x in (u.get("words") or [])]
        if uw and (uw == w or (len(w) > 1 and len(uw) > 1 and uw[1] == w[1])):
            print(f"ATTENZIONE: parole già usate il {u.get('data')} ({' / '.join(uw)}): scegline altre")
            break
    if (job.get("sub") or "").strip().lower().startswith("tutti ne parlano"):
        print("ATTENZIONE: «Tutti ne parlano…» è una formula fissa: scrivi il gancio specifico di oggi")


def run(job):
    sys.path.insert(0, HERE)
    import make_face
    warn_repeat(job)
    foto = choose(job.get("rubrica", ""), job.get("tono"))
    out = os.path.join(HERE, job["out"]) if not os.path.isabs(job["out"]) else job["out"]
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    if job.get("mode", "post") == "post":
        make_face.make(face_data(job, foto, "post"), out)
    else:
        import make_face_reel
        video = job["video"] if os.path.isabs(job["video"]) else os.path.join(HERE, job["video"])
        tmp = tempfile.mkdtemp()
        intro = os.path.join(tmp, "intro.mp4")
        # Piano di crescita del 3/11/2026: con un solo spezzone ogni reel apriva con gli stessi 3 secondi identici
        # (Instagram premia i contenuti originali e ogni apertura uguale fa scorrere via). Lo spezzone si usa solo
        # se in volto/clip/ ce ne sono almeno 3 tra cui ruotare; altrimenti la foto, che ruota su tutta la libreria.
        n_clip = len([k for k in load(os.path.join(CLIP, "indice.json"), {}).get("clip", {})
                      if os.path.exists(os.path.join(CLIP, k + ".mp4"))])
        clip = choose_clip(job.get("rubrica", ""), job.get("tono")) if job.get("clip", n_clip >= 3) else None
        if clip:
            make_face_reel.clip_intro({"clip": os.path.join(CLIP, clip + ".mp4"), "words": job["words"][:2],
                                       "kicker": job.get("kicker")}, intro)
            print("intro in movimento:", clip)
        else:
            make_face_reel.run({"face": os.path.join(LIB, foto + ".png"), "words": job["words"][:2],
                                "kicker": job.get("kicker"), "sub": job.get("sub"), "sub_x1": 600,
                                "duration": float(job.get("intro", 1.8)), "endcard": False},
                               intro)
            print("intro con la foto:", foto)
        norm = "fps=30,scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=0x111C35,setsar=1,format=yuv420p"
        # audio senza stacchi: la musica dell'intro sfuma in quella del reel (prima c'era un taglio netto al secondo 3)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", intro, "-i", video, "-filter_complex",
                        f"[0:v]{norm}[v0];[1:v]{norm}[v1];[v0][v1]concat=n=2:v=1:a=0[v];"
                        f"[0:a]aresample=44100,aformat=channel_layouts=stereo[a0];"
                        f"[1:a]aresample=44100,aformat=channel_layouts=stereo[a1];"
                        f"[a0][a1]acrossfade=d=0.4:c1=tri:c2=tri,apad=pad_dur=0.4[a]",
                        "-map", "[v]", "-map", "[a]", "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                        "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out], check=True)
        cover = out[:-4] + "-cover.jpg"
        png = os.path.join(tmp, "cover.png")
        make_face.make(face_data(job, foto, "reel"), png)
        from PIL import Image
        Image.open(png).convert("RGB").save(cover, "JPEG", quality=92)
        print("copertina", cover)
    record(foto, job, locals().get("clip"))
    print("ok", out, "foto:", foto)
    return out


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as fh:
        run(json.load(fh))
