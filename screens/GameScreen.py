from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Static, Footer


class GameScreen(Screen):
    CSS = """
        SettingsScreen {
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

        Static {
            align: center middle;
            width: auto;
        }
        """

    BINDINGS = [

    ]

    def __init__(self) -> None:
        super().__init__()
        self.index = 0

    def compose(self) -> ComposeResult:
        with Center():
            with Vertical(id="root"):
                yield Static("This will someday become the Game Screen")
        yield Footer()