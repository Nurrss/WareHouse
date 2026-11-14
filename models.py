from enums import StockStatus, OrderStatus
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


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

class Delivery(ABC):

    @abstractmethod
    def cost(self) -> int:
        """Цена за доставку"""

    @abstractmethod
    def days(self) -> int:
        """За сколько дней"""

@dataclass
class Order:
    id: int
    orders: list[OrderLine]
    delivery: Delivery
    status: OrderStatus = OrderStatus.CREATED

    @property
    def items_total(self) -> int:
        return sum(order.total for order in self.orders)

    @property
    def total(self) -> int:
        return sum(order.total for order in self.orders) + self.delivery.cost()


class StandardDelivery(Delivery):

    def cost(self) -> int:
        return 0

    def days(self) -> int:
        return 10

class ExpressDelivery(Delivery):

    def cost(self) -> int:
        return 100

    def days(self) -> int:
        return 3