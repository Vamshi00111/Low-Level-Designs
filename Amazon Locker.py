"""

Get Requirements: Discuss the requirements and make asssumptions.
Assumptions:

- There are 3 types of storage: Small, Medium, and Large.
Small packages can be put in medium and large storage. Same for the other storage.

- When the QR is scanned, the appropriate locker is opened we can put it there.

- We can empty the locker as well.

- If we want a certain product, we can check in the system and then go to the locker to get that.


Use Cases: (Functional Requirements)
System
    - Scan QR
    - Add Product(Adding a product into the system)
    - Choose Locker
    - Find Product
    - Place Item

Locker
    - Add Product
    - Remove Product
    - S/M/L Locker

Classes: # Most of the argument around this - Why this class/ why this arguments??

Product
    - ID
    - Name

Item (Why Item is will not be a subclass of Product?) Item and product are different entities 
# Item is a physical entity, Product is a logical entity
    - ID
    - Product_id
    - Size

Locker
    - ID
    - Size
    - Item
    ----------------
    - Add Item
    - Remove Item

LockerSystem:
    - Map Locker[]
    - Map Product[]
    - Map ProductList[product_id, List[Items]]
    ----------------
    - Place(Item) -> Locker
    - get(Product) -> Locker
    - AddProduct(Product)


"""
from typing import List, Dict, Optional

class Product:
    def __init__(self, product_id: str, name: str):
        self.product_id = product_id
        self.name = name

class Item:
    def __init__(self, item_id: str, product_id: str, size: str):
        self.item_id = item_id
        self.product_id = product_id
        self.size = size

class Locker:
    def __init__(self, locker_id: str, size: str):
        self.locker_id = locker_id
        self.size = size
        self.item: Optional[Item] = None  # Initially empty

    def add_item(self, item: Item) -> bool:
        if self.item is None:
            self.item = item
            return True
        return False  # Locker is already occupied

    def remove_item(self) -> Optional[Item]:
        if self.item:
            removed_item = self.item
            self.item = None
            return removed_item
        return None  # Locker is empty

class LockerSystem:
    def __init__(self):
        self.lockers: List[Locker] = []
        self.products: Dict[str, Product] = {}  # product_id -> Product
        self.product_items: Dict[str, List[Item]] = {}  # product_id -> List of Items

    def add_product(self, product: Product):
        self.products[product.product_id] = product
        self.product_items[product.product_id] = []

    def place_item(self, item: Item) -> Optional[str]:
        for locker in self.lockers:
            if locker.size in ["Large", "Medium", "Small"]:  # Can store smaller items in larger lockers
                if locker.size == item.size or (locker.size == "Medium" and item.size == "Small") or (locker.size == "Large"):
                    if locker.add_item(item):
                        self.product_items[item.product_id].append(item)
                        return locker.locker_id
        return None  # No suitable locker found

    def get_product(self, product_id: str) -> Optional[str]:
        if product_id in self.product_items and self.product_items[product_id]:
            item = self.product_items[product_id][0]  # Get first available item
            for locker in self.lockers:
                if locker.item and locker.item.item_id == item.item_id:
                    locker.remove_item()
                    self.product_items[product_id].remove(item)
                    return locker.locker_id
        return None  # Product not found

# Example Usage
locker_system = LockerSystem()
locker_system.lockers.append(Locker("L1", "Small"))
locker_system.lockers.append(Locker("L2", "Medium"))
locker_system.lockers.append(Locker("L3", "Large"))

# Add a product
product = Product("P1", "Laptop")
locker_system.add_product(product)

# Place an item
item = Item("I1", "P1", "Small")
locker_id = locker_system.place_item(item)
print(f"Item placed in locker: {locker_id}")

# Retrieve a product
retrieved_locker = locker_system.get_product("P1")
print(f"Product retrieved from locker: {retrieved_locker}")
