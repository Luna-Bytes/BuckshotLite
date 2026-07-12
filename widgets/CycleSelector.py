from __future__ import annotations
from typing import Generic, TypeVar, Sequence

from rich.text import Text
from textual.widget import Widget
from textual.reactive import reactive
from textual.binding import Binding
from textual.message import Message


T = TypeVar("T")


class CycleSelector(Generic[T], Widget, can_focus=True):
    """A '< value >' widget you cycle through with left/right."""

    DEFAULT_CSS = """
    CycleSelector {
        width: auto;
        height: auto;
        padding: 0 1;
    }
    """

    BINDINGS = [
        Binding("left", "prev", "Previous"),
        Binding("right", "next", "Next"),
    ]

    index = reactive(0, layout=True)

    class Changed(Message):
        def __init__(self, selector: "CycleSelector", value: T) -> None:
            self.value = value
            super().__init__()
            self.selector = selector

    def __init__(
        self,
        options: Sequence[T],
        *,
        initial: int = 0,
        label: str | None = None,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)
        self.options = list(options)
        self.index = initial
        self.label = label

    @property
    def value(self) -> T:
        return self.options[self.index]

    def render(self) -> Text:
        value_text = Text(f"{self.options[self.index]}")
        if self.has_focus:
            value_text.stylize("bold reverse")

        if self.label:
            return Text(f"{self.label}: < ") + value_text + Text(" >")
        return value_text

    def action_prev(self) -> None:
        self.index = (self.index - 1) % len(self.options)

    def action_next(self) -> None:
        self.index = (self.index + 1) % len(self.options)

    def watch_index(self) -> None:
        self.post_message(self.Changed(self, self.value))

    def on_focus(self) -> None:
        self.refresh()

    def on_blur(self) -> None:
        self.refresh()