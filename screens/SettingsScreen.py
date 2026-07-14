from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Static, Footer

from widgets.Confirm import Confirm
from widgets.SimpleButton import SimpleButton


class SettingsScreen(Screen):
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
        Binding("escape", "pop_screen", "Go Back", show=False),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.index = 0

    def compose(self) -> ComposeResult:
        with Center():
            with Vertical(id="root"):
                yield Static("This will someday become the Settings Screen")
                yield SimpleButton(label="Cancel")
                yield Confirm()
        yield Footer()

    def on_confirm_cancelled(self, event: Confirm.Cancelled) -> None:
        self.app.pop_screen()

    def on_simple_button_pressed(self, event: SimpleButton.Pressed) -> None:
        self.app.pop_screen()

    def action_pop_screen(self) -> None:
        self.app.pop_screen()