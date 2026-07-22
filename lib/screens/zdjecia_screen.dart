import 'package:flutter/material.dart';
import '../data/photo_manager.dart';

class ZdjeciaScreen extends StatefulWidget {
  const ZdjeciaScreen({super.key});
  @override
  State<ZdjeciaScreen> createState() => _ZdjeciaScreenState();
}

class _ZdjeciaScreenState extends State<ZdjeciaScreen> {
  PostepPobierania _postep = const PostepPobierania(StanPobierania.nieznany);
  bool _trwa = false;
  int _rozmiar = 0;
  bool _pobrane = false;

  @override
  void initState() {
    super.initState();
    _odswiez();
  }

  Future<void> _odswiez() async {
    final p = await PhotoManager.instance.czyPobrane();
    final r = await PhotoManager.instance.rozmiarNaDysku();
    if (!mounted) return;
    setState(() {
      _pobrane = p;
      _rozmiar = r;
    });
  }

  Future<void> _pobierz() async {
    setState(() => _trwa = true);
    await for (final p in PhotoManager.instance.pobierz()) {
      if (!mounted) return;
      setState(() => _postep = p);
    }
    if (!mounted) return;
    setState(() => _trwa = false);
    await _odswiez();
  }

  Future<void> _usun() async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (c) => AlertDialog(
        title: const Text('Usunąć zdjęcia?'),
        content: const Text(
            'Zwolni to miejsce na urządzeniu. Opisy, filtry i klucz '
            'będą działać dalej. Zdjęcia można pobrać ponownie.'),
        actions: [
          TextButton(
              onPressed: () => Navigator.pop(c, false),
              child: const Text('Anuluj')),
          FilledButton(
              onPressed: () => Navigator.pop(c, true),
              child: const Text('Usuń')),
        ],
      ),
    );
    if (ok != true) return;
    await PhotoManager.instance.usun();
    await _odswiez();
  }

  @override
  Widget build(BuildContext context) {
    final t = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Zdjęcia')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 12, 20, 28),
        children: [
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(14),
              border: Border.all(color: Colors.black.withValues(alpha: 0.08)),
            ),
            child: Row(
              children: [
                Icon(
                  _pobrane ? Icons.check_circle : Icons.photo_library_outlined,
                  color: _pobrane
                      ? const Color(0xFF2E7D32)
                      : t.colorScheme.onSurfaceVariant,
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(_pobrane ? 'Zdjęcia pobrane' : 'Brak zdjęć',
                          style: t.textTheme.titleSmall
                              ?.copyWith(fontWeight: FontWeight.w700)),
                      const SizedBox(height: 2),
                      Text(
                        _pobrane
                            ? 'Zajmują ${(_rozmiar / 1048576).toStringAsFixed(1)} MB'
                            : 'Karty gatunków pokazują symbole zastępcze',
                        style: t.textTheme.bodySmall?.copyWith(
                            color: t.colorScheme.onSurfaceVariant),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 18),
          if (_postep.komunikat != null && !_trwa)
            Padding(
              padding: const EdgeInsets.only(bottom: 16),
              child: Container(
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  color: _postep.stan == StanPobierania.blad
                      ? t.colorScheme.error.withValues(alpha: 0.08)
                      : t.colorScheme.surfaceContainerHighest,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(_postep.komunikat!,
                    style: const TextStyle(fontSize: 13.5, height: 1.45)),
              ),
            ),
          if (_trwa) ...[
            ClipRRect(
              borderRadius: BorderRadius.circular(8),
              child: LinearProgressIndicator(
                value: _postep.postep >= 0 ? _postep.postep : null,
                minHeight: 8,
              ),
            ),
            const SizedBox(height: 10),
            Text(_postep.komunikat ?? 'Pracuję…',
                style: t.textTheme.bodySmall
                    ?.copyWith(color: t.colorScheme.onSurfaceVariant)),
            const SizedBox(height: 18),
          ],
          if (!_trwa)
            SizedBox(
              width: double.infinity,
              child: FilledButton.icon(
                onPressed: _pobierz,
                icon: Icon(_pobrane ? Icons.refresh : Icons.download),
                label: Text(_pobrane
                    ? 'Sprawdź aktualizacje'
                    : 'Pobierz zdjęcia'),
                style: FilledButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 15),
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12)),
                ),
              ),
            ),
          if (!_trwa && _pobrane) ...[
            const SizedBox(height: 8),
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                onPressed: _usun,
                icon: const Icon(Icons.delete_outline, size: 19),
                label: const Text('Usuń zdjęcia'),
                style: OutlinedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 15),
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12)),
                ),
              ),
            ),
          ],
          const SizedBox(height: 24),
          Text(
            'Zdjęcia pobierane są raz i działają później bez internetu. '
            'Pochodzą z Wikimedia Commons na licencjach dopuszczających '
            'rozpowszechnianie; autorzy i licencje zapisane są przy każdym pliku.',
            style: t.textTheme.bodySmall
                ?.copyWith(color: t.colorScheme.outline, height: 1.5),
          ),
        ],
      ),
    );
  }
}
