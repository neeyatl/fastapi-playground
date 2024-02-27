from enum import Enum
from pydantic import BaseModel, Field, HttpUrl, EmailStr


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    type_: str = Field(alias="type")
    description: str = Field(
        title="The description of the item", max_length=300
    )
    price: float = Field(
        gt=0, description="The price must be greater than zero"
    )
    tax: float = 0.0
    tags: set[str] = set()
    images: list[Image] = []

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Sunglasses",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                    "tags": [
                        "style",
                        "blue",
                    ],
                    "images": [
                        {
                            "url": "https://example.com/images/sunglasses.jpg",
                            "name": "Sunglasses",
                        }
                    ],
                }
            ]
        }
    }


class User(BaseModel):
    username: str
    full_name: str = ''
    email: EmailStr


class UserIn(User):
    password: str


class Offer(BaseModel):
    user: User | None = None
    description: str
    price: float
    items: list[Item]


class Category(str, Enum):
    animals = "animals"
    vehicles = "vehicles"
    foods = "foods"
