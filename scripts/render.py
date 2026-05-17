#!/usr/bin/env python3
"""
Render the polished draft into newsletter.html (and optionally newsletter.pdf),
then archive the published items into data/history.db.

Usage:
    python scripts/render.py --week 2025-W20

Requires: jinja2, markdown, weasyprint (optional — PDF skipped if not installed)
"""
import argparse
import json
from datetime import datetime, date
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    raise SystemExit("Missing dependency: pip install jinja2")

try:
    import markdown as md_lib
except ImportError:
    raise SystemExit("Missing dependency: pip install markdown")

ROOT = Path(__file__).parent.parent
TEMPLATES = ROOT / "templates"
DATA = ROOT / "data"

SECTION_MAP = {
    "finance":    "1. AI in Finance",
    "agents":     "2. AI Agents & Applications",
    "physical":   "3. Physical AI",
    "foundation": "4. Foundation Models",
}


def load_selections(week: str) -> list[dict]:
    path = DATA / "issues" / week / "selections.json"
    if not path.exists():
        raise SystemExit(f"selections.json not found at {path}")
    return json.loads(path.read_text())


def load_candidates(week: str) -> dict[str, dict]:
    path = DATA / "issues" / week / "candidates.json"
    if not path.exists():
        raise SystemExit(f"candidates.json not found at {path}")
    items = json.loads(path.read_text())
    return {item["id"]: item for item in items}


def load_draft(week: str) -> str:
    path = DATA / "issues" / week / "draft.md"
    if not path.exists():
        raise SystemExit(f"draft.md not found at {path}")
    return path.read_text()


def extract_digest(draft_md: str) -> str:
    """Extract the digest paragraph between the # title and the first ## section."""
    import re
    # Strip the H1 title line, then grab text before the first ## header or ---
    body = re.sub(r"^#[^#].*$", "", draft_md, count=1, flags=re.MULTILINE).strip()
    # Take everything before the first ## or --- divider
    match = re.split(r"^(##|---)", body, maxsplit=1, flags=re.MULTILINE)
    candidate = match[0].strip()
    # Remove any leading/trailing markdown italics (the dateline)
    candidate = re.sub(r"^\*.*?\*\s*", "", candidate, flags=re.DOTALL).strip()
    return candidate


def parse_draft_sections(draft_md: str, selections: list[dict], candidates: dict) -> list[dict]:
    """
    Split draft.md on section headers and map body text back to selected items.
    Returns a list of section dicts ready for the Jinja2 template.

    Each item in draft.md follows voice.md format:
        Plain headline text

        **Bold impact lead.** Context sentence. Implication sentence.

        Source: https://...

    The function groups paragraphs by item boundary (each item ends with
    a "Source:" paragraph) so headline/body/URL never slip across items.
    It also handles the legacy single-paragraph format where the headline
    is embedded as **bold text** at the start of the body paragraph.
    """
    import re

    # Build a lookup: category -> ordered list of selected ids
    cat_order = list(SECTION_MAP.keys())
    selected_by_cat: dict[str, list[dict]] = {c: [] for c in cat_order}
    for sel in selections:
        item_id = sel["id"]
        category = item_id.rsplit("_", 1)[0]
        candidate = candidates.get(item_id, {})
        selected_by_cat.setdefault(category, []).append({
            "id": item_id,
            "headline": candidate.get("headline", item_id),
            "source_url": candidate.get("source_url", ""),
            "user_comment": sel.get("user_comment"),
        })

    # Split draft on ## headers
    blocks = re.split(r"^(##\s+.+)$", draft_md, flags=re.MULTILINE)
    section_bodies: dict[str, str] = {}
    for i in range(1, len(blocks) - 1, 2):
        header = blocks[i]
        body = blocks[i + 1].strip() if i + 1 < len(blocks) else ""
        for cat, label in SECTION_MAP.items():
            if label.lower() in header.lower():
                section_bodies[cat] = body
                break

    sections = []
    for cat in cat_order:
        sel_items = selected_by_cat.get(cat, [])
        if not sel_items:
            continue
        body_md = section_bodies.get(cat, "")

        # Split into paragraphs and group by item.
        # Each item ends with a "Source:" paragraph — use that as the boundary.
        all_paras = [p.strip() for p in re.split(r"\n{2,}", body_md) if p.strip()]
        item_groups: list[list[str]] = []
        current: list[str] = []
        for p in all_paras:
            current.append(p)
            if p.startswith("Source:"):
                item_groups.append(current)
                current = []
        if current:
            item_groups.append(current)

        rendered_items = []
        for idx, meta in enumerate(sel_items):
            group = item_groups[idx] if idx < len(item_groups) else []

            # Separate "Source:" paragraph from content paragraphs
            source_url = meta["source_url"]
            content = []
            for p in group:
                if p.startswith("Source:"):
                    source_url = p.replace("Source:", "").strip()
                else:
                    content.append(p)

            if not content:
                rendered_items.append({
                    "headline": meta["headline"],
                    "body_html": "",
                    "source_url": source_url,
                })
                continue

            # Two-paragraph format (voice.md): plain headline + **bold** body
            if len(content) >= 2 and not content[0].startswith("**"):
                headline  = content[0]
                body_text = " ".join(content[1:])
            else:
                # Legacy single-paragraph format: **Bold headline.** rest of body
                body_text = content[0]
                m = re.match(r"^\*\*(.+?)\*\*", body_text)
                headline  = m.group(1) if m else meta["headline"]
                body_text = body_text[m.end():].strip() if m else body_text

            rendered_items.append({
                "headline":  headline,
                "body_html": md_lib.markdown(body_text),
                "source_url": source_url,
            })

        sections.append({"label": SECTION_MAP[cat], "stories": rendered_items})

    return sections



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", required=True, help="ISO week string, e.g. 2025-W20")
    args = parser.parse_args()
    week = args.week

    issue_dir = DATA / "issues" / week
    issue_dir.mkdir(parents=True, exist_ok=True)

    selections = load_selections(week)
    candidates = load_candidates(week)
    draft_md   = load_draft(week)
    sections   = parse_draft_sections(draft_md, selections, candidates)
    digest     = extract_digest(draft_md)

    issue_date = date.today().strftime("%d %B %Y")

    env = Environment(loader=FileSystemLoader(str(TEMPLATES)))
    tmpl = env.get_template("newsletter.html.j2")
    html = tmpl.render(week=week, issue_date=issue_date, sections=sections,
                       digest=digest,
                       generated_at=datetime.now().isoformat(timespec="minutes"))

    html_path = issue_dir / "newsletter.html"
    html_path.write_text(html)
    print(f"HTML: {html_path}")

    # Optional PDF via WeasyPrint
    try:
        from weasyprint import HTML as WP_HTML
        pdf_path = issue_dir / "newsletter.pdf"
        WP_HTML(string=html, base_url=str(issue_dir)).write_pdf(str(pdf_path))
        print(f"PDF : {pdf_path}")
    except ImportError:
        print("PDF skipped (weasyprint not installed; run: pip install weasyprint)")

    print("Done. Copy newsletter.html to data/archive/ to register these URLs in history.")


if __name__ == "__main__":
    main()
