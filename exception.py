from enums import OrderStatus

class WareHouseError(Exception):
    """Базовая ошибка склада."""

class CategoryAlreadyExists(WareHouseError):
    def __init__(self, category_id: int):
        self.category_id = category_id
        super().__init__(f"Категория с id={category_id} уже существует")

class CategoryNotFound(WareHouseError):
    def __init__(self, category_id):
        self.category_id = category_id
        super().__init__(f"Категория с id={category_id} не найдена")

class ItemAlreadyExists(WareHouseError):
    def __init__(self, item_id: int):
        self.item_id = item_id
        super().__init__(f"Товар с id={item_id} уже существует")

class ItemNotFound(WareHouseError):
    def __init__(self, item_id: int):
        self.item_id = item_id
        super().__init__(f"Товар с id={item_id} не найден")

class InvalidQuantity(WareHouseError):
    def __init__(self, quantity: int):
        self.quantity = quantity
        super().__init__(f"Неверное количество: {quantity}")

class InvalidPrice(WareHouseError):
    def __init__(self, price: int):
        self.price = price
        super().__init__(f"Неверная цена: {price}")

class OrderNotFound(WareHouseError):
    def __init__(self, order_id):
        self.order_id = order_id
        super().__init__(f"Заказ с номером {order_id} не найден")

class InvalidStatusTransition(WareHouseError):
    def __init__(self, order_id: int, current: OrderStatus, target: OrderStatus):
        self.order_id = order_id
        self.current = current
        self.target = target
        super().__init__(f"Нельзя перевести заказ номер {order_id} из DELIVERED в CANCELLED")

class NotEnoughStock(WareHouseError):
    def __init__(self, title: str):
        self.title = title
        super().__init__(f"{title} недостаточно на складе")