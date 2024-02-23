from enum import Enum
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    type: str
    description: str
    price: float
    tax: float | None = None


class Category(str, Enum):
    animals = "animals"
    vehicles = "vehicles"
    foods = "foods"
