from typing import Type

from textual import work
from textual._path import CSSPathType
from textual.app import App
from textual.binding import Binding
from textual.driver import Driver
from textual.reactive import reactive
from textual.theme import Theme

from classes.Enums import Game
from screens.MenuScreen import MenuScreen
from screens.GameScreen import GameScreen

from utils.dialogs import confirm_dialog

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


class BuckshotTUI(App):
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", priority=True),
        Binding("ctrl+t", "cycle_theme", "Cycle theme", priority=True),
    ]

    THEMES = ["catppuccin-mocha", "nord", "gruvbox", "textual-dark"]
    theme_index: reactive[int] = reactive(0)

    MODES = {
        "home": MenuScreen,
        "game": GameScreen,
    }
    DEFAULT_MODE = "home"

    def __init__(
            self,
            driver_class: Type[Driver] | None = None,
            css_path: CSSPathType | None = None,
            watch_css: bool = False,
            ansi_color: bool | None = None,
    ):
        super().__init__(driver_class, css_path, watch_css, ansi_color)
        self.pending_game = None
        self.is_first_game = True

    def start_game(self, game: Game):
        self.pending_game = game
        self.switch_mode("game")
        if not self.is_first_game:
            if len(self.screen_stack) > 1:
                self.pop_screen()
            self.push_screen(GameScreen())
        self.is_first_game = False

    def on_mount(self) -> None:
        self.register_theme(CATPPUCCIN_MOCHA)
        self.theme = self.THEMES[self.theme_index]
        self.switch_mode("home")

    def action_cycle_theme(self) -> None:
        self.theme_index = (self.theme_index + 1) % len(self.THEMES)
        self.theme = self.THEMES[self.theme_index]

    def action_quit(self) -> None:
        self.confirm_and_quit()

    @work(exclusive=True)
    async def confirm_and_quit(self) -> None:
        if await confirm_dialog(self, text="Are you sure you want to quit?"):
            self.exit()


if __name__ == '__main__':
    app = BuckshotTUI()
    app.run()
