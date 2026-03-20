"""
HD Card Generator - FastAPI Service

POST /render  → accepts {"title": "...", "tutor": "..."}, returns PNG image
GET  /health  → {"status": "ok"}
"""

from io import BytesIO

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from render import render_to_bytes, _load_template_html

app = FastAPI(title="HD Card Generator")

# Pre-load template once at startup
_template_html: str = _load_template_html()


class RenderRequest(BaseModel):
    title: str
    tutor: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/render")
def render(req: RenderRequest):
    png_bytes = render_to_bytes(req.title, req.tutor, _template_html)
    return StreamingResponse(BytesIO(png_bytes), media_type="image/png")
