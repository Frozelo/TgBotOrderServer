from fastapi import HTTPException

from models.tg_users import TgUser, TgCategory


def get_tg_user_by_tg_id(tg_id, db):
    user = db.query(TgUser).filter(TgUser.tg_id == tg_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_category_by_id(category_id, db):
    category = db.query(TgCategory).filter(TgCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category



