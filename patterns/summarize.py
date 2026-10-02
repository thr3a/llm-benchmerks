from pathlib import Path

from .base import Pattern

LONG_TEXT = (Path(__file__).parent / "handoutai-vs-car.md").read_text(encoding="utf-8")

PATTERN = Pattern(
    name="summarize",
    prompt=f"次の文章を3行に要約してください。\n\n{LONG_TEXT}",
)
