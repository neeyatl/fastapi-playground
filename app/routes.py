import logging
from typing import Annotated

from fastapi import Query, Path, Body
from fastapi.routing import APIRouter

from .mockdb import mock_db_data, mock_users
from .schema import Category, Item, User, Offer, Image

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1")


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/items/")
async def read_items(skip: int = 0, limit: int = 5):
    return mock_db_data[skip : skip + limit]


@router.post("/items/")
async def create_item(
    item: Item,
    user: Annotated[
        User,
        Body(
            examples=[
                {
                    "username": "johndoe",
                    "full_name": "John Doe",
                },
                {
                    "username": "alice",
                },
            ]
        ),
    ],
    importance: Annotated[int, Body()],
):
    mock_db_data.append(item.model_dump())
    mock_users.append(user.model_dump())
    item_id = len(mock_db_data) - 1
    return {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance,
    }


@router.get("/items/{item_id}")
async def read_item(
    item_id: int,
    vendor: str,
    item_query: Annotated[
        list[str],
        Query(
            alias="item-query",
            deprecated=True,
        ),
    ] = ["list", "of", "strings"],
    q: Annotated[
        str | None,
        Query(
            title="Query string",
            description="Query string for the items to search "
            "in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="^[A-Za-z]+$",
        ),
    ] = None,
    short: bool = True,
):
    data = (
        mock_db_data[item_id]
        if item_id < len(mock_db_data)
        else {"message": "Item not found"}
    )
    item = {
        "item_id": item_id,
        "vendor": vendor,
        "item-query": item_query,
        **data,
    }
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": (
                    "This is an amazing item that has a long description "
                    f"that spans multiple lines as it is {item['description']}."
                )
            }
        )
    return item


@router.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            embed=True,
            examples=[
                {
                    "name": "Rainbow Shirt",
                    "description": "Looks like a rainbow",
                    "type": "clothing",
                    "price": 35.4,
                    "tax": 3.2,
                    "tags": [
                        "style",
                        "rainbow",
                        "fashion",
                    ],
                    "images": [
                        {
                            "url": "https://example.com/images/rainbow_shirt.jpg",
                            "name": "Rainbow Shirt",
                        }
                    ],
                },
                {
                    "name": "T-Shirt",
                    "type": "clothing",
                    "description": "Style: Purple, Size: Small",
                    "price": 35.4,
                },
            ],
        ),
    ],
):
    if item_id >= len(mock_db_data):
        return {"message": "Item not found"}
    mock_db_data[item_id] = item.model_dump()
    return {
        "item_id": item_id,
        "extra": {
            "total_price": item.price + (item.tax or 0.0),
        },
        **item.model_dump(),
    }


@router.get("/items/{category}/{item_id}")
async def read_category_item(
    category: Category,
    item_id: Annotated[
        int, Path(title="The ID of the item to get", ge=0, lt=1000)
    ],
    size: Annotated[
        float,
        Query(
            ge=0, lt=1, description="Size of the item in terms of centimeters"
        ),
    ],
):
    common_fields = {
        "item_id": item_id,
        "category": category,
        "size": size * 10,  # convert centimeters to meters
    }
    match category:
        case Category.animals:
            return {
                **common_fields,
                "message": (
                    "Living organisms that have the ability to move, "
                    "consume food for energy, and reproduce. They can "
                    "be found in various habitats and exhibit a wide "
                    "range of behaviors and characteristics."
                ),
            }
        case Category.vehicles:
            return {
                **common_fields,
                "message": (
                    "Machines designed for transporting people or goods "
                    "from one place to another. They come in different "
                    "forms, such as cars, trucks, airplanes, bicycles, "
                    "and boats, and are powered by various sources, "
                    "including gasoline, electricity, and human energy."
                ),
            }
        case Category.foods:
            return {
                **common_fields,
                "message": (
                    "Edible substances that provide nourishment and "
                    "sustenance for humans and other animals. Foods "
                    "can be classified into different groups based on "
                    "their nutritional content, such as fruits, "
                    "vegetables, grains, proteins, and dairy products. "
                    "They are essential for maintaining health and well-being."
                ),
            }
        case _:
            return {**common_fields, "message": "Unknown Category"}


@router.post("/offers/")
async def create_offer(offer: Offer):
    return offer


@router.post("/items/{item_id}/images/multiple/")
async def create_multiple_images(item_id: int, images: list[Image]):
    logger.info("Creating multiple images for item %s", item_id)
    return images


@router.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights
