"""Build a local, searchable text cache of every PDF under knowledge/.

PDFs are invisible to grep, so a fact already taught in e.g. `anylogic-in-3-days.pdf` looks "new"
to a novelty check that only greps the Markdown. This writes one text file per PDF to
`knowledge/.pdf-text/<same relative path>.txt`, with a `=== p. N ===` marker before each page so a
hit can be cited by page. The cache is gitignored: it is the publishers' text, kept only locally,
exactly like the PDFs themselves.

Run:  python scripts/extract-pdf-text.py          (only re-extracts PDFs newer than their cache)
      python scripts/extract-pdf-text.py --force  (rebuild everything)
Then: grep -rn -i "<term>" knowledge/.pdf-text/
Needs PyMuPDF (`pip install pymupdf`).
"""
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("PyMuPDF is required: pip install pymupdf")

ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = ROOT / "knowledge"
CACHE = KNOWLEDGE / ".pdf-text"


def main() -> int:
    force = "--force" in sys.argv[1:]
    pdfs = sorted(p for p in KNOWLEDGE.rglob("*") if p.suffix.lower() == ".pdf" and CACHE not in p.parents)
    written = skipped = failed = 0
    for pdf in pdfs:
        out = CACHE / pdf.relative_to(KNOWLEDGE).with_suffix(".txt")
        if not force and out.exists() and out.stat().st_mtime >= pdf.stat().st_mtime:
            skipped += 1
            continue
        try:
            with fitz.open(pdf) as doc:
                pages = [f"=== p. {i} ===\n{page.get_text()}" for i, page in enumerate(doc, start=1)]
        except Exception as e:  # a damaged or encrypted PDF should not stop the rest
            print(f"FAIL {pdf.relative_to(ROOT)}: {e}", file=sys.stderr)
            failed += 1
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(pages), encoding="utf-8")
        written += 1
    print(f"{len(pdfs)} PDFs: {written} extracted, {skipped} up to date, {failed} failed -> {CACHE.relative_to(ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
