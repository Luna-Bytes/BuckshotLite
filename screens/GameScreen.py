import random

from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Middle
from textual.screen import Screen
from textual.widgets import Footer

from classes.Enums import Game, ItemCount, ItemType, Target, TurnEvents, GameEnd, NewRound, NewShells, ItemGained, \
    KnownShells, ShellKnowledge, KnowledgeType
from classes.GameManager import GameManager
from classes.Item import Handcuffs, Saw, Cigarette, MagnifyingGlass, Beer
from utils.dialogs import modal_wait
from widgets.PlayerSelectModal import PlayerSelectModal
from widgets.SelectWidget import SelectWidget
from widgets.ConfirmModal import ConfirmModal
from widgets.GameHealth import GameHealth
from widgets.ItemWidget import ItemWidget
from widgets.ShellDisplay import ShellDisplay


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

    tmp_shells: list[KnownShells] = [
        KnownShells(
            type= ShellKnowledge.BLANK,
            known_by=KnowledgeType.FIRED,
            inverted=False
        ),
        KnownShells(
            type=ShellKnowledge.LIVE,
            known_by=KnowledgeType.FIRED,
            inverted=False
        ),
        KnownShells(
            type=ShellKnowledge.LIVE,
            known_by=KnowledgeType.NONE,
            inverted=True
        ),
        KnownShells(
            type=ShellKnowledge.UNKNOWN,
            known_by=KnowledgeType.NONE,
            inverted=False
        ),
        KnownShells(
            type=ShellKnowledge.LIVE,
            known_by=KnowledgeType.TELEFON,
            inverted=False
        ),
        KnownShells(
            type=ShellKnowledge.UNKNOWN,
            known_by=KnowledgeType.NONE,
            inverted=False
        ),
        KnownShells(
            type=ShellKnowledge.UNKNOWN,
            known_by=KnowledgeType.NONE,
            inverted=False
        ),
        KnownShells(
            type=ShellKnowledge.UNKNOWN,
            known_by=KnowledgeType.NONE,
            inverted=False
        )
    ]

    game: GameManager = None

    def __init__(self) -> None:
        super().__init__()
        self.game_setup: Game = None

    def compose(self) -> ComposeResult:
        with Center():
            with Middle():
                yield GameHealth(health=[("AUTUMN", 3), ("DEALER", 3)])
                yield ItemWidget(items=self.tmp_item_count, player_name="AUTUMN")
                yield SelectWidget(options=["SELF", "DEALER"])
                yield ShellDisplay(shells=self.tmp_shells, index=3)
        yield Footer()

    def action_shoot(self) -> None:
        self.target_select()

    @work(exclusive=True)
    async def target_select(self) -> None:
        await modal_wait(self.app, PlayerSelectModal())

    @work(exclusive=True)
    async def handel_events(self, events: list[TurnEvents] | TurnEvents) -> None:
        def item_type_to_name(_type: ItemType) -> str:
            items = [Handcuffs(), Saw(), Cigarette(), MagnifyingGlass(), Beer()]
            for item in items:
                if item.type == _type:
                    return item.name
            return "idk"

        if not isinstance(events, list):
            events = [events]

        for event in events:
            match event:
                case GameEnd():
                    pass
                case NewRound(lives=lives):
                    await modal_wait(self.app, ConfirmModal(
                        only_acknowledge=True,
                        confirm_label="OK",
                        text=f"New Round with {lives} lives per Player"
                        )
                    )
                case NewShells(lives=lives,blankes=blankes, total=total):
                    await modal_wait(self.app, ConfirmModal(
                        only_acknowledge=True,
                        confirm_label="OK",
                        text=f"Shotgun was loaded in a random Order with {lives} Lives and {blankes} Blankes"
                        )
                    )
                case ItemGained(type=item_type):
                    await modal_wait(self.app, ConfirmModal(
                        only_acknowledge=True,
                        confirm_label="OK",
                        text="You gained a " + item_type_to_name(item_type)
                        )
                    )

    async def on_mount(self) -> None:
        self.game_setup = self.app.pending_game
        self.setup_game()

    @work(exclusive=True)
    async def setup_game(self) -> None:
        def get_random_text():
            return self.ominous_texts[random.randint(0, len(self.ominous_texts) - 1)]

        await modal_wait(self.app, ConfirmModal(only_acknowledge=True, text=get_random_text()))

        game = GameManager()
        self.handel_events(game.setup(self.game_setup))

    def action_reset(self) -> None:
        self.app.start_game(self.game_setup)