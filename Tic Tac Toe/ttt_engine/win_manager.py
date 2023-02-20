from enum import StrEnum, auto
from dataclasses import dataclass, field


class WinType(StrEnum):
    HORIZONTAL = auto()
    VERTICAL = auto()
    DIAGONAL = auto()


@dataclass
class WinManager:
    winner: str | None = None
    win_type: WinType | None = None
    win_line: list[tuple[int, int]] = field(default_factory=list)
