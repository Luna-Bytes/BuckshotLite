from __future__ import annotations
from typing import Generic, TypeVar, Sequence

from textual.widget import Widget
from textual.reactive import reactive
from textual.binding import Binding
from textual.message import Message


T = TypeVar("T")


class CycleSelector(Widget, Generic[T], can_focus=True): # type: ignore[misc]
    """A '< value >' widget you cycle through with left/right."""

    DEFAULT_CSS = """
    CycleSelector {
        width: auto;
        height: 1;
        padding: 0 1;
    }
    CycleSelector:focus {
        text-style: bold reverse;
    }
    """

    BINDINGS = [
        Binding("left", "prev", "Previous"),
        Binding("right", "next", "Next"),
    ]

    index = reactive(0)

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

    def render(self) -> str:
        text = f"< {self.options[self.index]} >"
        return f"{self.label}: {text}" if self.label else text

    def action_prev(self) -> None:
        self.index = (self.index - 1) % len(self.options)

    def action_next(self) -> None:
        self.index = (self.index + 1) % len(self.options)

    def watch_index(self) -> None:
        self.post_message(self.Changed(self, self.value))