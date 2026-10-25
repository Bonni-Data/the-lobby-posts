# Come si pubblica (decisione di Andrea del 24 ottobre 2026: «fai il possibile per renderlo virale»)

Vale per OGNI automazione che pubblica su Instagram e Facebook, insieme a `METODO.md` (il tono) e a `../volto/README.md`
(la faccia). Sono le leve che Metricool ci dà davvero: usale tutte, sempre, senza spendere nulla.

## 1. Il post

- **Gancio nelle prime righe.** Su Instagram si vedono circa 125 caratteri prima di «altro»: lì va la frase che
  fa fermare il pollice (domanda, luogo comune da smontare, «Tutti ne parlano. Pochi sanno come funziona.»).
- **Chiedi i segnali che contano.** L'algoritmo spinge i contenuti che vengono salvati, condivisi e mandati in privato
  (gli invii in DM sono il segnale più forte per arrivare a chi non ci segue). In ogni didascalia c'è un invito vero a
  una di queste azioni, variato ogni volta: «Salvalo per quando ti servirà», «Mandalo a chi ne parla senza sapere come
  funziona», «Taggane uno che deve saperlo».
- **Domanda ai commenti** (vedi METODO.md, punto 5): le domande migliori diventano il post di un altro giorno.
- **Hashtag:** esattamente 5, pertinenti, sempre #thelobby. Mai liste lunghe o hashtag generici.
- **Primo commento** (`firstCommentText` in createScheduledPost): SEMPRE. Una riga diversa ogni volta che apre la
  discussione o chiede di salvare e condividere, per esempio «📌 Salvalo: ti servirà prima di quanto pensi. E tu
  lo sapevi? Rispondi qui 👇» oppure «Mandalo a un amico che vuole entrare in politica: ve lo spiego in 5 minuti
  nell'app 👆». Niente link (Instagram non li rende cliccabili), niente hashtag in più, niente @ di persone.
- **Video:** `instagramData.type` "REEL" con `showReelOnFeed` true, `facebookData.type` "REEL" (su Facebook i reel
  arrivano a molte più persone dei video normali), `videoThumbnailUrl` = la copertina con il volto di Andrea (quella
  creata da faccia.py). Nei reel l'intro con Andrea in movimento la mette faccia.py da solo.
- **Orario:** l'orario della rubrica resta fisso (il ritmo riconoscibile fa parte del metodo, e il post delle 8:00
  non si sposta mai). Solo se una rubrica non ha un orario fisso, scegli l'ora migliore del giorno con
  getBestTimeToPostByNetwork (instagram, brand 7398010, Europe/Rome), mai a meno di 2 ore da un altro nostro post.
- **Mai:** sponsorizzazioni a pagamento (`boost`) senza l'ok scritto di Andrea e il budget; collaboratori
  (`collaborators`) senza l'ok di Andrea; audio di tendenza di terzi; account falsi, gruppi di rilancio, concorsi.

## 2. La storia, dopo ogni post (decisione di Andrea del 24 ottobre 2026)

Ogni volta che pubblichi un post, lo rilanci anche nella storia di Instagram e di Facebook.

