from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.tg_users import TgUser, TgCategory


def get_tg_user_by_tg_id(tg_id, db: Session) -> TgUser:
    user = db.query(TgUser).filter(TgUser.tg_id == tg_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_tg_users_list_by_category(category_id: int, many: bool, db: Session) -> list[TgUser]:
    if many:
        users = db.query(TgUser).filter(TgUser.categories.any(id=category_id)).all()
    else:
        users = db.query(TgUser).filter(TgUser.categories.any(id=category_id)).first()
    if not users:
        raise HTTPException(status_code=404, detail=f"No users found for category with id {category_id}")
    return users


def get_category_by_id(category_id: int, db: Session) -> TgCategory:
    category = db.query(TgCategory).filter(TgCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def delete_tg_user(tg_id: int, db: Session) -> dict:
    user = get_tg_user_by_tg_id(tg_id, db)
    try:
        db.query(TgUser).filter_by(tg_id=user.tg_id).delete()
        db.commit()
        return {"message": "User deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting relation: {str(e)}")
