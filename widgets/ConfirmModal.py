from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Middle, Vertical
from textual.screen import ModalScreen
from textual.widgets import Static

from widgets.Confirm import Confirm


class ConfirmModal(ModalScreen[bool]):
    DEFAULT_CSS = """
    ConfirmModal {
        align: center middle;
        background: $background 40%;
    }
    
    #dialog {
        width: auto;
        height: auto;
        min-height: 3;
        background: $surface;
        border: round $primary;
        align: center middle;
        content-align: center middle;
    }
    
    #label {
        width: 100%;
        height: auto;
        align: center middle;
        content-align: center middle;
        padding-top: 1
    }
    """

    BINDINGS = [
        Binding("escape", "escape", "Dismiss", show=False),
    ]

    def __init__(
            self,
            *,
            cancel_label: str = "NO",
            confirm_label: str = "YES",
            only_acknowledge: bool = False,
            text:str = "Are you sure?",
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)
        self.cancel_label = cancel_label
        self.confirm_label = confirm_label
        self.only_acknowledge = only_acknowledge
        self.text = text

    def on_mount(self) -> None:
        self.query_one("#label", Static).styles.width = len(self.text) + 8

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Static(self.text, id="label")
            yield Confirm(cancel_label=self.cancel_label, confirm_label=self.confirm_label, id="confirm", only_acknowledge=self.only_acknowledge)


    def on_confirm_confirmed(self, event: Confirm.Confirmed) -> None:
        self.dismiss(True)

    def on_confirm_cancelled(self, event: Confirm.Cancelled) -> None:
        self.dismiss(False)

    def action_escape(self) -> None:
        if self.only_acknowledge:
            self.dismiss(True)
        else:
            self.dismiss(False)