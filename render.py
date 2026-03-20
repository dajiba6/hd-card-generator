#!/usr/bin/env python3
"""
HD Card Generator
Renders text onto a template image via HTML + Playwright screenshot.

Usage:
    python render.py                          # uses config.json in current dir
    python render.py --config my_config.json  # uses a custom config file
    python render.py --config cards/          # batch: processes all .json in folder
"""

import argparse
import json
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def load_config(config_path: str) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_html(template_html: str, config: dict, project_root: Path) -> str:
    """Replace placeholders in the HTML template with config values."""
    template_img = project_root / config.get("template", "templates/template.png")
    template_uri = template_img.resolve().as_uri()

    html = template_html
    html = html.replace("{{TEMPLATE_PATH}}", template_uri)
    html = html.replace("{{TITLE}}", config.get("title", ""))
    html = html.replace("{{SUBTITLE}}", config.get("subtitle", ""))
    html = html.replace("{{TUTOR}}", config.get("tutor", ""))
    return html


def render_card(config: dict, project_root: Path, template_html: str):
    """Render a single card from config dict."""
    html_content = build_html(template_html, config, project_root)

    # Write temporary HTML
    tmp_html = project_root / ".tmp_render.html"
    tmp_html.write_text(html_content, encoding="utf-8")

    output_path = project_root / config.get("output", "output/card.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1644, "height": 918})
        page.goto(tmp_html.resolve().as_uri())
        # Wait for Google Fonts to load
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        page.screenshot(path=str(output_path), full_page=False)
        browser.close()

    tmp_html.unlink(missing_ok=True)
    print(f"[OK] {output_path}")


def main():
    parser = argparse.ArgumentParser(description="HD Card Generator")
    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to a config JSON file or a directory of JSON files for batch mode",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent

    # Read HTML template
    template_html_path = project_root / "template.html"
    if not template_html_path.exists():
        print(f"[ERROR] template.html not found at {template_html_path}", file=sys.stderr)
        sys.exit(1)
    template_html = template_html_path.read_text(encoding="utf-8")

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = project_root / config_path

    if config_path.is_dir():
        # Batch mode: process all .json files in the directory
        json_files = sorted(config_path.glob("*.json"))
        if not json_files:
            print(f"[WARN] No .json files found in {config_path}")
            return
        print(f"[BATCH] Found {len(json_files)} config files")
        for jf in json_files:
            print(f"\n--- Processing {jf.name} ---")
            config = load_config(str(jf))
            render_card(config, project_root, template_html)
    else:
        # Single file mode
        config = load_config(str(config_path))
        render_card(config, project_root, template_html)


if __name__ == "__main__":
    main()
