# Atlas grzybów

Offline'owy atlas grzybów Polski. Baza w APK, zdjęcia pobierane przy pierwszym uruchomieniu.

## Stan: faza 1 — szkielet z 10 gatunkami

Działa: filtry, klucz oznaczania, karty gatunków, sobowtóry, pobieranie zdjęć.
Brak: treści (10 z ~120 gatunków), zdjęć (trzeba zbudować paczkę).

## Build — wyłącznie GitHub Actions

Nie potrzebujesz Fluttera lokalnie. Workflow sam generuje rusztowanie Androida.

1. Utwórz repo `atlas_grzybow` na GitHubie.
2. Wrzuć zawartość tego katalogu (GitHub Desktop → Add Local Repository → Publish).
3. Zakładka **Actions** → build startuje automatycznie po pushu na `main`.
4. Po ~5–8 min: Actions → ostatni run → sekcja **Artifacts** → `atlas-grzybow-apk`.

W paczce są cztery pliki. Na telefon bierzesz `app-arm64-v8a-release.apk`
(każdy telefon z ostatnich lat). Jak nie zadziała — `app-release.apk`,
uniwersalny, cięższy, ale zawsze się instaluje.

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
  models/species.dart      modele + stan filtrów
  data/db.dart             SQLite, dynamiczne budowanie SQL z filtrów
  data/photo_manager.dart  pobieranie/rozpakowywanie paczki zdjęć
  screens/                 setup, lista, filtry, klucz, detal
  widgets/common.dart      karty, badge, zdjęcia
tools/
  build_db.py              generator bazy (źródło prawdy dla treści)
  fetch_photos.py          pobieranie z Commons + weryfikacja + pakowanie
```

Baza jest generowana skryptem, nie edytowana ręcznie. Cała treść siedzi
w `tools/build_db.py` — dodanie gatunku to dopisanie krotki do `SPECIES`
plus wpisy w `KOLORY_SP`, `SIEDL_SP`, ewentualnie `LOOKALIKES`.

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

## Do zrobienia w fazie 2/3

- [ ] Uzupełnić `SPECIES` do ~120 gatunków
- [ ] Zbudować i zweryfikować paczkę zdjęć
- [ ] Ulubione (tabela lokalna, poza `atlas.db` — przetrwa aktualizację bazy)
- [ ] Tryb ciemny przełączalny
- [ ] Ikona aplikacji
- [ ] Rozszerzyć klucz o pytania dla grzybów bez blaszek i rurek

## Uwaga

Aplikacja edukacyjna. Nie zastępuje oceny grzyboznawcy. Disclaimer przy
pierwszym uruchomieniu jest wymagany do przejścia dalej — nie usuwaj go.
