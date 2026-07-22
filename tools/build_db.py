#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_db.py - generuje atlas.db dla aplikacji "Atlas grzybow".
Uruchomienie: python3 build_db.py [sciezka_wyjsciowa]
Wynik trafia do assets/db/atlas.db w projekcie Fluttera.
"""

import sqlite3
import sys
import os

OUT = sys.argv[1] if len(sys.argv) > 1 else "atlas.db"

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE species (
    id                  INTEGER PRIMARY KEY,
    nazwa_pl            TEXT NOT NULL,
    nazwa_lac           TEXT NOT NULL,
    synonimy_pl         TEXT,
    rodzina             TEXT,
    jadalnosc           TEXT NOT NULL,   -- jadalny|warunkowo|niejadalny|trujacy|smiertelny
    hymenofor           TEXT NOT NULL,   -- blaszki|rurki|kolce|gladki|fadki|brak
    pierscien           INTEGER NOT NULL DEFAULT 0,
    pochwa              INTEGER NOT NULL DEFAULT 0,
    mleczko             INTEGER NOT NULL DEFAULT 0,
    sinienie            INTEGER NOT NULL DEFAULT 0,
    ksztalt_kapelusza   TEXT,
    powierzchnia        TEXT,            -- gladka|luskowata|wlokienkowa|sluzowata|aksamitna
    wysyp_zarnikow      TEXT,
    zapach              TEXT,
    smak                TEXT,
    miesiac_od          INTEGER,
    miesiac_do          INTEGER,
    opis                TEXT,
    cechy_kluczowe      TEXT,
    uwagi               TEXT,
    chroniony           INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE kolory (
    id      INTEGER PRIMARY KEY,
    nazwa   TEXT NOT NULL UNIQUE,
    hex     TEXT
);

CREATE TABLE species_kolor (
    species_id  INTEGER NOT NULL REFERENCES species(id) ON DELETE CASCADE,
    kolor_id    INTEGER NOT NULL REFERENCES kolory(id) ON DELETE CASCADE,
    czesc       TEXT NOT NULL,           -- kapelusz|trzon|hymenofor|miazsz
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
    waga        INTEGER NOT NULL DEFAULT 1,  -- 3 = pomylka smiertelna
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

CREATE VIRTUAL TABLE species_fts USING fts5(
    nazwa_pl, nazwa_lac, synonimy_pl, opis,
    content='species', content_rowid='id', tokenize='unicode61'
);

CREATE TRIGGER species_ai AFTER INSERT ON species BEGIN
  INSERT INTO species_fts(rowid, nazwa_pl, nazwa_lac, synonimy_pl, opis)
  VALUES (new.id, new.nazwa_pl, new.nazwa_lac, new.synonimy_pl, new.opis);
END;
CREATE TRIGGER species_ad AFTER DELETE ON species BEGIN
  INSERT INTO species_fts(species_fts, rowid, nazwa_pl, nazwa_lac, synonimy_pl, opis)
  VALUES('delete', old.id, old.nazwa_pl, old.nazwa_lac, old.synonimy_pl, old.opis);
END;
CREATE TRIGGER species_au AFTER UPDATE ON species BEGIN
  INSERT INTO species_fts(species_fts, rowid, nazwa_pl, nazwa_lac, synonimy_pl, opis)
  VALUES('delete', old.id, old.nazwa_pl, old.nazwa_lac, old.synonimy_pl, old.opis);
  INSERT INTO species_fts(rowid, nazwa_pl, nazwa_lac, synonimy_pl, opis)
  VALUES (new.id, new.nazwa_pl, new.nazwa_lac, new.synonimy_pl, new.opis);
END;
"""

KOLORY = [
    ("bialy", "#F5F5F0"), ("kremowy", "#F0E6D2"), ("zolty", "#E8C547"),
    ("pomaranczowy", "#E08A2E"), ("czerwony", "#C0392B"), ("brazowy", "#7B5230"),
    ("rudy", "#A0522D"), ("ciemnobrazowy", "#4A3320"), ("szary", "#8C8C8C"),
    ("czarny", "#2B2B2B"), ("zielonkawy", "#7A8B4F"), ("oliwkowy", "#6B6B3A"),
    ("fioletowy", "#7D5BA6"), ("rozowy", "#D9909C"), ("niebieski", "#5B7BA6"),
]

