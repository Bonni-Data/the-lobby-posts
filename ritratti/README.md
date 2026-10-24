# Ritratti: la carriera di un personaggio politico, per ispirare

Decisione di Andrea del 19 ottobre 2026. Ogni settimana un carosello racconta la carriera di una persona
riconoscibile e influente nel mondo politico o istituzionale, come fonte di ispirazione: chi lo legge deve
pensare «ci è arrivata studiando e partendo dal basso, posso farlo anch'io» e venire su THE LOBBY a formarsi.
Si racconta il **percorso** (da dove è partita, i passaggi, cosa ha costruito, il metodo), **mai le idee**.

- **Settimanale:** ogni lunedì alle 13:00 (il primo è uscito lunedì 19 ottobre 2026 alle 21:00: Tina Anselmi).
- **Di riserva:** se un giorno nessun altro contenuto esce, la rete di sicurezza serale pubblica un ritratto in più.
  Al massimo 2 ritratti per settimana (da lunedì a domenica).
- Storico in `history-ritratti.json`, slide e foto in `posts/ritratti/<AAAA-MM-GG>/`, dati in `data/ritratto-<AAAA-MM-GG>.json`.

## Chi scegliere: tutte le fazioni, a rotazione

Andrea vuole anche i politici in attività, di **tutti gli schieramenti** (decisione del 19 ottobre 2026). La
neutralità di THE LOBBY sta nell'equilibrio: nel tempo ogni area politica ha lo stesso spazio, e di ognuno si
racconta solo il percorso.

Ammessi: politici in attività, italiani e stranieri, di qualunque partito; figure storiche; figure istituzionali.

Esclusi sempre:
- chi è stato condannato in via definitiva per reati gravi o ha avuto ruoli in regimi autoritari;
- chi è candidato a un'elezione che si tiene nei prossimi 30 giorni (per non sembrare propaganda elettorale):
  si passa al nome successivo e lo si recupera dopo il voto;
- qualsiasi riferimento al partito di Andrea come suo, alle sue cariche o al suo lavoro.

Regole di equilibrio (vincolanti):
- segui l'ordine della lista qui sotto: si prende il primo nome non ancora usato, saltando solo chi è escluso;
- alterna sempre un ritratto italiano e uno estero, mai due di fila della stessa area politica;
- su ogni 8 ritratti almeno 3 donne;
- tra i politici italiani in attività, nessun partito ha un secondo ritratto prima che tutti i principali partiti
  presenti in Parlamento abbiano avuto il loro;
- se aggiungi nomi alla lista, mantieni lo stesso equilibrio tra destra, centro e sinistra.
Nello storico scrivi `area`, `partito` (per chi è in attività) e `stato` («in attività», «ex», «storica»), così
l'equilibrio si può controllare.

### Ordine dei ritratti

| # | Nome | Paese | Area | Stato |
| --- | --- | --- | --- | --- |
| 1 | Tina Anselmi | Italia | centro (cattolico-democratica) | storica, fatto il 19/10/2026 |
| 2 | Roberta Metsola | Malta / UE | centrodestra (popolari europei) | in attività |
| 3 | Elly Schlein | Italia | centrosinistra (PD) | in attività |
| 4 | Simone Veil | Francia | centro (liberale) | storica |
| 5 | Giorgia Meloni | Italia | destra (FdI) | in attività |
| 6 | Willy Brandt | Germania | sinistra (socialdemocratica) | storica |
| 7 | Antonio Tajani | Italia | centrodestra (FI) | in attività |
| 8 | Emmanuel Macron | Francia | centro (liberale) | in attività |
| 9 | Sandro Pertini | Italia | sinistra (socialista) | storica |
| 10 | Angela Merkel | Germania | centrodestra (CDU) | ex |
| 11 | Giuseppe Conte | Italia | M5S | in attività |
| 12 | Margaret Thatcher | Regno Unito | destra (conservatrice) | storica |
| 13 | Nilde Iotti | Italia | sinistra (PCI) | storica |
| 14 | Konrad Adenauer | Germania | centrodestra (CDU) | storica |
| 15 | Matteo Salvini | Italia | destra (Lega) | in attività |
| 16 | Barack Obama | Stati Uniti | centrosinistra (democratici) | ex |
| 17 | Carlo Calenda | Italia | centro (Azione) | in attività |
| 18 | Winston Churchill | Regno Unito | destra (conservatrice) | storica |
| 19 | Teresa Mattei | Italia | sinistra (PCI) | storica |
| 20 | Ursula von der Leyen | Germania / UE | centrodestra (popolari europei) | in attività |
| 21 | Alcide De Gasperi | Italia | centro (DC) | storica |
| 22 | Nelson Mandela | Sudafrica | sinistra (ANC) | storica |
| 23 | Emma Bonino | Italia | centro (+Europa) | in attività |
| 24 | Ronald Reagan | Stati Uniti | destra (repubblicani) | storica |
| 25 | Un leader di AVS (Angelo Bonelli o Nicola Fratoianni) | Italia | sinistra (AVS) | in attività |
| 26 | Jacques Delors | Francia | sinistra (socialisti europei) | storica |
| 27 | Matteo Renzi | Italia | centro (Italia Viva) | in attività |
| 28 | Kofi Annan | Ghana / ONU | istituzionale | storica |
| 29 | Maurizio Lupi | Italia | centrodestra (Noi Moderati) | in attività |
| 30 | Václav Havel | Rep. Ceca | centro (dissidenza democratica) | storica |
| 31 | Sergio Mattarella | Italia | istituzionale | in carica |
| 32 | Jacinda Ardern | Nuova Zelanda | centrosinistra (laburisti) | ex |

