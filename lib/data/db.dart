import 'dart:io';
import 'package:flutter/services.dart';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';
import 'package:sqflite/sqflite.dart';
import '../models/species.dart';

class AtlasDb {
  AtlasDb._();
  static final AtlasDb instance = AtlasDb._();

  Database? _db;

  Future<Database> get db async => _db ??= await _open();

  Future<Database> _open() async {
    final dir = await getApplicationDocumentsDirectory();
    final path = p.join(dir.path, 'atlas.db');

    // Kopiujemy z assetow przy pierwszym uruchomieniu lub po podbiciu wersji.
    final file = File(path);
    var trzebaKopiowac = !await file.exists();

    if (!trzebaKopiowac) {
      try {
        final tmp = await openDatabase(path, readOnly: true);
        final r = await tmp.query('meta',
            where: 'klucz = ?', whereArgs: ['db_version'], limit: 1);
        await tmp.close();
        final lokalna = int.tryParse(r.first['wartosc'] as String? ?? '0') ?? 0;
        if (lokalna < _wersjaWbudowana) trzebaKopiowac = true;
      } catch (_) {
        // Baza uszkodzona - odtwarzamy z assetow.
        trzebaKopiowac = true;
      }
    }

    if (trzebaKopiowac) {
      final data = await rootBundle.load('assets/db/atlas.db');
      await file.writeAsBytes(
        data.buffer.asUint8List(data.offsetInBytes, data.lengthInBytes),
        flush: true,
      );
    }

    return openDatabase(path, readOnly: false);
  }

  static const _wersjaWbudowana = 1;

  Future<String?> meta(String klucz) async {
    final d = await db;
    final r = await d.query('meta',
        where: 'klucz = ?', whereArgs: [klucz], limit: 1);
    return r.isEmpty ? null : r.first['wartosc'] as String?;
  }

  Future<void> setMeta(String klucz, String wartosc) async {
    final d = await db;
    await d.insert('meta', {'klucz': klucz, 'wartosc': wartosc},
        conflictAlgorithm: ConflictAlgorithm.replace);
  }

  // ---------- slowniki ----------

  Future<List<({String nazwa, String? hex})>> kolory() async {
    final d = await db;
    final r = await d.rawQuery('''
      SELECT DISTINCT k.nazwa, k.hex FROM kolory k
      JOIN species_kolor sk ON sk.kolor_id = k.id
      WHERE sk.czesc = 'kapelusz' ORDER BY k.id
    ''');
    return r
        .map((m) => (nazwa: m['nazwa'] as String, hex: m['hex'] as String?))
        .toList();
  }

  Future<List<String>> siedliska() async {
    final d = await db;
    final r = await d.rawQuery('''
      SELECT DISTINCT s.nazwa FROM siedliska s
      JOIN species_siedlisko ss ON ss.siedlisko_id = s.id
      ORDER BY s.nazwa
    ''');
    return r.map((m) => m['nazwa'] as String).toList();
  }

  // ---------- budowanie zapytania z filtrow ----------

  ({String where, List<Object?> args}) _warunki(Filtry f) {
    final w = <String>[];
    final a = <Object?>[];

    if (f.hymenofor.isNotEmpty) {
      final ph = List.filled(f.hymenofor.length, '?').join(',');
      w.add('s.hymenofor IN ($ph)');
      a.addAll(f.hymenofor.map((h) => h.name));
    }

    if (f.jadalnosc.isNotEmpty) {
      final ph = List.filled(f.jadalnosc.length, '?').join(',');
      w.add('s.jadalnosc IN ($ph)');
      a.addAll(f.jadalnosc.map((j) => j.name));
    }

    if (f.pierscien != null) {
      w.add('s.pierscien = ?');
      a.add(f.pierscien! ? 1 : 0);
    }
    if (f.pochwa != null) {
      w.add('s.pochwa = ?');
      a.add(f.pochwa! ? 1 : 0);
    }
    if (f.mleczko != null) {
      w.add('s.mleczko = ?');
      a.add(f.mleczko! ? 1 : 0);
    }
    if (f.sinienie != null) {
      w.add('s.sinienie = ?');
      a.add(f.sinienie! ? 1 : 0);
    }

    if (f.miesiac != null) {
      w.add('(? BETWEEN s.miesiac_od AND s.miesiac_do)');
      a.add(f.miesiac);
    }

    // Kolor kapelusza: OR w obrebie grupy (grzyb ma kilka barw).
    if (f.koloryKapelusza.isNotEmpty) {
      final ph = List.filled(f.koloryKapelusza.length, '?').join(',');
      w.add('''EXISTS (
        SELECT 1 FROM species_kolor sk JOIN kolory k ON k.id = sk.kolor_id
        WHERE sk.species_id = s.id AND sk.czesc = 'kapelusz'
          AND k.nazwa IN ($ph))''');
      a.addAll(f.koloryKapelusza);
    }

    if (f.siedliska.isNotEmpty) {
      final ph = List.filled(f.siedliska.length, '?').join(',');
      w.add('''EXISTS (
        SELECT 1 FROM species_siedlisko ss JOIN siedliska si ON si.id = ss.siedlisko_id
        WHERE ss.species_id = s.id AND si.nazwa IN ($ph))''');
      a.addAll(f.siedliska);
    }

    if (f.szukaj.trim().isNotEmpty) {
      final q = f.szukaj.trim().toLowerCase();
      w.add('''(LOWER(s.nazwa_pl) LIKE ? OR LOWER(s.nazwa_lac) LIKE ?
                OR LOWER(IFNULL(s.synonimy_pl,'')) LIKE ?)''');
      a.addAll(['%$q%', '%$q%', '%$q%']);
    }

    return (where: w.isEmpty ? '1=1' : w.join(' AND '), args: a);
  }

