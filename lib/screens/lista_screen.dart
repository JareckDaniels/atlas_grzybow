import 'dart:async';
import 'package:flutter/material.dart';
import '../data/db.dart';
import '../models/species.dart';
import '../widgets/common.dart';
import 'detal_screen.dart';
import 'filtry_screen.dart';
import 'klucz_screen.dart';

class ListaScreen extends StatefulWidget {
  const ListaScreen({super.key});
  @override
  State<ListaScreen> createState() => _ListaScreenState();
}

class _ListaScreenState extends State<ListaScreen> {
  final _filtry = Filtry();
  final _ctrl = TextEditingController();
  Timer? _debounce;
  List<Species> _wyniki = [];
  bool _laduje = true;

  @override
  void initState() {
    super.initState();
    _odswiez();
  }

  @override
  void dispose() {
    _debounce?.cancel();
    _ctrl.dispose();
    super.dispose();
  }

  Future<void> _odswiez() async {
    setState(() => _laduje = true);
    final r = await AtlasDb.instance.szukaj(_filtry);
    if (!mounted) return;
    setState(() {
      _wyniki = r;
      _laduje = false;
    });
  }

  void _naSzukaj(String v) {
    _debounce?.cancel();
    _debounce = Timer(const Duration(milliseconds: 250), () {
      _filtry.szukaj = v;
      _odswiez();
    });
  }

  Future<void> _otworzFiltry() async {
    final wynik = await Navigator.push<Filtry>(
      context,
      MaterialPageRoute(builder: (_) => FiltryScreen(start: _filtry.kopia())),
    );
    if (wynik == null) return;
    _filtry
      ..hymenofor = wynik.hymenofor
      ..koloryKapelusza = wynik.koloryKapelusza
      ..jadalnosc = wynik.jadalnosc
      ..siedliska = wynik.siedliska
      ..pierscien = wynik.pierscien
      ..pochwa = wynik.pochwa
      ..mleczko = wynik.mleczko
      ..sinienie = wynik.sinienie
      ..miesiac = wynik.miesiac;
    _odswiez();
  }

  Future<void> _otworzKlucz() async {
    final wynik = await Navigator.push<Filtry>(
      context,
      MaterialPageRoute(builder: (_) => const KluczScreen()),
    );
    if (wynik == null) return;
    _filtry
      ..hymenofor = wynik.hymenofor
      ..pierscien = wynik.pierscien
      ..pochwa = wynik.pochwa
      ..mleczko = wynik.mleczko
      ..koloryKapelusza = wynik.koloryKapelusza;
    _odswiez();
  }

  @override
  Widget build(BuildContext context) {
    final t = Theme.of(context);
    final aktywne = _filtry.aktywnych;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Atlas grzybów'),
        actions: [
          IconButton(
            tooltip: 'Klucz oznaczania',
            onPressed: _otworzKlucz,
            icon: const Icon(Icons.account_tree_outlined),
          ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 4, 16, 10),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _ctrl,
                    onChanged: _naSzukaj,
                    textInputAction: TextInputAction.search,
                    decoration: InputDecoration(
                      hintText: 'Nazwa polska lub łacińska…',
                      prefixIcon: const Icon(Icons.search, size: 21),
                      suffixIcon: _ctrl.text.isEmpty
                          ? null
                          : IconButton(
                              icon: const Icon(Icons.clear, size: 19),
                              onPressed: () {
                                _ctrl.clear();
                                _filtry.szukaj = '';
                                _odswiez();
                              },
                            ),
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                Badge(
                  isLabelVisible: aktywne > 0,
                  label: Text('$aktywne'),
                  child: Material(
                    color: aktywne > 0
                        ? t.colorScheme.primary
                        : Colors.white,
                    borderRadius: BorderRadius.circular(12),
                    child: InkWell(
                      borderRadius: BorderRadius.circular(12),
                      onTap: _otworzFiltry,
                      child: Container(
                        width: 48,
                        height: 48,
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(
                              color: Colors.black.withValues(alpha: 0.12)),
                        ),
                        child: Icon(Icons.tune,
                            color: aktywne > 0
                                ? Colors.white
                                : t.colorScheme.onSurfaceVariant),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 18),
            child: Row(
              children: [
                Text(
                  _laduje
                      ? 'Szukam…'
                      : '${_wyniki.length} ${_odmiana(_wyniki.length)}',
                  style: t.textTheme.bodySmall?.copyWith(
                      color: t.colorScheme.onSurfaceVariant,
                      fontWeight: FontWeight.w600),
                ),
                const Spacer(),
                if (aktywne > 0)
                  TextButton.icon(
                    onPressed: () {
                      _filtry.wyczysc();
                      _ctrl.clear();
                      _odswiez();
                    },
                    icon: const Icon(Icons.close, size: 15),
                    label: const Text('Wyczyść'),
                    style: TextButton.styleFrom(
                        padding: const EdgeInsets.symmetric(horizontal: 8),
                        visualDensity: VisualDensity.compact),
                  ),
              ],
            ),
          ),
          const SizedBox(height: 6),
          Expanded(
            child: _laduje
                ? const Center(child: CircularProgressIndicator())
                : _wyniki.isEmpty
                    ? _pusto(context)
                    : ListView.separated(
                        padding: const EdgeInsets.fromLTRB(16, 4, 16, 24),
                        itemCount: _wyniki.length,
                        separatorBuilder: (_, __) => const SizedBox(height: 10),
                        itemBuilder: (_, i) => KartaGatunku(
                          s: _wyniki[i],
                          onTap: () => Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => DetalScreen(id: _wyniki[i].id),
                            ),
                          ),
                        ),
                      ),
          ),
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

  Widget _pusto(BuildContext context) {
    final t = Theme.of(context);
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.search_off,
                size: 44, color: t.colorScheme.outline),
            const SizedBox(height: 14),
            Text('Brak gatunków dla tych kryteriów',
                style: t.textTheme.titleMedium),
            const SizedBox(height: 6),
            Text(
              'Spróbuj usunąć część filtrów — grzyby bywają zmienne, '
              'a barwa kapelusza zależy od wieku i wilgotności.',
              textAlign: TextAlign.center,
              style: t.textTheme.bodySmall
                  ?.copyWith(color: t.colorScheme.onSurfaceVariant),
            ),
          ],
        ),
      ),
    );
  }
}
