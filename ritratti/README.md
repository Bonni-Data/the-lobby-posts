# Ritratti: la carriera di un personaggio politico, per ispirare

Decisione di Andrea del 19 ottobre 2026. Ogni settimana un carosello racconta la carriera di una persona
riconoscibile e influente nel mondo politico o istituzionale, come fonte di ispirazione: chi lo legge deve
pensare «ci è arrivata studiando e partendo dal basso, posso farlo anch'io» e venire su THE LOBBY a formarsi.
Si racconta il **percorso** (da dove è partita, i passaggi, cosa ha costruito, il metodo), **mai le idee**.

- **Settimanale:** ogni lunedì alle 13:00 (il primo è uscito lunedì 19 ottobre 2026 alle 21:00: Tina Anselmi).
- **Di riserva:** se un giorno nessun altro contenuto esce, la rete di sicurezza serale pubblica un ritratto in più.
  Al massimo 2 ritratti per settimana (da lunedì a domenica).
- Storico in `history-ritratti.json`, slide in `posts/ritratti/<AAAA-MM-GG>/`, dati in `data/ritratto-<AAAA-MM-GG>.json`.

## Chi scegliere (neutralità di THE LOBBY)

Ammessi:
- figure storiche della Repubblica, dell'Europa e del mondo;
- chi ricopre o ha ricoperto un ruolo istituzionale super partes (Presidente della Repubblica, presidenti delle
  istituzioni europee, segretari generali dell'ONU e simili);
- leader stranieri che non sono più in campagna elettorale.

Esclusi sempre:
- politici italiani oggi attivi in un partito, e chiunque sia candidato a elezioni in corso o imminenti;
- chi è stato condannato in via definitiva per reati gravi o ha avuto ruoli in regimi autoritari;
- qualsiasi riferimento al partito di Andrea, alle sue cariche o al suo lavoro.

Equilibrio: alterna un ritratto italiano e uno internazionale, mai due di fila della stessa area politica, e su
ogni 8 ritratti almeno 3 donne. Indica l'area nel campo `area` dello storico, per poterla controllare.

### Lista di partenza (si può allargare rispettando le regole)

| Nome | Paese | Area | Perché ispira |
| --- | --- | --- | --- |
| Tina Anselmi | Italia | cattolico-democratica | staffetta a 17 anni, prima donna ministra (fatto il 19/10/2026) |
| Simone Veil | Francia | liberale di centro | prima presidente del Parlamento europeo eletto dai cittadini |
| Sandro Pertini | Italia | socialista | dal confino alla presidenza della Camera e della Repubblica |
| Konrad Adenauer | Germania | cristiano-democratica | ricostruisce la Germania e fonda l'Europa |
| Nilde Iotti | Italia | comunista | prima donna presidente della Camera |
| Winston Churchill | Regno Unito | conservatrice | sconfitte, ritorni, la guida nella guerra |
| Luigi Einaudi | Italia | liberale | da economista a primo Presidente eletto dal Parlamento repubblicano |
| Nelson Mandela | Sudafrica | movimento di liberazione | 27 anni di carcere, poi presidente |
| Alcide De Gasperi | Italia | cattolico-democratica | ricostruzione e nascita dell'Europa |
| Roberta Metsola | Malta / UE | popolare europea | la più giovane presidente del Parlamento europeo |
| Teresa Mattei | Italia | comunista | la più giovane eletta all'Assemblea Costituente |
| Margaret Thatcher | Regno Unito | conservatrice | da figlia di un droghiere a prima donna premier britannica |
| Altiero Spinelli | Italia | federalista europea | il Manifesto di Ventotene scritto al confino |
| Willy Brandt | Germania | socialdemocratica | dal sindaco di Berlino al Nobel per la pace |
| Carlo Azeglio Ciampi | Italia | istituzionale | dalla Banca d'Italia al Quirinale |
| Angela Merkel | Germania | cristiano-democratica | dalla fisica alla cancelleria per 16 anni |
| Giorgio La Pira | Italia | cattolico-democratica | il sindaco di Firenze che parlava al mondo |
| Barack Obama | Stati Uniti | democratica | dal lavoro nei quartieri alla Casa Bianca |
| Sergio Mattarella | Italia | istituzionale | dal Parlamento alla Corte costituzionale al Quirinale |
| Robert Schuman | Francia | cristiano-democratica | la dichiarazione che fa nascere l'Europa unita |
| Jacques Delors | Francia | socialista europea | il mercato unico e l'euro |
| Kofi Annan | Ghana / ONU | istituzionale | dal primo impiego all'ONU al Nobel per la pace |
| Ronald Reagan | Stati Uniti | repubblicana | dal sindacato degli attori alla presidenza |
| Václav Havel | Rep. Ceca | dissidenza democratica | dal carcere alla presidenza |

## Come si fa

1. **Scelta:** il primo nome della lista non presente in `history-ritratti.json` che rispetti l'alternanza
   (italiano/internazionale, area diversa dall'ultimo, quota donne). Mai un nome già usato negli ultimi 12 mesi.
2. **Verifica:** ogni data, ruolo, numero ed età va confermato su almeno 2 fonti affidabili aperte con WebFetch
   (siti istituzionali: Camera, Senato, Quirinale, Parlamento europeo, Commissione, ONU, governi; archivi
   storici; agenzie e testate autorevoli). Le età si calcolano dalla data di nascita verificata. Nessuna
   citazione tra virgolette se non trovata identica su una fonte affidabile. Un fatto che non confermi non
   entra nel post.
3. **Carosello** (`data/ritratto-<data>.json` per `make_carousel.py`):
   - `kicker`: «RITRATTO DELLA SETTIMANA»;
   - `title` (max 60 caratteri): un gancio con le età, per esempio «A 17 anni faceva la staffetta. A 49 era ministra.»;
   - `subtitle` (max 70): nome e cognome e il primato o il ruolo per cui è riconoscibile;
   - da 5 a 6 slide di carriera: `tag` «ANNO · PASSAGGIO» (max 22), `title` (max 50), `text` (max 260),
     in ordine cronologico, dal punto di partenza più umile al ruolo più alto;
   - una slide finale `tag` «COSA IMPARI DA LEI» o «COSA IMPARI DA LUI»: il metodo (studio, gavetta, territorio,
     competenze, perseveranza) e sempre la frase «Le sue idee puoi condividerle o no: il metodo vale per tutti.»
     o una equivalente;
   - `cta`: {"title": "Inizia da qui.", "text": "Lezioni da 5 minuti, quiz e certificato. Gratis."};
   - `source`: «Fonti: ...» con le fonti usate.
   Esegui `python3 make_carousel.py data/ritratto-<data>.json posts/ritratti/<data>/` e apri TUTTE le slide con
   Read: niente testo tagliato o fuori margine, l'ultima slide mostra le tre promesse.
4. **Immagini:** solo il carosello tipografico. Nessuna foto della persona, nessuna immagine o video generato
   con l'IA che ritragga persone reali, nessun simbolo, logo o colore di partito.
5. **Didascalia:** il gancio; 2-3 righe sulla carriera; la riga fissa «Ogni settimana un ritratto: carriere di
   ogni colore politico, raccontate non per le idee ma per il percorso. Perché nessuno arriva lì per caso 💪»;
   una riga che collega a un corso gratuito di THE LOBBY pertinente (titolo esatto letto dal database); la riga
   «THE LOBBY: formazione per giovani politici, le migliori opportunità internazionali e networking con altri
   giovani di talento. Tutto gratis.»; «Entra dal link in bio 👆 o su thelobbyitalia.it»; un invito a salvare o
   condividere; «Fonti: ...»; esattamente 5 hashtag (#thelobby #ritratti più 3, tra cui il nome della persona).
6. **GitHub:** aggiungi la voce a `history-ritratti.json` e fai commit e push di dati, slide e storico.
7. **Metricool:** un post Instagram + Facebook di tipo POST con tutte le slide in ordine (diventa un carosello),
   `isAiGenerated` false, `mediaAltText` una descrizione per slide.

Formato dello storico:
`{"AAAA-MM-GG": {"nome": "...", "paese": "...", "area": "...", "genere": "donna|uomo", "motivo": "settimanale|riserva", "file": "posts/ritratti/AAAA-MM-GG/", "fonti": ["url", "url"]}}`
