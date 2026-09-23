"""Kommandozeilenschnittstelle für avv-checker."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .extract import ExtractionError, extract_text
from .matcher import evaluate
from .models import CheckResult
from .report import render_html, render_json, render_markdown

FORMAT_RENDERERS = {
    "md": render_markdown,
    "html": render_html,
    "json": render_json,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="avv-checker",
        description=(
            "Wortlautbasierte Prüfung eines Auftragsverarbeitungsvertrags "
            "(AVV) auf die Pflichtinhalte nach Art. 28 Abs. 2 bis 4 DSGVO."
        ),
    )
    parser.add_argument(
        "datei", help="Zu prüfende Vertragsdatei (.txt, .md, .docx oder .pdf)"
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("."),
        metavar="VERZEICHNIS",
        help="Zielverzeichnis für die Berichtsdateien (Standard: aktuelles Verzeichnis)",
    )
    parser.add_argument(
        "--format",
        default="md,html,json",
        help="Komma-getrennte Liste aus md, html, json (Standard: alle drei)",
    )
    parser.add_argument(
        "--basename",
        default="avv-bericht",
        help="Basisname der erzeugten Dateien ohne Endung (Standard: avv-bericht)",
    )
    parser.add_argument(
        "--version", action="version", version=f"avv-checker {__version__}"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    formats = [f.strip() for f in args.format.split(",") if f.strip()]
    unknown = [f for f in formats if f not in FORMAT_RENDERERS]
    if unknown:
        parser.error(f"Unbekannte(s) Format(e): {', '.join(unknown)}")

    try:
        text = extract_text(args.datei)
    except ExtractionError as exc:
        print(f"Konnte Dokument nicht lesen: {exc}", file=sys.stderr)
        return 1

    results = evaluate(text)
    result = CheckResult(
        document_name=Path(args.datei).name,
        checked_at=CheckResult.now(),
        results=results,
        tool_version=__version__,
        character_count=len(text),
    )

    args.out.mkdir(parents=True, exist_ok=True)
    extensions = {"md": "md", "html": "html", "json": "json"}
    for fmt in formats:
        content = FORMAT_RENDERERS[fmt](result)
        out_path = args.out / f"{args.basename}.{extensions[fmt]}"
        out_path.write_text(content, encoding="utf-8")
        print(f"geschrieben: {out_path}")

    print(f"Gefunden: {result.found_count} von {len(result.results)}")
    if result.missing_results:
        print("Nicht gefunden:")
        for r in result.missing_results:
            print(f"  - {r.requirement.title} ({r.requirement.legal_reference})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
