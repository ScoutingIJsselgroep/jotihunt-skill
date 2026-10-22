---
name: jotihunt-hints
description: Solve and coach Jotihunt hints (the yearly Scouting Gelderland fox hunt) — decode the hourly cryptic hint per fox team (Alpha–Hotel, Oscar) into a Dutch RD grid coordinate (XXXX YYYY) or answer word. Use whenever the user mentions Jotihunt, vossenjacht, a hint for the vossen/fox teams, RD/Rijksdriehoek coordinates from a puzzle, or pastes a puzzle with per-team parts (Alpha:, Bravo:, …). Contains the puzzle catalogue of 2024–2026 with solution methods, a recognition guide, code tables (KIX, Kenny, Hexahue, 7-segment, resistor colours, Gaelic numbers), pitfalls, and scripts/jh.py with decoders and RD conversion.
---

# Jotihunt-hints oplossen en coachen

Kennisbasis voor de uur-hints van de Jotihunt (jaarlijkse vossenjacht van Scouting Gelderland, derde weekend van oktober). Gebaseerd op alle hints van 2025 (Lord of the Rings, met de gepubliceerde uitleg), een blinde test op 2024 (LEGO) en de live gevolgde editie 2026 (Brave / Schotland). De inhoud is Nederlands, net als het spel.

## Zo help je de gebruiker

- **Puzzelen moet leuk blijven.** Geef hulp gefaseerd en laat de gebruiker kiezen hoeveel: eerst de **richting** (puzzeltype, waarom, een snelle check, bron/tabel), dan op verzoek de **stappen** (hoe lees je het, één team voorgedaan, de overige teams, controle), en pas als gevraagd het **antwoord** per team met zekerheid. Zet richting/stappen/antwoord achter spoilers als het in een chat of Discord komt.
- **Eerst de richting delen, dan rekenen.** Een vermoeden is al waardevol; wacht niet tot alles is uitgewerkt.
- **Reken met `scripts/jh.py`** (pad relatief aan de map van deze skill), niet uit het hoofd: `python3 <skillmap>/scripts/jh.py --help`.
- **Wees eerlijk over zekerheid.** AI-antwoorden zijn overtuigend maar kloppen vaak niet helemaal; controleer altijd bereik, deelgebied en de vorige positie van het team (zie §1 en §8).
- Antwoordformaat volgt de hint: meestal `XXXX YYYY`, maar 2×5 cijfers als de hint die oplevert, of een woord.

## 1. Spelcontext (wat je moet weten voordat je begint)

