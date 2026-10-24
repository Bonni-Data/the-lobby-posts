# Promo delle cene di networking e delle lezioni live (decisione di Andrea del 24 ottobre 2026)

Premium (gratuito, su selezione) comprende solo due cose: le **lezioni live su Microsoft Teams con Andrea** e le
**cene di networking**. Andrea vuole che si promuovano sui social. Lo fa l'automazione «THE LOBBY - Promo cene e
lezioni live», ogni giorno alle 13:4x: legge il calendario dell'app e, se oggi tocca, pubblica un carosello alle 15:00
(più la storia, vedi `../comunicazione/PUBBLICA.md`). Al massimo un promo al giorno.

## Quando

Calendario: `public.premium_events` (status 'published'), giorni contati sul calendario di Roma.

| Cosa | Quando si pubblica |
| --- | --- |
| Cena (`kind` 'cena', con data futura) | Annuncio la prima volta che compare (se mancano almeno 2 giorni), poi a 14, 7 e 2 giorni dalla data |
| Lezione live con data fissata (`kind` 'lezione', `starts_at` futuro) | Annuncio la prima volta che compare con quella data, poi a 7 giorni e il giorno prima |
| Lezioni live senza data («prenotazioni aperte») | Una ogni 14 giorni, a rotazione, solo nei giorni senza altri promo |

Priorità se ne toccano due nello stesso giorno: cena, poi lezione con data, poi prenotazioni aperte.
Non si pubblica se la cena è al completo (risposte «yes» in `event_rsvps` ≥ `seats`): si scrive nel resoconto.
Ogni promo pubblicato va in `../history-promo.json` (chiave: data di oggi) con `event_id`, `tipo` (annuncio,
-14, -7, -2, -1, prenotazioni), `titolo` e `file`.

## Cosa

Carosello di 2 immagini in `posts/promo/<AAAA-MM-GG>/`:
1. `01.png` con il volto di Andrea: `python3 faccia.py` con `{"mode": "post", "rubrica": "premium", "words": [...],
   "kicker": "Cena di networking" o "Lezione live", "sub": "<data · luogo · posti, max 45 caratteri>", "swipe": true}`.
   Parole vere e corte: CENA / CON ME?, ULTIMI / POSTI (solo se è vero), LIVE / SU TEAMS, PRENOTA / IL POSTO.
2. `02.png` con i dettagli: `python3 make_pill.py` con `{"label": "CENA DI NETWORKING" o "LEZIONE LIVE SU TEAMS",
   "course": "Premium · gratuito, su selezione", "title": "<max 70 caratteri>", "points": [3 righe vere: quando e
   dove (per le cene solo la città: il locale arriva a chi conferma), per chi e quanti posti, cosa succede e i costi
   (per le cene: ognuno paga la propria cena)], "takeaway": "Candidati dal link in bio" (o, per chi è già in Premium,
   "Rispondi presente nell'app"), "footer": "Premium è gratuito · thelobbyitalia.it"}`.

## Regole

- Solo fatti del calendario: data, ora (convertita in ora di Roma), città, posti, costi come sono scritti in
  `premium_events`. Mai inventare ospiti, locali, menu, posti rimasti o «ultimi posti» se non è vero.
- Le cene sono solo per maggiorenni in Premium: scrivilo sempre. Il locale esatto non si pubblica mai.
- Premium non si compra: «gratuito, su selezione, ti candidi dall'app e Andrea legge ogni candidatura».
- Tono e regole di sempre: `../comunicazione/METODO.md`, `../comunicazione/PUBBLICA.md`, `../volto/README.md`. Mai
  il partito di Andrea, le sue cariche, il suo lavoro. Nessuna sponsorizzazione a pagamento senza l'ok di Andrea.
