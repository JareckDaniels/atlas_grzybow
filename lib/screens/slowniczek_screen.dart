import 'package:flutter/material.dart';
import '../widgets/morfologia.dart';

class _Pojecie {
  final String nazwa;
  final String krotko;
  final String opis;
  final String? uwaga;
  final bool krytyczne;
  final CustomPainter Function(Color akcent, Color neutral, Color tlo) painter;

  const _Pojecie({
    required this.nazwa,
    required this.krotko,
    required this.opis,
    this.uwaga,
    this.krytyczne = false,
    required this.painter,
  });
}

class SlowniczekScreen extends StatelessWidget {
  const SlowniczekScreen({super.key});

  static final _pojecia = <_Pojecie>[
    _Pojecie(
      nazwa: 'Budowa owocnika',
      krotko: 'Podstawowe części grzyba',
      opis: 'Kapelusz przykrywa warstwę zarodnikotwórczą (hymenofor), '
          'czyli blaszki, rurki lub kolce. Trzon podtrzymuje kapelusz. '
          'U podstawy trzonu mogą występować bulwa lub pochwa.\n\n'
          'Zawsze wykopuj grzyb w całości — sama podstawa trzonu bywa '
          'najważniejszą cechą rozpoznawczą, a odcięcie nożem ją niszczy.',
      painter: (a, n, t) => PainterBudowa(akcent: a, neutral: n, tlo: t),
    ),
    _Pojecie(
      nazwa: 'Blaszki',
      krotko: 'Cienkie listewki pod kapeluszem',
      opis: 'Promieniście ułożone, cienkie płytki biegnące od trzonu '
          'ku brzegowi kapelusza. Dają się rozdzielić palcem.\n\n'
          'Zwróć uwagę na ich barwę i na to, jak łączą się z trzonem: '
          'blaszki wolne nie dotykają trzonu, przyrośnięte dochodzą do niego, '
          'zbiegające schodzą po nim w dół. Barwa blaszek zmienia się z wiekiem '
          'i bywa cechą rozstrzygającą.',
      painter: (a, n, t) => PainterBlaszki(akcent: a, neutral: n, tlo: t),
    ),
    _Pojecie(
      nazwa: 'Rurki (gąbka)',
      krotko: 'Warstwa przypominająca gąbkę',
      opis: 'Zamiast blaszek spód kapelusza tworzy warstwa pionowych rurek, '
          'widocznych od dołu jako drobne pory. Całą warstwę można zwykle '
          'oddzielić od miąższu kapelusza jednym ruchem.\n\n'
          'Tak zbudowane są borowiki, koźlarze, maślaki i podgrzybki. '
          'Barwa porów oraz to, czy sinieją po naciśnięciu, to ważne cechy.',
      painter: (a, n, t) => PainterRurki(akcent: a, neutral: n, tlo: t),
    ),
    _Pojecie(
      nazwa: 'Kolce',
      krotko: 'Zwisające igiełki',
      opis: 'Spód kapelusza pokrywają miękkie, zwisające kolce, dłuższe '
          'w środkowej części. Tak wygląda kolczak obłączasty i inne '
          'grzyby kolczakowate.',
      painter: (a, n, t) => PainterKolce(akcent: a, neutral: n, tlo: t),
    ),
    _Pojecie(
      nazwa: 'Pierścień',
      krotko: 'Kołnierzyk na trzonie',
      opis: 'Błoniasta obrączka w górnej części trzonu — pozostałość osłony, '
          'która u młodego owocnika okrywała blaszki.\n\n'
          'Sprawdź, czy pierścień daje się przesuwać palcem wzdłuż trzonu. '
          'Ruchomy pierścień to cecha kani. Pierścień bywa delikatny '
          'i u starszych owocników może zaniknąć.',
      painter: (a, n, t) => PainterPierscien(akcent: a, neutral: n, tlo: t),
    ),
    _Pojecie(
      nazwa: 'Pochwa',
      krotko: 'Workowata osłona u podstawy trzonu',
      opis: 'Pozostałość osłony, z której wyrósł owocnik — tworzy workowaty '
          'lub kubkowaty twór obejmujący podstawę trzonu.\n\n'
          'Pochwa bywa całkowicie ukryta w ściółce. Nie zobaczysz jej, '
          'jeśli grzyb odetniesz nożem. To dokładnie ten scenariusz, '
          'w którym muchomor sromotnikowy trafia do koszyka jako pieczarka.',
      uwaga: 'Obecność pochwy przy białych blaszkach to sygnał alarmowy — '
          'tak wygląda muchomor sromotnikowy, najbardziej trujący grzyb Europy. '
          'Zawsze wykopuj grzyb w całości.',
      krytyczne: true,
      painter: (a, n, t) => PainterPochwa(akcent: a, neutral: n, tlo: t),
    ),
    _Pojecie(
      nazwa: 'Mleczko',
      krotko: 'Sok wypływający po przecięciu',
      opis: 'Po nacięciu blaszek lub miąższu wypływa mleczny sok. '
          'Występuje u mleczajów — rydzów, mleczaja chrząstki i pokrewnych.\n\n'
          'Znaczenie ma barwa mleczka (biała, pomarańczowa, żółknąca) '
          'oraz to, czy zmienia kolor po kilku minutach na powietrzu.',
      painter: (a, n, t) => PainterMleczko(akcent: a, neutral: n, tlo: t),
    ),
    _Pojecie(
      nazwa: 'Sinienie',
      krotko: 'Zmiana barwy miąższu po przekrojeniu',
      opis: 'Miąższ niektórych grzybów po przecięciu lub uciśnięciu '
          'przybiera barwę niebieską, granatową lub zielonkawą. Reakcja '
          'bywa błyskawiczna albo zajmuje kilka minut.\n\n'
          'Przekrój owocnik wzdłuż i obserwuj przez 1–2 minuty. '
          'Samo sinienie nie oznacza, że grzyb jest trujący — '
          'to po prostu cecha rozpoznawcza.',
      painter: (a, n, t) => PainterSinienie(akcent: a, neutral: n, tlo: t),
    ),
  ];

