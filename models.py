from enums import StockStatus, OrderStatus
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

@dataclass
class OrderLine:
    item: WareHouseItem
    quantity: int
    price: int

    @property
    def total(self) -> int:
        return self.price * self.quantity

@dataclass
class Order:
    id: int
    orders: list[OrderLine]
    status: OrderStatus = OrderStatus.CREATED

    @property
    def total(self) -> int:
        return sum(order.total for order in self.orders)