Finita la lista, si ricomincia con nomi nuovi scelti con le stesse regole (mai la stessa persona entro 12 mesi).

## Come si fa

1. **Scelta:** il primo nome della lista non presente in `history-ritratti.json`, con le regole qui sopra.
2. **Verifica:** ogni data, ruolo, numero ed età va confermato su almeno 2 fonti affidabili aperte con WebFetch
   (siti istituzionali: Camera, Senato, Quirinale, governo, Parlamento europeo, Commissione, ONU, governi esteri;
   archivi storici; agenzie e testate autorevoli). Per chi è in attività verifica anche il ruolo di oggi. Le età si
   calcolano dalla data di nascita verificata. Nessuna citazione tra virgolette se non trovata identica su una
   fonte affidabile. Un fatto che non confermi non entra nel post.
3. **Foto** (con licenza libera, da Wikimedia Commons):
   - crea `ritratti/foto/<data>.json` = `{"name": "<nome e cognome>", "wikidata": "<Q-id se lo conosci>", "file": "", "output": "posts/ritratti/<data>/foto"}`,
     poi commit e push su main: la GitHub Action «Foto ritratto» cerca la foto ufficiale su Wikidata, la categoria
     Commons della persona e la ricerca per nome, tiene solo pubblico dominio, CC0, CC BY e CC BY-SA con lato
     corto di almeno 600 px, e salva fino a 4 candidate (`foto-1.jpg` ...) con `foto.json` (autore, licenza,
     riga di credito). In 1-2 minuti: aspetta con `git fetch -q origin main` e
     `git cat-file -e origin/main:posts/ritratti/<data>/foto.json` ogni 15 secondi, al massimo 6 minuti, poi `git pull --rebase`;
   - apri le candidate con Read e scegli quella in cui la persona è riconoscibile e protagonista: scarta foto di
     dipinti, statue, manifesti, tombe, targhe, gruppi in cui non si capisce chi è, e foto che la ritraggono in
     modo sgradevole o in contesti di partito con simboli in primo piano;
   - se nessuna va bene puoi indicare in `"file"` un file preciso trovato su commons.wikimedia.org con WebSearch
     e rilanciare (togli prima `foto.json`); se ancora niente, fai il carosello senza foto e scrivilo nel resoconto.
