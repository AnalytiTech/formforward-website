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
    pages = sorted((ROOT / "templates").rglob("*.html"))
    for page in pages:
        out = render(page.read_text(), values, partials)
        # Pretty URLs: privacy.html -> privacy/index.html, cppll/privacy.html ->
        # cppll/privacy/index.html; index.html stays put in its folder.
        rel = page.relative_to(ROOT / "templates")
        if rel == Path("404.html"):
            target = DIST / "404.html"
        elif page.stem == "index":
            target = DIST / rel
        else:
            target = DIST / rel.parent / page.stem / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(out)
    (DIST / "CNAME").write_text(values["domain"].split("//")[-1] + "\n")
    print(f"Built {len(pages)} pages into dist/")


if __name__ == "__main__":
    main()
