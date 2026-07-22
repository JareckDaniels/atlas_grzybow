# Atlas grzybów

Offline'owy atlas grzybów Polski. Baza w APK, zdjęcia pobierane przy pierwszym uruchomieniu.

## Stan

51 gatunków, 54 powiązania sobowtórów (26 oznaczonych jako potencjalnie
śmiertelne), 7 gatunków śmiertelnie trujących, 32 opisy zastosowania
kulinarnego.

**38 z 51 gatunków zweryfikowane** z dwoma źródłami: atlasem Marka Snowarskiego
(grzyby.pl) i przewodnikiem Markusa Flücka „Jaki to grzyb?". Szczegóły, lista
poprawek i wykaz tego, co pozostaje niezweryfikowane:
[`docs/WERYFIKACJA.md`](docs/WERYFIKACJA.md).
Działa: filtry, klucz oznaczania, słowniczek z rysunkami, karty gatunków,
sobowtóry, pobieranie zdjęć, własna ikona.
Brak: opublikowanej paczki zdjęć (aplikacja działa z placeholderami).

## Build — wyłącznie GitHub Actions

Nie potrzebujesz Fluttera lokalnie. Workflow sam generuje rusztowanie Androida.

1. Utwórz repo `atlas_grzybow` na GitHubie.
2. Wrzuć zawartość tego katalogu (GitHub Desktop → Add Local Repository → Publish).
3. Zakładka **Actions** → build startuje automatycznie po pushu na `main`.
4. Po ~5–8 min: Actions → ostatni run → sekcja **Artifacts** → `atlas-grzybow-apk`.

W paczce jest jeden plik: `atlas-grzybow-1.0.0-arm64.apk`. Budowany tylko
pod arm64-v8a, bo wszystkie telefony od ok. 2017 roku (w tym cała seria
Galaxy S) są 64-bitowe. Daje to mniejszy APK i krótszy build.

Gdybyś kiedyś potrzebował wersji na starsze 32-bitowe urządzenie, zmień
w workflow `--target-platform android-arm64` na `--split-per-abi`.

Tag `v1.0.0` dodatkowo tworzy Release z APK-ami.

### Co robi workflow

Katalog `android/` **nie jest w repo** — jest generowany w CI przez
`flutter create --overwrite`. Dlatego workflow przed tym krokiem chowa
`lib/`, `pubspec.yaml` i `analysis_options.yaml` do `/tmp`, a po wygenerowaniu
przywraca. Potem podnosi `minSdk` do 23 (wymóg sqflite), dopisuje uprawnienie
INTERNET i ustawia nazwę aplikacji w launcherze.

Jeśli kiedyś zechcesz budować lokalnie: usuń `/android/` z `.gitignore`,
odpal `flutter create --org pl.atlas --platforms=android .` raz u siebie
i zacommituj wynik. Wtedy workflow można uprościć.

## Architektura

```
lib/
  models/species.dart        modele + stan filtrów
  data/db.dart               SQLite, dynamiczne budowanie SQL z filtrów
  data/photo_manager.dart    pobieranie/rozpakowywanie paczki zdjęć
  screens/
    setup_screen.dart        disclaimer + pierwsze pobranie zdjęć
    lista_screen.dart        lista z wyszukiwarką
    filtry_screen.dart       filtry z licznikiem na żywo
    klucz_screen.dart        klucz krok po kroku
    detal_screen.dart        karta gatunku + sobowtóry
    slowniczek_screen.dart   objaśnienia pojęć z rysunkami
    zdjecia_screen.dart      zarządzanie paczką zdjęć
  widgets/
    common.dart              karty, badge, zdjęcia
    morfologia.dart          rysunki morfologii (CustomPainter, bez plików)
tools/
  gatunki.py                 DANE — tu dopisujesz gatunki i opisy kulinarne
  build_db.py                generator bazy + walidacja danych
  make_icon.py               generator ikony aplikacji (uruchamiany w CI)
  parse_atlas.py             czytnik atlasu grzyby.pl do weryfikacji danych
  fetch_photos.py            pobieranie z Commons + weryfikacja + pakowanie
photos/
  manifest.json              wskazuje aplikacji, skąd pobrać paczkę zdjęć
```

Baza jest generowana skryptem, nie edytowana ręcznie. Cała treść siedzi
w `tools/gatunki.py` — dodanie gatunku to dopisanie krotki do `SPECIES`
plus wpisy w `KOLORY_SP`, `SIEDL_SP`, ewentualnie `LOOKALIKES`.

