from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Item(BaseModel):
    title: str


language_dict = {
    "vi": "Xin Chao Viet Nam"
}


@router.get("/{language_id}")
async def helloworld(language_id: str) -> Item:
    item = Item(
        title=language_dict[language_id]
    )
    return item
