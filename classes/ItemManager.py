from typing import TYPE_CHECKING

from classes.Enums import ItemCount, ItemType, ItemGained, ItemUsed
from classes.Shotgun import Shotgun

from classes.Enums import itemtype_to_name, itemtype_to_item

if TYPE_CHECKING:
    from classes.Player import Player

class ItemManager:
    def __init__(self):
        self.items: dict[ItemType, ItemCount] = {}
        self.amount_items: int = 0
        self.max_items: int = 8

    def add_item(self, item: ItemType) -> ItemGained:
        if len(self.items) <= self.max_items:
            self.items[item].count += 1
            self.amount_items += 1
            return ItemGained(item, True)
        else:
            return ItemGained(item, False)

    def create_empty_dict(self, available_items : list[ItemType]):
        for item in available_items:
            self.items[item] = ItemCount(item, 0, itemtype_to_name(item))

    def use_item(self, item_type: ItemType, player: Player, shotgun: Shotgun):
        if self.items[item_type].count >= 1:
            self.items[item_type].count -= 1
            self.amount_items -= 1
            itemtype_to_item(item_type).use(player, shotgun)
            return ItemUsed(item_type, True)
        else:
            return ItemUsed(item_type, False)

    def get_items(self) -> list[ItemCount]:
        return [ self.items[item] for item in self.items]