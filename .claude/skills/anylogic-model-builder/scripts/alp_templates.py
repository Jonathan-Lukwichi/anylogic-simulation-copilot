"""Collect AnyLogic file-format templates from the AnyLogic installed on THIS machine.

The generator (alp_builder.py) never invents XML for library blocks or 3D objects: it copies the format of
an element that AnyLogic itself saved in one of its example models. This script finds those elements and
caches them in ../.cache/templates.json (git-ignored: the fragments come from AnyLogic's own files, so they
are rebuilt from each user's install rather than committed).

    python alp_templates.py            # build the cache (about 1-2 minutes)
    python alp_templates.py --show     # print what the cache holds

Cached: one EmbeddedObject per Process Modeling Library class found in the examples; the colour table and
axis order of every library 3D object used in an example; the workspace header, converter list and
required-library references of the reference model (Bank Office tutorial, phase 4).
"""
import glob
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
CACHE = HERE.parent / ".cache"
PML = "com.anylogic.libraries.processmodeling"


def find_install():
    """Return (install dir, examples dir, 3D library dir) of the newest AnyLogic 8.x found."""
    installs = sorted(glob.glob(r"C:\Program Files\AnyLogic 8*"), reverse=True)
    if not installs:
        sys.exit("AnyLogic 8 is not installed under C:\\Program Files")
    inst = Path(installs[0])
    data = Path(r"C:\ProgramData") / inst.name
    examples = sorted(glob.glob(str(data / "eclipse" / "plugins" / "com.anylogic.examples_*")), reverse=True)
    lib3d = sorted(glob.glob(str(inst / "plugins" / "com.anylogic.ui_*" / "resources" / "3d")), reverse=True)
    if not examples or not lib3d:
        sys.exit(f"examples or 3D library not found for {inst}")
    return inst, Path(examples[0]), Path(lib3d[0])


def elements(text, tag):
    """Yield every <tag ...>...</tag> element (nesting of the same tag handled)."""
    open_re, close = re.compile(r"<%s(?=[\s>])" % tag), "</%s>" % tag
    i = 0
    while True:
        m = open_re.search(text, i)
        if not m:
            return
        depth, j = 1, m.end()
        while depth:
            o, c = open_re.search(text, j), text.find(close, j)
            if c < 0:
                return
            if o and o.start() < c:
                depth, j = depth + 1, o.end()
            else:
                depth, j = depth - 1, c + len(close)
        yield text[m.start():j]
        i = m.end()


def build():
    inst, examples, lib3d = find_install()
    models = sorted(examples.glob("basicmodels/*/*.alp")) + sorted(examples.glob("models/*/*.alp")) \
        + sorted(examples.glob("bigbookmodels/*/*/*.alp"))
    ref_path = next(examples.glob("basicmodels/Bank Office - Phase 4/*.alp"))
    ref = ref_path.read_text(encoding="utf-8").replace("\r\n", "\n")
    out = {
        "install": str(inst), "examples": str(examples), "lib3d": str(lib3d), "reference_model": ref_path.name,
        "eol": "\r\n" if b"\r\n" in ref_path.read_bytes() else "\n",
        "header": ref[:ref.index("<Model>")],
        "converters": re.search(r"<ConvertersApplied>.*?</ConvertersApplied>", ref, re.S).group(0),
        "libraries": re.findall(r"<RequiredLibraryReference>.*?</RequiredLibraryReference>", ref, re.S),
        "blocks": {}, "block_sources": {}, "figures": {},
    }
    cls_re = re.compile(r"<ActiveObjectClass>\s*<PackageName><!\[CDATA\[" + re.escape(PML) +
                        r"\]\]></PackageName>\s*<ClassName><!\[CDATA\[(\w+)\]\]>")
    fig_res = re.compile(r"<ClassName><!\[CDATA\[3d/([\w\-]+)\.dae\]\]></ClassName>")
    alp_ver = lambda p: (re.search(r'AlpVersion="([^"]+)"', p.read_text(encoding="utf-8", errors="replace")[:600])
                         or [None, ""])[1]
    ref_ver = alp_ver(ref_path)
    out["alp_version"] = ref_ver
    # the reference model first, then models saved in the same file version, then the rest
    models = sorted(models, key=lambda p: alp_ver(p) != ref_ver)
    for m in [ref_path] + models:
        t = m.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
        for seg in elements(t, "EmbeddedObject"):
            c = cls_re.search(seg[:800])
            if c and c.group(1) not in out["blocks"] and "<Parameters>" in seg:
                out["blocks"][c.group(1)] = seg
                out["block_sources"][c.group(1)] = m.parent.name
        for seg in elements(t, "Figure3D"):
            f = fig_res.search(seg)
            if f and f.group(1) not in out["figures"]:
                ct = re.search(r"<ColorTable>.*?</ColorTable>|<ColorTable/>", seg, re.S)
                ax = re.search(r"<AxisOrder>(\w+)</AxisOrder>", seg)
                out["figures"][f.group(1)] = {"colorTable": ct.group(0) if ct else "",
                                              "AxisOrder": ax.group(1) if ax else "XYZ_AXIS_ORDER",
                                              "from": m.parent.name}
    CACHE.mkdir(parents=True, exist_ok=True)
    (CACHE / "templates.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"AnyLogic: {inst.name}; scanned {len(models)} example models")
    print(f"block templates: {len(out['blocks'])} ({', '.join(sorted(out['blocks']))})")
    print(f"3D object templates: {len(out['figures'])} of {len(list(lib3d.glob('*.dae')))} library objects")
    print(f"cache: {CACHE / 'templates.json'}")


def show():
    t = json.loads((CACHE / "templates.json").read_text(encoding="utf-8"))
    print(f"install {t['install']}\nreference model {t['reference_model']}")
    for k, v in sorted(t["block_sources"].items()):
        names = re.findall(r"<Parameter>\s*<Name><!\[CDATA\[(\w+)\]\]>", t["blocks"][k])
        print(f"  {k:22s} from {v[:30]:30s} {len(names)} parameters")
    print("3D objects: " + ", ".join(sorted(t["figures"])))


if __name__ == "__main__":
    show() if "--show" in sys.argv else build()
