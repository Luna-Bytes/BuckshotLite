from rich.text import Text
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

class GameHealth(Vertical):
    DEFAULT_CSS = """
        GameHealth {
            width: 18;
            height: 2;
        }
    """

    health: reactive[list[tuple[str, int]]] = reactive([("PLAYER", 2),("DEALER", 2)], layout=True)

    def __init__(
            self,
            *,
            health: list[tuple[str, int]] = [("PLAYER", 2),("DEALER", 2)],
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.health = health

    def compose(self) -> ComposeResult:
        self.names_static = Static()
        self.lives_static = Static()
        yield self.names_static
        yield self.lives_static
        self._render_health()

    def watch_health(self, health: list[tuple[str, int]]) -> None:
        if self.is_mounted:
            self._render_health()

    def _render_health(self) -> None:
        def name_render(name: str) -> str:
            return name + ":" + " " * (7 - len(name))

        def health_render(lives: int) -> str:
            remaining_space = 8 - lives
            lives_str = "❤" * lives
            leading_space = remaining_space // 2
            trailing_space = remaining_space - leading_space
            return " " * leading_space + lives_str + " " * trailing_space

        name1, lives1 = self.health[0]
        name2, lives2 = self.health[1]
        self.names_static.update(
            Text(name_render(name1)) + Text("| ") + Text(name_render(name2))
        )
        self.lives_static.update(
            Text(health_render(lives1)) + Text("| ") + Text(health_render(lives2))
        )