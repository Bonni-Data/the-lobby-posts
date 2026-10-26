# Come si pubblica (decisione di Andrea del 24 ottobre 2026: «fai il possibile per renderlo virale»)

Vale per OGNI automazione che pubblica sui social (Instagram, Facebook e le reti della sezione 3), insieme a `METODO.md` (il tono) e a `../volto/README.md`
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

## 3. Altre reti: TikTok, YouTube Shorts, Threads, LinkedIn

Decisioni di Andrea: il 25 ottobre 2026 «oltre i contatti che già ho»; il 26 ottobre 2026 ha attivato il piano Starter di
Metricool («usiamo tutte le funzionalità utili, tra cui voglio anche la pubblicazione dei contenuti su TikTok»). Con
Starter i post sono illimitati: nessun contenuto si salta per il numero di uscite del mese.

Queste reti mostrano i contenuti soprattutto a chi non ci segue. Si usano SOLO quando sono collegate al brand 7398010:
**prima di ogni createScheduledPost di un post o di un reel chiama getBrandSettings e guarda `networksData`.** Una rete
che non compare lì non va mai messa nei `providers` (Metricool rifiuterebbe tutto il post). Le storie restano solo su
Instagram e Facebook.

- **TikTok (quando c'è `tiktokData` in networksData), su TUTTO quello che esce nel feed:** reel e caroselli o post con
  immagini, nello stesso createScheduledPost di Instagram e Facebook. Aggiungi `{"network":"tiktok"}` ai `providers` e
  `tiktokData` {"title": <il gancio, al massimo 90 caratteri>, "privacyOption": "PUBLIC_TO_EVERYONE",
  "autoAddMusic": false, "disableComment": false, "disableDuet": false, "disableStitch": false,
  "isAigc": <come isAiGenerated del post>, "commercialContentOwnBrand": false, "commercialContentThirdParty": false}.
  Per i caroselli aggiungi `"photoCoverIndex": 0` (la copertina con il volto di Andrea). La didascalia (`text`) resta
  quella di Instagram. Niente musica di tendenza di terzi (vale anche su TikTok).
- **YouTube Shorts (quando c'è `youtubeData`), solo per i reel**, nello stesso post: `{"network":"youtube"}` con
  `youtubeData` {"type": "short", "title": <il gancio, al massimo 100 caratteri>, "privacy": "public", "madeForKids": false,
  "category": "EDUCATION", "tags": <i 5 hashtag senza #>, "isAiGeneratedContent": <come isAiGenerated del post>}.
- **Threads (quando c'è `threadsData`) → un post a parte, solo per «Dietro la notizia» delle 8:00**, programmato alle 8:05
  con una seconda chiamata createScheduledPost: `providers` [{"network":"threads"}], `threadsData` {}, `media` = [la
  copertina 01.png del giorno, con il volto di Andrea], `text` al massimo 450 caratteri: il gancio, due righe su come
  funziona, il link alla pagina `https://thelobbyitalia.it/notizie/<data>-<slug>/` (su Threads i link si aprono), la riga
  delle tre promesse («Formazione per giovani politici, le migliori opportunità internazionali e networking con altri
  giovani di talento»). Al massimo un hashtag (#thelobby).
- **LinkedIn (quando c'è `linkedinData`; deve essere la Pagina di THE LOBBY, mai il profilo personale di Andrea)**, nello
  stesso post, solo per «Dietro la notizia», il carosello del lunedì, il ritratto e le opportunità del martedì:
  `{"network":"linkedin"}` con `linkedinData` {"type": "post", "publishImagesAsPDF": true,
  "documentTitle": <il titolo della copertina, al massimo 60 caratteri>, "previewIncluded": true}. Il testo resta lo
  stesso. Se il brand mostra un profilo personale invece della pagina, non pubblicare su LinkedIn e scrivilo nel resoconto.
- **Se Metricool rifiuta il post per colpa di una delle nuove reti** (formato, durata, permessi), rifallo subito senza
  quella rete: il post su Instagram e Facebook non deve mai saltare. Scrivi nel resoconto quale rete ha dato errore e il
  messaggio.
- **Errori di limite del piano: non si recuperano** (decisione di Andrea del 26 ottobre 2026). I post andati in ERROR con
  «You have reached your Metricool account limit» (il 25 e il 26 ottobre 2026, prima del piano Starter) non vanno mai
  ripubblicati dal controllo dei giorni precedenti.
- **Canale Telegram:** non passa da Metricool. Lo pubblica ogni mattina l'automazione «Canale Telegram» del repository
  dell'app (vedi `the-lobby-app/docs/TELEGRAM.md`); qui non serve fare niente.

## 4. Cene e lezioni live

Le cene di networking e le lezioni live su Teams (il Premium, gratuito e su selezione) le promuove l'automazione
«Promo cene e lezioni live», che legge il calendario dell'app. Le altre rubriche possono citarle in una riga
(«In Premium ci sono le lezioni live con Andrea e le cene di networking»), mai con date o luoghi non confermati.
