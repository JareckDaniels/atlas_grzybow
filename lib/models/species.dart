import 'package:flutter/material.dart';

enum Jadalnosc { jadalny, warunkowo, niejadalny, trujacy, smiertelny }

extension JadalnoscX on Jadalnosc {
  static Jadalnosc from(String s) => switch (s) {
        'jadalny' => Jadalnosc.jadalny,
        'warunkowo' => Jadalnosc.warunkowo,
        'niejadalny' => Jadalnosc.niejadalny,
        'trujacy' => Jadalnosc.trujacy,
        'smiertelny' => Jadalnosc.smiertelny,
        _ => Jadalnosc.niejadalny,
      };

  String get etykieta => switch (this) {
        Jadalnosc.jadalny => 'Jadalny',
        Jadalnosc.warunkowo => 'Warunkowo jadalny',
        Jadalnosc.niejadalny => 'Niejadalny',
        Jadalnosc.trujacy => 'Trujący',
        Jadalnosc.smiertelny => 'Śmiertelnie trujący',
      };

  Color get kolor => switch (this) {
        Jadalnosc.jadalny => const Color(0xFF2E7D32),
        Jadalnosc.warunkowo => const Color(0xFF8D6E00),
        Jadalnosc.niejadalny => const Color(0xFF616161),
        Jadalnosc.trujacy => const Color(0xFFD84315),
        Jadalnosc.smiertelny => const Color(0xFFB71C1C),
      };

  IconData get ikona => switch (this) {
        Jadalnosc.jadalny => Icons.check_circle,
        Jadalnosc.warunkowo => Icons.error_outline,
        Jadalnosc.niejadalny => Icons.block,
        Jadalnosc.trujacy => Icons.warning_amber_rounded,
        Jadalnosc.smiertelny => Icons.dangerous,
      };

  bool get niebezpieczny =>
      this == Jadalnosc.trujacy || this == Jadalnosc.smiertelny;
}

enum Hymenofor { blaszki, rurki, kolce, gladki, fadki, brak }

extension HymenoforX on Hymenofor {
  static Hymenofor from(String s) => switch (s) {
        'blaszki' => Hymenofor.blaszki,
        'rurki' => Hymenofor.rurki,
        'kolce' => Hymenofor.kolce,
        'gladki' => Hymenofor.gladki,
        'fadki' => Hymenofor.fadki,
        _ => Hymenofor.brak,
      };

  String get etykieta => switch (this) {
        Hymenofor.blaszki => 'Blaszki',
        Hymenofor.rurki => 'Rurki (gąbka)',
        Hymenofor.kolce => 'Kolce',
        Hymenofor.gladki => 'Gładki',
        Hymenofor.fadki => 'Fałdki',
        Hymenofor.brak => 'Brak',
      };
}

class Species {
  final int id;
  final String nazwaPl;
  final String nazwaLac;
  final String? synonimyPl;
  final String? rodzina;
  final Jadalnosc jadalnosc;
  final Hymenofor hymenofor;
  final bool pierscien;
  final bool pochwa;
  final bool mleczko;
  final bool sinienie;
  final String? ksztaltKapelusza;
  final String? powierzchnia;
  final String? wysypZarnikow;
  final String? zapach;
  final String? smak;
  final int? miesiacOd;
  final int? miesiacDo;
  final String? opis;
  final String? cechyKluczowe;
  final String? uwagi;
  final String? kuchnia;
  final bool chroniony;

  List<String> kolorowKapelusza = [];
  List<String> siedliska = [];
  List<String> zdjecia = [];
  List<Zdjecie> zdjeciaMeta = [];

  Species({
    required this.id,
    required this.nazwaPl,
    required this.nazwaLac,
    this.synonimyPl,
    this.rodzina,
    required this.jadalnosc,
    required this.hymenofor,
    required this.pierscien,
    required this.pochwa,
    required this.mleczko,
    required this.sinienie,
    this.ksztaltKapelusza,
    this.powierzchnia,
    this.wysypZarnikow,
    this.zapach,
    this.smak,
    this.miesiacOd,
    this.miesiacDo,
    this.opis,
    this.cechyKluczowe,
    this.uwagi,
    this.kuchnia,
    required this.chroniony,
  });

