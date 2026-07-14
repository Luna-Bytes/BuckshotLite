from dataclasses import dataclass
from enum import Enum, auto
from typing import Union, Optional

class GameState(Enum):
    CONTINUE = auto()
    NEXT_ROUND = auto()
    NEXT_SHELLS = auto()
    GAME_OVER = auto()
    GAME_WON = auto()


class Target(Enum):
    SELF = auto()
    OTHER = auto()


@dataclass(frozen=True)
class ShootAction:
    target: Target


@dataclass(frozen=True)
class ItemUseAction:
    item: ItemType
    target: Optional[Target]  # some items also need a target (self/dealer)


Action = Union[ShootAction, ItemUseAction]

class ItemType(Enum):
    SAW = auto(),
    CIGARETTE = auto(),
    HANDCUFFS = auto(),
    MAGNIFYING_GLASS = auto(),
    BEER = auto(),

@dataclass()
class Game:
    mode: GameMode
    name: str

class GameMode(Enum):
    NORMAL = auto()
    ENDLESS = auto()
