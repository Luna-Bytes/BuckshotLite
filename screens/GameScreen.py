import random

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Static, Footer

from classes.Enums import Game
from widgets.ConfirmModal import ConfirmModal


class GameScreen(Screen):
    CSS = """
        GameScreen {
            background: $background;
            align: center middle;
            width: 100%;
            height: 100%;
        }
        """

    ominous_text_1 = r"""
There’s one at the door, at the gate to damnation
Is it thief, thug or whore?
There’s one at the door
and there’s room for one more 
until the end of creation.
    """.strip("\n")

    ominous_text_2 = r"""
Along the shore the cloud waves break,
The twin suns sink behind the lake,
The shadows lengthen
In Carcosa.

Strange is the night where black stars rise,
And strange moons circle through the skies
But stranger still is
Lost Carcosa.

Songs that the Hyades shall sing,
Where flap the tatters of the King,
Must die unheard in
Dim Carcosa.

Song of my soul, my voice is dead;
Die thou, unsung, as tears unshed
Shall dry and die in
Lost Carcosa.
        """.strip("\n")

    ominous_text_3 = r"""
What power would hell have;
if those imprisoned here,
would not be able to dream of heaven?
""".strip("\n")

    ominous_texts = [ominous_text_1, ominous_text_2, ominous_text_3]

    BINDINGS = [
        Binding("r", "reset", "Reset")
    ]

    def __init__(self) -> None:
        super().__init__()
        self.game_setup: Game = None

    def compose(self) -> ComposeResult:
        yield Static("This will someday become the Game Screen")
        yield Footer()

    def on_mount(self) -> None:
        def get_random_text():
            return self.ominous_texts[random.randint(0,len(self.ominous_texts)-1)]
        self.game_setup = self.app.pending_game
        self.app.push_screen(ConfirmModal(only_acknowledge=True, text=get_random_text()))

    def action_reset(self) -> None:
        self.app.start_game(self.game_setup)