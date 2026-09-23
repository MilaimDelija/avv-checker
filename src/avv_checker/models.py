"""Datenmodelle für ein Prüfungsergebnis."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from .requirements import Requirement


@dataclass(frozen=True)
class RequirementResult:
    requirement: Requirement
    found: bool
    matched_pattern: str | None = None
    excerpt: str | None = None


@dataclass
class CheckResult:
    document_name: str
    checked_at: datetime
    results: list[RequirementResult] = field(default_factory=list)
    tool_version: str = "1.0.0"
    character_count: int = 0

    @property
    def found_count(self) -> int:
        return sum(1 for r in self.results if r.found)

    @property
    def missing_count(self) -> int:
        return sum(1 for r in self.results if not r.found)

    @property
    def missing_results(self) -> list[RequirementResult]:
        return [r for r in self.results if not r.found]

    @staticmethod
    def now() -> datetime:
        return datetime.now(timezone.utc)
