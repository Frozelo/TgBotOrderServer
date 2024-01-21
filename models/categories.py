# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship
#
# from database import Base
# from models.tg_users import user_categories_relation
#
#
# class TgCategory(Base):
#     __tablename__ = 'tg_category'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True)
#
#     tg_user = relationship('TgUser', secondary=user_categories_relation)
