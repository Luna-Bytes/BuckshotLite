from enum import Enum

class GameState(Enum):
    CONTINUE = 0
    NEXT_ROUND = 1
    GAME_OVER = 2
    GAME_WON = 3
    NEXT_SHELLS = 4