- **Vossenteams**: Alpha, Bravo, Charlie, Delta, Echo, Foxtrot, Golf, Hotel (lopend/fiets in een eigen deelgebied) en **Oscar** (het OV-team, reist per trein/bus door Gelderland; soms "Oscar Victor" genoemd).
- **Elk uur één hint** (zaterdag 10:00 – zondag 12:00). Eén hintbericht bevat meestal **per team een eigen deelhint** ("Alpha: …", "Bravo: …"). Een `-` of `--` bij een team betekent: geen hint voor dat team dit uur (team inactief/verplaatst).
- **Antwoord = coördinaat van 8 cijfers** in het formaat `1234 5678`. Dit zijn **Rijksdriehoekscoördinaten (RD) op 100 m**: X-coördinaat eerste 4 cijfers (van de 6), Y-coördinaat eerste 4 cijfers. Voorbeeld: HQ Jotihunt RD `188362 440722` → hint-antwoord `1883 4407`.
  - Plausibiliteit Gelderland: **X tussen ~1450 en ~2650, Y tussen ~4100 en ~5000**. Eerste cijfer van X is vrijwel altijd 1 of 2, eerste cijfer van Y is 4 (heel soms 5 bij 't Harde/Hattem, Y 4970–4990 komt voor). In 2026 zat Alpha de hele dag rond X 1500–1580 (Tiel/Rhenen) en Hotel rond X 2250–2300, Charlie rond Y 4970–4980. Een te krappe grens (1600) heeft in 2026 een juiste decodering bijna gekost. Gebruik het bereik als check én als hulpmiddel bij het kraken (de "4" van Y en de "1"/"2" van X zijn vaak bekend).
  - **Sterkere check: de vorige positie van hetzelfde team.** Vossen lopen; per uur verplaatsen ze zich hooguit enkele km (een "grote verplaatsing" per speelhelft uitgezonderd). Vergelijk een nieuw coördinaat dus met het antwoord van het vorige uur voor dat team (eigen aantekeningen of het antwoord dat je team vorig uur instuurde). Een twijfelcijfer of twijfelbit kies je zo vaak met zekerheid.
  - Levert een hint **2×5 cijfers** op (10 m-precisie, bv. `18836 44072`), dan is dát het antwoord: 2×5 doorgeven, **niet afkappen** naar 4+4. De invoer volgt wat de hint oplevert of vraagt ("vijf cijfers spatie vijf cijfers" kwam in 2024 voor).
  - Sinds 2024 kan het antwoord **ook een woord** zijn (codewoord, plaatsnaam, postcode, what3words, naam van een OV-lijn). Lees de hint goed: de invulomschrijving staat erbij.
- **Punten**: 1 punt per team als het antwoord binnen 20 minuten volledig correct is ingevoerd. Een fout antwoord wordt niet aangepast → **liever 2 minuten extra controleren dan gokken**.
- **Thema**: elke editie heeft een thema; álle hints hangen eraan op. 2025 = Lord of the Rings, 2024 = LEGO. Het thema bepaalt de woordspelingen in de titels en de bronnen (wiki's, films, personages) die je nodig hebt.
- **Na afloop** publiceert de organisatie bij elke hint een knop **"Uitleg"** (`/solution/<id>`). Vorige edities zijn dé leerbron.

### Site & data ophalen
- Spelsite tijdens het spel: `https://www.jotihunt.nl` (feed met paginering `?page=N`). Oude edities: `https://2025.jotihunt.nl` (en Wayback Machine voor ouder).
- **Publieke API (JSON, geen login, ratelimit 30 calls/min)**:
  - `https://<host>/api/2.0/articles` → alle berichten, velden `id, title, type (hint|assignment|news), publish_at, message.content (HTML)`; gepagineerd (`?page=2`).
  - `https://<host>/api/2.0/areas` → status vossenteams per deelgebied.
  - `https://<host>/api/2.0/subscriptions` → deelnemende groepen.
- Bijlagen staan op `https://cdn.jotihunt.net/...` (png/jpg/mp3/mp4/docx/pdf/zip). Download met `curl -sL -A "Mozilla/5.0"`.
- HTML-berichten zijn Trix-editor output: `<figure data-trix-attachment=...><a href=IMG>`. De teamnaam staat als losse tekst vóór de afbeelding/link.

---

## 2. Werkwijze (altijd in deze volgorde)

1. **Lees titel + inleidende tekst twee keer.** De titel is bijna altijd een woordspeling die het codesysteem verraadt:
   - "Simian-rillion" → Simian = aap → Andy Serkis (Gollum) speelt in *Planet of the Apes* Caesar → **Caesar-cipher**.
   - "What Three Rings for the Elven-kings" → **what3words**.
   - "5661 Rings for the Dwarf-lords" → **postcode 5661 (Geldrop)**, wijk met LotR-straatnamen.
   - "The dark land of Mordor" met tekst van alleen o/r/k → **ORK = Kenny code** (m/p/f vervangen door o/r/k).
   - "Tweestrijd … goed en kwaad … zij aan zij" → **binair** (goed = 1, kwaad = 0).
   - "Elf on the Shelf … ik tel tot elf" → **tellen in het Quenya** (Elfentaal).
   - "Tijd als vergankelijkheid" + klokjes → **klokalfabet**.
   - "Palantír & Chill" (Netflix & chill) → **films**: acteurs in andere films, laatste cijfer van het releasejaar.
   - "Twintigste editie" → **Jotihunt-thema's van vorige jaren**, laatste cijfer van het jaartal.
   - "In de Ban van de Ring Buiten-Midden-Aarde" → ringen van **Saturnus** (D, C, B, A, F, G, E… ring-letters → volgorde-nummer).
2. **Tel de elementen per team.** Een coördinaat heeft 8 cijfers. Zie je per team 8 plaatjes/symbolen/zinnen/vragen/getallen → elk element is één cijfer. Zie je 2×4 of een spatie in het midden → X en Y. Zie je 3 woorden → what3words. Zie je 1 plaatje/zin → anagram, plaatsnaam of woord-antwoord.
3. **Zoek de gedeelde structuur tussen teams.** Alle teams gebruiken hetzelfde systeem. Het 5e element (eerste cijfer Y) is bijna altijd "4"; het 1e element is "1" of "2". Daarmee kalibreer je onbekende alfabetten (welk symbool is 4? welk is 1?) en controleer je je decodering.
4. **Decodeer met een script, niet uit het hoofd**, zodra het systeem bekend is (zie §5 en `scripts/jh.py`). Doe alle teams in één keer.
5. **Valideer**: 8 cijfers? X/Y in Gelderland-bereik? Ligt het punt in het deelgebied van dat team (`/areas`)? Ligt het binnen een paar km van de vorige positie van dat team (vorige hint)? Zet om naar WGS84 en bekijk op een kaart of het een logische plek is (weg, dorp, parkeerplaats; niet midden in een meer).
   Feiten die je nodig hebt (dierenlijst van een dierentuin, filmjaar, stationsnaam) zoek je **online op** voordat je gokt; één zoekopdracht is sneller dan redeneren over twijfelbits.
6. **Woordantwoord?** Controleer spelling exact (hoofdletters, koppeltekens) tegen de invulinstructie.
7. **Vastgelopen na 10 minuten?** Loop de catalogus in §3 en de herkenningsgids in §4 af; zoek de titel letterlijk + "code" of "alfabet" op geocachen.be of dcode.fr; probeer de woordspeling in het Engels én Nederlands.

---

## 3. Catalogus van hinttypes (editie 2025, met uitleg van de organisatie)

| Hint (2025) | Materiaal | Mechanisme | Tool/bron |
|---|---|---|---|
| Stambomen van Valinor | Tengwar-namen van Tolkien-personages | Generatie-afstand tot Lúthien & Beren (= 0); elke volgende generatie +1 | lotrproject.com (stambomen), tengwartranscriber.github.io |
| A Journey Through Middle-earth | Jigidi-links per team | Legpuzzel leggen; het plaatje toont het coördinaat | jigidi.com |
| The dark land of Mordor | Strings van o/r/k | **Kenny code** met o=m, r=p, k=f; levert Nederlandse telwoorden ("eenzeventweevier viervijfnulnul") | script |
| Hint Oscar | Plaatje stationsbord "Elraneth Camnar" | **Anagram** van een station (Arnhem Centraal) | anagram-solver + lijst NS-stations |
| What Have I Got In My Pocket? | 11 raadsels + filippine + docx met wachtwoord | Raadsels oplossen → roze kolom = wachtwoord (ARDALAMBION) → docx bevat coördinaten | LibreOffice/msoffcrypto om docx te openen |
| Schrift uit de Schaduwlanden | Rode symbolen: cirkels/vierkanten met lijntjes | **ELIA Frames** (alternatief voor braille) | elialife.com/elia-frames |
| Palantír & Chill | 8 filmstills per team | LotR-acteur in andere film → laatste cijfer releasejaar | IMDb/Wikipedia |
| OV Hint | AI-plaatje kip + trein | Kip + trein = **Kippenlijn** (Valleilijn Ede–Amersfoort); woordantwoord | Wikipedia spoorlijnen |
| De confrontatie in Moria | Zwarte hoekige runen | **Dovahzul** (Skyrim-drakentaal) cijfers | geocachen.be dovahzul |
| De Spreuk van Lothlórien | Tengwar-woorden | Tengwar → voluit geschreven cijfers (een, twee, …) | tengwartranscriber.github.io |
| Minas Tirith (docx per team) | Word-bestand met plaatjes van gebouwen | Gebouwen met oranje banier dragen bordjes met codes | docx → `unzip word/media` |
| The One Ring, and the One Ring only | Letters A–G + "DP" + km + graden, basispunt HQ | **7-segment display** (ABC=7, DP=decimaalpunt) → afstand + richting → **coördinatenprojectie** vanaf 188362 440722 | script `projectie` |
| Twintigste editie Jotihunt | 8 themaplaatjes per team | Jotihunt-thema's → jaartal → laatste cijfer | nl.scoutwiki.org/Jotihunt |
| The Fellowship of the Ring (docx) | Docx met wachtwoord + plaatje met personages | **Stapeltellen** van voornamen (letterwaarde optellen tot 1 cijfer) → 12-cijferig wachtwoord | script `stapeltel` |
| Simian-rillion | 8 zinnen Silmarillion per team, elk anders versleuteld | **Caesar**: per zin de shift terug = cijfer | script `caesar` |
| The Quiz of Power | 20 telvragen LotR + per team 8 vraagnummers | Antwoord (0–9) op elke vraag = cijfer | LotR-kennis/wiki |
| Welkom te Rivendell | Video LEGO-set + vragen A–J met tijdstippen + per team 8 letters | Tel in de video op het tijdstip → vraag-letter → cijfer (A=4, B=8, C=2, D=9, E=1, F=0, G=5, H=6, I=7, J=3) | ffmpeg frames |
| Tijd als vergankelijkheid | Rij klokjes | **Klokalfabet** (geocachen.be) → telwoorden | geocachen.be klokalfabet |
| Radagasts Waakzame Ogen | Dunne lijn met punten/haakjes | **Hymmnos**-cijfers | geocachen.be hymmnos |
| 5661 Rings for the Dwarf-lords | PDF met rijen plaatjes + huisnummers | Postcode 5661 = Geldrop; personage = straatnaam, getal = huisnummer; vogelvlucht-lijnen tussen adressen tekenen een cijfer op de kaart (let op 6 vs 9) | Google Maps / OSM |
| What Three Rings for the Elven-kings | 1 lange zin per team met 3 **vetgedrukte** woorden | **what3words** (Engels) | what3words.com |
| Dat zijn veel Hobbits! | mp3 per team ("They're taking the Hobbits to Isengard") | Tel hoe vaak "the Hobbits" herhaald wordt per "They're taking … to Isengard"; 8 getallen | luisteren / audio-analyse |
| Als de eerste zonnestralen… (Oscar) | Gedicht-plaatje | Cryptisch raadsel → naam blokhut ("Lichtdragers" = St. Christoforus Lichtdragers); woordantwoord | Google |
| In de Ban van de Ring Buiten-Midden-Aarde | Runen: "D-RING F-RING R/2004 S1 1-RING" | Ringen van **Saturnus** van binnen naar buiten genummerd (nl.wikipedia); "1-ring" = 0 | Wikipedia Saturnus ringen |
| The One Ring (zip per team) | 8 jpg's van hetzelfde plaatje + basisafbeelding (00.jpg) in de hint | **Zoek de verschillen**: aantal verschillen t.o.v. de basis = cijfer, 8 afbeeldingen = XXXX YYYY. Een **verplaatst** object (lichtreflectie op de ring) is één verschil, geen twee | `python3 scripts/jh.py verschillen --basis 00.jpg team.zip`; nagerekend: Alpha 1763 4379, Bravo 1826 4298, Delta 1925 4436 (alle 9 verschillen = de 9 cirkels van de officiële uitleg) |
| Elf on the Shelf | mp3 per team | Gesproken **Quenya-telwoorden** (minë, atta, neldë, canta, lempë, enquë, otso, tolto, nertë, cainen; 0 = munta) | tolkiengateway.net Quenya numbers |
| Oog van Sauron | Stereogram per team | **Magic-eye/stereogram** decoderen → cijfers verschijnen | magiceye.ecksdee.co.uk of script (autocorrelatie/shift) |
| Oscar? Vossen? Team? Start? | YouTube-filmpje | Locatie herkennen (busbord "Arnhem Zuid") | kijken, OV-kennis |
| Tweestrijd | 8 rijen portretten goed/kwaad | **Binair**: goed = 1, kwaad = 0; hele 8-cijferig getal (of per groep) binair | script |
| Oscar uitzwaaien | Plaatje "Zahrin Dume" | **Anagram** (Arnhem Zuid) | anagram-solver |
| Oscar Victor Vossen (nieuws) | Gemeentewapen + tijden 09:14, 09:35, 09:47 met pijlen | Gemeente herkennen via wapen (Wikipedia) + dienstregeling → route/halte OV-team | Wikipedia wapens, 9292.nl |

### Editie 2024 (thema LEGO, 6 teams Alfa–Foxtrot) – geverifieerd met de officiële uitleg

| Hint (2024) | Materiaal | Mechanisme |
|---|---|---|
| Groepsfoto om te beginnen | Foto minifigs op een toetsenbord + docx met wachtwoord | Elke minifig = een Jotihunt-thema (vanaf 2011); de toets waarop hij staat, in **chronologische volgorde** van de thema's = wachtwoord (`7xrl=9\`bqj;`) |
| Kan jij deze stenen stapelen | Plaatjes van LEGO-onderdelen | **Stapeltellen van het onderdeelnummer** (3007 → 10 → 1); tweekleurige stenen = som/verschil van twee vlakken |
| Er was eens een magisch koninkrijk | 2 rasters 10×10 LEGO-hoofden, rijsommen, cellen "E4 H6 A1 D2" | Elk hoofdtype heeft een waarde; rijsommen geven het stelsel; waarde op de genoemde cellen = cijfer |
| Overwatch (Tokki) | 8 minifigs per team; antwoord in kleine letters | **Color Tokki code** (kleurcombinatie torso/benen) → tekst |
| Met veel gevoel… | Plaatje | **Braille** |
| Ieder gaat zijn gang, zonder te matten of te slaan | Schaaknotatie per stuk (Q, R, H, T, P, B, L, V) | Teken het pad van elk stuk op het bord: elk pad is een **cijfer**; cijfervolgorde = volgorde van de stukken binnen een beurt (B,Q,T,V,R,H,P,L) |
| Plussen en minnen | Zelfde notatie, "iedereen begint op eigen nul" | Rood veld = −1, groen veld = +1; volgorde van de stukken uit de Jotihunt-thema's |
| Lego Eiland / Der LEGO Mannschaft | docx per team + foto voetbalteam | **Rugnummers** van de spelers → cijfers / wachtwoord |
| LEGO Sudoku | 9×9 met 9 soorten stenen, gekleurde cellen X/Y | Sudoku oplossen; steen-type → cijfer via "woordwaarde/opzoeken"; gekleurde cellen geven de 8 cijfers |
| Brickwatch goes Europe! | Screenshot met omcirkeld onderdeelnummer | Opzoeken op brickwatch.eu / BrickLink |
| Niet Alles Is Vierkant | Raster van gekleurde 2×2 tegels (rood, groen, blauw, geel, magenta, cyaan) | **Hexahue** (6 kleuren = zes-hoek) |
| Sorry, het gaat even te moeizaam | Foto met 12 torentjes van 4 gekleurde 1×1 stenen | **Weerstandskleurcode** (zwart 0 … wit 9); één torentje X, één Y per team |
| Postbode | Rijen groene/blauwe noppen, 3 hoog, 32 breed | **KIX-code** (PostNL; "Kopenhagen, Istanbul, Xanten" = K-I-X); 4 staven per teken, 8 cijfers |
| My Puzzles (JiGiDi) | Jigidi-links | Legpuzzel, plaatje toont coördinaat |
| zes tinten grijs | Mozaïek zwart/grijs/wit, 8 kolommen, 1 regel per team-coördinaat | **Hexahue-cijfers** (de cijfers 0–9 in Hexahue zijn zwart/grijs/wit-patronen) |
| LEGO Hardware Wars | YouTube-video + docx | Letters/cijfers op tijdstippen in de video (1:29, 2:10, 4:48, 8:48, 9:05, 9:51) samen = wachtwoord |
| LEGO vragen | 13 trivia-vragen met rekenregel (stapeltel woordwaarde / n-de cijfer van jaartal), antwoord in **graden-minuten** `N52 14.IGH E006 13.K(E-C)A` | Trivia (A 3002→0, B "LEg GOdt"→2, C STOP→1, D 1979→7, E 1999→9, F AFOL→7, G Billund→2, H 1947→4, I Cole/Jay/Kai/Zane→3, J Ole Kirk Christiansen→9, K Atlantis→6, L Visorak→5, M De Bouwsteen→7); antwoord in het gevraagde formaat invullen, niet omrekenen |
| LEGO Film | Gif van steenkolommen + letters per team | Niet gearchiveerd; vermoedelijk kleurkolommen = minifig-personages |
| MOC | Namen van MOC's/sets op rebrickable; antwoord 5+5 cijfers | Nummers opzoeken (MOC-nummer / setnummer / aantal onderdelen) |
| Zwart – Wit | PNG's met **transparantie** (minifigs op wit) | Sleep/leg de PNG op een donkere achtergrond: de cijfers staan er in wit naast |
| MindStorms | `.uf2`-bestanden (EV3-programma, "alpha.elf") | Programma uitlezen/uitvoeren; strings/getallen eruit halen |
| LEGO Architecture Box | Letters + verhaal over priemgetallen 3,5,7,11,13,17,19 | Priemgetal-posities / letterwaarden |
| Let the adventure begin! | Legoland-plattegrond met paren getallen `(42-82 / 3-53)` | **Kruispeiling** tussen attractienummers op de kaart |
| LEGO Geschiedenis | Formules met letters `(D-2)(L-10)(E+1)…` | Letters = **letterwaarde** (D=4, E=5, G=7, L=12, O=15, T=20); elke haak = één cijfer |

### Editie 2026 (thema Brave / Schotland, 8 teams + Oscar) – live gevolgd, achteraf gecontroleerd met de officiële uitleg (zie `references/resultaten-2026.md`)

| Hint (2026) | Materiaal | Mechanisme (officieel) | Coach / les |
|---|---|---|---|
| Starthint (za 10:00) | mp4, vanaf ~0:48 houdt elke vos een tartan-badge op met teamletter + X en Y van 5 cijfers | **Direct aflezen** (RD op 10 m); frame voor frame (ffmpeg `-ss` per 0,5 s), watermerk over de onderste regel | 8 goed. Twijfelcijfer beslissen met de positie in de volgende hint |
| Schotse les (za 11:30) | Per team woordzoeker + woordenlijst (kleur = hoe vaak een woord in álle roosters samen staat) + docx; Gaelische tip "vijftien letters, overgebleven letters, priemgetal" | **Woordzoeker**: 15 woorden wegstrepen, overgebleven letters op **priemposities** = wachtwoord; coördinaat in de docx als `X15754387X` | 7 geverifieerd; Echo onoplosbaar (CLYDE staat in geen enkel rooster, WHISKY 3× i.p.v. 4×): fout organisatie. Leg eerst de aantallen naast de kleurlegenda |
| Wat de Stenen Fluisteren (za 12:05) | Reeks Keltische spiraaltekens per team | Font **Pictish Swirl** → Nederlandse telwoorden | 8 goed via frequentieanalyse (vaakste teken = e, eerste woord "een"); fontherkenning was sneller geweest |
| Say Cheese! (za 13:00) | mp4 van 2 s met 8 rollende kazen | **Kaas = wijzerplaat van 10 vakken**, 0 gemarkeerd, met de klok mee tot het rode vak | 8 goed; hoekmeting per frame (cv2) |
| Brave Burgers (za 14:00) | Per team twee regels Schots-Gaelische dierennamen | Dier op **burgerszoo.nl/wiki/dieren** = 1, anders 0 → binair → decimaal | 4 fout: lijst uit eigen kennis ingevuld (Maleise tapir staat er níet op, zwartvoetpinguïn wél). Haal de genoemde bron op; de wiki staat als `umbracoContent.items` in de HTML |
| Meet de wereld aan de Grote Beer (za 15:00) | Foto met figuren op een grondlijn + korte streep rechtsboven | **Hoogte van de bovenkant**: grondlijn → streep = 1–9, onder de grondlijn = 0 | 4 fout: lengte van het figuur gemeten en elk dwaallichtje vast 1 gegeven; zwevende lichtjes zijn 2, hangende 0 |
| There can be only... (za 16:00) | Audio: Highlander-quote met Gaelische woorden | 'one' vervangen door een **Gaelisch telwoord 0–9** | 8 goed |
| Will-o-the-wisps (za 17:10) | Per team 6 puzzels (morse, runen, braille, polybius, Face-it, Kabouter ABC) + docx | Uit elk antwoord één letter = codewoord (MERIDA, ELINOR, FERGUS, TARTAN, DRUIDE, MOERAS, STENEN, HEKSEN) = docx-wachtwoord | 8 geverifieerd; codewoord raden uit 4 van 6 letters werkte |
| Highland Crafts (za 18:00) | Aankondiging | Hint in de Minecraft-wereld | Handwerk voor het team |
| De Ring of Stones (za 19:00) | Rekenraadsels + steentabel per team | Som → steennummer → cijfer uit de tabel (geen uitleg gepubliceerd) | 7 goed; steennummers schuiven per team één op |
| De verdwenen code van Crafty Carver (za 20:10) | Rijmpje per team + plaatje met genummerde voorwerpen (beren, flessen) | Elke regel wijst een voorwerp aan (geen uitleg gepubliceerd) | 3 fout: de UPDATE (`tekst_v2.md`) paste juist de rijmpjes van de drie probleemteams aan, maar die is niet verwerkt |
| Waar de stilte spreekt (za 21:10) | Audio: per team 8 fragmenten | Gesproken **letterparen stapeltellen** (G-R = 7+18 = 25 → 7), "nul" = 0 | Geen antwoord: de coach zocht Gaelische telwoorden in plaats van vrij te transcriberen |
| Whiskey in the jar (za 22:03) | Per cijfer een rij whiskyflessen + kaart van Schotland | Stokerijen opzoeken en op volgorde verbinden: de lijn tekent het cijfer | 8 goed |
| De Eer van de Schotse Hooglanden (za 23:15) | Geheimtekst per team, "speel eerlijk" | **Playfair** met de **teamnaam** als sleutel (I=J) → adres | 8 geverifieerd; de richting gokte eerst BRAVE als sleutel |
| Bits of Freedom (zo 00:01) | Gezichten met blauwe/witte banen | Binair (blauw = 1), getallen > 9 stapeltellen | 8 goed |
| Ook Grijze vossen lopen mee (zo 01:00) | docx per team + verwijzing naar grijzevossen.nl | In 3 trainingsvideo's worden 8 **straattaalwoorden** uitgesproken = wachtwoorden | Geen antwoord: na een spectrogram "alleen muziek" geconcludeerd en niet getranscribeerd |
| Doodlezak (zo 02:00) | Google Doodles per team | Laatste cijfer van het jaar van de doodle | 8 goed; drie doodles pas achteraf gevonden (Affandi 2017, Tanabata 2020, Google 27 jaar 2025) |
| De Geheimtaal van de Schotse Hooglanden (zo 03:01) | Ogham-inscriptie per team | **Hexadecimaal in Ogham**: 15 medeklinkers = 1–F, leeg = 0; 7 hex-cijfers → XXXX YYYY | 8 geverifieerd |
| Jigidi puzzel (zo 04:00) | Per team een jigidi.com-link (eerst Alpha = Foxtrot, later hersteld) | Legpuzzel; het plaatje toont het coördinaat | Handmatig (botcontrole); userscript Jigidi Auto Solver |
| De Erfenis van Þingvöllr (zo 05:00) | Runen per team | **Eigen runenalfabet van 26 letters** (geen Futhark) → Nederlandse telwoorden | 8 geverifieerd |
| Het Pad van de Roeiers (zo 06:16) | Vikingzeil met 8 kolommen X/Δ-paren + raster | **Turtle graphics**: ΔΔ = stap, één roeier = 45° draaien; de route tekent het cijfer | 2 fout: zelfbedachte 6/9-regel. 6 tegen 9 is bij een gedraaid route-cijfer niet af te leiden: geef beide en beslis met de positieketen |
| Scotland the Brave (zo 07:04) | mp3 doedelzak per team | Noten **G A B C D E F G A = 1–9**, fluit = 0 | 7 geverifieerd. Gemeten grondtonen ≈ 208, 232, 257, 286, 310, 346, 384, 416, 465 Hz; fluit ≈ 590 Hz |
| Tartan weaving (zo 08:00) | Tartan per team, twee keer gespiegeld | Draden per kleur − 10; zwart/wit scheidt X en Y | 8 geverifieerd; lees vanaf links tot het spiegelpunt |
| Is het een kraai? … (zo 09:00) | Fantasiebeesten per team | **Poten tellen** | 7 goed. Twijfel door een sprong van 15–35 km was onterecht: collectieve verplaatsing na het nieuwsbericht "Mor'du heeft flink huisgehouden" |
| Ik Bell je zomaar even op (zo 10:00) | Cijfers op een telefoontoetsenbord | **Jump the five**, maar de makers lieten 5 en 0 staan (strikt 5↔0 gaf een onmogelijk coördinaat) | 8 goed |
| De eenhoorn van de Hooglanden (zo 11:05) | Lint met Latijnse woorden | Latijnse telwoorden, DECEM = 0 (geen uitleg gepubliceerd) | 8 goed |

Patroon 2026 (22 hints met antwoord, 154 van 168 teamantwoorden goed; de 13 fouten kwamen uit een gemiste UPDATE, een niet opgehaalde bronlijst, een net verkeerde meetregel en een zelfbedachte 6/9-regel): weinig klassieke geocache-codetabellen, wel **zelfbedachte systemen die je uit het thema moet afleiden** (Burgers' Zoo, kaasrol-klok, fantasiealfabet) en veel **media** (video, docx). De "snelle check" van de coach (eerste cijfer 1/2, vijfde cijfer 4, vergelijk met vorige positie) was telkens de sleutel om een zelfbedacht systeem te bevestigen.

Terugkerende **basisvaardigheden** (ook voor andere edities): Caesar/ROT, letterwaarde (A=1…Z=26), stapeltellen, binair, 7-segment, Kenny code, morse, braille en varianten, fantasy-alfabetten (geocachen.be heeft er ~140), telwoorden in andere talen, anagrammen, projecties, what3words, postcodes, filmjaren, trivia-tellen in video/audio, zoek-de-verschillen, stereogrammen, wachtwoord-beveiligde bestanden.


### Editie 2023 (thema Pirates of the Caribbean, 6 teams Alpha–Foxtrot) – achteraf blind getest (zie `references/resultaten-2023.md`)

Alleen 72, 81, 82 (officiële uitleg) en 52 (docx opent) zijn hard gecontroleerd; de rest is de lezing van de coach.

| Hint (2023) | Mechanisme | Status |
|---|---|---|
| Koersvast | Video met kaartjes: graden + km vanaf het HQ (projectie) → plaatsnaam | niet gecontroleerd |
| Een stapel vragen aan Calypso | Quiz; elk antwoord heeft een waarde (aantal letters) → formule → WGS84 → RD | organisatie meldde zelf fouten (Echo, Foxtrot) |
| Alamala Sabi … (Inspector Gadget) | Dubbel binair: 8-bit groepen zijn '0', '1' en spatie → nog eens ASCII → telwoorden | niet gecontroleerd |
| Diepzeekaart | Hexkaart met gele route per schip; kleurcode onder schip/knik als hex → DEC | niet gecontroleerd |
| Not all treasures are silver and gold | Geocoin met trackingcode → geocaching.com/track → coördinaten in de beschrijving | niet gecontroleerd |
| Minecraft Hint (+ Vooraankondiging, Voorbereiding deel 2) | Minecraft-wereld (zip op de CDN): bij elk vossenbord een wachtwoordbord → docx per team | **6/6 geverifieerd** |
| Thuis bij de piraten of bij Governor Swann? | Zeekaart = Gelderland, ijkpunten Port Royal = Paleis Het Loo, Tortuga = HQ; schip → postcode | niet gecontroleerd |
| Up is Down | Coördinaten in de Indische Oceaan → antipode (Jamaica) → straatnaam per punt | niet gecontroleerd |
| Zeemafoor | Semafoor (Jack Sparrow met pistolen als vlaggen) in video | niet gecontroleerd |
| Piraat met de blues | Video + kleurwiel → cijfers | niet gecontroleerd |
| Quite some characters … | Personage + getal N → N-de letter → letterwaarde → stapeltellen; lege plaat = 0 | niet gecontroleerd |
| Aqua de Vida | Topokaart 1:25.000 + oleaat → kruis → postcode | coach liep vast |
| Captain Hector Barbossa … | **Major-systeem** (Winkelmann): medeklinkerklanken = cijfers | niet gecontroleerd |
| Silent Mary | Zoek de verschillen per genummerd plaatje (pdf per team) | niet gecontroleerd |
| Pirata Codex | Emoji-sudoku; letters A–F in lege vakjes → N/E-formule | niet gecontroleerd |
| La Lengua Perdida | T9-toetsen als pigpen-hoekjes, cijfer = aantal keer drukken → adres | niet gecontroleerd |
| The Stuttering Parrot | Ternaire code met a/g/r, 3 tekens per letter → straatnaam + huisnummer voluit | niet gecontroleerd |
| De Schrik van de zeven Zeeën | Internationale seinvlaggen + cijferwimpels → `straat nr plaats koers afstand` | niet gecontroleerd |
| De zeven zeeën | Havenstad → breedteband op de wereldkaart → cijfer | niet gecontroleerd |
| The Curse of the Black Pearl | Muntloten uit **NumisBids**-veiling (Heritage Europe, Auction 70); weggepoetst cijfer = RD-cijfer | **6/6 geverifieerd** |
| De drietand van Davy Jones | Drietand = 3 woorden: **what3words** uit misplaatste woorden in het verhaal (Engelse titelwoorden vertaald) | 3 goed, Bravo niet gevonden |
| Piratenwet | Piratencode van Edward Low/George Lowther (Wikipedia), artikelen I–X = 1…0 | **6/6 geverifieerd** |

---

## 4. Herkenningsgids (wat zie ik → wat is het)

**Tekst**
- Alleen 3 verschillende letters, lengte veelvoud van 3 → **Kenny code** (m/p/f of thema-letters, bv. o/r/k). Decodeert naar telwoorden.
- Alleen 2 symbolen/soorten (goed/kwaad, licht/donker, 2 kleuren, 2 LEGO-steentjes) → **binair** (groepjes van 4 bits per cijfer, of hele getal).
- Lange Engelse/Nederlandse tekst met per zin een andere "taal" van wartaal → **Caesar per zin**; shift = cijfer.
- Letters A–G, eventueel "DP" → **7-segment display** (A boven, B rechtsboven, C rechtsonder, D onder, E linksonder, F linksboven, G midden).
- Hoofdletters-naam die geen bestaand woord is op een stationsbord/plaatsnaambord → **anagram** van station/plaats (Oscar-team).
- Zin met 3 vetgedrukte woorden → **what3words**.
- 4-cijferig getal dat geen coördinaat is → **postcode**.
- Lijst namen/woorden → **letterwaarde** of **stapeltellen** (uitkomst 1 cijfer per woord) of **alfabetpositie van eerste letter**.
- Telwoorden in een vreemde taal (Quenya, Klingon, Esperanto, Deens…) → vertaal; thema bepaalt de taal.
- Vragen "Hoeveel …?" → trivia, antwoord 0–9 per vraag.

**Beeld**
- Klokjes met wijzers → **klokalfabet**.
- Rode cirkels/vierkanten met streepjes en puntjes → **ELIA frames**.
- Zwarte hoekige "krassen" (drakenklauw-achtig) → **Dovahzul**.
- Dunne horizontale lijn met puntjes en haakjes → **Hymmnos**.
- Sierlijk krullend elfenschrift → **Tengwar** (transcriber: let op modus Quenya/Sindarin/Engels).
- Rechte runen → **Runenschrift** (Futhark/Cirth) of **Dwergenrunen** (Angerthas; Hobbit-kaart).
- 6-punts rasters → **braille**; varianten: Moon, Quadoo, Hexahue (kleur).
- **Raster van herhaalde symbolen** (X/Δ-paren, pictogrammen, fantasietekens, Kenny-achtige plaatjes) → eerst `jh.py symbolen --vak x0,y0,x1,y1` over alle teambestanden tegelijk: gelijke vormen worden klassen A, B, C (gedeeld over de teams), met het raster per rij en per kolom en `klassen.png`/`<team>_labels.png` ter controle. Daarna hoef je alleen nog de betekenis per klasse te bepalen. Zelf segmenteren kostte bij "Het Pad van de Roeiers" 9 minuten; het script doet 8 teams in 2 seconden. Zonder `--vak` telt een drukke achtergrond mee.
- Reeks filmstills/portretten → **jaartal** (release/geboorte) of **alfabetische positie**/**aantal letters** van de naam, of **binair** (goed/kwaad).
- Reeks ogenschijnlijk willekeurige plaatjes (walkman, viking, Japan, maffia, piraat, filmcamera…) → **vorige Jotihunt-thema's** → jaartal (scoutwiki).
- Reeks planeten/manen/ringen/elementen → **volgordenummer** in een bekende reeks.
- Ruis-patroon met herhaling → **stereogram**.
- 8 bijna identieke foto's (of een zip ervan) plus één basisplaatje → **zoek de verschillen** (aantal = cijfer); zie §5 en `scripts/jh.py verschillen`.
- Gemeente-/provinciewapen → **Wikipedia "wapen van …"**; vlaggen van landen → ISO-code/letterpositie.
- Dienstregelingtijden met pijlen → OV-route (Oscar); zoek de lijn via 9292/NS.
- Legpuzzel (Jigidi-links per team) → **handmatige actie**: een mens legt hem in de browser. Een agent komt niet langs de botcontrole van Jigidi (WebFetch/curl krijgen "Let's make sure you are a real person"). Snelst met Tampermonkey/Violentmonkey + het userscript [Jigidi Auto Solver](https://greasyfork.org/en/scripts/600106-jigidi-auto-solver): link openen, Solve, Zen-modus aan, wachten tot het paneel "klaar" zegt, **Solve puzzle**. Het coördinaat staat in het gelegde plaatje. Let op dubbele links (2026: Alpha en Foxtrot eerst dezelfde puzzel, later via een UPDATE hersteld; kijk dus naar de nieuwste tekst). De coach post dit zelf als notitie zodra de hint binnenkomt.
- Kaart met lijnen/adressen → **vogelvlucht**-lijnen tekenen cijfers; of **kruispeiling**.

**Audio/video**
- mp3 met herhaalde zin → **tel herhalingen** (ffmpeg → spectrogram/segmenten; of handmatig luisteren).
- mp3 met gesproken vreemde woorden → **telwoorden** in thema-taal (transcribeer fonetisch, match met lijst).
- mp4 met vragen op tijdstippen → `ffmpeg -ss <t> -i f.mp4 -frames:v 1 frame.png` en tel.
- Muziek/lipdub → songtitel/artiest/jaartal of tekst meelezen.

**Bestanden**
- `.docx`/`.xlsx` met wachtwoord ("CDFV2 Encrypted") → wachtwoord komt uit een vorige stap (raadsels, stapeltellen). Open met `msoffcrypto-tool` (`pip install msoffcrypto-tool`) of LibreOffice. Onbeveiligd docx: `unzip -o f.docx -d out` → `word/document.xml` + `word/media/*`.
- `.pdf` → tekst/plaatjes eruit (`Read` tool, `magick`/`sips`), kijk ook naar verborgen witte tekst en metadata (`exiftool`).
- `.zip` met n plaatjes → vergelijk pixelsgewijs (zoek de verschillen) of bekijk bestandsnamen/volgorde/EXIF.
- Elke afbeelding: controleer **EXIF/metadata** (`exiftool`) en **bestandsnaam** (bv. "stereogram A.jpg" verraadt het type).

---

## 5. Codesystemen cheat-sheet

**Kenny code** (3 symbolen, basis 3; a=mmm, b=mmp, c=mmf, d=mpm, … z=ffp): index = 9·s1 + 3·s2 + s3 met m=0,p=1,f=2. Thema-varianten vervangen m/p/f door andere letters; probeer alle 6 toewijzingen tot er telwoorden uitkomen.

**7-segment**: ABCDEF=0, BC=1, ABDEG=2, ABCDG=3, BCFG=4, ACDFG=5, ACDEFG=6, ABC=7, ABCDEFG=8, ABCDFG=9. DP = punt.

**Stapeltellen**: letterwaarde (A=1…Z=26, accenten strippen, é→e) optellen, cijfers blijven optellen tot één cijfer (digital root; 0 blijft 0, 9 blijft 9). Bv. Frodo = 6+18+15+4+15 = 58 → 13 → 4.

**Caesar**: brute-force alle 26 shifts, kies de shift die Engels/Nederlands oplevert; shift-terug-waarde (0–9) is het cijfer. Shift 10–25 komt niet voor als cijfer nodig is.

**Binair**: 4 bits per cijfer (0000–1001) of het hele coördinaat als 1 getal (8 cijfers ≈ 24–27 bits). Als er 2 blokken zijn: X en Y apart.

**Nederlandse telwoorden** (uitkomst van veel decoders): nul een twee drie vier vijf zes zeven acht negen. Engels: zero one two … Duits: null eins zwei drei vier fünf sechs sieben acht neun. Quenya: munta(0) minë(1) atta(2) neldë(3) canta(4) lempë(5) enquë(6) otso(7) tolto(8) nertë(9) cainen(10)/quainen.

**Saturnusringen** (binnen → buiten, nl.wikipedia): D, C, B, A, F, G, E (en verder Phoebe-ring); in 2025: nummer in deze volgorde, "1-ring" (One Ring) = 0, "R/2004 S1" is een benoemde ring daartussen.

**Klokalfabet, ELIA, Dovahzul, Hymmnos, Tengwar-cijfers, Cistercian, Maya, Babylonisch, enz.**: tabellen op `https://geocachen.be/geocaching/geocache-puzzels-oplossen/<naam>/` (lijst van ~140 systemen op `/geocaching-code-tabellen/`). Engelse tegenhanger: `https://www.dcode.fr/` (heeft ook identifier: "cipher identifier").

**KIX-code (PostNL, = RM4SCC)**: 4 staven per teken; staaf = T (kort/tracker), A (omhoog), D (omlaag), F (beide). Links→rechts gelezen: 0=FFTT 1=FADT 2=AFDT 3=FATD 4=AFTD 5=AADD 6=FDAT 7=FTFT 8=ADFT 9=FTAD (geverifieerd met het PostNL-voorbeeld "5340 AB"). Letters: A=ADAD B=ATFD C=DFAT D=DAFT E=TFFT F=DAAD G=TFAD H=TAFD I=FDTA J=FTDA K=ADDA L=FTTF M=ADTF N=ATDF O=DFTA P=DADA Q=TFDA R=DATF S=TFTF T=TADF U=DDAA V=DTFA W=TDFA X=DTAF Y=TDAF Z=TTFF. In LEGO-vorm: 3 rijen noppen, groen in bovenste rij = A, groen in onderste rij = D, beide = F.

**Weerstandskleurcode**: zwart 0, bruin 1, rood 2, oranje 3, geel 4, groen 5, blauw 6, paars/magenta 7, grijs 8, wit 9. Van boven naar beneden lezen.

**Hexahue**: letters zijn 2×3 rasters met 6 kleuren (rood, groen, blauw, geel, magenta, cyaan); de **cijfers 0–9 gebruiken alleen zwart, grijs en wit**, de spatie is helemaal wit/grijs/zwart. Tabel: geocachen.be/…/hexahue/. Alles wat uit 2×3 blokjes in die kleuren bestaat is Hexahue; "zes" in de titel is de hint.

**Letterwaarde als variabele**: formules met losse hoofdletters (`(T-18)(E-D)…`) → vul A=1…Z=26 in; elke haak levert één cijfer. Check: alle delingen moeten geheel uitkomen.

**Jotihunt-thema's (voor "thema-volgorde"-hints)**: 2011 Frankenstein, 2012 Superhelden, 2013 Alice in Wonderland, 2014 Flowerpower, 2015 Star Wars, 2016 Azië, 2017 Vikingen, 2018 Jotihunt in Hollywood, 2019 Fata Morgana, 2020 (geen/online), 2021 Jaren '80, 2022 Harry Potter, 2023 Pirates of the Caribbean, 2024 LEGO, 2025 Lord of the Rings. Volledige lijst (ook vóór 2011): nl.scoutwiki.org/Jotihunt. Minifigs/plaatjes die deze thema's uitbeelden komen elk jaar terug (chronologische volgorde = sleutel, laatste cijfer jaartal = cijfer).

**Zoek de verschillen (komt elk jaar terug)**: één basisafbeelding en per team 2×4 varianten; het aantal verschillen van een variant met de basis is het cijfer (0 = identiek aan de basis, 9 = alle verschillen). Werkwijze:
1. `python3 scripts/jh.py verschillen --basis <basis> --uit <map> <8 varianten | map | zip>`. De poller doet dit al automatisch bij een zip met ≥4 even grote afbeeldingen (`bijlagen/verschillen_<zip>.txt` + `bijlagen/verschillen_<zip>/overzicht.png`).
2. Lees de tabel: "stabiel" betekent dat fijne en normale telling gelijk zijn. Bij "CONTROLEER" altijd de kaders in de geannoteerde afbeeldingen bekijken.
3. Telregels: een verplaatst object (verdwijnt op de ene plek, verschijnt vlakbij) is **één** verschil (blauw kader, zelfde nummer); een groot nieuw object (Gollum) is één verschil, ook al raakt het iets anders; twee kleine wijzigingen vlak naast elkaar zijn er twee.
4. Controle: identieke bestanden geven hetzelfde cijfer; het 5e cijfer is een 4; het hoogste aantal in de set is meestal het totaal aantal verschillen. Zonder basis kiest het script de meest "gemiddelde" afbeelding: controleer dat, want een variant met 0 verschillen is ook "gemiddeld".
5. Grote afbeeldingen met JPEG-ruis: hoger `--drempel` (bv. 40) als er spikkels als verschil geteld worden.

**Woordzoeker → wachtwoord (2026)**: streep alle lijstwoorden weg (ook achterstevoren en diagonaal, let op woorden-in-woorden), nummer de overgebleven letters rij voor rij, neem de letters op priemposities. Controleer de regel op één team dat wél opent voordat je bij een ander team uren zoekt: opent een document bij 7 van de 8 teams en bij één niet, dan ligt de fout bij de organisatie.

**Zelfbedachte "klok"-codes**: een rond object met een vaste markering (bruin partje, pijl, streep) en een bewegende (rood partje) is een wijzerplaat; tel het aantal stappen tussen beide. Bepaal het aantal partjes (10 → cijfers 0–9) uit de tekening, meet hoeken met Python als het beeld draait.

**Gaelic dierennamen (2026)**: sìobra = zebra, mathan = beer (mathan-bàn ijsbeer), tìgear = tijger, leòmhann = leeuw, ceann-fionn = pinguïn, sròn-adharcach = neushoorn, each-aibhne = nijlpaard, ailbhean = olifant, sioraf = giraf, pioton = python, crogall = krokodil, fiadh = hert, pantar = panter, liopard-sneachda = sneeuwluipaard, bò-mhara = zeekoe, uilebheist Gila = gilamonster, sìota = jachtluipaard, goiriola = gorilla, siompansaidh = chimpansee, morpho gorm = blauwe morpho, fang circe-Frangaich = kalkoengier.

**Transparante PNG's**: controleer altijd `im.mode == 'RGBA'`; leg het plaatje op zwart (`Image.alpha_composite`) om witte tekst zichtbaar te maken.

**Coördinatenprojectie**: vanaf basispunt (RD X,Y) afstand d (m) in richting θ (graden, 0 = noord, met de klok mee): X' = X + d·sin θ, Y' = Y + d·cos θ. Rond af op 100 m voor het antwoord.

**RD → WGS84** (voor kaartcontrole): zie `scripts/jh.py rd2wgs`. Grofweg: Gelderland ligt rond 52.0°N, 5.9°E; RD X 1450–2650 (×100 m) en Y 4100–4900.

---

## 6. Oscar / OV-team

- Hints voor Oscar zijn vaak **woordantwoorden**: een station, een plaats, een OV-lijn, een gebouw (blokhut van een scoutinggroep).
- Veelgebruikt: **anagrammen van stationsnamen** op een nagemaakt NS-bord ("Elraneth Camnar" → Arnhem Centraal, "Zahrin Dume" → Arnhem Zuid). Oplossen: letterfrequentie vergelijken met lijst NS-stations in Gelderland (Arnhem Centraal/Zuid/Velperpoort/Presikhaaf, Nijmegen (Dukenburg/Heyendaal/Lent/Goffert), Ede-Wageningen, Apeldoorn, Zutphen, Doetinchem, Tiel, Barneveld, Harderwijk, Nunspeet, Dieren, Velp, Elst, Zevenaar, Didam, Wijchen, Culemborg, Geldermalsen, Winterswijk, Lichtenvoorde-Groenlo, Aalten, Varsseveld, Terborg, Wehl, Duiven, Westervoort, Lunteren, Hoevelaken, Putten, Ermelo, 't Harde, Wezep, Oosterbeek, Wolfheze, Rheden, De Steeg, Brummen, Voorst-Empe, Klarenbeek, Twello, Eefde, Vorden, Ruurlo, Lochem, Opheusden, Kesteren, Hemmen-Dodewaard, Zaltbommel…).
- **Buslijnen**: Breng (Arnhem/Nijmegen), Hermes/Keolis/Arriva (Achterhoek/Veluwe); een nummer op een bushaltebord is een lijnnummer; zoek de route.
- **Bijnamen van spoorlijnen**: Kippenlijn/Valleilijn (Ede–Barneveld–Amersfoort), Betuwelijn, Maaslijn, Achterhoekse lijnen, Veluwelijn (Zwolle–Amersfoort), Rhijnspoorweg.
- **Gemeentewapens** herkennen via Wikipedia ("Wapen van <gemeente>"); de tijden ernaast zijn vertrek-/aankomsttijden van een dienstregeling.
- Begin-/eindhints van Oscar zijn vaak filmpjes: let op bushokjes, lijnnummers, stationsnamen, herkenbare gebouwen.

---

## 7. Praktische tooling (lokaal aanwezig op deze Mac)

- Python 3.12 met **PIL, numpy, cv2** (beelddiff, kleurtelling, stereogram-shift), geen tesseract (OCR: lees de afbeelding gewoon zelf met de Read-tool).
- **Spraak naar tekst (lokaal Whisper)**: `HF_HUB_OFFLINE=1 python3 -c "from transformers import pipeline; p=pipeline('automatic-speech-recognition', model='openai/whisper-large-v3-turbo'); print(p('fragment.wav')['text'])"`. Audio uit video eerst met `ffmpeg -i v.mp4 -ac 1 -ar 16000 a.wav`. Transcribeer eerst vrij; geef pas daarna een prompt ("Twee letters: G R."). Losse letternamen blijven onbetrouwbaar, dus luister twijfelgevallen na. De `whisper`-module zelf is niet geïnstalleerd.
- **ffmpeg** (audio/video knippen, frames, `-af silencedetect` om herhalingen te tellen), **magick/convert**, **sips** (snel verkleinen), **exiftool**.
- `scripts/toollinks.json`: sleutels → naam + URL van online tools (geocachen-tabellen, dCode, what3words, PDOK, Tengwar, Gaelic, tartan…).
- `scripts/jh.py` (naast deze SKILL.md): `rd2wgs`, `wgs2rd`, `projectie`, `kenny`, `seg7`, `caesar`, `letterwaarde`, `stapeltel`, `binair`, `imgdiff`, `verschillen`, `symbolen`, `anagram`. Voorbeelden:
  ```bash
  python3 scripts/jh.py kenny "orrorrrrrkkrorr…" --letters ork
  python3 scripts/jh.py seg7 "ABC DP ABCDG BC km ABDEG ACDEFG ABDEG graden"
  python3 scripts/jh.py projectie 188362 440722 7.31km 262
  python3 scripts/jh.py caesar "Hs hr snkc zlnmf sgd vhrd"
  python3 scripts/jh.py stapeltel Everard Éowyn Aragorn
  python3 scripts/jh.py imgdiff map_met_8_jpgs/
  python3 scripts/jh.py symbolen --vak 190,455,670,1095 --uit sym/ Alpha.png Bravo.png …   # symboolraster → klassen A/B/… per rij en kolom
  python3 scripts/jh.py rd2wgs 1883 4407
  ```
- Afbeeldingen groter dan ~2000 px eerst verkleinen (`sips -Z 1600 in.png --out klein.png`) voordat je ze bekijkt; voor fijne symbolen juist **uitsnijden en vergroten** (`magick in.png -crop WxH+X+Y +repage -resize 300% uit.png`).
- Zoekbronnen: Wikipedia (NL én EN), tolkiengateway.net / lotr.fandom.com (thema-wiki), nl.scoutwiki.org/Jotihunt (eerdere thema's), IMDb, what3words.com, 9292.nl, ns.nl, pdok.nl (RD-coördinaten op kaart: `https://www.pdok.nl/viewer`), geocachen.be, dcode.fr, anagram-solvers (bv. wordsmith.org/anagram, of eigen script met woordenlijst).

---

## 8. Valkuilen uit de praktijk

- **6 ↔ 9** bij gedraaide cijfers/plaatjes (de organisatie waarschuwt er zelf voor): kijk naar oriëntatie.
- **Identieke elementen = identiek cijfer**: handig als controle (bv. drie identieke plaatjes in een zip → drie keer hetzelfde cijfer).
- **"UPDATE"/correcties** in de hinttekst (bv. "er stond een zinnetje teveel in"): lees altijd de laatste versie van het bericht; de API geeft de actuele inhoud.
- **Teamnaam-spelling** wisselt: "Alfa"/"Alpha". Bestandsnamen gebruiken soms kleine letters (`elf_c.mp3`).
- **Antwoord in woorden**: "eenzeventweevier" = 1724, niet 1 7 2 4 los; "nul" komt voor.
- **Niet elk team heeft elk uur een hint** (`-`): sla over, geen punt te halen.
- **Decimale punt** ("DP") in 7-segment hints: afstand in km met decimalen.
- **Bestandsnamen verraden het type** ("stereogram A.jpg", "Filippine.png", "Windrose.png"): kijk altijd naar `attachment__name`.
- **Gedupliceerde plaatjes in een rij** betekenen hetzelfde cijfer; gebruik ze om een onbekend alfabet te kalibreren.
- **Jaartallen**: "laatste cijfer van het jaar" is de standaard; bij twijfel tussen boek/film: thema volgt meestal de **films** (Peter Jackson 2001/2002/2003, Hobbit 2012/2013/2014).
- **Trivia met discutabele antwoorden**: de organisatie heeft één antwoord; kies het "schoolse" antwoord en controleer met de plausibiliteit van het coördinaat (Y begint met 4).
- **Oscar-hints** vragen geen coördinaat maar een naam: niet converteren.
- **Tijd**: 20 minuten per hint voor punten. Eerst het team(en) van de eigen groep, daarna de rest.
- **Antwoordformaat volgt de hint**: in 2024 vroeg één hint "vijf cijfers spatie vijf cijfers" (RD op 10 m) en één hint graden/decimale minuten (`N52 14.324 E006 13.680`). Vul precies dat in; reken niet om naar 4+4. Komt er uit de decodering 2×5 cijfers (zoals Delta/Echo in de Mordor-hint 2025), geef dan 2×5 door.
- **De organisatie maakt ook fouten**: een formule die negatief uitkomt (2024 Bravo `(G-I)` = 2−3), twee stukken met identieke zetten, een KIX die buiten Gelderland uitkomt. Meld het, kies het meest plausibele cijfer en ga door; andere teams eerst.
- **Kalibreer onbekende tabellen aan de data**: bij de KIX-hint gaf de Wikipedia-afleiding alleen letters; staven per teken omdraaien gaf voor 5 van 6 teams een geldig `1xxx 4xxx`. Zo'n statistische check (eerste cijfer 1/2, vijfde cijfer 4) is sterker dan de tabel op het web.
- **Fout bij de organisatie herkennen**: als één team met dezelfde, bij alle andere teams werkende regel niet uitkomt (Echo bij "Schotse les" 2026, Hotel bij "Mordor" 2025), stop dan na een gerichte variantenronde (leesfouten, woorden weglaten, leesvolgorde) en laat het team de organisatie bellen. Uren brute-forcen levert niets op.
- **Video-hints**: frames per 0,5 s uitknippen (`ffmpeg -ss`), watermerken en overgangen kunnen cijfers verbergen; beelden van 2 s met 48 frames vragen om frame-voor-frame analyse met Python in plaats van kijken.
- **Feiten nazoeken**: de coach moet online kunnen zoeken (dierenlijsten, filmjaren, stations); zonder webtoegang blijven twijfelbits over.
- **UPDATE = opnieuw uitwerken**: komt er een `tekst_v2.md` ("bijgewerkt"), vergelijk dan per team wat er veranderde en werk die teams opnieuw uit. In 2026 (Crafty Carver) paste de update precies de drie teams aan waar de coach vastliep; die drie antwoorden bleven fout.
- **Bron uit de hint zelf ophalen**: noemt de hint of het thema een lijst (dierentuin-wiki, stationslijst), haal die lijst op en vul hem niet in uit eigen kennis. Brave Burgers 2026: 4 van 8 teams fout door één tapir en één pinguïn.
- **Meetpuzzels**: "hoogte" is de positie van de bovenkant boven de grondlijn, niet de lengte van het object. Meet elk exemplaar apart; zwevende of hangende losse objecten zijn vaak de valstrik (Grote Beer 2026).
- **6 of 9 bij gedraaide cijfers** (turtle-routes, gedraaide stempels): niet af te leiden uit de tekening of de commando's. Geef beide opties, beslis met de positieketen en zeg nooit 'zeker' (Roeiers 2026).
- **Twijfel door afstand: toets vooruit, niet alleen terug.** In 2026 was "onzeker want X km van de vorige positie" bij 7 hints onterecht. De vorige positie was zelf fout, of alle vossen sprongen tegelijk (na een nieuwsbericht of aan het begin van een helft). Een eenduidige lezing gaat vóór de afstandscheck; de positie in de volgende hint beslist.
- **Gesproken audio altijd eerst vrij transcriberen** (zie §7), zonder woordenlijst of verwachting. Twee vastgelopen hints in 2026: letterparen die als Gaelische telwoorden werden gezocht, en straattaal in video's die als "alleen muziek" werd afgedaan na een spectrogram. Losse letternamen in paren betekent stapeltellen per paar.
- **Bekende cipher, afwijkende variant**: geeft de standaardvariant bij één team een onmogelijk coördinaat (Jump the five strikt: Alpha 1008), leid de echte regel af uit de teams die wel kloppen en pas die consequent toe.
- **Eigen alfabetten van de organisatie**: runen en symbolen zijn meestal een eigen 26-letteralfabet (met V, W, J, H) en geen historische tabel. Een set van precies 16 tekens (Ogham-medeklinkers + leeg) betekent hex. Probeer bij fantasietekens eerst fontherkenning (Pictish Swirl).
- **Sleutels**: bij Playfair/Vigenère eerst de eigen teamnaam als sleutel proberen ("speel eerlijk", "trouw aan je clan").
- **Materiaal 'ontbreekt'**: eerst de CDN-link zelf proberen, dan de Wayback Machine (`web.archive.org/web/<jaar>id_/<url>`), en pas dan concluderen dat het er niet is. In de 2023-test vond de ene run de Minecraft-wereld wel en de andere niet.
- **RD-afronding**: altijd rekenen met `jh.py wgs2rd` en afkappen van de meterwaarde. Ligt een punt binnen enkele meters van een xx00-grens, meld dan beide (2023: 158100,3 werd in het hoofd 1580, moest 1581).
- **Getal buiten het RD-bereik**: ook als WGS84-decimalen lezen (5195 5872 → 51,95 N 5,872 O).
- **Handmatige acties**: Jigidi-legpuzzels (botcontrole) en alles wat inloggen of een mens vraagt, kan de coach niet zelf. Meld het meteen met de links per team en ga niet zoeken naar omwegen.
- **Fotohints**: eerst de bijlage op volle resolutie downloaden, dan per object uitsnijden en 2× vergroten voordat je kleuren of symbolen leest; geen OCR beschikbaar, dus zelf lezen.

---

## 9. Editie 2026: Brave & Schotland ("stoer, mystiek en Highlands") – voorbereiding

Spelsite: `https://www.jotihunt.nl` (API `https://www.jotihunt.nl/api/2.0/articles`, artikel-id's beginnen elk jaar opnieuw; id 10 = "Testhint"). Zaterdag 17 okt 2026 10:00 – zondag 18 okt 12:00; 9 teams (Alpha–Hotel + Oscar), 48 vossen, 24 jachtopzichters. Spelregels zijn t.o.v. 2025 inhoudelijk gelijk voor hints (1 punt per team, 20 min, exact invoeren); nieuw: hunts gaan via QR-codes, eigen deelgebied telt dubbel.

**Signalen uit de voorpret-berichten van de organisatie (14–15 okt 2026)**, letterlijk "dit is misschien wel een hint":
- "James Bond is Schots" + bonusfiguren van de startopdracht: **James Bond, Alexander Graham Bell, Mary Queen of Scots, William Wallace, Nessie** → verwacht hints met **beroemde Schotten** (zie lijst hieronder).
- "**Strijkkralen** zijn handig" → pixel-art/rasters: QR-code, binair, Hexahue, braille in kralen, kleuren tellen.
- "Beren uit de film kunnen op achterste benen staan", "will o' the wisp = geesten van de doden; Mor'du wordt een dwaallichtje", "de heks gebruikt een **keuzemenu** net als onze telefoonlijn" (→ VOIP-nummers/DTMF-tonen!), "Merida draagt op het wandkleed wit, in het echt groen", "Merida is de eerste Disneyprinses met broers en zonder liefdespartner", "stem van Merida ingesproken door een dertiger (Kelly Macdonald, geb. 1976)".
- "Secure **lineaal, gradenboog**, dowels 8–10 mm, prikpen, priem, spijkers, houtlijm, boor" → **kruispeiling/projectie op papier** en knutselopdrachten; "bewaar alle knutselopdrachten, ze komen terug".
- "Fries is van oorsprong Keltisch" → mogelijk Friese telwoorden/taal; "unicorn is het nationale dier van Schotland"; "kamelen met gouden bulten" (?), "huntpasjes", "je zit" (?), "Scouting Gelderland heeft error, wat staat er op het dashboard".

**Brave (Pixar, 2012) – feiten**: Merida (Kelly Macdonald), koningin Elinor (Emma Thompson), koning Fergus (Billy Connolly), de heks (Julie Walters), kraai, drieling **Hamish, Hubert, Harris**, paard **Angus**, beer **Mor'du** (vervloekte prins, oudste van vier broers), clans **DunBroch, Dingwall, MacGuffin, Macintosh** (Lords Dingwall – Robbie Coltrane, MacGuffin – Kevin McKidd, Macintosh – Craig Ferguson), Maudie (dienstmeid), will-o'-the-wisps (dwaallichtjes), spreuk "mend the bond, torn by pride", steencirkel, werktitel *The Bear and the Bow*, regie Mark Andrews & Brenda Chapman, muziek Patrick Doyle, liedjes *Touch the Sky*, *Into the Open Air* (Julie Fowlis), *Learn Me Right* (Mumford & Sons/Birdy), *Noble Maiden Fair* (Gaelic wiegelied), *Song of Mor'du*; première 10 juni 2012, VS-release 22 juni 2012, 93 min, Oscar/Golden Globe/BAFTA beste animatiefilm; DunBroch-tartan STA 10641; korte film *The Legend of Mor'du*. Pixar-nummers: Brave is Pixars 13e film. Gaelic in de film: "Mo ghaol" etc.

**Schotland – bronnen die een hintmaker gebruikt**
- **Schots-Gaelische telwoorden**: 0 neoni, 1 aon, 2 dhà, 3 trì, 4 ceithir, 5 còig, 6 sia, 7 seachd, 8 ochd, 9 naoi, 10 deich, 11 aon-deug, 12 dhà-dheug, 20 fichead, 100 ceud; personen tellen: aonar, dithis, triùir, ceathrar, còignear, sianar, seachdnar, ochdnar, naoinear, deichnear (controleer online bij twijfel). **Scots**: ane, twa, three, fower, five, sax, seiven, aicht, nine, ten. Gaelic spelling van cijfers kan ook gesproken (mp3) komen.
- **Gaelisch alfabet: 18 letters** a b c d e f g h i l m n o p r s t u (geen j k q v w x y z) → ciphers op 18 letters; **boomalfabet** A Ailm, B Beith, C Coll, D Dair, E Eadha, F Feàrn, G Gort, H Uath, I Iogh, L Luis, M Muin, N Nuin, O Onn, P Peith, R Ruis, S Suil, T Teine, U Ura. **Ogham** (Keltisch streepjesschrift op een stam; tabel geocachen.be/…/ogham/) en **Pictische symbolen**, **Keltische knopen**, **runen**.
- **Tartans**: Scottish Register of Tartans (STA/registratienummer, kleurvolgorde = streepjescode; "sett" met draadtellingen = getallen!). Clan-namen (MacDonald, Campbell, MacLeod, Stewart, Fraser, MacKenzie, Gordon, Cameron, MacGregor…).
- **Beroemde Schotten**: Sean Connery (Bond), Alexander Graham Bell (telefoon), John Logie Baird (televisie), James Watt (stoommachine), Alexander Fleming (penicilline), Robert Burns (dichter, 25 jan), Walter Scott, Arthur Conan Doyle, Robert Louis Stevenson, J.M. Barrie (Peter Pan), Mary Queen of Scots, William Wallace (Braveheart), Robert the Bruce, Rob Roy, Bonnie Prince Charlie, Adam Smith, David Hume, John Napier (logaritmen), James Clerk Maxwell, Kirkpatrick Macmillan (fiets), John Dunlop (band), Andy Murray, Ewan McGregor, Gerard Butler, David Tennant, Billy Connolly, Annie Lennox, Lewis Capaldi, Rod Stewart, Calvin Harris, Susan Boyle, Jackie Stewart, Alex Ferguson, Kenny Dalglish, Dolly the sheep (Roslin). Schotse **uitvindingen**: telefoon, tv, penicilline, stoommachine, fiets, luchtband, macadam, regenjas (Macintosh!), logaritmen, Kelvin-schaal, geldautomaat, ultrasound.
- **Aardrijkskunde**: hoofdstad Edinburgh, grootste stad Glasgow; steden Aberdeen, Dundee, Inverness, Stirling, Perth; **Loch Ness** (Nessie), Loch Lomond; **Ben Nevis 1345 m**; 282 **Munros** (>3000 ft); eilanden Skye, Mull, Islay, Orkney, Shetland, Hebriden; rivieren Tay, Clyde, Forth (Forth Bridge); Hadrian's Wall (Engeland!), Antonine Wall; **UK Ordnance Survey grid** (NN 1667 7128-achtige referenties, letterparen per 100 km-vak) en Britse postcodes (EH, G, AB, IV, PH, FK…); auto-kenteken, telefoonnetnummers (0131 Edinburgh, 0141 Glasgow).
- **Cultuur**: kilt/sporran, doedelzak (**bagpipe-chanter 9 tonen** → vingerzettingen als code), Highland Games (caber toss), haggis, whisky-regio's (Speyside, Highland, Lowland, Islay, Campbeltown), Burns Night 25 jan, St Andrew's Day 30 nov, Hogmanay, Saltire (wit andreaskruis op blauw), Lion Rampant, **unicorn** = nationaal dier, distel = nationale bloem, "Flower of Scotland", "Auld Lang Syne", Loch Ness Monster 1933, Edinburgh Fringe, Harry Potter-locaties (Glenfinnan-viaduct, Jacobite-stoomtrein), Outlander, Braveheart (1995, Mel Gibson), Trainspotting, Highlander ("There can be only one"), Macbeth, Brigadoon, Shrek (Schots accent), Groundskeeper Willie, Scrooge McDuck (Dagobert Duck is Schots!), Merida.
- **Getallen die vaak terugkomen**: 1314 (Bannockburn), 1707 (Act of Union), 1745/46 (Jacobieten, Culloden), 2014 (referendum), 1996 (Dolly), 1876 (telefoon), 1928 (penicilline), 1926 (tv), 1890 (Forth Bridge), 1933 (Nessie-foto), 893 (Edinburgh-Glasgow?) – controleer altijd.
- **Dieren uit de film/Schotland**: beer, kraai, paard, hooglander (Highland cow), hert, zalm, eenhoorn.

**Verwachte hintvormen 2026 (afgeleid van 2024/2025 + voorpret; achteraf: deze lijst stuurde de coach bij hint 83 de verkeerde kant op, zie §3 Editie 2026 voor wat het echt was)**: Gaelic telwoorden (tekst of audio), ogham/runen/Pictisch, tartan-kleurstrepen als cijfercode, strijkkralen-pixelart (QR/binair/Hexahue), DTMF/keuzemenu-tonen (telefoonlijn van de heks), kruispeiling/projectie met gradenboog, beroemde Schotten (geboortejaar/uitvinding-jaar → laatste cijfer), Brave-trivia (aantal broertjes = 3, clans = 4, Mor'du's broers = 4, 93 min, 2012), film-stills van de stemacteurs in andere films (Palantír-variant), anagrammen van Schotse plaatsnamen voor Oscar (OV-team), what3words (Engels), wachtwoord-docx via raadsels, jigidi-puzzels, stereogrammen, zoek-de-verschillen. Download bij elke hint meteen alle bijlagen en controleer bestandsnaam, EXIF en transparantie.

---

## 10. Testresultaat op editie 2024 (blind opgelost, daarna vergeleken met de uitleg)

Goed (methode én cijfers): LEGO Geschiedenis (6 teams), LEGO vragen (alle 13 deelantwoorden), Postbode/KIX (5 van 6 teams plausibel), weerstandscode (6 torentjesparen), Zwart-Wit (6 teams), schaakpaden (3 teams; cijfervolgorde zelf afgeleid). Methode goed herkend zonder uitwerking: Hexahue (Niet Alles Is Vierkant), Color Tokki (Overwatch), braille. Gemist: Hexahue in grijstinten, kruispeiling op de Legoland-kaart, thema-chronologie als toetsenbord-wachtwoord, stapeltellen van onderdeelnummers, rugnummers. Zie `references/resultaten-2024.md` voor de antwoorden per team.
