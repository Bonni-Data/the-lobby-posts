# Piano di crescita (decisione di Andrea del 3 novembre 2026)

Andrea, 3 novembre 2026: «i post non vanno virali e hanno zero interazione. Trova la soluzione e applicala […] fai
salire la pagina in qualsiasi modo […] sia su Facebook che su Instagram». Queste regole valgono per OGNI automazione
che pubblica e, dove sono in conflitto con il prompt dell'automazione, **prevalgono loro**. Restano validi tutti i
vincoli di sempre (METODO.md, PUBBLICA.md, volto/README.md, niente partito, cariche o lavoro di Andrea, niente spese).
**Attestato, mai «certificato»** (decisione di Andrea del 5 novembre 2026): alla fine dei corsi THE LOBBY rilascia un
«attestato di completamento», che non ha valore legale. In didascalie, slide, video, primo commento ed email scrivi sempre
«attestato» (es. «quiz e attestato»), anche dove il prompt dell'automazione dice «certificato»; mai «certificato»,
«certificazione», «diploma» o «riconosciuto», e mai crediti formativi o ore PCTO (li decide la scuola).
**Eventi, mai «Premium»** (decisione di Andrea del 7 novembre 2026): nell'app la sezione «Premium» si chiama ora «Eventi»
e contiene le cene di networking e le lezioni live su Teams con Andrea; l'accesso resta gratuito e su selezione, con la
candidatura che Andrea legge personalmente (dall'app, sezione Eventi). In didascalie, slide, storie, primo commento ed
email scrivi sempre «Eventi» / «gli eventi» («candidati agli eventi», «riservate a chi è ammesso agli eventi»), anche
dove il prompt dell'automazione dice «Premium»; mai la parola «Premium». Il resto non cambia (solo lezioni live e cene,
niente ospiti promessi).
Prima di pubblicare leggi anche `RISULTATI.md`: lo aggiorna ogni lunedì l'automazione «Crescita social» con i numeri
veri della settimana e le correzioni da fare.

## 0. Come si eseguono gli script e si leggono le fonti (dal 5 novembre 2026, vale prima di tutto il resto)

Dal 3 novembre le automazioni non pubblicavano più: nelle sessioni automatiche il controllo dei permessi **nega
l'esecuzione degli script del repository** («codice da repo esterno») e **WebFetch su indirizzi che non vengono da una
ricerca** (PROVENANCE_REQUIRED). Quindi, in tutte le automazioni, anche dove il prompt dice altro:
- **Repository**: se lo strumento add_repo non c'è, non serve: `git clone` e `git push` su main funzionano già.
- **Mai eseguire in sessione** `python3 make_*.py`, `faccia.py`, `cinema/render_assets.py` o altri
  script del repository, e non cercare giri alternativi (copiarli, incollarne il codice, `python3 -c`). Li esegue
  GitHub: scrivi i JSON dei dati come sempre (data/…, lavoro di faccia.py) e poi un **lavoro di render**
  `jobs/render/<AAAA-MM-GG>-<rubrica>-<n>.json` (n parte da 1) con TUTTI i passi in ordine, per esempio:
  `{"steps": [["make_carousel.py","data/notizia-2026-11-06.json","posts/notizie/2026-11-06/"],
  ["faccia.py","data/faccia-2026-11-06-notizia.json"],
  ["make_storia.py","posts/notizie/2026-11-06/01.png","posts/storie/2026-11-06-notizia.png","--hint","Scorri il carosello sul profilo"]]}`
  Gli argomenti sono gli stessi che il prompt dà per la riga di comando (percorsi relativi, mai `/` iniziale o `..`).
  Script ammessi: make_carousel.py, faccia.py, make_storia.py, make_story.py, make_pill.py, make_post.py,
  make_reel.py, make_face.py, estrai_fotogrammi.py, cinema/render_assets.py (make_slideshow.py non più: sezione 1).
  Per i reel veri metti sempre un passo estrai_fotogrammi.py (scrive i fotogrammi e `foglio.jpg`) e il file in `probe`.
- **Commit e push** dei JSON dei dati e del lavoro insieme, poi **aspetta il risultato**: lancia in background (Bash con
  run_in_background, il `sleep` in primo piano è bloccato) il ciclo
  `for i in $(seq 1 30); do git fetch -q origin main; git cat-file -e origin/main:jobs/render/<nome>.result.json && break; sleep 20; done`
  e attendi che finisca (di solito 2-4 minuti). Poi `git pull --rebase origin main`.
