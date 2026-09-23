import json

from avv_checker.matcher import evaluate_requirement
from avv_checker.models import CheckResult
from avv_checker.report import render_html, render_json, render_markdown
from avv_checker.requirements import REQUIREMENTS


def _sample_result() -> CheckResult:
    found_req = next(r for r in REQUIREMENTS if r.requirement_id == "B-vertraulichkeit")
    missing_req = next(r for r in REQUIREMENTS if r.requirement_id == "H-nachweis-audit")

    found_result = evaluate_requirement(
        "Alle Personen haben sich zur Vertraulichkeit verpflichtet.", found_req
    )
    missing_result = evaluate_requirement("Ein Text ohne Bezug.", missing_req)

    return CheckResult(
        document_name="test-vertrag.txt",
        checked_at=CheckResult.now(),
        results=[found_result, missing_result],
        tool_version="1.0.0",
        character_count=42,
    )


def test_render_markdown_contains_key_information():
    md = render_markdown(_sample_result())
    assert "# AVV-Prüfbericht: test-vertrag.txt" in md
    assert "Vertraulichkeitsverpflichtung" in md
    assert "NICHT GEFUNDEN" in md
    assert "Art. 28 Abs. 3 lit. b DSGVO" in md


def test_render_html_marks_missing_and_found_differently():
    html = render_html(_sample_result())
    assert 'class="req found"' in html
    assert 'class="req missing"' in html
    assert "<table" not in html  # bewusst Listendarstellung, keine Tabellen


def test_render_json_roundtrips():
    raw = render_json(_sample_result())
    data = json.loads(raw)
    assert data["document_name"] == "test-vertrag.txt"
    assert data["found_count"] == 1
    assert data["missing_count"] == 1
    ids = {r["requirement_id"] for r in data["results"]}
    assert ids == {"B-vertraulichkeit", "H-nachweis-audit"}
