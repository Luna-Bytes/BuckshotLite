import random
import os

from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer

from classes.Enums import Game, ItemCount, ItemType, TurnEvents, GameEnd, NewRound, NewShells, ItemGained
from classes.GameManager import GameManager
from classes.Item import Handcuffs, Saw, Cigarette, MagnifyingGlass, Beer
from classes.Shotgun import ShellCount
from utils.dialogs import modal_wait
from widgets.PlayerSelectModal import PlayerSelectModal
from widgets.RoundDisplay import RoundDisplay
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

    ominous_texts = [
        open(os.path.join("texts/ominous", file)).read().strip("\n")
        for file in os.listdir("texts/ominous")
    ]

    BINDINGS = [
        Binding("r", "reset", "Reset"),
        Binding("x", "shoot", "Shoot"),
    ]

    total_shells: ShellCount
    remaining_shells: ShellCount

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

    game: GameManager = None

    def __init__(self) -> None:
        super().__init__()
        self.game_health = None
        self.shell_display = None
        self.game_setup: Game = None
        self.round_display = None
        self.round: int = 0
        self.total_shells = ShellCount(0,0)
        self.remaining_shells = ShellCount(0,0)

    def compose(self) -> ComposeResult:
        self.game_health = GameHealth()
        yield self.game_health
        yield ItemWidget(items=self.tmp_item_count, player_name="AUTUMN")
        self.shell_display = ShellDisplay()
        yield self.shell_display
        self.round_display = RoundDisplay(total_shells=self.total_shells, remaining_shells=self.remaining_shells)
        yield self.round_display
        yield Footer()

    def update_info(self) -> None:
        self.total_shells = self.game.shotgun.shellTypes if self.game is not None else ShellCount(0, 0)
        self.remaining_shells = self.game.shotgun.remainingTypes if self.game is not None else ShellCount(0, 0)
        self.round = self.game.rounds.round_index + 1 if self.game is not None else 0
        self.round_display.total_shells = self.total_shells
        self.round_display.remaining_shells = self.remaining_shells
        self.round_display.round_index = self.round
        self.game_health.health = self.game.get_player_health() if self.game is not None else [("PLAYER", 2),("DEALER", 2)]
        self.shell_display.shells = self.game.players[0].shells
        self.shell_display.index = self.game.players[0].shell_index

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
        self.update_info()

    def on_mount(self) -> None:
        self.game_setup = self.app.pending_game
        self.setup_game()

    @work(exclusive=True)
    async def setup_game(self) -> None:
        def get_random_text():
            return self.ominous_texts[random.randint(0, len(self.ominous_texts) - 1)]

        await modal_wait(self.app, ConfirmModal(only_acknowledge=True, text=get_random_text()))

        self.game = GameManager()
        self.handel_events(self.game.setup(self.game_setup))

    def action_reset(self) -> None:
        self.app.start_game(self.game_setup)