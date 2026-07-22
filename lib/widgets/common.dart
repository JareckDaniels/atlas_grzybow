import 'dart:io';
import 'package:flutter/material.dart';
import '../data/photo_manager.dart';
import '../models/species.dart';

class BadgeJadalnosc extends StatelessWidget {
  final Jadalnosc jadalnosc;
  final bool maly;
  const BadgeJadalnosc(this.jadalnosc, {super.key, this.maly = false});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(
          horizontal: maly ? 8 : 10, vertical: maly ? 3 : 5),
      decoration: BoxDecoration(
        color: jadalnosc.kolor.withValues(alpha: 0.13),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(jadalnosc.ikona, size: maly ? 13 : 15, color: jadalnosc.kolor),
          const SizedBox(width: 5),
          Text(
            jadalnosc.etykieta,
            style: TextStyle(
              fontSize: maly ? 11.5 : 13,
              fontWeight: FontWeight.w600,
              color: jadalnosc.kolor,
            ),
          ),
        ],
      ),
    );
  }
}

class ZdjecieGatunku extends StatelessWidget {
  final String? plik;
  final double? width;
  final double? height;
  final BorderRadius? radius;

  const ZdjecieGatunku(this.plik,
      {super.key, this.width, this.height, this.radius});

  @override
  Widget build(BuildContext context) {
    final placeholder = Container(
      width: width,
      height: height,
      color: Theme.of(context).colorScheme.surfaceContainerHighest,
      child: Icon(Icons.photo_outlined,
          color: Theme.of(context).colorScheme.outline, size: 26),
    );

    if (plik == null || plik!.isEmpty) {
      return ClipRRect(
          borderRadius: radius ?? BorderRadius.zero, child: placeholder);
    }

    return ClipRRect(
      borderRadius: radius ?? BorderRadius.zero,
      child: FutureBuilder<String?>(
        future: PhotoManager.instance.sciezka(plik!),
        builder: (context, snap) {
          if (snap.connectionState != ConnectionState.done ||
              snap.data == null) {
            return placeholder;
          }
          return Image.file(
            File(snap.data!),
            width: width,
            height: height,
            fit: BoxFit.cover,
            errorBuilder: (_, __, ___) => placeholder,
          );
        },
      ),
    );
  }
}

class KartaGatunku extends StatelessWidget {
  final Species s;
  final VoidCallback onTap;
  const KartaGatunku({super.key, required this.s, required this.onTap});

  @override
  Widget build(BuildContext context) {
    final t = Theme.of(context);
    return Card(
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(10),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              ZdjecieGatunku(
                s.zdjecia.isEmpty ? null : s.zdjecia.first,
                width: 84,
                height: 84,
                radius: BorderRadius.circular(12),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(s.nazwaPl,
                        style: t.textTheme.titleMedium
                            ?.copyWith(fontWeight: FontWeight.w700),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis),
                    Text(s.nazwaLac,
                        style: t.textTheme.bodySmall?.copyWith(
                            fontStyle: FontStyle.italic,
                            color: t.colorScheme.onSurfaceVariant),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis),
                    const SizedBox(height: 7),
                    BadgeJadalnosc(s.jadalnosc, maly: true),
                    const SizedBox(height: 6),
                    Wrap(
                      spacing: 6,
                      runSpacing: 4,
                      children: [
                        _tag(context, s.hymenofor.etykieta),
                        if (s.pochwa) _tag(context, 'pochwa'),
                        if (s.pierscien) _tag(context, 'pierścień'),
                        if (s.mleczko) _tag(context, 'mleczko'),
                        _tag(context, s.sezon),
                      ],
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _tag(BuildContext context, String txt) {
    final t = Theme.of(context);
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 2),
      decoration: BoxDecoration(
        color: t.colorScheme.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(6),
      ),
      child: Text(txt,
          style: TextStyle(
              fontSize: 11, color: t.colorScheme.onSurfaceVariant)),
    );
  }
}

class OstrzezenieBaner extends StatelessWidget {
  final Jadalnosc jadalnosc;
  const OstrzezenieBaner(this.jadalnosc, {super.key});

  @override
  Widget build(BuildContext context) {
    if (!jadalnosc.niebezpieczny) return const SizedBox.shrink();
    final smiertelny = jadalnosc == Jadalnosc.smiertelny;
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      color: jadalnosc.kolor,
      child: Row(
        children: [
          const Icon(Icons.dangerous, color: Colors.white, size: 22),
          const SizedBox(width: 10),
          Expanded(
            child: Text(
              smiertelny
                  ? 'GRZYB ŚMIERTELNIE TRUJĄCY — nie zbieraj, nie spożywaj'
                  : 'GRZYB TRUJĄCY — nie nadaje się do spożycia',
              style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.w700,
                  fontSize: 13,
                  letterSpacing: 0.2),
            ),
          ),
        ],
      ),
    );
  }
}
