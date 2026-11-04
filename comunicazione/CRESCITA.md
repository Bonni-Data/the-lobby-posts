# Piano di crescita (decisione di Andrea del 3 novembre 2026)

Andrea, 3 novembre 2026: «i post non vanno virali e hanno zero interazione. Trova la soluzione e applicala […] fai
salire la pagina in qualsiasi modo […] sia su Facebook che su Instagram». Queste regole valgono per OGNI automazione
che pubblica e, dove sono in conflitto con il prompt dell'automazione, **prevalgono loro**. Restano validi tutti i
vincoli di sempre (METODO.md, PUBBLICA.md, volto/README.md, niente partito, cariche o lavoro di Andrea, niente spese).
Prima di pubblicare leggi anche `RISULTATI.md`: lo aggiorna ogni lunedì l'automazione «Crescita social» con i numeri
veri della settimana e le correzioni da fare.

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

## 1. Video ovunque (Facebook reel + Trial Reel di Instagram)

Per OGNI post con immagini (carosello o post singolo: notizia, lezione in slide, ritratto, opportunità, pillola,
sabato, promo, riserva):
1. **Prima del commit**, monta il video dalle immagini del post, nello stesso ordine (copertina con il volto per prima):
   `python3 make_slideshow.py <cartella o PNG in ordine> reels/<AAAA-MM-GG>-<rubrica>-slide.mp4` (scrive anche
   `...-slide-cover.jpg`). Controlli: ffprobe 1080x1920, h264 e aac; estrai 2 fotogrammi (-ss 1 e 1 secondo prima della
   fine) e aprili con Read. Aggiungi video e copertina al commit del post.
2. **Instagram, post con immagini**: resta come prima, ma nei `providers` del post NON metti Facebook.
3. **Il video, in DUE createScheduledPost separate** (stessi campi in tutte e due: `media` = [indirizzo
   raw.githubusercontent.com con lo sha del video], `videoThumbnailUrl` = indirizzo della sua copertina, `text` = la
   stessa didascalia (puoi accorciarla: restano gancio, contenuto, tre promesse, link in bio, invito, 5 hashtag),
   `firstCommentText` = una domanda con risposta di una parola, `mediaAltText`, `draft` false, `autoPublish` true):
   a) **Facebook**: `providers` [{"network":"facebook"}], `facebookData` {"type": "REEL"}, data = 2 minuti dopo il post.
   b) **Instagram**: `providers` [{"network":"instagram"}], `instagramData` {"type": "REEL", "autoPublish": true,
      "isAiGenerated": <come il post>, "showReelOnFeed": true}. **Mai `TRIAL_REEL`**: Instagram concede i Trial Reel
      solo agli account con almeno 1.000 follower; il 4 novembre 2026 Metricool l'ha rifiutato con «Trial Reel Not
      Enough Followers». Orario: almeno 4 ore dopo il post, nel primo di questi orari che è libero, oggi o domani:
      **12:40, 13:40, 21:10** (ora di Roma). Libero vuol dire che getScheduledPosts (da 45 minuti prima a 45 minuti
      dopo) non mostra un altro post o reel su Instagram (le storie non contano). Esempi: la notizia delle 8:00 → 12:40
      dello stesso giorno; il promo delle 15:00 → 21:10; un post delle 18:00 o delle 19:00 → 12:40 del giorno dopo (o
      13:40 se alle 12:40 c'è già la notizia). Così chi ci segue non vede lo stesso contenuto due volte di fila e il
      reel ha una seconda occasione di arrivare a chi non ci segue (scheda Reels ed Esplora).
   Se una delle due programmazioni fallisce, riprova una volta, poi scrivilo nel resoconto. Quando Instagram supera
   i 1.000 follower, l'automazione «Crescita social» lo scrive in RISULTATI.md e il punto b torna `TRIAL_REEL`.
4. **La storia** resta su Instagram e Facebook, come prima.
5. Se il video non si monta (errore due volte), su Facebook pubblica il post con immagini come prima e scrivilo.

I reel (Lo sapevi, Quiz lampo, Attualità) restano reel su Instagram e Facebook come prima.

## 2. Gancio e copertina: ogni giorno diversi

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
