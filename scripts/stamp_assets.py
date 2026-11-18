"""Add a content-hash version (?v=xxxxxxxx) to every /assets/ link in the HTML pages.

Run after changing any file in /assets:   python3 scripts/stamp_assets.py
Each link's version changes only when that file's contents change, so browsers
fetch the new file immediately and keep reusing unchanged ones.
"""
import hashlib, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = [ROOT / "index.html", ROOT / "hi" / "index.html"]
LINK = re.compile(r'((?:href|src)=")(/assets/[^"?#]+)(?:\?v=[0-9a-f]+)?(")')

def version(path: str) -> str:
    data = (ROOT / path.lstrip("/")).read_bytes()
    return hashlib.sha256(data).hexdigest()[:10]

for page in PAGES:
    html = page.read_text(encoding="utf-8")
    new = LINK.sub(lambda m: f"{m.group(1)}{m.group(2)}?v={version(m.group(2))}{m.group(3)}", html)
    page.write_text(new, encoding="utf-8")
    print(f"stamped {page.relative_to(ROOT)}")
