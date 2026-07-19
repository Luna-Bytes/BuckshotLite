from dataclasses import dataclass
from enum import Enum, auto
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from classes.Item import Item, Cigarette, Saw, Handcuffs, MagnifyingGlass, Beer


class GameState(Enum):
    CONTINUE = auto()
    NEXT_ROUND = auto()
    NEXT_SHELLS = auto()
    GAME_OVER = auto()
    GAME_WON = auto()


class Target(Enum):
    SELF = auto()
    OTHER = auto()
    NONE = auto()


@dataclass(frozen=True)
class ShootAction:
    target: Target


@dataclass(frozen=True)
class ItemUseAction:
    item: ItemType


Action = Union[ShootAction, ItemUseAction]

class ItemType(Enum):
    SAW = auto(),
    CIGARETTE = auto(),
    HANDCUFFS = auto(),
    MAGNIFYING_GLASS = auto(),
    BEER = auto(),

def itemtype_to_name(itemtype: ItemType) -> str:
    match itemtype:
        case ItemType.SAW:
            return "Saw"
        case ItemType.CIGARETTE:
            return "Cigarette"
        case ItemType.HANDCUFFS:
            return "Hand Cuffs"
        case ItemType.MAGNIFYING_GLASS:
            return "Magnifying Glass"
        case ItemType.BEER:
            return "Beer"

def itemtype_to_item(itemtype: ItemType) -> Item:
    match itemtype:
        case ItemType.SAW:
            return Saw()
        case ItemType.CIGARETTE:
            return Cigarette()
        case ItemType.HANDCUFFS:
            return Handcuffs()
        case ItemType.MAGNIFYING_GLASS:
            return MagnifyingGlass()
        case ItemType.BEER:
            return Beer()

@dataclass()
class Game:
    mode: GameMode
    player_name: str
    available_items: list[ItemType]

class GameMode(Enum):
    NORMAL = auto()
    ENDLESS = auto()

@dataclass(frozen=True)
class NewRound:
    lives: int

@dataclass(frozen=True)
class NewShells:
    lives: int
    blankes: int
    total: int

class GameEnd(Enum):
    GAME_LOST = auto()
    GAME_WON = auto()
    DOUBLE_OR_NOTHING = auto()

@dataclass
class ItemGained:
    type: ItemType
    success: bool

class ItemUsed:
    type: ItemType

TurnEvents = Union[GameEnd, NewRound, NewShells, ItemGained]

@dataclass
class ItemCount:
    type: ItemType
    count: int
    name: str

@dataclass
class KnownShells:
    type: ShellKnowledge
    known_by: KnowledgeType
    inverted: bool

class ShellKnowledge(Enum):
    LIVE = auto()
    BLANK = auto()
    UNKNOWN = auto()

class KnowledgeType(Enum):
    MAGNIFYING = auto()
    TELEFON = auto()
    FIRED = auto()
    NONE = auto()