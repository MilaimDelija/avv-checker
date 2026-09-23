"""Aufbereitung eines CheckResult als Markdown-, HTML- oder JSON-Bericht."""

from __future__ import annotations

import json
from html import escape

from .models import CheckResult, RequirementResult
from .requirements import REQUIREMENTS

INTRO_TEXT = (
    "Dieser Bericht listet, welche der in Art. 28 Abs. 2 bis 4 DSGVO "
    "vorgeschriebenen Vertragsinhalte im geprüften Dokument anhand "
    "typischer Formulierungen auffindbar waren. Ein Treffer zeigt nur, "
    "dass eine passende Formulierung vorhanden ist, nicht, dass sie "
    "inhaltlich ausreicht; das Fehlen eines Treffers zeigt nicht sicher, "
    "dass der Punkt im Vertrag ungeregelt ist, wenn eine unübliche "
    "Formulierung verwendet wurde. Der Bericht ersetzt keine rechtliche "
    "Prüfung. Methodik und Grenzen stehen in METHODIK.md."
)


def _group_order() -> list[str]:
    seen: list[str] = []
    for req in REQUIREMENTS:
        if req.group not in seen:
            seen.append(req.group)
    return seen


def _grouped_results(result: CheckResult) -> dict[str, list[RequirementResult]]:
    grouped: dict[str, list[RequirementResult]] = {g: [] for g in _group_order()}
    for r in result.results:
        grouped[r.requirement.group].append(r)
    return grouped


def render_markdown(result: CheckResult) -> str:
    lines: list[str] = []
    lines.append(f"# AVV-Prüfbericht: {result.document_name}")
    lines.append("")
    lines.append(INTRO_TEXT)
    lines.append("")
    lines.append(
        f"Geprüft am (UTC): {result.checked_at.isoformat()}  \n"
        f"Umfang des Dokuments: {result.character_count} Zeichen  \n"
        f"Gefunden: {result.found_count} von {len(result.results)}  \n"
        f"Werkzeugversion: avv-checker {result.tool_version}"
    )
    lines.append("")

    grouped = _grouped_results(result)
    for group, entries in grouped.items():
        lines.append(f"## {group}")
        lines.append("")
        for r in entries:
            status = "gefunden" if r.found else "NICHT GEFUNDEN"
            lines.append(f"### {r.requirement.title} — {status}")
            lines.append("")
            lines.append(f"Rechtsgrundlage: {r.requirement.legal_reference}")
            lines.append("")
            lines.append(r.requirement.description)
            if r.found and r.excerpt:
                lines.append("")
                lines.append(f"Fundstelle: „{r.excerpt}“")
            lines.append("")

    return "\n".join(lines)


def render_html(result: CheckResult) -> str:
    grouped = _grouped_results(result)
    parts: list[str] = []
    parts.append(
        "<!DOCTYPE html><html lang=\"de\"><head><meta charset=\"utf-8\">"
        f"<title>AVV-Prüfbericht: {escape(result.document_name)}</title>"
        "<style>"
        "body{font-family:Georgia,'Times New Roman',serif;max-width:52rem;"
        "margin:2rem auto;padding:0 1.25rem;color:#1a1a1a;"
        "background:#fbfaf7;line-height:1.55;}"
        "h1{font-size:1.6rem;border-bottom:1px solid #999;padding-bottom:0.4rem;}"
        "h2{font-size:1.2rem;margin-top:2rem;border-bottom:1px solid #ccc;"
        "padding-bottom:0.2rem;}"
        "h3{font-size:1.02rem;margin-bottom:0.15rem;}"
        ".meta{font-size:0.92rem;color:#333;}"
        ".req{border-left:4px solid #4a4a4a;padding-left:0.8rem;"
        "margin-bottom:1rem;}"
        ".req.missing{border-left-color:#7a2020;}"
        ".req.found{border-left-color:#2f5a2f;}"
        ".status{font-weight:600;}"
        ".status.missing{color:#7a2020;}"
        ".status.found{color:#2f5a2f;}"
        ".excerpt{font-style:italic;color:#333;}"
        ".legalref{color:#555;font-size:0.88rem;}"
        "</style></head><body>"
    )
    parts.append(f"<h1>AVV-Prüfbericht: {escape(result.document_name)}</h1>")
    parts.append(f"<p>{escape(INTRO_TEXT)}</p>")
    parts.append(
        "<p class=\"meta\">"
        f"Geprüft am (UTC): {escape(result.checked_at.isoformat())}<br>"
        f"Umfang des Dokuments: {result.character_count} Zeichen<br>"
        f"Gefunden: {result.found_count} von {len(result.results)}<br>"
        f"Werkzeugversion: avv-checker {escape(result.tool_version)}"
        "</p>"
    )

    for group, entries in grouped.items():
        parts.append(f"<h2>{escape(group)}</h2>")
        for r in entries:
            css_class = "found" if r.found else "missing"
            status_text = "gefunden" if r.found else "nicht gefunden"
            parts.append(f"<div class=\"req {css_class}\">")
            parts.append(
                f"<h3>{escape(r.requirement.title)} — "
                f"<span class=\"status {css_class}\">{status_text}</span></h3>"
            )
            parts.append(
                f"<p class=\"legalref\">{escape(r.requirement.legal_reference)}</p>"
            )
            parts.append(f"<p>{escape(r.requirement.description)}</p>")
            if r.found and r.excerpt:
                parts.append(f"<p class=\"excerpt\">Fundstelle: „{escape(r.excerpt)}“</p>")
            parts.append("</div>")

    parts.append("</body></html>")
    return "".join(parts)


def render_json(result: CheckResult) -> str:
    data = {
        "document_name": result.document_name,
        "checked_at": result.checked_at.isoformat(),
        "tool_version": result.tool_version,
        "character_count": result.character_count,
        "found_count": result.found_count,
        "missing_count": result.missing_count,
        "results": [
            {
                "requirement_id": r.requirement.requirement_id,
                "legal_reference": r.requirement.legal_reference,
                "group": r.requirement.group,
                "title": r.requirement.title,
                "description": r.requirement.description,
                "found": r.found,
                "matched_pattern": r.matched_pattern,
                "excerpt": r.excerpt,
            }
            for r in result.results
        ],
    }
    return json.dumps(data, indent=2, ensure_ascii=False)
