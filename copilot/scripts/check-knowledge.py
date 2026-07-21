#!/usr/bin/env python3
"""Knowledge-base linter — the feedback loop for the co-pilot's knowledge base.

Verifies internal consistency so grounding stays trustworthy. Exit code 0 = clean,
1 = problems found. Run before relying on the KB or after editing it.

Checks:
  1. Every SOURCES.md row marked `download` has a non-empty matching category folder.
  2. Every pattern card has a title + paradigm + "Problem it solves" line.
  3. 08-example-patterns/INDEX.md exists and counts match the cards on disk.
  4. Relative links inside INDEX files resolve to real files.

Usage (from the project root  ie-simulation-copilot/):
    python scripts/check-knowledge.py
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
KNOW = ROOT / "knowledge"
PATTERNS = KNOW / "08-example-patterns"
SUB = ["basicmodels", "models", "sdmodels"]

TITLE_RE = re.compile(r"^#\s*Pattern card\s*[—\-:]\s*(.+?)\s*$", re.M)
PARADIGM_RE = re.compile(r"-\s*\*\*Paradigm:\*\*", re.M)
PROBLEM_RE = re.compile(r"-\s*\*\*Problem it solves:\*\*", re.M)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

problems = []
notes = []


def fail(msg):
    problems.append(msg)


# --- Check 2: pattern cards well-formed ---
card_count = 0
for sub in SUB:
    d = PATTERNS / sub
    if not d.is_dir():
        continue
    for p in sorted(d.glob("*.md")):
        if p.name in {"README.md", "INDEX.md"}:
            continue
        md = p.read_text(encoding="utf-8")
        rel = p.relative_to(ROOT)
        card_count += 1
        if not TITLE_RE.search(md):
            fail(f"card missing title: {rel}")
        if not PARADIGM_RE.search(md):
            fail(f"card missing Paradigm: {rel}")
        if not PROBLEM_RE.search(md):
            fail(f"card missing 'Problem it solves': {rel}")

# --- Check 3: pattern index exists and is current ---
idx = PATTERNS / "INDEX.md"
if not idx.is_file():
    fail("knowledge/08-example-patterns/INDEX.md missing — run build-pattern-index.py")
else:
    m = re.search(r"\*\*(\d+) cards indexed\.\*\*", idx.read_text(encoding="utf-8"))
    if not m:
        fail("INDEX.md has no '<n> cards indexed' marker")
    elif int(m.group(1)) != card_count:
        fail(f"INDEX.md lists {m.group(1)} cards but {card_count} exist — re-run build-pattern-index.py")
    else:
        notes.append(f"pattern index in sync ({card_count} cards)")

# --- Check 1: SOURCES.md download folders non-empty ---
src = ROOT / "SOURCES.md"
if src.is_file():
    cat_dirs = {p.name.split("-", 1)[0]: p for p in KNOW.iterdir() if p.is_dir()}
    for line in src.read_text(encoding="utf-8").splitlines():
        if "download" not in line or not line.strip().startswith("|"):
            continue
        cm = re.search(r"`?(\d\d)[\s-]", line)
        if cm:
            cat = cm.group(1)
            d = cat_dirs.get(cat)
            if d and not any(d.rglob("*")):
                fail(f"SOURCES.md 'download' category {cat} maps to empty folder {d.name}")
    notes.append("SOURCES.md download rows checked")
else:
    notes.append("SOURCES.md not found (skipped check 1)")

# --- Check 4: links in INDEX files resolve ---
for index_file in list(KNOW.rglob("INDEX.md")) + ([KNOW / "INDEX.md"] if (KNOW / "INDEX.md").is_file() else []):
    if not index_file.is_file():
        continue
    base = index_file.parent
    for target in LINK_RE.findall(index_file.read_text(encoding="utf-8")):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        clean = target.split("#")[0]
        if clean and not (base / clean).exists():
            fail(f"broken link in {index_file.relative_to(ROOT)} -> {target}")

# --- Report ---
for n in notes:
    print(f"  ok: {n}")
if problems:
    print(f"\nFAIL: {len(problems)} problem(s):", file=sys.stderr)
    for p in problems:
        print(f"  - {p}", file=sys.stderr)
    sys.exit(1)
print(f"\nOK: knowledge base clean ({card_count} cards).")
