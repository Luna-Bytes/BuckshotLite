from typing import List, TYPE_CHECKING

from classes.Item import Item
from classes.Shotgun import Shotgun

if TYPE_CHECKING:
    from classes.Player import Player

class ItemManager:
    def __init__(self):
        self.items: List[Item] = []
        self.max_items: int = 8
        self.amount_items: int = 0

    def add_item(self, item: Item):
        if len(self.items) <= self.max_items:
            self.items.append(item)
            self.amount_items += 1
        else:
            print("Too many items cannot add " + item.name)

    def use_item(self, item_index: int, player: Player, shotgun: Shotgun):
        self.items.pop(item_index).use(player, shotgun)
        self.amount_items -= 1

    def get_items(self) -> List[Item]:
        return self.items