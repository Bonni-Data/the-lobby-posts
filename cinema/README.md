# Reel cinematografici

Come nasce un reel con scene video (usato dai reel del mercoledì, venerdì e domenica finché ci sono crediti OpenArt):

1. Le 5 scene video (9:16, 5 s, Grok Imagine 1.5 su OpenArt, circa 400 crediti l'una) si generano con gli strumenti OpenArt.
2. `jobs/<AAAA-MM-GG>-<rubrica>.json` descrive il reel: `output`, `assets`, `clips` (5 indirizzi delle scene), `transitions`, `scenes` (testo, sottotitolo e, per i quiz, `lines` con le risposte) ed `end` (chiusura).
3. `python3 cinema/render_assets.py jobs/<file>.json <assets>/` prepara in locale testi, logo, chiusura animata e musica (`music_epic.py`, sintetizzata: nessun brano di terzi).
4. Il push del file in `jobs/` avvia la GitHub Action `Monta reel cinematografico`, che scarica le scene, monta tutto con `compose.py` e salva il video in `reels/`.

Prova in locale con clip finte: `python3 cinema/compose.py jobs/<file>.json <cartella con c1.mp4 ... c5.mp4>`.