SIEDLISKA = [
    "las lisciasty", "las iglasty", "las mieszany", "bory sosnowe",
    "buczyny", "debiny", "brzeziny", "swierczyny", "laki i pastwiska",
    "parki i zadrzewienia", "drewno martwe", "drewno zywych drzew",
    "torfowiska", "obrzeza lasu", "tereny ruderalne",
]

# (nazwa_pl, nazwa_lac, synonimy, rodzina, jadalnosc, hymenofor, pierscien,
#  pochwa, mleczko, sinienie, ksztalt, powierzchnia, wysyp, zapach, smak,
#  mies_od, mies_do, opis, cechy_kluczowe, uwagi, chroniony)
SPECIES = [
    (1, "Borowik szlachetny", "Boletus edulis", "prawdziwek, grzyb prawdziwy",
     "Boletaceae", "jadalny", "rurki", 0, 0, 0, 0,
     "poduszkowaty", "gladka", "oliwkowobrazowy", "przyjemny, grzybowy", "lagodny, orzechowy",
     6, 11,
     "Najbardziej ceniony grzyb jadalny w Polsce. Kapelusz osiaga 8-25 cm srednicy, "
     "poczatkowo polkulisty, pozniej poduszkowaty, o barwie od jasnobezowej po ciemnobrazowa. "
     "Trzon bulwiasty, jasny, pokryty bialawa siateczka w gornej czesci. Rurki biale, "
     "z wiekiem zoltawe do oliwkowozielonych, nie sinieja po uszkodzeniu. Miazsz bialy, "
     "niezmienny na przekroju, o lagodnym orzechowym smaku.",
     "Biala siateczka na trzonie; miazsz nie sinieje; rurki biale do oliwkowych",
     "Nie mylic z goryczakiem zolciowym - ten ma ciemna siateczke i skrajnie gorzki smak.", 0),

    (2, "Goryczak zolciowy", "Tylopilus felleus", "szatan falszywy",
     "Boletaceae", "niejadalny", "rurki", 0, 0, 0, 0,
     "poduszkowaty", "gladka", "rozowawy", "slaby", "skrajnie gorzki",
     6, 10,
     "Grzyb bardzo podobny do borowika szlachetnego, przez co czesto trafia do koszyka "
     "poczatkujacych zbieraczy. Kapelusz 5-15 cm, brazowy. Kluczowa roznica: siateczka "
     "na trzonie jest ciemna, wyrazna i kontrastowa, a rurki z wiekiem przybieraja odcien "
     "rozowy zamiast oliwkowego. Miazsz gorzki jak zolc - jeden owocnik potrafi zepsuc "
     "cala potrawe.",
     "Ciemna siateczka na trzonie; rozowawe rurki; smak skrajnie gorzki",
     "Nie jest trujacy, ale gorycz nie znika po obrobce termicznej.", 0),

    (3, "Muchomor sromotnikowy", "Amanita phalloides", "zielona smierc",
     "Amanitaceae", "smiertelny", "blaszki", 1, 1, 0, 0,
     "dzwonkowaty do plaskiego", "gladka", "bialy", "mdly, z wiekiem nieprzyjemny", "lagodny",
     7, 11,
     "Najbardziej trujacy grzyb Europy, odpowiadajacy za wiekszosc smiertelnych zatruc. "
     "Kapelusz 5-15 cm, oliwkowozielony do zoltawozielonego, z wrosnietymi promienistymi "
     "wloknami. Blaszki zawsze biale, wolne. Trzon z blonaistym pierscieniem i - kluczowe - "
     "workowata pochwa u podstawy, czesto ukryta w sciolce. Objawy zatrucia pojawiaja sie "
     "dopiero po 6-24 godzinach, gdy uszkodzenie watroby juz trwa.",
     "Biale blaszki + pierscien + workowata pochwa u podstawy trzonu",
     "SMIERTELNIE TRUJACY. Zawsze wykopuj grzyb w calosci, aby zobaczyc podstawe trzonu. "
     "Jeden owocnik moze zabic doroslego czlowieka.", 0),

    (4, "Pieczarka polna", "Agaricus campestris", "pieczarka lakowa",
     "Agaricaceae", "jadalny", "blaszki", 1, 0, 0, 0,
     "polkulisty do plaskiego", "gladka", "ciemnobrazowy", "przyjemny, pieczarkowy", "lagodny",
     6, 10,
     "Popularny grzyb lak i pastwisk, blisko spokrewniony z pieczarka hodowlana. "
     "Kapelusz 4-10 cm, bialy do kremowego. Blaszki - i to jest cecha rozstrzygajaca - "
     "sa u mlodych owocnikow rozowe, a z wiekiem ciemnieja do czekoladowobrazowych. "
     "Trzon z delikatnym, czesto zanikajacym pierscieniem, bez pochwy.",
     "Rozowe, potem brazowe blaszki; brak pochwy; rosnie na otwartych terenach",
     "Rozowe blaszki to najwazniejsza roznica wobec bialych muchomorow.", 0),

    (5, "Muchomor czerwony", "Amanita muscaria", "musznik",
     "Amanitaceae", "trujacy", "blaszki", 1, 1, 0, 0,
     "polkulisty do plaskiego", "gladka", "bialy", "slaby", "lagodny",
     7, 11,
     "Najbardziej rozpoznawalny grzyb swiata. Kapelusz 8-20 cm, jaskrawoczerwony, "
     "pokryty bialymi kosmkami - pozostalosciami oslony, ktore moga zostac zmyte przez deszcz. "
     "Blaszki biale, wolne. Trzon bialy z pierscieniem i bulwiasta podstawa otoczona "
     "pierscieniowatymi lusakami. Zawiera kwas ibotenowy i muscymol - dziala na "
     "osrodkowy uklad nerwowy.",
     "Czerwony kapelusz z bialymi kosmkami; biale blaszki; pierscien i bulwiasta podstawa",
     "TRUJACY. Zatrucia rzadko smiertelne, ale przebieg bywa ciezki.", 0),

    (6, "Koźlarz babka", "Leccinum scabrum", "kozak, babka",
     "Boletaceae", "jadalny", "rurki", 0, 0, 0, 0,
     "poduszkowaty", "gladka", "brazowawy", "przyjemny", "lagodny",
     6, 10,
     "Pospolity grzyb rosnacy w symbiozie z brzozami. Kapelusz 5-15 cm, szarobrazowy "
     "do ciemnobrazowego. Trzon smukly, wysoki, pokryty charakterystycznymi ciemnymi "
     "luseczkami na jasnym tle. Rurki biale, z wiekiem szarawe. Miazsz miekki, "
     "u starszych okazow wodnisty i gabczasty.",
     "Ciemne luseczki na jasnym trzonie; wystepuje pod brzozami",
     "Mlode owocniki najlepsze - starsze robia sie wodniste.", 0),

    (7, "Maslak zwyczajny", "Suillus luteus", "maslak zolty",
     "Suillaceae", "jadalny", "rurki", 1, 0, 0, 0,
     "poduszkowaty", "sluzowata", "zoltobrazowy", "przyjemny", "lagodny",
     6, 11,
     "Grzyb sosnowych borow, latwy do rozpoznania po sliskiej, kleistej skorce kapelusza. "
     "Kapelusz 5-12 cm, kasztanowobrazowy, przy wilgotnej pogodzie wyraznie sluzowaty. "
     "Rurki zolte, drobne. Trzon z wyraznym blonaistym pierscieniem. Skorke kapelusza "
     "przed obrobka zwykle sie sciaga - u czesci osob wywoluje dolegliwosci trawienne.",
     "Sliska, kleista skorka; zolte rurki; pierscien na trzonie; pod sosnami",
     "Zaleca sie usuwanie skorki kapelusza przed przyrzadzeniem.", 0),

    (8, "Kania czubajka", "Macrolepiota procera", "czubajka kania, sowa",
     "Agaricaceae", "jadalny", "blaszki", 1, 0, 0, 0,
     "parasolowaty", "luskowata", "bialy", "przyjemny, orzechowy", "lagodny",
     7, 11,
     "Duzy grzyb o kapeluszu osiagajacym nawet 30 cm srednicy, rosnacy na obrzezach lasow "
     "i lakach. Kapelusz pokryty wyraznymi, odstajacymi brazowymi luskami na jasnym tle. "
     "Blaszki biale, wolne. Trzon wysoki, smukly, pokryty wezykowatym deseniem, "
     "z ruchomym pierscieniem, ktory mozna przesuwac palcem - to cecha diagnostyczna. "
     "Miazsz nie zmienia barwy.",
     "Ruchomy pierscien na trzonie; wezykowaty deseñ trzonu; brak pochwy",
     "Nie mylic z mlodymi muchomorami - kania nie ma pochwy, a pierscien jest ruchomy.", 0),

    (9, "Opienka miodowa", "Armillaria mellea", "opienka",
     "Physalacriaceae", "warunkowo", "blaszki", 1, 0, 0, 0,
     "wypukly do plaskiego", "luskowata", "bialy", "slaby, kwaskowaty", "cierpki na surowo",
     8, 11,
     "Rosnie kepami na pniach, korzeniach i martwym drewnie drzew lisciastych i iglastych. "
     "Kapelusz 3-10 cm, miodowozolty do brazowego, pokryty drobnymi ciemnymi luseczkami "
     "w srodkowej czesci. Blaszki zbiegajace, kremowe, z wiekiem plamiste. Trzon z bialym "
     "pierscieniem. Wymaga obowiazkowej obrobki termicznej - na surowo lub niedogotowana "
     "wywoluje dolegliwosci zoladkowo-jelitowe.",
     "Rosnie kepami na drewnie; drobne luseczki na kapeluszu; bialy pierscien",
     "WARUNKOWO JADALNY - konieczne gotowanie minimum 15-20 minut, wode odlac.", 0),

    (10, "Mleczaj rydz", "Lactarius deliciosus", "rydz",
     "Russulaceae", "jadalny", "blaszki", 0, 0, 1, 0,
     "wklesly, lejkowaty", "gladka", "kremowy", "przyjemny, owocowy", "lagodny",
     8, 11,
     "Grzyb borow sosnowych, rozpoznawalny po intensywnie pomaranczowej barwie i - przede "
     "wszystkim - po marchwiowopomaranczowym mleczku, ktore wyplywa po przecieciu miazszu. "
     "Kapelusz 4-12 cm, z koncentrycznymi ciemniejszymi strefami, brzeg podwiniety. "
     "Blaszki zbiegajace, pomaranczowe. Uszkodzone miejsca z czasem zieleniej - to normalne "
     "i nie swiadczy o zepsuciu.",
     "Pomaranczowe mleczko po przecieciu; zielenienie uszkodzonych miejsc; pod sosnami",
     "Zielone plamy na owocniku sa naturalne i nie dyskwalifikuja grzyba.", 0),
]

