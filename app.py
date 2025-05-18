from abc import ABC, abstractmethod
import json
from datetime import datetime

class OutOfStockError(Exception):
    def __init__(self, message="Itna stock available nahi hai."):
        super().__init__(message)

class DuplicateProductIDError(Exception):
    def __init__(self, message="Product ID already exist karta hai."):
        super().__init__(message)

class Product(ABC):
    def __init__(self, product_id, name, price, quantity):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__quantity = quantity

    def restock(self, amount):
        self.__quantity += amount

    def sell(self, amount):
        if amount > self.__quantity:
            raise OutOfStockError()
        self.__quantity -= amount

    def get_total_value(self):
        return self.__price * self.__quantity

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_quantity(self):
        return self.__quantity

    def get_price(self):
        return self.__price

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass

class Electronic(Product):
    def __init__(self, product_id, name, price, quantity, brand, warranty_period):
        super().__init__(product_id, name, price, quantity)
        self.__brand = brand
        self.__warranty_period = warranty_period

    def __str__(self):
        return f"[Electronic] {self.get_name()} | Brand: {self.__brand}, Warranty: {self.__warranty_period} months"

    def to_dict(self):
        return {
            "type": "Electronic",
            "product_id": self.get_product_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "quantity": self.get_quantity(),
            "brand": self.__brand,
            "warranty_period": self.__warranty_period
        }

class Grocery(Product):
    def __init__(self, product_id, name, price, quantity, expiry_date, is_expired):
        super().__init__(product_id, name, price, quantity)
        self.__expiry_date = expiry_date
        self.__is_expired = is_expired

    def __str__(self):
        return f"[Grocery] {self.get_name()} | Expiry: {self.__expiry_date}, Expired: {self.__is_expired}"

    def is_expired(self):
        return self.__is_expired

    def to_dict(self):
        return {
            "type": "Grocery",
            "product_id": self.get_product_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "quantity": self.get_quantity(),
            "expiry_date": self.__expiry_date,
            "is_expired": self.__is_expired
        }

class Clothing(Product):
    def __init__(self, product_id, name, price, quantity, size, material):
        super().__init__(product_id, name, price, quantity)
        self.__size = size
        self.__material = material

    def __str__(self):
        return f"[Clothing] {self.get_name()} | Size: {self.__size}, Material: {self.__material}"

    def to_dict(self):
        return {
            "type": "Clothing",
            "product_id": self.get_product_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "quantity": self.get_quantity(),
            "size": self.__size,
            "material": self.__material
        }

class Inventory:
    def __init__(self):
        self._products = {}

    def add_product(self, product):
        if product.get_product_id() in self._products:
            raise DuplicateProductIDError()
        self._products[product.get_product_id()] = product

    def remove_product(self, product_id):
        if product_id in self._products:
            del self._products[product_id]

    def search_by_type(self, product_type):
        return [p for p in self._products.values() if isinstance(p, product_type)]

    def list_all_products(self):
        for product in self._products.values():
            print(product)

    def sell_product(self, product_id, quantity):
        product = self._products.get(product_id)
        if product:
            product.sell(quantity)
        else:
            print("Product not found")

    def restock_product(self, product_id, quantity):
        product = self._products.get(product_id)
        if product:
            product.restock(quantity)
        else:
            print("Product not found")

    def total_inventory_value(self):
        return sum(p.get_total_value() for p in self._products.values())

    def remove_expired_products(self):
        self._products = {k: v for k, v in self._products.items() if not (isinstance(v, Grocery) and v.is_expired())}

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump([p.to_dict() for p in self._products.values()], f)

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            for item in data:
                type_ = item["type"]
                if type_ == "Electronic":
                    product = Electronic(item["product_id"], item["name"], item["price"], item["quantity"], item["brand"], item["warranty_period"])
                elif type_ == "Grocery":
                    product = Grocery(item["product_id"], item["name"], item["price"], item["quantity"], item["expiry_date"], item["is_expired"])
                elif type_ == "Clothing":
                    product = Clothing(item["product_id"], item["name"], item["price"], item["quantity"], item["size"], item["material"])
                self.add_product(product)


inventory = Inventory()

while True:
    print("\nMenu:")
    print("1. Add Product")
    print("2. Sell Product")
    print("3. Restock Product")
    print("4. View All Products")
    print("5. Save Inventory")
    print("6. Load Inventory")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        product_id = input("ID: ")
        name = input("Name: ")
        price = float(input("Price: "))
        quantity = int(input("Quantity: "))
        ptype = input("Type (Electronic/Grocery/Clothing): ")

        try:
            if ptype == "Electronic":
                brand = input("Brand: ")
                warranty = int(input("Warranty (months): "))
                product = Electronic(product_id, name, price, quantity, brand, warranty)
            elif ptype == "Grocery":
                expiry = input("Expiry Date (YYYY-MM-DD): ")
                is_expired = input("Is expired (yes/no): ").lower() == "yes"
                product = Grocery(product_id, name, price, quantity, expiry, is_expired)
            elif ptype == "Clothing":
                size = input("Size: ")
                material = input("Material: ")
                product = Clothing(product_id, name, price, quantity, size, material)
            else:
                print("Invalid product type")
                continue

            inventory.add_product(product)
            print("Product added successfully!")

        except DuplicateProductIDError as e:
            print(e)

    elif choice == "2":
        pid = input("Product ID: ")
        qty = int(input("Quantity to sell: "))
        try:
            inventory.sell_product(pid, qty)
            print("Product sold!")
        except OutOfStockError as e:
            print(e)

    elif choice == "3":
        pid = input("Product ID: ")
        qty = int(input("Quantity to restock: "))
        inventory.restock_product(pid, qty)
        print("Product restocked!")

    elif choice == "4":
        inventory.list_all_products()

    elif choice == "5":
        inventory.save_to_file("inventory.json")
        print("Inventory saved.")

    elif choice == "6":
        inventory.load_from_file("inventory.json")
        print("Inventory loaded.")

    elif choice == "7":
        break

    else:
        print("Invalid choice.")
