#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_db.py - generuje atlas.db dla aplikacji "Atlas grzybow".

Dane gatunkow siedza w gatunki.py - to jedyne miejsce, ktore edytujesz
przy dodawaniu nowych wpisow.

Uzycie: python3 tools/build_db.py assets/db/atlas.db
"""

import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gatunki import (SPECIES, KOLORY_SP, SIEDL_SP, LOOKALIKES,  # noqa: E402
                     KUCHNIA)

OUT = sys.argv[1] if len(sys.argv) > 1 else "atlas.db"

# Podmien na swoja nazwe uzytkownika GitHub.
GITHUB_USER = "JareckDaniels"
REPO = "atlas_grzybow"
MANIFEST_URL = (f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO}"
                f"/main/photos/manifest.json")

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE species (
    id                  INTEGER PRIMARY KEY,
    nazwa_pl            TEXT NOT NULL,
    nazwa_lac           TEXT NOT NULL,
    synonimy_pl         TEXT,
    rodzina             TEXT,
    jadalnosc           TEXT NOT NULL,
    hymenofor           TEXT NOT NULL,
    pierscien           INTEGER NOT NULL DEFAULT 0,
    pochwa              INTEGER NOT NULL DEFAULT 0,
    mleczko             INTEGER NOT NULL DEFAULT 0,
    sinienie            INTEGER NOT NULL DEFAULT 0,
    ksztalt_kapelusza   TEXT,
    powierzchnia        TEXT,
    wysyp_zarnikow      TEXT,
    zapach              TEXT,
    smak                TEXT,
    miesiac_od          INTEGER,
    miesiac_do          INTEGER,
    opis                TEXT,
    cechy_kluczowe      TEXT,
    uwagi               TEXT,
    kuchnia             TEXT,
    chroniony           INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE kolory (
    id      INTEGER PRIMARY KEY,
    nazwa   TEXT NOT NULL UNIQUE,
    etykieta TEXT NOT NULL,
    hex     TEXT
);

CREATE TABLE species_kolor (
    species_id  INTEGER NOT NULL REFERENCES species(id) ON DELETE CASCADE,
    kolor_id    INTEGER NOT NULL REFERENCES kolory(id) ON DELETE CASCADE,
    czesc       TEXT NOT NULL,
    PRIMARY KEY (species_id, kolor_id, czesc)
);

CREATE TABLE siedliska (
    id      INTEGER PRIMARY KEY,
    nazwa   TEXT NOT NULL UNIQUE
);

CREATE TABLE species_siedlisko (
    species_id      INTEGER NOT NULL REFERENCES species(id) ON DELETE CASCADE,
    siedlisko_id    INTEGER NOT NULL REFERENCES siedliska(id) ON DELETE CASCADE,
    PRIMARY KEY (species_id, siedlisko_id)
);

CREATE TABLE lookalikes (
    species_id  INTEGER NOT NULL REFERENCES species(id) ON DELETE CASCADE,
    similar_id  INTEGER NOT NULL REFERENCES species(id) ON DELETE CASCADE,
    roznice     TEXT NOT NULL,
    waga        INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (species_id, similar_id)
);

CREATE TABLE photos (
    id          INTEGER PRIMARY KEY,
    species_id  INTEGER NOT NULL REFERENCES species(id) ON DELETE CASCADE,
    plik        TEXT NOT NULL,
    autor       TEXT,
    licencja    TEXT,
    zrodlo_url  TEXT,
    kolejnosc   INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE meta (
    klucz   TEXT PRIMARY KEY,
    wartosc TEXT
);

CREATE INDEX idx_sp_hymenofor ON species(hymenofor);
CREATE INDEX idx_sp_jadalnosc ON species(jadalnosc);
CREATE INDEX idx_sp_nazwa_pl  ON species(nazwa_pl);
CREATE INDEX idx_sk_kolor     ON species_kolor(kolor_id, czesc);
CREATE INDEX idx_ss_sied      ON species_siedlisko(siedlisko_id);
CREATE INDEX idx_photos_sp    ON photos(species_id, kolejnosc);
"""