4. **Carosello** (`data/ritratto-<data>.json` per `make_carousel.py`):
   - `kicker`: «RITRATTO DELLA SETTIMANA»;
   - `title` (max 60 caratteri): un gancio con le età, per esempio «A 17 anni faceva la staffetta. A 49 era ministra.»;
   - `subtitle` (max 70): nome e cognome e il primato o il ruolo per cui è riconoscibile;
   - `photo`: il percorso della candidata scelta; `photo_credit`: il suo `credit` + « (ritagliata)»;
     `photo_focus_x` (0-1, dove sta il volto in orizzontale), `photo_zoom` (1-1.6) e `photo_focus` (0-1 in
     verticale) per inquadrare bene il volto nella parte alta della copertina;
   - da 5 a 6 slide di carriera: `tag` «ANNO · PASSAGGIO» (max 22), `title` (max 50), `text` (max 260), in ordine
     cronologico, dal punto di partenza al ruolo di oggi o più alto;
   - una slide finale `tag` «COSA IMPARI DA LEI» o «COSA IMPARI DA LUI»: il metodo (studio, gavetta, territorio,
     competenze, perseveranza) e sempre la frase «Le sue idee puoi condividerle o no: il metodo vale per tutti.»
     o una equivalente;
   - `cta`: {"title": "Inizia da qui.", "text": "Lezioni da 5 minuti, quiz e certificato. Gratis."};
   - `source`: «Fonti: ...» con le fonti usate.
   Esegui `python3 make_carousel.py data/ritratto-<data>.json posts/ritratti/<data>/`.
   **Copertina «faccia prima»** (decisione di Andrea del 24 ottobre 2026): la copertina 01.png si rifà con il volto
   di Andrea che presenta la foto del personaggio. Crea `data/faccia-<data>.json` =
   `{"mode": "post", "rubrica": "ritratti", "words": ["PRIMA", "MINISTRA"], "kicker": "Ritratto della settimana",
   "card": {"photo": "posts/ritratti/<data>/foto-N.jpg", "label": "<nome e cognome>", "credit": "<photo_credit>",
   "focus_x": 0.5, "focus_y": 0.3, "zoom": 1.4}, "swipe": true, "out": "posts/ritratti/<data>/01.png"}` (le 1-2
   parole, max 10 lettere l'una, dicono il primato o il ruolo in modo vero; `focus_x`/`focus_y` = dove sta il volto
   del personaggio nella sua foto, da 0 a 1) ed esegui `python3 faccia.py data/faccia-<data>.json`.
   Apri TUTTE le slide con Read: in copertina il volto del personaggio ben inquadrato nella cornice, il suo nome e il
   credito della foto leggibili, Andrea ben visibile; niente testo tagliato; l'ultima slide mostra le tre promesse.
5. **Mai** immagini o video generati con l'IA che ritraggano persone reali (nemmeno Andrea: di lui solo le foto vere di `volto/libreria/`), mai loghi o simboli di partito messi
   in evidenza dalla grafica, mai foto con licenze NC, ND o senza licenza.
6. **Didascalia:** il gancio; 2-3 righe sulla carriera; la riga fissa «Ogni settimana un ritratto: carriere di
   ogni colore politico, raccontate non per le idee ma per il percorso. Perché nessuno arriva lì per caso 💪»;
   una riga che collega a un corso gratuito di THE LOBBY pertinente (titolo esatto letto dal database); la riga
   «THE LOBBY: formazione per giovani politici, le migliori opportunità internazionali e networking con altri
   giovani di talento. Tutto gratis.»; «Entra dal link in bio 👆 o su thelobbyitalia.it»; un invito a salvare o
   condividere; «Fonti: ...»; «Foto: <autore>, <licenza>, via Wikimedia Commons (ritagliata). La persona ritratta
   non ha legami con THE LOBBY.»; esattamente 5 hashtag (#thelobby #ritratti più 3, tra cui il nome della persona).
7. **Storia e GitHub:** prima del commit crea la storia (vedi `../comunicazione/PUBBLICA.md`):
   `python3 make_storia.py posts/ritratti/<data>/01.png posts/storie/<data>-ritratto.png --hint "Scorri il carosello sul profilo"`
   (`make_storia.py`, non `make_story.py`) e aprila con Read. Poi aggiungi la voce a `history-ritratti.json` e fai
   commit e push di dati, slide, foto, storico, `data/faccia-<data>.json`, `volto/uso.json` e
   `posts/storie/<data>-ritratto.png`.
8. **Metricool:** un post Instagram + Facebook di tipo POST con tutte le slide in ordine (diventa un carosello),
   `isAiGenerated` false, `mediaAltText` una descrizione per slide. Negli indirizzi delle slide usa il commit appena
   pubblicato al posto di `main` (`https://raw.githubusercontent.com/Bonni-Data/the-lobby-posts/<sha del commit>/posts/ritratti/<data>/01.png`),
   così Metricool prende sempre la versione giusta. Sempre `firstCommentText` (un primo commento come spiega
   `../comunicazione/PUBBLICA.md`, senza link). Poi la storia: seconda chiamata con `posts/storie/<data>-ritratto.png`,
   `instagramData` {"type": "STORY"}, `facebookData` {"type": "STORY"}, senza testo, 5 minuti dopo il post.

Formato dello storico:
`{"AAAA-MM-GG": {"nome": "...", "paese": "...", "area": "...", "partito": "...", "stato": "in attività|ex|storica", "genere": "donna|uomo", "motivo": "settimanale|riserva", "file": "posts/ritratti/AAAA-MM-GG/", "foto": {"file": "...", "autore": "...", "licenza": "..."}, "fonti": ["url", "url"]}}`
