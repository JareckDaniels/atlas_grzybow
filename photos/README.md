# Paczka zdjęć

`manifest.json` jest odpytywany przez aplikację przy pierwszym uruchomieniu.

Dopóki `version` wynosi 0 albo `url` jest pusty, aplikacja pokazuje komunikat,
że zdjęcia nie są jeszcze dostępne, i działa dalej z placeholderami.

## Publikacja paczki

```bash
pip install requests pillow
python3 tools/fetch_photos.py fetch  --db assets/db/atlas.db --out photos_raw
python3 tools/fetch_photos.py review --out photos_raw
# otwórz photos_raw/review.html, zatwierdź zdjęcia, zapisz _meta.json
python3 tools/fetch_photos.py pack   --out photos_raw --version 1 \
    --url https://github.com/JareckDaniels/atlas_grzybow/releases/download/photos-v1/photos.zip
```

Następnie:
1. Utwórz Release z tagiem `photos-v1` i dołącz do niego `photos.zip`.
2. Podmień `photos/manifest.json` na wygenerowany plik.
3. Wklej zawartość `photos.sql` do `tools/gatunki.py` jako `PHOTOS` (patrz README główny).

Aktualizacja zdjęć bez nowego APK: podbij `version`, wgraj nowy ZIP jako
kolejny Release, zaktualizuj manifest.
