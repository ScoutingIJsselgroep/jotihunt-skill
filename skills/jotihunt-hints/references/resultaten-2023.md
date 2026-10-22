# Blinde test van de coach op editie 2023 (Pirates of the Caribbean)

Op 19 oktober 2026 is het volledige systeem (solver met `claude -p`, model Opus, skill zoals na de 2026-analyse) losgelaten op de hints van 2023. Het systeem had die hints nooit gezien: de skill bevat alleen 2024, 2025 en 2026.

## Opzet

- **Bron:** de feedpagina's van jotihunt.nl, gearchiveerd in de Wayback Machine op 21–25 oktober 2023, met 26 hints (11:00 za – 12:00 zo). Bijlagen per hint zijn gehaald uit de Wayback-snapshot die het dichtst na de publicatie lag, omdat namen als `jotihunt2023-files/Alpha.pdf` per hint opnieuw werden gebruikt.
- **Blind:** de links naar de uitleg zijn uit de hinttekst gehaald. De runs draaiden in een aparte testomgeving (kopie van `tools/` en de skill, eigen lege `hints/` en `verslagen/`), dus de positiecontrole zag alleen de 2023-antwoorden van eerdere runs en geen 2026-posities.
- **Draaien:** `solver.py --dry-run --parallel`, in publicatievolgorde, 3 tegelijk, maximaal 30 minuten per hint.
- **Lekcontrole:** één run (045) probeerde de oplossingspagina op te halen. Dat gaf een 404 in de Wayback Machine en de 2026-site op jotihunt.nl, dus er is niets gelekt. Andere webverzoeken waren bijlagen die in het archief ontbraken; die haalde de coach zelf alsnog op van de CDN of uit de Wayback Machine.
- **Beperking:** van 2023 zijn maar drie uitlegpagina's gearchiveerd (72, 81, 82). Hard gecontroleerd zijn die drie, plus hint 52, waar het coördinaat letterlijk in de docx van de organisatie staat. Voor de rest geldt alleen: is de lezing eenduidig en past de positie in de route van het team.

## Uitkomst

- **Hard gecontroleerd: 22 teamantwoorden, waarvan 21 goed.** Eén was fout, een afrondingsrandgeval van ~100 m.
  - 72 Piratenwet: 6 van 6 goed.
  - 81 The Curse of the Black Pearl: 6 van 6 goed (alle 17 munten nagekeken).
  - 52 Minecraft Hint: 6 van 6 goed. De docx gaat open met het wachtwoord van het bord in de wereld.
  - 82 De drietand van Davy Jones: 3 goed, Foxtrot 1580 i.p.v. 1581 (randgeval), Bravo niet gevonden, Charlie zonder tekst.
- **Richting:** waar te controleren (72, 81, 82, 52) was de richting goed. Bij de andere hints koos de coach steeds een type dat bij titel en materiaal past, ook bij typen die niet in de skill staan: Major-systeem, semafoor, internationale seinvlaggen, ternaire a/g/r-code, T9 in pigpen-vorm, emoji-sudoku, NumisBids-veiling, what3words uit misplaatste woorden, geocoin-trackable en wachtwoordborden in een Minecraft-wereld. De drie aankondigingen/handwerk-hints (32, 42, 49) herkende hij als zodanig.
- **Snelheid:** mediaan 3,6 minuten voor een volledige run (20 puzzels). Eén run duurde 25 minuten (35, hangende kaart-API) en twee liepen tegen de limiet van 30 minuten (38 zonder antwoord; 82 met een deelantwoord).
- **Geen antwoord:** 38 Aqua de Vida (oleaat op topokaart leggen, na 30 min nog zoekend) en 44 (de coach dacht dat de Minecraft-wereld niet gearchiveerd was, maar die stond nog op de CDN; de run van 52 vond hem wel).

## Per hint

Tijd = duur van de volledige run (richting, stappen en antwoord), niet de tijd tot het eerste bericht.

