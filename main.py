from classes.Enums import GameState, Action, ShootAction, Target
from classes.Player import Player, Human, AI
from classes.RoundManager import RoundManager
from classes.Shotgun import Shotgun, ShellCount

players: list[Player] = []
shotgun: Shotgun = Shotgun()
currentPlayer: int = 0
state: GameState = GameState.CONTINUE
rounds: RoundManager = RoundManager()


def main():
    global players, shotgun, currentPlayer, state, rounds
    init_players(True)

    rounds.load_default_rounds()
    init_round(rounds.current_round.lives)
    rounds.load_next_shells(shotgun)

    while state == GameState.CONTINUE:
        print_info()
        next_player()
        currentPlayer = (currentPlayer + 1) % len(players)
        if state == GameState.NEXT_ROUND:
            state = rounds.next_round()
            init_round(rounds.current_round.lives)
            rounds.load_next_shells(shotgun)
        if state == GameState.NEXT_SHELLS:
            rounds.load_next_shells(shotgun)
            state = GameState.CONTINUE

def next_player():
    global players
    player = players[currentPlayer]

    if player.skip_next_turn:
        player.skip_next_turn = False
        print(player.name + "'s turn got skipped by handcuffs")
    else:
        player.skipped_last_turn = False
        do_turn()

def update_state():
    global state, players, shotgun
    for player in players:
        if player.health == 0:
            if player.isAI:
                state = GameState.NEXT_ROUND
            else:
                state = GameState.GAME_OVER
            return
    if shotgun.remainingShells == 0:
        state = GameState.NEXT_SHELLS
        return
    state = GameState.CONTINUE
    return

def print_info():
    for player in players:
        print(player.name + ": " + "⚡︎"*player.health)

def do_turn():
    global state

    still_going: bool = True
    player = players[currentPlayer]
    print(player.name + "'s TURN:")

    while still_going and state == GameState.CONTINUE:
        action: Action = player.do_turn(shotgun.remainingShells, shotgun.remainingTypes)

        if type(action) is ShootAction:
            was_live = player.shot(shotgun, True if action.target == Target.SELF else False)

            if action.target == Target.OTHER or was_live:
                still_going = False

            print(player.name + " shot a " + ("live" if was_live else "blank") + " Shell at " + ("themselves" if action.target == Target.SELF else player.otherPlayer.name))
        update_state()

def init_players(solo:bool):
    global players
    def ask_player_name(player:Player):
        while not player.set_name(input(f"Your name: ")):
            print("You can't choose that name")

    players = [Human(), AI()]
    if solo:
        ask_player_name(players[0])

    players[0].set_other_player(players[1])
    players[1].set_other_player(players[0])

def init_round(lives:int):
    global players, currentPlayer
    for player in players:
        player.health = lives
        player.max_health = lives
        player.skip_next_turn = False
    currentPlayer = 0

    print(f"Each player has {lives} lives")

if __name__ == '__main__':
    main()
