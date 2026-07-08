from classes.Player import Player
from classes.Shotgun import Shotgun

players: list[Player] = []
shotgun: Shotgun = Shotgun()
currentPlayer: int = 0

def main():
    global players, shotgun, currentPlayer
    init_players(True)
    init_round(2)
    shotgun.load_shells(1,2)

    nobody_died = True
    while(nobody_died):
        print_info()
        do_turn()
        currentPlayer = (currentPlayer + 1) % len(players)

def print_info():
    for player in players:
        print(player.name + ": " + "⚡︎"*player.health)

def do_turn():
    def get_input():
        while True:
            i = input("input y to shoot yourself and d to shoot the other player").strip().lower()
            if i == "y":
                return True
            elif i == "d":
                return False

    still_going: bool = True
    player = players[currentPlayer]
    print(player.name + "'s TURN:")

    while still_going:
        yourself: bool = get_input()
        shot = player.shot(shotgun, yourself)

        if not yourself:
            still_going = False
            print(f"You shot a {"live" if shot else "blank"} Shell at the Dealer")
        elif shot:
            still_going = False
            print("You shot a live Shell at yourself")
        else:
            print("You shot a blank Shell at yourself")


def init_players(solo:bool):
    global players
    def ask_player_name(player:Player):
        while not player.set_name(input(f"Your name:")):
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
