"""Builds the static site into dist/.

  python3 build.py

Pages in templates/ can include partials with {{> name}} and use any value
from site.json as {{key}}. Change the app name, prices or email in
site.json and rebuild; everything updates.
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"


def render(text, values, partials):
    text = re.sub(r"\{\{>\s*(\w+)\s*\}\}", lambda m: partials[m.group(1)], text)
    return re.sub(r"\{\{\s*(\w+)\s*\}\}", lambda m: str(values[m.group(1)]), text)


def main():
    values = json.loads((ROOT / "site.json").read_text())
    partials = {p.stem: p.read_text() for p in (ROOT / "partials").glob("*.html")}
    # Partials can use values too.
    partials = {k: render(v, values, {}) for k, v in partials.items()}
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(ROOT / "assets", DIST / "assets")
    for page in (ROOT / "templates").glob("*.html"):
        out = render(page.read_text(), values, partials)
        # Pretty URLs: privacy.html -> privacy/index.html (index stays put).
        target = DIST / ("index.html" if page.stem == "index" or page.stem == "404" else f"{page.stem}/index.html")
        if page.stem == "404":
            target = DIST / "404.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(out)
    (DIST / "CNAME").write_text(values["domain"].split("//")[-1] + "\n")
    print(f"Built {len(list((ROOT / 'templates').glob('*.html')))} pages into dist/")


if __name__ == "__main__":
    main()
