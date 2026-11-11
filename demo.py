from warehouse import WareHouse
from models import WareHouseItem, ItemCategory

wareHouse = WareHouse()

wareHouse.create_category(ItemCategory(1, "Электроника"))

item = wareHouse.create_item(1, "Asus Rog Strix", 1, 1000)
print(item.status)          

wareHouse.receive(1, 20)


