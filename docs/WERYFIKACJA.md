# Weryfikacja danych — status

Źródło: **Marek Snowarski, „Na grzyby! — Atlas Polskich Grzybów"**,
www.grzyby.pl, kopia offline z 2000 r. (337 stron gatunkowych).

## Podsumowanie

| | liczba |
|---|---|
| Gatunków w bazie | 50 |
| Zweryfikowanych z atlasem | 32 |
| Bez pokrycia w atlasie | 18 |
| Poprawek naniesionych | 6 |
| Powiązań sobowtórów dodanych | 9 |

## Naniesione poprawki

**Gołąbek wymiotny (36)** — było „niejadalny", atlas podaje **trujący**. Zmienione.

**Maślak sitarz (10)** — brak oznaczenia sinienia; atlas: „miąższ nieco
błękitniejący", powierzchnia lepka, miąższ gumowaty. Ustawione `sinienie=1`,
powierzchnia poprawiona na śluzowatą, opis przepisany.

**Żagiew siarkowa (40)** — sezon był 5–9, atlas: „głównie w maju i czerwcu
(do lipca)". Poprawione na 5–7. Usunięta też sprzeczność: wcześniejsza uwaga
ostrzegała przed okazami z robinii, podczas gdy atlas wymienia robinię jako
typowe drzewo żywicielskie.

**Borowik ceglastopory (3)** — sezon 6–10 → **5–11** (atlas: od maja
do października/listopada).

**Muchomor sromotnikowy (12)** — sezon 7–11 → **7–10** (atlas: od lipca/sierpnia
do października).

**Krowiak podwinięty (50)** — doprecyzowany mechanizm toksyczności zgodnie
z atlasem: reakcja alergiczna na białko grzyba, narastające uczulenie
przy kolejnych kontaktach.

## Świadome rozbieżności z atlasem

**Gąska zielonka (25)** — atlas: „smaczny i poszukiwany grzyb jadalny".
W bazie zostaje **niejadalny**. Atlas pochodzi z 2000 r.; zatrucia ze skutkiem
śmiertelnym (rabdomioliza) opisano po jego wydaniu, a gatunek został w Polsce
wykreślony z listy dopuszczonych do obrotu. Do opisu dopisana nota
wyjaśniająca, dlaczego starsze przewodniki mówią co innego.

**Muchomor mglejarka (17)** — atlas: „jadalny". W bazie **warunkowo jadalny**,
z ostrzeżeniem o ryzyku pomylenia z młodymi muchomorami śmiertelnie trującymi.
Brak pierścienia przy obecnej pochwie czyni ten gatunek złym wyborem
dla niedoświadczonego zbieracza.

**Muchomor czerwieniejący (16)** — atlas: „jadalny, oczywiście nie na surowo".
W bazie **warunkowo jadalny** — to ta sama informacja, tylko wyrażona
kategorią z aplikacji.

## Potwierdzone bez zmian

Cechy morfologiczne (pierścień, pochwa, mleczko, sinienie) zweryfikowane
automatycznie dla 32 gatunków — poza maślakiem sitarzem wszystkie zgodne.

Dwa alarmy okazały się fałszywe i zasługują na odnotowanie:
- **Boczniak** — „stalowobłękitny" w atlasie opisuje barwę kapelusza,
  nie sinienie miąższu.
- **Muchomor czerwieniejący** — atlas wspomina o „wałeczkach — resztkach
  pochwy" na bulwiastej podstawie. To struktura szczątkowa, nie pełna pochwa;
  `pochwa=0` jest poprawne i istotne, bo właśnie to odróżnia go
  od muchomora sromotnikowego.

Strona rodzajowa *Agaricus* potwierdza dane dla pieczarek (18, 19, 20):
blaszki różowe → czekoladowobrązowe, podstawa trzonu bez pochwy, wysyp
ciemnobrązowy, a gatunki lekko trujące pachną karbolem i żółkną po uszkodzeniu.

## Dodane powiązania sobowtórów

Na podstawie sekcji „Uwagi" w atlasie:

