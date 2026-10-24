# the-lobby-posts

Grafiche settimanali di THE LOBBY (post Instagram/Facebook).

- `make_post.py`: genera il PNG 1080x1350 da un JSON (`python3 make_post.py dati.json out.png`)
- `history.json`: voci già usate nelle ultime edizioni (per non ripeterle)
- `posts/AAAA-MM-GG.png`: grafiche pubblicate, con indirizzo pubblico per Metricool

- `make_pill.py`: pillola formativa del giovedì (`history-pillole.json`)
- `make_storia.py`: la storia 1080x1920 che rilancia ogni post (vedi `comunicazione/PUBBLICA.md`)
- `make_story.py`: post «Scopri THE LOBBY» del sabato, impaginazione `brand` o `founder` con la foto in `assets/andrea-cut.png` (`history-storie.json`)

- `make_carousel.py`: carosello del lunedì, da 4 a 9 slide 1080x1350 (`python3 make_carousel.py dati.json posts/caroselli/AAAA-MM-GG/`), storico in `history-caroselli.json`
- `make_reel.py`: reel 1080x1920 di 18-30 secondi con musica sintetizzata (nessun brano di terzi) e copertina `-cover.jpg`
  (`python3 make_reel.py dati.json reels/AAAA-MM-GG.mp4`); formati `fact` (Lo sapevi?, mercoledì), `quiz` (Quiz lampo, venerdì),
  `news` (Attualità in 30 secondi, domenica); storico in `history-reel.json`

## La promessa di THE LOBBY (sempre visibile)

Decisione di Andrea del 18 ottobre 2026: in ogni contenuto deve essere chiaro cosa offriamo.
Le tre frasi stanno in `make_pill.py` (`PROMISE`, `PROMISE_LINE`) e i generatori le disegnano da soli:

1. Formazione per giovani politici
2. Le migliori opportunità internazionali
3. Networking con altri giovani di talento

- post 1080x1350 (`make_pill.py`, `make_post.py`, `make_story.py`): fascia corallo in fondo con le tre promesse su una riga;
- carosello (`make_carousel.py`): ultima slide con «Su THE LOBBY trovi» e le tre promesse;
- reel grafico (`make_reel.py`) e reel cinematografico (`cinema/render_assets.py`): schermata finale con le tre promesse.

Per cambiarle, modifica solo `PROMISE` e `PROMISE_LINE`.

## Faccia prima (dal 24 ottobre 2026)

Ogni contenuto mostra il volto di Andrea con 1-2 parole grandi accanto: `faccia.py` (legge `volto/libreria/`,
sceglie la foto per rubrica, registra l'uso in `volto/uso.json`). Post singoli → carosello di 2 immagini
(prima la faccia, poi la grafica della rubrica); caroselli e ritratti → la copertina 01.png diventa quella con la
faccia; reel → 3 secondi con Andrea in movimento (spezzoni di `volto/clip/`, o la foto per i temi tristi) davanti al
reel e copertina con la faccia. Dettagli in `volto/README.md`.

## Come si pubblica (dal 24 ottobre 2026)

Primo commento in ogni post, reel anche come reel su Facebook, e dopo ogni post la storia su Instagram e Facebook
(`make_storia.py`, file in `posts/storie/`): `comunicazione/PUBBLICA.md`. Le cene di networking e le lezioni live
(il Premium) le promuove ogni giorno l'automazione descritta in `promo/README.md` (file in `posts/promo/`).
