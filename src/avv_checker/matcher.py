"""Abgleich eines Vertragstexts gegen die Pflichtinhalte aus requirements.py.

Der Text wird vor dem Abgleich auf einzelne Leerzeichen normalisiert
(Zeilenumbrüche eingeschlossen). Ohne diesen Schritt würden Suchmuster, die
mit ".{0,N}" eine Lücke zwischen zwei Wörtern überbrücken, an jedem
Zeilenumbruch scheitern, da "." in Python standardmäßig keine Zeilenumbrüche
trifft — bei aus PDF oder DOCX extrahiertem, hart umgebrochenem Text wäre
das sonst ein häufiger Fehltreffer.
"""

from __future__ import annotations

import re

from .models import RequirementResult
from .requirements import REQUIREMENTS, Requirement

EXCERPT_CONTEXT_CHARS = 90


def _normalise_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _make_excerpt(text: str, start: int, end: int) -> str:
    lower = max(0, start - EXCERPT_CONTEXT_CHARS)
    upper = min(len(text), end + EXCERPT_CONTEXT_CHARS)
    prefix = "…" if lower > 0 else ""
    suffix = "…" if upper < len(text) else ""
    return prefix + text[lower:upper].strip() + suffix


def evaluate_requirement(text: str, requirement: Requirement) -> RequirementResult:
    """Prüft text gegen einen einzelnen Pflichtinhalt.

    text wird intern auf einzelne Leerzeichen normalisiert (siehe
    Moduldokumentation), sodass diese Funktion unabhängig davon korrekt
    arbeitet, ob der Aufrufer das schon getan hat.
    """
    normalised = _normalise_whitespace(text)
    for pattern in requirement.patterns:
        match = re.search(pattern, normalised, flags=re.IGNORECASE)
        if match:
            excerpt = _make_excerpt(normalised, match.start(), match.end())
            return RequirementResult(
                requirement=requirement,
                found=True,
                matched_pattern=pattern,
                excerpt=excerpt,
            )
    return RequirementResult(requirement=requirement, found=False)


def evaluate(text: str) -> list[RequirementResult]:
    """Prüft text gegen alle bekannten Pflichtinhalte.

    Die Reihenfolge des Ergebnisses folgt der Definitionsreihenfolge in
    requirements.REQUIREMENTS (Grundangaben, dann Pflichten des
    Auftragsverarbeiters, dann Regelungen zu weiteren
    Auftragsverarbeitern).
    """
    return [evaluate_requirement(text, req) for req in REQUIREMENTS]
