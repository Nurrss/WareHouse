from models import WareHouseItem, ItemCategory

class WareHouse:
    def __init__(self) -> None:
        self.items: dict[int, WareHouseItem] = {}
        self.categories : dict[int, ItemCategory] = {}
        

    def create_item(self, item_id : int, title: str, category_id: int, price:int) -> WareHouseItem:
        category = self._get_category(category_id)   
        item = WareHouseItem(item_id, title, category, price)                                   
        self.items[item_id] = item           
        return item     


    def create_category(self, category: ItemCategory) -> None:
        self.categories[category.id] = category
        
    def receive(self, item_id: int , amount: int):
        item = self.items[item_id]
        item.quantity += amount

    def _get_category(self, category_id) -> ItemCategory:
        return self.categories[category_id]

    def _get_item(self, item_id) -> WareHouseItem:
        return self.items[item_id]

    def category_list(self) -> list[str]:
        return [category.title for category in self.categories.values()]

    def item_list(self) -> list[WareHouseItem]:
        return [item for item in self.items.values()]