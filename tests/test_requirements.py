import re

from avv_checker.requirements import (
    GROUP_GRUNDANGABEN,
    GROUP_PFLICHTEN,
    GROUP_SUBVERARBEITER,
    REQUIREMENTS,
    by_group,
)


def test_seventeen_requirements_defined():
    assert len(REQUIREMENTS) == 17


def test_requirement_ids_are_unique():
    ids = [r.requirement_id for r in REQUIREMENTS]
    assert len(ids) == len(set(ids))


def test_every_requirement_has_at_least_one_pattern():
    for req in REQUIREMENTS:
        assert len(req.patterns) >= 1, req.requirement_id


def test_every_pattern_compiles():
    for req in REQUIREMENTS:
        for pattern in req.patterns:
            re.compile(pattern)  # wirft bei ungültigem Muster


def test_every_requirement_has_legal_reference_and_description():
    for req in REQUIREMENTS:
        assert req.legal_reference.strip()
        assert req.description.strip()
        assert req.title.strip()


def test_groups_are_one_of_the_three_known_groups():
    known = {GROUP_GRUNDANGABEN, GROUP_PFLICHTEN, GROUP_SUBVERARBEITER}
    for req in REQUIREMENTS:
        assert req.group in known


def test_by_group_counts_match_statute_structure():
    grouped = by_group()
    assert len(grouped[GROUP_GRUNDANGABEN]) == 6
    assert len(grouped[GROUP_PFLICHTEN]) == 8
    assert len(grouped[GROUP_SUBVERARBEITER]) == 3
