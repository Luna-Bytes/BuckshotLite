from typing import TYPE_CHECKING

from classes.Shotgun import Shotgun

if TYPE_CHECKING:
    from classes.Player import Player


class Item:
    def __init__(self):
        self.name: str = ""
        self.icon: str = ""

    def use(self, player: Player, shotgun: Shotgun):
        pass

class Saw(Item):
    def __init__(self):
        super().__init__()
        self.name: str = "Handsaw"
        self.icon: str = ""

    def use(self, player: Player, shotgun: Shotgun):
        shotgun.double_damage()

class Cigarette(Item):
    def __init__(self):
        super().__init__()
        self.name: str = "Cigarette"
        self.icon: str = ""

    def use(self, player: Player, shotgun: Shotgun):
        player.health = min(player.health + 1, player.max_health)

class Handcuffs(Item):
    def __init__(self):
        super().__init__()
        self.name: str = "Handcuffs"
        self.icon: str = ""

    def use(self, player: Player, shotgun: Shotgun):
        if player.otherPlayer is not None:
            player.otherPlayer.skip_turn()

class MagnifyingGlass:
    def __init__(self):
        super().__init__()
        self.name: str = "Magnifying Glass"
        self.icon: str = ""

    def use(self, player: Player, shotgun: Shotgun):
        print("Current Shell is " + ("live" if shotgun.loaded_shells[0].isLive else "blank"))