# (klucz, etykieta wyswietlana, hex)
KOLORY = [
    ("bialy", "biały", "#F5F5F0"),
    ("kremowy", "kremowy", "#F0E6D2"),
    ("zolty", "żółty", "#E8C547"),
    ("pomaranczowy", "pomarańczowy", "#E08A2E"),
    ("czerwony", "czerwony", "#C0392B"),
    ("rudy", "rudy", "#A0522D"),
    ("brazowy", "brązowy", "#7B5230"),
    ("ciemnobrazowy", "ciemnobrązowy", "#4A3320"),
    ("szary", "szary", "#8C8C8C"),
    ("czarny", "czarny", "#2B2B2B"),
    ("zielonkawy", "zielonkawy", "#7A8B4F"),
    ("oliwkowy", "oliwkowy", "#6B6B3A"),
    ("fioletowy", "fioletowy", "#7D5BA6"),
    ("rozowy", "różowy", "#D9909C"),
    ("niebieski", "niebieski", "#5B7BA6"),
]

SIEDLISKA = [
    "las liściasty", "las iglasty", "las mieszany", "bory sosnowe",
    "buczyny", "dąbrowy", "brzeziny", "świerczyny", "łąki i pastwiska",
    "parki i zadrzewienia", "drewno martwe", "drewno żywych drzew",
    "torfowiska", "obrzeża lasu", "tereny ruderalne",
]


def waliduj():
    """Kontrola spojnosci danych przed zapisem."""
    bledy = []
    ids = [s[0] for s in SPECIES]

    if len(ids) != len(set(ids)):
        bledy.append("Zduplikowane id gatunkow")

    dozwolone_jad = {"jadalny", "warunkowo", "niejadalny", "trujacy", "smiertelny"}
    dozwolone_hym = {"blaszki", "rurki", "kolce", "gladki", "fadki", "brak"}

    for s in SPECIES:
        sid, pl, lac = s[0], s[1], s[2]
        if s[5] not in dozwolone_jad:
            bledy.append(f"[{sid}] {pl}: zla jadalnosc '{s[5]}'")
        if s[6] not in dozwolone_hym:
            bledy.append(f"[{sid}] {pl}: zly hymenofor '{s[6]}'")
        if len(s) != 22:
            bledy.append(f"[{sid}] {pl}: krotka ma {len(s)} pol, oczekiwano 22")
        mo, md = s[16], s[17]
        if mo is not None and not (1 <= mo <= 12):
            bledy.append(f"[{sid}] {pl}: miesiac_od={mo}")
        if md is not None and not (1 <= md <= 12):
            bledy.append(f"[{sid}] {pl}: miesiac_do={md}")
        if sid not in KOLORY_SP:
            bledy.append(f"[{sid}] {pl}: brak wpisu w KOLORY_SP")
        if sid not in SIEDL_SP:
            bledy.append(f"[{sid}] {pl}: brak wpisu w SIEDL_SP")

    znane_kolory = {k[0] for k in KOLORY}
    for sid, lst in KOLORY_SP.items():
        if sid not in ids:
            bledy.append(f"KOLORY_SP: nieznane id {sid}")
        for kol, czesc in lst:
            if kol not in znane_kolory:
                bledy.append(f"[{sid}] nieznany kolor '{kol}'")
            if czesc not in {"kapelusz", "trzon", "hymenofor", "miazsz"}:
                bledy.append(f"[{sid}] nieznana czesc '{czesc}'")

    znane_sied = set(SIEDLISKA)
    for sid, lst in SIEDL_SP.items():
        if sid not in ids:
            bledy.append(f"SIEDL_SP: nieznane id {sid}")
        for s in lst:
            if s not in znane_sied:
                bledy.append(f"[{sid}] nieznane siedlisko '{s}'")

    for a, b, _, w in LOOKALIKES:
        if a not in ids:
            bledy.append(f"LOOKALIKES: nieznane species_id {a}")
        if b not in ids:
            bledy.append(f"LOOKALIKES: nieznane similar_id {b}")
        if a == b:
            bledy.append(f"LOOKALIKES: gatunek {a} wskazuje sam na siebie")
        if w not in (1, 2, 3):
            bledy.append(f"LOOKALIKES {a}->{b}: zla waga {w}")

    par = {(a, b) for a, b, _, _ in LOOKALIKES}
    if len(par) != len(LOOKALIKES):
        bledy.append("LOOKALIKES: zduplikowane pary")

    # Opisy kulinarne: tylko dla jadalnych, obowiazkowe dla wszystkich.
    jadalne = {s[0] for s in SPECIES if s[5] in ("jadalny", "warunkowo")}
    nazwy = {s[0]: s[1] for s in SPECIES}

    for sid in sorted(jadalne - set(KUCHNIA)):
        bledy.append(f"[{sid}] {nazwy[sid]}: jadalny, ale brak wpisu w KUCHNIA")

    for sid in sorted(set(KUCHNIA) - jadalne):
        bledy.append(f"[{sid}] {nazwy.get(sid, '?')}: wpis w KUCHNIA, "
                     f"ale gatunek nie jest jadalny")

    # Przy warunkowo jadalnych opis MUSI wspominac o obrobce termicznej -
    # inaczej rubryka kulinarna zacheca do zjedzenia grzyba na surowo.
    warunkowe = {s[0] for s in SPECIES if s[5] == "warunkowo"}
    slowa = ("ugotowan", "gotowan", "obróbce", "obróbki", "termicznej",
             "odlan", "odlać", "ugotować")
    for sid in sorted(warunkowe & set(KUCHNIA)):
        if not any(w in KUCHNIA[sid].lower() for w in slowa):
            bledy.append(f"[{sid}] {nazwy[sid]}: warunkowo jadalny, ale opis "
                         f"kulinarny nie wspomina o obrobce termicznej")

    return bledy


