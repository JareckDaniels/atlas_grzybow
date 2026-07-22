import 'package:flutter/material.dart';
import '../data/db.dart';
import '../models/species.dart';
import '../widgets/common.dart';
import 'detal_screen.dart';
import 'slowniczek_screen.dart';

class _Pytanie {
  final String tekst;
  final String? podpowiedz;
  final List<(String etykieta, void Function(Filtry) zastosuj)> odpowiedzi;
  final bool Function(Filtry) dotyczy;

  const _Pytanie({
    required this.tekst,
    this.podpowiedz,
    required this.odpowiedzi,
    required this.dotyczy,
  });
}

class KluczScreen extends StatefulWidget {
  const KluczScreen({super.key});
  @override
  State<KluczScreen> createState() => _KluczScreenState();
}

class _KluczScreenState extends State<KluczScreen> {
  final _f = Filtry();
  final _historia = <Filtry>[];
  int _pozostalo = 0;
  List<Species> _wyniki = [];
  bool _laduje = true;

  late final List<_Pytanie> _pytania = [
    _Pytanie(
      tekst: 'Co widzisz pod kapeluszem?',
      podpowiedz: 'Przekrój lub delikatnie oderwij fragment kapelusza.',
      dotyczy: (f) => f.hymenofor.isEmpty,
      odpowiedzi: [
        ('Blaszki', (f) => f.hymenofor = {Hymenofor.blaszki}),
        ('Rurki, jak gąbka', (f) => f.hymenofor = {Hymenofor.rurki}),
        ('Kolce', (f) => f.hymenofor = {Hymenofor.kolce}),
        ('Gładki spód', (f) => f.hymenofor = {Hymenofor.gladki}),
        ('Fałdki', (f) => f.hymenofor = {Hymenofor.fadki}),
      ],
    ),
    _Pytanie(
      tekst: 'Czy u podstawy trzonu jest pochwa?',
      podpowiedz:
          'Wykop grzyb w całości. Pochwa to workowata osłona, często ukryta '
          'w ściółce — jej obecność to sygnał ostrzegawczy.',
      dotyczy: (f) =>
          f.pochwa == null && f.hymenofor.contains(Hymenofor.blaszki),
      odpowiedzi: [
        ('Tak, jest pochwa', (f) => f.pochwa = true),
        ('Nie ma pochwy', (f) => f.pochwa = false),
      ],
    ),
    _Pytanie(
      tekst: 'Czy na trzonie jest pierścień?',
      podpowiedz: 'Kołnierzyk lub obrączka w górnej części trzonu.',
      dotyczy: (f) => f.pierscien == null,
      odpowiedzi: [
        ('Tak, jest pierścień', (f) => f.pierscien = true),
        ('Nie ma pierścienia', (f) => f.pierscien = false),
      ],
    ),
    _Pytanie(
      tekst: 'Czy po przecięciu wypływa mleczko?',
      podpowiedz: 'Naciąć blaszki lub miąższ i odczekać kilkanaście sekund.',
      dotyczy: (f) =>
          f.mleczko == null && f.hymenofor.contains(Hymenofor.blaszki),
      odpowiedzi: [
        ('Tak, wypływa', (f) => f.mleczko = true),
        ('Nie', (f) => f.mleczko = false),
      ],
    ),
    _Pytanie(
      tekst: 'Czy miąższ sinieje po przekrojeniu?',
      podpowiedz: 'Obserwuj przekrój przez 1–2 minuty.',
      dotyczy: (f) =>
          f.sinienie == null && f.hymenofor.contains(Hymenofor.rurki),
      odpowiedzi: [
        ('Tak, sinieje', (f) => f.sinienie = true),
        ('Nie zmienia barwy', (f) => f.sinienie = false),
      ],
    ),
    _Pytanie(
      tekst: 'Jaka jest dominująca barwa kapelusza?',
      dotyczy: (f) => f.koloryKapelusza.isEmpty,
      odpowiedzi: [
        ('Biały lub kremowy',
            (f) => f.koloryKapelusza = {'bialy', 'kremowy'}),
        ('Brązowy', (f) => f.koloryKapelusza = {'brazowy', 'ciemnobrazowy', 'rudy'}),
        ('Żółty lub pomarańczowy',
            (f) => f.koloryKapelusza = {'zolty', 'pomaranczowy'}),
        ('Czerwony', (f) => f.koloryKapelusza = {'czerwony'}),
        ('Zielonkawy lub oliwkowy',
            (f) => f.koloryKapelusza = {'zielonkawy', 'oliwkowy'}),
        ('Szary lub czarny', (f) => f.koloryKapelusza = {'szary', 'czarny'}),
      ],
    ),
  ];

  @override
  void initState() {
    super.initState();
    _przelicz();
  }

  Future<void> _przelicz() async {
    setState(() => _laduje = true);
    final n = await AtlasDb.instance.policz(_f);
    final w = n <= 8 ? await AtlasDb.instance.szukaj(_f) : <Species>[];
    if (!mounted) return;
    setState(() {
      _pozostalo = n;
      _wyniki = w;
      _laduje = false;
    });
  }

  _Pytanie? get _aktualne {
    for (final p in _pytania) {
      if (p.dotyczy(_f)) return p;
    }
    return null;
  }

  void _odpowiedz(void Function(Filtry) zastosuj) {
    _historia.add(_f.kopia());
    zastosuj(_f);
    _przelicz();
  }

