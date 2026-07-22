#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_icon.py - generuje ikone aplikacji (grzyb) we wszystkich gestosciach.

Uruchamiane automatycznie w CI po 'flutter create'.
Uzycie: python3 tools/make_icon.py android/app/src/main/res
"""

import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

OUT_RES = sys.argv[1] if len(sys.argv) > 1 else "android/app/src/main/res"

# Gestosci Androida: (katalog, rozmiar w px)
GESTOSCI = [
    ("mipmap-mdpi", 48),
    ("mipmap-hdpi", 72),
    ("mipmap-xhdpi", 96),
    ("mipmap-xxhdpi", 144),
    ("mipmap-xxxhdpi", 192),
]

# Paleta spojna z motywem aplikacji.
TLO_1 = (74, 107, 58)      # mech, gora gradientu
TLO_2 = (58, 86, 45)       # ciemniejszy mech, dol
KAPELUSZ_1 = (150, 92, 52) # jasniejszy braz
KAPELUSZ_2 = (108, 63, 34) # ciemniejszy braz
TRZON = (243, 237, 222)    # kremowy
TRZON_CIEN = (214, 203, 181)
RURKI = (226, 210, 170)    # spod kapelusza

# Rysujemy w duzej rozdzielczosci i skalujemy w dol - daje gladkie krawedzie.
SUPER = 1024


def gradient_pionowy(rozmiar, gora, dol):
    """Pionowy gradient jako obraz."""
    g = Image.new("RGB", (1, rozmiar))
    d = ImageDraw.Draw(g)
    for y in range(rozmiar):
        t = y / max(1, rozmiar - 1)
        c = tuple(int(gora[i] + (dol[i] - gora[i]) * t) for i in range(3))
        d.point((0, y), fill=c)
    return g.resize((rozmiar, rozmiar), Image.NEAREST)


def luk_kapelusza(cx, cy, szer, wys, punkty=120):
    """Punkty gornej krawedzi kapelusza - splaszczona polelipsa."""
    pts = []
    for i in range(punkty + 1):
        t = i / punkty
        kat = math.pi * (1 - t)
        x = cx + math.cos(kat) * szer / 2
        # Wykladnik <1 splaszcza luk u gory, dajac ksztalt grzyba, nie kuli.
        y = cy - (math.sin(kat) ** 0.78) * wys
        pts.append((x, y))
    return pts


def rysuj_grzyb(S):
    """Rysuje grzyb na przezroczystym tle o boku S."""
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    k = S / 100.0  # przelicznik z ukladu 100x100

    def p(*v):
        return tuple(x * k for x in v)

    # --- TRZON ---
    # Lekko bulwiasty, wezszy u gory - sylwetka borowika.
    trzon = [
        p(42, 54)[:2], p(39.5, 66)[:2], p(37, 76)[:2],
        p(36.5, 84)[:2], p(39, 89)[:2], p(44, 91)[:2],
        p(56, 91)[:2], p(61, 89)[:2], p(63.5, 84)[:2],
        p(63, 76)[:2], p(60.5, 66)[:2], p(58, 54)[:2],
    ]
    d.polygon(trzon, fill=TRZON)

    # Cien po prawej stronie trzonu - daje wrazenie objetosci.
    cien = [
        p(53.5, 54)[:2], p(56, 66)[:2], p(58, 76)[:2],
        p(58.5, 84)[:2], p(56.5, 90)[:2],
        p(56, 91)[:2], p(61, 89)[:2], p(63.5, 84)[:2],
        p(63, 76)[:2], p(60.5, 66)[:2], p(58, 54)[:2],
    ]
    d.polygon(cien, fill=TRZON_CIEN)

    # --- SPOD KAPELUSZA (rurki) ---
    d.ellipse([p(16, 45)[0], p(16, 45)[1], p(84, 61)[0], p(84, 61)[1]],
              fill=RURKI)

    # --- KAPELUSZ ---
    luk = luk_kapelusza(50 * k, 52 * k, 74 * k, 40 * k)
    dol_kapelusza = [
        (p(87, 52)[0], p(87, 52)[1]),
        (p(79, 56.5)[0], p(79, 56.5)[1]),
        (p(65, 59)[0], p(65, 59)[1]),
        (p(50, 59.5)[0], p(50, 59.5)[1]),
        (p(35, 59)[0], p(35, 59)[1]),
        (p(21, 56.5)[0], p(21, 56.5)[1]),
        (p(13, 52)[0], p(13, 52)[1]),
    ]
    d.polygon(luk + dol_kapelusza, fill=KAPELUSZ_2)

    # Jasniejsza gorna czesc kapelusza - swiatlo pada z gory-lewej.
    luk_jasny = luk_kapelusza(50 * k, 49.5 * k, 68 * k, 36 * k)
    d.polygon(luk_jasny + [(p(84, 49.5)[0], p(84, 49.5)[1]),
                           (p(50, 52)[0], p(50, 52)[1]),
                           (p(16, 49.5)[0], p(16, 49.5)[1])],
              fill=KAPELUSZ_1)

    # Refleks swiatla - male jasne pole u gory po lewej.
    refleks = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    dr = ImageDraw.Draw(refleks)
    dr.ellipse([p(27, 22)[0], p(27, 22)[1], p(47, 33)[0], p(47, 33)[1]],
               fill=(255, 255, 255, 46))
    refleks = refleks.filter(ImageFilter.GaussianBlur(radius=S / 90))
    im.alpha_composite(refleks)

    return im


def ikona(rozmiar, zaokraglona=True, margines=0.06):
    """Pelna ikona: tlo + grzyb."""
    S = SUPER
    tlo = gradient_pionowy(S, TLO_1, TLO_2).convert("RGBA")

    grzyb = rysuj_grzyb(S)
    # Skalujemy grzyb, zeby zostawic margines od krawedzi.
    skala = 1 - 2 * margines
    nowy = int(S * skala)
    grzyb = grzyb.resize((nowy, nowy), Image.LANCZOS)
    poz = (S - nowy) // 2
    tlo.alpha_composite(grzyb, (poz, poz - int(S * 0.01)))

    if zaokraglona:
        maska = Image.new("L", (S, S), 0)
        ImageDraw.Draw(maska).rounded_rectangle(
            [0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=255)
        tlo.putalpha(maska)

    return tlo.resize((rozmiar, rozmiar), Image.LANCZOS)


def ikona_adaptacyjna_pierwszy_plan(rozmiar):
    """
    Warstwa pierwszego planu dla ikon adaptacyjnych Androida.
    Android przycina do 66% srodka, wiec grzyb musi byc mniejszy.
    """
    S = SUPER
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    grzyb = rysuj_grzyb(S)
    skala = 0.68
    nowy = int(S * skala)
    grzyb = grzyb.resize((nowy, nowy), Image.LANCZOS)
    poz = (S - nowy) // 2
    im.alpha_composite(grzyb, (poz, poz))
    return im.resize((rozmiar, rozmiar), Image.LANCZOS)


def main():
    os.makedirs(OUT_RES, exist_ok=True)

    for katalog, rozmiar in GESTOSCI:
        sciezka = os.path.join(OUT_RES, katalog)
        os.makedirs(sciezka, exist_ok=True)

        ikona(rozmiar).save(os.path.join(sciezka, "ic_launcher.png"))
        ikona(rozmiar, zaokraglona=True).save(
            os.path.join(sciezka, "ic_launcher_round.png"))
        ikona_adaptacyjna_pierwszy_plan(rozmiar).save(
            os.path.join(sciezka, "ic_launcher_foreground.png"))

        print(f"  {katalog}: {rozmiar}x{rozmiar}")

    # Tlo ikony adaptacyjnej jako kolor.
    values = os.path.join(OUT_RES, "values")
    os.makedirs(values, exist_ok=True)
    with open(os.path.join(values, "ic_launcher_background.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n'
                '<resources>\n'
                '    <color name="ic_launcher_background">#4A6B3A</color>\n'
                '</resources>\n')

    # Definicja ikony adaptacyjnej (Android 8+).
    for katalog in ("mipmap-anydpi-v26",):
        sciezka = os.path.join(OUT_RES, katalog)
        os.makedirs(sciezka, exist_ok=True)
        xml = ('<?xml version="1.0" encoding="utf-8"?>\n'
               '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
               '    <background android:drawable="@color/ic_launcher_background"/>\n'
               '    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>\n'
               '    <monochrome android:drawable="@mipmap/ic_launcher_foreground"/>\n'
               '</adaptive-icon>\n')
        for nazwa in ("ic_launcher.xml", "ic_launcher_round.xml"):
            with open(os.path.join(sciezka, nazwa), "w") as f:
                f.write(xml)
        print(f"  {katalog}: ikona adaptacyjna")

    # Podglad do repo.
    ikona(512).save("icon_preview.png")
    print("\nPodglad: icon_preview.png")


if __name__ == "__main__":
    main()
