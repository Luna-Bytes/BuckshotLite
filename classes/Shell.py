class Shell:
    def __init__(self, is_live: bool):
        self.firstType: bool = is_live
        self.isLive: bool = is_live
        self.isInverted: bool = False
        self.isKnown = False

    def invert(self):
        if not self.isInverted:
            self.isInverted = not self.isInverted
            self.isLive = not self.isLive

    def get_state(self):
        return self.isLive

    def __str__(self):
        return f"Shell({'live' if self.isLive else 'blank'})"

    def __repr__(self):
        return f"Shell({'live' if self.isLive else 'blank'})"