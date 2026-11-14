from models import WareHouseItem, ItemCategory, Order, OrderLine, Delivery
from exception import (
    CategoryAlreadyExists,
    CategoryNotFound,
    ItemAlreadyExists,
    ItemNotFound,
    InvalidQuantity,
    InvalidPrice,
    OrderNotFound,
    InvalidStatusTransition,
    NotEnoughStock
)
from enums import OrderStatus
import time
from contextlib import contextmanager

class WareHouse:
    def __init__(self) -> None:
        self.items: dict[int, WareHouseItem] = {}
        self.categories: dict[int, ItemCategory] = {}
        self.orders: dict[int, Order] = {}
        
    def create_item(self, item_id : int, title: str, category_id: int, price:int) -> WareHouseItem:
        category = self._get_category(category_id)

        if item_id in self.items:
            raise ItemAlreadyExists(item_id)
        if price < 0:
            raise InvalidPrice(price)
           
        item = WareHouseItem(item_id, title, category, price)                                   
        self.items[item_id] = item           
        return item     

    def create_category(self, category: ItemCategory) -> None:
        if category.id in self.categories:
            raise CategoryAlreadyExists(category.id)
        self.categories[category.id] = category
        
    def receive(self, item_id: int , quantity: int):
        item = self._get_item(item_id)

        if quantity < 0:
            raise InvalidQuantity(quantity)
        item.quantity += quantity

    def _get_category(self, category_id) -> ItemCategory:
        try:
            return self.categories[category_id]
        except KeyError:
            raise CategoryNotFound(category_id) from None

    def _get_item(self, item_id) -> WareHouseItem:
        try:
            return self.items[item_id]
        except KeyError:
            raise ItemNotFound(item_id) from None

    def _get_order(self, order_id) -> Order:
            try:
                return self.orders[order_id]
            except KeyError:
                raise OrderNotFound(order_id) from None

    def place_order(self, order_id: int, wanted: dict[int, int], delivery: Delivery) -> Order:
        for item_id, quantity in wanted.items():
            item = self._get_item(item_id)
            if quantity <= 0:
                raise InvalidQuantity(quantity)
            if quantity > item.quantity:
                raise NotEnoughStock(item.title)

        lines = []
        for item_id, quantity in wanted.items():
            item = self._get_item(item_id)
            item.quantity -= quantity
            lines.append(OrderLine(item, quantity, item.price))

        order = Order(order_id, lines, delivery)
        self.orders[order_id] = order
        return order
            
    def ship_order(self, order_id: int) -> None:
        order = self._get_order(order_id)
        if order.status != OrderStatus.CREATED:
            raise InvalidStatusTransition(order_id, order.status, OrderStatus.SHIPPED)
        order.status = OrderStatus.SHIPPED

    def deliver_order(self, order_id: int) -> None:
        order = self._get_order(order_id)
        if order.status != OrderStatus.SHIPPED:
            raise InvalidStatusTransition(order_id, order.status, OrderStatus.DELIVERED)
        order.status = OrderStatus.DELIVERED

    def cancel_order(self, order_id: int) -> None:
        order = self._get_order(order_id)
        if order.status in (OrderStatus.DELIVERED, OrderStatus.CANCELLED):
            raise InvalidStatusTransition(order_id, order.status, OrderStatus.CANCELLED)

        for line in order.orders:
            line.item.quantity += line.quantity
           
        order.status = OrderStatus.CANCELLED

    def category_list(self) -> list[str]:
        return [category.title for category in self.categories.values()]

    def item_list(self) -> list[WareHouseItem]:
        return [item for item in self.items.values()]

@contextmanager
def operation(name: str):
    print(f"Начало: {name}")
    start_time = time.perf_counter()
    try:
        yield
    finally:
        finish_time = time.perf_counter() - start_time
        print(f"Конец: {name} {finish_time:.4f}")