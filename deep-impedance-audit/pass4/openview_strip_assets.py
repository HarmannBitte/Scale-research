#!/usr/bin/env python3
"""Working copy only (under ~/.cache): delete the asset and font declarations from pubspec.yaml,
because the collected snapshot omits the binary font and branding files they refer to.
The archived collection is NOT modified. Writes a receipt of the removed lines."""
import pathlib, json
wc = pathlib.Path('/home/user/.cache/open-projects/src/Open-Source-Projects-Collection/sources/Protocentral__protocentral_openview')
p = wc / 'pubspec.yaml'
lines = p.read_text().splitlines(keepends=True)
start = next(i for i, l in enumerate(lines) if l.startswith('  assets:'))
end = next(i for i, l in enumerate(lines) if 'assets/fonts/JetBrainsMono.ttf' in l)
removed = lines[start:end + 1]
p.write_text(''.join(lines[:start] + lines[end + 1:]))
(wc / 'STRIPPED-FOR-TEST.json').write_text(json.dumps({
    'note': 'pubspec assets and fonts removed in this working copy only; the archived collection is unchanged',
    'removed_lines': [l.rstrip() for l in removed]}, indent=1))
print('removed', len(removed), 'lines')
