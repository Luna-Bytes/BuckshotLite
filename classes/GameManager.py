import random

from classes.Enums import GameState, ItemType, Target, Action, ShootAction, Game, GameMode, TurnEvents, NewRound, \
    ShotEvent, ItemUseAction, NoEvent, Skipped, NextPlayer
from classes.ItemManager import ItemManager
from classes.Player import Player, Human, AI
from classes.RoundManager import RoundManager
from classes.Shotgun import Shotgun


class GameManager:
    def __init__(self, players: list[Player]|None = None):
        if players is None:
            players: list[Player] = [Player() for i in range(2)]
        self.players: list[Player] = players
        self.player_items: list[ItemManager] = [ItemManager() for i in range(2)]
        self.available_items: list[ItemType] = []
        self.shotgun: Shotgun = Shotgun()
        self.currentPlayer: int = 0
        self.state: GameState = GameState.CONTINUE
        self.rounds: RoundManager = RoundManager()
        self.endless = False

    def setup(self, setup:Game) -> list[TurnEvents]:
        self.endless = setup.mode == GameMode.ENDLESS
        if not self.endless:
            self.rounds.load_default_rounds()
        self.available_items = setup.available_items
        self.players = [Human(), AI()]
        self.players[0].name = setup.player_name.upper()[:6]
        self.players[0].set_other_player(self.players[1])
        self.players[1].set_other_player(self.players[0])

        return self.next_round()

    def player_turn(self, action: Action) -> list[TurnEvents]:
        events: list[TurnEvents] = []
        waiting_for_next_action, player_action_done = False, False

        while not waiting_for_next_action:
            still_going = True
            player = self.players[self.currentPlayer]

            if player.skip_next_turn:
                player.skip_next_turn = False
                events.append(Skipped())
                still_going = False
            else:
                player.skipped_last_turn = False

            if type(player) is Human and still_going and not player_action_done:
                new_still_going, new_events = self.do_action(action)
                events.extend(new_events)
                still_going = new_still_going
                player_action_done = True
            elif still_going and type(player) is AI:
                action = player.do_turn(self.shotgun.remainingShells, self.shotgun.remainingTypes, self.player_items[self.currentPlayer].get_items())
                new_still_going, new_events = self.do_action(action)
                events.extend(new_events)
                still_going = new_still_going
            else:
                waiting_for_next_action = True

            if not still_going:
                self.currentPlayer = (self.currentPlayer + 1) % len(self.players)
                events.append(NextPlayer())

            self.update_state()

            if self.state == GameState.NEXT_ROUND:
                events.extend(self.next_round())
            elif self.state == GameState.NEXT_SHELLS:
                events.extend(self.next_loadout())

        return events

    def do_action(self, action: Action) -> tuple[bool,list[TurnEvents]]:
        still_going = True
        events: list[TurnEvents] = []
        player = self.players[self.currentPlayer]

        if type(action) is ShootAction:
            shot = self.shotgun.shot(player, True if action.target == Target.SELF else False)
            events.append(ShotEvent(shot, action.target))
            for pl in self.players:
                pl.shoot_shell(shot)
            if shot or action.target == Target.OTHER:
                still_going = False

        if type(action) is ItemUseAction and still_going:
            events.append(self.player_items[self.currentPlayer].use_item(action.item, player, self.shotgun))

        return still_going, events


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

    def next_player(self):
        player = self.players[self.currentPlayer]

        if player.skip_next_turn:
            player.skip_next_turn = False
            print(player.name + "'s turn got skipped by handcuffs")
        else:
            player.skipped_last_turn = False
            self.do_turn()

    def next_round(self):
        events: list[TurnEvents] = []
        self.state = self.rounds.next_round()

        lives = self.rounds.current_round.lives
        for player in self.players:
            player.health = lives
            player.max_health = lives
        for items in self.player_items:
            items.create_empty_dict(self.available_items)
        events.append(NewRound(lives))
        events.extend(self.next_loadout())
        return events

    def next_loadout(self) -> list[TurnEvents]:
        def random_item():
            return self.available_items[random.randint(0, len(self.available_items) - 1)]
        events: list[TurnEvents] = []

        for index, player in enumerate(self.players):
            player.skip_next_turn = False
            player.skipped_last_turn = False
            for i in range(self.rounds.current_round.items):
                event = self.player_items[index].add_item(random_item())
                if type(player) is Human:
                    events.append(event)

        self.currentPlayer = 0
        shell_event = self.rounds.load_next_shells(self.shotgun)
        events.append(shell_event)
        for player in self.players:
            player.fill_with_empty_shells(shell_event.total)
        self.state = GameState.CONTINUE

        return events

    def get_player_health(self) -> list[tuple[str, int]]:
        return [(player.name, player.health) for player in self.players]

    def turn_events(self) -> list[TurnEvents]:
        pass

    def print_info(self):
        for player in self.players:
            print(player.name + ": " + "⚡︎" * player.health)

    def get_health(self) -> list[tuple[str, int]]:
        result: list[tuple[str, int]] = []
        for player in self.players:
            result.append((player.name, player.health))
        return result

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