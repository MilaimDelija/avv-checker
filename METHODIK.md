# Methodik und Grenzen

Dieses Dokument beschreibt, wie avv-checker zu seinen Ergebnissen kommt, und
hält an einer Stelle fest, was das Werkzeug nicht leisten kann.

## Rechtliche Grundlage

Die 17 geprüften Pflichtinhalte stammen aus Art. 28 Abs. 2, 3 und 4 DSGVO:
den sechs Grundangaben aus Art. 28 Abs. 3 Satz 1 (Gegenstand, Dauer, Art und
Zweck der Verarbeitung, Art der Daten, Kategorien betroffener Personen,
Pflichten und Rechte des Verantwortlichen), den acht Pflichten des
Auftragsverarbeiters aus Art. 28 Abs. 3 Satz 2 Buchstabe a bis h, sowie den
drei Bedingungen für die Einbindung weiterer Auftragsverarbeiter aus Art. 28
Abs. 2 und 4. Der Gesetzestext ist seit Inkrafttreten der DSGVO im Jahr 2018
unverändert. `requirements.py` verweist bei jedem Pflichtinhalt auf die
konkrete Fundstelle.

## Funktionsweise der Erkennung

avv-checker durchsucht den extrahierten Text nach handverlesenen,
regelbasierten Textmustern, die typische deutschsprachige
AVV-Formulierungen für den jeweiligen Pflichtinhalt abbilden. Ein Treffer
bedeutet ausschließlich, dass eine passende Formulierung im Text vorkommt.
Er belegt nicht, dass diese Formulierung dem konkreten Einzelfall gerecht
wird, dass die dort in Bezug genommene Anlage (etwa die TOM oder die Liste
der Unterauftragsverarbeiter) inhaltlich vollständig oder aktuell ist, oder
dass der Vertrag insgesamt wirksam zustande gekommen ist.

Das Fehlen eines Treffers bedeutet nicht sicher, dass der Vertrag den
betreffenden Punkt nicht regelt. Verträge, die stark abweichende,
unübliche oder in einer anderen Sprache verfasste Formulierungen verwenden,
können denselben Inhalt abdecken, ohne von den hinterlegten Mustern erkannt
zu werden. Die Musterliste wurde anhand gängiger deutschsprachiger
AVV-Vorlagen von Hand zusammengestellt und ist nicht erschöpfend.

## Textextraktion

Aus .txt- und .md-Dateien wird der Inhalt unverändert gelesen. Aus
.docx-Dateien werden Absätze und Tabellenzellen extrahiert; Kopf- und
Fußzeilen, Textfelder und eingebettete Grafiken mit Text werden nicht
erfasst. Aus .pdf-Dateien wird der Text pro Seite extrahiert; bei
gescannten, nicht texterkannten PDFs (reine Bilddateien ohne
Texterkennungsschicht) liefert dies keinen oder unbrauchbaren Text, was
avv-checker mit einer Fehlermeldung quittiert, statt einen leeren oder
fehlerhaften Bericht zu erzeugen. Die Qualität der PDF-Textextraktion hängt
zudem vom verwendeten Layoutprogramm ab; mehrspaltige Layouts oder Tabellen
können in falscher Reihenfolge extrahiert werden.

## Umfang der Prüfung

Geprüft wird ausschließlich der Inhalt eines einzelnen vorgelegten
Dokuments. Verweist der Vertrag auf externe Anlagen, die nicht Teil der
geprüften Datei sind (etwa eine separat verwaltete TOM-Dokumentation oder
eine Liste der Unterauftragsverarbeiter in einem anderen System), wird nur
der Verweis selbst erkannt, nicht der Inhalt der Anlage. avv-checker bewertet
nicht, ob die im Vertrag genannten technischen und organisatorischen
Maßnahmen den Anforderungen des Art. 32 DSGVO tatsächlich genügen, ob eine
etwaige Datenübermittlung in ein Drittland die Anforderungen der Art. 44 bis
49 DSGVO erfüllt, oder ob der Vertrag als Ganzes zivilrechtlich wirksam ist.
Diese Bewertungen erfordern juristische Sachkunde und den Abgleich mit
Informationen außerhalb des Vertragstexts.

## Einordnung der Ergebnisse

„Gefunden" und „nicht gefunden" sind technische Feststellungen zum
Vorhandensein bestimmter Formulierungen, keine rechtliche Bewertung der
Wirksamkeit oder Angemessenheit des Vertrags. Ein Bericht mit 17 von 17
Treffern ist kein Nachweis eines rechtmäßigen Vertrags, und ein Bericht mit
mehreren fehlenden Punkten ist keine Feststellung eines Rechtsverstoßes,
solange die tatsächliche vertragliche Regelung nicht durch eine dafür
qualifizierte Person geprüft wurde.
