#!/usr/bin/env python3
"""Jotihunt hint-hulpjes. Gebruik: python3 scripts/jh.py <commando> [args]

Commando's:
  rd2wgs X Y            RD (6 cijfers of 4-cijferige hintvorm) -> lat, lon + Google Maps link
  wgs2rd LAT LON        WGS84 -> RD
  projectie X Y AFSTAND GRADEN   projectie vanaf RD-punt (afstand in m, of '7.31km')
  kenny TEKST [--letters mpf]    Kenny code decoderen; --letters geeft de 3 gebruikte letters in m,p,f-volgorde
  kennyall TEKST                 probeer alle 6 toewijzingen van de 3 letters
  seg7 TEKST            7-segment codes (ABC, BCFG, DP ...) -> cijfers
  caesar TEKST          alle 26 shifts tonen (met score voor NL/EN)
  caesarzin TEKST       per zin de beste shift (cijfer) bepalen
  letterwaarde WOORD..  A=1..Z=26 som per woord
  stapeltel WOORD..     letterwaarde herleid tot 1 cijfer (digital root)
  binair BITS           binaire string -> decimaal (ook per 4 bits)
  imgdiff MAP           (oud) ruwe pixelgebieden t.o.v. de eerste afbeelding
  verschillen [--basis B] [--uit MAP] [--drempel N] BESTANDEN|MAPPEN|ZIP
                        zoek de verschillen: aantal verschillen per afbeelding t.o.v. de basis = cijfer
  symbolen [--vak X0,Y0,X1,Y1] [--uit MAP] [--gevoelig 0.1] [--samen N] [--inkt C] BESTANDEN|MAP
                        raster van herhaalde symbolen transcriberen: gelijke vormen -> klassen A, B, C (gedeeld
                        over alle bestanden), raster per rij en per kolom; klassen.png + <naam>_labels.png ter controle
  transcribeer [--taal nl] [--van S] [--tot S] [--venster 10] [--naast] [--marker PAD] BESTANDEN
                        gesproken tekst uit audio/video (lokale Whisper large-v3-turbo, offline). Standaard vrij:
                        geen prompt, geen taal. Doorlopend met tijden én per venster van 10 s los (beter voor losse
                        letters of woorden onder muziek). --naast schrijft <naam>.transcript.txt naast elk bestand
  anagram LETTERS [WOORDENLIJST]  anagram zoeken in woordenlijst (default: NS-stations Gelderland)
  telwoorden TEKST      aaneengeschreven NL telwoorden -> cijfers
"""
import sys, math, re, string, unicodedata, os, glob

# ---------- coördinaten ----------
def rd2wgs(x, y):
    x, y = float(x), float(y)
    if x < 10000: x *= 100
    if y < 10000: y *= 100
    dX = (x - 155000) * 1e-5; dY = (y - 463000) * 1e-5
    lat = 52.15517440 + (3235.65389*dY - 32.58297*dX**2 - 0.24750*dY**2 - 0.84978*dX**2*dY
          - 0.06550*dY**3 - 0.01709*dX**2*dY**2 - 0.00738*dX + 0.00530*dX**4 - 0.00039*dX**2*dY**3
          + 0.00033*dX**4*dY - 0.00012*dX*dY) / 3600
    lon = 5.38720621 + (5260.52916*dX + 105.94684*dX*dY + 2.45656*dX*dY**2 - 0.81885*dX**3
          + 0.05594*dX*dY**3 - 0.05607*dX**3*dY + 0.01199*dY - 0.00256*dX**3*dY**2 + 0.00128*dX*dY**4
          + 0.00022*dY**2 - 0.00022*dX**2 + 0.00026*dX**5) / 3600
    return lat, lon

def wgs2rd(lat, lon):
    lat, lon = float(lat), float(lon)
    dF = 0.36*(lat - 52.15517440); dL = 0.36*(lon - 5.38720621)
    x = 155000 + 190094.945*dL - 11832.228*dF*dL - 114.221*dF**2*dL - 32.391*dL**3 - 0.705*dF \
        - 2.340*dF**3*dL - 0.608*dF*dL**3 - 0.008*dL**2 + 0.148*dF**2*dL**3
    y = 463000 + 309056.544*dF + 3638.893*dL**2 + 73.077*dF**2 - 157.984*dF*dL**2 + 59.788*dF**3 \
        + 0.433*dL - 6.439*dF**2*dL**2 - 0.032*dF*dL + 0.092*dL**4 - 0.054*dF*dL**4
    return x, y

def hintvorm(x, y):
    return f"{int(x//100)} {int(y//100)}"

def projectie(x, y, afstand, graden):
    x, y = float(x), float(y)
    if isinstance(afstand, str) and afstand.lower().endswith('km'):
        d = float(afstand[:-2].replace(',', '.')) * 1000
    else:
        d = float(str(afstand).replace(',', '.'))
    b = math.radians(float(graden))
    return x + d*math.sin(b), y + d*math.cos(b)

