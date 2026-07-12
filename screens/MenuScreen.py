from textual.app import App, ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Static, Footer
from textual.binding import Binding
from textual.reactive import reactive

from screens.SettingsScreen import SettingsScreen
from screens.NewGameScreen import NewGameScreen

TITLE_ART = r"""
██████╗ ██╗   ██╗ ██████╗██╗  ██╗███████╗██╗  ██╗ ██████╗ ████████╗
██╔══██╗██║   ██║██╔════╝██║ ██╔╝██╔════╝██║  ██║██╔═══██╗╚══██╔══╝
██████╔╝██║   ██║██║     █████╔╝ ███████╗███████║██║   ██║   ██║
██╔══██╗██║   ██║██║     ██╔═██╗ ╚════██║██╔══██║██║   ██║   ██║
██████╔╝╚██████╔╝╚██████╗██║  ██╗███████║██║  ██║╚██████╔╝   ██║
╚═════╝  ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝

                 ██╗     ██╗████████╗███████╗
                 ██║     ██║╚══██╔══╝██╔════╝
                 ██║     ██║   ██║   █████╗
                 ██║     ██║   ██║   ██╔══╝
                 ███████╗██║   ██║   ███████╗
                 ╚══════╝╚═╝   ╚═╝   ╚══════╝
""".strip("\n")

class MenuOption(Static):

    selected = reactive(False)

    def __init__(self, label: str) -> None:
        super().__init__(label, markup=False)
        self.label_text = label

    def watch_selected(self, selected: bool) -> None:
        self.set_class(selected, "selected")

class MenuScreen(Screen):
    CSS = """
        MenuScreen {
            background: $background;
            align: center middle;
            width: 100%;
            height: 100%;
        }

        #root {
            width: auto;
            height: auto;
            align: center middle;
        }

        #title {
            color: $text;
            text-style: bold;
            content-align: center middle;
            width: 100%;
        }

        #tagline {
            color: $text-muted;
            content-align: center middle;
            width: 100%;
            margin-top: 1;
            margin-bottom: 2;
        }

        #menu {
            width: auto;
            height: auto;
            align: center middle;
        }

        MenuOption {
            width: auto;
            min-width: 20;
            content-align: center middle;
            color: $text-muted;
            text-style: bold;
            padding: 0 2;
        }

        MenuOption.selected {
            background: $primary;
            color: $background;
        }

        #version {
            color: $text-disabled;
            dock: bottom;
            margin: 0 0 1 2;
        }
        """

    BINDINGS = [
        Binding("up", "move_up", "Up"),
        Binding("down", "move_down", "Down"),
        Binding("enter", "select", "Select"),
    ]

    OPTIONS = ["START", "SETTINGS", "EXIT"]

    VERSION = "0.1"

    def __init__(self) -> None:
        super().__init__()
        self.index = 0

    def compose(self) -> ComposeResult:
        with Center():
            with Vertical(id="root"):
                yield Static(TITLE_ART, id="title")
                yield Static("A TUI COMPUTER GAME", id="tagline")
                with Center():
                    with Vertical(id="menu"):
                        for opt in self.OPTIONS:
                            yield MenuOption(opt)
        yield Static(f"v{self.VERSION}", id="version")
        yield Footer()

    def on_mount(self) -> None:
        self._refresh_selection()

    def _options(self) -> list[MenuOption]:
        return list(self.query(MenuOption))

    def _refresh_selection(self) -> None:
        opts = self._options()
        for i, opt in enumerate(opts):
            opt.selected = i == self.index

    def action_move_up(self) -> None:
        self.index = (self.index - 1) % len(self.OPTIONS)
        self._refresh_selection()

    def action_move_down(self) -> None:
        self.index = (self.index + 1) % len(self.OPTIONS)
        self._refresh_selection()

    def action_select(self) -> None:
        choice = self.OPTIONS[self.index]
        if choice == "EXIT":
            self.app.exit()
        elif choice == "SETTINGS":
            self.app.push_screen(SettingsScreen())
        elif choice == "START":
            self.app.push_screen(NewGameScreen())