- **Controlli**: leggi `jobs/render/<nome>.result.json` (per ogni passo `exit` 0 e l'output dello script; in `probe`
  durata, 1080x1920, h264 e aac al posto di ffprobe) e apri con Read le immagini prodotte e i fotogrammi. Se va
  corretto qualcosa, cambia i dati e scrivi un nuovo lavoro `<n+1>` (mai riusare un nome: un lavoro con il
  result.json non viene rieseguito). I file prodotti li ha già salvati GitHub: per gli indirizzi
  raw.githubusercontent.com usa lo sha di `git log -1 --format=%H -- <file>`.
- Se dopo 10 minuti il result.json non c'è, scrivi un nuovo lavoro `<n+1>` una sola volta; se anche quello non arriva,
  non pubblicare e scrivilo nel resoconto.
- **Fonti web**: WebFetch solo su indirizzi apparsi nei risultati di WebSearch in questa sessione (cerca prima la
  notizia, poi apri il risultato). Se un'azione viene negata dal controllo dei permessi, non riprovarla in un altro
  modo: passa alla fonte successiva o scrivilo nel resoconto.
- Il resto non cambia: Metricool, Supabase, Gmail e la lettura dei file funzionano come prima.

## Cosa dicevano i numeri (Metricool, 13 ottobre - 3 novembre 2026)

- **Instagram**: 30 follower. I post del feed arrivano a 7-27 persone, quasi tutte già follower; i primi post
  (16-24 ottobre) arrivavano anche a 200-300 persone che non ci seguivano, poi la quota di non follower è crollata.
  I reel: 5-60 persone dal 21 ottobre in poi; **tempo medio di visione 2-4 secondi**: la gente scorre via durante
  l'intro (3 secondi sempre uguali) e il gancio ripetuto.
- **Facebook**: 167 follower. I post con immagini (album) arrivano a **1-9 persone**; i **reel a circa 200-280
  visualizzazioni l'uno**, sempre. Su Facebook il formato che funziona è il reel.
- **Copertine tutte uguali**: «Tutti ne parlano. Pochi sanno come funziona.» su ogni copertina, «CHI DECIDE?» 4 volte
  in una settimana: nel feed sembrano lo stesso post e non fermano il pollice.
- **Temi «politici»**: Instagram e Threads, per impostazione predefinita, non consigliano a chi non ti segue i
  contenuti su elezioni, leggi e temi sociali (si può cambiare solo dalle impostazioni di ogni utente). Le notizie su
  elezioni estere, partiti e leader non arrivano a nuove persone.

## 1. Un solo post per contenuto (decisione di Andrea del 10 novembre 2026)

Andrea, 10 novembre 2026: «Non lo voglio assolutamente come cosa che mi crei dei reel su delle immagini. Non mi serve a
niente. Tieni un singolo post per sé. Non ripubblicarlo più volte perché mi rovina il feed.» Quindi, in tutte le
automazioni e anche dove il prompt dice altro:
1. **Mai video o reel montati dalle immagini di un post**: niente `make_slideshow.py`, niente `reels/<data>-<rubrica>-slide.mp4`.
2. **Ogni contenuto esce una sola volta**: il post con immagini (carosello o post singolo) va su Instagram **e** su
   Facebook nello stesso createScheduledPost (`providers` [{"network":"instagram"},{"network":"facebook"}] più le
   altre reti della sezione 3 di PUBBLICA.md, `instagramData` {"type": "POST", ...}, `facebookData` {"type": "POST"}).
   Mai un secondo post, reel o Trial Reel con lo stesso contenuto, né subito né in un altro orario.
3. **La storia resta** su Instagram e Facebook come prima (non va nel feed).
4. I reel veri (Lo sapevi, Quiz lampo, Attualità: video nati come video) escono una volta, come reel su Instagram e Facebook.
5. La crescita si cerca con la copertina (sezione 2 e `volto/README.md`), il gancio, i temi e l'interazione, non
   moltiplicando i post.

## 2. Gancio e copertina: ogni giorno diversi

