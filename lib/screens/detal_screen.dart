import 'package:flutter/material.dart';
import '../data/db.dart';
import '../models/species.dart';
import '../widgets/common.dart';

class DetalScreen extends StatefulWidget {
  final int id;
  const DetalScreen({super.key, required this.id});

  @override
  State<DetalScreen> createState() => _DetalScreenState();
}

class _DetalScreenState extends State<DetalScreen> {
  Species? _s;
  List<Lookalike> _sobowtory = [];
  bool _laduje = true;
  final _pageCtrl = PageController();
  int _strona = 0;

  @override
  void initState() {
    super.initState();
    _wczytaj();
  }

  @override
  void dispose() {
    _pageCtrl.dispose();
    super.dispose();
  }

  Future<void> _wczytaj() async {
    final s = await AtlasDb.instance.gatunek(widget.id);
    final l = await AtlasDb.instance.sobowtory(widget.id);
    if (!mounted) return;
    setState(() {
      _s = s;
      _sobowtory = l;
      _laduje = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_laduje || _s == null) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }
    final s = _s!;
    final t = Theme.of(context);

    return Scaffold(
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 260,
            pinned: true,
            flexibleSpace: FlexibleSpaceBar(
              background: Stack(
                fit: StackFit.expand,
                children: [
                  if (s.zdjecia.isEmpty)
                    const ZdjecieGatunku(null)
                  else
                    PageView.builder(
                      controller: _pageCtrl,
                      itemCount: s.zdjecia.length,
                      onPageChanged: (i) => setState(() => _strona = i),
                      itemBuilder: (_, i) => ZdjecieGatunku(s.zdjecia[i]),
                    ),
                  Positioned(
                    left: 0,
                    right: 0,
                    bottom: 0,
                    child: Container(
                      height: 70,
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          begin: Alignment.bottomCenter,
                          end: Alignment.topCenter,
                          colors: [
                            Colors.black.withValues(alpha: 0.5),
                            Colors.transparent
                          ],
                        ),
                      ),
                    ),
                  ),
                  if (s.zdjecia.length > 1)
                    Positioned(
                      bottom: 10,
                      left: 0,
                      right: 0,
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: List.generate(
                          s.zdjecia.length,
                          (i) => Container(
                            width: 6,
                            height: 6,
                            margin: const EdgeInsets.symmetric(horizontal: 3),
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              color: i == _strona
                                  ? Colors.white
                                  : Colors.white.withValues(alpha: 0.45),
                            ),
                          ),
                        ),
                      ),
                    ),
                ],
              ),
            ),
          ),
          SliverToBoxAdapter(child: OstrzezenieBaner(s.jadalnosc)),
          SliverPadding(
            padding: const EdgeInsets.fromLTRB(18, 18, 18, 32),
            sliver: SliverList(
              delegate: SliverChildListDelegate([
                Text(s.nazwaPl,
                    style: t.textTheme.headlineSmall
                        ?.copyWith(fontWeight: FontWeight.w800)),
                const SizedBox(height: 2),
                Text(s.nazwaLac,
                    style: t.textTheme.titleSmall?.copyWith(
                        fontStyle: FontStyle.italic,
                        color: t.colorScheme.onSurfaceVariant)),
                if (s.synonimyPl != null && s.synonimyPl!.isNotEmpty) ...[
                  const SizedBox(height: 3),
                  Text('zwany też: ${s.synonimyPl}',
                      style: t.textTheme.bodySmall
                          ?.copyWith(color: t.colorScheme.outline)),
                ],
                const SizedBox(height: 12),
                BadgeJadalnosc(s.jadalnosc),
                if (s.cechyKluczowe != null) ...[
                  const SizedBox(height: 18),
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: t.colorScheme.primary.withValues(alpha: 0.07),
                      borderRadius: BorderRadius.circular(14),
                      border: Border.all(
                          color:
                              t.colorScheme.primary.withValues(alpha: 0.22)),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(children: [
                          Icon(Icons.key_outlined,
                              size: 17, color: t.colorScheme.primary),
                          const SizedBox(width: 7),
                          Text('Cechy rozstrzygające',
                              style: t.textTheme.labelLarge?.copyWith(
                                  color: t.colorScheme.primary,
                                  fontWeight: FontWeight.w700)),
                        ]),
                        const SizedBox(height: 7),
                        Text(s.cechyKluczowe!,
                            style: const TextStyle(height: 1.45, fontSize: 14)),
                      ],
                    ),
                  ),
                ],
                if (s.opis != null) ...[
                  const SizedBox(height: 20),
                  Text('Opis', style: _naglowek(t)),
                  const SizedBox(height: 7),
                  Text(s.opis!,
                      style: const TextStyle(height: 1.55, fontSize: 14.5)),
                ],
                const SizedBox(height: 22),
                Text('Cechy morfologiczne', style: _naglowek(t)),
                const SizedBox(height: 10),
                _tabela(t, [
                  ('Spód kapelusza', s.hymenofor.etykieta),
                  ('Kształt kapelusza', s.ksztaltKapelusza ?? '—'),
                  ('Powierzchnia', s.powierzchnia ?? '—'),
                  ('Barwa kapelusza',
                      s.kolorowKapelusza.isEmpty
                          ? '—'
                          : s.kolorowKapelusza.join(', ')),
                  ('Pierścień', s.pierscien ? 'obecny' : 'brak'),
                  ('Pochwa', s.pochwa ? 'obecna' : 'brak'),
                  ('Mleczko', s.mleczko ? 'wypływa' : 'brak'),
                  ('Sinienie', s.sinienie ? 'sinieje' : 'nie sinieje'),
                  ('Wysyp zarodników', s.wysypZarnikow ?? '—'),
                  ('Zapach', s.zapach ?? '—'),
                  ('Smak', s.smak ?? '—'),
                  ('Sezon', s.sezon),
                  ('Rodzina', s.rodzina ?? '—'),
                ]),
                if (s.siedliska.isNotEmpty) ...[
                  const SizedBox(height: 22),
                  Text('Siedlisko', style: _naglowek(t)),
                  const SizedBox(height: 9),
                  Wrap(
                    spacing: 7,
                    runSpacing: 7,
                    children: s.siedliska
                        .map((x) => Chip(
                              label: Text(x),
                              visualDensity: VisualDensity.compact,
                            ))
                        .toList(),
                  ),
                ],
                if (_sobowtory.isNotEmpty) ...[
                  const SizedBox(height: 24),
                  Row(children: [
                    const Icon(Icons.compare_arrows, size: 19),
                    const SizedBox(width: 7),
                    Text('Można pomylić z', style: _naglowek(t)),
                  ]),
                  const SizedBox(height: 10),
                  ..._sobowtory.map(_kartaSobowtora),
                ],
                if (s.uwagi != null) ...[
                  const SizedBox(height: 22),
                  Container(
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: t.colorScheme.surfaceContainerHighest,
                      borderRadius: BorderRadius.circular(14),
                    ),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Icon(Icons.info_outline,
                            size: 18, color: t.colorScheme.onSurfaceVariant),
                        const SizedBox(width: 10),
                        Expanded(
                          child: Text(s.uwagi!,
                              style: const TextStyle(
                                  height: 1.45, fontSize: 13.5)),
                        ),
                      ],
                    ),
                  ),
                ],
                const SizedBox(height: 24),
                Text(
                  'Oznaczenie na podstawie zdjęć nie jest wystarczające do '
                  'spożycia grzyba. W razie wątpliwości skonsultuj się '
                  'z grzyboznawcą.',
                  style: t.textTheme.bodySmall
                      ?.copyWith(color: t.colorScheme.outline, height: 1.4),
                ),
              ]),
            ),
          ),
        ],
      ),
    );
  }

  TextStyle? _naglowek(ThemeData t) => t.textTheme.titleMedium
      ?.copyWith(fontWeight: FontWeight.w700, letterSpacing: 0.1);

  Widget _tabela(ThemeData t, List<(String, String)> wiersze) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: Colors.black.withValues(alpha: 0.07)),
      ),
      child: Column(
        children: [
          for (var i = 0; i < wiersze.length; i++) ...[
            Padding(
              padding:
                  const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  SizedBox(
                    width: 130,
                    child: Text(wiersze[i].$1,
                        style: t.textTheme.bodySmall?.copyWith(
                            color: t.colorScheme.onSurfaceVariant)),
                  ),
                  Expanded(
                    child: Text(wiersze[i].$2,
                        style: const TextStyle(
                            fontSize: 13.5, fontWeight: FontWeight.w500)),
                  ),
                ],
              ),
            ),
            if (i < wiersze.length - 1) const Divider(height: 1),
          ],
        ],
      ),
    );
  }

  Widget _kartaSobowtora(Lookalike l) {
    final t = Theme.of(context);
    final krytyczny = l.waga >= 3;
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Container(
        decoration: BoxDecoration(
          color: krytyczny
              ? const Color(0xFFB71C1C).withValues(alpha: 0.05)
              : Colors.white,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(
            color: krytyczny
                ? const Color(0xFFB71C1C).withValues(alpha: 0.3)
                : Colors.black.withValues(alpha: 0.08),
          ),
        ),
        child: InkWell(
          borderRadius: BorderRadius.circular(14),
          onTap: () => Navigator.push(
            context,
            MaterialPageRoute(
                builder: (_) => DetalScreen(id: l.gatunek.id)),
          ),
          child: Padding(
            padding: const EdgeInsets.all(12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    ZdjecieGatunku(
                      l.gatunek.zdjecia.isEmpty
                          ? null
                          : l.gatunek.zdjecia.first,
                      width: 52,
                      height: 52,
                      radius: BorderRadius.circular(10),
                    ),
                    const SizedBox(width: 11),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(l.gatunek.nazwaPl,
                              style: t.textTheme.titleSmall
                                  ?.copyWith(fontWeight: FontWeight.w700)),
                          const SizedBox(height: 4),
                          BadgeJadalnosc(l.gatunek.jadalnosc, maly: true),
                        ],
                      ),
                    ),
                    Icon(Icons.chevron_right,
                        color: t.colorScheme.outline, size: 20),
                  ],
                ),
                const SizedBox(height: 11),
                if (krytyczny)
                  Padding(
                    padding: const EdgeInsets.only(bottom: 7),
                    child: Row(children: [
                      const Icon(Icons.priority_high,
                          size: 15, color: Color(0xFFB71C1C)),
                      const SizedBox(width: 5),
                      Text('POMYŁKA MOŻE BYĆ ŚMIERTELNA',
                          style: t.textTheme.labelSmall?.copyWith(
                              color: const Color(0xFFB71C1C),
                              fontWeight: FontWeight.w800,
                              letterSpacing: 0.3)),
                    ]),
                  ),
                Text(l.roznice,
                    style: const TextStyle(height: 1.45, fontSize: 13.5)),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
