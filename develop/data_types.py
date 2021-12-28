from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Word_importance:
    word: str = ""
    importance: float = 0.0