# HD Card Generator

Template-based card image generator for HD EDU. Renders text onto a template background image using HTML + Playwright screenshot.

## How It Works

```
config.json  -->  HTML template (text overlay on background)  -->  Playwright screenshot  -->  PNG
```

1. Read a JSON config file with title, subtitle, tutor name
2. Inject the values into an HTML template positioned over the background image
3. Use Playwright (headless Chromium) to screenshot the page at exact template dimensions
4. Output a pixel-perfect PNG

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
```

Or with uv:

```bash
uv pip install -r requirements.txt
uv run playwright install chromium
```

## Usage

### Single card

```bash
python render.py
# Uses config.json in current directory

python render.py --config my_card.json
# Uses a specific config file
```

### Batch mode

```bash
python render.py --config examples/
# Processes all .json files in the directory
```

## Config Format

```json
{
  "title": "COMP1100 Mid-Term",
  "subtitle": "Key Points & Quick Review",
  "tutor": "Tutor Ruby",
  "template": "templates/template.png",
  "output": "output/card.png"
}
```

| Field | Description |
|-------|-------------|
| `title` | Main title text (large, top area) |
| `subtitle` | Secondary text (medium, middle area) |
| `tutor` | Tutor name (near bottom bar) |
| `template` | Path to background template image (relative to project root) |
| `output` | Output PNG path (relative to project root) |

## Customizing the Template

- Replace `templates/template.png` with your own background image
- Edit `template.html` to adjust text positions, fonts, sizes, and colors
- The HTML uses Google Fonts (Noto Sans SC) for reliable Chinese character rendering

## Project Structure

```
hd-card-generator/
├── config.json          # Default config
├── render.py            # Main render script
├── template.html        # HTML template with placeholders
├── requirements.txt     # Python dependencies
├── templates/
│   └── template.png     # Background template image
├── examples/            # Batch config examples
│   ├── card_comp1100.json
│   └── card_acct3101.json
└── output/              # Generated cards (gitignored)
```
