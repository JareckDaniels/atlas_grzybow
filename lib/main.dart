import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'data/db.dart';
import 'data/photo_manager.dart';
import 'screens/lista_screen.dart' show ListaScreen;
import 'screens/setup_screen.dart';
import 'theme.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const AtlasApp());
}

class AtlasApp extends StatelessWidget {
  const AtlasApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Atlas grzybów',
      debugShowCheckedModeBanner: false,
      theme: AtlasTheme.jasny(),
      darkTheme: AtlasTheme.ciemny(),
      themeMode: ThemeMode.light,
      home: const _Start(),
    );
  }
}

class _Start extends StatefulWidget {
  const _Start();
  @override
  State<_Start> createState() => _StartState();
}

class _StartState extends State<_Start> {
  Future<bool>? _gotowe;

  @override
  void initState() {
    super.initState();
    _gotowe = _sprawdz();
  }

  Future<bool> _sprawdz() async {
    await AtlasDb.instance.db; // wymusza kopiowanie bazy z assetow
    final prefs = await SharedPreferences.getInstance();
    final zaakceptowany = prefs.getBool('disclaimer_ok') ?? false;
    final zdjecia = await PhotoManager.instance.czyPobrane();
    return zaakceptowany && zdjecia;
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<bool>(
      future: _gotowe,
      builder: (context, snap) {
        if (!snap.hasData) {
          return const Scaffold(
            body: Center(child: CircularProgressIndicator()),
          );
        }
        return snap.data! ? const ListaScreen() : const SetupScreen();
      },
    );
  }
}
