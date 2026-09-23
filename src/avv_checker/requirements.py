"""Pflichtinhalte eines Auftragsverarbeitungsvertrags nach Art. 28 Abs. 2
bis 4 DSGVO, mit Suchmustern zur wortlautbasierten Erkennung.

Die Gliederung folgt dem Gesetzestext: die sechs Grundangaben aus Art. 28
Abs. 3 Satz 1 (Gegenstand, Dauer, Art und Zweck der Verarbeitung, Art der
Daten, Kategorien betroffener Personen, Pflichten und Rechte des
Verantwortlichen), die acht Pflichten des Auftragsverarbeiters aus Art. 28
Abs. 3 Satz 2 Buchstabe a bis h, sowie die drei Bedingungen für die
Einbindung weiterer Auftragsverarbeiter aus Art. 28 Abs. 2 und 4.

Die Suchmuster sind von Hand aus gängigen deutschsprachigen AVV-Formulierungen
zusammengestellt. Sie sind bewusst als Wortlaut-Heuristik angelegt: ein
Treffer zeigt, dass ein Vertrag eine zum jeweiligen Pflichtinhalt passende
Formulierung enthält, nicht, dass diese Formulierung inhaltlich ausreicht.
Andere, hier nicht erfasste Formulierungen können denselben Pflichtinhalt
abdecken, ohne erkannt zu werden; siehe METHODIK.md.
"""

from __future__ import annotations

from dataclasses import dataclass

Group = str

GROUP_GRUNDANGABEN: Group = "Grundangaben (Art. 28 Abs. 3 Satz 1 DSGVO)"
GROUP_PFLICHTEN: Group = "Pflichten des Auftragsverarbeiters (Art. 28 Abs. 3 Satz 2 DSGVO)"
GROUP_SUBVERARBEITER: Group = "Weitere Auftragsverarbeiter (Art. 28 Abs. 2 und 4 DSGVO)"


@dataclass(frozen=True)
class Requirement:
    requirement_id: str
    legal_reference: str
    group: Group
    title: str
    description: str
    patterns: tuple[str, ...]