# ---------- codes ----------
def kenny(tekst, letters='mpf'):
    tabel = {}
    for i, ch in enumerate(string.ascii_lowercase):
        tabel[letters[i//9] + letters[(i//3) % 3] + letters[i % 3]] = ch
    out = []
    for w in tekst.lower().split():
        w = ''.join(c for c in w if c in letters)
        out.append(''.join(tabel.get(w[i:i+3], '?') for i in range(0, len(w), 3)))
    return ' '.join(out)

SEG7 = {'ABCDEF': '0', 'BC': '1', 'ABDEG': '2', 'ABCDG': '3', 'BCFG': '4', 'ACDFG': '5',
        'ACDEFG': '6', 'ABC': '7', 'ABCDEFG': '8', 'ABCDFG': '9', 'DP': '.'}
def seg7(tekst):
    return ''.join(SEG7.get(''.join(sorted(t.upper())), ' ' + t + ' ') if t.upper() != 'DP' else '.'
                   for t in tekst.split())

VEEL = set("de het een en van in is dat die op te zijn met voor niet aan er ook als maar om dan nog wel bij uit tot the and of to a in is was that he for it with as his on be at by i this had not are but from or have an they which one you were her all she there would their we him been has when who will more no if out so said what up its about into than them can only other new some could time these two may then do first any my now such like our over man me even most made after also did many before must through back years where much your way well down should because each just those people mr how too little state good very make world still own see men work long get here between both life being under never day same another know while last might us great old year off come since against go came right used take three".split())
def score(t):
    return sum(1 for w in re.findall(r'[a-z]+', t.lower()) if w in VEEL)

def caesar_shift(t, n):
    out = []
    for c in t:
        if c.isalpha() and c.isascii():
            base = 65 if c.isupper() else 97
            out.append(chr((ord(c) - base - n) % 26 + base))
        else:
            out.append(c)
    return ''.join(out)

def caesar(tekst):
    for n in range(26):
        t = caesar_shift(tekst, n)
        print(f"{n:2d} [{score(t):3d}] {t[:110]}")

def caesarzin(tekst):
    zinnen = [z for z in re.split(r'(?<=[.!?])\s+', tekst.strip()) if z]
    cijfers = []
    for z in zinnen:
        best = max(range(26), key=lambda n: score(caesar_shift(z, n)))
        vooruit = (26 - best) % 26   # de shift waarmee de zin versleuteld is
        cijfer = vooruit if vooruit <= 9 else best
        cijfers.append(str(cijfer))
        print(f"versleuteld met +{vooruit:2d} (terug {best:2d}): {caesar_shift(z, best)[:80]}")
    print('cijfers (0-9 gekozen):', ' '.join(cijfers))

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def letterwaarde(w):
    return sum(ord(c) - 96 for c in strip_accents(w).lower() if 'a' <= c <= 'z')

def stapeltel(n):
    n = int(n)
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def binair(bits):
    b = ''.join(c for c in bits if c in '01')
    print('heel getal:', int(b, 2))
    if len(b) % 4 == 0:
        print('per 4 bits:', ' '.join(str(int(b[i:i+4], 2)) for i in range(0, len(b), 4)))
    if len(b) % 8 == 0:
        print('per 8 bits (ascii):', ''.join(chr(int(b[i:i+8], 2)) for i in range(0, len(b), 8)))

def imgdiff(map_, drempel=40, minpix=20):
    from PIL import Image, ImageChops
    import numpy as np
    from scipy import ndimage  # optioneel; valt terug op bbox-telling
    fs = sorted(glob.glob(os.path.join(map_, '*')))
    ims = [Image.open(f).convert('L') for f in fs]
    # referentie: eerste; verschillen = aantal samenhangende blobs
    base = ims[0]
    for f, im in zip(fs, ims):
        d = np.array(ImageChops.difference(base, im)) > drempel
        d = ndimage.binary_dilation(d, iterations=8)
        lab, n = ndimage.label(d)
        groot = sum(1 for i in range(1, n+1) if (lab == i).sum() > minpix)
        print(f"{os.path.basename(f)}: {groot} verschil-gebied(en) t.o.v. {os.path.basename(fs[0])}")

# ---------- zoek de verschillen ----------
def _natkey(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', os.path.basename(s))]


def _afbeeldingen(paden):
    exts = ('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif')
    out = []
    for p in paden:
        if os.path.isdir(p):
            out += [os.path.join(p, f) for f in os.listdir(p) if f.lower().endswith(exts)]
        elif p.lower().endswith('.zip'):
            import zipfile, tempfile
            d = tempfile.mkdtemp(prefix='jh_zip_'); zipfile.ZipFile(p).extractall(d)
            for root, _, files in os.walk(d):
                out += [os.path.join(root, f) for f in files if f.lower().endswith(exts) and not f.startswith('._')]
        elif os.path.isfile(p):
            out.append(p)
    return sorted(dict.fromkeys(out), key=_natkey)


def _laad(pad, size=None):
    from PIL import Image
    import numpy as np
    im = Image.open(pad).convert('RGB')
    if size and im.size != size:
        im = im.resize(size, Image.LANCZOS)
    return np.asarray(im).astype(np.float32)


def _diffkaart(a, b):
    """Per pixel het grootste kanaalverschil, na lichte vervaging (dempt JPEG-ruis) en een kleine uitlijning."""
    import numpy as np
    from scipy import ndimage
    try:
        import cv2
        ga, gb = a.mean(axis=2), b.mean(axis=2)
        (dx, dy), _ = cv2.phaseCorrelate(ga.astype(np.float64), gb.astype(np.float64))
        if 0.5 < abs(dx) < 20 or 0.5 < abs(dy) < 20:
            b = ndimage.shift(b, (-dy, -dx, 0), order=1, mode='nearest')
    except Exception:
        pass
    fa = ndimage.gaussian_filter(a, sigma=(1.2, 1.2, 0)); fb = ndimage.gaussian_filter(b, sigma=(1.2, 1.2, 0))
    return np.abs(fa - fb).max(axis=2)


def _tel(diff, drempel=None, straal=None, min_frac=0.00004):
    """Telt samenhangende verschilgebieden. Geeft (aantal, lijst van (y0,x0,y1,x1,oppervlak)), drempel)."""
    import numpy as np
    from scipy import ndimage
    h, w = diff.shape
    if drempel is None:
        med = float(np.median(diff)); mad = float(np.median(np.abs(diff - med))) * 1.4826
        drempel = max(28.0, med + 8 * mad)
    masker = diff > drempel
    masker = ndimage.binary_opening(masker, structure=np.ones((3, 3)))
    if straal is None:
        straal = max(3, int(round(0.008 * (h * h + w * w) ** 0.5)))
    samen = ndimage.binary_dilation(masker, structure=np.ones((3, 3)), iterations=straal)
    lab, n = ndimage.label(samen)
    min_opp = max(20, int(min_frac * h * w))
    gebieden = []
    for i, sl in enumerate(ndimage.find_objects(lab), start=1):
        if sl is None: continue
        opp = int((masker[sl] & (lab[sl] == i)).sum())
        if opp >= min_opp:
            gebieden.append((sl[0].start, sl[1].start, sl[0].stop, sl[1].stop, opp))
    return len(gebieden), gebieden, drempel


def _verplaatsingen(B, A, gebieden):
    """Zoekt paren gebieden die samen één verplaatst object zijn: wat in de basis bij gebied i stond, staat in de
    variant bij gebied j. Geeft lijst van (i, j, score)."""
    import numpy as np
    try:
        import cv2
    except Exception:
        return []
    h, w = B.shape[:2]; diag = (h * h + w * w) ** 0.5
    gb = B.mean(axis=2).astype(np.float32); ga = A.mean(axis=2).astype(np.float32)
    paren = []
    for i, (y0, x0, y1, x1, _) in enumerate(gebieden):
        for j, (v0, u0, v1, u1, _) in enumerate(gebieden):
            if i == j: continue
            ci = ((y0 + y1) / 2, (x0 + x1) / 2); cj = ((v0 + v1) / 2, (u0 + u1) / 2)
            if ((ci[0] - cj[0]) ** 2 + (ci[1] - cj[1]) ** 2) ** 0.5 > 0.15 * diag: continue
            sj = (max(1, (v1 - v0) * (u1 - u0)) / max(1, (y1 - y0) * (x1 - x0)))
            if not (0.33 < sj < 3): continue
            sjabloon = gb[y0:y1, x0:x1]
            m = max(6, int(0.25 * max(v1 - v0, u1 - u0)))
            zoek = ga[max(0, v0 - m):min(h, v1 + m), max(0, u0 - m):min(w, u1 + m)]
            if zoek.shape[0] < sjabloon.shape[0] or zoek.shape[1] < sjabloon.shape[1] or sjabloon.std() < 3: continue
            score = float(cv2.matchTemplate(zoek, sjabloon, cv2.TM_CCOEFF_NORMED).max())
            if score > 0.75: paren.append((i, j, score))
    return paren


def verschillen(paden, basis=None, uit=None, drempel=None):
    """Zoek de verschillen: aantal verschillen per afbeelding t.o.v. een basisafbeelding = cijfer.

    Zonder --basis kiest hij een bestand met 'basis', 'base', 'origineel', 'original' of '00' in de naam,
    anders de afbeelding die gemiddeld het minst van de rest afwijkt.
    Telt bij drie gevoeligheden; 'stabiel' = fijn en normaal geven hetzelfde (grof is ter info: naburige verschillen
    kunnen dan versmelten). Een verplaatst object (verdwijnt op de ene plek, verschijnt vlakbij) telt als één verschil.
    Met --uit MAP komen er afbeeldingen met genummerde kaders bij, plus overzicht.png.
    """
    import numpy as np
    from PIL import Image, ImageDraw
    fs = _afbeeldingen(paden)
    if basis is None:
        kand = [f for f in fs if re.search(r'(basis|base|origine|original|^0+[ _.-])', os.path.basename(f).lower())]
        if kand:
            basis = kand[0]
        else:
            size = Image.open(fs[0]).size
            arrs = [_laad(f, size) for f in fs]
            tot = [sum(float(np.abs(a - b).mean()) for b in arrs) for a in arrs]
            basis = fs[int(np.argmin(tot))]
            print(f'(geen basis opgegeven; gekozen als basis: {os.path.basename(basis)} = meest "gemiddelde" afbeelding)')
    fs = [f for f in fs if os.path.abspath(f) != os.path.abspath(basis)]
    b_im = Image.open(basis); size = b_im.size
    B = _laad(basis)
    if uit: os.makedirs(uit, exist_ok=True)
    print(f'basis: {os.path.basename(basis)} ({size[0]}x{size[1]}); {len(fs)} afbeeldingen\n')
    print(f"{'afbeelding':34s} {'aantal':>6s}  {'gevoeligheid laag/mid/hoog':26s} oordeel")
    cijfers, annot = [], []
    for f in fs:
        if Image.open(f).size != size: print(f'  let op: {os.path.basename(f)} heeft een ander formaat; geschaald naar de basis')
        A_ = _laad(f, size)
        D = _diffkaart(B, A_)
        diag = (size[0] ** 2 + size[1] ** 2) ** 0.5

        def telling(straal):
            n, geb, t = _tel(D, drempel, straal=straal)
            pr = _verplaatsingen(B, A_, geb); sm = set()
            for i, j, sc in pr:
                if i not in sm and j not in sm: sm.add(j)   # j is de nieuwe plek van i: één verschil
            return n - len(sm), geb, pr, sm

        n_mid, gebieden, paren, samen = telling(None)
        verpl = len(samen)
        n_laag = telling(max(2, int(round(0.004 * diag))))[0]
        n_hoog = telling(max(4, int(round(0.016 * diag))))[0]
        stabiel = n_laag == n_mid
        oordeel = 'stabiel' if stabiel else 'CONTROLEER (aantal hangt af van samenvoegen; bekijk de kaders)'
        if stabiel and n_hoog != n_mid: oordeel += f' (grof samenvoegen: {n_hoog}, naburige verschillen versmelten)'
        if n_mid > 9: oordeel += '; >9, is het wel één cijfer per afbeelding?'
        if verpl: oordeel += f'; {verpl} verplaatst object(en) als één verschil geteld'
        cijfers.append(n_mid)
        print(f'{os.path.basename(f)[:34]:34s} {n_mid:>6d}  {n_laag:>3d} / {n_mid:>3d} / {n_hoog:>3d}{"":13s} {oordeel}')
        if uit:
            im = Image.open(f).convert('RGB').resize(size); dr = ImageDraw.Draw(im)
            lw = max(2, size[0] // 300)
            nummer, k = {}, 0
            for idx in range(len(gebieden)):
                if idx in samen: continue
                k += 1; nummer[idx] = k
            for i, j, sc in paren:
                if j in samen and i in nummer: nummer[j] = nummer[i]
            for idx, (y0, x0, y1, x1, _) in enumerate(gebieden):
                kleur = (0, 200, 255) if any(idx in (i, j) for i, j, _ in paren if j in samen) else (255, 0, 0)
                dr.rectangle([x0, y0, x1, y1], outline=kleur, width=lw)
                dr.text((x0 + 3, y0 + 2), str(nummer.get(idx, '?')), fill=kleur)
            dr.text((8, 8), f'{n_mid} verschillen', fill=(255, 255, 0))
            naam = os.path.join(uit, 'verschil_' + os.path.splitext(os.path.basename(f))[0] + '.png'); im.save(naam); annot.append(naam)
    reeks = ''.join(str(c) if c <= 9 else f'({c})' for c in cijfers)
    print(f'\ncijfers in bestandsvolgorde: {reeks}')
    if len(cijfers) == 8: print(f'als coördinaat (4+4): {reeks[:4]} {reeks[4:]}')
    if uit and annot:
        th = [Image.open(a) for a in annot]; tw = 480; tth = int(tw * size[1] / size[0])
        cols = 4; rows = (len(th) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * tw, rows * tth), 'white')
        for i, t in enumerate(th): sheet.paste(t.resize((tw, tth)), ((i % cols) * tw, (i // cols) * tth))
        sheet.save(os.path.join(uit, 'overzicht.png')); print(f'geannoteerd: {uit}/ (overzicht.png + per afbeelding)')
    return cijfers


STATIONS = """Arnhem Centraal;Arnhem Zuid;Arnhem Velperpoort;Arnhem Presikhaaf;Nijmegen;Nijmegen Dukenburg;Nijmegen Heyendaal;Nijmegen Lent;Nijmegen Goffert;Ede-Wageningen;Ede Centrum;Apeldoorn;Apeldoorn De Maten;Apeldoorn Osseveld;Zutphen;Doetinchem;Doetinchem De Huet;Tiel;Tiel Passewaaij;Barneveld Centrum;Barneveld Noord;Barneveld Zuid;Harderwijk;Nunspeet;Dieren;Velp;Elst;Zevenaar;Zevenaar Poort;Didam;Wijchen;Culemborg;Geldermalsen;Winterswijk;Winterswijk West;Lichtenvoorde-Groenlo;Aalten;Varsseveld;Terborg;Gaanderen;Wehl;Duiven;Westervoort;Lunteren;Hoevelaken;Putten;Ermelo;'t Harde;Wezep;Oosterbeek;Wolfheze;Rheden;De Steeg;Brummen;Voorst-Empe;Klarenbeek;Twello;Eefde;Vorden;Ruurlo;Lochem;Opheusden;Kesteren;Hemmen-Dodewaard;Zaltbommel;Beesd;Leerdam;Arnhem;Nijkerk;Amersfoort;Utrecht Centraal;Den Bosch;Deventer;Zwolle;Oss;Boxmeer;Cuijk;Mook-Molenhoek;Lingewaard;Huissen;Bemmel;Wageningen;Renkum;Beuningen;Druten;Rhenen;Veenendaal;Veenendaal De Klomp;Veenendaal Centrum;Veenendaal West""".split(';')
# ---------- symbolen transcriberen ----------
def _symbolen_glyphs(pad, vak=None, samen=0, inkt=None):
    """Losse tekens (connected components) uit een afbeelding. Geeft (grijs-uitsnede, binair, [glyph-dicts])."""
    import numpy as np, cv2
    from PIL import Image
    im = np.array(Image.open(pad).convert('L'))
    if vak: x0, y0, x1, y1 = vak; im = im[y0:y1, x0:x1]
    blok = max(15, (min(im.shape) // 25) | 1)
    bw = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, blok, inkt if inkt is not None else 12)
    lab = bw
    if samen: lab = cv2.dilate(bw, np.ones((2 * samen + 1, 2 * samen + 1), np.uint8))
    n, cc, st, _ = cv2.connectedComponentsWithStats((lab > 0).astype(np.uint8), 8)
    g = []
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if a < 6 or w < 3 or h < 3: continue
        g.append({'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h), 'a': int(a), 'id': i})
    if not g: return im, bw, []
    # houd de tekens van de meest voorkomende grootte over (ruis en grote vlakken eruit)
    hs = np.array([max(t['w'], t['h']) for t in g], float)
    groot = hs[hs >= np.percentile(hs, 30)]
    hist, rand = np.histogram(np.log(groot), bins=20)
    k = int(np.argmax(hist)); typ = math.exp((rand[k] + rand[k + 1]) / 2)
    g = [t for t in g if 0.45 * typ <= max(t['w'], t['h']) <= 2.2 * typ]
    for t in g:
        m = (cc[t['y']:t['y'] + t['h'], t['x']:t['x'] + t['w']] == t['id']) & (bw[t['y']:t['y'] + t['h'], t['x']:t['x'] + t['w']] > 0)
        s = max(t['w'], t['h']); vierkant = np.zeros((s, s), np.uint8)
        oy, ox = (s - t['h']) // 2, (s - t['w']) // 2
        vierkant[oy:oy + t['h'], ox:ox + t['w']] = m.astype(np.uint8) * 255
        s2 = cv2.GaussianBlur(cv2.resize(vierkant, (24, 24), interpolation=cv2.INTER_AREA).astype(float), (5, 5), 1.5)
        v = s2.ravel(); t['vec'] = v / (np.linalg.norm(v) + 1e-9)
        t['cx'], t['cy'] = t['x'] + t['w'] / 2, t['y'] + t['h'] / 2
    return im, bw, g


def _groepeer(waarden, gat):
    """1D-clustering: gesorteerde waarden opdelen waar het gat groter is dan `gat`. Geeft index per waarde."""
    volg = sorted(range(len(waarden)), key=lambda i: waarden[i])
    idx, groep, vorige = [0] * len(waarden), 0, None
    for i in volg:
        if vorige is not None and waarden[i] - vorige > gat: groep += 1
        idx[i] = groep; vorige = waarden[i]
    return idx


def symbolen(paden, vak=None, uit=None, gevoelig=0.1, samen=0, inkt=None):
    """Transcribeer een raster van herhaalde symbolen: knip tekens uit, groepeer gelijke vormen in klassen A, B, C …
    (gedeeld over alle afbeeldingen), en print per afbeelding het raster (rijen) en per kolom van boven naar beneden."""
    import numpy as np, cv2
    from scipy.cluster.hierarchy import linkage, fcluster
    bestanden = _afbeeldingen(paden)
    alle, per = [], {}
    for p in bestanden:
        im, bw, g = _symbolen_glyphs(p, vak, samen, inkt)
        per[p] = (im, g); alle += [(p, t) for t in g]
    if len(alle) < 2: print('te weinig tekens gevonden; geef --vak x0,y0,x1,y1 rond de symbolen of verlaag --inkt'); return
    X = np.array([t['vec'] for _, t in alle])
    asp = np.array([[math.log(t['w'] / t['h'])] for _, t in alle])
    Z = linkage(np.hstack([X, asp * 0.3]), method='average', metric='cosine')
    lab = fcluster(Z, gevoelig, criterion='distance')
    tel = {}
    for l in lab: tel[l] = tel.get(l, 0) + 1
    namen = {}
    for i, (l, _) in enumerate(sorted(tel.items(), key=lambda kv: -kv[1])):
        namen[l] = string.ascii_uppercase[i] if i < 26 else f'{i}'
    zeldzaam = {l for l, c in tel.items() if c < max(2, 0.01 * len(alle))}
    for (p, t), l in zip(alle, lab): t['k'] = '?' if l in zeldzaam else namen[l]
    gesorteerd = sorted(tel.items(), key=lambda kv: -kv[1])
    print(f"{len(bestanden)} afbeelding(en), {len(alle)} tekens, {len(tel) - len(zeldzaam)} klassen: " +
          ', '.join(f"{namen[l]}={c}" for l, c in gesorteerd if l not in zeldzaam))
    if len(zeldzaam) > 0.5 * len(tel) and sum(tel[l] for l in zeldzaam) > 0.3 * len(alle):
        print('  LET OP: veel ruis (achtergrond telt mee). Geef --vak x0,y0,x1,y1 rond alleen de symbolen.')
    if zeldzaam: print(f"  {sum(tel[l] for l in zeldzaam)} tekens in {len(zeldzaam)} zeldzame klassen staan als '?' (ruis, of een teken dat afwijkt: bekijk de labels-plaat)")
    if len(tel) - len(zeldzaam) > 12: print('  (veel klassen: vormen variëren → --gevoelig 0.2; tekens uit losse delen (puntjes, streepjes) → --samen 2)')
    hs = [t['h'] for _, t in alle]; ws = [t['w'] for _, t in alle]
    mh, mw = float(np.median(hs)), float(np.median(ws))
    for p in bestanden:
        im, g = per[p]
        if not g: print(f"\n== {os.path.basename(p)}: geen tekens"); continue
        echt_g = [t for t in g if t['k'] != '?'] or g
        ri_e = _groepeer([t['cy'] for t in echt_g], 0.5 * mh); ki_e = _groepeer([t['cx'] for t in echt_g], 0.45 * mw)
        rij_y = [float(np.mean([t['cy'] for t, r in zip(echt_g, ri_e) if r == i])) for i in range(max(ri_e) + 1)]
        kol_x = [float(np.mean([t['cx'] for t, k in zip(echt_g, ki_e) if k == i])) for i in range(max(ki_e) + 1)]
        R, K = len(rij_y), len(kol_x)
        raster = [['.'] * K for _ in range(R)]
        for t in g:   # elk teken naar de dichtstbijzijnde rij/kolom; ruis die nergens bij hoort valt weg
            r = min(range(R), key=lambda i: abs(rij_y[i] - t['cy'])); k = min(range(K), key=lambda i: abs(kol_x[i] - t['cx']))
            if abs(rij_y[r] - t['cy']) > 0.5 * mh or abs(kol_x[k] - t['cx']) > 0.5 * mw: continue
            c = raster[r][k]
            if c == '.' or (c == '?' and t['k'] != '?'): raster[r][k] = t['k']
            elif t['k'] != '?': raster[r][k] = c + t['k']
        echt = lambda c: c not in ('.', '?')
        houd_r = [r for r in range(R) if sum(echt(c) for c in raster[r]) >= 2 or K == 1]
        houd_k = [k for k in range(K) if sum(echt(raster[r][k]) for r in range(R)) >= 2 or R == 1]
        raster = [[raster[r][k] for k in houd_k] for r in houd_r]; R, K = len(houd_r), len(houd_k)
        print(f"\n== {os.path.basename(p)}: {len(g)} tekens, {R} rijen x {K} kolommen")
        for rij in raster: print('  ' + ' '.join(c.ljust(1) for c in rij))
        print('  per kolom (boven -> onder):')
        for k in range(K): print(f"  k{k + 1:<2} " + ''.join(raster[r][k] for r in range(R)))
    if uit:
        os.makedirs(uit, exist_ok=True)
        _symbolen_platen(per, alle, lab, namen, tel, uit)
        print(f"\nklassen.png (voorbeelden per klasse) en <naam>_labels.png (labels over het beeld) in {uit}")


def _symbolen_platen(per, alle, lab, namen, tel, uit):
    import numpy as np, cv2
    kleuren = [(220, 40, 40), (40, 140, 40), (40, 70, 220), (200, 120, 0), (150, 40, 180), (0, 150, 160), (120, 120, 0), (200, 0, 120)]
    # klassenplaat: per klasse tot 10 voorbeelden, 3x vergroot
    rijen = []
    for l, c in sorted(tel.items(), key=lambda kv: -kv[1]):
        vb = [(p, t) for (p, t), x in zip(alle, lab) if x == l][:10]
        tegels = []
        for p, t in vb:
            im = per[p][0]; m = 3
            c_ = im[max(0, t['y'] - 3):t['y'] + t['h'] + 3, max(0, t['x'] - 3):t['x'] + t['w'] + 3]
            c_ = cv2.resize(c_, None, fx=m, fy=m, interpolation=cv2.INTER_NEAREST)
            tegel = np.full((90, 90), 255, np.uint8); h, w = min(90, c_.shape[0]), min(90, c_.shape[1])
            tegel[:h, :w] = c_[:h, :w]; tegels.append(tegel)
        kop = np.full((90, 110), 255, np.uint8)
        cv2.putText(kop, f"{namen[l]} x{c}", (4, 52), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 0, 2)
        rijen.append(np.hstack([kop] + tegels + [np.full((90, 90), 255, np.uint8)] * (10 - len(tegels))))
    cv2.imwrite(os.path.join(uit, 'klassen.png'), np.vstack(rijen))
    for p, (im, g) in per.items():
        f = 2; ov = cv2.cvtColor(cv2.resize(im, None, fx=f, fy=f), cv2.COLOR_GRAY2BGR)
        for t in g:
            kl = kleuren[(ord(t['k'][0]) - 65) % len(kleuren)]
            cv2.rectangle(ov, (t['x'] * f, t['y'] * f), ((t['x'] + t['w']) * f, (t['y'] + t['h']) * f), kl, 1)
            cv2.putText(ov, t['k'], (t['x'] * f, t['y'] * f - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.45, kl, 1)
        cv2.imwrite(os.path.join(uit, os.path.splitext(os.path.basename(p))[0] + '_labels.png'), ov)


# ---------- audio: vrije transcriptie ----------
WHISPER = 'openai/whisper-large-v3-turbo'
_asr = None
# wat Whisper op stilte of muziek verzint
_HALLU = re.compile(r'^(so|you|um+|uh+|hmm+|thank you\.?|thanks for watching!?|bye\.?|amen\.?|muziek|music|\[?muziek\]?|♪+|\.+)$|subtit|ondertitel|субтитр', re.I)


def _whisper():
    global _asr
    if _asr is None:
        os.environ.setdefault('HF_HUB_OFFLINE', '1')
        import warnings, torch
        from transformers import pipeline
        from transformers.utils import logging as hflog
        warnings.filterwarnings('ignore'); hflog.set_verbosity_error()
        dev = 'mps' if torch.backends.mps.is_available() else ('cuda' if torch.cuda.is_available() else 'cpu')
        _asr = pipeline('automatic-speech-recognition', model=WHISPER, device=dev, dtype=torch.float16 if dev != 'cpu' else torch.float32)
    return _asr


def _audio16k(pad, van=None, tot=None):
    """Geluidsspoor als 16 kHz mono float32 (numpy) via ffmpeg; leeg als er geen audio is."""
    import subprocess, numpy as np
    cmd = ['ffmpeg', '-loglevel', 'error', '-nostdin']
    if van is not None: cmd += ['-ss', str(van)]
    if tot is not None: cmd += ['-to', str(tot)]
    cmd += ['-i', pad, '-vn', '-ac', '1', '-ar', '16000', '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).copy()


def _schoon(t):
    """Weg met wat Whisper op stilte verzint; een herhaallus ('Bay E. Bay E. …') inkorten maar laten staan (kan info zijn)."""
    t = re.sub(r'(.{2,12}?)(?:\s*\1){4,}', r'\1 (herhaald)', t.strip())
    kern = t.replace(' (herhaald)', '')
    return '' if not re.search(r'\w', kern) or _HALLU.search(kern) else t[:200]


def transcribeer(pad, taal=None, van=None, tot=None, venster=10):
    """Vrije transcriptie (geen prompt; taal alleen als expliciet gevraagd) als leesbare tekst."""
    a = _audio16k(pad, van, tot)
    naam = os.path.basename(pad); start = float(van or 0)
    kop = f"Transcriptie van {naam} (Whisper large-v3-turbo, lokaal; {'taal ' + taal if taal else 'vrij: geen prompt, taal automatisch'})"
    if len(a) < 1600:
        return kop + '\nGeen audiospoor (of leeg geluid) in dit bestand.\n'
    dur = len(a) / 16000
    asr = _whisper(); gk = {'language': taal} if taal else {}
    r = asr({'raw': a, 'sampling_rate': 16000}, return_timestamps=True, generate_kwargs=gk)
    regels = [kop, f"Duur {dur:.1f} s" + (f" (vanaf {start:g} s)" if start else ''), '', '## Doorlopend, met tijden (s)']
    woorden = 0
    for c in r.get('chunks') or [{'timestamp': (0, dur), 'text': r['text']}]:
        t = _schoon(c['text']); b, e = c['timestamp']
        if not t: continue
        woorden += len(t.split())
        regels.append(f"[{start + (b or 0):6.1f}–{start + (e if e is not None else dur):6.1f}] {t}")
    if woorden == 0: regels.append('(niets herkend)')
    vensters = []
    if dur > venster * 1.5:
        regels += ['', f'## Per venster van {venster} s, elk los getranscribeerd (stilte/muziek = –)']
        n = int(venster * 16000)
        begins = [s for s in range(0, len(a), n) if len(a) - s >= 8000]
        uit = asr([{'raw': a[s:s + n], 'sampling_rate': 16000} for s in begins], generate_kwargs=gk | {'max_new_tokens': 48}, batch_size=8)
        for s, u in zip(begins, uit):
            t = _schoon(u['text']); vensters.append(t)
            regels.append(f"[{start + s / 16000:6.1f}–{start + min(s + n, len(a)) / 16000:6.1f}] {t or '–'}")
    wpm = woorden / max(dur / 60, 1e-9)
    if dur > 10 and wpm < 40:
        regels += ['', f"LET OP: weinig spraak herkend ({woorden} woorden in {dur:.0f} s). Vaak losse woorden of letters onder muziek, "
                   "die Whisper slecht pakt. Concludeer NIET dat er geen spraak is. Vergelijk de twee lezingen hierboven, "
                   "knip rond de tijden een stuk uit en transcribeer dat apart (jh.py transcribeer --van S --tot S, eventueel --taal nl), "
                   "en denk aan losse letternamen (a, bee, cee …) of telwoorden."]
    return '\n'.join(regels) + '\n'


def transcribeer_cli(r):
    o = {}; naast = False; marker = None; rest = []; it = iter(r)
    for x in it:
        if x == '--taal': o['taal'] = next(it)
        elif x == '--van': o['van'] = float(next(it))
        elif x == '--tot': o['tot'] = float(next(it))
        elif x == '--venster': o['venster'] = float(next(it))
        elif x == '--naast': naast = True
        elif x == '--marker': marker = next(it)
        else: rest.append(x)
    try:
        for p in rest:
            uit = os.path.splitext(p)[0] + '.transcript.txt'
            if naast and os.path.exists(uit): continue
            try: t = transcribeer(p, **o)
            except Exception as e: t = f'Transcriptie van {os.path.basename(p)} mislukt: {e}\n'
            if naast:
                open(uit, 'w').write(t); print(f'transcript: {os.path.basename(p)} -> {os.path.basename(uit)}', flush=True)
            else:
                print(t, flush=True)
    finally:
        if marker and os.path.exists(marker): os.remove(marker)


def anagram(letters, lijst=None):
    key = sorted(c for c in strip_accents(letters).lower() if c.isalpha())
    kandidaten = lijst or STATIONS
    for k in kandidaten:
        if sorted(c for c in strip_accents(k).lower() if c.isalpha()) == key:
            print('MATCH:', k)
    # ook sub-anagrammen tonen op letterfrequentie-afstand
    from collections import Counter
    ck = Counter(key)
    dichtbij = sorted(kandidaten, key=lambda k: sum((Counter(sorted(c for c in strip_accents(k).lower() if c.isalpha())) - ck).values()) + sum((ck - Counter(sorted(c for c in strip_accents(k).lower() if c.isalpha()))).values()))
    print('dichtstbij:', dichtbij[:8])

TELW = {'nul': '0', 'een': '1', 'één': '1', 'twee': '2', 'drie': '3', 'vier': '4', 'vijf': '5', 'zes': '6', 'zeven': '7', 'acht': '8', 'negen': '9',
        'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
        'null': '0', 'eins': '1', 'zwei': '2', 'drei': '3', 'fuenf': '5', 'sechs': '6', 'sieben': '7', 'neun': '9'}
def telwoorden(t):
    t = strip_accents(t.lower().replace('ü', 'ue'))
    out = ''; i = 0
    while i < len(t):
        for w in sorted(TELW, key=len, reverse=True):
            if t.startswith(w, i):
                out += TELW[w]; i += len(w); break
        else:
            out += t[i] if not t[i].isalpha() else '?'; i += 1
    return out

# ---------- CLI ----------
def main(a):
    if not a or a[0] in ('-h', '--help'):
        print(__doc__); return
    c, r = a[0], a[1:]
    if c == 'rd2wgs':
        lat, lon = rd2wgs(*r[:2]); print(f"{lat:.6f}, {lon:.6f}  https://www.google.com/maps?q={lat:.6f},{lon:.6f}")
    elif c == 'wgs2rd':
        x, y = wgs2rd(*r[:2]); print(f"RD {x:.0f} {y:.0f}  hint {hintvorm(x, y)}")
    elif c == 'projectie':
        x, y = projectie(*r[:4]); lat, lon = rd2wgs(x, y)
        print(f"RD {x:.0f} {y:.0f}  hint {hintvorm(x, y)}  wgs {lat:.6f},{lon:.6f}")
    elif c == 'kenny':
        letters = 'mpf'
        if '--letters' in r:
            i = r.index('--letters'); letters = r[i+1]; r = r[:i] + r[i+2:]
        print(kenny(' '.join(r), letters))
    elif c == 'kennyall':
        import itertools
        t = ' '.join(r); ls = sorted(set(ch for ch in t.lower() if ch.isalpha()))
        for p in itertools.permutations(ls, 3):
            print(''.join(p), '->', kenny(t, ''.join(p)))
    elif c == 'seg7': print(seg7(' '.join(r)))
    elif c == 'caesar': caesar(' '.join(r))
    elif c == 'caesarzin': caesarzin(' '.join(r))
    elif c == 'letterwaarde':
        for w in r: print(w, letterwaarde(w))
    elif c == 'stapeltel':
        for w in r: print(w, letterwaarde(w), '->', stapeltel(letterwaarde(w)))
    elif c == 'binair': binair(' '.join(r))
    elif c == 'imgdiff': imgdiff(r[0])
    elif c == 'verschillen':
        basis = uit = None; drempel = None; rest = []
        it = iter(r)
        for x in it:
            if x == '--basis': basis = next(it)
            elif x == '--uit': uit = next(it)
            elif x == '--drempel': drempel = float(next(it))
            else: rest.append(x)
        verschillen(rest, basis=basis, uit=uit, drempel=drempel)
    elif c == 'symbolen':
        o = {}; rest = []; it = iter(r)
        for x in it:
            if x == '--vak': o['vak'] = tuple(int(float(v)) for v in next(it).split(','))
            elif x == '--uit': o['uit'] = next(it)
            elif x == '--gevoelig': o['gevoelig'] = float(next(it))
            elif x == '--samen': o['samen'] = int(next(it))
            elif x == '--inkt': o['inkt'] = float(next(it))
            else: rest.append(x)
        symbolen(rest, **o)
    elif c == 'transcribeer': transcribeer_cli(r)
    elif c == 'anagram': anagram(r[0], open(r[1]).read().split('\n') if len(r) > 1 else None)
    elif c == 'telwoorden': print(telwoorden(' '.join(r)))
    else: print('onbekend commando', c); print(__doc__)

if __name__ == '__main__':
    main(sys.argv[1:])
