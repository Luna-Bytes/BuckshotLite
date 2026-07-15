from __future__ import annotations

from rich.text import Text
from textual.reactive import reactive
from textual.widgets import Static

from classes.Shotgun import ShellCount


class RoundDisplay(Static, can_focus=False):

    DEFAULT_CSS = """
    RoundDisplay {
        width: 12;
        height: 3;
        padding: 0 1;
    }
    """

    total_shells: reactive[ShellCount] = reactive(ShellCount(0, 0))
    remaining_shells: reactive[ShellCount] = reactive(ShellCount(0, 0))
    round_index: reactive[int] = reactive(0)

    def __init__(
        self,
        *,
        total_shells: ShellCount,
        remaining_shells: ShellCount,
        round_index: int = 0,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.total_shells = total_shells
        self.remaining_shells = remaining_shells
        self.round_index = round_index

    def render(self) -> Text:
        def shell_line(label: str, shells: ShellCount) -> Text:
            line = Text(f"{label}: ")

            live = Text(str(shells.live))
            live.stylize("red")

            sep = Text("/")

            blank = Text(str(shells.blank))
            blank.stylize("blue")

            return line + live + sep + blank

        round = Text(f"Round: {self.round_index}/3")
        total = shell_line("Total", self.total_shells)
        remaining = shell_line("Rest ", self.remaining_shells)

        return Text("\n").join([round, total, remaining])