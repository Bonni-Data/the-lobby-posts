# Email ai moltiplicatori (decisione di Andrea del 25 ottobre 2026: «falle partire senza mio ok»)

Le manda l'automazione «THE LOBBY - Email ai moltiplicatori» dal Gmail di Andrea, a piccoli gruppi nei giorni feriali.
I contatti stanno nella tabella `maint.outreach` del database (solo indirizzi pubblicati dagli enti sulle loro pagine
ufficiali, raccolti da `contatti.py`). Regole:

- Un'email per ente, mai due volte allo stesso indirizzo, nessun sollecito automatico.
- Prima di inviare, cerca in Gmail `to:<indirizzo>` negli ultimi 90 giorni: se c'è già un'email nostra, segna `esclusa`.
- Testo semplice (niente HTML, niente allegati, niente immagini), personalizzato con il nome dell'ente.
- Mai citare il partito di Andrea, le sue cariche o il suo lavoro. Tono neutrale.
- I numeri (opportunità aperte, lezioni) si leggono dal database il giorno stesso.
- Al massimo 35 invii al giorno, solo dal lunedì al venerdì, mai prima delle 9.

## Eurodesk e Informagiovani (`kind` = eurodesk)

Oggetto: Le opportunità per giovani verificate ogni mattina, in un'unica pagina gratuita

Buongiorno,

sono Andrea Bonazzi, fondatore di THE LOBBY, un'academy online gratuita e indipendente da qualsiasi partito, pensata per i giovani che vogliono capire come funzionano Comune, Stato ed Europa.

Vi scrivo perché ogni mattina verifichiamo sulle fonti ufficiali tirocini nelle istituzioni europee, concorsi, bandi, volontariato e viaggi con spese coperte dagli enti, e li raccogliamo gratis in un'unica pagina: https://thelobbyitalia.it/opportunita/

Oggi le opportunità aperte sono {N_OPPORTUNITA}, ognuna con requisiti, scadenza e link al bando ufficiale. Non organizziamo né finanziamo nulla: rimandiamo sempre alla pagina dell'ente che pubblica il bando.

Se la ritenete utile per i ragazzi che si rivolgono al punto Eurodesk di {ENTE}, siete liberi di consigliarla o di condividerla sui vostri canali. E se vi arriva un'opportunità che manca, rispondete pure a questa email: la verifichiamo e la aggiungiamo.

Grazie per il lavoro che fate ogni giorno con i giovani.

Andrea Bonazzi
THE LOBBY · https://thelobbyitalia.it

## Scuole secondarie di secondo grado (`kind` = scuola)

Oggetto: Educazione civica: {N_LEZIONI} lezioni gratuite su Costituzione, istituzioni ed Europa

Gentile Dirigente, gentili docenti dell'istituto «{ENTE}»,

sono Andrea Bonazzi, fondatore di THE LOBBY, un'academy online gratuita, senza pubblicità e indipendente da qualsiasi partito.

Abbiamo preparato {N_LEZIONI} lezioni da cinque minuti su Costituzione, istituzioni, Unione europea, economia e cittadinanza digitale, con domande di verifica, quiz, simulazioni e certificato finale. Seguono i nuclei delle Linee guida per l'educazione civica e si possono proiettare in classe. Le trovate divise per tema qui: https://thelobbyitalia.it/docenti/

Vi chiedo la cortesia di inoltrare questa email al referente per l'educazione civica e ai docenti di diritto e di storia, se lo ritenete utile. Ogni lezione indica le fonti ufficiali e la data dell'ultimo controllo; se trovate un errore o vi manca un tema, rispondete a questa email e lo prepariamo.

Grazie e buon lavoro,

Andrea Bonazzi
THE LOBBY · https://thelobbyitalia.it

## Agenzia Italiana per la Gioventù (`kind` = ente)

Oggetto: THE LOBBY: le opportunità per i giovani e la formazione civica, gratis in un unico posto

Buongiorno,

sono Andrea Bonazzi. Nel 2022 sono stato ambasciatore della Lombardia per l'Anno europeo dei giovani, nominato dall'Agenzia, ed è stata l'esperienza che mi ha fatto scoprire quante opportunità esistono per i giovani e quanto poco siano conosciute.

Da lì è nata THE LOBBY, un'academy online gratuita e indipendente da qualsiasi partito: lezioni da cinque minuti su Comune, Stato ed Europa e una pagina che ogni mattina raccoglie, verificate sulle fonti ufficiali, le opportunità aperte per i giovani (oggi {N_OPPORTUNITA}): https://thelobbyitalia.it/opportunita/

Ve la segnalo perché potrebbe essere utile ai ragazzi che si rivolgono all'Agenzia e alla rete Eurodesk. Non organizziamo né finanziamo nulla: rimandiamo sempre ai bandi ufficiali, compresi i vostri. Se vedete un errore o un'opportunità che manca, basta rispondere a questa email.

Un saluto e grazie,

Andrea Bonazzi
THE LOBBY · https://thelobbyitalia.it

## Media per studenti e docenti (`kind` = media)

Oggetto: Segnalazione: lezioni gratuite di educazione civica e opportunità europee per gli studenti

Gentile redazione,

vi segnalo THE LOBBY, un'academy online gratuita, senza pubblicità e indipendente da qualsiasi partito. Per i docenti abbiamo appena pubblicato una pagina con {N_LEZIONI} lezioni da cinque minuti divise secondo i nuclei delle Linee guida per l'educazione civica (Costituzione, istituzioni, Unione europea, economia, cittadinanza digitale), con quiz e certificato: https://thelobbyitalia.it/docenti/

Per gli studenti, ogni mattina raccogliamo e verifichiamo sulle fonti ufficiali tirocini UE, concorsi, bandi e viaggi con spese coperte dagli enti: https://thelobbyitalia.it/opportunita/

Se pensate possa interessare ai vostri lettori, sono a disposizione per ogni informazione.

Cordiali saluti,

Andrea Bonazzi
THE LOBBY · https://thelobbyitalia.it
