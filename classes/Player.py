from __future__ import annotations

import random
import re
from typing import TYPE_CHECKING

from classes.Enums import Action, ShootAction, Target, ItemUseAction, ShellKnowledge, KnownShells, KnowledgeType
from classes.Item import Item
from classes.ItemManager import ItemManager

if TYPE_CHECKING:
    from classes.Shotgun import Shotgun, ShellCount


class Player:
    def __init__(self):
        self.name: str = ""
        self.shells: list[KnownShells] = []
        self.shell_index: int = 0
        self.health: int = 0
        self.otherPlayer: Player = None
        self.isAI: bool = False
        self.max_health: int = 0
        self.skip_next_turn: bool = False
        self.skipped_last_turn: bool = False

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

    def shoot_shell(self, was_live: bool):
        self.shells[self.shell_index].type = ShellKnowledge.LIVE if was_live else ShellKnowledge.BLANK
        self.shell_index += 1

    def invert_current_shell(self):
        self.shells[self.shell_index].inverted = not self.shells[self.shell_index].inverted

    def fill_with_empty_shells(self, shells: int):
        self.shells = [KnownShells(type=ShellKnowledge.UNKNOWN,known_by=KnowledgeType.NONE,inverted=False) for _ in range(shells)]
        self.shell_index = 0

    def update_shell(self, offset_from_current: int, shell: KnownShells):
        self.shells[self.shell_index + offset_from_current] = shell

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

    def do_turn(self, remaining_shells: int, remaining_shell_types: ShellCount, available_items: list[Item]) -> Action:
        pass

class Human(Player):
    def do_turn(self, remaining_shells: int, remaining_shell_types: ShellCount, available_items: list[Item]) -> Action:
        def get_input() -> Action:
            while True:
                i = input("type:\ny to shoot yourself \nd to shoot the other player\nu to use an item\n").strip().lower()
                if i == "y":
                    return ShootAction(target=Target.SELF)
                elif i == "d":
                    return ShootAction(target=Target.OTHER)
                elif i == "u":
                    result = choose_item()
                    if result is not None:
                        return result

        def choose_item() -> ItemUseAction | None:
            while True:
                print("available items:")
                for i, item in enumerate(available_items):
                    print(f"{i}: {item.name}")
                print("or input x to return")

                item_input = input("choose a number: ").strip()
                if item_input.isnumeric() and int(item_input) <= len(available_items) != 0:
                    return ItemUseAction(self.items.items[int(item_input)].type)
                return None

        return get_input()

class AI(Player):
    def __init__(self):
        super().__init__()
        self.name = "DEALER"
        self.isAI = True

    def do_turn(self, remaining_shells: int, remaining_shell_types: ShellCount, available_items: list[Item]) -> Action:
        def chance(percent):
            return random.random() < percent / 100

        if remaining_shells == remaining_shell_types.live:
            return ShootAction(target=Target.OTHER)
        elif remaining_shells == remaining_shell_types.blank:
            return ShootAction(target=Target.SELF)
        else:
            shot_self = not chance((remaining_shell_types.live / remaining_shells))
            return ShootAction(target=Target.SELF if shot_self else Target.OTHER)
