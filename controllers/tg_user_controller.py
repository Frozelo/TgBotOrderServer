from fastapi import FastAPI, APIRouter, Depends

from sqlalchemy.orm import Session

from database import get_db
from dto import tg_user_dto, tg_user_category_relation_dto, categories_dto
from dto.categories_dto import TgCategory

from services import tg_user_service

router = APIRouter()


@router.post("/create-user", tags=["tg_user"])
async def create_user(data: tg_user_dto.CreateTgUser, db: Session = Depends(get_db)):
    return tg_user_service.create_user(data, db)


@router.get("/get-user-list", tags=["tg_user"])
async def get_tg_users_list(db: Session = Depends(get_db)):
    return tg_user_service.get_tg_users_list(db)


@router.post("/create-user-categories-relation", tags=["tg_user"])
async def create_user_categories_relation(data: tg_user_category_relation_dto.CreateTgUserCategoryRelation,
                                          db: Session = Depends(get_db)):
    return tg_user_service.create_user_categories_relation(data, db)


@router.get("/get-users-list-by-category/{category_id}", tags=["tg_user"])
async def get_users_list_by_relation(category_id: int, db: Session = Depends(get_db)):
    return tg_user_service.get_user_list_by_category(category_id, db)
