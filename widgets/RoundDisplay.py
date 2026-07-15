from __future__ import annotations

from rich.text import Text
from textual.widgets import Static

from classes.Shotgun import ShellCount


class RoundDisplay(Static, can_focus=False):

    DEFAULT_CSS = """
    RoundDisplay {
        width: 8;
        height: 2;
        padding: 0 1;
    }
    """

    def __init__(
        self,
        *,
        total_shells: ShellCount,
        remaining_shells: ShellCount,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.total_shells = total_shells
        self.remaining_shells = remaining_shells

    def render(self) -> Text:
        def shell_line(label: str, shells: ShellCount) -> Text:
            line = Text(f"{label}: ")

            live = Text(str(shells.live))
            live.stylize("red")

            sep = Text("/")

            blank = Text(str(shells.blank))
            blank.stylize("blue")

            return line + live + sep + blank

        total = shell_line("T", self.total_shells)
        remaining = shell_line("R", self.remaining_shells)

        return Text("\n").join([total, remaining])