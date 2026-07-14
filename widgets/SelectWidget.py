from rich.console import Group
from rich.text import Text

from textual.binding import Binding
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget

class SelectWidget(Widget, can_focus=True):
    class Selected(Message):
        def __init__(self, option: str, index: int) -> None:
            self.option = option
            self.index = index
            super().__init__()

    DEFAULT_CSS = """
    SelectWidget {
        width: auto;
        height: auto;
        align: center middle;
        content-align: center middle;
    }
    """

    BINDINGS = [
        Binding("up", "move_up", "Up"),
        Binding("down", "move_down", "Down"),
        Binding("enter", "select", "Select")
    ]

    options: reactive[list[str]] = reactive(list)
    selected_index: reactive[int] = reactive(0)

    def __init__(self, options: list[str], **kwargs):
        super().__init__(**kwargs)
        self.options = options
        self.width = max([len(option) for option in options])

    def watch_options(self, options: list[str]) -> None:
        self.selected_index = min(
            self.selected_index,
            len(options) - 1
        )
        self.refresh()

    def watch_selected_index(self, _: int) -> None:
        self.refresh()

    def action_move_up(self) -> None:
        if self.options:
            self.selected_index = (self.selected_index - 1) % len(self.options)

    def action_move_down(self) -> None:
        if self.options:
            self.selected_index = (self.selected_index + 1) % len(self.options)

    def action_select(self) -> None:
        option = self.options[self.selected_index]

        if option is not None:
            self.post_message(
                self.Selected(option, self.selected_index)
            )

    @property
    def selected_option(self) -> str | None:
        if not self.options:
            return None
        return self.options[self.selected_index]

    def on_mount(self) -> None:
        self.styles.min_width = max([len(option) for option in self.options])
        self.styles.min_height = len(self.options)

    def render(self):
        max_width = self.width
        lines: list[Text] = []

        for i, option in enumerate(self.options):
            line = Text(option.center(max_width))

            if i == self.selected_index and self.has_focus:
                line.stylize("bold reverse")

            lines.append(line)

        return Group(*lines)

    def on_focus(self) -> None:
        self.refresh()

    def on_blur(self) -> None:
        self.refresh()