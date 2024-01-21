from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, declarative_base

from database import Base

user_categories_relation = Table(
    'user_categories_relation',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('tg_user.id')),
    Column('category_id', Integer, ForeignKey('tg_category.id')),
)


class TgUser(Base):
    __tablename__ = 'tg_user'
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True)
    username = Column(String)

    categories = relationship('TgCategory', secondary=user_categories_relation, back_populates='tg_user')


class TgCategory(Base):
    __tablename__ = 'tg_category'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    tg_user = relationship('TgUser', secondary=user_categories_relation, back_populates='categories')
