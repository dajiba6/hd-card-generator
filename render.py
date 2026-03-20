#!/usr/bin/env python3
"""
HD Card Generator
Renders text onto a template image via HTML + Playwright screenshot.

Usage (CLI):
    python render.py                          # uses config.json in current dir
    python render.py --config my_config.json  # uses a custom config file
    python render.py --config cards/          # batch: processes all .json in folder

Usage (API):
    from render import render_to_bytes
    png_bytes = render_to_bytes("COMP1100 期中考试", "Tutor Ruby")
"""

import argparse
import json
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parent


def _load_template_html() -> str:
    path = PROJECT_ROOT / "template.html"
    return path.read_text(encoding="utf-8")


def _build_html(template_html: str, title: str, tutor: str) -> str:
    """Replace placeholders in the HTML template."""
    template_img = PROJECT_ROOT / "templates" / "template.png"
    template_uri = template_img.resolve().as_uri()

    html = template_html
    html = html.replace("{{TEMPLATE_PATH}}", template_uri)
    html = html.replace("{{TITLE}}", title)
    html = html.replace("{{TUTOR}}", tutor)
    return html


def render_to_bytes(title: str, tutor: str, template_html: str | None = None) -> bytes:
    """Render a card and return PNG bytes."""
    if template_html is None:
        template_html = _load_template_html()

    html_content = _build_html(template_html, title, tutor)

    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8", delete=False) as f:
        f.write(html_content)
        tmp_path = Path(f.name)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
            page = browser.new_page(viewport={"width": 1644, "height": 918})
            page.goto(tmp_path.resolve().as_uri())
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1000)
            png_bytes = page.screenshot(full_page=False)
            browser.close()
    finally:
        tmp_path.unlink(missing_ok=True)

    return png_bytes


# --------------- CLI ---------------

def load_config(config_path: str) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def render_card_to_file(config: dict, template_html: str):
    """CLI helper: render a card and write to the output path in config."""
    title = config.get("title", "")
    tutor = config.get("tutor", "")
    png_bytes = render_to_bytes(title, tutor, template_html)

    output_path = PROJECT_ROOT / config.get("output", "output/card.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(png_bytes)
    print(f"[OK] {output_path}")


def main():
    parser = argparse.ArgumentParser(description="HD Card Generator")
    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to a config JSON file or a directory of JSON files for batch mode",
    )
    args = parser.parse_args()

    template_html = _load_template_html()

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path

    if config_path.is_dir():
        json_files = sorted(config_path.glob("*.json"))
        if not json_files:
            print(f"[WARN] No .json files found in {config_path}")
            return
        print(f"[BATCH] Found {len(json_files)} config files")
        for jf in json_files:
            print(f"\n--- Processing {jf.name} ---")
            config = load_config(str(jf))
            render_card_to_file(config, template_html)
    else:
        config = load_config(str(config_path))
        render_card_to_file(config, template_html)


if __name__ == "__main__":
    main()
