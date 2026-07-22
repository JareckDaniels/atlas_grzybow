#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gatunki.py - dane gatunkow dla atlasu.

Format krotki SPECIES:
(id, nazwa_pl, nazwa_lac, synonimy, rodzina, jadalnosc, hymenofor,
 pierscien, pochwa, mleczko, sinienie, ksztalt, powierzchnia, wysyp,
 zapach, smak, mies_od, mies_do, opis, cechy_kluczowe, uwagi, chroniony)

jadalnosc: jadalny | warunkowo | niejadalny | trujacy | smiertelny
hymenofor: blaszki | rurki | kolce | gladki | fadki | brak

UWAGA: kazdy wpis w rubryce "jadalnosc" i kazdy tekst w LOOKALIKES
wymaga weryfikacji z atlasem papierowym przed publikacja APK.
"""

SPECIES = [
    # ---------------- BOROWIKOWATE (rurki) ----------------
    (1, "Borowik szlachetny", "Boletus edulis", "prawdziwek, grzyb prawdziwy",
     "Boletaceae", "jadalny", "rurki", 0, 0, 0, 0,
     "poduszkowaty", "gladka", "oliwkowobrązowy", "przyjemny, grzybowy",
     "łagodny, orzechowy", 6, 11,
     "Najbardziej ceniony grzyb jadalny w Polsce. Kapelusz osiąga 8–25 cm średnicy, "
     "początkowo półkulisty, później poduszkowaty, o barwie od jasnobeżowej po "
     "ciemnobrązową. Trzon bulwiasty, jasny, pokryty białawą siateczką w górnej "
     "części. Rurki białe, z wiekiem żółtawe do oliwkowozielonych, nie sinieją "
     "po uszkodzeniu. Miąższ biały, niezmienny na przekroju.",
     "Biała siateczka na trzonie; miąższ nie sinieje; rurki białe do oliwkowych",
     "Nie mylić z goryczakiem żółciowym — ten ma ciemną siateczkę i skrajnie "
     "gorzki smak.", 0),

    (2, "Goryczak żółciowy", "Tylopilus felleus", "szatan fałszywy",
     "Boletaceae", "niejadalny", "rurki", 0, 0, 0, 0,
     "poduszkowaty", "gladka", "różowawy", "słaby", "skrajnie gorzki", 6, 10,
     "Grzyb bardzo podobny do borowika szlachetnego, przez co często trafia "
     "do koszyka początkujących zbieraczy. Kapelusz 5–15 cm, brązowy. Kluczowa "
     "różnica: siateczka na trzonie jest ciemna, wyraźna i kontrastowa, a rurki "
     "z wiekiem przybierają odcień różowy zamiast oliwkowego. Miąższ gorzki "
     "jak żółć — jeden owocnik potrafi zepsuć całą potrawę.",
     "Ciemna siateczka na trzonie; różowawe rurki; smak skrajnie gorzki",
     "Nie jest trujący, ale gorycz nie znika po obróbce termicznej.", 0),

    (3, "Borowik ceglastopory", "Neoboletus luridiformis", "krasnoborowik ceglastopory",
     "Boletaceae", "warunkowo", "rurki", 0, 0, 0, 1,
     "poduszkowaty", "aksamitna", "oliwkowobrązowy", "przyjemny", "łagodny", 5, 11,
     "Masywny borowik o ciemnobrązowym, aksamitnym kapeluszu i pomarańczowo"
     "czerwonych porach. Trzon żółty, gęsto pokryty czerwonymi kropkami. "
     "Miąższ intensywnie i natychmiast sinieje po przekrojeniu — reakcja jest "
     "gwałtowna i całkowicie normalna dla tego gatunku.",
     "Czerwone pory; żółty trzon z czerwonymi kropkami; miąższ silnie sinieje",
     "WARUNKOWO JADALNY — wymaga gotowania. Na surowo trujący. Nie mylić "
     "z borowikiem szatańskim, który ma jasny, białawy kapelusz.", 0),

    (4, "Borowik szatański", "Rubroboletus satanas", "szatan",
     "Boletaceae", "trujacy", "rurki", 0, 0, 0, 1,
     "poduszkowaty", "gladka", "oliwkowy", "nieprzyjemny, u starszych odrażający",
     "łagodny", 6, 9,
     "Rzadki grzyb ciepłych lasów liściastych na podłożu wapiennym. Kapelusz "
     "8–25 cm, charakterystycznie jasny — białawy, szarawy lub bladokremowy. "
     "Pory czerwone do pomarańczowych, trzon gruby, bulwiasty, z czerwoną "
     "siateczką. Miąższ słabo sinieje. Starsze owocniki wydzielają wyraźnie "
     "nieprzyjemny zapach.",
     "Jasny, białawy kapelusz; czerwone pory; czerwona siateczka na trzonie",
     "TRUJĄCY — wywołuje silne dolegliwości żołądkowo-jelitowe. Kluczowa "
     "różnica wobec borowika ceglastoporego to jasna barwa kapelusza.", 0),

    (5, "Podgrzybek brunatny", "Imleria badia", "podgrzybek",
     "Boletaceae", "jadalny", "rurki", 0, 0, 0, 1,
     "poduszkowaty", "gladka", "oliwkowobrązowy", "przyjemny", "łagodny", 6, 11,
     "Bardzo pospolity grzyb jadalny, częsty w borach sosnowych. Kapelusz 4–15 cm, "
     "kasztanowobrązowy, przy wilgotnej pogodzie lekko lepki. Pory żółtawe "
     "do oliwkowych, po naciśnięciu wyraźnie niebieszczeją — to normalna "
     "i pomocna cecha rozpoznawcza. Trzon jaśniejszy, bez siateczki.",
     "Pory sinieją po naciśnięciu; brak siateczki na trzonie; kasztanowy kapelusz",
     "Sinienie porów jest naturalne i nie oznacza, że grzyb jest zepsuty.", 0),

    (6, "Podgrzybek zajączek", "Xerocomus subtomentosus", "zajączek",
     "Boletaceae", "jadalny", "rurki", 0, 0, 0, 1,
     "poduszkowaty", "aksamitna", "oliwkowy", "przyjemny", "łagodny", 6, 10,
     "Kapelusz 4–10 cm, oliwkowobrązowy, wyraźnie aksamitny w dotyku, u starszych "
     "owocników często spękany na drobne pola. Pory jasnożółte, duże, słabo "
     "sinieją. Trzon jaśniejszy, podłużnie żeberkowany.",
     "Aksamitny, spękany kapelusz; duże żółte pory; słabe sinienie",
     "Grzyb dobry, choć u starszych okazów miąższ bywa wodnisty.", 0),

    (7, "Koźlarz babka", "Leccinum scabrum", "kozak, babka",
     "Boletaceae", "jadalny", "rurki", 0, 0, 0, 0,
     "poduszkowaty", "gladka", "brązowawy", "przyjemny", "łagodny", 6, 10,
     "Pospolity grzyb rosnący w symbiozie z brzozami. Kapelusz 5–15 cm, "
     "szarobrązowy do ciemnobrązowego. Trzon smukły, wysoki, pokryty "
     "charakterystycznymi ciemnymi łuseczkami na jasnym tle. Rurki białe, "
     "z wiekiem szarawe. Miąższ miękki, u starszych okazów wodnisty.",
     "Ciemne łuseczki na jasnym trzonie; występuje pod brzozami",
     "Młode owocniki najlepsze — starsze robią się wodniste.", 0),

    (8, "Koźlarz czerwony", "Leccinum aurantiacum", "osiniak",
     "Boletaceae", "jadalny", "rurki", 0, 0, 0, 1,
     "poduszkowaty", "gladka", "brązowawy", "przyjemny", "łagodny", 6, 10,
     "Efektowny grzyb o ceglastopomarańczowym kapeluszu 5–20 cm i mocnym trzonie "
     "z ciemnymi łuseczkami. Rośnie pod osikami i topolami. Miąższ po przekrojeniu "
     "szybko ciemnieje przez odcienie wina do niemal czarnego — to naturalna "
     "reakcja, przez którą potrawa ciemnieje.",
     "Pomarańczowoceglasty kapelusz; ciemne łuseczki na trzonie; miąższ czernieje",
     "Ciemnienie miąższu jest normalne i nie dyskwalifikuje grzyba.", 0),

    (9, "Maślak zwyczajny", "Suillus luteus", "maślak żółty",
     "Suillaceae", "jadalny", "rurki", 1, 0, 0, 0,
     "poduszkowaty", "sluzowata", "żółtobrązowy", "przyjemny", "łagodny", 6, 11,
     "Grzyb sosnowych borów, łatwy do rozpoznania po śliskiej, kleistej skórce "
     "kapelusza. Kapelusz 5–12 cm, kasztanowobrązowy, przy wilgotnej pogodzie "
     "wyraźnie śluzowaty. Rurki żółte, drobne. Trzon z wyraźnym błoniastym "
     "pierścieniem.",
     "Śliska, kleista skórka; żółte rurki; pierścień na trzonie; pod sosnami",
     "Zaleca się usuwanie skórki kapelusza — u części osób wywołuje "
     "dolegliwości trawienne.", 0),

    (10, "Maślak sitarz", "Suillus bovinus", "sitarz",
     "Suillaceae", "jadalny", "rurki", 0, 0, 0, 1,
     "plaski", "sluzowata", "oliwkowobrązowy", "słaby", "łagodny", 7, 11,
     "Kapelusz 3–12 cm, płowy, pomarańczowobrązowy do bladocielistego, "
     "lepki i błyszczący po wyschnięciu; brzeg początkowo podwinięty, "
     "u starszych owocników falisto powyginany. Pory duże, nieregularne, "
     "kanciaste, żółtawe, z wiekiem zielonkawe — wyraźnie szersze niż "
     "u maślaka zwyczajnego. Trzon krótki, bez pierścienia. Miąższ bardzo "
     "elastyczny, gumowaty, lekko błękitniejący po przekrojeniu.",
     "Duże, kanciaste pory; brak pierścienia; gumowaty, elastyczny miąższ",
     "Grzyb średniej jakości — gumowaty miąższ zniechęca, często też "
     "bywa robaczywy.", 0),

    (11, "Maślak ziarnisty", "Suillus granulatus", "maślak bez pierścienia",
     "Suillaceae", "jadalny", "rurki", 0, 0, 0, 0,
     "poduszkowaty", "sluzowata", "żółtawy", "przyjemny", "łagodny", 6, 11,
     "Podobny do maślaka zwyczajnego, ale bez pierścienia na trzonie. "
     "Charakterystyczna cecha: u młodych owocników z porów wydzielają się "
     "mleczne kropelki, a górna część trzonu pokryta jest drobnymi ziarenkami.",
     "Brak pierścienia; mleczne kropelki na porach; ziarenka na trzonie",
     None, 0),

    # ---------------- MUCHOMORY (blaszki, pochwa) ----------------
    (12, "Muchomor sromotnikowy", "Amanita phalloides", "zielona śmierć",
     "Amanitaceae", "smiertelny", "blaszki", 1, 1, 0, 0,
     "dzwonkowaty do płaskiego", "gladka", "biały",
     "mdły, z wiekiem nieprzyjemny", "łagodny", 7, 10,
     "Najbardziej trujący grzyb Europy, odpowiadający za większość śmiertelnych "
     "zatruć. Kapelusz 5–15 cm, oliwkowozielony do żółtawozielonego, z wrośniętymi "
     "promienistymi włóknami. Blaszki zawsze białe, wolne. Trzon z błoniastym "
     "pierścieniem i workowatą pochwą u podstawy, często ukrytą w ściółce. "
     "Objawy zatrucia pojawiają się dopiero po 6–24 godzinach, gdy uszkodzenie "
     "wątroby już trwa.",
     "Białe blaszki + pierścień + workowata pochwa u podstawy trzonu",
     "ŚMIERTELNIE TRUJĄCY. Zawsze wykopuj grzyb w całości, aby zobaczyć podstawę "
     "trzonu. Jeden owocnik może zabić dorosłego człowieka. Trucizna nie "
     "rozkłada się podczas gotowania ani suszenia.", 0),

    (13, "Muchomor jadowity", "Amanita virosa", "biała śmierć",
     "Amanitaceae", "smiertelny", "blaszki", 1, 1, 0, 0,
     "stozkowaty", "gladka", "biały", "nieprzyjemny, mdlący", "łagodny", 7, 10,
     "W całości śnieżnobiały grzyb o stożkowatym kapeluszu 5–10 cm. Trzon "
     "kosmato-łuskowaty, z postrzępionym pierścieniem i workowatą pochwą. "
     "Zawiera te same amatoksyny co muchomor sromotnikowy. Rośnie w wilgotnych "
     "lasach iglastych i mieszanych.",
     "Cały biały; stożkowaty kapelusz; kosmaty trzon; pochwa u podstawy",
     "ŚMIERTELNIE TRUJĄCY. Bywa mylony z pieczarką i czubajką — zawsze "
     "sprawdzaj barwę blaszek i obecność pochwy.", 0),

    (14, "Muchomor czerwony", "Amanita muscaria", "musznik",
     "Amanitaceae", "trujacy", "blaszki", 1, 1, 0, 0,
     "polkulisty do płaskiego", "gladka", "biały", "słaby", "łagodny", 7, 11,
     "Najbardziej rozpoznawalny grzyb świata. Kapelusz 8–20 cm, jaskrawoczerwony, "
     "pokryty białymi kosmkami — pozostałościami osłony, które mogą zostać zmyte "
     "przez deszcz. Blaszki białe, wolne. Trzon biały z pierścieniem i bulwiastą "
     "podstawą otoczoną pierścieniowatymi łuskami. Zawiera kwas ibotenowy "
     "i muscymol, działające na ośrodkowy układ nerwowy.",
     "Czerwony kapelusz z białymi kosmkami; białe blaszki; pierścień i bulwiasta podstawa",
     "TRUJĄCY. Zatrucia rzadko śmiertelne, ale przebieg bywa ciężki. "
     "Po deszczu białe kosmki mogą zniknąć, przez co grzyb bywa mylony "
     "z czubajką cynamonową.", 0),

    (15, "Muchomor plamisty", "Amanita pantherina", "muchomor panterowy",
     "Amanitaceae", "trujacy", "blaszki", 1, 1, 0, 0,
     "plaski", "gladka", "biały", "słaby, rzodkiewkowy", "łagodny", 7, 10,
     "Kapelusz 5–12 cm, brązowy do oliwkowobrązowego, pokryty drobnymi białymi "
     "brodawkami ułożonymi koncentrycznie. Blaszki białe. Trzon z gładkim "
     "pierścieniem i wyraźnie obrzeżoną, bulwiastą podstawą z charakterystycznym "
     "kołnierzykiem. Silnie trujący, bardziej niż muchomor czerwony.",
     "Brązowy kapelusz z białymi brodawkami; kołnierzyk nad bulwą; białe blaszki",
     "TRUJĄCY — silniej niż muchomor czerwony. Mylony z muchomorem "
     "czerwonawym, który ma czerwieniejący miąższ i pierścień z żeberkami.", 0),

    (16, "Muchomor czerwieniejący", "Amanita rubescens", "czerwieniak",
     "Amanitaceae", "warunkowo", "blaszki", 1, 0, 0, 0,
     "polkulisty do płaskiego", "gladka", "biały", "słaby", "łagodny", 6, 11,
     "Kapelusz 5–15 cm, brudnoróżowy do czerwonobrązowego, pokryty szarawymi "
     "kosmkami. Cecha rozstrzygająca: miąższ w miejscach uszkodzonych "
     "i wygryzionych przez ślimaki wyraźnie czerwienieje. Pierścień z góry "
     "wyraźnie żeberkowany. Podstawa trzonu bulwiasta, bez pochwy.",
     "Miąższ czerwienieje po uszkodzeniu; żeberkowany pierścień; brak pochwy",
     "WARUNKOWO JADALNY — wyłącznie po dokładnym ugotowaniu. Na surowo "
     "trujący. Ze względu na łatwość pomylenia z muchomorem plamistym "
     "odradzany początkującym.", 0),

    (17, "Muchomor mglejarka", "Amanita vaginata", "mglejarka",
     "Amanitaceae", "warunkowo", "blaszki", 0, 1, 0, 0,
     "dzwonkowaty", "gladka", "biały", "słaby", "łagodny", 6, 10,
     "Smukły grzyb o szarym kapeluszu 4–10 cm z wyraźnie żeberkowanym brzegiem. "
     "Nie ma pierścienia, ale ma wyraźną, workowatą białą pochwę. Trzon kruchy, "
     "pusty w środku.",
     "Brak pierścienia, ale jest pochwa; żeberkowany brzeg kapelusza",
     "WARUNKOWO JADALNY, ale odradzany — brak pierścienia utrudnia odróżnienie "
     "od młodych muchomorów śmiertelnie trujących.", 0),

    # ---------------- PIECZARKI I CZUBAJKI ----------------
    (18, "Pieczarka polna", "Agaricus campestris", "pieczarka łąkowa",
     "Agaricaceae", "jadalny", "blaszki", 1, 0, 0, 0,
     "polkulisty do płaskiego", "gladka", "purpurowobrązowy",
     "przyjemny, pieczarkowy", "łagodny", 5, 10,
     "Popularny grzyb łąk i pastwisk, blisko spokrewniony z pieczarką hodowlaną. "
     "Kapelusz 4–10 cm, biały do kremowego. Blaszki — cecha rozstrzygająca — "
     "są u młodych owocników różowe, a z wiekiem ciemnieją do "
     "czekoladowobrązowych. Trzon z delikatnym, często zanikającym pierścieniem, "
     "bez pochwy.",
     "Różowe, potem brązowe blaszki; brak pochwy; rośnie na otwartych terenach",
     "Różowe blaszki to najważniejsza różnica wobec białych muchomorów. "
     "Owocniki pojawiają się dwiema falami: w maju i czerwcu, a potem "
     "od sierpnia do października. Gatunek kumuluje ołów — nie zbierać "
     "z łąk nawożonych osadami ściekowymi ani z poboczy ruchliwych dróg.", 0),

    (19, "Pieczarka leśna", "Agaricus silvaticus", "pieczarka czerwieniejąca",
     "Agaricaceae", "jadalny", "blaszki", 1, 0, 0, 0,
     "dzwonkowaty do płaskiego", "luskowata", "ciemnobrązowy",
     "przyjemny", "łagodny", 7, 11,
     "Kapelusz 5–12 cm, pokryty brązowymi łuskami na jasnym tle. Miąższ "
     "po przekrojeniu wyraźnie czerwienieje. Blaszki od różowych po ciemnobrązowe. "
     "Rośnie w lasach iglastych, często przy mrowiskach.",
     "Miąższ czerwienieje; łuskowaty kapelusz; różowe do brązowych blaszki",
     None, 0),

    (20, "Pieczarka żółtawa", "Agaricus xanthodermus", "pieczarka karbolowa",
     "Agaricaceae", "trujacy", "blaszki", 1, 0, 0, 0,
     "polkulisty", "gladka", "ciemnobrązowy", "karbolowy, apteczny",
     "nieprzyjemny", 6, 10,
     "Wygląda jak zwykła pieczarka, ale podstawa trzonu po przekrojeniu "
     "intensywnie żółknie, a grzyb wydziela nieprzyjemny zapach karbolu lub "
     "atramentu, szczególnie wyraźny podczas smażenia.",
     "Podstawa trzonu żółknie po przecięciu; zapach karbolu",
     "TRUJĄCY — wywołuje dolegliwości żołądkowo-jelitowe. Zawsze przekrój "
     "podstawę trzonu przy zbiorze pieczarek.", 0),

    (21, "Czubajka kania", "Macrolepiota procera", "kania, sowa",
     "Agaricaceae", "jadalny", "blaszki", 1, 0, 0, 0,
     "parasolowaty", "luskowata", "biały", "przyjemny, orzechowy",
     "łagodny", 7, 11,
     "Duży grzyb o kapeluszu osiągającym nawet 30 cm średnicy, rosnący "
     "na obrzeżach lasów i łąkach. Kapelusz pokryty wyraźnymi, odstającymi "
     "brązowymi łuskami na jasnym tle. Blaszki białe, wolne. Trzon wysoki, "
     "smukły, pokryty wężykowatym deseniem, z ruchomym pierścieniem, który "
     "można przesuwać palcem — to cecha diagnostyczna. Miąższ nie zmienia barwy.",
     "Ruchomy pierścień na trzonie; wężykowaty deseń trzonu; brak pochwy",
     "Nie mylić z młodymi muchomorami — kania nie ma pochwy, a pierścień "
     "jest ruchomy.", 0),

    (22, "Czubajka gwiaździsta", "Chlorophyllum rhacodes", "czubajka czerwieniejąca",
     "Agaricaceae", "warunkowo", "blaszki", 1, 0, 0, 0,
     "parasolowaty", "luskowata", "biały", "przyjemny", "łagodny", 7, 11,
     "Podobna do kani, ale niższa i masywniejsza, o trzonie bez wężykowatego "
     "deseniu. Miąższ po przekrojeniu wyraźnie czerwienieje, przechodząc "
     "w pomarańczowobrązowy. Rośnie często w parkach, ogrodach i przy kompostownikach.",
     "Miąższ czerwienieje; gładki trzon bez deseniu; ruchomy pierścień",
     "WARUNKOWO JADALNY — u części osób wywołuje dolegliwości żołądkowe. "
     "Konieczna obróbka termiczna.", 0),

    # ---------------- GĄSKI, OPIEŃKI, INNE BLASZKOWE ----------------
    (23, "Opieńka miodowa", "Armillaria mellea", "opieńka",
     "Physalacriaceae", "warunkowo", "blaszki", 1, 0, 0, 0,
     "wypukly do płaskiego", "luskowata", "biały", "słaby, kwaskowaty",
     "cierpki na surowo", 8, 11,
     "Rośnie kępami na pniach, korzeniach i martwym drewnie drzew liściastych "
     "i iglastych. Kapelusz 3–10 cm, miodowożółty do brązowego, pokryty drobnymi "
     "ciemnymi łuseczkami w środkowej części. Blaszki zbiegające, kremowe, "
     "z wiekiem plamiste. Trzon z białym pierścieniem.",
     "Rośnie kępami na drewnie; drobne łuseczki na kapeluszu; biały pierścień",
     "WARUNKOWO JADALNY — konieczne gotowanie minimum 15–20 minut, wodę odlać. "
     "Na surowo lub niedogotowana wywołuje dolegliwości żołądkowo-jelitowe.", 0),

    (24, "Maślanka wiązkowa", "Hypholoma fasciculare", "maślanka ceglasta",
     "Strophariaceae", "trujacy", "blaszki", 0, 0, 0, 0,
     "wypukly", "gladka", "fioletowobrązowy", "nieprzyjemny", "bardzo gorzki", 5, 12,
     "Rośnie gęstymi kępami na pniakach, podobnie jak opieńka. Kapelusz 2–6 cm, "
     "siarkowożółty z ciemniejszym środkiem. Blaszki — cecha rozstrzygająca — "
     "są początkowo siarkowożółte, potem zielonkawe, wreszcie fioletowobrązowe. "
     "Brak pierścienia. Smak wybitnie gorzki.",
     "Siarkowożółte, potem zielonkawe blaszki; brak pierścienia; gorzki smak",
     "TRUJĄCY. Najczęstsza pomyłka z opieńką — sprawdzaj barwę blaszek "
     "i obecność pierścienia.", 0),

    (25, "Gąska zielonka", "Tricholoma equestre", "zielonka",
     "Tricholomataceae", "niejadalny", "blaszki", 0, 0, 0, 0,
     "wypukly do płaskiego", "gladka", "biały", "mączny", "łagodny", 9, 11,
     "Kapelusz 5–12 cm, żółtozielonkawy, lekko lepki, często zapiaszczony. "
     "Blaszki siarkowożółte, gęste. Rośnie w borach sosnowych na piaszczystej "
     "glebie, często zagrzebana w piasku.",
     "Żółtozielony kapelusz; siarkowożółte blaszki; bory sosnowe na piasku",
     "UWAGA: starsze atlasy i przewodniki (w tym wydania sprzed 2001 r.) "
     "opisują zielonkę jako smaczny grzyb jadalny. Po serii zatruć ze skutkiem "
     "śmiertelnym — rabdomioliza, czyli rozpad mięśni po spożyciu większych "
     "ilości — została w Polsce wykreślona z listy grzybów dopuszczonych "
     "do obrotu. Nie zaleca się zbierania.", 0),

    (26, "Gąska szara", "Tricholoma portentosum", "podzielona",
     "Tricholomataceae", "jadalny", "blaszki", 0, 0, 0, 0,
     "wypukly", "wlokienkowa", "biały", "mączny", "łagodny", 9, 11,
     "Kapelusz 4–12 cm, szary z ciemniejszymi promienistymi włóknami, lekko "
     "lepki. Blaszki białe z żółtawym odcieniem. Rośnie późną jesienią "
     "w borach sosnowych, znosi pierwsze przymrozki.",
     "Szary, promieniście włóknisty kapelusz; białożółtawe blaszki; późna jesień",
     "Dobry grzyb jadalny. Uważać na gąski trujące o mączno-nieprzyjemnym zapachu.", 0),

    (27, "Twardzioszek przydrożny", "Marasmius oreades", "grzyb łąkowy",
     "Marasmiaceae", "jadalny", "blaszki", 0, 0, 0, 0,
     "dzwonkowaty", "gladka", "biały", "przyjemny, migdałowy", "łagodny", 5, 11,
     "Drobny grzyb łąk i trawników, rosnący w charakterystycznych "
     "kręgach czarownic. Kapelusz 2–5 cm, cielisty do jasnobrązowego, "
     "z tępym garbkiem. Blaszki rzadkie, szerokie, kremowe. Trzon twardy, "
     "żylasty — nie nadaje się do jedzenia.",
     "Rośnie w kręgach na trawnikach; rzadkie blaszki; twardy, żylasty trzon",
     "Uwaga: na łąkach rosną też drobne, trujące lejkówki o gęstych blaszkach "
     "i białym kapeluszu.", 0),

    (28, "Boczniak ostrygowaty", "Pleurotus ostreatus", "boczniak",
     "Pleurotaceae", "jadalny", "blaszki", 0, 0, 0, 0,
     "muszlowaty", "gladka", "biały do liliowego", "przyjemny", "łagodny", 9, 12,
     "Rośnie dachówkowato na pniach drzew liściastych, głównie późną jesienią "
     "i zimą. Kapelusz 5–20 cm, muszlowaty lub wachlarzowaty, szarobrązowy "
     "do niebieskawego. Blaszki białe, wyraźnie zbiegające na krótki, boczny "
     "trzon. Znosi mróz.",
     "Muszlowaty kształt; blaszki zbiegające na boczny trzon; rośnie na drewnie",
     None, 0),

    (29, "Płomiennica zimowa", "Flammulina velutipes", "zimówka aksamitnotrzonowa",
     "Physalacriaceae", "jadalny", "blaszki", 0, 0, 0, 0,
     "wypukly", "sluzowata", "biały", "przyjemny", "łagodny", 10, 3,
     "Grzyb zimowy, rosnący kępami na drewnie drzew liściastych od października "
     "do marca. Kapelusz 2–8 cm, żółtobrązowy, śliski. Trzon ciemnobrązowy "
     "do czarnego, wyraźnie aksamitny — to cecha rozpoznawcza.",
     "Aksamitny, ciemny trzon; śliski żółty kapelusz; rośnie zimą",
     "Trzon jest twardy — używa się tylko kapeluszy.", 0),

    (30, "Pieprznik jadalny", "Cantharellus cibarius", "kurka, lisiczka",
     "Cantharellaceae", "jadalny", "fadki", 0, 0, 0, 0,
     "lejkowaty", "gladka", "jasnożółty", "owocowy, morelowy", "lekko pieprzny",
     6, 11,
     "Jeden z najłatwiejszych do rozpoznania grzybów jadalnych. Cały owocnik "
     "jednolicie żółtopomarańczowy. Kapelusz 3–10 cm, lejkowaty, o falistym "
     "brzegu. Pod kapeluszem nie ma prawdziwych blaszek, lecz grube, rozwidlone "
     "fałdki zbiegające daleko na trzon. Miąższ zwarty, o zapachu moreli.",
     "Rozwidlone fałdki zamiast blaszek; jednolicie żółty; zapach moreli",
     "Nie mylić z lisówką pomarańczową, która ma prawdziwe, cienkie blaszki "
     "i rośnie na drewnie lub torfie.", 0),

    (31, "Lisówka pomarańczowa", "Hygrophoropsis aurantiaca", "kurka fałszywa",
     "Hygrophoropsidaceae", "niejadalny", "blaszki", 0, 0, 0, 0,
     "lejkowaty", "aksamitna", "biały", "słaby", "łagodny", 8, 11,
     "Podobna do kurki, ale ma prawdziwe blaszki — cienkie, gęste, wielokrotnie "
     "rozwidlone, wyraźnie jaskrawsze pomarańczowe niż kapelusz. Miąższ miękki, "
     "wodnisty. Rośnie na próchnie i torfie, często w borach sosnowych.",
     "Prawdziwe, cienkie blaszki; jaskrawsza pomarańcz; miękki miąższ",
     "Nie jest silnie trujący, ale u części osób wywołuje dolegliwości "
     "żołądkowe. Jakość kulinarna żadna.", 0),

    # ---------------- MLECZAJE I GOŁĄBKI ----------------
    (32, "Mleczaj rydz", "Lactarius deliciosus", "rydz",
     "Russulaceae", "jadalny", "blaszki", 0, 0, 1, 0,
     "wklesly, lejkowaty", "gladka", "kremowy", "przyjemny, owocowy",
     "łagodny", 8, 11,
     "Grzyb borów sosnowych, rozpoznawalny po intensywnie pomarańczowej barwie "
     "i po marchwiowoczerwonym mleczku, które wypływa po przecięciu miąższu "
     "i z czasem szarozielenieje. Kapelusz 4–12 cm, z koncentrycznymi "
     "ciemniejszymi strefami, brzeg długo podwinięty. Blaszki bladopomarańczowe, "
     "krótko zbiegające. Trzon krótki, szybko pusty, pokryty wyraźnymi "
     "pomarańczowymi, płytkimi jamkami — to dobra cecha rozpoznawcza.",
     "Marchwiowe mleczko; pomarańczowe jamki na trzonie; zielenienie uszkodzeń",
     "Zielone plamy na owocniku są naturalne i nie dyskwalifikują grzyba.", 0),

    (33, "Mleczaj świerkowy", "Lactarius deterrimus", "rydz świerkowy",
     "Russulaceae", "jadalny", "blaszki", 0, 0, 1, 0,
     "wklesly", "gladka", "kremowy", "przyjemny", "lekko gorzkawy", 8, 10,
     "Bardzo podobny do rydza, ale rośnie pod świerkami i znacznie szybciej "
     "oraz intensywniej zielenieje. Strefowanie kapelusza słabiej zaznaczone. "
     "Mleczko pomarańczowe, po kilkunastu minutach winnoczerwone.",
     "Silne, szybkie zielenienie; pod świerkami; słabe strefowanie kapelusza",
     "Jadalny, ale gorszej jakości niż rydz sosnowy.", 0),

    (34, "Mleczaj chrząstka", "Lactarius vellereus", "chrząstka",
     "Russulaceae", "niejadalny", "blaszki", 0, 0, 1, 0,
     "lejkowaty", "aksamitna", "biały", "słaby", "bardzo ostry, piekący", 7, 10,
     "Duży, w całości biały grzyb o kapeluszu 8–25 cm, aksamitnym w dotyku. "
     "Mleczko białe, natychmiast po spróbowaniu wywołuje silne pieczenie "
     "języka. Miąższ twardy, zbity.",
     "Cały biały i aksamitny; białe mleczko; skrajnie ostry smak",
     "Niejadalny ze względu na ostry smak.", 0),

    (35, "Gołąbek zielonawy", "Russula virescens", "gołąbek zielony",
     "Russulaceae", "jadalny", "blaszki", 0, 0, 0, 0,
     "wypukly do płaskiego", "gladka", "biały", "przyjemny", "łagodny, orzechowy",
     6, 10,
     "Jeden z najsmaczniejszych gołąbków. Kapelusz 5–12 cm, zielonkawy, "
     "charakterystycznie spękany na drobne, wielokątne pola przypominające "
     "mozaikę. Blaszki i trzon białe, kruche. Miąższ łamie się jak kreda.",
     "Zielony kapelusz spękany w mozaikę; biały, kruchy miąższ; łagodny smak",
     "Zielonkawa barwa bywa mylona z muchomorem sromotnikowym — gołąbek "
     "nie ma pierścienia ani pochwy.", 0),

    (36, "Gołąbek wymiotny", "Russula emetica", "gołąbek jadowity",
     "Russulaceae", "trujacy", "blaszki", 0, 0, 0, 0,
     "wypukly", "gladka", "biały", "owocowy", "skrajnie ostry, piekący", 7, 10,
     "Kapelusz 3–10 cm, jaskrawoczerwony, o skórce łatwo dającej się ściągnąć. "
     "Blaszki i trzon czysto białe. Smak natychmiast piekący. Rośnie "
     "na wilgotnych, kwaśnych glebach, często wśród mchów.",
     "Jaskrawoczerwony kapelusz; białe blaszki; skrajnie piekący smak",
     "TRUJĄCY — wywołuje wymioty i biegunkę. U gołąbków obowiązuje prosta "
     "zasada: ostry, piekący smak oznacza, że grzyba nie zbieramy.", 0),

    # ---------------- SMARDZE, PIESTRZENICE ----------------
    (37, "Smardz jadalny", "Morchella esculenta", "smardz",
     "Morchellaceae", "warunkowo", "gladki", 0, 0, 0, 0,
     "jajowaty", "komorkowa", "kremowy", "przyjemny", "łagodny", 4, 5,
     "Wiosenny grzyb workowy o charakterystycznym, gąbczastym kapeluszu "
     "pokrytym regularnymi, wyraźnie odgraniczonymi komorami. Kapelusz "
     "4–10 cm, żółtobrązowy, zrośnięty z trzonem na całym obwodzie. "
     "Po przekrojeniu wzdłuż wnętrze jest jedną, całkowicie pustą komorą — "
     "to cecha odróżniająca od śmiertelnie trujących piestrzenic, "
     "których miąższ wypełniają nieregularne pofałdowania.",
     "Regularne komory na kapeluszu; wnętrze jedną pustą komorą; wiosna",
     "WARUNKOWO JADALNY — konieczne dokładne ugotowanie. W Polsce smardze "
     "są pod ochroną częściową; sprawdź aktualne przepisy przed zbiorem.", 1),

    (38, "Piestrzenica kasztanowata", "Gyromitra esculenta", "babie uszy",
     "Discinaceae", "smiertelny", "gladki", 0, 0, 0, 0,
     "mozgowaty", "pofaldowana", "bialy", "bardzo słaby", "łagodny", 3, 5,
     "Wiosenny grzyb o główce 3–9 cm, kasztanowobrązowej do czerwonobrązowej, "
     "kulistej i silnie pofałdowanej — wyglądem przypomina zwoje mózgu. "
     "Brzeg zrośnięty z trzonem. Trzon białawy do bladoszarego, krótki, "
     "pomarszczony, o zgrubiałej podstawie. Miąższ woskowaty i kruchy, "
     "z nieregularnymi pustymi przestrzeniami w całym owocniku — "
     "w odróżnieniu od smardza, którego wnętrze jest jedną pustą komorą. "
     "Zawiera gyromitrynę, związek hepatotoksyczny i rakotwórczy.",
     "Mózgowato pofałdowana główka; miąższ z nieregularnymi komorami; wiosna",
     "W STANIE SUROWYM ŚMIERTELNIE TRUJĄCA. Dawniej bywała spożywana "
     "po obgotowaniu lub wysuszeniu, ale nawet tak przygotowana wywoływała "
     "poważne zatrucia. Toksyna jest lotna i groźna również przy wdychaniu "
     "oparów podczas gotowania. Nie zbierać.", 0),

    # ---------------- KOLCZAKI, ŻAGWIE, INNE ----------------
    (39, "Kolczak obłączasty", "Hydnum repandum", "kolczak żółty",
     "Hydnaceae", "jadalny", "kolce", 0, 0, 0, 0,
     "nieregularny", "gladka", "kremowy", "przyjemny", "lekko gorzkawy", 8, 11,
     "Łatwy do rozpoznania dzięki kolcom pod kapeluszem — miękkim, kruchym "
     "igiełkom, które łatwo odpadają przy potarciu. Kapelusz 4–15 cm, "
     "nieregularny, cielistożółty. Miąższ kruchy, biały.",
     "Miękkie kolce zamiast blaszek; cielistożółta barwa; nieregularny kapelusz",
     "U starszych owocników miąższ gorzknieje.", 0),

    (40, "Żagiew siarkowa", "Laetiporus sulphureus", "kurczak z lasu",
     "Fomitopsidaceae", "warunkowo", "rurki", 0, 0, 0, 0,
     "wachlarzowaty", "aksamitna", "biały", "przyjemny, kwaskowaty",
     "łagodny", 5, 7,
     "Jaskrawopomarańczowożółty grzyb rosnący dachówkowato na pniach drzew "
     "liściastych — robinii, dębów i topoli, często przydrożnych i parkowych. "
     "Owocniki pojawiają się wiosną i wczesnym latem, głównie w maju i czerwcu. "
     "Tworzą półkoliste, wachlarzowate kapelusze do 30 cm. Młode są miękkie "
     "i soczyste, starsze twardnieją i stają się niejadalne.",
     "Jaskrawopomarańczowe wachlarze na pniu; brak trzonu; drobne żółte pory",
     "WARUNKOWO JADALNY — tylko młode owocniki, po ugotowaniu; surowy jest "
     "trujący. Okazy rosnące na drzewach iglastych i na cisie mogą powodować "
     "zatrucia. Groźny pasożyt drzew.", 0),

    (41, "Purchawka chropowata", "Lycoperdon perlatum", "purchawka jeżowata",
     "Agaricaceae", "jadalny", "brak", 0, 0, 0, 0,
     "gruszkowaty", "kolczasta", "oliwkowobrązowy", "przyjemny", "łagodny", 7, 11,
     "Gruszkowaty owocnik 3–7 cm wysokości, pokryty drobnymi kolcami "
     "odpadającymi z wiekiem. Jadalna tylko dopóki miąższ w środku jest "
     "całkowicie biały i jednolity — po przekrojeniu należy to sprawdzić. "
     "Gdy wnętrze zżółknie lub zbrązowieje, grzyb jest już niejadalny.",
     "Gruszkowaty kształt; kolczasta powierzchnia; miąższ musi być czysto biały",
     "ZAWSZE przekrój purchawkę przed zbiorem. Białe, jajowate owocniki "
     "z zarysem grzyba w środku to młode muchomory, nie purchawki.", 0),

    (42, "Czernidłak kołpakowaty", "Coprinus comatus", "czernidłak pierzasty",
     "Agaricaceae", "warunkowo", "blaszki", 1, 0, 0, 0,
     "walcowaty", "luskowata", "czarny", "przyjemny", "łagodny", 5, 11,
     "Wysoki, walcowaty kapelusz 5–15 cm, biały, pokryty odstającymi łuskami. "
     "Blaszki początkowo białe, potem różowe, wreszcie czarne i rozpływające "
     "się w atramentowatą ciecz. Jadalny wyłącznie póki jest całkowicie biały "
     "w środku, najlepiej przyrządzony w dniu zbioru.",
     "Walcowaty biały kapelusz z łuskami; blaszki czernieją i rozpływają się",
     "WARUNKOWO JADALNY — tylko młode, białe owocniki. Nie spożywać "
     "z alkoholem: pokrewne gatunki zawierają koprynę wywołującą reakcję "
     "podobną do disulfiramowej.", 0),

    (43, "Uszak bzowy", "Auricularia auricula-judae", "ucho Judasza",
     "Auriculariaceae", "jadalny", "gladki", 0, 0, 0, 0,
     "uchowaty", "gladka", "biały", "słaby", "łagodny", 1, 12,
     "Galaretowaty owocnik w kształcie ucha, 3–10 cm, brunatny, rosnący "
     "na martwym drewnie bzu czarnego. Występuje przez cały rok, także zimą. "
     "Po wysuszeniu kurczy się, po namoczeniu wraca do pierwotnej formy.",
     "Galaretowaty, uchowaty kształt; rośnie na bzie czarnym; cały rok",
     None, 0),

    (44, "Płachetka kołpakowata", "Cortinarius caperatus", "płachetka zwyczajna",
     "Cortinariaceae", "jadalny", "blaszki", 1, 0, 0, 0,
     "dzwonkowaty", "pomarszczona", "rdzawobrązowy", "przyjemny", "łagodny", 8, 10,
     "Kapelusz 5–12 cm, ochrowożółty, u młodych owocników pokryty białawym "
     "nalotem, pomarszczony przy brzegu. Blaszki rdzawobrązowe. Trzon "
     "z białym pierścieniem. Rośnie w borach, często wśród borówek.",
     "Pomarszczony ochrowy kapelusz; rdzawe blaszki; biały pierścień",
     "Uwaga: to jedyny zasłonak powszechnie zbierany. Większość zasłonaków "
     "jest trująca, w tym śmiertelnie — początkującym odradza się cały rodzaj.", 0),

    (45, "Zasłonak rudy", "Cortinarius rubellus",
     "zasłonak szpiczasty, Cortinarius speciosissimus",
     "Cortinariaceae", "smiertelny", "blaszki", 0, 0, 0, 0,
     "stozkowaty", "luskowata", "rdzawobrązowy", "rzodkiewkowy", "łagodny", 7, 9,
     "Kapelusz 3–8 cm, pomarańczowoczerwony do rdzawobrązowego, u młodych "
     "owocników spiczasto-stożkowaty, później słabo wypukły, ale zawsze "
     "z wyraźnym spiczastym garbkiem. Powierzchnia delikatnie łuskowata, matowa. "
     "Blaszki czerwonobrązowe, grube i rzadkie. Trzon barwy kapelusza, mocny, "
     "zwykle z kilkoma pasmami żółtawych resztek osłony. Zawiera orellaninę "
     "uszkadzającą nerki — objawy pojawiają się dopiero po 2–3 tygodniach.",
     "Spiczasty garbek na kapeluszu; grube, rzadkie blaszki; żółtawe pasma na trzonie",
     "ŚMIERTELNIE TRUJĄCY. Bardzo długi okres bezobjawowy sprawia, że zatrucie "
     "bywa rozpoznane zbyt późno. Prowadzi do nieodwracalnej niewydolności nerek. "
     "Blisko spokrewniony zasłonak rudy (Cortinarius orellanus) zawiera tę samą "
     "truciznę, ale rośnie w cieplejszych okolicach i jest rzadszy.", 0),

    (46, "Hełmówka obrzeżona", "Galerina marginata", "hełmówka jadowita",
     "Hymenogastraceae", "smiertelny", "blaszki", 1, 0, 0, 0,
     "wypukly", "gladka", "rdzawobrązowy", "mączny", "łagodny", 8, 11,
     "Drobny grzyb o kapeluszu 1,5–4 cm, ochrowym do żółtobrązowego, "
     "wodochłonnym — przy wilgotnej pogodzie brzeg jest przeświecająco "
     "prążkowany. Rośnie kępami, głównie na martwym drewnie iglastym. "
     "Blaszki cynamonowobrązowe, gęste. Trzon pusty, z małym błoniastym "
     "pierścieniem; pod pierścieniem pokryty białawymi włóknami, ale "
     "BEZ łuseczek, z wiekiem czerniejący od podstawy. Zawiera te same "
     "amatoksyny co muchomor sromotnikowy.",
     "Trzon pod pierścieniem gładki, bez łuseczek; rdzawy wysyp; drewno iglaste",
     "ŚMIERTELNIE TRUJĄCA. Rośnie w tych samych miejscach co opieńki "
     "i łuszczak zmienny. Cecha rozstrzygająca: trzon pod pierścieniem jest "
     "gładki i włóknisty, bez wyraźnych łuseczek, a grzyb rośnie głównie "
     "na drewnie iglastym. Nie robić próby smakowej.", 0),

    (47, "Lejkówka jadowita", "Clitocybe rivulosa", "lejkówka biaława",
     "Tricholomataceae", "smiertelny", "blaszki", 0, 0, 0, 0,
     "wklesly", "gladka", "biały", "słaby, mączny", "łagodny", 7, 11,
     "Drobna, biaława lejkówka 2–5 cm rosnąca na trawnikach i łąkach, często "
     "w kręgach — dokładnie tam, gdzie zbiera się twardzioszka przydrożnego. "
     "Blaszki białe, gęste, zbiegające. Zawiera muskarynę.",
     "Biaława, drobna; gęste zbiegające blaszki; rośnie na trawnikach w kręgach",
     "ŚMIERTELNIE TRUJĄCA przy większych dawkach. Mylona z twardzioszkiem, "
     "który ma rzadkie blaszki i twardy trzon.", 0),

    (48, "Podgrzybek pasożytniczy", "Pseudoboletus parasiticus", None,
     "Boletaceae", "niejadalny", "rurki", 0, 0, 0, 0,
     "poduszkowaty", "aksamitna", "oliwkowy", "słaby", "łagodny", 8, 10,
     "Osobliwość — rośnie wyłącznie na owocnikach tęgoskóra pospolitego. "
     "Kapelusz 2–6 cm, oliwkowożółty, aksamitny. Rzadki, objęty ochroną "
     "częściową.",
     "Rośnie na tęgoskórze; drobne rozmiary; oliwkowy aksamitny kapelusz",
     "Chroniony — nie zbierać.", 1),

    (49, "Tęgoskór pospolity", "Scleroderma citrinum", "tęgoskór cytrynowy",
     "Sclerodermataceae", "trujacy", "brak", 0, 0, 0, 0,
     "kulisty", "luskowata", "czarnofioletowy", "nieprzyjemny, gumowy",
     "nieprzyjemny", 7, 11,
     "Kulisty owocnik 3–10 cm o grubej, twardej, żółtobrązowej skórce pokrytej "
     "łuskami. Bywa mylony z purchawką, ale po przekrojeniu wnętrze jest "
     "od początku ciemnofioletowe do czarnego, nie białe. Skórka gruba "
     "jak skóra, nie miękka.",
     "Twarda, łuskowata skórka; wnętrze od razu ciemne, nie białe",
     "TRUJĄCY. Zawsze przekrój okrągłe grzyby — purchawka ma wnętrze "
     "czysto białe, tęgoskór ciemne.", 0),

    (51, "Łuszczak zmienny", "Kuehneromyces mutabilis",
     "Pholiota mutabilis, opieńka zmienna",
     "Strophariaceae", "jadalny", "blaszki", 1, 0, 0, 0,
     "wypukly", "gladka", "rdzawobrązowy", "przyjemny", "łagodny", 4, 12,
     "Kapelusz 3–6 cm, cynamonowobrązowy do żółtobrązowego, wodochłonny — "
     "przy dużej wilgotności ma wyraźnie ciemniejszy brzeg i widoczne jasne "
     "oraz ciemne strefy. Rośnie kępami na obumarłym drewnie liściastym. "
     "Blaszki cynamonowe, przyrośnięte i nieco zbiegające. Cecha rozstrzygająca: "
     "trzon pod pierścieniem jest aż do podstawy pokryty wyraźnymi łuseczkami "
     "i ciemnordzawy, nad pierścieniem gładki i jasny.",
     "Trzon pod pierścieniem wyraźnie łuseczkowaty; rośnie kępami na drewnie liściastym",
     "Jadalny, ale zalecany wyłącznie doświadczonym grzybiarzom — rośnie "
     "w tych samych miejscach co śmiertelnie trująca hełmówka obrzeżona. "
     "Używa się tylko kapeluszy, trzony są włókniste.", 0),

    (50, "Krowiak podwinięty", "Paxillus involutus", "olszówka",
     "Paxillaceae", "smiertelny", "blaszki", 0, 0, 0, 0,
     "wklesly", "aksamitna", "brązowy", "kwaskowaty", "łagodny", 7, 10,
     "Kapelusz 5–15 cm, oliwkowobrązowy, o silnie podwiniętym brzegu. Blaszki "
     "zbiegające, dające się oddzielić od kapelusza, po uciśnięciu wyraźnie "
     "brązowieją. Przez dziesięciolecia zbierany jako jadalny po ugotowaniu.",
     "Silnie podwinięty brzeg kapelusza; blaszki brązowieją po dotknięciu",
     "ŚMIERTELNIE TRUJĄCY. Wywołuje reakcję alergiczną na białko grzyba, "
     "prowadzącą do rozpadu krwinek czerwonych. Uczulenie narasta przy "
     "kolejnych kontaktach, więc zatrucie może wystąpić nagle po latach "
     "bezobjawowego spożywania. Do lat 70. XX w. uznawany za jadalny — "
     "starsze atlasy i rodzinna tradycja bywają tu mylące.", 0),
]

# species_id -> [(kolor, czesc), ...]
KOLORY_SP = {
    1: [("brazowy","kapelusz"),("ciemnobrazowy","kapelusz"),("kremowy","trzon"),
        ("bialy","hymenofor"),("oliwkowy","hymenofor"),("bialy","miazsz")],
    2: [("brazowy","kapelusz"),("kremowy","trzon"),("rozowy","hymenofor"),("bialy","miazsz")],
    3: [("ciemnobrazowy","kapelusz"),("brazowy","kapelusz"),("zolty","trzon"),
        ("czerwony","hymenofor"),("niebieski","miazsz")],
    4: [("bialy","kapelusz"),("kremowy","kapelusz"),("szary","kapelusz"),
        ("czerwony","trzon"),("czerwony","hymenofor"),("bialy","miazsz")],
    5: [("brazowy","kapelusz"),("ciemnobrazowy","kapelusz"),("brazowy","trzon"),
        ("zolty","hymenofor"),("oliwkowy","hymenofor"),("bialy","miazsz")],
    6: [("oliwkowy","kapelusz"),("brazowy","kapelusz"),("zolty","trzon"),
        ("zolty","hymenofor"),("bialy","miazsz")],
    7: [("brazowy","kapelusz"),("szary","kapelusz"),("bialy","trzon"),
        ("bialy","hymenofor"),("bialy","miazsz")],
    8: [("pomaranczowy","kapelusz"),("czerwony","kapelusz"),("bialy","trzon"),
        ("bialy","hymenofor"),("czarny","miazsz")],
    9: [("brazowy","kapelusz"),("ciemnobrazowy","kapelusz"),("zolty","trzon"),
        ("zolty","hymenofor"),("zolty","miazsz")],
    10:[("brazowy","kapelusz"),("rudy","kapelusz"),("kremowy","trzon"),
        ("oliwkowy","hymenofor"),("kremowy","miazsz")],
    11:[("brazowy","kapelusz"),("rudy","kapelusz"),("zolty","trzon"),
        ("zolty","hymenofor"),("zolty","miazsz")],
    12:[("zielonkawy","kapelusz"),("oliwkowy","kapelusz"),("bialy","trzon"),
        ("bialy","hymenofor"),("bialy","miazsz")],
    13:[("bialy","kapelusz"),("bialy","trzon"),("bialy","hymenofor"),("bialy","miazsz")],
    14:[("czerwony","kapelusz"),("pomaranczowy","kapelusz"),("bialy","trzon"),
        ("bialy","hymenofor"),("bialy","miazsz")],
    15:[("brazowy","kapelusz"),("ciemnobrazowy","kapelusz"),("bialy","trzon"),
        ("bialy","hymenofor"),("bialy","miazsz")],
    16:[("rozowy","kapelusz"),("brazowy","kapelusz"),("bialy","trzon"),
        ("bialy","hymenofor"),("rozowy","miazsz")],
    17:[("szary","kapelusz"),("bialy","trzon"),("bialy","hymenofor"),("bialy","miazsz")],
    18:[("bialy","kapelusz"),("kremowy","kapelusz"),("bialy","trzon"),
        ("rozowy","hymenofor"),("brazowy","hymenofor"),("bialy","miazsz")],
    19:[("brazowy","kapelusz"),("kremowy","kapelusz"),("bialy","trzon"),
        ("rozowy","hymenofor"),("brazowy","hymenofor"),("czerwony","miazsz")],
    20:[("bialy","kapelusz"),("szary","kapelusz"),("bialy","trzon"),
        ("rozowy","hymenofor"),("zolty","miazsz")],
    21:[("brazowy","kapelusz"),("kremowy","kapelusz"),("brazowy","trzon"),
        ("bialy","hymenofor"),("bialy","miazsz")],
    22:[("brazowy","kapelusz"),("kremowy","kapelusz"),("kremowy","trzon"),
        ("bialy","hymenofor"),("czerwony","miazsz")],
    23:[("zolty","kapelusz"),("brazowy","kapelusz"),("brazowy","trzon"),
        ("kremowy","hymenofor"),("bialy","miazsz")],
    24:[("zolty","kapelusz"),("pomaranczowy","kapelusz"),("zolty","trzon"),
        ("zielonkawy","hymenofor"),("zolty","miazsz")],
    25:[("zolty","kapelusz"),("zielonkawy","kapelusz"),("zolty","trzon"),
        ("zolty","hymenofor"),("bialy","miazsz")],
    26:[("szary","kapelusz"),("ciemnobrazowy","kapelusz"),("bialy","trzon"),
        ("bialy","hymenofor"),("bialy","miazsz")],
    27:[("kremowy","kapelusz"),("brazowy","kapelusz"),("kremowy","trzon"),
        ("kremowy","hymenofor"),("bialy","miazsz")],
    28:[("szary","kapelusz"),("brazowy","kapelusz"),("bialy","trzon"),
        ("bialy","hymenofor"),("bialy","miazsz")],
    29:[("zolty","kapelusz"),("brazowy","kapelusz"),("czarny","trzon"),
        ("kremowy","hymenofor"),("bialy","miazsz")],
    30:[("zolty","kapelusz"),("pomaranczowy","kapelusz"),("zolty","trzon"),
        ("zolty","hymenofor"),("bialy","miazsz")],
    31:[("pomaranczowy","kapelusz"),("zolty","kapelusz"),("pomaranczowy","trzon"),
        ("pomaranczowy","hymenofor"),("kremowy","miazsz")],
    32:[("pomaranczowy","kapelusz"),("pomaranczowy","trzon"),
        ("pomaranczowy","hymenofor"),("pomaranczowy","miazsz")],
    33:[("pomaranczowy","kapelusz"),("zielonkawy","kapelusz"),("pomaranczowy","trzon"),
        ("pomaranczowy","hymenofor"),("zielonkawy","miazsz")],
    34:[("bialy","kapelusz"),("kremowy","kapelusz"),("bialy","trzon"),
        ("kremowy","hymenofor"),("bialy","miazsz")],
    35:[("zielonkawy","kapelusz"),("oliwkowy","kapelusz"),("bialy","trzon"),
        ("bialy","hymenofor"),("bialy","miazsz")],
    36:[("czerwony","kapelusz"),("bialy","trzon"),("bialy","hymenofor"),("bialy","miazsz")],
    37:[("brazowy","kapelusz"),("kremowy","kapelusz"),("kremowy","trzon"),
        ("kremowy","hymenofor"),("bialy","miazsz")],
    38:[("brazowy","kapelusz"),("ciemnobrazowy","kapelusz"),("kremowy","trzon"),
        ("brazowy","hymenofor"),("bialy","miazsz")],
    39:[("kremowy","kapelusz"),("zolty","kapelusz"),("kremowy","trzon"),
        ("kremowy","hymenofor"),("bialy","miazsz")],
    40:[("pomaranczowy","kapelusz"),("zolty","kapelusz"),
        ("zolty","hymenofor"),("bialy","miazsz")],
    41:[("bialy","kapelusz"),("kremowy","kapelusz"),("bialy","trzon"),
        ("bialy","miazsz")],
    42:[("bialy","kapelusz"),("kremowy","kapelusz"),("bialy","trzon"),
        ("bialy","hymenofor"),("czarny","hymenofor"),("bialy","miazsz")],
    43:[("brazowy","kapelusz"),("ciemnobrazowy","kapelusz"),("brazowy","hymenofor"),
        ("brazowy","miazsz")],
    44:[("kremowy","kapelusz"),("zolty","kapelusz"),("kremowy","trzon"),
        ("rudy","hymenofor"),("bialy","miazsz")],
    45:[("rudy","kapelusz"),("pomaranczowy","kapelusz"),("rudy","trzon"),
        ("rudy","hymenofor"),("zolty","miazsz")],
    46:[("brazowy","kapelusz"),("rudy","kapelusz"),("brazowy","trzon"),
        ("rudy","hymenofor"),("kremowy","miazsz")],
    47:[("bialy","kapelusz"),("kremowy","kapelusz"),("bialy","trzon"),
        ("bialy","hymenofor"),("bialy","miazsz")],
    48:[("oliwkowy","kapelusz"),("zolty","kapelusz"),("zolty","trzon"),
        ("zolty","hymenofor"),("zolty","miazsz")],
    49:[("zolty","kapelusz"),("brazowy","kapelusz"),("czarny","miazsz")],
    50:[("brazowy","kapelusz"),("oliwkowy","kapelusz"),("brazowy","trzon"),
        ("brazowy","hymenofor"),("kremowy","miazsz")],
    51:[("brazowy","kapelusz"),("rudy","kapelusz"),("ciemnobrazowy","trzon"),
        ("rudy","hymenofor"),("bialy","miazsz")],
}

SIEDL_SP = {
    1: ["las liściasty","las iglasty","las mieszany","buczyny","dąbrowy","świerczyny"],
    2: ["las iglasty","las mieszany","bory sosnowe"],
    3: ["las liściasty","las mieszany","buczyny","dąbrowy"],
    4: ["las liściasty","dąbrowy","buczyny"],
    5: ["bory sosnowe","las iglasty","las mieszany","świerczyny"],
    6: ["las liściasty","las mieszany","dąbrowy"],
    7: ["brzeziny","las mieszany","las liściasty","obrzeża lasu"],
    8: ["las liściasty","las mieszany","brzeziny"],
    9: ["bory sosnowe","las iglasty","las mieszany"],
    10:["bory sosnowe","las iglasty"],
    11:["bory sosnowe","las iglasty","las mieszany"],
    12:["las liściasty","las mieszany","buczyny","dąbrowy","parki i zadrzewienia"],
    13:["las iglasty","las mieszany","świerczyny"],
    14:["las iglasty","las mieszany","brzeziny","bory sosnowe"],
    15:["las liściasty","las mieszany","buczyny","dąbrowy"],
    16:["las liściasty","las iglasty","las mieszany"],
    17:["las liściasty","las mieszany","parki i zadrzewienia"],
    18:["łąki i pastwiska","parki i zadrzewienia","tereny ruderalne"],
    19:["las iglasty","las mieszany","świerczyny"],
    20:["parki i zadrzewienia","tereny ruderalne","łąki i pastwiska"],
    21:["obrzeża lasu","łąki i pastwiska","las liściasty","parki i zadrzewienia"],
    22:["parki i zadrzewienia","obrzeża lasu","tereny ruderalne"],
    23:["drewno martwe","drewno żywych drzew","las liściasty","las mieszany"],
    24:["drewno martwe","las liściasty","las mieszany","las iglasty"],
    25:["bory sosnowe","las iglasty"],
    26:["bory sosnowe","las iglasty","las mieszany"],
    27:["łąki i pastwiska","parki i zadrzewienia","tereny ruderalne"],
    28:["drewno martwe","drewno żywych drzew","las liściasty","parki i zadrzewienia"],
    29:["drewno martwe","las liściasty","parki i zadrzewienia"],
    30:["las liściasty","las iglasty","las mieszany","buczyny","dąbrowy"],
    31:["bory sosnowe","las iglasty","drewno martwe","torfowiska"],
    32:["bory sosnowe","las iglasty"],
    33:["świerczyny","las iglasty","las mieszany"],
    34:["las liściasty","las mieszany","buczyny"],
    35:["las liściasty","dąbrowy","buczyny","las mieszany"],
    36:["las iglasty","las mieszany","torfowiska"],
    37:["las liściasty","parki i zadrzewienia","obrzeża lasu"],
    38:["bory sosnowe","las iglasty","las mieszany"],
    39:["las liściasty","las iglasty","las mieszany","buczyny"],
    40:["drewno żywych drzew","drewno martwe","dąbrowy","parki i zadrzewienia"],
    41:["las liściasty","las iglasty","las mieszany","parki i zadrzewienia"],
    42:["łąki i pastwiska","tereny ruderalne","parki i zadrzewienia","obrzeża lasu"],
    43:["drewno martwe","parki i zadrzewienia","las liściasty"],
    44:["bory sosnowe","las iglasty","las mieszany","torfowiska"],
    45:["las iglasty","świerczyny","torfowiska","bory sosnowe"],
    46:["drewno martwe","las iglasty","las mieszany","las liściasty"],
    47:["łąki i pastwiska","parki i zadrzewienia","tereny ruderalne"],
    48:["las liściasty","las mieszany"],
    49:["las liściasty","las iglasty","las mieszany","bory sosnowe"],
    50:["las liściasty","las mieszany","brzeziny","parki i zadrzewienia"],
    51:["drewno martwe","las liściasty","las mieszany","las iglasty"],
}

# (species_id, similar_id, roznice, waga)  waga 3 = pomylka smiertelna
LOOKALIKES = [
    # borowik <-> goryczak
    (1, 2, "Goryczak ma ciemną, kontrastową siateczkę na trzonie i różowawe rurki. "
           "Smak skrajnie gorzki — wystarczy dotknąć językiem kawałek miąższu.", 2),
    (2, 1, "Borowik ma jasną, delikatną siateczkę i rurki białe do oliwkowych. "
           "Smak łagodny, orzechowy.", 2),
    # borowik ceglastopory <-> szatański
    (3, 4, "Borowik szatański ma JASNY, białawy lub szarawy kapelusz. "
           "Ceglastopory ma kapelusz ciemnobrązowy, aksamitny.", 2),
    (4, 3, "Borowik ceglastopory ma ciemnobrązowy kapelusz i żółty trzon "
           "z czerwonymi kropkami zamiast siateczki.", 2),
    # pieczarka <-> muchomory
    (18, 12, "Muchomor sromotnikowy ma blaszki ZAWSZE białe i workowatą pochwę "
             "u podstawy trzonu. Pieczarka ma blaszki różowe lub brązowe "
             "i nie ma pochwy.", 3),
    (12, 18, "Pieczarka ma różowe lub czekoladowobrązowe blaszki i brak pochwy. "
             "Muchomor sromotnikowy — białe blaszki, pochwa u podstawy.", 3),
    (18, 13, "Muchomor jadowity jest cały biały, ma białe blaszki i pochwę. "
             "Pieczarka ma różowe do brązowych blaszki i nie ma pochwy.", 3),
    (13, 18, "Pieczarka ma różowe lub brązowe blaszki i brak pochwy.", 3),
    (18, 20, "Pieczarka żółtawa po przecięciu podstawy trzonu intensywnie żółknie "
             "i pachnie karbolem. Zawsze przekrój podstawę trzonu.", 2),
    (20, 18, "Pieczarka polna nie żółknie po przecięciu i pachnie przyjemnie "
             "grzybowo.", 2),
    # kania <-> muchomory
    (21, 12, "Kania ma ruchomy pierścień, wężykowaty deseń na trzonie i brak pochwy. "
             "Młody muchomor sromotnikowy ma pochwę i blaszki stale białe.", 3),
    (21, 13, "Kania ma ruchomy pierścień i wężykowaty trzon. Muchomor jadowity "
             "jest cały biały, ma kosmaty trzon i workowatą pochwę.", 3),
    (13, 21, "Kania nie ma pochwy, jej pierścień jest ruchomy, a trzon pokryty "
             "wężykowatym deseniem.", 3),
    (21, 22, "Czubajka gwiaździsta ma gładki trzon bez deseniu i miąższ, "
             "który po przekrojeniu czerwienieje.", 1),
    # opieńka <-> maślanka i hełmówka
    (23, 24, "Maślanka wiązkowa ma siarkowożółte, potem zielonkawe blaszki, "
             "brak pierścienia i skrajnie gorzki smak.", 2),
    (24, 23, "Opieńka ma kremowe blaszki, wyraźny biały pierścień i łagodny smak.", 2),
    (23, 46, "Hełmówka obrzeżona jest drobniejsza i ma rdzawobrązowe blaszki "
             "oraz rdzawy wysyp zarodników. Opieńka ma blaszki kremowe "
             "i biały wysyp. Rosną w tych samych miejscach.", 3),
    (46, 23, "Opieńka ma kremowe blaszki i biały wysyp zarodników, jest większa "
             "i rośnie gęstszymi kępami.", 3),
    # kurka <-> lisówka
    (30, 31, "Lisówka ma prawdziwe, cienkie i gęste blaszki, wyraźnie jaskrawiej "
             "pomarańczowe niż kapelusz. Kurka ma grube, rozwidlone fałdki.", 1),
    (31, 30, "Kurka ma grube, rozwidlone fałdki zbiegające na trzon i zapach "
             "moreli. Miąższ zwarty, nie wodnisty.", 1),
    # muchomor czerwony <-> czerwieniejący, plamisty
    (14, 16, "Muchomor czerwieniejący ma brudnoróżowy kapelusz i miąższ, który "
             "czerwienieje po uszkodzeniu.", 1),
    (15, 16, "Muchomor czerwieniejący ma miąższ czerwieniejący po uszkodzeniu "
             "i pierścień wyraźnie żeberkowany od góry. Plamisty ma pierścień "
             "gładki i kołnierzyk nad bulwą.", 2),
    (16, 15, "Muchomor plamisty ma gładki pierścień, wyraźny kołnierzyk nad bulwą "
             "i miąższ, który NIE czerwienieje.", 2),
    # gołąbek zielonawy <-> muchomor sromotnikowy
    (35, 12, "Muchomor sromotnikowy ma pierścień na trzonie i pochwę u podstawy. "
             "Gołąbek nie ma ani jednego, ani drugiego, a jego miąższ jest kruchy "
             "i łamie się jak kreda.", 3),
    (12, 35, "Gołąbek zielonawy ma kapelusz spękany w mozaikę, kruchy miąższ, "
             "brak pierścienia i brak pochwy.", 3),
    # rydz <-> mleczaj świerkowy
    (32, 33, "Mleczaj świerkowy zielenieje znacznie szybciej i intensywniej, "
             "rośnie pod świerkami, ma słabsze strefowanie kapelusza.", 1),
    (33, 32, "Rydz rośnie pod sosnami, ma wyraźniejsze koncentryczne strefy "
             "i wolniej zielenieje.", 1),
    # smardz <-> piestrzenica
    (37, 38, "Piestrzenica ma kapelusz mózgowato pofałdowany, a nie komorowaty, "
             "i wnętrze wypełnione pofałdowaniami zamiast pustego.", 3),
    (38, 37, "Smardz ma kapelusz z regularnymi komorami i całkowicie puste wnętrze "
             "po przekrojeniu wzdłuż.", 3),
    # purchawka <-> tęgoskór i młode muchomory
    (41, 49, "Tęgoskór ma grubą, twardą, łuskowatą skórkę i wnętrze od początku "
             "ciemnofioletowe do czarnego. Purchawka ma miąższ czysto biały.", 2),
    (49, 41, "Purchawka ma cienką skórkę pokrytą kolcami i wnętrze czysto białe, "
             "dopóki jest jadalna.", 2),
    (41, 12, "Białe, jajowate owocniki znalezione w ściółce mogą być młodymi "
             "muchomorami. Przekrój wzdłuż: jeśli widać zarys kapelusza i trzonu, "
             "to muchomor, nie purchawka.", 3),
    # twardzioszek <-> lejkówka
    (27, 47, "Lejkówka jadowita ma gęste, białe, zbiegające blaszki i kruchy trzon. "
             "Twardzioszek ma blaszki rzadkie i twardy, żylasty trzon.", 3),
    (47, 27, "Twardzioszek ma rzadkie, szerokie blaszki i wybitnie twardy trzon, "
             "którego nie da się przerwać jak zwykłego grzyba.", 3),
    # płachetka <-> zasłonaki
    (44, 45, "Zasłonak rudy ma rdzawopomarańczowy, stożkowaty kapelusz z garbkiem "
             "i żółtawe pasma na trzonie. Brak białego nalotu na kapeluszu.", 3),
    (45, 44, "Płachetka ma pomarszczony ochrowy kapelusz, biały nalot u młodych "
             "owocników i wyraźny biały pierścień.", 3),
    # krowiak - najczestsze pomylki
    (50, 7, "Koźlarz ma rurki zamiast blaszek i ciemne łuseczki na trzonie.", 2),
    (50, 5, "Podgrzybek ma rurki (gąbkę) pod kapeluszem. Krowiak ma blaszki, "
            "które dają się oddzielić od kapelusza i brązowieją po dotknięciu.", 3),
    (5, 50, "Krowiak podwinięty ma blaszki zamiast rurek, silnie podwinięty brzeg "
            "kapelusza i blaszki brązowiejące po uciśnięciu. Jest śmiertelnie trujący.", 3),

    # --- uzupelnienia po weryfikacji z atlasem Snowarskiego ---
    (11, 9, "Maślak zwyczajny ma wyraźny błoniasty pierścień na trzonie. "
            "Maślak ziarnisty pierścienia nie ma, za to u młodych owocników "
            "z porów wydzielają się mleczne kropelki, a górna część trzonu "
            "pokryta jest drobnymi ziarenkami.", 1),
    (9, 11, "Maślak ziarnisty nie ma pierścienia i ma ziarenka na trzonie.", 1),

    (12, 25, "Gąska zielonka ma podobnie zielonkawy kapelusz, ale siarkowożółte "
             "blaszki i nie ma ani pierścienia, ani pochwy. Muchomor sromotnikowy "
             "ma blaszki zawsze białe, pierścień i workowatą pochwę.", 3),
    (25, 12, "Muchomor sromotnikowy ma białe blaszki, pierścień na trzonie "
             "i workowatą pochwę u podstawy. Zielonka ma siarkowożółte blaszki "
             "i nie ma żadnej z tych struktur.", 3),

    (12, 21, "Czubajka kania jest znacznie większa, ma ruchomy pierścień, "
             "wężykowaty deseń na trzonie i nie ma pochwy. Ta pomyłka wymaga "
             "całkowitej nieznajomości obu gatunków, ale bywa zgłaszana "
             "przy zatruciach.", 3),

    (21, 15, "Muchomor plamisty ma białe brodawki na brązowym kapeluszu, "
             "gładki pierścień i kołnierzyk nad bulwiastą podstawą. Kania ma "
             "odstające brązowe łuski, ruchomy pierścień i wężykowaty trzon.", 3),

    (22, 21, "Kania jest wyższa i smuklejsza, ma wężykowaty deseń na trzonie, "
             "a jej miąższ nie zmienia barwy. Czubajka gwiaździsta ma gładki "
             "trzon i miąższ wyraźnie czerwieniejący po przekrojeniu.", 1),

    (30, 39, "Kolczak obłączasty bywa łudząco podobny z wierzchu, ale pod "
             "kapeluszem ma miękkie kolce zamiast rozwidlonych fałdek. "
             "Obydwa są jadalne, więc pomyłka nie jest groźna.", 1),
    (39, 30, "Pieprznik ma grube, rozwidlone fałdki zbiegające na trzon "
             "i zapach moreli. Kolczak ma pod kapeluszem miękkie, kruche kolce.", 1),

    (51, 46, "Hełmówka obrzeżona ma trzon pod pierścieniem GŁADKI, pokryty "
             "tylko białawymi włóknami, bez łuseczek, i rośnie głównie "
             "na drewnie iglastym. Łuszczak ma trzon wyraźnie łuseczkowaty "
             "i wybiera drewno liściaste.", 3),
    (46, 51, "Łuszczak zmienny ma trzon pod pierścieniem gęsto pokryty "
             "łuseczkami i rośnie na drewnie liściastym. Hełmówka ma trzon "
             "gładki, włóknisty, i preferuje drewno iglaste.", 3),
    (51, 23, "Opieńka miodowa jest większa, ma kremowe blaszki i biały wysyp "
             "zarodników. Łuszczak ma blaszki cynamonowe i rdzawy wysyp.", 1),
    (50, 44, "Płachetka ma wyraźny biały pierścień i rdzawe blaszki, które nie "
             "dają się oddzielić od kapelusza.", 2),
    # podgrzybek <-> borowik
    (5, 1, "Borowik ma białą siateczkę na trzonie i pory, które nie sinieją. "
           "Podgrzybek nie ma siateczki, a jego pory wyraźnie niebieszczeją.", 1),
    (1, 5, "Podgrzybek nie ma siateczki na trzonie, a jego pory sinieją "
           "po naciśnięciu.", 1),
]

# ---------------------------------------------------------------------------
# Zastosowanie kulinarne - jedno zdanie dla gatunkow jadalnych i warunkowo
# jadalnych. Przy warunkowo jadalnych MUSI pojawic sie wzmianka o obrobce
# termicznej; build_db.py to sprawdza i przerywa build, jesli jej brakuje.
# ---------------------------------------------------------------------------
# species_id -> jedno zdanie o najpopularniejszym zastosowaniu kulinarnym.
KUCHNIA = {
1: "Król polskiej kuchni grzybowej — suszony na wigilijną zupę i sos, "
   "młode owocniki świetne smażone na maśle lub marynowane w occie.",
3: "Wyłącznie po dokładnym ugotowaniu (minimum 15 minut, wodę odlać) — "
   "wtedy nadaje się na duszone potrawy i sosy o wyrazistym smaku.",
5: "Najpopularniejszy grzyb na smażenie z cebulą i śmietaną, dobrze znosi "
   "też mrożenie i suszenie na zimowe zupy.",
6: "Smażony lub duszony, najlepszy w młodych owocnikach — starsze robią się "
   "wodniste i lepiej nadają się do suszenia.",
7: "Klasyk na smażone danie z cebulą, ale ciemnieje podczas obróbki; "
   "często dodawany do mieszanek grzybowych i suszony.",
8: "Smażony lub duszony; miąższ mocno czernieje podczas gotowania, "
   "co nie wpływa na smak, ale zaciemnia całą potrawę.",
9: "Przed obróbką ściąga się śluzowatą skórkę; najczęściej marynowany "
   "w occie, dobry też smażony i w zupach.",
10: "Zwykle marynowany lub dodawany do mieszanek; sam w sobie mdły, "
    "więc rzadko przyrządzany osobno.",
11: "Jak maślak zwyczajny — po zdjęciu skórki marynowany albo smażony, "
    "często razem z innymi maślakami.",
16: "Wyłącznie po dokładnym ugotowaniu; w praktyce rzadko zbierany "
    "ze względu na ryzyko pomylenia z muchomorem plamistym.",
17: "Wyłącznie po ugotowaniu, ale odradzany — łatwo pomylić z młodymi "
    "muchomorami śmiertelnie trującymi.",
18: "Smażona na maśle, duszona lub surowa w sałatkach; sprawdza się "
    "wszędzie tam, gdzie użyłbyś pieczarki ze sklepu.",
19: "Smażona lub duszona; miąższ czerwienieje podczas obróbki, "
    "co jest naturalne i nie zmienia smaku.",
21: "Kapelusze panierowane i smażone jak kotlet schabowy — to najbardziej "
    "znane zastosowanie; trzon jest twardy i się go odrzuca.",
22: "Kapelusze smażone w panierce, ale tylko po obróbce termicznej "
    "i w mniejszych ilościach — u części osób powoduje dolegliwości.",
23: "Obowiązkowe gotowanie 15–20 minut i odlanie wody; potem najlepsza "
    "marynowana w occie albo smażona z cebulą.",
26: "Smażona lub duszona; przed obróbką trzeba ją dokładnie opłukać, "
    "bo rośnie w piasku i bywa mocno zapiaszczona.",
27: "Suszony i mielony na aromatyczną przyprawę do zup i sosów; "
    "używa się wyłącznie kapeluszy, trzony są żylaste.",
28: "Smażony na patelni lub duszony, o mięsistej konsystencji; "
    "popularny jako baza dań wegetariańskich i gulaszy.",
29: "Używa się wyłącznie kapeluszy (trzon jest twardy) — do zup, "
    "sosów i dań azjatyckich, znany też jako enoki.",
30: "Smażona na maśle ze śmietaną i cebulą, klasyk polskiej kuchni; "
    "dobra też marynowana, ale nie nadaje się do suszenia.",
32: "Tradycyjnie smażony na maśle lub grillowany w całości z solą; "
    "bardzo dobry też marynowany i kiszony.",
33: "Jak rydz sosnowy — smażony lub marynowany, choć nieco gorszej "
    "jakości i wyraźniej gorzkawy.",
35: "Smażony lub duszony; jeden z niewielu gołąbków o na tyle łagodnym "
    "smaku, że nadaje się do samodzielnych dań.",
37: "Po dokładnym ugotowaniu (wodę odlać) używany do sosów śmietanowych "
    "i nadzień; w Polsce chroniony, więc głównie z hodowli lub importu.",
39: "Smażony lub duszony; u starszych owocników miąższ gorzknieje, "
    "więc zbiera się tylko młode.",
40: "Wyłącznie młode owocniki po ugotowaniu — panierowane i smażone, "
    "konsystencją przypominają kurczaka, stąd potoczna nazwa.",
41: "Młode, czysto białe w środku owocniki kroi się w plastry "
    "i smaży w panierce jak kotlety.",
42: "Tylko młode, białe owocniki, po ugotowaniu i najlepiej przyrządzone "
    "w dniu zbioru — na zupę krem lub smażone; nigdy z alkoholem.",
51: "Używa się wyłącznie kapeluszy (trzony są włókniste) — smażone "
    "lub duszone; grzyb ceniony w kuchni niemieckiej i austriackiej.",
43: "Suszony, potem namoczony — używany głównie w kuchni azjatyckiej "
    "do zup i dań smażonych, ceniony za chrupiącą konsystencję.",
44: "Smażona lub duszona; przed obróbką zdejmuje się skórkę z kapelusza, "
    "podobnie jak u maślaków.",
}
