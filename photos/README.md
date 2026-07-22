# Paczka zdjęć

`manifest.json` jest odpytywany przez aplikację przy pierwszym uruchomieniu.
Dopóki `version` wynosi 0 albo `url` jest pusty, aplikacja pokazuje komunikat
„Zdjęcia w przygotowaniu" i działa dalej z symbolami zastępczymi.

## Zanim zaczniesz

Wikimedia **wymaga** User-Agenta z prawdziwym adresem kontaktowym — bez tego
odrzuca pobieranie błędem 403. Ustaw swój adres:

```powershell
# PowerShell
$env:WIKI_KONTAKT = "twoj@email.pl"
```

```bash
# bash
export WIKI_KONTAKT="twoj@email.pl"
```

Bez tego skrypt użyje adresu domyślnego i część pobrań może się nie powieść.

## 1. Pobieranie

```bash
pip install requests pillow
python3 tools/fetch_photos.py fetch --db assets/db/atlas.db --out photos_raw
```

Trwa **20–40 minut** dla 51 gatunków — skrypt czeka między zapytaniami,
żeby nie obciążać serwerów Wikimedia. Można przerwać (Ctrl+C) i uruchomić
ponownie; pobrane gatunki są pomijane.

Co zobaczysz w trakcie:
- `+ nazwa_1.webp [CC BY-SA 3.0]` — pobrane, w porządku
- `pomijam licencje: GFDL 1.2` — licencja nie pozwala na redystrybucję
- `nie udalo sie pobrac` — trzy próby nieudane, pomijamy

Skrypt odrzuca automatycznie:
- licencje NC (niekomercyjne) i ND (bez utworów zależnych) — nie wolno ich
  rozpowszechniać w APK
- GFDL — wymaga dołączenia pełnego tekstu licencji
- skany rycin ze starych atlasów (Flora Batava, Bresadola, tablice
  z XIX-wiecznych atlasów) — rysunek nie pomaga rozpoznać grzyba w lesie

## 2. Weryfikacja — krok obowiązkowy

```bash
python3 tools/fetch_photos.py review --out photos_raw
```

Otwórz `photos_raw/review.html` w przeglądarce. Zobaczysz miniatury
pogrupowane po gatunkach. Przy każdej: **OK** albo **Odrzuć**.
Kliknięcie w zdjęcie otwiera stronę źródłową na Commons.

**Commons zawiera błędnie oznaczone zdjęcia.** Przy atlasie grzybów
fotografia podpisana złym gatunkiem to nie usterka kosmetyczna — to dokładnie
ten rodzaj błędu, przed którym aplikacja ma chronić. W razie wątpliwości
odrzuć.

Na koniec kliknij **Zapisz decyzje**, pobierz `_meta.json` i **nadpisz nim
plik w `photos_raw/`**.

## 3. Pakowanie

```bash
python3 tools/fetch_photos.py pack --out photos_raw --version 1 \
    --url https://github.com/JareckDaniels/atlas_grzybow/releases/download/photos-v1/photos.zip
```

Powstają trzy pliki:

| plik | co z nim zrobić |
|---|---|
| `photos.zip` | wgraj jako **GitHub Release** z tagiem `photos-v1` |
| `manifest.json` | podmień `photos/manifest.json` w repo |
| `photos.sql` | wklej do `tools/gatunki.py` jako `PHOTOS` |

Po pushu aplikacja wykryje `version: 1` i zaproponuje pobranie.

## Aktualizacja bez nowego APK

Podbij `version` w manifeście, wgraj nowy ZIP jako kolejny Release,
zaktualizuj `photos/manifest.json`. Aplikacja porówna wersje przy następnym
uruchomieniu i dociągnie różnicę. Menu ⋮ → Zdjęcia → „Sprawdź aktualizacje".
