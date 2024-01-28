from fastapi import HTTPException, Depends
from sqlalchemy.exc import IntegrityError

from dto.tg_user_category_relation_dto import CreateTgUserCategoryRelation
from models.tg_users import TgUser, user_categories_relation, TgCategory
from sqlalchemy.orm import Session
from dto import tg_user_dto


def check_user_permissions(tg_id: int, db: Session):
    user = db.query(TgUser).filter(TgUser.tg_id == tg_id).first()
    if not user or not user.has_permission:
        raise HTTPException(status_code=403, detail="You don't have permission to do this action")
    return user


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


def create_user_categories_relation(tg_id, category_id, db):
    user = check_user_permissions(tg_id, db)
    category = db.query(TgCategory).get(category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category in user.categories or user in category.tg_user:
        raise HTTPException(status_code=400, detail="Relation already exists")

    try:
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
        raise HTTPException(status_code=404, detail=f"No users found for category with id {category_id}")
    return users


def delete_user_categories_relation(tg_id: int, category_id: int, db: Session):
    tg_user = db.query(TgUser).filter_by(tg_id=tg_id).first()
    category = db.query(TgCategory).get(category_id)

    if not tg_user or not category:
        raise HTTPException(status_code=404, detail="User or category not found")

    relation = db.query(user_categories_relation).filter_by(user_id=tg_user.id, category_id=category.id).first()

    if not relation:
        raise HTTPException(status_code=404, detail="Relation not found")

    db.query(user_categories_relation).filter_by(user_id=tg_user.id, category_id=category.id).delete()
    db.commit()
    db.refresh(tg_user)

    return {"message": "User-Category relation deleted successfully"}
