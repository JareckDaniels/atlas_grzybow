#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_photos.py - pobiera zdjecia z Wikimedia Commons dla gatunkow z atlas.db.

UWAGA: Commons zawiera bledne oznaczenia. Kazde zdjecie WYMAGA recznej
weryfikacji przed publikacja. Skrypt generuje przeglad HTML do zatwierdzania.

Uzycie:
  python3 fetch_photos.py fetch   --db assets/db/atlas.db --out photos_raw
  python3 fetch_photos.py review  --out photos_raw          # generuje review.html
  python3 fetch_photos.py pack    --out photos_raw --zip photos.zip --version 1

Zaleznosci: pip install requests pillow
"""

import argparse
import json
import os
import sqlite3
import sys
import time
import zipfile

try:
    import requests
    from PIL import Image
except ImportError:
    print("Brak zaleznosci: pip install requests pillow")
    sys.exit(1)

API = "https://commons.wikimedia.org/w/api.php"

# Wikimedia odrzuca (403) zapytania bez sensownego User-Agenta.
# Podmien adres na swoj - to wymog regulaminu Wikimedia, nie kosmetyka.
KONTAKT = os.environ.get("WIKI_KONTAKT", "atlas-grzybow@example.org")
UA = f"AtlasGrzybow/1.1 (edukacyjny atlas grzybow; {KONTAKT})"

NA_GATUNEK = 4
SZEROKOSC = 1200
JAKOSC = 82

# Licencje dopuszczajace redystrybucje. Porownanie na tekscie
# znormalizowanym: male litery, myslniki i podkreslenia -> spacje.
# Commons zwraca np. "CC BY-SA 3.0", "CC0", "Public domain", "PD-old".
OK_WZORCE = ("cc by", "cc0", "cc zero", "public domain", "pd ",
             "no restrictions", "attribution")

# Te odrzucamy mimo ze zawieraja "cc by" - wykluczaja komercyjne
# uzycie albo modyfikacje, wiec nie nadaja sie do redystrybucji w APK.
ZLE_WZORCE = ("nc", "nd", "noncommercial", "no derivat")


# Skany starych atlasow i ryciny - dla atlasu chcemy fotografii,
# bo rysunek z 1890 r. nie pomaga rozpoznac grzyba w lesie.
ZLE_TYTULY = ("atlas des champignons", "flora batava", "coloured figures",
              "bresadola", "illustration", "planche", "drawing", "dessin",
              "engraving", "lithograph", "plate ", "tab.", "manual of poisonous",
              "icones", "svampe", "boletus_granulatus_—")


def tytul_ok(tytul: str) -> bool:
    """Odrzuca skany rycin i tablic z dawnych atlasow."""
    t = tytul.lower()
    return not any(z in t for z in ZLE_TYTULY)


def licencja_ok(nazwa: str) -> bool:
    """Czy licencja pozwala na rozpowszechnianie w paczce zdjec."""
    if not nazwa:
        return False
    n = nazwa.lower().replace("-", " ").replace("_", " ")
    n = " ".join(n.split())
    if any(z in n.split() or z in n for z in ZLE_WZORCE):
        return False
    return any(w in n for w in OK_WZORCE)


_SESJA = None


def sesja():
    """Jedna sesja HTTP na caly proces - Wikimedia lubi keep-alive."""
    global _SESJA
    if _SESJA is None:
        _SESJA = requests.Session()
        _SESJA.headers.update({
            "User-Agent": UA,
            "Accept": "image/webp,image/jpeg,image/png,*/*",
            "Referer": "https://commons.wikimedia.org/",
        })
    return _SESJA


def api(params):
    params = {**params, "format": "json"}
    r = sesja().get(API, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def szukaj_plikow(nazwa_lac, limit=12):
    """Zwraca liste tytulow plikow z kategorii gatunku."""
    tytuly = []
    try:
        d = api({
            "action": "query", "list": "categorymembers",
            "cmtitle": f"Category:{nazwa_lac}", "cmtype": "file",
            "cmlimit": limit,
        })
        tytuly = [m["title"] for m in d.get("query", {}).get("categorymembers", [])]
    except Exception:
        pass

    if not tytuly:
        d = api({
            "action": "query", "list": "search",
            "srsearch": f'{nazwa_lac} filetype:bitmap',
            "srnamespace": 6, "srlimit": limit,
        })
        tytuly = [m["title"] for m in d.get("query", {}).get("search", [])]

    return tytuly


def info_pliku(tytul):
    d = api({
        "action": "query", "titles": tytul, "prop": "imageinfo",
        "iiprop": "url|extmetadata|size", "iiurlwidth": SZEROKOSC,
    })
    pages = d.get("query", {}).get("pages", {})
    for _, p in pages.items():
        ii = p.get("imageinfo")
        if not ii:
            continue
        info = ii[0]
        meta = info.get("extmetadata", {})
        lic = (meta.get("LicenseShortName", {}).get("value") or "").lower()
        autor = meta.get("Artist", {}).get("value") or "nieznany"
        # Usuwamy tagi HTML z pola autora.
        import re
        autor = re.sub(r"<[^>]+>", "", autor).strip()
        return {
            "url": info.get("thumburl") or info.get("url"),
            "opis_url": info.get("descriptionurl"),
            "licencja": meta.get("LicenseShortName", {}).get("value", "?"),
            "licencja_lc": lic,
            "autor": autor[:120],
            "szer": info.get("width"),
        }
    return None


def pobierz_z_ponowieniem(url, prob=3):
    """Wikimedia bywa kapryslna - ponawiamy z narastajaca przerwa."""
    for i in range(prob):
        try:
            r = sesja().get(url, timeout=60)
            if r.status_code == 200:
                return r
            if r.status_code in (403, 429, 503):
                time.sleep(2 * (i + 1))
                continue
            return None
        except Exception:
            time.sleep(2 * (i + 1))
    return None


def cmd_fetch(args):
    con = sqlite3.connect(args.db)
    gatunki = con.execute(
        "SELECT id, nazwa_pl, nazwa_lac FROM species ORDER BY id").fetchall()
    con.close()

    os.makedirs(args.out, exist_ok=True)
    katalog_meta = os.path.join(args.out, "_meta.json")
    meta = {}
    if os.path.exists(katalog_meta):
        meta = json.load(open(katalog_meta, encoding="utf-8"))

    for sid, pl, lac in gatunki:
        slug = lac.lower().replace(" ", "_")
        if any(k.startswith(slug) for k in meta):
            print(f"[pomijam] {pl}")
            continue

        print(f"[{sid}] {pl} ({lac})")
        try:
            tytuly = szukaj_plikow(lac)
        except Exception as e:
            print(f"    blad wyszukiwania: {e}")
            continue

        zapisane = 0
        for tytul in tytuly:
            if zapisane >= NA_GATUNEK:
                break
            try:
                if not tytul_ok(tytul):
                    continue
                info = info_pliku(tytul)
                if not info or not info["url"]:
                    continue
                if not licencja_ok(info["licencja"]):
                    print(f"    pomijam licencje: {info['licencja']}")
                    continue

                r = pobierz_z_ponowieniem(info["url"])
                if r is None:
                    print("    nie udalo sie pobrac (403/timeout)")
                    continue

                tmp = os.path.join(args.out, f".tmp_{sid}")
                with open(tmp, "wb") as f:
                    f.write(r.content)

                zapisane += 1
                nazwa = f"{slug}_{zapisane}.webp"
                sciezka = os.path.join(args.out, nazwa)

                im = Image.open(tmp).convert("RGB")
                if im.width > SZEROKOSC:
                    h = int(im.height * SZEROKOSC / im.width)
                    im = im.resize((SZEROKOSC, h), Image.LANCZOS)
                im.save(sciezka, "WEBP", quality=JAKOSC, method=6)
                os.remove(tmp)

                meta[nazwa] = {
                    "species_id": sid,
                    "nazwa_pl": pl,
                    "nazwa_lac": lac,
                    "autor": info["autor"],
                    "licencja": info["licencja"],
                    "zrodlo": info["opis_url"],
                    "commons_title": tytul,
                    "zatwierdzone": None,
                }
                print(f"    + {nazwa}  [{info['licencja']}]")
                time.sleep(0.4)
            except Exception as e:
                print(f"    blad: {e}")

        json.dump(meta, open(katalog_meta, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)

    print(f"\nGotowe. {len(meta)} plikow w {args.out}")
    print("Nastepny krok: python3 fetch_photos.py review --out", args.out)


REVIEW_HTML = """<!DOCTYPE html><html lang="pl"><head><meta charset="utf-8">
<title>Weryfikacja zdjec</title><style>
body{font-family:system-ui,sans-serif;margin:0;padding:24px;background:#f5f2ec}
h1{font-size:20px}
.g{margin-bottom:32px;background:#fff;border-radius:12px;padding:16px}
.g h2{font-size:16px;margin:0 0 4px}.g .lac{color:#777;font-style:italic;font-size:13px;margin-bottom:12px}
.row{display:flex;gap:12px;flex-wrap:wrap}
.card{width:220px;border:2px solid #ddd;border-radius:10px;overflow:hidden;background:#fafafa}
.card.ok{border-color:#2e7d32}.card.no{border-color:#c62828;opacity:.45}
.card img{width:100%;height:160px;object-fit:cover;display:block;cursor:pointer}
.card .m{padding:8px;font-size:11px;color:#555;line-height:1.4}
.btns{display:flex;gap:4px;padding:0 8px 8px}
.btns button{flex:1;padding:5px;font-size:12px;cursor:pointer;border:1px solid #ccc;background:#fff;border-radius:6px}
#save{position:fixed;bottom:20px;right:20px;padding:14px 22px;background:#2e7d32;color:#fff;
border:none;border-radius:10px;font-size:15px;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,.2)}
</style></head><body>
<h1>Weryfikacja zdjec — zatwierdz tylko te, ktore na pewno przedstawiaja dany gatunek</h1>
<p style="color:#a33">Commons zawiera bledne oznaczenia. W razie watpliwosci odrzuc.</p>
<div id="app"></div>
<button id="save">Zapisz decyzje (_meta.json)</button>
<script>
const META = __META__;
const app = document.getElementById('app');
const grupy = {};
for (const [plik, m] of Object.entries(META)) {
  (grupy[m.nazwa_pl] ||= {lac: m.nazwa_lac, pliki: []}).pliki.push([plik, m]);
}
for (const [pl, g] of Object.entries(grupy)) {
  const d = document.createElement('div'); d.className = 'g';
  d.innerHTML = `<h2>${pl}</h2><div class="lac">${g.lac}</div>`;
  const row = document.createElement('div'); row.className = 'row';
  for (const [plik, m] of g.pliki) {
    const c = document.createElement('div');
    c.className = 'card' + (m.zatwierdzone === true ? ' ok' : m.zatwierdzone === false ? ' no' : '');
    c.innerHTML = `<img src="${plik}" onclick="window.open('${m.zrodlo}')">
      <div class="m"><b>${plik}</b><br>${m.autor}<br>${m.licencja}</div>
      <div class="btns"><button data-ok>OK</button><button data-no>Odrzuc</button></div>`;
    c.querySelector('[data-ok]').onclick = () => { META[plik].zatwierdzone = true; c.className='card ok'; };
    c.querySelector('[data-no]').onclick = () => { META[plik].zatwierdzone = false; c.className='card no'; };
    row.appendChild(c);
  }
  d.appendChild(row); app.appendChild(d);
}
document.getElementById('save').onclick = () => {
  const blob = new Blob([JSON.stringify(META, null, 1)], {type:'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = '_meta.json'; a.click();
};
</script></body></html>"""


def cmd_review(args):
    meta_path = os.path.join(args.out, "_meta.json")
    meta = json.load(open(meta_path, encoding="utf-8"))
    html = REVIEW_HTML.replace("__META__", json.dumps(meta, ensure_ascii=False))
    out = os.path.join(args.out, "review.html")
    open(out, "w", encoding="utf-8").write(html)
    print(f"Otworz w przegladarce: {out}")
    print("Po zatwierdzeniu pobierz _meta.json i nadpisz plik w tym katalogu.")


def cmd_pack(args):
    meta = json.load(open(os.path.join(args.out, "_meta.json"), encoding="utf-8"))
    zatwierdzone = {k: v for k, v in meta.items() if v.get("zatwierdzone") is True}

    if not zatwierdzone:
        print("Brak zatwierdzonych zdjec. Uruchom najpierw 'review'.")
        return

    with zipfile.ZipFile(args.zip, "w", zipfile.ZIP_STORED) as z:
        for plik in zatwierdzone:
            p = os.path.join(args.out, plik)
            if os.path.exists(p):
                z.write(p, plik)

    rozmiar = os.path.getsize(args.zip)
    manifest = {
        "version": args.version,
        "url": args.url,
        "size": rozmiar,
        "count": len(zatwierdzone),
    }
    json.dump(manifest, open("manifest.json", "w"), indent=1)

    # Wpisy do tabeli photos.
    sql = ["DELETE FROM photos;"]
    kolejnosc = {}
    for plik, m in sorted(zatwierdzone.items()):
        sid = m["species_id"]
        k = kolejnosc.get(sid, 0)
        kolejnosc[sid] = k + 1
        autor = m["autor"].replace("'", "''")
        lic = m["licencja"].replace("'", "''")
        zr = (m.get("zrodlo") or "").replace("'", "''")
        sql.append(
            f"INSERT INTO photos(species_id,plik,autor,licencja,zrodlo_url,kolejnosc) "
            f"VALUES ({sid},'{plik}','{autor}','{lic}','{zr}',{k});")
    open("photos.sql", "w", encoding="utf-8").write("\n".join(sql))

    print(f"{args.zip}: {len(zatwierdzone)} zdjec, {rozmiar/1048576:.1f} MB")
    print("manifest.json + photos.sql wygenerowane.")
    print("Wgraj ZIP jako GitHub Release, manifest.json do repo,")
    print("photos.sql zaaplikuj w build_db.py.")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fetch")
    f.add_argument("--db", default="assets/db/atlas.db")
    f.add_argument("--out", default="photos_raw")
    f.set_defaults(fn=cmd_fetch)

    r = sub.add_parser("review")
    r.add_argument("--out", default="photos_raw")
    r.set_defaults(fn=cmd_review)

    p = sub.add_parser("pack")
    p.add_argument("--out", default="photos_raw")
    p.add_argument("--zip", default="photos.zip")
    p.add_argument("--version", type=int, default=1)
    p.add_argument("--url", default="https://github.com/USER/atlas-grzybow/"
                                    "releases/download/photos-v1/photos.zip")
    p.set_defaults(fn=cmd_pack)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
