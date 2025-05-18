🛒 Inventory Management System – Project Overview
This project is a console-based Inventory Management System developed in Python using advanced Object-Oriented Programming (OOP) principles. It is designed to help users manage different types of products such as Electronics, Grocery, and Clothing, along with inventory tracking, restocking, selling, and file saving/loading capabilities.

.

🎯 Project Purpose
The goal of this project is to simulate a real-world inventory system where a store owner or warehouse manager can:

Add new products by category

Sell or restock items

Automatically remove expired grocery items

View and search products by type

Calculate the total value of inventory

Save and load inventory data using files

🧱 Main Components
✅ 1. Abstract Class – Product
Acts as a blueprint for all products.

Contains private attributes: product_id, name, price, quantity.

Defines methods like:

restock() – Add stock

sell() – Reduce stock, raise an error if not enough quantity

get_total_value() – Returns total worth of a product

Abstract method __str__() – To display product details

✅ 2. Child Classes
Each product category has a dedicated class inheriting from Product:

Electronic: Includes brand and warranty_period

Grocery: Includes expiry_date and is_expired

Clothing: Includes size and material

Each class overrides the __str__() method to provide category-specific output.

✅ 3. Inventory Class
This is the core of the system. It manages all product-related operations:

add_product() – Adds a new product to the inventory

remove_product() – Deletes a product

search_by_type() – Filters products by category

list_all_products() – Displays all products

sell_product() and restock_product() – Handles quantity changes

total_inventory_value() – Calculates total stock worth

remove_expired_products() – Deletes expired grocery items

save_to_file() and load_from_file() – File operations using JSON

⚠️ Custom Exceptions
Two custom error classes are defined to improve validation:

OutOfStockError: Raised when trying to sell more than available

DuplicateProductIDError: Raised when trying to add a product with an existing ID

💻 User Interface (CLI)
The program runs in a terminal with a menu-driven interface, allowing the user to:

Add a new product by category

Sell products by ID

Restock existing products

Search or view all products

Save or load data to/from a file

Exit the program

All input is user-friendly, and clear error messages are displayed when invalid actions are taken.

🧠 Concepts Used
Abstract Classes with the abc module

Inheritance and Polymorphism

Encapsulation (private data)

Custom Exceptions

File Handling with JSON

Dynamic object reconstruction during file loading

Interactive CLI for user-friendly experience

🌟 Future Scope
This project can be extended further by:

Adding a GUI using Tkinter, Streamlit, or Flask

Adding user authentication

Storing data in a database like SQLite or PostgreSQL

Generating sales and inventory reports

