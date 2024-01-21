from pydantic import BaseModel


class CreateTgUserCategoryRelation(BaseModel):
    user_id: int
    category_id: int
