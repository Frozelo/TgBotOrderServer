from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from dto.tg_user_category_relation_dto import CreateTgUserCategoryRelation
from models.tg_users import TgUser, user_categories_relation, TgCategory
from sqlalchemy.orm import Session
from dto import tg_user_dto


def create_user(data: tg_user_dto.CreateTgUser, db: Session):
    user = TgUser(tg_id=data.tg_id, username=data.username)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Integrity error: user already exists")


def get_tg_users_list(db: Session):
    return db.query(TgUser).all()


def create_user_categories_relation(data: CreateTgUserCategoryRelation, db: Session):
    user = db.query(TgUser).get(data.user_id)
    category = db.query(TgCategory).get(data.category_id)

    if user is None or category is None:
        raise HTTPException(status_code=404, detail="User or category not found")

    try:
        if category in user.categories or user in category.tg_user:
            raise HTTPException(status_code=400, detail="Relation already exists")

        user.categories.append(category)
        category.tg_user.append(user)
        db.commit()
        db.refresh(user)
        db.refresh(category)

        return {"message": "User-Category relation created successfully"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Integrity error: relation already exists")


def get_user_list_by_category(category_id: int, db: Session):
    users = db.query(TgUser).filter(TgUser.categories.any(id=category_id)).all()

    if not users:
        return HTTPException(status_code=404, detail=f"No users found for category with id {category_id}")
    return users
