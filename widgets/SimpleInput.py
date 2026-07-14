from __future__ import annotations

from rich.text import Text
from textual import events
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget


class SimpleInput(Widget, can_focus=True):

    DEFAULT_CSS = """
    SimpleInput {
        width: auto;
        height: 1;
    }
    """

    value: reactive[str] = reactive("", init=False)

    class Changed(Message):
        def __init__(self, simple_input: "SimpleInput", value: str) -> None:
            self.simple_input = simple_input
            self.value = value
            super().__init__()

    def __init__(
        self,
        *,
        label: str,
        mark_label: bool = True,
        force_upper: bool = False,
        max_chars: int | None = None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.label = label
        self.max_chars = max_chars
        self.mark_label = mark_label
        self.force_upper = force_upper

    def get_value(self) -> str:
        return self.value

    def render(self) -> Text:
        label = Text(self.label)

        if self.max_chars is not None:
            remaining = self.max_chars - len(self.value)
            body = Text(self.value) + Text("_" * max(remaining, 0), style="dim")
        else:
            body = Text(self.value) if self.value else Text("_", style="dim")

        if self.has_focus:
            if self.mark_label:
                label.stylize("reverse")
            else:
                body.stylize("reverse")

        return label + Text(": ") + body

    def on_key(self, event: events.Key) -> None:
        if event.key == "backspace":
            self.value = self.value[:-1]
            event.stop()
        elif event.character is not None and event.character.isprintable():
            if self.max_chars is None or len(self.value) < self.max_chars:
                self.value += event.character
                if self.force_upper:
                    self.value = self.value.upper()
            event.stop()
        else:
            return

        self.post_message(self.Changed(self, self.value))
        self.refresh()

    def on_focus(self) -> None:
        self.refresh()

    def on_blur(self) -> None:
        self.refresh()