**Nuovo stile delle copertine (decisione di Andrea del 10 novembre 2026: «uno stile grafico più accattivante, più
marketing»)**: faccia.py fa da solo titolo enorme a tutta larghezza in alto, volto grande sotto e colore di fondo
secondo la rubrica (notizie corallo, opportunità, pillole e consiglio crema, il resto navy; le notizie tristi con
«tono» "serio" sempre navy), così il feed alterna i colori. Per sfruttarlo: in "words" la prima parola corta e
fortissima (meglio ancora un numero: «30», «34», «2.500€» diventano giganti), la seconda nel riquadro; "sub" una
frase concreta di massimo 45 caratteri. Non serve altro nel lavoro di faccia.py.

- Le 1-2 parole e la frase della copertina cambiano ogni volta. **Vietate le formule fisse**: «Tutti ne parlano. Pochi
  sanno come funziona.» non va più nelle copertine (al massimo, raramente, nella didascalia); «CHI DECIDE?» al massimo
  una volta ogni 7 giorni. faccia.py avvisa con «ATTENZIONE» se le parole sono già uscite nelle ultime 20 copertine:
  in quel caso cambiale.
- Il gancio promette qualcosa di concreto **per chi guarda**: soldi, tempo, un diritto, un'opportunità, una cosa che
  può fare da domani, un errore da evitare, o una sorpresa vera con un numero preciso («2.500 € al mese», «50.000
  firme», «60 giorni»). Mai clickbait falso.
- Parla prima della vita di chi guarda (studio, lavoro, casa, soldi, telefono, viaggi, sport, diritti), poi della
  regola. Il «come funziona» è il cuore, il fatto di cronaca è solo l'aggancio.

## 3. Reel: i primi 2 secondi decidono tutto

- Nel lavoro di faccia.py per i reel metti sempre `"sub"`: la frase del gancio, specifica di oggi, al massimo
  70 caratteri (es. «Il sindaco non sceglie i vigili. Ecco chi lo fa»). L'intro con il volto ora dura 1,8 secondi.
- Nel JSON di make_reel.py aggiungi `"skip_hook": true`: il gancio lo porta già l'intro con il volto, così il
  contenuto parte subito. Con skip_hook la durata scende di circa 2,5 secondi: i minimi di durata dei prompt si
  abbassano di 3 secondi (per esempio «tra 18 e 33» diventa «tra 15 e 33»).
- Meglio 15-25 secondi che 30: un video corto rivisto due volte vale più di uno lungo abbandonato.

## 4. Temi e parole che arrivano a nuove persone

- Nelle scelte del giorno, a parità di valore, preferisci i temi che toccano la vita di un 18-30enne in Italia
  (lavoro, stipendio, affitto, scuola e università, Erasmus e opportunità, tecnologia e AI, diritti, multe, tasse,
  sport con una regola dietro) alle notizie su elezioni estere, partiti e leader. Una notizia elettorale o di partito
  va bene solo se è LA notizia del giorno in Italia; anche allora il gancio parla della regola («come si conta un
  voto»), non di chi vince.
- Hashtag e prima riga: parole chiave che la gente cerca (educazione civica, diritti, lavoro, tirocini, Europa,
  opportunità, Erasmus, scuola). Evita #elezioni, #politica, #partiti nei post del feed (le storie e le lezioni
  restano neutrali come sempre).

## 5. Interazione a basso sforzo

- Ogni didascalia e ogni primo commento chiudono con una domanda a cui si risponde con **una parola o un numero**:
  «A o B?», «Scrivi 1, 2 o 3», «Sì o no?», «Lo sapevi? Scrivi SÌ o NO». Le domande aperte lunghe non le scrive nessuno.
- L'invito a mandare il post a un amico resta sempre, con un destinatario preciso («mandalo a chi fa la maturità
  quest'anno», «a chi cerca un tirocinio»): l'invio in privato è il segnale più forte per arrivare a chi non ci segue.

## 6. Cosa resta da fare ad Andrea (non si può fare in automatico)

- **TikTok** (Business): è la rete che mostra i video a chi non ti segue anche con zero follower. Quando è collegato
  in Metricool, tutte le automazioni lo usano già (PUBBLICA.md, sezione 3).
- Condividere i reel nelle sue storie personali e nei gruppi WhatsApp: i primi 30-60 minuti contano.
- Collaborazioni (post in collaborazione con il suo profilo personale o con associazioni): solo con il suo ok scritto.
