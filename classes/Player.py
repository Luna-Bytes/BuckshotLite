from __future__ import annotations
import re
from typing import Optional, TYPE_CHECKING

from classes.Shell import Shell
from classes.ItemManager import ItemManager

if TYPE_CHECKING:
    from classes.Shotgun import Shotgun


class Player:
    def __init__(self):
        self.name: str = ""
        self.shells: list[Shell] = []
        self.health: int = 0
        self.otherPlayer: Optional[Player] = None
        self.isAI: bool = False
        self.max_health: int = 0
        self.skip_next_turn: bool = False
        self.skipped_last_turn: bool = False
        self.items: ItemManager = ItemManager()

    def __repr__(self):
        return (
            f"Player(\n"
            f"  name={self.name},\n"
            f"  health={self.health},\n"
            f"  otherPlayer={self.otherPlayer.name if self.otherPlayer else None},\n)"
            f")"
        )

    def skip_turn(self):
        self.skip_next_turn = True
        self.skipped_last_turn = True

    def last_live(self):
        self.max_health = 1
        self.health = 1

    def set_other_player(self, other_player: Player):
        self.otherPlayer = other_player

    def set_name(self, name: str):
        # returns True if successful else returns False
        def sanitize_name(_name):
            return re.sub(r'[^A-Z]', '', _name.strip().upper())
        name = sanitize_name(name)

        if len(name) <= 2 or name == "DEALER" or name == "GOD":
            return False

        self.name = sanitize_name(name)
        return True

    def set_dealer(self):
        self.name = "DEALER"
        self.isAI = True

    def shot(self, shotgun: Shotgun, shot_self:bool):
        return shotgun.shot(self, shot_self)