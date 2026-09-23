from pathlib import Path

from avv_checker.extract import extract_text
from avv_checker.matcher import evaluate, evaluate_requirement
from avv_checker.requirements import REQUIREMENTS

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _requirement(requirement_id: str):
    return next(r for r in REQUIREMENTS if r.requirement_id == requirement_id)


def test_finds_requirement_in_matching_text():
    req = _requirement("B-vertraulichkeit")
    text = "Alle Mitarbeitenden haben sich zur Vertraulichkeit verpflichtet."
    result = evaluate_requirement(text, req)
    assert result.found is True
    assert result.excerpt is not None
    assert "Vertraulichkeit" in result.excerpt


def test_missing_requirement_returns_not_found_without_excerpt():
    req = _requirement("H-nachweis-audit")
    text = "Dieser Vertrag regelt nur die Vergütung der Dienstleistung."
    result = evaluate_requirement(text, req)
    assert result.found is False
    assert result.excerpt is None
    assert result.matched_pattern is None


def test_matching_is_case_insensitive():
    req = _requirement("C-tom-art32")
    text = "der ARTRAGNEHMER trifft ART. 32 maßnahmen"  # bewusst unregelmäßige Groß-/Kleinschreibung
    result = evaluate_requirement(text, req)
    assert result.found is True


def test_survives_hard_line_wraps_across_a_gap_pattern():
    # Regressionstest: ".{0,N}"-Lücken in Mustern dürfen nicht an
    # Zeilenumbrüchen scheitern, wie sie bei aus PDF/DOCX extrahiertem Text
    # häufig vorkommen. evaluate() normalisiert dafür die Leerzeichen.
    req = _requirement("G-loeschung-rueckgabe")
    text = (
        "Nach Wahl des Auftraggebers löscht oder gibt der Auftragsverarbeiter\n"
        "alle personenbezogenen Daten nach Abschluss der Erbringung der\n"
        "Verarbeitungsleistungen zurück."
    )
    results = evaluate(text)
    result = next(r for r in results if r.requirement.requirement_id == req.requirement_id)
    assert result.found is True


def test_complete_sample_contract_covers_all_requirements():
    text = extract_text(FIXTURES / "sample_avv_complete.txt")
    results = evaluate(text)
    missing = [r.requirement.requirement_id for r in results if not r.found]
    assert missing == []


def test_incomplete_sample_contract_misses_exactly_the_expected_four():
    text = extract_text(FIXTURES / "sample_avv_incomplete.txt")
    results = evaluate(text)
    missing = {r.requirement.requirement_id for r in results if not r.found}
    assert missing == {
        "G5-kategorien-betroffener",
        "G-loeschung-rueckgabe",
        "H-nachweis-audit",
        "S2-informationspflicht-widerspruch",
    }