REQUIREMENTS: tuple[Requirement, ...] = (
    Requirement(
        requirement_id="G1-gegenstand",
        legal_reference="Art. 28 Abs. 3 Satz 1 DSGVO",
        group=GROUP_GRUNDANGABEN,
        title="Gegenstand der Verarbeitung",
        description=(
            "Der Vertrag muss festlegen, was konkret Gegenstand der "
            "Verarbeitung ist."
        ),
        patterns=(
            r"gegenstand\s+(der|des)\s+(verarbeitung|vertrags|auftrags)",
            r"gegenstand\s+und\s+dauer",
        ),
    ),
    Requirement(
        requirement_id="G2-dauer",
        legal_reference="Art. 28 Abs. 3 Satz 1 DSGVO",
        group=GROUP_GRUNDANGABEN,
        title="Dauer der Verarbeitung",
        description="Der Vertrag muss die Dauer der Verarbeitung festlegen.",
        patterns=(
            r"dauer\s+der\s+verarbeitung",
            r"dauer\s+dies(es|er)\s+(vertrag|vereinbarung)",
            r"laufzeit\s+dies(es|er)\s+(vertrag|vereinbarung)",
        ),
    ),
    Requirement(
        requirement_id="G3-art-und-zweck",
        legal_reference="Art. 28 Abs. 3 Satz 1 DSGVO",
        group=GROUP_GRUNDANGABEN,
        title="Art und Zweck der Verarbeitung",
        description="Der Vertrag muss Art und Zweck der Verarbeitung festlegen.",
        patterns=(
            r"art\s+und\s+zweck\s+der\s+verarbeitung",
            r"zweck\s+der\s+verarbeitung",
        ),
    ),
    Requirement(
        requirement_id="G4-art-der-daten",
        legal_reference="Art. 28 Abs. 3 Satz 1 DSGVO",
        group=GROUP_GRUNDANGABEN,
        title="Art der personenbezogenen Daten",
        description=(
            "Der Vertrag muss festlegen, welche Art beziehungsweise welche "
            "Kategorien personenbezogener Daten verarbeitet werden."
        ),
        patterns=(
            r"art\s+der\s+(personenbezogenen\s+)?daten",
            r"kategorien\s+(von\s+)?personenbezogene[rn]\s+daten",
            r"arten\s+personenbezogener\s+daten",
        ),
    ),
    Requirement(
        requirement_id="G5-kategorien-betroffener",
        legal_reference="Art. 28 Abs. 3 Satz 1 DSGVO",
        group=GROUP_GRUNDANGABEN,
        title="Kategorien betroffener Personen",
        description="Der Vertrag muss die Kategorien betroffener Personen festlegen.",
        patterns=(
            r"kategorien\s+betroffener\s+personen",
            r"kreis\s+der\s+betroffenen",
        ),
    ),
    Requirement(
        requirement_id="G6-pflichten-rechte-verantwortlicher",
        legal_reference="Art. 28 Abs. 3 Satz 1 DSGVO",
        group=GROUP_GRUNDANGABEN,
        title="Pflichten und Rechte des Verantwortlichen",
        description=(
            "Der Vertrag muss die Pflichten und Rechte des Verantwortlichen "
            "(Auftraggebers) festlegen."
        ),
        patterns=(
            r"pflichten\s+und\s+rechte\s+des\s+verantwortlichen",
            r"rechte\s+und\s+pflichten\s+des\s+(verantwortlichen|auftraggebers)",
        ),
    ),
    Requirement(
        requirement_id="A-weisungsgebunden",
        legal_reference="Art. 28 Abs. 3 lit. a DSGVO",
        group=GROUP_PFLICHTEN,
        title="Verarbeitung nur auf dokumentierte Weisung",
        description=(
            "Der Auftragsverarbeiter darf personenbezogene Daten nur auf "
            "dokumentierte Weisung des Verantwortlichen verarbeiten."
        ),
        patterns=(
            r"nur\s+auf\s+(dokumentierte[rn]?\s+)?weisung",
            r"auf\s+dokumentierte\s+weisung",
            r"im\s+rahmen\s+der\s+weisungen\s+des\s+verantwortlichen",
            r"weisungsgebunden",
        ),
    ),
    Requirement(
        requirement_id="B-vertraulichkeit",
        legal_reference="Art. 28 Abs. 3 lit. b DSGVO",
        group=GROUP_PFLICHTEN,
        title="Vertraulichkeitsverpflichtung der befugten Personen",
        description=(
            "Personen, die zur Verarbeitung befugt sind, müssen sich zur "
            "Vertraulichkeit verpflichtet haben oder einer gesetzlichen "
            "Verschwiegenheitspflicht unterliegen."
        ),
        patterns=(
            r"zur\s+vertraulichkeit\s+verpflichtet",
            r"verschwiegenheitspflicht",
            r"vertraulichkeitsverpflichtung",
        ),
    ),
    Requirement(
        requirement_id="C-tom-art32",
        legal_reference="Art. 28 Abs. 3 lit. c DSGVO",
        group=GROUP_PFLICHTEN,
        title="Technische und organisatorische Maßnahmen (Art. 32 DSGVO)",
        description=(
            "Der Vertrag muss vorsehen, dass der Auftragsverarbeiter die "
            "nach Art. 32 DSGVO erforderlichen Maßnahmen ergreift, "
            "üblicherweise durch Bezug auf eine TOM-Anlage."
        ),
        patterns=(
            r"art(ikel)?\.?\s*32",
            r"technische[n]?\s+und\s+organisatorische[n]?\s+maßnahmen",
            r"\btom\b",
        ),
    ),
    Requirement(
        requirement_id="D-bedingungen-subav",
        legal_reference="Art. 28 Abs. 3 lit. d DSGVO",
        group=GROUP_PFLICHTEN,
        title="Einhaltung der Bedingungen für weitere Auftragsverarbeiter",
        description=(
            "Der Vertrag muss auf die Bedingungen für die Einbindung "
            "weiterer Auftragsverarbeiter (Unterauftragsverarbeiter) "
            "verweisen."
        ),
        patterns=(
            r"weitere[nr]?\s+auftragsverarbeiter",
            r"unterauftragsverarbeiter",
            r"subunternehmer",
            r"sub-auftragsverarbeiter",
        ),
    ),
    Requirement(
        requirement_id="E-unterstuetzung-betroffenenrechte",
        legal_reference="Art. 28 Abs. 3 lit. e DSGVO",
        group=GROUP_PFLICHTEN,
        title="Unterstützung bei der Wahrnehmung von Betroffenenrechten",
        description=(
            "Der Auftragsverarbeiter muss den Verantwortlichen mit "
            "geeigneten Maßnahmen dabei unterstützen, Anträge auf "
            "Betroffenenrechte zu beantworten."
        ),
        patterns=(
            r"rechte\s+der\s+betroffenen\s+person",
            r"betroffenenrechte",
            r"anträge?\s+auf\s+(wahrnehmung\s+der\s+)?rechte",
            r"unterstützt\s+den\s+verantwortlichen.{0,80}betroffenen",
        ),
    ),
    Requirement(
        requirement_id="F-unterstuetzung-art32-36",
        legal_reference="Art. 28 Abs. 3 lit. f DSGVO",
        group=GROUP_PFLICHTEN,
        title="Unterstützung bei Pflichten nach Art. 32 bis 36 DSGVO",
        description=(
            "Der Auftragsverarbeiter muss den Verantwortlichen bei der "
            "Einhaltung der Pflichten aus Art. 32 bis 36 DSGVO unterstützen, "
            "insbesondere bei der Meldung von Datenschutzverletzungen."
        ),
        patterns=(
            r"art(ikel)?\.?\s*3[2-6]",
            r"meldung\s+von\s+(datenschutz-?)?verletzungen",
            r"datenschutzverletzung",
            r"meldepflicht",
        ),
    ),
    Requirement(
        requirement_id="G-loeschung-rueckgabe",
        legal_reference="Art. 28 Abs. 3 lit. g DSGVO",
        group=GROUP_PFLICHTEN,
        title="Löschung oder Rückgabe der Daten nach Vertragsende",
        description=(
            "Nach Wahl des Verantwortlichen müssen alle personenbezogenen "
            "Daten nach Abschluss der Verarbeitungsdienstleistung gelöscht "
            "oder zurückgegeben werden."
        ),
        patterns=(
            # "gibt ... zurück" statt "gibt zurück", da deutsche trennbare
            # Verben im Nebensatz auseinandergezogen werden können.
            r"löscht\s+oder\s+gibt\b.{0,160}zurück",
            r"löschung\s+oder\s+rückgabe",
            r"nach\s+(beendigung|abschluss|vertragsende).{0,120}(löscht|löschung|zurückgibt|rückgabe)",
            r"(löscht|löschung).{0,120}(nach\s+(beendigung|abschluss|vertragsende))",
            r"rückgabe\s+der\s+(personenbezogenen\s+)?daten",
        ),
    ),
    Requirement(
        requirement_id="H-nachweis-audit",
        legal_reference="Art. 28 Abs. 3 lit. h DSGVO",
        group=GROUP_PFLICHTEN,
        title="Nachweispflichten und Kontroll-/Auditrechte",
        description=(
            "Der Auftragsverarbeiter muss dem Verantwortlichen Nachweise "
            "der Einhaltung seiner Pflichten bereitstellen und Kontrollen "
            "beziehungsweise Audits ermöglichen."
        ),
        patterns=(
            r"nachweis\s+der\s+einhaltung",
            r"kontrollrechte",
            r"\baudit",
            r"inspektionen",
            r"überprüfungen.{0,40}(ermöglicht|durchführen)",
        ),
    ),
    Requirement(
        requirement_id="S1-vorherige-genehmigung",
        legal_reference="Art. 28 Abs. 2 DSGVO",
        group=GROUP_SUBVERARBEITER,
        title="Vorherige schriftliche Genehmigung für weitere Auftragsverarbeiter",
        description=(
            "Der Auftragsverarbeiter darf keinen weiteren Auftragsverarbeiter "
            "ohne vorherige gesonderte oder allgemeine schriftliche "
            "Genehmigung des Verantwortlichen einsetzen."
        ),
        patterns=(
            # ".{0,100}" statt "\s+", da zwischen "vorherige" und
            # "Genehmigung" in der Praxis oft weitere Wörter stehen
            # ("vorherige, gesonderte oder allgemeine schriftliche
            # Genehmigung").
            r"vorherige[nr]?\b.{0,100}(zustimmung|genehmigung)",
            r"schriftliche[n]?\s+zustimmung",
            r"vorab.{0,30}(zustimm|genehmig)",
        ),
    ),
    Requirement(
        requirement_id="S2-informationspflicht-widerspruch",
        legal_reference="Art. 28 Abs. 2 Satz 2 DSGVO",
        group=GROUP_SUBVERARBEITER,
        title="Informationspflicht bei Änderungen und Widerspruchsrecht",
        description=(
            "Bei einer allgemeinen Genehmigung muss der Auftragsverarbeiter "
            "über beabsichtigte Änderungen informieren und dem "
            "Verantwortlichen die Möglichkeit zum Widerspruch geben."
        ),
        patterns=(
            r"widerspruchsrecht",
            r"informiert.{0,60}(beabsichtigte[n]?\s+)?änderung",
            r"widerspruch.{0,40}einzulegen",
        ),
    ),
    Requirement(
        requirement_id="S3-gleiche-pflichten-weitergeben",
        legal_reference="Art. 28 Abs. 4 DSGVO",
        group=GROUP_SUBVERARBEITER,
        title="Weitergabe derselben Datenschutzpflichten an Sub-Auftragsverarbeiter",
        description=(
            "Setzt der Auftragsverarbeiter einen weiteren Auftragsverarbeiter "
            "ein, müssen diesem dieselben Datenschutzpflichten auferlegt "
            "werden wie im Vertrag mit dem Verantwortlichen."
        ),
        patterns=(
            r"dieselben\s+(datenschutz-?)?pflichten",
            r"gleichen\s+pflichten\s+aufer(legt|legen)",
            r"selben\s+vertraglichen\s+pflichten",
        ),
    ),
)


def by_group() -> dict[Group, list[Requirement]]:
    grouped: dict[Group, list[Requirement]] = {}
    for req in REQUIREMENTS:
        grouped.setdefault(req.group, []).append(req)
    return grouped
