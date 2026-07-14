from textual.app import ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Static

from classes.Enums import Target
from widgets.Confirm import Confirm
from widgets.SelectWidget import SelectWidget


class PlayerSelectModal(ModalScreen[Target]):
    DEFAULT_CSS = """
    PlayerSelectModal {
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

    #select {
        width: 100%;
        padding-top: 1;
    }
    """

    BINDINGS = [

    ]

    class Selected(Message):
        def __init__(self, target: Target) -> None:
            self.target = target
            super().__init__()

    def __init__(
            self,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)

    def on_mount(self) -> None:
        longest_line = len("Who do you want to shoot?")
        self.query_one("#label", Static).styles.width = longest_line + 8
        self.query_one("#select").focus() #prevent Confirm from stealing focus

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Static("Who do you want to shoot?", id="label")
            yield SelectWidget(["SELF", "DEALER"], id="select")
            yield Confirm(only_acknowledge=True,confirm_label="Cancel", id="confirm")

    def on_select_widget_selected(self, event: SelectWidget.Selected) -> None:
        choice = event.option
        if choice == "SELF":
            self.dismiss(Target.SELF)
        else:
            self.dismiss(Target.OTHER)

    def on_confirm_confirmed(self, event: Confirm.Confirmed) -> None:
        self.dismiss(Target.NONE)