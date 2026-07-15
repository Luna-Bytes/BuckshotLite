from __future__ import annotations

from rich.console import Group
from rich.text import Text
from textual.widget import Widget
from textual.reactive import reactive
from textual.binding import Binding

from classes.Enums import KnownShells, ShellKnowledge, KnowledgeType


class ShellDisplay(Widget, can_focus=False):

    DEFAULT_CSS = """
    CycleSelector {
        min-width: 10;
        min-height: 3;
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

    def __init__(
        self,
        *,
        shells: list[KnownShells],
        index: int = 0,
        label: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.shells = shells
        self.index = index
        self.label = label


    def render(self):
        padding_left: int = int((8 - len(self.shells)) / 2)
        padding_right: int = (8 - len(self.shells)) - padding_left

        lines: list[Text] = []

        lines.append(Text(" " * (padding_left + self.index) + "↓" + " " * (len(self.shells) - self.index + padding_right)))

        shells_text = Text(" " * padding_left)
        for shell in self.shells:
            if shell.inverted:
                tmp = Text("🗘")
            else:
                tmp = Text("▮")
            if shell.type == ShellKnowledge.LIVE:
                tmp.stylize("red")
            elif shell.type == ShellKnowledge.BLANK:
                tmp.stylize("blue")
            else:
                tmp.stylize("dim")
            shells_text = shells_text + tmp
        shells_text = shells_text + Text(" " * padding_right)
        lines.append(shells_text)

        known_by_text = Text(" " * padding_left)
        for shell in self.shells:
            if shell.known_by == KnowledgeType.MAGNIFYING:
                tmp = Text("M")
            elif shell.known_by == KnowledgeType.TELEFON:
                tmp = Text("T")
            else:
                tmp = Text(" ")
            known_by_text = known_by_text + tmp
        known_by_text = known_by_text + Text(" " * padding_right)
        lines.append(known_by_text)

        return Group(*lines)