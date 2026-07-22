#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_atlas.py - wyciaga tekst z lokalnej kopii atlasu grzyby.pl
(Marek Snowarski, 2000) do weryfikacji danych w gatunki.py.

Zrodlo jest w cp1250, HTML 3.2, bez semantycznych znacznikow -
sekcje rozpoznajemy po naglowkach tekstowych.
"""

import html
import os
import re
import sys

GATUNKI = sys.argv[1] if len(sys.argv) > 1 else "GATUNKI"

# Naglowki sekcji uzywane w atlasie.
SEKCJE = [
    ("cechy", r"cechy makroskopowe|owocnik"),
    ("zarodniki", r"zarodniki"),
    ("wystepowanie", r"wyst[ęe]powanie"),
    ("wartosc", r"warto[śs][ćc]"),
    ("uwagi", r"uwagi"),
    ("fotografie", r"inne fotografie"),
]


def na_tekst(sciezka):
    """HTML -> czysty tekst."""
    raw = open(sciezka, "rb").read().decode("cp1250", errors="replace")
    t = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
    t = re.sub(r"(?i)<br\s*/?>", "\n", t)
    t = re.sub(r"(?i)</(p|tr|td|div|table|h\d)>", "\n", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = t.replace("\xa0", " ")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n[ \t]+", "\n", t)
    t = re.sub(r"\n{2,}", "\n", t)
    return t.strip()


def naglowek(sciezka):
    """Nazwa lacinska i polska z <title>."""
    raw = open(sciezka, "rb").read().decode("cp1250", errors="replace")
    m = re.search(r"(?is)<title>(.*?)</title>", raw)
    if not m:
        return None, None
    tyt = html.unescape(m.group(1)).strip()
    m2 = re.match(r"([A-Z][a-z]+(?:\s+[a-z\-]+)+)\s*\((.*?)\)", tyt)
    if m2:
        return m2.group(1).strip(), m2.group(2).strip()
    return tyt, None


def sekcje(tekst):
    """Dzieli tekst na sekcje wg naglowkow."""
    linie = tekst.split("\n")
    out = {}
    biezaca = "wstep"
    bufor = []

    for ln in linie:
        czysta = ln.strip()
        # Naglowki sa krotkie i czesto z angielskim tlumaczeniem w nawiasie.
        krotka = len(czysta) < 60
        dopasowana = None
        if krotka:
            bez_ang = re.sub(r"\(.*?\)", "", czysta).strip().lower()
            for nazwa, wzor in SEKCJE:
                if re.fullmatch(wzor, bez_ang):
                    dopasowana = nazwa
                    break
        if dopasowana:
            out[biezaca] = "\n".join(bufor).strip()
            biezaca = dopasowana
            bufor = []
        else:
            bufor.append(ln)
    out[biezaca] = "\n".join(bufor).strip()
    return out


def czysc_naglowek(tekst):
    """Usuwa nawigacje i stopke, ktore powtarzaja sie na kazdej stronie."""
    t = re.sub(r"(?s)^.*?Słownik\s*\|", "", tekst)
    t = re.sub(r"(?s)\|\s*Skorowidz.*$", "", t)
    t = re.sub(r"(?s)Copyright ©.*?\]", "", t)
    t = re.sub(r"\[Copyright[^\]]*\]", "", t)
    return t.strip()


def wczytaj(nazwa_pliku):
    p = os.path.join(GATUNKI, nazwa_pliku)
    if not os.path.exists(p):
        return None
    lac, pl = naglowek(p)
    tekst = czysc_naglowek(na_tekst(p))
    s = sekcje(tekst)
    return {
        "plik": nazwa_pliku,
        "lacinska": lac,
        "polska": pl,
        "sekcje": s,
    }


if __name__ == "__main__":
    if len(sys.argv) > 2:
        d = wczytaj(sys.argv[2])
        if not d:
            print("Nie ma takiego pliku")
            sys.exit(1)
        print(f"=== {d['lacinska']} ({d['polska']}) ===")
        for k, v in d["sekcje"].items():
            if not v.strip():
                continue
            print(f"\n--- [{k}] ---")
            print(v[:2500])
    else:
        pliki = sorted(f for f in os.listdir(GATUNKI) if f.endswith(".htm"))
        print(f"{len(pliki)} plikow w {GATUNKI}")
