from enum import StrEnum, auto
from dataclasses import dataclass, field


class WinType(StrEnum):
    """Enum for all possible ways to Win in Tic Tac Toe game"""
    HORIZONTAL = auto()
    VERTICAL = auto()
    DIAGONAL = auto()


@dataclass
class WinData:
    """Contains data about which player won the game
    and coordinates of cells which made the winning line and the win type

    Attributes
    ----------
    winner : str
        mark of player who won, "X" or "O" or other marks can be possible values to be stored in this attribute
    win_type : WinType | None
        stores if player won by horizontal, vertical or diagonal line connection
        should be None or an enum member of WinType enum
    win_line : list[tuple[int, int]]
        list of coordinates of points which caused the player to win
    """
    winner: str | None = None
    win_type: WinType | None = None
    win_line: list[tuple[int, int]] = field(default_factory=list)