- maślak ziarnisty ↔ maślak zwyczajny (pierścień)
- muchomor sromotnikowy ↔ gąska zielonka (waga 3)
- muchomor sromotnikowy → czubajka kania (waga 3)
- czubajka kania → muchomor plamisty (waga 3)
- czubajka gwiaździsta → kania
- pieprznik ↔ kolczak obłączasty

Ostatnia para jest ciekawa: atlas nazywa kolczaka „równie jeśli nie bardziej
łudząco podobnym" do kurki niż lisówka. Oba są jadalne, więc waga 1.

## Nadal niezweryfikowane (18 gatunków)

Atlas z 2000 r. ich nie zawiera:

4 borowik szatański · 8 koźlarz czerwony · 9 maślak zwyczajny ·
13 muchomor jadowity · 15 muchomor plamisty · 18 pieczarka polna ·
19 pieczarka leśna · 20 pieczarka żółtawa · 26 gąska szara ·
32 mleczaj rydz · 35 gołąbek zielonawy · 37 smardz jadalny ·
38 piestrzenica kasztanowata · 43 uszak bzowy · 45 zasłonak rudy ·
46 hełmówka obrzeżona · 47 lejkówka jadowita · 48 podgrzybek pasożytniczy

Wśród nich są cztery gatunki oznaczone jako śmiertelnie trujące
(13, 45, 46, 47) i kilka bardzo popularnych zbieranych (9, 18, 32).
**To są miejsca, gdzie weryfikacja jest najbardziej potrzebna.**

## Jak weryfikować dalej

`tools/parse_atlas.py` czyta strony atlasu i dzieli je na sekcje:

```bash
python3 tools/parse_atlas.py "sciezka/do/GATUNKI" Boletus_edulis.htm
```

Przy dokładaniu gatunków warto sprawdzić, czy atlas ma odpowiednią stronę —
nazwy plików odpowiadają nazwom łacińskim z 2000 r., więc dla gatunków
przeklasyfikowanych trzeba szukać pod starą nazwą (np. podgrzybek brunatny
to `Xerocomus_badius.htm`, nie `Imleria_badia.htm`).

---

# Runda 2 — Markus Flück, „Jaki to grzyb?"

Źródło: **Markus Flück, „Jaki to grzyb? — oznaczanie, zbiór, użytkowanie"**,
ponad 300 gatunków Europy Środkowej. Skan 228 stron, bez warstwy tekstowej —
odczytany przez OCR (Tesseract, 185 stron opisowych).

Książka ma układ idealnie dopasowany do struktury bazy: Kapelusz / Blaszki
lub Rurki / Trzon / Miąższ / Zarodniki / **Wartość** / Występowanie / **Uwagi**,
przy czym sekcja „Uwagi" systematycznie omawia sobowtóry.

## Ograniczenie techniczne

W środowisku dostępne były wyłącznie angielskie dane językowe Tesseracta,
więc polskie znaki diakrytyczne wychodzą przekręcone (ł→t, ą→q, ś→s).
Tekst pozostaje czytelny, ale **każdy przepisany fragment wymagał ręcznej
korekty** — nie da się tego zautomatyzować bez `tesseract-ocr-pol`.

Druga książka, **Ewald Gerhardt, „Grzyby — wielki ilustrowany przewodnik"**
(726 stron), okazała się nie do wykorzystania: mimo przetworzenia przez
ABBYY FineReader nie ma dostępnej warstwy tekstowej, a OCR zwraca pustkę
nawet przy 300 DPI.

## Poprawki

**Piestrzenica kasztanowata (38)** — było „trujący", Flück podaje: *„Grzyb
bardzo trujący, surowy śmiertelnie trujący"*. Zmienione na **śmiertelny**.
Dopisana informacja, że nawet obgotowane lub suszone owocniki wywoływały
poważne zatrucia. Walidator automatycznie usunął opis kulinarny przy zmianie
kategorii — mechanizm zadziałał zgodnie z projektem.

