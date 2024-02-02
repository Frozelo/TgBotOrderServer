from functools import wraps

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.tg_users import TgUser
from utils.object_shortcuts import get_tg_user_by_tg_id


class CheckUserPermission:
    def __init__(self, db: Session):
        self.db = db

    def __call__(self, tg_id):
        user = get_tg_user_by_tg_id(tg_id, self.db)
        if not user or not user.has_permission:
            raise HTTPException(status_code=403, detail="You don't have permission to do this action")
        return user
