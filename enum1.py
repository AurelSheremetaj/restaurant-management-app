from enum import Enum

class Priority(Enum):
    CHEAP = "CHEAP"
    NORMAL = "NORMAL"
    EXPENSIVE = "EXPENSIVE"
    
    
class UserRole(Enum):
    ADMIN = 1
    WAITER = 2
    COOK = 3

class UserFeatures(Enum):
    RESTAURANT_MANAGER = 1
    MENU_MANAGER = 2
    MENU_ITEM_MANAGER = 3
    TABLE_MANAGER = 4
    TABLE_ORDER = 5
    ORDER_STATUS = 6
    SIGN_OUT = 7
    
class Status(Enum):
    QUEUE = 1
    IN_PROGRESS = 2
    READY = 3
    DELIVERED = 4
    PAID = 5
