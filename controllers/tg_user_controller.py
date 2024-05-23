from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database import get_db
from dto import tg_user_dto
from services import tg_user_service

router = APIRouter()


@router.post("/user", tags=["tg_user"])
async def create_user(data: tg_user_dto.CreateTgUser, db: Session = Depends(get_db)):
    return tg_user_service.create_user(data, db)


@router.get("/users/{tg_id}", tags=["tg_user"])
async def get_tg_user(tg_id: int, db: Session = Depends(get_db)):
    return tg_user_service.get_user(tg_id, db)


@router.get("/users", tags=["tg_user"])
async def get_tg_users_list(db: Session = Depends(get_db)):
    return tg_user_service.get_tg_users_list(db)


@router.get("/user/{tg_id}/categories", tags=["tg_user"])
async def get_category_list_for_user(tg_id: int, db: Session = Depends(get_db)):
    return tg_user_service.get_category_list_for_user(tg_id, db)


@router.post("/relation/user/{tg_id}/{category_id}", tags=["tg_user"])
async def create_user_categories_relation(tg_id: int, category_id: int,
                                          db: Session = Depends(get_db),
                                          ):
    return tg_user_service.create_user_categories_relation(tg_id, category_id, db)


# TODO EDIT THIS URL PATH
@router.get("/users/category/{category_id}", tags=["tg_user"])
async def get_users_list_by_relation(category_id: int, db: Session = Depends(get_db)):
    return tg_user_service.get_user_list_by_category(category_id, True, db)


@router.delete("/users/{tg_id}", tags=["tg_user"])
async def delete_user(tg_id: int, db: Session = Depends(get_db)):
    return tg_user_service.delete_tg_user(tg_id, db)


@router.delete("/relation/user/{tg_id}/{category_id}", tags=["tg_user"])
async def delete_tg_user_categories_relation(tg_id: int, category_id: int, db: Session = Depends(get_db)):
    return tg_user_service.delete_user_categories_relation(tg_id, category_id, db)
