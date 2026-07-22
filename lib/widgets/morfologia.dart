import 'dart:math' as math;
import 'package:flutter/material.dart';

/// Schematyczne rysunki morfologii grzyba. Rysowane kodem, bez plikow.
/// Kazdy painter rysuje w ukladzie 100x100 i skaluje sie do dostepnego miejsca.

abstract class _Baza extends CustomPainter {
  final Color akcent;
  final Color neutral;
  final Color tlo;

  _Baza({required this.akcent, required this.neutral, required this.tlo});

  @override
  bool shouldRepaint(covariant CustomPainter old) => false;

  /// Skala z ukladu 100x100 na faktyczny rozmiar.
  void skaluj(Canvas c, Size s) {
    final k = math.min(s.width, s.height) / 100.0;
    c.translate((s.width - 100 * k) / 2, (s.height - 100 * k) / 2);
    c.scale(k);
  }

  Paint get linia => Paint()
    ..color = neutral
    ..style = PaintingStyle.stroke
    ..strokeWidth = 1.6
    ..strokeCap = StrokeCap.round
    ..strokeJoin = StrokeJoin.round;

  Paint get liniaAkcent => Paint()
    ..color = akcent
    ..style = PaintingStyle.stroke
    ..strokeWidth = 2.4
    ..strokeCap = StrokeCap.round
    ..strokeJoin = StrokeJoin.round;

  Paint wypelnienie(Color c) => Paint()
    ..color = c
    ..style = PaintingStyle.fill;

  /// Kontur kapelusza w formie luku (grzyb widziany z boku).
  Path kapelusz({double szer = 64, double wys = 30, double y = 38}) {
    final p = Path();
    p.moveTo(50 - szer / 2, y);
    // Wyzsze punkty kontrolne = pelniejszy, bardziej grzybowy luk.
    p.cubicTo(50 - szer / 2 + 2, y - wys * 1.55, 50 + szer / 2 - 2,
        y - wys * 1.55, 50 + szer / 2, y);
    p.close();
    return p;
  }

  void trzon(Canvas c, {double gora = 38, double dol = 84, double szer = 11}) {
    final p = Path()
      ..moveTo(50 - szer / 2, gora)
      ..lineTo(50 - szer / 2 - 1.5, dol)
      ..quadraticBezierTo(50, dol + 4, 50 + szer / 2 + 1.5, dol)
      ..lineTo(50 + szer / 2, gora)
      ..close();
    c.drawPath(p, wypelnienie(tlo));
    c.drawPath(p, linia);
  }

  void podloze(Canvas c, {double y = 88}) {
    final p = Paint()
      ..color = neutral.withValues(alpha: 0.35)
      ..strokeWidth = 1.4
      ..strokeCap = StrokeCap.round;
    c.drawLine(Offset(14, y), Offset(86, y), p);
  }
}

/// BLASZKI - promieniste listewki pod kapeluszem.
class PainterBlaszki extends _Baza {
  PainterBlaszki({required super.akcent, required super.neutral, required super.tlo});

  @override
  void paint(Canvas c, Size s) {
    skaluj(c, s);
    podloze(c);
    trzon(c);

    final kap = kapelusz();
    c.drawPath(kap, wypelnienie(tlo));

    // Blaszki - pionowe kreski pod kapeluszem.
    final pBlaszka = Paint()
      ..color = akcent
      ..strokeWidth = 1.5
      ..strokeCap = StrokeCap.round;

    c.save();
    c.clipPath(Path()..addRect(const Rect.fromLTWH(18, 33, 64, 9)));
    for (var i = 0; i <= 21; i++) {
      final x = 18.0 + i * 3.05;
      c.drawLine(Offset(x, 33), Offset(x, 43), pBlaszka);
    }
    c.restore();

    c.drawPath(kap, linia);
  }
}

/// RURKI - gabczasta warstwa, widoczna jako kropki.
class PainterRurki extends _Baza {
  PainterRurki({required super.akcent, required super.neutral, required super.tlo});

  @override
  void paint(Canvas c, Size s) {
    skaluj(c, s);
    podloze(c);
    trzon(c, szer: 17);

    final kap = kapelusz(szer: 68, wys: 31);
    c.drawPath(kap, wypelnienie(tlo));

    // Warstwa rurek - pas kropek.
    final pas = Path()
      ..addRRect(RRect.fromRectAndRadius(
          const Rect.fromLTWH(18, 36, 64, 10), const Radius.circular(3)));
    c.drawPath(pas, wypelnienie(akcent.withValues(alpha: 0.16)));

    c.save();
    c.clipPath(pas);
    final kropka = wypelnienie(akcent);
    for (var row = 0; row < 3; row++) {
      for (var i = 0; i < 23; i++) {
        final x = 19.0 + i * 2.85 + (row.isOdd ? 1.4 : 0);
        final y = 38.5 + row * 3.0;
        c.drawCircle(Offset(x, y), 0.95, kropka);
      }
    }
    c.restore();

    c.drawPath(pas, Paint()
      ..color = akcent
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.4);
    c.drawPath(kap, linia);
  }
}