  void _cofnij() {
    if (_historia.isEmpty) return;
    final poprzedni = _historia.removeLast();
    _f
      ..hymenofor = poprzedni.hymenofor
      ..koloryKapelusza = poprzedni.koloryKapelusza
      ..pierscien = poprzedni.pierscien
      ..pochwa = poprzedni.pochwa
      ..mleczko = poprzedni.mleczko
      ..sinienie = poprzedni.sinienie;
    _przelicz();
  }

  @override
  Widget build(BuildContext context) {
    final t = Theme.of(context);
    final pytanie = _aktualne;
    final koniec = pytanie == null || _pozostalo <= 8;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Klucz oznaczania'),
        leading: IconButton(
          icon: const Icon(Icons.close),
          onPressed: () => Navigator.pop(context),
        ),
        actions: [
          IconButton(
            tooltip: 'Słowniczek pojęć',
            icon: const Icon(Icons.menu_book_outlined),
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const SlowniczekScreen()),
            ),
          ),
          if (_historia.isNotEmpty)
            IconButton(
              tooltip: 'Cofnij',
              icon: const Icon(Icons.undo),
              onPressed: _cofnij,
            ),
        ],
      ),
      body: _laduje
          ? const Center(child: CircularProgressIndicator())
          : ListView(
              padding: const EdgeInsets.fromLTRB(20, 8, 20, 32),
              children: [
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                  decoration: BoxDecoration(
                    color: t.colorScheme.primary.withValues(alpha: 0.09),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Row(
                    children: [
                      Icon(Icons.filter_alt_outlined,
                          size: 18, color: t.colorScheme.primary),
                      const SizedBox(width: 9),
                      Text('Pozostało $_pozostalo ${_odmiana(_pozostalo)}',
                          style: t.textTheme.bodyMedium?.copyWith(
                              fontWeight: FontWeight.w600,
                              color: t.colorScheme.primary)),
                    ],
                  ),
                ),
                const SizedBox(height: 24),
                if (!koniec) ...[
                  Text(pytanie.tekst,
                      style: t.textTheme.headlineSmall
                          ?.copyWith(fontWeight: FontWeight.w700, height: 1.3)),
                  if (pytanie.podpowiedz != null) ...[
                    const SizedBox(height: 8),
                    Text(pytanie.podpowiedz!,
                        style: t.textTheme.bodySmall?.copyWith(
                            color: t.colorScheme.onSurfaceVariant,
                            height: 1.45)),
                  ],
                  const SizedBox(height: 20),
                  ...pytanie.odpowiedzi.map((o) => Padding(
                        padding: const EdgeInsets.only(bottom: 10),
                        child: SizedBox(
                          width: double.infinity,
                          child: OutlinedButton(
                            onPressed: () => _odpowiedz(o.$2),
                            style: OutlinedButton.styleFrom(
                              padding: const EdgeInsets.symmetric(
                                  vertical: 16, horizontal: 18),
                              alignment: Alignment.centerLeft,
                              shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(12)),
                            ),
                            child: Text(o.$1,
                                style: const TextStyle(
                                    fontSize: 15.5,
                                    fontWeight: FontWeight.w500)),
                          ),
                        ),
                      )),
                  const SizedBox(height: 8),
                  TextButton(
                    onPressed: () => Navigator.pop(context, _f),
                    child: const Text('Pokaż wyniki teraz'),
                  ),
                ] else ...[
                  Text(
                      _pozostalo == 0
                          ? 'Brak dopasowania'
                          : 'Możliwe gatunki',
                      style: t.textTheme.headlineSmall
                          ?.copyWith(fontWeight: FontWeight.w700)),
                  const SizedBox(height: 8),
                  Text(
                    _pozostalo == 0
                        ? 'Żaden gatunek w atlasie nie pasuje do tego zestawu cech. '
                            'Cofnij ostatnią odpowiedź — barwy i cechy bywają '
                            'mylące u starszych owocników.'
                        : 'Porównaj cechy rozstrzygające na kartach gatunków. '
                            'Zwróć szczególną uwagę na sekcję „Można pomylić z".',
                    style: t.textTheme.bodyMedium?.copyWith(
                        color: t.colorScheme.onSurfaceVariant, height: 1.5),
                  ),
                  const SizedBox(height: 18),
                  ..._wyniki.map((s) => Padding(
                        padding: const EdgeInsets.only(bottom: 10),
                        child: KartaGatunku(
                          s: s,
                          onTap: () => Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (_) => DetalScreen(id: s.id)),
                          ),
                        ),
                      )),
                  const SizedBox(height: 10),
                  if (_historia.isNotEmpty)
                    SizedBox(
                      width: double.infinity,
                      child: OutlinedButton.icon(
                        onPressed: _cofnij,
                        icon: const Icon(Icons.undo, size: 18),
                        label: const Text('Cofnij ostatnią odpowiedź'),
                        style: OutlinedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 14),
                          shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12)),
                        ),
                      ),
                    ),
                ],
              ],
            ),
    );
  }

  String _odmiana(int n) {
    if (n == 1) return 'gatunek';
    final r100 = n % 100, r10 = n % 10;
    if (r100 >= 12 && r100 <= 14) return 'gatunków';
    if (r10 >= 2 && r10 <= 4) return 'gatunki';
    return 'gatunków';
  }
}
