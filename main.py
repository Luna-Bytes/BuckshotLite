from classes.GameManager import GameManager
from classes.Player import Player, Human, AI


def main():
    players = init_players(True)

    while True:
        game = GameManager(players)
        game.run()


def init_players(solo:bool) -> list[Player]:
    def ask_player_name(player:Player):
        while not player.set_name(input(f"Your name: ")):
            print("You can't choose that name")

    if solo:
        _players = [Human(), AI()]
        ask_player_name(_players[0])

    _players[0].set_other_player(_players[1])
    _players[1].set_other_player(_players[0])

    return _players

if __name__ == '__main__':
    main()