# species_id -> [(kolor, czesc), ...]
KOLORY_SP = {
    1: [("brazowy","kapelusz"),("ciemnobrazowy","kapelusz"),("kremowy","trzon"),
        ("bialy","hymenofor"),("oliwkowy","hymenofor"),("bialy","miazsz")],
    2: [("brazowy","kapelusz"),("kremowy","trzon"),("rozowy","hymenofor"),("bialy","miazsz")],
    3: [("zielonkawy","kapelusz"),("oliwkowy","kapelusz"),("bialy","trzon"),
        ("bialy","hymenofor"),("bialy","miazsz")],
    4: [("bialy","kapelusz"),("kremowy","kapelusz"),("bialy","trzon"),
        ("rozowy","hymenofor"),("brazowy","hymenofor"),("bialy","miazsz")],
    5: [("czerwony","kapelusz"),("pomaranczowy","kapelusz"),("bialy","trzon"),
        ("bialy","hymenofor"),("bialy","miazsz")],
    6: [("brazowy","kapelusz"),("szary","kapelusz"),("bialy","trzon"),
        ("bialy","hymenofor"),("bialy","miazsz")],
    7: [("brazowy","kapelusz"),("ciemnobrazowy","kapelusz"),("zolty","trzon"),
        ("zolty","hymenofor"),("zolty","miazsz")],
    8: [("brazowy","kapelusz"),("kremowy","kapelusz"),("brazowy","trzon"),
        ("bialy","hymenofor"),("bialy","miazsz")],
    9: [("zolty","kapelusz"),("brazowy","kapelusz"),("brazowy","trzon"),
        ("kremowy","hymenofor"),("bialy","miazsz")],
    10:[("pomaranczowy","kapelusz"),("pomaranczowy","trzon"),
        ("pomaranczowy","hymenofor"),("pomaranczowy","miazsz")],
}

