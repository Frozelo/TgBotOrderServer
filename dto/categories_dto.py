from typing import Optional

from pydantic import BaseModel


class TgCategory(BaseModel):
    category_id: int
    name: Optional[str] = None