/// KOLCE - zwisajace igielki.
class PainterKolce extends _Baza {
  PainterKolce({required super.akcent, required super.neutral, required super.tlo});

  @override
  void paint(Canvas c, Size s) {
    skaluj(c, s);
    podloze(c);
    trzon(c);

    final kap = kapelusz();
    c.drawPath(kap, wypelnienie(tlo));
    c.drawPath(kap, linia);

    // Kolce - trojkaty skierowane w dol, dluzsze na srodku.
    final p = wypelnienie(akcent);
    for (var i = 0; i < 18; i++) {
      final x = 21.0 + i * 3.4;
      final odSrodka = (x - 50).abs() / 30.0;
      final dl = 12.0 * (1 - odSrodka * 0.5);
      final t = Path()
        ..moveTo(x - 1.6, 38)
        ..lineTo(x + 1.6, 38)
        ..lineTo(x, 38 + dl)
        ..close();
      c.drawPath(t, p);
    }
  }
}

/// PIERSCIEN - kolnierzyk na trzonie.
class PainterPierscien extends _Baza {
  PainterPierscien({required super.akcent, required super.neutral, required super.tlo});

  @override
  void paint(Canvas c, Size s) {
    skaluj(c, s);
    podloze(c);
    trzon(c);

    final kap = kapelusz(szer: 56, wys: 25);
    c.drawPath(kap, wypelnienie(tlo));
    c.drawPath(kap, linia);

    // Pierscien - spodniczka wokol trzonu.
    final p = Path()
      ..moveTo(35, 54)
      ..quadraticBezierTo(50, 50, 65, 54)
      ..quadraticBezierTo(65, 60, 58, 60)
      ..lineTo(42, 60)
      ..quadraticBezierTo(35, 60, 35, 54)
      ..close();
    c.drawPath(p, wypelnienie(akcent.withValues(alpha: 0.28)));
    c.drawPath(p, liniaAkcent);

    _strzalka(c, const Offset(80, 56), const Offset(67, 56));
  }

  void _strzalka(Canvas c, Offset od, Offset doo) {
    final p = Paint()
      ..color = akcent
      ..strokeWidth = 1.8
      ..strokeCap = StrokeCap.round;
    c.drawLine(od, doo, p);
    c.drawLine(doo, doo + const Offset(4, -3), p);
    c.drawLine(doo, doo + const Offset(4, 3), p);
  }
}

/// POCHWA - workowata oslona u podstawy. Cecha krytyczna.
class PainterPochwa extends _Baza {
  PainterPochwa({required super.akcent, required super.neutral, required super.tlo});

  @override
  void paint(Canvas c, Size s) {
    skaluj(c, s);

    // Linia sciolki - pochwa czesto jest pod nia ukryta.
    final sciolka = Paint()
      ..color = neutral.withValues(alpha: 0.3)
      ..strokeWidth = 1.4
      ..strokeCap = StrokeCap.round;
    c.drawLine(const Offset(12, 74), const Offset(88, 74), sciolka);

    trzon(c, dol: 78, szer: 12);

    final kap = kapelusz(szer: 54, wys: 24);
    c.drawPath(kap, wypelnienie(tlo));
    c.drawPath(kap, linia);

    // Pochwa - workowata struktura u podstawy.
    final p = Path()
      ..moveTo(38, 74)
      ..quadraticBezierTo(35, 86, 42, 91)
      ..quadraticBezierTo(50, 94, 58, 91)
      ..quadraticBezierTo(65, 86, 62, 74)
      ..quadraticBezierTo(56, 78, 50, 77)
      ..quadraticBezierTo(44, 78, 38, 74)
      ..close();
    c.drawPath(p, wypelnienie(akcent.withValues(alpha: 0.3)));
    c.drawPath(p, liniaAkcent);

    // Kreskowana linia - podkresla, ze trzeba wykopac.
    final przer = Paint()
      ..color = akcent.withValues(alpha: 0.55)
      ..strokeWidth = 1.2;
    for (var x = 14.0; x < 86; x += 5) {
      c.drawLine(Offset(x, 74), Offset(x + 2.6, 74), przer);
    }
  }
}

/// MLECZKO - kropla wyplywajaca z przecietego miazszu.
class PainterMleczko extends _Baza {
  PainterMleczko({required super.akcent, required super.neutral, required super.tlo});

  @override
  void paint(Canvas c, Size s) {
    skaluj(c, s);
    podloze(c);
    trzon(c);

    final kap = kapelusz();
    c.drawPath(kap, wypelnienie(tlo));
    c.drawPath(kap, linia);

    // Naciecie.
    c.drawLine(const Offset(29, 40), const Offset(44, 48),
        Paint()
          ..color = neutral
          ..strokeWidth = 1.6
          ..strokeCap = StrokeCap.round);

    // Krople.
    final k = wypelnienie(akcent);
    _kropla(c, const Offset(36, 51), 3.6, k);
    _kropla(c, const Offset(41, 62), 2.6, k);
    _kropla(c, const Offset(38, 72), 1.8, k);
  }

