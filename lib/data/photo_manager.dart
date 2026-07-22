import 'dart:convert';
import 'dart:io';
import 'package:archive/archive.dart';
import 'package:http/http.dart' as http;
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';
import 'db.dart';

enum StanPobierania { nieznany, brak, pobieranie, rozpakowywanie, gotowe, blad }

class PostepPobierania {
  final StanPobierania stan;
  final double postep; // 0..1, -1 = nieokreslony
  final String? komunikat;
  const PostepPobierania(this.stan, {this.postep = -1, this.komunikat});
}

/// Manifest na GitHubie:
/// { "version": 3, "url": "https://github.com/.../releases/download/photos-v3/photos.zip",
///   "size": 48210332, "count": 412 }
class PhotoManager {
  PhotoManager._();
  static final PhotoManager instance = PhotoManager._();

  Directory? _katalog;

  Future<Directory> get katalog async {
    if (_katalog != null) return _katalog!;
    final dir = await getApplicationDocumentsDirectory();
    final d = Directory(p.join(dir.path, 'photos'));
    if (!await d.exists()) await d.create(recursive: true);
    return _katalog = d;
  }

  Future<String?> sciezka(String plik) async {
    if (plik.isEmpty) return null;
    final f = File(p.join((await katalog).path, plik));
    return await f.exists() ? f.path : null;
  }

  Future<bool> czyPobrane() async {
    final v = await AtlasDb.instance.meta('photos_version');
    if (v == null || v == '0') return false;
    final d = await katalog;
    return await d.exists() && !await d.list().isEmpty;
  }

  Future<Map<String, dynamic>?> sprawdzManifest() async {
    final url = await AtlasDb.instance.meta('photos_manifest_url');
    if (url == null) return null;
    try {
      final r = await http
          .get(Uri.parse(url))
          .timeout(const Duration(seconds: 15));
      if (r.statusCode != 200) return null;
      return jsonDecode(utf8.decode(r.bodyBytes)) as Map<String, dynamic>;
    } catch (_) {
      return null;
    }
  }

  /// Pobiera i rozpakowuje paczke. Emituje postep.
  Stream<PostepPobierania> pobierz() async* {
    yield const PostepPobierania(StanPobierania.pobieranie,
        komunikat: 'Sprawdzanie dostępnych zdjęć…');

    final manifest = await sprawdzManifest();
    if (manifest == null) {
      yield const PostepPobierania(StanPobierania.blad,
          komunikat: 'Brak połączenia z serwerem zdjęć.');
      return;
    }

    final url = manifest['url'] as String?;
    final wersja = (manifest['version'] as num?)?.toInt() ?? 0;
    final rozmiar = (manifest['size'] as num?)?.toInt() ?? 0;

    // Manifest istnieje, ale paczka nie zostala jeszcze opublikowana.
    if (wersja == 0 || url == null || url.isEmpty) {
      yield const PostepPobierania(StanPobierania.brak,
          komunikat: 'Paczka zdjęć nie została jeszcze opublikowana. '
              'Atlas działa bez zdjęć — opisy, filtry i klucz są kompletne.');
      return;
    }

    final dir = await katalog;
    final tmp = File(p.join(dir.parent.path, 'photos_tmp.zip'));

    try {
      final req = http.Request('GET', Uri.parse(url));
      final resp = await req.send().timeout(const Duration(seconds: 30));

      if (resp.statusCode != 200) {
        yield PostepPobierania(StanPobierania.blad,
            komunikat: 'Serwer zwrócił błąd ${resp.statusCode}.');
        return;
      }

      final total = resp.contentLength ?? rozmiar;
      var odebrane = 0;
      final sink = tmp.openWrite();

      await for (final chunk in resp.stream) {
        sink.add(chunk);
        odebrane += chunk.length;
        yield PostepPobierania(
          StanPobierania.pobieranie,
          postep: total > 0 ? odebrane / total : -1,
          komunikat: total > 0
              ? '${(odebrane / 1048576).toStringAsFixed(1)} / '
                  '${(total / 1048576).toStringAsFixed(1)} MB'
              : '${(odebrane / 1048576).toStringAsFixed(1)} MB',
        );
      }
      await sink.close();

      yield const PostepPobierania(StanPobierania.rozpakowywanie,
          komunikat: 'Rozpakowywanie…');

      final bytes = await tmp.readAsBytes();
      final archive = ZipDecoder().decodeBytes(bytes);
      var i = 0;
      for (final entry in archive) {
        if (!entry.isFile) continue;
        // Zabezpieczenie przed zip slip.
        final nazwa = p.basename(entry.name);
        if (nazwa.isEmpty || nazwa.startsWith('.')) continue;
        final out = File(p.join(dir.path, nazwa));
        await out.writeAsBytes(entry.content as List<int>, flush: false);
        i++;
        if (i % 20 == 0) {
          yield PostepPobierania(StanPobierania.rozpakowywanie,
              postep: i / archive.length, komunikat: 'Rozpakowywanie… $i');
        }
      }

      await tmp.delete();
      await AtlasDb.instance.setMeta('photos_version', '$wersja');

      yield PostepPobierania(StanPobierania.gotowe,
          postep: 1, komunikat: 'Pobrano $i zdjęć.');
    } catch (e) {
      if (await tmp.exists()) {
        try {
          await tmp.delete();
        } catch (_) {}
      }
      yield PostepPobierania(StanPobierania.blad,
          komunikat: 'Nie udało się pobrać zdjęć: $e');
    }
  }

  Future<void> usun() async {
    final d = await katalog;
    if (await d.exists()) await d.delete(recursive: true);
    _katalog = null;
    await AtlasDb.instance.setMeta('photos_version', '0');
  }

  Future<int> rozmiarNaDysku() async {
    final d = await katalog;
    if (!await d.exists()) return 0;
    var suma = 0;
    await for (final e in d.list()) {
      if (e is File) suma += await e.length();
    }
    return suma;
  }
}
