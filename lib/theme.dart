import 'package:flutter/material.dart';

class AtlasTheme {
  static const _ziemia = Color(0xFF6D4C33);
  static const _mech = Color(0xFF4A6B3A);
  static const _pergamin = Color(0xFFF7F3EA);

  static ThemeData jasny() {
    final scheme = ColorScheme.fromSeed(
      seedColor: _mech,
      brightness: Brightness.light,
    ).copyWith(
      primary: _mech,
      secondary: _ziemia,
      surface: _pergamin,
    );

    return ThemeData(
      useMaterial3: true,
      colorScheme: scheme,
      scaffoldBackgroundColor: _pergamin,
      appBarTheme: AppBarTheme(
        backgroundColor: _pergamin,
        surfaceTintColor: Colors.transparent,
        elevation: 0,
        centerTitle: false,
        titleTextStyle: TextStyle(
          fontSize: 22,
          fontWeight: FontWeight.w700,
          color: scheme.onSurface,
          letterSpacing: -0.3,
        ),
      ),
      cardTheme: CardThemeData(
        elevation: 0,
        color: Colors.white,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: BorderSide(color: Colors.black.withValues(alpha: 0.07)),
        ),
        margin: EdgeInsets.zero,
      ),
      chipTheme: ChipThemeData(
        showCheckmark: false,
        side: BorderSide(color: Colors.black.withValues(alpha: 0.12)),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10),
        ),
        // Kolor MUSI byc jawny - bez niego M3 bierze domyslny z ThemeData
        // i etykieta robi sie niewidoczna na bialym tle.
        labelStyle: TextStyle(
          fontSize: 13.5,
          fontWeight: FontWeight.w500,
          color: scheme.onSurface,
        ),
        secondaryLabelStyle: TextStyle(
          fontSize: 13.5,
          fontWeight: FontWeight.w600,
          color: scheme.onSurface,
        ),
        backgroundColor: Colors.white,
        selectedColor: _mech.withValues(alpha: 0.16),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: Colors.white,
        contentPadding:
            const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: Colors.black.withValues(alpha: 0.12)),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: Colors.black.withValues(alpha: 0.12)),
        ),
      ),
      dividerTheme: DividerThemeData(
        color: Colors.black.withValues(alpha: 0.07),
        space: 1,
        thickness: 1,
      ),
    );
  }

  static ThemeData ciemny() {
    final scheme = ColorScheme.fromSeed(
      seedColor: _mech,
      brightness: Brightness.dark,
    );
    return ThemeData(
      useMaterial3: true,
      colorScheme: scheme,
      appBarTheme: const AppBarTheme(
        elevation: 0,
        centerTitle: false,
        surfaceTintColor: Colors.transparent,
      ),
      chipTheme: ChipThemeData(
        showCheckmark: false,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10),
        ),
        labelStyle: TextStyle(
          fontSize: 13.5,
          fontWeight: FontWeight.w500,
          color: scheme.onSurface,
        ),
      ),
    );
  }
}
