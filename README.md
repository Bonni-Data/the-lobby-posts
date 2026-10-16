# the-lobby-posts

Grafiche settimanali di THE LOBBY (post Instagram/Facebook).

- `make_post.py`: genera il PNG 1080x1350 da un JSON (`python3 make_post.py dati.json out.png`)
- `history.json`: voci già usate nelle ultime edizioni (per non ripeterle)
- `posts/AAAA-MM-GG.png`: grafiche pubblicate, con indirizzo pubblico per Metricool

- `make_pill.py`: pillola formativa del giovedì (`history-pillole.json`)
- `make_story.py`: post «Scopri THE LOBBY» del sabato, impaginazione `brand` o `founder` con la foto in `assets/andrea-cut.png` (`history-storie.json`)

- `make_carousel.py`: carosello del lunedì, da 4 a 9 slide 1080x1350 (`python3 make_carousel.py dati.json posts/caroselli/AAAA-MM-GG/`), storico in `history-caroselli.json`
- `make_reel.py`: reel 1080x1920 di 18-30 secondi con musica sintetizzata (nessun brano di terzi) e copertina `-cover.jpg`
  (`python3 make_reel.py dati.json reels/AAAA-MM-GG.mp4`); formati `fact` (Lo sapevi?, mercoledì), `quiz` (Quiz lampo, venerdì),
  `news` (Attualità in 30 secondi, domenica); storico in `history-reel.json`
