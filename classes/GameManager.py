import random
from typing import Optional

from classes.Enums import GameState, ItemType, Target, Action, ShootAction, Game, GameMode
from classes.Item import Item, Saw, Cigarette, Handcuffs, MagnifyingGlass, Beer
from classes.Player import Player, Human, AI
from classes.RoundManager import RoundManager
from classes.Shotgun import Shotgun


class GameManager:
    def __init__(self, players: list[Player]|None = None):
        self.players: list[Player] = players
        self.shotgun: Shotgun = Shotgun()
        self.currentPlayer: int = 0
        self.state: GameState = GameState.CONTINUE
        self.rounds: RoundManager = RoundManager()
        self.endless = False

    def setup(self, setup:Game):
        self.endless = setup.mode == GameMode.ENDLESS
        self.players = [Human(), AI()]
        self.players[0].name = setup.name.upper()[:6]
        self.players[0].set_other_player(self.players[1])
        self.players[1].set_other_player(self.players[0])


    def next_round(self):
        self.state = self.rounds.next_round()

        lives = self.rounds.current_round.lives
        print(lives)
        for player in self.players:
            player.health = lives
            player.max_health = lives
        self.next_loadout()
        print(f"Each player has {lives} lives")

    def next_loadout(self):
        def random_item():
            return available_items[random.randint(0, len(available_items) - 1)]

        available_items: list[Item] = [Saw(), Cigarette(), Handcuffs(), MagnifyingGlass(), Beer()]
        for player in self.players:
            player.skip_next_turn = False
            player.skipped_last_turn = False
            for i in range(self.rounds.current_round.items):
                player.items.add_item(random_item())

        self.currentPlayer = 0
        self.rounds.load_next_shells(self.shotgun)
        self.state = GameState.CONTINUE



    def run(self):
        self.rounds.load_default_rounds()
        self.next_round()

        while self.state == GameState.CONTINUE:
            self.print_info()
            self.next_player()
            self.currentPlayer = (self.currentPlayer + 1) % len(self.players)
            if self.state == GameState.NEXT_ROUND:
                self.next_round()
            if self.state == GameState.NEXT_SHELLS:
                self.next_loadout()

    def print_info(self):
        for player in self.players:
            print(player.name + ": " + "⚡︎" * player.health)

    def do_turn(self):
        def use_item(_item: ItemType, _target: Optional[Target]):
            for index, iitem in enumerate(player.items.get_items()):
                if _item == iitem.type:
                    player.items.use_item(index, player, self.shotgun)
                    return

        still_going: bool = True
        player = self.players[self.currentPlayer]
        print(player.name + "'s TURN:")

        while still_going and self.state == GameState.CONTINUE:
            action: Action = player.do_turn(self.shotgun.remainingShells, self.shotgun.remainingTypes, player.items.get_items())

            if type(action) is ShootAction:
                was_live = player.shot(self.shotgun, True if action.target == Target.SELF else False)

                if action.target == Target.OTHER or was_live:
                    still_going = False

                print(player.name + " shot a " + ("live" if was_live else "blank") + " Shell at " + (
                    "themselves" if action.target == Target.SELF else player.otherPlayer.name))
            else:
                item = action.item
                target = action.target
                use_item(item, target)

            self.update_state()

    def update_state(self):
        for player in self.players:
            if player.health == 0:
                if player.isAI:
                    self.state = GameState.NEXT_ROUND
                else:
                    self.state = GameState.GAME_OVER
                return
        if self.shotgun.remainingShells == 0:
            self.state = GameState.NEXT_SHELLS
            return
        self.state = GameState.CONTINUE
        return

    def next_player(self):
        player = self.players[self.currentPlayer]

        if player.skip_next_turn:
            player.skip_next_turn = False
            print(player.name + "'s turn got skipped by handcuffs")
        else:
            player.skipped_last_turn = False
            self.do_turn()