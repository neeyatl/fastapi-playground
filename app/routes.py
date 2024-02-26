import logging
from typing import Annotated

from fastapi import Query
from fastapi.routing import APIRouter

from .mockdb import mock_db_data
from .schema import Category, Item

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1")


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/items/")
async def read_items(skip: int = 0, limit: int = 5):
    return mock_db_data[skip : skip + limit]


@router.post("/items/")
async def create_item(item: Item):
    mock_db_data.append(item.model_dump())
    # item_id = len(mock_db_data) - 1
    return item


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
async def update_item(item_id: int, item: Item):
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
async def read_category_item(category: Category, item_id: int):
    common_fields = {"item_id": item_id, "category": category}
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
