"""Regenerate every Duskwood Design brand asset into src/assets/brand/.

Run from the repo root:  python tools/build-brand.py
"""
import pathlib
import re
import subprocess
import sys
import tempfile

SEED, DEPTH = 7, 6
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "assets" / "brand"
GEN = ROOT / "tools" / "duskwood-oak.py"


def oak(path, min_twig=0.0, ring=3.0):
    subprocess.run(
        [sys.executable, "-I", str(GEN), str(SEED), str(DEPTH), str(path), "moon", str(min_twig), str(ring)],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    return path.read_text()


def inner(svg):
    return re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1)


OUT.mkdir(parents=True, exist_ok=True)
mark = oak(OUT / "duskwood-mark.svg")
oak(OUT / "duskwood-mark-small.svg", min_twig=1.8, ring=7)

with tempfile.TemporaryDirectory() as tmp:
    fav = oak(pathlib.Path(tmp) / "fav.svg", min_twig=2.6, ring=8)
(OUT / "duskwood-favicon.svg").write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" color="#64ffda">\n'
    '  <rect width="200" height="200" rx="40" fill="#0a192f"/>\n'
    f'  <svg x="4" y="14" width="192" height="172" viewBox="0 0 200 180">{inner(fav)}</svg>\n'
    "</svg>\n",
    newline="\n",
)

(OUT / "duskwood-logo.svg").write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 290" color="#64ffda">\n'
    "  <!-- Text uses Cinzel (SIL Open Font License). Outline it before using outside a browser. -->\n"
    '  <style>@import url("https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&amp;display=swap");'
    " .dw{font-family:Cinzel,serif;font-weight:700;font-size:40px;fill:#ccd6f6}"
    " .ds{font-family:Cinzel,serif;font-weight:500;font-size:14px;fill:currentColor}</style>\n"
    f'  <svg x="50" y="0" width="200" height="180" viewBox="0 0 200 180">{inner(mark)}</svg>\n'
    '  <text class="dw" x="150" y="230" text-anchor="middle" textLength="276" lengthAdjust="spacing">DUSKWOOD</text>\n'
    '  <text class="ds" x="150" y="262" text-anchor="middle" textLength="110" lengthAdjust="spacing">DESIGN</text>\n'
    '  <path d="M42 257h46M212 257h46" stroke="currentColor" stroke-width="1.5"/>\n'
    "</svg>\n",
    newline="\n",
)
print("wrote", ", ".join(sorted(p.name for p in OUT.glob("*.svg"))))
