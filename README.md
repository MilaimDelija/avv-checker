# avv-checker

[English version](README.en.md)

avv-checker durchsucht den Text eines Auftragsverarbeitungsvertrags (AVV)
nach Formulierungen, die üblicherweise die 17 in Art. 28 Abs. 2 bis 4 DSGVO
vorgeschriebenen Vertragsinhalte abdecken, und meldet, welche davon nicht
auffindbar waren. Das Werkzeug liest .txt-, .docx- und .pdf-Dateien.

Ein Treffer zeigt nur, dass eine zum jeweiligen Pflichtinhalt passende
Formulierung vorhanden ist, nicht, dass sie inhaltlich ausreicht. Das
Fehlen eines Treffers zeigt nicht sicher, dass der Punkt ungeregelt ist,
wenn eine unübliche Formulierung verwendet wurde. Das Werkzeug ersetzt
keine rechtliche Prüfung und keine Beratung durch eine dafür qualifizierte
Person. Methodik und Grenzen stehen vollständig in
[METHODIK.md](METHODIK.md).

## Installation

```bash
git clone https://github.com/milaimdelija/avv-checker.git
cd avv-checker
pip install -e .
```

Python 3.10 oder neuer wird vorausgesetzt.

## Verwendung

```bash
avv-checker vertrag.pdf --out berichte/ --format md,html,json
```

Der Befehl erzeugt `avv-bericht.md`, `avv-bericht.html` und
`avv-bericht.json` im angegebenen Verzeichnis und listet auf der
Kommandozeile, welche Pflichtinhalte nicht gefunden wurden.

## Lokale Demonstration

Im Verzeichnis `tests/fixtures/` liegen zwei frei erfundene Beispielverträge:
`sample_avv_complete.txt` deckt alle 17 Pflichtinhalte ab,
`sample_avv_incomplete.txt` lässt absichtlich vier davon aus. Mit
`scripts/demo.py` lassen sich beide direkt prüfen:

```bash
python3 scripts/demo.py
```

Die Berichte werden nach `demo_output/` geschrieben.

## Aufbau des Quellcodes

`requirements.py` enthält die 17 Pflichtinhalte mit ihren Suchmustern,
`extract.py` liest Text aus .txt-, .docx- und .pdf-Dateien, `matcher.py`
gleicht den extrahierten Text gegen die Pflichtinhalte ab, und `report.py`
erzeugt daraus die Berichte. Diese Trennung erlaubt es, die Erkennungslogik
in `tests/` ohne Beispieldateien in verschiedenen Formaten zu testen.

## Tests

```bash
pip install -e ".[dev]"
pytest
```

## Lizenz

MIT, siehe [LICENSE](LICENSE).
