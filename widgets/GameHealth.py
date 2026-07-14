from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

class GameHealth(Vertical):
    DEFAULT_CSS = """
        GameHealth {
            width: 17;
            height: 2;
        }
    """

    def __init__(
            self,
            *,
            health: list[tuple[str, int]],
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)
        self.health = health

    def compose(self) -> ComposeResult:
        def name_render(name: str) -> str:
            return name + ":" + " " * (7 - len(name))

        def health_render(lives: int) -> str:
            remaining_space = 8 - lives
            lives_str = "❤" * lives
            leading_space = int(remaining_space / 2)
            trailing_space = remaining_space - leading_space
            return " " * leading_space + lives_str + " " * trailing_space

        name1, lives1 = self.health[0]
        name2, lives2 = self.health[1]
        names = Text(name_render(name1)) + Text("| ") + Text(name_render(name2))
        lives = Text(health_render(lives1)) + Text("| ") + Text(health_render(lives2))

        yield Static(names)
        yield Static(lives)