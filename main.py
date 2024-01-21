import uvicorn
from fastapi import FastAPI

from controllers.tg_user_controller import router
from database import SessionLocal, engine
from models.tg_users import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router, prefix="/api")
if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True, workers=3)
   