SIEDL_SP = {
    1: ["las lisciasty","las iglasty","las mieszany","buczyny","debiny","swierczyny"],
    2: ["las iglasty","las mieszany","bory sosnowe"],
    3: ["las lisciasty","las mieszany","buczyny","debiny","parki i zadrzewienia"],
    4: ["laki i pastwiska","parki i zadrzewienia","tereny ruderalne"],
    5: ["las iglasty","las mieszany","brzeziny","bory sosnowe"],
    6: ["brzeziny","las mieszany","las lisciasty","obrzeza lasu"],
    7: ["bory sosnowe","las iglasty","las mieszany"],
    8: ["obrzeza lasu","laki i pastwiska","las lisciasty","parki i zadrzewienia"],
    9: ["drewno martwe","drewno zywych drzew","las lisciasty","las mieszany"],
    10:["bory sosnowe","las iglasty"],
}

# (species_id, similar_id, roznice, waga)
LOOKALIKES = [
    (1, 2, "Goryczak ma ciemna, kontrastowa siateczke na trzonie i rozowawe rurki. "
           "Smak skrajnie gorzki - wystarczy dotknac jezykiem kawalek miazszu.", 2),
    (2, 1, "Borowik ma jasna, delikatna siateczke i rurki biale do oliwkowych. "
           "Smak lagodny, orzechowy.", 2),
    (4, 3, "Muchomor sromotnikowy ma blaszki ZAWSZE biale i workowata pochwe u podstawy trzonu. "
           "Pieczarka ma blaszki rozowe lub brazowe i nie ma pochwy.", 3),
    (3, 4, "Pieczarka ma rozowe lub czekoladowobrazowe blaszki i brak pochwy. "
           "Muchomor sromotnikowy - biale blaszki, pochwa u podstawy.", 3),
    (8, 3, "Kania ma ruchomy pierscien i wezykowaty deseñ na trzonie, brak pochwy. "
           "Mlody muchomor sromotnikowy ma pochwe i stala barwe blaszek.", 3),
    (8, 5, "Kania ma bialy kapelusz z brazowymi luskami i ruchomy pierscien. "
           "Muchomor czerwony - czerwony kapelusz, bulwiasta podstawa.", 2),
    (9, 1, "Opienka rosnie kepami na drewnie, ma blaszki. Borowik rosnie pojedynczo "
           "na ziemi i ma rurki.", 1),
    (6, 1, "Kozlarz ma ciemne luseczki na trzonie zamiast siateczki, miazsz miekszy.", 1),
]