  factory Species.fromMap(Map<String, Object?> m) => Species(
        id: m['id'] as int,
        nazwaPl: m['nazwa_pl'] as String,
        nazwaLac: m['nazwa_lac'] as String,
        synonimyPl: m['synonimy_pl'] as String?,
        rodzina: m['rodzina'] as String?,
        jadalnosc: JadalnoscX.from(m['jadalnosc'] as String),
        hymenofor: HymenoforX.from(m['hymenofor'] as String),
        pierscien: (m['pierscien'] as int) == 1,
        pochwa: (m['pochwa'] as int) == 1,
        mleczko: (m['mleczko'] as int) == 1,
        sinienie: (m['sinienie'] as int) == 1,
        ksztaltKapelusza: m['ksztalt_kapelusza'] as String?,
        powierzchnia: m['powierzchnia'] as String?,
        wysypZarnikow: m['wysyp_zarnikow'] as String?,
        zapach: m['zapach'] as String?,
        smak: m['smak'] as String?,
        miesiacOd: m['miesiac_od'] as int?,
        miesiacDo: m['miesiac_do'] as int?,
        opis: m['opis'] as String?,
        cechyKluczowe: m['cechy_kluczowe'] as String?,
        uwagi: m['uwagi'] as String?,
        kuchnia: m['kuchnia'] as String?,
        chroniony: (m['chroniony'] as int? ?? 0) == 1,
      );

  String get sezon {
    if (miesiacOd == null || miesiacDo == null) return '—';
    const m = ['', 'I', 'II', 'III', 'IV', 'V', 'VI',
               'VII', 'VIII', 'IX', 'X', 'XI', 'XII'];
    return '${m[miesiacOd!]} – ${m[miesiacDo!]}';
  }
}

class Zdjecie {
  final String plik;
  final String? autor;
  final String? licencja;
  final String? zrodlo;
  Zdjecie({required this.plik, this.autor, this.licencja, this.zrodlo});

  /// Podpis wymagany przez licencje CC BY / CC BY-SA.
  String get podpis {
    final a = (autor == null || autor!.isEmpty) ? 'autor nieznany' : autor!;
    final l = (licencja == null || licencja!.isEmpty) ? '' : ', $licencja';
    return '$a$l';
  }
}

class Lookalike {
  final Species gatunek;
  final String roznice;
  final int waga;
  Lookalike({required this.gatunek, required this.roznice, required this.waga});
}

/// Stan filtrów. Puste kolekcje = brak ograniczenia.
class Filtry {
  Set<Hymenofor> hymenofor = {};
  Set<String> koloryKapelusza = {};
  Set<Jadalnosc> jadalnosc = {};
  Set<String> siedliska = {};
  bool? pierscien;
  bool? pochwa;
  bool? mleczko;
  bool? sinienie;
  int? miesiac;
  String szukaj = '';

  bool get pusty =>
      hymenofor.isEmpty &&
      koloryKapelusza.isEmpty &&
      jadalnosc.isEmpty &&
      siedliska.isEmpty &&
      pierscien == null &&
      pochwa == null &&
      mleczko == null &&
      sinienie == null &&
      miesiac == null &&
      szukaj.isEmpty;

  int get aktywnych {
    var n = 0;
    n += hymenofor.length;
    n += koloryKapelusza.length;
    n += jadalnosc.length;
    n += siedliska.length;
    if (pierscien != null) n++;
    if (pochwa != null) n++;
    if (mleczko != null) n++;
    if (sinienie != null) n++;
    if (miesiac != null) n++;
    return n;
  }

  void wyczysc() {
    hymenofor.clear();
    koloryKapelusza.clear();
    jadalnosc.clear();
    siedliska.clear();
    pierscien = null;
    pochwa = null;
    mleczko = null;
    sinienie = null;
    miesiac = null;
    szukaj = '';
  }

  Filtry kopia() => Filtry()
    ..hymenofor = {...hymenofor}
    ..koloryKapelusza = {...koloryKapelusza}
    ..jadalnosc = {...jadalnosc}
    ..siedliska = {...siedliska}
    ..pierscien = pierscien
    ..pochwa = pochwa
    ..mleczko = mleczko
    ..sinienie = sinienie
    ..miesiac = miesiac
    ..szukaj = szukaj;
}
