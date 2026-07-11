from dataclasses import dataclass
from typing import Optional

from classes.Shotgun import ShellCount, Shotgun
from classes.Enums import GameState


@dataclass
class Round:
    items: int
    lives: int
    fixed_loaded_shells: Optional[list[ShellCount]]

class RoundManager:
    def __init__(self):
        self.loadedRounds: list[Round] = []
        self.round_count: int = 0
        self.current_round: Round = None
        self.round_index: int = 0

    def load_default_rounds(self):
        self.loadedRounds = [
            # Round I — Stage 1, no items
            Round(
                items=0,
                lives=2,
                fixed_loaded_shells=[
                    ShellCount(live=1, blank=2),
                    ShellCount(live=3, blank=2),
                    ShellCount(live=3, blank=2),
                    ShellCount(live=3, blank=3),
                    ShellCount(live=5, blank=2),
                ],
            ),
            # Round II — Stage 2, 2 items per load
            Round(
                items=2,
                lives=4,
                fixed_loaded_shells=[
                    ShellCount(live=1, blank=1),
                    ShellCount(live=2, blank=2),
                    ShellCount(live=3, blank=2),
                    ShellCount(live=3, blank=3),
                    ShellCount(live=5, blank=2),
                ],
            ),
            # Round III — Stage 3, 4 items per load (loads 2-5 shuffled)
            Round(
                items=4,
                lives=6,
                fixed_loaded_shells=[
                    ShellCount(live=1, blank=2),
                    ShellCount(live=4, blank=4),
                    ShellCount(live=3, blank=2),
                    ShellCount(live=4, blank=2),
                    ShellCount(live=5, blank=3),
                ],
            ),
        ]
        self.round_count = len(self.loadedRounds)
        self.current_round = self.loadedRounds[0]

    def load_next_shells(self, shotgun: Shotgun):
        if self.current_round.fixed_loaded_shells is not None:
            next_shells: ShellCount = self.current_round.fixed_loaded_shells.pop(0)
            shotgun.load_shells(next_shells.live, next_shells.blank)

    def next_round(self) -> GameState:
        self.round_index += 1
        if self.round_index > self.round_count:
            return GameState.GAME_WON

        self.current_round = self.loadedRounds[self.round_index]
        return GameState.CONTINUE
