# Il volto di Andrea (regola «faccia prima», dal 24 ottobre 2026)

**Tono e metodo:** leggi anche `comunicazione/METODO.md` (vincolante per tutte le rubriche).

Ogni contenuto mostra Andrea, in foto o in video, con 1-2 parole grandi accanto. Qui ci sono gli strumenti e le foto.

- `libreria/`: foto di Andrea già scontornate (PNG trasparente) + un `.json` per foto con il riquadro del viso,
  l'espressione e le rubriche adatte. `libreria/indice.json` riassume tutto: scegli la foto in base alla rubrica e
  non usare la stessa due giorni di fila.
- `scontorna.py foto.jpg uscita.png`: toglie lo sfondo a una foto nuova (modelli ONNX in ~/.u2net, da
  github.com/danielgatis/rembg/releases/v0.0.0: isnet-general-use.onnx e u2net_human_seg.onnx). Controlla sempre il
  risultato su fondo magenta: niente pezzi di altre persone, simboli, bandiere o scritte.
- `clip/`: spezzoni di 3 secondi di Andrea in movimento, già con lo sfondo di THE LOBBY e senza audio (decisione del
  24/10/2026: piace il formato video). `faccia.py` li mette da solo come intro dei reel al posto della foto, a
  rotazione (`clip/indice.json`); per i temi tristi (`"tono": "serio"`) usa la foto. Nuovi spezzoni solo con
  `clip_base.py`, controllando TUTTI i fotogrammi.
- `../make_face.py`: copertine post (1080x1350) e cover reel/storie (1080x1920). Opzioni utili: `side`, `face_h`,
  `face_x`, `face_shift`, `words_y` (per le foto in cui Andrea indica in alto: le parole sopra il dito), `card`
  (ritratti: la foto del personaggio in una cornice che Andrea presenta).
- `../make_face_reel.py`: reel dai video di Andrea (gancio, logo, nome, sottotitoli, fascia promesse, chiusura) o,
  se il video manca, dalla foto con zoom lento. `replace_bg: true` toglie lo sfondo del video e mette quello di
  THE LOBBY.

Mai: foto o video con simboli, sfondi, manifesti o messaggi di partito (anche se scontornati, se resta traccia),
riprese che rivelano cariche politiche (es. dirette del consiglio comunale), persone terze riconoscibili,
foto, video o voci di Andrea generati con l'IA.

Ogni foto ha un `tono` (serio, neutro, sorriso). Per le notizie tristi o delicate (cronaca, processi, lutti, guerre,
disastri) il lavoro di `faccia.py` mette `"tono": "serio"`; per i temi seri ma non tristi `"tono": "neutro"` (niente
sorrisi). «mani-aperte-1» è un fotogramma a mezzo busto (`face_h` 230 per far vedere le mani): ad Andrea piace molto
con «TE LO / SPIEGO». Le altre 5 foto ricavate il 24/10 (selfie in polo, selfie con il gilet, «sorpreso») le ha
scartate: non rimetterle.

Foto escluse il 24/10/2026 (non sono qui): santino elettorale, comizio con i simboli, grafica «Nuovo consigliere
comunale», foto di profilo con lo striscione, panel con altre persone in primo piano, foto con la mano di un'altra
persona sulla spalla, foto con la persona dietro sovrapposta; video del consiglio comunale e video davanti al logo.
Video del 24/10/2026: la story con l'articolo di giornale (rivela la carica) è esclusa del tutto; dal video davanti al
pannello dell'evento si usa solo il fotogramma scontornato «mani-aperte-1», controllato senza tracce del pannello; il
video con lo sfondo sostituito e senza audio è in prova (24/10, in attesa dell'ok di Andrea); il selfie in polo non si usa.
