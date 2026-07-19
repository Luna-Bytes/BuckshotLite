from __future__ import annotations

from rich.console import Group
from rich.text import Text
from textual.widget import Widget
from textual.reactive import reactive

from classes.Enums import KnownShells, ShellKnowledge, KnowledgeType


class ShellDisplay(Widget, can_focus=False):

    DEFAULT_CSS = """
    ShellDisplay {
        min-width: 10;
        min-height: 3;
        width: auto;
        height: auto;
        padding: 0 1;
    }
    """

    index: reactive[int] = reactive(0, layout=True)
    shells: reactive[list[ShellKnowledge]] = reactive([
        KnownShells(
            type= ShellKnowledge.BLANK,
            known_by=KnowledgeType.FIRED,
            inverted=False
        ) for _ in range(3)
    ], layout=True)

    def __init__(
        self,
        *,
        shells: list[KnownShells]|None = None,
        index: int = 0,
        **kwargs,
    ) -> None:
        if shells is None:
            shells = [KnownShells(
            type= ShellKnowledge.BLANK,
            known_by=KnowledgeType.FIRED,
            inverted=False
        ) for _ in range(3)]
        super().__init__(**kwargs)
        self.shells = shells
        self.index = index


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