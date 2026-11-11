from enums import StockStatus
from dataclasses import dataclass, field
from abc import ABC


@dataclass
class ItemCategory:
    id: int
    title: str

@dataclass
class WareHouseItem:
    id: int
    title: str
    category: ItemCategory
    price:int
    quantity:int = 0

    @property
    def status(self):
        return StockStatus.IN_STOCK if self.quantity > 0 else StockStatus.OUT_OF_STOCK

