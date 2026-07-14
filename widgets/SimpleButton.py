from rich.text import Text
from textual.binding import Binding
from textual.message import Message
from textual.widget import Widget


class SimpleButton(Widget, can_focus=True):
    DEFAULT_CSS = """
       SimpleButton {
           width: auto;
           height: auto;
       }
       """


    BINDINGS = [
        Binding("enter", "select", "Select"),
    ]

    class Pressed(Message):
        def __init__(self, simple_button: "SimpleButton") -> None:
            self.simple_button = simple_button
            super().__init__()

    def __init__(
            self,
            *,
            label: str,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
    ) -> None:
        super().__init__(name=name,id=id,classes=classes)
        self.label = label

    def on_mount(self) -> None:
        self.styles.min_width = len(self.label)

    def render(self) -> Text:
        text = Text(self.label)

        if self.has_focus:
            text.stylize("bold reverse")

        return text

    def action_select(self) -> None:
        self.post_message(self.Pressed(self))


    def on_focus(self) -> None:
        self.refresh()

    def on_blur(self) -> None:
        self.refresh()