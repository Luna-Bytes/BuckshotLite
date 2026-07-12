from textual.app import App
from textual.binding import Binding
from textual.reactive import reactive
from textual.theme import Theme

from screens.MenuScreen import MenuScreen
from screens.SettingsScreen import SettingsScreen
from classes.GameManager import GameManager
from classes.Player import Player, Human, AI

CATPPUCCIN_MOCHA = Theme(
    name="catppuccin-mocha",
    primary="#89b4fa",
    secondary="#a6e3a1",
    accent="#f38ba8",
    warning="#f9e2af",
    error="#f38ba8",
    success="#a6e3a1",
    background="#1e1e2e",
    surface="#313244",
    panel="#45475a",
    foreground="#cdd6f4",
    dark=True,
)


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

class BuckshotTUI(App):
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", priority=True),
        Binding("ctrl+t", "cycle_theme", "Cycle theme", priority=True),
    ]

    THEMES = ["catppuccin-mocha", "nord", "gruvbox", "textual-dark"]
    theme_index: reactive[int] = reactive(0)

    MODES = {
        "home": MenuScreen,
        "settings": SettingsScreen,
    }
    DEFAULT_MODE = "home"

    def on_mount(self) -> None:
        self.register_theme(CATPPUCCIN_MOCHA)
        self.theme = self.THEMES[self.theme_index]
        self.switch_mode("home")

    def action_cycle_theme(self) -> None:
        self.theme_index = (self.theme_index + 1) % len(self.THEMES)
        self.theme = self.THEMES[self.theme_index]


if __name__ == '__main__':
    #main()
    app = BuckshotTUI()
    app.run()
