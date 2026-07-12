from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Footer, Static, Button

from widgets.Confirm import Confirm
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
            width: auto;
            min-width: 40;
            height: auto;
            align: center middle;
            border: round $accent;
            padding: 2;
        }
        
        CycleSelector {
            width: 100%;
            content-align: center middle;
            padding-top: 1;
        }
        
        #confirm {
            height: auto;
            width: 100%;
            align: center middle;
        }
        
        Static {
            height: auto;
            width: auto;
            padding: 1;
        }
    """

    BINDINGS = [
        Binding("up", "move_up", "Up"),
        Binding("down", "move_down", "Down"),
        Binding("enter", "select", "Select", show=False),
        Binding("escape", "pop_screen", "Go Back", show=False),
    ]

    def compose(self) -> ComposeResult:
        with Center():
            with Vertical(id="root"):
                yield CycleSelector(["Normal", "Endless"], label="MODE")
                yield Confirm(confirm_label="Start")

        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#root", Vertical).border_title = "New Game"

    def action_move_up(self) -> None:
        self.focus_previous()

    def action_move_down(self) -> None:
        self.focus_next()

    def on_confirm_confirmed(self, event: Confirm.Confirmed) -> None:
        selector = self.query_one(CycleSelector)
        value = selector.value
        if value == "Normal":
            print("Normal mode chosen")
        elif value == "Endless":
            print("Endless mode chosen")
        else:
            print("Invalid choice")

    def on_confirm_cancelled(self, event: Confirm.Cancelled) -> None:
        self.app.pop_screen()

    def action_select(self) -> None:
        self.focus_next()

    def action_pop_screen(self) -> None:
        self.app.pop_screen()