#!/usr/bin/env python3
"""Prüft die beiden mitgelieferten Beispielverträge und schreibt die Berichte
nach demo_output/ im Projektverzeichnis."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from avv_checker.extract import extract_text  # noqa: E402
from avv_checker.matcher import evaluate  # noqa: E402
from avv_checker.models import CheckResult  # noqa: E402
from avv_checker.report import render_html, render_json, render_markdown  # noqa: E402


def run_one(sample_path: Path, out_dir: Path, basename: str) -> CheckResult:
    text = extract_text(sample_path)
    results = evaluate(text)
    result = CheckResult(
        document_name=sample_path.name,
        checked_at=CheckResult.now(),
        results=results,
        character_count=len(text),
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{basename}.md").write_text(render_markdown(result), encoding="utf-8")
    (out_dir / f"{basename}.html").write_text(render_html(result), encoding="utf-8")
    (out_dir / f"{basename}.json").write_text(render_json(result), encoding="utf-8")
    return result


def main() -> int:
    out_dir = REPO_ROOT / "demo_output"
    fixtures = REPO_ROOT / "tests" / "fixtures"

    for sample_name, basename in (
        ("sample_avv_complete.txt", "bericht-vollstaendig"),
        ("sample_avv_incomplete.txt", "bericht-unvollstaendig"),
    ):
        result = run_one(fixtures / sample_name, out_dir, basename)
        print(f"=== {sample_name} ===")
        print(f"Gefunden: {result.found_count} von {len(result.results)}")
        if result.missing_results:
            print("Nicht gefunden:")
            for r in result.missing_results:
                print(f"  - {r.requirement.title} ({r.requirement.legal_reference})")
        print()

    print(f"Berichte geschrieben nach: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
