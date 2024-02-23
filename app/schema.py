from enum import Enum

mock_db_data = [
    {"name": "Apple", "type": "Fruit", "description": "Delicious"},
    {"name": "Car", "type": "Vehicle", "description": "Vroom"},
    {"name": "Book", "type": "Book", "description": "Informative"},
    {"name": "Sunglasses", "type": "Accessories", "description": "Stylish"},
    {"name": "Laptop", "type": "Portable", "description": "Powerful"},
    {"name": "Bicycle", "type": "Vehicle", "description": "Eco-friendly"},
    {"name": "Watch", "type": "Accessories", "description": "Elegant"},
    {"name": "Headphones", "type": "Accessories", "description": "Wireless"},
    {"name": "Backpack", "type": "Luggage", "description": "Spacious"},
    {"name": "Camera", "type": "Electronics", "description": "High-resolution"},
]


class Category(str, Enum):
    animals = "animals"
    vehicles = "vehicles"
    foods = "foods"
