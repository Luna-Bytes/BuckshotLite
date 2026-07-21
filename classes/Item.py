from typing import TYPE_CHECKING

from classes.Enums import ItemType, ShellKnowledge, KnownShells, KnowledgeType
from classes.Shotgun import Shotgun

if TYPE_CHECKING:
    from classes.Player import Player


class Item:
    def __init__(self):
        self.name: str = ""
        self.icon: str = ""
        self.type: ItemType = None

    def use(self, player: Player, shotgun: Shotgun):
        pass

class Saw(Item):
    def __init__(self):
        super().__init__()
        self.name: str = "Handsaw"
        self.icon: str = ""
        self.type: ItemType = ItemType.SAW

    def use(self, player: Player, shotgun: Shotgun):
        shotgun.double_damage()

class Cigarette(Item):
    def __init__(self):
        super().__init__()
        self.name: str = "Cigarette"
        self.icon: str = ""
        self.type: ItemType = ItemType.CIGARETTE

    def use(self, player: Player, shotgun: Shotgun):
        player.health = min(player.health + 1, player.max_health)

class Handcuffs(Item):
    def __init__(self):
        super().__init__()
        self.name: str = "Handcuffs"
        self.icon: str = ""
        self.type: ItemType = ItemType.HANDCUFFS

    def use(self, player: Player, shotgun: Shotgun):
        if player.otherPlayer is not None:
            player.otherPlayer.skip_turn()

class MagnifyingGlass(Item):
    def __init__(self):
        super().__init__()
        self.name: str = "Magnifying Glass"
        self.icon: str = ""
        self.type: ItemType = ItemType.MAGNIFYING_GLASS

    def use(self, player: Player, shotgun: Shotgun):
        player.update_shell(0, KnownShells(
            type=ShellKnowledge.LIVE if shotgun.loaded_shells[0] else ShellKnowledge.BLANK,
            known_by=KnowledgeType.MAGNIFYING
        , inverted=shotgun.loaded_shells[0].isInverted
        ))

class Beer(Item):
    def __init__(self):
        super().__init__()
        self.name: str = "Beer"
        self.icon: str = ""
        self.type: ItemType = ItemType.BEER

    def use(self, player: Player, shotgun: Shotgun):
        was_live = shotgun.eject_shell()
        print("Ejected a " + ("live" if was_live else "blank") + " Shell")