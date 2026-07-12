from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Static

from widgets.CycleSelector import CycleSelector


class NewGameScreen(Screen):
    CSS = """
        NewGameScreen {
            background: $background;
            align: center middle;
            width: 100%;
            height: 100%;
        }
        
        #root {
            width: 50%;
            height: auto;
            align: center middle;
            border: round $accent;
        }
        
        Static {
            align: center middle;
            width: auto;
            padding: 3;
        }
    """

    BINDINGS = [
        Binding("up", "move_up", "Up"),
        Binding("down", "move_down", "Down"),
        Binding("left", "move_left", "Left"),
        Binding("right", "move_right", "Right"),
        Binding("enter", "select", "Select"),
    ]

    def compose(self) -> ComposeResult:
        with Center():
            with Vertical(id="root"):
                yield CycleSelector(["Normal", "Endless"], label="MODE")

        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#root", Vertical).border_title = "New Game"