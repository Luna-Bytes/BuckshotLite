from __future__ import annotations

import random
import re
from typing import Optional, TYPE_CHECKING

from classes.Enums import Action, ShootAction, Target
from classes.Shell import Shell
from classes.ItemManager import ItemManager

if TYPE_CHECKING:
    from classes.Shotgun import Shotgun, ShellCount


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

    def shot(self, shotgun: Shotgun, shot_self:bool):
        return shotgun.shot(self, shot_self)

    def do_turn(self, remaining_shells: int, remaining_shell_types: ShellCount) -> Action:
        pass

class Human(Player):
    def do_turn(self, remaining_shells: int, remaining_shell_types: ShellCount) -> Action:
        def get_input():
            while True:
                i = input("input y to shoot yourself and d to shoot the other player: ").strip().lower()
                if i == "y":
                    return True
                elif i == "d":
                    return False

        return ShootAction(target=Target.SELF if get_input() else Target.OTHER)

class AI(Player):
    def __init__(self):
        super().__init__()
        self.name = "DEALER"
        self.isAI = True

    def do_turn(self, remaining_shells: int, remaining_shell_types: ShellCount) -> Action:
        def chance(percent):
            return random.random() < percent / 100

        if remaining_shells == remaining_shell_types.live:
            return ShootAction(target=Target.OTHER)
        elif remaining_shells == remaining_shell_types.blank:
            return ShootAction(target=Target.SELF)
        else:
            shot_self = not chance((remaining_shell_types.live / remaining_shells))
            return ShootAction(target=Target.SELF if shot_self else Target.OTHER)
