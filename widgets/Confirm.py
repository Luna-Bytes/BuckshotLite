from __future__ import annotations

from rich.text import Text
from textual.widget import Widget
from textual.reactive import reactive
from textual.binding import Binding
from textual.message import Message


class Confirm(Widget, can_focus=True):

    DEFAULT_CSS = """
    Confirm {
        width: 100%;
        height: 3;
        content-align: center middle;
        padding: 1;
    }
    """

    BINDINGS = [
        Binding("left", "move_left", "Left"),
        Binding("right", "move_right", "Right"),
        Binding("enter", "select", "Select"),
    ]

    index = reactive(0)

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
        initial: int = 1,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)
        self.cancel_label = cancel_label
        self.confirm_label = confirm_label
        self.index = initial

    def _on_mount(self) -> None:
        self.styles.min_width = len(self.cancel_label) + len(self.confirm_label) + 5

    def render(self) -> Text:
        confirm_text = Text(self.confirm_label)
        cancel_text = Text(self.cancel_label)

        if self.has_focus:
            if self.index == 1:
                confirm_text.stylize("bold reverse")
            else:
                cancel_text.stylize("bold reverse")

        return cancel_text + Text("   ") + confirm_text

    def action_move_left(self) -> None:
        self.index = 0
        self.refresh()

    def action_move_right(self) -> None:
        self.index = 1
        self.refresh()

    def action_select(self) -> None:
        if self.index == 0:
            self.post_message(self.Cancelled(self))
        else:
            self.post_message(self.Confirmed(self))

    def on_focus(self) -> None:
        self.refresh()

    def on_blur(self) -> None:
        self.refresh()