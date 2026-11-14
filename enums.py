from enum import Enum, auto

class StockStatus(Enum):
    IN_STOCK = auto()
    OUT_OF_STOCK = auto()

class OrderStatus(Enum):
    CREATED = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()