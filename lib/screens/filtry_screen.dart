import 'package:flutter/material.dart';
import '../data/db.dart';
import '../models/species.dart';

class FiltryScreen extends StatefulWidget {
  final Filtry start;
  const FiltryScreen({super.key, required this.start});

  @override
  State<FiltryScreen> createState() => _FiltryScreenState();
}

class _FiltryScreenState extends State<FiltryScreen> {
  late Filtry _f;
  int _trafienia = 0;
  List<({String nazwa, String? hex})> _kolory = [];
  List<String> _siedliska = [];

  static const _miesiace = [
    'sty', 'lut', 'mar', 'kwi', 'maj', 'cze',
    'lip', 'sie', 'wrz', 'paź', 'lis', 'gru'
  ];

  @override
  void initState() {
    super.initState();
    _f = widget.start;
    _wczytaj();
  }

  Future<void> _wczytaj() async {
    final k = await AtlasDb.instance.kolory();
    final s = await AtlasDb.instance.siedliska();
    if (!mounted) return;
    setState(() {
      _kolory = k;
      _siedliska = s;
    });
    _przelicz();
  }

  Future<void> _przelicz() async {
    final n = await AtlasDb.instance.policz(_f);
    if (mounted) setState(() => _trafienia = n);
  }

  void _zmien(VoidCallback fn) {
    setState(fn);
    _przelicz();
  }

  @override
  Widget build(BuildContext context) {
    final t = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Filtry'),
        actions: [
          TextButton(
            onPressed: () => _zmien(() => _f.wyczysc()),
            child: const Text('Wyczyść'),
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 8, 16, 100),
        children: [
          _sekcja(
            'Spód kapelusza',
            'Najważniejsza cecha — decyduje o całej grupie grzybów.',
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: Hymenofor.values.map((h) {
                return FilterChip(
                  label: Text(h.etykieta),
                  selected: _f.hymenofor.contains(h),
                  onSelected: (v) => _zmien(() =>
                      v ? _f.hymenofor.add(h) : _f.hymenofor.remove(h)),
                );
              }).toList(),
            ),
          ),
          _sekcja(
            'Barwa kapelusza',
            'Barwa bywa zmienna — zaznacz kilka odcieni, jeśli masz wątpliwość.',
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: _kolory.map((k) {
                final wybrany = _f.koloryKapelusza.contains(k.nazwa);
                return FilterChip(
                  avatar: CircleAvatar(
                    radius: 8,
                    backgroundColor: _hex(k.hex),
                  ),
                  label: Text(_ladnie(k.nazwa)),
                  selected: wybrany,
                  onSelected: (v) => _zmien(() => v
                      ? _f.koloryKapelusza.add(k.nazwa)
                      : _f.koloryKapelusza.remove(k.nazwa)),
                );
              }).toList(),
            ),
          ),
          _sekcja(
            'Cechy trzonu i miąższu',
            null,
            Column(
              children: [
                _trojstan('Pierścień na trzonie', _f.pierscien,
                    (v) => _zmien(() => _f.pierscien = v)),
                _trojstan('Pochwa u podstawy', _f.pochwa,
                    (v) => _zmien(() => _f.pochwa = v)),
                _trojstan('Wypływa mleczko', _f.mleczko,
                    (v) => _zmien(() => _f.mleczko = v)),
                _trojstan('Sinieje po przekrojeniu', _f.sinienie,
                    (v) => _zmien(() => _f.sinienie = v)),
              ],
            ),
          ),
          _sekcja(
            'Jadalność',
            null,
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: Jadalnosc.values.map((j) {
                final sel = _f.jadalnosc.contains(j);
                return FilterChip(
                  avatar: Icon(j.ikona, size: 16, color: j.kolor),
                  label: Text(j.etykieta),
                  selected: sel,
                  selectedColor: j.kolor.withValues(alpha: 0.16),
                  onSelected: (v) => _zmien(() =>
                      v ? _f.jadalnosc.add(j) : _f.jadalnosc.remove(j)),
                );
              }).toList(),
            ),
          ),
          _sekcja(
            'Siedlisko',
            null,
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: _siedliska.map((s) {
                return FilterChip(
                  label: Text(s),
                  selected: _f.siedliska.contains(s),
                  onSelected: (v) => _zmien(
                      () => v ? _f.siedliska.add(s) : _f.siedliska.remove(s)),
                );
              }).toList(),
            ),
          ),
          _sekcja(
            'Miesiąc',
            null,
            Wrap(
              spacing: 6,
              runSpacing: 6,
              children: List.generate(12, (i) {
                final m = i + 1;
                return FilterChip(
                  label: Text(_miesiace[i]),
                  selected: _f.miesiac == m,
                  onSelected: (v) =>
                      _zmien(() => _f.miesiac = v ? m : null),
                );
              }),
            ),
          ),
        ],
      ),
      bottomNavigationBar: SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 8, 16, 12),
          child: FilledButton(
            onPressed: _trafienia == 0
                ? null
                : () => Navigator.pop(context, _f),
            style: FilledButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12)),
            ),
            child: Text(_trafienia == 0
                ? 'Brak dopasowań'
                : 'Pokaż $_trafienia ${_odmiana(_trafienia)}'),
          ),
        ),
      ),
    );
  }

  Widget _sekcja(String tytul, String? podtytul, Widget child) {
    final t = Theme.of(context);
    return Padding(
      padding: const EdgeInsets.only(bottom: 22),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(tytul,
              style: t.textTheme.titleSmall?.copyWith(
                  fontWeight: FontWeight.w700, letterSpacing: 0.1)),
          if (podtytul != null) ...[
            const SizedBox(height: 3),
            Text(podtytul,
                style: t.textTheme.bodySmall
                    ?.copyWith(color: t.colorScheme.onSurfaceVariant)),
          ],
          const SizedBox(height: 10),
          child,
        ],
      ),
    );
  }

  /// tak / nie / bez znaczenia
  Widget _trojstan(String etykieta, bool? wartosc, ValueChanged<bool?> onZmiana) {
    final t = Theme.of(context);
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        children: [
          Expanded(
              child: Text(etykieta, style: t.textTheme.bodyMedium)),
          SegmentedButton<int>(
            style: SegmentedButton.styleFrom(
              visualDensity: VisualDensity.compact,
              padding: const EdgeInsets.symmetric(horizontal: 10),
            ),
            segments: const [
              ButtonSegment(value: 0, label: Text('—')),
              ButtonSegment(value: 1, label: Text('tak')),
              ButtonSegment(value: 2, label: Text('nie')),
            ],
            selected: {wartosc == null ? 0 : (wartosc ? 1 : 2)},
            onSelectionChanged: (s) {
              final v = s.first;
              onZmiana(v == 0 ? null : v == 1);
            },
          ),
        ],
      ),
    );
  }

  Color _hex(String? h) {
    if (h == null || !h.startsWith('#')) return Colors.grey;
    return Color(int.parse('FF${h.substring(1)}', radix: 16));
  }

  String _ladnie(String s) =>
      s[0].toUpperCase() + s.substring(1).replaceAll('_', ' ');

  String _odmiana(int n) {
    if (n == 1) return 'gatunek';
    final r100 = n % 100, r10 = n % 10;
    if (r100 >= 12 && r100 <= 14) return 'gatunków';
    if (r10 >= 2 && r10 <= 4) return 'gatunki';
    return 'gatunków';
  }
}
