"""ベンチマークパターンの集約。新しいパターンは1ファイル追加してここに登録する。"""
from . import async_retry_comment, saitama, summarize
from .base import Pattern

ALL_PATTERNS: list[Pattern] = [
    saitama.PATTERN,
    async_retry_comment.PATTERN,
    summarize.PATTERN,
]

__all__ = ["ALL_PATTERNS", "Pattern"]
