from fastapi import HTTPException, Depends
from sqlalchemy.exc import IntegrityError

from models.tg_users import TgUser, user_categories_relation, TgCategory
from sqlalchemy.orm import Session
from dto import tg_user_dto
from utils.object_shortcuts import get_tg_user_by_tg_id, get_tg_users_list_by_category
from utils.perm import CheckUserPermission


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


def get_user_list_by_category(category_id: int, db: Session):
    return get_tg_users_list_by_category(category_id, db)


def create_user_categories_relation(tg_id: int, category_id: int, db: Session):
    check_permission = CheckUserPermission(db)
    user = check_permission(tg_id)
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


def get_category_list_for_user(tg_id: int, db: Session):
    user = get_tg_user_by_tg_id(tg_id, db)
    categories = db.query(TgCategory).filter(TgCategory.tg_user.any(id=user.id)).all()
    return categories


def delete_user_categories_relation(tg_id: int, category_id: int, db: Session):
    user = get_tg_user_by_tg_id(tg_id, db)
    category = db.query(TgCategory).get(category_id)

    if not user or not category:
        raise HTTPException(status_code=404, detail="User or category not found")

    if category not in user.categories:
        raise HTTPException(status_code=400, detail="Relation not found")

    try:
        relation = db.query(user_categories_relation).filter_by(user_id=user.id, category_id=category_id).first()
        if not relation:
            raise HTTPException(status_code=404, detail="Relation not found")

        db.query(user_categories_relation).filter_by(user_id=user.id, category_id=category_id).delete()
        db.commit()
        db.refresh(user)
        return {"message": "User-Category relation deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error deleting relation: " + str(e))