def main():
    if os.path.exists(OUT):
        os.remove(OUT)
    con = sqlite3.connect(OUT)
    con.executescript(SCHEMA)
    cur = con.cursor()

    cur.executemany("INSERT INTO kolory(nazwa,hex) VALUES (?,?)", KOLORY)
    cur.executemany("INSERT INTO siedliska(nazwa) VALUES (?)", [(s,) for s in SIEDLISKA])

    cur.executemany("""
        INSERT INTO species(id,nazwa_pl,nazwa_lac,synonimy_pl,rodzina,jadalnosc,hymenofor,
            pierscien,pochwa,mleczko,sinienie,ksztalt_kapelusza,powierzchnia,wysyp_zarnikow,
            zapach,smak,miesiac_od,miesiac_do,opis,cechy_kluczowe,uwagi,chroniony)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, SPECIES)

    kol_id = dict(cur.execute("SELECT nazwa,id FROM kolory").fetchall())
    sied_id = dict(cur.execute("SELECT nazwa,id FROM siedliska").fetchall())

    for sp, lst in KOLORY_SP.items():
        cur.executemany("INSERT INTO species_kolor(species_id,kolor_id,czesc) VALUES (?,?,?)",
                        [(sp, kol_id[k], c) for k, c in lst])

    for sp, lst in SIEDL_SP.items():
        cur.executemany("INSERT INTO species_siedlisko(species_id,siedlisko_id) VALUES (?,?)",
                        [(sp, sied_id[s]) for s in lst])

    cur.executemany("INSERT INTO lookalikes(species_id,similar_id,roznice,waga) VALUES (?,?,?,?)",
                    LOOKALIKES)

    for sp_id, _, lac, *_ in [(s[0], s[1], s[2]) + tuple(s[3:]) for s in SPECIES]:
        slug = lac.lower().replace(" ", "_")
        cur.execute("INSERT INTO photos(species_id,plik,kolejnosc) VALUES (?,?,0)",
                    (sp_id, f"{slug}_1.webp"))

    cur.executemany("INSERT INTO meta(klucz,wartosc) VALUES (?,?)", [
        ("db_version", "1"),
        ("photos_version", "0"),
        ("photos_manifest_url",
         "https://raw.githubusercontent.com/USER/atlas-grzybow/main/photos/manifest.json"),
    ])

    con.commit()
    n = cur.execute("SELECT COUNT(*) FROM species").fetchone()[0]
    con.execute("VACUUM")
    con.close()
    print(f"OK: {OUT} ({n} gatunkow, {os.path.getsize(OUT)/1024:.0f} KB)")

if __name__ == "__main__":
    main()
