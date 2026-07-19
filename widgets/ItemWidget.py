from rich.text import Text

from textual.binding import Binding
from textual.reactive import reactive
from textual.widget import Widget

from classes.Enums import ItemCount, ItemType


class ItemWidget(Widget, can_focus=True):
    DEFAULT_CSS = """
    ItemWidget {
        border: round $primary;
        padding: 0 2;
        width: auto;
        height: auto;
    }

    ItemWidget:focus {
        border: round $accent;
    }
    """

    BINDINGS = [
        Binding("up", "move_up", "Up"),
        Binding("down", "move_down", "Down")
    ]

    items: reactive[list[ItemCount]] = reactive(list, layout=True, always_update=True)
    selected_index: reactive[int] = reactive(0, layout=True, always_update=True)
    player_name: reactive[str | None] = reactive(None, layout=True)

    def __init__(self, items: list[ItemCount] | None = None, player_name: str | None = None, **kwargs):
        super().__init__(**kwargs)
        self.items = items or [ItemCount(type=ItemType.SAW, count=0, name="Saw")]
        self.player_name = player_name
        self.label = f"{player_name}'s ITEMS" if player_name is not None else "TMP ITEMS"

    def watch_items(self, _: list[ItemCount]) -> None:
        if self.selected_index >= len(self.items):
            self.selected_index = max(0, len(self.items) - 1)
        if self.items:
            self.styles.width = max(len(item.name) for item in self.items) + 10
            self.styles.height = len(self.items) + 2
        self.refresh(layout=True)

    def watch_player_name(self, name: str | None) -> None:
        self.label = f"{name}'s ITEMS" if name is not None else "TMP ITEMS"
        if self.is_mounted:
            self.border_title = self.label

    def watch_selected_index(self, _: int) -> None:
        self.refresh()

    def action_move_up(self) -> None:
        if self.items:
            self.selected_index = (self.selected_index - 1) % len(self.items)

    def action_move_down(self) -> None:
        if self.items:
            self.selected_index = (self.selected_index + 1) % len(self.items)

    @property
    def selected_item(self) -> ItemCount | None:
        if not self.items:
            return None
        return self.items[self.selected_index]

    def on_mount(self) -> None:
        self.styles.width = (max([len(item.name) for item in self.items]) + 10)
        self.styles.height = len(self.items) + 2
        self.border_title = self.label

    def render(self) -> Text:
        text = Text()

        for i, item in enumerate(self.items):
            style = "dim" if item.count == 0 else ""

            text.append(f"{item.count}x: ", style=style)

            if i == self.selected_index and self.has_focus:
                name_style = "bold reverse"
                if style:
                    name_style += f" {style}"
            else:
                name_style = style

            text.append(item.name, style=name_style)

            if i != len(self.items) - 1:
                text.append("\n")

        return text

    def on_focus(self) -> None:
        self.refresh()

    def on_blur(self) -> None:
        self.refresh()