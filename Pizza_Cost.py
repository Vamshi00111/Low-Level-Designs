"""
Design a program to calculate pizza cost based on size, crust type, and toppings.

Questions to ask:   
Base Pricing
Toppings & Customization
Discounts & Special Offers
Order & Checkout
Design Considerations


Builder vs Factory??
"""

from typing import List

# Constants for pricing
BASE_PRICES = {"small": 8, "medium": 10, "large": 12}  # Base price based on pizza size
CRUST_PRICES = {"regular": 0, "thin": 1, "stuffed": 2}  # Additional cost for crust type
TOPPING_PRICES = {"cheese": 2, "pepperoni": 1, "mushrooms": 1, "olives": 1}  # Topping prices
TAX_RATE = 0.08  # 8% tax

class Pizza:
    """ Represents a pizza with size, crust, and toppings. """

    def __init__(self, size: str, crust: str, toppings: List[str]):
        self.size = size
        self.crust = crust
        self.toppings = toppings

    def calculate_price(self) -> float:
        """ Calculates the total price of the pizza including base, crust, and toppings. """
        price = BASE_PRICES.get(self.size, 0) + CRUST_PRICES.get(self.crust, 0)
        price += sum(TOPPING_PRICES.get(t, 1) for t in self.toppings)  # Default $1 if topping is unknown
        return price

class PizzaBuilder:
    """ Builder class to create customizable pizzas with method chaining. """

    def __init__(self):
        self.size = "medium"  # Default size
        self.crust = "regular"  # Default crust
        self.toppings = []  # No toppings initially

    def set_size(self, size: str):
        """ Sets the pizza size. """
        self.size = size
        return self  # Returning self for method chaining

    def set_crust(self, crust: str):
        """ Sets the pizza crust type. """
        self.crust = crust
        return self

    def add_topping(self, topping: str):
        """ Adds a topping to the pizza. """
        self.toppings.append(topping)
        return self

    def build(self) -> Pizza:
        """ Returns the fully constructed Pizza object. """
        return Pizza(self.size, self.crust, self.toppings)

class Order:
    """ Represents an order containing multiple pizzas. """

    def __init__(self):
        self.pizzas = []  # List to store ordered pizzas

    def add_pizza(self, pizza: Pizza):
        """ Adds a pizza to the order. """
        self.pizzas.append(pizza)

    def calculate_total(self) -> float:
        """ Calculates the total cost of the order including tax. """
        total = sum(pizza.calculate_price() for pizza in self.pizzas)
        return round(total * (1 + TAX_RATE), 2)  # Applying 8% tax and rounding to 2 decimal places

# Example Usage
builder = PizzaBuilder()
pizza1 = builder.set_size("large").set_crust("stuffed").add_topping("cheese").add_topping("pepperoni").build()
pizza2 = builder.set_size("small").set_crust("thin").add_topping("mushrooms").build()

order = Order()
order.add_pizza(pizza1)
order.add_pizza(pizza2)

# Printing the total order price
print(f"Total Order Price: ${order.calculate_total()}")
