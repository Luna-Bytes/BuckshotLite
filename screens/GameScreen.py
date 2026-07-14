import random

from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Middle
from textual.screen import Screen
from textual.widgets import Footer

from classes.Enums import Game, ItemCount, ItemType, Target
from utils.dialogs import modal_wait
from widgets.PlayerSelectModal import PlayerSelectModal
from widgets.SelectWidget import SelectWidget
from widgets.ConfirmModal import ConfirmModal
from widgets.GameHealth import GameHealth
from widgets.ItemWidget import ItemWidget


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
        Binding("r", "reset", "Reset"),
        Binding("x", "shoot", "Shoot"),
    ]

    tmp_item_count: list[ItemCount] = [
        ItemCount(
            type= ItemType.BEER,
            count= 1,
            name="Beer"
        ),
        ItemCount(
            type= ItemType.HANDCUFFS,
            count= 1,
            name="Handcuff"
        ),
        ItemCount(
            type= ItemType.CIGARETTE,
            count= 1,
            name="Cigarette"
        ),
        ItemCount(
            type= ItemType.MAGNIFYING_GLASS,
            count= 5,
            name="Magnifying Glass"
        ),
        ItemCount(
            type= ItemType.SAW,
            count= 0,
            name="Saw"
        )
    ]

    def __init__(self) -> None:
        super().__init__()
        self.game_setup: Game = None

    def compose(self) -> ComposeResult:
        with Center():
            with Middle():
                yield GameHealth(health=[("AUTUMN", 3), ("DEALER", 3)])
                yield ItemWidget(items=self.tmp_item_count, player_name="AUTUMN")
                yield SelectWidget(options=["SELF", "DEALER"])
        yield Footer()

    def action_shoot(self) -> None:
        self.target_select()

    @work(exclusive=True)
    async def target_select(self) -> None:
        await modal_wait(self.app, PlayerSelectModal())

    def on_mount(self) -> None:
        def get_random_text():
            return self.ominous_texts[random.randint(0,len(self.ominous_texts)-1)]
        self.game_setup = self.app.pending_game
        self.app.push_screen(ConfirmModal(only_acknowledge=True, text=get_random_text()))

    def action_reset(self) -> None:
        self.app.start_game(self.game_setup)