  @override
  Widget build(BuildContext context) {
    final t = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: const Text('Słowniczek pojęć')),
      body: ListView.separated(
        padding: const EdgeInsets.fromLTRB(16, 8, 16, 28),
        itemCount: _pojecia.length + 1,
        separatorBuilder: (_, __) => const SizedBox(height: 14),
        itemBuilder: (context, i) {
          if (i == 0) {
            return Padding(
              padding: const EdgeInsets.only(bottom: 4),
              child: Text(
                'Terminy używane w filtrach i na kartach gatunków. '
                'Rysunki są schematyczne — pokazują zasadę, nie konkretny gatunek.',
                style: t.textTheme.bodyMedium?.copyWith(
                    color: t.colorScheme.onSurfaceVariant, height: 1.5),
              ),
            );
          }
          return _karta(context, _pojecia[i - 1]);
        },
      ),
    );
  }

  Widget _karta(BuildContext context, _Pojecie p) {
    final t = Theme.of(context);
    final akcent =
        p.krytyczne ? const Color(0xFFB71C1C) : t.colorScheme.primary;

    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: p.krytyczne
              ? const Color(0xFFB71C1C).withValues(alpha: 0.28)
              : Colors.black.withValues(alpha: 0.08),
        ),
      ),
      clipBehavior: Clip.antiAlias,
      child: Theme(
        data: t.copyWith(dividerColor: Colors.transparent),
        child: ExpansionTile(
          tilePadding: const EdgeInsets.fromLTRB(12, 6, 14, 6),
          childrenPadding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
          expandedCrossAxisAlignment: CrossAxisAlignment.start,
          leading: SizedBox(
            width: 62,
            height: 62,
            child: CustomPaint(
              painter: p.painter(
                akcent,
                t.colorScheme.onSurface.withValues(alpha: 0.75),
                const Color(0xFFF2EDE2),
              ),
            ),
          ),
          title: Text(p.nazwa,
              style: t.textTheme.titleMedium
                  ?.copyWith(fontWeight: FontWeight.w700)),
          subtitle: Padding(
            padding: const EdgeInsets.only(top: 2),
            child: Text(p.krotko,
                style: t.textTheme.bodySmall
                    ?.copyWith(color: t.colorScheme.onSurfaceVariant)),
          ),
          children: [
            // Duzy rysunek po rozwinieciu.
            Center(
              child: Container(
                width: 168,
                height: 168,
                margin: const EdgeInsets.only(bottom: 14),
                decoration: BoxDecoration(
                  color: const Color(0xFFFAF7F0),
                  borderRadius: BorderRadius.circular(14),
                  border:
                      Border.all(color: Colors.black.withValues(alpha: 0.06)),
                ),
                child: CustomPaint(
                  painter: p.painter(
                    akcent,
                    t.colorScheme.onSurface.withValues(alpha: 0.75),
                    const Color(0xFFF2EDE2),
                  ),
                ),
              ),
            ),
            Text(p.opis,
                style: const TextStyle(height: 1.55, fontSize: 14.5)),
            if (p.uwaga != null) ...[
              const SizedBox(height: 14),
              Container(
                padding: const EdgeInsets.all(13),
                decoration: BoxDecoration(
                  color: const Color(0xFFB71C1C).withValues(alpha: 0.07),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(
                      color: const Color(0xFFB71C1C).withValues(alpha: 0.25)),
                ),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Icon(Icons.warning_amber_rounded,
                        size: 19, color: Color(0xFFB71C1C)),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Text(p.uwaga!,
                          style: const TextStyle(
                              height: 1.45,
                              fontSize: 13.5,
                              fontWeight: FontWeight.w500)),
                    ),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
