from pathlib import Path

from .base import Pattern

CODE = (Path(__file__).parent / "async_retry_client.txt").read_text(encoding="utf-8")

PATTERN = Pattern(
    name="async_retry_comment",
    prompt=f"次のコードに日本語でコードコメントを付けてください。\n\n```python\n{CODE}```",
)
