from functools import wraps

from fastapi import HTTPException
from models.tg_users import TgUser
from utils.object_shortcuts import get_tg_user_by_tg_id


def check_user_permissions_and_get_user(tg_id, db):
    user = get_tg_user_by_tg_id(tg_id, db)
    if not user.has_permission:
        raise HTTPException(status_code=403, detail='Forbbiden')
    return user
