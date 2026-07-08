from classes.Shell import Shell

class Player:
    def __init__(self):
        self.name: str = ""
        self.shells: list[Shell] = []
        self.health: int = 0
        self.otherPlayer: None|Player = None


