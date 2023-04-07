"""
ttt_engine.state_data
~~~~~~~~~~~~~~~~~~~~~
Data module for data oriented classes used
"""

from enum import StrEnum, auto
from dataclasses import dataclass, field

from .grid import Coordinate


class GameState(StrEnum):
    """Enum for all game states"""
    WIN = auto()
    DRAW = auto()
    ONGOING = auto()


class WinType(StrEnum):
    """Enum for all possible ways to win"""
    HORIZONTAL = auto()
    VERTICAL = auto()
    DIAGONAL = auto()


@dataclass
class WinData:
    """Contains data about which player won the game,
    coordinates of cells which made the winning line and the win type

    Attributes
    ----------
    winner : str
        player mark of winner
    win_type : WinType | None
        stores if player won by horizontal, vertical or diagonal line connection
    win_line : list[Coordinate]
        list of coordinates of cells which made winning line
    """

    winner: str = ""
    win_type: WinType | None = None
    win_line: list[Coordinate] = field(default_factory=list)