Doprecyzowana też różnica wobec smardza: piestrzenica ma miąższ z **nieregularnymi
pustymi przestrzeniami**, smardz — jedną pustą komorę. Wcześniejszy opis
mówił, że wnętrze piestrzenicy „nie jest puste", co było mylące.

**Zasłonak rudy (45)** — Flück rozróżnia dwa gatunki, których wcześniej
nie rozdzielałem. Opisywany przeze mnie *Cortinarius rubellus* to **zasłonak
szpiczasty** (syn. *C. speciosissimus*); osobnym gatunkiem jest *C. orellanus*.
Oba zawierają orellaninę. Dopisany synonim, poprawiony sezon (7–9),
powierzchnia kapelusza (łuskowata, nie włókienkowa) i nota o pokrewnym gatunku.

**Hełmówka obrzeżona (46)** — dodana **cecha rozstrzygająca**, której wcześniej
nie miałem: trzon pod pierścieniem jest gładki i włóknisty, **bez łuseczek**,
a grzyb rośnie głównie na drewnie **iglastym**. To jedyna pewna różnica wobec
jadalnego łuszczaka zmiennego.

**Mleczaj rydz (32)** — dodane **pomarańczowe, płytkie jamki na trzonie**,
dobra cecha rozpoznawcza. Mleczko doprecyzowane: marchwiowoczerwone,
później szarozielone.

**Pieczarka polna (18)** — sezon poprawiony na 5–10 (Flück opisuje dwie fale:
maj–czerwiec, potem sierpień–październik). Wysyp poprawiony na purpurowobrązowy.
Dopisane ostrzeżenie, że gatunek **kumuluje ołów** — nie zbierać z łąk
nawożonych osadami ściekowymi ani z poboczy dróg.

## Nowy gatunek

**Łuszczak zmienny (51)** — *Kuehneromyces mutabilis*, jadalny. Dodany, bo jest
sobowtórem hełmówki obrzeżonej, a jego brak zostawiał lukę w najgroźniejszej
parze na drewnie. Flück zaleca go wyłącznie doświadczonym grzybiarzom.
Dodane trzy powiązania, w tym para łuszczak ↔ hełmówka o wadze 3.

## Potwierdzone bez zmian

- **Pieczarka żółtawa (20)** — żółknięcie podstawy trzonu, zapach fenolu
  nasilający się podczas gotowania, trujący. Zgodne co do szczegółu.
- **Muchomor plamisty (15)** — pierścień nieprążkowany i nisko osadzony,
  pierścieniowate paski nad bulwiastą podstawą, białe blaszki.
- **Pieczarka leśna (19)** — jadalna, smaczna.
- **Smardz jadalny (37)** — jadalny, bardzo smaczny.

## Stan po dwóch rundach

| | |
|---|---|
| Gatunków w bazie | **51** |
| Zweryfikowanych | **38** (32 Snowarski + 6 Flück) |
| Niezweryfikowanych | **13** |
| Powiązań sobowtórów | **54** |

Nadal bez weryfikacji: 4 borowik szatański · 8 koźlarz czerwony ·
9 maślak zwyczajny · 13 muchomor jadowity · 26 gąska szara ·
35 gołąbek zielonawy · 43 uszak bzowy · 47 lejkówka jadowita ·
48 podgrzybek pasożytniczy (oraz kilka potwierdzonych tylko częściowo).

Wśród nich pozostają dwa gatunki śmiertelnie trujące: **muchomor jadowity (13)**
i **lejkówka jadowita (47)**. Obu nie udało się zlokalizować w żadnym z dwóch
źródeł — to priorytet przy kolejnej weryfikacji.

## Uwaga metodyczna

Skorowidz Flücka okazał się bezużyteczny — OCR gubił numery stron w gęstym
dwukolumnowym składzie. Skuteczne było dopiero zOCR-owanie wszystkich 185 stron
opisowych i przeszukiwanie pełnej treści. Zindeksowane pliki tekstowe
nie weszły do repo (ok. 2 MB, jakość OCR wymaga korekty), ale procedurę
da się odtworzyć: `pdftoppm -r 170` na stronę, potem `tesseract --psm 3`.
