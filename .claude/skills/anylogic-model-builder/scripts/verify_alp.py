"""Check a generated (or hand-edited) AnyLogic .alp before opening it in AnyLogic.

    python verify_alp.py "C:\\...\\Mini ED 2D-3D\\Mini ED 2D-3D.alp"

Checks: XML well-formed; element ids unique; every connector names an existing block and port side; every
block parameter name exists for that block class (against the template cache, when present); every
ModelResources file exists next to the model; no absolute C:/ paths in code (gotcha G123); one line ending
style throughout. Exit code 1 if anything fails. Passing this does not prove the model builds or runs - only
AnyLogic can tell that (run it, then read the build log / screen: copilot/workflow/model-generation.md step G6).
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CACHE = Path(__file__).resolve().parent.parent / ".cache" / "templates.json"


def check(path):
    p = Path(path)
    raw = p.read_bytes()
    problems, notes = [], []
    crlf, lf = raw.count(b"\r\n"), raw.count(b"\n")
    if crlf and crlf != lf:
        problems.append(f"mixed line endings ({crlf} CRLF of {lf} lines)")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        return [f"XML not well-formed: {e}"], notes
    # An experiment's parameter values (FreeformParamValue, RangeVariationParamValue, ...) repeat the <Id> of
    # the parameter they refer to - references, not definitions - so they are left out of the uniqueness check.
    parent = {c: q for q in root.iter() for c in q}
    ids = [e.text for e in root.iter("Id") if not parent[e].tag.endswith("ParamValue")]
    dups = sorted({i for i in ids if ids.count(i) > 1})
    if dups:
        problems.append(f"{len(dups)} duplicate ids, e.g. {dups[:3]}")
    templates = json.loads(CACHE.read_text(encoding="utf-8"))["blocks"] if CACHE.is_file() else {}
    for cls in root.iter("ActiveObjectClass"):
        name = cls.find("Name")
        eos = cls.find("EmbeddedObjects")
        if name is None or eos is None:
            continue
        blocks = {}
        for eo in eos.findall("EmbeddedObject"):
            n, c = eo.find("Name"), eo.find("ActiveObjectClass/ClassName")
            if n is None or c is None:
                continue
            blocks[n.text] = c.text
            if c.text in templates:
                valid = set(re.findall(r"<Parameter>\s*<Name><!\[CDATA\[(\w+)\]\]>", templates[c.text]))
                plist = eo.find("Parameters")
                used = {q.find("Name").text for q in (plist if plist is not None else [])}
                bad = used - valid
                if bad:
                    problems.append(f"{name.text}.{n.text} ({c.text}): unknown parameters {sorted(bad)}")
        cons = cls.find("Connectors")
        for con in (cons if cons is not None else []):
            for side in ("Source", "Target"):
                item = con.find(f"{side}EmbeddedObjectReference/ItemName")
                ccls = con.find(f"{side}ConnectableItemReference/ClassName")
                if item is not None and item.text not in blocks:
                    problems.append(f"{name.text}: connector {side.lower()} '{item.text}' is not a block")
                elif item is not None and ccls is not None and blocks.get(item.text) != ccls.text:
                    problems.append(f"{name.text}: connector says {item.text} is {ccls.text}, block is {blocks.get(item.text)}")
        notes.append(f"{name.text}: {len(blocks)} blocks, {len(cons) if cons is not None else 0} connectors")
    for res in root.iter("Resource"):
        rp = res.find("Path")
        if rp is not None and res.findtext("Location") == "FILE_SYSTEM" and not (p.parent / rp.text).is_file():
            problems.append(f"resource missing next to the model: {rp.text}")
    text = raw.decode("utf-8", errors="replace")
    abs_paths = re.findall(r'"[A-Za-z]:[/\\][^"\n]{3,400}"', text)
    if abs_paths:
        problems.append(f"{len(abs_paths)} absolute path(s) in the model (G123), e.g. {abs_paths[0][:90]}")
    notes.append(f"{len(ids)} ids, header {re.search(r'AlpVersion=\"([^\"]+)\"', text[:500]).group(1) if 'AlpVersion' in text[:500] else '?'}")
    return problems, notes


if __name__ == "__main__":
    problems, notes = check(sys.argv[1])
    for n in notes:
        print("  " + n)
    for pr in problems:
        print("FAIL " + pr)
    print("OK - file checks passed" if not problems else f"{len(problems)} problem(s)")
    sys.exit(1 if problems else 0)