`build_db.py` waliduje dane przed zapisem i przerywa build przy niespójności
(nieznany kolor, brak wpisu w KOLORY_SP, złe id w LOOKALIKES, zła jadalność).
Ta walidacja jest częścią CI — błąd w danych zatrzyma budowanie APK.

Osobna reguła dotyczy opisów kulinarnych (`KUCHNIA`): każdy gatunek jadalny
lub warunkowo jadalny musi mieć wpis, żaden trujący nie może go mieć,
a przy gatunkach **warunkowo jadalnych** opis musi wspominać o obróbce
termicznej. Bez tego rubryka „W kuchni" zachęcałaby do zjedzenia na surowo
grzyba, który surowy jest trujący.

## Ikona

`tools/make_icon.py` rysuje ikonę (borowik na zielonym tle) w Pillow
i zapisuje wszystkie gęstości plus wariant adaptacyjny dla Androida 8+.
Uruchamiana automatycznie w CI po `flutter create`. Podgląd: `icon_preview.png`.

Zmiana wyglądu: edytuj `rysuj_grzyb()` — rysunek jest w układzie 100×100
skalowanym do docelowego rozmiaru.

## Model danych

Kolory i siedliska w relacji M:N — grzyb ma kilka barw kapelusza,
więc filtr „brązowy lub rudy" działa jako OR w obrębie grupy, AND między grupami.

`lookalikes` jest kierunkowe: wpis A→B opisuje różnice widziane od strony A.
Dla pary krytycznej warto dodać oba kierunki. Pole `waga=3` oznacza pomyłkę
potencjalnie śmiertelną i wywołuje czerwone ostrzeżenie na karcie.

## Zdjęcia

Paczka ZIP w GitHub Releases, manifest JSON w repo:

```json
{"version": 1, "url": "https://github.com/USER/atlas-grzybow/releases/download/photos-v1/photos.zip",
 "size": 48210332, "count": 412}
```

Aplikacja porównuje `photos_version` w lokalnej bazie z wersją w manifeście.
Podbicie wersji manifestu = aktualizacja zdjęć bez nowego APK.

Adres manifestu wpisany jest w `build_db.py` w tabeli `meta` — podmień `USER`
na swoją nazwę na GitHubie. Do pierwszego buildu nie jest to konieczne:
bez zdjęć aplikacja działa, tylko pokazuje placeholdery.

### Workflow pozyskiwania zdjęć

```bash
pip install requests pillow
python3 tools/fetch_photos.py fetch  --db assets/db/atlas.db --out photos_raw
python3 tools/fetch_photos.py review --out photos_raw   # otwórz review.html
# klikasz OK/Odrzuć, zapisujesz _meta.json, nadpisujesz plik
python3 tools/fetch_photos.py pack   --out photos_raw --version 1 \
    --url https://github.com/USER/atlas-grzybow/releases/download/photos-v1/photos.zip
```

Skrypt filtruje licencje (przepuszcza tylko CC-BY, CC-BY-SA, CC0, PD)
i zapisuje autora oraz źródło do `photos.sql`, który trzeba wkleić do `build_db.py`.

**Weryfikacja jest obowiązkowa.** Commons zawiera błędnie oznaczone zdjęcia —
przy atlasie grzybów to nie jest kosmetyczny problem.

## Rysunki morfologii

`lib/widgets/morfologia.dart` rysuje schematy kodem przez `CustomPainter`
w układzie 100×100, skalowanym do dostępnego miejsca. Zero plików graficznych,
idealna ostrość na każdym ekranie. Dodanie nowego pojęcia: nowa klasa
dziedzicząca po `_Baza` plus wpis w `_pojecia` w `slowniczek_screen.dart`.

## Do zrobienia

- [ ] Uzupełnić `SPECIES` do ~120 gatunków
- [ ] Zbudować i zweryfikować paczkę zdjęć
- [ ] Ulubione (osobna tabela, poza `atlas.db` — przetrwa aktualizację bazy)
- [ ] Tryb ciemny przełączalny
- [ ] Rozszerzyć klucz o pytania dla grzybów bez blaszek i rurek

## Uwaga

Aplikacja edukacyjna. Nie zastępuje oceny grzyboznawcy. Disclaimer przy
pierwszym uruchomieniu jest wymagany do przejścia dalej — nie usuwaj go.