1. **Immagine o video della storia, PRIMA del commit** (il generatore è `make_storia.py`; attenzione: `make_story.py` è un'altra cosa, la grafica del post del sabato):
   - post con immagini (post singolo o carosello): `python3 make_storia.py <la prima immagine del post> posts/storie/<AAAA-MM-GG>-<rubrica>.png`
     (per i caroselli aggiungi `--hint "Scorri il carosello sul profilo"`). Apri il file con Read: copertina ben visibile,
     testi non tagliati. Aggiungilo al commit del post (`git add posts/storie/...`).
   - reel: la storia è lo stesso video del reel (è già verticale), nessun file in più.
2. **Metricool**, subito dopo aver programmato il post: una seconda chiamata createScheduledPost con
   - `providers` [{"network":"instagram"},{"network":"facebook"}],
   - `media` = [indirizzo raw.githubusercontent.com con lo sha del commit dell'immagine della storia, o del video del reel],
   - `instagramData` {"type": "STORY", "autoPublish": true, "isAiGenerated": <come il post>}, `facebookData` {"type": "STORY"},
   - NESSUN campo `text` (le storie non hanno didascalia), `draft` false, `autoPublish` true,
   - data e `publicationDate` = 5 minuti dopo il post.
3. Controlla con getScheduledPosts che la storia risulti programmata. Se la creazione fallisce, riprova UNA volta; se
   fallisce ancora, il post resta valido: scrivilo nel resoconto e vai avanti.

## 3. Altre reti: TikTok, YouTube Shorts, Threads (piano del 25 ottobre 2026: «oltre i contatti che già ho»)

Sono le reti che mostrano i contenuti soprattutto a chi non ci segue. Si usano SOLO quando Andrea le ha collegate a
Metricool: prima di programmare, chiama getBrandSettings e guarda `networksData` del brand 7398010. Una rete che non
compare lì non va mai messa nei `providers` (Metricool rifiuterebbe tutto il post). Oggi (25/10) ci sono solo Instagram e
Facebook: finché è così, questa sezione non cambia niente.

- **Reel → TikTok e YouTube Shorts, nello stesso post.** Aggiungi ai `providers` del reel `{"network":"tiktok"}` e/o
  `{"network":"youtube"}`, con:
  - `tiktokData` {"title": <il gancio, al massimo 90 caratteri>, "privacyOption": "PUBLIC_TO_EVERYONE", "autoAddMusic": false,
    "isAigc": <come isAiGenerated del post>, "commercialContentOwnBrand": false, "commercialContentThirdParty": false};
  - `youtubeData` {"type": "short", "title": <il gancio, al massimo 100 caratteri>, "privacy": "public", "madeForKids": false,
    "category": "EDUCATION", "tags": <i 5 hashtag senza #>, "isAiGeneratedContent": <come isAiGenerated del post>}.
  - La didascalia (`text`) resta la stessa di Instagram. Su YouTube diventa la descrizione: va bene così.
- **Caroselli → TikTok in modalità foto**, nello stesso post: `{"network":"tiktok"}` con `tiktokData` come sopra e
  `"photoCoverIndex": 0` (la copertina con il volto di Andrea). Su YouTube i caroselli non vanno.
- **Threads → un post a parte, solo per «Dietro la notizia» delle 8:00**, programmato alle 8:05 con una seconda chiamata
  createScheduledPost: `providers` [{"network":"threads"}], `threadsData` {}, `media` = [la copertina 01.png del giorno,
  con il volto di Andrea], `text` al massimo 450 caratteri: il gancio, due righe su come funziona, il link alla pagina
  `https://thelobbyitalia.it/notizie/<data>-<slug>/` (su Threads i link si aprono), la riga delle tre promesse
  («Formazione per giovani politici, le migliori opportunità internazionali e networking con altri giovani di talento»).
  Niente hashtag in fila: al massimo uno (#thelobby).
- **Se Metricool rifiuta il post per colpa di una delle nuove reti**, rifallo subito senza quella rete: il post su
  Instagram e Facebook non deve mai saltare. Scrivi nel resoconto quale rete ha dato errore.
- **Piano gratuito di Metricool:** pubblica al massimo 20 post al mese. Se il calendario del mese è vicino al limite,
  il post a parte di Threads è il primo a saltare.
- **Canale Telegram:** non passa da Metricool. Lo pubblica ogni mattina l'automazione «Canale Telegram» del repository
  dell'app (vedi `the-lobby-app/docs/TELEGRAM.md`); qui non serve fare niente.

## 4. Cene e lezioni live

Le cene di networking e le lezioni live su Teams (il Premium, gratuito e su selezione) le promuove l'automazione
«Promo cene e lezioni live», che legge il calendario dell'app. Le altre rubriche possono citarle in una riga
(«In Premium ci sono le lezioni live con Andrea e le cene di networking»), mai con date o luoghi non confermati.