def main():
    bledy = waliduj()
    if bledy:
        print("BLEDY W DANYCH:")
        for b in bledy:
            print("  !", b)
        sys.exit(1)

    katalog = os.path.dirname(OUT)
    if katalog:
        os.makedirs(katalog, exist_ok=True)
    if os.path.exists(OUT):
        os.remove(OUT)

    con = sqlite3.connect(OUT)
    con.executescript(SCHEMA)
    cur = con.cursor()

    cur.executemany("INSERT INTO kolory(nazwa,etykieta,hex) VALUES (?,?,?)", KOLORY)
    cur.executemany("INSERT INTO siedliska(nazwa) VALUES (?)",
                    [(s,) for s in SIEDLISKA])

    # Doklejamy opis kulinarny przed ostatnim polem (chroniony).
    wiersze = [tuple(s[:21]) + (KUCHNIA.get(s[0]),) + (s[21],) for s in SPECIES]
    cur.executemany("""
        INSERT INTO species(id,nazwa_pl,nazwa_lac,synonimy_pl,rodzina,jadalnosc,
            hymenofor,pierscien,pochwa,mleczko,sinienie,ksztalt_kapelusza,
            powierzchnia,wysyp_zarnikow,zapach,smak,miesiac_od,miesiac_do,
            opis,cechy_kluczowe,uwagi,kuchnia,chroniony)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, wiersze)

    kol_id = dict(cur.execute("SELECT nazwa,id FROM kolory").fetchall())
    sied_id = dict(cur.execute("SELECT nazwa,id FROM siedliska").fetchall())

    for sp, lst in KOLORY_SP.items():
        cur.executemany(
            "INSERT OR IGNORE INTO species_kolor(species_id,kolor_id,czesc) "
            "VALUES (?,?,?)",
            [(sp, kol_id[k], c) for k, c in lst])

    for sp, lst in SIEDL_SP.items():
        cur.executemany(
            "INSERT OR IGNORE INTO species_siedlisko(species_id,siedlisko_id) "
            "VALUES (?,?)",
            [(sp, sied_id[s]) for s in lst])

    cur.executemany(
        "INSERT INTO lookalikes(species_id,similar_id,roznice,waga) "
        "VALUES (?,?,?,?)", LOOKALIKES)

    # Placeholdery zdjec - nazwy plikow wynikaja z nazwy lacinskiej.
    for s in SPECIES:
        slug = s[2].lower().replace(" ", "_").replace("-", "_")
        for i in range(1, 4):
            cur.execute(
                "INSERT INTO photos(species_id,plik,kolejnosc) VALUES (?,?,?)",
                (s[0], f"{slug}_{i}.webp", i - 1))

    cur.executemany("INSERT INTO meta(klucz,wartosc) VALUES (?,?)", [
        ("db_version", "3"),
        ("photos_version", "0"),
        ("photos_manifest_url", MANIFEST_URL),
    ])

    con.commit()

    n = cur.execute("SELECT COUNT(*) FROM species").fetchone()[0]
    nl = cur.execute("SELECT COUNT(*) FROM lookalikes").fetchone()[0]
    smiert = cur.execute(
        "SELECT COUNT(*) FROM species WHERE jadalnosc='smiertelny'").fetchone()[0]
    nk = cur.execute(
        "SELECT COUNT(*) FROM species WHERE kuchnia IS NOT NULL").fetchone()[0]
    con.execute("VACUUM")
    con.close()

    print(f"OK: {OUT}")
    print(f"    {n} gatunkow ({smiert} smiertelnie trujacych)")
    print(f"    {nl} powiazan sobowtorow")
    print(f"    {nk} opisow kulinarnych")
    print(f"    {os.path.getsize(OUT)/1024:.0f} KB")


if __name__ == "__main__":
    main()
