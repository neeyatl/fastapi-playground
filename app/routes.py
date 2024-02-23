from .schema import Category
from fastapi.routing import APIRouter

router = APIRouter(prefix='/api/v1')

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

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
                )
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
                )
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
                )
            }
        case _:
            return {
                **common_fields,
                "message": "Unknown Category"
            }
