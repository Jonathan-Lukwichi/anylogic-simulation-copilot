"""Tests for the gotchas-file consistency check.

The gotchas file is the co-pilot's pitfall lookup: a reader finds an entry through the quick-lookup
table and then follows its "Card:" pointer. A row that points at a missing entry, an entry nobody can
find from the table, a duplicated number, or a card that does not exist each sends the reader the
wrong way, so the check must flag all four.

Run: python -m pytest scripts/test_gotchas_check.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.gotchas_check import check_gotchas  # noqa: E402

CARDS = {"basicmodels/hold", "videos/flowchart-block-animation-binding"}


def doc(lookup_rows, entries):
    return (
        "# Gotchas\n\n## Quick lookup — find the entry by what you see\n\n"
        "| You see… | Entry |\n|---|---|\n" + "".join(lookup_rows) + "\n---\n\n" + "".join(entries)
    )


G1 = "## G1 — First trap\n**Cause:** x.\n**Fix:** y. Card: `hold`.\n\n"
G2 = "## G2 — Second trap\n**Cause:** x.\n**Fix:** y. Cards: `videos/flowchart-block-animation-binding`,\n`basicmodels/hold`.\n\n"
ROWS = ["| first symptom | G1 |\n", "| second symptom | G2, then G1 |\n"]


def test_consistent_file_passes():
    assert check_gotchas(doc(ROWS, [G1, G2]), CARDS) == []


def test_duplicate_entry_number_is_flagged():
    problems = check_gotchas(doc(ROWS, [G1, G2, G2]), CARDS)
    assert any("G2" in p and "more than once" in p for p in problems)


def test_gap_in_numbering_is_flagged():
    g3 = "## G3 — Third\n**Fix:** z.\n\n"
    problems = check_gotchas(doc(ROWS + ["| third | G3 |\n"], [G1, g3]), CARDS)
    assert any("G2" in p and "missing" in p for p in problems)


def test_entry_without_lookup_row_is_flagged():
    problems = check_gotchas(doc(ROWS[:1], [G1, G2]), CARDS)
    assert any("G2" in p and "lookup" in p for p in problems)


def test_lookup_row_to_missing_entry_is_flagged():
    problems = check_gotchas(doc(ROWS + ["| ghost | G9 |\n"], [G1, G2]), CARDS)
    assert any("G9" in p for p in problems)


def test_unknown_card_is_flagged():
    bad = "## G2 — Second trap\n**Fix:** y. Card: `no-such-card`.\n\n"
    problems = check_gotchas(doc(ROWS, [G1, bad]), CARDS)
    assert any("no-such-card" in p for p in problems)


def test_card_reference_with_wrong_folder_is_flagged():
    bad = "## G2 — Second trap\n**Fix:** y. Card: `models/hold`.\n\n"
    problems = check_gotchas(doc(ROWS, [G1, bad]), CARDS)
    assert any("models/hold" in p for p in problems)


def test_code_in_backticks_after_card_is_not_mistaken_for_a_card():
    ok = "## G2 — Second trap\n**Fix:** y. Card: `hold` — call `recalculateConditions()` there.\n\n"
    assert check_gotchas(doc(ROWS, [G1, ok]), CARDS) == []
