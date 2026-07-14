from __future__ import annotations

from textual.containers import Horizontal
from textual.binding import Binding
from textual.message import Message

from widgets.SimpleButton import SimpleButton


class Confirm(Horizontal):
    DEFAULT_CSS = """
        Confirm {
            width: 100%;
            height: 3;
            align: center middle;
            content-align: center middle;
        }

        Confirm > SimpleButton {
            margin: 0 2;
        }
    """

    BINDINGS = [
        Binding("left", "move_left", "Left"),
        Binding("right", "move_right", "Right"),
    ]

    class Confirmed(Message):
        def __init__(self, confirm: "Confirm") -> None:
            self.confirm = confirm
            super().__init__()

    class Cancelled(Message):
        def __init__(self, confirm: "Confirm") -> None:
            self.confirm = confirm
            super().__init__()

    def __init__(
        self,
        *,
        cancel_label: str = "Cancel",
        confirm_label: str = "OK",
        only_acknowledge: bool = False,
        initial: int = 1,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)
        self.cancel_label = cancel_label
        self.confirm_label = confirm_label
        self.index = initial
        self.only_acknowledge = only_acknowledge

    def compose(self):
        if not self.only_acknowledge:
            yield SimpleButton(label=self.cancel_label, id="cancel")
        yield SimpleButton(label=self.confirm_label, id="confirm")

    def on_mount(self) -> None:
        if self.only_acknowledge:
            self.query_one("#confirm", SimpleButton).focus()
        else:
            self.query_one("#cancel", SimpleButton).focus()

    def action_move_left(self) -> None:
        self.query_one("#cancel", SimpleButton).focus()

    def action_move_right(self) -> None:
        self.query_one("#confirm", SimpleButton).focus()

    def on_simple_button_pressed(self, event: SimpleButton.Pressed) -> None:
        event.stop()
        if event.simple_button.id == "cancel":
            self.post_message(self.Cancelled(self))
        else:
            self.post_message(self.Confirmed(self))

    def on_focus(self) -> None:
        self.refresh()

    def on_blur(self) -> None:
        self.refresh()