import random
from enum import Enum

from classes.Player import Player
from classes.Shotgun import Shotgun, ShellCount


class GameState(Enum):
    CONTINUE = 0
    NEXT_ROUND = 1
    GAME_OVER = 2
    GAME_WON = 3

players: list[Player] = []
shotgun: Shotgun = Shotgun()
currentPlayer: int = 0
state: GameState = GameState.CONTINUE


def main():
    global players, shotgun, currentPlayer, state
    init_players(True)
    init_round(2)
    shotgun.load_shells(1,2)

    while state == GameState.CONTINUE:
        print_info()
        next_player()
        currentPlayer = (currentPlayer + 1) % len(players)
        if state == GameState.NEXT_ROUND:
            shotgun.load_shells(2,3)
            state = GameState.CONTINUE

def next_player():
    global players
    player = players[currentPlayer]
    if player.isAI:
        ai_turn()
    else:
        do_turn()

def update_state():
    global state, players, shotgun
    for player in players:
        if player.health == 0:
            state = GameState.GAME_OVER
            return
    if shotgun.remainingShells == 0:
        state = GameState.NEXT_ROUND
        return
    state = GameState.CONTINUE
    return

def print_info():
    for player in players:
        print(player.name + ": " + "⚡︎"*player.health)

def ai_turn():
    def chance(percent):
        return random.random() < percent / 100
    global players
    player = players[currentPlayer]
    keep_going = True

    print(player.name + "'s TURN:")
    while state == GameState.CONTINUE and keep_going:
        remaining_shells: int = shotgun.remainingShells
        remaining_types: ShellCount = shotgun.remainingTypes

        shot_self = False
        if remaining_shells == shotgun.remainingTypes.live:
            shot = player.shot(shotgun, shot_self=False)
        elif remaining_shells == shotgun.remainingTypes.blank:
            shot_self = True
            shot = player.shot(shotgun, shot_self=True)
        else:
            shot_self = not chance((remaining_types.live / remaining_shells))
            shot = player.shot(shotgun, shot_self=shot_self)

        if not shot_self or shot:
            keep_going = False

        print(player.name + " shot " + ("himself" if shot_self else "you") + " with a " + ("live" if shot else "blank") + " Shell")
        update_state()


def do_turn():
    global state
    def get_input():
        while True:
            i = input("input y to shoot yourself and d to shoot the other player: ").strip().lower()
            if i == "y":
                return True
            elif i == "d":
                return False

    still_going: bool = True
    player = players[currentPlayer]
    print(player.name + "'s TURN:")

    while still_going and state == GameState.CONTINUE:
        yourself: bool = get_input()
        shot = player.shot(shotgun, yourself)

        if not yourself:
            still_going = False
        elif shot:
            still_going = False

        print("You shot a " + ("live" if shot else "blank") + " Shell at " + ("yourself" if yourself else "the Dealer"))
        update_state()

def init_players(solo:bool):
    global players
    def ask_player_name(player:Player):
        while not player.set_name(input(f"Your name: ")):
            print("You can't choose that name")

    players = [Player() for i in range(2)]
    if solo:
        ask_player_name(players[0])
        players[1].set_dealer()

    players[0].set_other_player(players[1])
    players[1].set_other_player(players[0])

def init_round(lives:int):
    global players
    for player in players:
        player.health = lives

    print(f"Each player has {lives} lives")

if __name__ == '__main__':
    main()
