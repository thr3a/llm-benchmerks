from dataclasses import dataclass


@dataclass(frozen=True)
class Pattern:
    name: str
    prompt: str
    max_tokens: int = 1024
