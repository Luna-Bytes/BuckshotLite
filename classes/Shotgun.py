from __future__ import annotations
import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

from classes.Shell import Shell
if TYPE_CHECKING:
    from classes.Player import Player

@dataclass
class ShellCount:
    live: int
    blank: int


class Shotgun:
    def __init__(self):
        self.loaded_shells: list[Shell] = []
        self.shellTypes = ShellCount(0, 0)
        self.remainingTypes = ShellCount(0, 0)
        self.totalShells: int = 0
        self.remainingShells: int = 0
        self.doubleDamage: bool = False

    def shot(self, player: Player, yourself: bool):
        is_live: bool = self.next_shell()
        if not(is_live):
            return False
        target: Player = player if yourself else player.otherPlayer
        target.health -= 1 + self.doubleDamage
        self.doubleDamage = False
        return True

    def eject_shell(self):
        is_live: bool = self.next_shell()
        if not is_live:
            return False
        return True

    def next_shell(self):
        # returns true if shell is Live else returns False
        next_shell: Shell = self.loaded_shells.pop(0)
        self.remainingShells -= 1
        if next_shell.firstType:
            self.remainingTypes.live -= 1
        else:
            self.remainingTypes.blank -= 1

        if next_shell.isLive:
            self.shellTypes.live -= 1
            return True
        else:
            self.shellTypes.blank -= 1
            return False

    def double_damage(self):
        self.doubleDamage = True

    def invert_shell(self):
        self.loaded_shells[0].invert()

    def load_shells(self, lives: int, blanks: int):
        total_count: int = lives + blanks
        if total_count == 0 or lives < 1 or blanks < 1:
            self.clear_shells()
            return

        self.shellTypes = ShellCount(lives, blanks)
        self.remainingTypes = ShellCount(lives, blanks)
        self.totalShells = total_count
        self.remainingShells = total_count

        shell_list: list[Shell] = [Shell(True) for _ in range(lives)] + [Shell(False) for _ in range(blanks)]
        random.shuffle(shell_list)
        self.loaded_shells = shell_list
        print(f"Loaded shells: {self.shellTypes.live} Lives and {self.shellTypes.blank} Blanks")

    def clear_shells(self):
        self.loaded_shells = []
        self.shellTypes = ShellCount(0, 0)
        self.remainingTypes = ShellCount(0, 0)
        self.totalShells = 0
        self.remainingShells = 0
        self.doubleDamage = False

    def __str__(self):
        return (
            f"Shotgun(\n"
            f"  loaded_shells={str(self.loaded_shells)},\n"
            f"  shellTypes={self.shellTypes},\n"
            f"  remainingTypes={self.remainingTypes},\n"
            f"  totalShells={self.totalShells},\n"
            f"  remainingShells={self.remainingShells}\n"
            f")"
        )
