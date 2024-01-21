from pydantic import BaseModel


class CreateTgUser(BaseModel):
    tg_id: int
    username: str
