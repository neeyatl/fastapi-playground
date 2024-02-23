from fastapi.routing import APIRouter

from .schema import Category, mock_db_data

router = APIRouter(prefix="/api/v1")


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/items/")
async def read_item(skip: int = 0, limit: int = 5):
    return mock_db_data[skip : skip + limit]


@router.get("/items/{item_id}")
async def read_item(
    item_id: int, vendor: str, q: str | None = None, short: bool = True
):
    data = (
        mock_db_data[item_id]
        if item_id < len(mock_db_data)
        else {"message": "Item not found"}
    )
    item = {"item_id": item_id, "vendor": vendor, **data}
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


@router.get("/items/{category}/{item_id}")
async def read_item(category: Category, item_id: int):
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
