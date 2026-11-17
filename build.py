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
    write_sitemap(values["domain"])
    print(f"Built {len(pages)} pages into dist/")


def write_sitemap(domain):
    """sitemap.xml lists every built page except 404; robots.txt points to it."""
    import datetime
    today = datetime.date.today().isoformat()
    urls = []
    for f in sorted(DIST.rglob("index.html")):
        if f.parent.name == "assets" or "assets" in f.relative_to(DIST).parts:
            continue
        html = f.read_text()
        if 'name="robots" content="noindex' in html:
            continue
        rel = f.parent.relative_to(DIST).as_posix()
        urls.append(domain + "/" + (rel + "/" if rel != "." else ""))
    body = "".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls)
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "</urlset>\n")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {domain}/sitemap.xml\n")


if __name__ == "__main__":
    main()