  Future<int> policz(Filtry f) async {
    final d = await db;
    final c = _warunki(f);
    final r = await d.rawQuery(
        'SELECT COUNT(*) AS n FROM species s WHERE ${c.where}', c.args);
    return r.first['n'] as int;
  }

  Future<List<Species>> szukaj(Filtry f) async {
    final d = await db;
    final c = _warunki(f);
    final rows = await d.rawQuery('''
      SELECT s.* FROM species s WHERE ${c.where}
      ORDER BY s.nazwa_pl COLLATE NOCASE
    ''', c.args);

    final lista = rows.map(Species.fromMap).toList();
    if (lista.isEmpty) return lista;

    await _dolaczRelacje(d, lista);
    return lista;
  }

  Future<void> _dolaczRelacje(Database d, List<Species> lista) async {
    final ids = lista.map((s) => s.id).join(',');
    final byId = {for (final s in lista) s.id: s};

    final kol = await d.rawQuery('''
      SELECT sk.species_id, k.nazwa FROM species_kolor sk
      JOIN kolory k ON k.id = sk.kolor_id
      WHERE sk.czesc = 'kapelusz' AND sk.species_id IN ($ids)
    ''');
    for (final m in kol) {
      byId[m['species_id'] as int]?.kolorowKapelusza.add(m['nazwa'] as String);
    }

    final sie = await d.rawQuery('''
      SELECT ss.species_id, si.nazwa FROM species_siedlisko ss
      JOIN siedliska si ON si.id = ss.siedlisko_id
      WHERE ss.species_id IN ($ids)
    ''');
    for (final m in sie) {
      byId[m['species_id'] as int]?.siedliska.add(m['nazwa'] as String);
    }

    final ph = await d.rawQuery('''
      SELECT species_id, plik FROM photos
      WHERE species_id IN ($ids) ORDER BY kolejnosc
    ''');
    for (final m in ph) {
      byId[m['species_id'] as int]?.zdjecia.add(m['plik'] as String);
    }
  }

  Future<Species?> gatunek(int id) async {
    final d = await db;
    final r = await d.query('species', where: 'id = ?', whereArgs: [id], limit: 1);
    if (r.isEmpty) return null;
    final s = Species.fromMap(r.first);
    await _dolaczRelacje(d, [s]);
    return s;
  }

  Future<List<Lookalike>> sobowtory(int speciesId) async {
    final d = await db;
    final r = await d.rawQuery('''
      SELECT sp.*, l.roznice, l.waga FROM lookalikes l
      JOIN species sp ON sp.id = l.similar_id
      WHERE l.species_id = ? ORDER BY l.waga DESC
    ''', [speciesId]);
    final out = <Lookalike>[];
    for (final m in r) {
      final s = Species.fromMap(m);
      await _dolaczRelacje(d, [s]);
      out.add(Lookalike(
        gatunek: s,
        roznice: m['roznice'] as String,
        waga: m['waga'] as int,
      ));
    }
    return out;
  }

  /// Tryb klucza: ile gatunkow zostanie po dolozeniu jednej cechy.
  Future<int> policzZ(Filtry f, void Function(Filtry) mod) async {
    final k = f.kopia();
    mod(k);
    return policz(k);
  }
}
