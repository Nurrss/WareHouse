from warehouse import WareHouse
from models import ItemCategory, Order, ExpressDelivery, StandardDelivery
from exception import WareHouseError, ItemNotFound, InvalidStatusTransition


def show_stock(wh: WareHouse) -> None:
    for item in wh.item_list():
        print(f"  {item.id}. {item.title} [{item.category.title}] — "
              f"{item.quantity} шт., {item.price} ₸, {item.status.name}")


def show_order(order: Order) -> None:
    print(f"  Заказ №{order.id} [{order.status.name}] — итого {order.total} ₸")
    for line in order.orders:
        print(f"    • {line.item.title}: {line.quantity} × {line.price} ₸ = {line.total} ₸")


def try_it(action, *args) -> None:
    """Выполнить действие и красиво показать ошибку склада, если она будет."""
    try:
        action(*args)
    except WareHouseError as e:
        print(f"⚠️ {type(e).__name__}: {e}")


warehouse = WareHouse()

# ===== 1. Категории =====
warehouse.create_category(ItemCategory(1, "Электроника"))
warehouse.create_category(ItemCategory(2, "Продукты"))
print("Категории:", warehouse.category_list())

# ===== 2. Товары =====
warehouse.create_item(1, "Asus Rog Strix", 1, 1000)
warehouse.create_item(2, "Мышка Logitech", 1, 50)
warehouse.create_item(3, "Сахар 1 кг", 2, 5)
print("\nПосле создания:")
show_stock(warehouse)

# ===== 3. Приёмка =====
warehouse.receive(1, 20)
warehouse.receive(2, 100)
print("\nПосле приёмки:")
show_stock(warehouse)

# ===== 4. Заказы =====
print("\n--- Заказы ---")

order1 = warehouse.place_order(1, {1: 2, 2: 1}, ExpressDelivery())
order3 = warehouse.place_order(3, {1: 3}, ExpressDelivery())
show_order(order1)
print(order1.items_total)       
print(order1.delivery.cost())   
print(order1.total)   
show_order(order3)
print("Склад после оформления (ноутбуков 15, мышек 99):")
show_stock(warehouse)

# Жизнь заказа №1: на складе → курьер → доставлен
warehouse.ship_order(1)
print(f"\nЗаказ №1 передан курьеру: {order1.status.name}")
warehouse.deliver_order(1)
print(f"Заказ №1 доставлен: {order1.status.name}")

# Отмена заказа №3 — ноутбуки должны вернуться
warehouse.cancel_order(3)
print(f"\nЗаказ №3 отменён: {order3.status.name}")
print("Склад после отмены (ноутбуков снова 18):")
show_stock(warehouse)

# ===== 5. Ошибки =====
print("\n--- Ошибки: товары и категории ---")
try_it(warehouse.create_category, ItemCategory(1, "Ещё электроника"))  # повторная категория
try_it(warehouse.create_item, 10, "Телефон", 99, 500)                  # нет категории
try_it(warehouse.create_item, 1, "Другой ноутбук", 1, 900)             # повторный товар
try_it(warehouse.create_item, 11, "Наушники", 1, -100)                 # плохая цена
try_it(warehouse.receive, 1, -5)                                       # плохое количество

try:                                                                   # конкретная ошибка
    warehouse.receive(999, 5)
except ItemNotFound as e:
    print(f"⚠️ {e}")

print("\n--- Ошибки: заказы ---")
try_it(warehouse.place_order, 2, {1: 500}, ExpressDelivery())     # не хватает ноутбуков
try_it(warehouse.place_order, 4, {3: 1}, ExpressDelivery())       # сахара 0 шт.
try_it(warehouse.place_order, 5, {1: 0}, ExpressDelivery())       # количество 0
try_it(warehouse.place_order, 6, {999: 1}, ExpressDelivery())     # нет такого товара
try_it(warehouse.ship_order, 999)              # нет такого заказа

try:                                           # конкретная ошибка: отмена доставленного
    warehouse.cancel_order(1)
except InvalidStatusTransition as e:
    print(f"⚠️ {e}")

try_it(warehouse.deliver_order, 3)             # доставить отменённый
try_it(warehouse.ship_order, 1)                # отправить уже доставленный

# ===== 6. Склад не испорчен ошибками =====
print("\nИтог (ноутбуков 18, мышек 99, сахара 0):")
show_stock(warehouse)
print("Категории:", warehouse.category_list())