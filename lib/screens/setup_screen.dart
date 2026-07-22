import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../data/photo_manager.dart';
import 'lista_screen.dart';

class SetupScreen extends StatefulWidget {
  const SetupScreen({super.key});
  @override
  State<SetupScreen> createState() => _SetupScreenState();
}

class _SetupScreenState extends State<SetupScreen> {
  int _krok = 0; // 0 = disclaimer, 1 = pobieranie
  PostepPobierania _postep =
      const PostepPobierania(StanPobierania.nieznany);
  bool _pobieranieTrwa = false;

  @override
  void initState() {
    super.initState();
    _wczytajKrok();
  }

  Future<void> _wczytajKrok() async {
    final prefs = await SharedPreferences.getInstance();
    if ((prefs.getBool('disclaimer_ok') ?? false) && mounted) {
      setState(() => _krok = 1);
    }
  }

  Future<void> _akceptuj() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('disclaimer_ok', true);
    if (mounted) setState(() => _krok = 1);
  }

  Future<void> _pobierz() async {
    setState(() => _pobieranieTrwa = true);
    await for (final p in PhotoManager.instance.pobierz()) {
      if (!mounted) return;
      setState(() => _postep = p);
    }
    if (!mounted) return;
    setState(() => _pobieranieTrwa = false);
    if (_postep.stan == StanPobierania.gotowe) _wejdz();
  }

  void _wejdz() {
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(builder: (_) => const ListaScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: _krok == 0 ? _disclaimer(context) : _pobieranie(context),
      ),
    );
  }

  Widget _disclaimer(BuildContext context) {
    final t = Theme.of(context);
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const SizedBox(height: 24),
          Icon(Icons.eco_outlined, size: 52, color: t.colorScheme.primary),
          const SizedBox(height: 20),
          Text('Atlas grzybów',
              style: t.textTheme.headlineMedium
                  ?.copyWith(fontWeight: FontWeight.w800)),
          const SizedBox(height: 6),
          Text('Przewodnik po grzybach Polski',
              style: t.textTheme.bodyLarge
                  ?.copyWith(color: t.colorScheme.onSurfaceVariant)),
          const SizedBox(height: 28),
          Expanded(
            child: SingleChildScrollView(
              child: Container(
                padding: const EdgeInsets.all(18),
                decoration: BoxDecoration(
                  color: const Color(0xFFB71C1C).withValues(alpha: 0.07),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(
                      color: const Color(0xFFB71C1C).withValues(alpha: 0.25)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(children: [
                      const Icon(Icons.warning_amber_rounded,
                          color: Color(0xFFB71C1C)),
                      const SizedBox(width: 10),
                      Text('Przeczytaj przed użyciem',
                          style: t.textTheme.titleMedium?.copyWith(
                              fontWeight: FontWeight.w700,
                              color: const Color(0xFFB71C1C))),
                    ]),
                    const SizedBox(height: 14),
                    const Text(
                      'Ta aplikacja ma charakter wyłącznie edukacyjny i nie zastępuje '
                      'oceny doświadczonego grzybiarza ani grzyboznawcy.\n\n'
                      'Nigdy nie spożywaj grzyba, którego oznaczenie opiera się '
                      'wyłącznie na podobieństwie do zdjęcia. Wiele gatunków '
                      'śmiertelnie trujących wygląda niemal identycznie jak jadalne, '
                      'a cechy rozstrzygające bywają ukryte w ściółce lub widoczne '
                      'dopiero po przekrojeniu owocnika.\n\n'
                      'W razie wątpliwości skorzystaj z bezpłatnej porady grzyboznawcy '
                      'w stacji sanitarno-epidemiologicznej.\n\n'
                      'Przy podejrzeniu zatrucia grzybami zadzwoń pod 112 i zachowaj '
                      'resztki potrawy oraz obierki do badania.',
                      style: TextStyle(height: 1.5, fontSize: 14.5),
                    ),
                  ],
                ),
              ),
            ),
          ),
          const SizedBox(height: 18),
          SizedBox(
            width: double.infinity,
            child: FilledButton(
              onPressed: _akceptuj,
              style: FilledButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12)),
              ),
              child: const Text('Rozumiem i akceptuję'),
            ),
          ),
        ],
      ),
    );
  }

  Widget _pobieranie(BuildContext context) {
    final t = Theme.of(context);
    final blad = _postep.stan == StanPobierania.blad;
    final brakPaczki = _postep.stan == StanPobierania.brak;

    final (ikona, kolor, naglowek) = switch (_postep.stan) {
      StanPobierania.blad => (
          Icons.cloud_off,
          t.colorScheme.error,
          'Nie udało się pobrać'
        ),
      StanPobierania.brak => (
          Icons.photo_library_outlined,
          t.colorScheme.onSurfaceVariant,
          'Zdjęcia w przygotowaniu'
        ),
      _ => (
          Icons.cloud_download_outlined,
          t.colorScheme.primary,
          'Pobieranie zdjęć'
        ),
    };

    return Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(ikona, size: 48, color: kolor),
          const SizedBox(height: 20),
          Text(naglowek,
              style: t.textTheme.headlineSmall
                  ?.copyWith(fontWeight: FontWeight.w700)),
          const SizedBox(height: 10),
          Text(
            _postep.komunikat ??
                'Zdjęcia pobierane są jednorazowo i działają później bez internetu. '
                    'Zalecane połączenie WiFi.',
            style: t.textTheme.bodyMedium
                ?.copyWith(color: t.colorScheme.onSurfaceVariant, height: 1.5),
          ),
          const SizedBox(height: 24),
          if (_pobieranieTrwa) ...[
            ClipRRect(
              borderRadius: BorderRadius.circular(8),
              child: LinearProgressIndicator(
                value: _postep.postep >= 0 ? _postep.postep : null,
                minHeight: 8,
              ),
            ),
            const SizedBox(height: 24),
          ],
          if (!_pobieranieTrwa && !brakPaczki)
            SizedBox(
              width: double.infinity,
              child: FilledButton.icon(
                onPressed: _pobierz,
                icon: const Icon(Icons.download),
                label: Text(blad ? 'Spróbuj ponownie' : 'Pobierz zdjęcia'),
                style: FilledButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12)),
                ),
              ),
            ),
          if (!_pobieranieTrwa && brakPaczki)
            SizedBox(
              width: double.infinity,
              child: FilledButton(
                onPressed: _wejdz,
                style: FilledButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12)),
                ),
                child: const Text('Przejdź do atlasu'),
              ),
            ),
          const SizedBox(height: 10),
          if (!_pobieranieTrwa && !brakPaczki)
            SizedBox(
              width: double.infinity,
              child: TextButton(
                onPressed: _wejdz,
                child: const Text('Pomiń — używaj bez zdjęć'),
              ),
            ),
        ],
      ),
    );
  }
}
