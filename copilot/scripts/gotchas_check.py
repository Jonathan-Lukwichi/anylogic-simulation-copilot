"""Consistency check for knowledge/01-anylogic-core/anylogic-gotchas.md.

Flags: an entry number used twice or skipped; an entry with no quick-lookup row; a lookup row that
names a missing entry; a "Card:" pointer to a card that does not exist. `cards` is the set of card
paths relative to knowledge/08-example-patterns, without ".md" (e.g. "basicmodels/hold").
"""
import re

HEADING = re.compile(r"^## G(\d+) — ", re.M)
LOOKUP = re.compile(r"^## Quick lookup.*?\n(.*?)\n---", re.M | re.S)
CARD_SPAN = re.compile(r"\bCards?:(.*?)(?=\*\*|\n\n|\n## |\Z)", re.S)
TICKED = re.compile(r"`([^`]+)`")
SLUG = re.compile(r"^(?:[a-z0-9]+/)?[a-z0-9]+(?:-[a-z0-9]+)*$")


def check_gotchas(text, cards):
    problems = []
    numbers = [int(n) for n in HEADING.findall(text)]
    seen = set()
    for n in numbers:
        if n in seen:
            problems.append(f"G{n} heading appears more than once")
        seen.add(n)
    for n in range(1, max(seen, default=0) + 1):
        if n not in seen:
            problems.append(f"G{n} is missing from the numbering")

    m = LOOKUP.search(text)
    rows = [line for line in (m.group(1) if m else "").splitlines() if line.startswith("|")]
    listed = {int(n) for row in rows for n in re.findall(r"\bG(\d+)\b", row.rsplit("|", 2)[-2])}
    for n in sorted(seen - listed):
        problems.append(f"G{n} has no quick-lookup row")
    for n in sorted(listed - seen):
        problems.append(f"quick-lookup row points to G{n}, which has no entry")

    basenames = {c.rsplit("/", 1)[-1] for c in cards}
    for span in CARD_SPAN.findall(text):
        for token in TICKED.findall(span):
            ref = token.removesuffix(".md")
            if not SLUG.match(ref):
                continue
            known = ref in cards if "/" in ref else ref in basenames
            if not known:
                problems.append(f"card reference `{token}` matches no card")
    return problems


if __name__ == "__main__":
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    patterns = root / "knowledge" / "08-example-patterns"
    card_set = {str(p.relative_to(patterns).with_suffix("")).replace("\\", "/")
                for p in patterns.glob("*/*.md") if p.name not in {"README.md", "INDEX.md"}}
    found = check_gotchas((root / "knowledge" / "01-anylogic-core" / "anylogic-gotchas.md")
                          .read_text(encoding="utf-8"), card_set)
    print("\n".join(found) or "gotchas file consistent")
    sys.exit(1 if found else 0)