| # | Hint | Gepubliceerd | Tijd | Type volgens de coach | Uitkomst |
|---|---|---|---|---|---|
| 12 | Koersvast | za 11:00 | 3,4 min | Projectie vanaf het HQ met graden/km uit de video → plaatsnaam | 6 antwoorden; niet te controleren |
| 13 | Een stapel vragen aan Calypso | za 12:00 | 5,2 min | Quizformule (waarden tussen haakjes) → WGS84 → RD | Deels: X of Y open bij 3 teams. De organisatie meldde zelf dat Echo en Foxtrot fout waren; de route bevestigt dat Echo een uitschieter is |
| 17 | Alamala Sabi Casiri … | za 13:00 | 0,7 min | Dubbel binair (ASCII in ASCII) → telwoorden | 6 "zeker"; past in de routes |
| 26 | Diepzeekaart | za 14:10 | 6,3 min | Gele route op hexkaart; kleur onder schip/knik als hex → DEC | 5 antwoorden; Charlie/Delta mogelijk verwisseld |
| 32 | Vooraankondiging | za 14:45 | 0,6 min | Aankondiging Minecraft-wereld, geen puzzel | Terecht geen antwoord |
| 41 | Not all treasures are silver and gold | za 15:18 | 1,5 min | Geocoin-trackable LSBKW3; coördinaten in de beschrijving | 6 "zeker" (uit de bron) |
| 44 | Joshame Gibbs moest goed kijken … | za 16:00 | 3,3 min | Getallen verwijzen naar de Minecraft-wereld | **Geen antwoord**: wereld ten onrechte als ontbrekend beschouwd |
| 42 | Voorbereiding deel 2 | za 16:15 | 0,8 min | Tweede Minecraft-wereld, geen puzzel | Terecht geen antwoord |
| 52 | Minecraft Hint | za 17:00 | 2,1 min | Wachtwoordborden in de wereld → docx per team | **6/6 geverifieerd** (docx opent) |
| 22 | Thuis bij de piraten of bij Governor Swann? | za 18:00 | 6,7 min | Zeekaart = Gelderland, Port Royal = Het Loo, Tortuga = HQ → postcode | 6 postcodes; 2 met een alternatief |
| 35 | Up is Down | za 19:00 | 25,5 min | Antipode van coördinaten op Jamaica; straatnaam per punt | Deels, 3 punten gegokt. Overpass-API hing |
| 46 | Zeemafoor | za 20:00 | 3,8 min | Semafoor met pistolen in de video | 4 "zeker" (2 teams zonder video) |
| 49 | Jigidi puzzel | za 21:00 | 0,6 min | Handmatige actie | Juist doorverwezen |
| 73 | Piraat met de blues | za 22:00 | 5,7 min | Video + kleurwiel → cijfers (wit = 0 afgeleid) | 5 "zeker" |
| 45 | Quite some characters … | za 23:00 | 4,0 min | Personage + letterpositie → letterwaarde → stapeltellen | 4 zeker, 2 waarschijnlijk |
| 38 | Aqua de Vida | zo 00:20 | 30 min | Oleaat op topokaart → postcode | **Geen antwoord** (tijdslimiet) |
| 29 | Captain Hector Barbossa onthoudt het wel | zo 02:00 | 2,1 min | Major-systeem (Winkelmann) | 6 antwoorden, 4 met een ch/sh-alternatief |
| 64 | Silent Mary | zo 03:00 | 2,2 min | Zoek de verschillen, aantal = cijfer | Alleen Bravo (andere pdf's niet gearchiveerd) |
| 60 | Pirata Codex | zo 04:12 | 3,9 min | Emoji-sudoku → cijfers in N/E-formule | 5 antwoorden; Charlie komt in Frankrijk uit, dus daar zit een fout |
| 70 | La Lengua Perdida | zo 05:03 | 2,4 min | T9-toetsen als pigpen-hoekjes → adres | 6 adressen, "zeker" |
| 67 | The Stuttering Parrot | zo 06:04 | 1,2 min | Ternaire code a/g/r, 3 tekens per letter → straatnaam | 4 straten; Alpha 'strokelweg vier' sluit aan op hint 80 |
| 80 | De Schrik van de zeven Zeeën | zo 07:07 | 1,7 min | Internationale seinvlaggen (letters + cijferwimpels) | Alleen Alpha (andere plaatjes niet gearchiveerd); consistent met 67 |
| 39 | De zeven zeeën | zo 08:06 | 6,3 min | Havenstad → breedteband op de wereldkaart → cijfer | 6 antwoorden, 4 "waarschijnlijk" |
| 81 | The Curse of the Black Pearl | zo 09:03 | 8,4 min | Muntloten in NumisBids-veiling 70; weggepoetst cijfer | **6/6 geverifieerd** |
| 82 | De drietand van Davy Jones | zo 10:09 | 30 min | what3words uit drie misplaatste woorden per verhaal | 3 goed, 1 randgeval fout, Bravo niet gevonden |
| 72 | Piratenwet | zo 12:00 | 1,5 min | Artikelen van Low/Lowther, I–X = 1…0 | **6/6 geverifieerd** |

## Wat dit zegt over het systeem

1. **Patroonherkenning werkt ook op een onbekende editie.** De meeste typen kwamen niet uit de skill maar uit algemene kennis plus de titel. Waar het hard te controleren was (22 teamantwoorden), klopte op één afrondingsrandgeval na alles. Voor de overige hints is dat niet te bewijzen, omdat de uitleg niet gearchiveerd is.
2. **Het systeem helpt zichzelf aan ontbrekend materiaal:** bijlagen van de CDN en uit de Wayback Machine, lotpagina's op NumisBids, een Minecraft-wereld uitlezen. Maar niet consequent: dezelfde wereld was voor run 44 "niet beschikbaar" en voor run 52 wel. Regel: eerst de CDN proberen, dan de Wayback Machine, en pas daarna "ontbreekt" concluderen.
3. **Er zit nog 2026-kennis in de prompt.** `COACH_REGELS` in `tools/solver.py` zegt "Alpha zit vaak rond X 1500"; in 2023 liet de coach zich daar even door afleiden ("Alpha zit bij Doornspijk, niet rond X 1500"). Dat soort editiespecifieke feiten hoort in de skill (per editie), niet in de vaste prompt.
4. **Geen tijdsbudget per hint.** Drie runs duurden 25–30+ minuten (hangende Overpass-API, eindeloos oleaat passen, combinaties proberen). Een budget van ~15 minuten, met daarna "post wat je hebt en stop of ga in de achtergrond verder", zou de 20-minutengrens beschermen. Bij een time-out bleef ook een `claude`-proces draaien (de solver start ze in een eigen procesgroep), dus de solver moet zijn kinderen zelf opruimen.
5. **RD-afronding:** omrekenen in het hoofd gaf bij 82 1580 in plaats van 1581 (het vakje lag 0,3 m van de grens). Altijd `jh.py wgs2rd` gebruiken en randgevallen melden.
