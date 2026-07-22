#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sql_do_gatunkow.py - przerabia photos.sql (z fetch_photos.py pack)
na blok PHOTOS do wklejenia w gatunki.py.

Uzycie: python3 tools/sql_do_gatunkow.py photos.sql > blok.txt
"""

import re
import sys

PLIK = sys.argv[1] if len(sys.argv) > 1 else "photos.sql"

# Commons wstawia w pole autora cale zdania z Mushroom Observer.
# Wyciagamy z nich samo nazwisko/nick.
WZORCE_MO = [
    r"This image was created by user (.+?) at Mushroom Observer.*",
    r"^(.+?)\.jpg:\s*(.+?)\s*derivative work.*",
    r"^(.+?):\s*(.+?)\s*derivative work.*",
]


def czysc_autora(a: str) -> str:
    """Skraca rozwlekle pola autora do czytelnej nazwy."""
    if not a:
        return "nieznany"
    a = a.replace("\n", " ").strip()

    # "This image was created by user NICK (login) at Mushroom Observer..."
    m = re.match(WZORCE_MO[0], a, re.S)
    if m:
        nick = m.group(1).strip()
        # "Copyright ©2011 Byrain" -> "Byrain"
        nick = re.sub(r"^Copyright\s*©?\s*\d*\s*", "", nick).strip()
        # "Alan Rockefeller (Alan Rockefeller)" -> "Alan Rockefeller"
        nick = re.sub(r"\s*\((.+?)\)$", "", nick).strip()
        return nick or "nieznany"

    # "plik.jpg: Autor derivative work: Ktos" -> bierzemy pierwszego
    m = re.match(r"^\S+\.(?:jpg|png|jpeg|JPG|PNG):\s*(.+?)\s*derivative work", a, re.S | re.I)
    if m:
        return m.group(1).strip()

    m = re.match(r"^source file:\s*(.+?)\s*derivative work", a, re.S | re.I)
    if m:
        return m.group(1).strip()

    # Placeholder z niepodstawionym szablonem
    if "{{{" in a:
        return "nieznany"

    # Dlugie opisy instytucji - bierzemy pierwszy czlon przed srednikiem
    if len(a) > 60 and ";" in a:
        a = a.split(";")[0].strip()

    return a[:70].strip() or "nieznany"


def main():
    tresc = open(PLIK, encoding="utf-8").read()

    # Rekordy moga byc wielolinijkowe (autor z \n)
    wzor = re.compile(
        r"INSERT INTO photos\([^)]*\)\s*VALUES\s*\(\s*"
        r"(\d+)\s*,\s*'((?:[^']|'')*)'\s*,\s*'((?:[^']|'')*)'\s*,\s*"
        r"'((?:[^']|'')*)'\s*,\s*'((?:[^']|'')*)'\s*,\s*(\d+)\s*\)",
        re.S,
    )

    rekordy = []
    for m in wzor.finditer(tresc):
        sid = int(m.group(1))
        plik = m.group(2).replace("''", "'")
        autor = czysc_autora(m.group(3).replace("''", "'"))
        lic = m.group(4).replace("''", "'")
        url = m.group(5).replace("''", "'")
        rekordy.append((sid, plik, autor, lic, url))

    print(f"# Wczytano {len(rekordy)} rekordow", file=sys.stderr)

    # Grupujemy po gatunku, zachowujac kolejnosc
    wg_gat = {}
    for sid, plik, autor, lic, url in rekordy:
        wg_gat.setdefault(sid, []).append((plik, autor, lic, url))

    print("PHOTOS = {")
    for sid in sorted(wg_gat):
        print(f"    {sid}: [")
        for plik, autor, lic, url in wg_gat[sid]:
            a = autor.replace('"', '\\"')
            print(f'        ("{plik}",')
            print(f'         "{a}",')
            print(f'         "{lic}",')
            print(f'         "{url}"),')
        print("    ],")
    print("}")

    print(f"# {len(wg_gat)} gatunkow ze zdjeciami", file=sys.stderr)


if __name__ == "__main__":
    main()