  void _kropla(Canvas c, Offset o, double r, Paint p) {
    final path = Path()
      ..moveTo(o.dx, o.dy - r * 1.5)
      ..quadraticBezierTo(o.dx + r, o.dy - r * 0.2, o.dx + r * 0.75, o.dy + r * 0.4)
      ..quadraticBezierTo(o.dx, o.dy + r * 1.3, o.dx - r * 0.75, o.dy + r * 0.4)
      ..quadraticBezierTo(o.dx - r, o.dy - r * 0.2, o.dx, o.dy - r * 1.5)
      ..close();
    c.drawPath(path, p);
  }
}

/// SINIENIE - miazsz zmieniajacy barwe po przekrojeniu.
class PainterSinienie extends _Baza {
  PainterSinienie({required super.akcent, required super.neutral, required super.tlo});

  @override
  void paint(Canvas c, Size s) {
    skaluj(c, s);
    podloze(c);

    // Przekrojony grzyb - lewa polowa jasna, prawa siniejaca.
    final lewa = Path()
      ..moveTo(50, 38)
      ..lineTo(18, 38)
      ..cubicTo(18, 6, 50, 6, 50, 6)
      ..close();
    final trzonL = Path()
      ..moveTo(44, 38)
      ..lineTo(43, 84)
      ..quadraticBezierTo(46, 87, 50, 86)
      ..lineTo(50, 38)
      ..close();

    c.drawPath(lewa, wypelnienie(tlo));
    c.drawPath(trzonL, wypelnienie(tlo));

    final prawa = Path()
      ..moveTo(50, 38)
      ..lineTo(82, 38)
      ..cubicTo(82, 6, 50, 6, 50, 6)
      ..close();
    final trzonP = Path()
      ..moveTo(50, 38)
      ..lineTo(50, 86)
      ..quadraticBezierTo(54, 87, 57, 84)
      ..lineTo(56, 38)
      ..close();

    const niebieski = Color(0xFF3F6FB5);
    c.drawPath(prawa, wypelnienie(niebieski.withValues(alpha: 0.35)));
    c.drawPath(trzonP, wypelnienie(niebieski.withValues(alpha: 0.35)));

    c.drawPath(lewa, linia);
    c.drawPath(trzonL, linia);
    c.drawPath(prawa, linia);
    c.drawPath(trzonP, linia);

    // Linia ciecia.
    c.drawLine(const Offset(50, 6), const Offset(50, 86),
        Paint()
          ..color = neutral
          ..strokeWidth = 1.2);

    // Strzalka czasu.
    final p = Paint()
      ..color = niebieski
      ..strokeWidth = 1.8
      ..strokeCap = StrokeCap.round;
    c.drawLine(const Offset(64, 22), const Offset(76, 22), p);
    c.drawLine(const Offset(76, 22), const Offset(72, 19), p);
    c.drawLine(const Offset(76, 22), const Offset(72, 25), p);
  }
}

/// TRZON - podstawowa budowa z nazwami czesci.
class PainterBudowa extends _Baza {
  PainterBudowa({required super.akcent, required super.neutral, required super.tlo});

  @override
  void paint(Canvas c, Size s) {
    skaluj(c, s);
    podloze(c, y: 90);
    trzon(c, dol: 86);

    final kap = kapelusz(szer: 60, wys: 27);
    c.drawPath(kap, wypelnienie(tlo));
    c.drawPath(kap, linia);

    // Blaszki lekko zaznaczone.
    final pBl = Paint()
      ..color = neutral.withValues(alpha: 0.5)
      ..strokeWidth = 1.1;
    for (var i = 0; i <= 18; i++) {
      final x = 22.0 + i * 3.1;
      c.drawLine(Offset(x, 34), Offset(x, 38), pBl);
    }

    final wsk = Paint()
      ..color = akcent
      ..strokeWidth = 1.3
      ..strokeCap = StrokeCap.round;
    final kropka = wypelnienie(akcent);

    // Wskazniki do czesci.
    c.drawCircle(const Offset(34, 24), 1.7, kropka);
    c.drawLine(const Offset(34, 24), const Offset(12, 17), wsk);

    c.drawCircle(const Offset(30, 37), 1.7, kropka);
    c.drawLine(const Offset(30, 37), const Offset(10, 44), wsk);

    c.drawCircle(const Offset(50, 62), 1.7, kropka);
    c.drawLine(const Offset(50, 62), const Offset(84, 62), wsk);

    c.drawCircle(const Offset(50, 84), 1.7, kropka);
    c.drawLine(const Offset(50, 84), const Offset(84, 84), wsk);
  }
}
